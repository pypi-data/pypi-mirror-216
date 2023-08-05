from cook.actions import CompositeAction, FunctionAction, ShellAction, SubprocessAction
from pathlib import Path
import pytest
from subprocess import SubprocessError


def test_shell_action(tmp_wd: Path) -> None:
    action = ShellAction("echo hello > world.txt")
    action.execute_sync(None)
    assert (tmp_wd / "world.txt").read_text().strip() == "hello"


def test_subprocess_action(tmp_wd: Path) -> None:
    action = SubprocessAction("touch", "foo")
    action.execute_sync(None)
    assert (tmp_wd / "foo").is_file()


def test_bad_subprocess_action() -> None:
    action = SubprocessAction("false")
    with pytest.raises(SubprocessError):
        action.execute_sync(None)


def test_function_action() -> None:
    args = []

    action = FunctionAction(args.append)
    action.execute_sync(42)

    assert args == [42]


def test_async_function_action() -> None:
    args = []

    async def func(*x) -> None:
        args.append(*x)

    action = FunctionAction(func)
    action.execute_sync(17)

    assert args == [17]


def test_composite_action() -> None:
    args = []

    action = CompositeAction(FunctionAction(args.append), FunctionAction(args.append))
    action.execute_sync("hello")
    assert args == ["hello", "hello"]
