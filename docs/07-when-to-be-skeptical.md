# 7. When to be skeptical

## The fluent-voice problem, in plain English

Everything in this guide so far has been about getting *better* answers. This chapter is about the quiet cost of getting better at this: better questions produce more confident-sounding answers, and a confident-sounding answer is not the same thing as a **true or verified** one.

AI models sometimes produce errors that look — on the page — exactly like facts. Clean sentences, tidy structure, plausible names and numbers. This failure mode has a name you'll see everywhere: *hallucination*. The word is a little dramatic; a more level description is that a model sometimes **states things it does not actually know, in a voice that doesn't signal not-knowing.** It isn't lying to you. It's autocomplete with a PhD demeanor.

You should not become a skeptic about everything — that would exhaust you and waste the tool. The skill is **triage**: knowing which answers need a raised eyebrow and which can pass on the nod.

## The danger zones (a triage table)

Skim this table and keep the last column in your head. You don't need to memorize anything else in the chapter.

| The answer involves... | Skepticism level | Why |
|---|---|---|
| Facts, names, numbers, dates | **Verify** | Most common hallucination home. Apocryphal quotations, invented statistics, plausible-but-wrong dates. |
| Legal, medical, tax, and money-binding advice | **Verify with a real source** | High stakes + the model doesn't know your jurisdiction, your insurance, your lease, *you*. Educational thinking-partner, not authority. |
| Anything citing a specific book, paper, article, or web page | **Check the source exists** | Invented references have been the #1 AI embarrassment in public life since day one. |
| Current or very recent events, prices, openings, schedules | **Check live sources** | The model may not have today's information at all. |
| Step-by-step instructions for tools, buttons, menus, websites | **Trust but spot-check** | Interfaces change faster than training data; steps are often one version behind. |
| Math with more than a couple of steps | **Re-run or verify** | Models make arithmetic slips in multi-step chains, sometimes confidently. |
| The model's opinion of *your situation* | Mild | It's riffing on a description, not your life. Its critiques are usually directionally useful anyway. |
| Writing help, brainstorming, rephrasing, explaining a concept you'll restate | Low | Near-zero stakes, easy to eyeball yourself. This is where AI is at its safest and best. |

The pattern under the table: **risk lives where facts are specific and stakes are real.** A brainstorm of charity 5K names? Take it as given. A citation, a dosage-adjacent claim, a statute number, a price? Treat it like a rumor from a very well-dressed stranger — interesting, worth checking.

## Signals you can actually watch for

You can't always tell a confident hallucination from an accurate statement — that's the whole problem. But you *can* watch for warning lights:

- **Oddly specific, oddly round, or oddly rare.** A survey from 2019 with a precise percentage but no named source. A "study" with no journal. A quotation attributed to someone famous that you've never once heard anywhere else.
- **Links to nothing.** URL structure that looks real but goes nowhere, or papers with real-sounding titles. One check — paste the title into a search engine — settles it in ten seconds.
- **Details that changed mid-conversation.** The model said rent was due on the 1st, then later, the 15th. Drift like that means the earlier statement was guessed, not known.
- **Too-perfect support for your original question.** If you asked "isn't X a good idea?" and the answer is a confident essay about why X is, in fact, a good idea — that's a pushover echo, not evidence. Ask the counterargument version (chapter 5).
- **The tool hedges correctly and then... un-hedges.** "It varies by state, but in your case, fees are typically 2–3%..." — the second half of that sentence is doing hallucination work dressed up as local knowledge.

## The verification habit, made small

You don't need to fact-check your AI like a tabloid editor. You need a verification habit small enough to actually use. Three questions, fifteen seconds:

1. **"Does this need to be true to act?"** If I'm ordering plates off this menu, no. If I'm quoting the interest rate on this loan, yes. Only "yes" answers earn a check.
2. **"Do I have an independent way to check it?"** A second source, the actual document, the actual website, or — the most underused move — *asking the model itself to argue the other side.* "You said the deadline is April 15 for this form type. What would make that wrong?"
3. **"Can I re-ask it fresh?"** Open a new chat, ask the same factual question cold, with no context that could bias it. Two different framings agreeing is soft corroboration; two *phrasings* disagreeing is a stop sign. (It's soft, not hard: models can repeat an error from their training. For real stakes, the outside source wins.)

## Confidence that deserves skepticism most: your own

One last turn of the lens, because this chapter is really the "you" chapter: the most dangerous confident voice in this loop is the *familiarity effect* — after twenty minutes of a good conversation, the *model's* ease starts to become *your* certainty. That's a human bias, not a machine one. The countermove is so simple it's almost embarrassing: **when you're about to act on AI help, name for yourself where the fact came from.** If you can name an independent source, act. If all you can name is "the chat said so," you've found the missing link, and you know the drill: verify, or ask the question that surfaces what you're missing.

> **The one-line version of the whole guide:** *AI is a brilliantly read, endlessly patient, occasionally wrong intern from the future. Give it context, sharpen it with rounds, make it critique you and itself, steer it in the plainest English you own — and check the load-bearing facts before anything you'd sign, pay for, or put your name on.*

---

## Where to go from here

- Test yourself on all six habits with the [practice drills](drills.md), then check against the [answer key](answer-key.md).
- Watch the same weak questions get fixed line by line in [before & after rewrites](rewrites.md).
- When a term is fuzzy, the [glossary](glossary.md) has you covered.
- And when you're ready to go deeper: pick up its companion, **The Prompt-Writing Handbook**, which covers the craft of the first message in the same plain-English voice.
