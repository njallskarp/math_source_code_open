#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <compare>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int N = 21;
constexpr uint32_t WORD_MASK = (uint32_t{1} << N) - 1;
constexpr uint16_t TAU_SIGNATURE =
    (uint16_t{1} << (4 - 1)) | (uint16_t{1} << (10 - 1));
constexpr uint64_t NIBBLE_LANES = 0x0f0f0f0f0f0f0f0fULL;
constexpr uint64_t EIGHT_LANES = 0x0707070707070707ULL;
constexpr uint64_t NEGATION_BASE = 0x1010101010101010ULL;

constexpr std::array<std::array<int, 4>, 6> CASES = {{
    {1, 0, 5, 0},
    {3, 0, 4, 1},
    {3, 0, 3, -2},
    {3, 2, 3, 2},
    {3, 2, 2, 3},
    {4, 1, 2, -1},
}};
constexpr std::array<int, 6> EXPECTED_A_PHASES = {1225, 441, 441, 245, 245, 147};
constexpr std::array<long long, 6> EXPECTED_B_PHASES = {
    31750, 93498, 50760, 93498, 93498, 164728,
};

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

G active(int axis, int sign) {
    G value = axis ? G{-1, 1} : G{1, 1};
    return sign ? scale(value, -1) : value;
}

using Word = std::array<G, N>;

G paf(const Word& word, int shift) {
    G result{};
    for (int position = 0; position < N; ++position) {
        result = add(result, mul(word[position], conj(word[(position + shift) % N])));
    }
    return result;
}

G target_s(int shift) {
    if (shift == 4) return {-2, 0};
    if (shift == 10) return {2, 0};
    return {0, 0};
}

std::pair<G, G> sum_targets(const std::array<int, 4>& values) {
    auto [p, q, x, y] = values;
    return {{p + q, q - p}, {x + y - 1, y - x}};
}

// Ten Gaussian residues modulo 16. Coordinates 0--7 occupy byte lanes in
// words 0 and 2; coordinates 8--9 occupy words 1 and 3. Only each byte's low
// nibble is used, so lane-wise modular addition has no inter-lane carry.
struct Residue {
    std::array<uint64_t, 4> lane{};
    bool operator==(const Residue&) const = default;
};

struct ResidueHash {
    size_t operator()(const Residue& value) const {
        uint64_t hash = 0xcbf29ce484222325ULL;
        for (uint64_t lane : value.lane) {
            hash ^= lane;
            hash *= 0x100000001b3ULL;
            hash ^= lane >> 32;
            hash *= 0x100000001b3ULL;
        }
        return size_t(hash);
    }
};

Residue residue_add(Residue a, const Residue& b) {
    for (int j = 0; j < 4; ++j) {
        a.lane[j] = (a.lane[j] + b.lane[j]) & NIBBLE_LANES;
    }
    return a;
}

Residue residue_negate(Residue a) {
    for (uint64_t& lane : a.lane) {
        lane = (NEGATION_BASE - lane) & NIBBLE_LANES;
    }
    return a;
}

Residue residue_subtract(Residue a, const Residue& b) {
    return residue_add(a, residue_negate(b));
}

void set_coordinate(Residue& value, int shift_index, G coordinate) {
    int side = shift_index < 8 ? 0 : 1;
    int offset = 8 * (shift_index % 8);
    value.lane[side] |= uint64_t(coordinate.r & 15) << offset;
    value.lane[2 + side] |= uint64_t(coordinate.i & 15) << offset;
}

Residue paf_residue(const Word& word) {
    Residue result;
    for (int shift = 1; shift <= 10; ++shift) {
        set_coordinate(result, shift - 1, paf(word, shift));
    }
    return result;
}

Residue target_residue() {
    Residue result;
    for (int shift = 1; shift <= 10; ++shift) {
        set_coordinate(result, shift - 1, target_s(shift));
    }
    return result;
}

Residue reduce_sixth(Residue value) {
    for (uint64_t& lane : value.lane) lane &= EIGHT_LANES;
    return value;
}

