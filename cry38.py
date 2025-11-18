#include <stdio.h>
#include <stdlib.h>

int modInverse(int a, int m) {
    a = a % m;
    for (int x = 1; x < m; x++)
        if ((a * x) % m == 1)
            return x;
    return -1;
}

void getInverseMatrix(int P[2][2], int invP[2][2]) {
    int det = (P[0][0]*P[1][1] - P[0][1]*P[1][0]) % 26;
    if (det < 0) det += 26;

    int detInv = modInverse(det, 26);
    if (detInv == -1) {
        printf("Matrix is not invertible mod 26. Attack failed.\n");
        exit(0);
    }

    invP[0][0] =  (P[1][1] * detInv) % 26;
    invP[0][1] = (-P[0][1] * detInv) % 26;
    invP[1][0] = (-P[1][0] * detInv) % 26;
    invP[1][1] =  (P[0][0] * detInv) % 26;

    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            if (invP[i][j] < 0)
                invP[i][j] += 26;
}

void multiplyMatrices(int A[2][2], int B[2][2], int C[2][2]) {
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++) {
            C[i][j] = 0;
            for (int k = 0; k < 2; k++)
                C[i][j] += A[i][k] * B[k][j];
            C[i][j] %= 26;
        }
}

void decrypt(int K[2][2], char *cipher) {
    printf("\nDecrypted text: ");
    for (int i = 0; cipher[i] && cipher[i+1]; i += 2) {
        int c1 = cipher[i]   - 'A';
        int c2 = cipher[i+1] - 'A';

        int p1 = (K[0][0]*c1 + K[0][1]*c2) % 26;
        int p2 = (K[1][0]*c1 + K[1][1]*c2) % 26;

        printf("%c%c", p1 + 'A', p2 + 'A');
    }
    printf("\n");
}

int main() {
    int P[2][2], C[2][2], invP[2][2], K[2][2];

    printf("=== Hill Cipher Known Plaintext Attack (2x2) ===\n\n");

    printf("Enter plaintext pairs (4 letters): ");
    char ptext[5];
    scanf("%s", ptext);

    printf("Enter ciphertext pairs (4 letters): ");
    char ctext[5];
    scanf("%s", ctext);

    // Fill matrices P and C
    P[0][0] = ptext[0] - 'A';
    P[1][0] = ptext[1] - 'A';
    P[0][1] = ptext[2] - 'A';
    P[1][1] = ptext[3] - 'A';

    C[0][0] = ctext[0] - 'A';
    C[1][0] = ctext[1] - 'A';
    C[0][1] = ctext[2] - 'A';
    C[1][1] = ctext[3] - 'A';

    // Compute inverse of P matrix
    getInverseMatrix(P, invP);

    // Solve for key matrix K = C × P^{-1}
    multiplyMatrices(C, invP, K);

    printf("\nRecovered Key Matrix K:\n");
    for (int i = 0; i < 2; i++)
        printf("%d %d\n", K[i][0], K[i][1]);

    printf("\nEnter ciphertext to decrypt: ");
    char longCipher[100];
    scanf("%s", longCipher);

    decrypt(K, longCipher);

    return 0;
}
