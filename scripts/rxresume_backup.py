"""Backup all resumes from Reactive Resume (rxresu.me) API."""

import json
from pathlib import Path

from rxresume import RxResumeClient

BACKUPS_DIR = Path(__file__).resolve().parent.parent / "backups"


def save_resume(slug, data):
    """Save resume JSON to backups directory."""
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = BACKUPS_DIR / f"{slug}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filepath


def main():
    client = RxResumeClient()

    print(f"Connecting to {client.base_url}...")
    resumes = client.list_resumes()
    print(f"Found {len(resumes)} resume(s).\n")

    backed_up = []
    for resume_meta in resumes:
        rid = resume_meta["id"]
        name = resume_meta["name"]
        slug = resume_meta["slug"]
        print(f"  Backing up: {name} (slug: {slug})...")

        full_data = client.get_resume(rid)
        filepath = save_resume(slug, full_data)
        backed_up.append(slug)
        print(f"    Saved to {filepath}")

    print(f"\nBackup complete: {len(backed_up)} resume(s) saved.")
    for slug in backed_up:
        print(f"  - backups/{slug}.json")


if __name__ == "__main__":
    main()
