#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int N = 21;
constexpr std::uint32_t FULL = (std::uint32_t{1} << N) - 1;

struct Gaussian {
    int r;
    int i;
};

Gaussian operator-(Gaussian a, Gaussian b) { return {a.r - b.r, a.i - b.i}; }
Gaussian operator+(Gaussian a, Gaussian b) { return {a.r + b.r, a.i + b.i}; }
bool operator==(Gaussian a, Gaussian b) { return a.r == b.r && a.i == b.i; }

Gaussian multiply(Gaussian a, Gaussian b) {
    return {a.r * b.r - a.i * b.i, a.r * b.i + a.i * b.r};
}

Gaussian conjugate(Gaussian value) { return {value.r, -value.i}; }

Gaussian unit(int axis, int sign) {
    if (axis == 0) return {sign ? -1 : 1, 0};
    return {0, sign ? -1 : 1};
}

struct Key70 {
    std::uint64_t lo{};
    std::uint8_t hi{};
    friend bool operator==(const Key70&, const Key70&) = default;
    friend bool operator<(const Key70& a, const Key70& b) {
        return a.hi < b.hi || (a.hi == b.hi && a.lo < b.lo);
    }
};

struct KeyWide {
    std::uint64_t lo{};
    std::uint64_t hi{};
    friend bool operator==(const KeyWide&, const KeyWide&) = default;
    friend bool operator<(const KeyWide& a, const KeyWide& b) {
        return a.hi < b.hi || (a.hi == b.hi && a.lo < b.lo);
    }
};

struct AxisMask {
    std::array<std::uint64_t, 16> words{};
    void set(unsigned axis) { words[axis / 64] |= std::uint64_t{1} << (axis % 64); }
    AxisMask& operator|=(const AxisMask& other) {
        for (std::size_t index = 0; index < words.size(); ++index) words[index] |= other.words[index];
        return *this;
    }
    std::uint64_t count() const {
        std::uint64_t result = 0;
        for (auto word : words) result += std::popcount(word);
        return result;
    }
    bool test(unsigned axis) const { return (words[axis / 64] >> (axis % 64)) & 1U; }
    std::string hex() const {
        std::ostringstream stream;
        stream << std::hex << std::setfill('0');
        for (auto iterator = words.rbegin(); iterator != words.rend(); ++iterator) {
            stream << std::setw(16) << *iterator;
        }
        return stream.str();
    }
};

template <class Key>
struct AEntry {
    Key key;
    AxisMask axes;
    std::uint32_t assignments{};
};

template <class Key>
struct RawAEntry {
    Key key;
    std::uint16_t axis;
};

struct AMaps {
    std::array<std::vector<AEntry<std::uint64_t>>, 3> low;
    std::vector<AEntry<Key70>> seventh;
    std::uint64_t exact_sum_assignments{};
};

struct HighMaps {
    std::array<std::vector<AEntry<KeyWide>>, 5> orders;
    std::uint64_t exact_sum_assignments{};
};

struct Match {
    AxisMask axes;
    std::uint64_t assignments{};
};

struct OrbitResult {
    std::uint32_t b_axis{};
    unsigned signature{};
    std::array<std::uint64_t, 9> b_fingerprints{};
    std::array<AxisMask, 9> axes;
    std::array<std::uint64_t, 9> a_assignment_hits{};
};

std::uint32_t rotate(std::uint32_t mask, int shift) {
    shift %= N;
    return ((mask << shift) | (mask >> (N - shift))) & FULL;
}

int bit(std::uint32_t mask, int index) { return int((mask >> index) & 1U); }

unsigned pi_residue(Gaussian value, int power) {
    unsigned result = 0;
    for (int place = 0; place < power; ++place) {
        const int digit = (value.r + value.i) & 1;
        result |= unsigned(digit) << place;
        value.r -= digit;
        const int old_r = value.r;
        const int old_i = value.i;
        assert(((old_r + old_i) & 1) == 0);
        value = {(old_r + old_i) / 2, (old_i - old_r) / 2};
    }
    return result;
}

std::uint64_t stable_mix(std::uint64_t value) {
    value += 0x9e3779b97f4a7c15ULL;
    value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
    value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
    return value ^ (value >> 31);
}

