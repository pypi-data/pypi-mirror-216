use arrow2::{
    array::Float64Array,
    datatypes::{DataType, Field},
    ffi,
};
use pyo3::{ffi::Py_uintptr_t, prelude::*};

pub fn to_array(name: &str, data: Vec<f64>, py: Python) -> PyResult<PyObject> {
    let raw_array = Float64Array::from_vec(data);

    let schema = Box::new(ffi::export_field_to_c(&Field::new(
        name,
        DataType::Float64,
        false,
    )));
    let array = Box::new(ffi::export_array_to_c(raw_array.boxed()));

    let array_ptr: *const ffi::ArrowArray = &*array;
    let schema_ptr: *const ffi::ArrowSchema = &*schema;

    let pa = py.import("pyarrow")?;
    let array = pa.getattr("Array")?.call_method1(
        "_import_from_c",
        (array_ptr as Py_uintptr_t, schema_ptr as Py_uintptr_t),
    )?;

    Ok(array.to_object(py))
}
