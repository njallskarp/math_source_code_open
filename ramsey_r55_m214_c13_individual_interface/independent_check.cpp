#include <array>
#include <bit>
#include <cstdlib>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int core_order = 13;
constexpr int outside_order = 28;
constexpr int full = (1 << core_order) - 1;
constexpr std::array<int, outside_order> rows = {
    0x1c48, 0x1630, 0x1391, 0x02ee, 0x11a9, 0x04de, 0x1fff,
    0x0067, 0x19c5, 0x091c, 0x0e2c, 0x18f3, 0x0f12, 0x19f7,
    0x0703, 0x1033, 0x078c, 0x1eb4, 0x1f42, 0x0b4b, 0x04be,
    0x189b, 0x1f6d, 0x07fc, 0x19c0, 0x0979, 0x069f, 0x1667,
};
constexpr std::array<bool, outside_order> marked = {
    true, true, true, true, true, true, false,
    true, true, true, true, true, true, false,
    true, false, false, false, false, false, false,
    false, false, false, false, false, false, false,
};
constexpr std::array<unsigned, outside_order> outside_adjacency = {
    0x3e40e3e, 0x6a6f039, 0x7a1c529, 0xf810897,
    0x369c12b, 0x45a2a17, 0x1005f00, 0x8fad708,
    0x91a16d4, 0x217b9e1, 0x45569c5, 0x8e01669,
    0xc0e6bc2, 0xf005622, 0x91db4d6, 0xff94296,
    0xfe8c61c, 0xfe013a2, 0xff05603, 0xfa1d1b0,
    0xfa4c7a0, 0x31f8897, 0x1078cb1, 0x01f888f,
    0x07fe15d, 0x03fa21f, 0x01fb42e, 0x01ff988,
};

[[noreturn]] void fail(const std::string& message) {
  std::cerr << "FAIL " << message << '\n';
  std::exit(1);
}

void require(bool condition, const std::string& message) {
  if (!condition) fail(message);
}

bool core_edge(int i, int j) {
  if (i == j) return false;
  int difference = (i - j + core_order) % core_order;
  return difference == 1 || difference == 5 || difference == 8 || difference == 12;
}

bool is_independent_mask(int mask) {
  for (int i = 0; i < core_order; ++i)
    for (int j = i + 1; j < core_order; ++j)
      if ((mask & (1 << i)) && (mask & (1 << j)) && core_edge(i, j)) return false;
  return true;
}

bool contains_core_edge(int mask) {
  for (int i = 0; i < core_order; ++i)
    for (int j = i + 1; j < core_order; ++j)
      if ((mask & (1 << i)) && (mask & (1 << j)) && core_edge(i, j)) return true;
  return false;
}

bool contains_independent_triple(int mask) {
  for (int i = 0; i < core_order; ++i)
    for (int j = i + 1; j < core_order; ++j)
      for (int k = j + 1; k < core_order; ++k) {
        int triple = (1 << i) | (1 << j) | (1 << k);
        if ((mask & triple) == triple && !core_edge(i, j) && !core_edge(i, k) &&
            !core_edge(j, k)) return true;
      }
  return false;
}

bool legal_footprint(int mask) {
  for (int subset = 0; subset <= full; ++subset)
    if (std::popcount(static_cast<unsigned>(subset)) == 4 && is_independent_mask(subset) &&
        (mask & subset) == 0) return false;
  return true;
}

bool blue_forbidden(int x, int y) {
  return contains_independent_triple(full ^ (rows[x] | rows[y]));
}

bool red_forbidden(int x, int y) {
  return contains_core_edge(rows[x] & rows[y]);
}

} // namespace