bool audit_a(unsigned signature, unsigned a_half, unsigned pair_signs) {
    const std::uint64_t key = (std::uint64_t{signature} << 20)
        | (std::uint64_t{a_half} << 10) | pair_signs;
    return stable_mix(key) % 8191 == 0;
}

bool audit_b(std::uint32_t b_axis, std::uint32_t signs) {
    const std::uint64_t key = (std::uint64_t{b_axis} << 21) | signs;
    return stable_mix(key) % 8191 == 0;
}

Key70 key7(const std::array<Gaussian, 10>& values) {
    Key70 result;
    for (int shift = 0; shift < 9; ++shift) {
        result.lo |= std::uint64_t(pi_residue(values[shift], 7)) << (7 * shift);
    }
    result.hi = static_cast<std::uint8_t>(pi_residue(values[9], 7));
    return result;
}

std::uint64_t truncate_key(Key70 key, int power) {
    assert(power >= 4 && power <= 6);
    const std::uint64_t mask = (std::uint64_t{1} << power) - 1;
    std::uint64_t result = 0;
    for (int shift = 0; shift < 9; ++shift) {
        result |= ((key.lo >> (7 * shift)) & 0x7fU & mask) << (power * shift);
    }
    result |= (std::uint64_t(key.hi) & mask) << (power * 9);
    return result;
}

KeyWide key_wide(const std::array<Gaussian, 10>& values, int power) {
    assert(power >= 8 && power <= 12);
    KeyWide result;
    for (int shift = 0; shift < 10; ++shift) {
        const std::uint64_t value = pi_residue(values[shift], power);
        const int offset = power * shift;
        if (offset < 64) {
            result.lo |= value << offset;
            if (offset + power > 64) result.hi |= value >> (64 - offset);
        } else {
            result.hi |= value << (offset - 64);
        }
    }
    return result;
}

KeyWide required_b_wide_key(const std::array<Gaussian, 10>& a, int power) {
    std::array<Gaussian, 10> required{};
    for (int shift = 0; shift < 10; ++shift) required[shift] = Gaussian{-2, 0} - a[shift];
    return key_wide(required, power);
}

std::array<Gaussian, 10> paf_fast(
    std::uint32_t axes, std::uint32_t signs, bool zero_at_origin
) {
    std::array<Gaussian, 10> result{};
    for (int shift = 1; shift <= 10; ++shift) {
        const std::uint32_t next_axes = rotate(axes, N - shift);
        const std::uint32_t next_signs = rotate(signs, N - shift);
        std::uint32_t valid = FULL;
        if (zero_at_origin) valid ^= 1U | (std::uint32_t{1} << (N - shift));
        const std::uint32_t same = valid & ~(axes ^ next_axes) & FULL;
        const std::uint32_t up = valid & axes & ~next_axes;
        const std::uint32_t down = valid & ~axes & next_axes;
        const std::uint32_t different_sign = valid & (signs ^ next_signs);
        const int real = int(std::popcount(same)) - 2 * int(std::popcount(same & different_sign));
        const int imag = int(std::popcount(up)) - int(std::popcount(down))
            - 2 * (int(std::popcount(up & different_sign)) - int(std::popcount(down & different_sign)));
        result[shift - 1] = {real, imag};
    }
    return result;
}

std::array<Gaussian, 10> paf_direct(
    std::uint32_t axes, std::uint32_t signs, bool zero_at_origin
) {
    std::array<Gaussian, 10> result{};
    for (int shift = 1; shift <= 10; ++shift) {
        Gaussian total{0, 0};
        for (int j = 0; j < N; ++j) {
            const int k = (j + shift) % N;
            if (zero_at_origin && (j == 0 || k == 0)) continue;
            const int sj = bit(signs, j) ? -1 : 1;
            const int sk = bit(signs, k) ? -1 : 1;
            const int aj = bit(axes, j);
            const int ak = bit(axes, k);
            if (aj == ak) total.r += sj * sk;
            else if (aj == 1) total.i += sj * sk;
            else total.i -= sj * sk;
        }
        result[shift - 1] = total;
    }
    return result;
}

