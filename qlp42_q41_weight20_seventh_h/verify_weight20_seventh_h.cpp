#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <unordered_set>
#include <vector>

namespace {

constexpr int N = 21;
constexpr std::uint32_t FULL = (std::uint32_t{1} << N) - 1;

struct Gaussian {
    int r;
    int i;
};

using ExactPAF = std::array<std::int8_t, 20>;
using ResiduePAF = std::array<std::uint8_t, 10>;

Gaussian operator+(Gaussian a, Gaussian b) { return {a.r + b.r, a.i + b.i}; }
Gaussian operator-(Gaussian a, Gaussian b) { return {a.r - b.r, a.i - b.i}; }

Gaussian multiply(Gaussian a, Gaussian b) {
    return {a.r * b.r - a.i * b.i, a.r * b.i + a.i * b.r};
}

Gaussian conjugate(Gaussian a) { return {a.r, -a.i}; }

Gaussian unit(int axis, int sign) {
    if (axis == 0) return {sign ? -1 : 1, 0};
    return {0, sign ? -1 : 1};
}

std::uint32_t rotate(std::uint32_t mask, int shift) {
    shift %= N;
    return ((mask << shift) | (mask >> (N - shift))) & FULL;
}

int bit(std::uint32_t mask, int index) { return int((mask >> index) & 1U); }

std::array<Gaussian, 10> paf(const std::array<Gaussian, N>& word) {
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

std::uint64_t fingerprint(const std::array<Gaussian, 10>& values, int power) {
    std::uint64_t result = 0;
    for (int shift = 0; shift < 10; ++shift) {
        result |= std::uint64_t(pi_residue(values[shift], power)) << (power * shift);
    }
    return result;
}

std::uint64_t required_b_fingerprint(const std::array<Gaussian, 10>& a, int power) {
    std::array<Gaussian, 10> required{};
    for (int shift = 0; shift < 10; ++shift) required[shift] = Gaussian{-2, 0} - a[shift];
    return fingerprint(required, power);
}

ExactPAF exact_paf_record(const std::array<Gaussian, 10>& values) {
    ExactPAF result{};
    for (int shift = 0; shift < 10; ++shift) {
        assert(values[shift].r >= -127 && values[shift].r <= 127);
        assert(values[shift].i >= -127 && values[shift].i <= 127);
        result[2 * shift] = static_cast<std::int8_t>(values[shift].r);
        result[2 * shift + 1] = static_cast<std::int8_t>(values[shift].i);
    }
    return result;
}

ExactPAF required_exact_b_record(const std::array<Gaussian, 10>& a) {
    std::array<Gaussian, 10> required{};
    for (int shift = 0; shift < 10; ++shift) required[shift] = Gaussian{-2, 0} - a[shift];
    return exact_paf_record(required);
}

ResiduePAF residue_paf_record(const std::array<Gaussian, 10>& values, int power) {
    ResiduePAF result{};
    for (int shift = 0; shift < 10; ++shift) {
        result[shift] = static_cast<std::uint8_t>(pi_residue(values[shift], power));
    }
    return result;
}

ResiduePAF required_b_residue_record(const std::array<Gaussian, 10>& a, int power) {
    std::array<Gaussian, 10> required{};
    for (int shift = 0; shift < 10; ++shift) required[shift] = Gaussian{-2, 0} - a[shift];
    return residue_paf_record(required, power);
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
    const int parity = __builtin_popcount(mask) & 1;
    unsigned result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        const int overlap = __builtin_popcount(mask & rotate(mask, shift)) & 1;
        result |= unsigned(parity ^ overlap) << (shift - 1);
    }
    return result;
}

unsigned theta_h(unsigned a_half, unsigned e_signature) {
    const std::uint32_t a = reflected_axes(a_half);
    unsigned result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        const int a_shift = int((a_half >> (shift - 1)) & 1U);
        const int c_a = __builtin_popcount(a & rotate(a, shift)) & 1;
        const int e = int((e_signature >> (shift - 1)) & 1U);
        result |= unsigned(1 ^ a_shift ^ c_a ^ e) << (shift - 1);
    }
    return result;
}

