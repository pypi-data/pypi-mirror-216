import typer
import json
from rich.progress import Progress, SpinnerColumn, TextColumn
from . import rest_helper as rest
from rich import print
app = typer.Typer()


@app.command("list", help="Lists brokers in project")
def list(project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_get(f"/api/project/{project}/brokers")


@app.command("describe", help="Shows details about a specific broker")
def describe(name: str, project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    rest.handle_get(f"/api/project/{project}/brokers/{name}")


@app.command("remove", help="Stops and removes a broker from project")
def stop(name: str, project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT')):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Stopping broker {name}...", total=None)
        rest.handle_delete(f"/api/project/{project}/brokers/{name}")


def do_start(name: str, project: str, api_key: str, tag: str, return_response: bool = False):
    if tag == "":
        tag_to_use = None
    else:
        tag_to_use = tag

    if api_key == "":
        body = {"size": "S", 'tag': tag_to_use}
    else:
        body = {"size": "S", 'apiKey': api_key, 'tag': tag_to_use}
    return rest.handle_post(f"/api/project/{project}/brokers/{name}", body=json.dumps(body),
                            return_response=return_response)


@app.command(name="create", help="Create a broker in project")
def start(name: str,
          project: str = typer.Option(..., help="Project ID", envvar='REMOTIVE_CLOUD_PROJECT'),
          tag: str = typer.Option("", help="Optional specific tag/version"),
          silent: bool = typer.Option(False, help="Optional specific tag/version"),
          api_key: str = typer.Option("", help="Start with your own api-key")):

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Starting broker {name}...", total=None)
        do_start(name, project, api_key, tag, return_response=silent)
