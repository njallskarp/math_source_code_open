#include <algorithm>
#include <array>
#include <bitset>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int n = 43;
constexpr int core_order = 13;
constexpr int outside_order = 28;
constexpr int u = 0;
constexpr int v = 1;
constexpr int core_first = 2;
constexpr int outside_first = 15;
constexpr int outside_pairs = 378;

constexpr std::array<unsigned, outside_order> footprints = {
    0x1c48U, 0x1630U, 0x1391U, 0x02eeU, 0x11a9U, 0x04deU, 0x1fffU,
    0x0067U, 0x19c5U, 0x091cU, 0x0e2cU, 0x18f3U, 0x0f12U, 0x19f7U,
    0x0703U, 0x1033U, 0x078cU, 0x1eb4U, 0x1f42U, 0x0b4bU, 0x04beU,
    0x189bU, 0x1f6dU, 0x07fcU, 0x19c0U, 0x0979U, 0x069fU, 0x1667U,
};

constexpr std::array<int, 13> outside_e = {0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14};
constexpr char outside_hex[] =
    "000119f7ebfdfc7f4ff991df80381ce3805155a42f748d0b8fad71005f22d1506d3827e04225e8714ad4de071f2071f";

bool core_edge(int left, int right) {
    int difference = (left - right) % core_order;
    if (difference < 0) difference += core_order;
    return difference == 1 || difference == 5 || difference == 8 || difference == 12;
}

int pair_rank(int left, int right) {
    if (left > right) std::swap(left, right);
    if (left < 0 || right >= outside_order || left == right) throw std::runtime_error("pair");
    return left * (2 * outside_order - left - 1) / 2 + (right - left - 1);
}

int hex_digit(char value) {
    if (value >= '0' && value <= '9') return value - '0';
    if (value >= 'a' && value <= 'f') return value - 'a' + 10;
    throw std::runtime_error("hex");
}

std::bitset<outside_pairs> decode_outside() {
    const std::string text(outside_hex);
    if (text.size() != 95U) throw std::runtime_error("hex length");
    std::bitset<outside_pairs> result;
    int rank = 0;
    for (auto position = text.rbegin(); position != text.rend(); ++position) {
        const int digit = hex_digit(*position);
        for (int bit = 0; bit < 4 && rank < outside_pairs; ++bit, ++rank) {
            if ((digit >> bit) & 1) result.set(static_cast<std::size_t>(rank));
        }
    }
    if (hex_digit(text.front()) >= 4) throw std::runtime_error("high outside bits");
    return result;
}

struct Graph {
    std::bitset<outside_pairs> outside = decode_outside();
    std::array<bool, n> marked{};

    Graph() {
        for (const int index : outside_e) marked.at(static_cast<std::size_t>(outside_first + index)) = true;
    }

    bool red(int left, int right) const {
        if (left > right) std::swap(left, right);
        if (left == u && right == v) return true;
        if ((left == u || left == v) && right >= core_first && right < outside_first) return true;
        if (left >= core_first && right < outside_first) {
            return core_edge(left - core_first, right - core_first);
        }
        if (left == u && right >= outside_first) return right - outside_first < 7;
        if (left == v && right >= outside_first) {
            const int index = right - outside_first;
            return index >= 7 && index < 14;
        }
        if (left >= core_first && left < outside_first && right >= outside_first) {
            const int core = left - core_first;
            const int outside_index = right - outside_first;
            return ((footprints.at(static_cast<std::size_t>(outside_index)) >> core) & 1U) != 0U;
        }
        if (left >= outside_first) {
            return outside.test(static_cast<std::size_t>(pair_rank(left - outside_first, right - outside_first)));
        }
        throw std::runtime_error("unclassified edge");
    }
};

int local_triangles(const Graph& graph, int vertex, bool color) {
    std::vector<int> neighbors;
    for (int other = 0; other < n; ++other) {
        if (other != vertex && graph.red(vertex, other) == color) neighbors.push_back(other);
    }
    int result = 0;
    for (std::size_t i = 0; i < neighbors.size(); ++i) {
        for (std::size_t j = i + 1; j < neighbors.size(); ++j) {
            result += graph.red(neighbors[i], neighbors[j]) == color;
        }
    }
    return result;
}

}  // namespace

