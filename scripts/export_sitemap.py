"""Sitemap generation helpers for exported resumes."""

from datetime import date

from export_config import SITE_URL


def generate_sitemap(slugs):
    """Generate sitemap.xml with all resume URLs."""
    today = date.today().isoformat()

    urls = [
        f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
  </url>"""
    ]
    for slug in slugs:
        urls.append(
            f"""  <url>
    <loc>{SITE_URL}/resume/index-{slug}.html</loc>
    <lastmod>{today}</lastmod>
  </url>"""
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
