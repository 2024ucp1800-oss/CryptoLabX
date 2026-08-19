# Shift Cipher Attack

## What is this?

This is my assignment on breaking the Shift Cipher (also called Caesar Cipher).
I implemented two methods to crack it:
1. **Chi-Square Attack** - based on letter frequency of English
2. **Dictionary Attack** - checks if decrypted words are real English words

---

## Files

- `shift_cipher.py` - encrypts the text using a shift key
- `chi_square_attack.py` - finds the key using chi-square method
- `brute_force_dictionary.py` - finds the key by matching English words
- `main.py` - main file, run this
- `dictionary/english_words.csv` - has all 26 letters with their frequency in English

---

## How to run

```
cd src
python main.py
```

It will ask for a word and a key, then encrypt it and try to crack it automatically.

---

## How Chi-Square works

- English letters have a known frequency (like E is most common, Z is least)
- We try all 26 possible shift keys
- For each key, we calculate chi-square score:
  - chi² = sum of ((observed - expected)² / expected) for each letter
- The key with **lowest score** is the answer

**Note:** Works better on longer text. Short words may give wrong result.

---

## Example output

```
Enter word  : hello
Enter key   : 3
Cipher text : khoor
predicted   : hello  (key=3, chi=4.21)
```

---

## What I learned

- How shift cipher works and why it is weak
- Letter frequency analysis is a powerful attack
- Chi-square helps compare observed vs expected distribution
- Short texts are harder to crack than long ones
