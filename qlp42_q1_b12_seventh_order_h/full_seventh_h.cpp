#define B12_H_MAIN embedded_sixth_h_main
#include "../qlp42_q1_b12_sixth_order_h/prototype_sixth_h.cpp"
#undef B12_H_MAIN

namespace {

struct RemainingRow {
    uint32_t a_word = 0;
    uint32_t b_word = 0;
    uint8_t cases = 0;
};

struct HAFingerprints {
    std::unordered_set<Residue, ResidueHash> values;
    long long exact_assignments = 0;
};

HAFingerprints enumerate_h_a_fingerprints(uint32_t s_support) {
    std::array<int, 12> positions{};
    int active_count = 0;
    for (int position = 0; position < N; ++position) {
        if (((s_support >> position) & 1) == 0) positions[active_count++] = position;
    }
    assert(active_count == 12);

    HAFingerprints result;
    result.values.reserve(150000);
    for (uint16_t axes = 0; axes < (uint16_t{1} << 12); ++axes) {
        int n1 = std::popcount(axes);
        if (n1 & 1) continue;
        int n0 = 12 - n1;
        Word baseline_word = h_a_word(positions, axes, 0);
        Residue baseline = reduce_sixth(paf_residue(baseline_word));
        std::array<Residue, 12> columns{};
        for (int j = 0; j < 12; ++j) {
            Word changed = baseline_word;
            changed[positions[j]] = scale(changed[positions[j]], -1);
            columns[j] = h_subtract(reduce_sixth(paf_residue(changed)), baseline);
        }

        std::array<Residue, 64> left_residues{};
        std::array<int, 64> left_negative0{};
        std::array<int, 64> left_negative1{};
        for (uint16_t mask = 1; mask < 64; ++mask) {
            int local = std::countr_zero(mask);
            uint16_t rest = mask & (mask - 1);
            left_residues[mask] = h_add(left_residues[rest], columns[local]);
            left_negative0[mask] = left_negative0[rest];
            left_negative1[mask] = left_negative1[rest];
            ((axes >> local) & 1 ? left_negative1[mask] : left_negative0[mask])++;
        }

        std::array<std::array<std::vector<Residue>, 7>, 7> right;
        for (uint16_t mask = 0; mask < 64; ++mask) {
            Residue residue{};
            int negative0 = 0;
            int negative1 = 0;
            for (int local = 0; local < 6; ++local) if ((mask >> local) & 1) {
                int index = 6 + local;
                residue = h_add(residue, columns[index]);
                ((axes >> index) & 1 ? negative1 : negative0)++;
            }
            right[negative0][negative1].push_back(residue);
        }

        for (uint16_t left = 0; left < 64; ++left) {
            int need0 = n0 / 2 - left_negative0[left];
            int need1 = n1 / 2 - left_negative1[left];
            if (need0 < 0 || need0 > 6 || need1 < 0 || need1 > 6) continue;
            Residue partial = h_add(baseline, left_residues[left]);
            for (const Residue& right_residue : right[need0][need1]) {
                result.values.insert(h_add(partial, right_residue));
                ++result.exact_assignments;
            }
        }
    }
    assert(result.exact_assignments == 853776);
    return result;
}

struct SeventhBData {
    std::unordered_set<Residue, ResidueHash> complements;
    int exact_assignments = 0;
};

struct SeventhAData {
    std::unordered_set<Residue, ResidueHash> values;
    long long exact_assignments = 0;
    long long direct_checks = 0;
    long long quadratic_audits = 0;
};

struct SixthFrontier {
    std::vector<RemainingRow> rows;
    int orbit_incidences = 0;
};

Residue seventh_target_raw() {
    Residue result;
    for (int shift = 1; shift <= 10; ++shift) {
        set_coordinate(result, shift - 1, {-2, 0});
    }
    return result;
}

SeventhBData enumerate_h_b_seventh(const B12Entry& entry) {
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) {
        if (((entry.b_word >> shift) & 1) == 0) shifts.push_back(shift);
    }
    assert(shifts.size() == 4);
    Residue target = seventh_target_raw();
    SeventhBData result;
    for (uint16_t axes = 0; axes < 16; ++axes) {
        Word baseline{};
        std::array<int, 8> positions{};
        int count = 0;
        for (int j = 0; j < 4; ++j) {
            int shift = shifts[j];
            int axis = (axes >> j) & 1;
            baseline[shift] = active(axis, 0);
            baseline[N - shift] = active(axis ^ entry.theta[shift - 1], 0);
            positions[count++] = shift;
            positions[count++] = N - shift;
        }
        baseline[0] = {1, 0};
        assert(count == 8);
        for (uint16_t signs = 0; signs < 256; ++signs) {
            Word word = baseline;
            for (int j = 0; j < 8; ++j) if ((signs >> j) & 1) {
                word[positions[j]] = scale(word[positions[j]], -1);
            }
            if (word_sum(word) != G{1, 0}) continue;
            ++result.exact_assignments;
            result.complements.insert(reduce_seventh(
                residue_subtract(target, paf_residue(word))
            ));
        }
    }
    assert(result.exact_assignments >= 608);
    assert(result.exact_assignments <= 676);
    return result;
}

