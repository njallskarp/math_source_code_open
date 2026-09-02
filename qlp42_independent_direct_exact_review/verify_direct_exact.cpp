#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int N = 21;
constexpr std::uint32_t FULL = (std::uint32_t{1} << N) - 1;
constexpr std::uint32_t NONCENTER = FULL ^ 1U;

struct Gaussian {
    int r{};
    int i{};
    friend bool operator==(Gaussian, Gaussian) = default;
};

using Paf = std::array<Gaussian, 10>;

struct Key {
    std::uint64_t lo{};
    std::uint64_t hi{};
    friend bool operator==(Key, Key) = default;
};

struct KeyHash {
    std::size_t operator()(Key key) const noexcept {
        std::uint64_t x = key.lo ^ (key.hi + 0x9e3779b97f4a7c15ULL
            + (key.lo << 6) + (key.lo >> 2));
        x ^= x >> 30;
        x *= 0xbf58476d1ce4e5b9ULL;
        x ^= x >> 27;
        x *= 0x94d049bb133111ebULL;
        return static_cast<std::size_t>(x ^ (x >> 31));
    }
};

struct AxisSet {
    std::array<std::uint64_t, 16> words{};

    void set(unsigned value) {
        words[value / 64] |= std::uint64_t{1} << (value % 64);
    }

    void merge(const AxisSet& other) {
        for (std::size_t k = 0; k < words.size(); ++k) words[k] |= other.words[k];
    }

    bool test(unsigned value) const {
        return ((words[value / 64] >> (value % 64)) & 1U) != 0;
    }

    std::uint64_t count() const {
        std::uint64_t total = 0;
        for (auto word : words) total += std::popcount(word);
        return total;
    }
};

struct HPair {
    std::uint32_t b_axis{};
    unsigned signature{};
    unsigned a_half{};
};

std::uint32_t rotate_left(std::uint32_t value, int shift) {
    shift %= N;
    if (shift == 0) return value & FULL;
    return ((value << shift) | (value >> (N - shift))) & FULL;
}

int bit(std::uint32_t value, int index) {
    return static_cast<int>((value >> index) & 1U);
}

Key pack(const Paf& values) {
    Key key;
    int offset = 0;
    for (const auto value : values) {
        for (int coordinate : {value.r, value.i}) {
            assert(coordinate >= -32 && coordinate < 32);
            const std::uint64_t code = static_cast<std::uint64_t>(coordinate + 32);
            if (offset < 64) {
                key.lo |= code << offset;
                if (offset + 6 > 64) key.hi |= code >> (64 - offset);
            } else {
                key.hi |= code << (offset - 64);
            }
            offset += 6;
        }
    }
    assert(offset == 120);
    return key;
}

Paf paf_units(std::uint32_t axes, std::uint32_t negative, bool zero_center) {
    Paf result{};
    for (int shift = 1; shift <= 10; ++shift) {
        const std::uint32_t next_axes = rotate_left(axes, N - shift);
        const std::uint32_t next_negative = rotate_left(negative, N - shift);
        std::uint32_t valid = FULL;
        if (zero_center) valid &= ~(1U | (std::uint32_t{1} << (N - shift)));
        const std::uint32_t sign_change = negative ^ next_negative;
        const std::uint32_t same = valid & ~(axes ^ next_axes) & FULL;
        const std::uint32_t plus_i = valid & axes & ~next_axes;
        const std::uint32_t minus_i = valid & ~axes & next_axes;
        const int real = static_cast<int>(std::popcount(same))
            - 2 * static_cast<int>(std::popcount(same & sign_change));
        const int imag = static_cast<int>(std::popcount(plus_i))
            - static_cast<int>(std::popcount(minus_i))
            - 2 * (static_cast<int>(std::popcount(plus_i & sign_change))
                - static_cast<int>(std::popcount(minus_i & sign_change)));
        result[shift - 1] = {real, imag};
    }
    return result;
}

