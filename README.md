# ✦ STREAK TODO

A minimal, beautiful terminal to-do app with streak tracking.  
No dependencies — just Python 3.6+.

---

## Project Info

| Field | Details |
|-------|---------|
| **NetID** | wmy1 |
| **Name** | Christie Yiu |
| **GitHub Repository** | [ToDoList](https://github.com/Christiewmy1/ToDoList.git) |

## Idea

A terminal-based to-do list application designed to build consistent daily habits through a streak system. The core idea is that productivity is best maintained through momentum — so the app rewards you for completing all your tasks every day by incrementing a streak counter, and resets it if you miss a day.

Users can add tasks, check them off as they complete them, uncheck them if needed, and delete ones that are no longer relevant. Each task displays how old it is, so nothing gets forgotten or left to linger. A visual progress bar shows how close you are to completing everything for the day.

The streak feature is the heart of the app: it only increments when every single task is marked done, encouraging you to finish what you start rather than leaving things half-done. A total completed count tracks your overall productivity over time, separate from the streak so past effort is never lost even if the streak breaks.

All data persists locally between sessions using a JSON file, meaning the app works entirely offline with no accounts or setup required beyond Python.

---

## Features

- ✅ Add, check off, uncheck, and delete tasks
- 🔥 Daily streak counter — complete ALL tasks to keep your streak alive
- 📊 Progress bar showing today's completion
- 🗓️ Task age tracking (how old each task is)
- 💾 Persistent data stored locally across sessions
- 🎨 Colorful terminal UI with ANSI colors

## Run locally

```bash
python todo.py
```

## Build your own executable

```bash
pip install pyinstaller
pyinstaller --onefile --name streak-todo todo.py
# Output: dist/streak-todo  (or dist/streak-todo.exe on Windows)
```

## Controls

| Key | Action          |
|-----|-----------------|
| `a` | Add a new task  |
| `c` | Check off a task|
| `u` | Uncheck a task  |
| `d` | Delete a task   |
| `q` | Quit            |

## Streak rules

- Complete **all** tasks in a single day → streak +1
- Miss a day → streak resets to 1
- Total completed tasks are tracked separately from the streak

## Data storage

Data is saved to a platform-appropriate location:
- **Linux**: `~/.local/share/streak_todo/data.json`
- **macOS**: `~/Library/Application Support/streak_todo/data.json`
- **Windows**: `%APPDATA%\streak_todo\data.json`
