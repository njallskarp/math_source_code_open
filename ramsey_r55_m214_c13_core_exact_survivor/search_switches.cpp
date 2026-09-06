#include <algorithm>
#include <array>
#include <bitset>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {

constexpr int n = 28;
constexpr int h_order = 13;
constexpr int pair_count = 378;
constexpr std::array<unsigned, n> footprints = {
    0x1c48U, 0x1630U, 0x1391U, 0x02eeU, 0x11a9U, 0x04deU, 0x1fffU,
    0x0067U, 0x19c5U, 0x091cU, 0x0e2cU, 0x18f3U, 0x0f12U, 0x19f7U,
    0x0703U, 0x1033U, 0x078cU, 0x1eb4U, 0x1f42U, 0x0b4bU, 0x04beU,
    0x189bU, 0x1f6dU, 0x07fcU, 0x19c0U, 0x0979U, 0x069fU, 0x1667U,
};
constexpr std::array<int, 13> marked_vertices = {0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14};
constexpr char initial_hex[] =
    "000119f7ebfdfc7f4ff991df80381ce3805155a42f748d0b8fad71005f22d1506d3827e04225e8714ad4de071f2071f";

int pair_rank(int left, int right) {
    if (left > right) std::swap(left, right);
    if (left < 0 || right >= n || left == right) throw std::runtime_error("pair");
    return left * (2 * n - left - 1) / 2 + (right - left - 1);
}

bool core_edge(int left, int right) {
    int difference = (left - right) % h_order;
    if (difference < 0) difference += h_order;
    return difference == 1 || difference == 5 || difference == 8 || difference == 12;
}

int hex_digit(char value) {
    if (value >= '0' && value <= '9') return value - '0';
    if (value >= 'a' && value <= 'f') return value - 'a' + 10;
    throw std::runtime_error("hex");
}

std::bitset<pair_count> decode() {
    const std::string text(initial_hex);
    if (text.size() != 95U) throw std::runtime_error("hex length");
    std::bitset<pair_count> result;
    int rank = 0;
    for (auto position = text.rbegin(); position != text.rend(); ++position) {
        const int digit = hex_digit(*position);
        for (int bit = 0; bit < 4 && rank < pair_count; ++bit, ++rank) {
            if (((digit >> bit) & 1) != 0) result.set(static_cast<std::size_t>(rank));
        }
    }
    return result;
}

std::string encode(const std::bitset<pair_count>& bits) {
    std::string result(95U, '0');
    constexpr char digits[] = "0123456789abcdef";
    for (int nibble = 0; nibble < 95; ++nibble) {
        int value = 0;
        for (int bit = 0; bit < 4; ++bit) {
            const int rank = 4 * nibble + bit;
            if (rank < pair_count && bits.test(static_cast<std::size_t>(rank))) value |= 1 << bit;
        }
        result.at(static_cast<std::size_t>(94 - nibble)) = digits[value];
    }
    return result;
}

int cell(int vertex) {
    return vertex < 7 ? 0 : vertex < 14 ? 1 : 2;
}

struct Move {
    std::array<int, 2> first{};
    std::array<int, 2> second{};
    std::array<int, 4> toggled{};
    std::vector<std::array<int, 3>> affected;
    std::array<int, h_order> core_delta{};
};

std::array<int, 2> matching(int a, int b, int c, int d) {
    return {pair_rank(a, b), pair_rank(c, d)};
}

