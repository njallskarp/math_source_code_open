#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main embedded_b14_main
#include "../qlp42_q1_b14_sixth_order_s/independent_cpp.cpp"
#undef main
#pragma GCC diagnostic pop

#include <climits>

namespace {

struct Entry6 {
    uint32_t b_word = 0;
    uint16_t required_signature = 0;
    std::array<int, 10> theta{};
};

struct Inputs6 {
    std::array<int, 1024> labeled{};
    std::array<std::set<uint32_t>, 1024> representatives;
    std::vector<Entry6> entries;
};

Inputs6 reconstruct_inputs6() {
    Inputs6 result;
    for (uint32_t word = 0; word <= WORD_MASK; ++word) {
        if (std::popcount(word) != 15) continue;
        uint16_t signature = correlation_signature(word);
        ++result.labeled[signature];
        result.representatives[signature].insert(orbit_representative(word));
    }
    for (uint16_t bits = 0; bits < 1024; ++bits) {
        uint32_t b_word = symmetric_b_word(bits);
        if (std::popcount(b_word) != 6) continue;
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
            result.entries.push_back({b_word, required, theta});
        }
    }
    assert(result.entries.size() == 50);
    int labeled_pairs = 0;
    int orbit_pairs = 0;
    for (const Entry6& entry : result.entries) {
        labeled_pairs += result.labeled[entry.required_signature];
        orbit_pairs += int(result.representatives[entry.required_signature].size());
    }
    assert(labeled_pairs == 3402);
    assert(orbit_pairs == 162);
    return result;
}

Residue h_target6() {
    Residue result;
    for (int shift = 1; shift <= 10; ++shift) {
        set_coordinate(result, shift - 1, {-2, 0});
    }
    return result;
}

long long count_h_sum6(const Entry6& entry, int center) {
    std::map<G, long long> totals;
    totals[G{center, 0}] = 1;
    for (int shift = 1; shift <= 10; ++shift) {
        if ((entry.b_word >> shift) & 1) continue;
        std::map<G, long long> pair_sums;
        for (int axis = 0; axis < 2; ++axis) {
            G left = active(axis, 0);
            G right = active(axis ^ entry.theta[shift - 1], 0);
            for (int left_sign = 0; left_sign < 2; ++left_sign) {
                for (int right_sign = 0; right_sign < 2; ++right_sign) {
                    pair_sums[add(
                        scale(left, left_sign ? -1 : 1),
                        scale(right, right_sign ? -1 : 1)
                    )]++;
                }
            }
        }
        std::map<G, long long> next;
        for (const auto& [partial, partial_count] : totals) {
            for (const auto& [pair, pair_count] : pair_sums) {
                next[add(partial, pair)] += partial_count * pair_count;
            }
        }
        totals = std::move(next);
    }
    return totals[G{1, 0}];
}

struct BData6 {
    std::unordered_set<Residue, ResidueHash> complement6;
    std::unordered_set<Residue, ResidueHash> complement7;
    long long exact_assignments = 0;
    long long direct_evaluations = 0;
    long long quadratic_audits = 0;
};

