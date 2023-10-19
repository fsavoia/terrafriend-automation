# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Felipe Savoia
#
import os

import click
from git import GitCommandError
from git.repo.base import Repo
from termcolor import cprint

from constants import Menu
from constants import TerraformSettings as ts
from constants import UsageCLIErrors as uce
from tf_parser import TerraformParser
from tf_runner import TerraformRunner


def show_app_name() -> None:
    """
    Print the name of the application to the console.
    """
    cprint(
        Menu.STARTUP_MSG.value,
        Menu.COLOR_MSG.value,
        attrs=["bold"],
    )


def is_valid_cli_argument(terra_dir: str, git: str) -> bool:
    """
    Check if the CLI arguments are valid.

    Parameters
    ----------
    terra_dir : str
        The path to the Terraform directory.
    git : str
        The URL of the Git repository to clone the Terraform directory from.

    Returns
    -------
    bool
        True if the CLI arguments are valid, False otherwise.
    """
    if not terra_dir and not git:
        raise click.UsageError(uce.MISSING_ARGS.value)
    elif terra_dir and git:
        raise click.UsageError(uce.MUTUALLY_EXCLUSIVE.value)
    return True


def clone_repo(git) -> str:
    """
    Clone a Git repository.

    Parameters
    ----------
    git : str
        The URL of the Git repository to clone.

    Returns
    -------
    str
        The path to the cloned repository.
    """
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


def should_apply() -> bool:
    """
    Prompt the user to apply the changes.

    Returns
    -------
    bool
        True if the user wants to apply the changes, False otherwise.
    """
    while True:
        should_apply = input(
            "Do you want to apply the changes? (y/n) "
        ).lower()
        if should_apply in ("y", "yes"):
            return True
        elif should_apply in ("n", "no"):
            cprint("\n👋 See you later!", "green")
            return False
        else:
            cprint("Invalid input. Please enter 'y' or 'n'.", "red")


def run_tf_flow(
    terra_dir: str,
    terraform_runner: TerraformRunner,
    terraform_parser: TerraformParser,
) -> None:
    """
    Run the Terraform workflow.

    Parameters
    ----------
    terra_dir : str
        The path to the Terraform directory to run the workflow for.
    terraform_runner : TerraformRunner
        The TerraformRunner object to use to run the Terraform workflow.
    terraform_parser : TerraformParser
        The TerraformParser object to use to parse the Terraform plan output.
    """
    terraform_runner.terraform_init()
    terraform_runner.terraform_validate()
    terraform_runner.terraform_plan()
    terraform_parser.parse_terraform_plan()

    if should_apply():
        terraform_runner.terraform_apply()
        try:
            os.remove(f"{terra_dir}/{ts.TF_PLAN_OUTPUT_FILE.value}")
        except OSError as e:
            cprint(f"\n🚨 {e}", "red")
            exit(1)
