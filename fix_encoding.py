import sys
import os
from pathlib import Path

# Fix encoding for all Python files
def fix_encoding():
    src_dir = Path("src")
    if not src_dir.exists():
        print("src directory not found")
        return
    
    for py_file in src_dir.rglob("*.py"):
        try:
            # Read with UTF-8
            with open(py_file, 'r', encoding='utf-8-sig') as f:  # Handle BOM
                content = f.read()
            
            # Write back as UTF-8 without BOM
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed: {py_file}")
            
        except Exception as e:
            print(f"Error fixing {py_file}: {e}")

if __name__ == "__main__":
    fix_encoding()
    print("Encoding fix complete!")
