"""HTML rendering helpers for Reactive Resume and JSON Resume exports."""

import json
import re
from html import escape

from export_config import BANNER_IMAGE

_PDF_BUTTON_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'


def _build_fonts_url(body_font, heading_font):
    """Build a Google Fonts CSS URL for the given fonts."""
    families = {body_font, heading_font}
    params = "&".join(
        f"family={font.replace(' ', '+')}:wght@400;600"
        for font in sorted(families)
    )
    return f"https://fonts.googleapis.com/css2?{params}&display=swap"


def _build_pdf_button(pdf_filename, assets_prefix="assets"):
    """Return an HTML download button for the PDF, or empty string."""
    if not pdf_filename:
        return ""
    return (
        f'<a class="download-btn" href="{assets_prefix}/{pdf_filename}" download>'
        f"{_PDF_BUTTON_SVG} Descargar PDF</a>"
    )


def _build_css(primary_color, body_font, heading_font):
    """Return the shared CSS rules used by all resume HTML pages."""
    return f"""*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

        :root {{
            --color-primary: {primary_color};
            --color-text: #171717;
            --color-muted: #6b7280;
            --color-border: #e5e7eb;
            --color-bg: #fafafa;
            --color-surface: #ffffff;
            --font-body: '{body_font}', serif;
            --font-heading: '{heading_font}', serif;
        }}

        body {{
            font-family: var(--font-body);
            color: var(--color-text);
            background: var(--color-bg);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}

        a {{ color: var(--color-primary); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}

        .container {{
            max-width: 860px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }}

        .resume-header {{
            background: var(--color-surface);
            border-bottom: 1px solid var(--color-border);
            padding: 2.5rem 0 2rem;
        }}
        .resume-header .container {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1.5rem;
        }}
        .header-left h1 {{
            font-family: var(--font-heading);
            font-size: 1.75rem;
            font-weight: 600;
            letter-spacing: -0.025em;
            line-height: 1.2;
        }}
        .header-left .headline {{
            color: var(--color-muted);
            font-size: 0.95rem;
            margin-top: 0.35rem;
        }}
        .header-left .contact {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.25rem;
            margin-top: 0.75rem;
            font-size: 0.85rem;
            color: var(--color-muted);
        }}
        .header-left .contact a {{ color: var(--color-primary); }}
        .sep {{ opacity: 0.4; margin: 0 0.25rem; }}

        .download-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--color-text);
            color: #fff;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 500;
            white-space: nowrap;
            transition: background 0.15s;
            text-decoration: none;
            flex-shrink: 0;
        }}
        .download-btn:hover {{ background: #404040; text-decoration: none; }}

        .summary {{
            border-bottom: 1px solid var(--color-border);
            padding: 1.5rem 0;
        }}
        .summary p {{
            font-size: 0.9rem;
            color: var(--color-text);
            line-height: 1.7;
            margin-bottom: 0.5rem;
        }}
        .summary p:last-child {{ margin-bottom: 0; }}
        .summary strong {{ font-weight: 600; }}

        .section {{
            padding: 1.5rem 0;
            border-bottom: 1px solid var(--color-border);
        }}
        .section:last-child {{ border-bottom: none; }}

        .section-title {{
            font-family: var(--font-heading);
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--color-primary);
            margin-bottom: 1rem;
            margin-top: 1.5rem;
        }}

        .entry {{ margin-bottom: 1.25rem; }}
        .entry:last-child {{ margin-bottom: 0; }}

        .entry-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 1rem;
            margin-bottom: 0.3rem;
        }}
        .entry-left {{ flex: 1; min-width: 0; }}
        .entry-right {{
            text-align: right;
            flex-shrink: 0;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }}

        .entry-title {{
            font-family: var(--font-heading);
            font-size: 0.95rem;
            font-weight: 600;
            line-height: 1.3;
        }}
        .entry-title a {{ color: var(--color-text); }}
        .entry-title a:hover {{ color: var(--color-primary); }}

        .entry-subtitle {{ font-size: 0.85rem; color: var(--color-muted); }}
        .entry-period {{ font-size: 0.8rem; color: var(--color-muted); white-space: nowrap; }}
        .entry-area {{ font-size: 0.78rem; color: var(--color-muted); }}
        .location {{ font-size: 0.78rem; color: var(--color-muted); }}

        .entry-body {{
            font-size: 0.85rem;
            line-height: 1.65;
            color: #374151;
            margin-top: 0.25rem;
        }}
        .entry-body p {{ margin-bottom: 0.5rem; }}
        .entry-body p:last-child {{ margin-bottom: 0; }}
        .entry-body a {{ color: var(--color-primary); }}
        .entry-tags {{ font-size: 0.78rem; color: var(--color-primary); margin-top: 0.25rem; }}

        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
        }}
        .skill-item {{
            padding: 0.6rem 0.75rem;
            background: var(--color-bg);
            border-radius: 6px;
            border: 1px solid var(--color-border);
        }}
        .skill-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 0.25rem;
            font-size: 0.85rem;
        }}
        .skill-level {{
            font-size: 0.7rem;
            color: var(--color-primary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }}
        .skill-keywords {{
            font-size: 0.78rem;
            color: var(--color-muted);
            line-height: 1.5;
        }}

        .certs-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.4rem;
        }}
        .cert-item {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 1rem;
            padding: 0.35rem 0;
            font-size: 0.85rem;
        }}
        .cert-title {{ flex: 1; min-width: 0; }}
        .cert-meta {{
            font-size: 0.78rem;
            color: var(--color-muted);
            white-space: nowrap;
            flex-shrink: 0;
        }}

        .reference-item {{
            padding: 0.75rem;
            background: var(--color-bg);
            border-radius: 6px;
            border: 1px solid var(--color-border);
        }}
        .reference-item .entry-body {{
            margin-top: 0.4rem;
            font-style: italic;
        }}

        .langs-grid {{
            display: flex;
            gap: 1.5rem;
            font-size: 0.85rem;
        }}
        .lang-item span {{
            color: var(--color-muted);
            margin-left: 0.25rem;
        }}

        .resume-footer {{
            text-align: center;
            padding: 1.5rem 0;
            font-size: 0.75rem;
            color: var(--color-muted);
        }}

        @media (max-width: 640px) {{
            .resume-header .container {{ flex-direction: column; }}
            .entry-header {{ flex-direction: column; gap: 0.15rem; }}
            .entry-right {{ text-align: left; align-items: flex-start; }}
            .skills-grid {{ grid-template-columns: 1fr; }}
        }}

        @media print {{
            body {{ background: #fff; }}
            .download-btn {{ display: none; }}
            .resume-footer {{ display: none; }}
            .section {{ break-inside: avoid; }}
        }}"""


