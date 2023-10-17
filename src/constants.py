# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Felipe Savoia
#
from enum import Enum


class Menu(Enum):
    STARTUP_MSG = """
=================================
=    Terrafriend Automation     =
=================================
"""
    COLOR_MSG = "green"


class TerraformSettings(Enum):
    """Terraform settings."""

    CAPTURED_PLAN_OUTPUT_FILE = "terraform_plan_output.txt"
    TF_PLAN_OUTPUT_FILE = "terraform_plan.tfplan"


class TerraformCommands(Enum):
    """Terraform commands to be executed."""

    VALIDATE = "terraform validate -no-color"
    INIT = "terraform init -no-color"
    PLAN = f"terraform plan -no-color -out {TerraformSettings.TF_PLAN_OUTPUT_FILE.value}"
    APPLY = f"terraform apply -no-color {TerraformSettings.TF_PLAN_OUTPUT_FILE.value}"
    # DESTROY = "terraform destroy -no-color"
    # OUTPUT = "terraform output -no-color"
    # SHOW = "terraform show -no-color"


class GlobalCLI(Enum):
    """Global CLI constants."""

    DIR_OPT = "--terra-dir"
    DIR_SHORT_OPT = "-d"
    GIT_OPT = "--git"
    GIT_SHORT_OPT = "-g"
    METAVAR_DIR = "<dir>"
    METAVAR_GIT = "<git>"
    DIR_HELP = "Full path to terraform directory. Option is mutually exclusive with --git"
    GIT_HELP = "Git repository for you terraform project. Option is mutually exclusive with --terra-dir"


class UsageCLIErrors(Enum):
    """Usage CLI errors."""

    MISSING_ARGS = "Illegal usage: you must specify at least one of the options '-d' or '-g'."
    MUTUALLY_EXCLUSIVE = (
        "Illegal usage: options '-d' and '-g' are mutually exclusive."
    )


class CmdCLI(Enum):
    """Terraform plan CLI constants."""

    START_HELP = """Initiates and run 'terraform apply' in a friendly way.
    For your comfort, the output is parsed and displayed in a nice table."""
