#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int N = 21;
constexpr uint32_t WORD_MASK = (uint32_t{1} << N) - 1;

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
    G value = axis == 0 ? G{1, 0} : G{0, 1};
    return sign ? scale(value, -1) : value;
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

uint32_t delta_bits(const Word& word, const Word& baseline) {
    uint32_t result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        G value = sub(paf(word, shift), paf(baseline, shift));
        for (int j = 0; j < 3; ++j) value = div_pi(value);
        result |= uint32_t(value.r & 1) << (shift - 1);
        result |= uint32_t(value.i & 1) << (10 + shift - 1);
    }
    return result;
}

uint32_t residual_bits(const Word& a, const Word& b) {
    uint32_t result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        G value = sub(add(paf(a, shift), paf(b, shift)), {-2, 0});
        for (int j = 0; j < 3; ++j) value = div_pi(value);
        result |= uint32_t(value.r & 1) << (shift - 1);
        result |= uint32_t(value.i & 1) << (10 + shift - 1);
    }
    return result;
}

std::vector<int> parse_positions(const std::string& text) {
    std::vector<int> result;
    std::stringstream stream(text);
    std::string item;
    while (std::getline(stream, item, ',')) result.push_back(std::stoi(item));
    return result;
}

std::vector<std::string> split_tabs(const std::string& line) {
    std::vector<std::string> result;
    std::stringstream stream(line);
    std::string item;
    while (std::getline(stream, item, '\t')) result.push_back(item);
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

int verify_local_formulas() {
    int checks = 0;
    G diagonal_baseline = scale(mul(unit(0, 0), conj(unit(0, 0))), 2);
    for (int a = 0; a < 2; ++a) for (int b = 0; b < 2; ++b)
    for (int s = 0; s < 2; ++s) for (int t = 0; t < 2; ++t) {
        G value = scale(mul(unit(a, s), conj(unit(b, t))), 2);
        G quotient = sub(value, diagonal_baseline);
        for (int j = 0; j < 3; ++j) quotient = div_pi(quotient);
        int product = a & b;
        assert((quotient.r & 1) == (a ^ product ^ s ^ t));
        assert((quotient.i & 1) == (b ^ product ^ s ^ t));
        ++checks;
    }
    for (int center_axis = 0; center_axis < 2; ++center_axis)
    for (int theta = 0; theta < 2; ++theta) {
        G center_baseline = add(
            mul(unit(center_axis, 0), conj(active(0, 0))),
            mul(active(theta, 0), conj(unit(center_axis, 0))));
        for (int a = 0; a < 2; ++a) for (int p = 0; p < 2; ++p)
        for (int m = 0; m < 2; ++m) for (int z = 0; z < 2; ++z) {
            G value = add(
                mul(unit(center_axis, z), conj(active(a, p))),
                mul(active(a ^ theta, m), conj(unit(center_axis, z))));
            G quotient = sub(value, center_baseline);
            for (int j = 0; j < 3; ++j) quotient = div_pi(quotient);
            int common = a ^ (a & p) ^ (a & m) ^ z ^ (a & center_axis)
                ^ (p & center_axis) ^ (m & center_axis) ^ (a & theta)
                ^ (m & theta) ^ (z & theta);
            assert((quotient.r & 1) == (common ^ p));
            assert((quotient.i & 1) == (common ^ m));
            ++checks;
        }
    }
    assert(checks == 80);
    return checks;
}

struct BState {
    uint32_t delta = 0;
    std::array<int, 2> axes{};
    std::array<int, 2> plus_signs{};
    std::array<int, 2> minus_signs{};
    int center_sign = 0;
};

struct BData {
    Word baseline{};
    std::vector<int> shifts;
    std::vector<BState> states;
    int exact_assignments = 0;
};

BData enumerate_b(uint32_t b_word) {
    BData data;
    auto theta = theta_values(b_word);
    for (int shift = 1; shift <= 10; ++shift) {
        if (((b_word >> shift) & 1) == 0) data.shifts.push_back(shift);
    }
    assert(data.shifts.size() == 2);
    for (int shift : data.shifts) {
        data.baseline[shift] = active(0, 0);
        data.baseline[N - shift] = active(theta[shift - 1], 0);
    }
    data.baseline[0] = {1, 0};

    std::map<uint32_t, BState> unique;
    for (int a0 = 0; a0 < 2; ++a0) for (int p0 = 0; p0 < 2; ++p0)
    for (int m0 = 0; m0 < 2; ++m0) for (int a1 = 0; a1 < 2; ++a1)
    for (int p1 = 0; p1 < 2; ++p1) for (int m1 = 0; m1 < 2; ++m1)
    for (int z = 0; z < 2; ++z) {
        BState state;
        state.axes = {a0, a1};
        state.plus_signs = {p0, p1};
        state.minus_signs = {m0, m1};
        state.center_sign = z;
        Word word{};
        G sum{};
        for (int j = 0; j < 2; ++j) {
            int shift = data.shifts[j];
            G plus = active(state.axes[j], state.plus_signs[j]);
            G minus = active(state.axes[j] ^ theta[shift - 1], state.minus_signs[j]);
            word[shift] = plus;
            word[N - shift] = minus;
            sum = add(sum, add(plus, minus));
        }
        word[0] = unit(0, z);
        sum = add(sum, word[0]);
        if (sum == G{1, 0}) {
            ++data.exact_assignments;
            state.delta = delta_bits(word, data.baseline);
            unique.try_emplace(state.delta, state);
        }
    }
    for (auto& [_, state] : unique) data.states.push_back(state);
    assert(data.exact_assignments > 0 && !data.states.empty());
    return data;
}

struct Polynomial {
    std::array<uint32_t, 32> linear{};
    std::array<std::array<uint32_t, 32>, 32> quadratic{};
    int direct_checks = 0;
};

Word build_a(const std::vector<int>& positions, uint32_t axes, uint32_t signs) {
    Word word{};
    for (int j = 0; j < 16; ++j) {
        word[positions[j]] = active((axes >> j) & 1, (signs >> j) & 1);
    }
    return word;
}

uint32_t polynomial_value(const Polynomial& polynomial, uint32_t variables) {
    uint32_t result = 0;
    for (int j = 0; j < 32; ++j) if ((variables >> j) & 1) {
        result ^= polynomial.linear[j];
        for (int k = j + 1; k < 32; ++k) if ((variables >> k) & 1) {
            result ^= polynomial.quadratic[j][k];
        }
    }
    return result;
}

Polynomial interpolate_polynomial(const std::vector<int>& positions, const Word& baseline) {
    Polynomial polynomial;
    for (int j = 0; j < 32; ++j) {
        uint32_t variables = uint32_t{1} << j;
        polynomial.linear[j] = delta_bits(
            build_a(positions, variables & 0xffffu, variables >> 16), baseline);
        ++polynomial.direct_checks;
    }
    for (int j = 0; j < 32; ++j) for (int k = j + 1; k < 32; ++k) {
        uint32_t variables = (uint32_t{1} << j) | (uint32_t{1} << k);
        uint32_t value = delta_bits(
            build_a(positions, variables & 0xffffu, variables >> 16), baseline);
        polynomial.quadratic[j][k] = value ^ polynomial.linear[j] ^ polynomial.linear[k];
        ++polynomial.direct_checks;
    }
    for (int j = 16; j < 32; ++j) for (int k = j + 1; k < 32; ++k) {
        assert(polynomial.quadratic[j][k] == 0);
    }
    const std::array<uint32_t, 16> audits = {
        0xffffffffu, 0xaaaaaaaau, 0x55555555u, 0x0f0f0f0fu,
        0xf0f0f0f0u, 0x3333ccccu, 0xcccc3333u, 0x13579bdfu,
        0x2468ace0u, 0x0000ffffu, 0xffff0000u, 0x00ff00ffu,
        0xff00ff00u, 0x12481248u, 0x84218421u, 0x69c3a5f0u,
    };
    for (uint32_t variables : audits) {
        uint32_t direct = delta_bits(
            build_a(positions, variables & 0xffffu, variables >> 16), baseline);
        assert(direct == polynomial_value(polynomial, variables));
        ++polynomial.direct_checks;
    }
    assert(polynomial.direct_checks == 544);
    return polynomial;
}

struct Witness {
    bool found = false;
    uint32_t a_axes = 0;
    uint32_t a_signs = 0;
    BState b;
    int axes_examined = 0;
};

Witness search_a(
    const Polynomial& polynomial,
    uint32_t combined_baseline,
    const BData& b_data) {
    Witness witness;
    for (uint32_t axes = 0; axes < (uint32_t{1} << 16); ++axes) {
        int n1 = __builtin_popcount(axes);
        if (n1 & 1) continue;
        ++witness.axes_examined;
        int n0 = 16 - n1;
        uint32_t axis_delta = 0;
        std::array<uint32_t, 16> columns{};
        for (int j = 0; j < 16; ++j) if ((axes >> j) & 1) {
            axis_delta ^= polynomial.linear[j];
            for (int k = j + 1; k < 16; ++k) if ((axes >> k) & 1) {
                axis_delta ^= polynomial.quadratic[j][k];
            }
        }
        for (int j = 0; j < 16; ++j) {
            columns[j] = polynomial.linear[16 + j];
            for (int k = 0; k < 16; ++k) if ((axes >> k) & 1) {
                int lo = std::min(k, 16 + j);
                int hi = std::max(k, 16 + j);
                columns[j] ^= polynomial.quadratic[lo][hi];
            }
        }

        std::array<std::array<std::unordered_set<uint32_t>, 9>, 9> right;
        std::array<std::array<std::map<uint32_t, uint8_t>, 9>, 9> right_witness;
        for (uint32_t mask = 0; mask < 256; ++mask) {
            int negative0 = 0, negative1 = 0;
            uint32_t residue = 0;
            for (int j = 0; j < 8; ++j) if ((mask >> j) & 1) {
                int index = 8 + j;
                ((axes >> index) & 1 ? negative1 : negative0)++;
                residue ^= columns[index];
            }
            right[negative0][negative1].insert(residue);
            right_witness[negative0][negative1].try_emplace(residue, uint8_t(mask));
        }

        for (uint32_t left_mask = 0; left_mask < 256; ++left_mask) {
            int negative0 = 0, negative1 = 0;
            uint32_t left_residue = 0;
            for (int j = 0; j < 8; ++j) if ((left_mask >> j) & 1) {
                ((axes >> j) & 1 ? negative1 : negative0)++;
                left_residue ^= columns[j];
            }
            int need0 = n0 / 2 - negative0;
            int need1 = n1 / 2 - negative1;
            if (need0 < 0 || need0 > 8 || need1 < 0 || need1 > 8) continue;
            for (const BState& b_state : b_data.states) {
                uint32_t target = combined_baseline ^ axis_delta ^ b_state.delta;
                uint32_t needed_right = target ^ left_residue;
                auto found = right_witness[need0][need1].find(needed_right);
                if (found == right_witness[need0][need1].end()) continue;
                witness.found = true;
                witness.a_axes = axes;
                witness.a_signs = left_mask | (uint32_t(found->second) << 8);
                witness.b = b_state;
                return witness;
            }
        }
    }
    assert(witness.axes_examined == 32768);
    return witness;
}

void verify_witness(
    const std::vector<int>& positions,
    uint32_t b_word,
    const BData& b_data,
    const Witness& witness) {
    assert(witness.found);
    Word a = build_a(positions, witness.a_axes, witness.a_signs);
    G a_sum{};
    for (G value : a) a_sum = add(a_sum, value);
    assert((a_sum == G{0, 0}));

    auto theta = theta_values(b_word);
    Word b{};
    G b_sum{};
    for (int j = 0; j < 2; ++j) {
        int shift = b_data.shifts[j];
        b[shift] = active(witness.b.axes[j], witness.b.plus_signs[j]);
        b[N - shift] = active(
            witness.b.axes[j] ^ theta[shift - 1], witness.b.minus_signs[j]);
        b_sum = add(b_sum, add(b[shift], b[N - shift]));
    }
    b[0] = unit(0, witness.b.center_sign);
    b_sum = add(b_sum, b[0]);
    assert((b_sum == G{1, 0}));
    assert(residual_bits(a, b) == 0);
}

std::string bits16(uint32_t value) {
    std::string result;
    for (int j = 0; j < 16; ++j) result.push_back(((value >> j) & 1) ? '1' : '0');
    return result;
}

std::string bits2(const std::array<int, 2>& value) {
    return std::to_string(value[0]) + std::to_string(value[1]);
}

struct Row {
    std::string b_equal;
    std::string a_opposite;
    std::string rank;
    std::string b_s_residues;
};

}  // namespace

