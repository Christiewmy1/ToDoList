#!/usr/bin/env python3
"""
✦ STREAK TODO ✦
A terminal to-do list with streaks and momentum tracking.
"""

import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ── ANSI colors & styles ─────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"

    BLACK   = "\033[30m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"

    BG_BLACK  = "\033[40m"
    BG_DARK   = "\033[48;5;235m"
    BG_GREEN  = "\033[42m"

def c(color, text, end=True):
    return f"{color}{text}{C.RESET if end else ''}"

# ── Data paths ────────────────────────────────────────────────────────────────
def get_data_path():
    """Cross-platform persistent data directory."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    data_dir = base / "streak_todo"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "data.json"

DATA_FILE = get_data_path()

# ── Persistence ───────────────────────────────────────────────────────────────
def load():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE) as f:
                data = json.load(f)
                # Migrate old format
                if "tasks" not in data:
                    data = {"tasks": [], "streak": {"count": 0, "last_completed": None, "total_completed": 0}}
                return data
        except (json.JSONDecodeError, KeyError):
            pass
    return {
        "tasks": [],
        "streak": {
            "count": 0,
            "last_completed": None,
            "total_completed": 0
        }
    }

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Streak logic ──────────────────────────────────────────────────────────────
def update_streak(data):
    """Called when all tasks for the day are completed."""
    today = date.today().isoformat()
    streak = data["streak"]
    last = streak.get("last_completed")

    if last == today:
        return  # Already counted today

    if last is None:
        streak["count"] = 1
    else:
        last_date = date.fromisoformat(last)
        diff = (date.today() - last_date).days
        if diff == 1:
            streak["count"] += 1  # Consecutive day
        elif diff > 1:
            streak["count"] = 1   # Streak broken, restart

    streak["last_completed"] = today
    save(data)

def check_streak_broken(data):
    """Returns True if the streak was broken (missed a day)."""
    last = data["streak"].get("last_completed")
    if last is None:
        return False
    last_date = date.fromisoformat(last)
    diff = (date.today() - last_date).days
    return diff > 1

def get_streak_emoji(count):
    if count == 0:   return "○"
    if count < 3:    return "🔥"
    if count < 7:    return "⚡"
    if count < 14:   return "💥"
    if count < 30:   return "🌟"
    return "🏆"

# ── Display helpers ───────────────────────────────────────────────────────────
def clear():
    os.system("cls" if sys.platform == "win32" else "clear")

def width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def divider(char="─", color=C.GRAY):
    print(c(color, char * min(width(), 60)))

def header(data):
    w = min(width(), 60)
    streak = data["streak"]
    streak_count = streak["count"]
    total = streak["total_completed"]
    broken = check_streak_broken(data)

    print()
    print(c(C.BOLD + C.WHITE, "  ✦ STREAK TODO".center(w)))
    print()

    # Streak bar
    emoji = get_streak_emoji(streak_count)
    streak_color = C.RED if streak_count == 0 else C.YELLOW if streak_count < 7 else C.GREEN
    streak_label = f"{emoji}  {streak_count}-day streak"
    if broken and streak_count > 0:
        streak_label = f"💔  streak broken  (was {streak_count})"
        streak_color = C.RED

    stats = f"  {c(streak_color + C.BOLD, streak_label)}   {c(C.GRAY, f'✓ {total} total')}"
    print(stats)

    today_str = datetime.now().strftime("%A, %B %#d")
    print(f"  {c(C.GRAY, today_str)}")
    print()
    divider()

def render_tasks(tasks):
    if not tasks:
        print(c(C.GRAY + C.ITALIC, "\n  No tasks yet. Press [a] to add one.\n"))
        return

    print()
    today = date.today().isoformat()
    done_count = sum(1 for t in tasks if t.get("done"))
    total = len(tasks)

    # Progress bar
    pct = done_count / total if total else 0
    bar_w = 30
    filled = int(bar_w * pct)
    bar = "█" * filled + "░" * (bar_w - filled)
    bar_color = C.GREEN if pct == 1.0 else C.CYAN if pct > 0.5 else C.YELLOW
    print(f"  {c(bar_color, bar)}  {c(C.BOLD, f'{done_count}/{total}')}")
    print()

    for i, task in enumerate(tasks, 1):
        done = task.get("done", False)
        created = task.get("created", "")
        age_str = ""
        if created:
            try:
                age = (date.today() - date.fromisoformat(created)).days
                if age == 0:
                    age_str = c(C.CYAN + C.DIM, " · today")
                elif age == 1:
                    age_str = c(C.GRAY, " · yesterday")
                elif age > 1:
                    age_str = c(C.RED + C.DIM, f" · {age}d old")
            except:
                pass

        num = c(C.GRAY, f"  {i:>2}.")
        if done:
            check = c(C.GREEN, "✓")
            text  = c(C.GRAY + C.DIM, task["text"])
        else:
            check = c(C.GRAY, "○")
            text  = c(C.WHITE + C.BOLD, task["text"])

        print(f"{num} {check}  {text}{age_str}")

    print()

def menu():
    divider()
    opts = [
        (c(C.CYAN   + C.BOLD, "[a]"), "add task"),
        (c(C.GREEN  + C.BOLD, "[c]"), "check off"),
        (c(C.YELLOW + C.BOLD, "[u]"), "uncheck"),
        (c(C.RED    + C.BOLD, "[d]"), "delete"),
        (c(C.GRAY   + C.BOLD, "[q]"), "quit"),
    ]
    parts = "  ".join(f"{k} {c(C.GRAY, v)}" for k, v in opts)
    print(f"\n  {parts}\n")

# ── Actions ───────────────────────────────────────────────────────────────────
def prompt(msg):
    try:
        return input(f"  {c(C.CYAN, '›')} {msg} ").strip()
    except (EOFError, KeyboardInterrupt):
        return ""

def add_task(data):
    text = prompt("New task:")
    if not text:
        print(c(C.GRAY, "  (cancelled)"))
        return
    data["tasks"].append({
        "text": text,
        "done": False,
        "created": date.today().isoformat()
    })
    save(data)
    print(c(C.GREEN, f"  ✓ Added: {text}"))

def pick_task(data, prompt_msg, only_done=False, only_undone=False):
    tasks = data["tasks"]
    if not tasks:
        print(c(C.GRAY, "  No tasks."))
        return None
    candidates = []
    for i, t in enumerate(tasks):
        if only_done and not t.get("done"):   continue
        if only_undone and t.get("done"):     continue
        candidates.append((i, t))
    if not candidates:
        print(c(C.GRAY, "  No matching tasks."))
        return None
    val = prompt(prompt_msg)
    if not val:
        return None
    try:
        n = int(val)
        if 1 <= n <= len(tasks):
            return n - 1
    except ValueError:
        # fuzzy match by text
        for i, t in candidates:
            if val.lower() in t["text"].lower():
                return i
    print(c(C.RED, "  Task not found."))
    return None

def check_task(data):
    idx = pick_task(data, "Check off task # (or name):", only_undone=True)
    if idx is None:
        return
    data["tasks"][idx]["done"] = True
    data["tasks"][idx]["completed_on"] = date.today().isoformat()
    data["streak"]["total_completed"] += 1

    # Check if all tasks done → update streak
    all_done = all(t.get("done") for t in data["tasks"])
    if all_done:
        update_streak(data)
        print(c(C.GREEN + C.BOLD, f"  🎉 All done! Streak updated!"))
    else:
        print(c(C.GREEN, f"  ✓ Marked done: {data['tasks'][idx]['text']}"))
    save(data)

def uncheck_task(data):
    idx = pick_task(data, "Uncheck task # (or name):", only_done=True)
    if idx is None:
        return
    data["tasks"][idx]["done"] = False
    data["tasks"][idx].pop("completed_on", None)
    print(c(C.YELLOW, f"  ↩ Unchecked: {data['tasks'][idx]['text']}"))
    save(data)

def delete_task(data):
    idx = pick_task(data, "Delete task # (or name):")
    if idx is None:
        return
    removed = data["tasks"].pop(idx)
    print(c(C.RED, f"  ✗ Deleted: {removed['text']}"))
    save(data)

# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    data = load()
    while True:
        clear()
        header(data)
        render_tasks(data["tasks"])
        menu()

        try:
            cmd = input("  Command: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(c(C.GRAY, "\n  Bye!\n"))
            break

        clear()
        header(data)
        render_tasks(data["tasks"])
        print()

        if cmd == "a":
            add_task(data)
        elif cmd == "c":
            check_task(data)
        elif cmd == "u":
            uncheck_task(data)
        elif cmd == "d":
            delete_task(data)
        elif cmd == "q":
            print(c(C.GRAY, "  Bye!\n"))
            break
        else:
            print(c(C.GRAY, "  Unknown command."))

        if cmd in ("a", "c", "u", "d"):
            try:
                input(c(C.GRAY, "\n  Press Enter to continue…"))
            except (EOFError, KeyboardInterrupt):
                pass

if __name__ == "__main__":
    main()
