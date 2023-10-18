# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Felipe Savoia
#
import re
from dataclasses import dataclass, field

from prettytable import PrettyTable, prettytable
from termcolor import colored, cprint


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


class TableManager:
    @staticmethod
    def create_summary_table() -> PrettyTable:
        """
        Create a summary table.

        Returns
        -------
        PrettyTable
            The summary table.
        """
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
        """
        Create a detail table.

        Returns
        -------
        PrettyTable
            The detail table.
        """
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
        """
        Add a row to the summary table.

        Parameters
        ----------
        summary_table : PrettyTable
            The summary table to add the row to.
        resource_type : str
            The type of the resource.
        resource_name : str
            The name of the resource.
        action : str
            The action to be taken on the resource.
        """
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
        """
        Add a row to the detail table.

        Parameters
        ----------
        detail_table : PrettyTable
            The detail table to add the row to.
        resource_name : str
            The name of the resource.
        attribute : str
            The attribute of the resource.
        value : str
            The value of the attribute.
        """
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
        """
        Print the summary and detail tables.

        Parameters
        ----------
        summary_table : PrettyTable
            The summary table to print.
        detail_table : PrettyTable
            The detail table to print.
        """
        print(summary_table)
        cprint("\n📝 Checking known resource details.\n")
        print(detail_table)


@dataclass
class TerraformParser:
    captured_plan_output_file: str
    table_manager: TableManager = field(default_factory=TableManager)

    def read_plan_output(self) -> str:
        """
        Read the captured Terraform plan output.

        Returns
        -------
        str
            The captured Terraform plan output.
        """
        with open(self.captured_plan_output_file, "r") as file:
            return file.read()

    def parse_resource_blocks(self, plan_output: str) -> list:
        """
        Parse the resource blocks from the Terraform plan output.

        Parameters
        ----------
        plan_output : str
            The Terraform plan output to parse.

        Returns
        -------
        list
            A list of tuples containing the resource name, action, and details.
        """
        return re.findall(
            r"# (.*?) will be (created|updated|destroyed)\n([\s\S]+?)(?=#|\Z)",
            plan_output,
        )

    def parse_terraform_plan(self) -> None:
        """
        Parse the Terraform plan output and print the summary and detail tables.
        """
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
