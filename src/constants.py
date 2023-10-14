from enum import Enum


class Menu(Enum):
    WELCOME_MSG = """
=================================
=    Terrafriend Automation     =
=================================
"""
    COLOR_MSG = "green"


class TerraformSettings(Enum):
    """Terraform settings."""

    # TODO: this will be deleted in the feature to pass via command line
    TERRAFORM_DIR = "/Users/fsavoia/Dev/terra-friend/terraform-samples/"
    CAPTURED_PLAN_OUTPUT_FILE = f"{TERRAFORM_DIR}terraform_plan_output.txt"
    TF_PLAN_OUTPUT_FILE = f"{TERRAFORM_DIR}terraform_plan.tfplan"


class TerraformCommands(Enum):
    """Terraform commands to be executed."""

    VALIDATE = "terraform validate -no-color"
    INIT = "terraform init -no-color"
    PLAN = f"terraform plan -no-color -out {TerraformSettings.TF_PLAN_OUTPUT_FILE.value}"
    APPLY = f"terraform apply -no-color {TerraformSettings.TF_PLAN_OUTPUT_FILE.value}"
    DESTROY = "terraform destroy -no-color"
    OUTPUT = "terraform output -no-color"
    SHOW = "terraform show -no-color"
