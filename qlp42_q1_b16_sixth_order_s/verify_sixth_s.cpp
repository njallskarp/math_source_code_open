#include <algorithm>
#include <array>
#include <cassert>
#include <compare>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr int N = 21;
constexpr uint32_t WORD_MASK = (uint32_t{1} << N) - 1;
constexpr uint16_t TEN_BITS = (uint16_t{1} << 10) - 1;

struct G {
    int r = 0;
    int i = 0;
    auto operator<=>(const G&) const = default;
};

G add(G a, G b) { return {a.r + b.r, a.i + b.i}; }
G sub(G a, G b) { return {a.r - b.r, a.i - b.i}; }
G scale(G a, int k) { return {a.r * k, a.i * k}; }
G mul(G a, G b) { return {a.r * b.r - a.i * b.i, a.r * b.i + a.i * b.r}; }
G conj(G a) { return {a.r, -a.i}; }

G div_pi(G a) {
    assert(((a.r + a.i) & 1) == 0);
    assert(((a.i - a.r) & 1) == 0);
    return {(a.r + a.i) / 2, (a.i - a.r) / 2};
}

G unit(int axis, int sign) {
    G result = axis ? G{0, 1} : G{1, 0};
    return sign ? scale(result, -1) : result;
}

G active(int axis, int sign) { return mul({1, 1}, unit(axis, sign)); }

using Word = std::array<G, N>;

G paf(const Word& word, int shift) {
    G result{};
    for (int index = 0; index < N; ++index) {
        result = add(result, mul(word[index], conj(word[(index + shift) % N])));
    }
    return result;
}

G target_s(int shift) {
    if (shift == 4) return {-2, 0};
    if (shift == 10) return {2, 0};
    return {0, 0};
}

// Ten copies of Z[i]/(pi^3) = Z/2 x Z/4.  For each shift, x is real mod 2
// and y is (real+imaginary) mod 4.  y0 and y1 are its bit planes.
struct Residue {
    uint16_t x = 0;
    uint16_t y0 = 0;
    uint16_t y1 = 0;
    auto operator<=>(const Residue&) const = default;
};

Residue residue_add(Residue a, Residue b) {
    uint16_t carry = a.y0 & b.y0;
    return {
        uint16_t((a.x ^ b.x) & TEN_BITS),
        uint16_t((a.y0 ^ b.y0) & TEN_BITS),
        uint16_t((a.y1 ^ b.y1 ^ carry) & TEN_BITS),
    };
}

Residue residue_negate(Residue a) {
    return {a.x, a.y0, uint16_t((a.y1 ^ a.y0) & TEN_BITS)};
}

Residue residue_subtract(Residue a, Residue b) {
    return residue_add(a, residue_negate(b));
}

uint32_t residue_key(Residue value) {
    return uint32_t(value.x) | (uint32_t(value.y0) << 10) | (uint32_t(value.y1) << 20);
}

Residue quotient_fingerprint(const Word& word, const Word& baseline) {
    Residue result;
    for (int shift = 1; shift <= 10; ++shift) {
        G quotient = sub(paf(word, shift), paf(baseline, shift));
        for (int j = 0; j < 3; ++j) quotient = div_pi(quotient);
        uint16_t bit = uint16_t{1} << (shift - 1);
        if (quotient.r & 1) result.x |= bit;
        int sum_mod_four = (quotient.r + quotient.i) & 3;
        if (sum_mod_four & 1) result.y0 |= bit;
        if (sum_mod_four & 2) result.y1 |= bit;
    }
    return result;
}

Residue combined_fingerprint(const Word& a, const Word& b) {
    Residue result;
    for (int shift = 1; shift <= 10; ++shift) {
        G quotient = sub(add(paf(a, shift), paf(b, shift)), target_s(shift));
        for (int j = 0; j < 3; ++j) quotient = div_pi(quotient);
        uint16_t bit = uint16_t{1} << (shift - 1);
        if (quotient.r & 1) result.x |= bit;
        int sum_mod_four = (quotient.r + quotient.i) & 3;
        if (sum_mod_four & 1) result.y0 |= bit;
        if (sum_mod_four & 2) result.y1 |= bit;
    }
    return result;
}

