#include <array>
#include <cassert>
#include <compare>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace {

constexpr int N = 21;
constexpr uint32_t WORD_MASK = (uint32_t{1} << N) - 1;
constexpr uint32_t TWENTY_BITS = (uint32_t{1} << 20) - 1;

struct G {
    int r = 0;
    int i = 0;
    auto operator<=>(const G&) const = default;
};

G add(G a, G b) { return {a.r + b.r, a.i + b.i}; }
G scale(G a, int k) { return {a.r * k, a.i * k}; }
G mul(G a, G b) { return {a.r * b.r - a.i * b.i, a.r * b.i + a.i * b.r}; }
G conj(G a) { return {a.r, -a.i}; }
G unit(int axis, int sign) {
    G value = axis ? G{0, 1} : G{1, 0};
    return sign ? scale(value, -1) : value;
}
G active(int axis, int sign) { return mul({1, 1}, unit(axis, sign)); }

using Word = std::array<G, N>;

G paf(const Word& word, int shift) {
    G result{};
    for (int position = 0; position < N; ++position) {
        result = add(result, mul(word[position], conj(word[(position + shift) % N])));
    }
    return result;
}

// Twenty independent Z/8 coordinates: real slots 0--9, imaginary slots 10--19.
struct Residue8 {
    uint32_t b0 = 0;
    uint32_t b1 = 0;
    uint32_t b2 = 0;
    auto operator<=>(const Residue8&) const = default;
};

Residue8 residue_add(Residue8 a, Residue8 b) {
    uint32_t c0 = a.b0 & b.b0;
    uint32_t low = a.b0 ^ b.b0;
    uint32_t c1 = (a.b1 & b.b1) | (a.b1 & c0) | (b.b1 & c0);
    uint32_t middle = a.b1 ^ b.b1 ^ c0;
    return {
        low & TWENTY_BITS,
        middle & TWENTY_BITS,
        (a.b2 ^ b.b2 ^ c1) & TWENTY_BITS,
    };
}

Residue8 residue_negate(Residue8 a) {
    return {
        a.b0,
        (a.b1 ^ a.b0) & TWENTY_BITS,
        (a.b2 ^ (a.b1 | a.b0)) & TWENTY_BITS,
    };
}

Residue8 residue_subtract(Residue8 a, Residue8 b) {
    return residue_add(a, residue_negate(b));
}

void set_slot(Residue8& result, int slot, int value) {
    unsigned residue = unsigned(value) & 7;
    uint32_t bit = uint32_t{1} << slot;
    if (residue & 1) result.b0 |= bit;
    if (residue & 2) result.b1 |= bit;
    if (residue & 4) result.b2 |= bit;
}

Residue8 paf_fingerprint(const Word& word) {
    Residue8 result;
    for (int shift = 1; shift <= 10; ++shift) {
        G value = paf(word, shift);
        set_slot(result, shift - 1, value.r);
        set_slot(result, 10 + shift - 1, value.i);
    }
    return result;
}

uint32_t rotate_word(uint32_t word, int shift) {
    return ((word >> shift) | (word << (N - shift))) & WORD_MASK;
}

uint32_t correlation_signature(uint32_t word) {
    uint32_t result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        result |= uint32_t(__builtin_popcount(word & rotate_word(word, shift)) & 1)
                  << (shift - 1);
    }
    return result;
}

std::array<int, 10> theta_values(uint32_t b_word) {
    uint32_t f_word = ((~b_word) & WORD_MASK) & ~uint32_t{1};
    uint32_t b_signature = correlation_signature(b_word);
    uint32_t f_signature = correlation_signature(f_word);
    std::array<int, 10> theta{};
    for (int shift = 1; shift <= 10; ++shift) {
        theta[shift - 1] = 1 ^ int(shift == 4 || shift == 10)
            ^ int((b_signature >> (shift - 1)) & 1)
            ^ int((f_signature >> (shift - 1)) & 1);
    }
    return theta;
}

struct BTarget {
    Residue8 target{};
    Word word{};
};

std::vector<BTarget> b_targets(uint32_t b_word) {
    auto theta = theta_values(b_word);
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) if (((b_word >> shift) & 1) == 0) {
        shifts.push_back(shift);
    }
    assert(shifts.size() == 2);
    std::map<Residue8, Word> unique;
    int exact = 0;
    for (int a0 = 0; a0 < 2; ++a0) for (int p0 = 0; p0 < 2; ++p0)
    for (int m0 = 0; m0 < 2; ++m0) for (int a1 = 0; a1 < 2; ++a1)
    for (int p1 = 0; p1 < 2; ++p1) for (int m1 = 0; m1 < 2; ++m1)
    for (int z = 0; z < 2; ++z) {
        Word word{};
        G sum{};
        std::array<int, 2> axes{a0, a1};
        std::array<int, 2> plus{p0, p1};
        std::array<int, 2> minus{m0, m1};
        for (int j = 0; j < 2; ++j) {
            int shift = shifts[j];
            word[shift] = active(axes[j], plus[j]);
            word[N - shift] = active(axes[j] ^ theta[shift - 1], minus[j]);
            sum = add(sum, add(word[shift], word[N - shift]));
        }
        word[0] = unit(0, z);
        sum = add(sum, word[0]);
        if (sum != G{1, 0}) continue;
        ++exact;
        Residue8 target;
        for (int shift = 1; shift <= 10; ++shift) {
            G value = paf(word, shift);
            set_slot(target, shift - 1, -2 - value.r);
            set_slot(target, 10 + shift - 1, -value.i);
        }
        unique.try_emplace(target, word);
    }
    assert(exact == 20 && unique.size() == 10);
    std::vector<BTarget> result;
    for (auto& [target, word] : unique) result.push_back({target, word});
    return result;
}

