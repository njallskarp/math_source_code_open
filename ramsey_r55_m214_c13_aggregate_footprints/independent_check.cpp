#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {

constexpr int kCore = 13;
constexpr std::uint16_t kFull = (1U << kCore) - 1U;

struct RowType {
  char cell;
  int marked;
  std::uint16_t mask;
  int count;
};

constexpr std::array<RowType, 24> kTypes{{
    {'A', 0, 0x1fff, 1}, {'A', 1, 0x031a, 2}, {'A', 1, 0x058c, 1},
    {'A', 1, 0x0e25, 1}, {'A', 1, 0x1858, 1}, {'A', 1, 0x1b81, 1},
    {'B', 0, 0x1fff, 1}, {'B', 1, 0x0067, 2}, {'B', 1, 0x0ce0, 1},
    {'B', 1, 0x10ce, 1}, {'B', 1, 0x1f90, 1}, {'B', 1, 0x1fff, 1},
    {'O', 0, 0x0399, 1}, {'O', 0, 0x04f9, 1}, {'O', 0, 0x0686, 1},
    {'O', 0, 0x0863, 2}, {'O', 0, 0x0d2c, 1}, {'O', 0, 0x131e, 2},
    {'O', 0, 0x13e4, 1}, {'O', 0, 0x1d29, 1}, {'O', 0, 0x1dd7, 1},
    {'O', 0, 0x1ed0, 1}, {'O', 0, 0x1eff, 1}, {'O', 1, 0x1431, 1},
}};

struct EdgeCounts {
  int i_a = 45;
  int i_b = 54;
  int d_a = 89;
  int d_b = 80;
  int d_o = 197;
  int m_a = 16;
  int m_b = 7;
  int m_o = 37;
  int m_ab = 0;
  int m_ao = 57;
  int m_bo = 66;
};

bool CoreEdge(int left, int right) {
  int difference = (left - right) % kCore;
  if (difference < 0) difference += kCore;
  return left != right &&
         (difference == 1 || difference == 5 || difference == 8 || difference == 12);
}

bool IsTransversal(std::uint16_t mask, const std::vector<std::uint16_t>& fours) {
  return std::all_of(fours.begin(), fours.end(),
                     [mask](std::uint16_t four) { return (mask & four) != 0U; });
}

int CellSize(char cell) { return cell == 'O' ? 14 : 7; }
int AnchorRed(char cell) { return cell == 'O' ? 0 : 1; }

void Require(bool condition, const std::string& message) {
  if (!condition) throw std::runtime_error(message);
}

}  // namespace

