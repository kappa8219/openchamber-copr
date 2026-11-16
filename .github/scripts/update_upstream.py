#!/usr/bin/env python3
"""Prepare an update PR for the latest stable OpenChamber release."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
API_URL = "https://api.github.com/repos/openchamber/openchamber/releases/latest"
ASSET_BASE = "https://github.com/openchamber/openchamber/releases/download/"
ASSET_NAMES = (
    "OpenChamber-{version}-linux-x86_64.rpm",
    "openchamber-web-{version}.tgz",
)


def request(url: str):
    req = Request(url, headers={"User-Agent": "openchamber-copr-release-check"})
    return urlopen(req, timeout=120)


def sha256(url: str) -> str:
    if not url.startswith(ASSET_BASE):
        raise ValueError(f"Unexpected upstream asset URL: {url}")
    digest = hashlib.sha256()
    with request(url) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    result, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"Expected one {label} in packaging files; found {count}")
    return result


def version_tuple(version: str) -> tuple[int, ...]:
    if not re.fullmatch(r"\d+(?:\.\d+)+", version):
        raise ValueError(f"Unsupported stable version format: {version}")
    return tuple(int(part) for part in version.split("."))


def main() -> int:
    with request(API_URL) as response:
        release = json.load(response)

    if release.get("draft") or release.get("prerelease"):
        raise ValueError("GitHub returned a draft or pre-release as the latest release")

    tag = release.get("tag_name", "")
    version = tag.removeprefix("v")
    version_tuple(version)

    desktop_spec_path = ROOT / "openchamber.spec"
    cli_spec_path = ROOT / "openchamber-cli.spec"
    makefile_path = ROOT / ".copr" / "Makefile"
    desktop_spec = desktop_spec_path.read_text()
    cli_spec = cli_spec_path.read_text()
    makefile = makefile_path.read_text()

    versions = []
    for path, text in ((desktop_spec_path, desktop_spec), (cli_spec_path, cli_spec)):
        match = re.search(r"^Version:\s+(\S+)$", text, re.MULTILINE)
        if not match:
            raise ValueError(f"Could not read package version from {path.name}")
        versions.append(match.group(1))
    if versions[0] != versions[1]:
        raise ValueError("Desktop and CLI package versions differ; refusing to update")

    current = versions[0]
    if version_tuple(version) <= version_tuple(current):
        print("updated=false")
        print(f"version={current}")
        print(f"release_url={release.get('html_url', '')}")
        return 0

    assets = {item.get("name"): item.get("browser_download_url") for item in release.get("assets", [])}
    asset_urls = {
        name.format(version=version): assets.get(name.format(version=version))
        for name in ASSET_NAMES
    }
    for name, url in asset_urls.items():
        if not url:
            raise ValueError(f"Missing expected upstream asset: {name}")

    desktop_hash = sha256(asset_urls[ASSET_NAMES[0].format(version=version)])
    cli_hash = sha256(asset_urls[ASSET_NAMES[1].format(version=version)])
    date = datetime.now(timezone.utc).strftime("%a %b %d %Y")

    desktop_spec = replace_once(
        desktop_spec,
        r"^(Version:\s+)\S+$",
        rf"\g<1>{version}",
        "desktop Version",
    )
    desktop_spec = replace_once(
        desktop_spec,
        r'^(echo ")[0-9a-f]{64}(  %\{SOURCE0\}" \| sha256sum --check)$',
        rf"\g<1>{desktop_hash}\g<2>",
        "desktop source checksum",
    )
    cli_spec = replace_once(
        cli_spec,
        r"^(Version:\s+)\S+$",
        rf"\g<1>{version}",
        "CLI Version",
    )
    cli_spec = replace_once(
        cli_spec,
        r'^(echo ")[0-9a-f]{64}(  %\{SOURCE0\}" \| sha256sum --check)$',
        rf"\g<1>{cli_hash}\g<2>",
        "CLI source checksum",
    )
    makefile = replace_once(
        makefile,
        r"^(version := )\S+$",
        rf"\g<1>{version}",
        "COPR Makefile version",
    )

    desktop_entry = (
        f"* {date} OpenChamber COPR <noreply@github.com> - {version}-1\n"
        f"- Update to OpenChamber {version}\n\n"
    )
    cli_entry = (
        f"* {date} OpenChamber COPR <noreply@github.com> - {version}-1\n"
        f"- Update web CLI to v{version}; keep bundled Node.js 24.22.3\n\n"
    )
    desktop_spec = replace_once(
        desktop_spec,
        r"^%changelog[ \t]*\n",
        "%changelog\n" + desktop_entry,
        "desktop changelog",
    )
    cli_spec = replace_once(
        cli_spec,
        r"^%changelog[ \t]*\n",
        "%changelog\n" + cli_entry,
        "CLI changelog",
    )

    desktop_spec_path.write_text(desktop_spec)
    cli_spec_path.write_text(cli_spec)
    makefile_path.write_text(makefile)

    print("updated=true")
    print(f"version={version}")
    print(f"release_url={release.get('html_url', '')}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:  # fail closed so no partial update PR is made
        print(f"Release update failed: {error}", file=sys.stderr)
        sys.exit(1)
