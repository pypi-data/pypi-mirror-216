from setuptools import setup

def get_long_description(path):
    """Opens and fetches text of long descrition file."""
    with open(path, 'r') as f:
        text = f.read()
    return text

setup(
    name = 'pywinstyles',
    version = '1.1',
    description = " Customize window styles in windows 11",
    license = "Creative Commons Zero v1.0 Universal",
    readme = "README.md",
    long_description = get_long_description('README.md'),
    long_description_content_type = "text/markdown",
    author = 'Akash Bora',
    url = "https://github.com/Akascape/py-window-styles",
    classifiers = [
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords = ['window-styles', 'customtkinter', 'tkinter', 'python-window',
                'gui', 'python-gui', 'pyqt', 'title-bar', 'title-bar-color'],
    packages = ["pywinstyles"],
    python_requires = '>=3.8',
)