std::vector<int> parse_positions(const std::string& text) {
    std::vector<int> result;
    std::stringstream input(text);
    std::string item;
    while (std::getline(input, item, ',')) result.push_back(std::stoi(item));
    return result;
}

std::vector<std::string> split_tabs(const std::string& line) {
    std::vector<std::string> result;
    std::stringstream input(line);
    std::string item;
    while (std::getline(input, item, '\t')) result.push_back(item);
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

Residue evaluate_quadratic(
    uint32_t mask,
    const std::vector<Residue>& linear,
    const std::vector<std::vector<Residue>>& quadratic) {
    Residue result;
    for (int j = 0; j < int(linear.size()); ++j) if ((mask >> j) & 1) {
        result = residue_add(result, linear[j]);
        for (int k = j + 1; k < int(linear.size()); ++k) if ((mask >> k) & 1) {
            result = residue_add(result, quadratic[j][k]);
        }
    }
    return result;
}

struct BState {
    Residue delta{};
    uint8_t axes = 0;
    uint16_t signs = 0;
    int center_sign = 0;
};

struct BData {
    Word baseline{};
    std::vector<int> shifts;
    std::unordered_map<uint32_t, BState> states;
    long long exact_assignments = 0;
    int direct_checks = 0;
};

BData enumerate_b(uint32_t b_word) {
    BData data;
    auto theta = theta_values(b_word);
    for (int shift = 1; shift <= 10; ++shift) {
        if ((b_word >> shift) & 1) data.shifts.push_back(shift);
    }
    assert(data.shifts.size() == 8);
    for (int shift : data.shifts) {
        data.baseline[shift] = active(0, 0);
        data.baseline[N - shift] = active(theta[shift - 1], 0);
    }
    data.baseline[0] = {0, -1};

    for (uint32_t axes = 0; axes < 256; ++axes) {
        Word word{};
        std::vector<int> sign_positions;
        for (int j = 0; j < 8; ++j) {
            int shift = data.shifts[j];
            int axis = (axes >> j) & 1;
            word[shift] = active(axis, 0);
            word[N - shift] = active(axis ^ theta[shift - 1], 0);
            sign_positions.push_back(shift);
            sign_positions.push_back(N - shift);
        }
        word[0] = {0, -1};
        sign_positions.push_back(0);
        assert(sign_positions.size() == 17);
        Residue axis_delta = quotient_fingerprint(word, data.baseline);

        std::vector<Residue> linear(17);
        std::vector<std::vector<Residue>> quadratic(17, std::vector<Residue>(17));
        for (int j = 0; j < 17; ++j) {
            Word changed = word;
            changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            linear[j] = quotient_fingerprint(changed, word);
            ++data.direct_checks;
        }
        for (int j = 0; j < 17; ++j) for (int k = j + 1; k < 17; ++k) {
            Word changed = word;
            changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            changed[sign_positions[k]] = scale(changed[sign_positions[k]], -1);
            Residue pair = quotient_fingerprint(changed, word);
            quadratic[j][k] = residue_subtract(
                residue_subtract(pair, linear[j]), linear[k]);
            ++data.direct_checks;
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
            assert(quotient_fingerprint(changed, word)
                   == evaluate_quadratic(mask, linear, quadratic));
            ++data.direct_checks;
        }

        G baseline_sum{};
        std::array<G, 17> changes{};
        for (int j = 0; j < 17; ++j) {
            G value = word[sign_positions[j]];
            baseline_sum = add(baseline_sum, value);
            changes[j] = scale(value, -2);
        }
        G required = sub({0, -3}, baseline_sum);

        std::array<G, 256> left_sums{};
        std::array<Residue, 256> left_residues{};
        for (uint32_t mask = 1; mask < 256; ++mask) {
            int j = __builtin_ctz(mask);
            uint32_t rest = mask & (mask - 1);
            left_sums[mask] = add(left_sums[rest], changes[j]);
            Residue value = residue_add(left_residues[rest], linear[j]);
            for (int k = j + 1; k < 8; ++k) if ((rest >> k) & 1) {
                value = residue_add(value, quadratic[j][k]);
            }
            left_residues[mask] = value;
        }

        std::array<G, 512> right_sums{};
        std::array<Residue, 512> right_residues{};
        std::map<G, std::vector<uint16_t>> right_by_sum;
        right_by_sum[G{}].push_back(0);
        for (uint32_t mask = 1; mask < 512; ++mask) {
            int local = __builtin_ctz(mask);
            int j = 8 + local;
            uint32_t rest = mask & (mask - 1);
            right_sums[mask] = add(right_sums[rest], changes[j]);
            Residue value = residue_add(right_residues[rest], linear[j]);
            for (int k = j + 1; k < 17; ++k) if ((rest >> (k - 8)) & 1) {
                value = residue_add(value, quadratic[j][k]);
            }
            right_residues[mask] = value;
            right_by_sum[right_sums[mask]].push_back(uint16_t(mask));
        }

        std::array<std::array<Residue, 512>, 8> cross_columns{};
        for (int j = 0; j < 8; ++j) {
            for (uint32_t mask = 1; mask < 512; ++mask) {
                int local = __builtin_ctz(mask);
                uint32_t rest = mask & (mask - 1);
                cross_columns[j][mask] = residue_add(
                    cross_columns[j][rest], quadratic[j][8 + local]);
            }
        }

        for (uint32_t left = 0; left < 256; ++left) {
            auto found = right_by_sum.find(sub(required, left_sums[left]));
            if (found == right_by_sum.end()) continue;
            for (uint16_t right : found->second) {
                Residue delta = residue_add(
                    axis_delta, residue_add(left_residues[left], right_residues[right]));
                for (int j = 0; j < 8; ++j) if ((left >> j) & 1) {
                    delta = residue_add(delta, cross_columns[j][right]);
                }
                ++data.exact_assignments;
                uint32_t key = residue_key(delta);
                data.states.try_emplace(
                    key, BState{delta, uint8_t(axes), uint16_t(left | (uint32_t(right) << 8)),
                                int((right >> 8) & 1)});
            }
        }
    }
    assert(data.exact_assignments == 804968);
    assert(data.direct_checks == 43264);
    return data;
}

struct Row {
    std::string b_equal;
    std::string a_opposite;
    std::string rank;
};

struct Witness {
    bool found = false;
    int a_real_position = -1;
    BState b{};
};

std::string bit_string(uint32_t value, int count) {
    std::string result;
    for (int j = 0; j < count; ++j) result.push_back(((value >> j) & 1) ? '1' : '0');
    return result;
}

void verify_witness(
    const std::vector<int>& a_positions,
    uint32_t b_word,
    const BData& b_data,
    const Witness& witness) {
    Word a{};
    G a_sum{};
    for (int position : a_positions) {
        int exceptional = position == witness.a_real_position;
        a[position] = active(exceptional ? 0 : 1, exceptional ? 0 : 1);
        a_sum = add(a_sum, a[position]);
    }
    assert((a_sum == G{5, -3}));

    auto theta = theta_values(b_word);
    Word b{};
    G b_sum{};
    for (int j = 0; j < 8; ++j) {
        int shift = b_data.shifts[j];
        int axis = (witness.b.axes >> j) & 1;
        int plus_sign = (witness.b.signs >> (2 * j)) & 1;
        int minus_sign = (witness.b.signs >> (2 * j + 1)) & 1;
        b[shift] = active(axis, plus_sign);
        b[N - shift] = active(axis ^ theta[shift - 1], minus_sign);
        b_sum = add(b_sum, add(b[shift], b[N - shift]));
    }
    b[0] = witness.b.center_sign ? G{0, 1} : G{0, -1};
    b_sum = add(b_sum, b[0]);
    assert((b_sum == G{0, -3}));
    assert(combined_fingerprint(a, b) == Residue{});
}

}  // namespace