unsigned theta_s(unsigned a_half, unsigned e_signature) {
    const std::uint32_t a = reflected_axes(a_half);
    const std::uint32_t f = (FULL ^ 1U) ^ a;
    unsigned result = 0;
    for (int shift = 1; shift <= 10; ++shift) {
        const int f_shift = 1 ^ int((a_half >> (shift - 1)) & 1U);
        const int c_f = __builtin_popcount(f & rotate(f, shift)) & 1;
        const int e = int((e_signature >> (shift - 1)) & 1U);
        const int tau = (shift == 4 || shift == 10) ? 1 : 0;
        result |= unsigned(1 ^ f_shift ^ c_f ^ e ^ tau) << (shift - 1);
    }
    return result;
}

Gaussian s_target(int shift) {
    if (shift == 4) return {-2, 0};
    if (shift == 10) return {2, 0};
    return {0, 0};
}

std::uint64_t required_s_b_fingerprint(const std::array<Gaussian, 10>& a, int power) {
    std::array<Gaussian, 10> required{};
    for (int shift = 1; shift <= 10; ++shift) required[shift - 1] = s_target(shift) - a[shift - 1];
    return fingerprint(required, power);
}

struct BRecords {
    std::unordered_set<std::uint64_t> fourth;
    std::unordered_set<std::uint64_t> fifth;
    std::unordered_set<std::uint64_t> sixth;
    std::vector<ResiduePAF> seventh;
    std::vector<ExactPAF> exact;
};

BRecords enumerate_b(std::uint32_t b_mask) {
    std::vector<int> imaginary;
    int real_position = -1;
    for (int j = 0; j < N; ++j) {
        if (bit(b_mask, j)) imaginary.push_back(j);
        else real_position = j;
    }
    assert(imaginary.size() == 20 && real_position >= 0);

    std::unordered_set<std::uint64_t> fourth;
    std::unordered_set<std::uint64_t> fifth;
    std::unordered_set<std::uint64_t> sixth;
    std::vector<ResiduePAF> seventh;
    seventh.reserve(184756);
    std::vector<ExactPAF> exact;
    exact.reserve(184756);
    std::uint32_t choose = (std::uint32_t{1} << 10) - 1;
    const std::uint32_t limit = std::uint32_t{1} << 20;
    std::uint64_t assignments = 0;
    while (choose < limit) {
        std::array<Gaussian, N> word{};
        word[real_position] = unit(0, 0);
        for (int k = 0; k < 20; ++k) word[imaginary[k]] = unit(1, bit(choose, k));
        const auto values = paf(word);
        fourth.insert(fingerprint(values, 4));
        fifth.insert(fingerprint(values, 5));
        sixth.insert(fingerprint(values, 6));
        seventh.push_back(residue_paf_record(values, 7));
        exact.push_back(exact_paf_record(values));
        ++assignments;

        const std::uint32_t low = choose & -choose;
        const std::uint32_t next = choose + low;
        choose = (((next ^ choose) >> 2) / low) | next;
    }
    assert(assignments == 184756);
    std::sort(exact.begin(), exact.end());
    exact.erase(std::unique(exact.begin(), exact.end()), exact.end());
    std::sort(seventh.begin(), seventh.end());
    seventh.erase(std::unique(seventh.begin(), seventh.end()), seventh.end());
    std::cout << "b_exact_sum_assignments=" << assignments << '\n';
    std::cout << "b_fourth_fingerprints=" << fourth.size() << '\n';
    std::cout << "b_fifth_fingerprints=" << fifth.size() << '\n';
    std::cout << "b_sixth_fingerprints=" << sixth.size() << '\n';
    std::cout << "b_seventh_fingerprints=" << seventh.size() << '\n';
    std::cout << "b_exact_paf_vectors=" << exact.size() << '\n';
    return {
        std::move(fourth), std::move(fifth), std::move(sixth),
        std::move(seventh), std::move(exact)
    };
}

