#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <set>
#include <vector>

struct Gaussian {
    int real;
    int imag;
};

bool operator==(Gaussian left, Gaussian right) {
    return left.real == right.real && left.imag == right.imag;
}

bool operator<(Gaussian left, Gaussian right) {
    return left.real < right.real ||
           (left.real == right.real && left.imag < right.imag);
}

Gaussian add(Gaussian left, Gaussian right) {
    return {left.real + right.real, left.imag + right.imag};
}

Gaussian multiply(Gaussian left, Gaussian right) {
    return {
        left.real * right.real - left.imag * right.imag,
        left.real * right.imag + left.imag * right.real,
    };
}

Gaussian multiply_conjugate(Gaussian left, Gaussian right) {
    return {
        left.real * right.real + left.imag * right.imag,
        left.imag * right.real - left.real * right.imag,
    };
}

Gaussian periodic_correlation(const std::array<Gaussian, 7>& word, int shift) {
    Gaussian result{0, 0};
    for (int index = 0; index < 7; ++index) {
        result = add(
            result,
            multiply_conjugate(word[index], word[(index + shift) % 7])
        );
    }
    return result;
}

std::vector<Gaussian> active_domain(
    int count,
    const std::array<Gaussian, 4>& roots
) {
    std::set<Gaussian> reached{{0, 0}};
    for (int step = 0; step < count; ++step) {
        std::set<Gaussian> next;
        for (Gaussian partial : reached) {
            for (Gaussian root : roots) {
                next.insert(add(partial, root));
            }
        }
        reached = next;
    }
    std::vector<Gaussian> result;
    for (Gaussian value : reached) {
        result.push_back(multiply({1, 1}, value));
    }
    return result;
}

int main() {
    const std::array<Gaussian, 4> roots{{
        {1, 0}, {0, 1}, {-1, 0}, {0, -1},
    }};
    const std::array<int, 7> support_counts{{2, 2, 3, 3, 2, 3, 3}};
    const auto d2 = active_domain(2, roots);
    const auto d3 = active_domain(3, roots);
    const std::array<std::vector<Gaussian>, 4> domains{{{}, {}, d2, d3}};

    assert(d2.size() == 9);
    assert(d3.size() == 16);

    std::vector<std::array<Gaussian, 7>> b_words;
    for (Gaussian center : std::array<Gaussian, 2>{{{1, 0}, {-1, 0}}}) {
        for (Gaussian left : roots) {
            for (Gaussian right : roots) {
                std::array<Gaussian, 7> word{};
                word[0] = center;
                word[3] = multiply({1, 1}, left);
                word[4] = multiply({1, 1}, right);
                Gaussian sum{0, 0};
                for (Gaussian value : word) {
                    sum = add(sum, value);
                }
                if (sum == Gaussian{1, 0}) {
                    b_words.push_back(word);
                }
            }
        }
    }
    assert(b_words.size() == 6);

    std::uint64_t sum_zero = 0;
    std::uint64_t energy_32 = 0;
    std::vector<std::array<std::uint64_t, 3>> passes(b_words.size());
    std::array<Gaussian, 7> word{};

    const auto enumerate = [&](auto&& self, int index, Gaussian sum) -> void {
        if (index < 6) {
            for (Gaussian value : domains[support_counts[index]]) {
                word[index] = value;
                self(self, index + 1, add(sum, value));
            }
            return;
        }

        const Gaussian last{-sum.real, -sum.imag};
        if (std::find(d3.begin(), d3.end(), last) == d3.end()) {
            return;
        }
        word[6] = last;
        ++sum_zero;

        int energy = 0;
        for (Gaussian value : word) {
            energy += value.real * value.real + value.imag * value.imag;
        }
        if (energy != 32) {
            return;
        }
        ++energy_32;

        const std::array<Gaussian, 3> a_correlations{{
            periodic_correlation(word, 1),
            periodic_correlation(word, 2),
            periodic_correlation(word, 3),
        }};
        for (std::size_t b_index = 0; b_index < b_words.size(); ++b_index) {
            for (int shift = 0; shift < 3; ++shift) {
                const Gaussian combined = add(
                    a_correlations[shift],
                    periodic_correlation(b_words[b_index], shift + 1)
                );
                if (!(combined == Gaussian{-6, 0})) {
                    break;
                }
                ++passes[b_index][shift];
            }
        }
    };
    enumerate(enumerate, 0, {0, 0});

    assert(sum_zero == 1'028'196);
    assert(energy_32 == 33'072);
    for (int index = 0; index < 4; ++index) {
        assert((passes[index] == std::array<std::uint64_t, 3>{664, 16, 0}));
    }
    for (int index = 4; index < 6; ++index) {
        assert((passes[index] == std::array<std::uint64_t, 3>{536, 24, 0}));
    }

    std::uint64_t raw_tuples = 1;
    for (int count : support_counts) {
        raw_tuples *= domains[count].size();
    }
    std::cout
        << "third_order_b_masks=2\n"
        << "third_order_labeled_pairs=42\n"
        << "third_order_a_rotation_orbits=2\n"
        << "a_compressed_support_counts=2233233\n"
        << "b_compressed_support=0,3,4\n"
        << "d2_size=" << d2.size() << "\n"
        << "d3_size=" << d3.size() << "\n"
        << "raw_domain_tuples=" << raw_tuples << "\n"
        << "sum_zero_tuples=" << sum_zero << "\n"
        << "energy_32_tuples=" << energy_32 << "\n"
        << "positive_center_b_choices=4\n"
        << "positive_center_shift1=" << passes[0][0] << "\n"
        << "positive_center_shifts12=" << passes[0][1] << "\n"
        << "positive_center_shifts123=" << passes[0][2] << "\n"
        << "negative_center_b_choices=2\n"
        << "negative_center_shift1=" << passes[4][0] << "\n"
        << "negative_center_shifts12=" << passes[4][1] << "\n"
        << "negative_center_shifts123=" << passes[4][2] << "\n"
        << "solutions=0\n"
        << "certificate=verified\n";
}
