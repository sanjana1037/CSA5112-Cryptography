def generate_key_matrix(keyword):
    keyword = keyword.lower().replace("j", "i")
    matrix = []
    for char in keyword:
        if char not in matrix and char.isalpha():
            matrix.append(char)
    for char in "abcdefghijklmnopqrstuvwxyz":
        if char not in matrix and char != 'j':
            matrix.append(char)

    key_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    return key_matrix


def find_position(matrix, char):
    if char == 'j':
        char = 'i'
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None


def encrypt_pair(matrix, a, b):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    if r1 == r2:
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]


def playfair_encrypt(plaintext, matrix):
    plaintext = plaintext.lower().replace("j", "i").replace(" ", "")
    
    pairs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = ''
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
        if a == b or b == '':
            b = 'x'
            i += 1
        else:
            i += 2
        pairs.append((a, b))
    ciphertext = ""
    for a, b in pairs:
        ciphertext += encrypt_pair(matrix, a, b)
    return ciphertext.upper()

keyword = input("Enter the keyword: ")
plaintext = input("Enter the plaintext message: ")

key_matrix = generate_key_matrix(keyword)

print("\nPlayfair Key Matrix:")
for row in key_matrix:
    print(" ".join(row))

ciphertext = playfair_encrypt(plaintext, key_matrix)
print("\nEncrypted Text:", ciphertext)