Key70 required_b_key(const std::array<Gaussian, 10>& a) {
    std::array<Gaussian, 10> required{};
    for (int shift = 0; shift < 10; ++shift) required[shift] = Gaussian{-2, 0} - a[shift];
    return key7(required);
}

std::uint32_t reflected_axes(unsigned half) {
    std::uint32_t result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        if ((half >> (shift - 1)) & 1U) {
            result |= (std::uint32_t{1} << shift) | (std::uint32_t{1} << (N - shift));
        }
    }
    return result;
}

unsigned autocorrelation_signature(std::uint32_t mask) {
    const int parity = int(std::popcount(mask)) & 1;
    unsigned result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        const int overlap = int(std::popcount(mask & rotate(mask, shift))) & 1;
        result |= unsigned(parity ^ overlap) << (shift - 1);
    }
    return result;
}

unsigned theta_h(unsigned a_half, unsigned signature) {
    const std::uint32_t a = reflected_axes(a_half);
    unsigned result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        const int a_shift = int((a_half >> (shift - 1)) & 1U);
        const int c_a = int(std::popcount(a & rotate(a, shift))) & 1;
        const int e = int((signature >> (shift - 1)) & 1U);
        result |= unsigned(1 ^ a_shift ^ c_a ^ e) << (shift - 1);
    }
    return result;
}

unsigned theta_s(unsigned a_half, unsigned signature) {
    const std::uint32_t a = reflected_axes(a_half);
    const std::uint32_t f = (FULL ^ 1U) ^ a;
    unsigned result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        const int f_shift = 1 ^ int((a_half >> (shift - 1)) & 1U);
        const int c_f = int(std::popcount(f & rotate(f, shift))) & 1;
        const int e = int((signature >> (shift - 1)) & 1U);
        const int tau = (shift == 4 || shift == 10) ? 1 : 0;
        result |= unsigned(1 ^ f_shift ^ c_f ^ e ^ tau) << (shift - 1);
    }
    return result;
}

std::array<Gaussian, 10> paf_gaussian(const std::array<Gaussian, N>& word) {
    std::array<Gaussian, 10> result{};
    for (int shift = 1; shift <= 10; ++shift) {
        Gaussian total{0, 0};
        for (int j = 0; j < N; ++j) {
            total = total + multiply(word[j], conjugate(word[(j + shift) % N]));
        }
        result[shift - 1] = total;
    }
    return result;
}

Gaussian s_target(int shift) {
    if (shift == 4) return {-2, 0};
    if (shift == 10) return {2, 0};
    return {0, 0};
}

KeyWide required_s_b_key(const std::array<Gaussian, 10>& a) {
    std::array<Gaussian, 10> required{};
    for (int shift = 1; shift <= 10; ++shift) required[shift - 1] = s_target(shift) - a[shift - 1];
    return key_wide(required, 12);
}

std::vector<std::uint32_t> fixed_submasks(std::uint32_t mask, int weight) {
    std::vector<int> positions;
    for (int index = 0; index < N; ++index) if (bit(mask, index)) positions.push_back(index);
    assert(weight >= 0 && weight <= int(positions.size()));
    std::vector<std::uint32_t> result;
    if (weight == 0) return {0};
    std::uint32_t choice = (std::uint32_t{1} << weight) - 1;
    const std::uint32_t limit = std::uint32_t{1} << positions.size();
    while (choice < limit) {
        std::uint32_t expanded = 0;
        for (std::size_t local = 0; local < positions.size(); ++local) {
            if ((choice >> local) & 1U) expanded |= std::uint32_t{1} << positions[local];
        }
        result.push_back(expanded);
        const std::uint32_t low = choice & -choice;
        const std::uint32_t next = choice + low;
        choice = (((next ^ choice) >> 2) / low) | next;
    }
    return result;
}

std::vector<std::uint32_t> weight4_orbit_representatives() {
    std::vector<std::uint32_t> result;
    for (std::uint32_t value : fixed_submasks(FULL, 4)) {
        std::uint32_t canonical = value;
        for (int shift = 1; shift < N; ++shift) canonical = std::min(canonical, rotate(value, shift));
        if (value == canonical) result.push_back(value);
    }
    assert(result.size() == 285);
    assert(result.size() * N == 5985);
    return result;
}