SeventhAData enumerate_h_a_seventh(uint32_t s_support) {
    std::array<int, 12> positions{};
    int active_count = 0;
    for (int position = 0; position < N; ++position) {
        if (((s_support >> position) & 1) == 0) positions[active_count++] = position;
    }
    assert(active_count == 12);

    SeventhAData result;
    result.values.reserve(700000);
    for (uint16_t axes = 0; axes < (uint16_t{1} << 12); ++axes) {
        int n1 = std::popcount(axes);
        if (n1 & 1) continue;
        int n0 = 12 - n1;
        Word baseline_word = h_a_word(positions, axes, 0);
        Residue baseline = paf_residue(baseline_word);
        std::array<Residue, 15> linear{};
        std::array<std::array<Residue, 15>, 15> quadratic{};
        for (int j = 0; j < 12; ++j) {
            Word changed = baseline_word;
            changed[positions[j]] = scale(changed[positions[j]], -1);
            linear[j] = residue_subtract(paf_residue(changed), baseline);
            ++result.direct_checks;
        }
        for (int j = 0; j < 12; ++j) for (int k = j + 1; k < 12; ++k) {
            Word changed = baseline_word;
            changed[positions[j]] = scale(changed[positions[j]], -1);
            changed[positions[k]] = scale(changed[positions[k]], -1);
            quadratic[j][k] = residue_subtract(
                residue_subtract(
                    residue_subtract(paf_residue(changed), baseline), linear[j]
                ),
                linear[k]
            );
            ++result.direct_checks;
        }

        uint16_t audit_mask = uint16_t(((uint32_t(axes) + 1) * 0x9e37u) & 0x0fffu);
        Word audited = baseline_word;
        for (int j = 0; j < 12; ++j) if ((audit_mask >> j) & 1) {
            audited[positions[j]] = scale(audited[positions[j]], -1);
        }
        assert(
            residue_subtract(paf_residue(audited), baseline)
            == evaluate_quadratic(audit_mask, linear, quadratic)
        );
        ++result.direct_checks;
        ++result.quadratic_audits;

        std::array<G, 64> left_sums{};
        std::array<Residue, 64> left_residues{};
        std::array<int, 64> left_negative0{};
        std::array<int, 64> left_negative1{};
        for (uint16_t mask = 1; mask < 64; ++mask) {
            int j = std::countr_zero(mask);
            uint16_t rest = mask & (mask - 1);
            G change = scale(baseline_word[positions[j]], -2);
            left_sums[mask] = add(left_sums[rest], change);
            Residue value = residue_add(left_residues[rest], linear[j]);
            for (int k = j + 1; k < 6; ++k) if ((rest >> k) & 1) {
                value = residue_add(value, quadratic[j][k]);
            }
            left_residues[mask] = value;
            left_negative0[mask] = left_negative0[rest];
            left_negative1[mask] = left_negative1[rest];
            ((axes >> j) & 1 ? left_negative1[mask] : left_negative0[mask])++;
        }

        std::array<Residue, 64> right_residues{};
        std::array<int, 64> right_negative0{};
        std::array<int, 64> right_negative1{};
        std::array<std::array<std::vector<uint8_t>, 7>, 7> right_by_count;
        right_by_count[0][0].push_back(0);
        for (uint16_t mask = 1; mask < 64; ++mask) {
            int local = std::countr_zero(mask);
            int j = 6 + local;
            uint16_t rest = mask & (mask - 1);
            Residue value = residue_add(right_residues[rest], linear[j]);
            for (int k = j + 1; k < 12; ++k) if ((rest >> (k - 6)) & 1) {
                value = residue_add(value, quadratic[j][k]);
            }
            right_residues[mask] = value;
            right_negative0[mask] = right_negative0[rest];
            right_negative1[mask] = right_negative1[rest];
            ((axes >> j) & 1 ? right_negative1[mask] : right_negative0[mask])++;
            right_by_count[right_negative0[mask]][right_negative1[mask]].push_back(
                uint8_t(mask)
            );
        }

        std::array<std::array<Residue, 64>, 6> cross_columns{};
        for (int j = 0; j < 6; ++j) for (uint16_t mask = 1; mask < 64; ++mask) {
            int local = std::countr_zero(mask);
            uint16_t rest = mask & (mask - 1);
            cross_columns[j][mask] = residue_add(
                cross_columns[j][rest], quadratic[j][6 + local]
            );
        }

        for (uint16_t left = 0; left < 64; ++left) {
            int need0 = n0 / 2 - left_negative0[left];
            int need1 = n1 / 2 - left_negative1[left];
            if (need0 < 0 || need0 > 6 || need1 < 0 || need1 > 6) continue;
            for (uint8_t right : right_by_count[need0][need1]) {
                Residue value = residue_add(
                    baseline, residue_add(left_residues[left], right_residues[right])
                );
                for (int j = 0; j < 6; ++j) if ((left >> j) & 1) {
                    value = residue_add(value, cross_columns[j][right]);
                }
                result.values.insert(reduce_seventh(value));
                ++result.exact_assignments;
            }
        }
    }
    assert(result.exact_assignments == 853776);
    assert(result.direct_checks == 2048LL * 79);
    assert(result.quadratic_audits == 2048);
    return result;
}

