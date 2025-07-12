# 🎯 Context Builder

Transform your codebase into AI-ready implementation guides—in one command.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 Quick Start

> **Note:** This is a local development project. Installation must be done from the cloned repository.

```bash
# Clone the repository
git clone <your-repository-url>
cd context-builder

# Install locally in development mode (Python 3.6+)
pip install -e .

# Combine files - copies to clipboard by default
ctx src/*.py README.md

# Or create an output file
ctx src/*.py README.md -o project_context.md
```

---

## ✨ Key Features

- 🧠 Smart File Detection: Auto-categorizes and enriches metadata
- 🌐 Flexible Input: Files, directories, and glob patterns
- 🌳 **NEW!** Directory Tree: Beautiful ASCII tree visualization of project structure
- 📋 Clean Markdown: Syntax-highlighted, ready for AI agents
- 📋 Auto-Clipboard: Copies output to clipboard by default (no file created unless specified)
- ⚡ Zero Dependencies: Pure Python, no extra libraries
- 🤖 AI-Optimized: System prompt tuned for flawless guides

---

## 📂 Project Layout (Example)

```text
MyProject/
├── src/               # Source code
├── tests/             # Test suite
├── docs/              # Documentation
├── requirements.txt   # Dependencies
└── README.md          # Project overview
```

---

## 💎 Sample Output

```markdown
# Context Generated: 2025-07-11T19:00:00Z
Total files: 3
---
## File Manifest
- main.py (45 lines)
- utils.py (30 lines)
- config.json (20 lines)
---
### File 1: main.py
```python
# (file contents...)
```
```

---

## 🎛️ Usage Options

```bash
# Clipboard only (default behavior)
ctx src/*.py README.md

# Create output file
ctx src/*.py README.md -o context.md

# Disable clipboard copying
ctx src/*.py README.md -o context.md --no-clipboard
```

**Try it now** → `ctx --help`

