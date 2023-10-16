import os

import click
from git import GitCommandError
from git.repo.base import Repo
from termcolor import cprint

from constants import Menu
from constants import UsageCLIErrors as uce


def show_app_name() -> None:
    cprint(
        Menu.STARTUP_MSG.value,
        Menu.COLOR_MSG.value,
        attrs=["bold"],
    )


def is_valid_cli_argument(terra_dir: str, git: str) -> bool:
    if not terra_dir and not git:
        raise click.UsageError(uce.MISSING_ARGS.value)
    elif terra_dir and git:
        raise click.UsageError(uce.MUTUALLY_EXCLUSIVE.value)
    return True


def clone_repo(git) -> str:
    try:
        cprint(f"🔍 Cloning git repo {git}...", "yellow")
        temp_dir = os.path.join(os.getcwd(), "temp")
        terra_dir = temp_dir
        Repo.clone_from(git, temp_dir)
    except GitCommandError as e:
        cprint(f"🚨 Git clone failed. Error: {e}")
        exit(1)
    else:
        cprint("\n✅ Git repo cloned successfully.\n")
        return terra_dir
