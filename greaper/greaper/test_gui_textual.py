import subprocess
import sys
import json
from pathlib import Path

def run_and_log():
    script_path = Path(__file__).parent / "gui_textual.py"
    out_path = Path(__file__).parent / "gui_textual_output.json"

    proc = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True
    )

    result = {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr
    }

    # Optionally, parse tracebacks from stderr and add as a list
    tracebacks = []
    tb_lines = []
    in_tb = False
    for line in proc.stderr.splitlines():
        if line.startswith("Traceback (most recent call last):"):
            in_tb = True
            tb_lines = [line]
        elif in_tb and line.strip() == "":
            tracebacks.append("\n".join(tb_lines))
            in_tb = False
        elif in_tb:
            tb_lines.append(line)
    if tb_lines:
        tracebacks.append("\n".join(tb_lines))
    result["tracebacks"] = tracebacks

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Output and tracebacks written to {out_path}")

if __name__ == "__main__":
    run_and_log()