Residue reduce_seventh(const Residue& value) {
    Residue result;
    for (int side = 0; side < 2; ++side) {
        result.lane[side] = value.lane[side] & EIGHT_LANES;
        result.lane[2 + side] =
            (value.lane[side] + value.lane[2 + side]) & NIBBLE_LANES;
    }
    return result;
}

uint32_t rotate_word(uint32_t word, int shift) {
    if (shift == 0) return word;
    return ((word >> shift) | (word << (N - shift))) & WORD_MASK;
}

uint32_t orbit_representative(uint32_t word) {
    uint32_t result = word;
    for (int shift = 1; shift < N; ++shift) {
        result = std::min(result, rotate_word(word, shift));
    }
    return result;
}

uint16_t correlation_signature(uint32_t word) {
    uint16_t result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        result |= uint16_t(std::popcount(word & rotate_word(word, shift)) & 1)
                  << (shift - 1);
    }
    return result;
}

uint32_t symmetric_b_word(uint16_t bits) {
    uint32_t result = 0;
    for (int shift = 1; shift <= 10; ++shift) if ((bits >> (shift - 1)) & 1) {
        result |= (uint32_t{1} << shift) | (uint32_t{1} << (N - shift));
    }
    return result;
}

struct Entry {
    uint32_t b_word = 0;
    uint16_t required_signature = 0;
    std::array<int, 10> theta{};
    int labeled = 0;
    int orbits = 0;
};

struct Inputs {
    std::array<int, 1024> labeled{};
    std::array<std::set<uint32_t>, 1024> representatives;
    std::vector<Entry> entries;
};

Inputs reconstruct_inputs() {
    Inputs result;
    for (uint32_t word = 0; word <= WORD_MASK; ++word) {
        if (std::popcount(word) != 7) continue;
        uint16_t signature = correlation_signature(word);
        ++result.labeled[signature];
        result.representatives[signature].insert(orbit_representative(word));
    }

    for (uint16_t bits = 0; bits < 1024; ++bits) {
        uint32_t b_word = symmetric_b_word(bits);
        if (std::popcount(b_word) != 14) continue;
        uint32_t f_word = ((~b_word) & WORD_MASK) & ~uint32_t{1};
        uint16_t b_signature = correlation_signature(b_word);
        uint16_t f_signature = correlation_signature(f_word);
        uint16_t required = 0;
        std::array<int, 10> theta{};
        for (int shift = 1; shift <= 10; ++shift) {
            int bit = shift - 1;
            int tau = (TAU_SIGNATURE >> bit) & 1;
            int b_corr = (b_signature >> bit) & 1;
            int f_corr = (f_signature >> bit) & 1;
            int a_corr = ((b_word >> shift) & 1) ? f_corr : (tau ^ b_corr);
            required |= uint16_t(a_corr) << bit;
            theta[bit] = 1 ^ tau ^ b_corr ^ f_corr;
        }
        if (result.labeled[required]) {
            result.entries.push_back(
                {b_word, required, theta, result.labeled[required],
                 int(result.representatives[required].size())}
            );
        }
    }
    assert(result.entries.size() == 56);
    int labeled_pairs = 0;
    int orbit_pairs = 0;
    for (const Entry& entry : result.entries) {
        labeled_pairs += entry.labeled;
        orbit_pairs += entry.orbits;
    }
    assert(labeled_pairs == 6762);
    assert(orbit_pairs == 322);
    return result;
}

Residue evaluate_quadratic(
    uint16_t mask,
    const std::array<Residue, 15>& linear,
    const std::array<std::array<Residue, 15>, 15>& quadratic) {
    Residue result;
    for (int j = 0; j < 15; ++j) if ((mask >> j) & 1) {
        result = residue_add(result, linear[j]);
        for (int k = j + 1; k < 15; ++k) if ((mask >> k) & 1) {
            result = residue_add(result, quadratic[j][k]);
        }
    }
    return result;
}

struct BData {
    std::array<std::unordered_set<Residue, ResidueHash>, 6> order_six;
    std::array<std::unordered_set<Residue, ResidueHash>, 6> order_seven;
    std::array<std::unordered_set<Residue, ResidueHash>, 6> order_eight;
    std::array<long long, 6> exact_assignments{};
    long long direct_checks = 0;
};

