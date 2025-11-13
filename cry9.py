def generate_matrix(key):
    key = "".join(dict.fromkeys(key.upper().replace("J","I")))
    matrix = key
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in matrix:
            matrix += ch
    return [list(matrix[i*5:(i+1)*5]) for i in range(5)]

def find_pos(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j

def playfair_encrypt(text, matrix):
    text = text.upper().replace("J","I").replace(" ","")
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1<len(text) else "X"
        if a==b: b="X"; i+=1
        else: i+=2
        r1,c1 = find_pos(matrix,a)
        r2,c2 = find_pos(matrix,b)
        if r1==r2:
            result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1==c2:
            result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
    return result

def playfair_decrypt(text, matrix):
    result = ""
    i=0
    while i<len(text):
        a=text[i]; b=text[i+1] if i+1<len(text) else "X"; i+=2
        r1,c1=find_pos(matrix,a)
        r2,c2=find_pos(matrix,b)
        if r1==r2:
            result+=matrix[r1][(c1-1)%5]+matrix[r2][(c2-1)%5]
        elif c1==c2:
            result+=matrix[(r1-1)%5][c1]+matrix[(r2-1)%5][c2]
        else:
            result+=matrix[r1][c2]+matrix[r2][c1]
    return result

# --- Main ---
key = input("Enter key: ")
matrix = generate_matrix(key)
mode = input("Encrypt or Decrypt (E/D): ").upper()
text = input("Enter text: ").upper()
if mode=="E":
    print("Ciphertext:", playfair_encrypt(text,matrix))
else:
    print("Plaintext:", playfair_decrypt(text,matrix))
