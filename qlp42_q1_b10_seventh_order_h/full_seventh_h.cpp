#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define B10_FRONTIER_MAIN embedded_b10_sixth_h_main
#include "../qlp42_q1_b10_frontier/explore_b10.cpp"
#undef B10_FRONTIER_MAIN
#pragma GCC diagnostic pop

namespace {

struct FrontierRow10 {
    uint32_t a_support = 0;
    uint32_t b_word = 0;
};

struct SixthFrontier10 {
    Inputs10 inputs;
    std::vector<FrontierRow10> rows;
};

SixthFrontier10 reconstruct_sixth_frontier10() {
    SixthFrontier10 result;
    result.inputs = reconstruct_inputs10();
    std::vector<H6BData10> b_data;
    b_data.reserve(result.inputs.entries.size());
    for (const Entry10& entry : result.inputs.entries) {
        b_data.push_back(enumerate_h6_b10(entry));
    }
    std::map<uint32_t, std::vector<int>> entries_by_support;
    for (int entry_index = 0;
         entry_index < int(result.inputs.entries.size()); ++entry_index) {
        const Entry10& entry = result.inputs.entries[entry_index];
        for (uint32_t support : result.inputs.representatives[entry.required_signature]) {
            entries_by_support[support].push_back(entry_index);
        }
    }
    assert(entries_by_support.size() == 1972);
    for (const auto& [support, entry_indices] : entries_by_support) {
        H6AData10 a_data = enumerate_h6_a10(support);
        for (int entry_index : entry_indices) {
            bool feasible = false;
            for (const Residue& complement : b_data[entry_index].complements) {
                if (a_data.fingerprints.contains(complement)) {
                    feasible = true;
                    break;
                }
            }
            if (feasible) {
                result.rows.push_back(
                    {support, result.inputs.entries[entry_index].b_word}
                );
            }
        }
    }
    std::sort(result.rows.begin(), result.rows.end(), [](const auto& x, const auto& y) {
        return std::pair{x.a_support, x.b_word} < std::pair{y.a_support, y.b_word};
    });
    assert(result.rows.size() == 198);
    return result;
}

Residue seventh_h_target10() {
    Residue result;
    for (int shift = 1; shift <= 10; ++shift) {
        set_coordinate(result, shift - 1, {-2, 0});
    }
    return result;
}

struct SeventhBData10 {
    std::unordered_set<Residue, ResidueHash> complements;
    int exact_assignments = 0;
};

SeventhBData10 enumerate_h_b_seventh10(const Entry10& entry) {
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) {
        if (!((entry.b_word >> shift) & 1)) shifts.push_back(shift);
    }
    assert(shifts.size() == 5);
    Residue target = seventh_h_target10();
    SeventhBData10 result;
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
            result.complements.insert(reduce_seventh(
                residue_subtract(target, paf_residue(changed))
            ));
        }
    }
    assert(result.exact_assignments == 3384);
    return result;
}

struct SeventhAData10 {
    std::unordered_set<Residue, ResidueHash> values;
    long long exact_assignments = 0;
    long long direct_checks = 0;
    long long quadratic_audits = 0;
};

