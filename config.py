from dataclasses import dataclass

# --- Default homepage ---
DEFAULT_HOMEPAGE = "https://duckduckgo.com/"

# --- Default download directory ---
DEFAULT_DOWNLOAD_DIR = r"C:\Downloads"

# --- User agent strings ---
DEFAULT_USER_AGENT = "CopperBrowser/1.0 (PyQt6 WebEngine)"
CHROME_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/129.0.0.0 Safari/537.36"
)

# --- Search engines ---
SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q={query}",
    "DuckDuckGo": "https://duckduckgo.com/?q={query}",
    "Bing": "https://www.bing.com/search?q={query}",
}

# Default search engine (DuckDuckGo)
DEFAULT_SEARCH_ENGINE = SEARCH_ENGINES["DuckDuckGo"]


@dataclass
class Config:
    homepage: str = DEFAULT_HOMEPAGE
    download_dir: str = DEFAULT_DOWNLOAD_DIR
    user_agent: str = DEFAULT_USER_AGENT
    search_engine: str = DEFAULT_SEARCH_ENGINE

    def to_dict(self):
        return {
            "homepage": self.homepage,
            "download_dir": self.download_dir,
            "user_agent": self.user_agent,
            "search_engine": self.search_engine,
        }

    @staticmethod
    def from_dict(d: dict) -> "Config":
        c = Config()
        for k, v in d.items():
            if hasattr(c, k):
                setattr(c, k, v)
        return c