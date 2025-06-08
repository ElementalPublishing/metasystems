# Changelog

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
