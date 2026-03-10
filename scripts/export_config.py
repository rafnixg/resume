"""Shared configuration for the resume export pipeline."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKUPS_DIR = ROOT_DIR / "backups"
PUBLIC_DIR = ROOT_DIR / "public"
RESUME_DIR = PUBLIC_DIR / "resume"
ASSETS_DIR = PUBLIC_DIR / "assets"
RESUME_JSON_PATH = PUBLIC_DIR / "resume.json"

SITE_URL = "https://resume.rafnixg.dev"
BANNER_IMAGE = "https://links.rafnixg.dev/images/banner_web.png"
UMAMI_SCRIPT = '<script defer src="https://umami.rafnixg.dev/script.js" data-website-id="3d3cdb5f-0751-4c3e-85b7-5ff046f5c2da"></script>'
