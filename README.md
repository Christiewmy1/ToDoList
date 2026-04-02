# ✦ STREAK TODO

A minimal, beautiful terminal to-do app with streak tracking.  
No dependencies — just Python 3.6+.

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
