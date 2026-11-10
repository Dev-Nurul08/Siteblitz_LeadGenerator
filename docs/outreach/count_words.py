"""Count words and run the basic style checks on every example in reference-messages.md.

Run: .venv/Scripts/python.exe docs/outreach/count_words.py
Counts the greeting through the last sentence and leaves out the subject, signature and opt-out line. The same rules
will move into the phase-13 validator. This script only keeps the reference examples honest.
"""
import pathlib
import re

HERE = pathlib.Path(__file__).parent
TEXT = (HERE / "reference-messages.md").read_text(encoding="utf-8")

# Lines that are commentary about the example, not part of the message.
SKIP_PREFIXES = ("Subject:", "Owner's message:", "Why it works", "QR text", "effect for their", "with one yes/no",
                 "(P5)", "(P9)")
# A message ends where the signature or the opt-out line begins.
END_PREFIXES = ("[Sender]", "If this isn't useful", "If you'd rather not hear", "Same reply when", "No further")
BANNED = ["i hope this email finds you well", "i came across", "reaching out", "elevate", "seamless", "unlock",
          "vibrant", "testament", "nestled", "delve", "showcase", "leverage", "online presence", "solutions",
          "dear sir/madam", "feel free to", "don't hesitate"]


def messages():
    for block in re.split(r"^## ", TEXT, flags=re.M)[1:]:
        title, *lines = block.splitlines()
        if title.startswith("Replies"):
            continue
        body = []
        for line in lines:
            s = line.strip()
            if s.startswith(END_PREFIXES):
                break
            if not s or s.startswith(SKIP_PREFIXES):
                continue
            body.append(s)
        yield title, " ".join(body)


for title, body in messages():
    words = len(body.split())
    problems = [p for p in BANNED if p in body.lower()]
    for ch, name in (("—", "em dash"), ("!", "exclamation"), (";", "semicolon")):
        if ch in body:
            problems.append(name)
    first_touch = title.startswith("Email touch 1") or title.startswith("Social")
    if first_touch and body.count("?") != 1:
        problems.append(f"{body.count('?')} questions")
    if first_touch and re.search(r"https?://", body):
        problems.append("link in a first message")
    print(f"{words:4d} words  {title}  {'OK' if not problems else 'FAIL: ' + ', '.join(problems)}")
