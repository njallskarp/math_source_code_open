#define main embedded_sixth_h_main
#include "prototype_sixth_h.cpp"
#undef main

#include <unordered_set>

namespace {

struct Residue7 {
    std::array<uint8_t, 10> x{};
    std::array<uint8_t, 10> y{};
    bool operator==(const Residue7&) const = default;
};

struct Residue7Hash {
    size_t operator()(const Residue7& value) const {
        size_t result = 0xcbf29ce484222325ULL;
        for (int shift = 0; shift < 10; ++shift) {
            result ^= value.x[shift] | (value.y[shift] << 3);
            result *= 0x100000001b3ULL;
        }
        return result;
    }
};

Residue7 r7_add(Residue7 a, const Residue7& b) {
    for (int shift = 0; shift < 10; ++shift) {
        a.x[shift] = (a.x[shift] + b.x[shift]) & 7;
        a.y[shift] = (a.y[shift] + b.y[shift]) & 15;
    }
    return a;
}

Residue7 r7_negate(Residue7 a) {
    for (int shift = 0; shift < 10; ++shift) {
        a.x[shift] = (-a.x[shift]) & 7;
        a.y[shift] = (-a.y[shift]) & 15;
    }
    return a;
}

Residue7 r7_subtract(Residue7 a, const Residue7& b) {
    return r7_add(a, r7_negate(b));
}

Residue7 r7_paf(const Word& word) {
    Residue7 result;
    for (int shift = 1; shift <= 10; ++shift) {
        G value = paf(word, shift);
        result.x[shift - 1] = value.r & 7;
        result.y[shift - 1] = (value.r + value.i) & 15;
    }
    return result;
}

Residue7 r7_difference(const Word& word, const Word& baseline) {
    return r7_subtract(r7_paf(word), r7_paf(baseline));
}

Residue7 evaluate_r7(
    uint32_t mask,
    const std::vector<Residue7>& linear,
    const std::vector<std::vector<Residue7>>& quadratic) {
    Residue7 result;
    for (int j = 0; j < int(linear.size()); ++j) if ((mask >> j) & 1) {
        result = r7_add(result, linear[j]);
        for (int k = j + 1; k < int(linear.size()); ++k) if ((mask >> k) & 1) {
            result = r7_add(result, quadratic[j][k]);
        }
    }
    return result;
}

std::unordered_set<Residue7, Residue7Hash> enumerate_case1_b(uint32_t b_word) {
    auto theta = theta_values(b_word);
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) if ((b_word >> shift) & 1) {
        shifts.push_back(shift);
    }
    assert(shifts.size() == 8);
    std::unordered_set<Residue7, Residue7Hash> reachable;
    long long exact = 0;
    int direct_checks = 0;
    for (uint32_t axes = 0; axes < 256; ++axes) {
        Word word{};
        std::vector<int> sign_positions;
        for (int j = 0; j < 8; ++j) {
            int shift = shifts[j];
            int axis = (axes >> j) & 1;
            word[shift] = active(axis, 0);
            word[N - shift] = active(axis ^ theta[shift - 1], 0);
            sign_positions.push_back(shift);
            sign_positions.push_back(N - shift);
        }
        word[0] = {0, -1};
        sign_positions.push_back(0);
        Residue7 axis_value = r7_paf(word);
        std::vector<Residue7> linear(17);
        std::vector<std::vector<Residue7>> quadratic(17, std::vector<Residue7>(17));
        for (int j = 0; j < 17; ++j) {
            Word changed = word;
            changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            linear[j] = r7_difference(changed, word);
            ++direct_checks;
        }
        for (int j = 0; j < 17; ++j) for (int k = j + 1; k < 17; ++k) {
            Word changed = word;
            changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            changed[sign_positions[k]] = scale(changed[sign_positions[k]], -1);
            quadratic[j][k] = r7_subtract(
                r7_subtract(r7_difference(changed, word), linear[j]), linear[k]);
            ++direct_checks;
        }
        const std::array<uint32_t, 16> audits = {
            0x1ffffu, 0x15555u, 0x0aaaau, 0x00ff0u,
            0x1f00fu, 0x13333u, 0x0ccccu, 0x13579u,
            0x0468au, 0x000ffu, 0x1ff00u, 0x05555u,
            0x0aaaau, 0x12481u, 0x08421u, 0x069c3u,
        };
        for (uint32_t mask : audits) {
            Word changed = word;
            for (int j = 0; j < 17; ++j) if ((mask >> j) & 1) {
                changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            }
            assert(r7_difference(changed, word) == evaluate_r7(mask, linear, quadratic));
            ++direct_checks;
        }

        G baseline_sum{};
        std::array<G, 17> changes{};
        for (int j = 0; j < 17; ++j) {
            G value = word[sign_positions[j]];
            baseline_sum = add(baseline_sum, value);
            changes[j] = scale(value, -2);
        }
        G required{4 - baseline_sum.r, -3 - baseline_sum.i};
        std::array<G, 256> left_sums{};
        std::array<Residue7, 256> left_residues{};
        for (uint32_t mask = 1; mask < 256; ++mask) {
            int j = __builtin_ctz(mask);
            uint32_t rest = mask & (mask - 1);
            left_sums[mask] = add(left_sums[rest], changes[j]);
            Residue7 value = r7_add(left_residues[rest], linear[j]);
            for (int k = j + 1; k < 8; ++k) if ((rest >> k) & 1) {
                value = r7_add(value, quadratic[j][k]);
            }
            left_residues[mask] = value;
        }
        std::array<G, 512> right_sums{};
        std::array<Residue7, 512> right_residues{};
        std::map<G, std::vector<uint16_t>> right_by_sum;
        right_by_sum[G{}].push_back(0);
        for (uint32_t mask = 1; mask < 512; ++mask) {
            int local = __builtin_ctz(mask);
            int j = 8 + local;
            uint32_t rest = mask & (mask - 1);
            right_sums[mask] = add(right_sums[rest], changes[j]);
            Residue7 value = r7_add(right_residues[rest], linear[j]);
            for (int k = j + 1; k < 17; ++k) if ((rest >> (k - 8)) & 1) {
                value = r7_add(value, quadratic[j][k]);
            }
            right_residues[mask] = value;
            right_by_sum[right_sums[mask]].push_back(uint16_t(mask));
        }
        std::array<std::array<Residue7, 512>, 8> cross_columns{};
        for (int j = 0; j < 8; ++j) for (uint32_t mask = 1; mask < 512; ++mask) {
            int local = __builtin_ctz(mask);
            uint32_t rest = mask & (mask - 1);
            cross_columns[j][mask] = r7_add(
                cross_columns[j][rest], quadratic[j][8 + local]);
        }
        for (uint32_t left = 0; left < 256; ++left) {
            auto found = right_by_sum.find(G{required.r - left_sums[left].r,
                                              required.i - left_sums[left].i});
            if (found == right_by_sum.end()) continue;
            for (uint16_t right : found->second) {
                Residue7 value = r7_add(
                    axis_value, r7_add(left_residues[left], right_residues[right]));
                for (int j = 0; j < 8; ++j) if ((left >> j) & 1) {
                    value = r7_add(value, cross_columns[j][right]);
                }
                ++exact;
                reachable.insert(value);
            }
        }
    }
    assert(exact == 500992);
    assert(direct_checks == 43264);
    assert(reachable.size() == 500740);
    return reachable;
}

