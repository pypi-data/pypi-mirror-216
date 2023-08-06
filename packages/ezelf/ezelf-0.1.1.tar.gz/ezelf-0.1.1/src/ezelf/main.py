import warnings

warnings.filterwarnings("ignore")


import logging
import os
from pathlib import Path
from typing import List, Optional

import typer
from typing_extensions import Annotated

import ezelf

from .sync import ezpie

log_dir = os.path.join(str(Path.home()), ".ezelf/log")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# FORMAT = "%(asctime)s [%(pathname)s:%(lineno)d] %(levelname)s %(message)s"
FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(
    filename=os.path.join(log_dir, "ezelf.log"), format=FORMAT, level=logging.INFO
)


app = typer.Typer()


@app.callback()
def callback():
    """
    Ez-elf is a convenient script for ezpie, which provides:

    - package code and save to ezpie.
    """


@app.command()
def version():
    """
    Show the version of ezelf.
    """
    typer.echo(ezelf.__version__)


@app.command()
def save_my_dir(src: str = None, dest: str = None, include_hidden: bool = False):
    """
    Pack the contents of given directory and save it to ezpie.
    """
    ezpie.copy_dir(src, dest, include_hidden)


@app.command()
def save_files(
    file: Annotated[Optional[List[str]], typer.Option()] = None, dest: str = None
):
    """
    Pack a list of files and save it to ezpie, relative paths are reserved.
    """
    if not file:
        print("Please specify at least one file.")
        raise typer.Abort()
    ezpie.copy_files(file, dest)
