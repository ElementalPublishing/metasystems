import os
import re
import time

def fix_lines(lines, verbose=False, loop_issues=None, filename=None):
    fixed_lines = []
    imports = set()
    used_imports = set()
    needed_imports = {
        "np.": "import numpy as np\n",
        "pd.": "import pandas as pd\n",
        "sp.": "import scipy as sp\n",
        "re.": "import re\n",
        "time.": "import time\n",
        "os.": "import os\n",
        "sys.": "import sys\n",
        "urlparse": "from urllib.parse import urlparse\n",
        "as_completed": "from concurrent.futures import as_completed\n",
        "ThreadPoolExecutor": "from concurrent.futures import ThreadPoolExecutor\n",
        "RobotsRules": "from .robots_rules import RobotsRules\n",
    }

    total_lines = len(lines)
    for idx, line in enumerate(lines):
        # Skip already marked loop issue lines
        if line.strip() == "# LOOP ISSUE: see summary below":
            fixed_lines.append(line)
            continue

        # Track used imports
        for key, imp in needed_imports.items():
            if key in line:
                used_imports.add(imp)

        # Remove duplicate imports
        if line.strip().startswith("import ") or line.strip().startswith("from "):
            if line in imports or line in used_imports:
                continue
            imports.add(line)

        # --- Aggressive line-by-line fixing ---
        seen = []
        for pass_num in range(1, 121):
            orig_line = line

            # Skip already marked loop issue lines (in case it gets set during passes)
            if line.strip() == "# LOOP ISSUE: see summary below":
                break

            if verbose:
                print(f"  Line {idx+1}/{total_lines}, pass {pass_num}")

            # Fix invalid f-string in function signatures and bodies
            line = re.sub(r'f"def ([^(]+)\(\{[^\}]*\}\):"', r'def \1():', line)
            line = re.sub(r"f([\"'])(.*)\{([^}]*)\}(.*)([\"'])", r"\1\2{\3}\4\5", line)
            line = re.sub(r"f([\"'])(.*)\{([^}]*)\)(.*)([\"'])", r"\1\2{\3}\4\5", line)

            # Fix mismatched curly braces in f-strings or dicts
            line = re.sub(r"\{([^}]*)\)\)", r"{\1}}", line)
            line = re.sub(r"\{([^}]*)\)", r"{\1}", line)

            # Fix mismatched brackets and parentheses
            line = re.sub(r"\[([^\]]*)\)", r"[\1]", line)
            line = re.sub(r"\(([^\)]*)\)", r"(\1)", line)
            line = re.sub(r"\(([^\)]*)\}", r"(\1)", line)
            line = re.sub(r"\{([^\}]*)\}", r"{\1}", line)

            # Fix common missing parenthesis at end of function calls
            line = re.sub(r"(\w+\([^\)]*)\):", r"\1):", line)
            line = re.sub(r"(\w+\([^\)]*):", r"\1):", line)
            line = re.sub(r"(\([^\)]*):", lambda m: m.group(0) + ")" if m.group(0).count("(") > m.group(0).count(")") else m.group(0), line)

            # Fix missing colon at end of def/for/if/class
            line = re.sub(r"^( *)(def .+\))(\s*)$", r"\1\2:\3", line)
            line = re.sub(r"^( *)(for .+\))(\s*)$", r"\1\2:\3", line)
            line = re.sub(r"^( *)(if .+\))(\s*)$", r"\1\2:\3", line)
            line = re.sub(r"^( *)(class .+\))(\s*)$", r"\1\2:\3", line)

            # Replace bare 'run(' with 'subprocess.run(' if not already qualified
            line = re.sub(r'(?<!\w)run\(', 'subprocess.run(', line)

            # Aggressively balance parentheses/brackets/braces at line end
            for open_c, close_c in [("(", ")"), ("[", "]"), ("{", "}")] :
                diff = line.count(open_c) - line.count(close_c)
                if diff > 0:
                    line = line.rstrip("\n") + (close_c * diff) + "\n"

            # Aggressively balance quotes at line end
            if line.count("'") % 2 != 0:
                line = line.rstrip("\n") + "'\n"
            if line.count('"') % 2 != 0:
                line = line.rstrip("\n") + '"\n'

            # Remove or comment out incomplete assignments (e.g. "self.rules =")
            if re.match(r"^\s*\w[\w\.]*\s*=\s*$", line):
                line = "# Skipped: incomplete assignment\n"

            # Remove or comment out lines with only a colon or unmatched assignment
            if re.match(r"^\s*:\s*$", line) or re.match(r"^\s*=\s*$", line):
                line = "# Skipped: syntax error (dangling colon or equals)\n"

            # Loop detection: if we've seen this line before, mark and break
            if line in seen:
                last_versions = (seen + [line])[-4:]  # last 4 versions including current
                if loop_issues is not None and filename is not None:
                    loop_issues.append({
                        "file": filename,
                        "line_number": idx+1,
                        "pass_num": pass_num,
                        "versions": last_versions,
                        "original": orig_line
                    })
                if verbose:
                    print(f"LOOP DETECTED at line {idx+1}/{total_lines} (pass {pass_num})")
                    for i, v in enumerate(last_versions, 1):
                        print(f"  Version {-4 + i}: {repr(v)}")
                    print("  Original line:   ", repr(orig_line))
                # Only replace if not already marked
                if line.strip() != "# LOOP ISSUE: see summary below":
                    line = "# LOOP ISSUE: see summary below\n"
                break
            seen.append(line)

            if line == orig_line:
                break  # No more changes for this line

        fixed_lines.append(line)

    # Ensure 'import subprocess' is present if 'subprocess.run(' is used
    content = "".join(fixed_lines)
    if "subprocess.run(" in content and "import subprocess" not in content:
        fixed_lines.insert(0, "import subprocess\n")

    # Add all detected imports at the top, remove duplicates
    all_imports = sorted(set(imports) | used_imports)
    import_lines = [imp for imp in all_imports if imp not in content]
    fixed_content = "".join(import_lines) + "".join(fixed_lines)
    return fixed_content

