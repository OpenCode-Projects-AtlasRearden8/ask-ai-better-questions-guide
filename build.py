#!/usr/bin/env python3
"""Build the "Ask AI Better Questions" static HTML site from docs/*.md.

Local-first and dependency-free: Python 3 standard library only, no
network access, no external packages. Output goes to site/.

Usage:
    python3 build.py            # build the site
    python3 build.py --clean    # delete the site/ directory
"""

from __future__ import annotations

import argparse
import html as html_mod
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
SITE_DIR = ROOT / "site"

TITLE = "Ask AI Better Questions"
SUBTITLE = "A short guide to question-asking as a skill"
# Pages in reading order. index.md becomes site/index.html (the home page).
READING_ORDER = [
    "index.md",
    "01-questions-are-the-skill.md",
    "02-give-the-model-context.md",
    "03-layered-follow-ups.md",
    "04-ask-for-critique-not-answers.md",
    "05-what-am-i-missing.md",
    "06-steering-long-tasks.md",
    "07-when-to-be-skeptical.md",
    "rewrites.md",
    "drills.md",
    "answer-key.md",
    "glossary.md",
]

# --------------------------------------------------------------------------
# Minimal markdown subset -> HTML
# Supports: ATX headings, paragraphs, bullet/numbered lists, pipe tables,
# blockquotes, fenced code blocks, horizontal rules, bold/italic/inline code,
# and markdown links (internal .md links are rewritten to .html).
# --------------------------------------------------------------------------

MD_EXT = re.compile(r"\.md\b")

_slug_counts: dict[str, int] = {}


def slugify(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text)  # strip any inline markup
    s = s.replace("&amp;", "&").lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s or "section"


def unique_slug(title_html: str) -> str:
    base = slugify(title_html)
    n = _slug_counts.get(base, 0)
    _slug_counts[base] = n + 1
    return base if n == 0 else f"{base}-{n + 1}"


def rewrite_link_target(target: str) -> str:
    t = target.strip()
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", t) or t.startswith("#"):
        return t  # external or same-page anchor
    return MD_EXT.sub(".html", t)


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(text: str) -> str:
    """Render inline markdown (code, links, bold, italic). Text is raw."""
    out = []
    # Split around code spans so their contents are verbatim.
    parts = re.split(r"(`[^`]+`)", text)
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            out.append(f"<code>{_escape(part[1:-1])}</code>")
            continue
        t = _escape(part)
        t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                   lambda m: f'<a href="{html_mod.escape(rewrite_link_target(m.group(2)), quote=True)}">{m.group(1)}</a>',
                   t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
        out.append(t)
    return "".join(out)


def _render_cell(raw: str) -> str:
    return _inline(raw.strip())


def _table_html(rows: list[list[str]]) -> str:
    if len(rows) < 2:
        return ""
    head = (
        "<thead><tr>"
        + "".join(f"<th>{_render_cell(c)}</th>" for c in rows[0])
        + "</tr></thead>"
    )
    body = "<tbody>" + "".join(
        "<tr>" + "".join(f"<td>{_render_cell(c)}</td>" for c in row) + "</tr>"
        for row in rows[2:]
    ) + "</tbody>"
    return f"<table>{head}{body}</table>"


def _is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|")


def _split_row(line: str) -> list[str]:
    return [c for c in line.strip()[1:-1].split("|")]


def _is_sep_row(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells) and bool(cells)


