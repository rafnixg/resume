"""Add Plausible Analytics script to HTML file."""
import re


class CustomTagAdder:
    """Class to add custom tags to HTML file."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.html_content = None
        self.read_file()

    def read_file(self):
        """Read HTML file."""
        with open(self.file_path, "r", encoding="UTF-8") as f:
            self.html_content = f.read()

    def write_file(self):
        """Write HTML file."""
        with open(self.file_path, "w", encoding="UTF-8") as f:
            f.write(self.html_content)

    def add_script(self, script):
        """Add script to HTML file."""
        self.html_content = re.sub(
            "</body></html>", script + "</body></html>", self.html_content
        )

    def add_meta(self, meta):
        """Add meta to HTML file."""
        self.html_content = re.sub("</head>", meta + "</head>", self.html_content)

    def save(self):
        """Save HTML file."""
        self.write_file()


if __name__ == "__main__":
    FILE_PATH = "index.html"
    SCRIPT = """<script
        defer 
        data-domain="resume.rafnixg.dev" 
        src="https://analytics.rafnixg.dev/js/script.js">
    </script>"""
    META = """<title>Rafnix Guzmán - Desarrollador de Software | CV Profesional</title>
    <meta name="author" content="Rafnix Guzman" />
    <meta
      name="description"
      content="Resumen profesional de Rafnix Guzmán: Explora mi CV lleno de experiencia en desarrollo de software, especialización en Python, Linux y Odoo, y una sólida carrera tecnológica de más de 10 años."
    />
    <meta
      itemprop="name"
      content="Rafnix Guzmán - Desarrollador de Software | CV Profesional"
    />
    <meta
      itemprop="description"
      content="Resumen profesional de Rafnix Guzmán: Explora mi CV lleno de experiencia en desarrollo de software, especialización en Python, Linux y Odoo, y una sólida carrera tecnológica de más de 10 años."
    />
    <meta itemprop="image" content="https://links.rafnixg.dev/images/banner_web.png" />
    <meta property="og:url" content="https://resume.rafnixg.dev" />
    <meta property="og:type" content="website" />
    <meta
        property="og:title"
        content="Rafnix Guzmán - Desarrollador de Software | CV Profesional"
    />
    <meta
        property="og:description"
        content="Resumen profesional de Rafnix Guzmán: Explora mi CV lleno de experiencia en desarrollo de software, especialización en Python, Linux y Odoo, y una sólida carrera tecnológica de más de 10 años."
    />
    <meta property="og:image" content="https://links.rafnixg.dev/images/banner_web.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta
        name="twitter:title"
        content="Rafnix Guzmán - Desarrollador de Software | CV Profesional"
    />
    <meta
        name="twitter:description"
        content="Resumen profesional de Rafnix Guzmán: Explora mi CV lleno de experiencia en desarrollo de software, especialización en Python, Linux y Odoo, y una sólida carrera tecnológica de más de 10 años."
    />
    <meta name="twitter:image" content="https://links.rafnixg.dev/images/banner_web.png" />"""

    tag_adder = CustomTagAdder(FILE_PATH)
    tag_adder.add_script(SCRIPT)
    tag_adder.add_meta(META)
    tag_adder.save()
