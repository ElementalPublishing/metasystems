import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import sys
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "pypi_installs.db")

def get_packages():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT package_name FROM install_commands")
    packages = [row[0] for row in cur.fetchall()]
    conn.close()
    return packages

def pip_action(package, action):
    try:
        if action == "install":
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            messagebox.showinfo("Success", f"Installed {package}")
        elif action == "uninstall":
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])
            messagebox.showinfo("Success", f"Uninstalled {package}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to {action} {package}:\n{e}")

def refresh_listbox():
    listbox.delete(0, tk.END)
    for pkg in get_packages():
        listbox.insert(tk.END, pkg)

def on_install():
    selected = listbox.curselection()
    if selected:
        pkg = listbox.get(selected[0])
        pip_action(pkg, "install")

def on_uninstall():
    selected = listbox.curselection()
    if selected:
        pkg = listbox.get(selected[0])
        pip_action(pkg, "uninstall")

root = tk.Tk()
root.title("PyPI Package Installer/Uninstaller")

listbox = tk.Listbox(root, width=40, height=15)
listbox.pack(padx=10, pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

install_btn = tk.Button(btn_frame, text="Install", command=on_install)
install_btn.pack(side=tk.LEFT, padx=5)

uninstall_btn = tk.Button(btn_frame, text="Uninstall", command=on_uninstall)
uninstall_btn.pack(side=tk.LEFT, padx=5)

refresh_btn = tk.Button(btn_frame, text="Refresh", command=refresh_listbox)
refresh_btn.pack(side=tk.LEFT, padx=5)

refresh_listbox()
root.mainloop()