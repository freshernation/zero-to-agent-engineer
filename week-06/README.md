# Week 6 — Talking to a model

> **Destination**
> Drive a language model from code, with no framework, and explain what every parameter
> in the request does.

Last week you learned that anything outside your program is a liar. A model is the most
interesting liar you will ever call: it is slow, it is expensive, it is different every
time, and it will confidently return something in the wrong format.

Everything you built last week applies. A model call is an HTTP request with a JSON
body. The SDK is `ApiClient` with a nicer name.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Make a call, read the response, count what it cost |
| Tue | `day-2/` | Shape the output with the system prompt and examples |
| Wed | `day-3/` | Get JSON back and refuse to trust it until it validates |
| Thu | `day-4/` | Hold a conversation, stream it, and handle the model failing |
| Fri | `milestone/` | Ship a streaming assistant with memory and a cost counter |

---

## Everything takes a `client`

```python
def summarise(client, text):
    ...
```

The tests hand you a stand-in from `fake_model.py` — scripted, free, instant, and the
same every run. Your code cannot tell the difference, which is the entire point.

Read `FENCE.md` before you start. `week-06/try_it.py` makes one real call if you have a
key; do it once so the fake never feels like the whole story.

---

## The four things that will surprise you

**It is not a function.** The same input gives different output. Anything you build on
top has to survive that, which is why week 3's validation and week 5's retries come
back immediately.

**It will not follow your format.** Ask for JSON and sometimes you get JSON wrapped in
a friendly sentence. Handling that is not a hack — it is the job.

**It has no memory.** Every call is the first one. A conversation is you resending the
whole history, every time, which is also why long chats get expensive.

**It charges by the token, in both directions.** You pay for what you send *and* what
comes back. By Friday you will have a counter showing you exactly that, because a
number changes behaviour in a way that advice does not.
