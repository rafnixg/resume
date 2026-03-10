"""Export resumes from Reactive Resume API: PDF, screenshot, and static HTML."""

import json

from rxresume import RxResumeClient
from add_custom_tags import CustomTagAdder
from export_config import (
    ASSETS_DIR,
    BACKUPS_DIR,
    PUBLIC_DIR,
    RESUME_DIR,
    RESUME_JSON_PATH,
    UMAMI_SCRIPT,
)
from export_rendering import generate_html, generate_html_from_jsonresume
from export_sitemap import generate_sitemap


def main():
    # Try to create API client (optional — needed only for PDF/screenshot)
    client = None
    try:
        client = RxResumeClient()
        print(f"API client ready ({client.base_url})")
    except ValueError:
        print("Warning: RXRESUME_API_KEY not set, skipping PDF/screenshot export.")

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    RESUME_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # Discover backup JSONs
    backup_files = sorted(BACKUPS_DIR.glob("*.json"))
    if not backup_files:
        print("No backup files found in backups/. Run rxresume_backup.py first.")
    else:
        print(f"Found {len(backup_files)} backup(s) in backups/.\n")

    exported = []
    for backup_path in backup_files:
        slug = backup_path.stem  # e.g. "rafnix-guzman-python"
        print(f"  Processing: {slug}...")

        with open(backup_path, "r", encoding="utf-8") as f:
            resume_data = json.load(f)

        # PDF & screenshot via API (if client available)
        pdf_filename = None
        screenshot_filename = None
        if client:
            rid = resume_data.get("id")
            if rid:
                # Export PDF
                pdf_filename = f"{slug}.pdf"
                pdf_path = ASSETS_DIR / pdf_filename
                print("    Generating PDF...")
                try:
                    pdf_url = client.export_pdf(rid)
                    if pdf_url:
                        RxResumeClient.download_file(pdf_url, pdf_path)
                        print(f"    PDF saved to {pdf_path}")
                    else:
                        print("    Warning: No PDF URL returned")
                        pdf_filename = None
                except SystemExit:
                    print("    Warning: PDF export failed")
                    pdf_filename = None

                # Get screenshot
                print("    Getting screenshot...")
                try:
                    screenshot_url = client.get_screenshot(rid)
                    if screenshot_url:
                        screenshot_filename = f"{slug}.png"
                        screenshot_path = ASSETS_DIR / screenshot_filename
                        RxResumeClient.download_file(screenshot_url, screenshot_path)
                        print(f"    Screenshot saved to {screenshot_path}")
                except SystemExit:
                    print("    Warning: Screenshot export failed")

        # Generate HTML in public/resume/
        html_path = RESUME_DIR / f"index-{slug}.html"
        html_content = generate_html(resume_data, slug, pdf_filename, screenshot_filename)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"    HTML saved to {html_path}")

        exported.append(slug)

    # Generate public/index.html from resume.json (JSON Resume format)
    if RESUME_JSON_PATH.exists():
        print("\n  Generating public/index.html from resume.json...")
        # Find a matching PDF if available
        first_pdf = f"{exported[0]}.pdf" if exported else None
        full_html = generate_html_from_jsonresume(RESUME_JSON_PATH, first_pdf)
        full_path = PUBLIC_DIR / "index.html"
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"    Saved to {full_path}")
    else:
        print("\n  Warning: resume.json not found, skipping public/index.html")

    # Inject analytics into all generated HTML files
    html_files = []
    index_path = PUBLIC_DIR / "index.html"
    if index_path.exists():
        html_files.append(index_path)
    for slug in exported:
        html_files.append(RESUME_DIR / f"index-{slug}.html")

    for html_file in html_files:
        tag_adder = CustomTagAdder(str(html_file))
        tag_adder.add_script(UMAMI_SCRIPT)
        tag_adder.save()
    print(f"  Analytics injected into {len(html_files)} HTML file(s).")

    # Generate sitemap.xml
    sitemap_path = PUBLIC_DIR / "sitemap.xml"
    sitemap_content = generate_sitemap(exported)
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"  Sitemap saved to {sitemap_path}")

    print("\nExport complete:")
    print("  - public/index.html")
    for slug in exported:
        print(f"  - public/resume/index-{slug}.html")
        print(f"  - public/assets/{slug}.pdf")
        print(f"  - public/assets/{slug}.png")
    print("  - public/sitemap.xml")


if __name__ == "__main__":
    main()
