# Resume - Rafnix Gabriel Guzmán Garcia

[![Publish Resume](https://github.com/rafnixg/resume/actions/workflows/main.yml/badge.svg)](https://github.com/rafnixg/resume/actions/workflows/main.yml)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fresume.rafnixg.dev)](https://resume.rafnixg.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JSON Resume](https://img.shields.io/badge/JSON-Resume-green.svg)](https://jsonresume.org/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/rafnixg/resume)

> 💼 Mi currículum profesional en formato JSON Resume, publicado automáticamente como página web usando GitHub Actions

## 📋 Tabla de Contenidos

- [Acerca de](#acerca-de)
- [Vista Previa](#vista-previa)
- [Tecnologías](#tecnologías)
- [Cómo Usar](#cómo-usar)
- [Personalización](#personalización)
- [Despliegue](#despliegue)
- [Licencia](#licencia)

## 🎯 Acerca de

Este repositorio contiene mi currículum vitae profesional en formato [JSON Resume](https://jsonresume.org/), un estándar de código abierto para currículums. El CV se convierte automáticamente en una página web estática y se publica en GitHub Pages mediante GitHub Actions.

**Características principales:**
- ✅ Formato estándar JSON Resume
- ✅ Generación automática de HTML con tema elegante
- ✅ Publicación automática con GitHub Actions
- ✅ Inyección de metadatos personalizados (SEO, Open Graph, Twitter Cards)
- ✅ Análisis con Umami Analytics
- ✅ Responsive y accesible

## 👀 Vista Previa

Puedes ver mi currículum en línea aquí: **[https://resume.rafnixg.dev](https://resume.rafnixg.dev)**

## 🛠️ Tecnologías

- **[JSON Resume](https://jsonresume.org/)**: Estándar para currículums en formato JSON
- **[JSON Resume Elegant Theme](https://github.com/mudassir0909/jsonresume-theme-elegant)**: Tema elegante para la visualización
- **GitHub Actions**: CI/CD para generación y publicación automática
- **GitHub Pages**: Hosting gratuito
- **Python**: Scripts personalizados para inyección de metadatos

## 📦 Cómo Usar

### Requisitos previos

- Cuenta de GitHub
- Python 3.8+ (opcional, solo para desarrollo local)

### Uso de este template

1. **Fork este repositorio** o úsalo como template
2. **Edita el archivo `resume.json`** con tu información personal
3. **Actualiza el script `add_custom_tags.py`** con tus propios metadatos y analytics
4. **Configura GitHub Pages**:
   - Ve a Settings > Pages
   - Source: Deploy from a branch
   - Branch: `main` / `root`
5. **Actualiza el README.md** con tu información

## ✏️ Personalización

### Modificar el contenido del CV

Edita el archivo `resume.json` siguiendo el [esquema de JSON Resume](https://jsonresume.org/schema/):

```json
{
  "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
  "basics": {
    "name": "Tu Nombre",
    "label": "Tu Título Profesional",
    "email": "tu@email.com",
    ...
  },
  "work": [...],
  "education": [...],
  ...
}
```

### Cambiar el tema

Modifica el archivo `.github/workflows/main.yml` y cambia el valor del parámetro `theme`:

```yaml
- uses: kelvintaywl/action-jsonresume-export@v1
  with:
    theme: elegant  # Puedes usar: elegant, flat, modern, etc.
```

Temas disponibles: https://jsonresume.org/themes/

### Personalizar metadatos

Edita el archivo `add_custom_tags.py` para:
- Añadir o modificar metadatos SEO
- Integrar tu propio analytics (Umami, Google Analytics, etc.)
- Añadir scripts personalizados

## 🚀 Despliegue

El despliegue es automático mediante GitHub Actions:

1. **Commit y Push**: Realiza cambios en `resume.json` o cualquier archivo
2. **GitHub Actions**: Se ejecuta automáticamente el workflow
3. **Generación**: Convierte el JSON a HTML con el tema seleccionado
4. **Inyección**: Añade metadatos personalizados con Python
5. **Publicación**: Actualiza automáticamente el `index.html` en la rama `main`
6. **GitHub Pages**: Publica la nueva versión

Para evitar que se ejecute el workflow, incluye `[ci skip]` en el mensaje del commit.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

**Desarrollado por** [Rafnix Gabriel Guzmán Garcia](https://links.rafnixg.dev) | Backend Python | Odoo Developer | Tech Writer

