#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Felipe Savoia
#
import os

import click
from termcolor import cprint

from constants import GlobalCLI as gc
from constants import TerraformPlanCLI as tp
from constants import TerraformSettings as ts
from terraform import (
    parse_terraform_plan,
    terraform_init,
    terraform_plan,
    terraform_validate,
)
from utils import clone_repo, is_valid_cli_argument, show_app_name


@click.group
def cli() -> None:
    """The available commands for execution are listed below.
    The primary workflow commands are given first, followed by
    less common or more advanced commands."""


@click.command("plan", help=tp.CMD_HELP.value)
@click.option(
    gc.DIR_OPT.value,
    gc.DIR_SHORT_OPT.value,
    metavar=gc.METAVAR_DIR.value,
    help=gc.DIR_HELP.value,
    default=None,
)
@click.option(
    gc.GIT_OPT.value,
    gc.GIT_SHORT_OPT.value,
    metavar=gc.METAVAR_GIT.value,
    help=gc.GIT_HELP.value,
    default=None,
)
def plan(terra_dir: str, git: str) -> None:
    """Initiates and run 'terraform plan' in a friendly way."""
    if is_valid_cli_argument(terra_dir=terra_dir, git=git):
        show_app_name()
        if git:
            terra_dir = clone_repo(git) if git else terra_dir

        terraform_init(terra_dir)
        terraform_validate(terra_dir)
        terraform_plan(terra_dir)
        parse_terraform_plan(ts.CAPTURED_PLAN_OUTPUT_FILE.value)

    try:
        # TODO: only remove in the apply option
        # os.remove(f"{terra_dir}/{ts.TF_PLAN_OUTPUT_FILE.value}")
        # os.remove("temp")
        os.remove(ts.CAPTURED_PLAN_OUTPUT_FILE.value)
    except OSError as e:
        cprint(f"\n🚨 {e}", "red")
        exit(1)


cli.add_command(plan)

if __name__ == "__main__":
    cli()