int main() {
  int core_edges = 0;
  for (int i = 0; i < core_order; ++i)
    for (int j = i + 1; j < core_order; ++j) core_edges += core_edge(i, j);
  int independent_triples = 0;
  int independent_fours = 0;
  for (int mask = 0; mask <= full; ++mask) {
    int size = std::popcount(static_cast<unsigned>(mask));
    if (is_independent_mask(mask) && size == 3) ++independent_triples;
    if (is_independent_mask(mask) && size == 4) ++independent_fours;
  }
  int transversals = 0;
  for (int mask = 0; mask <= full; ++mask) transversals += legal_footprint(mask);
  require(core_edges == 26 && independent_triples == 78 && independent_fours == 39 &&
          transversals == 3459, "core census");
  for (int mask : rows) require(legal_footprint(mask), "nontransversal row");

  std::array<int, core_order> columns{};
  std::array<int, core_order> marked_columns{};
  for (int x = 0; x < outside_order; ++x)
    for (int i = 0; i < core_order; ++i) {
      columns[i] += (rows[x] >> i) & 1;
      if (marked[x]) marked_columns[i] += (rows[x] >> i) & 1;
    }
  for (int i = 0; i < core_order; ++i)
    require(columns[i] == 15 && marked_columns[i] == 6, "column equation");

  auto outside_red = [&](int x, int y) {
    return ((outside_adjacency[x] >> y) & 1U) != 0;
  };
  int outside_red_edges = 0;
  for (int x = 0; x < outside_order; ++x) {
    require((outside_adjacency[x] >> outside_order) == 0, "outside adjacency range");
    require(!outside_red(x, x), "outside loop");
    for (int y = x + 1; y < outside_order; ++y) {
      require(outside_red(x, y) == outside_red(y, x), "outside adjacency symmetry");
      outside_red_edges += outside_red(x, y);
      if (!outside_red(x, y)) require(!blue_forbidden(x, y), "forbidden blue edge");
      bool same_cell = (x < 7 && y < 7) || (7 <= x && y < 14);
      if (outside_red(x, y) && same_cell)
        require(!red_forbidden(x, y), "forbidden red edge");
    }
  }
  require(outside_red_edges == 183, "outside edge count");

  int incidence_a = 0, incidence_b = 0, incidence_o = 0;
  for (int x = 0; x < 7; ++x) incidence_a += std::popcount(static_cast<unsigned>(rows[x]));
  for (int x = 7; x < 14; ++x) incidence_b += std::popcount(static_cast<unsigned>(rows[x]));
  for (int x = 14; x < 28; ++x) incidence_o += std::popcount(static_cast<unsigned>(rows[x]));
  require(incidence_a == 49 && incidence_b == 47 && incidence_o == 99, "incidences");

  auto edge_count = [&](int first_a, int last_a, int first_b, int last_b, bool internal) {
    int result = 0;
    for (int x = first_a; x < last_a; ++x)
      for (int y = first_b; y < last_b; ++y)
        if ((!internal || x < y) && outside_red(x, y)) ++result;
    return result;
  };
  int m_a = edge_count(0, 7, 0, 7, true);
  int m_b = edge_count(7, 14, 7, 14, true);
  int m_o = edge_count(14, 28, 14, 28, true);
  int m_ab = edge_count(0, 7, 7, 14, false);
  int m_ao = edge_count(0, 7, 14, 28, false);
  int m_bo = edge_count(7, 14, 14, 28, false);
  require(m_a == 12 && m_b == 14 && m_o == 55 && m_ab == 18 && m_ao == 43 &&
          m_bo == 41, "cell edge counts");
  require(m_a + incidence_a == 61 && m_b + incidence_b == 61, "anchor red equations");
  require(m_b + m_o + m_bo == 110 && m_a + m_o + m_ao == 110,
          "anchor blue equations");

  auto red = [&](int left, int right) {
    if (left > right) std::swap(left, right);
    if (left == 0 && right == 1) return true;
    if (left < 2 && right >= 2 && right < 15) return true;
    if (left >= 2 && left < 15 && right < 15) return core_edge(left - 2, right - 2);
    if (left == 0 && right >= 15) return right - 15 < 7;
    if (left == 1 && right >= 15) return right - 15 >= 7 && right - 15 < 14;
    if (left >= 2 && left < 15 && right >= 15)
      return ((rows[right - 15] >> (left - 2)) & 1) != 0;
    if (left >= 15) return outside_red(left - 15, right - 15);
    fail("unclassified edge");
  };

  auto globally_marked = [&](int vertex) {
    return vertex >= 15 && marked[vertex - 15];
  };
  for (int vertex = 0; vertex < 43; ++vertex) {
    int degree = 0;
    int e_incidence = 0;
    for (int other = 0; other < 43; ++other) {
      if (other == vertex) continue;
      bool color = red(vertex, other);
      degree += color;
      e_incidence += color && globally_marked(other);
    }
    require(degree == 21 - static_cast<int>(globally_marked(vertex)), "individual degree");
    require(e_incidence == 6 + 2 * (vertex == 15), "individual E incidence");
  }

  auto triangle_count = [&](int vertex, bool color) {
    int result = 0;
    for (int left = 0; left < 43; ++left) {
      if (left == vertex || red(vertex, left) != color) continue;
      for (int right = left + 1; right < 43; ++right)
        if (right != vertex && red(vertex, right) == color && red(left, right) == color)
          ++result;
    }
    return result;
  };
  require(triangle_count(0, true) == 100 && triangle_count(0, false) == 100 &&
          triangle_count(1, true) == 100 && triangle_count(1, false) == 100,
          "anchor triangle counts");
  int triangle_mismatches = 0;
  for (int vertex = 0; vertex < 43; ++vertex) {
    int expected = globally_marked(vertex) ? 93 : 100;
    if (triangle_count(vertex, true) != expected || triangle_count(vertex, false) != expected)
      ++triangle_mismatches;
  }
  require(triangle_mismatches == 39, "triangle mismatch census");

  std::array<int, 6> red_fives{};
  std::array<int, 6> blue_fives{};
  for (int a = 0; a < 43; ++a)
    for (int b = a + 1; b < 43; ++b)
      for (int c = b + 1; c < 43; ++c)
        for (int d = c + 1; d < 43; ++d)
          for (int e = d + 1; e < 43; ++e) {
            int outside = (a >= 15) + (b >= 15) + (c >= 15) + (d >= 15) + (e >= 15);
            std::array<int, 5> vertices{a, b, c, d, e};
            bool all_red = true, all_blue = true;
            for (int i = 0; i < 5; ++i)
              for (int j = i + 1; j < 5; ++j) {
                bool color = red(vertices[i], vertices[j]);
                all_red = all_red && color;
                all_blue = all_blue && !color;
              }
            red_fives[outside] += all_red;
            blue_fives[outside] += all_blue;
          }
  require(red_fives == std::array<int, 6>{0, 0, 0, 181, 123, 31},
          "red K5 census");
  require(blue_fives == std::array<int, 6>{0, 0, 0, 42, 321, 168},
          "blue K5 census");

  std::cout << "VERIFIED INDIVIDUAL PAIRWISE-INTERFACE WITNESS\n";
  std::cout << "core_edges=26 independent_triples=78 independent_fours=39 transversals=3459\n";
  std::cout << "columns=15x13 marked_columns=6x13\n";
  std::cout << "degrees=20^13,21^30 E_incidences=6^42,8^1 anchor_triangles=100,100,100,100\n";
  std::cout << "IA=49 IB=47 IO=99 mA=12 mB=14 mO=55 mAB=18 mAO=43 mBO=41\n";
  std::cout << "K5_by_outside red=0,0,0,181,123,31 blue=0,0,0,42,321,168\n";
  std::cout << "outside_edges=183 triangle_mismatch_vertices=39\n";
}
