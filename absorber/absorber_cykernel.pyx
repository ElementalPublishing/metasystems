import os

cpdef object discover_systems():
# Skipped: incomplete assignment
    for fname in os.listdir(os.path.dirname(__file__)):
        if fname.endswith('.py') and fname not in ('mainframe.py', '__init__.py'):
            modname = fname[:-3]
            systems[modname] = modname
    return systems

