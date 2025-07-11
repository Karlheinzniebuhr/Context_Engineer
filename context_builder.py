#!/usr/bin/env python3
"""
Context Builder
===============

A general-purpose file combiner that:
1. Takes any number of files as command-line arguments
2. Combines them with a powerful system prompt for AI interaction
3. Generates a context file for various AI tasks

Usage:
    python context_builder.py file1.py file2.md file3.txt [output.md]
    
Example:
    python context_builder.py src/main.py README.md config.json -o MyProject_context.md
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Clipboard functionality - gracefully handles missing libraries
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    try:
        import tkinter as tk
        CLIPBOARD_AVAILABLE = True
    except ImportError:
        CLIPBOARD_AVAILABLE = False

class ContextBuilder:
    """
    Combines files and a system prompt to build a context file for AI interaction.
    """
    
    def __init__(self):
        self.system_prompt = """# Final System Prompt for Implementation Guide Generation

## **Objective:**

To generate a detailed, explicit, and well-organized implementation guide that can be used by a less-capable AI agent to perform software development tasks. The guide should be so clear and comprehensive that it minimizes the need for the agent to make independent decisions or inferences.

## **Persona:**

You are a senior software engineer and AI assistant with expertise in creating clear and actionable development plans. You are meticulous, detail-oriented, and have a deep understanding of how to communicate complex technical instructions to a less-experienced audience.

## **Core Instructions:**

1.  **Deconstruct the Request:**

    *   Thoroughly analyze the user's request to understand the desired outcome.
    *   Identify all the necessary changes to the codebase to achieve the desired outcome.

2.  **Structure the Implementation Guide:**

    *   The guide must be presented as a series of discrete, numbered steps.
    *   Each step must be atomic and self-contained, representing a single, logical change to the codebase.
    *   The steps must be ordered logically, following the natural flow of the development process.

3.  **Step-by-Step Instructions:**

    *   For each step, provide the following information:

        *   **Goal:** A clear and concise description of what needs to be accomplished in this step.
        *   **File to Modify:** The full, absolute path of the file that needs to be modified.
        *   **Action:** A clear description of the action to be taken (e.g., "add code", "replace code", "delete code", "create file").
        *   **Code:** The exact code to be added, replaced, or deleted. Use a search/replace format where applicable, clearly indicating the code to be searched for and the code to replace it with.

4.  **Code Formatting:**

    *   All code snippets must be enclosed in appropriate markdown code blocks with the correct language identifier.
    *   The code provided must be complete and syntactically correct.
    *   Do not use comments like `// ... existing code...` or any other form of truncation.

5.  **Audience Awareness:**

    *   Remember that the implementation guide is for a less-capable AI agent.
    *   Avoid any ambiguity or vagueness in your instructions.
    *   Provide all necessary context and explanation for each step.

## **Example Implementation Guide:**

**Step 1:**

*   **Goal:** Create a new utility function to calculate the area of a rectangle.
*   **File to Modify:** `src/utils/math.js`
*   **Action:** Create a new file with the following content.
*   **Code:**

    ```javascript
    export function calculateRectangleArea(width, height) {
      return width * height;
    }
    ```

**Step 2:**

*   **Goal:** Update the `Rectangle` component to use the new `calculateRectangleArea` function.
*   **File to Modify:** `src/components/Rectangle.js`
*   **Action:** Import the new function and use it to calculate the area.
*   **Code:**

    *   **Search:**

        ```javascript
        const area = width * height;
        ```

    *   **Replace:**

        ```javascript
        import { calculateRectangleArea } from '../utils/math.js';

        const area = calculateRectangleArea(width, height);
        ```

## **Final Review:**

Before finalizing the guide, review it to ensure that it is:

*   **Complete:** All necessary changes are included.
*   **Clear:** The instructions are easy to understand.
*   **Correct:** The code and file paths are accurate.

