use pyo3::prelude::*;

#[pyfunction]
pub fn input() -> String {
    "input".to_string()
}
