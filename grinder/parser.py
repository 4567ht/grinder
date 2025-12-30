import subprocess
import json
from pathlib import Path

def parse_crate_doc(ws, config):
    crate_dir = ws / "crate"

    if not crate_dir.exists():
        raise RuntimeError(f"Crate folder does not exist: {crate_dir}")

    crate_dir_str = str(crate_dir)

    subprocess.check_call([
        "cargo", "doc", "--no-deps",
        "--document-private-items",
        "--output-format", "json",
        "-Z", "unstable-options"
    ], cwd=crate_dir_str)

    doc_file = crate_dir / "target" / "doc" / f"{crate_dir.name}.json"
    if not doc_file.exists():
        raise RuntimeError(f"Grinder error: JSON doc not found at {doc_file}")

    data = json.loads(doc_file.read_text())
    schema = {
        "crate_name": crate_dir.name,
        "functions": [],
        "structs": [],
        "enums": [],
        "consts": []
    }

    index = data.get("index", {})

    def is_public(item):
        return item.get("visibility") == "public"

    for item in index.values():
        if not is_public(item):
            continue
        kind = item.get("kind")
        name = item.get("name")
        if kind == "function":
            args = [a["name"] for a in item.get("decl", {}).get("inputs", [])]
            schema["functions"].append({"name": name, "args": args})
        elif kind == "struct":
            fields, methods, staticmethods, classmethods = [], [], [], []
            derives = item.get("attributes", {}).get("derive", [])
            for f in item.get("fields", []):
                if is_public(f):
                    fields.append(f["name"])
            for m in item.get("impls", []):
                if m.get("kind") == "method" and is_public(m):
                    m_args = [a["name"] for a in m.get("decl", {}).get("inputs", [])]
                    if "staticmethod" in m.get("attributes", []):
                        staticmethods.append({"name": m["name"], "args": m_args})
                    elif "classmethod" in m.get("attributes", []):
                        classmethods.append({"name": m["name"], "args": m_args})
                    else:
                        methods.append({"name": m["name"], "args": m_args})
            schema["structs"].append({
                "name": name,
                "fields": fields,
                "methods": methods,
                "staticmethods": staticmethods,
                "classmethods": classmethods,
                "derives": derives
            })
        elif kind == "enum":
            variants = [v["name"] for v in item.get("variants", []) if is_public(v)]
            schema["enums"].append({"name": name, "variants": variants})
        elif kind == "const":
            schema["consts"].append({"name": name, "value": item.get("value", None)})

    return schema