std::vector<Word> case1_a_words(const std::vector<int>& positions) {
    std::vector<Word> result;
    for (int code = 0; code < 1024; ++code) {
        int value = code;
        Word word{};
        G sum{};
        for (int j = 0; j < 5; ++j) {
            int root = value & 3;
            value >>= 2;
            word[positions[j]] = active(root >> 1, root & 1);
            sum = add(sum, word[positions[j]]);
        }
        if (sum == G{3, -3}) result.push_back(word);
    }
    assert(result.size() == 25);
    return result;
}

Residue7 needed_b(const Word& a) {
    Residue7 result;
    for (int shift = 1; shift <= 10; ++shift) {
        G value = paf(a, shift);
        G target = shift == 4 ? G{-2, 0} : (shift == 10 ? G{2, 0} : G{0, 0});
        int real = target.r - value.r;
        int imag = target.i - value.i;
        result.x[shift - 1] = real & 7;
        result.y[shift - 1] = (real + imag) & 15;
    }
    return result;
}

}  // namespace


int main() {
    uint32_t equal_word = 0;
    for (int position : {2, 6, 15, 19}) equal_word |= uint32_t{1} << position;
    uint32_t b_word = WORD_MASK ^ equal_word ^ uint32_t{1};
    auto reachable = enumerate_case1_b(b_word);
    const std::array<std::vector<int>, 2> supports = {
        std::vector<int>{0, 2, 4, 10, 12},
        std::vector<int>{0, 2, 4, 13, 15},
    };
    int survivors = 0;
    for (const auto& support : supports) {
        bool feasible = false;
        for (const Word& a : case1_a_words(support)) {
            if (reachable.contains(needed_b(a))) {
                feasible = true;
                break;
            }
        }
        survivors += int(feasible);
        std::cout << "a_support=";
        for (size_t j = 0; j < support.size(); ++j) {
            if (j) std::cout << ',';
            std::cout << support[j];
        }
        std::cout << " seventh_s_soluble=" << int(feasible) << '\n';
    }
    assert(survivors == 0);
    std::cout << "exact_b_assignments=500992\n"
              << "seventh_b_residue_fingerprints=" << reachable.size() << '\n'
              << "surviving_orbits=0\ncertificate=verified\n";
}
