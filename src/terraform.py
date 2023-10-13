import os
import re
import subprocess

from prettytable import PrettyTable, prettytable
from termcolor import colored, cprint

# Define the paths to the Terraform files and output
terraform_dir = "/Users/fsavoia/Dev/terra-friend/terraform-samples/"
captured_plan_output_file = os.path.join(
    terraform_dir, "terraform_plan_output.txt"
)
tf_plan_output_file = f"{terraform_dir}terraform_plan.tfplan"

# using try and except, here creates terraform sintaxe check using subprocess
try:
    result = subprocess.run(
        ["terraform", "validate", "-no-color"],
        cwd=terraform_dir,
        check=True,
        capture_output=True,
    )
    cprint(
        "✅ Terraform sintaxe check completed successfully.\n",
        "green",
        attrs=["bold"],
    )
except subprocess.CalledProcessError as e:
    cprint(f"🚨 Terraform sintaxe check failed. Error: {e}", attrs=["bold"])
    cprint(e.stderr.decode(), "red")
    exit(1)

# using try and except, here creates terraform init using subprocess
try:
    result = subprocess.run(
        ["terraform", "init", "-no-color"],
        cwd=terraform_dir,
        check=True,
        capture_output=True,
    )
    cprint(
        "✅ Terraform init completed successfully.\n", "green", attrs=["bold"]
    )
except subprocess.CalledProcessError as e:
    cprint(f"🚨 Terraform init failed. Error: {e}i", attrs=["bold"])
    cprint(e.stderr.decode(), "red")
    exit(1)

# Run the Terraform plan command and save the output to a file
try:
    result = subprocess.run(
        ["terraform", "plan", "-no-color", "-out", tf_plan_output_file],
        cwd=terraform_dir,
        capture_output=True,
        check=True,
    )

    with open(captured_plan_output_file, "w") as output_file:
        output_file.write(result.stdout.decode())

    cprint(
        "✅ Terraform plan completed successfully.\n", "green", attrs=["bold"]
    )
except subprocess.CalledProcessError as e:
    cprint(f"🚨 Terraform plan failed. Error: {e}", attrs=["bold"])
    cprint(e.stderr.decode(), "red")
    exit(1)


# Parse the Terraform plan output and print the resource information
def parse_terraform_plan(captured_plan_output_file: str) -> None:
    with open(captured_plan_output_file, "r") as file:
        plan_output = file.read()

    # Extract the relevant information using regular expressions
    resource_blocks = re.findall(
        r"# (.*?) will be (created|updated|destroyed)\n([\s\S]+?)(?=#|\Z)",
        plan_output,
    )

    # Create a table to hold the resource summary information
    summary_table = PrettyTable()
    summary_table.field_names = ["Resource type", "Resource name", "Status"]
    summary_table.align["Resource type"] = "l"
    summary_table.align["Resource name"] = "l"
    summary_table.align["Status"] = "l"

    # Create a table to hold the resource detail information
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
                colored(resource_type, "green", attrs=["bold"]),
                colored(resource_name, "green", attrs=["bold"]),
                colored(f"will be {action}", "green", attrs=["bold"]),
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

    # Print the summary and detail tables
    print(summary_table)
    cprint("\n📝 Checking the resources details.\n", "yellow", attrs=["bold"])
    print(detail_table)


parse_terraform_plan(captured_plan_output_file)

# removing the plan file
os.remove(tf_plan_output_file)
# removing the captured plan output file
os.remove(captured_plan_output_file)
