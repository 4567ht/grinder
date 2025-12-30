from dataclasses import dataclass
from pathlib import Path

@dataclass
class GrinderConfig:
    crate: str
    module_name: str | None
    fc: bool
    install: bool
    out: str | None
    features: str
    crate_path_type: str = "local"
    out_path: Path | None = None

    def resolved_module_name(self, crate_name: str) -> str:
        return self.module_name or f"py_{crate_name}"

    def output_dir(self, crate_name: str) -> Path:
        if self.out:
            self.out_path = Path(self.out)
            return self.out_path
        self.out_path = Path.cwd() / f"py_{crate_name}"
        return self.out_path
    