std::unordered_set<std::uint64_t> enumerate_s_b_fourth(std::uint32_t h_b_mask) {
    const std::uint32_t s_axes = FULL ^ h_b_mask;
    std::vector<int> real;
    int imaginary_position = -1;
    for (int j = 0; j < N; ++j) {
        if (bit(s_axes, j)) imaginary_position = j;
        else real.push_back(j);
    }
    assert(real.size() == 20 && imaginary_position >= 0);

    // Case 3 target is 4-i.  The unique imaginary entry is -i and exactly
    // eight of the twenty real entries are negative.
    std::unordered_set<std::uint64_t> fourth;
    std::uint32_t choose = (std::uint32_t{1} << 8) - 1;
    const std::uint32_t limit = std::uint32_t{1} << 20;
    std::uint64_t assignments = 0;
    while (choose < limit) {
        std::array<Gaussian, N> word{};
        word[imaginary_position] = unit(1, 1);
        for (int k = 0; k < 20; ++k) word[real[k]] = unit(0, bit(choose, k));
        fourth.insert(fingerprint(paf(word), 4));
        ++assignments;

        const std::uint32_t low = choose & -choose;
        const std::uint32_t next = choose + low;
        choose = (((next ^ choose) >> 2) / low) | next;
    }
    assert(assignments == 125970);
    std::cout << "s_b_exact_sum_assignments=" << assignments << '\n';
    std::cout << "s_b_fourth_fingerprints=" << fourth.size() << '\n';
    return fourth;
}

}  // namespace

