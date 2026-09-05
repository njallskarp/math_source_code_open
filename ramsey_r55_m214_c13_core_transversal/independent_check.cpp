#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {
constexpr int n = 13;
constexpr std::uint16_t full = (1U << n) - 1U;
constexpr std::array<int, 4> differences{1, 5, 8, 12};
constexpr std::array<int, 4> multipliers{1, 5, 8, 12};
constexpr auto model_graph6 = R"G6(jSyIic|JekmixW~?IxLkbGjwfp_NjVcJZXHaVKVuCmZCqztIR~MZQYARD[_nGeLBQ][bNCUyb_E{Jj}sO@pyRIXtZFIldAXrHUFEd\?}wXcTjSJTGycm]HtGqX{nV@grUwQThDZDVVGq\IVUWpwcfdv_)G6";
constexpr std::array<int, 13> model_core_labels{1, 3, 5, 15, 16, 17, 18, 19, 20, 24, 25, 26, 28};
constexpr std::array<int, 13> model_core_images{0, 4, 2, 3, 6, 10, 7, 5, 12, 11, 1, 9, 8};

bool edge(int a, int b) {
    if (a == b) return false;
    int d = (a - b + n) % n;
    return std::find(differences.begin(), differences.end(), d) != differences.end();
}

bool is_independent(std::uint16_t vertices) {
    for (int i = 0; i < n; ++i) {
        if (!(vertices & (1U << i))) continue;
        for (int j = i + 1; j < n; ++j) {
            if ((vertices & (1U << j)) && edge(i, j)) return false;
        }
    }
    return true;
}

std::uint16_t make_mask(std::initializer_list<int> xs) {
    std::uint16_t result = 0;
    for (int x : xs) result |= static_cast<std::uint16_t>(1U << x);
    return result;
}

std::set<std::uint16_t> orbit(std::uint16_t seed) {
    std::set<std::uint16_t> result;
    for (int m : multipliers) {
        for (int b = 0; b < n; ++b) {
            std::uint16_t image = 0;
            for (int x = 0; x < n; ++x) {
                if (seed & (1U << x)) image |= static_cast<std::uint16_t>(1U << ((m * x + b) % n));
            }
            result.insert(image);
        }
    }
    return result;
}
}  // namespace

