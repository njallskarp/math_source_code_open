#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main embedded_b14_main
#include "../qlp42_q1_b14_sixth_order_s/independent_cpp.cpp"
#undef main
#pragma GCC diagnostic pop

namespace {

struct Entry10 {
    uint32_t b_word = 0;
    uint16_t required_signature = 0;
    std::array<int, 10> theta{};
    int labeled = 0;
    int orbits = 0;
};

struct Inputs10 {
    std::array<int, 1024> labeled{};
    std::array<std::set<uint32_t>, 1024> representatives;
    std::vector<Entry10> entries;
};

Inputs10 reconstruct_inputs10() {
    Inputs10 result;
    for (uint32_t word = 0; word <= WORD_MASK; ++word) {
        if (std::popcount(word) != 11) continue;
        uint16_t signature = correlation_signature(word);
        ++result.labeled[signature];
        result.representatives[signature].insert(orbit_representative(word));
    }
    for (uint16_t bits = 0; bits < 1024; ++bits) {
        uint32_t b_word = symmetric_b_word(bits);
        if (std::popcount(b_word) != 10) continue;
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
    assert(result.entries.size() == 140);
    int labeled_pairs = 0;
    int orbit_pairs = 0;
    for (const Entry10& entry : result.entries) {
        labeled_pairs += entry.labeled;
        orbit_pairs += entry.orbits;
    }
    assert(labeled_pairs == 56490);
    assert(orbit_pairs == 2690);
    return result;
}

std::array<long long, 6> count_a_phase_patterns10() {
    std::array<G, 6> targets{};
    for (int case_number = 0; case_number < 6; ++case_number) {
        targets[case_number] = sum_targets(CASES[case_number]).first;
    }
    std::array<long long, 6> result{};
    for (uint32_t code = 0; code < (uint32_t{1} << 22); ++code) {
        uint32_t encoded = code;
        G sum{};
        for (int j = 0; j < 11; ++j) {
            int root = encoded & 3;
            encoded >>= 2;
            sum = add(sum, active(root >> 1, root & 1));
        }
        for (int case_number = 0; case_number < 6; ++case_number) {
            result[case_number] += int(sum == targets[case_number]);
        }
    }
    return result;
}

std::array<long long, 6> count_b_s_phase_patterns10(
    const Entry10& entry, int center_imag) {
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) {
        if ((entry.b_word >> shift) & 1) shifts.push_back(shift);
    }
    assert(shifts.size() == 5);
    std::array<G, 6> targets{};
    for (int case_number = 0; case_number < 6; ++case_number) {
        targets[case_number] = sum_targets(CASES[case_number]).second;
    }
    std::array<long long, 6> result{};
    for (uint16_t axes = 0; axes < 32; ++axes) {
        std::array<G, 10> values{};
        int count = 0;
        for (int j = 0; j < 5; ++j) {
            int shift = shifts[j];
            int axis = (axes >> j) & 1;
            values[count++] = active(axis, 0);
            values[count++] = active(axis ^ entry.theta[shift - 1], 0);
        }
        assert(count == 10);
        for (uint16_t signs = 0; signs < 1024; ++signs) {
            G sum{0, center_imag};
            for (int j = 0; j < 10; ++j) {
                sum = add(sum, ((signs >> j) & 1) ? scale(values[j], -1) : values[j]);
            }
            for (int case_number = 0; case_number < 6; ++case_number) {
                result[case_number] += int(sum == targets[case_number]);
            }
        }
    }
    return result;
}

long long count_b_h_phase_patterns10(const Entry10& entry, int center_real) {
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) {
        if (!((entry.b_word >> shift) & 1)) shifts.push_back(shift);
    }
    assert(shifts.size() == 5);
    long long result = 0;
    for (uint16_t axes = 0; axes < 32; ++axes) {
        std::array<G, 10> values{};
        int count = 0;
        for (int j = 0; j < 5; ++j) {
            int shift = shifts[j];
            int axis = (axes >> j) & 1;
            values[count++] = active(axis, 0);
            values[count++] = active(axis ^ entry.theta[shift - 1], 0);
        }
        assert(count == 10);
        for (uint16_t signs = 0; signs < 1024; ++signs) {
            G sum{center_real, 0};
            for (int j = 0; j < 10; ++j) {
                sum = add(sum, ((signs >> j) & 1) ? scale(values[j], -1) : values[j]);
            }
            result += int(sum == G{1, 0});
        }
    }
    return result;
}

