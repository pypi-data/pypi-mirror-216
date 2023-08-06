# StellaNow CLI Tool - Contributors

StellaNow CLI is a command-line interface for interacting with the StellaNow services.

## Installation
To install StellaNow CLI, you can use pip:

    pip install -e .

This command installs the CLI in editable mode, which is convenient for development purposes.

## Usage
After installation, you can use the **'stellanow'** command in your terminal to interact with StellaNow services. Here is how to use some of the available commands:

### Configure
You can use the **'configure'** command to setup the necessary credentials and configurations for a specific profile. The profile will store a particular set of configurations.

Here is how to use the command:

    stellanow configure --profile YOUR_PROFILE_NAME

If no profile is specified, the configurations will be stored under the 'DEFAULT' profile.

### Internal Environment Selection
As an internal development feature, all commands in the StellaNow CLI tool - including the **'configure'** command - come equipped with a hidden option, **'--env'**. This feature is specifically designed for our internal developers to easily designate the target API environment during their operations.

The **'--env'** option accepts one of two arguments: **'dev'** or **'int'**. These arguments enable developers to switch between the Development and Integration environments, offering a high degree of control over their interactions with the StellaNow services.

In the case of the **'configure'** command, the **'--env'** option goes a step further - the selected environment ('dev' or 'int') gets saved in the configuration file under the associated profile. This ensures the persistence of the chosen API environment across multiple sessions, relieving developers from the need to specify it each time.

As a hidden feature, **'--env'** does not appear when using the **'--help'** command. This maintains the simplicity of the help output for general users while providing a powerful, flexible tool for our developers to streamline their workflows.

### Environment Variables
The stellanow CLI can also read the following environment variables:

* **`STELLANOW_ACCESS_KEY`**: Your access key.
* **`STELLANOW_ACCESS_TOKEN`**: Your access token.


These environment variables take precedence over the settings from the command line options and your configuration file. The precedence order is: 
    
    Environment Variables -> Command Line Options -> Configuration File

### Development
StellaNow CLI is built using the Python Click library.

If you want to add a new command, follow these steps:

* Create a new Python file for your command in the **'commands'** directory.
* Define your command as a function, and decorate it with the **'@click.command()'** decorator.
* In **'cli.py'**, import your command function and add it to the main cli group using **'cli.add_command(your_command_function)'**.

Please note that StellaNow CLI follows the conventions of Python Click library.



# StellaNow CLI Tool - Users
Welcome to the StellaNow CLI tool. This tool automates the process of generating class code from StellaNow event specifications and provides a summary of changes between the generated classes and the specifications fetched from the API. It's recommended to use this tool in conjunction with the StellaNow SDK's to ensure that your application's message classes are up-to-date with the latest specifications.

## Installation
To install the StellaNow CLI tool, run the following command:

    pip install stellanow-cli

The tool is hosted on PYPI and can be installed via pip.

## Usage
After installation, you can use the 'stellanow' command in your terminal to interact with StellaNow services. Here is how to use some of the available commands:

### Configure
You can use the 'configure' command to setup the necessary credentials and configurations for a specific profile. The profile will store a particular set of configurations.

Here is how to use the command:

    stellanow configure --profile YOUR_PROFILE_NAME

If no profile is specified, the configurations will be stored under the 'DEFAULT' profile. Profile names are case-sensitive.

### Environment Variables
The stellanow CLI can also read the following environment variables:

    STELLANOW_ACCESS_KEY: Your access key.
    STELLANOW_ACCESS_TOKEN: Your access token.

### Credentials Precedence Order
In StellaNow CLI, there is a specific order of precedence for the way credentials and other settings are obtained. This means if a setting is provided in more than one place, the setting from the source with the highest precedence will be used. The order of precedence is:

    Environment Variables -> Command Line Options -> Configuration File

* **Environment Variables**: These have the highest precedence. If a setting is provided as an environment variable, it will override any value provided as a command line option or in the configuration file.
* **Command Line Options**: These have the second-highest precedence. If a setting is provided as a command line option, it will override any value provided in the configuration file.
* **Configuration File**: This has the lowest precedence. Settings in the configuration file will be used if no value for the same setting is provided as an environment variable or as a command line option.

