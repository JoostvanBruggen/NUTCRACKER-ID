#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
"""Technische controles met zelfgemaakte geometrische afbeeldingen."""
from pathlib import Path
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote
from PIL import Image, ImageDraw, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("nutcracker_prototype", ROOT / "nutcracker_id.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.images.append(dict(attrs)["src"])


class SyntheticTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".synthetische-test-", dir=ROOT)
        self.base = Path(self.temp.name).resolve()
        if not self.base.is_relative_to(ROOT):
            raise RuntimeError("Testmap valt buiten project.")
        self.addCleanup(self.temp.cleanup)
        self.photos = self.base / "input"
        self.photos.mkdir()
        for name, shift in [("DEMO A #1.png", 0), ("DEMO B %.png", 3)]:
            im = Image.new("RGB", (320, 240), (210, 210, 210))
            draw = ImageDraw.Draw(im)
            draw.ellipse((30, 15, 195, 215), fill=(85, 85, 85))
            for x, y in [(65, 45), (90, 38), (125, 42), (70, 70),
                         (135, 65), (80, 105), (115, 100), (90, 140)]:
                draw.ellipse((x+shift, y, x+shift+7, y+7), fill="white")
            draw.ellipse((98, 48, 114, 64), fill=(235, 235, 235))
            draw.ellipse((103, 53, 109, 59), fill=(25, 25, 25))
            draw.polygon([(120, 58), (220, 58), (130, 69)], fill=(45, 45, 45))
            metadata = PngImagePlugin.PngInfo()
            metadata.add_text("Photographer", "Synthetic test fixture")
            im.save(self.photos / name, pnginfo=metadata)

    def run_cli(self, *args):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "nutcracker_id.py"), *map(str, args)],
            cwd=self.base, capture_output=True, text=True, encoding="utf-8",
            env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
            timeout=90,
        )
        return result

    def check_links(self, report):
        parser = Links()
        parser.feed(report.read_text(encoding="utf-8"))
        self.assertTrue(parser.images)
        for src in parser.images:
            self.assertFalse(src.startswith(("file:", "http:", "https:", "data:")))
            resolved = (report.parent / unquote(src)).resolve()
            self.assertTrue(resolved.is_relative_to(report.parent.resolve()))
            self.assertTrue(resolved.is_file(), src)

    def test_no_arguments_only_help(self):
        before = set(self.base.rglob("*"))
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--photos", result.stdout)
        self.assertEqual(before, set(self.base.rglob("*")))

    def test_help(self):
        self.assertEqual(self.run_cli("--help").returncode, 0)

    def test_missing_input_has_no_output(self):
        output = self.base / "must-not-exist"
        result = self.run_cli("--photos", self.base / "missing", "--output", output)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(output.exists())

    def test_crop_requires_explicit_input(self):
        result = self.run_cli("--crop-review")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.base / ".local-output").exists())

    def test_empty_input_has_no_output(self):
        empty = self.base / "empty"
        empty.mkdir()
        output = self.base / "must-not-exist"
        self.assertEqual(self.run_cli("--photos", empty, "--output", output).returncode, 2)
        self.assertFalse(output.exists())

    def test_pattern_output_and_unchanged_inputs(self):
        before = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                  for f in self.photos.iterdir()}
        output = self.base / "patterns"
        result = self.run_cli("--photos", self.photos, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((output / "groepsindeling.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["photos"]), 2)
        self.check_links(output / "index.html")
        self.assertEqual(before, {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                                 for f in self.photos.iterdir()})

    def test_crop_output_is_self_contained(self):
        output = self.base / "crops"
        result = self.run_cli("--photos", self.photos, "--crop-review",
                              "--crop-output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((output / "kopdetectie.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data), 2)
        self.assertTrue(all(r["visual_review"] == "niet beoordeeld" for r in data))
        self.check_links(output / "index.html")
        for original in (output / "originals").glob("*.png"):
            with Image.open(original) as im:
                self.assertFalse(im.getexif())
                self.assertNotIn("Photographer", im.info)

    def test_small_image_returns_unknown(self):
        im = Image.new("RGB", (12, 12), "gray")
        self.assertEqual(MODULE.find_eye(MODULE.gray(im)), (None, 0.0))
        self.assertIsNone(MODULE.locate_head_crop(im)[0])

    def test_group_cannot_extend_through_only_one_link(self):
        pairs = [
            {"a": "A", "b": "B", "score": 90, "region_count": 3, "matched_features": 8},
            {"a": "A", "b": "C", "score": 85, "region_count": 3, "matched_features": 8},
            {"a": "B", "b": "C", "score": 20, "region_count": 3, "matched_features": 8},
        ]
        groups = MODULE.candidate_groups(pairs)
        self.assertEqual(groups, [["A", "B"]])

    def test_all_pairs_can_form_group(self):
        pairs = [{"a": a, "b": b, "score": 90, "region_count": 3, "matched_features": 8}
                 for a, b in [("A", "B"), ("A", "C"), ("B", "C")]]
        self.assertEqual(MODULE.candidate_groups(pairs), [["A", "B", "C"]])



    def test_invalid_png_has_no_output(self):
        (self.photos / "invalid.png").write_text("synthetic non-image", encoding="utf-8")
        output = self.base / "must-not-exist"
        self.assertEqual(self.run_cli("--photos", self.photos, "--output", output).returncode, 2)
        self.assertFalse(output.exists())

    def test_output_inside_input_rejected(self):
        output = self.photos / "output"
        self.assertEqual(self.run_cli("--photos", self.photos, "--output", output).returncode, 2)
        self.assertFalse(output.exists())

    @unittest.skipUnless(sys.platform == "win32", "PowerShell-controle op Windows")
    def test_powershell_wrappers_from_other_working_directory(self):
        for script, json_file in [
            ("start_nutcracker_id.ps1", "groepsindeling.json"),
            ("start_kopdetectie_review.ps1", "kopdetectie.json"),
        ]:
            output = self.base / script.removesuffix(".ps1")
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-File", str(ROOT / script),
                 "-PythonExecutable", sys.executable,
                 "-Photos", str(self.photos.relative_to(ROOT)),
                 "-Output", str(output.relative_to(ROOT))],
                cwd=self.base, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=90,
            )
            if result.returncode != 0 and "UnauthorizedAccess" in result.stderr and "running scripts is disabled" in result.stderr:
                self.skipTest("Lokaal PowerShell-uitvoeringsbeleid blokkeert scripts; beleid niet gewijzigd.")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / json_file).is_file())
            self.assertTrue((output / "index.html").is_file())
            self.check_links(output / "index.html")


if __name__ == "__main__":
    unittest.main(verbosity=2)
