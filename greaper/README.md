# Greaper: Grep on Steroids

Greaper is a next-generation search tool for developers, data scientists, and power users.  
It combines the speed and flexibility of classic grep with modern features for code, data, and package search.

---

## 🚀 Goals & Milestones

### 1. Core CLI and Search Engine
- [ ] Design command-line interface (CLI) and help system
- [ ] Implement basic regex search
- [ ] Add fuzzy search capability (using optimized algorithms)
- [ ] Support case-insensitive and whole-word options

### 2. File & Directory Traversal
- [ ] Implement recursive file/directory traversal
- [ ] Add include/exclude pattern support
- [ ] Integrate `.gitignore` and custom ignore files

### 3. Output and Usability
- [ ] Show N lines before/after matches (context)
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
- [ ] Add syntax-aware search (e.g., only in comments/strings)
- [ ] Implement parallel/multithreaded search for large projects
- [ ] Presets and reusable search patterns

### 7. Integration and API
- [ ] Provide a Python API for scripting
- [ ] Add hooks/integration for popular editors/IDEs

### 8. Robustness & Professionalism
- [ ] Write user and developer documentation
- [ ] Create unit and integration tests for all modules
- [ ] Ensure cross-platform compatibility (Windows, Linux, macOS)
- [ ] Provide easy installation instructions

---

## ⚡️ Performance & Algorithms

- **Core performance-critical functions** (such as the main search loop, fuzzy matching, and batch replace) will be implemented or accelerated using **Cython** to generate `.c` files for maximum speed.
- We will use or build optimized algorithms for:
  - Fuzzy search (e.g., Levenshtein distance, string similarity)
  - Pattern matching and scoring
  - Tokenization for syntax-aware search
- Where possible, we will leverage existing high-performance libraries (like `rapidfuzz`) and only implement our own algorithms when necessary.
- All performance-critical code will be organized in an `algorithms/` or `utils/` module, not a traditional math module, since the focus is on string processing and search algorithms.

---

## Why Use Greaper?

- Fuzzy and regex search in one tool
- Colorized, context-rich output
- Search inside archives and package files (.zip, .tar, .whl, .egg, .jar, .nupkg, etc.)
- Optionally search inside installed Python packages and node_modules
- Ignore patterns and .gitignore support
- Interactive and batch replace modes
- Output as JSON, CSV, or Markdown
- Syntax-aware search for codebases
- Modern, interactive terminal UI powered by [Textual](https://github.com/Textualize/textual)
- And more!

---

## License

MIT License

---

## Author

Wesley Alexander Houser
