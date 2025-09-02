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

If using a system that supports Make, you can run the following command to build the documentation and serve locally:

```sh
make live
```

## Adding Content

To add content to the documentation, create a new markdown or rst file in the `docs` directory. You can use the existing files as templates for your new content.

The main entry point for the documentation is `index.rst`. You can add new sections by creating new markdown or rst files and linking them in the `index.rst` file or within one of the existing sections.

## Adding to an existing Section

There are three main sections in the documentation: examples, help, and faq.

### Examples / Integrations

Adding to the examples section is done by creating a new markdown file in the `docs/examples` directory. You can then link to this file from the `index.rst` (or `index.md`, depending on your Sphinx configuration) in that directory. Ensure the format matches your project's configuration for consistency.

### Help / Downloads / Tutorials

To edit the help section, you can modify the `docs/help/index.md` file. This file contains the contact information and links to the main website. Additional files can be added in this directory and linked back to the main `index.md` page.

### FAQs

To add or edit FAQ entries, modify the `docs/faq/index.md` file. You can add new questions and answers in markdown format, following the structure of the existing entries.


## Resources

This documentation is built using Sphinx and the PyData Theme. You can find more information about how to use the theme using the following link:
- [PyData Sphinx Theme Documentation](https://pydata-sphinx-theme.readthedocs.io/en/stable/)

## Deployment

This documentation can be deployed using GitHub Pages or any other static site hosting service. To deploy using GitHub Pages, follow these steps:

1. Push your changes to the `main` branch of your repository. *Note:* We often require a Pull Request to be approved before this Push.
2. The GitHub Actions workflow will automatically build and deploy your documentation. *See:* `.github/workflows/wiki.yml`
3. Your documentation will be available at `https://support.wearablesensing.com`.

The CNAME file should contain the following line:

```
support.wearablesensing.com
```

While this can be changed in the repository settings, it is recommended to keep it in the CNAME file to prevent any issues with custom domain resolution when deploying the documentation next.
