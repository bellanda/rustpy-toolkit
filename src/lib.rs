use pyo3::prelude::*;

mod expressions;

/// A Python module implemented in Rust.
#[pymodule]
fn expression_lib(m: &Bound<'_, PyModule>) -> PyResult<()>
{
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
