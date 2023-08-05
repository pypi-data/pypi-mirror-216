from cook.__main__ import __main__
from cook.util import working_directory
import pytest


@pytest.mark.parametrize("name, task", [
    ("hellomake", "say-hello"),
])
def test_example(name: str, task: str) -> None:
    with working_directory(f"examples/{name}"):
        __main__(["exec", task])
