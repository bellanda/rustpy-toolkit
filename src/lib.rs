use pyo3::prelude::*;

// Módulos organizados por funcionalidade
mod cpf_cnpj;
mod phone;
mod text_utils;

/// A Python module implemented in Rust.
#[pymodule]
fn _internal(m: &Bound<'_, PyModule>) -> PyResult<()>
{
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
