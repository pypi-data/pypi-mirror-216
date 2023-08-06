from setuptools import setup, find_packages
from featurelayers.__version__ import __version__


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# test
setup(
    name='featurelayers',
    version=__version__,
    description='FeatureLayers Package',
    author='khengyun',
    author_email='khaangnguyeen@email.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        'scipy',
        'tensorflow',
        'keras',
        'scipy',
        'rich',
        'matplotlib',
        'scikit-learn',
        'graphviz',
        'pydot',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
