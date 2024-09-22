# Imports and Setup
import argparse
import json
from abc import ABC, abstractmethod
from file_management.file_management import FileManagementInterface
from file_management.bst import BinarySearchTree
import os

#Command interface
class CommandInterface(ABC):
    """Abstract base class for commands.
    
    All commands must implement the execute method.
    """
    @abstractmethod
    def execute(self):
        """Execute the command.

        This method should be overridden by subclasses of CommandInterface and
        contain the code that should be run when the command is executed.
        """
        pass
    
class AddFileCommand(CommandInterface):
    """Command to add a new file to the file management system."""

    def __init__(self, file_management, path, content):
        """Initialize the command.

        Args:
            file_management (FileManagementInterface): The file management
                system to use.
            path (str): The relative path where the file will be created. 
                        The path must be relative to the base directory 
                        and should not start with 'configs/'.
            content (str): The content to write to the file.
        
        Raises:
            ValueError: If the path is absolute or starts with 'configs/'.
        """
        self.file_management = file_management
        self.path = path
        self.content = content


    def execute(self):
        """Execute the command.

        This method adds a new file to the file management system.
        """
        self.file_management.add_file(self.path, self.content)
    
class UpdateFileCommand(CommandInterface):
    """Command to update an existing file in the file management system."""

    def __init__(self, file_management, path, content):
        """Initialize the command.

        Args:
            file_management (FileManagementInterface): The file management
                system to use.
            path (str): The path to the file to update.
            content (str): The content to write to the file.
        """
        self.file_management = file_management
        self.path = path
        self.content = content

    def execute(self):
        """Execute the command.

        This method updates an existing file in the file management system.
        """
        self.file_management.update_file(self.path, self.content)

class DeleteFileCommand(CommandInterface):
    """Command to delete an existing file from the file management system."""

    def __init__(self, file_management, file_id):
        """
        Initialize the command.

        Args:
            file_management (FileManagementInterface): The file management
                system to use.
            file_id (int): The unique identifier of the file to delete.
        """
        self.file_management = file_management
        self.file_id = file_id

    def execute(self):
        """Execute the command.

        This method deletes an existing file from the file management system.
        """
        self.file_management.delete_file(self.file_id)

class ListAllFilesCommand(CommandInterface):
    """Command to list all files and their metadata."""

    def __init__(self, file_management):
        """
        Initialize the command.

        Args:
            file_management (FileManagementInterface): The file management
                system to use.
        """
        self.file_management = file_management

    def execute(self):
        """Execute the command.

        This method lists all files and their metadata.
        """
        files_metadata = self.file_management.list_all_files()
        for metadata in files_metadata:
            print(metadata)


# User Interface Class
class UserInterface:
    """
    The UserInterface class is responsible for executing commands.

    It provides a single method, `run_command`, which takes a `CommandInterface`
    object as its argument and executes the command.
    """

    def __init__(self):
        pass

    def run_command(self, command: CommandInterface):
        """
        Execute the given command.

        Args:
            command (CommandInterface): The command to execute.
        """
        command.execute()

# 4. Argument Parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="File Management CLI for ConfigMap")
    
    # Optional argument to specify the configuration file
    parser.add_argument('--config', default='config.json', help='Path to the configuration file')
    
    subparsers = parser.add_subparsers(dest='command')
    
    # Add file command
    parser_add = subparsers.add_parser('add', help='Add a new configuration file')
    parser_add.add_argument('--path', required=True, help='Path where the file will be stored')
    parser_add.add_argument('--content', required=True, help='Content of the configuration file in JSON format')

    # Update file command
    parser_update = subparsers.add_parser('update', help='Update an existing configuration file')
    parser_update.add_argument('--path', required=True, help='Path to the file that will be updated')
    parser_update.add_argument('--content', required=True, help='New content for the configuration file in JSON format')

    # Delete file command
    parser_update = subparsers.add_parser('delete', help='Delete an existing configuration file')
    parser_update.add_argument('--file_id', required=True, help='File ID of the file that will be deleted')

    # List file's metadata command
    parser_update = subparsers.add_parser('list', help='List metadata for all files')
    
    # Add more parsers for other commands like delete, retrieve, etc.

    return parser.parse_args()

def load_config(config_path):
    """Load configuration from the provided JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")
    
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    return config

# 5. Main Function
def main():
    
    # Parse command-line arguments
    args = parse_arguments()

    # Load configuration from config.json
    config = load_config(args.config)

    # Retrieve the base directory from the configuration
    base_directory = config.get('base_directory', '/configs')
    
    # Ensure the base directory exists, create it if not
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
        print(f"Created base directory: {base_directory}")
        
    # Initialize necessary components
    bst = BinarySearchTree()
    file_management = FileManagementInterface(bst, base_directory)
    ui = UserInterface()

    # Execute the appropriate command based on the parsed arguments
    if args.command == 'add':
        content_dict = json.loads(args.content)  # Ensure content is valid JSON
        command = AddFileCommand(file_management, args.path, json.dumps(content_dict))
        ui.run_command(command)

    elif args.command == 'update':
        content_dict = json.loads(args.content)  # Ensure content is valid JSON
        command = UpdateFileCommand(file_management, args.path, json.dumps(content_dict))
        ui.run_command(command)

    elif args.command == 'delete':
        command = DeleteFileCommand(file_management, args.file_id)
        ui.run_command(command)

    elif args.command == 'list':
        command = ListAllFilesCommand(file_management)
        ui.run_command(command)

    # Add elif blocks for other commands

    # Serialize the BST before exiting the program
    bst.serialize_bst()

# 6. Main Loop (if needed)
# This could be implemented if you want an interactive shell-like interface
# Otherwise, the main() function as it stands is sufficient for single-command execution.

if __name__ == "__main__":
    main()