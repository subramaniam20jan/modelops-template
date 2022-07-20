import typer

app = typer.Typer()

@app.command("echo")
def cmd_echo(
    text: str = typer.Option("test", help="What to echo?")
):
    print(f"Hello {text}")