int main() {
    const std::uint32_t b_mask = FULL ^ 1U;
    const unsigned signature = autocorrelation_signature(b_mask);
    const auto b_records = enumerate_b(b_mask);
    const auto s_b4 = enumerate_s_b_fourth(b_mask);
    std::uint64_t a_assignments = 0;
    int fourth_axes = 0;
    int fifth_axes = 0;
    int fourth_assignments = 0;
    int fifth_assignments = 0;
    int sixth_assignments = 0;
    int seventh_assignments = 0;
    int exact_h_assignments = 0;
    int exact_h_axes = 0;
    int sixth_axes = 0;
    int seventh_axes = 0;
    int all_sums_fourth_axes = 0;
    int all_sums_fifth_h_axes = 0;

    for (unsigned a_half = 0; a_half < (1U << 10); ++a_half) {
        const std::uint32_t axes = reflected_axes(a_half);
        const unsigned theta = theta_h(a_half, signature);
        bool survives4 = false;
        bool survives5 = false;
        bool survives6 = false;
        bool survives7 = false;
        bool survives_exact_h = false;
        for (unsigned pair_signs = 0; pair_signs < (1U << 10); ++pair_signs) {
            std::array<Gaussian, N> word{};
            Gaussian sum{0, 0};
            for (int shift = 1; shift <= 10; ++shift) {
                const int axis = bit(axes, shift);
                const int left_sign = bit(pair_signs, shift - 1);
                const int right_sign = left_sign ^ bit(theta, shift - 1);
                word[shift] = unit(axis, left_sign);
                word[N - shift] = unit(axis, right_sign);
                sum = sum + word[shift] + word[N - shift];
            }
            if (sum.r != 0 || sum.i != 0) continue;
            ++a_assignments;
            const auto values = paf(word);
            const bool ok4 = b_records.fourth.contains(required_b_fingerprint(values, 4));
            const bool ok5 = b_records.fifth.contains(required_b_fingerprint(values, 5));
            const bool ok6 = b_records.sixth.contains(required_b_fingerprint(values, 6));
            const bool ok7 = std::binary_search(
                b_records.seventh.begin(), b_records.seventh.end(),
                required_b_residue_record(values, 7)
            );
            const bool ok_exact = std::binary_search(
                b_records.exact.begin(), b_records.exact.end(), required_exact_b_record(values)
            );
            assert(!ok_exact || ok5);
            assert(!ok_exact || ok6);
            assert(!ok_exact || ok7);
            assert(!ok7 || ok6);
            assert(!ok6 || ok5);
            assert(!ok5 || ok4);
            fourth_assignments += int(ok4);
            fifth_assignments += int(ok5);
            sixth_assignments += int(ok6);
            seventh_assignments += int(ok7);
            exact_h_assignments += int(ok_exact);
            survives4 = survives4 || ok4;
            survives5 = survives5 || ok5;
            survives6 = survives6 || ok6;
            survives7 = survives7 || ok7;
            survives_exact_h = survives_exact_h || ok_exact;
        }
        fourth_axes += int(survives4);
        fifth_axes += int(survives5);
        sixth_axes += int(survives6);
        seventh_axes += int(survives7);
        if (survives6) std::cout << "sixth_order_a_axis=" << a_half << '\n';
        exact_h_axes += int(survives_exact_h);

        bool survives_s4 = false;
        const std::uint32_t s_axes = (FULL ^ 1U) ^ axes;
        const unsigned s_theta = theta_s(a_half, signature);
        constexpr std::array<Gaussian, 4> centers{{{1, 1}, {-1, 1}, {-1, -1}, {1, -1}}};
        for (Gaussian center : centers) {
            for (unsigned pair_signs = 0; pair_signs < (1U << 10); ++pair_signs) {
                std::array<Gaussian, N> word{};
                word[0] = center;
                Gaussian sum = center;
                for (int shift = 1; shift <= 10; ++shift) {
                    const int axis = bit(s_axes, shift);
                    const int left_sign = bit(pair_signs, shift - 1);
                    const int right_sign = left_sign ^ bit(s_theta, shift - 1);
                    word[shift] = unit(axis, left_sign);
                    word[N - shift] = unit(axis, right_sign);
                    sum = sum + word[shift] + word[N - shift];
                }
                if (sum.r != 5 || sum.i != -1) continue;
                if (s_b4.contains(required_s_b_fingerprint(paf(word), 4))) {
                    survives_s4 = true;
                    break;
                }
            }
            if (survives_s4) break;
        }
        all_sums_fourth_axes += int(survives4 && survives_s4);
        all_sums_fifth_h_axes += int(survives5 && survives_s4);
        if (survives_exact_h && survives_s4) {
            std::cerr << "unexpected_all_sums_exact_h_survivor=" << a_half << '\n';
        }
    }

    std::cout << "b_axis_weight=20\n";
    std::cout << "b_rotation_orbits=1\n";
    std::cout << "a_exact_sum_assignments=" << a_assignments << '\n';
    std::cout << "fourth_order_h_compatible_assignments=" << fourth_assignments << '\n';
    std::cout << "fifth_order_h_compatible_assignments=" << fifth_assignments << '\n';
    std::cout << "sixth_order_h_compatible_assignments=" << sixth_assignments << '\n';
    std::cout << "seventh_order_h_compatible_assignments=" << seventh_assignments << '\n';
    std::cout << "exact_h_compatible_assignments=" << exact_h_assignments << '\n';
    std::cout << "fourth_order_h_surviving_a_axes=" << fourth_axes << '\n';
    std::cout << "fifth_order_h_surviving_a_axes=" << fifth_axes << '\n';
    std::cout << "sixth_order_h_surviving_a_axes=" << sixth_axes << '\n';
    std::cout << "seventh_order_h_surviving_a_axes=" << seventh_axes << '\n';
    std::cout << "exact_h_surviving_a_axes=" << exact_h_axes << '\n';
    std::cout << "case_3_all_sums_fourth_order_a_axes=" << all_sums_fourth_axes << '\n';
    std::cout << "case_3_all_sums_plus_fifth_h_a_axes=" << all_sums_fifth_h_axes << '\n';
    assert(all_sums_fourth_axes == 388);
}