BData enumerate_b(const Entry& entry) {
    BData data;
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) if ((entry.b_word >> shift) & 1) {
        shifts.push_back(shift);
    }
    assert(shifts.size() == 7);
    std::array<G, 6> targets{};
    for (int case_number = 0; case_number < 6; ++case_number) {
        targets[case_number] = sum_targets(CASES[case_number]).second;
        data.order_eight[case_number].reserve(size_t(EXPECTED_B_PHASES[case_number]));
    }

    constexpr std::array<uint16_t, 16> AUDITS = {
        0x7fffu, 0x5555u, 0x2aaau, 0x0ff0u,
        0x700fu, 0x3333u, 0x4cccu, 0x3579u,
        0x468au, 0x00ffu, 0x7f00u, 0x1555u,
        0x2aaau, 0x2481u, 0x0421u, 0x69c3u,
    };

    for (uint16_t axes = 0; axes < 128; ++axes) {
        Word word{};
        std::array<int, 15> sign_positions{};
        int variable = 0;
        for (int j = 0; j < 7; ++j) {
            int shift = shifts[j];
            int axis = (axes >> j) & 1;
            word[shift] = active(axis, 0);
            word[N - shift] = active(axis ^ entry.theta[shift - 1], 0);
            sign_positions[variable++] = shift;
            sign_positions[variable++] = N - shift;
        }
        word[0] = {0, -1};
        sign_positions[variable++] = 0;
        assert(variable == 15);

        Residue axis_value = paf_residue(word);
        std::array<Residue, 15> linear{};
        std::array<std::array<Residue, 15>, 15> quadratic{};
        for (int j = 0; j < 15; ++j) {
            Word changed = word;
            changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            linear[j] = residue_subtract(paf_residue(changed), axis_value);
            ++data.direct_checks;
        }
        for (int j = 0; j < 15; ++j) for (int k = j + 1; k < 15; ++k) {
            Word changed = word;
            changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            changed[sign_positions[k]] = scale(changed[sign_positions[k]], -1);
            Residue pair = residue_subtract(paf_residue(changed), axis_value);
            quadratic[j][k] = residue_subtract(
                residue_subtract(pair, linear[j]), linear[k]
            );
            ++data.direct_checks;
        }
        for (uint16_t mask : AUDITS) {
            Word changed = word;
            for (int j = 0; j < 15; ++j) if ((mask >> j) & 1) {
                changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            }
            Residue direct = residue_subtract(paf_residue(changed), axis_value);
            assert(direct == evaluate_quadratic(mask, linear, quadratic));
            ++data.direct_checks;
        }

        G baseline_sum{};
        std::array<G, 15> changes{};
        for (int j = 0; j < 15; ++j) {
            G value = word[sign_positions[j]];
            baseline_sum = add(baseline_sum, value);
            changes[j] = scale(value, -2);
        }

        std::array<G, 128> left_sums{};
        std::array<Residue, 128> left_residues{};
        for (uint16_t mask = 1; mask < 128; ++mask) {
            int j = std::countr_zero(mask);
            uint16_t rest = mask & (mask - 1);
            left_sums[mask] = add(left_sums[rest], changes[j]);
            Residue value = residue_add(left_residues[rest], linear[j]);
            for (int k = j + 1; k < 7; ++k) if ((rest >> k) & 1) {
                value = residue_add(value, quadratic[j][k]);
            }
            left_residues[mask] = value;
        }

        std::array<G, 256> right_sums{};
        std::array<Residue, 256> right_residues{};
        std::map<G, std::vector<uint8_t>> right_by_sum;
        right_by_sum[G{}].push_back(0);
        for (uint16_t mask = 1; mask < 256; ++mask) {
            int local = std::countr_zero(mask);
            int j = 7 + local;
            uint16_t rest = mask & (mask - 1);
            right_sums[mask] = add(right_sums[rest], changes[j]);
            Residue value = residue_add(right_residues[rest], linear[j]);
            for (int k = j + 1; k < 15; ++k) if ((rest >> (k - 7)) & 1) {
                value = residue_add(value, quadratic[j][k]);
            }
            right_residues[mask] = value;
            right_by_sum[right_sums[mask]].push_back(uint8_t(mask));
        }

        std::array<std::array<Residue, 256>, 7> cross_columns{};
        for (int j = 0; j < 7; ++j) {
            for (uint16_t mask = 1; mask < 256; ++mask) {
                int local = std::countr_zero(mask);
                uint16_t rest = mask & (mask - 1);
                cross_columns[j][mask] = residue_add(
                    cross_columns[j][rest], quadratic[j][7 + local]
                );
            }
        }

        for (uint16_t left = 0; left < 128; ++left) {
            for (int case_number = 0; case_number < 6; ++case_number) {
                G required = sub(sub(targets[case_number], baseline_sum), left_sums[left]);
                auto found = right_by_sum.find(required);
                if (found == right_by_sum.end()) continue;
                for (uint8_t right : found->second) {
                    Residue value = residue_add(
                        axis_value,
                        residue_add(left_residues[left], right_residues[right])
                    );
                    for (int j = 0; j < 7; ++j) if ((left >> j) & 1) {
                        value = residue_add(value, cross_columns[j][right]);
                    }
                    ++data.exact_assignments[case_number];
                    data.order_eight[case_number].insert(value);
                }
            }
        }
    }

    assert(data.exact_assignments == EXPECTED_B_PHASES);
    assert(data.direct_checks == 17'408);
    for (int case_number = 0; case_number < 6; ++case_number) {
        data.order_six[case_number].reserve(data.order_eight[case_number].size());
        data.order_seven[case_number].reserve(data.order_eight[case_number].size());
        for (const Residue& value : data.order_eight[case_number]) {
            data.order_six[case_number].insert(reduce_sixth(value));
            data.order_seven[case_number].insert(reduce_seventh(value));
        }
    }
    return data;
}