template <class Key>
std::vector<AEntry<Key>> group_a_entries(std::vector<RawAEntry<Key>> raw) {
    std::sort(raw.begin(), raw.end(), [](const auto& a, const auto& b) {
        return a.key < b.key || (!(b.key < a.key) && a.axis < b.axis);
    });
    std::vector<AEntry<Key>> result;
    for (const auto& item : raw) {
        if (result.empty() || !(result.back().key == item.key)) result.push_back({item.key, {}, 0});
        result.back().axes.set(item.axis);
        ++result.back().assignments;
    }
    return result;
}

AMaps build_a_maps(unsigned signature, std::uint64_t& direct_checks) {
    std::array<std::vector<RawAEntry<std::uint64_t>>, 3> low;
    std::vector<RawAEntry<Key70>> seventh;
    AMaps maps;
    for (unsigned a_half = 0; a_half < (1U << 10); ++a_half) {
        const std::uint32_t axes = reflected_axes(a_half);
        const unsigned theta = theta_h(a_half, signature);
        for (unsigned pair_signs = 0; pair_signs < (1U << 10); ++pair_signs) {
            std::uint32_t signs = 0;
            int sum_r = 0;
            int sum_i = 0;
            for (int pair = 0; pair < 10; ++pair) {
                const int shift = pair + 1;
                const int left = int((pair_signs >> pair) & 1U);
                const int right = left ^ int((theta >> pair) & 1U);
                if (left) signs |= std::uint32_t{1} << shift;
                if (right) signs |= std::uint32_t{1} << (N - shift);
                const int coefficient = (left ? -1 : 1) + (right ? -1 : 1);
                if (bit(axes, shift)) sum_i += coefficient;
                else sum_r += coefficient;
            }
            if (sum_r != 0 || sum_i != 0) continue;
            const auto values = paf_fast(axes, signs, true);
            if (audit_a(signature, a_half, pair_signs)) {
                assert(values == paf_direct(axes, signs, true));
                ++direct_checks;
            }
            const Key70 key = required_b_key(values);
            seventh.push_back({key, static_cast<std::uint16_t>(a_half)});
            for (int power = 4; power <= 6; ++power) {
                low[power - 4].push_back({truncate_key(key, power), static_cast<std::uint16_t>(a_half)});
            }
            ++maps.exact_sum_assignments;
        }
    }
    for (int index = 0; index < 3; ++index) maps.low[index] = group_a_entries(std::move(low[index]));
    maps.seventh = group_a_entries(std::move(seventh));
    return maps;
}

HighMaps build_a_high_maps(unsigned signature) {
    std::array<std::vector<RawAEntry<KeyWide>>, 5> raw;
    HighMaps maps;
    for (unsigned a_half = 0; a_half < (1U << 10); ++a_half) {
        const std::uint32_t axes = reflected_axes(a_half);
        const unsigned theta = theta_h(a_half, signature);
        for (unsigned pair_signs = 0; pair_signs < (1U << 10); ++pair_signs) {
            std::uint32_t signs = 0;
            int sum_r = 0;
            int sum_i = 0;
            for (int pair = 0; pair < 10; ++pair) {
                const int shift = pair + 1;
                const int left = int((pair_signs >> pair) & 1U);
                const int right = left ^ int((theta >> pair) & 1U);
                if (left) signs |= std::uint32_t{1} << shift;
                if (right) signs |= std::uint32_t{1} << (N - shift);
                const int coefficient = (left ? -1 : 1) + (right ? -1 : 1);
                if (bit(axes, shift)) sum_i += coefficient;
                else sum_r += coefficient;
            }
            if (sum_r != 0 || sum_i != 0) continue;
            const auto values = paf_fast(axes, signs, true);
            for (int power = 8; power <= 12; ++power) {
                raw[power - 8].push_back(
                    {required_b_wide_key(values, power), static_cast<std::uint16_t>(a_half)}
                );
            }
            ++maps.exact_sum_assignments;
        }
    }
    for (int index = 0; index < 5; ++index) maps.orders[index] = group_a_entries(std::move(raw[index]));
    return maps;
}

