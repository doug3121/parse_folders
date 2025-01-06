from pathlib import Path
from typing import List, Tuple
import fnmatch

class FolderParserClass:
    def __init__(self, folder_path: str):
        """
        Initialize the FolderParser with the folder path.

        :param folder_path: Path to the folder to be parsed
        """
        self.folder_path = Path(folder_path).resolve()

    def get_files_containing(self, substring: str, extension: str) -> List[Tuple[Path, str]]:
        """
        Find files containing a specific substring in their filenames and optionally matching a specific extension.
        This version handles case-insensitive searches.
        """
        if not self.folder_path.is_dir():
            raise ValueError(f"{self.folder_path} is not a valid directory.")

        # Search for files containing the substring in their names
        matching_files = [
            (file, file.name)
            for file in self.folder_path.rglob("*")  # Search recursively
            if file.is_file() and substring.lower() in file.name.lower() and (
                (extension == ".*")  # Match files with any extension
                or (extension is None and file.suffix == '')  # Match files without extension
                or (extension is not None and file.suffix == extension)  # Match files with specific extension
            )
        ]

        return matching_files


    def get_single_file_containing(self, substring: str, extension: str) -> Tuple[Path, str]:
        """
        Find a single file containing a specific substring in its filename and matching a specific extension.
        Handles case-insensitive substring matching.
        """
        if not self.folder_path.is_dir():
            raise ValueError(f"{self.folder_path} is not a valid directory.")

        # Search for files containing the substring in their names and matching the extension
        matching_files = [
            file
            for file in self.folder_path.rglob("*")  # Search recursively
            if file.is_file() and substring.lower() in file.name.lower() and (
                (extension == ".*")  # Match files with any extension
                or (extension is None and file.suffix == '')  # Match files without extension
                or (extension is not None and file.suffix == extension)  # Match files with specific extension
            )
        ]

        # Check the number of matching files
        if len(matching_files) == 0:
            raise ValueError(f"No files found matching '{substring}' with extension '{extension}'.")
        elif len(matching_files) > 1:
            raise ValueError(f"Multiple files found matching '{substring}' with extension '{extension}': {[str(f) for f in matching_files]}")

        # Return the single matching file
        single_file = matching_files[0]
        return single_file, single_file.name


    def get_single_file_details(self, substring: str, extension: str) -> Tuple[Path, str]:
        """
        Find the path to a single file containing a specific substring in its filename
        and matching a specific extension, returning the path without the filename and the filename separately.

        :param substring: Substring to search for in filenames (supports wildcard patterns)
        :param extension: File extension to filter (e.g., '.txt', '.*')
        :return: Tuple containing the directory path (Path) and the filename (str)
        :raises: ValueError if no files or more than one file matches the criteria
        """
        if not self.folder_path.is_dir():
            raise ValueError(f"{self.folder_path} is not a valid directory.")

        # Search for files containing the substring in their names and matching the extension
        matching_files = [
            file
            for file in self.folder_path.rglob("*")  # Search recursively
            if file.is_file() and fnmatch.fnmatch(file.name, substring) and (
                (extension == ".*")  # Match files with any extension
                or (extension is None and file.suffix == '')  # Match files without extension
                or (extension is not None and file.suffix == extension)  # Match files with specific extension
            )
        ]

        # Check the number of matching files
        if len(matching_files) == 0:
            raise ValueError(f"No files found matching '{substring}' with extension '{extension}'.")
        elif len(matching_files) > 1:
            raise ValueError(f"Multiple files found matching '{substring}' with extension '{extension}': {[str(f) for f in matching_files]}")

        # Return the directory path without filename and the filename
        single_file = matching_files[0]  # single_file is now a Path object
        return single_file.parent, single_file.name
