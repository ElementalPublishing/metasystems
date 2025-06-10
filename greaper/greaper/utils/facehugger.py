from greaper.integraton import hf_summarize_code

def summarize_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    return hf_summarize_code(code)

def summarize_project(folder):
    # Walk all .py files, summarize each, return dict of {filename: summary}
    import os
    summaries = {}
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                summaries[path] = summarize_file(path)
    return summaries