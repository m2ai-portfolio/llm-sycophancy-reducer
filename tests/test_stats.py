"""Unit tests for in-memory statistics counters."""

from llmsyc.stats import Stats


def test_counter_increment() -> None:
    stats = Stats()

    # Initial state
    assert Stats().summary() == {"attempts": 0, "hits": 0, "saved_tokens": 0}

    stats.record_attempt()
    stats.record_attempt()
    stats.record_hit(5)

    s = stats.summary()
    assert s["attempts"] == 2
    assert s["hits"] == 1
    assert s["saved_tokens"] == 5


def test_counter_reset_on_exit() -> None:
    old = Stats()
    old.record_attempt()
    old.record_hit(10)

    # New instance starts fresh
    new = Stats()
    s = new.summary()
    assert s["attempts"] == 0
    assert s["hits"] == 0
    assert s["saved_tokens"] == 0
