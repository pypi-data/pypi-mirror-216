from setuptools import setup

def get_long_description(path):
    """Opens and fetches text of long descrition file."""
    with open(path, 'r') as f:
        text = f.read()
    return text

setup(
    name = 'CTkTable',
    version = '0.6',
    description = "Customtkinter Table widget",
    license = "MIT",
    readme = "README.md",
    long_description = get_long_description('README.md'),
    long_description_content_type = "text/markdown",
    author = 'Akash Bora',
    url = "https://github.com/Akascape/CTkTable",
    classifiers = [
        "License :: OSI Approved :: MIT License ",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords = ['customtkinter', 'tkinter', 'table-widget', 'table',
                'ctktable', 'tabular-data', 'customtkinter-table'],
    packages = ["CTkTable"],
    install_requires = ['customtkinter'],
    dependency_links = ['https://pypi.org/project/customtkinter/'],
    python_requires = '>=3.6',
)
