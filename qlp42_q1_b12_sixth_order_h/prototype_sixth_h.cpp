#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wreturn-type"
#endif
#define B12_MAIN embedded_b12_s_main
#include "../qlp42_q1_b12_sixth_order_s/independent_cpp.cpp"
#undef B12_MAIN
#if defined(__clang__)
#pragma clang diagnostic pop
#endif

namespace {

constexpr std::array<int, 6> H_CENTER_NEGATIVE = {0, 1, 0, 0, 1, 1};

Residue h_add(Residue left, const Residue& right) {
    return reduce_sixth(residue_add(left, right));
}

Residue h_subtract(Residue left, const Residue& right) {
    return reduce_sixth(residue_subtract(left, right));
}

Residue h_target_residue() {
    Residue result;
    for (int shift = 1; shift <= 10; ++shift) {
        set_coordinate(result, shift - 1, {-2, 0});
    }
    return reduce_sixth(result);
}

G word_sum(const Word& word) {
    G result{};
    for (G value : word) result = add(result, value);
    return result;
}

struct HTarget {
    Residue complement{};
    Word word{};
};

struct HBData {
    std::array<std::vector<HTarget>, 2> targets;
    std::array<int, 2> exact_assignments{};
};

HBData enumerate_h_b(const B12Entry& entry) {
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) {
        if (((entry.b_word >> shift) & 1) == 0) shifts.push_back(shift);
    }
    assert(shifts.size() == 4);
    Residue target = h_target_residue();
    HBData result;
    for (int center_negative = 0; center_negative < 2; ++center_negative) {
        std::unordered_map<Residue, Word, ResidueHash> unique;
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
            baseline[0] = center_negative ? G{-1, 0} : G{1, 0};
            assert(count == 8);
            for (uint16_t signs = 0; signs < 256; ++signs) {
                Word word = baseline;
                for (int j = 0; j < 8; ++j) if ((signs >> j) & 1) {
                    word[positions[j]] = scale(word[positions[j]], -1);
                }
                if (word_sum(word) != G{1, 0}) continue;
                ++result.exact_assignments[center_negative];
                Residue complement = h_subtract(target, reduce_sixth(paf_residue(word)));
                unique.try_emplace(complement, word);
            }
        }
        result.targets[center_negative].reserve(unique.size());
        for (const auto& [complement, word] : unique) {
            result.targets[center_negative].push_back({complement, word});
        }
    }
    return result;
}

Word h_a_word(const std::array<int, 12>& positions, uint16_t axes, uint16_t signs) {
    Word word{};
    for (int j = 0; j < 12; ++j) {
        word[positions[j]] = active((axes >> j) & 1, (signs >> j) & 1);
    }
    return word;
}

struct HSearchResult {
    bool feasible = false;
    int axes_examined = 0;
    long long affine_audits = 0;
};

HSearchResult search_h_a(uint32_t s_support, const std::vector<HTarget>& targets) {
    std::array<int, 12> positions{};
    int active_count = 0;
    for (int position = 0; position < N; ++position) {
        if (((s_support >> position) & 1) == 0) positions[active_count++] = position;
    }
    assert(active_count == 12);

    HSearchResult result;
    if (targets.empty()) return result;
    for (uint16_t axes = 0; axes < (uint16_t{1} << 12); ++axes) {
        int n1 = std::popcount(axes);
        if (n1 & 1) continue;
        ++result.axes_examined;
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

        using ResidueMap = std::unordered_map<Residue, uint8_t, ResidueHash>;
        std::array<std::array<ResidueMap, 7>, 7> right;
        for (uint16_t mask = 0; mask < 64; ++mask) {
            int negative0 = 0;
            int negative1 = 0;
            Residue residue{};
            for (int local = 0; local < 6; ++local) if ((mask >> local) & 1) {
                int index = 6 + local;
                ((axes >> index) & 1 ? negative1 : negative0)++;
                residue = h_add(residue, columns[index]);
            }
            right[negative0][negative1].try_emplace(residue, uint8_t(mask));
        }

        for (uint16_t left = 0; left < 64; ++left) {
            int negative0 = 0;
            int negative1 = 0;
            Residue left_residue{};
            for (int j = 0; j < 6; ++j) if ((left >> j) & 1) {
                ((axes >> j) & 1 ? negative1 : negative0)++;
                left_residue = h_add(left_residue, columns[j]);
            }
            int need0 = n0 / 2 - negative0;
            int need1 = n1 / 2 - negative1;
            if (need0 < 0 || need0 > 6 || need1 < 0 || need1 > 6) continue;
            for (const HTarget& target : targets) {
                Residue needed = h_subtract(
                    h_subtract(target.complement, baseline), left_residue
                );
                auto found = right[need0][need1].find(needed);
                if (found == right[need0][need1].end()) continue;
                uint16_t signs = left | (uint16_t(found->second) << 6);
                Word a = h_a_word(positions, axes, signs);
                assert((word_sum(a) == G{0, 0}));
                assert((word_sum(target.word) == G{1, 0}));
                for (int shift = 1; shift <= 10; ++shift) {
                    G residual = add(
                        add(paf(a, shift), paf(target.word, shift)), {2, 0}
                    );
                    assert((residual.r & 7) == 0 && (residual.i & 7) == 0);
                }
                result.feasible = true;
                return result;
            }
        }
    }
    assert(result.axes_examined == 2048);
    return result;
}

