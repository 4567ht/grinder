from typer import Typer, Argument, Option
from rich import print
from grinder.config import GrinderConfig
from grinder.resolver import resolve_source
from grinder.workspace import create_workspace
from grinder.parser import parse_crate_doc
from grinder.wrapper import generate_wrapper
from grinder.pyi import generate_pyi
from grinder.build import build_wheel

app = Typer()

@app.command()
def main(
    crate: str = Argument(...),
    module_name: str = Option(None, "--module-name"),
    no_fc: bool = Option(False, "--no-fc"),
    install: bool = Option(False, "-i", "--install"),
    out: str = Option(None, "--out"),
    features: str = Option("", "--features")
):
    config = GrinderConfig(
        crate=crate,
        module_name=module_name,
        fc=not no_fc,
        install=install,
        out=out,
        features=features
    )

    print("[bold green]🔥 Grinder starting 🔥[/bold green]")

    source = resolve_source(config)
    ws = create_workspace(config, source)
    schema = parse_crate_doc(ws, config)
    generate_wrapper(ws, config, schema)
    generate_pyi(ws, config, schema)
    build_wheel(ws, config)

    print("[bold green]✔ Grinder finished successfully![/bold green]")
    