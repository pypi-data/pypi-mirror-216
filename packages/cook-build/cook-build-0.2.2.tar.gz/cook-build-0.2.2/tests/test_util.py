from cook import util
import hashlib
from pathlib import Path


def test_evaluate_digest(tmp_wd: Path) -> None:
    fn = tmp_wd / "foo.txt"
    fn.write_text("bar")
    assert util.evaluate_hexdigest(fn) == hashlib.sha1(b"bar").hexdigest()
