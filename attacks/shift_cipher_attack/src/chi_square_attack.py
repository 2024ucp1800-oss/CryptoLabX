import os
from pandas import read_csv

_CSV = os.path.join(os.path.dirname(__file__), "..", "dictionary", "english_words.csv")
freq = read_csv(
    _CSV,
    header=None,
    names=["Letter", "Frequency"]
).sort_values("Letter").reset_index(drop=True)

letters    = freq["Letter"].tolist()
frequencies = freq["Frequency"].tolist()


def binary_search(target):
    s, e = 0, len(letters) - 1
    while s <= e:
        mid = (s + e) // 2
        if   letters[mid] == target: 
            return frequencies[mid]
        elif letters[mid] <  target: 
            s = mid + 1
        else:                        
            e = mid - 1
    return 0 


def chi_square(text):
    text = text.upper()
    n = sum(1 for c in text if c.isalpha())

    chi_sq = 0.0
    for char in set(text):
        if char.isalpha():
            observed = text.count(char)
            expected = (binary_search(char) / 100) * n
            chi_sq  += (observed - expected) ** 2 / expected

    return chi_sq


def best_match(cipher_text):
    best_text  = ""
    best_key   = 0
    best_score = float("inf")

    for shift in range(26):
        candidate = "".join(
            chr((ord(c) - ord('a') - shift) % 26 + ord('a')) if c.isalpha() else c
            for c in cipher_text.lower()   
        )
        score = chi_square(candidate)
        if score < best_score:
            best_score = score
            best_text  = candidate
            best_key   = shift

    return best_text, best_key, best_score
