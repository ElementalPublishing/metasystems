import subprocess
import sys
import os

def run(cmd, check=True):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result

def check_uncommitted():
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("You have uncommitted changes. Please commit or stash them before proceeding.")
        sys.exit(1)

def regenerate_cython():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyx"):
                pyx_path = os.path.join(root, file)
                print(f"Regenerating C file for {pyx_path}")
                run(f"cython {pyx_path}")

def commit_all(msg):
    run("git add .", check=True)
    # Allow git commit to fail if there's nothing to commit
    try:
        run(f'git commit -m "{msg}"', check=True)
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in e.stderr or "nothing added to commit" in e.stderr:
            print("Nothing to commit.")
        else:
            raise

def tag_version(version):
    run(f"git tag {version}")
    run(f"git push origin {version}")

def build():
    run("python -m build --sdist --wheel --no-isolation")

def main():
    check_uncommitted()
    regenerate_cython()
    commit_all("Automated release commit by gitdestroyer")
    version = input("Enter new version tag (e.g., v2.2.0): ").strip()
    tag_version(version)
    build()
    print("\nAll done! Check your dist/ folder and upload to PyPI if desired.")

if __name__ == "__main__":
    main()