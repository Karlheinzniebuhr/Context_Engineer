# Context Builder

A powerful file combiner tool designed to create comprehensive, unambiguous implementation guides for AI agents. Context Builder intelligently merges multiple files into a single, well-structured document with metadata, optimized for use with Google AI Studio and other AI platforms.

## Features

- **Intelligent File Combining**: Merges multiple files with proper formatting and metadata
- **AI-Optimized System Prompt**: Includes a carefully researched system prompt designed to generate foolproof implementation guides
- **Flexible Input**: Accepts any combination of files via command-line arguments
- **Rich Metadata**: Includes file paths, sizes, types, and modification dates
- **Markdown Output**: Produces clean, readable Markdown files
- **Progress Tracking**: Shows real-time progress during file processing
- **Error Handling**: Robust error handling with informative messages

## The Purpose

Context Builder is specifically designed to bridge the gap between complex codebases and AI implementation. It creates comprehensive guides that:

- Are clear enough for less-capable AI agents to follow
- Include step-by-step instructions with explicit verification
- Prevent common implementation errors through detailed guidance
- Provide complete context without ambiguity

## Installation

### Prerequisites

- Python 3.6 or higher
- Standard Python libraries (no additional dependencies required)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/context-builder.git
cd context-builder
```

2. The script is ready to use - no additional installation required!

## Usage

### Basic Usage

```bash
python context_builder.py file1.py file2.md file3.txt
```

### Advanced Usage

```bash
# Combine specific project files and name the output
python context_builder.py src/main.py README.md config.json -o MyProject_context.md

# Combine all python files in the src directory
python context_builder.py "src/*.py"
```

### Output

The script generates a single markdown file (default: `combined_context.md`) that contains the system prompt and the contents of the combined files.

## Contributing

We welcome contributions! Please feel free to:

1. **Report Issues**: Found a bug or have a feature request? Open an issue!
2. **Submit Pull Requests**: Improvements and new features are always welcome
3. **Improve Documentation**: Help make the documentation clearer and more comprehensive

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
