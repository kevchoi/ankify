from pathlib import Path

from ankify.parser import (
    MarkdownCard,
    get_deck_from_path,
    parse_markdown_file,
    parse_all,
)


def test_compute_hash():
    hash1 = MarkdownCard.compute_hash("What is Python?")
    hash2 = MarkdownCard.compute_hash("What is Python?")
    hash3 = MarkdownCard.compute_hash("What is Java?")

    assert hash1 == hash2
    assert hash1 != hash3
    assert len(hash1) == 16


def test_get_deck_from_path_root():
    base = Path("/notes")
    file = Path("/notes/test.md")
    assert get_deck_from_path(file, base) == "default"


def test_get_deck_from_path_nested():
    base = Path("/notes")
    file = Path("/notes/python/basics/test.md")
    assert get_deck_from_path(file, base) == "python::basics"


def test_parse_markdown_file(tmp_path: Path):
    file = tmp_path / "test.md"
    file.write_text("""# Title

## What is Python?

A programming language.

## How do you print?

```python
print("hello")
```
""")
    cards = parse_markdown_file(file, tmp_path)

    assert len(cards) == 2

    assert cards[0].front_raw == "What is Python?"
    assert cards[0].back_raw == "A programming language."
    assert cards[0].deck == "default"

    assert cards[1].front_raw == "How do you print?"
    assert "print" in cards[1].back_raw


def test_parse_markdown_file_empty_back(tmp_path: Path):
    file = tmp_path / "test.md"
    file.write_text("""## Question with no answer

## Another question

Has an answer.
""")
    cards = parse_markdown_file(file, tmp_path)

    assert len(cards) == 1
    assert cards[0].front_raw == "Another question"


def test_parse_all(tmp_path: Path):
    (tmp_path / "topic1").mkdir()
    (tmp_path / "topic1" / "file.md").write_text("## Q1\n\nA1")

    (tmp_path / "topic2").mkdir()
    (tmp_path / "topic2" / "file.md").write_text("## Q2\n\nA2")

    cards = parse_all(tmp_path)

    assert len(cards) == 2
    decks = {c.deck for c in cards}
    assert "topic1" in decks
    assert "topic2" in decks