def md_to_html(md_text: str) -> tuple[str, str, dict[str, str]]:
    """Convert markdown to HTML. Returns (html, title, toc) where toc maps
    heading slug -> heading text."""
    _slug_counts.clear()
    lines = md_text.splitlines()
    blocks: list[str] = []
    toc: dict[str, str] = {}
    para: list[str] = []
    i = 0
    title = ""

    def flush_para() -> None:
        nonlocal para
        if para:
            blocks.append(f"<p>{_inline(' '.join(para))}</p>")
            para = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Fenced code block
        if stripped.startswith("```"):
            flush_para()
            lang = stripped[3:].strip()
            i += 1
            code: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            cls = f' class="language-{html_mod.escape(lang, quote=True)}"' if lang else ""
            blocks.append(f"<pre><code{cls}>{_escape(chr(10).join(code))}\n</code></pre>")
            continue

        if not stripped:
            flush_para()
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            flush_para()
            level = len(m.group(1))
            inner = _inline(m.group(2))
            if level == 1 and not title:
                title = re.sub(r"<[^>]+>", "", inner)
            sid = unique_slug(inner)
            toc[sid] = re.sub(r"<[^>]+>", "", inner)
            blocks.append(f"<h{level} id=\"{sid}\">{inner}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            flush_para()
            blocks.append("<hr>")
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            flush_para()
            quote: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q = lines[i].strip()
                content = q[1:].strip()
                quote.append(content)
                i += 1
            paras: list[str] = []
            buf: list[str] = []
            for q in quote:
                if q == "":
                    if buf:
                        paras.append(f"<p>{_inline(' '.join(buf))}</p>")
                        buf = []
                else:
                    buf.append(q)
            if buf:
                paras.append(f"<p>{_inline(' '.join(buf))}</p>")
            blocks.append("<blockquote>" + "".join(paras) + "</blockquote>")
            continue

        # Table
        if _is_table_row(line) and i + 1 < len(lines) and _is_table_row(lines[i + 1]):
            flush_para()
            tbl: list[list[str]] = []
            while i < len(lines) and _is_table_row(lines[i]):
                tbl.append(_split_row(lines[i]))
                i += 1
            blocks.append(_table_html(tbl))
            continue

        # Lists (bulleted or numbered)
        m = re.match(r"^([-*])\s+(.*)$", stripped)
        if m:
            flush_para()
            items: list[str] = []
            while i < len(lines):
                lm = re.match(r"^([-*])\s+(.*)$", lines[i].strip())
                if not lm:
                    break
                items.append(f"<li>{_inline(lm.group(2))}</li>")
                i += 1
            blocks.append("<ul>" + "".join(items) + "</ul>")
            continue
        m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m:
            flush_para()
            numbered: list[str] = []
            while i < len(lines):
                lm = re.match(r"^(\d+)\.\s+(.*)$", lines[i].strip())
                if not lm:
                    break
                numbered.append(f"<li>{_inline(lm.group(2))}</li>")
                i += 1
            blocks.append("<ol>" + "".join(numbered) + "</ol>")
            continue

        para.append(stripped)
        i += 1

    flush_para()
    return "\n".join(blocks), title, toc


# --------------------------------------------------------------------------
# Site assembly
# --------------------------------------------------------------------------

def page_label(md_name: str, title: str) -> str:
    if md_name == "index.md":
        return "Home"
    short = {
        "01-questions-are-the-skill.md": "The skill",
        "02-give-the-model-context.md": "Context",
        "03-layered-follow-ups.md": "Follow-ups",
        "04-ask-for-critique-not-answers.md": "Critique",
        "05-what-am-i-missing.md": "What am I missing?",
        "06-steering-long-tasks.md": "Long tasks",
        "07-when-to-be-skeptical.md": "Skepticism",
        "rewrites.md": "Before & after",
        "drills.md": "Drills",
        "answer-key.md": "Answer key",
        "glossary.md": "Glossary",
    }
    return short.get(md_name, title or md_name)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E&#10067;%3C/text%3E%3C/svg%3E">
</head>
<body>
<header class="site-header">
  <div class="masthead">
    <a class="site-title" href="index.html">{title}</a>
    <p class="site-subtitle">{subtitle}</p>
  </div>
  <div class="searchbox">
    <input id="search" type="search" placeholder="Search the guide&#8230;" aria-label="Search the guide" autocomplete="off">
    <div id="search-results" class="search-results" hidden></div>
  </div>
</header>
<nav class="pagenav" aria-label="Guide contents">
  <span class="nav-label">Contents</span>
  {navlinks}
</nav>
<main>
<article>
{body}
</article>
<nav class="readon" aria-label="Page navigation">
  {readon}
</nav>
</main>
<footer class="site-footer">
  <p><strong>Ask AI Better Questions</strong> &#183; {subtitle}</p>
  <p>A free beginner guide by <a href="https://dylanasdale.github.io">Dylan Asdale &amp; Asdale Dynamics, LLC</a> &#183; pairs with <em>The Prompt-Writing Handbook</em> &#183; built locally, no data leaves your device.</p>
  <p>&copy; 2026 Asdale Dynamics, LLC &#183; MIT License</p>
</footer>
<script src="search-index.js"></script>
<script src="search.js"></script>
</body>
</html>
"""


def build() -> None:
    if not DOCS_DIR.is_dir():
        raise SystemExit(f"docs/ directory not found at {DOCS_DIR}")

    missing = [n for n in READING_ORDER if not (DOCS_DIR / n).exists()]
    if missing:
        raise SystemExit(f"docs/ is missing listed pages: {', '.join(missing)}")

    extras = sorted(p.name for p in DOCS_DIR.glob("*.md") if p.name not in READING_ORDER)
    if extras:
        raise SystemExit(f"docs/ has pages not listed in READING_ORDER: {', '.join(extras)}")

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    pages = []
    bodies: dict[str, str] = {}
    for md_name in READING_ORDER:
        raw = (DOCS_DIR / md_name).read_text(encoding="utf-8")
        body, title, _toc = md_to_html(raw)
        out_name = "index.html" if md_name == "index.md" else MD_EXT.sub(".html", md_name)
        bodies[out_name] = body
        pages.append((md_name, out_name, title or out_name))

    # Search index (plain text per page)
    index_entries = []
    for md_name, out_name, title in pages:
        plain = re.sub(r"<[^>]+>", " ", bodies[out_name])
        plain = html_mod.unescape(plain)
        plain = re.sub(r"\s+", " ", plain).strip()
        index_entries.append({"u": out_name, "t": title, "b": plain[:6000]})
    (SITE_DIR / "search-index.js").write_text(
        "window.SEARCH_INDEX = " + json.dumps(index_entries, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )

    (SITE_DIR / "style.css").write_text(CSS, encoding="utf-8")
    (SITE_DIR / "search.js").write_text(SEARCH_JS, encoding="utf-8")

    for idx, (md_name, out_name, title) in enumerate(pages):
        navlinks = ""
        for j, (nm, on, tt) in enumerate(pages):
            label = page_label(nm, tt)
            cls = ' class="current"' if nm == md_name else ""
            navlinks += f'<a href="{on}"{cls}>{html_mod.escape(label)}</a>'
        readon = ""
        prev_pair = pages[idx - 1] if idx > 0 else None
        next_pair = pages[idx + 1] if idx + 1 < len(pages) else None
        if prev_pair:
            readon += (
                f'<a class="prev" href="{prev_pair[1]}">&#8592; '
                f'{html_mod.escape(page_label(prev_pair[0], prev_pair[2]))}</a>'
            )
        else:
            readon += '<span class="prev ghost"></span>'
        if next_pair:
            readon += (
                f'<a class="next" href="{next_pair[1]}">'
                f'{html_mod.escape(page_label(next_pair[0], next_pair[2]))} &#8594;</a>'
            )
        else:
            readon += '<span class="next ghost"></span>'

        label = page_label(md_name, title)
        desc = (
            "A free, plain-English beginner guide to asking AI better questions: "
            "layered follow-ups, context, critique, and healthy skepticism."
            if md_name == "index.md"
            else f"{label} - part of the beginner guide 'Ask AI Better Questions' by Asdale Dynamics, LLC."
        )
        html_out = HTML_TEMPLATE.format(
            title=f"{TITLE} - {label}" if md_name != "index.md" else TITLE,
            desc=html_mod.escape(desc),
            subtitle=SUBTITLE,
            navlinks=navlinks,
            body=bodies[out_name],
            readon=readon,
        )
        (SITE_DIR / out_name).write_text(html_out, encoding="utf-8")

    print(f"Built {len(pages)} pages into {SITE_DIR}")


def clean() -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
        print("Removed site/")
    else:
        print("Nothing to remove")


CSS = """:root {
  --bg: #faf7f2;
  --panel: #ffffff;
  --ink: #2b2622;
  --muted: #6f655c;
  --accent: #b4552d;
  --accent-soft: #f3e2d7;
  --border: #e4dacd;
  --code-bg: #f1ece4;
  --link: #9a4522;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #201b17;
    --panel: #292320;
    --ink: #ede6dd;
    --muted: #b3a79b;
    --accent: #e08a5c;
    --accent-soft: #3a2b21;
    --border: #3f362d;
    --code-bg: #332c26;
    --link: #e79a70;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: ui-serif, Georgia, Cambria, "Times New Roman", serif;
  font-size: 17px;
  line-height: 1.65;
}
.site-header, .pagenav, main, .site-footer { max-width: 46rem; margin: 0 auto; padding: 0 1.25rem; }
.masthead { padding: 1.6rem 0 0.4rem; }
.site-title {
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: 1.45rem; font-weight: 700; text-decoration: none; color: var(--ink);
  letter-spacing: -0.01em;
}
.site-title:hover { color: var(--accent); }
.site-subtitle { margin: 0.15rem 0 0; color: var(--muted); font-size: 0.95rem; font-style: italic; }
.searchbox { position: relative; margin: 0.6rem 0 0.4rem; max-width: 24rem; }
#search {
  width: 100%; padding: 0.45rem 0.7rem; font: inherit; font-size: 0.9rem;
  border: 1px solid var(--border); border-radius: 999px; background: var(--panel); color: var(--ink);
}
#search:focus { outline: 2px solid var(--accent-soft); border-color: var(--accent); }
.search-results {
  position: absolute; z-index: 10; top: calc(100% + 0.35rem); left: 0; right: 0;
  background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12); overflow: hidden;
}
.search-results a { display: block; padding: 0.5rem 0.8rem; color: var(--ink); text-decoration: none; border-bottom: 1px solid var(--border); }
.search-results a:last-child { border-bottom: none; }
.search-results a:hover { background: var(--accent-soft); }
.search-results .rt { font-weight: 600; font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.88rem; }
.search-results .rs { display: block; color: var(--muted); font-size: 0.8rem; }
.search-results .none { padding: 0.6rem 0.8rem; color: var(--muted); font-size: 0.85rem; }
.pagenav {
  display: flex; flex-wrap: wrap; gap: 0.3rem 0.15rem; align-items: center;
  padding-top: 0.6rem; padding-bottom: 0.8rem; border-bottom: 1px solid var(--border);
  font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.82rem;
}
.nav-label { color: var(--muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; margin-right: 0.4rem; }
.pagenav a { color: var(--muted); text-decoration: none; padding: 0.2rem 0.55rem; border-radius: 999px; }
.pagenav a:hover { color: var(--accent); background: var(--accent-soft); }
.pagenav a.current { background: var(--accent); color: #fff; }
main { padding-bottom: 2rem; }
article { background: var(--panel); border: 1px solid var(--border); border-radius: 16px; padding: 1.6rem 1.7rem 1.2rem; margin-top: 1.4rem; }
h1, h2, h3 { font-family: ui-sans-serif, system-ui, sans-serif; line-height: 1.25; letter-spacing: -0.01em; }
h1 { font-size: 1.7rem; margin: 0.2rem 0 1rem; }
h2 { font-size: 1.22rem; margin: 1.9rem 0 0.55rem; color: var(--accent); }
h3 { font-size: 1.02rem; margin: 1.4rem 0 0.4rem; }
p { margin: 0.65rem 0; }
a { color: var(--link); }
a:hover { text-decoration-thickness: 2px; }
blockquote {
  margin: 1.1rem 0; padding: 0.75rem 1.1rem; background: var(--accent-soft);
  border-left: 4px solid var(--accent); border-radius: 0 10px 10px 0;
}
blockquote p { margin: 0.35rem 0; }
ul, ol { padding-left: 1.4rem; }
li { margin: 0.3rem 0; }
table { border-collapse: collapse; margin: 1.1rem 0; width: 100%; font-size: 0.94rem; }
th, td { text-align: left; padding: 0.45rem 0.6rem; border-bottom: 1px solid var(--border); vertical-align: top; }
thead th { font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); border-bottom: 2px solid var(--accent-soft); }
tbody tr:hover { background: var(--accent-soft); }
code {
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.86em; background: var(--code-bg); border: 1px solid var(--border);
  border-radius: 5px; padding: 0.08em 0.35em;
}
pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: 10px; padding: 0.8rem 1rem; overflow-x: auto; }
pre code { background: none; border: none; padding: 0; font-size: 0.85rem; line-height: 1.55; }
hr { border: none; border-top: 1px solid var(--border); margin: 1.8rem 0; }
.readon { display: flex; justify-content: space-between; gap: 1rem; margin: 1.2rem 0 0; font-family: ui-sans-serif, system-ui, sans-serif; font-size: 0.9rem; }
.readon a { text-decoration: none; color: var(--accent); padding: 0.55rem 0.9rem; border: 1px solid var(--border); border-radius: 999px; background: var(--panel); }
.readon a:hover { background: var(--accent-soft); }
.readon .ghost { flex: 1; }
.site-footer { border-top: 1px solid var(--border); padding: 1.2rem 1.25rem 2rem; color: var(--muted); font-size: 0.85rem; }
.site-footer p { margin: 0.25rem 0; }
@media print {
  .site-header, .pagenav, .readon, .site-footer { display: none; }
  article { border: none; margin: 0; padding: 0; }
  body { font-size: 12pt; }
}
"""

SEARCH_JS = """(function () {
  "use strict";
  var input = document.getElementById("search");
  var box = document.getElementById("search-results");
  if (!input || !box) return;

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function snippet(text, q) {
    var idx = text.toLowerCase().indexOf(q);
    if (idx === -1) return esc(text.slice(0, 90)) + "\\u2026";
    var start = Math.max(0, idx - 45);
    var end = Math.min(text.length, idx + q.length + 45);
    var head = (start > 0 ? "\\u2026" : "") + esc(text.slice(start, idx));
    var mid = esc(text.slice(idx, idx + q.length));
    var tail = esc(text.slice(idx + q.length, end)) + (end < text.length ? "\\u2026" : "");
    return head + "<strong>" + mid + "</strong>" + tail;
  }

  function close() {
    box.hidden = true;
    box.innerHTML = "";
  }

  input.addEventListener("input", function () {
    var q = input.value.trim().toLowerCase();
    if (q.length < 2) { close(); return; }
    var raw = (window.SEARCH_INDEX || []);
    var scored = [];
    for (var i = 0; i < raw.length; i++) {
      var p = raw[i];
      var t = p.t.toLowerCase(), b = p.b.toLowerCase();
      var score = -1;
      if (t.indexOf(q) === 0) score = 100;
      else if (t.indexOf(q) !== -1) score = 60;
      else if (b.indexOf(q) !== -1) score = 10;
      if (score !== -1) scored.push({ s: score, p: p, i: b.indexOf(q) });
    }
    scored.sort(function (a, c) { return c.s - a.s || a.i - c.i; });
    if (!scored.length) {
      box.innerHTML = '<span class="none">No matches in the guide.</span>';
      box.hidden = false;
      return;
    }
    var out = "";
    for (var j = 0; j < scored.length && j < 6; j++) {
      out += '<a href="' + esc(scored[j].p.u) + '"><span class="rt">' +
        esc(scored[j].p.t) + '</span><span class="rs">' + snippet(scored[j].p.b, q) + "</span></a>";
    }
    box.innerHTML = out;
    box.hidden = false;
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") close();
  });
  document.addEventListener("click", function (e) {
    if (!box.contains(e.target) && e.target !== input) close();
  });
  window.addEventListener("hashchange", close);
})();
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--clean", action="store_true", help="remove the site/ directory")
    args = ap.parse_args()
    if args.clean:
        clean()
    else:
        build()


if __name__ == "__main__":
    main()
