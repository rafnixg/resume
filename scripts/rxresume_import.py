"""Import a backup JSON file into Reactive Resume as a new resume."""

import json
import sys
from pathlib import Path

from rxresume import RxResumeClient

BACKUPS_DIR = Path(__file__).resolve().parent.parent / "backups"


def main():
    if len(sys.argv) < 2:
        print("Usage: python rxresume_import.py <backup_filename>")
        print("Example: python rxresume_import.py rafnix-guzman-python-en.json")
        sys.exit(1)

    filename = sys.argv[1]
    backup_path = BACKUPS_DIR / filename
    if not backup_path.exists():
        backup_path = Path(filename)
    if not backup_path.exists():
        print(f"Error: file not found: {filename}")
        sys.exit(1)

    with open(backup_path, "r", encoding="utf-8") as f:
        backup = json.load(f)

    client = RxResumeClient()
    print(f"Importing {backup_path.name}...")
    result = client.import_resume(backup)
    print(f"Done! Resume ID: {result.get('id')}")
    print(f"Slug: {result.get('slug')}")
    print(f"Name: {result.get('name')}")


if __name__ == "__main__":
    main()
