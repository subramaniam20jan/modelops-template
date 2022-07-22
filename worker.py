import typer

app = typer.Typer()

@app.command("echo")
def echo_cmd(text: str = typer.Option("test", help="What to echo?")):
    """
    Echo what you pass!
    """
    typer.echo(f"Hello {text}")

if __name__ == "__main__":
    app()