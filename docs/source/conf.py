import os
import sys

# Add project directories to Python path
sys.path.insert(0, os.path.abspath("../../src"))

# Project information
project = "scenariomanager"
copyright = "2025, Florencia Kabas"
author = "Florencia Kabas"
release = "1.0.0"

# Extensions
extensions = [
    "sphinx.ext.autodoc",  # Auto-documentation from docstrings
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    "sphinx.ext.viewcode",  # Add links to source code
]

# Theme configuration
html_theme = "sphinx_rtd_theme"  # Read the Docs theme (professional look)
html_theme_options = {
    "navigation_depth": 4,
    "titles_only": False,
    "logo_only": False,
}

# AutoDoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
    "exclude-members": "__weakref__",
}

# Napoleon settings (for Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Intersphinx mapping for external references
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    # Add other libraries your project uses
}

# Default autodoc flags
autoclass_content = "both"  # Include both class and __init__ docstrings
