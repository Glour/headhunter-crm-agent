"""Deterministic normalization of cover-letter text before storage or display."""

import re

COVER_LETTER_TYPOGRAPHY_TRANSLATION = str.maketrans({"—": "-", "–": "-", "«": '"', "»": '"'})
GENERATED_PHRASE_REPLACEMENTS = [
    (re.compile(r"\bчеловек\s+в\s+контуре\b", re.IGNORECASE), "human-in-the-loop"),
    (
        re.compile(r"\bпроверяем(?:ый|ого|ому|ым|ом)?\s+контур[а-яё]*\b", re.IGNORECASE),
        "проверяемую систему",
    ),
    (
        re.compile(r"\bрабоч(?:ий|его|ему|им|ем)?\s+контур[а-яё]*\b", re.IGNORECASE),
        "рабочую систему",
    ),
    (re.compile(r"\bproduction-контур[а-яё]*\b", re.IGNORECASE), "production-системы"),
    (
        re.compile(r"\bагентн(?:ый|ые|ых|ым|ыми|ом)?\s+контур[а-яё]*\b", re.IGNORECASE),
        "агентные системы",
    ),
    (re.compile(r"\bконтур[а-яё]*\b", re.IGNORECASE), "система"),
]
_LEGACY_GREETING_WITH_ADDRESSEE_RE = re.compile(
    r"^\s*Здравствуйте\s*,\s*.{1,180}?[!.]\s*", re.IGNORECASE | re.DOTALL
)


def sanitize_cover_letter_greeting(message: str) -> str:
    """Normalize legacy greetings without changing the remainder of the message."""
    text = (message or "").strip()
    if not text:
        return ""
    if text.startswith("Здравствуйте!"):
        return text

    match = _LEGACY_GREETING_WITH_ADDRESSEE_RE.match(text)
    if match:
        rest = text[match.end() :].lstrip()
        return ("Здравствуйте!" + (f" {rest}" if rest else "")).strip()

    if re.match(r"^\s*Здравствуйте\b", text, flags=re.IGNORECASE):
        rest = re.sub(
            r"^\s*Здравствуйте\b[\s,!.:;—-]*", "", text, count=1, flags=re.IGNORECASE
        ).lstrip()
        return ("Здравствуйте!" + (f" {rest}" if rest else "")).strip()
    return text


def sanitize_cover_letter(message: str) -> str:
    text = sanitize_cover_letter_greeting(message)
    text = text.translate(COVER_LETTER_TYPOGRAPHY_TRANSLATION)
    for pattern, replacement in GENERATED_PHRASE_REPLACEMENTS:
        text = pattern.sub(replacement, text)
    return text
