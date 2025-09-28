import os
import json
from dataclasses import dataclass, asdict
from typing import List

# --- Path under AppData\Roaming\CopperBrowserV1 ---
APPDATA_DIR = os.path.join(os.environ["APPDATA"], "CopperBrowserV1")
os.makedirs(APPDATA_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(APPDATA_DIR, "history.json")


@dataclass
class HistoryEntry:
    url: str
    title: str


class History:
    def __init__(self):
        self.entries: List[HistoryEntry] = []

    def add(self, url: str, title: str):
        """Add a new entry to history."""
        self.entries.append(HistoryEntry(url, title))

    def list(self) -> List[HistoryEntry]:
        """Return all history entries."""
        return self.entries

    def clear(self):
        """Remove all history entries."""
        self.entries = []


def load_history() -> History:
    """Load history from JSON file into a History object."""
    h = History()
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    h.entries.append(HistoryEntry(**item))
        except Exception:
            # If file is corrupt or unreadable, start fresh
            pass
    return h


def save_history(history: History):
    """Save history entries to JSON file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in history.entries], f, indent=2)
    except Exception:
        # Fail silently if file cannot be written
        pass