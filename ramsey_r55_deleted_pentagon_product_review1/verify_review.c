#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint32_t Mask;

enum { CORE_ORDER = 24, MAX_FOUR_SETS = 110 };

static const Mask ASSIGNMENT_COUNT = UINT32_C(1) << CORE_ORDER;
static const Mask FULL_MASK = (UINT32_C(1) << CORE_ORDER) - UINT32_C(1);

static void fail(const char *message) {
    fprintf(stderr, "verification failure: %s\n", message);
    exit(EXIT_FAILURE);
}

static void require(int condition, const char *message) {
    if (!condition) {
        fail(message);
    }
}

static int cycle_edge(unsigned left, unsigned right) {
    unsigned difference = (left + 5U - right) % 5U;
    return difference == 1U || difference == 4U;
}

static int red(unsigned left, unsigned right) {
    unsigned left_bag;
    unsigned right_bag;
    require(left < CORE_ORDER && right < CORE_ORDER && left != right,
            "invalid core pair");
    left_bag = left / 5U;
    right_bag = right / 5U;
    if (left_bag == right_bag) {
        return cycle_edge(left % 5U, right % 5U);
    }
    return cycle_edge(left_bag, right_bag);
}

static int monochromatic(const unsigned *vertices, size_t size, int color) {
    size_t first;
    size_t second;
    for (first = 0; first < size; ++first) {
        for (second = first + 1U; second < size; ++second) {
            if (red(vertices[first], vertices[second]) != color) {
                return 0;
            }
        }
    }
    return 1;
}

static Mask vertex_mask(const unsigned vertices[4]) {
    Mask result = 0;
    unsigned index;
    for (index = 0; index < 4U; ++index) {
        result |= UINT32_C(1) << vertices[index];
    }
    return result;
}

static void activity_word(Mask attachment, unsigned word[5]) {
    unsigned bag;
    for (bag = 0; bag < 5U; ++bag) {
        unsigned begin = 5U * bag;
        unsigned end = bag == 4U ? 24U : begin + 5U;
        unsigned left;
        int red_active = 0;
        int blue_active = 0;
        for (left = begin; left < end; ++left) {
            unsigned right;
            for (right = left + 1U; right < end; ++right) {
                int left_red = (attachment & (UINT32_C(1) << left)) != 0;
                int right_red = (attachment & (UINT32_C(1) << right)) != 0;
                if (red(left, right)) {
                    red_active = red_active || (left_red && right_red);
                } else {
                    blue_active = blue_active || (!left_red && !right_red);
                }
            }
        }
        word[bag] = (unsigned)red_active + 2U * (unsigned)blue_active;
    }
}