def _build_meta_tags(full_name, meta_description):
    """Return common HTML meta tags."""
    return f"""<meta itemprop="image" content="{BANNER_IMAGE}" />
    <meta name="description" content="{escape(meta_description)}" />
    <meta name="author" content="{full_name}" />
    <meta property="og:title" content="{full_name} - CV" />
    <meta property="og:description" content="{escape(meta_description)}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="{BANNER_IMAGE}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{full_name} - CV" />
    <meta name="twitter:description" content="{escape(meta_description)}" />
    <meta name="twitter:image" content="{BANNER_IMAGE}" />"""


def strip_html(text):
    """Strip HTML tags from text for meta descriptions."""
    return re.sub(r"<[^>]+>", "", text or "").strip()


def visible_items(section):
    """Return non-hidden items from a section."""
    if not section or section.get("hidden"):
        return []
    return [item for item in section.get("items", []) if not item.get("hidden")]


def render_section_title(title):
    """Render a section title."""
    return f'<h2 class="section-title">{escape(title)}</h2>'


def render_experience(section):
    """Render experience section."""
    items = visible_items(section)
    if not items:
        return ""
    html = render_section_title(section.get("title", "Experience"))
    for item in items:
        company = escape(item.get("company", ""))
        position = escape(item.get("position", ""))
        period = escape(item.get("period", ""))
        location = escape(item.get("location", ""))
        website = item.get("website", {})
        url = website.get("url", "")
        description = item.get("description", "")

        company_html = f'<a href="{escape(url)}" target="_blank" rel="noopener">{company}</a>' if url else company
        location_html = f'<span class="location">{location}</span>' if location else ""

        html += f"""<div class="entry">
            <div class="entry-header">
                <div class="entry-left">
                    <h3 class="entry-title">{company_html}</h3>
                    <span class="entry-subtitle">{position}</span>
                </div>
                <div class="entry-right">
                    <span class="entry-period">{period}</span>
                    {location_html}
                </div>
            </div>
            <div class="entry-body">{description}</div>
        </div>\n"""
    return html


