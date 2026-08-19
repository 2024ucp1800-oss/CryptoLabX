def shift_cipher(k, plain_text):
    cipher_text = ""
    for char in plain_text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            cipher_text += chr((ord(char) - base + k) % 26 + base)
    return cipher_text
