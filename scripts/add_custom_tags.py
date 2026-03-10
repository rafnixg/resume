"""Inject custom scripts and meta tags into HTML files."""


class CustomTagAdder:
    """Inject scripts and meta tags into an HTML file."""

    def __init__(self, file_path):
        self.file_path = file_path
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.html_content = f.read()

    def add_script(self, script):
        """Insert a script tag before </body>."""
        self.html_content = self.html_content.replace(
            "</body>", f"{script}\n</body>", 1
        )

    def add_meta(self, meta):
        """Insert meta tags before </head>."""
        self.html_content = self.html_content.replace(
            "</head>", f"{meta}\n</head>", 1
        )

    def save(self):
        """Write the modified HTML back to disk."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(self.html_content)
