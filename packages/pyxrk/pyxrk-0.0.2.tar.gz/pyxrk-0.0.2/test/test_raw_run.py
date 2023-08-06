import datetime

import pyarrow  # type: ignore
import pytest

from pyxrk import pyxrk_raw

TEST_FILE = "./test/data/test.xrk"


def test_load_run():
    pyxrk_raw.load_run(TEST_FILE)
    with pytest.raises(ValueError, match="does not exist"):
        pyxrk_raw.load_run("./non-existant-file.xrk")


def test_run_attributes() -> None:
    run = pyxrk_raw.load_run(TEST_FILE)
    assert run.lap_count == 7
    assert run.championship == ""
    assert run.track == "Watkins Glen"
    assert run.venue_type == ""
    assert run.vehicle == "Porsche 981 GT4"
    assert run.racer == "Joe Portela"
    assert run.datetime == datetime.datetime(2023, 5, 11, 16, 5, 9)


def test_channel_names() -> None:
    run = pyxrk_raw.load_run(TEST_FILE)
    assert len(run.channel_names) == 57
    assert run.channels_count == 57
    assert run.get_channel_idx("TRQ_LOSS") == 13
    assert run.get_channel_idx("OIL_TEMP") == 42
    assert run.get_channel_idx("GPS Speed") == 46
    assert run.get_channel_idx("GPS Radius") == 56
    with pytest.raises(ValueError, match="Channel not found"):
        run.get_channel_idx("foo")


def test_channel_unit() -> None:
    run = pyxrk_raw.load_run(TEST_FILE)
    assert run.get_channel_unit("OIL_TEMP") == "C"
    assert run.get_channel_unit("GPS Speed") == "m/s"
    with pytest.raises(ValueError, match="Channel not found"):
        run.get_channel_unit("foo")
    assert run.get_channel_unit_by_idx(42) == "C"
    assert run.get_channel_unit_by_idx(46) == "m/s"
    with pytest.raises(ValueError, match="Couldn't get channel unit"):
        run.get_channel_unit_by_idx(1000)


def test_channel() -> None:
    run = pyxrk_raw.load_run(TEST_FILE)
    oil_temp_channel = run.get_channel("OIL_TEMP")
    assert oil_temp_channel.name == "OIL_TEMP"
    assert oil_temp_channel.unit == "C"
    assert oil_temp_channel.frequency == 2.0
    assert oil_temp_channel.sample_count() == 2511

    gps_speed_channel = run.get_channel("GPS Speed")
    assert gps_speed_channel.name == "GPS Speed"
    assert gps_speed_channel.unit == "m/s"
    # This value is wrong. It should be 100.0, but is actually .1,
    # but the xdrk min frequency is 1.0, so we're in a pretty weird place.
    # There is some bug (likely in the dll) where the timestamps are
    # returned off by an order of magnitude when no lap is specified.
    assert gps_speed_channel.frequency == 1.0
    assert gps_speed_channel.sample_count() == 125572

    trq_loss_channel = run.get_channel("TRQ_LOSS")
    assert trq_loss_channel.name == "TRQ_LOSS"
    assert trq_loss_channel.unit == "#"
    assert trq_loss_channel.frequency == 10.0
    assert trq_loss_channel.sample_count() == 12596

    # Test syncing
    synced_oil_temp_channel = oil_temp_channel.sync_with(gps_speed_channel)
    assert synced_oil_temp_channel.frequency == 1.0
    assert synced_oil_temp_channel.sample_count() == 125572

    synced_trq_loss_channel = trq_loss_channel.sync_with(oil_temp_channel)
    assert synced_trq_loss_channel.frequency == 2.0
    assert synced_trq_loss_channel.sample_count() == 2511


def test_channel_lap() -> None:
    run = pyxrk_raw.load_run(TEST_FILE)
    oil_temp_channel = run.get_channel("OIL_TEMP", 2)
    assert oil_temp_channel.name == "OIL_TEMP"
    assert oil_temp_channel.unit == "C"
    assert oil_temp_channel.frequency == 2.0
    assert oil_temp_channel.sample_count() == 255

    gps_speed_channel = run.get_channel("GPS Speed", 2)
    assert gps_speed_channel.name == "GPS Speed"
    assert gps_speed_channel.unit == "m/s"
    assert gps_speed_channel.frequency == 100.0
    assert gps_speed_channel.sample_count() == 12758

    trq_loss_channel = run.get_channel("TRQ_LOSS", 2)
    assert trq_loss_channel.name == "TRQ_LOSS"
    assert trq_loss_channel.unit == "#"
    assert trq_loss_channel.frequency == 10.0
    assert trq_loss_channel.sample_count() == 1286

    # Test syncing
    synced_oil_temp_channel = oil_temp_channel.sync_with(gps_speed_channel)
    assert synced_oil_temp_channel.frequency == 100.0
    assert synced_oil_temp_channel.sample_count() == 12758


def test_combo_lap_channels():
    """
    Test that the total sample count is equal to the sum
    of the sample counts from each lap.
    """
    run = pyxrk_raw.load_run(TEST_FILE)
    full_oil_temp_channel = run.get_channel("OIL_TEMP")
    assert full_oil_temp_channel.sample_count() == 2511

    lap_oil_temp_sample_count = 0
    for i in range(run.lap_count):
        lap_count = run.get_channel("OIL_TEMP", i).sample_count()
        lap_oil_temp_sample_count += lap_count

    assert lap_oil_temp_sample_count == full_oil_temp_channel.sample_count()


def test_channel_to_arrow_array():
    run = pyxrk_raw.load_run(TEST_FILE)
    channel = run.get_channel("GPS Speed", 2)
    array = channel.get_samples_array()
    assert isinstance(array, pyarrow.FloatingPointArray)