Paf paf_definition(const std::array<Gaussian, N>& word) {
    Paf result{};
    for (int shift = 1; shift <= 10; ++shift) {
        Gaussian total{};
        for (int j = 0; j < N; ++j) {
            const Gaussian a = word[j];
            const Gaussian b = word[(j + shift) % N];
            total.r += a.r * b.r + a.i * b.i;
            total.i += a.i * b.r - a.r * b.i;
        }
        result[shift - 1] = total;
    }
    return result;
}

std::array<Gaussian, N> unit_word(
    std::uint32_t axes, std::uint32_t negative, bool zero_center
) {
    std::array<Gaussian, N> word{};
    for (int j = 0; j < N; ++j) {
        if (zero_center && j == 0) continue;
        const int sign = bit(negative, j) ? -1 : 1;
        word[j] = bit(axes, j) ? Gaussian{0, sign} : Gaussian{sign, 0};
    }
    return word;
}

std::uint64_t mix(std::uint64_t value) {
    value += 0x9e3779b97f4a7c15ULL;
    value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
    value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
    return value ^ (value >> 31);
}

std::vector<std::uint32_t> subsets_of_weight(std::uint32_t mask, int weight) {
    std::vector<int> positions;
    for (int j = 0; j < N; ++j) if (bit(mask, j)) positions.push_back(j);
    assert(weight >= 0 && weight <= static_cast<int>(positions.size()));
    std::vector<std::uint32_t> result;
    auto generate = [&](auto&& self, int start, int left, std::uint32_t value) -> void {
        if (left == 0) {
            result.push_back(value);
            return;
        }
        for (int k = start; k <= static_cast<int>(positions.size()) - left; ++k) {
            self(self, k + 1, left - 1, value | (std::uint32_t{1} << positions[k]));
        }
    };
    generate(generate, 0, weight, 0);
    return result;
}

std::vector<std::uint32_t> orbit_representatives(int weight) {
    const auto words = subsets_of_weight(FULL, weight);
    std::vector<std::uint32_t> representatives;
    std::unordered_set<std::uint32_t> covered;
    for (auto word : words) {
        std::uint32_t least = word;
        for (int shift = 1; shift < N; ++shift) least = std::min(least, rotate_left(word, shift));
        if (word != least) continue;
        std::unordered_set<std::uint32_t> orbit;
        for (int shift = 0; shift < N; ++shift) orbit.insert(rotate_left(word, shift));
        assert(orbit.size() == N);
        for (auto member : orbit) assert(covered.insert(member).second);
        representatives.push_back(word);
    }
    assert(covered.size() == words.size());
    return representatives;
}

std::uint32_t reflected_axes(unsigned half) {
    std::uint32_t axes = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        if (((half >> (shift - 1)) & 1U) != 0) {
            axes |= (std::uint32_t{1} << shift) | (std::uint32_t{1} << (N - shift));
        }
    }
    return axes;
}

unsigned signature(std::uint32_t b_axis) {
    const int parity = static_cast<int>(std::popcount(b_axis) & 1U);
    unsigned result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        const int overlap = static_cast<int>(
            std::popcount(b_axis & rotate_left(b_axis, shift)) & 1U
        );
        result |= static_cast<unsigned>(parity ^ overlap) << (shift - 1);
    }
    return result;
}

unsigned theta_h(unsigned half, unsigned e) {
    const auto axes = reflected_axes(half);
    unsigned theta = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        const int a = bit(half, shift - 1);
        const int overlap = static_cast<int>(
            std::popcount(axes & rotate_left(axes, shift)) & 1U
        );
        theta |= static_cast<unsigned>(1 ^ a ^ overlap ^ bit(e, shift - 1))
            << (shift - 1);
    }
    return theta;
}

