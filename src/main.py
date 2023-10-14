#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Felipe Savoia
#
import os

from termcolor import cprint

from constants import Menu
from constants import TerraformSettings as ts
from terraform import (
    parse_terraform_plan,
    terraform_init,
    terraform_plan,
    terraform_validate,
)


def main():
    cprint(
        Menu.WELCOME_MSG.value,
        Menu.COLOR_MSG.value,
        attrs=["bold"],
    )

    terraform_validate()
    terraform_init()
    terraform_plan()
    parse_terraform_plan(ts.CAPTURED_PLAN_OUTPUT_FILE.value)

    try:
        os.remove(ts.TF_PLAN_OUTPUT_FILE.value)
        os.remove(ts.CAPTURED_PLAN_OUTPUT_FILE.value)
    except OSError as e:
        cprint(f"\n🚨 {e}", "red")
        exit(1)


if __name__ == "__main__":
    main()