Move make_move(std::array<int, 2> first, std::array<int, 2> second) {
    Move move;
    move.first = first;
    move.second = second;
    move.toggled = {first[0], first[1], second[0], second[1]};
    std::sort(move.toggled.begin(), move.toggled.end());
    if (std::adjacent_find(move.toggled.begin(), move.toggled.end()) != move.toggled.end()) {
        throw std::runtime_error("duplicate edge");
    }
    std::array<bool, 3276> seen{};
    auto triple_rank = [](int a, int b, int c) {
        int rank = 0;
        for (int i = 0; i < a; ++i) rank += (n - i - 1) * (n - i - 2) / 2;
        for (int j = a + 1; j < b; ++j) rank += n - j - 1;
        return rank + c - b - 1;
    };
    for (const int edge_rank : move.toggled) {
        int x = -1;
        int y = -1;
        for (int i = 0; i < n && x < 0; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (pair_rank(i, j) == edge_rank) {
                    x = i;
                    y = j;
                    break;
                }
            }
        }
        for (int z = 0; z < n; ++z) {
            if (z == x || z == y) continue;
            std::array<int, 3> triple = {x, y, z};
            std::sort(triple.begin(), triple.end());
            const int rank = triple_rank(triple[0], triple[1], triple[2]);
            if (!seen.at(static_cast<std::size_t>(rank))) {
                seen.at(static_cast<std::size_t>(rank)) = true;
                move.affected.push_back(triple);
            }
        }
    }
    auto mask_intersection = [](int rank, int h) {
        int x = -1;
        int y = -1;
        for (int i = 0; i < n && x < 0; ++i) for (int j = i + 1; j < n; ++j) {
            if (pair_rank(i, j) == rank) {
                x = i;
                y = j;
                break;
            }
        }
        return ((footprints.at(static_cast<std::size_t>(x)) >> h) & 1U) != 0U &&
               ((footprints.at(static_cast<std::size_t>(y)) >> h) & 1U) != 0U;
    };
    for (int h = 0; h < h_order; ++h) {
        move.core_delta.at(static_cast<std::size_t>(h)) =
            static_cast<int>(mask_intersection(second[0], h)) +
            static_cast<int>(mask_intersection(second[1], h)) -
            static_cast<int>(mask_intersection(first[0], h)) -
            static_cast<int>(mask_intersection(first[1], h));
    }
    return move;
}

bool triangle(const std::bitset<pair_count>& bits, const std::array<int, 3>& triple) {
    return bits.test(static_cast<std::size_t>(pair_rank(triple[0], triple[1]))) &&
           bits.test(static_cast<std::size_t>(pair_rank(triple[0], triple[2]))) &&
           bits.test(static_cast<std::size_t>(pair_rank(triple[1], triple[2])));
}

int triangle_count(const std::bitset<pair_count>& bits) {
    int result = 0;
    for (int a = 0; a < n; ++a) for (int b = a + 1; b < n; ++b)
    for (int c = b + 1; c < n; ++c) result += triangle(bits, {a, b, c});
    return result;
}

std::array<int, h_order> core_vector(const std::bitset<pair_count>& bits) {
    std::array<int, h_order> result{};
    for (int x = 0; x < n; ++x) for (int y = x + 1; y < n; ++y) {
        if (!bits.test(static_cast<std::size_t>(pair_rank(x, y)))) continue;
        for (int h = 0; h < h_order; ++h) {
            result.at(static_cast<std::size_t>(h)) +=
                ((footprints.at(static_cast<std::size_t>(x)) >> h) & 1U) != 0U &&
                ((footprints.at(static_cast<std::size_t>(y)) >> h) & 1U) != 0U;
        }
    }
    return result;
}

int score(int triangles, const std::array<int, h_order>& core,
          const std::array<int, h_order>& target) {
    int result = 2 * std::abs(triangles - 360);
    for (int h = 0; h < h_order; ++h) {
        result += std::abs(core.at(static_cast<std::size_t>(h)) -
                           target.at(static_cast<std::size_t>(h)));
    }
    return result;
}

}  // namespace

