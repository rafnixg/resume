"""Add Plausible Analytics script to HTML file."""
import re

# Abre el archivo en modo de lectura y escribe en una variable
with open("index.html", "r", encoding="UTF-8") as f:
    content = f.read()

# Define el script que quieres insertar
script = '<script defer data-domain="resume.rafnixg.dev" src="https://analytics.rafnixg.dev/js/script.js"></script>'

# Reemplaza el '</body></html>' con el script + '</body></html>'
content_new = re.sub("</body></html>", script + "\n</body></html>", content)

# Escribe el nuevo contenido en el archivo
with open("index.html", "w", encoding="UTF-8") as f:
    f.write(content_new)
