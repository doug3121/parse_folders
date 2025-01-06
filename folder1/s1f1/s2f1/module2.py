from pathlib import Path



if __name__ == '__main__':
    
    
    # Start from the current file
    current_path = Path(__file__).resolve()
    print(current_path)
    
    # Get the absolute path of the current script's directory
    module2_path = Path(__file__).resolve().parent
    
    print(module2_path)
    
    
    # Get the root folder
    root_path = Path(__file__).resolve().parents[1]
    
    print(root_path)
    
    # Start from the current file
    current_path = Path(__file__).resolve()
    # Traverse upwards until you find the marker file/directory
    for parent in current_path.parents:
        if (parent / "README.md").exists():  # Replace ".git" with your marker file/folder
            root_path = parent
            break 
        
    print("Root Path:", root_path)