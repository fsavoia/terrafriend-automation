import os
import re
import subprocess
import sys

from prettytable import PrettyTable, prettytable
from termcolor import colored, cprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from constants import TerraformCommands as tf
from constants import TerraformSettings as ts

try:
    result = subprocess.run(
        tf.VALIDATE.value.split(" "),
        cwd=ts.TERRAFORM_DIR.value,
        check=True,
        capture_output=True,
    )
    cprint("✅ Terraform syntax check completed successfully.\n")
except subprocess.CalledProcessError as e:
    cprint(f"🚨 Terraform syntax check failed. Error: {e}", attrs=["bold"])
    cprint(e.stderr.decode(), "red")
    exit(1)

try:
    result = subprocess.run(
        tf.INIT.value.split(" "),
        cwd=ts.TERRAFORM_DIR.value,
        check=True,
        capture_output=True,
    )
    cprint("✅ Terraform init completed successfully.\n")
except subprocess.CalledProcessError as e:
    cprint(f"🚨 Terraform init failed. Error: {e}i", attrs=["bold"])
    cprint(e.stderr.decode(), "red")
    exit(1)

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
except subprocess.CalledProcessError as e:
    cprint(f"🚨 Terraform plan failed. Error: {e}", attrs=["bold"])
    cprint(e.stderr.decode(), "red")
    exit(1)


def parse_terraform_plan(captured_plan_output_file: str) -> None:
    with open(captured_plan_output_file, "r") as file:
        plan_output = file.read()

    resource_blocks = re.findall(
        r"# (.*?) will be (created|updated|destroyed)\n([\s\S]+?)(?=#|\Z)",
        plan_output,
    )

    summary_table = PrettyTable()
    summary_table.field_names = ["Resource type", "Resource name", "Status"]
    summary_table.align["Resource type"] = "l"
    summary_table.align["Resource name"] = "l"
    summary_table.align["Status"] = "l"

    detail_table = PrettyTable()
    detail_table.field_names = ["Resource name", "Attribute", "Value"]
    detail_table.align["Resource name"] = "l"
    detail_table.align["Attribute"] = "l"
    detail_table.align["Value"] = "l"
    detail_table.hrules = prettytable.ALL

    # Add each resource to the summary and detail tables
    for resource_name, action, resource_details in resource_blocks:
        # Extract the resource type and name from the resource name string
        resource_type, _, resource_name = resource_name.partition(".")

        # Add the resource summary information to the summary table
        summary_table.add_row(
            [
                colored(resource_type, "green"),
                colored(resource_name, "green"),
                colored(f"will be {action}", "green"),
            ]
        )

        # Extract the resource details using regular expressions
        resource_attributes = re.findall(
            r"(\w+)\s+=\s+(.*)\n", resource_details
        )

        # Add the resource detail information to the detail table
        for attribute, value in resource_attributes:
            if value != "(known after apply)":
                # Use the same colored format for the detail table
                colored_resource_name = colored(resource_name, "yellow")
                colored_attribute = colored(attribute, "yellow")
                colored_value = colored(value, "yellow")
                detail_table.add_row(
                    [colored_resource_name, colored_attribute, colored_value]
                )

    print(summary_table)
    cprint("\n📝 Checking known resource details.\n")
    print(detail_table)


parse_terraform_plan(ts.CAPTURED_PLAN_OUTPUT_FILE.value)

os.remove(ts.TF_PLAN_OUTPUT_FILE.value)
os.remove(ts.CAPTURED_PLAN_OUTPUT_FILE.value)
