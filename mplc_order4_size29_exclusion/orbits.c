/* Complete orbit generation under S_4 wr S_3, without a graph library. */
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint64_t Mask;
enum { CAPACITY = 4096 };
static unsigned words[64][3];
static Mask balls[64];
static Mask levels[8][CAPACITY];
static unsigned counts[8];

static unsigned positions(Mask mask, unsigned *out) {
    unsigned count = 0;
    while (mask != 0) {
        out[count++] = (unsigned)__builtin_ctzll(mask);
        mask &= mask - 1;
    }
    return count;
}

static int next_permutation(unsigned *p, unsigned k) {
    if (k < 2) return 0;
    unsigned i = k - 1;
    while (i > 0 && p[i-1] >= p[i]) --i;
    if (i == 0) return 0;
    unsigned j = k - 1;
    while (p[j] <= p[i-1]) --j;
    unsigned tmp = p[i-1]; p[i-1] = p[j]; p[j] = tmp;
    j = k - 1;
    while (i < j) { tmp = p[i]; p[i] = p[j]; p[j] = tmp; ++i; --j; }
    return 1;
}

static Mask canonical(Mask mask) {
    unsigned selected[64], order[7];
    const unsigned k = positions(mask, selected);
    if (k == 0) return 0;
    if (k > 7) { fputs("canonical domain exceeds seven\n", stderr); exit(1); }
    for (unsigned j = 0; j < k; ++j) order[j] = j;
    Mask best = UINT64_MAX;
    do {
        Mask columns[3] = {0, 0, 0};
        for (unsigned axis = 0; axis < 3; ++axis) {
            unsigned labels[4] = {4, 4, 4, 4}, next = 0;
            for (unsigned j = 0; j < k; ++j) {
                const unsigned value = words[selected[order[j]]][axis];
                if (labels[value] == 4) labels[value] = next++;
                columns[axis] = (columns[axis] << 2U) | labels[value];
            }
        }
        for (unsigned a = 0; a < 3; ++a) {
            for (unsigned b = a+1; b < 3; ++b) {
                if (columns[a] > columns[b]) { Mask tmp = columns[a]; columns[a] = columns[b]; columns[b] = tmp; }
            }
        }
        const Mask code = (columns[0] << (4U*k)) | (columns[1] << (2U*k)) | columns[2];
        if (code < best) best = code;
    } while (next_permutation(order, k));
    return best;
}

static Mask covered(Mask mask) {
    Mask result = 0;
    while (mask != 0) {
        const unsigned i = (unsigned)__builtin_ctzll(mask);
        result |= balls[i];
        mask &= mask - 1;
    }
    return result;
}

static int compare_mask(const void *left, const void *right) {
    const Mask a = *(const Mask *)left, b = *(const Mask *)right;
    return (a > b) - (a < b);
}

int main(void) {
    for (unsigned i = 0; i < 64; ++i) {
        words[i][0] = i / 16U; words[i][1] = (i / 4U) % 4U; words[i][2] = i % 4U;
    }
    for (unsigned i = 0; i < 64; ++i) {
        for (unsigned j = 0; j < 64; ++j) {
            unsigned d = 0;
            for (unsigned axis = 0; axis < 3; ++axis) d += words[i][axis] != words[j][axis];
            if (d <= 1) balls[i] |= UINT64_C(1) << j;
        }
    }
    counts[0] = 1;
    for (unsigned k = 1; k <= 7; ++k) {
        Mask codes[CAPACITY];
        for (unsigned p = 0; p < counts[k-1]; ++p) {
            const Mask parent = levels[k-1][p];
            Mask allowed = ~covered(parent);
            while (allowed != 0) {
                const unsigned i = (unsigned)__builtin_ctzll(allowed);
                allowed &= allowed - 1;
                const Mask child = parent | (UINT64_C(1) << i), code = canonical(child);
                unsigned j = 0;
                while (j < counts[k] && codes[j] != code) ++j;
                if (j == counts[k]) {
                    if (j == CAPACITY) { fputs("orbit capacity exceeded\n", stderr); return 1; }
                    codes[j] = code; levels[k][j] = child; ++counts[k];
                }
            }
        }
        qsort(levels[k], counts[k], sizeof(Mask), compare_mask);
        fprintf(stderr, "k=%u orbits=%u\n", k, counts[k]);
    }
    fputs("{\"levels\":[", stdout);
    for (unsigned k = 0; k <= 7; ++k) {
        if (k != 0) putchar(',');
        putchar('[');
        for (unsigned j = 0; j < counts[k]; ++j) {
            if (j != 0) putchar(',');
            printf("%" PRIu64, levels[k][j]);
        }
        putchar(']');
    }
    puts("]}");
    return 0;
}
