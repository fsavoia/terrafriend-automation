# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Felipe Savoia
#
import subprocess
from dataclasses import dataclass

from termcolor import cprint

from src.constants import TerraformCommands as tfc
from src.constants import TerraformSettings as tfs


class ErrorHandler:
    @staticmethod
    def log_and_exit(error_message: str, error_details: str) -> None:
        """
        Log an error message and exit the program.

        Parameters
        ----------
        error_message : str
            The error message to log.
        error_details : str
            The details of the error to log.
        """
        cprint(f"🚨 {error_message}", attrs=["bold"])
        cprint(error_details, "red")
        exit(1)


@dataclass
class TerraformRunner:
    terraform_dir: str

    def run_command(self, command: str) -> None:
        """
        Run a Terraform command.

        Parameters
        ----------
        command : str
            The Terraform command to run.
        """
        try:
            subprocess.run(
                command.split(" "),
                cwd=self.terraform_dir,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            ErrorHandler.log_and_exit(
                f"Terraform command failed: {e}", e.stderr.decode()
            )

    def terraform_validate(self) -> None:
        """
        Run the 'terraform validate' command.
        """
        self.run_command(tfc.VALIDATE.value)
        cprint("✅ Terraform syntax check completed successfully.\n")

    def terraform_init(self) -> None:
        """
        Run the 'terraform init' command.
        """
        self.run_command(tfc.INIT.value)
        cprint("✅ Terraform init completed successfully.\n")

    def terraform_plan(self) -> None:
        """
        Run the 'terraform plan' command and capture the output.
        """
        try:
            result = subprocess.run(
                tfc.PLAN.value.split(" "),
                cwd=self.terraform_dir,
                capture_output=True,
                check=True,
            )

            with open(tfs.CAPTURED_PLAN_OUTPUT_FILE.value, "w") as output_file:
                output_file.write(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            ErrorHandler.log_and_exit(
                f"Terraform command failed: {e}", e.stderr.decode()
            )

    def terraform_apply(self) -> None:
        """Run 'terraform apply' command."""
        self.run_command(tfc.APPLY.value)
        cprint("✅ Terraform apply completed successfully.\n")
