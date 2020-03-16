import os
import re

# Project information
project = '3D-CSEM-CC'
copyright = '2019, emg3d, SimPEG, custEM, PETGEM'
author = 'emg3d, SimPEG, custEM, PETGEM'
description = '3D CSEM code comparison article'

# General configuration
extensions = ['sphinx.ext.mathjax', ]
exclude_patterns = ['_build', ]         # List of exclude patterns.
version = re.sub('^v', '', os.popen('git describe --tags').read().strip())
today_fmt = '%d %B %Y'

# Figures
numfig = True
numfig_format = {'figure': 'Figure %s:'}

# HTML related
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static', ]  # Static paths.
html_theme_options = {
    'prev_next_buttons_location': 'both',
}

# CSS fixes
def setup(app):
    app.add_stylesheet("style.css")