def render_education(section):
    """Render education section."""
    items = visible_items(section)
    if not items:
        return ""
    html = render_section_title(section.get("title", "Education"))
    for item in items:
        school = escape(item.get("school", ""))
        degree = escape(item.get("degree", ""))
        area = escape(item.get("area", ""))
        grade = escape(item.get("grade", ""))
        period = escape(item.get("period", ""))

        subtitle = f"{degree}" + (f" &middot; {grade}" if grade else "")

        html += f"""<div class="entry">
            <div class="entry-header">
                <div class="entry-left">
                    <h3 class="entry-title">{school}</h3>
                    <span class="entry-subtitle">{subtitle}</span>
                </div>
                <div class="entry-right">
                    <span class="entry-period">{period}</span>
                    <span class="entry-area">{area}</span>
                </div>
            </div>
        </div>\n"""
    return html


def render_projects(section):
    """Render projects section."""
    items = visible_items(section)
    if not items:
        return ""
    html = render_section_title(section.get("title", "Projects"))
    for item in items:
        name = escape(item.get("name", ""))
        period = escape(item.get("period", ""))
        website = item.get("website", {})
        url = website.get("url", "")
        description = item.get("description", "")

        name_html = f'<a href="{escape(url)}" target="_blank" rel="noopener">{name}</a>' if url else name

        html += f"""<div class="entry">
            <div class="entry-header">
                <div class="entry-left">
                    <h3 class="entry-title">{name_html}</h3>
                </div>
                <div class="entry-right">
                    <span class="entry-period">{period}</span>
                </div>
            </div>
            <div class="entry-body">{description}</div>
        </div>\n"""
    return html


def render_skills(section):
    """Render skills section."""
    items = visible_items(section)
    if not items:
        return ""
    html = render_section_title(section.get("title", "Skills"))
    html += '<div class="skills-grid">\n'
    for item in items:
        name = escape(item.get("name", ""))
        proficiency = escape(item.get("proficiency", ""))
        keywords = item.get("keywords", [])
        kw_html = ", ".join(escape(keyword) for keyword in keywords)
        prof_html = f'<span class="skill-level">{proficiency}</span>' if proficiency else ""

        html += f"""<div class="skill-item">
            <div class="skill-header">
                <strong>{name}</strong>
                {prof_html}
            </div>
            <div class="skill-keywords">{kw_html}</div>
        </div>\n"""
    html += "</div>\n"
    return html


def render_certifications(section):
    """Render certifications section."""
    items = visible_items(section)
    if not items:
        return ""
    html = render_section_title(section.get("title", "Certifications"))
    html += '<div class="certs-grid">\n'
    for item in items:
        title = escape(item.get("title", ""))
        issuer = escape(item.get("issuer", ""))
        item_date = escape(item.get("date", ""))
        website = item.get("website", {})
        url = website.get("url", "")

        title_html = f'<a href="{escape(url)}" target="_blank" rel="noopener">{title}</a>' if url else title

        html += f"""<div class="cert-item">
            <span class="cert-title">{title_html}</span>
            <span class="cert-meta">{issuer} &middot; {item_date}</span>
        </div>\n"""
    html += "</div>\n"
    return html


