import hashlib
import shutil
from pathlib import Path
import subprocess

def create_workspace(config, source):
    h = hashlib.sha256(str(source).encode()).hexdigest()[:12]
    base = Path.home() / ".cache" / "grinder" / "jobs" / h
    crate_dir = base / "crate"
    base.mkdir(parents=True, exist_ok=True)

    if not crate_dir.exists():
        if source["type"] == "local":
            shutil.copytree(source["path"], crate_dir)
        else:
            subprocess.check_call([
                "cargo", "download", source["name"], "--output", crate_dir
            ])
    return base
