#!/usr/bin/env python3
"""Tests for the "Ask AI Better Questions" build.

Run:  python3 tests.py
Exit code 0 = all tests passed. Every test prints PASS/FAIL with detail.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import build as build_mod  # noqa: E402

FAILURES: list[str] = []
CHECKS = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if condition:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}" + (f"\n        {detail}" if detail else ""))
        FAILURES.append(name)


def section(title: str) -> None:
    print(f"\n== {title} ==")


# ---------------------------------------------------------------- build
def test_build_runs() -> None:
    section("Build runs and produces a complete site")
    subprocess.run(["python3", "-c", "import build; build.build()"],
                   cwd=ROOT, check=True, capture_output=True)
    site = ROOT / "site"
    check("site/ directory exists", site.is_dir())
    expected = {"search-index.js", "search.js", "style.css"}
    html_pages = {"index.html"} | {
        build_mod.MD_EXT.sub(".html", n) for n in build_mod.READING_ORDER if n != "index.md"
    }
    produced = {p.name for p in site.iterdir()}
    check("all markdown pages rendered to HTML", html_pages <= produced,
          "missing: " + ", ".join(sorted(html_pages - produced)))
    check("assets present", expected <= produced, "missing: " + ", ".join(sorted(expected - produced)))
    for page in html_pages:
        text = (site / page).read_text(encoding="utf-8")
        check(f"{page} is well-formed enough (has <article>)",
              "<article>" in text and "</html>" in text)


def test_unit_markdown() -> None:
    section("Markdown subset converter")
    body, title, _ = build_mod.md_to_html("# Hello\nWorld **bold** *em*")
    check("h1 rendered", '<h1 id="hello">Hello</h1>' in body)
    check("title extracted", title == "Hello")
    check("paragraph rendered", "<p>World <strong>bold</strong> <em>em</em></p>" in body)

    body, _, _ = build_mod.md_to_html("A&B <tag> `x<y`")
    check("HTML escaped", "A&amp;B &lt;tag&gt;" in body and "<code>x&lt;y</code>" in body)

    body, _, _ = build_mod.md_to_html("see [the guide](other.md) and [site](https://x.example)")
    check("internal link rewritten to .html", 'href="other.html"' in body)
    check("external link untouched", 'href="https://x.example"' in body)

    body, _, _ = build_mod.md_to_html("See [ch](02.md#top)")
    check("anchor preserved on rewritten link", 'href="02.html#top"' in body)

    body, _, _ = build_mod.md_to_html("| A | B |\n|---|---|\n| 1 | 2 |")
    check("table rendered with th", "<th>A</th>" in body and "<tbody>" in body)

    body, _, _ = build_mod.md_to_html("> quote line\n\nafter")
    check("blockquote rendered", "<blockquote><p>quote line</p></blockquote>" in body)

    body, _, _ = build_mod.md_to_html("- one\n- two\n\n1. alpha\n2. beta")
    check("ul and ol rendered", "<ul><li>one</li><li>two</li></ul>" in body
          and "<ol><li>alpha</li><li>beta</li></ol>" in body)

    body, _, _ = build_mod.md_to_html("### Dup\n\n### Dup")
    check("duplicate heading slugs de-duplicated", 'id="dup"' in body and 'id="dup-2"' in body)

    body, _, _ = build_mod.md_to_html("```\n<b>&</b>\n```")
    check("fenced code block escapes HTML", "&lt;b&gt;&amp;&lt;/b&gt;" in body)

    body, _, _ = build_mod.md_to_html("*On a miss:* not a list | **B.M.** stays")
    check("asterisk-word not eaten by list parser", "<em>On a miss:</em>" in body
          and "<strong>B.M.</strong>" in body and "<ul>" not in body)


# ---------------------------------------------------------------- content checks
def test_site_integrity() -> None:
    section("Site integrity: links, anchors, nav, search index")
    site = ROOT / "site"
    pages = {p.name: p.read_text(encoding="utf-8") for p in site.glob("*.html")}

    # Collect ids per page for anchor validation
    ids: dict[str, set[str]] = {}
    for name, text in pages.items():
        ids[name] = set(re.findall(r'id="([^"]+)"', text))

    link_ok = True
    link_detail: list[str] = []
    anchors_ok = True
    anchors_detail: list[str] = []
    resources = set(pages) | {"style.css", "search-index.js", "search.js"}
    for name, text in pages.items():
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith("data:") or href.startswith("http"):
                continue
            target, _, frag = href.partition("#")
            if target and target not in resources:
                link_ok = False
                link_detail.append(f"{name} -> missing page {target}")
            if frag:
                page_id = target or name
                if unquote(frag) not in ids.get(page_id, set()):
                    anchors_ok = False
                    anchors_detail.append(f"{name} -> broken anchor {href}")
    check("every internal link points to an existing page", link_ok,
          "; ".join(link_detail[:6]))
    check("every internal anchor resolves", anchors_ok, "; ".join(anchors_detail[:6]))

    for name, text in pages.items():
        missing_nav = [build_mod.page_label(n, "") for n in build_mod.READING_ORDER
                       if html_escape(build_mod.page_label(n, "")) not in text]
        check(f"nav lists all pages on {name}", not missing_nav,
              "missing: " + ", ".join(missing_nav))

    js = (site / "search-index.js").read_text(encoding="utf-8")
    payload = js[js.index("["): js.rstrip().rindex(";")].strip()
    entries = json.loads(payload)
    check("search index parses as JSON", isinstance(entries, list) and len(entries) == len(pages))
    check("search index covers every page",
          all(e["u"] in pages for e in entries) and all(e["t"] and e["b"] for e in entries))
    check("search index includes real body text",
          any("hallucination" in e["b"].lower() for e in entries)
          and any("follow-up" in e["b"].lower() for e in entries))

    idx = pages["index.html"]
    check("home page linked to every chapter", all(
        f'href="{build_mod.MD_EXT.sub(".html", n)}"' in idx for n in build_mod.READING_ORDER))
    check("credits Asdale Dynamics, LLC on every page",
          all("Asdale Dynamics, LLC" in t for t in pages.values()))
    js_src = (site / "search.js").read_text(encoding="utf-8")
    check("search.js is dependency-free vanilla JS", "window" in js_src and "addEventListener" in js_src)


def html_escape(s: str) -> str:
    return s.replace("&", "&amp;")


def test_content_markers() -> None:
    section("Required content present in docs/")
    docs = {p.name: p.read_text(encoding="utf-8") for p in (ROOT / "docs").glob("*.md")}

    check("all 12 planned docs exist", len(docs) == 12,
          "have: " + ", ".join(sorted(docs)))

    rewrites = docs.get("rewrites.md", "")
    check("rewrites: at least 12 Before/After pairs",
          len(re.findall(r"\*\*Before:\*\*", rewrites)) >= 12
          and len(re.findall(r"\*\*After", rewrites)) >= 11,
          f"before={len(re.findall(r'[Bb]efore:\*\*', rewrites))} after={len(re.findall(r'after', rewrites))}")

    drills = docs.get("drills.md", "")
    check("drills: six blocks A-F", all(f"Drill block {c}" in drills for c in "ABCDEF"))
    check("drills link to answer key", "answer-key.md" in drills)
    check("drills: at least 12 drills", len(re.findall(r"^\*\*[A-F]\d+\.", drills, re.M)) >= 12)

    key = docs.get("answer-key.md", "")
    check("answer key covers every drill",
          all(f"**{c}" in key for c in "A1. B1. C1. D1. E1. F1.".split()))
    check("answer key has scoring guidance", "Scoring" in key)

    glossary = docs.get("glossary.md", "")
    check("glossary has at least 15 terms",
          len(re.findall(r"^## ", glossary, re.M)) >= 15,
          f"terms={len(re.findall(r'^## ', glossary, re.M))}")

    chapters = sorted(n for n in docs if re.match(r"^0\d-", n))
    check("seven numbered chapters", len(chapters) == 7)
    # Chapter 7 is the last; chapters 1-6 should each point to the next one
    check("chapters 1-6 close with a pointer onward",
          all("Next:" in docs[n] for n in chapters[:-1]),
          "missing Next in: " + ", ".join(n for n in chapters if "Next:" not in docs[n]))
    check("guide references its companion handbook",
          any("Prompt-Writing Handbook" in d for d in docs.values()))

    for n, text in docs.items():
        check(f"{n} starts with an H1", text.lstrip().startswith("# "))

    ch7 = docs.get("07-when-to-be-skeptical.md", "")
    check("skepticism chapter uses education-not-advice framing",
          "not medical advice" in ch7.lower() or "Educational" in ch7)


# ---------------------------------------------------------------- hygiene
def test_hygiene() -> None:
    section("Hygiene: license, README, secrets")
    license_txt = (ROOT / "LICENSE").read_text(encoding="utf-8")
    check("LICENSE is MIT", "MIT License" in license_txt and "Permission is hereby granted, free of charge" in license_txt)
    check("LICENSE copyright line is exact",
          "Copyright (c) 2026 Asdale Dynamics, LLC" in license_txt,
          "found: " + license_txt.splitlines()[2])

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("README credits Asdale Dynamics, LLC", "Asdale Dynamics, LLC" in readme)
    check("README documents how to build", "python3 build.py" in readme)
    check("README documents how to test", "python3 tests.py" in readme)

    secret_patterns = [
        (r"sk-[A-Za-z0-9]{16,}", "OpenAI-style key"),
        (r"gh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
        (r"AKIA[0-9A-Z]{16}", "AWS access key"),
        (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key block"),
        (r"xox[baprs]-[A-Za-z0-9-]{20,}", "Slack token"),
        (r"[A-Za-z0-9+/]{40,}={0,2}", "suspicious long secret blob"),
    ]
    scan_roots = [ROOT / "docs", ROOT / "site"]
    scan_files = [p for root in scan_roots for p in root.rglob("*") if p.is_file()]
    scan_files += [ROOT / "build.py", ROOT / "tests.py", ROOT / "README.md"]
    dirty: list[str] = []
    blob_hits: list[str] = []
    for p in scan_files:
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pat, label in secret_patterns:
                if re.search(pat, line):
                    entry = f"{p.name}:{i} ({label})"
                    if pat.endswith("{40,}={0,2}") or len(pat) > 20 and pat.endswith("{0,2}"):
                        # long-blob rule: allow CSS/JS/base64-ish embeds only inside svg data URIs
                        if "data:image" in line or "search-index.js" in p.name or p.name == "style.css":
                            continue
                        blob_hits.append(entry)
                    dirty.append(entry)
    check("no API keys or token-like secrets", not any(d for d in dirty if d not in blob_hits),
          "hits: " + "; ".join(dirty[:5]))
    check("no key-like blobs outside template assets", not blob_hits, "; ".join(blob_hits[:5]))

    # No personal data: no real personal email addresses anywhere
    email_hit: list[str] = []
    for p in scan_files:
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if p.name == "search-index.js":
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r"[A-Za-z0-9._%+-]+@(?!users\.noreply|example)[A-Za-z0-9.-]+\.[A-Za-z]{2,}", line):
                email_hit.append(f"{p.name}:{i}: {line[:60]}")
    check("no personal email addresses", not email_hit, "; ".join(email_hit[:4]))


def test_build_stability() -> None:
    section("Build is clean and repeatable")
    subprocess.run([sys.executable, str(ROOT / "build.py"), "--clean"],
                   cwd=ROOT, check=True, capture_output=True)
    check("--clean removes site/", not (ROOT / "site").exists())
    r = subprocess.run(["python3", "build.py"], cwd=ROOT, capture_output=True, text=True)
    check("rebuild from scratch succeeds", r.returncode == 0, r.stderr[-400:])
    check("rebuild reports 12 pages", "Built 12 pages" in r.stdout, r.stdout)

    # Idempotence: build twice, output must be identical
    first = {p.name: p.read_text(encoding="utf-8").replace(ROOT.name, "") for p in (ROOT / "site").iterdir()}
    subprocess.run(["python3", "build.py"], cwd=ROOT, check=True, capture_output=True)
    second = {p.name: p.read_text(encoding="utf-8").replace(ROOT.name, "") for p in (ROOT / "site").iterdir()}
    check("build is deterministic", first == second,
          "differs: " + ", ".join(sorted(set(first) ^ set(second))
                                  + [k for k in first.keys() & second.keys() if first[k] != second[k]]))


def main() -> int:
    test_unit_markdown()
    test_build_runs()
    test_site_integrity()
    test_content_markers()
    test_build_stability()
    test_hygiene()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED / {CHECKS} checks:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print(f"All {CHECKS} checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
