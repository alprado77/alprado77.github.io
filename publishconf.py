# =============================================================
# publishconf.py — settings used when building the REAL site
# for publication. Run with:  pelican content -s publishconf.py
#
# It imports everything from pelicanconf.py, then overrides the
# handful of things that differ in production.
# =============================================================

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *   # noqa: F401,F403

# The real domain. Absolute URLs matter for RSS feeds,
# canonical tags and Open Graph images.
SITEURL = 'https://prado-cabrero.com'
RELATIVE_URLS = False

# Turn the RSS feed on for production
FEED_ALL_RSS = 'feeds/all.rss.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'

DELETE_OUTPUT_DIRECTORY = True
