use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn init(filepath:&str)  {
    echo_log::init(filepath);
}
#[pyfunction]
fn echo(msg:&str) {
    if let Ok(_)=echo_log::echo(msg){}
}

/// A Python module implemented in Rust.
#[pymodule]
fn echo_logrs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(echo, m)?)?;
    m.add_function(wrap_pyfunction!(init, m)?)?;
    Ok(())
}