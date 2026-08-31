# Week 6 Milestone — The Assistant

> A streaming command-line assistant with memory, a cost counter, and one command that
> returns structured data.

Everything from this week in one program. It is also the last thing you build before
the agent, and the pieces map across almost one to one: a conversation loop becomes an
agent loop, structured output becomes a tool call, and the cost counter becomes the
thing that stops a runaway agent.

---

## The files

| File | Holds |
|---|---|
| `chat.py` | `Conversation` — history, trimming, cost. No printing. |
| `extract.py` | `Note` model and structured extraction. No printing. |
| `assistant.py` | The program. All the printing and asking. |

`chat.py` and `extract.py` take a `client`. `assistant.py` decides which client that
is — the fake one by default, the real one if a key is present.

---

## `chat.py`

**`Conversation(system=None, max_turns=10)`**

| Member | Does |
|---|---|
| `messages` | the history, trimmed, always starting with `user` |
| `add_user(text)` / `add_assistant(text)` | record a turn |
| `send(client, text)` | ask, record both sides, return the reply |
| `stream(client, text, write)` | the same, calling `write(chunk)` as text arrives |
| `total_cost(input_rate, output_rate)` | everything spent, to 6dp |
| `turn_count` | how many turns are held |
| `reset()` | forget everything, including the cost |

`stream` must record the reply in the history too — a streamed turn is still a turn.

## `extract.py`

**`Note`** — `title: str` (≥1 char), `body: str` (≥1 char),
`tags: list[str]` (default `[]`), `priority: int` (1–3, default 2).

| Function | Returns |
|---|---|
| `build_note_system()` | a system prompt naming every field |
| `extract_note(client, text, attempts=2)` | a validated `Note`, or `None` |

Retry once, telling the model what was wrong. `temperature=0`.

## `assistant.py`

Prompts with `> `. Streams every normal reply as it arrives.

| Command | Does |
|---|---|
| anything else | streams the model's reply |
| `/note <text>` | extracts a `Note` and prints it, or `Could not extract a note.` |
| `/cost` | `Spent so far: $0.001035` |
| `/turns` | `Turns: 4` |
| `/reset` | clears the history, prints `Forgotten.` |
| `/quit` | prints `Total: $0.001035` and stops |

Unknown slash commands print `Unknown command: /banana`. A plain message is never
treated as a command.

A printed `Note`:

```
Note: Buy milk
  Tags: shopping, urgent
  Priority: 1
  Buy milk on the way home
```

With no tags, the `Tags:` line is omitted entirely.

### When the model fails

Never a traceback. A failed reply prints:

```
The model is unavailable right now. Try again.
```

and the loop carries on.

---

## Check it

```bash
pytest week-06/milestone -v
```

Twenty-nine tests, all against `FakeClient`. No key, no cost, no network.

Then, if you have a key, talk to it for real:

```bash
export ANTHROPIC_API_KEY=your-key-here
python3 week-06/milestone/assistant.py --real
```

Watch the `/cost` number climb. That number is the most educational part of the whole
week — advice about token cost changes nobody's behaviour, and a counter changes it
immediately.

---

## Then make it good

- [ ] `chat.py` and `extract.py` contain no `print()` and no `input()`
- [ ] `assistant.py` contains no `anthropic` import except where it builds the client
- [ ] Every model call has a `max_tokens`
- [ ] Anything parsed uses `temperature=0`
- [ ] No key anywhere in the source
- [ ] `/quit` on a fresh session prints `$0.000000`, not a crash

---

## Ship it

```bash
git add -A && git commit -m "week 6 milestone: streaming assistant" && git push
```

---

## Friday

Usual three phases. Then read `week-07/README.md` over the weekend — Monday you throw
away the frameworks nobody has offered you yet and build an agent out of the loop you
already know how to write.