struct AData {
    std::array<std::vector<Residue>, 6> residues;
};

AData enumerate_a(uint32_t support_word) {
    std::vector<int> positions;
    for (int position = 0; position < N; ++position) if ((support_word >> position) & 1) {
        positions.push_back(position);
    }
    assert(positions.size() == 7);
    std::array<G, 6> targets{};
    for (int case_number = 0; case_number < 6; ++case_number) {
        targets[case_number] = sum_targets(CASES[case_number]).first;
    }
    AData result;
    for (int code = 0; code < (1 << 14); ++code) {
        int value = code;
        Word word{};
        G sum{};
        for (int j = 0; j < 7; ++j) {
            int root = value & 3;
            value >>= 2;
            word[positions[j]] = active(root >> 1, root & 1);
            sum = add(sum, word[positions[j]]);
        }
        bool needed = false;
        for (G target : targets) needed = needed || sum == target;
        if (!needed) continue;
        Residue fingerprint = paf_residue(word);
        for (int case_number = 0; case_number < 6; ++case_number) {
            if (sum == targets[case_number]) {
                result.residues[case_number].push_back(fingerprint);
            }
        }
    }
    for (int case_number = 0; case_number < 6; ++case_number) {
        assert(int(result.residues[case_number].size()) == EXPECTED_A_PHASES[case_number]);
    }
    return result;
}

std::string positions(uint32_t word) {
    std::string result;
    for (int position = 0; position < N; ++position) if ((word >> position) & 1) {
        if (!result.empty()) result += ',';
        result += std::to_string(position);
    }
    return result;
}

struct SeventhRow {
    int case_number = 0;
    uint32_t equal_word = 0;
    uint32_t a_word = 0;
    auto operator<=>(const SeventhRow&) const = default;
};

}  // namespace