unsigned theta_s(unsigned half, unsigned e) {
    const auto h_axes = reflected_axes(half);
    const auto s_axes = NONCENTER ^ h_axes;
    unsigned theta = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        const int f = 1 ^ bit(half, shift - 1);
        const int overlap = static_cast<int>(
            std::popcount(s_axes & rotate_left(s_axes, shift)) & 1U
        );
        const int tau = (shift == 4 || shift == 10) ? 1 : 0;
        theta |= static_cast<unsigned>(1 ^ f ^ overlap ^ bit(e, shift - 1) ^ tau)
            << (shift - 1);
    }
    return theta;
}

std::vector<std::uint32_t> build_pair_words() {
    std::vector<std::uint32_t> table(std::size_t{1} << 20);
    for (unsigned theta = 0; theta < (1U << 10); ++theta) {
        for (unsigned left = 0; left < (1U << 10); ++left) {
            std::uint32_t negative = 0;
            for (int pair = 0; pair < 10; ++pair) {
                const int shift = pair + 1;
                const int left_sign = bit(left, pair);
                const int right_sign = left_sign ^ bit(theta, pair);
                if (left_sign) negative |= std::uint32_t{1} << shift;
                if (right_sign) negative |= std::uint32_t{1} << (N - shift);
            }
            table[(std::size_t{theta} << 10) | left] = negative;
        }
    }
    return table;
}

Paf h_requirement(const Paf& a) {
    Paf required{};
    for (int k = 0; k < 10; ++k) required[k] = {-2 - a[k].r, -a[k].i};
    return required;
}

using HIndex = std::unordered_map<Key, AxisSet, KeyHash>;

HIndex build_h_index(
    unsigned e, const std::vector<std::uint32_t>& pair_words,
    std::uint64_t& exact_sum_assignments, std::uint64_t& definition_audits
) {
    HIndex index;
    for (unsigned half = 0; half < (1U << 10); ++half) {
        const auto axes = reflected_axes(half);
        const auto real_mask = NONCENTER & ~axes;
        const auto imaginary_mask = axes;
        const int real_count = static_cast<int>(std::popcount(real_mask));
        const int imaginary_count = static_cast<int>(std::popcount(imaginary_mask));
        const unsigned theta = theta_h(half, e);
        for (unsigned left = 0; left < (1U << 10); ++left) {
            const auto negative = pair_words[(std::size_t{theta} << 10) | left];
            const int sum_r = real_count - 2 * static_cast<int>(std::popcount(real_mask & negative));
            const int sum_i = imaginary_count
                - 2 * static_cast<int>(std::popcount(imaginary_mask & negative));
            if (sum_r != 0 || sum_i != 0) continue;
            const auto values = paf_units(axes, negative, true);
            if (mix((std::uint64_t{e} << 20) | (std::uint64_t{half} << 10) | left) % 4093 == 0) {
                assert(values == paf_definition(unit_word(axes, negative, true)));
                ++definition_audits;
            }
            index[pack(h_requirement(values))].set(half);
            ++exact_sum_assignments;
        }
    }
    return index;
}

AxisSet scan_h_b_axis(
    std::uint32_t b_axis, int weight, const HIndex& index,
    std::uint64_t& exact_sum_assignments, std::uint64_t& definition_b_audits
) {
    const int negative_imaginary = weight / 2;
    const int negative_real = (N - weight - 1) / 2;
    const auto imaginary_choices = subsets_of_weight(b_axis, negative_imaginary);
    const auto real_choices = subsets_of_weight(FULL ^ b_axis, negative_real);
    AxisSet survivors;
    for (auto imaginary : imaginary_choices) {
        for (auto real : real_choices) {
            const auto negative = imaginary | real;
            const auto values = paf_units(b_axis, negative, false);
            if (mix((std::uint64_t{b_axis} << N) | negative) % 4093 == 0) {
                assert(values == paf_definition(unit_word(b_axis, negative, false)));
                ++definition_b_audits;
            }
            if (const auto found = index.find(pack(values)); found != index.end()) {
                survivors.merge(found->second);
            }
            ++exact_sum_assignments;
        }
    }
    return survivors;
}

