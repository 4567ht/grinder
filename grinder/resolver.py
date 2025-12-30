from pathlib import Path

def resolve_source(config):
    p = Path(config.crate)
    if p.exists():
        config.crate_path_type = "local"
        return {"type": "local", "path": p.resolve()}
    config.crate_path_type = "remote"
    return {"type": "remote", "name": config.crate}
