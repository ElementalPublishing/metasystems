"""
Banner Enforcer Utility

- Reads input.txt from greaper/ASCII/
- Converts it to ASCII art using pyfiglet
- Inserts the ASCII art as a CSS comment at the top of greaper_theme.css
"""

import os
import sys

try:
    from pyfiglet import Figlet
except ImportError:
    print("pyfiglet is required. Install with: pip install pyfiglet")
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(__file__))
ASCII_DIR = os.path.join(ROOT, "ASCII")
CSS_PATH = os.path.join(ROOT, "greaper_theme.css")
INPUT_TXT = "input.txt"
BANNER_TXT_PATH = os.path.join(ROOT, "banner.txt")

def get_ascii_txt_file():
    path = os.path.join(ASCII_DIR, INPUT_TXT)
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def inject_banner_to_css(ascii_art):
    # Read existing CSS
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            css = f.read()
    else:
        css = ""
    # Remove any previous banner comment (between /* ASCII BANNER START */ and /* ASCII BANNER END */)
    import re
    css = re.sub(
        r"/\* ASCII BANNER START \*/.*?/\* ASCII BANNER END \*/\n?",
        "",
        css,
        flags=re.DOTALL,
    )
    # Prepare new banner comment
    banner_comment = "/* ASCII BANNER START */\n" + "\n".join(f" * {line}" for line in ascii_art.splitlines()) + "\n/* ASCII BANNER END */\n"
    # Insert at the top
    css = banner_comment + css.lstrip()
    # Write back
    with open(CSS_PATH, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"Banner injected into {CSS_PATH}")

def save_ascii_art(ascii_art):
    with open(BANNER_TXT_PATH, "w", encoding="utf-8") as f:
        f.write(ascii_art)
    print(f"Banner ASCII art saved to {BANNER_TXT_PATH}")

def main():
    font = "standard"
    plain_text = get_ascii_txt_file()
    figlet = Figlet(font=font)
    ascii_art = figlet.renderText(plain_text)
    inject_banner_to_css(ascii_art)
    save_ascii_art(ascii_art)
    print(ascii_art)

if __name__ == "__main__":
    main()