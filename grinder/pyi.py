from pathlib import Path
import shutil

def generate_pyi(ws, config, schema):
    crate = schema["crate_name"]
    mod = config.resolved_module_name(crate)

    crate_path = ws / "crate"
    pyi = crate_path / f"{mod}.pyi"

    lines = ["from typing import Any", "from enum import Enum"]

    for f in schema.get("functions", []):
        args = ", ".join(f"{a}: Any" for a in f["args"])
        lines.append(f"def {f['name']}({args}) -> Any: ...")

    for s in schema.get("structs", []):
        lines.append(f"class {s['name']}:")
        for field in s.get("fields", []):
            lines.append(f"    {field}: Any")
        for m in s.get("methods", []):
            args = ", ".join(["self"] + m["args"])
            lines.append(f"    def {m['name']}({args}) -> Any: ...")
        for m in s.get("staticmethods", []):
            args = ", ".join(m["args"])
            lines.append(f"    @staticmethod\ndef {m['name']}({args}) -> Any: ...")
        for m in s.get("classmethods", []):
            args = ", ".join(["cls"] + m["args"])
            lines.append(f"    @classmethod\ndef {m['name']}({args}) -> Any: ...")
        if not s.get("fields") and not s.get("methods"):
            lines.append("    pass")

    for e in schema.get("enums", []):
        lines.append(f"class {e['name']}(Enum):")
        for v in e.get("variants", []):
            lines.append(f"    {v} = '{v}'")
        if not e.get("variants"):
            lines.append("    pass")

    for c in schema.get("consts", []):
        lines.append(f"{c['name']}: Any")

    pyi.write_text("\n".join(lines))

    # For remote crates, copy to CWD or --out folder
    if config.crate_path_type == "remote":
        out = config.out_path or Path.cwd()
        out.mkdir(parents=True, exist_ok=True)
        shutil.copy(pyi, out / f"{mod}.pyi")
        