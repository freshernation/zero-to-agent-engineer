# Week 6 — Friday defence

Three phases. This is the last defence before the agent, and phase 2 is deliberately a
preview of it.

---

## Phase 1 — Explain (6 min)

1. *"Every function you wrote takes a `client`. Why? What would break if `chat.py`
   built its own?"* — the answer is that the tests could not run, and more deeply that
   the module would be welded to one provider. Dependency injection is a genuine
   interview topic; make them say the phrase.
2. *"Walk me from `/note buy milk` to a `Note` object. Every step."* — prompt, call,
   extract the JSON substring, `json.loads`, `model_validate`, retry-or-return. Six
   stages; a strong answer names five.
3. *"Why `temperature=0` for the note and not for the chat?"*
4. *"Your `trim` drops turns in pairs. What goes wrong if it drops one at a time?"*
5. *"A 20-turn conversation — how many times has the first message been sent?"* Twenty.
   If they say once, memory has not landed and week 7 will hurt.

## Phase 2 — Mutate (7 min)

### Mutation A — *"Add `/summarise`: replace the whole history with a one-paragraph summary, and keep talking."*

This is the agent loop in miniature and it is why it is here. Named before typing:

1. A model call whose *input is the conversation itself* — the program feeding its own
   state back in
2. Replacing `_messages` with a synthesised user/assistant pair
3. The cost counter must keep counting, because the summary call costs money too
4. What happens if the summary call fails — you must not lose the history you were
   about to replace

Point 4 is the one that separates a 3 from a 5. Ask it explicitly if they do not raise
it: *"you called the model to summarise, and it failed. What state is your conversation
in now?"*

### Mutation B — *"The model starts returning notes with a `priority` of 7."*

Discussion only. Looking for: validation already rejects it, so the retry fires and
tells the model what was wrong — the system is *already* correct, and they should be
able to say why without changing anything. Then the follow-up: *"and if it does it three
times running?"* (You return `None`, and the CLI says so. Degrading is a feature.)

## Phase 3 — Debug (7 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | `total_cost` rounds to 4dp instead of 6 | Reading a numeric diff |
| Medium | `stream` forgets to `add_assistant` the reply | Conversation silently loses every model turn |
| Medium | `trim` slices but drops the `while` that fixes the first role | Only fails at certain history lengths |
| Hard | `extract_note` sends the *same* prompt on retry | Everything works except one test, and its name is the whole clue |
| Nasty | `_record_usage` is called before the reply is parsed, so a failed parse still bills | No test fails. Only the numbers are wrong. |

The **Nasty** one is worth using on a strong student: nothing goes red, and finding it
requires asking "is this number right?" rather than "does this pass?".

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Names dependency injection and defends the boundary | Describes the flow correctly | Cannot say why the client is a parameter |
| **Mutate** | Raises the failed-summary case unprompted | Builds it, misses the failure state | Cannot see where the call goes |
| **Debug** | Reproduces, isolates, one change | Finds it, scrappy | Guesses; blames the model |

Pass is 3 in every phase.

---

## Retro (15 min)

1. *"What did the `/cost` number change about how you used it?"* — everyone says
   something here, and it is the most durable lesson of the week.
2. *"Name three ways a model call can go wrong that a normal HTTP call cannot."*
   (Wrong format, plausible nonsense, truncation.)
3. *"What did I explain badly?"*

---

## Instructor: the handover to week 7

Say this out loud on Friday, because it reframes the whole of next week:

> **You have already written the agent loop. It is your chat loop.**
>
> Read a message, call the model, do something with the reply, go round again. Next
> week the "do something" becomes *run a tool and feed the result back*, and the
> "go round again" gets a stopping condition. That is the entire difference.

A student who believes agents are a new kind of thing will spend week 7 waiting for
magic. A student who sees it as this week's loop with two changes will build one in
three days.

Week 7 is the keystone of the course. Do not let it start with anyone still shaky on
the conversation loop — if either student cannot explain how a 20-turn chat resends its
history, spend Monday on that instead.
