from pathlib import Path



if __name__ == '__main__':
    
    
    # Get the absolute path of the current script's directory
    module1_path = Path(__file__).resolve().parent
    
    print(module1_path)
    
    
    # Get the root folder
    root_path = Path(__file__).resolve().parents[1]
    
    print(root_path)