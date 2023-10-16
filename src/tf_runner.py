import subprocess
from dataclasses import dataclass

from termcolor import cprint

from constants import TerraformCommands as tfc
from constants import TerraformSettings as tfs
from utils import ErrorHandler


@dataclass
class TerraformRunner:
    terraform_dir: str

    def run_command(self, command: str) -> None:
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
        """Run 'terraform validate' command."""
        self.run_command(tfc.VALIDATE.value)
        cprint("✅ Terraform syntax check completed successfully.\n")

    def terraform_init(self) -> None:
        """Run 'terraform init' command."""
        self.run_command(tfc.INIT.value)
        cprint("✅ Terraform init completed successfully.\n")

    def terraform_plan(self) -> None:
        """Run 'terraform plan' command."""
        try:
            result = subprocess.run(
                tfc.PLAN.value.split(" "),
                cwd=self.terraform_dir,
                capture_output=True,
                check=True,
            )

            with open(tfs.CAPTURED_PLAN_OUTPUT_FILE.value, "w") as output_file:
                output_file.write(result.stdout.decode())

            cprint("✅ Terraform plan completed successfully.\n")

        except subprocess.CalledProcessError as e:
            ErrorHandler.log_and_exit(
                f"Terraform plan failed: {e}", e.stderr.decode()
            )
