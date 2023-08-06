use pyo3::prelude::*;
mod keyboard;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn minus_as_string(a: i32, b: i32) -> PyResult<String> {
    Ok((a - b).to_string())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn windows_control(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // Add your module's functions here
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(minus_as_string, m)?)?;

    // import sub modules
    register_keyboard_sub_module(py, m)?;

    Ok(())
}

fn register_keyboard_sub_module(py: Python<'_>, parent_module: &PyModule) -> PyResult<()> {
    // define childe module name
    let child_module = PyModule::new(py, "keyboard")?;

    // Add your sub module's functions here
    child_module.add_function(wrap_pyfunction!(keyboard::input, child_module)?)?;

    // add sub modules to parent module
    parent_module.add_submodule(child_module)?;

    Ok(())
}
