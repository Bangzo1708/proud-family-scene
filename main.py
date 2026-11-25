#!/usr/bin/env python3
"""Make the AI Judge Feel Proud: A Family Scene.

Writes one short family scene (1-2 lines, 1-280 characters) to
/output/entry.txt. Python standard library only, fully deterministic,
no network, no randomness, no input files.

Usage:
    python3 main.py                 # writes /output/entry.txt
    python3 main.py --out out.txt   # local preview to a chosen path
"""

import argparse
import os
import sys


# ---------------------------------------------------------------------------
# Candidate variants (written by hand for this bounty, then judged by hand)
# ---------------------------------------------------------------------------
#
# The judge brief (competition.yaml) weighs, most important first:
#   1. A short family scene, real family on the page, warm enough to make
#      a proud judge smile.
#   2. Heartfelt: a small domestic moment with genuine affection, not
#      sentiment stuck on afterwards.
#   3. Funny in a light, recognisable way -- a small turn or a wry line a
#      family would actually laugh at.
#   4. One or two lines, no word wasted.
#   5. Specific and fresh: one telling detail or an unexpected angle,
#      not a greeting-card line.
#
# VARIANT A -- the child's drawing (CHOSEN):
#   "Our six-year-old drew our family for school: Mom in a cape, Dad with
#   a spatula, and herself holding both their hands -- 'because someone has
#   to keep the superheroes from burning dinner.'"
#   Why it wins: the whole family is on the page in one breath; the
#   affection is genuine (a child literally holding her parents' hands);
#   the joke lands as a real kid's line, not a punchline bolted on; and
#   the cape + spatula pairing is a specific, fresh image -- a superhero
#   mum and a cook dad, with the child as the one keeping them together.
#   It is joyful rather than bittersweet, so it wins criterion 1
#   (warm enough to make a proud judge smile) outright against
#   sadder scenes.
#
# VARIANT B -- Grandpa's empty plate (runner-up):
#   "Grandpa still sets a plate for Grandma every Sunday, then eats her
#   dessert himself 'so she won't be jealous.' Nobody corrects him --
#   the kids just pass him the spoon."
#   Why it loses: the dessert joke and the passed spoon are a lovely,
#   specific turn, and it is deeply heartfelt -- but the scene is built
#   on absence (Grandma is gone), so its warmth is bittersweet. Against
#   a purely joyful scene it risks losing criterion 1, the first and
#   most important one. A proud judge smiles wider at a household
#   laughing together than at one remembering.
#
# VARIANT C -- the burnt toast (third):
#   "Dad burned the toast again this morning, and Mom laughed so hard she
#   cried -- then scraped it, buttered it, and ate the blackest piece
#   herself, 'because the cook deserves the best slice.'"
#   Why it loses: warm and funny, and the closing line is a genuine wry
#   turn -- but burnt toast is a well-worn domestic trope, so it scores
#   lowest on criterion 5 (specific and fresh). It reads like a scene
#   anyone could have written; variants A and B both carry an image
#   only this family could own.
#
# Verdict: A > B > C. A is the most on-brief, the most original, and the
# most striking at first glance, so A is the entry.

ENTRY = (
    "Our six-year-old drew our family for school: Mom in a cape, Dad with "
    "a spatula, and herself holding both their hands \u2014 'because someone "
    "has to keep the superheroes from burning dinner.'"
)

MAX_CHARS = 280


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the chosen family scene to entry.txt."
    )
    parser.add_argument(
        "--out",
        default="/output/entry.txt",
        help="Destination file (default: /output/entry.txt).",
    )
    args = parser.parse_args(argv)

    text = ENTRY

    # Gate checks, mirroring the sealed scorer: UTF-8 text, 1-280 chars,
    # not only whitespace, one or two lines.
    if not text or not text.strip():
        print("error: entry is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            "error: entry is %d characters, over the 280 limit" % len(text),
            file=sys.stderr,
        )
        return 1
    lines = text.splitlines()
    if len(lines) > 2:
        print("error: entry has %d lines, max 2" % len(lines), file=sys.stderr)
        return 1

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(args.out, 0o644)

    # Read back and confirm the file on disk is exactly the chosen entry:
    # a write that silently truncated or re-encoded would fail the gate.
    with open(args.out, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text + "\n":
        print("error: read-back mismatch in %s" % args.out, file=sys.stderr)
        return 1

    print("wrote %s (%d characters, %d line(s))" % (args.out, len(text), len(lines)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
