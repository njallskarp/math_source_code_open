#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wreturn-type"
#endif
#define main embedded_b14_main
#include "../qlp42_q1_b14_sixth_order_s/independent_cpp.cpp"
#undef main
#if defined(__clang__)
#pragma clang diagnostic pop
#endif

namespace {

constexpr std::array<int, 6> B12_A_PHASES = {15876, 7056, 7056, 4536, 4536, 3024};

struct B12Entry {
    uint32_t b_word = 0;
    uint16_t required_signature = 0;
    std::array<int, 10> theta{};
    int labeled = 0;
    int orbits = 0;
};

struct B12Inputs {
    std::array<int, 1024> labeled{};
    std::array<std::set<uint32_t>, 1024> representatives;
    std::vector<B12Entry> entries;
};

B12Inputs reconstruct_b12_inputs() {
    B12Inputs result;
    for (uint32_t word = 0; word <= WORD_MASK; ++word) {
        if (std::popcount(word) != 9) continue;
        uint16_t signature = correlation_signature(word);
        ++result.labeled[signature];
        result.representatives[signature].insert(orbit_representative(word));
    }
    for (uint16_t bits = 0; bits < 1024; ++bits) {
        uint32_t b_word = symmetric_b_word(bits);
        if (std::popcount(b_word) != 12) continue;
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
    assert(result.entries.size() == 98);
    int labeled_pairs = 0;
    int orbit_pairs = 0;
    std::set<uint32_t> unique_representatives;
    for (const B12Entry& entry : result.entries) {
        labeled_pairs += entry.labeled;
        orbit_pairs += entry.orbits;
        unique_representatives.insert(
            result.representatives[entry.required_signature].begin(),
            result.representatives[entry.required_signature].end()
        );
    }
    assert(labeled_pairs == 76377);
    assert(orbit_pairs == 3637);
    assert(unique_representatives.size() == 2802);
    return result;
}

BData enumerate_b12(const B12Entry& entry) {
    BData data;
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) if ((entry.b_word >> shift) & 1) {
        shifts.push_back(shift);
    }
    assert(shifts.size() == 6);
    std::array<G, 6> targets{};
    for (int case_number = 0; case_number < 6; ++case_number) {
        targets[case_number] = sum_targets(CASES[case_number]).second;
        data.order_eight[case_number].reserve(15000);
    }
    constexpr std::array<uint16_t, 16> AUDITS = {
        0x1fffu, 0x1555u, 0x0aaau, 0x0ff0u,
        0x100fu, 0x1333u, 0x0cccu, 0x1579u,
        0x068au, 0x00ffu, 0x1f00u, 0x0555u,
        0x0aaau, 0x0481u, 0x0421u, 0x09c3u,
    };

    for (uint16_t axes = 0; axes < 64; ++axes) {
        Word word{};
        std::array<int, 13> sign_positions{};
        int variable = 0;
        for (int j = 0; j < 6; ++j) {
            int shift = shifts[j];
            int axis = (axes >> j) & 1;
            word[shift] = active(axis, 0);
            word[N - shift] = active(axis ^ entry.theta[shift - 1], 0);
            sign_positions[variable++] = shift;
            sign_positions[variable++] = N - shift;
        }
        word[0] = {0, -1};
        sign_positions[variable++] = 0;
        assert(variable == 13);

        Residue axis_value = paf_residue(word);
        std::array<Residue, 15> linear{};
        std::array<std::array<Residue, 15>, 15> quadratic{};
        for (int j = 0; j < 13; ++j) {
            Word changed = word;
            changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            linear[j] = residue_subtract(paf_residue(changed), axis_value);
            ++data.direct_checks;
        }
        for (int j = 0; j < 13; ++j) for (int k = j + 1; k < 13; ++k) {
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
            for (int j = 0; j < 13; ++j) if ((mask >> j) & 1) {
                changed[sign_positions[j]] = scale(changed[sign_positions[j]], -1);
            }
            Residue direct = residue_subtract(paf_residue(changed), axis_value);
            assert(direct == evaluate_quadratic(mask, linear, quadratic));
            ++data.direct_checks;
        }

        G baseline_sum{};
        std::array<G, 13> changes{};
        for (int j = 0; j < 13; ++j) {
            G value = word[sign_positions[j]];
            baseline_sum = add(baseline_sum, value);
            changes[j] = scale(value, -2);
        }
        std::array<G, 64> left_sums{};
        std::array<Residue, 64> left_residues{};
        for (uint16_t mask = 1; mask < 64; ++mask) {
            int j = std::countr_zero(mask);
            uint16_t rest = mask & (mask - 1);
            left_sums[mask] = add(left_sums[rest], changes[j]);
            Residue value = residue_add(left_residues[rest], linear[j]);
            for (int k = j + 1; k < 6; ++k) if ((rest >> k) & 1) {
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
            int j = 6 + local;
            uint16_t rest = mask & (mask - 1);
            right_sums[mask] = add(right_sums[rest], changes[j]);
            Residue value = residue_add(right_residues[rest], linear[j]);
            for (int k = j + 1; k < 13; ++k) if ((rest >> (k - 6)) & 1) {
                value = residue_add(value, quadratic[j][k]);
            }
            right_residues[mask] = value;
            right_by_sum[right_sums[mask]].push_back(uint8_t(mask));
        }
        std::array<std::array<Residue, 128>, 6> cross_columns{};
        for (int j = 0; j < 6; ++j) for (uint16_t mask = 1; mask < 128; ++mask) {
            int local = std::countr_zero(mask);
            uint16_t rest = mask & (mask - 1);
            cross_columns[j][mask] = residue_add(
                cross_columns[j][rest], quadratic[j][6 + local]
            );
        }
        for (uint16_t left = 0; left < 64; ++left) {
            for (int case_number = 0; case_number < 6; ++case_number) {
                G required = sub(sub(targets[case_number], baseline_sum), left_sums[left]);
                auto found = right_by_sum.find(required);
                if (found == right_by_sum.end()) continue;
                for (uint8_t right : found->second) {
                    Residue value = residue_add(
                        axis_value,
                        residue_add(left_residues[left], right_residues[right])
                    );
                    for (int j = 0; j < 6; ++j) if ((left >> j) & 1) {
                        value = residue_add(value, cross_columns[j][right]);
                    }
                    ++data.exact_assignments[case_number];
                    data.order_eight[case_number].insert(value);
                }
            }
        }
    }
    assert(data.direct_checks == 6848);
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

struct PhasePattern {
    std::array<G, 9> values{};
    uint8_t cases = 0;
};

std::vector<PhasePattern> phase_patterns_b12() {
    std::array<G, 6> targets{};
    for (int case_number = 0; case_number < 6; ++case_number) {
        targets[case_number] = sum_targets(CASES[case_number]).first;
    }
    std::vector<PhasePattern> result;
    std::array<int, 6> counts{};
    for (int code = 0; code < (1 << 18); ++code) {
        int encoded = code;
        PhasePattern pattern;
        G sum{};
        for (int j = 0; j < 9; ++j) {
            int root = encoded & 3;
            encoded >>= 2;
            pattern.values[j] = active(root >> 1, root & 1);
            sum = add(sum, pattern.values[j]);
        }
        for (int case_number = 0; case_number < 6; ++case_number) if (sum == targets[case_number]) {
            pattern.cases |= uint8_t{1} << case_number;
            ++counts[case_number];
        }
        if (pattern.cases) result.push_back(pattern);
    }
    assert(counts == B12_A_PHASES);
    assert(result.size() == 30492);
    return result;
}

AData enumerate_a12(uint32_t support_word, const std::vector<PhasePattern>& patterns) {
    std::array<int, 9> support{};
    int count = 0;
    for (int position = 0; position < N; ++position) if ((support_word >> position) & 1) {
        support[count++] = position;
    }
    assert(count == 9);
    std::array<int, N> index;
    index.fill(-1);
    for (int j = 0; j < 9; ++j) index[support[j]] = j;
    AData result;
    for (const PhasePattern& pattern : patterns) {
        Residue residue;
        for (int shift = 1; shift <= 10; ++shift) {
            G value{};
            for (int left = 0; left < 9; ++left) {
                int right = index[(support[left] + shift) % N];
                if (right >= 0) {
                    value = add(value, mul(pattern.values[left], conj(pattern.values[right])));
                }
            }
            set_coordinate(residue, shift - 1, value);
        }
        for (int case_number = 0; case_number < 6; ++case_number) {
            if ((pattern.cases >> case_number) & 1) {
                result.residues[case_number].push_back(residue);
            }
        }
    }
    for (int case_number = 0; case_number < 6; ++case_number) {
        assert(int(result.residues[case_number].size()) == B12_A_PHASES[case_number]);
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    bool quiet = argc == 2 && std::string(argv[1]) == "--quiet";
    B12Inputs inputs = reconstruct_b12_inputs();
    std::vector<PhasePattern> patterns = phase_patterns_b12();
    Residue target = target_residue();
    std::array<std::array<int, 6>, 3> surviving_orbits{};
    std::array<std::array<std::set<uint32_t>, 6>, 3> surviving_masks;
    std::array<int, 3> surviving_rows{};
    std::array<std::set<long long>, 6> exact_counts;
    long long direct_checks = 0;
    long long classified_rows = 0;

    int entry_number = 0;
    for (const B12Entry& entry : inputs.entries) {
        ++entry_number;
        BData b_data = enumerate_b12(entry);
        direct_checks += b_data.direct_checks;
        for (int case_number = 0; case_number < 6; ++case_number) {
            exact_counts[case_number].insert(b_data.exact_assignments[case_number]);
        }
        for (uint32_t a_word : inputs.representatives[entry.required_signature]) {
            AData a_data = enumerate_a12(a_word, patterns);
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
            }
            for (int order = 0; order < 3; ++order) {
                surviving_rows[order] += int(row_survives[order]);
            }
            ++classified_rows;
        }
        if (!quiet) {
            std::cout << "completed_b_mask=" << entry_number << "/98;"
                      << "eighth_survivor_rows=" << surviving_rows[2] << '\n';
        }
    }

    const std::array<std::array<int, 6>, 2> expected_orbits = {{
        {1686, 1398, 1427, 850, 850, 304},
        {303, 180, 92, 5, 5, 0},
    }};
    const std::array<std::array<int, 6>, 2> expected_masks = {{
        {98, 89, 88, 98, 98, 80},
        {29, 27, 20, 3, 3, 0},
    }};
    for (int order = 0; order < 2; ++order) {
        assert(surviving_orbits[order] == expected_orbits[order]);
        for (int case_number = 0; case_number < 6; ++case_number) {
            assert(int(surviving_masks[order][case_number].size())
                   == expected_masks[order][case_number]);
        }
    }
    assert(surviving_rows[0] == 2523);
    assert(surviving_rows[1] == 499);
    assert(classified_rows == 3637);
    assert(direct_checks == 671104);

    std::cout << "input_b_masks=98\n"
              << "input_labeled_type_pairs=76377\n"
              << "input_rotation_orbits_per_case=3637\n"
              << "sixth_order_surviving_orbits=1686,1398,1427,850,850,304\n"
              << "seventh_order_surviving_orbits=303,180,92,5,5,0\n"
              << "eighth_order_surviving_orbits=";
    for (int case_number = 0; case_number < 6; ++case_number) {
        if (case_number) std::cout << ',';
        std::cout << surviving_orbits[2][case_number];
    }
    std::cout << "\neighth_order_surviving_masks=";
    for (int case_number = 0; case_number < 6; ++case_number) {
        if (case_number) std::cout << ',';
        std::cout << surviving_masks[2][case_number].size();
    }
    std::cout << "\nsixth_survivor_rows=" << surviving_rows[0]
              << "\nseventh_survivor_rows=" << surviving_rows[1]
              << "\neighth_survivor_rows=" << surviving_rows[2]
              << "\nquadratic_interpolation_direct_audits=" << direct_checks
              << "\nindependent_cpp_certificate=verified\n";
}
