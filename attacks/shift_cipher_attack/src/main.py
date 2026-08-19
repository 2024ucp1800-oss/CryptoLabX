from shift_cipher import shift_cipher
from chi_square_attack import best_match

text = input("Enter word  : ")
key  = int(input("Enter key   : "))

cipher = shift_cipher(key, text)
print(f"Cipher text : {cipher}")

cracked, found_key, score = best_match(cipher)
print(f"predicted     : {cracked}  (key={found_key}, chi={score:.2f})")
