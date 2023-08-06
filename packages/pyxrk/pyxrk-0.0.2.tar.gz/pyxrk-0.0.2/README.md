# pyxrk
Python package for reading .xrk files. The `Run` class can be used to turn .xrk data files into pyarrow Tables.

---

Install pyxrk using pip:

```shell
$ pip install pyxrk
```

To load an .xrk file into a pyarrow Table:
```pycon
>>> from pyxrk import Run
>>> run = Run.load("./my_run.xrk")
>>> run.racer
'Lewis Hamilton'
>>> run.to_table()  # pyarrow.Table instance
>>> # Or for specific laps
>>> run.get_lap(1).to_table()
```
Channel unit information can be found in the arrow table metadata.

---

 The `pyxrk_raw` submodule wraps much of the functionality from the rust library [xdrk](https://github.com/bmc-labs/xdrk) while adding some convenience methods.
To use the raw submodule for reading .xrk files:

```pycon
>>> from pyxrk import pyxrk_raw
>>> run = pyxrk_raw.load_run("./my_run.xrk")
>>> run.lap_count
7
>>> run.racer
'Lewis Hamilton'
>>> channel = run.get_channel("GPS Speed")
>>> channel.unit
'm/s'
>>> channel.frequency  # in Hz
100.0
>>> for data in channel.data():
...     print(data)  # tuple of (time offset, data point)
...     break
...
(0.0, 0.1846618503332138)
```

In lieau of better API documentation, see `pyxrk_raw.pyi` for full interface and tests for more example usage.


## Compatibility

Currently known to work on Linux and Windows, but not Mac.  Contributions for getting it working on Mac are more than welcome.