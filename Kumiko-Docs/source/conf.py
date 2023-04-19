# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Kumiko"
copyright = "2023, No767"
author = "No767"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.napoleon", "sphinxext.opengraph"]


templates_path = ["_templates"]
exclude_patterns = []

latex_elements = {
    "sphinxsetup": "verbatimwithframe=false",
}

html_title = "Kumiko"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

html_theme_options = {
    "dark_css_variables": {
        "color-brand-primary": "#A685E2",
        "color-brand-content": "#FFABE1",
    },
    "light_css_variables": {
        "color-brand-primary": "#6867AC",
        "color-brand-content": "#CE7BB0",
    },
}

ogp_site_url = "https://kumiko.readthedocs.io"
ogp_image = (
    "https://raw.githubusercontent.com/No767/Kumiko/dev/assets/kumiko-resized-round.png"
)
