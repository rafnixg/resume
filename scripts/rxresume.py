"""Wrapper class for the Reactive Resume (rxresu.me) API."""

import json
import os
import time
from pathlib import Path

import requests

DEFAULT_BASE_URL = "https://rxresu.me/api/openapi"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


class RxResumeClient:
    """Client for interacting with the Reactive Resume API."""

    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.environ.get("RXRESUME_API_KEY", "")
        self.base_url = (base_url or os.environ.get("RXRESUME_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")

        if not self.api_key:
            raise ValueError("API key is required. Set RXRESUME_API_KEY or pass api_key.")

    def _request(self, method, endpoint, **kwargs):
        """Make an authenticated request with retry logic."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {"x-api-key": self.api_key}
        kwargs.setdefault("timeout", 60)

        for attempt in range(MAX_RETRIES):
            try:
                resp = requests.request(method, url, headers=headers, **kwargs)
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.HTTPError as e:
                if resp.status_code == 429 and attempt < MAX_RETRIES - 1:
                    wait = RETRY_DELAY * (attempt + 1)
                    print(f"  Rate limited, retrying in {wait}s...")
                    time.sleep(wait)
                    continue
                raise SystemExit(f"API error {resp.status_code} on {endpoint}: {e}") from e
            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                raise SystemExit(f"Request failed on {endpoint}: {e}") from e

    def list_resumes(self):
        """List all resumes (metadata only)."""
        return self._request("GET", "resumes", params={"sort": "lastUpdatedAt"})

    def get_resume(self, resume_id):
        """Get full resume data by ID."""
        return self._request("GET", f"resumes/{resume_id}")

    def export_pdf(self, resume_id):
        """Export resume as PDF, returns download URL."""
        data = self._request("GET", f"resumes/{resume_id}/pdf")
        return data.get("url")

    def get_screenshot(self, resume_id):
        """Get resume screenshot, returns URL or None."""
        data = self._request("GET", f"resumes/{resume_id}/screenshot")
        return data.get("url")

    def create_resume(self, name, slug=None, tags=None):
        """Create a new empty resume, returns the resume ID (string)."""
        payload = {"name": name, "tags": tags or []}
        if slug:
            payload["slug"] = slug
        return self._request("POST", "resumes", json=payload)

    def update_resume(self, resume_id, data):
        """Update resume data using operations format.

        Args:
            resume_id: The resume UUID.
            data: Dict with keys like picture, basics, summary, sections, etc.
        """
        operations = [
            {"op": "replace", "path": f"/{key}", "value": value}
            for key, value in data.items()
        ]
        return self._request("PATCH", f"resumes/{resume_id}", json={"operations": operations})

    def import_resume(self, backup):
        """Import a backup JSON as a new resume.

        Creates a new resume with the backup's name+slug+tags, then patches
        it with the full data contents. Returns the updated resume object.
        """
        name = backup.get("name", "imported-resume")
        slug = backup.get("slug", name)
        tags = backup.get("tags", [])
        data = backup.get("data", {})

        resume_id = self.create_resume(name, slug, tags)
        if not resume_id:
            raise RuntimeError("Failed to create resume: no ID returned")

        result = self.update_resume(resume_id, data)
        print(f"  Imported '{name}' as {resume_id}")
        return result

    @staticmethod
    def download_file(url, dest):
        """Download a file from URL to destination path."""
        resp = requests.get(url, timeout=60, stream=True)
        resp.raise_for_status()
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return dest

    @staticmethod
    def load_backup(slug, backups_dir):
        """Load a backup JSON file by slug."""
        path = Path(backups_dir) / f"{slug}.json"
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
