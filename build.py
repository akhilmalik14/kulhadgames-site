#!/usr/bin/env python3
"""Builds the static site: wraps each src/<slug>.html fragment in the shared layout → <slug>/index.html.

A fragment starts with two comment lines:
    <!-- title: Privacy policy -->
    <!-- description: How Gaon Ki Daud handles your data. -->
Run `python3 build.py` after editing anything in src/, then commit the generated files (GitHub Pages serves them as they are).
"""
import html, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://kulhadgames.com"
NAV = [("/", "Home"), ("/gaon-ki-daud/", "Gaon Ki Daud"), ("/support/", "Support"), ("/privacy/", "Privacy")]
FOOT = [("/gaon-ki-daud/", "Gaon Ki Daud"), ("/support/", "Support"), ("/privacy/", "Privacy policy"),
        ("/terms/", "Terms of use"), ("/delete-account/", "Delete your data")]
# (src fragment, output path, url path)
PAGES = [("home", "index.html", "/"), ("gaon-ki-daud", "gaon-ki-daud/index.html", "/gaon-ki-daud/"),
         ("privacy", "privacy/index.html", "/privacy/"), ("terms", "terms/index.html", "/terms/"),
         ("support", "support/index.html", "/support/"), ("delete-account", "delete-account/index.html", "/delete-account/"),
         ("404", "404.html", None)]

CUP = ('<svg class="cup" viewBox="0 0 32 32" aria-hidden="true"><path d="M7 9h18l-2.4 17.2a2 2 0 0 1-2 1.8h-9.2a2 2 0 0 1-2-1.8z" '
       'fill="#C2603A" stroke="#2A1E14" stroke-width="2"/><path d="M8.2 14h15.6" stroke="#E8A317" stroke-width="2.4"/>'
       '<path d="M13 3c-1.5 2 1.5 3 0 5M19 3c-1.5 2 1.5 3 0 5" stroke="#F5F0E6" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>')


def layout(title, desc, body, url, lang):
    full = "Kulhad Games" if url == "/" else f"{title} · Kulhad Games"
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{cur if h == url else ""}>{t}</a>' for h, t in NAV)
    foot = "".join(f'<a href="{h}">{t}</a>' for h, t in FOOT)
    canon = f'<link rel="canonical" href="{SITE}{url}">\n' if url else '<meta name="robots" content="noindex">\n'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
{canon}<meta name="theme-color" content="#2B3A8C">
<meta property="og:title" content="{html.escape(full)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}/assets/img/feature.jpg">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/baloo2.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header>
<div class="top"><div class="wrap"><a class="brand" href="/">{CUP}Kulhad Games</a><nav aria-label="Main">{nav}</nav></div></div>
<div class="band"></div><div class="drops"></div>
</header>
<main id="main"><div class="wrap">
{body.strip()}
</div></main>
<footer>
<div class="drops"></div><div class="band"></div>
<div class="inner"><div class="wrap">
<nav aria-label="Footer">{foot}</nav>
<p>© 2026 Kulhad Games · Akhil Malik, India · <a href="mailto:hello@kulhadgames.com">hello@kulhadgames.com</a></p>
<p>This site uses no cookies, no analytics and no tracking scripts.</p>
</div></div>
</footer>
</body>
</html>
"""


def main():
    for src, out, url in PAGES:
        text = open(os.path.join(ROOT, "src", src + ".html"), encoding="utf-8").read()
        title = re.search(r"<!-- title: (.*?) -->", text).group(1)
        desc = re.search(r"<!-- description: (.*?) -->", text).group(1)
        lang_m = re.search(r"<!-- lang: (.*?) -->", text)
        body = re.sub(r"<!-- (title|description|lang): .*? -->\n?", "", text)
        path = os.path.join(ROOT, out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(layout(title, desc, body, url, lang_m.group(1) if lang_m else "en"))
        print("wrote", out)
    urls = "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for _, _, u in PAGES if u)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')


if __name__ == "__main__":
    main()
