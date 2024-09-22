import pickle
import os

class TreeNode:
    """
    A class to represent a node in the binary search tree
    """
    def __init__(self, 
                 file_id: int, 
                 file_timestamp: int, 
                 file_path: str, 
                 file_size: int = None, 
                 file_type: str = None, 
                 access_frequency: int = 0, 
                 speaker_name: str = None,
                 version: str = None, 
                 permissions: str = None, 
                 checksum: str = None, 
                 creation_date: int = None, 
                 description: str = None):
        """
        Initialize a new TreeNode
        
        Args:
            file_id (int): The unique identifier of the file
            file_timestamp (int): The timestamp when the file was last modified
            file_path (str): The path to the file
            file_size (int): The size of the file in bytes
            file_type (str): The type of the file
            access_frequency (int): The number of times the file has been accessed
            speaker_name (str): The name of the speaker  associated with teh file
            version (str): The version of the file
            permissions (str): The permissions of the file
            checksum (str): The checksum of the file
            creation_date (int): The timestamp when the file was created
            description (str): A description of the file
        """
        self.file_id = file_id
        self.file_timestamp = file_timestamp
        self.file_path = file_path
        self.file_size = file_size
        self.file_type = file_type
        self.access_frequency = access_frequency
        self.speaker_name = speaker_name
        self.version = version
        self.permissions = permissions
        self.checksum = checksum
        self.creation_date = creation_date
        self.description = description
        self.left = None
        self.right = None 
        
