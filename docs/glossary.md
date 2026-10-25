# Glossary

Every term this guide leans on, defined in plain English the way a friend would. Terms are roughly in the order you meet them in the guide.

## Context

The background the model needs but doesn't have: who you are, what you're trying to do, what you already know, what constraints apply. The single biggest fix for generic answers. The model only knows what's in the chat — anything else, it guesses or goes vague about. (Chapter 2.)

## Model

Shorthand for the AI program answering you (the underlying "brain" behind a chatbot). When this guide says "the model," it means the thing generating the answers in your chat session.

## Chat

The conversation window between you and the model. Most models treat everything in one chat as connected, so corrections stick and context accumulates — which is why a *fresh chat* is sometimes the honest fix for a soured conversation (and why "which chat is this answer from?" matters when verifying facts).

## Session

A fancy name for the same thing — one continuous chat, up until you open a new window. Used interchangeably with "chat" in this guide.

## Prompt

The message you send the model — anything from one word to a page. This guide's sister book, **The Prompt-Writing Handbook**, covers crafting first prompts at length; here "prompt" is basically "your question."

## System prompt

A standing instruction that shapes *all* of a chat's answers. In consumer chatbots you mostly meet these as customization settings ("always answer me casually," "give me step-by-steps"). Worth knowing the term; mostly not worth configuring at this stage.

## Role assignment

Asking the model to take a perspective: "Act as my skeptical roommate," "Answer like an experienced charge nurse." Works by *context, not magic*: the role quietly pulls in the habits and standards of the reader it names. All the power is in **who the role actually is** — "a skeptical landlord-tenant lawyer" steers, "an expert" doesn't.

## Follow-up

Any message you send after the first — a correction, a narrowing, a "go deeper on point 2." Follow-ups are cheap steering wheels; you control where the conversation goes next. (Chapter 3.)

## Layered follow-ups

The habit of interviewing the model in rounds — get the shape, react, sharpen — instead of demanding a final answer in one shot. Three small pushes beat one giant pull. (Chapter 3.)

## Anti-pattern

A common move that *feels* useful and reliably underdelivers — the sigh-and-leave, the mega-prompt, asking "make it better." Named and avoided throughout.

## Mega-prompt

A single giant message with a paragraph of instructions, sent all at once. When the answer disappoints, you've lost *localization* — you can't tell which instruction failed. Prefer layers: one short ask per round. (Chapter 3.)

## Localization

The debugging superpower of asking one thing per round: when each round asks a single question, a bad round is obvious — and cheap to fix. Same idea in regular software; the guide borrows it because it's exactly what layering buys you.

## Critique

A judgment of work against a named standard — what's weak, ranked, and *why*. Asking for critique instead of an answer flips the model from generic producer to sharp editor. (Chapter 4.)

## Named reader

The specific imaginary person a piece of writing is judged against: "a busy teacher on her phone," "a skeptical buyer," "a tired charge nurse at 0300." The most reliable way to get specific critiques instead of vague ones.

## Devil's advocate prompt

Explicitly requesting arguments *against* your plan or belief: "Play devil's advocate against my plan." A critique-flavored version of "what am I missing?" — it counters the model's tendency to be agreeable. (Chapters 4 and 5.)

## Sounding board

Using the model to think *with* rather than to produce *for* — e.g., "ask me three questions that would change your advice." Often the best first message when you don't know what your question is yet. (Chapter 5.)

## Bias

A systematic tilt. The model's: agreeableness, generic filler, confident guessing on facts it lacks. The human's: *familiarity effect* — mistaking a fluent chat partner's ease for certainty about facts you haven't verified. Both matter; only one is yours to fix.

## Hallucination

A confident statement the model produced that isn't backed — invented studies, quotes nobody said, wrong dates, plausible-sounding prices. Not lying: the model generates plausible text, and sometimes plausibility runs ahead of truth. The core defense is **triage**: knowing which answers deserve verification before you act on them. (Chapter 7.)

## Verification

Checking a claim against something outside the chat — a search engine, the real document, a professional who knows your situation. The fifteen-second three-question habit: *Does this need to be true? Do I have a way to check? Can I re-ask it fresh?* (Chapter 7.)

## Triage

Deciding *in advance* which answers to verify and which to accept on the nod. Risk lives where facts are specific and stakes are real — citations, legal-medical-financial, prices — and is lowest where you can eyeball the output yourself: drafts, brainstorms, rephrasing.

## Check-in

The long-task steering move: "Before you produce the whole thing, show me your outline and wait for my OK." Catches drift while it's still a one-sentence fix. (Chapter 6.)

## Intercept

Stopping the model mid-output to correct course: "Stop there. Sections 1–2 are right; fix section 3." Models resume cleanly from surgical corrections — you're allowed to operate like an editor, not an audience. (Chapter 6.)

## Graceful reset

Restarting a tangled long task without losing its value: fresh, improved brief + the worth-keeping excerpts + the original goal. Ends trench warfare in your own chat. (Chapter 6.)

## Block

A grouping of drills in the [practice section](drills.md); twelve drills in six blocks, one per habit, with an [answer key](answer-key.md) that scores by habit, not by word match.

## Plain words

The whole guide's steering philosophy in two words: models follow ordinary language. "Shorter." "Slower there." "Go deeper on point 2." No incantations, no magic vocabulary — the skill is honesty with direction, not vocabulary with italics.
