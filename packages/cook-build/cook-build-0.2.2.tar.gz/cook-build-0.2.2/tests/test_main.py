from cook.__main__ import __main__, Formatter
import logging
from pathlib import Path
import pytest
import shutil
from typing import List


RECIPES = Path(__file__).parent / "recipes"


def test_blah_recipe_run(tmp_wd: Path) -> None:
    __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "run"])


@pytest.mark.parametrize("patterns, expected", [
    ([], ["create_source", "compile", "link", "run"]),
    (["c*"], ["create_source", "compile"]),
    (["--re", r"^\w{3}\w?$"], ["link", "run"]),
    (["run"], ["run"]),
])
def test_blah_recipe_ls(patterns: str, expected: List[str], capsys: pytest.CaptureFixture) -> None:
    __main__(["--recipe", str(RECIPES / "blah.py"), "ls", *patterns])
    out, _ = capsys.readouterr()
    for task in expected:
        assert f"<task `{task}` @ " in out


def test_blah_recipe_info() -> None:
    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "link"])


def test_blah_recipe_reset() -> None:
    __main__(["--recipe", str(RECIPES / "blah.py"), "reset", "link"])


def test_simple_dag_run(tmp_wd: Path) -> None:
    __main__(["--recipe", str(RECIPES / "simple_dag.py"), "exec", "3-1"])


@pytest.mark.parametrize("patterns", [
    ["foo"],
    ["foo", "bar"],
    ["foo", "bar", "baz"],
])
def test_simple_dag_no_matching_tasks(caplog: pytest.LogCaptureFixture, patterns: List[str]) \
        -> None:
    with pytest.raises(SystemExit), caplog.at_level("WARNING"):
        __main__(["--recipe", str(RECIPES / "simple_dag.py"), "ls", *patterns])
    assert "found no tasks matching" in caplog.text


def test_module_import(tmp_wd: Path) -> None:
    recipe = tmp_wd / "my_recipe.py"
    shutil.copy(RECIPES / "simple_dag.py", recipe)
    __main__(["-m", "my_recipe", "ls"])


def test_bad_recipe(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit), caplog.at_level("ERROR"):
        __main__(["--recipe", str(RECIPES / "bad.py"), "exec", "false"])
    assert "failed to execute" in caplog.text


def test_custom_formatter() -> None:
    formatter = Formatter()
    record = logging.LogRecord("a", logging.ERROR, "b", 2, "foo", None, None)
    assert isinstance(formatter.format(record), str)
