from cook import Controller, Manager, Task
from cook.actions import FunctionAction, ShellAction
from cook.contexts import normalize_dependencies
from cook.controller import QUERIES
from cook.util import FailedTaskError, Timer
from pathlib import Path
import pytest
import shutil
from sqlite3 import Connection
from unittest.mock import patch


def touch(task: Task) -> None:
    for target in task.targets:
        target.write_text(target.name)


@pytest.fixture
def patched_hexdigest() -> None:
    with patch("cook.util.evaluate_hexdigest", lambda path: path.name):
        yield


def test_controller_empty_task(m: Manager, conn: Connection) -> None:
    task = m.create_task("foo")
    c = Controller(m, conn)
    assert c.is_stale(task)
    assert c.resolve_stale_tasks() == {task}


def test_controller_missing_target(m: Manager, conn: Connection) -> None:
    task = m.create_task("foo", targets=["bar"])
    c = Controller(m, conn)
    assert c.is_stale(task)
    assert c.resolve_stale_tasks() == {task}


def test_controller_simple_file_deps(m: Manager, conn: Connection, patched_hexdigest: None) -> None:
    for path in ["input.txt", "output.txt"]:
        Path(path).write_text(path)
    with normalize_dependencies():
        task = m.create_task("foo", dependencies=["input.txt"], targets=["output.txt"])
    c = Controller(m, conn)

    # No entry in the database.
    assert c.is_stale(task)
    assert c.resolve_stale_tasks() == {task}

    # Up to date entry in the database.
    conn.execute(QUERIES["upsert"], {"name": "input.txt", "digest": "input.txt", "size": 9})
    c = Controller(m, conn)
    assert not c.is_stale(task)

    # Wrong file size in the database.
    conn.execute(QUERIES["upsert"], {"name": "input.txt", "digest": "input.txt", "size": 7})
    c = Controller(m, conn)
    assert c.is_stale(task)

    # Wrong digest in the database.
    conn.execute(QUERIES["upsert"], {"name": "input.txt", "digest": "-", "size": 9})
    c = Controller(m, conn)
    assert c.is_stale(task)


def test_controller(m: Manager, conn: Connection, patched_hexdigest: None) -> None:
    for filename in ["input1.txt", "input2.txt", "intermediate.txt", "output1.txt"]:
        Path(filename).write_text(filename)

    with normalize_dependencies():
        intermediate = m.create_task("intermediate", dependencies=["input1.txt", "input2.txt"],
                                     targets=["intermediate.txt"], action=FunctionAction(touch))
        output1 = m.create_task("output1", dependencies=["intermediate.txt"],
                                targets=["output1.txt"], action=FunctionAction(touch))
        output2 = m.create_task("output2", targets=["output2.txt"], action=FunctionAction(touch),
                                dependencies=["intermediate.txt", "input2.txt", "output1.txt"])
        special = m.create_task("special", dependencies=["intermediate.txt"])

    # Make sure that the first output is not itself stale.
    conn.executemany(QUERIES["upsert"], [
        {"name": "intermediate.txt", "digest": "intermediate.txt", "size": 16},
    ])
    c = Controller(m, conn)
    assert not c.is_stale(output1, recursive=False)

    # We should get back all tasks anyway because the intermediate task is out of date (its inputs
    # are not in the database).
    c = Controller(m, conn)
    assert c.resolve_stale_tasks() == {intermediate, output1, output2, special}

    # Make sure we don't get any tasks that are upstream from what we request.
    c = Controller(m, conn)
    assert c.resolve_stale_tasks([output1]) == {intermediate, output1}

    # Execute tasks and check that they are no longer stale.
    c = Controller(m, conn)
    c.execute_sync(output1)
    assert not c.resolve_stale_tasks([output1])

    # But the other ones are still stale.
    c = Controller(m, conn)
    assert c.resolve_stale_tasks() == {output2, special}

    # Execute the second output. The special task without outputs never disappears.
    c = Controller(m, conn)
    c.execute_sync(output2)
    assert c.resolve_stale_tasks() == {special}


def test_target_not_created(m: Manager, conn: Connection) -> None:
    task = m.create_task("nothing", targets=["missing"])
    c = Controller(m, conn)
    with pytest.raises(FailedTaskError, match="did not create"):
        c.execute_sync(task)


def test_failing_task(m: Manager, conn: Connection) -> None:
    def raise_exception(_) -> None:
        raise RuntimeError

    task = m.create_task("nothing", action=FunctionAction(raise_exception))
    c = Controller(m, conn)
    with pytest.raises(FailedTaskError):
        c.execute_sync(task)


def test_concurrency(m: Manager, conn: Connection) -> None:
    delay = 0.2
    num_tasks = 4

    tasks = [m.create_task(str(i), action=ShellAction(f"sleep {delay} && touch {i}.txt"),
                           targets=[f"{i}.txt"]) for i in range(num_tasks)]
    task = m.create_task("result", dependencies=[task.targets[0] for task in tasks])

    c = Controller(m, conn)
    with Timer() as timer:
        c.execute_sync(task)
    assert timer.duration > num_tasks * delay

    c = Controller(m, conn, num_concurrent=num_tasks)
    with Timer() as timer:
        c.execute_sync(task)
    assert timer.duration < 2 * delay


def test_hexdigest_cache(m: Manager, conn: Connection, tmp_wd: Path) -> None:
    c = Controller(m, conn)
    shutil.copy(__file__, tmp_wd / "foo")
    with patch("cook.util.evaluate_hexdigest") as evaluate_hexdigest:
        c.evaluate_size_digest("foo")
        c.evaluate_size_digest("foo")
    evaluate_hexdigest.assert_called_once()


# TODO: add tests to verify what happens when tasks are cancelled, e.g., by `KeyboardInterrupt`.
