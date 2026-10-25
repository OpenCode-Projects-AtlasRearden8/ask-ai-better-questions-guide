# 6. Steering long tasks in plain words

## When a chat becomes a work shift

This chapter of the guide is about the moments when AI goes from being a *fountain of text* to being *part of your workday*: drafting a multi-page document, building a budget sheet step by step, writing a whole ebook chapter, planning a garage-sale-and-shipping weekend, restructuring your on-call paperwork.

On short questions, misfires are cheap — you ask again, you move on. On long tasks, a bad steer at minute two ruins hour three. So the asking skill changes shape: it becomes **supervision**. And here is the headline of this chapter, which people find mildly disappointing and then find liberating:

> **You do not need special vocabulary to supervise an AI. You need the plain words you already use on coworkers.**

"Shorter." "Stop and check with me before doing that part." "That's drifting, go back to step 2." "Redo the last section, it lost the thread." That's the entire toolkit. Models are trained to follow guidance in ordinary language — no incantations of the form `"You must obey, O great oracle"` — and the mystical versions of those words actually make it *harder* to see which instruction mattered.

## The start of a long task: one screen of nouns

Long tasks still begin with a request, and the *first* request deserves slightly more ceremony than a one-off question. Not more complexity — more information. Aim to cover five things, in any order, in a few sentences:

1. **The goal** — the finished thing, described like you'd describe it to a temp agency. ("A one-page sheet my brother's college roommate could follow for moving Mom's paperwork after discharge.")
2. **The audience** — who reads it and what they already know.
3. **The constraints** — length, format, tone, tools involved, deadline, "must not exceed 300 words." "One page" is doing more work in that instruction than you'd suspect; it certainly isn't a formality.
4. **The ingredients** — paste in the source material. The draft, the numbers, the resume, the budget figures. Models are dramatically better with *yours* in front of them than with a generic description of yours.
5. **The check-ins** — the move most beginners skip, and the secret weapon of this chapter. More below.

A first request like this is two to four sentences per item. Not one enormous paragraph — an organized note. If writing that feels heavy, remember: you would give a coworker at least this much. (And if you truly can't enumerate any of the five, you're missing context, not prompting skill — see chapter 2.)

## Check-ins: the "stop and wait for me" move

For any task with more than a couple of moving parts, add one instruction to the first message:

> **"Before you produce the whole thing, show me your outline/plan first and wait for my OK."**

Why it earns first place on every list like this:

- **Cheap redirects.** A wrong plan gets fixed in one sentence. A wrong finished document gets fixed with irritation.
- **You steer *early*, which is where steering is cheap.** It costs nothing to say "actually, make section 2 about the estate papers, that's the urgent one" to an outline, and a world of trouble to say it to a formatted 900-word document.
- **It surfaces assumptions you didn't know you'd invited.** You'll read the plan and think, "no — that's not the point at all," and you'll have caught the drift before it happened.

The close relative: **"Walk me through your approach before doing it, then stop."** Same idea when the task isn't a document — a research process, a plan of steps, a budget scheme, what have you.

## The mid-stream dictionary: steering in plain words

Here's the part to focus on, because it's what this chapter is actually for once the task is rolling. What you need mid-stream is a small, steady lexicon of plain-word commands. Steal this table whole:

| What's happening in your head | The plain-words stick |
|---|---|
| Too long / bloated | "Cut this to half the words. Same information." |
| Too shallow | "Go deeper on point 2. Give a real example with numbers." |
| Wrong target | "Rewrite that for a [busy landlord] instead of [general reader]." |
| Losing the thread | "Stop. Re-read my original request. Then continue and close with what I actually asked for." |
| It's too salesy / over-hyped | "Tone it down 50%. No exclamation points, no 'game-changer' words." |
| Uncertain about a part | "Are you confident about step 3? What's it based on?" |
| about to burn a full draft fast | "Before expanding that into 4 pages, list what you'd add — then wait." |
| It said something you doubt | "You said X. I believe Y. Check which of us is right and show your basis." |
| You want options, not a deliverable | "Don't write the final version. Give me three different approaches in one paragraph each." |
| It's going great, you want more | "Continue in the same style/structure as the first two sections." |

Read that middle row twice, because it's the one people never think to do: **you may stop the model mid-sentence.** If a wall of text is coming out half wrong, it is completely acceptable — *good* — to interrupt: "Stop there. Sections 1–2 are right; section 3 wandered. Just fix 3." Models pick up smoothly from surgical corrections; you're allowed to operate like an editor, not an audience.

## The reset move: when direction fails

Sometimes a long task gets 60% right and the conversation is tangled past the point of salvaging — three corrections have collided, everything is half-updated, and each new reply costs more parsing effort than it's worth. In that state you don't keep grinding; you do the **graceful reset**:

> "Let's restart cleanly. Here's the situation: [brief, improved version of your original brief, now rich with everything you've learned]. Here's the good work from this conversation worth keeping: [paste]. Now, produce [the goal] from scratch on that foundation."

Two things happen and both are wins: you get a clean run built on your corrections, and — usually, invisibly — you learn which parts of your original brief were underwater. Long tasks teach *you*; the reset is how you capture the lesson.

The cousin of the reset, for when it's semi-working but sagging: **"Summarize where we are and what's still open, in five bullets."** That one re-generates shared ground truth and often un-sticks the stick point outright, because the summary itself shows you what the model thinks the task is.

> **The one-line version of this chapter:** *Run long tasks like a shift supervisor, not a wish-granter: a clear head start, a "show me the plan first" clause, plain-word corrections as they arise, and a clean reset when the chat gets too tangled to save.*

Next: the string that ties everything together — [when the answer deserves skepticism](07-when-to-be-skeptical.md).
