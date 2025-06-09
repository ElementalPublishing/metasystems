# Greaper: Grep on Steroids

Greaper is a next-generation search tool for developers, data scientists, and power users.  
It combines the speed and flexibility of classic grep with modern features for code, data, and package search.  
Now with a modern TUI, robust error handling, Cython-accelerated algorithms, and an extensible architecture.

---

## 🚀 Goals & Milestones

### 1. Core CLI and Search Engine
- [x] Command-line interface (CLI) and help system
- [x] Regex and fuzzy search (Cython-accelerated if available)
- [x] Case-insensitive and whole-word options
- [x] Syntax-aware search (comments, strings, code)
- [x] Persistent and colorized output (TUI, CLI)
- [x] Python API for scripting

### 2. File & Directory Traversal
- [x] Recursive file/directory traversal
- [x] Include/exclude pattern support
- [ ] `.gitignore` and custom ignore files

### 3. Output and Usability
- [x] Context lines before/after matches
- [x] Highlight matches in color (TUI)
- [x] Syntax highlighting for code files (TUI)
- [x] Output as plain text, JSON, CSV, or Markdown
- [x] Export results for editors and data science

### 4. Archive and Package Support
- [x] Detect and open archives (.zip, .tar, etc.)
- [x] Search inside Python packages (.whl, .egg)
- [ ] Search inside Java/.NET packages (.jar, .nupkg)
- [ ] Optionally search inside installed Python packages and `node_modules`

### 5. Interactive and Batch Replace Modes
- [x] Interactive review of matches (TUI)
- [x] Open/edit files from results (TUI)
- [x] Batch search-and-replace functionality
- [x] Support piping input/output

### 6. Advanced Search Features
- [x] Regex, fuzzy, case-insensitive, and whole-word options
- [x] Syntax-aware search (comments, strings, code)
- [x] Parallel/multithreaded search for large projects
- [x] Presets and reusable search patterns

### 7. Integration and API
- [x] Python API for scripting
- [x] Hooks/integration for popular editors/IDEs (VS Code, Sublime, JetBrains, Vim, Emacs)
- [x] Export in editor-native formats

### 8. Robustness & Professionalism
- [x] User and developer documentation
- [x] Unit and integration tests for all modules
- [x] Cross-platform compatibility (Windows, Linux, macOS)
- [x] Easy installation instructions
- [x] Robust error handling and user-friendly dialogs

### 9. Utilities and Extensibility
- [x] Dynamic utilities system: run any utility in the `utils` folder from CLI or TUI
- [x] Import fixer utility for auto-resolving and fixing broken imports
- [x] John Wick import resolver for reliable imports

---

## ✨ Current Features

- **Modern TUI** with theme support, persistent error dialogs, and a dynamic Utilities menu
- **Recursive search** with include/exclude globs
- **Regex, fuzzy, and whole-word search** (Cython-accelerated if available)
- **Context lines** before/after matches
- **Syntax-aware search** for codebases (comments, strings, code)
- **Archive/package search** (.zip, .tar, .whl, .egg, etc.)
- **Robust error handling** and user-friendly dialogs
- **Cross-platform** (Windows, Linux, macOS)
- **Dynamic utilities system**: run any utility in the `utils` folder from CLI or TUI
- **Import fixer utility** for auto-resolving and fixing broken imports
- **John Wick import resolver** for reliable imports
- **Export results** as plain text, JSON, CSV, Markdown, or editor-native formats
- **Integration with VS Code, Sublime, JetBrains, Vim, Emacs, and more**

---

## 🛣️ Roadmap & Next Steps

- [ ] `.gitignore` and custom ignore file support
- [ ] More archive/package formats (e.g., .jar, .nupkg)
- [ ] Interactive review and batch replace in CLI
- [ ] More advanced syntax highlighting and code intelligence
- [ ] More editor integrations and plugins
- [ ] Documentation, tests, and easy install improvements

---

## ⚡️ Performance & Algorithms

- **Cython-accelerated core functions** (search loop, fuzzy matching, batch replace) for maximum speed
- Optimized algorithms for:
  - Fuzzy search (Levenshtein, string similarity)
  - Pattern matching and scoring
  - Tokenization for syntax-aware search
- Uses high-performance libraries (like `rapidfuzz`) where possible
- All performance-critical code is in `algorithms/` or `cython_ext/`

---

## Why Use Greaper?

- Fuzzy and regex search in one tool
- Colorized, context-rich output
- Search inside archives and package files (.zip, .tar, .whl, .egg, .jar, .nupkg, etc.)
- Optionally search inside installed Python packages and node_modules
- Ignore patterns and .gitignore support (coming soon)
- Interactive and batch replace modes
- Output as JSON, CSV, Markdown, or editor-native formats
- Syntax-aware search for codebases
- Modern, interactive terminal UI powered by [Textual](https://github.com/Textualize/textual)
- Dynamic utilities system for extensibility
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
│   ├── utils.py                    # Utility manager (dynamic discovery/execution)
│   ├── utils/                      # Folder for user and system utilities
│   │   ├── __init__.py
│   │   ├── imports.py              # Import fixer utility
│   │   └── ...                     # Other utilities
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

## Editor & Tool Integrations

- **VS Code**: Export search results in Problems panel format.
- **Sublime Text**: Export in Find Results format.
- **JetBrains IDEs**: Export in Find in Path format.
- **Vim/Neovim**: Export in quickfix format.
- **Emacs**: Export in compilation buffer format.
- **JSON/CSV/Markdown**: For scripting, reporting, and data science.

Use the CLI `export` command to generate output for your favorite tool!
