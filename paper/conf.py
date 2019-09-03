import os
import re
import time


# -- Project information -----------------------------------------------------

project = '3D-CSEM-CC'
copyright = '2019, emg3d, SimPEG, custEM, PETGEM'
author = 'emg3d, SimPEG, custEM, PETGEM'
description = '3D CSEM code comparison article'


# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of exclude patterns.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The full version, including alpha/beta/rc tags.
release = re.sub('^v', '', os.popen('git describe --tags').read().strip())
version = release
today_fmt = '%d %B %Y'

# Figures
numfig = True
numfig_format = {'figure': 'Figure %s:'}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# Static paths.
html_static_path = ['_static']

html_theme_options = {
    'display_version': True,
    'prev_next_buttons_location': 'both',
}
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
    ]
}

# -- CSS fixes --
def setup(app):
    app.add_stylesheet("style.css")

