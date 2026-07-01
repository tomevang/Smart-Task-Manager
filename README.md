# Smart Task Manager

A lightweight, AI-powered command line task manager — think of it as a mini Jira with a built-in AI assistant. Add tasks, work through them, and let Claude suggest the smartest order to tackle them.

Built as a hands-on demonstration of Python fundamentals: OOP design, five different core data structures used purposefully (not just for show), clean API-style architecture, and AI integration via the Anthropic API.

---

## Features

- **Add, process, and complete tasks** through a simple command line interface
- **Undo** support — restore the last completed task
- **AI-powered prioritization** — ask Claude to suggest the smartest order to tackle your backlog
- **Follow AI suggestions** — automatically reorder your task queue based on Claude's recommendation
- Clean separation between core logic and the command line interface, so a future web UI (Flask) can reuse the same backend without any changes

---

## How It's Built

This project intentionally uses five different data structures, each chosen for a specific reason:

| Data Structure | Used For | Why |
|---|---|---|
| **Dictionary** | Storing all tasks (`{id: description}`) | O(1) lookup by task ID |
| **Set** | Tracking completed task IDs | Fast existence checks, no duplicates |
| **Queue (`deque`)** | The task backlog | First-in-first-out processing order |
| **Stack (list)** | Undo history | Last completed task is the first one undone |
| **Linked List** | Reordering the backlog from AI suggestions | O(1) insertion, demonstrates the data structure directly |

The core logic (`task_manager.py`) is written like a small internal API — every method returns structured data (like `(True, task_id)` or `("busy", task_id)`) rather than printing directly. The command line interface (`main.py`) is just one possible "client" of that API. This means a future Flask-based web interface could call the exact same `task_manager.py` without modifying a single line of it.

---

## Project Structure

```
Smart-Task-Manager/
├── main.py                  # Command line interface — the "client"
├── task_manager.py          # Core logic and data structures — the "API"
├── linked_list.py           # Linked list used for AI-based reordering
├── ai_client.py             # Anthropic API integration
├── requirements.txt         # Python dependencies
├── tests/
│   └── test_task_manager.py # Unit tests
└── .github/
    └── workflows/
        └── ci.yml            # GitHub Actions CI/CD pipeline
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tomevang/Smart-Task-Manager.git
cd Smart-Task-Manager
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key

The AI suggestion feature needs an Anthropic API key. Get one at [console.anthropic.com](https://console.anthropic.com), then set it as an environment variable.

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your-key-here"
```

**Windows (permanent, recommended):**
1. Search "Environment Variables" in the Start menu
2. Click "Edit the system environment variables" → "Environment Variables"
3. Under "User variables" click "New"
4. Name: `ANTHROPIC_API_KEY`, Value: your key
5. Click OK — this persists across restarts

**macOS / Linux:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 4. Run it

```bash
python main.py
```

You should see a `>` prompt ready for commands.

---

## Usage

Once running, type commands at the `>` prompt.

| Command | What it does | Example |
|---|---|---|
| `add <description>` | Add a new task | `add write unit tests for auth module` |
| `show` | Display all tasks grouped by status (Backlog / In Progress / Completed) | `show` |
| `process` | Move the next task from the backlog into "in progress" | `process` |
| `complete <id>` | Mark a task as complete | `complete 3` |
| `undo` | Undo the most recently completed task | `undo` |
| `ai suggest` | Ask Claude to suggest a priority order for the backlog | `ai suggest` |
| `follow` | Reorder the backlog to match the AI's last suggestion | `follow` |
| `quit` / `q` | Exit the program | `quit` |

### Example Session

```
> add fix login bug in production
Task 1 was created successfully.

> add write unit tests for auth module
Task 2 was created successfully.

> add update README documentation
Task 3 was created successfully.

> ai suggest
AI suggests this order: [1, 2, 3]

> follow
Reordering the task list according to the AI suggested order.

> process
Task 1 successfully processed!

> complete 1
Task 1 marked as complete!

> show

Backlog:
  2: write unit tests for auth module
  3: update README documentation

In Progress:
(None)

Completed tasks
  1: fix login bug in production
```

---

## Task Lifecycle

```
add_task()      →  task enters the backlog
process()       →  oldest backlog task moves to "in progress" (one at a time)
complete()      →  task moves to "completed", can be from backlog OR in progress
undo()          →  most recently completed task returns to the back of the backlog
ai suggest      →  Claude analyzes current tasks and suggests a priority order
follow()        →  backlog is rebuilt in the AI's suggested order
```

Only one task can be "in progress" at a time — if you try to `process` while a task is already in progress, you'll be told to complete it first.

---

## Design Decisions Worth Knowing

- **API-style return values, not print statements** — every `task_manager.py` method returns structured data like `(success, value)` tuples rather than printing to the console. This keeps the core logic completely independent of *how* it's displayed, whether that's a command line, a future web page, or an automated test.
- **Linked list for AI reordering** — technically a plain Python list would work fine at this scale. The linked list is used deliberately here to demonstrate O(1) insertion when rebuilding an ordered sequence, and to showcase the data structure directly in a real, working context rather than an isolated exercise.
- **Consistent status-based returns** — methods like `process_next()` return a status string (`"success"`, `"busy"`, `"empty"`) alongside relevant data, so the calling code can respond precisely to *why* something did or didn't happen, not just whether it worked.

---

## Running Tests

```bash
python -m pytest tests/
```

---

## Roadmap — Phase 2

This is Phase 1 of the project: a fully functional command line application. Phase 2 will extend it into a full web application without changing the core logic at all:

- **Flask REST API** — expose `task_manager.py` through HTTP endpoints
- **SQLite** — persist tasks across restarts
- **Simple HTML/JS frontend** — a browser-based UI that talks to the REST API
- **Docker** — containerize the full application
- **Polished documentation** — screenshots and a full walkthrough

---

## Tech Stack

- **Python 3.13**
- **Anthropic Claude API** — AI-powered task prioritization
- **GitHub Actions** — CI/CD pipeline (lint, test, security scan)

---

## Author

Built by [Tome Vang](https://github.com/tomevang) as a hands-on portfolio project — combining Python fundamentals, thoughtful data structure usage, and modern AI integration.