int main() {
    std::array<bool, n> marked{};
    for (const int vertex : marked_vertices) marked.at(static_cast<std::size_t>(vertex)) = true;
    std::vector<std::vector<int>> groups(6);
    for (int vertex = 0; vertex < n; ++vertex) {
        groups.at(static_cast<std::size_t>(2 * cell(vertex) + static_cast<int>(marked.at(static_cast<std::size_t>(vertex)))))
            .push_back(vertex);
    }

    std::vector<std::array<int, 3>> independent_triples;
    for (int a = 0; a < h_order; ++a) for (int b = a + 1; b < h_order; ++b)
    for (int c = b + 1; c < h_order; ++c) {
        if (!core_edge(a, b) && !core_edge(a, c) && !core_edge(b, c)) {
            independent_triples.push_back({a, b, c});
        }
    }
    std::bitset<pair_count> forced_red;
    std::bitset<pair_count> forced_blue;
    for (int x = 0; x < n; ++x) for (int y = x + 1; y < n; ++y) {
        const unsigned union_mask = footprints.at(static_cast<std::size_t>(x)) |
                                    footprints.at(static_cast<std::size_t>(y));
        for (const auto triple : independent_triples) {
            if (std::all_of(triple.begin(), triple.end(), [&](int h) {
                    return ((union_mask >> h) & 1U) == 0U;
                })) {
                forced_red.set(static_cast<std::size_t>(pair_rank(x, y)));
                break;
            }
        }
        if (cell(x) == cell(y) && cell(x) < 2) {
            const unsigned intersection = footprints.at(static_cast<std::size_t>(x)) &
                                          footprints.at(static_cast<std::size_t>(y));
            for (int a = 0; a < h_order; ++a) for (int b = a + 1; b < h_order; ++b) {
                if (core_edge(a, b) && ((intersection >> a) & 1U) != 0U &&
                    ((intersection >> b) & 1U) != 0U) {
                    forced_blue.set(static_cast<std::size_t>(pair_rank(x, y)));
                }
            }
        }
    }
    if ((forced_red & forced_blue).any()) throw std::runtime_error("forced conflict");

    std::vector<Move> moves;
    for (std::size_t gi = 0; gi < groups.size(); ++gi) {
        for (std::size_t gj = gi; gj < groups.size(); ++gj) {
            const auto& left = groups[gi];
            const auto& right = groups[gj];
            if (gi != gj) {
                for (std::size_t ai = 0; ai < left.size(); ++ai)
                for (std::size_t ci = ai + 1; ci < left.size(); ++ci)
                for (std::size_t bi = 0; bi < right.size(); ++bi)
                for (std::size_t di = bi + 1; di < right.size(); ++di) {
                    moves.push_back(make_move(
                        matching(left[ai], right[bi], left[ci], right[di]),
                        matching(left[ai], right[di], left[ci], right[bi])));
                }
            } else {
                for (std::size_t ai = 0; ai < left.size(); ++ai)
                for (std::size_t bi = ai + 1; bi < left.size(); ++bi)
                for (std::size_t ci = bi + 1; ci < left.size(); ++ci)
                for (std::size_t di = ci + 1; di < left.size(); ++di) {
                    const int a = left[ai], b = left[bi], c = left[ci], d = left[di];
                    const std::array<std::array<int, 2>, 3> matchings = {
                        matching(a, b, c, d), matching(a, c, b, d), matching(a, d, b, c)};
                    for (int p = 0; p < 3; ++p) for (int q = p + 1; q < 3; ++q) {
                        moves.push_back(make_move(matchings.at(static_cast<std::size_t>(p)),
                                                  matchings.at(static_cast<std::size_t>(q))));
                    }
                }
            }
        }
    }

    std::array<int, h_order> target{};
    for (int h = 0; h < h_order; ++h) {
        int cell_incidence = 0;
        int core_lift = 0;
        for (int x = 0; x < n; ++x) {
            const unsigned mask = footprints.at(static_cast<std::size_t>(x));
            if (x < 14 && ((mask >> h) & 1U) != 0U) ++cell_incidence;
            if (((mask >> h) & 1U) == 0U) continue;
            for (int other = 0; other < h_order; ++other) {
                if (other != h && core_edge(h, other) && ((mask >> other) & 1U) != 0U) ++core_lift;
            }
        }
        target.at(static_cast<std::size_t>(h)) = 91 - cell_incidence - core_lift;
    }
    std::cout << "moves=" << moves.size() << " target_sum="
              << std::accumulate(target.begin(), target.end(), 0) << '\n';

    const auto initial = decode();
    for (std::uint64_t restart = 0; restart < 40U; ++restart) {
        auto bits = initial;
        int triangles = triangle_count(bits);
        auto core = core_vector(bits);
        int best = score(triangles, core, target);
        std::mt19937_64 generator(53001U + 104729U * restart);
        std::uniform_int_distribution<std::size_t> choose_move(0U, moves.size() - 1U);
        std::uniform_real_distribution<double> unit(0.0, 1.0);
        constexpr std::uint64_t steps = 2'000'000U;
        for (std::uint64_t step = 0; step < steps; ++step) {
            const Move& move = moves.at(choose_move(generator));
            const bool first_red = bits.test(static_cast<std::size_t>(move.first[0])) &&
                                   bits.test(static_cast<std::size_t>(move.first[1]));
            const bool second_red = bits.test(static_cast<std::size_t>(move.second[0])) &&
                                    bits.test(static_cast<std::size_t>(move.second[1]));
            const bool first_blue = !bits.test(static_cast<std::size_t>(move.first[0])) &&
                                    !bits.test(static_cast<std::size_t>(move.first[1]));
            const bool second_blue = !bits.test(static_cast<std::size_t>(move.second[0])) &&
                                     !bits.test(static_cast<std::size_t>(move.second[1]));
            int direction = 0;
            if (first_red && second_blue) direction = 1;
            if (second_red && first_blue) direction = -1;
            if (direction == 0) continue;
            const auto& removed = direction == 1 ? move.first : move.second;
            const auto& added = direction == 1 ? move.second : move.first;
            if (forced_red.test(static_cast<std::size_t>(removed[0])) ||
                forced_red.test(static_cast<std::size_t>(removed[1])) ||
                forced_blue.test(static_cast<std::size_t>(added[0])) ||
                forced_blue.test(static_cast<std::size_t>(added[1]))) continue;

            int triangle_delta = 0;
            for (const auto triple : move.affected) {
                const bool before = triangle(bits, triple);
                bool after = true;
                for (int i = 0; i < 3; ++i) for (int j = i + 1; j < 3; ++j) {
                    const int rank = pair_rank(triple[static_cast<std::size_t>(i)],
                                               triple[static_cast<std::size_t>(j)]);
                    const bool toggled = std::find(move.toggled.begin(), move.toggled.end(), rank) !=
                                         move.toggled.end();
                    after = after && (bits.test(static_cast<std::size_t>(rank)) != toggled);
                }
                triangle_delta += static_cast<int>(after) - static_cast<int>(before);
            }
            auto candidate_core = core;
            for (int h = 0; h < h_order; ++h) {
                candidate_core.at(static_cast<std::size_t>(h)) +=
                    direction * move.core_delta.at(static_cast<std::size_t>(h));
            }
            const int candidate_triangles = triangles + triangle_delta;
            const int old_score = score(triangles, core, target);
            const int new_score = score(candidate_triangles, candidate_core, target);
            const double fraction = static_cast<double>(step) / static_cast<double>(steps);
            const double temperature = std::max(0.05, 7.0 * (1.0 - fraction));
            if (new_score <= old_score ||
                unit(generator) < std::exp(static_cast<double>(old_score - new_score) / temperature)) {
                for (const int rank : move.toggled) bits.flip(static_cast<std::size_t>(rank));
                triangles = candidate_triangles;
                core = candidate_core;
                best = std::min(best, new_score);
                if (new_score == 0) {
                    if (triangle_count(bits) != 360 || core_vector(bits) != target) {
                        throw std::runtime_error("incremental mismatch");
                    }
                    std::cout << "FOUND restart=" << restart << " step=" << step
                              << " bits=" << encode(bits) << '\n';
                    return 0;
                }
            }
        }
        std::cout << "restart=" << restart << " best=" << best << '\n';
    }
    std::cout << "NOT_FOUND\n";
    return 1;
}
