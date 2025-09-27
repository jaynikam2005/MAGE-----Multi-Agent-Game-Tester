import sys
import os
from pathlib import Path
import traceback

def find_problematic_file():
    """Find the file causing the UTF-8 error"""
    
    # Check main.py first
    main_file = Path("src/main.py")
    if main_file.exists():
        try:
            print(f"Checking {main_file}...")
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✓ {main_file} is OK")
        except UnicodeDecodeError as e:
            print(f"✗ Problem in {main_file}: {e}")
            return main_file
    
    # Check all Python files in order of import
    check_order = [
        "src/__init__.py",
        "src/core/__init__.py", 
        "src/core/config.py",
        "src/core/logger.py",
        "src/core/exception_handler.py",
        "src/security/__init__.py",
        "src/security/encryption.py",
        "src/database/__init__.py",
        "src/database/connection.py",
        "src/api/__init__.py",
        "src/api/server.py",
        "src/gui/__init__.py",
        "src/gui/main_window.py"
    ]
    
    for file_path in check_order:
        py_file = Path(file_path)
        if py_file.exists():
            try:
                print(f"Checking {py_file}...")
                with open(py_file, 'rb') as f:
                    raw_bytes = f.read(10)
                print(f"First 10 bytes: {raw_bytes}")
                
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"✓ {py_file} is OK")
                
            except UnicodeDecodeError as e:
                print(f"✗ Problem in {py_file}: {e}")
                return py_file
            except Exception as e:
                print(f"! Error checking {py_file}: {e}")
    
    # Check all other Python files
    for py_file in Path("src").rglob("*.py"):
        if str(py_file) not in check_order:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError as e:
                print(f"✗ Problem in {py_file}: {e}")
                return py_file
            except Exception as e:
                print(f"! Error checking {py_file}: {e}")
    
    print("No problematic files found in individual checks.")
    return None

def test_import():
    """Test importing the main module"""
    try:
        print("Testing import of src.main...")
        
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Try to import main
        import src.main
        print("✓ Import successful!")
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Diagnostic Script ===")
    problematic_file = find_problematic_file()
    
    if problematic_file:
        print(f"\nFound problematic file: {problematic_file}")
    else:
        print("\nNo problematic files found in scan.")
    
    print("\n=== Testing Import ===")
    test_import()
