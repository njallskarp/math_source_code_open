#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main embedded_b14_main
#include "../qlp42_q1_b14_sixth_order_s/independent_cpp.cpp"
#undef main
#pragma GCC diagnostic pop

#include <climits>

namespace {

constexpr std::array<uint64_t, 20> HASH_COEFFICIENTS = {
    0x2cb0f69f4abea221ULL, 0x9417034723148989ULL,
    0xdd555950609dfe03ULL, 0xdbafb150deb12800ULL,
    0x7e789b2e6c442cb6ULL, 0xf41e5636c7e4f8c4ULL,
    0x0959d150f8fba7e4ULL, 0xa97316f13cdb9eeaULL,
    0x74cd8258f9520068ULL, 0x55c74a62e116868bULL,
    0xd2f4c799a2023cbdULL, 0xdf98cb79a37b51b9ULL,
    0x396f5885524f3905ULL, 0xaf1d56386ca3b276ULL,
    0xa9ffbe6b5104e85aULL, 0x6bd0c51b9fd533b3ULL,
    0x980ce91c50ab4b56ULL, 0x28ac395780fe62c5ULL,
    0x768912e3a6bcedc7ULL, 0x50b3e8c9332c7c88ULL,
};

struct FrontierPair {
    uint32_t a_support;
    uint32_t b_word;
    auto operator<=>(const FrontierPair&) const = default;
};

constexpr std::array<FrontierPair, 40> EXACT_H_FRONTIER = {{
    {77819, 724020}, {113143, 663060}, {114665, 724020},
    {117695, 147216}, {122683, 663060}, {129959, 147216},
    {163573, 1215570}, {179705, 1215570}, {182239, 461880},
    {188087, 175440}, {192399, 400920}, {196267, 461880},
    {212439, 1191186}, {215007, 461880}, {217039, 920604},
    {218621, 461880}, {223135, 461880}, {241395, 1191186},
    {243181, 175440}, {247773, 400920}, {249295, 400920},
    {249551, 400920}, {249803, 920604}, {255391, 920604},
    {255647, 920604}, {255899, 461880}, {308733, 724020},
    {311213, 724020}, {352059, 204336}, {370399, 724020},
    {370651, 724020}, {372443, 1191186}, {380839, 1187346},
    {390055, 1187346}, {423343, 920604}, {424663, 920604},
    {441007, 1191186}, {449453, 1191186}, {452565, 204336},
    {502507, 1191186},
}};

uint64_t signed_term(uint64_t coefficient, int sign) {
    return sign > 0 ? coefficient : uint64_t{0} - coefficient;
}

uint64_t linear_hash_word(const Word& word) {
    uint64_t result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        G value = paf(word, shift);
        result += uint64_t(int64_t(value.r)) * HASH_COEFFICIENTS[2 * (shift - 1)];
        result += uint64_t(int64_t(value.i)) * HASH_COEFFICIENTS[2 * (shift - 1) + 1];
    }
    return result;
}

uint64_t target_s_hash() {
    return (uint64_t{0} - uint64_t{2}) * HASH_COEFFICIENTS[2 * (4 - 1)]
           + uint64_t{2} * HASH_COEFFICIENTS[2 * (10 - 1)];
}

std::array<int, 10> theta_for(uint32_t b_word) {
    uint32_t f_word = ((~b_word) & WORD_MASK) & ~uint32_t{1};
    uint16_t b_signature = correlation_signature(b_word);
    uint16_t f_signature = correlation_signature(f_word);
    std::array<int, 10> theta{};
    for (int shift = 1; shift <= 10; ++shift) {
        int bit = shift - 1;
        int tau = (TAU_SIGNATURE >> bit) & 1;
        int b_corr = (b_signature >> bit) & 1;
        int f_corr = (f_signature >> bit) & 1;
        theta[bit] = 1 ^ tau ^ b_corr ^ f_corr;
    }
    return theta;
}

struct BHashes {
    std::array<std::unordered_set<uint64_t>, 6> required;
    std::array<int, 6> exact_assignments{};
};