Residue h6_add(Residue left, const Residue& right) {
    return reduce_sixth(residue_add(left, right));
}

Residue h6_subtract(Residue left, const Residue& right) {
    return reduce_sixth(residue_subtract(left, right));
}

Residue h6_target() {
    Residue result;
    for (int shift = 1; shift <= 10; ++shift) {
        set_coordinate(result, shift - 1, {-2, 0});
    }
    return reduce_sixth(result);
}

struct H6BData10 {
    std::unordered_set<Residue, ResidueHash> complements;
    int exact_assignments = 0;
};

H6BData10 enumerate_h6_b10(const Entry10& entry) {
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) {
        if (!((entry.b_word >> shift) & 1)) shifts.push_back(shift);
    }
    assert(shifts.size() == 5);
    Residue target = h6_target();
    H6BData10 result;
    for (uint16_t axes = 0; axes < 32; ++axes) {
        Word word{};
        std::array<int, 10> positions{};
        int count = 0;
        for (int j = 0; j < 5; ++j) {
            int shift = shifts[j];
            int axis = (axes >> j) & 1;
            word[shift] = active(axis, 0);
            word[N - shift] = active(axis ^ entry.theta[shift - 1], 0);
            positions[count++] = shift;
            positions[count++] = N - shift;
        }
        word[0] = {-1, 0};
        assert(count == 10);
        for (uint16_t signs = 0; signs < 1024; ++signs) {
            Word changed = word;
            for (int j = 0; j < 10; ++j) if ((signs >> j) & 1) {
                changed[positions[j]] = scale(changed[positions[j]], -1);
            }
            G sum{-1, 0};
            for (int j = 0; j < 10; ++j) sum = add(sum, changed[positions[j]]);
            if (sum != G{1, 0}) continue;
            ++result.exact_assignments;
            result.complements.insert(h6_subtract(
                target, reduce_sixth(paf_residue(changed))
            ));
        }
    }
    assert(result.exact_assignments == 3384);
    return result;
}

struct H6AData10 {
    std::unordered_set<Residue, ResidueHash> fingerprints;
    long long exact_assignments = 0;
    int affine_audits = 0;
};

H6AData10 enumerate_h6_a10(uint32_t s_support) {
    std::array<int, 10> positions{};
    int active_count = 0;
    for (int position = 0; position < N; ++position) {
        if (!((s_support >> position) & 1)) positions[active_count++] = position;
    }
    assert(active_count == 10);

    H6AData10 result;
    result.fingerprints.reserve(70000);
    for (uint16_t axes = 0; axes < 1024; ++axes) {
        int n1 = std::popcount(axes);
        if (n1 & 1) continue;
        int n0 = 10 - n1;
        Word baseline_word{};
        for (int j = 0; j < 10; ++j) {
            baseline_word[positions[j]] = active((axes >> j) & 1, 0);
        }
        Residue baseline = reduce_sixth(paf_residue(baseline_word));
        std::array<Residue, 10> columns{};
        for (int j = 0; j < 10; ++j) {
            Word changed = baseline_word;
            changed[positions[j]] = scale(changed[positions[j]], -1);
            columns[j] = h6_subtract(
                reduce_sixth(paf_residue(changed)), baseline
            );
        }

        uint16_t audit = uint16_t(((uint32_t(axes) + 1) * 0x025du) & 0x03ffu);
        Word audited_word = baseline_word;
        Residue predicted = baseline;
        for (int j = 0; j < 10; ++j) if ((audit >> j) & 1) {
            audited_word[positions[j]] = scale(audited_word[positions[j]], -1);
            predicted = h6_add(predicted, columns[j]);
        }
        assert(predicted == reduce_sixth(paf_residue(audited_word)));
        ++result.affine_audits;

        struct Partial {
            Residue residue{};
            int negative0 = 0;
            int negative1 = 0;
        };
        std::array<std::array<std::vector<Residue>, 6>, 6> right;
        for (uint16_t mask = 0; mask < 32; ++mask) {
            Partial part;
            for (int local = 0; local < 5; ++local) if ((mask >> local) & 1) {
                int j = 5 + local;
                part.residue = h6_add(part.residue, columns[j]);
                ((axes >> j) & 1 ? part.negative1 : part.negative0)++;
            }
            right[part.negative0][part.negative1].push_back(part.residue);
        }
        for (uint16_t mask = 0; mask < 32; ++mask) {
            Partial left;
            for (int j = 0; j < 5; ++j) if ((mask >> j) & 1) {
                left.residue = h6_add(left.residue, columns[j]);
                ((axes >> j) & 1 ? left.negative1 : left.negative0)++;
            }
            int need0 = n0 / 2 - left.negative0;
            int need1 = n1 / 2 - left.negative1;
            if (need0 < 0 || need0 > 5 || need1 < 0 || need1 > 5) continue;
            for (const Residue& right_residue : right[need0][need1]) {
                result.fingerprints.insert(h6_add(
                    baseline, h6_add(left.residue, right_residue)
                ));
                ++result.exact_assignments;
            }
        }
    }
    assert(result.exact_assignments == 63504);
    assert(result.affine_audits == 512);
    return result;
}