def render_references(section):
    """Render references section."""
    items = visible_items(section)
    if not items:
        return ""
    html = render_section_title(section.get("title", "References"))
    for item in items:
        name = escape(item.get("name", ""))
        position = escape(item.get("position", ""))
        description = item.get("description", "")

        html += f"""<div class="entry reference-item">
            <h3 class="entry-title">{name}</h3>
            <span class="entry-subtitle">{position}</span>
            <div class="entry-body">{description}</div>
        </div>\n"""
    return html


def render_languages(section):
    """Render languages section."""
    items = visible_items(section)
    if not items:
        return ""
    html = render_section_title(section.get("title", "Languages"))
    html += '<div class="langs-grid">\n'
    for item in items:
        language = escape(item.get("language", ""))
        fluency = escape(item.get("fluency", ""))
        html += f'<div class="lang-item"><strong>{language}</strong> <span>{fluency}</span></div>\n'
    html += "</div>\n"
    return html


def generate_html(resume_data, slug, pdf_filename, screenshot_filename):
    """Generate a full resume HTML page from rxresume JSON data."""
    del slug
    del screenshot_filename

    data = resume_data.get("data", {})
    basics = data.get("basics", {})
    summary = data.get("summary", {})
    sections = data.get("sections", {})
    metadata = data.get("metadata", {})

    design = metadata.get("design", {})
    colors = design.get("colors", {})
    primary_color = colors.get("primary", "rgba(0, 150, 137, 1)")
    typography = metadata.get("typography", {})
    body_font = typography.get("body", {}).get("fontFamily", "IBM Plex Serif")
    heading_font = typography.get("heading", {}).get("fontFamily", "IBM Plex Serif")

    full_name = escape(basics.get("name", ""))
    headline = escape(basics.get("headline", ""))
    email = basics.get("email", "")
    location = escape(basics.get("location", ""))
    website = basics.get("website", {})
    website_url = website.get("url", "")

    summary_content = summary.get("content", "") if not summary.get("hidden") else ""
    meta_description = strip_html(summary_content)[:200]

    layout_pages = metadata.get("layout", {}).get("pages", [])
    section_order = []
    for page in layout_pages:
        section_order.extend(page.get("main", []))
        section_order.extend(page.get("sidebar", []))

    renderers = {
        "experience": render_experience,
        "education": render_education,
        "projects": render_projects,
        "skills": render_skills,
        "certifications": render_certifications,
        "references": render_references,
        "languages": render_languages,
    }

    sections_html = ""
    for section_key in section_order:
        if section_key in ("summary", "profiles"):
            continue
        renderer = renderers.get(section_key)
        if renderer and section_key in sections:
            sections_html += renderer(sections[section_key])

    contact_parts = []
    if email:
        contact_parts.append(f'<a href="mailto:{escape(email)}">{escape(email)}</a>')
    if location:
        contact_parts.append(f"<span>{location}</span>")
    if website_url:
        label = escape(website.get("label", "") or website_url)
        contact_parts.append(f'<a href="{escape(website_url)}" target="_blank" rel="noopener">{label}</a>')
    contact_html = ' <span class="sep">&middot;</span> '.join(contact_parts)

    fonts_url = _build_fonts_url(body_font, heading_font)
    pdf_btn = _build_pdf_button(pdf_filename, "../assets")
    css = _build_css(primary_color, body_font, heading_font)
    meta_tags = _build_meta_tags(full_name, meta_description)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{full_name} - CV</title>
    {meta_tags}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="{fonts_url}" rel="stylesheet" />
    <style>
        {css}
    </style>
</head>
<body>
    <div class="resume-header">
        <div class="container">
            <div class="header-left">
                <h1>{full_name}</h1>
                <div class="headline">{headline}</div>
                <div class="contact">{contact_html}</div>
            </div>
            {pdf_btn}
        </div>
    </div>

    <div class="container">
        {'' if not summary_content else f'<div class="summary">{summary_content}</div>'}
        {sections_html}
    </div>

    <div class="resume-footer">
        Generado desde <a href="https://rxresu.me" target="_blank" rel="noopener">Reactive Resume</a>
    </div>
