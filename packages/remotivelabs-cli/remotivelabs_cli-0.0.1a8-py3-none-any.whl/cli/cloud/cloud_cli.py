import typer

from . import recordings, brokers, configs, auth, service_accounts, projects
from . import rest_helper as rest

app = typer.Typer()


@app.command(help="List licenses for an organisation")
def licenses(
        organisation: str = typer.Option(..., help="Organisation ID", envvar='REMOTIVE_CLOUD_ORGANISATION'),
        filter: str = typer.Option("all", help="all, valid, expired")
):
    rest.handle_get(f"/api/bu/{organisation}/licenses", {'filter': filter})


#@app.command(help="Get your organisation and projects with permissions")
#def home(
#        organisation: str = typer.Option(..., help="Organisation ID", envvar='REMOTIVE_CLOUD_ORGANISATION'),
#):
#    rest.handle_get(f"/api/bu/{organisation}/me")


# @app.command(help="Get your organisation and projects with permissions")
# def home2():
#    rest.handle_get(f"/api/home")


#@app.command(help="List users in an organisation")
#def users(
#        organisation: str = typer.Option(..., help="Organisation ID", envvar='REMOTIVE_CLOUD_ORGANISATION'),
#):
#    rest.handle_get(f"/api/bu/{organisation}/users")


app.add_typer(projects.app, name="projects", help="Manage projects")
app.add_typer(auth.app, name="auth")
app.add_typer(brokers.app, name="brokers", help="Manage cloud broker lifecycle")
app.add_typer(recordings.app, name="recordings", help="Manage recordings")
app.add_typer(configs.app, name="signal-databases", help="Manage signal databases")
app.add_typer(service_accounts.app, name="service-accounts", help="Manage project service account keys")


if __name__ == "__main__":
    app()
