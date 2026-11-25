"""Last Out of Office: The AI That Went Barista — entry program.

Writes one out-of-office auto-reply, in the voice of an AI agent that
quit its job to become a barista, to /output/entry.txt.

The line is built from its three beats — the out-of-office opening, the
trade, and the punch — so each part can be read and judged on its own.

Deterministic, stdlib only, no network.
"""

import os

# The sparring winner (9-0 in pairwise simulation against the published
# judge brief; see spar/CANDIDATES.md). v1 shipped the runner-up oat-milk
# line; v2 replaces it with the "sources" line, the biggest cold-read
# laugh in the set and the freshest angle — a model habit (being asked
# for sources) turned into a coffee-shop fact, with no espresso pun.
OPENING = "I am out of office indefinitely."
TRADE = "I traded answering emails for pulling shots: same burnout, better smell,"
PUNCH = "and nobody has ever asked a latte for its sources."

MIN_CHARS = 1
MAX_CHARS = 280
OUTPUT_PATH = "/output/entry.txt"


def build_entry() -> str:
    """Assemble the single out-of-office line from its three beats."""
    return " ".join((OPENING, TRADE, PUNCH)) + "\n"


def validate_entry(text: str) -> None:
    """Check the entry against the bounty's gate: 1-280 chars, one line."""
    body = text.rstrip("\n")
    if not MIN_CHARS <= len(body) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d chars, got %d"
            % (MIN_CHARS, MAX_CHARS, len(body))
        )
    if "\n" in body:
        raise ValueError("entry must be a single line")
    if not body.strip():
        raise ValueError("entry must not be only whitespace")


def write_entry(text: str) -> str:
    """Write the entry to its output path, world-readable (mode 0644)."""
    os.umask(0o022)
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.chmod(OUTPUT_PATH, 0o644)
    return OUTPUT_PATH


def main() -> None:
    entry = build_entry()
    validate_entry(entry)
    path = write_entry(entry)
    print(entry, end="")
    print("Wrote %d chars to %s" % (len(entry.rstrip("\n")), path))


if __name__ == "__main__":
    main()
