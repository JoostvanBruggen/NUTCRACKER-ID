#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
"""Controle van de exacte openbare bestandenlijst en SHA-256-vingerafdrukken."""
from pathlib import Path
import hashlib
import re
import sys


def main():
    root = Path(__file__).resolve().parent.parent
    names = (root / "PUBLICATIEBESTANDEN.txt").read_text(encoding="utf-8").splitlines()
    if len(names) != len(set(names)):
        raise SystemExit("Dubbele namen in de bestandenlijst.")
    for name in names:
        path = Path(name)
        if not name or path.is_absolute() or ".." in path.parts or "\\" in name:
            raise SystemExit("Ongeldige naam in de bestandenlijst.")
    actual = {f.relative_to(root).as_posix() for f in root.rglob("*") if f.is_file()}
    errors = []
    if actual != set(names):
        errors.append("Bestandenlijst wijkt af: " + ", ".join(sorted(actual ^ set(names))))
    for path in root.rglob("*"):
        if path.is_symlink() or path.is_junction():
            errors.append("Koppeling aangetroffen: " + path.relative_to(root).as_posix())
    checksums = {}
    for line in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        checksums[name] = digest
    if set(checksums) != set(names) - {"SHA256SUMS"}:
        errors.append("SHA256SUMS dekt niet exact alle overige openbare bestanden.")
    for name, expected in checksums.items():
        path = root / name
        if name not in names or not path.is_file():
            errors.append("Ontbrekend of onverwacht hashbestand: " + name)
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append("Bestand gewijzigd sinds de controle: " + name)
    patterns = [
        r"\b[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]",
        r"/(?:home|Users)/[^/\s]+/",
        r"data:image/[^;\s]+;base64,",
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"IMG_[A-Z0-9]{5}\.png",
        r"(?i)(?:password|api_key|access_token)\s*=\s*['\"][^'\"]{6,}['\"]",
    ]
    for name in names:
        path = root / name
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append("Niet-tekstbestand: " + name)
            continue
        if any(re.search(pattern, content) for pattern in patterns):
            errors.append("Handmatige privacycontrole nodig: " + name)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {len(names)} toegestane tekstbestanden; hashes kloppen; "
          "geen onverwachte bestanden of bekende privésignalen.")
    print("Controleer ook rechten, inhoud en eventuele Git-geschiedenis vóór publicatie.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
