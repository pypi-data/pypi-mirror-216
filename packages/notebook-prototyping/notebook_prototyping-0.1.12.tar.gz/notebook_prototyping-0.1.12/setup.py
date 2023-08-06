from setuptools import setup, find_packages


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()


import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='notebook_prototyping',
    version=get_version("src/notebook_prototyping/__init__.py"),
    license='MIT',
    author="Reitze Jansen",
    author_email='rlh.jansen@outlook.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # packages=find_packages('src'),
    # package_dir={'': 'src'},
    url='https://github.com/rlhjansen/nbprototyping',
    keywords='jupyter notebook, tooling',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=['jupyter', 'ipynbname', 'ast-comments']
)