SeventhAData10 enumerate_h_a_seventh10(uint32_t s_support) {
    std::array<int, 10> positions{};
    int active_count = 0;
    for (int position = 0; position < N; ++position) {
        if (!((s_support >> position) & 1)) positions[active_count++] = position;
    }
    assert(active_count == 10);

    SeventhAData10 result;
    result.values.reserve(65000);
    for (uint16_t axes = 0; axes < 1024; ++axes) {
        int n1 = std::popcount(axes);
        if (n1 & 1) continue;
        int n0 = 10 - n1;
        Word baseline_word{};
        for (int j = 0; j < 10; ++j) {
            baseline_word[positions[j]] = active((axes >> j) & 1, 0);
        }
        Residue baseline = paf_residue(baseline_word);
        std::array<Residue, 15> linear{};
        std::array<std::array<Residue, 15>, 15> quadratic{};
        for (int j = 0; j < 10; ++j) {
            Word changed = baseline_word;
            changed[positions[j]] = scale(changed[positions[j]], -1);
            linear[j] = residue_subtract(paf_residue(changed), baseline);
            ++result.direct_checks;
        }
        for (int j = 0; j < 10; ++j) for (int k = j + 1; k < 10; ++k) {
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

        uint16_t audit = uint16_t(((uint32_t(axes) + 1) * 0x025du) & 0x03ffu);
        Word audited = baseline_word;
        for (int j = 0; j < 10; ++j) if ((audit >> j) & 1) {
            audited[positions[j]] = scale(audited[positions[j]], -1);
        }
        assert(
            residue_subtract(paf_residue(audited), baseline)
            == evaluate_quadratic(audit, linear, quadratic)
        );
        ++result.direct_checks;
        ++result.quadratic_audits;

        std::array<Residue, 32> left_residues{};
        std::array<int, 32> left_negative0{};
        std::array<int, 32> left_negative1{};
        for (uint16_t mask = 1; mask < 32; ++mask) {
            int j = std::countr_zero(mask);
            uint16_t rest = mask & (mask - 1);
            Residue value = residue_add(left_residues[rest], linear[j]);
            for (int k = j + 1; k < 5; ++k) if ((rest >> k) & 1) {
                value = residue_add(value, quadratic[j][k]);
            }
            left_residues[mask] = value;
            left_negative0[mask] = left_negative0[rest];
            left_negative1[mask] = left_negative1[rest];
            ((axes >> j) & 1 ? left_negative1[mask] : left_negative0[mask])++;
        }

        std::array<Residue, 32> right_residues{};
        std::array<int, 32> right_negative0{};
        std::array<int, 32> right_negative1{};
        std::array<std::array<std::vector<uint8_t>, 6>, 6> right_by_count;
        right_by_count[0][0].push_back(0);
        for (uint16_t mask = 1; mask < 32; ++mask) {
            int local = std::countr_zero(mask);
            int j = 5 + local;
            uint16_t rest = mask & (mask - 1);
            Residue value = residue_add(right_residues[rest], linear[j]);
            for (int k = j + 1; k < 10; ++k) if ((rest >> (k - 5)) & 1) {
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

        std::array<std::array<Residue, 32>, 5> cross_columns{};
        for (int j = 0; j < 5; ++j) for (uint16_t mask = 1; mask < 32; ++mask) {
            int local = std::countr_zero(mask);
            uint16_t rest = mask & (mask - 1);
            cross_columns[j][mask] = residue_add(
                cross_columns[j][rest], quadratic[j][5 + local]
            );
        }

        for (uint16_t left = 0; left < 32; ++left) {
            int need0 = n0 / 2 - left_negative0[left];
            int need1 = n1 / 2 - left_negative1[left];
            if (need0 < 0 || need0 > 5 || need1 < 0 || need1 > 5) continue;
            for (uint8_t right : right_by_count[need0][need1]) {
                Residue value = residue_add(
                    baseline, residue_add(left_residues[left], right_residues[right])
                );
                for (int j = 0; j < 5; ++j) if ((left >> j) & 1) {
                    value = residue_add(value, cross_columns[j][right]);
                }
                result.values.insert(reduce_seventh(value));
                ++result.exact_assignments;
            }
        }
    }
    assert(result.exact_assignments == 63504);
    assert(result.direct_checks == 512LL * 56);
    assert(result.quadratic_audits == 512);
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

    SixthFrontier10 frontier = reconstruct_sixth_frontier10();
    if (dump_sixth_frontier) {
        std::cout << "a_s_word\tb_s_word\n";
        for (const FrontierRow10& row : frontier.rows) {
            std::cout << row.a_support << '\t' << row.b_word << '\n';
        }
        return 0;
    }

    std::unordered_map<uint32_t, Entry10> entries_by_word;
    for (const Entry10& entry : frontier.inputs.entries) {
        entries_by_word.emplace(entry.b_word, entry);
    }
    std::map<uint32_t, std::vector<FrontierRow10>> by_support;
    std::set<uint32_t> input_b_masks;
    for (const FrontierRow10& row : frontier.rows) {
        by_support[row.a_support].push_back(row);
        input_b_masks.insert(row.b_word);
    }

    std::unordered_map<uint32_t, SeventhBData10> b_data;
    size_t minimum_b_fingerprints = SIZE_MAX;
    size_t maximum_b_fingerprints = 0;
    for (uint32_t b_word : input_b_masks) {
        SeventhBData10 data = enumerate_h_b_seventh10(entries_by_word.at(b_word));
        minimum_b_fingerprints = std::min(minimum_b_fingerprints, data.complements.size());
        maximum_b_fingerprints = std::max(maximum_b_fingerprints, data.complements.size());
        b_data.emplace(b_word, std::move(data));
    }

    std::vector<FrontierRow10> surviving;
    long long exact_assignments = 0;
    long long direct_checks = 0;
    long long quadratic_audits = 0;
    size_t minimum_a_fingerprints = SIZE_MAX;
    size_t maximum_a_fingerprints = 0;
    int supports_completed = 0;
    for (const auto& [a_support, rows] : by_support) {
        SeventhAData10 a_data = enumerate_h_a_seventh10(a_support);
        exact_assignments += a_data.exact_assignments;
        direct_checks += a_data.direct_checks;
        quadratic_audits += a_data.quadratic_audits;
        minimum_a_fingerprints = std::min(minimum_a_fingerprints, a_data.values.size());
        maximum_a_fingerprints = std::max(maximum_a_fingerprints, a_data.values.size());
        for (const FrontierRow10& row : rows) {
            bool feasible = false;
            for (const Residue& complement : b_data.at(row.b_word).complements) {
                if (a_data.values.contains(complement)) {
                    feasible = true;
                    break;
                }
            }
            if (feasible) surviving.push_back(row);
        }
        ++supports_completed;
        if (!quiet && supports_completed % 10 == 0) {
            std::cout << "completed_a_support=" << supports_completed << '/'
                      << by_support.size() << ";surviving_rows="
                      << surviving.size() << '\n';
        }
    }

    std::set<uint32_t> surviving_masks;
    for (const FrontierRow10& row : surviving) surviving_masks.insert(row.b_word);
    std::cout << "input_sixth_h_orbit_pairs=" << frontier.rows.size() << "\n"
              << "input_sixth_h_case_incidences=" << 6 * frontier.rows.size() << "\n"
              << "input_unique_a_supports=" << by_support.size() << "\n"
              << "input_unique_b_masks=" << input_b_masks.size() << "\n"
              << "supports_completed=" << supports_completed << "\n"
              << "seventh_h_surviving_orbit_pairs=" << surviving.size() << "\n"
              << "seventh_h_surviving_case_incidences=" << 6 * surviving.size() << "\n"
              << "seventh_h_surviving_b_masks=" << surviving_masks.size() << "\n"
              << "h_a_seventh_fingerprint_range=" << minimum_a_fingerprints << '-'
              << maximum_a_fingerprints << "\n"
              << "h_b_seventh_fingerprint_range=" << minimum_b_fingerprints << '-'
              << maximum_b_fingerprints << "\n"
              << "h_b_exact_assignments=3384\n"
              << "h_a_exact_assignments=" << exact_assignments << "\n"
              << "h_a_quadratic_direct_checks=" << direct_checks << "\n"
              << "h_a_quadratic_global_audits=" << quadratic_audits << "\n"
              << "full_seventh_h_certificate=verified\n";
    std::sort(surviving.begin(), surviving.end(), [](const auto& x, const auto& y) {
        return std::pair{x.a_support, x.b_word} < std::pair{y.a_support, y.b_word};
    });
    for (const FrontierRow10& row : surviving) {
        std::cout << "frontier_pair=" << row.a_support << ',' << row.b_word << "\n";
    }
    return 0;
}
