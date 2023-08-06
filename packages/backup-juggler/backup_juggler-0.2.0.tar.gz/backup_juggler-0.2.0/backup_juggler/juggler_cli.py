from pathlib import Path

import toml
from rich.console import Console
from rich.panel import Panel
from typer import Context, Exit, Option, Typer
from typing_extensions import Annotated

from backup_juggler.files_manager import calculates_size, parallel_backups

app = Typer(
    help='Multiple copies of files and directories simultaneously made easy.'
)
console = Console()


def get_version():
    root_dir = Path(__file__).resolve().parents[1]
    pyproject_path = root_dir / 'pyproject.toml'
    with open(pyproject_path) as f:
        pyproject = toml.load(f)
        version = pyproject['tool']['poetry']['version']
        return version


def version_callback(value: bool):
    if value:
        version = get_version()
        version_message = f'Backup Juggler {version}'
        panel = Panel(
            version_message, title='Version', title_align='left', expand=False
        )
        console.print(panel)
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def callback(
    ctx: Context,
    version: Annotated[
        bool,
        Option(
            ...,
            '--version',
            '-v',
            callback=version_callback,
            is_eager=True,
            is_flag=True,
            help='Shows the version of the Backup Juggler.',
        ),
    ] = False,
):
    if ctx.invoked_subcommand:
        return

    ctx.get_help()


@app.command(help='Perform backups of source to destination.')
def do_backups(
    sources: Annotated[
        list[Path],
        Option(..., '--source', '-s', help='Source path(s) to be backed up.'),
    ],
    destinations: Annotated[
        list[Path],
        Option(
            ...,
            '--destination',
            '-d',
            help='Destination directory(s) for the backups.',
        ),
    ],
):
    parallel_backups(sources, destinations)


@app.command(help='Calculate the total size of the specified source.')
def get_size(
    sources: Annotated[
        list[Path],
        Option(
            ...,
            '--source',
            '-s',
            help='Source path(s) that will have their total sizes calculated.',
        ),
    ]
):
    calculates_size(sources)
