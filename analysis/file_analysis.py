from collections import Counter


def analyze_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()

    characters = len(text)
    words = len(text.split())
    lines = len(text.splitlines())
    unique_characters = len(set(text))
    letters = [char.lower() for char in text if char.isalpha()]
    frequency = Counter(letters)

    print("\n------ Analysis ------")
    print("File:", filepath)
    print("Characters :", characters)
    print("Words :", words)
    print("Lines :", lines)
    print("Unique Characters :", unique_characters)
    print("\nLetter Frequency")
    for letter in sorted(frequency):
        print(letter, ":", frequency[letter])
