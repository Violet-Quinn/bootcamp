import typer
from typing import Optional
from dotenv import load_dotenv
from dag_engine import DAGEngine
from pipeline import load_dag_pipeline

app = typer.Typer()
load_dotenv()

def read_lines(path: str):
    with open(path) as f:
        for line in f:
            yield line.rstrip("\n")

def write_output(lines, output_path: Optional[str]) -> None:
    if output_path:
        with open(output_path, "w") as f:
            for line in lines:
                f.write(line + "\n")
    else:
        for line in lines:
            typer.echo(line)

@app.command()
def main(
    input_path: str = typer.Option(..., "--input", "-i", help="Input file path"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    config: str = typer.Option("pipeline.yaml", "--config", "-c", help="DAG pipeline YAML config"),
    start_node: str = typer.Option(..., "--start-node", "-s", help="Start node name in DAG"),
):
    processors, routes = load_dag_pipeline(config)
    engine = DAGEngine(processors, routes)

    lines = read_lines(input_path)
    output_lines = engine.run(lines, start_node)
    write_output(output_lines, output)

if __name__ == "__main__":
    app()