template <class Key>
Match intersect(const std::vector<AEntry<Key>>& a, const std::vector<Key>& b) {
    Match result;
    std::size_t left = 0;
    std::size_t right = 0;
    while (left < a.size() && right < b.size()) {
        if (a[left].key < b[right]) ++left;
        else if (b[right] < a[left].key) ++right;
        else {
            result.axes |= a[left].axes;
            result.assignments += a[left].assignments;
            ++left;
            ++right;
        }
    }
    return result;
}

OrbitResult scan_b_orbit(
    std::uint32_t b_axis, const AMaps& a_maps, std::uint64_t& b_assignments,
    std::uint64_t& direct_checks
) {
    assert(std::popcount(b_axis) == 4);
    const auto imaginary_choices = fixed_submasks(b_axis, 2);
    const auto real_choices = fixed_submasks(FULL ^ b_axis, 8);
    assert(imaginary_choices.size() == 6);
    assert(real_choices.size() == 24310);
    std::vector<Key70> seventh;
    seventh.reserve(145860);
    for (auto imaginary : imaginary_choices) {
        for (auto real : real_choices) {
            const std::uint32_t signs = imaginary | real;
            const auto values = paf_fast(b_axis, signs, false);
            if (audit_b(b_axis, signs)) {
                assert(values == paf_direct(b_axis, signs, false));
                ++direct_checks;
            }
            seventh.push_back(key7(values));
        }
    }
    b_assignments += seventh.size();
    std::sort(seventh.begin(), seventh.end());
    seventh.erase(std::unique(seventh.begin(), seventh.end()), seventh.end());

    std::array<std::vector<std::uint64_t>, 3> low;
    for (int power = 4; power <= 6; ++power) {
        auto& values = low[power - 4];
        values.reserve(seventh.size());
        for (auto key : seventh) values.push_back(truncate_key(key, power));
        std::sort(values.begin(), values.end());
        values.erase(std::unique(values.begin(), values.end()), values.end());
    }

    OrbitResult result;
    result.b_axis = b_axis;
    result.signature = autocorrelation_signature(b_axis);
    for (int index = 0; index < 3; ++index) {
        const Match match = intersect(a_maps.low[index], low[index]);
        result.b_fingerprints[index] = low[index].size();
        result.axes[index] = match.axes;
        result.a_assignment_hits[index] = match.assignments;
    }
    const Match seventh_match = intersect(a_maps.seventh, seventh);
    result.b_fingerprints[3] = seventh.size();
    result.axes[3] = seventh_match.axes;
    result.a_assignment_hits[3] = seventh_match.assignments;
    return result;
}

void deepen_b_orbit(std::uint32_t b_axis, const HighMaps& a_maps, OrbitResult& result) {
    const auto imaginary_choices = fixed_submasks(b_axis, 2);
    const auto real_choices = fixed_submasks(FULL ^ b_axis, 8);
    std::array<std::vector<KeyWide>, 5> supports;
    for (auto& support : supports) support.reserve(145860);
    for (auto imaginary : imaginary_choices) {
        for (auto real : real_choices) {
            const auto values = paf_fast(b_axis, imaginary | real, false);
            for (int power = 8; power <= 12; ++power) {
                supports[power - 8].push_back(key_wide(values, power));
            }
        }
    }
    for (int index = 0; index < 5; ++index) {
        auto& support = supports[index];
        std::sort(support.begin(), support.end());
        support.erase(std::unique(support.begin(), support.end()), support.end());
        const Match match = intersect(a_maps.orders[index], support);
        result.b_fingerprints[index + 4] = support.size();
        result.axes[index + 4] = match.axes;
        result.a_assignment_hits[index + 4] = match.assignments;
    }
}

constexpr std::array<std::array<int, 2>, 6> S_A_TARGETS{{
    {{1, -1}}, {{3, -3}}, {{3, -3}}, {{5, -1}}, {{5, -1}}, {{5, -3}}
}};
constexpr std::array<std::array<int, 2>, 6> S_B_TARGETS{{
    {{4, -5}}, {{4, -3}}, {{0, -5}}, {{4, -1}}, {{4, 1}}, {{0, -3}}
}};
constexpr std::array<Gaussian, 4> S_A_CENTERS{{
    {1, 1}, {-1, 1}, {-1, -1}, {1, -1}
}};

