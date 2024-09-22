from abc import ABC, abstractmethod
import os
import time
import hashlib

import src.file_management.bst as bst


class FileManagementBase(ABC):
    @abstractmethod
    def add_file(self, file_path, file_content):
        """
        Add a new file to the directory and update the BST.
        
        Args:
            file_path (str): The path where the file will be created.
            file_content (str): The content to write to the file.
        """
        pass

    @abstractmethod
    def update_file(self, file_id, new_content):
        """
        Update an existing file and its metadata in the BST.
        
        Args:
            file_id (int): The unique identifier of the file.
            new_content (str): The new content for the file.
        """
        pass

    @abstractmethod
    def delete_file(self, file_id):
        """
        Delete a file from the directory and remove it from the BST.
        
        Args:
            file_id (int): The unique identifier of the file.
        """
        pass

    @abstractmethod
    def get_file_metadata(self, file_id):
        """
        Retrieve metadata for a file from the BST.
        
        Args:
            file_id (int): The unique identifier of the file.
            
        Returns:
            dict: A dictionary containing the file's metadata.
        """
        pass

import os

class FileManagementInterface(FileManagementBase):
    def __init__(self, bst, base_directory):
        """
        Initialize a new FileManagementInterface object.
        
        Args:
            bst (BinarySearchTree): The binary search tree to use for storing and retrieving file metadata.
            base_directory (str): The base directory that will be used to store files.
        """
        self.bst = bst
        self.base_directory = base_directory
        
        # Ensure the base directory exists
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)
            print(f"Created base directory: {self.base_directory}")

    def add_file(self, file_path, file_content):
        """
        Add a new file to the directory and update the BST.
        
        Args:
            file_path (str): The relative path where the file will be created.
            file_content (str): The content to write to the file.
        """
        if os.path.isabs(file_path) or file_path.startswith('configs/'):
            raise ValueError("The file path must be relative and should not start with 'configs/'.")

        # Convert to an absolute path
        self.base_directory = os.path.abspath(self.base_directory)

        # Ensure file_path is relative to base_directory
        if os.path.isabs(file_path):
            # Strip leading slash to make it relative
            file_path = file_path.lstrip('/')
        
        # Construct the full file path
        full_path = os.path.join(self.base_directory, file_path)
        
        # Validate that file_content is either string or bytes
        if not isinstance(file_content, (str, bytes)):
            raise TypeError("file_content must be either a string or bytes")
        # Set the file mode based on content type
        elif isinstance(file_content, bytes):
            file_mode = 'wb'
        else:
            file_mode = 'w'

        # Generate a consistent file ID using md5 hash
        file_id = hashlib.md5(file_path.encode()).hexdigest()

        # Get the current timestamp for when the file is added
        file_timestamp = int(time.time())
        
        try:
            # Write the file to the directory
            with open(full_path, file_mode) as f:
                f.write(file_content)
                
            # Calculate the actual file size after writing 
            file_size = os.path.getsize(full_path)

            # Insert metadata into the BST
            self.bst.insert(
                file_id=file_id,
                file_timestamp=file_timestamp,
                file_path=full_path,
                file_size=file_size,
                file_type=file_path.split('.')[-1],  # Get the file extension
                creation_date=file_timestamp,
                description=f"Added file at {full_path}"
            )

        except IOError as io_error:
            print(f"Error writing file {full_path}: {io_error}")
            # Optionally: Remove the file if it was created before the error occurred
            if os.path.exists(full_path):
                os.remove(full_path)
            raise io_error

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Optionally: Clean up by removing the file if it was written
            if os.path.exists(full_path):
                os.remove(full_path)
            raise e  # Re-raise the actual caught exception

            
    def update_file(self, file_id, new_content):
        """
        Update an existing file and its metadata in the BST.
        
        Args:
            file_id (int): The unique identifier of the file.
            new_content (str): The new content for the file.
        """
        try:
            # Try to find the file in the BST
            node = self.bst.search_recursive(file_id)
            if node is None:
                # If the file is not found in the BST, raise a FileNotFoundError
                raise FileNotFoundError(f"No file with ID {file_id} found in the BST.")
            
            # Open the file and write the new content
            with open(node.file_path, 'w') as f:
                f.write(new_content)
            
            # Update the file's metadata in the BST
            node.file_timestamp = int(time.time())
            node.file_size = len(new_content)
            node.access_frequency += 1
        
        except FileNotFoundError as error:
            # Handle FileNotFoundError
            print(f"Error: {error}")
            # Depending on your use case, you could decide to exit or just return.
            return
        
        except IOError as io_error:
            # Handle IOError
            print(f"File operation error: {io_error}")
            # If file I/O fails, stop the operation.
            raise io_error
        
        except Exception as general_error:
            # Handle any other unexpected errors
            print(f"An unexpected error occurred: {general_error}")
            # Decide whether to crash or handle
            raise general_error  # Re-raise to allow the application to crash

    def delete_file(self, file_id):
        """
        Delete a file from the directory and remove it from the BST.
        
        Args:
            file_id (int): The unique identifier of the file.
        """
        try:
            # Search the BST for the node with the given file_id
            node = self.bst.search_recursive(file_id)
            if node is None:
                raise FileNotFoundError(f"No file with ID {file_id} found in the BST.")
            
            # Delete the file from the directory
            if os.path.exists(node.file_path):
                os.remove(node.file_path)
            else:
                raise FileNotFoundError(f"File not found on disk: {node.file_path}")
            
            # Remove the node from the BST
            self.bst.delete_node(file_id)
        
        except FileNotFoundError as error:
            print(f"Error: {error}")
            return
        
        except IOError as io_error:
            print(f"File operation error: {io_error}")
            raise io_error
        
        except Exception as general_error:
            print(f"An unexpected error occurred: {general_error}")
            raise general_error

    def get_file_metadata(self, file_id):
        """
        Retrieve metadata for a file from the BST.
        
        Args:
            file_id (int): The unique identifier of the file.
            
        Returns:
            dict: A dictionary containing the file's metadata.
        """
        try:
            # Search the BST for the node with the given file_id
            node = self.bst.search_recursive(file_id)
            if node is None:
                raise FileNotFoundError(f"No file with ID {file_id} found in the BST.")
            
            # Return the metadata as a dictionary
            metadata = {
                "file_id": node.file_id,
                "file_timestamp": node.file_timestamp,
                "file_path": node.file_path,
                "file_size": node.file_size,
                "file_type": node.file_type,
                "access_frequency": node.access_frequency,
                "version": node.version,
                "permissions": node.permissions,
                "checksum": node.checksum,
                "creation_date": node.creation_date,
                "description": node.description,
            }
            
            return metadata
        
        except FileNotFoundError as error:
            print(f"Error: {error}")
            return None
        
        except Exception as general_error:
            print(f"An unexpected error occurred: {general_error}")
            return None

    def list_all_files(self):
        """
        List all files and their metadata from the BST.
        
        This method traverses the BST in-order and returns a list of dictionaries, each containing metadata for a file.
        
        Returns:
            list: A list of dictionaries, each containing metadata for a file.
        """
        def in_order_traversal(node):
            """
            Perform an in-order traversal of the BST.
            
            This method traverses the BST in-order and returns a list of dictionaries, each containing metadata for a file.
            
            Args:
                node (TreeNode): The current node being traversed.
            
            Returns:
                list: A list of dictionaries, each containing metadata for a file.
            """
            if node is None:
                return []
            
            # Traverse the left subtree
            left_subtree = in_order_traversal(node.left)
            
            # Get the metadata for the current node
            current_node_metadata = [self.get_file_metadata(node.file_id)]
            
            # Traverse the right subtree
            right_subtree = in_order_traversal(node.right)
            
            # Combine the results from the left subtree, the current node, and the right subtree
            return left_subtree + current_node_metadata + right_subtree

        
        # Start the traversal from the root of the BST
        return in_order_traversal(self.bst.root)

    def get_file_content(self, file_id):
        """
        Retrieve the content of a file using the file_id by searching in the BST.
        
        Args:
            file_id (str): The unique identifier of the file.
        
        Returns:
            bytes or str: The content of the file (binary or text), or None if the file is not found.
        """
        try:
            # Try to find the file in the BST
            node = self.bst.search_recursive(file_id)
            if node is None:
                # If the file is not found in the BST, raise a FileNotFoundError
                raise FileNotFoundError(f"No file with ID {file_id} found in the BST.")
            
            # Open the file and read its content based on file type
            if node.file_path.endswith('.pkl') or node.file_path.endswith('.npy'):
                file_mode = 'rb'  # Read as binary for GMM models or MFCC files
            else:
                file_mode = 'r'  # Read as text for metadata or other text files

            # Read the content from the file
            with open(node.file_path, file_mode) as f:
                return f.read()

        except FileNotFoundError as error:
            print(f"Error: {error}")
            return None
        
        except IOError as io_error:
            print(f"File operation error: {io_error}")
            raise io_error
        
        except Exception as general_error:
            print(f"An unexpected error occurred: {general_error}")
            raise general_error  # Re-raise to allow the application to handle unexpected errors
