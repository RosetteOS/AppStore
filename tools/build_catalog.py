#!/usr/bin/env python3
"""
Rosette App Store Catalog Builder & Validator

Scans per-app JSON definitions, validates schemas, computes checksums (optional),
and compiles a unified dist/apps.json (and dist/catalog.json) suitable for distribution.
"""

import os
import sys
import json
import glob
import hashlib
import argparse
import urllib.request
from datetime import datetime, timezone

REQUIRED_FIELDS = ["id", "name", "category", "description", "author", "version", "type"]
VALID_CATEGORIES = ["web_ui", "touch_ui", "plugin", "tool"]
VALID_TYPES = ["web_ui", "touch_ui", "plugin", "tool"]


def validate_app_schema(app: dict, filename: str) -> list:
    errors = []
    for f in REQUIRED_FIELDS:
        if f not in app or not app[f]:
            errors.append(f"Missing required field '{f}' in {filename}")

    cat = app.get("category")
    if cat not in VALID_CATEGORIES:
        errors.append(f"Invalid category '{cat}' in {filename}. Valid: {VALID_CATEGORIES}")

    t = app.get("type")
    if t not in VALID_TYPES:
        errors.append(f"Invalid type '{t}' in {filename}. Valid: {VALID_TYPES}")

    is_builtin = app.get("is_builtin", False)
    if is_builtin:
        if not app.get("builtin_path"):
            errors.append(f"Built-in app '{app.get('id')}' must define 'builtin_path'")
    else:
        if not app.get("download_url") and not app.get("install_path"):
            errors.append(f"External app '{app.get('id')}' must define 'download_url' and 'install_path'")

    if "changelog" in app and app["changelog"] is not None:
        cl = app["changelog"]
        if isinstance(cl, list):
            for idx, entry in enumerate(cl):
                if isinstance(entry, dict):
                    if not entry.get("version") or not isinstance(entry.get("version"), str):
                        errors.append(f"Changelog entry #{idx} in {filename} missing string 'version'")
                    changes = entry.get("changes")
                    if not isinstance(changes, (list, str)) or not changes:
                        errors.append(f"Changelog entry #{idx} in {filename} must have non-empty 'changes' (list or string)")
                elif not isinstance(entry, str):
                    errors.append(f"Changelog entry #{idx} in {filename} must be an object or string")
        elif not isinstance(cl, str):
            errors.append(f"'changelog' in {filename} must be a list of version entries or a string")

    return errors


def fetch_url_sha256(url: str) -> str:
    print(f"Fetching and computing sha256 for: {url}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Rosette-AppStore-Builder/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        h = hashlib.sha256()
        while chunk := resp.read(65536):
            h.update(chunk)
        return h.hexdigest()


def build_catalog(repo_root: str, compute_hashes: bool = False, check_urls: bool = False) -> dict:
    categories_file = os.path.join(repo_root, "categories.json")
    if not os.path.isfile(categories_file):
        raise FileNotFoundError(f"Missing categories.json at {categories_file}")

    with open(categories_file, "r", encoding="utf-8") as f:
        categories = json.load(f)

    apps_glob = os.path.join(repo_root, "apps", "**", "*.json")
    app_files = sorted(glob.glob(apps_glob, recursive=True))

    apps = []
    all_errors = []

    for af in app_files:
        try:
            with open(af, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            all_errors.append(f"JSON parse error in {af}: {e}")
            continue

        rel_path = os.path.relpath(af, repo_root)
        errs = validate_app_schema(data, rel_path)
        if errs:
            all_errors.extend(errs)
            continue

        if not data.get("is_builtin") and data.get("download_url"):
            url = data["download_url"]
            filename = os.path.basename(url.split("?")[0])
            local_pkg = os.path.join(repo_root, "packages", filename)
            if os.path.isfile(local_pkg):
                with open(local_pkg, "rb") as pf:
                    computed_sha = hashlib.sha256(pf.read()).hexdigest()
                if data.get("sha256") != computed_sha:
                    print(f"Updating sha256 for {data['id']} from local package {filename}: {data.get('sha256')} -> {computed_sha}")
                    data["sha256"] = computed_sha
                    with open(af, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                        f.write("\n")
            elif compute_hashes:
                try:
                    computed_sha = fetch_url_sha256(data["download_url"])
                    if data.get("sha256") and data["sha256"] != computed_sha:
                        print(f"Updating sha256 for {data['id']}: {data['sha256']} -> {computed_sha}")
                    data["sha256"] = computed_sha
                    with open(af, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                        f.write("\n")
                except Exception as e:
                    all_errors.append(f"Failed to fetch {data['download_url']} for {data['id']}: {e}")

        apps.append(data)

    if all_errors:
        print("Validation errors encountered:", file=sys.stderr)
        for err in all_errors:
            print(f" - {err}", file=sys.stderr)
        raise ValueError(f"{len(all_errors)} catalog validation error(s) found.")

    catalog = {
        "version": "1.0",
        "name": "Rosette App Store Catalog",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "categories": categories,
        "apps": apps
    }
    return catalog


def main():
    parser = argparse.ArgumentParser(description="Rosette App Store Catalog Builder")
    parser.add_argument("--repo-root", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
                        help="Root directory of AppStore repository")
    parser.add_argument("--output-dir", default=None, help="Directory to write output files")
    parser.add_argument("--compute-hashes", action="store_true", help="Download external archives to compute SHA256 hashes")
    parser.add_argument("--check-urls", action="store_true", help="Check that download URLs exist")
    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    output_dir = args.output_dir or os.path.join(repo_root, "dist")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Building Rosette App Store catalog from {repo_root}...")
    try:
        catalog = build_catalog(repo_root, compute_hashes=args.compute_hashes, check_urls=args.check_urls)
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)

    apps_out = os.path.join(output_dir, "apps.json")
    catalog_out = os.path.join(output_dir, "catalog.json")
    root_apps_out = os.path.join(repo_root, "apps.json")

    with open(apps_out, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")

    with open(catalog_out, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")

    with open(root_apps_out, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")

    configs_src = os.path.join(repo_root, "configs")
    configs_dst = os.path.join(output_dir, "configs")
    if os.path.isdir(configs_src):
        import shutil
        os.makedirs(configs_dst, exist_ok=True)
        for cf in os.listdir(configs_src):
            s = os.path.join(configs_src, cf)
            d = os.path.join(configs_dst, cf)
            if os.path.isfile(s):
                shutil.copy2(s, d)

    # Publish app icons alongside the catalog
    icons_src = os.path.join(repo_root, "icons")
    if os.path.isdir(icons_src):
        import shutil
        shutil.copytree(icons_src, os.path.join(output_dir, "icons"), dirs_exist_ok=True)

    # Copy website landing page assets
    site_src = os.path.join(repo_root, "site")
    if os.path.isdir(site_src):
        import shutil
        for sf in os.listdir(site_src):
            s = os.path.join(site_src, sf)
            d = os.path.join(output_dir, sf)
            if os.path.isfile(s):
                shutil.copy2(s, d)
            elif os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)

    print(f"OK: Catalog and landing page built successfully with {len(catalog['apps'])} apps across {len(catalog['categories'])} categories.")
    print(f"    - {apps_out}")
    print(f"    - {catalog_out}")
    print(f"    - {root_apps_out}")
    print(f"    - {os.path.join(output_dir, 'index.html')}")


if __name__ == "__main__":
    main()