constexpr std::array<std::array<int, 2>, 6> S_A_TARGETS{{
    {{1, -1}}, {{3, -3}}, {{3, -3}}, {{5, -1}}, {{5, -1}}, {{5, -3}}
}};
constexpr std::array<std::array<int, 2>, 6> S_B_TARGETS{{
    {{4, -5}}, {{4, -3}}, {{0, -5}}, {{4, -1}}, {{4, 1}}, {{0, -3}}
}};
constexpr std::array<Gaussian, 4> CENTERS{{
    {1, 1}, {-1, 1}, {-1, -1}, {1, -1}
}};

std::unordered_set<Key, KeyHash> build_s_b_support(
    std::uint32_t h_b_axis, int case_index, std::uint64_t& assignments
) {
    const std::uint32_t axes = FULL ^ h_b_axis;
    const int imaginary_count = static_cast<int>(std::popcount(axes));
    const int real_count = N - imaginary_count;
    const int negative_real = (real_count - S_B_TARGETS[case_index][0]) / 2;
    const int negative_imaginary = (imaginary_count - S_B_TARGETS[case_index][1]) / 2;
    assert(2 * negative_real == real_count - S_B_TARGETS[case_index][0]);
    assert(2 * negative_imaginary == imaginary_count - S_B_TARGETS[case_index][1]);
    const auto real_choices = subsets_of_weight(FULL ^ axes, negative_real);
    const auto imaginary_choices = subsets_of_weight(axes, negative_imaginary);
    std::unordered_set<Key, KeyHash> support;
    support.reserve(real_choices.size() * imaginary_choices.size());
    for (auto real : real_choices) {
        for (auto imaginary : imaginary_choices) {
            support.insert(pack(paf_units(axes, real | imaginary, false)));
            ++assignments;
        }
    }
    return support;
}

Paf s_requirement(const Paf& a) {
    Paf required{};
    for (int shift = 1; shift <= 10; ++shift) {
        int target = 0;
        if (shift == 4) target = -2;
        if (shift == 10) target = 2;
        required[shift - 1] = {target - a[shift - 1].r, -a[shift - 1].i};
    }
    return required;
}

bool s_pair_survives(
    unsigned half, unsigned e, int case_index,
    const std::unordered_set<Key, KeyHash>& b_support,
    const std::vector<std::uint32_t>& pair_words,
    std::uint64_t& exact_sum_assignments
) {
    const auto axes = NONCENTER ^ reflected_axes(half);
    const auto real_mask = NONCENTER & ~axes;
    const auto imaginary_mask = axes;
    const int real_count = static_cast<int>(std::popcount(real_mask));
    const int imaginary_count = static_cast<int>(std::popcount(imaginary_mask));
    const unsigned theta = theta_s(half, e);
    for (const auto center : CENTERS) {
        for (unsigned left = 0; left < (1U << 10); ++left) {
            const auto negative = pair_words[(std::size_t{theta} << 10) | left];
            const int sum_r = center.r + real_count
                - 2 * static_cast<int>(std::popcount(real_mask & negative));
            const int sum_i = center.i + imaginary_count
                - 2 * static_cast<int>(std::popcount(imaginary_mask & negative));
            if (sum_r != S_A_TARGETS[case_index][0]
                || sum_i != S_A_TARGETS[case_index][1]) continue;
            auto word = unit_word(axes, negative, true);
            word[0] = center;
            ++exact_sum_assignments;
            if (b_support.contains(pack(s_requirement(paf_definition(word))))) return true;
        }
    }
    return false;
}

}  // namespace

