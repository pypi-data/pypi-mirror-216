import sys
import functools
import subprocess

from metaflow.includefile import IncludeFile 
from metaflow.exception import MetaflowException

from typing import Dict

def write_to_disk(data: str, filename: str):
    with open(filename, mode='w+') as f:
        f.write(data)

# TODO: extras option, poetry add extra stuff 
# additonal_libraries: [library, version]
# dictionary of library name and version constraint
# make sure to supply constraint in version: ==, >=, @^, @~, @latest

def poetry(additional_libraries: Dict[str, str] = None, use_pypi: bool = True, local_module_dir: str = None):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, "lockfile"):
                write_to_disk(self.lockfile, "poetry.lock")
            write_to_disk(self.pyproject, "pyproject.toml")
            if(not use_pypi):
                subprocess.run(['poetry', 'source', 'add', '--priority=default', 'local', f'file:///{local_module_dir}'])
            if(additional_libraries):
                additional_libraries_str = ''
                for library, version in additional_libraries.items():
                    curr = f'{library}{version}'
                    additional_libraries_str = f'{additional_libraries_str} {curr}'
                subprocess.run(['poetry', 'add', additional_libraries_str.strip()])
            subprocess.run([sys.executable, '-m', 'poetry', 'install', '-C', 'pyproject.toml'])
            return function(self, *args, **kwargs)
        return wrapper
    return decorator