int main() {
  try {
    std::vector<std::uint16_t> independent_fours;
    for (int a = 0; a < kCore; ++a) {
      for (int b = a + 1; b < kCore; ++b) {
        for (int c = b + 1; c < kCore; ++c) {
          for (int d = c + 1; d < kCore; ++d) {
            const std::array<int, 4> vertices{{a, b, c, d}};
            bool independent = true;
            for (int i = 0; i < 4; ++i) {
              for (int j = i + 1; j < 4; ++j) {
                independent = independent && !CoreEdge(vertices[i], vertices[j]);
              }
            }
            if (independent) {
              independent_fours.push_back(static_cast<std::uint16_t>(
                  (1U << a) | (1U << b) | (1U << c) | (1U << d)));
            }
          }
        }
      }
    }
    Require(independent_fours.size() == 39U, "independent-four census");
    int transversal_count = 0;
    for (std::uint16_t mask = 0; mask <= kFull; ++mask) {
      transversal_count += IsTransversal(mask, independent_fours) ? 1 : 0;
    }
    Require(transversal_count == 3459, "transversal census");

    std::vector<RowType> rows;
    for (const RowType& type : kTypes) {
      Require(type.cell == 'A' || type.cell == 'B' || type.cell == 'O', "cell");
      Require(type.marked == 0 || type.marked == 1, "mark");
      Require(type.count > 0 && IsTransversal(type.mask, independent_fours), "row domain");
      for (int repeat = 0; repeat < type.count; ++repeat) rows.push_back(type);
    }
    Require(rows.size() == 28U, "row count");

    constexpr int k = 0;
    for (char cell : std::array<char, 3>{{'A', 'B', 'O'}}) {
      const int size = static_cast<int>(std::count_if(
          rows.begin(), rows.end(), [cell](const RowType& row) { return row.cell == cell; }));
      const int marked = static_cast<int>(std::count_if(
          rows.begin(), rows.end(), [cell](const RowType& row) {
            return row.cell == cell && row.marked == 1;
          }));
      const int expected_marked = cell == 'O' ? 1 + k : 6 - k;
      Require(size == CellSize(cell) && marked == expected_marked, "cell census");
    }

    for (int core_vertex = 0; core_vertex < kCore; ++core_vertex) {
      int total = 0;
      int marked = 0;
      for (const RowType& row : rows) {
        const int bit = (row.mask >> core_vertex) & 1U;
        total += bit;
        marked += row.marked * bit;
      }
      Require(total == 15, "core column total");
      Require(marked == 6, "core marked column");
    }

    const EdgeCounts edges;
    auto footprint_sum = [&rows](char cell) {
      int result = 0;
      for (const RowType& row : rows) {
        if (row.cell == cell) result += std::popcount(row.mask);
      }
      return result;
    };
    Require(footprint_sum('A') == edges.i_a && edges.m_a + edges.i_a == 61,
            "A anchor red");
    Require(footprint_sum('B') == edges.i_b && edges.m_b + edges.i_b == 61,
            "B anchor red");
    Require(edges.m_b + edges.m_o + edges.m_bo == 110, "u anchor blue");
    Require(edges.m_a + edges.m_o + edges.m_ao == 110, "v anchor blue");

    auto required_sum = [&rows](char cell) {
      int result = 0;
      for (const RowType& row : rows) {
        if (row.cell == cell) {
          result += 21 - row.marked - AnchorRed(cell) - std::popcount(row.mask);
        }
      }
      return result;
    };
    Require(required_sum('A') == edges.d_a &&
                edges.d_a == 2 * edges.m_a + edges.m_ab + edges.m_ao,
            "A degree accounting");
    Require(required_sum('B') == edges.d_b &&
                edges.d_b == 2 * edges.m_b + edges.m_ab + edges.m_bo,
            "B degree accounting");
    Require(required_sum('O') == edges.d_o &&
                edges.d_o == 2 * edges.m_o + edges.m_ao + edges.m_bo,
            "O degree accounting");

    Require(3 <= edges.m_a && edges.m_a <= 16 && 3 <= edges.m_b && edges.m_b <= 16,
            "seven-vertex bounds");
    Require(18 <= edges.m_o && edges.m_o <= 73, "O bounds");
    const int ab = edges.m_a + edges.m_b + edges.m_ab;
    const int all_d = ab + edges.m_o + edges.m_ao + edges.m_bo;
    Require(18 <= ab && ab <= 73 && 84 <= all_d && all_d <= 294,
            "union Turan bounds");

    std::vector<std::uint16_t> a_masks;
    for (const RowType& row : rows) {
      if (row.cell == 'A') a_masks.push_back(row.mask);
    }
    Require(std::count(a_masks.begin(), a_masks.end(), kFull) == 1,
            "one full A footprint");
    for (std::uint16_t mask : a_masks) {
      if (mask == kFull) continue;
      bool contains_edge = false;
      for (int left = 0; left < kCore; ++left) {
        for (int right = left + 1; right < kCore; ++right) {
          contains_edge = contains_edge ||
                          (((mask >> left) & 1U) && ((mask >> right) & 1U) &&
                           CoreEdge(left, right));
        }
      }
      Require(contains_edge, "full-row partner has no core edge");
    }
    constexpr int pairwise_cap = 15;
    Require(edges.m_a == 16 && edges.m_a > pairwise_cap, "missing pairwise coupling");

    std::cout << "status=VERIFIED_AGGREGATE_COUNTEREXAMPLE\n";
    std::cout << "core_independent_fours=39 transversals=3459 rows=28 types=24 k=0\n";
    std::cout << "anchor_incidence_A=45 B=54 internal_A=16 B=7 O=37\n";
    std::cout << "pairwise_full_A_cap=15 required_A_edges=16 gap=1\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAIL " << error.what() << '\n';
    return 1;
  }
}
