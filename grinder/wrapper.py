from pathlib import Path

def generate_wrapper(ws, config, schema):
    wrapper = ws / "wrapper"
    src = wrapper / "src"
    src.mkdir(parents=True, exist_ok=True)

    crate = schema["crate_name"]
    mod = config.resolved_module_name(crate)

    (wrapper / "Cargo.toml").write_text(f"""
[package]
name = "{mod}"
version = "0.1.0"

[lib]
crate-type = ["cdylib"]

[dependencies]
pyo3 = {{ version = "0.21", features = ["abi3-py38"] }}
{crate} = {{ path = "../crate" }}
""")

    lines = ["use pyo3::prelude::*;", f"use {crate}::*;", ""]

    for s in schema.get("structs", []):
        lines.append(f"#[pyclass]")
        lines.append(f"pub struct {s['name']} {{")
        for f in s.get("fields", []):
            lines.append(f"    #[pyo3(get, set)] pub {f}: Any,")
        lines.append("}")
        lines.append(f"#[pymethods]")
        lines.append(f"impl {s['name']} {{")
        if "Default" in s.get("derives", []):
            lines.append(f"    #[new] fn new() -> Self {{ Self::default() }}")
        for m in s.get("methods", []):
            args = ", ".join(["&self"] + m["args"])
            lines.append(f"    pub fn {m['name']}({args}) -> PyResult<()> {{ Ok(()) }}")
        for m in s.get("staticmethods", []):
            args = ", ".join(m["args"])
            lines.append(f"    #[staticmethod] pub fn {m['name']}({args}) -> PyResult<()> {{ Ok(()) }}")
        for m in s.get("classmethods", []):
            args = ", ".join(["_cls"] + m["args"])
            lines.append(f"    #[classmethod] pub fn {m['name']}({args}) -> PyResult<()> {{ Ok(()) }}")
        lines.append("}\n")

    for e in schema.get("enums", []):
        lines.append(f"#[pyclass]")
        lines.append(f"pub struct {e['name']} {{}}")
        lines.append(f"impl {e['name']} {{")
        for v in e.get("variants", []):
            lines.append(f'    #[classattr] pub const {v}: &str = "{v}";')
        lines.append("}\n")

    for c in schema.get("consts", []):
        lines.append(f'const {c["name"]}: Any = {c.get("value", "None")};')

    lines.append(f"#[pymodule]")
    lines.append(f"fn {mod}(_py: Python, m: &PyModule) -> PyResult<()> {{")
    for f in schema.get("functions", []):
        lines.append(f'    m.add_function(wrap_pyfunction!({f["name"]}, m)?)?;')
    for s in schema.get("structs", []):
        lines.append(f'    m.add_class::<{s["name"]}>()?;')
    for e in schema.get("enums", []):
        lines.append(f'    m.add_class::<{e["name"]}>()?;')
    for c in schema.get("consts", []):
        lines.append(f'    m.add("{c["name"]}", {c["name"]})?;')
    lines.append("    Ok(())\n}")

    (src / "lib.rs").write_text("\n".join(lines))
    