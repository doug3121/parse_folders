

from pathlib import Path
from typing import List, Tuple

from app.parse_folders.parse_folders import FolderParserClass


# Example Usage
if __name__ == "__main__":
    
    # Get the absolute path of the current script's directory
    app_path = Path.cwd()
    
    folder_search_dir = app_path / "folder1"
    
    parser = FolderParserClass(folder_search_dir)  # Replace with your folder path
    sm0_files = parser.get_files_containing("SM0", ".*")

    for file_path, file_name in sm0_files:
        print(f"Path: {file_path}")
        print(f"Filename: {file_name}")
   
   
    # search that only one file exist
    parser = FolderParserClass(folder_search_dir)  # Replace with your folder path
    try:
        sm0_file, filename = parser.get_single_file_containing("SM0", ".txt")
        print(f"Path: {sm0_file}")
        print(f"Filename: {filename}")
    
    
    except ValueError as e:
        print(e)
   
    # search that only one file exist
    parser = FolderParserClass(folder_search_dir)  # Replace with your folder path
    try:
        directory_path, filename = parser.get_single_file_details("*S*VAL*CRC*", ".*")
        
        print(f"Path: {directory_path}")
        print(f"Filename: {filename}")
   
    
    except ValueError as e:
        print(e)
   
   
   
        
    print("program finished")
