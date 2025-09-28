import os
import json
from dataclasses import dataclass, asdict
from typing import List

# --- Path under AppData\Roaming\CopperBrowserV1 ---
APPDATA_DIR = os.path.join(os.environ["APPDATA"], "CopperBrowserV1")
os.makedirs(APPDATA_DIR, exist_ok=True)

BOOKMARKS_FILE = os.path.join(APPDATA_DIR, "bookmarks.json")


@dataclass
class Bookmark:
    id: int
    name: str
    url: str


class Bookmarks:
    def __init__(self):
        self.items: List[Bookmark] = []
        self._next_id = 1

    def add(self, name: str, url: str):
        """Add a new bookmark."""
        b = Bookmark(self._next_id, name, url)
        self.items.append(b)
        self._next_id += 1

    def list(self) -> List[Bookmark]:
        """Return all bookmarks."""
        return self.items

    def delete(self, id_: int) -> bool:
        """Delete a bookmark by ID."""
        for i, b in enumerate(self.items):
            if b.id == id_:
                del self.items[i]
                return True
        return False


def load_bookmarks() -> Bookmarks:
    """Load bookmarks from JSON file into a Bookmarks object."""
    b = Bookmarks()
    if os.path.exists(BOOKMARKS_FILE):
        try:
            with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    bm = Bookmark(**item)
                    b.items.append(bm)
                    b._next_id = max(b._next_id, bm.id + 1)
        except Exception:
            # If file is corrupt/unreadable, start fresh
            pass
    return b


def save_bookmarks(bookmarks: Bookmarks):
    """Save bookmarks to JSON file."""
    try:
        with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
            json.dump([asdict(b) for b in bookmarks.items], f, indent=2)
    except Exception:
        # Fail silently if file cannot be written
        pass