BHashes enumerate_b_hashes(uint32_t b_word) {
    assert(std::popcount(b_word) == 8);
    std::array<int, 10> theta = theta_for(b_word);
    std::vector<int> shifts;
    for (int shift = 1; shift <= 10; ++shift) {
        if ((b_word >> shift) & 1) shifts.push_back(shift);
    }
    assert(shifts.size() == 4);

    BHashes result;
    uint64_t target_hash = target_s_hash();
    for (uint16_t axes = 0; axes < 16; ++axes) {
        Word baseline{};
        std::array<int, 8> positions{};
        int count = 0;
        for (int j = 0; j < 4; ++j) {
            int shift = shifts[j];
            int axis = (axes >> j) & 1;
            baseline[shift] = active(axis, 0);
            baseline[N - shift] = active(axis ^ theta[shift - 1], 0);
            positions[count++] = shift;
            positions[count++] = N - shift;
        }
        assert(count == 8);
        for (uint16_t signs = 0; signs < 256; ++signs) {
            Word word = baseline;
            for (int j = 0; j < 8; ++j) if ((signs >> j) & 1) {
                word[positions[j]] = scale(word[positions[j]], -1);
            }
            for (int case_number = 0; case_number < 6; ++case_number) {
                int center_imag =
                    (case_number == 0 || case_number == 2 || case_number == 3)
                    ? -1 : 1;
                word[0] = {0, center_imag};
                G sum{};
                for (const G& value : word) sum = add(sum, value);
                G target = sum_targets(CASES[case_number]).second;
                if (sum != target) continue;
                ++result.exact_assignments[case_number];
                result.required[case_number].insert(
                    target_hash - linear_hash_word(word)
                );
            }
        }
    }
    assert((result.exact_assignments == std::array<int, 6>{96, 96, 248, 248, 248, 248}));
    return result;
}

struct PairCoefficient {
    int left;
    int right;
    uint64_t real;
    uint64_t imag;
};

std::vector<PairCoefficient> coefficients_for(uint32_t support) {
    std::array<int, N> index{};
    index.fill(-1);
    int count = 0;
    for (int position = 0; position < N; ++position) {
        if ((support >> position) & 1) index[position] = count++;
    }
    assert(count == 13);
    std::vector<PairCoefficient> result;
    for (int shift = 1; shift <= 10; ++shift) {
        for (int position = 0; position < N; ++position) {
            int left = index[position];
            int right = index[(position + shift) % N];
            if (left < 0 || right < 0) continue;
            result.push_back({
                left,
                right,
                HASH_COEFFICIENTS[2 * (shift - 1)],
                HASH_COEFFICIENTS[2 * (shift - 1) + 1],
            });
        }
    }
    assert(result.size() == 78);
    return result;
}

std::array<std::vector<uint16_t>, 14> masks_by_weight() {
    std::array<std::vector<uint16_t>, 14> result;
    for (uint16_t mask = 0; mask < (1 << 13); ++mask) {
        result[std::popcount(mask)].push_back(mask);
    }
    return result;
}

uint64_t direct_support_hash(uint32_t support, uint16_t real, uint16_t imag) {
    Word word{};
    int index = 0;
    for (int position = 0; position < N; ++position) if ((support >> position) & 1) {
        word[position] = {
            ((real >> index) & 1) ? 1 : -1,
            ((imag >> index) & 1) ? 1 : -1,
        };
        ++index;
    }
    assert(index == 13);
    return linear_hash_word(word);
}

struct ScanCounts {
    std::array<unsigned long long, 6> case_assignment_checks{};
    unsigned long long unique_phase_words = 0;
    unsigned long long direct_formula_audits = 0;
    unsigned long long hash_matches = 0;
};

