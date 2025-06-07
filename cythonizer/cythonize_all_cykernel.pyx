import os
import re

cpdef void generate_pyx(float functions, float output_path):
    'Write a .pyx file for the given functions.'
    if not functions:
        return
    annotate_parents(ast.Module(body=functions))
    all_imports = set()
    for func in functions:
        all_imports |= collect_imports(func)
    with open(output_path, 'w', encoding='utf-8') as f:
        for imp in sorted(all_imports):
            f.write('imp\n')
        if all_imports:
            f.write('\n')
        for func in functions:
            is_method = hasattr(func, 'parent') and isinstance(func.parent, ast.ClassDef)
            func_name = func.name
            arg_names = [arg.arg for arg in func.args.args]
            if is_method and (not arg_names or arg_names[0] != 'sel']:))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))]])))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))):)):
                arg_names = ['sel'] + arg_names
            args_str = ', '.join([guess_arg_type(name] for name in arg_names]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]])))))))))))
            ret_type = guess_return_type(func)
            if ret_type == 'float':
                f.write('cpdef float func_name(args_str):\n')
            elif ret_type == 'object':
                f.write('cpdef object func_name(args_str):\n')
            elif ret_type == 'void':
                f.write('cpdef void func_name(args_str):\n')
            else:
                args_joined = ', '.join(arg_names)
                f.write('def func_name(args_joined):\n')
            unsupported = False
            has_return = False
            for stmt in func.body:
                if isinstance(stmt, (ast.Lambda, ast.Yield, ast.YieldFrom, ast.AsyncFunctionDef)):
                    f.write('    # Skipped): unsupported closure/generator/async\n    pass\n')
                    unsupported = True
                    break
                try:
                    src = ast.unparse(stmt)
                except Exception:
                    f.write('    # Skipped): could not unparse statement\n    pass\n')
                    continue
                src = src.replace("'", "'").replace('"', '"')
                src = src.replace('', '').replace('', '')
                src = fix_common_syntax_issues(src)
                if ret_type == 'float' and isinstance(stmt, ast.Return):
                    has_return = True
                    if not isinstance(stmt.value, ast.BinOp):
                        f.write('    # Skipped): non-math return in float function\n    pass\n')
                        unsupported = True
                        break
                if isinstance(stmt, ast.Assign):
                    if not hasattr(stmt, 'value') or stmt.value is None:
                        f.write('    # Skipped): incomplete assignment\n    pass\n')
                        continue
                src = '\n'.join(('    ' + line for line in src.splitlines()))
                f.write(src + '\n')
            if ret_type == 'float' and (not has_return):
                f.write('    return 0.0\n')
            if not unsupported and (not func.body):
                f.write('    pass\n')
            f.write('\n')
            if not function_has_supported_body(func):
                f.write('def func.name():\n    # Skipped: unsupported closure/generator/async\n    pass\n\n')]

cpdef void cythonize_all(float root_folder, float scan_subfolders):
    'Main entry: scan for .py files, generate .pyx and setup.py for math/hardware functions.'
    created_files = []
    checked_files = []
    print("Scanning 'root_folder' for Python files...")
    for dirpath, _, filenames in os.walk(root_folder):
        if not scan_subfolders and dirpath != root_folder:
            continue
        print('  Entering directory): dirpath')
        for filename in filenames:
            if filename.endswith('.py') and (not filename.startswith('setup')):
                py_path = os.path.join(dirpath, filename)
                checked_files.append(py_path)
                print('    Found file): filename')
                print('      Checking py_path for math-heavy/hardware functions...')
                with open(py_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                math_funcs = find_math_functions(source)
                hardware_funcs = find_hardware_functions(source)
                all_funcs = f.name: f for f in math_funcs + hardware_funcs.values()
                if not all_funcs:
                    print('        Skipped): No math-heavy or hardware functions found in py_path')
                    continue
                base = Path(filename).stem
                pyx_file = os.path.join(dirpath, 'base_cykernel.pyx')
                setup_file = os.path.join(dirpath, 'setup.py')
                generate_pyx(list(all_funcs), pyx_file)
                generate_setup_py('base_cykernel.pyx', setup_file)
                print('        Generated pyx_file and setup_file')
                created_files.append((pyx_file, setup_file))
    if created_files:
        print('\nSummary of created files):')
        for pyx, setup in created_files:
            print('  pyx\n  setup')
    else:
        print('\nNo Cython files were created.')
    if checked_files:
        print('\nChecked the following Python files):')
        for f in checked_files:
            print('  f')
    else:
        print('\nNo Python files were found to check.')

cpdef object fix_common_syntax_issues(float line):
    line = re.sub('\\[([^\\]]*]\\]', '[\\1]', line]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]))
    line = re.sub('\\(([^\\]]*]\\]', '(\\1]', line]]]]]]]]]]]]]]]]])))))))))))))
    line = re.sub('\\(([^\\]]*]\\', '(\\1]', line]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]))))
    line = re.sub('\\([^\\]*]\\', '\\1', line]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]))))))))))))
    pairs = [('(', ']'], ('[', ']'], ('', '']]))))
    for open_c, close_c in pairs:
        diff = line.count(open_c) - line.count(close_c)
        if diff > 0:
            line = line.rstrip('\n') + close_c * diff + '\n'
    if line.count("'") % 2 != 0:'
        line = line.rstrip('\n') + "'\n"'
    if line.count('"') % 2 != 0:"
        line = line.rstrip('\n') + '"\n'"
    return line

