# Week 5 — Friday defence

Three phases. The debug phase is different this week: the bug is in code that talks to
a network, so "it works on my machine" and "it works" have come apart.

---

## Phase 1 — Explain (6 min)

1. *"Walk me through what happens between `client.users()` and a list of `User`
   objects. Every step."* — request, status check, retry decision, JSON parse,
   validation, skip-or-keep. Five stages; a strong answer names four.
2. *"Why does `ApiError` exist? What would break if you raised `ValueError` instead?"*
3. *"You skip records that fail validation. When would that be the wrong call?"* —
   looking for: anything where a missing record is worse than no answer. Payments,
   medical, compliance. If they say "it is always right" they have not thought about it.
4. *"Your client retries 5xx but not 4xx. Convince me."*
5. *"Where exactly does `report.py` know that the data came from a web API?"* — the
   answer should be *nowhere*, and they should be able to say why that matters.

## Phase 2 — Mutate (7 min)

### Mutation A — *"There's a new endpoint, `/reviews?product_id=10`. Add an average rating per product to the report."*

Name the layers before typing: a `Review` model, a `reviews()` method on the client, a
lookup built once in `summarise`, a column in `render`. Four files, four changes, in
that order.

The thing to watch for: do they fetch reviews **once**, or once per product? A student
who writes the N+1 version after Thursday has not internalised it, and this is a
question they will be asked in a real interview.

### Mutation B — *"The API now rate-limits you: 429 after ten requests a minute."*

Discussion only, no code. Looking for: 429 is not a 5xx but *should* be retried, unlike
other 4xx — and it usually comes with a `Retry-After` header saying how long to wait.
The deeper answer is that the real fix is making fewer requests, not retrying harder.

## Phase 3 — Debug (7 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | `render` uses `:>8.2f` instead of `:>9.2f` on the line total | Reading a column diff |
| Medium | `ApiClient.get` retries 4xx as well as 5xx | Only shows as slowness and one failing test |
| Medium | drop `timeout=` from the session call | Everything passes until you point it at `/slow` |
| Hard | `_validate_all` re-raises instead of skipping | One malformed record loses the whole report |
| Nasty | `summarise` fetches products **inside** the user loop | Every test still passes. Only the N+1 test fails, and its name is the only clue. |

The **Nasty** seed is the one to prefer: the report is still completely correct, which
is exactly what makes performance bugs hard. Ask them how they would have caught it
without the test.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Names the layers and defends the boundaries | Describes the flow accurately | Cannot say where validation happens |
| **Mutate** | Names four files before typing, fetches once | Gets there, writes the N+1 version first | Puts the HTTP call in `report.py` |
| **Debug** | Reproduces first, isolates the layer, one change | Finds it, scrappy | Guesses; blames the network |

Pass is 3 in every phase.

---

## Retro (15 min)

1. *"Four things can happen to a network call. Name them and what your code does about
   each."*
2. *"Which was harder: the HTTP, or deciding what to do when it failed?"* — it is
   always the second, and naming that is useful before week 7, where an agent's tools
   fail constantly.
3. *"What did I explain badly?"*

---

## Instructor: what next week rests on

Week 6 is one API call in a loop. That is genuinely all it is — the Anthropic client is
`ApiClient` with a nicer name, and a model response is a JSON body you validate before
trusting.

A student who is fluent here finds week 6 easy and week 7 possible. A student who is
still copying `requests` calls without understanding the status-code branch will hit
week 7 — where the agent loop *is* a retry loop with a decision in it — and be lost for
reasons that look like "AI is hard" and are actually "HTTP is unfinished".
