# https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html

import io, os, sys, types
import traceback

from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

import ast_comments as ast # https://github.com/t3rn0/ast-comments/tree/master
import ipynbname


def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """

    if fullname.endswith('.ipynb'):
        split_path = fullname.split('.')

        fullname = '.'.join([os.path.join(*split_path[:-1]), split_path[-1]])

    if fullname.endswith(".ipynb"):
        name = fullname.split(".ipynb")[0]
    else:
        name = fullname
    if not path:
        path = ''
    nb_path = os.path.join(path, name + ".ipynb")
    print(f"looking for notebook {nb_path}")
    if os.path.isfile(nb_path):
        return nb_path
    # let import Notebook_Name find "Notebook Name.ipynb"
    nb_path = nb_path.replace("_", " ")
    print(f"looking for notebook {nb_path}")
    if os.path.isfile(nb_path):
        return nb_path

    raise ValueError(f"could not find path {nb_path}")



def count_substring_occurences(substr, str_list, raise_recursion_error_at):
    count = 0
    for elem in str_list:
        if substr in elem:
            count += 1
    # print(count, len(str_list))

    if len(str_list) > raise_recursion_error_at:
        # print("\n".join(str_list))
        return len(str_list)

    return count


def import_notebook(fullname, path=None, raise_recursion_error_at=50):
    """import a notebook as a module

    still in development and currently vulnerable to endless recursion
    hardcoded / magic number stack depth to raise value error
    """
    stack_traceback = traceback.format_stack()
    count_self_calls = sum([count_substring_occurences(f"import_notebook({fullname},", stack_traceback, raise_recursion_error_at), \
                            count_substring_occurences(f"import_notebook({fullname})", stack_traceback, raise_recursion_error_at)])
    if count_self_calls > 1:
        raise ValueError(f"notebook {fullname} is likely imported recursively:\n\n{stack_traceback}")


    path = find_notebook(fullname, path)
    shell = InteractiveShell.instance()

    print ("importing Jupyter notebook from %s" % path)

    # load the notebook object
    with io.open(path, 'r', encoding='utf-8') as f:
        nb = read(f, 4)


    # create the module and add it to sys.modules
    # if name in sys.modules:
    #    return sys.modules[name]
    mod = types.ModuleType(fullname)
    mod.__file__ = path
    # mod.__loader__ = self
    mod.__dict__['get_ipython'] = get_ipython

    # extra work to ensure that magics that would affect the user_ns
    # actually affect the notebook module's ns
    save_user_ns = shell.user_ns
    shell.user_ns = mod.__dict__

    try:
        for cell in nb.cells:
            if cell.cell_type == 'code':
                # transform the input to executable Python
                code = shell.input_transformer_manager.transform_cell(cell.source)
                # run the code in themodule
                exec(code, mod.__dict__)
    finally:
        shell.user_ns = save_user_ns
    return mod



# class NotebookFinder(object):
#     """Module finder that locates Jupyter Notebooks"""
#     def __init__(self):
#         self.loaders = {}

#     def find_module(self, fullname, path=None):
#         nb_path = find_notebook(fullname, path)
#         if not nb_path:
#             return

#         key = path
#         if path:
#             # lists aren't hashable
#             key = os.path.sep.join(path)

#         if key not in self.loaders:
#             self.loaders[key] = NotebookLoader(path)
#         return self.loaders[key]



def convert_to_module(fullname, path=None, overwrite=False):
    """import a notebook as a module"""
    path = find_notebook(fullname, path)

    print ("converting Jupyter notebook from %s" % path)

    # load the notebook object
    with io.open(path, 'r', encoding='utf-8') as f:
        nb = read(f, 4)


    code_cell_contents = []
    all_imports = []

    try:
        for cell in nb.cells:
            if cell.cell_type == 'code':
                # transform the input to executable Python
                code, imports = strip_code(cell.source)
                code_cell_contents.append(code)
                all_imports.append(imports)
    except Exception as e:
        raise e


    # print(code_cell_contents)
    all_code = reformat_imports("\n".join(all_imports).split("\n")) + "\n\n" + \
        "\n\n".join([c for c in [ccc for ccc in code_cell_contents if ccc is not None] if c])

    # exclusion_line = f"NotebookConverter().convert_module('{fullname}', True)"
    # all_code = all_code.replace(exclusion_line, '')

    # exclusion_line = f'NotebookConverter().convert_module("{fullname}", True)'
    # all_code = all_code.replace(exclusion_line, '')


    new_filename = path.split(".ipynb")[0]+ ".py"

    if overwrite or not os.path.exists(new_filename):
        with open(new_filename, 'w+') as f:
            f.write(all_code)
    else:
        raise ValueError(f"converted file {new_filename} already exists")


def strip_code(cell_code) -> (str, list):
    parsed_ast = ast.parse(cell_code)
    stripped_code = []
    imports = []

    for node in parsed_ast.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            stripped_code.append(ast.unparse(node))

    return '\n\n'.join(stripped_code), "\n".join(imports)


def reformat_imports(import_list):
    stdlib_imports = []
    third_party_imports = []
    local_imports = []

    for import_line in import_list:
        if import_line.startswith('import') or import_line.startswith('from'):
            package_name = import_line.split()[1]
            if package_name.startswith(('os', 'sys', 'json')):
                stdlib_imports.append(import_line)
            elif package_name.startswith(('pandas', 'numpy', 'matplotlib', 'sklearn', 'torch', 'PIL')):
                third_party_imports.append(import_line)
            else:
                local_imports.append(import_line)

    reformatted_imports = []

    def format_import_lines(import_lines):
        formatted_lines = []
        imports = {}
        for import_line in import_lines:
            import_parts = import_line.split()
            module_name = import_parts[1]

            import_values = import_line
            if import_parts[0] == 'from':
                if 'as' in import_parts:
                    module_name = import_line
                else:
                    if module_name in imports:
                        import_values = " ".join(import_parts[3:])
                        # print("#", module_name, imports[module_name], import_values)
                    else:
                        import_values = import_line
                        # print("##", module_name, import_values)

            if module_name not in imports:
                imports[module_name] = []

            if not (import_values in imports[module_name]):
                outer_continue = False
                for i_v in imports[module_name]:
                    if import_values in i_v.split(' '):
                        print("sss", i_v.split(' '))
                        outer_continue = True
                if outer_continue:
                    # print("####", module_name, import_values)
                    continue
                imports[module_name].append(import_values)
                # print("###", module_name, import_values)
        for module_name, module_imports in imports.items():
            formatted_lines.append(', '.join(module_imports))
        return '\n'.join(formatted_lines)

    if stdlib_imports:
        reformatted_imports.append(format_import_lines(stdlib_imports))

    if third_party_imports:
        reformatted_imports.append(format_import_lines(third_party_imports))

    if local_imports:
        reformatted_imports.append(format_import_lines(local_imports))

    return '\n\n'.join(reformatted_imports)



def get_notebook_name():
    nb_fname = ipynbname.name()
    return nb_fname
