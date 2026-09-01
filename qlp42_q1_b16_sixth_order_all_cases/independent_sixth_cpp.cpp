#define main embedded_case5_main
#include "../qlp42_q1_b16_sixth_order_s/verify_sixth_s.cpp"
#undef main

#include <optional>

namespace {

constexpr std::array<std::array<int, 4>, 5> GENERAL_CASES = {{
    {1, 0, 5, 0},
    {3, 0, 4, 1},
    {3, 0, 3, -2},
    {3, 2, 3, 2},
    {3, 2, 2, 3},
}};

std::pair<G, G> exact_sum_targets(const std::array<int, 4>& values) {
    auto [p, q, x, y] = values;
    return {{p + q, q - p}, {x + y - 1, y - x}};
}

BData enumerate_b_for_sum(uint32_t b_word, G target_sum) {
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
        G required = sub(target_sum, baseline_sum);

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
        for (int j = 0; j < 8; ++j) for (uint32_t mask = 1; mask < 512; ++mask) {
            int local = __builtin_ctz(mask);
            uint32_t rest = mask & (mask - 1);
            cross_columns[j][mask] = residue_add(
                cross_columns[j][rest], quadratic[j][8 + local]);
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
                data.states.try_emplace(residue_key(delta), BState{delta});
            }
        }
    }
    assert(data.direct_checks == 43264);
    return data;
}

std::vector<Word> exact_a_words(const std::vector<int>& positions, G target) {
    assert(positions.size() == 5);
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
        if (sum == target) result.push_back(word);
    }
    return result;
}

struct GeneralRow {
    std::string equal;
    std::string opposite;
    int rank = 0;
    uint32_t b_word = 0;
    std::vector<int> a_positions;
};

}  // namespace


int main(int argc, char** argv) {
    bool dump = argc == 2 && std::string(argv[1]) == "--dump-table";
    std::ifstream input("input_orbits.tsv");
    assert(input);
    std::string line;
    std::getline(input, line);
    std::vector<GeneralRow> rows;
    while (std::getline(input, line)) {
        auto fields = split_tabs(line);
        assert(fields.size() == 3);
        uint32_t equal_word = 0;
        for (int position : parse_positions(fields[0])) equal_word |= uint32_t{1} << position;
        rows.push_back({
            fields[0], fields[1], std::stoi(fields[2]), WORD_MASK ^ equal_word ^ uint32_t{1},
            parse_positions(fields[1]),
        });
    }
    assert(rows.size() == 32);
    if (dump) {
        std::cout << "b_equal_positions\ta_opposite_orbit_representative\tfourth_order_rank"
                     "\tsixth_s_feasible_cases\tb_residue_counts\n";
    }
    std::array<int, 5> orbit_counts{};
    std::array<std::set<uint32_t>, 5> mask_counts;
    std::array<std::set<long long>, 5> assignment_counts;
    long long direct_checks = 0;
    std::map<uint32_t, std::vector<size_t>> grouped;
    for (size_t j = 0; j < rows.size(); ++j) grouped[rows[j].b_word].push_back(j);
    assert(grouped.size() == 18);
    std::vector<std::array<int, 5>> row_feasible(rows.size());
    std::vector<std::array<size_t, 5>> row_residue_counts(rows.size());
    std::array<int, 5> a_pattern_counts{};

    for (auto& [b_word, indices] : grouped) {
        for (int case_number = 0; case_number < 5; ++case_number) {
            auto [target_a, target_b] = exact_sum_targets(GENERAL_CASES[case_number]);
            BData b_data = enumerate_b_for_sum(b_word, target_b);
            direct_checks += b_data.direct_checks;
            assignment_counts[case_number].insert(b_data.exact_assignments);
            for (size_t index : indices) {
                Word a_baseline{};
                for (int position : rows[index].a_positions) a_baseline[position] = active(0, 0);
                Residue combined_baseline = combined_fingerprint(a_baseline, b_data.baseline);
                auto words = exact_a_words(rows[index].a_positions, target_a);
                a_pattern_counts[case_number] = words.size();
                bool feasible = false;
                for (const Word& word : words) {
                    Residue required = residue_negate(residue_add(
                        combined_baseline, quotient_fingerprint(word, a_baseline)));
                    if (b_data.states.contains(residue_key(required))) {
                        feasible = true;
                        break;
                    }
                }
                row_feasible[index][case_number] = int(feasible);
                row_residue_counts[index][case_number] = b_data.states.size();
                if (feasible) {
                    ++orbit_counts[case_number];
                    mask_counts[case_number].insert(b_word);
                }
            }
        }
    }
    if (dump) {
        for (size_t index = 0; index < rows.size(); ++index) {
            std::cout << rows[index].equal << '\t' << rows[index].opposite << '\t'
                      << rows[index].rank << '\t';
            bool first = true;
            for (int case_number = 0; case_number < 5; ++case_number) {
                if (!row_feasible[index][case_number]) continue;
                if (!first) std::cout << ',';
                std::cout << case_number;
                first = false;
            }
            if (first) std::cout << '-';
            std::cout << '\t';
            for (int case_number = 0; case_number < 5; ++case_number) {
                if (case_number) std::cout << ',';
                std::cout << row_residue_counts[index][case_number];
            }
            std::cout << '\n';
        }
        return 0;
    }
    std::cout << "direct_interpolation_and_audit_checks=" << direct_checks << '\n';
    for (int case_number = 0; case_number < 5; ++case_number) {
        assert(assignment_counts[case_number].size() == 1);
        std::cout << "case_" << case_number
                  << "_a_phase_assignments=" << a_pattern_counts[case_number]
                  << " b_exact_assignments=" << *assignment_counts[case_number].begin()
                  << " surviving_orbits=" << orbit_counts[case_number]
                  << " surviving_masks=" << mask_counts[case_number].size() << '\n';
    }
    assert((orbit_counts == std::array<int, 5>{0, 2, 0, 0, 0}));
    std::cout << "certificate=verified\n";
}