int main(int argc, char** argv) {
    bool dump_table = argc == 2 && std::string(argv[1]) == "--dump-table";
    bool dump_witnesses = argc == 2 && std::string(argv[1]) == "--dump-witnesses";
    int local_checks = verify_local_formulas();

    std::ifstream input("../qlp42_q1_b16_fifth_order_s/orbit_table.tsv");
    assert(input);
    std::string line;
    std::getline(input, line);
    std::vector<Row> rows;
    while (std::getline(input, line)) {
        auto fields = split_tabs(line);
        assert(fields.size() == 5);
        if (fields[4] == "1") rows.push_back({fields[0], fields[1], fields[2], fields[3]});
    }
    assert(rows.size() == 16);

    if (dump_table) {
        std::cout << "b_equal_positions\ta_opposite_orbit_representative\tfourth_order_rank"
                     "\tb_fifth_s_residue_fingerprints\tb_exact_h_phase_assignments"
                     "\tb_fifth_h_residue_fingerprints\tfifth_h_soluble\taxes_examined\n";
    }
    if (dump_witnesses) {
        std::cout << "b_equal_positions\ta_opposite_orbit_representative\ta_h_axes"
                     "\ta_h_signs\tb_h_axes\tb_h_plus_signs\tb_h_minus_signs"
                     "\tb_h_center_sign\n";
    }

    std::map<uint32_t, BData> b_cache;
    int soluble = 0;
    int eliminated = 0;
    int direct_checks = 0;
    int fully_exhausted = 0;
    int total_axes_examined = 0;
    std::set<uint32_t> soluble_b_masks;
    std::set<uint32_t> eliminated_b_masks;
    std::set<int> b_assignment_counts;
    int witness_checks = 0;

    for (const Row& row : rows) {
        uint32_t equal_word = 0;
        for (int position : parse_positions(row.b_equal)) equal_word |= uint32_t{1} << position;
        uint32_t b_word = WORD_MASK ^ equal_word ^ uint32_t{1};
        auto [it, inserted] = b_cache.try_emplace(b_word);
        if (inserted) it->second = enumerate_b(b_word);
        const BData& b_data = it->second;
        b_assignment_counts.insert(b_data.exact_assignments);

        uint32_t a_s_word = 0;
        for (int position : parse_positions(row.a_opposite)) a_s_word |= uint32_t{1} << position;
        std::vector<int> a_h_positions;
        for (int position = 0; position < N; ++position) {
            if (((a_s_word >> position) & 1) == 0) a_h_positions.push_back(position);
        }
        assert(a_h_positions.size() == 16);
        Word a_baseline = build_a(a_h_positions, 0, 0);
        uint32_t combined_baseline = residual_bits(a_baseline, b_data.baseline);
        Polynomial polynomial = interpolate_polynomial(a_h_positions, a_baseline);
        direct_checks += polynomial.direct_checks;
        Witness witness = search_a(polynomial, combined_baseline, b_data);
        total_axes_examined += witness.axes_examined;
        if (witness.found) {
            ++soluble;
            soluble_b_masks.insert(b_word);
            verify_witness(a_h_positions, b_word, b_data, witness);
            ++witness_checks;
        } else {
            ++eliminated;
            ++fully_exhausted;
            eliminated_b_masks.insert(b_word);
        }

        if (dump_table) {
            std::cout << row.b_equal << '\t' << row.a_opposite << '\t' << row.rank << '\t'
                << row.b_s_residues << '\t' << b_data.exact_assignments << '\t'
                << b_data.states.size() << '\t' << int(witness.found) << '\t'
                << witness.axes_examined << '\n';
        }
        if (dump_witnesses && witness.found) {
            std::cout << row.b_equal << '\t' << row.a_opposite << '\t'
                << bits16(witness.a_axes) << '\t' << bits16(witness.a_signs) << '\t'
                << bits2(witness.b.axes) << '\t' << bits2(witness.b.plus_signs) << '\t'
                << bits2(witness.b.minus_signs) << '\t' << witness.b.center_sign << '\n';
        }
    }

    if (dump_table || dump_witnesses) return 0;
    std::cout
        << "local_fifth_order_formula_checks=" << local_checks << '\n'
        << "input_fifth_s_a_rotation_orbits=" << rows.size() << '\n'
        << "input_fifth_s_b_masks=" << b_cache.size() << '\n'
        << "b_exact_h_phase_assignment_counts=";
    bool first = true;
    for (int count : b_assignment_counts) {
        if (!first) std::cout << ',';
        std::cout << count;
        first = false;
    }
    std::cout
        << '\n' << "direct_quadratic_interpolation_and_audit_checks=" << direct_checks
        << '\n' << "direct_full_witness_checks=" << witness_checks
        << '\n' << "axis_patterns_examined=" << total_axes_examined
        << '\n' << "fully_exhausted_orbits=" << fully_exhausted
        << '\n' << "fifth_h_surviving_a_rotation_orbits=" << soluble
        << '\n' << "fifth_h_surviving_labeled_pairs=" << 21 * soluble
        << '\n' << "fifth_h_surviving_b_masks=" << soluble_b_masks.size()
        << '\n' << "fifth_h_eliminated_a_rotation_orbits=" << eliminated
        << '\n' << "fifth_h_eliminated_labeled_pairs=" << 21 * eliminated
        << '\n' << "fifth_h_eliminated_b_masks=" << eliminated_b_masks.size()
        << '\n' << "certificate=verified\n";
}
