from __future__ import annotations

from typing import Optional

import typer
from rich.table import Table

from slingshot.sdk.config import project_config

from ..sdk.errors import SlingshotException
from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp
from .shared import prompt_for_single_choice

app = SlingshotCLIApp()


@app.command("list", requires_auth=True)
async def list_projects(sdk: SlingshotSDK) -> None:
    """Lists all projects that the current user has access to."""
    projects = await sdk.list_projects()
    table = Table(title="Projects")
    table.add_column("Name", style="cyan")
    table.add_column("Project ID", style="cyan")
    for i, project in enumerate(projects):
        table.add_row(project.display_name, project.project_id)
    console.print(table)


@app.command("open", requires_project=True)
async def open_project(sdk: SlingshotSDK) -> None:
    """
    Opens the project in your default browser.
    """
    url = await sdk.web_path_util.project()
    console.print(f"Opening project in browser: [link={url}]{url}[/link]")
    typer.launch(url)


@app.command("use", requires_auth=True, requires_project=False, top_level=True)
async def set_tracked_project(project_id: Optional[str] = typer.Argument(None), *, sdk: SlingshotSDK) -> None:
    """
    Select which project to use for the current directory.
    """
    if project_id:
        _set_project_id(project_id)
        return
    await list_and_set_project_id(sdk)


async def list_and_set_project_id(sdk: SlingshotSDK) -> None:
    me = await sdk.me()
    if not me:
        raise SlingshotException("You must be logged in to use this command.")
    projects = me.projects
    if not projects:
        console.print("No projects found.")
        return  # Can't set a project ID if user has no projects
    choice = prompt_for_single_choice(
        f"Select the project you want to work on", [i.project_id for i in projects], skip_if_one_value=True
    )

    project_id = projects[choice].project_id
    _set_project_id(project_id)


def _set_project_id(project_id: str) -> None:
    old_project_id = project_config.project_id
    project_config.project_id = project_id
    if old_project_id != project_id:
        project_config.last_pushed_manifest = None
    console.print(f"This directory is now associated with the project: [bold]{project_id}[/bold]")