BData6 enumerate_b6(const Entry6& entry) {
    std::array<int, 14> positions{};
    int position_count = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        if ((entry.b_word >> shift) & 1) continue;
        positions[position_count++] = shift;
        positions[position_count++] = N - shift;
    }
    assert(position_count == 14);

    BData6 result;
    result.complement6.reserve(90000);
    result.complement7.reserve(90000);
    Residue target = h_target6();
    constexpr std::array<uint16_t, 16> AUDITS = {
        0x0000u, 0x3fffu, 0x1555u, 0x2aaau,
        0x00ffu, 0x3f00u, 0x0f0fu, 0x30f0u,
        0x1234u, 0x2345u, 0x3456u, 0x0249u,
        0x2492u, 0x0924u, 0x3333u, 0x0cccu,
    };

    for (uint16_t axes = 0; axes < 128; ++axes) {
        Word baseline_word{};
        baseline_word[0] = {-1, 0};
        int pair_index = 0;
        for (int shift = 1; shift <= 10; ++shift) {
            if ((entry.b_word >> shift) & 1) continue;
            int axis = (axes >> pair_index) & 1;
            baseline_word[shift] = active(axis, 0);
            baseline_word[N - shift] = active(
                axis ^ entry.theta[shift - 1], 0
            );
            ++pair_index;
        }
        assert(pair_index == 7);

        Residue baseline = paf_residue(baseline_word);
        std::array<Residue, 15> linear{};
        std::array<std::array<Residue, 15>, 15> quadratic{};
        for (int j = 0; j < 14; ++j) {
            Word changed = baseline_word;
            changed[positions[j]] = scale(changed[positions[j]], -1);
            linear[j] = residue_subtract(paf_residue(changed), baseline);
            ++result.direct_evaluations;
        }
        for (int j = 0; j < 14; ++j) for (int k = j + 1; k < 14; ++k) {
            Word changed = baseline_word;
            changed[positions[j]] = scale(changed[positions[j]], -1);
            changed[positions[k]] = scale(changed[positions[k]], -1);
            Residue pair = residue_subtract(paf_residue(changed), baseline);
            quadratic[j][k] = residue_subtract(
                residue_subtract(pair, linear[j]), linear[k]
            );
            ++result.direct_evaluations;
        }
        for (uint16_t mask : AUDITS) {
            Word changed = baseline_word;
            for (int j = 0; j < 14; ++j) if ((mask >> j) & 1) {
                changed[positions[j]] = scale(changed[positions[j]], -1);
            }
            Residue direct = residue_subtract(paf_residue(changed), baseline);
            assert(direct == evaluate_quadratic(mask, linear, quadratic));
            ++result.direct_evaluations;
            ++result.quadratic_audits;
        }

        G baseline_sum{-1, 0};
        std::array<G, 14> changes{};
        for (int j = 0; j < 14; ++j) {
            G value = baseline_word[positions[j]];
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

        std::array<G, 128> right_sums{};
        std::array<Residue, 128> right_residues{};
        std::map<G, std::vector<uint8_t>> right_by_sum;
        right_by_sum[G{}].push_back(0);
        for (uint16_t mask = 1; mask < 128; ++mask) {
            int local = std::countr_zero(mask);
            int j = 7 + local;
            uint16_t rest = mask & (mask - 1);
            right_sums[mask] = add(right_sums[rest], changes[j]);
            Residue value = residue_add(right_residues[rest], linear[j]);
            for (int k = j + 1; k < 14; ++k) if ((rest >> (k - 7)) & 1) {
                value = residue_add(value, quadratic[j][k]);
            }
            right_residues[mask] = value;
            right_by_sum[right_sums[mask]].push_back(uint8_t(mask));
        }

        std::array<std::array<Residue, 128>, 7> cross_columns{};
        for (int j = 0; j < 7; ++j) {
            for (uint16_t mask = 1; mask < 128; ++mask) {
                int local = std::countr_zero(mask);
                uint16_t rest = mask & (mask - 1);
                cross_columns[j][mask] = residue_add(
                    cross_columns[j][rest], quadratic[j][7 + local]
                );
            }
        }

        for (uint16_t left = 0; left < 128; ++left) {
            G required = sub(sub(G{1, 0}, baseline_sum), left_sums[left]);
            auto found = right_by_sum.find(required);
            if (found == right_by_sum.end()) continue;
            for (uint8_t right : found->second) {
                Residue value = residue_add(
                    baseline, residue_add(left_residues[left], right_residues[right])
                );
                for (int j = 0; j < 7; ++j) if ((left >> j) & 1) {
                    value = residue_add(value, cross_columns[j][right]);
                }
                Residue complement = residue_subtract(target, value);
                result.complement6.insert(reduce_sixth(complement));
                result.complement7.insert(reduce_seventh(complement));
                ++result.exact_assignments;
            }
        }
    }
    assert(result.exact_assignments == 164728);
    assert(result.direct_evaluations == 128LL * (14 + 91 + 16));
    assert(result.quadratic_audits == 128LL * 16);
    return result;
}

struct AData6 {
    std::unordered_set<Residue, ResidueHash> values6;
    std::unordered_set<Residue, ResidueHash> values7;
    int exact_assignments = 0;
};

AData6 enumerate_a6(uint32_t support) {
    std::array<int, 6> positions{};
    int count = 0;
    for (int position = 0; position < N; ++position) {
        if (!((support >> position) & 1)) positions[count++] = position;
    }
    assert(count == 6);

    AData6 result;
    for (uint16_t code = 0; code < 4096; ++code) {
        uint16_t encoded = code;
        Word word{};
        G sum{};
        for (int j = 0; j < 6; ++j) {
            int root = encoded & 3;
            encoded >>= 2;
            word[positions[j]] = active(root >> 1, root & 1);
            sum = add(sum, word[positions[j]]);
        }
        if (sum != G{}) continue;
        Residue value = paf_residue(word);
        result.values6.insert(reduce_sixth(value));
        result.values7.insert(reduce_seventh(value));
        ++result.exact_assignments;
    }
    assert(result.exact_assignments == 400);
    return result;
}

