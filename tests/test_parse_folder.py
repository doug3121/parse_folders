import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from typing import List, Tuple
from io import StringIO

# Assuming the FolderParser class is already imported
from app.parse_folders.parse_folders import FolderParserClass


# Assuming FolderParserClass is defined elsewhere in your module, for example:
# from your_module import FolderParserClass

class TestFolderParserClass(unittest.TestCase):
    def setUp(self):
        # Set up a mock object for self.folder_path
        self.folder_path = MagicMock()
        self.folder_path.is_dir.return_value = True

    @patch('pathlib.Path.is_dir', return_value=True)  # Mocking is_dir to return True for any folder path
    @patch('pathlib.Path.rglob')
    def test_get_files_containing_with_specific_extension(self, mock_rglob: MagicMock, mock_is_dir: MagicMock):
        # Mock the rglob method to return mock files
        mock_files = [
            MagicMock(spec=Path),
            MagicMock(spec=Path),
            MagicMock(spec=Path),
        ]

        # Set up mock file names and extensions
        mock_files[0].name = "SM0_report.txt"
        mock_files[0].suffix = ".txt"

        mock_files[1].name = "SM0_data.csv"
        mock_files[1].suffix = ".csv"

        mock_files[2].name = "unrelated_file.txt"
        mock_files[2].suffix = ".txt"

        # Return the mock files when rglob is called
        mock_rglob.return_value = mock_files

        parser = FolderParserClass("mock_folder")
        # Test for specific extension '.txt'
        result = parser.get_files_containing("SM0", ".txt")

        # Verify the results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "SM0_report.txt")

    @patch('pathlib.Path.is_dir', return_value=True)  # Mocking is_dir to return True for any folder path
    @patch('pathlib.Path.rglob')
    def test_get_files_containing_with_any_extension(self, mock_rglob: MagicMock, mock_is_dir: MagicMock):
        # Mock the rglob method to return mock files
        mock_files = [
            MagicMock(spec=Path),
            MagicMock(spec=Path),
            MagicMock(spec=Path),
            MagicMock(spec=Path)
        ]
        
        # Set up mock file names and extensions
        mock_files[0].name = "SM0_report.txt"
        mock_files[0].suffix = ".txt"
        
        mock_files[1].name = "SM0_data.csv"
        mock_files[1].suffix = ".csv"
        
        mock_files[2].name = "SM0_notes.log"
        mock_files[2].suffix = ".log"
        
        mock_files[3].name = "SM0_script"
        mock_files[3].suffix = ""

        # Return the mock files when rglob is called
        mock_rglob.return_value = mock_files

        parser = FolderParserClass("mock_folder")
        # Test for any extension (i.e., .*)
        result = parser.get_files_containing("SM0", ".*")

        # Verify the results
        self.assertEqual(len(result), 4)
        filenames = [file[1] for file in result]
        self.assertIn("SM0_report.txt", filenames)
        self.assertIn("SM0_data.csv", filenames)
        self.assertIn("SM0_notes.log", filenames)
        self.assertIn("SM0_script", filenames)

    @patch('pathlib.Path.is_dir', return_value=True)  # Mocking is_dir to return True for any folder path
    @patch('pathlib.Path.rglob')
    def test_get_files_containing_without_extension(self, mock_rglob: MagicMock, mock_is_dir: MagicMock):
        # Mock the rglob method to return mock files
        mock_files = [
            MagicMock(spec=Path),
            MagicMock(spec=Path),
            MagicMock(spec=Path),
        ]
        
        # Set up mock file names and extensions
        mock_files[0].name = "SM0_report.txt"
        mock_files[0].suffix = ".txt"
        
        mock_files[1].name = "SM0_script"
        mock_files[1].suffix = ""  # No extension
        
        mock_files[2].name = "SM0_notes.log"
        mock_files[2].suffix = ".log"

        # Return the mock files when rglob is called
        mock_rglob.return_value = mock_files

        parser = FolderParserClass("mock_folder")
        # Test for files without an extension (None)
        result = parser.get_files_containing("SM0", None)

        # Verify the results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "SM0_script")

    @patch('pathlib.Path.is_dir', return_value=True)  # Mocking is_dir to return True for any folder path
    @patch('pathlib.Path.rglob')
    def test_get_single_file_containing_found(self, mock_rglob: MagicMock, mock_is_dir: MagicMock):
        # Mock the rglob method to return mock files
        mock_files = [
            MagicMock(spec=Path),
            MagicMock(spec=Path),
        ]
        
        # Set up mock file names and extensions
        mock_files[0].name = "SM0_report.txt"
        mock_files[0].suffix = ".txt"
        
        mock_files[1].name = "unrelated_file.txt"
        mock_files[1].suffix = ".txt"

        # Return the mock files when rglob is called
        mock_rglob.return_value = mock_files

        parser = FolderParserClass("mock_folder")
        # Test for finding a single file with a specific substring and extension
        result = parser.get_single_file_containing("SM0", ".txt")

        # Verify the result
        self.assertEqual(result[1], "SM0_report.txt")

    @patch('pathlib.Path.is_dir', return_value=True)  # Mocking is_dir to return True for any folder path
    @patch('pathlib.Path.rglob')
    def test_get_single_file_containing_no_files(self, mock_rglob: MagicMock, mock_is_dir: MagicMock):
        # Mock the rglob method to return mock files
        mock_files = [
            MagicMock(spec=Path),
            MagicMock(spec=Path),
        ]
        
        # Set up mock file names and extensions
        mock_files[0].name = "unrelated_file.txt"
        mock_files[0].suffix = ".txt"
        
        mock_files[1].name = "another_file.csv"
        mock_files[1].suffix = ".csv"

        # Return the mock files when rglob is called
        mock_rglob.return_value = mock_files

        parser = FolderParserClass("mock_folder")
        # Test for no files matching the substring and extension
        with self.assertRaises(ValueError):
            parser.get_single_file_containing("SM0", ".txt")

    @patch('pathlib.Path.is_dir', return_value=True)  # Mocking is_dir to return True for any folder path
    @patch('pathlib.Path.rglob')
    def test_get_single_file_containing_multiple_files(self, mock_rglob: MagicMock, mock_is_dir: MagicMock):
        # Mock the rglob method to return mock files
        mock_files = [
            MagicMock(spec=Path),
            MagicMock(spec=Path),
            MagicMock(spec=Path)
        ]
        
        # Set up mock file names and extensions
        mock_files[0].name = "SM0_report.txt"
        mock_files[0].suffix = ".txt"
        
        mock_files[1].name = "SM0_data.txt"
        mock_files[1].suffix = ".txt"
        
        mock_files[2].name = "SM0_notes.txt"
        mock_files[2].suffix = ".txt"

        # Return the mock files when rglob is called
        mock_rglob.return_value = mock_files

        parser = FolderParserClass("mock_folder")
        # Test for multiple files matching the substring and extension
        with self.assertRaises(ValueError):
            parser.get_single_file_containing("SM0", ".txt")

    @patch('pathlib.Path.is_dir', return_value=False)  # Mocking is_dir to return False to simulate invalid folder
    def test_invalid_directory(self, mock_is_dir: MagicMock):
        # Test for invalid directory path
        parser = FolderParserClass("invalid_folder")
        with self.assertRaises(ValueError):
            parser.get_files_containing("SM0", ".txt")

    def test_no_files_found(self):
        # Simulate no matching files
        self.folder_path.rglob.return_value = []

        with self.assertRaises(ValueError) as context:
            FolderParserClass.get_single_file_details(self, "test", ".txt")

        self.assertEqual(str(context.exception), "No files found matching 'test' with extension '.txt'.")

    def test_multiple_files_found(self):
        # Simulate multiple matching files
        file1 = MagicMock(spec=Path, name="file1.txt")
        file1.is_file.return_value = True
        file2 = MagicMock(spec=Path, name="file2.txt")
        file1.is_file.returnable = True
        self.folder_path.is_dir.return_value

    def test_multiple_files_found2(self):
        # Simulate multiple matching files
        file1 = MagicMock(spec=Path, name="test_S02_VAL018_CRC_xxx.s19.txt")
        file1.is_file.return_value = True
        file2 = MagicMock(spec=Path, name="filtest_S08_VAL020_CRC_xxx.s19e2.txt")
        file2.is_file.return_value = True
        self.folder_path.rglob.return_value = [file1, file2]

        with self.assertRaises(ValueError) as context:
            FolderParserClass.get_single_file_details(self, "*S*VAL*CRC*", ".*")

        self.assertTrue("Multiple files found matching" in str(context.exception))

    def test_single_file_found2(self):
        # Simulate a single matching file
        file1 = MagicMock(spec=Path, name="FS_S12_VAL023_CRCxxxx.txt")
        file1.is_file.return_value = True
        file1.name = "SVALCRC123.txt"
        file1.suffix = ".txt"
        file1.parent = Path("/mock/path")
        self.folder_path.rglob.return_value = [file1]

        directory_path, filename = FolderParserClass.get_single_file_details(self, "*S*VAL*CRC*", ".*")

        self.assertEqual(directory_path, Path("/mock/path"))
        self.assertEqual(filename, "SVALCRC123.txt")


if __name__ == '__main__':
    unittest.main()
