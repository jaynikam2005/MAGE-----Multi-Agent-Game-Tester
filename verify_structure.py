"""
Verify Project Structure and Fix Import Issues
"""

from pathlib import Path
import sys

def verify_structure():
    """Verify that all functional files are in place"""
    
    print("🔍 Verifying MAGE Enterprise project structure...")
    
    base_path = Path("src")
    
    required_files = [
        "main.py",
        "gui/__init__.py", 
        "gui/advanced/functional_main_window.py",
        "core/implementations.py",
        "reporting/report_generator.py", 
        "testing/webdriver_integration.py",
        "database/advanced_operations.py",
        "gui/dialogs/advanced_dialogs.py"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - MISSING")
    
    print(f"\n📊 Summary:")
    print(f"✅ Existing files: {len(existing_files)}")
    print(f"❌ Missing files: {len(missing_files)}")
    
    if missing_files:
        print(f"\n🚨 MISSING FILES PREVENTING FUNCTIONAL MODE:")
        for file in missing_files:
            print(f"  - {file}")
        print(f"\n💡 These files need to be created for full functionality.")
        return False
    else:
        print(f"\n🎉 ALL REQUIRED FILES ARE PRESENT!")
        print(f"✅ The application should run in FUNCTIONAL mode")
        return True

def create_missing_directories():
    """Create missing directories"""
    
    directories = [
        "src/gui/advanced",
        "src/gui/dialogs", 
        "src/testing",
        "src/database",
        "src/reporting",
        "reports",
        "data",
        "logs"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {dir_path}")

if __name__ == "__main__":
    create_missing_directories()
    
    if verify_structure():
        print(f"\n🚀 Ready to run: python src/main.py")
    else:
        print(f"\n⚠️  Please create the missing files first")