std::vector<KeyWide> exact_s_b_support(std::uint32_t h_b_axis, int case_index, std::uint64_t& assignments) {
    const std::uint32_t s_axes = FULL ^ h_b_axis;
    const int target_r = S_B_TARGETS[case_index][0];
    const int target_i = S_B_TARGETS[case_index][1];
    const int real_count = N - int(std::popcount(s_axes));
    const int imag_count = int(std::popcount(s_axes));
    const int negative_real = (real_count - target_r) / 2;
    const int negative_imag = (imag_count - target_i) / 2;
    assert(2 * negative_real == real_count - target_r);
    assert(2 * negative_imag == imag_count - target_i);
    const auto real_choices = fixed_submasks(FULL ^ s_axes, negative_real);
    const auto imag_choices = fixed_submasks(s_axes, negative_imag);
    std::vector<KeyWide> support;
    support.reserve(real_choices.size() * imag_choices.size());
    for (auto real : real_choices) {
        for (auto imag : imag_choices) {
            support.push_back(key_wide(paf_fast(s_axes, real | imag, false), 12));
        }
    }
    assignments += support.size();
    std::sort(support.begin(), support.end());
    support.erase(std::unique(support.begin(), support.end()), support.end());
    return support;
}

std::vector<KeyWide> exact_s_a_requirements(
    unsigned a_half, unsigned signature, int case_index, std::uint64_t& assignments
) {
    const std::uint32_t h_axes = reflected_axes(a_half);
    const std::uint32_t s_axes = (FULL ^ 1U) ^ h_axes;
    const unsigned theta = theta_s(a_half, signature);
    const int target_r = S_A_TARGETS[case_index][0];
    const int target_i = S_A_TARGETS[case_index][1];
    std::vector<KeyWide> requirements;
    for (Gaussian center : S_A_CENTERS) {
        for (unsigned pair_signs = 0; pair_signs < (1U << 10); ++pair_signs) {
            std::array<Gaussian, N> word{};
            word[0] = center;
            Gaussian sum = center;
            for (int pair = 0; pair < 10; ++pair) {
                const int shift = pair + 1;
                const int left = int((pair_signs >> pair) & 1U);
                const int right = left ^ int((theta >> pair) & 1U);
                const int axis = bit(s_axes, shift);
                word[shift] = unit(axis, left);
                word[N - shift] = unit(axis, right);
                sum = sum + word[shift] + word[N - shift];
            }
            if (sum.r != target_r || sum.i != target_i) continue;
            requirements.push_back(required_s_b_key(paf_gaussian(word)));
            ++assignments;
        }
    }
    std::sort(requirements.begin(), requirements.end());
    requirements.erase(std::unique(requirements.begin(), requirements.end()), requirements.end());
    return requirements;
}

bool intersects(const std::vector<KeyWide>& left, const std::vector<KeyWide>& right) {
    std::size_t i = 0;
    std::size_t j = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i] < right[j]) ++i;
        else if (right[j] < left[i]) ++j;
        else return true;
    }
    return false;
}

}  // namespace

