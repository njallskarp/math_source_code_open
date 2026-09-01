#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wreturn-type"
#endif
#define B12_H_MAIN embedded_b12_h_main
#include "prototype_sixth_h.cpp"
#undef B12_H_MAIN
#if defined(__clang__)
#pragma clang diagnostic pop
#endif

namespace {

struct RemainingRow {
    uint32_t a_word = 0;
    uint32_t b_word = 0;
    uint8_t cases = 0;
};

struct HAFingerprints {
    std::unordered_set<Residue, ResidueHash> values;
    long long exact_assignments = 0;
    long long affine_audits = 0;
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

        uint16_t audit_mask = uint16_t(((uint32_t(axes) + 1) * 0x9e37u) & 0x0fffu);
        Residue predicted = baseline;
        for (int j = 0; j < 12; ++j) if ((audit_mask >> j) & 1) {
            predicted = h_add(predicted, columns[j]);
        }
        assert(predicted == reduce_sixth(
            paf_residue(h_a_word(positions, axes, audit_mask))
        ));
        ++result.affine_audits;

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
    assert(result.affine_audits == 2048);
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    bool quiet = false;
    bool dump_frontier = false;
    int support_limit = -1;
    for (int j = 1; j < argc; ++j) {
        std::string argument = argv[j];
        if (argument == "--quiet") quiet = true;
        else if (argument == "--dump-frontier") dump_frontier = true;
        else if (argument == "--limit-supports" && j + 1 < argc) {
            support_limit = std::stoi(argv[++j]);
        } else {
            assert(false && "unknown argument");
        }
    }

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
    if (dump_frontier) {
        std::cout << "a_s_word\tb_s_word\tcases\n";
        for (const auto& [pair, cases] : row_cases) {
            std::cout << pair.first << '\t' << pair.second << '\t'
                      << int(cases) << '\n';
        }
        return 0;
    }
    int input_incidences = 0;
    std::map<uint32_t, std::vector<RemainingRow>> by_support;
    for (const auto& [pair, cases] : row_cases) {
        input_incidences += std::popcount(cases);
        by_support[pair.first].push_back({pair.first, pair.second, cases});
    }
    assert(input_incidences == 395);
    assert(by_support.size() == 345);

    std::array<int, 6> surviving_orbits{};
    std::array<std::set<uint32_t>, 6> surviving_masks;
    int surviving_rows = 0;
    int supports_completed = 0;
    long long exact_assignments = 0;
    long long affine_audits = 0;
    size_t minimum_fingerprints = SIZE_MAX;
    size_t maximum_fingerprints = 0;
    for (const auto& [a_word, rows] : by_support) {
        if (support_limit >= 0 && supports_completed >= support_limit) break;
        HAFingerprints a_data = enumerate_h_a_fingerprints(a_word);
        exact_assignments += a_data.exact_assignments;
        affine_audits += a_data.affine_audits;
        minimum_fingerprints = std::min(minimum_fingerprints, a_data.values.size());
        maximum_fingerprints = std::max(maximum_fingerprints, a_data.values.size());
        for (const RemainingRow& row : rows) {
            bool feasible = false;
            const auto& targets = b_targets_by_word.at(row.b_word);
            for (const HTarget& target : targets) {
                if (a_data.values.contains(target.complement)) {
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

    std::cout << "input_case02_orbit_incidences=395\n"
              << "input_case02_rows=375\n"
              << "input_unique_a_supports=345\n"
              << "input_unique_b_masks=29\n"
              << "supports_completed=" << supports_completed << "\n"
              << "sixth_h_surviving_case0_orbits=" << surviving_orbits[0] << "\n"
              << "sixth_h_surviving_case2_orbits=" << surviving_orbits[2] << "\n"
              << "sixth_h_surviving_case0_masks=" << surviving_masks[0].size() << "\n"
              << "sixth_h_surviving_case2_masks=" << surviving_masks[2].size() << "\n"
              << "sixth_h_surviving_rows=" << surviving_rows << "\n"
              << "h_a_fingerprint_range=" << minimum_fingerprints << '-'
              << maximum_fingerprints << "\n"
              << "h_a_exact_assignments=" << exact_assignments << "\n"
              << "h_a_affine_direct_audits=" << affine_audits << "\n";
    if (support_limit < 0) {
        assert(supports_completed == 345);
        assert(exact_assignments == 345LL * 853776);
        assert(affine_audits == 345LL * 2048);
        std::cout << "full_precomputed_certificate=verified\n";
    } else {
        std::cout << "partial_precomputed_certificate=verified\n";
    }
    return 0;
}
