import os
import random
from typing import Annotated

import pandas as pd
import typer
from rich.console import Console
from rich.filesize import decimal as filesize_decimal
from rich.progress import Progress, SpinnerColumn, TextColumn, open
from rich.status import Status
from rich.table import Table

app = typer.Typer(add_completion=False)
console = Console()

input_help = "Path to the input CSV file."
pctg_help = "Percentage of data to sample. The value should be between 0.0 and 1.0."


@app.command()
def sample_csv(
    input_path: Annotated[str, typer.Argument(help=input_help)],
    percentage: Annotated[float, typer.Argument(help=pctg_help)] = 0.1,
):
    """
    A minimal CLI tool for sampling data from large CSV files.
    """
    console = Console()

    # Check if the input file exists
    if not os.path.exists(input_path):
        raise typer.BadParameter(f"The file {input_path} does not exist.")

    # Autogenerate output path
    file_name = os.path.basename(input_path)
    name, ext = os.path.splitext(file_name)
    percentage_str = f"{percentage*100:.2g}"
    sampled_file_name = f"{name}_sampled_{percentage_str}{ext}"
    output_path = os.path.join(os.path.dirname(input_path), sampled_file_name)

    console.print(
        f"\nSampling [yellow]{percentage_str}%[/yellow] of rows into [magenta]{output_path}[/magenta]\n"
    )

    # Count the number of lines in the input file
    with open(input_path, "rb", description="") as f:
        num_lines = sum(1 for _ in f)

    # Sample the lines
    console.print()
    with Status("Sampling", console=console):
        skip = int(num_lines * (1 - percentage))
        skip_ids = sorted(random.sample(range(1, num_lines + 1), skip))  # 0-indexed
        df = pd.read_csv(input_path, skiprows=skip_ids)

    # Save to a new file
    if os.path.exists(output_path):
        typer.confirm(
            f"The file {output_path} already exists.\nDo you want to overwrite it?",
            abort=True,
            default=True,
        )
        console.print()

    with Status("Writing to new file", console=console):
        df.to_csv(output_path, index=False)

    # Print the summary in a nice table
    table = Table(title="")

    table.add_column("Original")
    table.add_column("Sampled")

    table.add_row(input_path, output_path, style="magenta")
    table.add_row(
        filesize_decimal(os.path.getsize(input_path)),
        filesize_decimal(os.path.getsize(output_path)),
        style="green",
    )
    table.add_row(
        f"{num_lines} rows",
        f"{df.shape[0]} rows",
        style="yellow",
    )

    console.print(table, end="\n\n")
