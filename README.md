# Introduction:

Terrafriend is a Python script designed to automate and enhance the Terraform workflow. It simplifies the execution of common Terraform commands, such as initialization, validation, and planning, while providing a user-friendly output.

## Features:

### Automated Terraform Initialization:

* Automatically run terraform init to initialize the working directory. You can also indicate a git repository to your code and the application will manage everything.

### Execute Terraform Commands:

* Provide a simple interface to execute common Terraform commands like terraform apply, terraform destroy, and others.

### Environment Management:

* Support multiple environments (dev, staging, production) with separate Terraform configurations.

### Output Parsing:

* Parse and display Terraform command output in a readable format.

### Security

* Security by design. In every Terraform plan or apply command, you will see the security scan for you code and you can decide "Go" or "NoGo".

### Log and History:

* Log executed commands and maintain a history of infrastructure changes.

### Documentation:

* Generate a nice documentation of your Terraform modules

## Implementation:

### Prerequisites

Before using Terrafriend, ensure you have the following prerequisites installed:

```bash
pip install -r requirements.txt
```

### Installation

1. Clone the Terrafriend repository:

```bash
git clone https://github.com/felipesavoia/terrafriend.git
```

2. Navigate to the Terrafriend directory:

```bash
cd terrafriend
```

3. Make the script executable:

```bash
chmod +x terrafriend.py
```

### Usage

1. **start** Command

Initiates and runs the entire Terraform workflow in a user-friendly way. The output is parsed and displayed in a readable table.

Options:

* `-d, --terra-dir <dir>:` Full path to the Terraform directory.
* `-g, --git <git>:` Git repository for your Terraform project.

Example:

```bash
./terrafriend.py start -d /path/to/terraform/project
```

### Example Workflow

1. Execute the ``start`` command:

```bash
./terrafriend.py start -d /path/to/terraform/project
```

2. Terrafriend will clone the Git repository (if provided) and perform Terraform initialization, validation, and planning.
3. View the parsed output, including a summary and detailed table of Terraform plan results.
4. Optionally, proceed with applying the Terraform changes.

### Notes

* The captured Terraform plan output is stored in ``terraform_plan_output.txt``.
* Some commands in the code (e.g., ``os.remove``) are marked as TODO and may require modification based on your workflow.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/fsavoia/terrafriend-automation/blob/master/LICENSE) file for details.