struct HCacheKey {
    uint32_t a_word = 0;
    uint32_t b_word = 0;
    uint8_t center_negative = 0;
    bool operator==(const HCacheKey&) const = default;
};

struct HCacheKeyHash {
    size_t operator()(const HCacheKey& value) const {
        uint64_t packed = value.a_word
            | (uint64_t(value.b_word) << 21)
            | (uint64_t(value.center_negative) << 42);
        packed ^= packed >> 30;
        packed *= 0xbf58476d1ce4e5b9ULL;
        packed ^= packed >> 27;
        packed *= 0x94d049bb133111ebULL;
        packed ^= packed >> 31;
        return size_t(packed);
    }
};

}  // namespace

#ifndef B12_H_MAIN
#define B12_H_MAIN main
#endif

int B12_H_MAIN(int argc, char** argv) {
    bool quiet = false;
    bool singleton_only = true;
    for (int j = 1; j < argc; ++j) {
        std::string argument = argv[j];
        if (argument == "--quiet") quiet = true;
        else if (argument == "--singletons") singleton_only = true;
        else if (argument == "--full") singleton_only = false;
        else assert(false && "unknown argument");
    }
    B12Inputs inputs = reconstruct_b12_inputs();
    std::vector<PhasePattern> patterns = phase_patterns_b12();
    Residue s_target = target_residue();
    std::array<int, 6> eighth_orbits{};
    std::array<int, 6> h_orbits{};
    std::array<std::set<uint32_t>, 6> h_masks;
    std::array<int, 6> h_b_exact_min;
    std::array<int, 6> h_b_exact_max{};
    h_b_exact_min.fill(INT32_MAX);
    std::unordered_map<HCacheKey, HSearchResult, HCacheKeyHash> h_cache;
    long long axes_examined = 0;
    long long affine_audits = 0;
    int eighth_rows = 0;
    int h_rows = 0;
    int remaining_case02_rows = 0;
    std::set<uint32_t> remaining_case02_a_supports;
    std::set<uint32_t> remaining_case02_b_masks;
    std::set<uint64_t> remaining_case02_pairs;

    int entry_number = 0;
    for (const B12Entry& entry : inputs.entries) {
        ++entry_number;
        BData s_b_data = enumerate_b12(entry);
        HBData h_b_data = enumerate_h_b(entry);
        assert(h_b_data.exact_assignments[0] >= 608);
        assert(h_b_data.exact_assignments[0] <= 676);
        assert(h_b_data.exact_assignments[1] == 0);
        for (int case_number = 0; case_number < 6; ++case_number) {
            int orientation = H_CENTER_NEGATIVE[case_number];
            int exact = h_b_data.exact_assignments[orientation];
            h_b_exact_min[case_number] = std::min(h_b_exact_min[case_number], exact);
            h_b_exact_max[case_number] = std::max(h_b_exact_max[case_number], exact);
        }
        for (uint32_t a_word : inputs.representatives[entry.required_signature]) {
            AData s_a_data = enumerate_a12(a_word, patterns);
            bool row_eighth = false;
            bool row_h = false;
            bool row_case02 = false;
            for (int case_number = 0; case_number < 6; ++case_number) {
                bool eighth_feasible = false;
                for (const Residue& a_value : s_a_data.residues[case_number]) {
                    Residue needed = residue_subtract(s_target, a_value);
                    if (s_b_data.order_eight[case_number].contains(needed)) {
                        eighth_feasible = true;
                        break;
                    }
                }
                if (!eighth_feasible) continue;
                ++eighth_orbits[case_number];
                row_eighth = true;
                if (case_number == 0 || case_number == 2) {
                    row_case02 = true;
                    remaining_case02_a_supports.insert(a_word);
                    remaining_case02_b_masks.insert(entry.b_word);
                    remaining_case02_pairs.insert(
                        uint64_t(a_word) | (uint64_t(entry.b_word) << 21)
                    );
                }
                if (singleton_only && case_number < 3) continue;
                int orientation = H_CENTER_NEGATIVE[case_number];
                HCacheKey key{a_word, entry.b_word, uint8_t(orientation)};
                auto found = h_cache.find(key);
                if (found == h_cache.end()) {
                    HSearchResult computed = search_h_a(
                        a_word, h_b_data.targets[orientation]
                    );
                    axes_examined += computed.axes_examined;
                    affine_audits += computed.affine_audits;
                    found = h_cache.emplace(key, computed).first;
                }
                if (found->second.feasible) {
                    ++h_orbits[case_number];
                    h_masks[case_number].insert(entry.b_word);
                    row_h = true;
                }
                if (singleton_only && !quiet) {
                    std::cout << "singleton_case=" << case_number
                              << ";b_equal_positions="
                              << positions(WORD_MASK ^ entry.b_word ^ uint32_t{1})
                              << ";a_s_support=" << positions(a_word)
                              << ";h_center_negative=" << orientation
                              << ";h_b_exact_assignments="
                              << h_b_data.exact_assignments[orientation]
                              << ";h_b_fingerprints="
                              << h_b_data.targets[orientation].size()
                              << ";sixth_h_feasible=" << int(found->second.feasible)
                              << '\n';
                }
            }
            eighth_rows += int(row_eighth);
            h_rows += int(row_h);
            remaining_case02_rows += int(row_case02);
        }
        if (!quiet) {
            std::cout << "completed_b_mask=" << entry_number << "/98;"
                      << "eighth_rows=" << eighth_rows << ";"
                      << "sixth_h_rows=" << h_rows << '\n';
        }
    }

    assert((eighth_orbits == std::array<int, 6>{303, 178, 92, 1, 1, 0}));
    assert(eighth_rows == 493);
    assert(remaining_case02_rows <= 395);
    if (singleton_only) {
        assert(h_cache.size() == 2);
        std::cout << "input_b_masks=98\n"
                  << "negative_center_h_b_exact_assignments=0\n"
                  << "exact_h_sum_eliminated_cases=1,4,5\n"
                  << "target_cases=3,4\n"
                  << "case3_sixth_h_surviving_orbits=" << h_orbits[3] << "\n"
                  << "case4_sixth_h_surviving_orbits=" << h_orbits[4] << "\n"
                  << "remaining_case02_orbit_incidences=395\n"
                  << "remaining_case02_rows=" << remaining_case02_rows << "\n"
                  << "remaining_case02_unique_a_supports="
                  << remaining_case02_a_supports.size() << "\n"
                  << "remaining_case02_unique_b_masks="
                  << remaining_case02_b_masks.size() << "\n"
                  << "remaining_case02_unique_pairs="
                  << remaining_case02_pairs.size() << "\n"
                  << "h_classifications=" << h_cache.size() << "\n"
                  << "h_axes_examined=" << axes_examined << "\n"
                  << "h_affine_direct_audits=" << affine_audits << "\n"
                  << "prototype_certificate=verified\n";
        return 0;
    }
    std::cout << "input_eighth_s_orbits=303,178,92,1,1,0\n"
              << "input_eighth_s_rows=" << eighth_rows << "\n"
              << "sixth_h_surviving_orbits=";
    for (int case_number = 0; case_number < 6; ++case_number) {
        if (case_number) std::cout << ',';
        std::cout << h_orbits[case_number];
    }
    std::cout << "\nsixth_h_surviving_masks=";
    for (int case_number = 0; case_number < 6; ++case_number) {
        if (case_number) std::cout << ',';
        std::cout << h_masks[case_number].size();
    }
    std::cout << "\nremaining_case02_orbit_incidences=395"
              << "\nremaining_case02_rows=" << remaining_case02_rows
              << "\nsixth_h_surviving_rows=" << h_rows
              << "\nh_classifications=" << h_cache.size()
              << "\nh_axes_examined=" << axes_examined
              << "\nh_affine_direct_audits=" << affine_audits
              << "\nh_b_exact_assignment_ranges=";
    for (int case_number = 0; case_number < 6; ++case_number) {
        if (case_number) std::cout << ',';
        std::cout << h_b_exact_min[case_number] << '-' << h_b_exact_max[case_number];
    }
    std::cout << "\nprototype_certificate=verified\n";
    return 0;
}
