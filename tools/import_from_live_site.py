#!/usr/bin/env python3
"""
import_from_live_site.py
========================

Converts your live WordPress/Divi pages into Pelican Markdown files.

WHY THIS AND NOT THE XML EXPORT
-------------------------------
Divi does not store your articles as clean text. It stores them as
shortcodes ([et_pb_section], [et_pb_text], ...) with the text buried
inside. The WordPress XML export hands you that raw soup, and it also
duplicates whole articles inside attributes like content_tablet="...".
Cleaning that up reliably is harder than it looks.

The rendered page on your live site, by contrast, is clean HTML —
Divi has already done the work of turning shortcodes into text.
So this script reads your live pages and converts those instead.

WHAT IT DOES
------------
1. Fetches each URL you list below.
2. Grabs the main content, discarding header, nav, footer, cookie banner.
3. Converts it to Markdown.
4. Downloads every image into content/images/ and rewrites the links.
5. Writes a Pelican .md file with the metadata my templates expect.

HOW TO RUN
----------
    pip install requests beautifulsoup4 markdownify
    python tools/import_from_live_site.py

Run it from the root of the pelican-site folder.

AFTER RUNNING
-------------
Open each generated file and check it. Automated conversion gets you
95% of the way; the last 5% (a stray caption, a figure in the wrong
place) is quicker to fix by eye than to automate.
"""

import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    from markdownify import markdownify
except ImportError:
    sys.exit("Missing libraries. Run:\n"
             "    pip install requests beautifulsoup4 markdownify")


# =============================================================
# CONFIGURATION — edit this section
# =============================================================

SITE = "https://prado-cabrero.com"

# Where things get written. Relative to where you run the script.
ARTICLES_DIR = "content/articles"
PAGES_DIR = "content/pages"
IMAGES_DIR = "content/images"

AUTHOR = "Alfonso Prado-Cabrero, PhD"

# --- Your blog articles ---
# slug: the bit after the domain. This becomes the URL, so it must
#       match your current WordPress URL exactly.
# date: publication date, YYYY-MM-DD. Used for ordering on the home page.
# kicker: the small label above the title. Yours to choose.
ARTICLES = [
    {"slug": "creatine-the-why-and-the-how",
     "date": "2025-12-10", "kicker": "Metabolism — Explainer"},

    {"slug": "why-the-sun-doesnt-have-vitamin-d-and-your-cat-couldnt-care-less",
     "date": "2025-11-20", "kicker": "Vitamins — Explainer"},

    {"slug": "which-omega-3s-are-essential",
     "date": "2025-10-25", "kicker": "Essential Fatty Acids — Explainer"},

    {"slug": "where-do-the-ducks-in-central-park-go-in-winter",
     "date": "2025-11-05", "kicker": "Reasoning — Essay"},

    {"slug": "a-different-way-to-explain-the-structure-of-dna",
     "date": "2025-05-20", "kicker": "Molecular Biology — Explainer"},

    {"slug": "gene-and-allele-how-to-tell-the-difference",
     "date": "2025-05-15", "kicker": "Genetics — Explainer"},

    {"slug": "haplossuficiency-and-haploinsufficiency",
     "date": "2025-05-10", "kicker": "Genetics — Explainer"},

    # --- Spanish versions and older English pages ---
    # These appeared in your export. Uncomment any you still want live.
    # {"slug": "la-estructura-del-adn-explicada-de-una-forma-diferente",
    #  "date": "2025-05-20", "kicker": "Biología Molecular"},
    # {"slug": "gen-y-alelo-como-diferenciarlos",
    #  "date": "2025-05-15", "kicker": "Genética"},
    # {"slug": "por-que-el-sol-no-tiene-vitamina-d-y-a-tu-gato-le-da-igual",
    #  "date": "2025-11-20", "kicker": "Vitaminas"},
    # {"slug": "adonde-van-los-patos-de-central-park-en-invierno-2",
    #  "date": "2025-11-05", "kicker": "Razonamiento"},
    # {"slug": "lutein-fortified-yoghurt", "date": "2024-01-01", "kicker": "Project"},
    # {"slug": "mass-production-of-zooplankton", "date": "2024-01-01", "kicker": "Project"},
    # {"slug": "the-exploitation-of-antarctic-krill-and-calanus",
    #  "date": "2024-01-01", "kicker": "Project"},
    # {"slug": "yogur-con-luteina-espanol", "date": "2024-01-01", "kicker": "Proyecto"},
    # {"slug": "produccion-en-masa-de-zooplankton", "date": "2024-01-01", "kicker": "Proyecto"},
]

# --- Your standalone pages (no date, no byline) ---
PAGES = ["about", "projects", "publications", "hobbies"]

# Elements to throw away wherever they appear.
JUNK_SELECTORS = [
    "header", "footer", "nav", "script", "style", "noscript",
    "#main-header", "#main-footer", "#top-header",
    ".et_pb_menu", ".et-social-icons", ".et_pb_widget",
    ".cmplz-cookiebanner", "#cmplz-cookiebanner-container",
    ".et_pb_scroll_top", ".screen-reader-text",
]


# =============================================================
# The script itself — you shouldn't need to change anything below
# =============================================================

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (site migration script)"})