int main(int argc, char** argv) {
    int weight = 4;
    for (int index = 1; index < argc; ++index) {
        const std::string argument = argv[index];
        if (argument == "--weight" && index + 1 < argc) weight = std::stoi(argv[++index]);
        else {
            std::cerr << "usage: " << argv[0] << " --weight 4|8|16\n";
            return 2;
        }
    }
    if (weight != 4 && weight != 8 && weight != 16) {
        std::cerr << "unsupported_weight=" << weight << '\n';
        return 2;
    }

    const auto pair_words = build_pair_words();
    const auto b_orbits = orbit_representatives(weight);
    std::unordered_map<unsigned, std::vector<std::uint32_t>> grouped;
    for (auto b_axis : b_orbits) grouped[signature(b_axis)].push_back(b_axis);

    std::vector<HPair> h_pairs;
    std::uint64_t a_exact_sum_assignments = 0;
    std::uint64_t b_exact_sum_assignments = 0;
    std::uint64_t a_definition_audits = 0;
    std::uint64_t b_definition_audits = 0;
    std::uint64_t processed = 0;
    for (const auto& [e, axes] : grouped) {
        const auto index = build_h_index(
            e, pair_words, a_exact_sum_assignments, a_definition_audits
        );
        for (auto b_axis : axes) {
            const auto survivors = scan_h_b_axis(
                b_axis, weight, index, b_exact_sum_assignments, b_definition_audits
            );
            for (unsigned half = 0; half < (1U << 10); ++half) {
                if (survivors.test(half)) h_pairs.push_back({b_axis, e, half});
            }
            if (++processed % 50 == 0) {
                std::cerr << "processed_b_orbits=" << processed << '/' << b_orbits.size() << '\n';
            }
        }
    }

    std::unordered_set<std::uint32_t> h_b_orbits;
    for (const auto pair : h_pairs) h_b_orbits.insert(pair.b_axis);

    std::uint64_t s_b_assignments = 0;
    std::uint64_t s_a_assignments = 0;
    std::uint64_t case_tests = 0;
    std::uint64_t hs_survivors = 0;
    for (auto b_axis : h_b_orbits) {
        std::array<std::unordered_set<Key, KeyHash>, 6> b_supports;
        for (int case_index = 0; case_index < 6; ++case_index) {
            b_supports[case_index] = build_s_b_support(b_axis, case_index, s_b_assignments);
        }
        for (const auto pair : h_pairs) {
            if (pair.b_axis != b_axis) continue;
            for (int case_index = 0; case_index < 6; ++case_index) {
                ++case_tests;
                hs_survivors += static_cast<std::uint64_t>(s_pair_survives(
                    pair.a_half, pair.signature, case_index, b_supports[case_index],
                    pair_words, s_a_assignments
                ));
            }
        }
    }

    std::cout << "implementation=independent_direct_exact_no_certificate\n";
    std::cout << "producer_stream_used=no\n";
    std::cout << "pi_adic_filter_used=no\n";
    std::cout << "weight=" << weight << '\n';
    std::cout << "axis_words=" << b_orbits.size() * N << '\n';
    std::cout << "rotation_orbits=" << b_orbits.size() << '\n';
    std::cout << "autocorrelation_signatures=" << grouped.size() << '\n';
    std::cout << "a_exact_sum_assignments=" << a_exact_sum_assignments << '\n';
    std::cout << "b_exact_sum_assignments=" << b_exact_sum_assignments << '\n';
    std::cout << "definition_paf_audits=" << a_definition_audits + b_definition_audits << '\n';
    std::cout << "exact_h_surviving_b_orbits=" << h_b_orbits.size() << '\n';
    std::cout << "exact_h_surviving_axis_pairs=" << h_pairs.size() << '\n';
    std::cout << "exact_s_b_assignments=" << s_b_assignments << '\n';
    std::cout << "exact_s_a_assignments=" << s_a_assignments << '\n';
    std::cout << "exact_hs_case_tests=" << case_tests << '\n';
    std::cout << "exact_hs_survivors=" << hs_survivors << '\n';
    std::cout << "exclusion=" << (hs_survivors == 0 ? "verified" : "not_verified") << '\n';
    return hs_survivors == 0 ? 0 : 1;
}
