mod channel;
mod run;
mod utils;
use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
fn pyxrk_raw(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run::load_run, m)?)?;
    Ok(())
}
