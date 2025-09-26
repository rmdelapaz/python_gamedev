#!/usr/bin/env python3
"""
Add clipboard.js to all HTML files in python_gamedev
This script handles both Windows and WSL path formats
"""

import os
import re
import sys
import platform

def detect_path_format():
    """Detect if we're running on Windows or WSL/Linux"""
    system = platform.system()
    if system == "Windows":
        return "windows"
    else:
        return "wsl"

def get_project_path():
    """Get the correct path based on the system"""
    system_type = detect_path_format()
    
    if system_type == "windows":
        # Windows path format for WSL files
        paths_to_try = [
            r"\\wsl$\Ubuntu\home\practicalace\projects\python_gamedev",
            r"\\wsl.localhost\Ubuntu\home\practicalace\projects\python_gamedev",
            r"C:\Users\practicalace\projects\python_gamedev",  # If copied locally
        ]
    else:
        # WSL/Linux path format
        paths_to_try = [
            "/home/practicalace/projects/python_gamedev",
            "~/projects/python_gamedev",
            os.path.expanduser("~/projects/python_gamedev"),
        ]
    
    # Find which path exists
    for path in paths_to_try:
        if os.path.exists(path):
            return path
    
    # If no path found, ask user
    print("Could not automatically detect project path.")
    print("Please enter the full path to python_gamedev folder:")
    user_path = input().strip()
    if os.path.exists(user_path):
        return user_path
    else:
        print(f"Error: Path '{user_path}' does not exist!")
        sys.exit(1)

def add_clipboard_to_file(filepath):
    """Add clipboard.js script tag to an HTML file"""
    
    try:
        # Read file with UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    # Check if clipboard.js is already included
    if 'clipboard.js' in content:
        return False, "already has clipboard.js"
    
    # Track if we made changes
    original_content = content
    
    # Pattern 1: Insert after course-enhancements.js (most common in gamedev)
    pattern1 = r'(    <script src="/js/course-enhancements.js" defer></script>)'
    replacement1 = r'\1\n    <script src="/js/clipboard.js" defer></script>'
    new_content = re.sub(pattern1, replacement1, content)
    
    # If pattern 1 didn't work, try pattern 2: Insert before </head>
    if new_content == content:
        pattern2 = r'(</head>)'
        replacement2 = r'    <script src="/js/clipboard.js" defer></script>\n\1'
        new_content = re.sub(pattern2, replacement2, content)
    
    # Check if we made any changes
    if new_content != original_content:
        try:
            # Write the updated content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "successfully added clipboard.js"
        except Exception as e:
            return False, f"Error writing file: {e}"
    else:
        return False, "could not find insertion point"

def process_files(base_path):
    """Process all HTML files in the given directory"""
    
    # Statistics
    total_files = 0
    updated_files = 0
    skipped_files = 0
    failed_files = []
    
    # Get all HTML files
    html_files = []
    try:
        for filename in os.listdir(base_path):
            if filename.endswith('.html'):
                html_files.append(filename)
    except Exception as e:
        print(f"Error listing directory: {e}")
        return
    
    html_files.sort()
    total_files = len(html_files)
    
    print(f"Found {total_files} HTML files to process")
    print("-" * 60)
    
    # Process each file
    for i, filename in enumerate(html_files, 1):
        filepath = os.path.join(base_path, filename)
        
        # Show progress
        progress = f"[{i}/{total_files}]"
        
        # Process the file
        success, message = add_clipboard_to_file(filepath)
        
        if success:
            print(f"{progress} ✅ {filename}: {message}")
            updated_files += 1
        elif "already has" in message:
            print(f"{progress} ✓  {filename}: {message}")
            skipped_files += 1
        else:
            print(f"{progress} ⚠  {filename}: {message}")
            failed_files.append((filename, message))
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {total_files}")
    print(f"Files updated: {updated_files}")
    print(f"Files skipped (already had clipboard.js): {skipped_files}")
    print(f"Files failed: {len(failed_files)}")
    
    if failed_files:
        print("\n⚠ Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    if updated_files > 0:
        print(f"\n✅ Successfully added clipboard functionality to {updated_files} files!")
    else:
        print("\n✓ All files already have clipboard functionality or no updates were needed.")

def verify_clipboard_js_exists(base_path):
    """Verify that clipboard.js exists in the js directory"""
    
    js_dir = os.path.join(base_path, "js")
    clipboard_file = os.path.join(js_dir, "clipboard.js")
    
    if not os.path.exists(js_dir):
        print(f"⚠ Warning: js directory not found at {js_dir}")
        print("Creating js directory...")
        try:
            os.makedirs(js_dir)
            print("✅ Created js directory")
        except Exception as e:
            print(f"❌ Failed to create js directory: {e}")
            return False
    
    if not os.path.exists(clipboard_file):
        print(f"⚠ Warning: clipboard.js not found at {clipboard_file}")
        print("You need to copy clipboard.js to the js directory first!")
        print("\nYou can copy it from python_intro/js/clipboard.js")
        return False
    
    print(f"✅ Found clipboard.js at {clipboard_file}")
    return True

def main():
    """Main function"""
    
    print("=" * 60)
    print("CLIPBOARD.JS INSTALLER FOR PYTHON GAMEDEV")
    print("=" * 60)
    print()
    
    # Get the project path
    print("Detecting project path...")
    base_path = get_project_path()
    print(f"✅ Using path: {base_path}\n")
    
    # Verify clipboard.js exists
    print("Checking for clipboard.js...")
    if not verify_clipboard_js_exists(base_path):
        print("\n⚠ Please ensure clipboard.js is in the js directory before running this script.")
        response = input("\nDo you want to continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            print("Exiting...")
            sys.exit(0)
    
    print("\n" + "-" * 60)
    print("Starting file processing...")
    print("-" * 60 + "\n")
    
    # Process all HTML files
    process_files(base_path)
    
    print("\n✅ Process complete!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
