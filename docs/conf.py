# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Kumiko"
copyright = "2026, No767"
author = "No767"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_design", "sphinxext.opengraph", "sphinx_copybutton"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_title = "Kumiko"
html_favicon = "/_static/public/favicon.svg"


# -- Open Graph (OGP) options ------------------------------------------------
# https://sphinxext-opengraph.readthedocs.io/en/latest/

ogp_site_name = "Kumiko Documentation"
ogp_description_length = 130
ogp_type = "website"

ogp_custom_meta_tags = [
    '<link rel="icon" type="image/png" href="/_static/public/favicon-96x96.png" sizes="96x96" />'
    '<link rel="icon" type="image/svg+xml" href="/_static/public/favicon.svg" />',
    '<link rel="shortcut icon" href="/_static/public/favicon.ico" />',
    '<link rel="apple-touch-icon" sizes="180x180" href="/_static/public/apple-touch-icon.png" />',
    '<meta name="apple-mobile-web-app-title" content="Kumiko Documentation" />',
    '<link rel="manifest" href="/_static/public/site.webmanifest" />',
]

ogp_social_cards = {
    "enable": True,
    "image": "./_images/kumiko-resized-round.png",
    "line_color": "#FFABE1",
}


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
