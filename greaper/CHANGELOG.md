# Changelog

## [v1.2.0] - 2025-06-08

### Added
- Cython-accelerated fuzzy search backend with automatic Python fallback
- Utilities system: dynamic discovery and execution of utilities from both CLI and TUI
- TUI "Utilities" menu for running any utility in the `utils` folder
- Import fixer utility for auto-resolving and fixing broken imports across the codebase
- Advanced tokenization with robust regex for Python/C/JavaScript strings and comments
- Improved error modals and notifications in TUI
- Theme switching and persistent theme support in TUI
- Integration with CLI for launching TUI (`--tui` flag)
- Unit test for TUI startup and output capture

### Changed
- Refactored TUI (`gui_textual.py`) for modularity and easier extension
- Updated tokenization regex to fix syntax errors and support triple-quoted strings
- Improved backend detection and notification for fuzzy search (Cython vs Python)
- Enhanced CLI and TUI to share backend logic and options
- Improved import management and absolute import usage throughout the codebase

### Fixed
- Syntax error in tokenization regex for triple-double-quoted strings
- Import errors when running as a module or script
- Removed improper use of `await` with synchronous `.focus()` method in TUI
- Fixed theme selection and style updates in TUI
- Fixed CLI and TUI integration with new backend and utility features

---

## [v1.1.0] - 2025-06-08

### Added
- Integration functions for VS Code, Sublime Text, JetBrains IDEs, Vim/Neovim, and Emacs
- Export functions for JSON, CSV, and Markdown for reporting and data science
- CLI `export` command to generate results in any supported format
- Syntax-aware search and export support in CLI and integrations
- Improved interactive CLI for export and search with all advanced options

### Changed
- Refactored CLI to support export workflows and editor/tool integration
- Enhanced modularity and extensibility of integration layer

### Fixed
- CLI and backend now fully support all advanced search and export options
- Fixed theme selection bug in GUI when using syntax mode select

---

## [v1.0.0] - 2025-06-08

### Added
- Modern TUI with theme support and persistent error modals
- Recursive file/directory search with include/exclude globs
- Regex, fuzzy, and whole-word search options
- Context lines before/after matches
- Robust error handling and user-friendly dialogs
- Cross-platform support (Windows, Linux, macOS)
- John Wick import resolver for reliable imports

### Changed
- Improved backend/frontend integration for seamless user experience

### Fixed
- Markup errors in footer text
- Import errors with dynamic path resolution

---
