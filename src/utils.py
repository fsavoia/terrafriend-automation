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


def should_apply() -> bool:
    should_apply = input("Do you want to apply the changes? (y/n) ").lower()
    while True:
        if should_apply == "y" or should_apply == "yes":
            return True
        elif should_apply == "n" or should_apply == "no":
            cprint("\n👋 See you later!", "green")
            return False
        else:
            should_apply = input(
                "Do you want to apply the changes? (y/n) "
            ).lower()


def run_tf_flow(terra_dir: str) -> None:
    terraform_runner = TerraformRunner(terra_dir)
    terraform_parser = TerraformParser(ts.CAPTURED_PLAN_OUTPUT_FILE.value)
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
