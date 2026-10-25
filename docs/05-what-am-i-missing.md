# 5. "What am I missing?"

## The four words, and why they work

You can close most of this guide and just remember one sentence:

> **"What am I missing?"**

It's the Swiss Army knife of AI questions, for one deep reason: nearly every other question you ask invites the model to *agree with you* — to fill in *around* your frame. "Which of these two laptops should I buy?" invites a choice between the two laptops. "How do I word this email?" assumes an email is the right move. The question smuggles in assumptions, and the model — bless it — answers *inside* the frame you drew.

"What am I missing?" temporarily tears down the frame. It's a standing invitation for the model to inspect your blind spots instead of decorating inside them.

## Where blind spots actually live

Here's the thing that makes this question so valuable: **you cannot ask about your own blind spot directly, because you don't know it's there.** You *can* ask a broad question that covers whatever it is. The model's job is to notice the gap in your plan the way a chess coach glances at a position and immediately sees the unprotected file.

Blind-spot questions that earn their keep:

- "I'm planning to [situation]. What am I missing?"
- "I've decided to [choice]. What am I missing?"
- "Here's my to-do list for [project]. What am I missing or getting out of order?"
- "I'm about to sign this lease / listing agreement / form summary. What am I missing?"
- "I understand [thing] as follows: [your explanation]. What am I missing?"

That last one is a star. **Explain your understanding, then ask what's missing.** Because now the model isn't checking an abstract topic — it's checking *your version* of it, and comparing your version against what it knows. Misconceptions surface immediately: "That's mostly right, except overtime rules for your state's hospital setting work differently..."

## The "missing" family of prompts

"What am I missing?" has well-dressed siblings. All of them invite the model to challenge you, and every one is a complete sentence you can send with no edits:

- **"What do you think I'm getting wrong?"**
- **"Ask me three questions that would change your answer."** — devious and excellent. The model's questions to you reveal what it's missing about your situation; you then answer them, and the advice gets personal.
- **"What would a skeptical person say is the weakest point of this plan?"** — critique chapter, new clothes.
- **"What haven't I asked you that I should have?"** — lets the model inventory your conversation and its own topic knowledge.
- **"Give me the counterarguments to what you just told me."** — keeps *the model* honest, too (more in chapter 7).
- **"What does the person on the other side of this know that I probably don't?"**

## Why the model is *good* at this job

You might reasonably wonder: can I trust a machine to know what I don't know? Fair suspicion. The honest answer: the model isn't psychic — it's *well-read on typical situations*, and your plan, especially if it's concrete, will very often be a slightly scrambled version of a very common one. Selling a used car online, asking for a raise, sorting out paperwork after a family member's hospital stay — these are extremely common situations, and their failure modes are famous and *documented*. "What am I missing?" doesn't ask for prophecy. It asks: *"which of the famous failure modes applies to me?"* That, the model does extremely well.

## Two rules to keep it honest

The question is powerful, which is exactly why two guardrails matter.

1. **Don't accept the list passively.** When it names your misses, respond like a colleague, not a student: "Yes on #1, I hadn't thought of that. Not sure about #2 — why would that matter here?" The pushback turns a list into a conversation, and the second round is where you actually learn the topic.
2. **Remember what the model is *not* checking.** It hasn't met your boss, seen your eBay seller account, or read your actual lease. Everything is one degree abstracted: it knows *your neighbor's* version of your situation perfectly and *yours* only through your description. If detail that matters never made it into the chat, no prompt can rescue that. (Chapter 2, again, forever.)

> **The one-line version of this chapter:** *"What am I missing?" is the question you ask before trusting your plan, signing the thing, sending the email, or placing the order. It is the cheapest life insurance in this guide.*

Next: what to do when the task is too big for one message — [steering long tasks in plain words](06-steering-long-tasks.md).
