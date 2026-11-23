"""One Line, Best Line — make.fun entry.

Writes a single original line of text to ``entry.txt`` inside
``MAKEFUN_OUTPUT_DIR`` (default ``/output``).

The line was written and chosen in this session: 12 original candidates were
scored pairwise against the contest's published judge brief (one line on a
free/entertaining theme, scroll-stopping first words, genuinely entertaining,
single-sentence landing with a turn at the end, fresh), and the winner was
tightened in a second revision pass. See ``../variants.md`` for the tournament.

Standard library only. No network, no third-party code.
"""

import os
import sys
import tempfile

# The winning line (95 characters, one sentence, one line).
LINE = (
    "My plants died while I was on a wellness retreat learning to take "
    "better care of living things."
)

MAX_CHARS = 240


def validate(line: str) -> None:
    """Fail loudly if the line breaks the contest gate."""
    if not line:
        raise ValueError("entry line is empty")
    if line != line.strip():
        raise ValueError("entry line has leading or trailing whitespace")
    if not line.strip():
        raise ValueError("entry line is only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line (contains newline)")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    # Must be encodable as UTF-8, and count characters, not bytes.
    line.encode("utf-8")


def main() -> int:
    validate(LINE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    # Atomic write: temp file in the same directory, then os.replace.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(LINE)
            fh.write("\n")
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    os.replace(tmp_path, target)

    # Read back and re-validate exactly what landed on disk.
    with open(target, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != LINE + "\n":
        raise ValueError("entry.txt contents do not match the validated line")
    validate(written.rstrip("\n"))

    print("wrote %s (%d chars)" % (target, len(LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