int main(int argc, char** argv) {
    bool quiet = argc == 2 && std::string(argv[1]) == "--quiet";
    Inputs inputs = reconstruct_inputs();
    Residue target = target_residue();
    std::map<uint32_t, AData> a_cache;
    std::array<std::array<int, 6>, 3> surviving_orbits{};
    std::array<std::array<std::set<uint32_t>, 6>, 3> surviving_masks;
    std::array<int, 3> surviving_rows{};
    std::set<SeventhRow> seventh_rows;
    long long direct_checks = 0;

    int entry_number = 0;
    for (const Entry& entry : inputs.entries) {
        ++entry_number;
        BData b_data = enumerate_b(entry);
        direct_checks += b_data.direct_checks;
        for (uint32_t a_word : inputs.representatives[entry.required_signature]) {
            auto [iterator, inserted] = a_cache.try_emplace(a_word);
            if (inserted) iterator->second = enumerate_a(a_word);
            const AData& a_data = iterator->second;
            std::array<bool, 3> row_survives{};
            for (int case_number = 0; case_number < 6; ++case_number) {
                std::array<bool, 3> feasible{};
                for (const Residue& a_value : a_data.residues[case_number]) {
                    Residue needed = residue_subtract(target, a_value);
                    feasible[0] = feasible[0] || b_data.order_six[case_number].contains(
                        reduce_sixth(needed)
                    );
                    feasible[1] = feasible[1] || b_data.order_seven[case_number].contains(
                        reduce_seventh(needed)
                    );
                    feasible[2] = feasible[2] || b_data.order_eight[case_number].contains(
                        needed
                    );
                    if (feasible[0] && feasible[1] && feasible[2]) break;
                }
                for (int order = 0; order < 3; ++order) if (feasible[order]) {
                    ++surviving_orbits[order][case_number];
                    surviving_masks[order][case_number].insert(entry.b_word);
                    row_survives[order] = true;
                }
                if (feasible[1]) {
                    seventh_rows.insert(
                        {case_number, WORD_MASK ^ entry.b_word ^ uint32_t{1}, a_word}
                    );
                }
            }
            for (int order = 0; order < 3; ++order) {
                surviving_rows[order] += int(row_survives[order]);
            }
        }
        if (!quiet) std::cout << "completed_b_mask=" << entry_number << "/56\n";
    }

    const std::array<std::array<int, 6>, 3> expected_orbits = {{
        {24, 29, 7, 32, 32, 12},
        {0, 0, 0, 2, 2, 0},
        {0, 0, 0, 0, 0, 0},
    }};
    const std::array<std::array<int, 6>, 3> expected_masks = {{
        {9, 13, 3, 16, 16, 6},
        {0, 0, 0, 1, 1, 0},
        {0, 0, 0, 0, 0, 0},
    }};
    assert(surviving_orbits == expected_orbits);
    for (int order = 0; order < 3; ++order) {
        for (int case_number = 0; case_number < 6; ++case_number) {
            assert(int(surviving_masks[order][case_number].size())
                   == expected_masks[order][case_number]);
        }
    }
    assert((surviving_rows == std::array<int, 3>{94, 2, 0}));

    uint32_t expected_equal = 0;
    for (int position : {5, 6, 10, 11, 15, 16}) {
        expected_equal |= uint32_t{1} << position;
    }
    std::set<uint32_t> expected_a;
    for (const std::vector<int>& support : {
             std::vector<int>{0, 2, 3, 5, 7, 9, 14},
             std::vector<int>{0, 5, 7, 9, 11, 12, 14},
         }) {
        uint32_t word = 0;
        for (int position : support) word |= uint32_t{1} << position;
        expected_a.insert(word);
    }
    assert(seventh_rows.size() == 4);
    for (const SeventhRow& row : seventh_rows) {
        assert(row.case_number == 3 || row.case_number == 4);
        assert(row.equal_word == expected_equal);
        assert(expected_a.contains(row.a_word));
    }
    assert(direct_checks == 974'848);

    std::cout << "input_b_masks=56\n"
              << "input_labeled_type_pairs=6762\n"
              << "input_rotation_orbits_per_case=322\n"
              << "sixth_order_surviving_orbits=24,29,7,32,32,12\n"
              << "seventh_order_surviving_orbits=0,0,0,2,2,0\n"
              << "eighth_order_surviving_orbits=0,0,0,0,0,0\n"
              << "quadratic_interpolation_direct_audits=" << direct_checks << '\n'
              << "cached_a_supports=" << a_cache.size() << '\n'
              << "seventh_survivor_b_equal=" << positions(expected_equal) << '\n'
              << "eighth_order_surviving_orbits=0\n"
              << "independent_cpp_certificate=verified\n";
}
