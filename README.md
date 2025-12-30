# Grinder 🔥

Grinder is the Great Rust Binder, a CLI tool to automatically generate PyO3 bindings for any Rust crate, local or online, fully automated with .pyi type hints and wheel generation.


---

Features

Automatically binds all functions, structs, enums, constants recursively from a crate.

Supports local crates and crates.io crates.

Generates .pyi for full Python type hints in the same folder.

Builds Python wheels (.whl) and optionally installs them.

Default module name prefixed with py_, customizable with --module-name.

Forward-compatibility enabled by default (-fc), optional.

Fully automated: no manual wrapper coding required.

Supports custom output folders for generated wheels.



---

Installation

1. Install Grinder wheel (after building with Hatch):



.\build.ps1

2. Install cargo-download for online crates:



cargo install cargo-download


---

Usage

Basic local crate

grinder path/to/local/crate

Generates py_<crate_name>/ folder with wheel.

Generates <crate_name>.pyi in the crate root.


Online crate

grinder regex -i

Downloads regex crate from crates.io.

Generates PyO3 wrapper, .pyi file, wheel.

-i flag automatically installs the wheel.


Options

Option	Description

-i	Auto-install the generated wheel
--module-name <name>	Override default py_ module name
-fc	Enable forward compatibility (default)
--out <path>	Specify output folder for wheel
<crate>	Local path or crate name


Examples

# Local crate, default settings
grinder ./my_crate

# Online crate with auto-install
grinder regex -i

# Override module name
grinder regex --module-name my_regex

# Specify custom output folder
grinder regex --out C:\Users\Soumalya\Desktop\py_crates


---

Python Usage

import py_regex  # Or custom module name

r = py_regex.Regex("[0-9]+")
print(r.is_match("1234"))  # True

# Full autocompletion works thanks to .pyi file

.pyi ensures IDEs see all functions, structs, and classes.

Wheel is Python-importable immediately.



---

Notes

.pyi is always generated in crate root (local) or copied to CWD (online).

Forward-compatibility ABI is enabled by default.

Works with Python 3.9+ and Rust 1.80+.

Recommended to use Hatch for building Grinder itself.



---

Building Grinder (PowerShell)

.uild.ps1

Builds with Hatch, generates wheel, and installs it automatically.



---

References

PyO3 Guide

Maturin

Cargo Commands

Hatch Documentation
