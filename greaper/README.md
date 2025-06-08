# Greaper: Grep on Steroids

Greaper is a next-generation search tool for developers, data scientists, and power users.  
It combines the speed and flexibility of classic grep with modern features for code, data, and package search.  
Now with a modern TUI, robust error handling, and extensible architecture.

---

## 🚀 Goals & Milestones

### 1. Core CLI and Search Engine
- [x] Design command-line interface (CLI) and help system
- [x] Implement basic regex search
- [x] Add fuzzy search capability (using optimized algorithms)
- [x] Support case-insensitive and whole-word options

### 2. File & Directory Traversal
- [x] Implement recursive file/directory traversal
- [x] Add include/exclude pattern support
- [ ] Integrate `.gitignore` and custom ignore files

### 3. Output and Usability
- [x] Show N lines before/after matches (context)
- [ ] Highlight matches in color
- [ ] Add syntax highlighting for code files
- [ ] Output results as plain text, JSON, CSV, or Markdown

### 4. Archive and Package Support
- [ ] Detect and open archives (.zip, .tar, etc.)
- [ ] Search inside Python packages (.whl, .egg)
- [ ] Search inside Java/.NET packages (.jar, .nupkg)
- [ ] Optionally search inside installed Python packages and `node_modules`

### 5. Interactive and Batch Replace Modes
- [ ] Implement interactive review of matches
- [ ] Allow opening/editing files from results
- [ ] Add batch search-and-replace functionality
- [ ] Support piping input/output

### 6. Advanced Search Features
- [x] Regex search
- [x] Fuzzy search
- [x] Case-insensitive and whole-word options
- [ ] Add syntax-aware search (e.g., only in comments/strings)
- [ ] Implement parallel/multithreaded search for large projects
- [ ] Presets and reusable search patterns

### 7. Integration and API
- [ ] Provide a Python API for scripting
- [ ] Add hooks/integration for popular editors/IDEs

### 8. Robustness & Professionalism
- [ ] Write user and developer documentation
- [ ] Create unit and integration tests for all modules
- [x] Ensure cross-platform compatibility (Windows, Linux, macOS)
- [ ] Provide easy installation instructions

---

## ✨ Current Features

- **Modern TUI** with theme support and persistent error dialogs
- **Recursive search** with include/exclude globs
- **Regex, fuzzy, and whole-word search** options
- **Context lines** before/after matches
- **Robust error handling** and user-friendly dialogs
- **Cross-platform** support (Windows, Linux, macOS)
- **John Wick import resolver** for reliable imports

---

## 🛣️ Roadmap & Next Steps

- [ ] Match highlighting in TUI
- [ ] Syntax highlighting for code files
- [ ] Export results (plain text, JSON, CSV, Markdown)
- [ ] `.gitignore` and custom ignore file support
- [ ] Interactive review and batch replace
- [ ] Archive/package search
- [ ] Python API and editor integration
- [ ] Documentation, tests, and easy install

---

## ⚡️ Performance & Algorithms

- **Core performance-critical functions** (such as the main search loop, fuzzy matching, and batch replace) will be implemented or accelerated using **Cython** to generate `.c` files for maximum speed.
- We use or build optimized algorithms for:
  - Fuzzy search (e.g., Levenshtein distance, string similarity)
  - Pattern matching and scoring
  - Tokenization for syntax-aware search
- Where possible, we leverage existing high-performance libraries (like `rapidfuzz`) and only implement our own algorithms when necessary.
- All performance-critical code is organized in an `algorithms/` or `utils/` module, not a traditional math module, since the focus is on string processing and search algorithms.

---

## Why Use Greaper?

- Fuzzy and regex search in one tool
- Colorized, context-rich output (coming soon)
- Search inside archives and package files (.zip, .tar, .whl, .egg, .jar, .nupkg, etc.)
- Optionally search inside installed Python packages and node_modules
- Ignore patterns and .gitignore support (coming soon)
- Interactive and batch replace modes (planned)
- Output as JSON, CSV, or Markdown (planned)
- Syntax-aware search for codebases (planned)
- Modern, interactive terminal UI powered by [Textual](https://github.com/Textualize/textual)
- And more!

---

## License

MIT License

---

## Author

Wesley Alexander Houser

---

## Directory Structure

greaper/
│
├── greaper/                        # Main package
│   ├── __init__.py
│   ├── cli.py                      # Command-line interface
│   ├── gui_textual.py              # Textual TUI interface
│   ├── core.py                     # Core search logic (calls Cython where needed)
│   ├── filewalker.py               # File/directory traversal, ignore/include logic
│   ├── output.py                   # Output formatting (plain, JSON, CSV, Markdown)
│   ├── archive.py                  # Archive/package support (.zip, .tar, .whl, etc.)
│   ├── integration.py              # Integration and batch replace logic
│   ├── syntax.py                   # Syntax-aware search/tokenization
│   ├── utils.py                    # General helpers (timing, logging, etc.)
│   └── algorithms/                 # Algorithms for fuzzy, scoring, etc.
│       ├── __init__.py
│       ├── fuzzy.py                # Fuzzy matching (Levenshtein, etc.)
│       └── tokenization.py         # Tokenization for syntax-aware search
│
├── cython_ext/                     # Cython/C extensions for speed
│   ├── __init__.py
│   ├── search_cython.pyx           # Cython-accelerated search loop
│   ├── fuzzy_cython.pyx            # Cython-accelerated fuzzy matching
│   └── replace_cython.pyx          # Cython-accelerated batch replace
│
├── tests/                          # Unit and integration tests
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_filewalker.py
│   ├── test_output.py
│   ├── test_archive.py
│   ├── test_interactive.py
│   ├── test_syntax.py
│   └── test_algorithms.py
│
├── greaper_theme.css               # Default Textual CSS theme
├── README.md
├── LICENSE
├── setup.py                        # For pip install
├── pyproject.toml                  # For modern builds
└── requirements.txt

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release notes.
