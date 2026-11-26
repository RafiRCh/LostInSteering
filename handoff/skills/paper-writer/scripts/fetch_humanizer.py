#!/usr/bin/env python3
"""Fetch the latest humanizer skill (github.com/blader/humanizer) for paper-writer.

Usage:
    python fetch_humanizer.py            # fetch from the main branch
    python fetch_humanizer.py --ref v4.0.0

Downloads SKILL.md from the humanizer repository, checks that it looks like the
humanizer skill, and saves it to a cache folder. If the download fails, it falls
back to the snapshot bundled in vendor/humanizer/. Either way it prints one line
starting with HUMANIZER_PATH= that names the file to read, and one line starting
with HUMANIZER_SOURCE= saying whether it is live or the bundled fallback.

Standard library only, so it runs on Windows, macOS and Linux. It respects the
HTTPS_PROXY / HTTP_PROXY environment variables through urllib.
"""
import argparse
import os
import re
import sys
import tempfile
import urllib.request

REPO = "blader/humanizer"
RAW = "https://raw.githubusercontent.com/{repo}/{ref}/SKILL.md"
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
VENDOR = os.path.join(SKILL_DIR, "vendor", "humanizer", "SKILL.md")


def version_of(text):
    m = re.search(r'^\s*version:\s*"?([^"\n]+)"?', text, re.M)
    return m.group(1).strip() if m else "unknown"


def looks_valid(text):
    head = text[:2000]
    return text.startswith("---") and re.search(r"^name:\s*humanizer\s*$", head, re.M) and len(text) > 2000


def cache_dir():
    # Prefer a cache next to the skill; fall back to a temp folder when the
    # skill folder is read-only (for example an installed or synced skill).
    for base in (os.path.join(SKILL_DIR, ".cache"), os.path.join(tempfile.gettempdir(), "paper-writer-cache")):
        try:
            os.makedirs(base, exist_ok=True)
            probe = os.path.join(base, ".write-test")
            with open(probe, "w") as f:
                f.write("ok")
            os.remove(probe)
            return base
        except OSError:
            continue
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="main", help="branch or tag to fetch (default: main)")
    ap.add_argument("--timeout", type=float, default=20)
    args = ap.parse_args()

    url = RAW.format(repo=REPO, ref=args.ref)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "paper-writer-skill"})
        with urllib.request.urlopen(req, timeout=args.timeout) as r:
            text = r.read().decode("utf-8")
        if not looks_valid(text):
            raise ValueError("downloaded file does not look like the humanizer SKILL.md")
        out_dir = cache_dir()
        if out_dir is None:
            raise OSError("no writable cache folder")
        out = os.path.join(out_dir, "humanizer-SKILL.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print("HUMANIZER_SOURCE=live")
        print("HUMANIZER_URL=" + url)
        print("HUMANIZER_VERSION=" + version_of(text))
        print("HUMANIZER_PATH=" + out)
        return 0
    except Exception as e:  # network blocked, proxy refused, 404, bad content
        print("HUMANIZER_FETCH_ERROR=" + str(e).replace("\n", " "), file=sys.stderr)
        if os.path.exists(VENDOR):
            with open(VENDOR, encoding="utf-8") as f:
                v = version_of(f.read())
            print("HUMANIZER_SOURCE=bundled-fallback")
            print("HUMANIZER_VERSION=" + v)
            print("HUMANIZER_PATH=" + VENDOR)
            return 0
        print("HUMANIZER_SOURCE=none")
        return 1


if __name__ == "__main__":
    sys.exit(main())
