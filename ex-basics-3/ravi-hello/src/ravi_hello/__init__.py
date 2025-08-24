import typer

app = typer.Typer()

@app.command()
def main(name: str = typer.Argument("world")) -> None:
    """
    Greet the user by name or 'world' by default.
    """
    typer.echo(f"Hello {name}")

if __name__ == "__main__":
    app()
