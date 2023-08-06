from mb_cli import settings
from functools import wraps

from mb_cli.cli.api import API

from rich import print
from rich.style import Style
from rich.panel import Panel
from rich.console import Console

api = API(proxy=settings.TOR_PROXY)

def version_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if settings.VERSION != (version := api.get_version()):
            print(Panel.fit(f'[red]Update the app to version: [bold italic]{version}', title='[orange1]WARNING',
                                title_align='center',
                                subtitle=f'[blue italic][link=https://pypi.org/project/mb-cli/{version}]Go to release',
                                subtitle_align='center'))
            print('\n')
        return func(*args, **kwargs)
    return wrapper
