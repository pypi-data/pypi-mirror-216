from setuptools import setup, find_packages


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='notebook_prototyping',
    version='0.1.4',
    license='MIT',
    author="Reitze Jansen",
    author_email='rlh.jansen@outlook.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # packages=find_packages('src'),
    # package_dir={'': 'src'},
    url='https://github.com/rlhjansen/nbprototyping',
    keywords='jupyter notebook tooling',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['jupyter', 'ipynbname', 'ast-comments']
)