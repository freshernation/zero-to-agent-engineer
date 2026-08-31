# Week 11 — Put it where people can reach it

> **Destination**
> An agent behind an API on the public internet, that you can see inside when it
> misbehaves, with an evaluation that runs before every deploy.

An agent on your laptop is a hobby. This week it becomes something you can send someone
a link to — which is what makes it a portfolio piece rather than a repository.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Put a service behind HTTP, with validated requests |
| Tue | `day-2/` | Configure it, check its health, and deploy it |
| Wed | `day-3/` | See what happened inside a request, after the fact |
| Thu | `day-4/` | Gate a deploy on an evaluation, and cap what it can spend |
| Fri | `milestone/` | **Project 3** — deployed, traced, evaluated |

---

## What changes

Everything so far ran when you ran it. From today it runs when **somebody else** does,
which brings four problems you have not had:

| Problem | Answer |
|---|---|
| You are not watching | logs and traces |
| The input is not yours | validation at the boundary |
| It costs money per request | caps, and a number you can see |
| A bad deploy affects real people | an evaluation that blocks it |

None of those is difficult. All of them are the difference between a demo and a service,
and all of them come up in interviews as *"how would you know if it broke?"*

---

## Project 3

The interview centrepiece: a deployed agentic app with retrieval, tracing, and an eval
suite that runs before deployment.

Of the three projects this is the one that gets clicked. Make it work on a phone, make
the first screen explain itself, and make sure the link in your README is live on the
day somebody reads it.

---

## The honest note about deploying

Deployment platforms change, their free tiers change, and any specific instructions here
would be wrong within a year. What does not change is what a deployable service needs:
configuration from the environment, a health check, a documented start command, and no
secrets in the repository.

Everything this week builds those. The `Dockerfile` and `render.yaml` you write are a
worked example, and your instructor will pick the platform.
