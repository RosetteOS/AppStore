#!/usr/bin/env python3
"""
Unit tests for Rosette App Store repository and catalog builder.
"""

import os
import sys
import json
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))

from build_catalog import build_catalog, validate_app_schema


class TestAppStoreCatalog(unittest.TestCase):
    def setUp(self):
        self.repo_root = REPO_ROOT
        self.categories_file = os.path.join(self.repo_root, "categories.json")

    def test_categories_schema(self):
        self.assertTrue(os.path.isfile(self.categories_file), "categories.json must exist")
        with open(self.categories_file, "r", encoding="utf-8") as f:
            categories = json.load(f)

        self.assertIsInstance(categories, list)
        self.assertGreaterEqual(len(categories), 4)

        category_ids = set()
        for cat in categories:
            self.assertIn("id", cat)
            self.assertIn("name", cat)
            self.assertIn("icon", cat)
            self.assertNotIn(cat["id"], category_ids, f"Duplicate category id: {cat['id']}")
            category_ids.add(cat["id"])

        self.assertIn("web_ui", category_ids)
        self.assertIn("touch_ui", category_ids)
        self.assertIn("plugin", category_ids)
        self.assertIn("tool", category_ids)

    def test_catalog_compilation(self):
        catalog = build_catalog(self.repo_root, compute_hashes=False)
        self.assertIn("version", catalog)
        self.assertGreaterEqual(len(catalog["apps"]), 8)

        app_ids = set()
        for app in catalog["apps"]:
            self.assertNotIn(app["id"], app_ids, f"Duplicate app ID: {app['id']}")
            app_ids.add(app["id"])
            errs = validate_app_schema(app, f"app:{app['id']}")
            self.assertEqual(errs, [], f"Validation errors in {app['id']}: {errs}")

        # Verify key baseline apps exist
        self.assertIn("mainsail", app_ids)
        self.assertIn("fluidd", app_ids)
        self.assertIn("guppyscreen", app_ids)
        self.assertIn("helixscreen", app_ids)
        self.assertIn("timelapse", app_ids)
        self.assertIn("mobileraker", app_ids)
        self.assertIn("spoolman", app_ids)
        self.assertIn("octoapp", app_ids)
        self.assertIn("klipper-backup", app_ids)

    def test_schema_validator_catches_invalid_app(self):
        invalid_app = {
            "id": "bad_app",
            "category": "non_existent_category",
            "type": "invalid_type"
        }
        errs = validate_app_schema(invalid_app, "dummy.json")
        self.assertGreater(len(errs), 0)

    def test_landing_page_assets(self):
        site_dir = os.path.join(self.repo_root, "site")
        self.assertTrue(os.path.isdir(site_dir), "site/ directory must exist")
        self.assertTrue(os.path.isfile(os.path.join(site_dir, "index.html")), "site/index.html must exist")
        self.assertTrue(os.path.isfile(os.path.join(site_dir, "style.css")), "site/style.css must exist")
        self.assertTrue(os.path.isfile(os.path.join(site_dir, "app.js")), "site/app.js must exist")


if __name__ == "__main__":
    unittest.main(verbosity=2)
