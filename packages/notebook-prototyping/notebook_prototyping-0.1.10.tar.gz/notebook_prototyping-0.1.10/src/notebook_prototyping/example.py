import os

from notebook_import import import_notebook, convert_to_module
import second_example as se
import ipynbname

class Foo:
    """
    docstring
    """
    # comment

    def __init__(self):
        """another docstring"""
        print('initialized class')
        # another comment
        tnb = import_notebook('second_example')
        print('second notebook name:', tnb.snn)
        print('nested import function calls are possible, but do you really want it?', tnb.te.foobar())
        self.value = tnb.bar()