def fix_pyx_file(filepath, max_passes=5000, loop_issues=None):
    with open(filepath, "r", encoding="utf-8") as f:
        old_content = f.read()
    lines = old_content.splitlines(keepends=True)
    print(f"{filepath}: {len(lines)} lines to process.")
    for i in range(max_passes):
        new_content = fix_lines(lines, verbose=True, loop_issues=loop_issues, filename=filepath)
        if new_content == old_content:
            print(f"{filepath}: Fixed in {i+1} passes.")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            return
        if (i+1) % 100 == 0:
            print(f"{filepath}: Pass {i+1} ...")
        old_content = new_content
        lines = old_content.splitlines(keepends=True)
    # If we get here, it's still looping after max_passes
    print(f"\nFATAL: {filepath} is stuck in an infinite loop after {max_passes} passes!")
    print("Writing last attempted content and continuing to next file...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return

def scan_and_fix_all_pyx(root_folder):
    loop_issues = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".pyx"):
                pyx_path = os.path.join(dirpath, filename)
                print(f"Fixing {pyx_path} ...")
                fix_pyx_file(pyx_path, loop_issues=loop_issues)
    print("\n=== SUMMARY OF LOOP ISSUES ===")
    if not loop_issues:
        print("No loop issues detected.")
    else:
        for issue in loop_issues:
            print(f"\nFile: {issue['file']}, Line: {issue['line_number']}, Pass: {issue['pass_num']}")
            for i, v in enumerate(issue['versions'], 1):
                print(f"  Version {-4 + i}: {repr(v)}")
            print(f"  Original: {repr(issue['original'])}")
    print("\nAuto-fix complete. Please re-run your Cython build.")

if __name__ == "__main__":
    scan_and_fix_all_pyx(".")