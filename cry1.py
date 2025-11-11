def caesar_cipher(text, k):
    result = ""
    
    for char in text:
        # Encrypt uppercase letters
        if char.isupper():
            result += chr((ord(char) - 65 + k) % 26 + 65)
        # Encrypt lowercase letters
        elif char.islower():
            result += chr((ord(char) - 97 + k) % 26 + 97)
        # Leave other characters unchanged
        else:
            result += char
    return result


# Input from user
text = input("Enter the text to encrypt: ")
k = int(input("Enter the shift value (1-25): "))

if 1 <= k <= 25:
    encrypted_text = caesar_cipher(text, k)
    print(f"Encrypted text (shift={k}):", encrypted_text)
else:
    print("Please enter a valid shift between 1 and 25.")
