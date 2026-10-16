#!/usr/bin/env python3
"""Read-only summary of a public GitHub repository using the GitHub REST API."""

from __future__ import annotations

import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"
USER_AGENT = "HToolboxGuides-RepoAudit/1.0"


def fetch_repository(owner: str, name: str) -> dict:
    owner = quote(owner, safe="")
    name = quote(name, safe="")
    url = f"{API_ROOT}/repos/{owner}/{name}"
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=10) as response:
            data = json.load(response)
    except HTTPError as exc:
        if exc.code == 404:
            raise RuntimeError(
                "Repository not found or not public. Check the owner/name."
            ) from exc
        if exc.code == 403:
            raise RuntimeError(
                "GitHub API rate limit or access restriction. Wait and try again."
            ) from exc
        raise RuntimeError(f"GitHub API returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach GitHub API: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError("The request to GitHub API timed out.") from exc

    if not isinstance(data, dict):
        raise RuntimeError("Unexpected response format from GitHub API.")
    return data


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python3 main.py OWNER REPOSITORY", file=sys.stderr)
        return 2

    owner, name = argv[1], argv[2]
    if not owner.strip() or not name.strip():
        print("Owner and repository name must not be empty.", file=sys.stderr)
        return 2

    try:
        repo = fetch_repository(owner, name)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    license_info = repo.get("license") or {}
    topics = repo.get("topics") or []
    values = [
        ("Repository", repo.get("full_name", "unknown")),
        ("URL", repo.get("html_url", "unknown")),
        ("Description", repo.get("description") or "(none)"),
        ("Visibility", repo.get("visibility", "unknown")),
        ("Default branch", repo.get("default_branch", "unknown")),
        ("Language", repo.get("language") or "(not detected)"),
        ("License", license_info.get("spdx_id") or "(not specified)"),
        ("Stars", repo.get("stargazers_count", 0)),
        ("Forks", repo.get("forks_count", 0)),
        ("Open issues", repo.get("open_issues_count", 0)),
        ("Topics", ", ".join(topics) if topics else "(none)"),
        ("Created", repo.get("created_at", "unknown")),
        ("Last updated", repo.get("updated_at", "unknown")),
    ]
    width = max(len(label) for label, _ in values)
    for label, value in values:
        print(f"{label:<{width}} : {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