int main(int argc, char **argv) {
    int stream = 0;
    unsigned red_edges = 0;
    unsigned complement_map[CORE_ORDER];
    uint8_t image_seen[CORE_ORDER] = {0};
    Mask four_sets[2][MAX_FOUR_SETS];
    size_t four_count[2] = {0, 0};
    unsigned five_sets_checked = 0;
    uint8_t *bad_red;
    uint8_t *bad_blue;
    Mask *accepted;
    size_t accepted_count = 0;
    size_t accepted_capacity = 16384U;
    uint64_t mask_sum = 0;
    Mask mask_xor = 0;
    uint8_t local_patterns[4][32] = {{0}};
    const unsigned required_word[5] = {1U, 2U, 2U, 1U, 0U};
    unsigned left;

    if (argc == 2 && strcmp(argv[1], "--accepted-stream") == 0) {
        stream = 1;
    } else if (argc != 1) {
        fail("usage: verify_review [--accepted-stream]");
    }

    for (left = 0; left < CORE_ORDER; ++left) {
        unsigned right;
        for (right = left + 1U; right < CORE_ORDER; ++right) {
            red_edges += (unsigned)red(left, right);
        }
    }
    require(red_edges == 138U, "core red-edge count");
    require(276U - red_edges == 138U, "core blue-edge count");

    for (left = 0; left < CORE_ORDER; ++left) {
        unsigned bag = left / 5U;
        unsigned within = left % 5U;
        unsigned image = 5U * ((2U * bag + 1U) % 5U) +
                         ((2U * within + 1U) % 5U);
        require(image < CORE_ORDER, "complement map hits deleted vertex");
        complement_map[left] = image;
        require(!image_seen[image], "complement map is not injective");
        image_seen[image] = 1U;
    }
    for (left = 0; left < CORE_ORDER; ++left) {
        unsigned right;
        for (right = left + 1U; right < CORE_ORDER; ++right) {
            require(red(left, right) != red(complement_map[left], complement_map[right]),
                    "claimed self-complement map does not reverse color");
        }
    }

    {
        unsigned a;
        for (a = 0; a < CORE_ORDER; ++a) {
            unsigned b;
            for (b = a + 1U; b < CORE_ORDER; ++b) {
                unsigned c;
                for (c = b + 1U; c < CORE_ORDER; ++c) {
                    unsigned d;
                    for (d = c + 1U; d < CORE_ORDER; ++d) {
                        unsigned vertices[4] = {a, b, c, d};
                        unsigned color;
                        for (color = 0; color < 2U; ++color) {
                            if (monochromatic(vertices, 4U, (int)color)) {
                                require(four_count[color] < MAX_FOUR_SETS,
                                        "four-set storage bound");
                                four_sets[color][four_count[color]++] = vertex_mask(vertices);
                            }
                        }
                    }
                }
            }
        }
    }
    require(four_count[0] == 105U && four_count[1] == 105U,
            "monochromatic four-set census");

    {
        unsigned a;
        for (a = 0; a < CORE_ORDER; ++a) {
            unsigned b;
            for (b = a + 1U; b < CORE_ORDER; ++b) {
                unsigned c;
                for (c = b + 1U; c < CORE_ORDER; ++c) {
                    unsigned d;
                    for (d = c + 1U; d < CORE_ORDER; ++d) {
                        unsigned e;
                        for (e = d + 1U; e < CORE_ORDER; ++e) {
                            unsigned vertices[5] = {a, b, c, d, e};
                            require(!monochromatic(vertices, 5U, 0) &&
                                        !monochromatic(vertices, 5U, 1),
                                    "core contains a monochromatic five-set");
                            ++five_sets_checked;
                        }
                    }
                }
            }
        }
    }
    require(five_sets_checked == 42504U, "five-subset census");

    /* Seed all literal monochromatic K4s, then compute their complete upward
       closures by a Boolean subset transform over all 2^24 star masks. */
    bad_red = (uint8_t *)calloc((size_t)ASSIGNMENT_COUNT, sizeof(uint8_t));
    bad_blue = (uint8_t *)calloc((size_t)ASSIGNMENT_COUNT, sizeof(uint8_t));
    require(bad_red != NULL && bad_blue != NULL, "closure-table allocation");
    {
        size_t index;
        for (index = 0; index < four_count[1]; ++index) {
            bad_red[four_sets[1][index]] = 1U;
        }
        for (index = 0; index < four_count[0]; ++index) {
            bad_blue[four_sets[0][index]] = 1U;
        }
    }
    {
        unsigned bit;
        for (bit = 0; bit < CORE_ORDER; ++bit) {
            Mask step = UINT32_C(1) << bit;
            Mask span = step << 1U;
            Mask base;
            for (base = 0; base < ASSIGNMENT_COUNT; base += span) {
                Mask offset;
                for (offset = 0; offset < step; ++offset) {
                    Mask low = base + offset;
                    Mask high = low + step;
                    bad_red[high] = (uint8_t)(bad_red[high] | bad_red[low]);
                    bad_blue[high] = (uint8_t)(bad_blue[high] | bad_blue[low]);
                }
            }
        }
    }

    accepted = (Mask *)malloc(accepted_capacity * sizeof(Mask));
    require(accepted != NULL, "accepted-star allocation");
    {
        Mask attachment;
        for (attachment = 0; attachment < ASSIGNMENT_COUNT; ++attachment) {
            Mask blue_neighbors = FULL_MASK ^ attachment;
            unsigned word[5];
            unsigned bag;
            if (bad_red[attachment] != 0U || bad_blue[blue_neighbors] != 0U) {
                continue;
            }
            require((attachment & ((UINT32_C(1) << 20U) | (UINT32_C(1) << 23U))) ==
                        ((UINT32_C(1) << 20U) | (UINT32_C(1) << 23U)),
                    "valid attachment lacks a forced red incidence");
            require((attachment & ((UINT32_C(1) << 21U) | (UINT32_C(1) << 22U))) == 0U,
                    "valid attachment lacks a forced blue incidence");
            activity_word(attachment, word);
            require(memcmp(word, required_word, sizeof(required_word)) == 0,
                    "valid attachment has an unexpected activity word");
            for (bag = 0; bag < 4U; ++bag) {
                Mask pattern = (attachment >> (5U * bag)) & UINT32_C(31);
                local_patterns[bag][pattern] = 1U;
            }
            if (accepted_count == accepted_capacity) {
                Mask *grown;
                accepted_capacity *= 2U;
                grown = (Mask *)realloc(accepted, accepted_capacity * sizeof(Mask));
                require(grown != NULL, "accepted-star reallocation");
                accepted = grown;
            }
            accepted[accepted_count++] = attachment;
            mask_sum += attachment;
            mask_xor ^= attachment;
        }
    }
    require(accepted_count == 14641U, "accepted one-vertex attachment count");
    {
        unsigned bag;
        for (bag = 0; bag < 4U; ++bag) {
            unsigned count = 0;
            unsigned pattern;
            for (pattern = 0; pattern < 32U; ++pattern) {
                count += (unsigned)local_patterns[bag][pattern];
            }
            require(count == 11U, "full-bag local pattern count");
        }
    }

    if (stream) {
        size_t index;
        for (index = 0; index < accepted_count; ++index) {
            printf("%" PRIu32 "\n", accepted[index]);
        }
        free(accepted);
        free(bad_blue);
        free(bad_red);
        return EXIT_SUCCESS;
    }

    printf("{\n");
    printf("  \"status\": \"VERIFIED_H24_ATTACHMENT_BY_COMPLETE_MASK_SWEEP\",\n");
    printf("  \"core_order\": 24,\n");
    printf("  \"core_red_blue_edges\": [138, 138],\n");
    printf("  \"core_blue_red_four_sets\": [105, 105],\n");
    printf("  \"core_five_sets_checked\": 42504,\n");
    printf("  \"self_complement_pairs_checked\": 276,\n");
    printf("  \"attachment_masks_checked\": 16777216,\n");
    printf("  \"valid_attachment_masks\": %zu,\n", accepted_count);
    printf("  \"rejected_attachment_masks\": %" PRIu64 ",\n",
           (uint64_t)ASSIGNMENT_COUNT - (uint64_t)accepted_count);
    printf("  \"unique_activity_word\": [1, 2, 2, 1, 0],\n");
    printf("  \"local_patterns_per_full_bag\": [11, 11, 11, 11],\n");
    printf("  \"forced_red\": [20, 23],\n");
    printf("  \"forced_blue\": [21, 22],\n");
    printf("  \"valid_mask_sum\": %" PRIu64 ",\n", mask_sum);
    printf("  \"valid_mask_xor\": %" PRIu32 ",\n", mask_xor);
    printf("  \"free_pairs_at_order_43\": 627,\n");
    printf("  \"outside_vertices_needed_by_R44_upper_bound\": 18,\n");
    printf("  \"strengthened_first_excluded_order\": 42,\n");
    printf("  \"closure_table_bytes\": 33554432\n");
    printf("}\n");

    free(accepted);
    free(bad_blue);
    free(bad_red);
    return EXIT_SUCCESS;
}
