'''

Support widgets

'''


import os.path as path
import glob
modules = glob.glob(path.join(path.dirname(__file__), "*.py"))
__all__ = [ path.basename(f)[:-3] for f in modules if path.isfile(f) and not f.endswith('__init__.py')]