def slugify_filename(url):
    """Turn an image URL into a tidy local filename."""
    name = os.path.basename(urlparse(url).path)
    name = re.sub(r"[^A-Za-z0-9._-]", "-", name)
    # WordPress appends size suffixes like -300x300 or -scaled; keep them,
    # they distinguish different crops of the same original.
    return name.lower()


def download_image(url, dest_dir):
    """Save one image locally. Returns the filename, or None on failure."""
    filename = slugify_filename(url)
    if not filename:
        return None
    path = os.path.join(dest_dir, filename)
    if os.path.exists(path):
        return filename  # already have it
    try:
        r = session.get(url, timeout=30)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        print(f"      image: {filename}")
        return filename
    except Exception as e:
        print(f"      ! could not fetch {url}  ({e})")
        return None


def extract_content(soup):
    """Find the main article body, minus all the site furniture."""
    for sel in JUNK_SELECTORS:
        for el in soup.select(sel):
            el.decompose()

    # Divi wraps page content in one of these, in order of preference
    for sel in ["#main-content .entry-content", "#main-content",
                "article", "main", "#et-main-area"]:
        node = soup.select_one(sel)
        if node and len(node.get_text(strip=True)) > 200:
            return node
    return soup.body


def process(slug, date=None, kicker=None, is_page=False):
    url = f"{SITE}/{slug}/"
    print(f"\n--> {url}")

    try:
        r = session.get(url, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"    ! FAILED: {e}")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # --- metadata from the page's own <head> ---
    title = ""
    if soup.title:
        title = soup.title.get_text().split("|")[0].strip()
    desc_tag = soup.find("meta", attrs={"name": "description"})
    summary = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

    body = extract_content(soup)
    if body is None:
        print("    ! no content found — check the page manually")
        return

    # --- the first <h1> is the title; remove it so it isn't duplicated,
    #     because the template already renders the title itself ---
    h1 = body.find("h1")
    if h1:
        if not title:
            title = h1.get_text(strip=True)
        h1.decompose()

    # --- images: download and rewrite to local paths ---
    hero = None
    hero_alt = ""
    for img in body.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            img.decompose()
            continue
        src = urljoin(url, src)
        filename = download_image(src, IMAGES_DIR)
        if not filename:
            img.decompose()
            continue
        if hero is None:                     # first image becomes the hero
            hero = filename
            hero_alt = img.get("alt", "")
            img.decompose()                  # template renders it separately
        else:
            img["src"] = f"/images/{filename}"
            for attr in ("srcset", "sizes", "class", "width", "height",
                         "data-src", "loading", "title"):
                img.attrs.pop(attr, None)

    # --- HTML -> Markdown ---
    md = markdownify(str(body), heading_style="ATX", bullets="-")

    # --- tidy up Divi's habits ---
    # Divi wraps every heading in bold: "## **Introduction**" -> "## Introduction"
    md = re.sub(r"^(#{1,6}\s+)\*\*(.+?)\*\*\s*$", r"\1\2", md, flags=re.MULTILINE)
    # Empty links Divi leaves behind: "[](https://...)"
    md = re.sub(r"\[\]\([^)]*\)", "", md)
    # Divi's %22 escaping for quotation marks
    md = md.replace("%22", '"')
    # Collapse runs of blank lines, strip trailing spaces
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = "\n".join(line.rstrip() for line in md.splitlines()).strip()

    # --- assemble the Pelican metadata block ---
    meta = [f"Title: {title}"]
    if not is_page:
        meta += [
            f"Date: {date} 10:00",
            f"Author: {AUTHOR}",
        ]
    meta.append(f"Slug: {slug}")
    if kicker:
        meta.append(f"Kicker: {kicker}")
    if summary:
        meta.append(f"Dek: {summary}")
        meta.append(f"Summary: {summary}")
    if hero:
        meta.append(f"Image: {hero}")
        if hero_alt:
            meta.append(f"Image_alt: {hero_alt}")
        meta.append(f"Card_image: {hero}")

    out_dir = PAGES_DIR if is_page else ARTICLES_DIR
    out_path = os.path.join(out_dir, f"{slug}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(meta) + "\n\n" + md + "\n")

    words = len(md.split())
    print(f"    wrote {out_path}  ({words} words)")


def main():
    for d in (ARTICLES_DIR, PAGES_DIR, IMAGES_DIR):
        os.makedirs(d, exist_ok=True)

    print("=" * 60)
    print("ARTICLES")
    print("=" * 60)
    for a in ARTICLES:
        process(a["slug"], date=a["date"], kicker=a.get("kicker"))
        time.sleep(1)          # be polite to your own server

    print("\n" + "=" * 60)
    print("PAGES")
    print("=" * 60)
    for slug in PAGES:
        process(slug, is_page=True)
        time.sleep(1)

    print("\n" + "=" * 60)
    print("Done. Now:")
    print("  1. Open each file in content/articles/ and read it through.")
    print("  2. Check the Dek: line — it may need shortening.")
    print("  3. Wrap the reference list in:")
    print('     <section class="references" markdown="1"> ... </section>')
    print("  4. pelican content -s pelicanconf.py -l")
    print("=" * 60)


if __name__ == "__main__":
    main()
