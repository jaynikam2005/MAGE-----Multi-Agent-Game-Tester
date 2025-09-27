import sys
import os
from pathlib import Path

def scan_for_0xff():
    """Find files containing 0xFF byte at position 0"""
    problematic_files = []
    
    for file_path in Path("src").rglob("*"):
        if file_path.is_file():
            try:
                with open(file_path, 'rb') as f:
                    first_byte = f.read(1)
                    if first_byte == b'\xff':
                        print(f"Found 0xFF at start of: {file_path}")
                        problematic_files.append(file_path)
                        
                        # Show more bytes for context
                        f.seek(0)
                        first_20 = f.read(20)
                        print(f"First 20 bytes: {first_20}")
                        print(f"File size: {file_path.stat().st_size} bytes")
                        print("-" * 50)
                        
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return problematic_files

def check_import_chain():
    """Check the exact import chain to find where it fails"""
    try:
        print("Testing imports step by step:")
        
        print("1. Testing sys...")
        import sys
        print("✓ sys OK")
        
        print("2. Testing os...")
        import os
        print("✓ os OK")
        
        print("3. Testing pathlib...")
        from pathlib import Path
        print("✓ pathlib OK")
        
        print("4. Adding src to path...")
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        print("✓ path OK")
        
        print("5. Testing src import...")
        import src
        print("✓ src OK")
        
        print("6. Testing src.core...")
        import src.core
        print("✓ src.core OK")
        
        print("7. Testing src.core.config...")
        import src.core.config
        print("✓ src.core.config OK")
        
        print("8. Testing get_settings...")
        from src.core.config import get_settings
        print("✓ get_settings OK")
        
        print("9. Testing src.main...")
        import src.main
        print("✓ src.main OK")
        
    except Exception as e:
        print(f"Import failed at step: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Scanning for 0xFF bytes ===")
    problematic = scan_for_0xff()
    
    if problematic:
        print(f"\nFound {len(problematic)} files with 0xFF:")
        for f in problematic:
            print(f"  - {f}")
    else:
        print("No files with 0xFF found")
    
    print("\n=== Testing Import Chain ===")
    check_import_chain()
