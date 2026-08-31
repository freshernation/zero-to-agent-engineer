# Week 10 — Multi-agent, and the cost of abstraction

> **Destination**
> Build the same system twice, in two frameworks, and defend the choice between them —
> including the choice to use neither.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Save a graph's state and pick a run back up later |
| Tue | `day-2/` | Pause for a human, and build a graph out of graphs |
| Wed | `day-3/` | Use CrewAI, and say what its abstraction assumes |
| Thu | `day-4/` | Judge when several agents beat one, and debug a crew |
| Fri | `milestone/` | The same task, both ways, plus a recommendation |

---

## The honest framing

This is the week where the right answer is most often **"you do not need this."**

Multi-agent systems are the most over-recommended idea in the field. Most of the
problems people solve with three agents are solved better by one agent with three tools,
because every extra agent is another model call, another place to lose context, and
another thing that can confidently do the wrong job.

Your task on Friday is a recommendation, and *"we tried it and it was not worth it"* is
a perfectly good one. It is also a more senior thing to say than *"we used CrewAI"* —
being able to reject a tool for a stated reason is the skill; using it is not.

---

## What genuinely earns the extra machinery

| Feature | Earns its place when |
|---|---|
| **Persistence** | a run must survive a restart, or take longer than one request |
| **Interrupts** | a human has to approve something before it happens |
| **Subgraphs** | a piece of the process is reused, or is complex enough to test alone |
| **Multiple agents** | the sub-tasks genuinely need different tools, prompts, or permissions |

Monday and Tuesday are the first three, and they are the strongest argument for
LangGraph you will see — they are hard to build by hand and easy to get for free.

Wednesday and Thursday are the fourth, and the argument is much weaker. Notice that
difference; it is the week's actual lesson.
