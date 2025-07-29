# Wearable Sensing Techincal Documentation 

## Install

- Install Python. Current version used: [3.13](https://www.python.org/downloads/release/python-3130/)
- Create a virtualenv: `python -m venv .venv`
- Activate the virtualenv. On Windows: `.venv\Scripts\activate`
- Install the requirements: `pip install -r requirements.txt`

## Build

You can manually build the code from within the docs folder and then navidate to `index.html` using,
> `sphinx-build . _build`

A better approach is to use sphinx autobuild to spin up a server that re-builds everytime a file is added or changed in the docs directory.

```sh
sphinx-autobuild docs docs/_build
```

This should print several things to the terminal and if the build is scucceful a final message like this will appear where you can see the page,

> [sphinx-autobuild] Serving on http://127.0.0.1:8000

## Adding Content

To add content to the documentation, create a new markdown or rst file in the `docs` directory. You can use the existing files as templates for your new content.

The main entry point for the documentation is `index.rst`. You can add new sections by creating new markdown or rst files and linking them in the `index.rst` file or within one of the existing sections.

## Adding to an existing Section

There are three main sections in the documentation: Examples, Help, and API Reference.

Adding to the examples section is done by creating a new markdown file in the `docs/examples` directory. You can then link to this file from the `index.md` in that directory.

To edit the help section, you can modify the `docs/help/index.md` file. This file contains the contact information and links to the main website.

To add to the API reference, you can create a new markdown file in the `docs/api` directory. This will allow you to document your code and link it from the main API reference page.

## Resources

This documentation is built using Sphinx and the PyData Theme. You can find more information about how to use the theme using the following link:
- [PyData Sphinx Theme Documentation](https://pydata-sphinx-theme.readthedocs.io/en/stable/)