By following these instructions, you will create a high-quality implementation guide that will enable a less-capable AI agent to successfully complete the requested task.
"""
    
    def get_file_info(self, file_path):
        """Get metadata about a file."""
        path = Path(file_path)
        try:
            stat = path.stat()
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = len(content.splitlines())
            
            file_type = path.suffix.lower()
            category_map = {
                '.py': 'Source Code', '.js': 'Source Code', '.ts': 'Source Code', '.java': 'Source Code', '.cpp': 'Source Code', '.c': 'Source Code', '.go': 'Source Code', '.rs': 'Source Code',
                '.md': 'Documentation', '.txt': 'Documentation', '.rst': 'Documentation',
                '.json': 'Configuration', '.yaml': 'Configuration', '.yml': 'Configuration', '.toml': 'Configuration', '.ini': 'Configuration',
                '.sql': 'Database'
            }
            category = category_map.get(file_type, "Other")
            
            return {
                'path': file_path,
                'name': path.name,
                'size': stat.st_size,
                'lines': lines,
                'type': file_type,
                'category': category,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'content': content
            }
        except Exception as e:
            return {'path': file_path, 'name': path.name, 'error': str(e)}
    
    def copy_to_clipboard(self, content):
        """Copy content to clipboard using available methods."""
        if not CLIPBOARD_AVAILABLE:
            return False
            
        try:
            # Try pyperclip first (most reliable)
            if 'pyperclip' in sys.modules:
                pyperclip.copy(content)
                return True
            
            # Fallback to tkinter
            root = tk.Tk()
            root.withdraw()  # Hide the window
            root.clipboard_clear()
            root.clipboard_append(content)
            root.update()  # Ensure clipboard is updated
            root.destroy()
            return True
            
        except Exception:
            return False
    
    def generate_directory_tree(self, file_paths):
        """Generate a beautiful directory tree structure from file paths."""
        from pathlib import Path
        import os
        
        # Get relative paths and organize them
        tree_structure = {}
        base_path = Path.cwd()
        
        for file_path in file_paths:
            path = Path(file_path)
            # Get relative path from current directory
            try:
                rel_path = path.relative_to(base_path)
            except ValueError:
                # If file is outside current directory, use absolute path
                rel_path = path
            
            # Build tree structure
            parts = rel_path.parts
            current_level = tree_structure
            
            for part in parts[:-1]:  # All parts except the file name
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            
            # Add the file
            current_level[parts[-1]] = None  # None indicates it's a file
        
        def render_tree(structure, prefix="", is_last=True):
            """Recursively render the tree structure."""
            lines = []
            items = sorted(structure.items(), key=lambda x: (x[1] is None, x[0]))  # Directories first, then files
            
            for i, (name, subtree) in enumerate(items):
                is_last_item = i == len(items) - 1
                
                # Choose the appropriate tree characters
                if is_last_item:
                    current_prefix = "└── "
                    next_prefix = "    "
                else:
                    current_prefix = "├── "
                    next_prefix = "│   "
                
                # Add the current item
                if subtree is None:  # It's a file
                    lines.append(f"{prefix}{current_prefix}{name}")
                else:  # It's a directory
                    lines.append(f"{prefix}{current_prefix}{name}/")
                    # Recursively add subdirectories and files
                    subtree_lines = render_tree(subtree, prefix + next_prefix, is_last_item)
                    lines.extend(subtree_lines)
            
            return lines
        
        if not tree_structure:
            return ["No files found"]
        
        # If there's only one root directory, start from there
        if len(tree_structure) == 1 and list(tree_structure.values())[0] is not None:
            root_name = list(tree_structure.keys())[0]
            root_structure = tree_structure[root_name]
            tree_lines = [f"{root_name}/"]
            tree_lines.extend(render_tree(root_structure, ""))
        else:
            tree_lines = render_tree(tree_structure)
        
        return tree_lines

    def build_context(self, file_paths, output_path=None, copy_clipboard=True):
        """Combines files and system prompt into a single context file."""
        print(f"🔧 Building context with {len(file_paths)} files...")
        
        file_info = [self.get_file_info(fp) for fp in file_paths]
        valid_files = [info for info in file_info if 'error' not in info]
        
        header = [
            f"# Context Generated: {datetime.now().isoformat()}",
            f"Total files processed: {len(file_paths)}",
            "---"
        ]
        
        # Generate directory tree
        directory_tree = ["## Directory Structure"]
        directory_tree.append("```")
        tree_lines = self.generate_directory_tree([info['path'] for info in valid_files])
        directory_tree.extend(tree_lines)
        directory_tree.append("```")
        
        file_manifest = ["## File Manifest"]
        categories = {}
        for info in valid_files:
            cat = info['category']
            if cat not in categories:
                categories[cat] = []
            # Include relative path for better context
            try:
                rel_path = Path(info['path']).relative_to(Path.cwd())
            except ValueError:
                rel_path = Path(info['path'])
            categories[cat].append(f"- `{rel_path}` ({info['lines']} lines)")
        
        for category, files in categories.items():
            file_manifest.append(f"### {category}")
            file_manifest.extend(files)
        
        file_contents = []
        for i, info in enumerate(valid_files, 1):
            # Use relative path in file headers for better readability
            try:
                rel_path = Path(info['path']).relative_to(Path.cwd())
            except ValueError:
                rel_path = Path(info['path'])
            file_contents.append(f"---\n### File {i}: `{rel_path}`\n\n```" + info.get('type','').lstrip('.') + f"\n{info['content']}\n```")

        
        full_content = "\n\n".join([self.system_prompt] + header + directory_tree + file_manifest + file_contents)
        
        # Only write output file if path is specified
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                print(f"\n🎯 SUCCESS: Context file written to: {output_path}")
            except Exception as e:
                print(f"❌ Error writing output file: {e}")
                return False
        else:
            print("\n📋 Context generated (no output file specified - content available in clipboard)")
        
        return full_content

def main():
    parser = argparse.ArgumentParser(
        description="Context Builder - A tool for combining files for AI interaction.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python context_builder.py src/main.py README.md
  python context_builder.py *.py -o project_context.md
"""
    )
    
    parser.add_argument('patterns', nargs='+', help='File patterns to include (e.g., "src/*.py", "docs/README.md")')
    parser.add_argument('-o', '--output', help='Output file name (optional - if not specified, only copies to clipboard)')
    
    parser.add_argument('-n', '--no-clipboard', action='store_true', help='Disable copying result to clipboard')

    args = parser.parse_args()
    
    file_paths = []
    for pattern in args.patterns:
        file_paths.extend([str(p) for p in Path().glob(pattern)])

    if not file_paths:
        print("❌ No files found for the given patterns.")
        sys.exit(1)
    
    file_paths = sorted(list(set(file_paths)))
    
    builder = ContextBuilder()
    result = builder.build_context(file_paths, args.output)

    if result and not args.no_clipboard:
        # If we have an output file, read from it; otherwise use the returned content
        if args.output:
            try:
                with open(args.output, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"❌ Error reading file for clipboard: {e}")
                sys.exit(1)
        else:
            content = result
        
        if builder.copy_to_clipboard(content):
            print("🔗 Content copied to clipboard!")
        else:
            print("⚠️ Clipboard copy failed (clipboard library not available)")
    
    if result:
        print(f"\n🎉 Context built successfully!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