Word a_word(const std::vector<int>& positions, uint32_t axes, uint32_t signs) {
    Word word{};
    for (int j = 0; j < 16; ++j) {
        word[positions[j]] = active((axes >> j) & 1, (signs >> j) & 1);
    }
    return word;
}

struct SearchResult {
    bool found = false;
    int axes_examined = 0;
    uint32_t axes = 0;
    uint32_t signs = 0;
    Word b{};
};

SearchResult search(const std::vector<int>& positions, const std::vector<BTarget>& targets) {
    SearchResult result;
    for (uint32_t axes = 0; axes < (uint32_t{1} << 16); ++axes) {
        int n1 = __builtin_popcount(axes);
        if (n1 & 1) continue;
        ++result.axes_examined;
        int n0 = 16 - n1;
        Word baseline_word = a_word(positions, axes, 0);
        Residue8 baseline = paf_fingerprint(baseline_word);
        std::array<Residue8, 16> columns{};
        for (int j = 0; j < 16; ++j) {
            Word changed = baseline_word;
            changed[positions[j]] = scale(changed[positions[j]], -1);
            columns[j] = residue_subtract(paf_fingerprint(changed), baseline);
        }
        uint32_t audit_mask = ((axes + 1) * 0x9e37u) & 0xffffu;
        Residue8 predicted = baseline;
        for (int j = 0; j < 16; ++j) if ((audit_mask >> j) & 1) {
            predicted = residue_add(predicted, columns[j]);
        }
        assert(predicted == paf_fingerprint(a_word(positions, axes, audit_mask)));

        std::array<std::array<std::map<Residue8, uint8_t>, 9>, 9> right;
        for (uint32_t mask = 0; mask < 256; ++mask) {
            int negative0 = 0, negative1 = 0;
            Residue8 residue;
            for (int j = 0; j < 8; ++j) if ((mask >> j) & 1) {
                int index = 8 + j;
                ((axes >> index) & 1 ? negative1 : negative0)++;
                residue = residue_add(residue, columns[index]);
            }
            right[negative0][negative1].try_emplace(residue, uint8_t(mask));
        }
        for (uint32_t left = 0; left < 256; ++left) {
            int negative0 = 0, negative1 = 0;
            Residue8 left_residue;
            for (int j = 0; j < 8; ++j) if ((left >> j) & 1) {
                ((axes >> j) & 1 ? negative1 : negative0)++;
                left_residue = residue_add(left_residue, columns[j]);
            }
            int need0 = n0 / 2 - negative0;
            int need1 = n1 / 2 - negative1;
            if (need0 < 0 || need0 > 8 || need1 < 0 || need1 > 8) continue;
            for (const BTarget& target : targets) {
                Residue8 needed = residue_subtract(
                    residue_subtract(target.target, baseline), left_residue);
                auto found = right[need0][need1].find(needed);
                if (found == right[need0][need1].end()) continue;
                result.found = true;
                result.axes = axes;
                result.signs = left | (uint32_t(found->second) << 8);
                result.b = target.word;
                Word a = a_word(positions, result.axes, result.signs);
                G sum{};
                for (G value : a) sum = add(sum, value);
                assert((sum == G{0, 0}));
                for (int shift = 1; shift <= 10; ++shift) {
                    G residual = add(add(paf(a, shift), paf(result.b, shift)), {2, 0});
                    assert((residual.r & 7) == 0 && (residual.i & 7) == 0);
                }
                return result;
            }
        }
    }
    assert(result.axes_examined == 32768);
    return result;
}

std::vector<int> complement_positions(const std::vector<int>& s_positions) {
    std::set<int> excluded(s_positions.begin(), s_positions.end());
    std::vector<int> result;
    for (int position = 0; position < N; ++position) if (!excluded.contains(position)) {
        result.push_back(position);
    }
    assert(result.size() == 16);
    return result;
}

}  // namespace


int main() {
    uint32_t equal_word = 0;
    for (int position : {2, 6, 15, 19}) equal_word |= uint32_t{1} << position;
    uint32_t b_word = WORD_MASK ^ equal_word ^ uint32_t{1};
    auto targets = b_targets(b_word);
    const std::array<std::vector<int>, 2> s_supports = {
        std::vector<int>{0, 2, 4, 10, 12},
        std::vector<int>{0, 2, 4, 13, 15},
    };
    int survivors = 0;
    for (const auto& support : s_supports) {
        SearchResult result = search(complement_positions(support), targets);
        survivors += int(result.found);
        for (size_t j = 0; j < support.size(); ++j) {
            if (j) std::cout << ',';
            std::cout << support[j];
        }
        std::cout << "\tsixth_h_soluble=" << int(result.found)
                  << "\taxes_examined=" << result.axes_examined << '\n';
    }
    std::cout << "input_orbits=2\nsurviving_orbits=" << survivors
              << "\neliminated_orbits=" << 2 - survivors << "\ncertificate=verified\n";
}
