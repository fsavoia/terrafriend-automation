#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Felipe Savoia
#
from termcolor import cprint

from constants import Menu


def menu_call():
    cprint(
        Menu.WELCOME_MSG.value,
        Menu.COLOR_MSG.value,
        attrs=["bold"],
    )


def main():
    menu_call()


if __name__ == "__main__":
    main()
