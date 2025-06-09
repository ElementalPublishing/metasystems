# GREAPER Theme Hot-Swap Roadmap

## Goal

Implement a robust, professional, and instant theme hot-swap feature in GREAPER’s TUI.  
Users can press `Ctrl+T` to cycle through available themes, and the UI updates colors immediately—no restart, no lag.

---

## Milestones

### 1. **Define Theme Variables**
- [ ] Refactor `greaper_theme.css` to use CSS variables for all theme colors.
- [ ] Ensure all color values in the CSS reference variables (e.g., `var(--primary)`).

### 2. **Theme Data Structure**
- [ ] Store all theme color values in a Python dictionary (`THEMES`) in `gui_textual.py`.

### 3. **Theme Swap Logic**
- [ ] Add a key binding for `Ctrl+T` to trigger theme swap.
- [ ] Implement cycling through themes in Python.

### 4. **Live CSS Variable Update**
- [ ] On theme swap, update CSS variables at runtime using Textual’s API.
- [ ] Ensure all widgets and containers update their colors instantly.

### 5. **User Feedback**
- [ ] Show a notification or animation when the theme changes.

### 6. **Testing**
- [ ] Test theme swap on all supported platforms (Windows, macOS, Linux).
- [ ] Verify no visual glitches or lag during theme change.

### 7. **Documentation**
- [ ] Document the feature in the README and help screens.
- [ ] List available themes and how to add new ones.

---

## Stretch Goals

- [ ] Allow users to create and save custom themes.
- [ ] Add animated transitions between themes.
- [ ] Support for light/dark mode auto-switching.

---

## Implementation Notes

- Use Textual’s `styles.set_variable()` or equivalent to update CSS variables at runtime.
- Keep theme logic centralized for maintainability.
- Ensure accessibility and readability for all color schemes.

---

## Owner

- Feature lead: [Your Name]
- Reviewers: [Team/Contributors]

---

## Status

- **Not Started**