struct Pair6 {
    uint32_t a_support = 0;
    uint32_t b_word = 0;
    auto operator<=>(const Pair6&) const = default;
};

}  // namespace

int main() {
    Inputs6 inputs = reconstruct_inputs6();
    std::vector<BData6> b_data;
    b_data.reserve(inputs.entries.size());
    size_t b6_min = SIZE_MAX;
    size_t b6_max = 0;
    size_t b7_min = SIZE_MAX;
    size_t b7_max = 0;
    long long direct_evaluations = 0;
    long long quadratic_audits = 0;
    for (const Entry6& entry : inputs.entries) {
        assert(count_h_sum6(entry, 1) == 0);
        assert(count_h_sum6(entry, -1) == 164728);
        BData6 data = enumerate_b6(entry);
        b6_min = std::min(b6_min, data.complement6.size());
        b6_max = std::max(b6_max, data.complement6.size());
        b7_min = std::min(b7_min, data.complement7.size());
        b7_max = std::max(b7_max, data.complement7.size());
        direct_evaluations += data.direct_evaluations;
        quadratic_audits += data.quadratic_audits;
        b_data.push_back(std::move(data));
    }

    std::map<uint32_t, std::vector<int>> by_support;
    for (int entry_index = 0; entry_index < int(inputs.entries.size()); ++entry_index) {
        const Entry6& entry = inputs.entries[entry_index];
        for (uint32_t support : inputs.representatives[entry.required_signature]) {
            by_support[support].push_back(entry_index);
        }
    }
    assert(by_support.size() == 134);
    int input_pairs = 0;
    for (const auto& [support, entries] : by_support) {
        (void)support;
        input_pairs += int(entries.size());
    }
    assert(input_pairs == 162);

    std::vector<Pair6> frontier6;
    std::vector<Pair6> frontier7;
    size_t a6_min = SIZE_MAX;
    size_t a6_max = 0;
    size_t a7_min = SIZE_MAX;
    size_t a7_max = 0;
    long long a_assignments = 0;
    for (const auto& [support, entry_indices] : by_support) {
        AData6 a_data = enumerate_a6(support);
        a_assignments += a_data.exact_assignments;
        a6_min = std::min(a6_min, a_data.values6.size());
        a6_max = std::max(a6_max, a_data.values6.size());
        a7_min = std::min(a7_min, a_data.values7.size());
        a7_max = std::max(a7_max, a_data.values7.size());
        for (int entry_index : entry_indices) {
            const Entry6& entry = inputs.entries[entry_index];
            bool feasible6 = false;
            for (const Residue& value : a_data.values6) {
                if (b_data[entry_index].complement6.contains(value)) {
                    feasible6 = true;
                    break;
                }
            }
            if (feasible6) frontier6.push_back({support, entry.b_word});

            bool feasible7 = false;
            for (const Residue& value : a_data.values7) {
                if (b_data[entry_index].complement7.contains(value)) {
                    feasible7 = true;
                    break;
                }
            }
            if (feasible7) frontier7.push_back({support, entry.b_word});
        }
    }
    std::sort(frontier6.begin(), frontier6.end());
    std::sort(frontier7.begin(), frontier7.end());
    assert(frontier6.size() == 4);
    assert(frontier7.empty());

    std::cout << "reflected_b_masks=" << inputs.entries.size() << '\n'
              << "labeled_type_pairs=3402\n"
              << "input_rotation_orbit_pairs=" << input_pairs << '\n'
              << "distinct_a_supports=" << by_support.size() << '\n'
              << "h_b_positive_center_assignments=0\n"
              << "h_b_negative_center_assignments=164728\n"
              << "h_a_zero_sum_assignments_per_support=400\n"
              << "h_b_sixth_fingerprint_range=" << b6_min << '-' << b6_max << '\n'
              << "h_b_seventh_fingerprint_range=" << b7_min << '-' << b7_max << '\n'
              << "h_a_sixth_fingerprint_range=" << a6_min << '-' << a6_max << '\n'
              << "h_a_seventh_fingerprint_range=" << a7_min << '-' << a7_max << '\n'
              << "h_a_exact_assignments=" << a_assignments << '\n'
              << "b_quadratic_direct_evaluations=" << direct_evaluations << '\n'
              << "b_quadratic_global_audits=" << quadratic_audits << '\n'
              << "sixth_order_h_pairs=" << frontier6.size() << '\n'
              << "seventh_order_h_pairs=" << frontier7.size() << '\n'
              << "certificate=verified\n";
    for (const Pair6& pair : frontier6) {
        std::cout << "sixth_frontier_pair=" << pair.a_support << ',' << pair.b_word << '\n';
    }
    return 0;
}
