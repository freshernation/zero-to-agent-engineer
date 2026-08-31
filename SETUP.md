# Day Zero — Setup

Do this once. Budget two hours and do not feel bad if it takes them; environment
problems are the single most demoralising part of learning to program and they are
also the least important. Get through it, then never think about it again.

**If you are stuck for more than 20 minutes on any step, stop and message your
instructor.** This is the one part of the course where struggling alone teaches you
nothing.

---

## 1. Open a terminal

- **macOS** — press <kbd>Cmd</kbd>+<kbd>Space</kbd>, type `Terminal`, press Enter.
- **Windows** — install [Windows Terminal] from the Microsoft Store, then use it to
  open **PowerShell**. (Everything below works in PowerShell; where a command differs
  it is marked.)
- **Linux** — you already know.

Five commands to learn right now. You will use them every day for the rest of your career.

| Command | What it does |
|---|---|
| `pwd` | Print working directory — *where am I?* |
| `ls` | List the files here (`dir` on PowerShell also works) |
| `cd foldername` | Go into a folder |
| `cd ..` | Go up one folder |
| `mkdir name` | Make a new folder |

Type each one. Watch what happens. Do not move on until `pwd`, `ls`, and `cd` feel boring.

---

## 2. Install Python 3.12 or newer

Check what you have:

```bash
python3 --version
```

If that prints `Python 3.12.x` or higher, skip ahead. Otherwise:

- **macOS** — install [Homebrew], then `brew install python@3.12`
- **Windows** — download from [python.org/downloads]. **Tick "Add python.exe to PATH"**
  on the first screen of the installer. This is the step everyone misses.
- **Linux** — `sudo apt install python3.12 python3.12-venv`

> On Windows the command is `python`, not `python3`. Everywhere else, use `python3`.

---

## 3. Install VS Code

Download from [code.visualstudio.com]. Install it, open it, then install one extension:

- **Python** (by Microsoft) — open the Extensions panel with
  <kbd>Cmd/Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd>, search `Python`, click Install.

Do not install anything else yet. Not a theme, not Copilot, not a formatter. An
autocomplete that finishes your thoughts is actively harmful for the next four weeks.

---

## 4. Get your own copy of the course

You are not cloning the course repo. You are making **your own repo from it**, because
by week thirteen it is your portfolio — thirteen weeks of commits with your name on
them, and the first thing an interviewer will open.

1. Sign in to GitHub (create a free account if you do not have one — use a username you
   would be happy to put on a CV).
2. Go to **https://github.com/freshernation/zero-to-agent-engineer**
3. Click the green **Use this template** button → **Create a new repository**.
4. Name it `zero-to-agent-engineer`, leave it **Public**, click **Create**.

Now clone the copy you just made. Replace `YOUR-USERNAME`:

```bash
cd ~
mkdir -p code
cd code
git clone https://github.com/YOUR-USERNAME/zero-to-agent-engineer.git
cd zero-to-agent-engineer
```

If `git` is not installed, macOS will offer to install it when you first type `git` —
say yes. On Windows, install [Git for Windows].

### Point at the course, so you can get fixes

The course gets patched during the cohort — a test gets clearer, a day gets rewritten.
Run this once, now, so those fixes can reach you:

```bash
git remote add upstream https://github.com/freshernation/zero-to-agent-engineer.git
```

When your instructor says a patch has shipped, pull it:

```bash
git pull upstream main
```

The **first** time only, that command will refuse and complain about unrelated
histories. That is expected — your repo started from a template, so it has no ancestor
in common with the course. Do it once with the flag, and never again:

```bash
git pull upstream main --allow-unrelated-histories
```

---

## 5. Create your virtual environment

A virtual environment is a private box of Python packages for this project only. You do
not need to understand it yet. You do need to activate it **every time you open a new terminal**.

```bash
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\Activate.ps1         # Windows PowerShell
pip install -r requirements.txt
```

You will know it worked because your prompt now starts with `(.venv)`.

> **The most common error in week 1** is running a command without activating the venv
> first. If something worked yesterday and doesn't today, check for `(.venv)` before
> you check anything else.

---

## 6. Tell git who you are

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## 7. Prove it all works

```bash
python3 check_setup.py
```

Every line should say **OK**. If any line says **FAIL**, it tells you exactly what to fix.

When all seven checks pass, you are done. Message your instructor the output and go
open `week-01/README.md`.

[Windows Terminal]: https://apps.microsoft.com/detail/9n0dx20hk701
[Homebrew]: https://brew.sh
[python.org/downloads]: https://www.python.org/downloads/
[code.visualstudio.com]: https://code.visualstudio.com/
[Git for Windows]: https://git-scm.com/download/win
