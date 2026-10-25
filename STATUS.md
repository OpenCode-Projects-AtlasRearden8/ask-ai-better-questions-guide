# STATUS — Ask AI Better Questions

Last updated: 2026-10-25 · Version: 1.0.0 · Owner: Asdale Dynamics, LLC

## What was built

A complete, beginner-friendly guide to **question-asking as an AI skill**, in
the plain-English style of Asdale Dynamics, LLC (Dylan Asdale's LLC), designed
as the companion to *The Prompt-Writing Handbook*.

**Content (12 Markdown documents in `docs/`):**

- `index.md` — welcome, idea map, how to use the guide
- `01` – `07` — the seven short chapters:
  1. Questions are the skill (why your side of the conversation matters)
  2. Give the model the context it lacks
  3. Layered follow-ups (interview the model in rounds)
  4. Ask for a critique instead of an answer
  5. "What am I missing?" (blind-spot prompts)
  6. Steering long tasks in plain words (supervision, check-ins, intercepts, resets)
  7. When to be skeptical (triage for hallucination risk, verification habit)
- `rewrites.md` — 12 before/after question rewrites, each diagnosed
- `drills.md` — 12 practice drills in six blocks (one per habit)
- `answer-key.md` — full answer key with scoring bands and cross-links back to chapters
- `glossary.md` — 19 plainly-defined terms

**Code:**

- `build.py` — dependency-free (Python 3 stdlib only, offline) Markdown →
  static HTML site builder. Renders headings, paragraphs, lists, pipe tables,
  blockquotes, fenced code, bold/italic/code, and internal links
  (`*.md` → `*.html`, anchors validated). Generates:
  - 12 HTML pages with full navigation, reading-order prev/next, footer credit
  - warm, responsive CSS with automatic dark-mode and a print stylesheet
  - local client-side search (`search.js` + `search-index.js`), zero network calls
- `tests.py` — 84-check test suite (see below)

## How to run it

```bash
python3 build.py        # build the site into site/
python3 build.py --clean   # remove site/
python3 tests.py        # run the full test suite
```

Then open `site/index.html` in any browser — works offline from the local
filesystem, no accounts, no telemetry. Requires only Python 3.8+.

## Verification results

All commands were run in this folder and passed:

- `python3 tests.py` → **All 84 checks passed.** The suite covers:
  - unit tests of the Markdown subset converter (13 checks)
  - build produces all 12 pages + 3 assets; every page has an article body (18)
  - every internal link and every internal anchor resolves; nav lists all
    pages on every page; search index is valid JSON covering all pages (23)
  - required content: 12 docs, 12+ Before/After pairs, drill blocks A–F,
    ≥12 drills, answer key covers blocks A1–F1 and has scoring, ≥15 glossary
    terms, chapters 1–6 each point onward, companion handbook referenced,
    every doc starts with an H1, education-not-medical-advice framing present (26)
  - build is clean and repeatable: `--clean` works, rebuild reports 12 pages,
    two consecutive builds are byte-identical (3)
  - hygiene: exact LICENSE line `Copyright (c) 2026 Asdale Dynamics, LLC`,
    MIT text verified, README credits + build/test docs verified, no API-key/
    token-like secrets, no personal email addresses, no key-like blobs (9)
- `node --check site/search.js` → syntax OK; a Node smoke test over the real
  search index found the expected pages for a sample query
- Spot-checked rendered HTML for the tables, blockquotes, and drill answer
  markup — all render as intended

## Known gaps

- **Local-first only (by design):** no deployment pipeline. `site/` is
  gitignored; publish-ready output requires running `build.py` first (one
  command). A future GitHub Pages hook could commit the built site.
- **Markdown subset, not full CommonMark:** the renderer supports what the
  guide uses (no nested lists, no images, no inline HTML passthrough).
  Nested lists would need a parser upgrade if content grows that way.
- **Search is substring/rank based:** no stemming or fuzzy matching; fine for
  a 12-page guide.
- **No sitemap/meta-OG tags:** acceptable for local use; worth adding if the
  site is ever published publicly.
- **Single-page/print compilation** (one continuous HTML page for PDF export)
  was deliberately deferred; the print stylesheet covers on-page printing.

## Compliance notes

- Initializes git locally with plain commit messages, no Co-authored-by
  trailers, no remote, nothing pushed or published.
- `LICENSE` is MIT with the exact required copyright line; README credits
  Asdale Dynamics, LLC.
- No secrets, API keys, or personal data anywhere in the files (verified by
  the test suite, not just by hand).
- Health-related content is framed as education, never medical advice.
