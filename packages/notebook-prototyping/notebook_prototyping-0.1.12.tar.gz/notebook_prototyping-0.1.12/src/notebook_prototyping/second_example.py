import os

from notebook_import import import_notebook, convert_to_module, get_notebook_name
import nested.directory.third_example as te

def bar():
    """dosctring"""
    # extra comment
    return 'baz'