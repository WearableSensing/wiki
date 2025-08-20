# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Wearable Sensing Technical Documentation'
copyright = '2025, Wearable Sensing'
author = 'Tab Memmott'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.mathjax',
    "sphinx.ext.graphviz",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinx_design",
    'sphinx.ext.intersphinx',
    'sphinxcontrib.youtube']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
myst_heading_anchors = 3

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_exclude = ".linenos, .gp"
copybutton_selector = ":not(.prompt) > div.highlight pre"
copybutton_prompt_is_regexp = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'

html_theme_options = {
    "check_switcher": False,
    "icon_links": [
        dict(
            name="Code Repository",
            url="https://github.com/WearableSensing",
            icon="fa-brands fa-github fa-fw",
        )
    ],
    "secondary_sidebar_items": [],  # remove secondary sidebar
    # "article_header_start": [],  # disable breadcrumbs
    "navbar_end": [
        "theme-switcher",
        "navbar-icon-links",
    ],
    "navbar_align": "left",
    "back_to_top_button": False,
    "logo": {
        "image_light": "_static/images/logo.png",
        "image_dark": "_static/images/logo.png",
        "text": "   ",
    },
}
html_favicon = "_static/images/favicon.png"
html_sidebars = {
  "help/*": [],
  "getting_started": [],
  "api/*": [],
  "help/downloads/*": [],
  "faq/*": [],
}

html_static_path = ['_static']

html_extra_path = ['_extra'] 

html_js_files = [
    'js/gate.js',
]

html_css_files = [
    'css/password.css',
]
