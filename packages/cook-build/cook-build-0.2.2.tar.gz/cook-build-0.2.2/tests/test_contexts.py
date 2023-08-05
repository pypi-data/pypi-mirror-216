from cook import Manager, Task
from cook.actions import CompositeAction, FunctionAction, ShellAction, SubprocessAction
from cook.contexts import Context, create_target_directories, FunctionContext, create_group, \
    normalize_action, normalize_dependencies
from cook.controller import Controller
from pathlib import Path
import pytest
import sqlite3
from typing import List


def test_function_context(m: Manager) -> None:
    tasks: List[Task] = []

    def func(t: Task) -> Task:
        tasks.append(t)
        return t

    with FunctionContext(func):
        m.create_task("my-task")
    m.create_task("my-other-task")

    task, = tasks
    assert task.name == "my-task"


def test_missing_task_context(m: Manager) -> None:
    with pytest.raises(ValueError, match="did not return a task"), FunctionContext(lambda _: None):
        m.create_task("my-task")


def test_context_management(m: Manager) -> None:
    with pytest.raises(RuntimeError, match="no active contexts"), Context():
        m.contexts = []
    with pytest.raises(RuntimeError, match="unexpected context"), Context():
        m.contexts.append("something else")


def test_create_target_directories(m: Manager, tmp_wd: Path, conn: sqlite3.Connection) -> None:
    filename = tmp_wd / "this/is/a/hierarchy.txt"
    with normalize_action(), create_target_directories():
        task = m.create_task("foo", targets=[filename], action=["touch", filename])
    assert not filename.parent.is_dir()

    controller = Controller(m, conn)
    controller.execute_sync(task)
    assert filename.parent.is_dir()


def test_create_target_directories_with_multiple_targets(m: Manager, tmp_wd: Path, conn: sqlite3) \
        -> None:
    filenames = [tmp_wd / "this/is/a/hierarchy.txt", tmp_wd / "this/is/a/hierarchy2.txt"]
    with normalize_action(), create_target_directories():
        for filename in filenames:
            task = m.create_task(filename.name, targets=[filename], action=["touch", filename])
    assert not filename.parent.is_dir()

    controller = Controller(m, conn)
    controller.execute_sync(task)
    assert filename.parent.is_dir()


def test_normalize_action(m: Manager) -> None:
    with normalize_action():
        task = m.create_task("foo", action="bar")
        assert isinstance(task.action, ShellAction) and task.action.cmd == "bar"

        task = m.create_task("bar", action=["baz"])
        assert isinstance(task.action, SubprocessAction) and task.action.program == "baz"

        actions = [ShellAction("hello"), SubprocessAction("world")]
        task = m.create_task("baz", action=actions)
        assert isinstance(task.action, CompositeAction) and task.action.actions == tuple(actions)

        task = m.create_task("xyz", action=lambda x: None)
        assert isinstance(task.action, FunctionAction)


def test_group_no_tasks(m: Manager) -> None:
    with pytest.raises(RuntimeError, match="no tasks"), create_group("g"):
        pass


def test_group(m: Manager) -> None:
    with create_group("g"):
        t1 = m.create_task("t1")
        t2 = m.create_task("t2")
    assert m.tasks["g"].task_dependencies == [t1, t2]


def test_normalize_dependencies(m: Manager) -> None:
    with create_group("g") as g:
        base = m.create_task("base")
    with normalize_dependencies():
        task = m.create_task("task1", dependencies=[g])
        assert task.task_dependencies == [g.task]

        task = m.create_task("task2", dependencies=[base])
        assert task.task_dependencies == [base]

        task = m.create_task("task3", task_dependencies=["g"])
        assert task.task_dependencies == [g.task]