</body>
</html>"""


def generate_html_from_jsonresume(resume_path, pdf_filename=None):
    """Generate a full HTML resume page from a JSON Resume file."""
    with open(resume_path, "r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    basics = data.get("basics", {})
    full_name = escape(basics.get("name", ""))
    label = escape(basics.get("label", ""))
    email = basics.get("email", "")
    summary = basics.get("summary", "")
    location = basics.get("location", {})
    location_str = escape(location.get("address", ""))
    website_url = basics.get("url", "")
    profiles = basics.get("profiles", [])

    meta_description = summary[:200]

    contact_parts = []
    if email:
        contact_parts.append(f'<a href="mailto:{escape(email)}">{escape(email)}</a>')
    if location_str:
        contact_parts.append(f"<span>{location_str}</span>")
    if website_url:
        escaped_website = escape(website_url)
        contact_parts.append(f'<a href="{escaped_website}" target="_blank" rel="noopener">{escaped_website}</a>')
    for profile in profiles:
        url = profile.get("url", "")
        network = escape(profile.get("network", ""))
        username = escape(profile.get("username", ""))
        if url:
            contact_parts.append(f'<a href="{escape(url)}" target="_blank" rel="noopener">{network}: {username}</a>')
    contact_html = ' <span class="sep">&middot;</span> '.join(contact_parts)

    work_html = ""
    work = data.get("work", [])
    if work:
        work_html = render_section_title("Experience")
        for item in work:
            company = escape(item.get("name", ""))
            position = escape(item.get("position", ""))
            start = escape(item.get("startDate", "")[:7])
            end = escape(item.get("endDate", "Present")[:7]) if item.get("endDate") else "Present"
            period = f"{start} — {end}"
            location_value = escape(item.get("location", ""))
            url = item.get("url", "")
            description = escape(item.get("summary", ""))
            highlights = item.get("highlights", [])

            company_html = f'<a href="{escape(url)}" target="_blank" rel="noopener">{company}</a>' if url else company
            location_html = f'<span class="location">{location_value}</span>' if location_value else ""
            highlights_html = ""
            if highlights:
                highlights_html = '<div class="entry-tags">' + ", ".join(escape(highlight) for highlight in highlights) + "</div>"

            work_html += f"""<div class="entry">
                <div class="entry-header">
                    <div class="entry-left">
                        <h3 class="entry-title">{company_html}</h3>
                        <span class="entry-subtitle">{position}</span>
                    </div>
                    <div class="entry-right">
                        <span class="entry-period">{period}</span>
                        {location_html}
                    </div>
                </div>
                <div class="entry-body"><p>{description}</p></div>
                {highlights_html}
            </div>\n"""

    edu_html = ""
    education = data.get("education", [])
    if education:
        edu_html = render_section_title("Education")
        for item in education:
            school = escape(item.get("institution", ""))
            degree = escape(item.get("studyType", ""))
            area = escape(item.get("area", ""))
            score = escape(item.get("score", ""))
            start = escape(item.get("startDate", "")[:7])
            end = escape(item.get("endDate", "")[:7]) if item.get("endDate") else ""
            period = f"{start} — {end}" if end else start
            subtitle = degree + (f" &middot; {score}" if score else "")

            edu_html += f"""<div class="entry">
                <div class="entry-header">
                    <div class="entry-left">
                        <h3 class="entry-title">{school}</h3>
                        <span class="entry-subtitle">{subtitle}</span>
                    </div>
                    <div class="entry-right">
                        <span class="entry-period">{period}</span>
                        <span class="entry-area">{area}</span>
                    </div>
                </div>
            </div>\n"""

    skills_html = ""
    skills = data.get("skills", [])
    if skills:
        skills_html = render_section_title("Skills")
        skills_html += '<div class="skills-grid">\n'
        for item in skills:
            name = escape(item.get("name", ""))
            level = escape(item.get("level", ""))
            keywords = item.get("keywords", [])
            kw_html = ", ".join(escape(keyword) for keyword in keywords)
            level_html = f'<span class="skill-level">{level}</span>' if level else ""
            skills_html += f"""<div class="skill-item">
                <div class="skill-header"><strong>{name}</strong>{level_html}</div>
                <div class="skill-keywords">{kw_html}</div>
            </div>\n"""
        skills_html += "</div>\n"

    projects_html = ""
    projects = data.get("projects", [])
    if projects:
        projects_html = render_section_title("Projects")
        for item in projects:
            name = escape(item.get("name", ""))
            url = item.get("url", "")
            description = escape(item.get("description", ""))
            start = escape(item.get("startDate", "")[:7])
            end = escape(item.get("endDate", "")[:7]) if item.get("endDate") else ""
            period = f"{start} — {end}" if end else start
            name_html = f'<a href="{escape(url)}" target="_blank" rel="noopener">{name}</a>' if url else name

            projects_html += f"""<div class="entry">
                <div class="entry-header">
                    <div class="entry-left"><h3 class="entry-title">{name_html}</h3></div>
                    <div class="entry-right"><span class="entry-period">{period}</span></div>
                </div>
                <div class="entry-body"><p>{description}</p></div>
            </div>\n"""

    certs_html = ""
    certifications = data.get("certificates", [])
    if certifications:
        certs_html = render_section_title("Certifications")
        certs_html += '<div class="certs-grid">\n'
        for item in certifications:
            title = escape(item.get("name", ""))
            issuer = escape(item.get("issuer", ""))
            item_date = escape(item.get("date", ""))
            url = item.get("url", "")
            title_html = f'<a href="{escape(url)}" target="_blank" rel="noopener">{title}</a>' if url else title
            certs_html += f"""<div class="cert-item">
                <span class="cert-title">{title_html}</span>
                <span class="cert-meta">{issuer} &middot; {item_date}</span>
            </div>\n"""
        certs_html += "</div>\n"

    langs_html = ""
    languages = data.get("languages", [])
    if languages:
        langs_html = render_section_title("Languages")
        langs_html += '<div class="langs-grid">\n'
        for item in languages:
            language = escape(item.get("language", ""))
            fluency = escape(item.get("fluency", ""))
            langs_html += f'<div class="lang-item"><strong>{language}</strong> <span>{fluency}</span></div>\n'
        langs_html += "</div>\n"

    refs_html = ""
    references = data.get("references", [])
    if references:
        refs_html = render_section_title("References")
        for item in references:
            name = escape(item.get("name", ""))
            reference = escape(item.get("reference", ""))
            refs_html += f"""<div class="entry reference-item">
                <h3 class="entry-title">{name}</h3>
                <div class="entry-body"><p>{reference}</p></div>
            </div>\n"""

    sections_html = work_html + edu_html + skills_html + projects_html + certs_html + langs_html + refs_html

    summary_section = ""
    if summary:
        paragraphs = summary.split("\n\n")
        summary_section = '<div class="summary">' + "".join(
            f"<p>{escape(paragraph)}</p>" for paragraph in paragraphs if paragraph.strip()
        ) + "</div>"

    primary_color = "rgba(0, 150, 137, 1)"
    body_font = "IBM Plex Serif"
    heading_font = "IBM Plex Serif"
    fonts_url = _build_fonts_url(body_font, heading_font)
    pdf_btn = _build_pdf_button(pdf_filename)
    css = _build_css(primary_color, body_font, heading_font)
    meta_tags = _build_meta_tags(full_name, meta_description)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{full_name} - CV (Full)</title>
    {meta_tags}
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="{fonts_url}" rel="stylesheet" />
    <style>
        {css}
    </style>
</head>
<body>
    <div class="resume-header">
        <div class="container">
            <div class="header-left">
                <h1>{full_name}</h1>
                <div class="headline">{label}</div>
                <div class="contact">{contact_html}</div>
            </div>
            {pdf_btn}
        </div>
    </div>
    <div class="container">
        {summary_section}
        {sections_html}
    </div>
    <div class="resume-footer">
        Generado desde <a href="https://github.com/jsonresume" target="_blank" rel="noopener">JSON Resume</a>
    </div>
</body>
</html>"""
