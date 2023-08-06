use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn fibonacci(n: u32) -> u32 {
    if n <= 1 {
        return n;
    }
    fibonacci(n - 1) + fibonacci(n - 2)
}

/// A Python module implemented in Rust.
#[pymodule]
fn litmus_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    Ok(())
}