ScanCounts scan_support(
    const FrontierPair& pair,
    const BHashes& b_hashes,
    const std::array<std::vector<uint16_t>, 14>& masks) {
    std::vector<PairCoefficient> terms = coefficients_for(pair.a_support);
    std::array<uint64_t, 1 << 13> diagonal{};
    for (uint16_t mask = 0; mask < (1 << 13); ++mask) {
        uint64_t value = 0;
        for (const PairCoefficient& term : terms) {
            int left = ((mask >> term.left) & 1) ? 1 : -1;
            int right = ((mask >> term.right) & 1) ? 1 : -1;
            value += signed_term(term.real, left * right);
        }
        diagonal[mask] = value;
    }

    ScanCounts result;
    std::set<std::pair<int, int>> completed_targets;
    for (int case_number = 0; case_number < 6; ++case_number) {
        G target = sum_targets(CASES[case_number]).first;
        if (!completed_targets.insert({target.r, target.i}).second) continue;
        std::vector<int> cases;
        for (int candidate = 0; candidate < 6; ++candidate) {
            G other = sum_targets(CASES[candidate]).first;
            if (other == target) cases.push_back(candidate);
        }
        int real_weight = (13 + target.r) / 2;
        int imag_weight = (13 + target.i) / 2;
        unsigned long long assignments =
            uint64_t(masks[real_weight].size()) * masks[imag_weight].size();
        result.unique_phase_words += assignments;
        for (int candidate : cases) result.case_assignment_checks[candidate] += assignments;

        bool audited = false;
        for (uint16_t real_mask : masks[real_weight]) {
            std::array<uint64_t, 13> alpha{};
            for (const PairCoefficient& term : terms) {
                int left = ((real_mask >> term.left) & 1) ? 1 : -1;
                int right = ((real_mask >> term.right) & 1) ? 1 : -1;
                alpha[term.left] += signed_term(term.imag, right);
                alpha[term.right] -= signed_term(term.imag, left);
            }

            std::array<uint64_t, 64> left_cross{};
            std::array<uint64_t, 128> right_cross{};
            for (int j = 0; j < 6; ++j) left_cross[0] -= alpha[j];
            for (int j = 6; j < 13; ++j) right_cross[0] -= alpha[j];
            for (uint16_t mask = 1; mask < 64; ++mask) {
                int bit = std::countr_zero(mask);
                left_cross[mask] = left_cross[mask & (mask - 1)] + 2 * alpha[bit];
            }
            for (uint16_t mask = 1; mask < 128; ++mask) {
                int bit = std::countr_zero(mask);
                right_cross[mask] =
                    right_cross[mask & (mask - 1)] + 2 * alpha[6 + bit];
            }

            for (uint16_t imag_mask : masks[imag_weight]) {
                uint64_t value = diagonal[real_mask] + diagonal[imag_mask]
                    + left_cross[imag_mask & 63] + right_cross[imag_mask >> 6];
                if (!audited) {
                    assert(value == direct_support_hash(pair.a_support, real_mask, imag_mask));
                    ++result.direct_formula_audits;
                    audited = true;
                }
                for (int candidate : cases) {
                    if (b_hashes.required[candidate].contains(value)) {
                        ++result.hash_matches;
                    }
                }
            }
        }
        assert(audited);
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    bool quiet = false;
    bool dump_input = false;
    for (int j = 1; j < argc; ++j) {
        std::string argument = argv[j];
        if (argument == "--quiet") quiet = true;
        else if (argument == "--dump-input") dump_input = true;
        else assert(false && "unknown argument");
    }
    if (dump_input) {
        std::cout << "a_s_word\tb_s_word\n";
        for (const FrontierPair& pair : EXACT_H_FRONTIER) {
            std::cout << pair.a_support << '\t' << pair.b_word << '\n';
        }
        return 0;
    }

    assert(std::is_sorted(EXACT_H_FRONTIER.begin(), EXACT_H_FRONTIER.end()));
    std::set<uint32_t> b_words;
    for (const FrontierPair& pair : EXACT_H_FRONTIER) {
        assert(std::popcount(pair.a_support) == 13);
        assert(std::popcount(pair.b_word) == 8);
        b_words.insert(pair.b_word);
    }
    assert(b_words.size() == 11);

    std::map<uint32_t, BHashes> b_data;
    for (uint32_t b_word : b_words) b_data.emplace(b_word, enumerate_b_hashes(b_word));
    std::array<std::vector<uint16_t>, 14> masks = masks_by_weight();

    ScanCounts total;
    int completed = 0;
    for (const FrontierPair& pair : EXACT_H_FRONTIER) {
        ScanCounts current = scan_support(pair, b_data.at(pair.b_word), masks);
        for (int case_number = 0; case_number < 6; ++case_number) {
            total.case_assignment_checks[case_number] += current.case_assignment_checks[case_number];
        }
        total.unique_phase_words += current.unique_phase_words;
        total.direct_formula_audits += current.direct_formula_audits;
        total.hash_matches += current.hash_matches;
        ++completed;
        if (!quiet && completed % 10 == 0) {
            std::cerr << "completed_exact_s_support=" << completed << "/40;"
                      << "linear_hash_matches=" << total.hash_matches << '\n';
        }
    }

    assert(total.unique_phase_words == 269'926'800ULL);
    assert((total.case_assignment_checks == std::array<unsigned long long, 6>{
        117'786'240ULL, 66'254'760ULL, 66'254'760ULL,
        49'077'600ULL, 49'077'600ULL, 36'808'200ULL,
    }));
    assert(total.direct_formula_audits == 160);
    assert(total.hash_matches == 0);

    std::cout << "input_exact_h_orbit_pairs=40\n"
              << "input_unique_a_supports=40\n"
              << "input_unique_b_masks=11\n"
              << "input_exact_h_frontier_sha256="
              << "0e3fa74a39e7a5ff91ef3d56a33a5f1a62a9528839f6facfdd47e2b789418cfd\n"
              << "s_b_exact_assignments_by_case=96,96,248,248,248,248\n"
              << "s_a_unique_phase_words_checked=" << total.unique_phase_words << '\n'
              << "s_a_case_assignment_checks=";
    for (int case_number = 0; case_number < 6; ++case_number) {
        if (case_number) std::cout << ',';
        std::cout << total.case_assignment_checks[case_number];
    }
    std::cout << "\nlinear_hash_formula_audits=" << total.direct_formula_audits
              << "\nlinear_hash_matches=" << total.hash_matches
              << "\nexact_s_surviving_case_incidences=0\n"
              << "exact_s_surviving_orbit_pairs=0\n"
              << "q1_b8_shell=excluded\n"
              << "independent_scalar_cpp_certificate=verified\n";
    return 0;
}
