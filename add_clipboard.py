#!/usr/bin/env python3
"""
Add clipboard.js to all HTML files in python_gamedev
"""

import os
import re

def add_clipboard_to_file(filepath):
    """Add clipboard.js script tag to an HTML file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if clipboard.js is already included
    if 'clipboard.js' in content:
        print(f"  ✓ {os.path.basename(filepath)} already has clipboard.js")
        return False
    
    # Find the location to insert (after course-enhancements.js or before </head>)
    if 'course-enhancements.js' in content:
        # Insert after course-enhancements.js
        pattern = r'(<script src="/js/course-enhancements.js" defer></script>)'
        replacement = r'\1\n    <script src="/js/clipboard.js" defer></script>'
        new_content = re.sub(pattern, replacement, content)
    elif '/js/script.js' in content:
        # Some files might use script.js instead
        pattern = r'(<script src="/js/script.js"></script>)'
        replacement = r'\1\n    <script src="/js/clipboard.js" defer></script>'
        new_content = re.sub(pattern, replacement, content)
    else:
        # Insert before </head>
        pattern = r'(</head>)'
        replacement = r'    <script src="/js/clipboard.js" defer></script>\n\1'
        new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ Added clipboard.js to {os.path.basename(filepath)}")
        return True
    else:
        print(f"  ⚠ Could not add clipboard.js to {os.path.basename(filepath)}")
        return False

def main():
    base_path = '\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\python_gamedev\\'
    
    print("Adding clipboard functionality to Python GameDev course...")
    print("-" * 50)
    
    # Get all HTML files
    html_files = []
    for filename in os.listdir(base_path):
        if filename.endswith('.html'):
            filepath = os.path.join(base_path, filename)
            html_files.append(filepath)
    
    html_files.sort()
    
    # Process each file
    updated_count = 0
    for filepath in html_files:
        if add_clipboard_to_file(filepath):
            updated_count += 1
    
    print("-" * 50)
    print(f"Updated {updated_count} files")
    print("Clipboard functionality added to Python GameDev course!")

if __name__ == "__main__":
    main()
