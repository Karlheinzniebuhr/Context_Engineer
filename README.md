<div align="center">

# 🎯 **Context Builder**

*Transform your codebase into AI-ready implementation guides*

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/yourusername/context-builder)

</div>

---

## ✨ **What is Context Builder?**

Context Builder is an elegant file combiner that transforms scattered codebases into comprehensive, AI-ready implementation guides. Built from extensive research of top AI systems, it creates crystal-clear documentation that even less-capable AI agents can follow flawlessly.

<div align="center">

### 🎨 **The Magic**

```
📁 Multiple Files  →  🔧 Context Builder  →  📋 AI-Ready Guide  →  🤖 Perfect Implementation
```

</div>

---

## 🌟 **Key Features**

<table>
<tr>
<td width="50%">

### 🧠 **Intelligence**
- **Smart File Detection** - Automatically categorizes and processes files
- **Metadata Enrichment** - Adds comprehensive file information
- **Error Prevention** - Robust handling with informative messages

</td>
<td width="50%">

### 🚀 **Efficiency**
- **Zero Dependencies** - Pure Python, works everywhere
- **Flexible Input** - Glob patterns, multiple files, directories
- **Clean Output** - Beautiful Markdown with syntax highlighting

</td>
</tr>
</table>

### 🎯 **AI-Optimized System Prompt**

Built from analyzing **hundreds** of AI system prompts including:
- 🔥 **Anthropic Claude** variants
- 🤖 **OpenAI GPT-4** models  
- 💻 **Cursor AI** development assistant
- 🌊 **Windsurf** coding assistant
- ❤️ **Lovable** development platform

---

## 🚀 **Quick Start**

### ⚡ **Installation via pip**

#### Requirements
- Python 3.6 or higher

#### Steps

```bash
# Step 1: Clone the repository
git clone https://github.com/yourusername/context-builder.git
cd context-builder

# Step 2: Install using pip (makes it directly executable!)
pip install -e .
```

After installation, use the `context_builder` command from anywhere, or its short alias `ctx`!

### 🎮 **Basic Usage**

<table>
<tr>
<td width="50%">

#### ✨ **After pip install** (Recommended)
```bash
# Use the direct command
context_builder file1.py file2.md file3.txt

# Or use the short alias
ctx file1.py file2.md file3.txt
```

</td>
<td width="50%">

#### 🐍 **Direct Python execution**
```bash
# Traditional method
python context_builder.py file1.py file2.md file3.txt
```

</td>
</tr>
</table>

### 🎨 **Advanced Examples**

<details>
<summary>📂 <strong>Project Files</strong></summary>

```bash
# Using direct command (after pip install)
context_builder src/main.py README.md config.json -o MyProject_context.md

# OR using Python directly
python context_builder.py src/main.py README.md config.json -o MyProject_context.md
```

</details>

<details>
<summary>🐍 <strong>Python Projects</strong></summary>

```bash
# Quick with short alias
ctx "src/*.py"

# OR traditional method
python context_builder.py "src/*.py"
```

</details>

<details>
<summary>📚 <strong>Documentation</strong></summary>

```bash
# Combine all documentation files
context_builder "docs/*.md" README.md

# Same thing the traditional way
python context_builder.py "docs/*.md" README.md
```

</details>

---

## 🏗️ **Repository Layout (Abridged)**

One of Context Builder's most **amazing features** is its intelligent repository layout generation! It automatically creates a beautiful, structured overview of your project's architecture.

<div align="center">

### 🎨 **Visual Project Structure**

```
MyAwesomeProject/
│
├── 📂 src/
│   ├── 🐍 main.py              # Core application logic
│   ├── 🔧 utils.py             # Utility functions
│   ├── 📊 data_processor.py    # Data processing module
│   └── 🌐 api_client.py        # External API integration
│
├── 📂 tests/
│   ├── 🧪 test_main.py         # Main logic tests
│   └── 🔍 test_utils.py        # Utility function tests
│
├── 📂 docs/
│   ├── 📖 installation.md      # Setup instructions
│   └── 🎯 usage_guide.md       # How-to documentation
│
├── 📋 requirements.txt         # Dependencies
├── ⚙️ config.json             # Configuration file
└── 📚 README.md               # Project overview
```

</div>

### ✨ **What makes it special:**

🔍 **Smart categorization** - Automatically detects file types and purposes  
📊 **Line count analysis** - Shows relative file sizes for quick understanding  
🎨 **Beautiful formatting** - Clean, readable structure with emojis and descriptions  
📱 **Responsive layout** - Works perfectly in any markdown viewer  
🤖 **AI-optimized** - Helps AI assistants understand your project structure instantly

<div align="center">

*"This feature alone has saved me hours of explaining project structure to AI assistants!"*

</div>

---

## 🎯 **Perfect For**

<div align="center">

| 🤖 **AI Development** | 📖 **Documentation** | 🔍 **Code Review** |
|:---:|:---:|:---:|
| Generate implementation guides for AI assistants | Create comprehensive project overviews | Prepare complete context for AI analysis |
| Optimize prompts for Google AI Studio | Build onboarding materials | Generate implementation summaries |
| Prepare codebases for AI agents | Combine scattered documentation | Create detailed project snapshots |

</div>

---

## 🎨 **Output Example**

```markdown
# Final System Prompt for Implementation Guide Generation

## **Objective:**
To generate a detailed, explicit, and well-organized implementation guide...

# Context Generated: 2024-07-11T18:17:29Z
Total files processed: 3
---

## File Manifest
### Source Code
- `main.py` (45 lines)
- `utils.py` (23 lines)

### Documentation  
- `README.md` (156 lines)

---
### File 1: `main.py`

```python
class Calculator:
    def add(self, a, b):
        return a + b
```
```

---

## 🤝 **Contributing**

<div align="center">

We'd love your help making Context Builder even better!

[![Issues](https://img.shields.io/badge/🐛-Report%20Issues-red)](https://github.com/yourusername/context-builder/issues)
[![Pull Requests](https://img.shields.io/badge/🔧-Submit%20PRs-green)](https://github.com/yourusername/context-builder/pulls)
[![Documentation](https://img.shields.io/badge/📚-Improve%20Docs-blue)](https://github.com/yourusername/context-builder)

</div>

---

## 📜 **License**

<div align="center">

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Made with ❤️ for the AI development community**

⭐ *Star this repo if you find it useful!* ⭐

</div>
