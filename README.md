# Resume - Rafnix Gabriel Guzmán Garcia

[![Sync Resumes](https://github.com/rafnixg/resume/actions/workflows/rxresume-sync.yml/badge.svg)](https://github.com/rafnixg/resume/actions/workflows/rxresume-sync.yml)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fresume.rafnixg.dev)](https://resume.rafnixg.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JSON Resume](https://img.shields.io/badge/JSON-Resume-green.svg)](https://jsonresume.org/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/rafnixg/resume)

> Mi curriculum profesional publicado como sitio estatico, generado desde [Reactive Resume](https://rxresu.me) y [JSON Resume](https://jsonresume.org/) con GitHub Actions.

## Acerca de

Repositorio que gestiona mi CV profesional con un pipeline automatizado:

1. **Reactive Resume** (rxresu.me) como editor principal del CV
2. **Backup automatico** del JSON completo via API
3. **Generacion de HTML estatico** desde los backups y desde `resume.json`
4. **Publicacion** en GitHub Pages

**Caracteristicas:**
- Backup de resumes desde Reactive Resume API
- Generacion de HTML estatico con diseno responsivo
- Export de PDF y screenshots via API
- Pagina principal desde JSON Resume (`resume.json`)
- Paginas adicionales por cada resume de rxresume
- Sitemap automatico
- Umami Analytics integrado
- SEO (Open Graph, Twitter Cards)
- Workflow manual con GitHub Actions

## Vista Previa

- **Pagina principal:** [https://resume.rafnixg.dev](https://resume.rafnixg.dev)
- **Resume rxresume:** [https://resume.rafnixg.dev/resume/index-rafnix-guzman-python.html](https://resume.rafnixg.dev/resume/index-rafnix-guzman-python.html)

## Estructura del Proyecto

```
├── backups/                          # Backups JSON de rxresume (API)
│   └── {slug}.json
├── public/                           # Sitio estatico (GitHub Pages root)
│   ├── index.html                    # Pagina principal (desde resume.json)
│   ├── resume.json                   # JSON Resume estandar
│   ├── sitemap.xml                   # Sitemap generado automaticamente
│   ├── assets/                       # Recursos estaticos
│   │   ├── {slug}.pdf                # PDF exportado desde rxresume
│   │   ├── {slug}.png                # Screenshot desde rxresume
│   │   ├── banner_web.png
│   │   └── logo.png
│   └── resume/                       # Paginas HTML por resume
│       └── index-{slug}.html         # HTML generado desde backup
├── scripts/
│   ├── rxresume.py                   # Wrapper class para rxresume API
│   ├── rxresume_backup.py            # Backup de resumes desde API
│   ├── rxresume_export.py            # Export: HTML, PDF, sitemap, analytics
│   └── add_custom_tags.py            # Inyeccion de analytics y meta tags
└── .github/workflows/
    └── rxresume-sync.yml             # Workflow: backup -> export -> commit
```

## Scripts

| Script | Descripcion |
|--------|-------------|
| `rxresume.py` | Clase `RxResumeClient` que encapsula las llamadas a la API de rxresume |
| `rxresume_backup.py` | Lista y descarga todos los resumes como JSON en `backups/` |
| `rxresume_export.py` | Genera HTML, descarga PDF/PNG, inyecta analytics, crea sitemap |
| `add_custom_tags.py` | Clase `CustomTagAdder` para inyectar scripts y meta tags en HTML |

## Como Usar

### Requisitos

- Python 3.10+
- `pip install requests`
- API key de [rxresu.me](https://rxresu.me) (Settings -> API Keys)

### Ejecucion local

```bash
# 1. Backup de todos los resumes
RXRESUME_API_KEY=tu-api-key python scripts/rxresume_backup.py

# 2. Export HTML + PDF + sitemap + analytics
RXRESUME_API_KEY=tu-api-key python scripts/rxresume_export.py

# Sin API key solo genera HTML desde los backups existentes
python scripts/rxresume_export.py
```

## Despliegue

El despliegue se ejecuta manualmente desde GitHub Actions:

1. **Ejecutar workflow** desde Actions -> "Sync resumes from Reactive Resume" -> Run workflow
2. **Backup**: Descarga los resumes desde la API de rxresume
3. **Export**: Genera HTML, descarga PDF/PNG, inyecta analytics, crea sitemap
4. **Commit & Push**: Sube los cambios a `backups/` y `public/`
5. **GitHub Pages**: Sirve `public/` como sitio estatico

### Configuracion del repositorio

1. Agrega el secret `RXRESUME_API_KEY`:
   - Settings -> Secrets and variables -> Actions -> New repository secret
2. Configura GitHub Pages:
   - Settings -> Pages -> Source: Deploy from branch -> `main` / `public`

## Licencia

Este proyecto esta bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para mas detalles.

---

**Desarrollado por** [Rafnix Gabriel Guzman Garcia](https://links.rafnixg.dev) | Python Backend | AI Engineer | Odoo Developer
