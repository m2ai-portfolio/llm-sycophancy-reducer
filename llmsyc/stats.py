"""In-memory per-process counters for optimization statistics."""


class Stats:
    """Per-process statistics tracker. Each instance starts at zero."""

    def __init__(self) -> None:
        self._attempts: int = 0
        self._hits: int = 0
        self._saved_tokens: int = 0

    def record_attempt(self) -> None:
        self._attempts += 1

    def record_hit(self, saved: int) -> None:
        self._hits += 1
        self._saved_tokens += saved

    def summary(self) -> dict[str, int]:
        return {
            "attempts": self._attempts,
            "hits": self._hits,
            "saved_tokens": self._saved_tokens,
        }