* This order of precedence provides flexibility, allowing you to set default values in the configuration file but override them for specific operations with command line options or environment variables.

## Commands

### 'configure'
The **'configure'** command sets up the necessary credentials and configurations for a specific profile or for the DEFAULT profile if none is specified.

#### Command usage:

    stellanow configure --profile myProfile

#### Command options:

* **'--profile'**: The profile name for storing a particular set of configurations. If no profile is specified, the configurations will be stored under the 'DEFAULT' profile.

This will prompt you for the access key, access token, organization ID, and project ID for the specified profile, which in this case is 'myProfile'. If you do not specify a profile, the command will default to the 'DEFAULT' profile.

The command validates the provided values to ensure they meet the expected formats: the access key should be a valid email address or a string containing only alphanumeric characters, dashes, and underscores; the access token should be a string with no whitespace and a length of 8-64 characters; and both the organization ID and project ID should be valid UUIDs.

The command then writes these configurations to a file named 'config.ini' in the '.stellanow' directory of your home folder. If this directory or file does not exist, they will be created.

### 'events'
The **'events'** command fetches the latest event specifications from the API and outputs a list of the events into the terminal prompt.

#### Command usage:

    stellanow events

This will print a table of all available events with their metadata (EventID, Event Name, Is Active, Created At, Updated At).

#### Command options:

* No options required.

### 'plan'
The **'plan'** command compares currently generated classes with the specifications fetched from the API and provides a summary of changes.

#### Command usage:

    stellanow plan --input_dir .

This will scan all the auto-generated files in the current directory and compare them with the latest specifications from the API.

#### Command options:

* **'--input_dir (-i)'**: The directory to read generated classes from. Defaults to the current directory.

### 'generate'
The **'generate'** command fetches the latest event specifications from the API and generates corresponding class code in the desired programming language.

#### Command usage:

    stellanow generate --namespace MyApp.Messages --destination . --force --events Event1,Event2 --language csharp

This will generate C# classes for events 'Event1' and 'Event2', placing them in the current directory. The generated classes will be in the namespace 'MyApp.Messages'. If a file for an event already exists, it will be overwritten due to the **'--force'** flag.

#### Command options:

* **'--namespace (-n)'**: The namespace for the generated classes. Defaults to an empty string.
* **'--destination (-d)'**: The directory to save the generated classes. Defaults to the current directory.
* **'--force (-f)'**: A flag indicating whether to overwrite existing files. Defaults to false.
* **'--events (-e)'**: A list of specific events to generate. If this option is not provided, classes for all events will be generated.
* **'--language (-l)'**: The programming language for the generated classes. Can be 'csharp'. Defaults to 'csharp'.

### Common Command Options

* **'--access_key'**: The access key credential for accessing the StellaNow API. This should be the same as your StellaNow account access key.
* **'--access_token'**: The access token credential for accessing the StellaNow API. This should be the same as your StellaNow account access token.
* **'--organization_id'**: The unique identifier (UUID) of the organization in StellaNow. This is used to scope the operations within the given organization's context.
* **'--project_id'**: The unique identifier (UUID) of the project in StellaNow. This is used to scope the operations within the given project's context.
* **'--profile'**: The profile name for storing a particular set of configurations. If no profile is specified, the configurations will be stored under the 'DEFAULT' profile.
* **'--verbose (-v)'**: Enables verbose mode, which outputs more detailed logging messages.

These options allow for flexible command-line operation, as they let you provide command-specific details without altering your saved profile configurations. If these options are not specified in the command, the values saved in the specified profile (or the DEFAULT profile if none is specified) will be used.

Please note that providing these options at the command line overrides the corresponding saved profile values for the duration of that command execution only. See **Credential Precedence Order** section for details.

## Contact and Licensing
For further assistance and support, please contact us at ***help@stella.systems***

The StellaNow CLI is now open-source software, licensed under the terms of the MIT License. This allows for authorized copying, modification, and redistribution of the CLI tool, subject to the terms outlined in the license.

Please note that while the StellaNow CLI is open-source, the StellaNow platform and its associated code remain proprietary software. Unauthorized copying, modification, redistribution, and use of the StellaNow platform is prohibited without a proper license agreement. For inquiries about the licensing of the StellaNow platform, please contact us via the above email.