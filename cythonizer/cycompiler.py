import os
import re
import subprocess

def compile_all_pyx(root_folder, scan_subfolders=True):
    compiled = []
    skipped = []
    skip_reasons = {}
    found_any = False
    print(f"Scanning '{root_folder}' for .pyx files to compile...")
    for dirpath, _, filenames in os.walk(root_folder):
        if not scan_subfolders and dirpath != root_folder:
            continue
        print(f"  Entering directory: {dirpath}")
        for filename in filenames:
            if filename.endswith('.pyx'):
                found_any = True
                pyx_path = os.path.join(dirpath, filename)
                setup_path = os.path.join(dirpath, 'setup.py')
                print(f"    Found .pyx file: {filename}")
                if os.path.exists(setup_path):
                    print(f"      Compiling {filename} using setup.py...")
                    result = subprocess.run(
                        ['python', 'setup.py', 'build_ext', '--inplace'],
                        cwd=dirpath,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        print(f"        Success: {filename} compiled.")
                        compiled.append(pyx_path)
                    else:
                        print(f"        Error compiling {filename}:\n{result.stderr}")
                        print(f"        Stdout:\n{result.stdout}")
                        skipped.append(pyx_path)
                        stderr = result.stderr.strip()
                        # Error pattern matching
                        if "Python headers needed" in stderr:
                            reason = "Missing Python development headers"
                        elif "Cython requires Python 3.8+" in stderr:
                            reason = "Python version too old for Cython"
                        elif "undeclared name not builtin" in stderr:
                            match = re.search(r"undeclared name not builtin: (\w+)", stderr)
                            reason = f"Undeclared name: {match.group(1)}" if match else "Undeclared name"
                        elif "syntax error" in stderr:
                            reason = "Syntax error in .pyx file"
                        elif "No module named" in stderr:
                            match = re.search(r"No module named '([^']+)'", stderr)
                            reason = f"Missing module: {match.group(1)}" if match else "Missing module"
                        elif "Return with value in void function" in stderr:
                            match = re.search(r"([^\s:]+\.pyx):(\d+):(\d+): Return with value in void function", stderr)
                            if match:
                                fname, lineno, col = match.groups()
                                reason = f"Return with value in void function at {fname}:{lineno}:{col}"
                            else:
                                reason = "Return with value in void function"
                        elif "Expected an identifier or literal" in stderr:
                            reason = "Expected identifier or literal (likely invalid syntax)"
                        elif "empty expression not allowed in f-string" in stderr or "missing '}' in format string expression" in stderr:
                            reason = "Invalid or empty expression in f-string"
                        elif "Expected ')'" in stderr or "Expected '('" in stderr:
                            reason = "Mismatched parentheses"
                        elif "Expected ':'" in stderr:
                            reason = "Expected colon (likely missing after if/for/def/class)"
                        elif "Cannot assign to" in stderr:
                            reason = "Invalid assignment"
                        elif stderr:
                            match = re.search(r"([^\s:]+\.pyx:\d+:\d+: .+)", stderr)
                            reason = match.group(1) if match else stderr.splitlines()[0]
                        else:
                            reason = "Unknown error"
                        skip_reasons[pyx_path] = reason
                else:
                    print(f"      Skipped: No setup.py found for {filename}.")
                    skipped.append(pyx_path)
                    skip_reasons[pyx_path] = "No setup.py found"
    if not found_any:
        print("No .pyx files found in the specified directory.")

    print("\nSummary Table:")
    print(f"{'Compiled':<50} | {'Skipped/Failed':<50} | Reason")
    print("-" * 130)
    max_len = max(len(compiled), len(skipped))
    for i in range(max_len):
        left = compiled[i] if i < len(compiled) else ""
        right = skipped[i] if i < len(skipped) else ""
        reason = skip_reasons.get(right, "") if right else ""
        print(f"{left:<50} | {right:<50} | {reason}")

if __name__ == "__main__":
    scan = input("Are there subfolders to scan for .pyx files? (y/n): ").strip().lower()
    scan_subfolders = scan == "y"
    compile_all_pyx(".", scan_subfolders)