class BinarySearchTree:
    def __init__(self, serialized_file=None):
        """
        Initialize a new BinarySearchTree object.
        
        Args:
            serialized_file (str): The path to the file containing the serialized BST data.
                                   If None, the BST will be initialized with an empty root
                                   and will use 'data/bst_data.pkl' as the default file.
        """
        # Ensure the data directory exists
        data_directory = 'data'
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        
        # Set the path to the serialized file
        self.serialized_file = serialized_file or os.path.join(data_directory, 'bst_data.pkl')
        self.root = None
        
        # Load the BST from the serialized file, if it exists
        self.deserialize_bst()
    
    def deserialize_bst(self):
        """
        Load the BST from a file.

        If the file does not exist, the BST will be empty.
        """
        if os.path.exists(self.serialized_file):
            with open(self.serialized_file, 'rb') as file:
                self.root = pickle.load(file)
            print(f"BST loaded from {self.serialized_file}")
        else:
            print(f"No serialized BST file found at {self.serialized_file}. Starting with an empty BST.")
                
    def serialize_bst(self, filename=None):
        """
        Serialize the Binary Search Tree and save it to a file.

        The BST is serialized using the pickle library, which converts the tree's
        structure and data into a byte stream that can be written to a file.

        Args:
            filename (str): The name of the file where the BST will be saved.
                            If None, it will use the default `self.serialized_file`.

        Returns:
            None
        """
        # Check if the BST is empty
        if self.root is None:
            # If the tree is empty, delete the file if it exists and return
            filename = filename or self.serialized_file
            if os.path.exists(filename):
                os.remove(filename)
                print(f"BST is empty. Deleted {filename} if it existed.")
            return

        # If the tree is not empty, proceed with serialization
        filename = filename or self.serialized_file
        with open(filename, 'wb') as file:
            pickle.dump(self.root, file)
        print(f"BST serialized and saved to {filename}")

    def insert(self, 
               file_id, 
               file_timestamp, 
               file_path, 
               file_size=None, 
               file_type=None, 
               access_frequency=0, 
               version=None, 
               permissions=None, 
               checksum=None, 
               creation_date=None, 
               description=None):
        """
        Insert a new node to the binary search tree.
        
        The node is inserted in the correct position based on its file_id.
        If the tree is empty, the new node becomes the root.
        If the tree is not empty, the node is inserted to the left subtree if its file_id is less than the current node's,
        or to the right subtree if its file_id is greater than the current node's.
        
        If the node already exists in the tree, its metadata is updated with the new data.
        
        Args:
            file_id (int): The unique identifier of the file.
            file_timestamp (int): The timestamp when the file was last modified.
            file_path (str): The path to the file.
            file_size (int): The size of the file in bytes.
            file_type (str): # Type of file (e.g., 'wav', 'npy', 'pkl', 'txt')
            access_frequency (int): The number of times the file has been accessed.
            version (str): The version of the file.
            permissions (str): The permissions of the file.
            checksum (str): The checksum of the file.
            creation_date (int): The timestamp when the file was created.
            description (str): A description of the file.
        
        Returns:
            TreeNode or None: The newly inserted node, or the updated node if the file_id already exists.
        """
        new_node = TreeNode(
            file_id, 
            file_timestamp, 
            file_path, 
            file_size, 
            file_type, 
            access_frequency, 
            version, 
            permissions, 
            checksum, 
            creation_date, 
            description
            )
        if self.root is None:
            # If the tree is empty, the new node becomes the root
            self.root = new_node
            return new_node

        current = self.root
        while True:
            if file_id < current.file_id:
                # If the file_id is less than the current node's, go to the left subtree
                if current.left is None:
                    # If the left child is None, insert the new node here
                    current.left = new_node
                    return current.left
                current = current.left
            elif file_id > current.file_id:
                # If the file_id is greater than the current node's, go to the right subtree
                if current.right is None:
                    # If the right child is None, insert the new node here
                    current.right = new_node
                    return current.right
                current = current.right
            else:
                # If the file_id is equal to the current node's, update the existing node
                current.file_timestamp = file_timestamp
                current.file_path = file_path
                current.file_size = file_size
                current.file_type = file_type
                current.version = version
                current.permissions = permissions
                current.checksum = checksum
                current.creation_date = creation_date
                current.description = description
                return current  # Return the updated node
                    
    def search(self, file_id):
        """
        Search for a node with a given file_id in the binary search tree.
        
        Args:
            file_id (int): The file_id to search for.
            
        Returns:
            TreeNode or None: The node if found, None otherwise.
        """
        # If the tree is empty, return None
        if self.root is None:
            return None
        # Otherwise, search the tree iteratively
        current = self.root
        while current is not None:
            # If the current node's file_id matches the target file_id, return the file_timestamp
            if file_id == current.file_id:
                return current
            # If the target file_id is less than the current node's file_id, search the left subtree
            elif file_id < current.file_id:
                current = current.left
            # If the target file_id is greater than the current node's file_id, search the right subtree
            else:
                current = current.right
        # If the target file_id is not found in the tree, return None
        return None

    def search_recursive(self, file_id):
        """
        A recursive function to search for a node with a given file_id.
        
        Args:
            file_id (int): The file_id to search for.
            
        Returns:
            TreeNode or None: The node if found, None otherwise.
        """
        # If the tree is empty, return None
        if self.root is None:
            return None
        # Otherwise, search the tree recursively
        else:
            return self._search_recursive(self.root, file_id)
        
    def _search_recursive(self, current, file_id):
        """
        A recursive function to search for a node with a given file_id.
        
        Args:
            current (TreeNode): The current node being searched.
            file_id (int): The file_id to search for.
            
        Returns:
            TreeNode or None: The node if found, None otherwise.
        """
        # If the current node is None, return None
        if current is None:
            return None
        # If the current node's file_id matches the target file_id, return the node
        elif current.file_id == file_id:
            return current
        # If the target file_id is greater than the current node's file_id, search the right subtree
        elif current.file_id < file_id:
            return self._search_recursive(current.right, file_id)
        # If the target file_id is less than the current node's file_id, search the left subtree
        else:
            return self._search_recursive(current.left, file_id)
            
        
    def delete_node(self, file_id):
        """
        Delete a node from the binary search tree.
        
        If the tree is empty, this function does nothing.
        
        Args:
            file_id (int): The file_id of the node to delete.
        """
        if self.root is None:
            return
        else:
            self.root = self._delete_recursive(self.root, file_id)

    def _delete_recursive(self, node, file_id):
        """
        A recursive function to delete a node from the binary search tree.
        
        Args:
            node (TreeNode): The current node being traversed.
            file_id (int): The file_id of the node to delete.
            
        Returns:
            TreeNode: The root of the modified tree after the deletion.
        """
        if node is None:
            return node
        
        # Traverse the tree to find the node to delete
        if file_id < node.file_id:
            # Search the left subtree
            node.left = self._delete_recursive(node.left, file_id)
        elif file_id > node.file_id:
            # Search the right subtree
            node.right = self._delete_recursive(node.right, file_id)
        else:
            # Node found, perform deletion
            if node.left is None and node.right is None:
                # Case 1: Node with no children (Leaf Node)
                return None
            elif node.left is None:
                # Case 2: Node with one child
                return node.right
            elif node.right is None:
                return node.left
            
            # Case 3: Node with two children
            # Find the in-order successor (smallest in the right subtree)
            min_larger_node = self._find_min(node.right)
            
            # Copy the in-order successor's content to this node
            node.file_id = min_larger_node.file_id
            node.file_timestamp = min_larger_node.file_timestamp
            
            # Delete the in-order successor
            node.right = self._delete_recursive(node.right, min_larger_node.file_id)
            
        return node
            
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node
    
    def print_data(self):
        """TBD"""
        if self.root is None:
            print("The data base is empty...")
        else:
            self._print_recursive(self.root)
            
    def _print_recursive(self, node):
        """TBD"""
        if node is not None:
            # Traverse the left subtree first
            self._print_recursive(node.left)
            # Print the current node's data
            print(f"File ID: {node.file_id}, Last Modified: {node.file_timestamp}")
            # Traverse the right subtree
            self._print_recursive(node.right)
        

            
                    

                
                
                
                
                    
            
            

            

            
                