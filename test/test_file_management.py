import os
import sys
import time
import shutil
import unittest

# Insert the parent directory of the configmap package to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_management.bst import BinarySearchTree
from file_management.file_management import FileManagementInterface


class TestFileManagementInterface(unittest.TestCase):
    def setUp(self):
        self.bst = BinarySearchTree()
        self.base_directory = "tmp"
        self.base_directory = os.path.abspath(self.base_directory)
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)
        self.fmi = FileManagementInterface(self.bst, self.base_directory)

    def tearDown(self):
        if os.path.exists(self.base_directory):
            shutil.rmtree(self.base_directory)

    def test_add_file(self):
        """
        Test adding a new file to the directory and updating the BST.
        """
        
        file_path = "test_add_file.txt"
        file_content = "This is a test file."
        self.fmi.add_file(file_path, file_content)
        node = self.bst.search_recursive(hash(file_path))
        self.assertIsNotNone(node)
        self.assertEqual(node.file_path, os.path.join(self.base_directory, file_path))
        self.assertEqual(node.file_size, len(file_content))
        self.assertEqual(node.file_type, file_path.split('.')[-1])
        self.assertEqual(node.access_frequency, 0)
        self.assertEqual(node.version, None)
        self.assertEqual(node.permissions, None)
        self.assertEqual(node.checksum, None)
        self.assertEqual(node.creation_date, int(time.time()))
        self.assertEqual(node.description, f"Added file at {os.path.join(self.base_directory, file_path)}")

    @unittest.skip("This test is skipped")
    def test_update_file(self):
        file_path = "test_update_file.txt"
        initial_content = "This is a test file."
        updated_content = "This is an updated test file."
        self.fmi.add_file(file_path, initial_content)
        self.fmi.update_file(hash(file_path), updated_content)
        node = self.bst.search_recursive(hash(file_path))
        self.assertIsNotNone(node)
        self.assertEqual(node.file_path, os.path.join(self.base_directory, file_path))
        self.assertEqual(node.file_size, len(updated_content))
        self.assertEqual(node.file_type, file_path.split('.')[-1])
        self.assertEqual(node.access_frequency, 2)
        self.assertEqual(node.version, None)
        self.assertEqual(node.permissions, None)
        self.assertEqual(node.checksum, None)
        self.assertEqual(node.creation_date, int(time.time()))
        self.assertEqual(node.description, f"Updated file at {os.path.join(self.base_directory, file_path)}")
    
    #@unittest.skip("This test is skipped")
    def test_delete_file(self):
        file_path = "test_delete_file.txt"
        file_content = "This is a test file."
        self.fmi.add_file(file_path, file_content)
        self.fmi.delete_file(hash(file_path))
        node = self.bst.search_recursive(hash(file_path))
        self.assertIsNone(node)

    #@unittest.skip("This test is skipped")
    def test_get_file_metadata(self):
        file_path = "test_get_file_metadata.txt"
        file_content = "This is a test file."
        self.fmi.add_file(file_path, file_content)
        metadata = self.fmi.get_file_metadata(hash(file_path))
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["file_id"], hash(file_path))
        self.assertEqual(metadata["file_timestamp"], int(time.time()))
        self.assertEqual(metadata["file_path"], os.path.join(self.base_directory, file_path))
        self.assertEqual(metadata["file_size"], len(file_content))
        self.assertEqual(metadata["file_type"], file_path.split('.')[-1])
        self.assertEqual(metadata["access_frequency"], 0)
        self.assertEqual(metadata["version"], None)
        self.assertEqual(metadata["permissions"], None)
        self.assertEqual(metadata["checksum"], None)
        self.assertEqual(metadata["creation_date"], int(time.time()))
        self.assertEqual(metadata["description"], f"Added file at {os.path.join(self.base_directory, file_path)}")

if __name__ == '__main__':
    unittest.main()
