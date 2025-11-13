SIZE = 5

matrix = [
    ['M','F','H','I','K'],
    ['U','N','O','P','Q'],
    ['Z','V','W','X','Y'],
    ['E','L','A','R','G'],
    ['D','S','T','B','C']
]

def find_position(ch):
    if ch == 'J': ch = 'I'
    for i in range(SIZE):
        for j in range(SIZE):
            if matrix[i][j] == ch:
                return i,j
    return None

def preprocess_text(text):
    text = ''.join([c.upper() for c in text if c.isalpha()])
    text = text.replace('J','I')
    processed = ''
    i=0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1<len(text) else 'X'
        if a==b:
            processed += a + 'X'
            i += 1
        else:
            processed += a + b
            i += 2
    if len(processed) % 2 != 0:
        processed += 'X'
    return processed

def encrypt_playfair(text):
    cipher = ''
    for i in range(0,len(text),2):
        a,b = text[i], text[i+1]
        r1,c1 = find_position(a)
        r2,c2 = find_position(b)
        if r1==r2: # same row
            cipher += matrix[r1][(c1+1)%SIZE] + matrix[r2][(c2+1)%SIZE]
        elif c1==c2: # same column
            cipher += matrix[(r1+1)%SIZE][c1] + matrix[(r2+1)%SIZE][c2]
        else: # rectangle swap
            cipher += matrix[r1][c2] + matrix[r2][c1]
    return cipher

# --- Main ---
message = "Must see you over Cadogan West. Coming at once."
processed = preprocess_text(message)
ciphertext = encrypt_playfair(processed)

print("Original message:", message)
print("Processed text:", processed)
print("Encrypted text:", ciphertext)