int main(int argc, char** argv) {
    bool dump_table = argc == 2 && std::string(argv[1]) == "--dump-table";
    bool dump_witnesses = argc == 2 && std::string(argv[1]) == "--dump-witnesses";
    std::ifstream input("../qlp42_q1_b16_fifth_order_s/orbit_table.tsv");
    assert(input);
    std::string line;
    std::getline(input, line);
    std::vector<Row> rows;
    while (std::getline(input, line)) {
        auto fields = split_tabs(line);
        assert(fields.size() == 5);
        if (fields[4] == "1") rows.push_back({fields[0], fields[1], fields[2]});
    }
    assert(rows.size() == 16);

    if (dump_table) {
        std::cout << "b_equal_positions\ta_opposite_orbit_representative\tfourth_order_rank"
                     "\tb_exact_s_phase_assignments\tb_sixth_residue_fingerprints"
                     "\tsixth_s_soluble\n";
    }
    if (dump_witnesses) {
        std::cout << "b_equal_positions\ta_opposite_orbit_representative\ta_s_real_position"
                     "\tb_s_axes\tb_s_plus_minus_signs\tb_s_center_sign\n";
    }

    std::map<uint32_t, BData> b_cache;
    int soluble = 0;
    int eliminated = 0;
    int witness_checks = 0;
    long long direct_checks = 0;
    std::set<uint32_t> soluble_masks;
    std::set<uint32_t> eliminated_masks;

    for (const Row& row : rows) {
        uint32_t equal_word = 0;
        for (int position : parse_positions(row.b_equal)) equal_word |= uint32_t{1} << position;
        uint32_t b_word = WORD_MASK ^ equal_word ^ uint32_t{1};
        auto [iterator, inserted] = b_cache.try_emplace(b_word);
        if (inserted) {
            iterator->second = enumerate_b(b_word);
            direct_checks += iterator->second.direct_checks;
        }
        const BData& b_data = iterator->second;

        std::vector<int> a_positions = parse_positions(row.a_opposite);
        assert(a_positions.size() == 5);
        Word a_baseline{};
        for (int position : a_positions) a_baseline[position] = active(0, 0);
        Residue combined_baseline = combined_fingerprint(a_baseline, b_data.baseline);
        Witness witness;
        for (int real_position : a_positions) {
            Word a{};
            for (int position : a_positions) {
                int exceptional = position == real_position;
                a[position] = active(exceptional ? 0 : 1, exceptional ? 0 : 1);
            }
            Residue a_delta = quotient_fingerprint(a, a_baseline);
            Residue required_b = residue_negate(residue_add(combined_baseline, a_delta));
            auto found = b_data.states.find(residue_key(required_b));
            if (found != b_data.states.end()) {
                witness = {true, real_position, found->second};
                break;
            }
        }
        if (witness.found) {
            ++soluble;
            soluble_masks.insert(b_word);
            verify_witness(a_positions, b_word, b_data, witness);
            ++witness_checks;
        } else {
            ++eliminated;
            eliminated_masks.insert(b_word);
        }

        if (dump_table) {
            std::cout << row.b_equal << '\t' << row.a_opposite << '\t' << row.rank << '\t'
                << b_data.exact_assignments << '\t' << b_data.states.size() << '\t'
                << int(witness.found) << '\n';
        }
        if (dump_witnesses && witness.found) {
            std::cout << row.b_equal << '\t' << row.a_opposite << '\t'
                << witness.a_real_position << '\t' << bit_string(witness.b.axes, 8) << '\t'
                << bit_string(witness.b.signs, 16) << '\t' << witness.b.center_sign << '\n';
        }
    }

    if (dump_table || dump_witnesses) return 0;
    std::cout
        << "input_fifth_s_a_rotation_orbits=" << rows.size() << '\n'
        << "input_fifth_s_b_masks=" << b_cache.size() << '\n'
        << "exact_b_s_phase_assignments_per_mask=804968\n"
        << "direct_quadratic_interpolation_and_audit_checks=" << direct_checks << '\n'
        << "direct_full_witness_checks=" << witness_checks << '\n'
        << "sixth_s_surviving_a_rotation_orbits=" << soluble << '\n'
        << "sixth_s_surviving_labeled_pairs=" << 21 * soluble << '\n'
        << "sixth_s_surviving_b_masks=" << soluble_masks.size() << '\n'
        << "sixth_s_eliminated_a_rotation_orbits=" << eliminated << '\n'
        << "sixth_s_eliminated_labeled_pairs=" << 21 * eliminated << '\n'
        << "sixth_s_eliminated_b_masks=" << eliminated_masks.size() << '\n'
        << "certificate=verified\n";
}
