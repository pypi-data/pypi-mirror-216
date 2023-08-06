from __future__ import annotations

from typing import Dict, Optional

import pyarrow  # type: ignore

from pyxrk import pyxrk_raw

DEFAULT_SYNC_CHANNEL = "GPS Speed"


class Lap:
    def __init__(self, lap_num: int, run: pyxrk_raw.Run, sync_channel: str):
        self.lap_num = lap_num
        self.lap_idx = lap_num - 1
        self._run = run
        self.sync_channel = sync_channel
        # TODO add lap_info stuff here

    def to_table(self) -> pyarrow.Table:
        # This is the channel that we'll sync everything else to
        sync_channel = self._run.get_channel(self.sync_channel, self.lap_idx)
        # Initialize the columns with a Time column
        columns: Dict[str, pyarrow.Array] = {
            "Time": sync_channel.get_timestamps_array()
        }
        units: Dict[str, str] = {"Time": "s"}
        for channel_name in self._run.channel_names:
            try:
                base_channel = self._run.get_channel(channel_name, self.lap_idx)
                synced_channel = base_channel.sync_with(sync_channel)
                columns[channel_name] = synced_channel.get_samples_array()
                units[channel_name] = synced_channel.unit
            # TODO: Make this error more specific, we're ignoring empty channels
            except ValueError:
                continue

        return pyarrow.Table.from_pydict(columns, metadata=units)


class Run:
    def __init__(self, raw_run: pyxrk_raw.Run, sync_channel: Optional[str] = None):
        self._run = raw_run

        self.racer = self._run.racer
        self.vehicle = self._run.vehicle
        self.datetime = self._run.datetime

        self.track = self._run.track
        self.championship = self._run.championship
        self.venue_type = self._run.venue_type

        self.lap_count = self._run.lap_count
        self.channel_names = self._run.channel_names
        self.channels_count = self._run.channels_count
        self.sync_channel = sync_channel or DEFAULT_SYNC_CHANNEL

    @classmethod
    def load(cls, filepath: str, sync_channel: Optional[str] = None) -> "Run":
        return cls(raw_run=pyxrk_raw.load_run(filepath), sync_channel=sync_channel)

    def to_table(self) -> pyarrow.Table:
        lap_tables = []
        for lap_num in range(1, self.lap_count + 1):
            lap_table = self.get_lap(lap_num).to_table()
            # Add lap number column to first position
            lap_table = lap_table.add_column(
                0, "Lap", pyarrow.array([lap_num] * len(lap_table), pyarrow.int16())
            )
            lap_tables.append(lap_table)
        return pyarrow.concat_tables(lap_tables)

    def get_lap(self, lap_num: int) -> Lap:
        return Lap(lap_num, self._run, self.sync_channel)
