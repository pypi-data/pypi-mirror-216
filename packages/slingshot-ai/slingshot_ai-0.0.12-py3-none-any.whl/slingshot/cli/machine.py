from __future__ import annotations

from rich.table import Table

from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp

app = SlingshotCLIApp()


@app.command(name="machines")
async def list_machines(sdk: SlingshotSDK) -> None:
    """Lists all machines available to the user in a table format."""
    all_machine_types = await sdk.list_machine_types()
    table = Table(title=f"Machine Types")
    table.add_column("Machine Type", style="cyan")
    table.add_column("Number of GPUs", style="cyan")
    table.add_column("GPU VRAM", style="cyan")
    table.add_column("CPU", style="cyan")
    table.add_column("RAM", style="cyan")

    # TODO: show price per hour
    for machine_type in all_machine_types:
        name = machine_type.name
        details = machine_type.details
        for gpu_count_machine_size in details.gpu_count_machine_sizes:
            gpu_vram = str(details.vram_gb) + "GB" if details.vram_gb else "-"
            gpu_count = str(gpu_count_machine_size.specs.gpu_limit)
            cpu = gpu_count_machine_size.specs.cpu_limit + " cores"
            ram = gpu_count_machine_size.specs.memory_limit.replace("Gi", "GB")
            table.add_row(name, gpu_count, gpu_vram, cpu, ram)
    console.print(table)
    console.print(
        "💡 To specify a machine type in your [yellow]slingshot.yaml[/yellow], "
        "set the [cyan]machine_type[/cyan] field to the value of the 'Machine Type' column, "
        "and the [cyan]num_gpu[/cyan] field to the number of GPUs you want to use (defaults to 0).\n"
    )