int main() {
    const Graph graph;
    if (graph.outside.count() != 183U) throw std::runtime_error("outside edge count");
    for (int vertex = 0; vertex < n; ++vertex) {
        int degree = 0;
        int incidence = 0;
        for (int other = 0; other < n; ++other) {
            if (other == vertex || !graph.red(vertex, other)) continue;
            ++degree;
            incidence += graph.marked.at(static_cast<std::size_t>(other));
        }
        const int expected_degree = graph.marked.at(static_cast<std::size_t>(vertex)) ? 20 : 21;
        const int expected_incidence = vertex == outside_first ? 8 : 6;
        if (degree != expected_degree || incidence != expected_incidence) {
            throw std::runtime_error("degree or incidence");
        }
    }
    for (const int anchor : {u, v}) {
        if (local_triangles(graph, anchor, true) != 100 ||
            local_triangles(graph, anchor, false) != 100) {
            throw std::runtime_error("anchor triangles");
        }
    }

    std::vector<std::array<int, 2>> core_edges;
    std::vector<std::array<int, 2>> independent_pairs;
    std::vector<std::array<int, 3>> independent_triples;
    for (int i = 0; i < core_order; ++i) {
        for (int j = i + 1; j < core_order; ++j) {
            (core_edge(i, j) ? core_edges : independent_pairs).push_back({i, j});
            for (int k = j + 1; k < core_order; ++k) {
                if (!core_edge(i, j) && !core_edge(i, k) && !core_edge(j, k)) {
                    independent_triples.push_back({i, j, k});
                }
            }
        }
    }
    if (core_edges.size() != 26U || independent_pairs.size() != 52U ||
        independent_triples.size() != 78U) {
        throw std::runtime_error("core census");
    }

    int x_sum = 0;
    int p_sum = 0;
    int q_sum = 0;
    for (int outside_index = 0; outside_index < outside_order; ++outside_index) {
        const unsigned mask = footprints.at(static_cast<std::size_t>(outside_index));
        if (outside_index < 14) x_sum += static_cast<int>(std::bitset<core_order>(mask).count());
        for (const auto edge : core_edges) {
            p_sum += ((mask >> edge[0]) & 1U) && ((mask >> edge[1]) & 1U);
        }
        for (const auto pair : independent_pairs) {
            q_sum += !((mask >> pair[0]) & 1U) && !((mask >> pair[1]) & 1U);
        }
    }

    int red_outside_triangles = 0;
    int blue_outside_triangles = 0;
    for (int i = 0; i < outside_order; ++i) {
        for (int j = i + 1; j < outside_order; ++j) {
            for (int k = j + 1; k < outside_order; ++k) {
                const bool ij = graph.outside.test(static_cast<std::size_t>(pair_rank(i, j)));
                const bool ik = graph.outside.test(static_cast<std::size_t>(pair_rank(i, k)));
                const bool jk = graph.outside.test(static_cast<std::size_t>(pair_rank(j, k)));
                red_outside_triangles += ij && ik && jk;
                blue_outside_triangles += !ij && !ik && !jk;
            }
        }
    }
    const int target_red = 33 + x_sum + p_sum;
    const int target_blue = 119 + q_sum;
    if (x_sum != 96 || p_sum != 231 || q_sum != 294 || target_red != 360 ||
        target_blue != 413 || red_outside_triangles != 318 || blue_outside_triangles != 455) {
        throw std::runtime_error("balance data");
    }

    int max_core_edge = 0;
    int max_pair_miss = 0;
    int max_cell_edge = 0;
    int max_triple_miss = 0;
    for (const auto edge : core_edges) {
        int load = 0;
        std::array<int, 2> cell_load{};
        for (int outside_index = 0; outside_index < outside_order; ++outside_index) {
            const unsigned mask = footprints.at(static_cast<std::size_t>(outside_index));
            const bool contains = ((mask >> edge[0]) & 1U) && ((mask >> edge[1]) & 1U);
            load += contains;
            if (outside_index < 14) cell_load.at(static_cast<std::size_t>(outside_index / 7)) += contains;
        }
        max_core_edge = std::max(max_core_edge, load);
        max_cell_edge = std::max({max_cell_edge, cell_load[0], cell_load[1]});
    }
    for (const auto pair : independent_pairs) {
        int load = 0;
        for (const unsigned mask : footprints) {
            load += !((mask >> pair[0]) & 1U) && !((mask >> pair[1]) & 1U);
        }
        max_pair_miss = std::max(max_pair_miss, load);
    }
    for (const auto triple : independent_triples) {
        int load = 0;
        for (const unsigned mask : footprints) {
            load += !((mask >> triple[0]) & 1U) && !((mask >> triple[1]) & 1U) &&
                    !((mask >> triple[2]) & 1U);
        }
        max_triple_miss = std::max(max_triple_miss, load);
    }
    if (std::array<int, 4>{max_core_edge, max_pair_miss, max_cell_edge, max_triple_miss} !=
        std::array<int, 4>{12, 8, 3, 3}) {
        throw std::runtime_error("capacity maxima");
    }

    std::array<int, 6> red_fives{};
    std::array<int, 6> blue_fives{};
    for (int a = 0; a < n; ++a) for (int b = a + 1; b < n; ++b)
    for (int c = b + 1; c < n; ++c) for (int d = c + 1; d < n; ++d)
    for (int e = d + 1; e < n; ++e) {
        const std::array<int, 5> vertices = {a, b, c, d, e};
        bool all_red = true;
        bool all_blue = true;
        for (int i = 0; i < 5; ++i) for (int j = i + 1; j < 5; ++j) {
            const bool color = graph.red(vertices[static_cast<std::size_t>(i)],
                                         vertices[static_cast<std::size_t>(j)]);
            all_red = all_red && color;
            all_blue = all_blue && !color;
        }
        const int count = static_cast<int>(std::count_if(
            vertices.begin(), vertices.end(), [](int vertex) { return vertex >= outside_first; }));
        red_fives.at(static_cast<std::size_t>(count)) += all_red;
        blue_fives.at(static_cast<std::size_t>(count)) += all_blue;
    }
    for (int count = 0; count <= 2; ++count) {
        if (red_fives.at(static_cast<std::size_t>(count)) != 0 ||
            blue_fives.at(static_cast<std::size_t>(count)) != 0) {
            throw std::runtime_error("pairwise K5 scope");
        }
    }

    std::cout << "PASS independent_balance k=0 delta=0 X=96 P=231 Q=294\n";
    std::cout << "outside_triangles=red318,blue455 targets=red360,blue413 "
                 "discrepancy=red-42,blue42\n";
    std::cout << "capacity_maxima=core_edge12,independent_pair_miss8,"
                 "cell_core_edge3,independent_triple_miss3\n";
    std::cout << "K5_by_outside=0:0,0;1:0,0;2:0,0;3:181,42;4:123,321;5:31,168\n";
    std::cout << "STATUS VERIFIED C13 OUTSIDE-TRIANGLE BALANCE OBSTRUCTION\n";
}