int main(int argc, char** argv) {
    bool emit_stream = false;
    unsigned shard_count = 1;
    unsigned shard_index = 0;
    for (int argument = 1; argument < argc; ++argument) {
        const std::string value = argv[argument];
        if (value == "--stream") emit_stream = true;
        else if (value == "--shard-count" && argument + 1 < argc) {
            shard_count = static_cast<unsigned>(std::stoul(argv[++argument]));
        } else if (value == "--shard-index" && argument + 1 < argc) {
            shard_index = static_cast<unsigned>(std::stoul(argv[++argument]));
        } else {
            std::cerr << "unknown_argument=" << value << '\n';
            return 2;
        }
    }
    if (shard_count == 0 || shard_index >= shard_count) {
        std::cerr << "invalid_shard=" << shard_index << "/" << shard_count << '\n';
        return 2;
    }
    const auto b_orbits = weight4_orbit_representatives();
    std::map<unsigned, std::vector<std::uint32_t>> by_signature;
    for (auto b : b_orbits) by_signature[autocorrelation_signature(b)].push_back(b);

    std::vector<OrbitResult> results;
    std::uint64_t b_assignments = 0;
    std::uint64_t a_assignment_orbit_checks = 0;
    std::uint64_t direct_checks = 0;
    std::uint64_t processed = 0;
    std::uint64_t processed_signatures = 0;
    std::uint64_t signature_ordinal = 0;
    for (const auto& [signature, masks] : by_signature) {
        if (signature_ordinal++ % shard_count != shard_index) continue;
        ++processed_signatures;
        const AMaps a_maps = build_a_maps(signature, direct_checks);
        a_assignment_orbit_checks += a_maps.exact_sum_assignments * masks.size();
        for (auto b : masks) {
            results.push_back(scan_b_orbit(b, a_maps, b_assignments, direct_checks));
            ++processed;
            if (processed % 50 == 0) std::cerr << "processed_b_orbits=" << processed << '\n';
        }
    }
    std::sort(results.begin(), results.end(), [](const auto& a, const auto& b) {
        return a.b_axis < b.b_axis;
    });

    std::map<unsigned, HighMaps> high_cache;
    std::uint64_t deepened_orbits = 0;
    for (auto& result : results) {
        if (result.axes[3].count() == 0) continue;
        auto iterator = high_cache.find(result.signature);
        if (iterator == high_cache.end()) {
            iterator = high_cache.emplace(result.signature, build_a_high_maps(result.signature)).first;
        }
        assert(iterator->second.exact_sum_assignments > 0);
        deepen_b_orbit(result.b_axis, iterator->second, result);
        ++deepened_orbits;
    }

    std::array<std::uint64_t, 6> exact_h_input_pairs{};
    std::array<std::uint64_t, 6> exact_hs_surviving_pairs{};
    std::uint64_t exact_s_b_assignments = 0;
    std::uint64_t exact_s_a_assignments = 0;
    std::map<std::tuple<unsigned, unsigned, int>, std::vector<KeyWide>> s_a_cache;
    for (const auto& result : results) {
        if (result.axes[8].count() == 0) continue;
        std::array<std::vector<KeyWide>, 6> s_b_supports;
        for (int case_index = 0; case_index < 6; ++case_index) {
            s_b_supports[case_index] = exact_s_b_support(
                result.b_axis, case_index, exact_s_b_assignments
            );
        }
        for (unsigned a_half = 0; a_half < (1U << 10); ++a_half) {
            if (!result.axes[8].test(a_half)) continue;
            for (int case_index = 0; case_index < 6; ++case_index) {
                ++exact_h_input_pairs[case_index];
                const auto cache_key = std::make_tuple(result.signature, a_half, case_index);
                auto iterator = s_a_cache.find(cache_key);
                if (iterator == s_a_cache.end()) {
                    iterator = s_a_cache.emplace(
                        cache_key,
                        exact_s_a_requirements(
                            a_half, result.signature, case_index, exact_s_a_assignments
                        )
                    ).first;
                }
                if (intersects(iterator->second, s_b_supports[case_index])) {
                    ++exact_hs_surviving_pairs[case_index];
                }
            }
        }
    }

    std::array<std::uint64_t, 9> orbit_pairs{};
    std::array<std::uint64_t, 9> b_orbits_with_survivors{};
    std::array<std::uint64_t, 9> assignment_hits{};
    std::array<std::uint64_t, 9> fingerprint_min{};
    std::array<std::uint64_t, 9> fingerprint_max{};
    std::array<std::uint64_t, 9> fingerprint_sum{};
    fingerprint_min.fill(UINT64_MAX);
    for (const auto& result : results) {
        for (int order = 0; order < 9; ++order) {
            if (order >= 4 && result.b_fingerprints[order] == 0) continue;
            const auto count = result.axes[order].count();
            orbit_pairs[order] += count;
            b_orbits_with_survivors[order] += count != 0;
            assignment_hits[order] += result.a_assignment_hits[order];
            fingerprint_min[order] = std::min(fingerprint_min[order], result.b_fingerprints[order]);
            fingerprint_max[order] = std::max(fingerprint_max[order], result.b_fingerprints[order]);
            fingerprint_sum[order] += result.b_fingerprints[order];
        }
    }

    std::cout << "b_axis_weight=4\n";
    std::cout << "manifest_b_axis_words=5985\n";
    std::cout << "manifest_b_rotation_orbits=285\n";
    std::cout << "shard_count=" << shard_count << '\n';
    std::cout << "shard_index=" << shard_index << '\n';
    std::cout << "b_axis_words=" << N * results.size() << '\n';
    std::cout << "b_rotation_orbits=" << results.size() << '\n';
    std::cout << "b_signatures=" << processed_signatures << '\n';
    std::cout << "b_exact_sum_assignments_per_orbit=145860\n";
    std::cout << "b_exact_sum_assignments_evaluated=" << b_assignments << '\n';
    std::cout << "a_assignment_orbit_checks=" << a_assignment_orbit_checks << '\n';
    std::cout << "direct_paf_audits=" << direct_checks << '\n';
    std::cout << "deepened_seventh_order_b_orbits=" << deepened_orbits << '\n';
    std::cout << "deepened_signatures=" << high_cache.size() << '\n';
    for (int index = 0; index < 9; ++index) {
        const int power = index + 4;
        std::cout << "order_" << power << "_b_fingerprint_min=" << fingerprint_min[index] << '\n';
        std::cout << "order_" << power << "_b_fingerprint_max=" << fingerprint_max[index] << '\n';
        std::cout << "order_" << power << "_b_fingerprint_sum=" << fingerprint_sum[index] << '\n';
        std::cout << "order_" << power << "_b_orbits_with_survivors=" << b_orbits_with_survivors[index] << '\n';
        std::cout << "order_" << power << "_surviving_axis_orbits=" << orbit_pairs[index] << '\n';
        std::cout << "order_" << power << "_surviving_labeled_axis_pairs=" << 21 * orbit_pairs[index] << '\n';
        std::cout << "order_" << power << "_compatible_a_assignments=" << assignment_hits[index] << '\n';
    }
    std::cout << "seventh_order_weight4_exclusion=" << (orbit_pairs[3] == 0 ? "verified" : "not_obtained") << '\n';
    int first_empty_order = 0;
    for (int index = 0; index < 9; ++index) {
        if (orbit_pairs[index] == 0) {
            first_empty_order = index + 4;
            break;
        }
    }
    std::cout << "first_empty_order=" << first_empty_order << '\n';
    std::cout << "exact_weight4_exclusion=" << (orbit_pairs[8] == 0 ? "verified" : "not_obtained") << '\n';
    std::cout << "exact_s_b_assignments_evaluated=" << exact_s_b_assignments << '\n';
    std::cout << "exact_s_a_assignments_evaluated=" << exact_s_a_assignments << '\n';
    for (int case_index = 0; case_index < 6; ++case_index) {
        std::cout << "case_" << case_index << "_exact_h_input_axis_orbits="
                  << exact_h_input_pairs[case_index] << '\n';
        std::cout << "case_" << case_index << "_exact_hs_surviving_axis_orbits="
                  << exact_hs_surviving_pairs[case_index] << '\n';
    }
    const auto full_survivors = std::accumulate(
        exact_hs_surviving_pairs.begin(), exact_hs_surviving_pairs.end(), std::uint64_t{0}
    );
    std::cout << "exact_hs_surviving_axis_case_orbits=" << full_survivors << '\n';
    std::cout << "full_weight4_exclusion=" << (full_survivors == 0 ? "verified" : "not_obtained") << '\n';

    if (emit_stream) {
        std::cout << "stream_begin\n";
        std::cout << "b_axis\tsignature\tb4\tb5\tb6\tb7\tb8\tb9\tb10\tb11\tb12"
                     "\ta4_mask\ta5_mask\ta6_mask\ta7_mask\ta8_mask\ta9_mask\ta10_mask\ta11_mask\ta12_mask\n";
        for (const auto& result : results) {
            std::cout << std::hex << std::setfill('0') << std::setw(6) << result.b_axis
                      << '\t' << std::setw(3) << result.signature << std::dec;
            for (auto count : result.b_fingerprints) std::cout << '\t' << count;
            for (const auto& mask : result.axes) std::cout << '\t' << mask.hex();
            std::cout << '\n';
        }
        std::cout << "stream_end\n";
    }
}
