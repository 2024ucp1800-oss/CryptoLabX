"""
Brute-force and dictionary-scoring cryptanalysis.
"""

import re
from pathlib import Path

from shift_cipher import decrypt


def load_dictionary(dictionary_path):
    """Load English words from a file."""

    path = Path(dictionary_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dictionary not found: {dictionary_path}"
        )

    words = set()

    with path.open("r", encoding="utf-8") as file:

        for line in file:

            word = line.strip().lower()

            if word and word.isalpha():
                words.add(word)

    return words


def extract_words(text):
    """Extract words from plaintext."""

    return re.findall(
        r"[A-Za-z]+",
        text.lower()
    )


def dictionary_score(text, dictionary):
    """Count dictionary words in plaintext."""

    words = extract_words(text)

    score = 0

    for word in words:

        if word in dictionary:
            score += 1

    return score


def brute_force(ciphertext):
    """Try all 26 possible keys."""

    results = []

    for key in range(26):

        plaintext = decrypt(
            ciphertext,
            key
        )

        results.append({
            "key": key,
            "plaintext": plaintext
        })

    return results


def dictionary_attack(ciphertext, dictionary):
    """Select key with highest dictionary score."""

    candidates = brute_force(ciphertext)

    best_candidate = None

    for candidate in candidates:

        score = dictionary_score(
            candidate["plaintext"],
            dictionary
        )

        candidate["score"] = score

        if (
            best_candidate is None
            or score > best_candidate["score"]
        ):
            best_candidate = candidate

    return best_candidate, candidates