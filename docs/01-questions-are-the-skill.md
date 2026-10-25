# 1. Questions are the skill

## Two people, same tool, different worlds

Picture two nurses at the end of a change-of-report conversation with the same AI assistant.

**Nurse A types:**

> Give me advice for night shifts.

She gets a paragraph so generic it could be printed on a mousepad. "Prioritize sleep. Stay hydrated. Nap before your shift." She shrugs. The answer *was* technically advice.

**Nurse B types:**

> I'm an RN switching from day shift to my first stretch of nights (three 12s in a row). I have a long commute, a toddler in day care, and I already drink coffee only in the mornings. What's the smartest sleep schedule for this exact week, and where do most people like me mess it up?

She gets a plan: a specific sleep-shift schedule, a nudge about caffeine *timing*, a warning about day-care pickup after a full night shift, and the two common failure modes for her situation. Same tool. Night and day.

There is no mysterious "prompt gene." Nurse B just did four tiny things:

1. Said who she is (**context** — chapter 2)
2. Named her real constraint instead of hoping the model would guess
3. Asked for something specific ("this exact week") instead of the whole topic
4. Asked where people mess up, which invites honesty instead of cheerleading (chapters 4 and 5)

## Betting on the right horse

It's tempting to think the answer quality is a property of the model — so the fix is to wait for a better model, or switch tools, or buy the premium tier. Sometimes those help. But you generally *can't* control the model. You fully control the question.

Think of the model as a hired expert who just walked into the room, knows a huge amount about everything but nothing about **you**, and doesn't hang around after the meeting. The question is your only chance to brief them. A great expert given a one-word brief will still produce something bland, because they're going for the safest, most common denominator. A modest expert given a sharp, rich brief can run laps around them.

**The rule of the thumb: the answer can only be as specific as the question.** A vague question forces the model to guess what you want, and its guess is going to be the average of everyone who ever asked — which is exactly the average, unremarkable answer you're hoping to avoid.

## What "better" looks like

| Weak | Why it's weak | The underlying cause |
|---|---|---|
| "Tell me about eBay" | No goal, no audience, no constraint | Missing context |
| "Improve my resume" | Which job? What target? What's wrong? | No goal |
| "Is this good?" | "Good" against what standard? | No success test |
| "Explain AI" | Scope the size of a library | Too broad |

Each of these has a fix, and the fixes repeat. That's the encouraging finding: there are only about six recurring problems with questions, and this guide has one short chapter for each.

## The six habits, in one breath

1. **Give context.** Tell the model who you are, what you're doing, and what you already know. (Chapter 2)
2. **Follow up in layers.** Don't demand the final answer in round one. Interview it. (Chapter 3)
3. **Ask for critique.** "Find the problems in this" is a stronger request than "make this better." (Chapter 4)
4. **Ask what you're missing.** Invite the model to challenge you, not just please you. (Chapter 5)
5. **Steer in plain words.** Long tasks are supervised and corrected like a new hire's first week of work, not handed off and forgotten. (Chapter 6)
6. **Stay skeptically awake.** Confident, fluent writing is not the same as a correct, *verified* statement. (Chapter 7)

That's the guide, already. The rest is detail, drills, and rewrites. Next: the habit with the best payoff per keystroke — [giving the model the context it lacks](02-give-the-model-context.md).