template <typename T>
void print_array(const std::array<T, 6>& values) {
    for (int j = 0; j < 6; ++j) {
        if (j) std::cout << ',';
        std::cout << values[j];
    }
    std::cout << '\n';
}

}  // namespace

#ifndef B10_FRONTIER_MAIN
#define B10_FRONTIER_MAIN main
#endif

int B10_FRONTIER_MAIN() {
    Inputs10 inputs = reconstruct_inputs10();
    std::array<long long, 6> a_counts = count_a_phase_patterns10();
    std::array<long long, 6> s_minus_min;
    std::array<long long, 6> s_minus_max{};
    std::array<long long, 6> s_plus_min;
    std::array<long long, 6> s_plus_max{};
    s_minus_min.fill(INT64_MAX);
    s_plus_min.fill(INT64_MAX);
    long long h_plus_min = INT64_MAX;
    long long h_plus_max = 0;
    long long h_minus_min = INT64_MAX;
    long long h_minus_max = 0;
    std::array<int, 6> positive_h_entries{};
    std::array<int, 6> negative_h_entries{};
    std::array<int, 6> positive_h_orbits{};
    std::array<int, 6> negative_h_orbits{};
    std::set<uint32_t> unique_a_supports;
    for (const Entry10& entry : inputs.entries) {
        std::array<long long, 6> s_minus = count_b_s_phase_patterns10(entry, -1);
        std::array<long long, 6> s_plus = count_b_s_phase_patterns10(entry, 1);
        long long h_plus = count_b_h_phase_patterns10(entry, 1);
        long long h_minus = count_b_h_phase_patterns10(entry, -1);
        for (int case_number = 0; case_number < 6; ++case_number) {
            s_minus_min[case_number] = std::min(s_minus_min[case_number], s_minus[case_number]);
            s_minus_max[case_number] = std::max(s_minus_max[case_number], s_minus[case_number]);
            s_plus_min[case_number] = std::min(s_plus_min[case_number], s_plus[case_number]);
            s_plus_max[case_number] = std::max(s_plus_max[case_number], s_plus[case_number]);

            // Cases 0,2,3 pair positive H center with S(0)=-i; the
            // remaining cases pair positive H center with S(0)=+i.
            bool positive_h_uses_minus_s =
                case_number == 0 || case_number == 2 || case_number == 3;
            long long positive_s = positive_h_uses_minus_s
                ? s_minus[case_number] : s_plus[case_number];
            long long negative_s = positive_h_uses_minus_s
                ? s_plus[case_number] : s_minus[case_number];
            bool positive_feasible = positive_s > 0 && h_plus > 0;
            bool negative_feasible = negative_s > 0 && h_minus > 0;
            assert(int(positive_feasible) + int(negative_feasible) == 1);
            if (positive_feasible) {
                ++positive_h_entries[case_number];
                positive_h_orbits[case_number] += entry.orbits;
            } else {
                ++negative_h_entries[case_number];
                negative_h_orbits[case_number] += entry.orbits;
            }
        }
        h_plus_min = std::min(h_plus_min, h_plus);
        h_plus_max = std::max(h_plus_max, h_plus);
        h_minus_min = std::min(h_minus_min, h_minus);
        h_minus_max = std::max(h_minus_max, h_minus);
        unique_a_supports.insert(
            inputs.representatives[entry.required_signature].begin(),
            inputs.representatives[entry.required_signature].end()
        );
    }

    std::vector<H6BData10> h6_b_data;
    h6_b_data.reserve(inputs.entries.size());
    int h6_b_fingerprint_min = INT32_MAX;
    int h6_b_fingerprint_max = 0;
    for (const Entry10& entry : inputs.entries) {
        H6BData10 data = enumerate_h6_b10(entry);
        int size = int(data.complements.size());
        h6_b_fingerprint_min = std::min(h6_b_fingerprint_min, size);
        h6_b_fingerprint_max = std::max(h6_b_fingerprint_max, size);
        h6_b_data.push_back(std::move(data));
    }
    std::map<uint32_t, std::vector<int>> entries_by_a_support;
    for (int entry_index = 0; entry_index < int(inputs.entries.size()); ++entry_index) {
        const Entry10& entry = inputs.entries[entry_index];
        for (uint32_t a_support : inputs.representatives[entry.required_signature]) {
            entries_by_a_support[a_support].push_back(entry_index);
        }
    }
    assert(entries_by_a_support.size() == 1972);
    int input_orbit_pairs = 0;
    for (const auto& [support, indices] : entries_by_a_support) {
        (void)support;
        input_orbit_pairs += int(indices.size());
    }
    assert(input_orbit_pairs == 2690);

    int h6_surviving_orbit_pairs = 0;
    std::set<uint32_t> h6_surviving_b_masks;
    std::vector<std::pair<uint32_t, uint32_t>> h6_frontier;
    long long h6_a_exact_assignments = 0;
    long long h6_affine_audits = 0;
    int completed_supports = 0;
    for (const auto& [a_support, entry_indices] : entries_by_a_support) {
        H6AData10 a_data = enumerate_h6_a10(a_support);
        h6_a_exact_assignments += a_data.exact_assignments;
        h6_affine_audits += a_data.affine_audits;
        for (int entry_index : entry_indices) {
            bool feasible = false;
            for (const Residue& complement : h6_b_data[entry_index].complements) {
                if (a_data.fingerprints.contains(complement)) {
                    feasible = true;
                    break;
                }
            }
            if (feasible) {
                ++h6_surviving_orbit_pairs;
                h6_surviving_b_masks.insert(inputs.entries[entry_index].b_word);
                h6_frontier.emplace_back(a_support, inputs.entries[entry_index].b_word);
            }
        }
        ++completed_supports;
        if (completed_supports % 100 == 0) {
            std::cerr << "completed_supports=" << completed_supports << "/1972"
                      << ";surviving_orbit_pairs=" << h6_surviving_orbit_pairs << "\n";
        }
    }

    std::cout << "input_b_masks=140\n"
              << "input_labeled_type_pairs=56490\n"
              << "input_rotation_orbits_per_case=2690\n"
              << "unique_a_supports=" << unique_a_supports.size() << "\n"
              << "a_exact_phase_assignments=";
    print_array(a_counts);
    std::cout << "s_b_fixed_minus_i_minima=";
    print_array(s_minus_min);
    std::cout << "s_b_fixed_minus_i_maxima=";
    print_array(s_minus_max);
    std::cout << "s_b_fixed_plus_i_minima=";
    print_array(s_plus_min);
    std::cout << "s_b_fixed_plus_i_maxima=";
    print_array(s_plus_max);
    std::cout << "h_b_fixed_plus_1_minmax=" << h_plus_min << ',' << h_plus_max << "\n"
              << "h_b_fixed_minus_1_minmax=" << h_minus_min << ',' << h_minus_max << "\n"
              << "positive_h_entry_counts=";
    print_array(positive_h_entries);
    std::cout << "negative_h_entry_counts=";
    print_array(negative_h_entries);
    std::cout << "positive_h_orbit_counts=";
    print_array(positive_h_orbits);
    std::cout << "negative_h_orbit_counts=";
    print_array(negative_h_orbits);
    std::cout << "orientation_resolved_by_exact_sums=verified\n"
              << "h6_b_fingerprint_range=" << h6_b_fingerprint_min << '-'
              << h6_b_fingerprint_max << "\n"
              << "h6_a_exact_assignments=" << h6_a_exact_assignments << "\n"
              << "h6_affine_audits=" << h6_affine_audits << "\n"
              << "h6_surviving_orbit_pairs=" << h6_surviving_orbit_pairs << "\n"
              << "h6_surviving_b_masks=" << h6_surviving_b_masks.size() << "\n"
              << "sixth_order_h_scan=verified\n";
    std::sort(h6_frontier.begin(), h6_frontier.end());
    for (const auto& [a_support, b_word] : h6_frontier) {
        std::cout << "frontier_pair=" << a_support << ',' << b_word << "\n";
    }
}
