# Ask AI Better Questions

*A short guide to question-asking as a skill* — layered follow-ups, giving
the model context it lacks, asking for critique instead of an answer,
"What am I missing?" prompts, steering long tasks in plain words, and
knowing when an answer deserves skepticism.

A free, beginner-friendly guide in the same plain-English, never-condescending
voice as *The Massive AI Manual*. It is designed as the conversation-side
companion to the **Prompt-Writing Handbook**: that handbook covers the first
message; this guide covers everything you do after you press Enter.

Written and published by **Asdale Dynamics, LLC** — LLC of Dylan Asdale,
registered nurse turned AI author. Beginner-friendly AI education, books,
and practical tools.

## What's inside

- **7 short chapters** on the six habits of people who ask well — plus
  skepticism and verification as the tie-breaker for everything else
- **12 before & after question rewrites** — real weak questions, diagnosed
  and rebuilt line by line
- **12 practice drills with a full answer key** — scored by habit, not
  word-matching
- **A glossary** of every term, defined the way a friend would

## How to use it

Nothing to install, no account needed. Read it in order, then do the drills.

### Build the static HTML site (local-first, dependency-free)

Requires only Python 3.8+ (standard library, no packages, no network):

```bash
python3 build.py      # builds the site into site/
python3 build.py --clean   # removes site/
```

Then open `site/index.html` in any browser — it works from your local disk,
offline. The site includes page navigation, before/after search, dark mode,
and a print stylesheet.

### Run the tests

```bash
python3 tests.py
```

The test suite checks the markdown renderer unit-by-unit, runs the build,
validates every internal link and anchor, verifies required content
(rewrites pairs, drills, glossary, answer key), confirms the build is
deterministic, and scans for leaked secrets or stray personal data.

## Project layout

```
docs/       the guide, in Markdown (source of truth)
build.py    dependency-free Markdown -> static HTML site builder
tests.py    test suite for content, build, links, and hygiene
site/       generated output (gitignored; rebuild any time)
```

## Companion guides

- **The Prompt-Writing Handbook** — the craft of the first message
- *The Massive AI Manual* — AI explained like a friend would, start to finish

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
