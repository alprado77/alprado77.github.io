import os
import sys
sys.path.append(os.curdir)
from publishconf import *

# Point at the GitHub Pages address while testing,
# so internal links stay on the staging site.
SITEURL = 'https://alprado77.github.io'

# Hold back the custom domain — see below.
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
}