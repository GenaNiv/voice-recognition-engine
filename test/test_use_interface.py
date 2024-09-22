import unittest
from unittest.mock import MagicMock
import os
import sys

# Insert the parent directory of the configmap package to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
from file_management.file_management import FileManagementInterface
from user_interface import AddFileCommand

class TestAddFileCommand(unittest.TestCase):

    def setUp(self):
        self.file_management = MagicMock(spec=FileManagementInterface)
        self.command = AddFileCommand(self.file_management, 'path', 'content')

    def test_successful_file_addition(self):
        self.command.execute()
        self.file_management.add_file.assert_called_once_with('path', 'content')

    def test_file_addition_with_empty_path(self):
        self.command.path = ''
        self.command.execute()
        self.file_management.add_file.assert_called_once_with('', 'content')

    def test_file_addition_with_empty_content(self):
        self.command.content = ''
        self.command.execute()
        self.file_management.add_file.assert_called_once_with('path', '')

    def test_file_addition_with_none_path(self):
        self.command.path = None
        with self.assertRaises(ValueError):
            self.command.execute()

    def test_file_addition_with_none_content(self):
        self.command.content = None
        self.command.execute()
        self.file_management.add_file.assert_called_once_with('path', None)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])