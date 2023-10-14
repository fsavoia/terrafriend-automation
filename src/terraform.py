import re
import subprocess

from prettytable import PrettyTable, prettytable
from termcolor import colored, cprint

from constants import TerraformCommands as tf
from constants import TerraformSettings as ts


def terraform_validate() -> subprocess.CompletedProcess:
    """Run terraform validate command."""
    try:
        result = subprocess.run(
            ["terraform", "validate", "-no-color"],
            cwd=ts.TERRAFORM_DIR.value,
            check=True,
            capture_output=True,
        )
        cprint("✅ Terraform syntax check completed successfully.\n")
        return result
    except subprocess.CalledProcessError as e:
        cprint(f"🚨 Terraform syntax check failed. Error: {e}", attrs=["bold"])
        cprint(e.stderr.decode(), "red")
        exit(1)


def terraform_init() -> subprocess.CompletedProcess[bytes]:
    """Run terraform init command."""
    try:
        result = subprocess.run(
            tf.INIT.value.split(" "),
            cwd=ts.TERRAFORM_DIR.value,
            check=True,
            capture_output=True,
        )
        cprint("✅ Terraform init completed successfully.\n")
        return result
    except subprocess.CalledProcessError as e:
        cprint(f"🚨 Terraform init failed. Error: {e}i", attrs=["bold"])
        cprint(e.stderr.decode(), "red")
        exit(1)


def terraform_plan() -> subprocess.CompletedProcess[bytes]:
    """Run terraform plan command."""
    try:
        result = subprocess.run(
            tf.PLAN.value.split(" "),
            cwd=ts.TERRAFORM_DIR.value,
            capture_output=True,
            check=True,
        )

        with open(ts.CAPTURED_PLAN_OUTPUT_FILE.value, "w") as output_file:
            output_file.write(result.stdout.decode())

        cprint("✅ Terraform plan completed successfully.\n")
        return result
    except subprocess.CalledProcessError as e:
        cprint(f"🚨 Terraform plan failed. Error: {e}", attrs=["bold"])
        cprint(e.stderr.decode(), "red")
        exit(1)


def create_summary_table() -> PrettyTable:
    """Create a summary table for the terraform plan output."""
    summary_table = PrettyTable()
    summary_table.field_names = ["Resource type", "Resource name", "Status"]
    summary_table.align["Resource type"] = "l"
    summary_table.align["Resource name"] = "l"
    summary_table.align["Status"] = "l"
    return summary_table


def create_detail_table() -> PrettyTable:
    """Create a detail table for the terraform plan output."""
    detail_table = PrettyTable()
    detail_table.field_names = ["Resource name", "Attribute", "Value"]
    detail_table.align["Resource name"] = "l"
    detail_table.align["Attribute"] = "l"
    detail_table.align["Value"] = "l"
    detail_table.hrules = prettytable.ALL
    return detail_table


def parse_terraform_plan(captured_plan_output_file: str) -> None:
    """Parse the terraform plan output and print a summary and detail table."""
    with open(captured_plan_output_file, "r") as file:
        plan_output = file.read()

    resource_blocks = re.findall(
        r"# (.*?) will be (created|updated|destroyed)\n([\s\S]+?)(?=#|\Z)",
        plan_output,
    )

    summary_table = create_summary_table()
    detail_table = create_detail_table()

    for resource_name, action, resource_details in resource_blocks:
        resource_type, _, resource_name = resource_name.partition(".")

        summary_table.add_row(
            [
                colored(resource_type, "green"),
                colored(resource_name, "green"),
                colored(f"will be {action}", "green"),
            ]
        )

        resource_attributes = re.findall(
            r"(\w+)\s+=\s+(.*)\n", resource_details
        )

        for attribute, value in resource_attributes:
            if value != "(known after apply)":
                colored_resource_name = colored(resource_name, "yellow")
                colored_attribute = colored(attribute, "yellow")
                colored_value = colored(value, "yellow")
                detail_table.add_row(
                    [colored_resource_name, colored_attribute, colored_value]
                )

    print(summary_table)
    cprint("\n📝 Checking known resource details.\n")
    print(detail_table)
