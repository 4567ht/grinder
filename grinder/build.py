import subprocess
import os
from pathlib import Path

def build_wheel(ws, config):
    env = os.environ.copy()
    env["PYO3_USE_ABI3_FORWARD_COMPATIBILITY"] = "1" if config.fc else "0"

    subprocess.check_call(
        ["maturin", "build", "--release"],
        cwd=ws / "wrapper",
        env=env
    )

    wheel_dir = ws / "wrapper" / "target" / "wheel"
    if not wheel_dir.exists():
        raise RuntimeError("Grinder error: wheel directory not found")

    crate_name = ws.name
    out = config.output_dir(crate_name)
    out.mkdir(parents=True, exist_ok=True)

    for f in wheel_dir.glob("*.whl"):
        f.replace(out / f.name)

    for pyi in (ws / "crate").glob("*.pyi"):
        pyi.replace(out / pyi.name)

    if config.install:
        for w in out.glob("*.whl"):
            subprocess.check_call(["pip", "install", "--force-reinstall", str(w)])
            