int main() {
    int edges = 0;
    for (int i = 0; i < n; ++i) {
        int degree = 0;
        for (int j = 0; j < n; ++j) degree += edge(i, j);
        if (degree != 4) throw std::runtime_error("core degree mismatch");
        for (int j = i + 1; j < n; ++j) edges += edge(i, j);
    }
    if (edges != 26) throw std::runtime_error("core edge mismatch");

    // A subset-DP marks every mask containing an independent four-set.  Thus a
    // red footprint S is legal precisely when complement(S) remains unmarked.
    std::array<unsigned char, 1U << n> contains_independent_four{};
    std::vector<std::uint16_t> independent_four_masks;
    int independent_fours = 0;
    for (std::uint16_t bits = 0; bits <= full; ++bits) {
        if (std::popcount(bits) == 4 && is_independent(bits)) {
            contains_independent_four[bits] = 1;
            independent_four_masks.push_back(bits);
            ++independent_fours;
        }
    }
    for (int bit = 0; bit < n; ++bit) {
        for (std::uint16_t bits = 0; bits <= full; ++bits) {
            if (bits & (1U << bit)) {
                contains_independent_four[bits] = static_cast<unsigned char>(
                    contains_independent_four[bits] || contains_independent_four[bits ^ (1U << bit)]
                );
            }
        }
    }
    if (independent_fours != 39) throw std::runtime_error("independent-four mismatch");

    std::array<int, n + 1> histogram{};
    std::array<int, n + 1> minimal_histogram{};
    std::set<std::uint16_t> minimal;
    for (std::uint16_t footprint = 0; footprint <= full; ++footprint) {
        if (contains_independent_four[full ^ footprint]) continue;
        ++histogram[std::popcount(footprint)];
        bool is_minimal = true;
        for (int bit = 0; bit < n; ++bit) {
            if ((footprint & (1U << bit)) &&
                !contains_independent_four[full ^ (footprint ^ (1U << bit))]) {
                is_minimal = false;
            }
        }
        if (is_minimal) {
            minimal.insert(footprint);
            ++minimal_histogram[std::popcount(footprint)];
        }
    }
    constexpr std::array<int, n + 1> expected_histogram{
        0, 0, 0, 0, 0, 65, 416, 910, 1014, 676, 286, 78, 13, 1
    };
    if (histogram != expected_histogram || minimal_histogram[5] != 65 ||
        minimal_histogram[6] != 52 || minimal.size() != 117) {
        throw std::runtime_error("transversal census mismatch");
    }

    const auto first = orbit(make_mask({0, 1, 2, 5, 6}));
    const auto second = orbit(make_mask({0, 1, 2, 6, 9}));
    const auto third = orbit(make_mask({0, 1, 2, 3, 5, 8}));
    if (first.size() != 52 || second.size() != 13 || third.size() != 52) {
        throw std::runtime_error("orbit-size mismatch");
    }
    std::set<std::uint16_t> union_orbits = first;
    union_orbits.insert(second.begin(), second.end());
    union_orbits.insert(third.begin(), third.end());
    if (union_orbits != minimal) throw std::runtime_error("orbit cover mismatch");

    int third_anchor_types = 0;
    for (int alpha = 0; alpha <= 7; ++alpha) {
        for (int beta = 0; beta <= 7; ++beta) {
            if (alpha + beta == 0) continue;
            const std::array<int, 8> cells{
                4, 8, alpha, beta, 7 - alpha, 7 - beta,
                15 - alpha - beta, alpha + beta - 1
            };
            if (*std::min_element(cells.begin(), cells.end()) < 0) {
                throw std::runtime_error("negative third-anchor cell");
            }
            int cell_sum = 0;
            for (int value : cells) cell_sum += value;
            if (cell_sum != 40) throw std::runtime_error("third-anchor cells do not sum to 40");
            ++third_anchor_types;
        }
    }
    if (third_anchor_types != 63) throw std::runtime_error("third-anchor type count mismatch");

    // Independently decode the compact height-2807 model and apply the core
    // interface in the supplied explicit isomorphism.
    constexpr int model_n = 43;
    std::array<std::array<bool, model_n>, model_n> red{};
    const std::string record(model_graph6);
    if (record.empty() || record.front() - 63 != model_n) {
        throw std::runtime_error("model graph6 order mismatch");
    }
    std::vector<int> graph_bits;
    for (std::size_t position = 1; position < record.size(); ++position) {
        int value = static_cast<unsigned char>(record[position]) - 63;
        if (value < 0 || value >= 64) throw std::runtime_error("invalid graph6 byte");
        for (int shift = 5; shift >= 0; --shift) graph_bits.push_back((value >> shift) & 1);
    }
    int index = 0;
    int model_edges = 0;
    for (int j = 1; j < model_n; ++j) {
        for (int i = 0; i < j; ++i) {
            red[i][j] = red[j][i] = graph_bits.at(index++) != 0;
            model_edges += red[i][j];
        }
    }
    if (model_edges != 445) throw std::runtime_error("model edge-count mismatch");
    std::vector<int> derived_core;
    for (int x = 0; x < model_n; ++x) {
        if (x != 13 && x != 14 && red[13][x] && red[14][x]) derived_core.push_back(x);
    }
    if (!std::equal(derived_core.begin(), derived_core.end(), model_core_labels.begin(), model_core_labels.end())) {
        throw std::runtime_error("model common core mismatch");
    }
    std::array<int, model_n> image{};
    image.fill(-1);
    for (std::size_t i = 0; i < model_core_labels.size(); ++i) image[model_core_labels[i]] = model_core_images[i];
    for (int i : model_core_labels) {
        for (int j : model_core_labels) {
            if (i < j && red[i][j] != edge(image[i], image[j])) {
                throw std::runtime_error("model core isomorphism mismatch");
            }
        }
    }
    int passing_vertices = 0;
    int failing_vertices = 0;
    int uncovered_fours = 0;
    for (int z = 0; z < model_n; ++z) {
        if (z == 13 || z == 14 || image[z] >= 0) continue;
        std::uint16_t footprint = 0;
        for (int x : model_core_labels) {
            if (red[z][x]) footprint |= static_cast<std::uint16_t>(1U << image[x]);
        }
        int misses = 0;
        for (std::uint16_t four : independent_four_masks) misses += !(footprint & four);
        if (misses == 0) {
            ++passing_vertices;
        } else {
            ++failing_vertices;
            uncovered_fours += misses;
        }
    }
    constexpr std::array<int, 5> first_blue_five{8, 15, 19, 20, 25};
    for (std::size_t i = 0; i < first_blue_five.size(); ++i) {
        for (std::size_t j = i + 1; j < first_blue_five.size(); ++j) {
            if (red[first_blue_five[i]][first_blue_five[j]]) {
                throw std::runtime_error("first obstruction is not blue");
            }
        }
    }
    if (passing_vertices != 18 || failing_vertices != 10 || uncovered_fours != 35) {
        throw std::runtime_error("model interface census mismatch");
    }

    std::cout << "PASS independent_subset_dp core_edges=26 independent4=39\n";
    std::cout << "transversals=3459 minimum=5 minimal=117 minimal_sizes=5:65,6:52\n";
    std::cout << "affine_orbits=52,13,52 exact_minimal_cover=yes\n";
    std::cout << "third_anchor_types=63 cell_order=111,110,101,011,100,010,001,000\n";
    std::cout << "height2807_interface=pass:18,fail:10,uncovered4:35 first_blueK5=8,15,19,20,25\n";
}
