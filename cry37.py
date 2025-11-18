#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define MAX_TEXT 10000
#define ALPHABET 26

// English frequency order (most → least)
char englishRank[] = "ETAOINSHRDLCUMWFGYPBVKJXQZ";

typedef struct {
    int score;
    char plaintext[MAX_TEXT];
} Candidate;

int cmp(const void *a, const void *b) {
    return ((Candidate*)a)->score - ((Candidate*)b)->score;
}

void count_frequency(char *text, int freq[]) {
    for (int i = 0; i < ALPHABET; i++) freq[i] = 0;
    for (int i = 0; text[i]; i++) {
        if (isalpha(text[i])) {
            freq[toupper(text[i]) - 'A']++;
        }
    }
}

void rank_by_frequency(int freq[], char out[]) {
    int used[ALPHABET] = {0};

    for (int i = 0; i < ALPHABET; i++) {
        int best = -1, bestVal = -1;
        for (int j = 0; j < ALPHABET; j++) {
            if (!used[j] && freq[j] > bestVal) {
                bestVal = freq[j];
                best = j;
            }
        }
        out[i] = best + 'A';
        used[best] = 1;
    }
}

void substitute(char *ciphertext, char map[], char *out) {
    for (int i = 0; ciphertext[i]; i++) {
        if (isalpha(ciphertext[i])) {
            int idx = toupper(ciphertext[i]) - 'A';
            out[i] = map[idx];
        } else {
            out[i] = ciphertext[i];
        }
    }
}

int score_plaintext(char *pt) {
    int score = 0;
    int freq[ALPHABET] = {0};
    count_frequency(pt, freq);

    char rankList[ALPHABET];
    rank_by_frequency(freq, rankList);

    for (int i = 0; i < ALPHABET; i++) {
        int actualPos = strchr(englishRank, rankList[i]) - englishRank;
        score += abs(i - actualPos);
    }
    return score;
}

int main() {
    char ciphertext[MAX_TEXT];
    int topN;

    printf("=== Monoalphabetic Substitution Cipher Frequency Attack ===\n\n");

    printf("Enter ciphertext: ");
    fgets(ciphertext, MAX_TEXT, stdin);

    printf("How many top plaintexts to show? ");
    scanf("%d", &topN);

    // Step 1: Count ciphertext frequencies
    int freq[ALPHABET];
    count_frequency(ciphertext, freq);

    // Step 2: Rank ciphertext letters by frequency
    char cipherRank[ALPHABET];
    rank_by_frequency(freq, cipherRank);

    // Step 3: Produce candidate mappings by permuting top English letters
    // For simplicity, swap top 6 letters (common heuristic)
    char engTop[] = "ETAOIN";
    int num = 0;

    Candidate candidates[800];
    int idx = 0;

    for (int a = 0; a < 6; a++)
    for (int b = 0; b < 6; b++)
    for (int c = 0; c < 6; c++)
    for (int d = 0; d < 6; d++)
    for (int e = 0; e < 6; e++)
    for (int f = 0; f < 6; f++) {
        if (idx >= 800) break;

        char map[ALPHABET];
        // initial mapping
        for (int i = 0; i < ALPHABET; i++)
            map[cipherRank[i] - 'A'] = englishRank[i];

        // modify top 6
        char perm[6] = {engTop[a], engTop[b], engTop[c], engTop[d], engTop[e], engTop[f]};
        int used[6]={0};

        for (int i = 0; i < 6; i++) {
            map[cipherRank[i] - 'A'] = perm[i];
        }

        char plaintext[MAX_TEXT];
        substitute(ciphertext, map, plaintext);
        plaintext[strlen(ciphertext)] = '\0';

        candidates[idx].score = score_plaintext(plaintext);
        strcpy(candidates[idx].plaintext, plaintext);
        idx++;
    }

    // Sort by likelihood
    qsort(candidates, idx, sizeof(Candidate), cmp);

    printf("\n=== Top %d Possible Plaintexts ===\n\n", topN);
    for (int i = 0; i < topN && i < idx; i++) {
        printf("[%d] Score = %d\n%s\n", i+1, candidates[i].score, candidates[i].plaintext);
        printf("----------------------------------------------------\n");
    }

    return 0;
}
