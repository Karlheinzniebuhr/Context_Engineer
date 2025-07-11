#!/usr/bin/env python3
"""
Example usage of Context Builder

This script demonstrates how to use the Context Builder tool to create
a comprehensive context file from multiple source files.
"""

import subprocess
import sys
from pathlib import Path

def create_example_files():
    """Create example files to demonstrate Context Builder functionality."""
    
    example_dir = Path("example_project")
    example_dir.mkdir(exist_ok=True)
    
    (example_dir / "main.py").write_text("""# main.py
class Calculator:
    def add(self, a, b):
        return a + b
""")
    
    (example_dir / "README.md").write_text("""# Example Project

A simple calculator application.
""")
    
    return [str(example_dir / "main.py"), str(example_dir / "README.md")]

def run_context_builder(files):
    """Run Context Builder on the provided files."""
    
    builder_script = Path(__file__).parent / "context_builder.py"
    
    if not builder_script.exists():
        print(f"Error: Context Builder script not found at {builder_script}")
        return False
    
    cmd = [sys.executable, str(builder_script)] + files
    
    try:
        print(f"Running Context Builder with files: {files}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Context Builder ran successfully!")
        print("Output:")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Context Builder failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main function to demonstrate Context Builder usage."""
    print("Context Builder Example Usage")
    print("=" * 40)
    
    example_files = create_example_files()
    
    if run_context_builder(example_files):
        print("\n🎉 Example completed successfully!")

if __name__ == "__main__":
    main()
