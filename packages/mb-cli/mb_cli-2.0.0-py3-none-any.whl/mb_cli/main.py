import typer

from mb_cli import settings

app = typer.Typer()

from mb_cli.cli import ex

app.add_typer(ex.app, name='exchange', help='Exchange commands.', rich_help_panel='Sub-commands')

from rich import print
from rich.style import Style

from mb_cli import version_check

@app.command('version', rich_help_panel='Utility')
@version_check
def version():
    """
    Show version of the app and exit.
    """
    print(f'Version: v{settings.VERSION}')
    print(f'[blue italic][link=https://codeberg.org/notmtth/mb-cli]Go to repo')

    typer.Exit()



