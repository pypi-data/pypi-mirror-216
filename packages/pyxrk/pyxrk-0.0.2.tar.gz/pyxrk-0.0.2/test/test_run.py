import pyarrow  # type: ignore

from pyxrk import Run

TEST_FILE = "./test/data/test.xrk"


def test_lap_table() -> None:
    run = Run.load(TEST_FILE)
    lap = run.get_lap(3)
    assert isinstance(lap.to_table(), pyarrow.Table)


def test_run_table() -> None:
    run = Run.load(TEST_FILE)
    assert isinstance(run.to_table(), pyarrow.Table)
