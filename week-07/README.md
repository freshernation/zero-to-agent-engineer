# Week 7 — Build the agent

> **Destination**
> Hand-write the loop that every agent framework is hiding, and know exactly why it
> stops.

This is the keystone week. Everything before it was preparation and everything after it
is elaboration.

---

## The whole idea, up front

You already wrote the agent loop. It is week 6's chat loop:

```
read a message  ->  call the model  ->  do something with the reply  ->  go round again
```

An agent changes two things:

1. **"do something with the reply"** becomes *if the model asked for a tool, run it and
   tell it what happened*
2. **"go round again"** gets a **stopping condition**, because now the loop can run
   without a human in it

That is the entire difference. There is no third thing.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Describe a tool to a model and dispatch the call it asks for |
| Tue | `day-2/` | Write the loop, end to end, and watch it think |
| Wed | `day-3/` | Survive tools that fail, arguments that are wrong, and loops that will not stop |
| Thu | `day-4/` | Handle several tool calls at once, and debug an agent |
| Fri | `milestone/` | Ship **Project 2** — a working agent, no framework, and a write-up |

---

## What a "tool" actually is

Three ordinary things, and no magic anywhere:

1. **A JSON schema** — a dict describing a function's name, purpose, and arguments.
   You send it with the request.
2. **A choice** — the model replies with `stop_reason="tool_use"` and a block saying
   *"call `calculate` with `{"expression": "2+2"}`"*. It has not run anything. It
   cannot. It emitted some JSON.
3. **A dispatch table** — your dict of `{"calculate": calculate_function}`. **You** look
   up the name, **you** call the function, **you** send the result back as an ordinary
   user message.

The model never executes anything. It asks. Every agent framework in existence is
wrapping those three things, and by Wednesday you will have written all of them.

---

## Project 2

A ReAct-style agent with at least three real tools, an iteration cap, and a write-up
explaining the loop **in your own words**.

That write-up is not a formality. It is the artifact that makes an interviewer sit up,
because it demonstrates the thing almost no junior candidate can demonstrate: that you
know what is underneath.

---

## The fence is absolute this week

No frameworks. Not one. Read `FENCE.md` for why — it is the most important paragraph in
the course.
