# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Felipe Savoia
#
# import re
# from dataclasses import dataclass

# from prettytable import PrettyTable, prettytable
# from termcolor import colored, cprint


# @dataclass
# class TerraformParser:
#     captured_plan_output_file: str

#     def create_summary_table(self) -> PrettyTable:
#         """Create a summary table for the Terraform plan output."""
#         summary_table = PrettyTable()
#         summary_table.field_names = [
#             "Resource type",
#             "Resource name",
#             "Status",
#         ]
#         summary_table.align["Resource type"] = "l"
#         summary_table.align["Resource name"] = "l"
#         summary_table.align["Status"] = "l"
#         return summary_table

#     def create_detail_table(self) -> PrettyTable:
#         """Create a detail table for the Terraform plan output."""
#         detail_table = PrettyTable()
#         detail_table.field_names = ["Resource name", "Attribute", "Value"]
#         detail_table.align["Resource name"] = "l"
#         detail_table.align["Attribute"] = "l"
#         detail_table.align["Value"] = "l"
#         detail_table.hrules = prettytable.ALL
#         return detail_table

#     def parse_terraform_plan(self) -> None:
#         """Parse the Terraform plan output and print a summary and detail table."""
#         try:
#             with open(self.captured_plan_output_file, "r") as file:
#                 plan_output = file.read()

#             resource_blocks = re.findall(
#                 r"# (.*?) will be (created|updated|destroyed)\n([\s\S]+?)(?=#|\Z)",
#                 plan_output,
#             )

#             # resource_blocks = re.findall(
#             #     r"# (.*?) will be (created|updated|destroyed)| must be replaced\n([\s\S]+?)(?=#|\Z)",
#             #     plan_output,
#             # )

#             summary_table = self.create_summary_table()
#             detail_table = self.create_detail_table()

#             for resource_name, action, resource_details in resource_blocks:
#                 resource_type, _, resource_name = resource_name.partition(".")

#                 summary_table.add_row(
#                     [
#                         colored(resource_type, "green"),
#                         colored(resource_name, "green"),
#                         colored(f"will be {action}", "green"),
#                     ]
#                 )

#                 resource_attributes = re.findall(
#                     r"(\w+)\s+=\s+(.*)\n", resource_details
#                 )

#                 for attribute, value in resource_attributes:
#                     if value != "(known after apply)":
#                         colored_resource_name = colored(
#                             resource_name, "yellow"
#                         )
#                         colored_attribute = colored(attribute, "yellow")
#                         colored_value = colored(value, "yellow")
#                         detail_table.add_row(
#                             [
#                                 colored_resource_name,
#                                 colored_attribute,
#                                 colored_value,
#                             ]
#                         )

#             print(summary_table)
#             cprint("\n📝 Checking known resource details.\n")
#             print(detail_table)
#         except Exception as e:
#             cprint(f"🚨 Error parsing Terraform plan: {e}", attrs=["bold"])
#             cprint(str(e), "red")
#             exit(1)

import re
from dataclasses import dataclass, field

from prettytable import PrettyTable, prettytable
from termcolor import colored, cprint


class ErrorHandler:
    @staticmethod
    def log_and_exit(error_message: str, error_details: str) -> None:
        cprint(f"🚨 {error_message}", attrs=["bold"])
        cprint(error_details, "red")
        exit(1)


class TableManager:
    @staticmethod
    def create_summary_table() -> PrettyTable:
        """Create a summary table."""
        summary_table = PrettyTable()
        summary_table.field_names = [
            "Resource type",
            "Resource name",
            "Status",
        ]
        summary_table.align["Resource type"] = "l"
        summary_table.align["Resource name"] = "l"
        summary_table.align["Status"] = "l"
        return summary_table

    @staticmethod
    def create_detail_table() -> PrettyTable:
        """Create a detail table."""
        detail_table = PrettyTable()
        detail_table.field_names = ["Resource name", "Attribute", "Value"]
        detail_table.align["Resource name"] = "l"
        detail_table.align["Attribute"] = "l"
        detail_table.align["Value"] = "l"
        detail_table.hrules = prettytable.ALL
        return detail_table

    @staticmethod
    def add_summary_row(
        summary_table: PrettyTable,
        resource_type: str,
        resource_name: str,
        action: str,
    ) -> None:
        """Add a row to the summary table."""
        summary_table.add_row(
            [
                colored(resource_type, "green"),
                colored(resource_name, "green"),
                colored(f"will be {action}", "green"),
            ]
        )

    @staticmethod
    def add_detail_row(
        detail_table: PrettyTable,
        resource_name: str,
        attribute: str,
        value: str,
    ) -> None:
        """Add a row to the detail table."""
        colored_resource_name = colored(resource_name, "yellow")
        colored_attribute = colored(attribute, "yellow")
        colored_value = colored(value, "yellow")
        detail_table.add_row(
            [colored_resource_name, colored_attribute, colored_value]
        )

    @staticmethod
    def print_tables(
        summary_table: PrettyTable, detail_table: PrettyTable
    ) -> None:
        """Print the summary and detail tables."""
        print(summary_table)
        cprint("\n📝 Checking known resource details.\n")
        print(detail_table)


@dataclass
class TerraformParser:
    captured_plan_output_file: str
    table_manager: TableManager = field(default_factory=TableManager)

    def read_plan_output(self) -> str:
        """Read the Terraform plan output from the file."""
        with open(self.captured_plan_output_file, "r") as file:
            return file.read()

    def parse_resource_blocks(self, plan_output: str) -> list:
        """Parse resource blocks from the Terraform plan output."""
        return re.findall(
            r"# (.*?) will be (created|updated|destroyed)\n([\s\S]+?)(?=#|\Z)",
            plan_output,
        )

    def parse_terraform_plan(self) -> None:
        """Parse the Terraform plan output and print a summary and detail table."""
        try:
            plan_output = self.read_plan_output()
            resource_blocks = self.parse_resource_blocks(plan_output)

            summary_table = self.table_manager.create_summary_table()
            detail_table = self.table_manager.create_detail_table()

            for resource_name, action, resource_details in resource_blocks:
                resource_type, _, resource_name = resource_name.partition(".")

                self.table_manager.add_summary_row(
                    summary_table, resource_type, resource_name, action
                )

                resource_attributes = re.findall(
                    r"(\w+)\s+=\s+(.*)\n", resource_details
                )

                for attribute, value in resource_attributes:
                    if value != "(known after apply)":
                        self.table_manager.add_detail_row(
                            detail_table, resource_name, attribute, value
                        )

            self.table_manager.print_tables(summary_table, detail_table)
        except Exception as e:
            ErrorHandler.log_and_exit(
                f"Error parsing Terraform plan: {e}", str(e)
            )