SixthFrontier reconstruct_sixth_frontier() {
    B12Inputs inputs = reconstruct_b12_inputs();
    std::vector<PhasePattern> patterns = phase_patterns_b12();
    Residue s_target = target_residue();
    std::map<std::pair<uint32_t, uint32_t>, uint8_t> row_cases;
    std::unordered_map<uint32_t, std::vector<HTarget>> b_targets_by_word;
    for (const B12Entry& entry : inputs.entries) {
        BData s_b_data = enumerate_b12(entry);
        HBData h_b_data = enumerate_h_b(entry);
        assert(h_b_data.exact_assignments[1] == 0);
        b_targets_by_word.emplace(entry.b_word, std::move(h_b_data.targets[0]));
        for (uint32_t a_word : inputs.representatives[entry.required_signature]) {
            AData s_a_data = enumerate_a12(a_word, patterns);
            for (int case_number : {0, 2}) {
                bool eighth_feasible = false;
                for (const Residue& a_value : s_a_data.residues[case_number]) {
                    Residue needed = residue_subtract(s_target, a_value);
                    if (s_b_data.order_eight[case_number].contains(needed)) {
                        eighth_feasible = true;
                        break;
                    }
                }
                if (eighth_feasible) {
                    row_cases[{a_word, entry.b_word}] |= uint8_t{1} << case_number;
                }
            }
        }
    }
    assert(row_cases.size() == 375);

    std::map<uint32_t, std::vector<RemainingRow>> by_support;
    for (const auto& [pair, cases] : row_cases) {
        by_support[pair.first].push_back({pair.first, pair.second, cases});
    }
    SixthFrontier result;
    for (const auto& [a_word, rows] : by_support) {
        HAFingerprints a_data = enumerate_h_a_fingerprints(a_word);
        for (const RemainingRow& row : rows) {
            bool feasible = false;
            for (const HTarget& target : b_targets_by_word.at(row.b_word)) {
                if (a_data.values.contains(target.complement)) {
                    feasible = true;
                    break;
                }
            }
            if (!feasible) continue;
            result.rows.push_back(row);
            result.orbit_incidences += std::popcount(row.cases);
        }
    }
    assert(result.rows.size() == 77);
    assert(result.orbit_incidences == 79);
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    bool dump_sixth_frontier = false;
    bool quiet = false;
    for (int j = 1; j < argc; ++j) {
        std::string argument = argv[j];
        if (argument == "--dump-sixth-frontier") dump_sixth_frontier = true;
        else if (argument == "--quiet") quiet = true;
        else assert(false && "unknown argument");
    }

    SixthFrontier frontier = reconstruct_sixth_frontier();
    if (dump_sixth_frontier) {
        std::cout << "a_s_word\tb_s_word\tcases\n";
        for (const RemainingRow& row : frontier.rows) {
            std::cout << row.a_word << '\t' << row.b_word << '\t'
                      << int(row.cases) << '\n';
        }
        return 0;
    }

    B12Inputs inputs = reconstruct_b12_inputs();
    std::unordered_map<uint32_t, B12Entry> entries_by_word;
    for (const B12Entry& entry : inputs.entries) {
        entries_by_word.emplace(entry.b_word, entry);
    }
    std::map<uint32_t, std::vector<RemainingRow>> by_support;
    std::set<uint32_t> input_b_masks;
    for (const RemainingRow& row : frontier.rows) {
        by_support[row.a_word].push_back(row);
        input_b_masks.insert(row.b_word);
    }

    std::unordered_map<uint32_t, SeventhBData> b_data;
    size_t minimum_b_fingerprints = SIZE_MAX;
    size_t maximum_b_fingerprints = 0;
    int minimum_b_exact = INT32_MAX;
    int maximum_b_exact = 0;
    for (uint32_t b_word : input_b_masks) {
        SeventhBData data = enumerate_h_b_seventh(entries_by_word.at(b_word));
        minimum_b_fingerprints = std::min(minimum_b_fingerprints, data.complements.size());
        maximum_b_fingerprints = std::max(maximum_b_fingerprints, data.complements.size());
        minimum_b_exact = std::min(minimum_b_exact, data.exact_assignments);
        maximum_b_exact = std::max(maximum_b_exact, data.exact_assignments);
        b_data.emplace(b_word, std::move(data));
    }

    std::array<int, 6> surviving_orbits{};
    std::array<std::set<uint32_t>, 6> surviving_masks;
    int surviving_rows = 0;
    int supports_completed = 0;
    long long exact_assignments = 0;
    long long direct_checks = 0;
    long long quadratic_audits = 0;
    size_t minimum_a_fingerprints = SIZE_MAX;
    size_t maximum_a_fingerprints = 0;
    for (const auto& [a_word, rows] : by_support) {
        SeventhAData a_data = enumerate_h_a_seventh(a_word);
        exact_assignments += a_data.exact_assignments;
        direct_checks += a_data.direct_checks;
        quadratic_audits += a_data.quadratic_audits;
        minimum_a_fingerprints = std::min(minimum_a_fingerprints, a_data.values.size());
        maximum_a_fingerprints = std::max(maximum_a_fingerprints, a_data.values.size());
        for (const RemainingRow& row : rows) {
            bool feasible = false;
            for (const Residue& complement : b_data.at(row.b_word).complements) {
                if (a_data.values.contains(complement)) {
                    feasible = true;
                    break;
                }
            }
            if (!feasible) continue;
            ++surviving_rows;
            for (int case_number : {0, 2}) if ((row.cases >> case_number) & 1) {
                ++surviving_orbits[case_number];
                surviving_masks[case_number].insert(row.b_word);
            }
        }
        ++supports_completed;
        if (!quiet) {
            std::cout << "completed_a_support=" << supports_completed << '/'
                      << by_support.size() << ";surviving_rows=" << surviving_rows
                      << '\n';
        }
    }

    std::cout << "input_sixth_h_orbit_incidences=" << frontier.orbit_incidences << "\n"
              << "input_sixth_h_rows=" << frontier.rows.size() << "\n"
              << "input_unique_a_supports=" << by_support.size() << "\n"
              << "input_unique_b_masks=" << input_b_masks.size() << "\n"
              << "supports_completed=" << supports_completed << "\n"
              << "seventh_h_surviving_case0_orbits=" << surviving_orbits[0] << "\n"
              << "seventh_h_surviving_case2_orbits=" << surviving_orbits[2] << "\n"
              << "seventh_h_surviving_case0_masks=" << surviving_masks[0].size() << "\n"
              << "seventh_h_surviving_case2_masks=" << surviving_masks[2].size() << "\n"
              << "seventh_h_surviving_rows=" << surviving_rows << "\n"
              << "h_a_seventh_fingerprint_range=" << minimum_a_fingerprints << '-'
              << maximum_a_fingerprints << "\n"
              << "h_b_seventh_fingerprint_range=" << minimum_b_fingerprints << '-'
              << maximum_b_fingerprints << "\n"
              << "h_b_exact_assignment_range=" << minimum_b_exact << '-'
              << maximum_b_exact << "\n"
              << "h_a_exact_assignments=" << exact_assignments << "\n"
              << "h_a_quadratic_direct_checks=" << direct_checks << "\n"
              << "h_a_quadratic_global_audits=" << quadratic_audits << "\n"
              << "full_seventh_h_certificate=verified\n";
    return 0;
}
