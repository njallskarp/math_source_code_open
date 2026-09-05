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
    0x1123, 0x1c48, 0x03ce, 0x10d6, 0x0674, 0x0f78, 0x1fff,
    0x1439, 0x0389, 0x0e0e, 0x0f17, 0x1895, 0x08e2, 0x1fbf,
    0x11a1, 0x1b85, 0x017b, 0x07a1, 0x1c61, 0x1cdd, 0x1c1e,
    0x0c6f, 0x1399, 0x1f3e, 0x0bc2, 0x15f4, 0x02c6, 0x027a,
};
constexpr std::array<bool, outside_order> marked = {
    true, true, true, true, true, true, false,
    true, true, true, true, true, true, false,
    true, false, false, false, false, false, false,
    false, false, false, false, false, false, false,
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

struct CategoryResult {
  int forced{};
  int forbidden{};
};

CategoryResult color_category(const std::vector<std::pair<int, int>>& pairs,
                              int target, bool same_anchor_cell,
                              std::array<std::array<bool, outside_order>, outside_order>& red_d) {
  std::vector<std::pair<int, int>> forced;
  std::vector<std::pair<int, int>> allowed;
  int forbidden = 0;
  for (auto pair : pairs) {
    bool force = blue_forbidden(pair.first, pair.second);
    bool forbid = same_anchor_cell && red_forbidden(pair.first, pair.second);
    if (force) forced.push_back(pair);
    if (!forbid) allowed.push_back(pair);
    else ++forbidden;
    require(!(force && forbid), "no-color pair");
  }
  require(static_cast<int>(forced.size()) <= target, "too many forced-red edges");
  require(target <= static_cast<int>(allowed.size()), "too few red-allowed edges");
  int chosen = 0;
  for (auto pair : forced) {
    red_d[pair.first][pair.second] = red_d[pair.second][pair.first] = true;
    ++chosen;
  }
  for (auto pair : allowed) {
    if (chosen == target) break;
    if (red_d[pair.first][pair.second]) continue;
    red_d[pair.first][pair.second] = red_d[pair.second][pair.first] = true;
    ++chosen;
  }
  require(chosen == target, "category target");
  return {static_cast<int>(forced.size()), forbidden};
}

std::vector<std::pair<int, int>> internal_pairs(int first, int last) {
  std::vector<std::pair<int, int>> answer;
  for (int i = first; i < last; ++i)
    for (int j = i + 1; j < last; ++j) answer.emplace_back(i, j);
  return answer;
}

std::vector<std::pair<int, int>> cross_pairs(int first_a, int last_a, int first_b, int last_b) {
  std::vector<std::pair<int, int>> answer;
  for (int i = first_a; i < last_a; ++i)
    for (int j = first_b; j < last_b; ++j) answer.emplace_back(i, j);
  return answer;
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

  int incidence_a = 0, incidence_b = 0, incidence_o = 0;
  for (int x = 0; x < 7; ++x) incidence_a += std::popcount(static_cast<unsigned>(rows[x]));
  for (int x = 7; x < 14; ++x) incidence_b += std::popcount(static_cast<unsigned>(rows[x]));
  for (int x = 14; x < 28; ++x) incidence_o += std::popcount(static_cast<unsigned>(rows[x]));
  require(incidence_a == 50 && incidence_b == 48 && incidence_o == 97, "incidences");

  constexpr int m_o = 47;
  int m_a = 61 - incidence_a;
  int m_b = 61 - incidence_b;
  int m_ab = m_o - 37;
  int m_ao = 49 + incidence_a - m_o;
  int m_bo = 49 + incidence_b - m_o;
  require(m_a == 11 && m_b == 13 && m_ab == 10 && m_ao == 52 && m_bo == 50,
          "edge targets");

  std::array<std::array<bool, outside_order>, outside_order> red_d{};
  auto result_a = color_category(internal_pairs(0, 7), m_a, true, red_d);
  auto result_b = color_category(internal_pairs(7, 14), m_b, true, red_d);
  auto result_o = color_category(internal_pairs(14, 28), m_o, false, red_d);
  auto result_ab = color_category(cross_pairs(0, 7, 7, 14), m_ab, false, red_d);
  auto result_ao = color_category(cross_pairs(0, 7, 14, 28), m_ao, false, red_d);
  auto result_bo = color_category(cross_pairs(7, 14, 14, 28), m_bo, false, red_d);
  require(result_a.forced == 0 && result_b.forced == 0 && result_o.forced == 5 &&
          result_ab.forced == 10 && result_ao.forced == 17 && result_bo.forced == 21,
          "forced-red census");
  require(result_a.forbidden == 10 && result_b.forbidden == 8, "red-forbidden census");

  int outside_red_edges = 0;
  for (int x = 0; x < outside_order; ++x)
    for (int y = x + 1; y < outside_order; ++y) outside_red_edges += red_d[x][y];
  require(outside_red_edges == 183, "outside edge count");
  require(m_a + incidence_a == 61 && m_b + incidence_b == 61, "anchor red equations");
  require(m_b + m_o + m_bo == 110 && m_a + m_o + m_ao == 110,
          "anchor blue equations");

  auto cell_degree_sum = [&](int first, int last) {
    int total = 0;
    for (int x = first; x < last; ++x) {
      int degree = (x < 14) + std::popcount(static_cast<unsigned>(rows[x]));
      for (int y = 0; y < outside_order; ++y) degree += red_d[x][y];
      total += degree;
    }
    return total;
  };
  auto expected_degree_sum = [&](int first, int last) {
    int total = 0;
    for (int x = first; x < last; ++x) total += 21 - static_cast<int>(marked[x]);
    return total;
  };
  require(cell_degree_sum(0, 7) == expected_degree_sum(0, 7), "A degree sum");
  require(cell_degree_sum(7, 14) == expected_degree_sum(7, 14), "B degree sum");
  require(cell_degree_sum(14, 28) == expected_degree_sum(14, 28), "O degree sum");

  auto red = [&](int left, int right) {
    if (left > right) std::swap(left, right);
    if (left == 0 && right == 1) return true;
    if (left < 2 && right >= 2 && right < 15) return true;
    if (left >= 2 && left < 15 && right < 15) return core_edge(left - 2, right - 2);
    if (left == 0 && right >= 15) return right - 15 < 7;
    if (left == 1 && right >= 15) return right - 15 >= 7 && right - 15 < 14;
    if (left >= 2 && left < 15 && right >= 15)
      return ((rows[right - 15] >> (left - 2)) & 1) != 0;
    if (left >= 15) return red_d[left - 15][right - 15];
    fail("unclassified edge");
  };
  int monochromatic = 0;
  for (int a = 0; a < 43; ++a)
    for (int b = a + 1; b < 43; ++b)
      for (int c = b + 1; c < 43; ++c)
        for (int d = c + 1; d < 43; ++d)
          for (int e = d + 1; e < 43; ++e) {
            int outside = (a >= 15) + (b >= 15) + (c >= 15) + (d >= 15) + (e >= 15);
            if (outside > 2) continue;
            std::array<int, 5> vertices{a, b, c, d, e};
            bool all_red = true, all_blue = true;
            for (int i = 0; i < 5; ++i)
              for (int j = i + 1; j < 5; ++j) {
                bool color = red(vertices[i], vertices[j]);
                all_red = all_red && color;
                all_blue = all_blue && !color;
              }
            monochromatic += all_red || all_blue;
          }
  require(monochromatic == 0, "local monochromatic K5");

  std::cout << "VERIFIED PAIRWISE-COMPATIBLE AGGREGATE SELECTION\n";
  std::cout << "core_edges=26 independent_triples=78 independent_fours=39 transversals=3459\n";
  std::cout << "columns=15x13 marked_columns=6x13\n";
  std::cout << "IA=50 IB=48 IO=97 mA=11 mB=13 mO=47 mAB=10 mAO=52 mBO=50\n";
  std::cout << "forced=A:0,B:0,O:5,AB:10,AO:17,BO:21 red_forbidden=A:10,B:8\n";
  std::cout << "monochromatic_K5_outside_le_2=0 outside_edges=183\n";
}
