#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int n = 43;
constexpr int prior_variables = 13633;
constexpr int selector_first = 13245;
constexpr std::array<const char*, 5> families = {
    "E8", "E77", "C8", "C77", "C77partition"};

using MKey = std::tuple<int, int, int>;
using QKey = std::tuple<int, int, int, int>;

struct Root {
  std::string family;
  int common;
  int exceptional_common;
  std::string pattern;
};

void require(bool condition, const std::string& message) {
  if (!condition) throw std::runtime_error(message);
}

int occurrences(const std::string& pattern, char cell) {
  return static_cast<int>(std::count(pattern.begin(), pattern.end(), cell));
}

std::vector<std::string> patterns(const std::string& family) {
  if (family == "E8") return {"H", "A"};
  if (family == "E77") return {"BB", "BO", "OO"};
  if (family == "C8") return {"B", "O"};
  if (family == "C77") return {"BB", "BO", "OO"};
  if (family == "C77partition") return {"HO", "AB"};
  throw std::runtime_error("unknown family");
}

std::vector<Root> make_roots() {
  std::vector<Root> result;
  constexpr std::array<char, 4> cell_names = {'H', 'A', 'B', 'O'};
  for (const char* family_text : families) {
    const std::string family(family_text);
    for (int common = 9; common <= 13; ++common) {
      for (int k = 0; k <= 6; ++k) {
        const std::array<int, 4> e_sizes = {k, 6-k, 6-k, 1+k};
        const std::array<int, 4> c_sizes = {
            common-k, 14-common+k, 14-common+k, common-k};
        const auto& sizes = family.front() == 'E' ? e_sizes : c_sizes;
        for (const auto& pattern : patterns(family)) {
          bool valid = true;
          for (std::size_t index = 0; index < cell_names.size(); ++index) {
            valid = valid && occurrences(pattern, cell_names[index]) <= sizes[index];
          }
          if (valid) result.push_back({family, common, k, pattern});
        }
      }
    }
  }
  return result;
}

std::array<std::vector<int>, 8> cells(const Root& root) {
  const int c = root.common;
  const int k = root.exceptional_common;
  const std::array<int, 8> sizes = {
      k, 6-k, 6-k, 1+k, c-k, 14-c+k, 14-c+k, c-k};
  std::array<std::vector<int>, 8> result;
  int cursor = 2;
  for (std::size_t index = 0; index < result.size(); ++index) {
    for (int count = 0; count < sizes[index]; ++count) result[index].push_back(cursor++);
  }
  require(cursor == n, "cell partition");
  return result;
}

std::pair<std::vector<int>, std::vector<int>> root_data(const Root& root) {
  const auto partition = cells(root);
  std::vector<int> core = partition[0];
  core.insert(core.end(), partition[4].begin(), partition[4].end());
  std::array<bool, n> in_core{};
  for (int vertex : core) in_core[vertex] = true;
  std::vector<int> exterior;
  for (int vertex = 2; vertex < n; ++vertex) {
    if (!in_core[vertex]) exterior.push_back(vertex);
  }
  require(static_cast<int>(core.size()) == root.common, "core size");
  require(static_cast<int>(exterior.size()) == 41-root.common, "exterior size");
  return {core, exterior};
}

int edge_id(int i, int j) {
  if (i > j) std::swap(i, j);
  require(0 <= i && i < j && j < n, "physical edge");
  return i * (2*n-i-1) / 2 + (j-i-1) + 1;
}

std::string opb_row(const std::vector<std::pair<int, int>>& terms, int rhs) {
  std::ostringstream output;
  bool first = true;
  for (const auto& [coefficient, variable] : terms) {
    if (!first) output << ' ';
    first = false;
    output << (coefficient >= 0 ? "+" : "") << coefficient << " x" << variable;
  }
  output << " >= " << rhs << " ;";
  return output.str();
}

std::string read_all(const std::string& path) {
  std::ifstream input(path, std::ios::binary);
  require(static_cast<bool>(input), "cannot open " + path);
  std::ostringstream output;
  output << input.rdbuf();
  require(!input.bad(), "read failure " + path);
  return output.str();
}

bool red13(int i, int j) {
  const int difference = (i-j+13) % 13;
  return difference == 1 || difference == 5 || difference == 8 || difference == 12;
}

bool independent(std::uint16_t vertices) {
  for (int i = 0; i < 13; ++i) {
    if (!(vertices & (1u << i))) continue;
    for (int j = i+1; j < 13; ++j) {
      if ((vertices & (1u << j)) && red13(i, j)) return false;
    }
  }
  return true;
}

int alpha(std::uint16_t vertices) {
  int maximum = 0;
  for (std::uint16_t subset = vertices;; subset = (subset-1) & vertices) {
    if (independent(subset)) maximum = std::max(maximum, std::popcount(subset));
    if (subset == 0) break;
  }
  return maximum;
}

std::array<int, 6> enumerate_min_edges() {
  std::array<int, 6> minima{};
  minima.fill(100);
  for (int order = 0; order <= 5; ++order) {
    std::vector<std::pair<int, int>> edges;
    for (int i = 0; i < order; ++i) {
      for (int j = i+1; j < order; ++j) edges.push_back({i, j});
    }
    const std::uint32_t limit = 1u << edges.size();
    for (std::uint32_t graph = 0; graph < limit; ++graph) {
      bool triangle_free = true;
      bool complement_triangle_free = true;
      for (int i = 0; i < order; ++i) {
        for (int j = i+1; j < order; ++j) {
          for (int k = j+1; k < order; ++k) {
            auto present = [&](int a, int b) {
              if (a > b) std::swap(a, b);
              const auto it = std::find(edges.begin(), edges.end(), std::pair<int, int>{a, b});
              require(it != edges.end(), "edge lookup");
              const auto index = static_cast<unsigned>(it-edges.begin());
              return (graph >> index) & 1u;
            };
            const bool ij = present(i, j);
            const bool ik = present(i, k);
            const bool jk = present(j, k);
            triangle_free = triangle_free && !(ij && ik && jk);
            complement_triangle_free = complement_triangle_free && !(!ij && !ik && !jk);
          }
        }
      }
      if (triangle_free && complement_triangle_free) {
        minima[order] = std::min(minima[order], std::popcount(graph));
      }
    }
  }
  return minima;
}

void check_logic() {
  for (int left = 0; left <= 1; ++left) {
    for (int right = 0; right <= 1; ++right) {
      int feasible = -1;
      for (int missed = 0; missed <= 1; ++missed) {
        const bool ok = -missed-left >= -1 && -missed-right >= -1 &&
                        missed+left+right >= 1;
        if (ok) {
          require(feasible == -1, "nonunique missed definition");
          feasible = missed;
        }
      }
      require(feasible == (1-left)*(1-right), "missed truth table");
    }
  }
  for (int mi = 0; mi <= 1; ++mi) {
    for (int mj = 0; mj <= 1; ++mj) {
      for (int edge = 0; edge <= 1; ++edge) {
        int feasible = -1;
        for (int inside = 0; inside <= 1; ++inside) {
          const bool ok = -inside+mi >= 0 && -inside+mj >= 0 &&
                          -inside+edge >= 0 && inside-mi-mj-edge >= -2;
          if (ok) {
            require(feasible == -1, "nonunique inside definition");
            feasible = inside;
          }
        }
        require(feasible == mi*mj*edge, "inside truth table");
      }
    }
  }

  for (int common = 9; common <= 13; ++common) {
    for (int selector = 0; selector <= 1; ++selector) {
      for (int pair_edge = 0; pair_edge <= 1; ++pair_edge) {
        for (int missed = 0; missed <= common; ++missed) {
          for (int inside = 0; inside <= missed*(missed-1)/2; ++inside) {
            const bool active_blue = selector == 1 && pair_edge == 0;
            const bool row0 = -missed + (common-5)*pair_edge -
                              (common-5)*selector >= -common;
            const bool row1 = inside-missed + (common-2)*pair_edge -
                              (common-2)*selector >= -common;
            const bool row2 = inside-3*missed + (3*common-10)*pair_edge -
                              (3*common-10)*selector >= -3*common;
            require(row0 == (!active_blue || missed <= 5), "missed guard");
            require(row1 == (!active_blue || inside >= missed-2), "first facet guard");
            require(row2 == (!active_blue || inside >= 3*missed-10), "second facet guard");
          }
        }
      }
    }
  }
}

void check_sharpness(const std::array<int, 6>& minima) {
  require(minima == std::array<int, 6>{0, 0, 0, 1, 2, 5}, "small Ramsey minima");
  const std::array<std::uint16_t, 3> missed = {
      static_cast<std::uint16_t>((1u<<0)|(1u<<1)|(1u<<3)),
      static_cast<std::uint16_t>((1u<<0)|(1u<<1)|(1u<<3)|(1u<<4)),
      static_cast<std::uint16_t>((1u<<0)|(1u<<1)|(1u<<2)|(1u<<3)|(1u<<8))};
  const std::array<int, 3> expected_edges = {1, 2, 5};
  for (std::size_t index = 0; index < missed.size(); ++index) {
    int count = 0;
    for (int i = 0; i < 13; ++i) {
      if (!(missed[index] & (1u << i))) continue;
      for (int j = i+1; j < 13; ++j) {
        if ((missed[index] & (1u << j)) && red13(i, j)) ++count;
      }
    }
    require(count == expected_edges[index] && alpha(missed[index]) == 2,
            "cyclic sharp missed set");
  }
  const std::array<int, 13> order = {0,1,2,3,4,5,8,9,6,7,10,11,12};
  std::uint16_t core = 0;
  for (int index = 0; index < 13; ++index) {
    core |= static_cast<std::uint16_t>(1u << order[index]);
    if (index >= 8) require(alpha(core) == 4, "cyclic core alpha");
  }
}

void compare_formula(const std::string& prior_path, const std::string& formula_path,
                     const std::string& suffix_path) {
  std::ifstream prior(prior_path, std::ios::binary);
  std::ifstream formula(formula_path, std::ios::binary);
  require(static_cast<bool>(prior) && static_cast<bool>(formula), "cannot open formula stream");
  std::string prior_header;
  std::string formula_header;
  std::getline(prior, prior_header);
  std::getline(formula, formula_header);
  require(prior_header ==
          "* #variable= 13633 #constraint= 2131051 #equal= 87 intsize= 64",
          "prior formula header");
  require(formula_header ==
          "* #variable= 98758 #constraint= 2969925 #equal= 87 intsize= 64",
          "strengthened formula header");

  std::vector<char> prior_buffer(1 << 20);
  std::vector<char> formula_buffer(1 << 20);
  while (prior) {
    prior.read(prior_buffer.data(), static_cast<std::streamsize>(prior_buffer.size()));
    const std::streamsize count = prior.gcount();
    if (count == 0) break;
    formula.read(formula_buffer.data(), count);
    require(formula.gcount() == count, "short strengthened prior body");
    require(std::equal(prior_buffer.begin(), prior_buffer.begin()+count,
                       formula_buffer.begin()), "strengthened prior-body mismatch");
  }

  std::ifstream suffix(suffix_path, std::ios::binary);
  require(static_cast<bool>(suffix), "cannot reopen suffix");
  while (suffix) {
    suffix.read(prior_buffer.data(), static_cast<std::streamsize>(prior_buffer.size()));
    const std::streamsize count = suffix.gcount();
    if (count == 0) break;
    formula.read(formula_buffer.data(), count);
    require(formula.gcount() == count, "short strengthened suffix");
    require(std::equal(prior_buffer.begin(), prior_buffer.begin()+count,
                       formula_buffer.begin()), "strengthened suffix mismatch");
  }
  char extra = 0;
  require(!formula.get(extra), "strengthened formula has trailing bytes");
}

}  // namespace

int main(int argc, char** argv) {
  try {
    require(argc == 3 || argc == 5,
            "usage: independent_check ROOTS SUFFIX [PRIOR FORMULA]");
    const auto roots = make_roots();
    require(roots.size() == 389, "root count");

    std::set<MKey> missed_support;
    std::set<QKey> inside_support;
    std::array<std::int64_t, 5> pair_counts{};
    std::int64_t root_pairs = 0;
    for (const auto& root : roots) {
      const auto [core, exterior] = root_data(root);
      const auto pairs = static_cast<std::int64_t>(exterior.size()*(exterior.size()-1)/2);
      pair_counts[static_cast<std::size_t>(root.common-9)] += pairs;
      root_pairs += pairs;
      for (std::size_t a = 0; a < exterior.size(); ++a) {
        for (std::size_t b = a+1; b < exterior.size(); ++b) {
          const int left = exterior[a];
          const int right = exterior[b];
          for (int vertex : core) missed_support.emplace(left, right, vertex);
          for (std::size_t i = 0; i < core.size(); ++i) {
            for (std::size_t j = i+1; j < core.size(); ++j) {
              inside_support.emplace(left, right, core[i], core[j]);
            }
          }
        }
      }
    }
    require(missed_support.size() == 10612, "missed support count");
    require(inside_support.size() == 74513, "inside support count");
    require(root_pairs == 169662, "root pair count");
    require(pair_counts == std::array<std::int64_t, 5>{38688,36270,33930,31668,29106},
            "root pair distribution");

    std::map<MKey, int> missed_ids;
    int next = prior_variables+1;
    for (const auto& key : missed_support) missed_ids[key] = next++;
    std::map<QKey, int> inside_ids;
    for (const auto& key : inside_support) inside_ids[key] = next++;
    require(next-1 == 98758, "final variable count");

    std::ostringstream certificate;
    certificate << "index\tfamily\tc\tk\tpattern\tselector\tH\texterior\tpairs\trows\n";
    for (std::size_t index = 0; index < roots.size(); ++index) {
      const auto& root = roots[index];
      const auto [core, exterior] = root_data(root);
      const auto pairs = exterior.size()*(exterior.size()-1)/2;
      certificate << index << '\t' << root.family << '\t' << root.common << '\t'
                  << root.exceptional_common << '\t' << root.pattern << '\t'
                  << selector_first+static_cast<int>(index) << '\t';
      for (std::size_t i = 0; i < core.size(); ++i) {
        if (i) certificate << ',';
        certificate << core[i];
      }
      certificate << '\t' << exterior.size() << '\t' << pairs << '\t' << 3*pairs << '\n';
    }
    require(read_all(argv[1]) == certificate.str(), "root certificate mismatch");

    std::ifstream suffix(argv[2], std::ios::binary);
    require(static_cast<bool>(suffix), "cannot open suffix");
    std::int64_t rows_checked = 0;
    auto check_row = [&](const std::string& expected) {
      std::string actual;
      require(static_cast<bool>(std::getline(suffix, actual)), "short suffix");
      require(actual == expected, "suffix row mismatch at " + std::to_string(rows_checked+1));
      ++rows_checked;
    };

    for (const auto& [key, missed] : missed_ids) {
      const auto [left, right, vertex] = key;
      const int left_edge = edge_id(left, vertex);
      const int right_edge = edge_id(right, vertex);
      check_row(opb_row({{-1,missed},{-1,left_edge}}, -1));
      check_row(opb_row({{-1,missed},{-1,right_edge}}, -1));
      check_row(opb_row({{1,missed},{1,left_edge},{1,right_edge}}, 1));
    }
    for (const auto& [key, inside] : inside_ids) {
      const auto [left, right, i, j] = key;
      const int mi = missed_ids.at({left,right,i});
      const int mj = missed_ids.at({left,right,j});
      const int edge = edge_id(i,j);
      check_row(opb_row({{-1,inside},{1,mi}}, 0));
      check_row(opb_row({{-1,inside},{1,mj}}, 0));
      check_row(opb_row({{-1,inside},{1,edge}}, 0));
      check_row(opb_row({{1,inside},{-1,mi},{-1,mj},{-1,edge}}, -2));
    }
    for (std::size_t root_index = 0; root_index < roots.size(); ++root_index) {
      const auto& root = roots[root_index];
      const auto [core, exterior] = root_data(root);
      const int selector = selector_first+static_cast<int>(root_index);
      for (std::size_t a = 0; a < exterior.size(); ++a) {
        for (std::size_t b = a+1; b < exterior.size(); ++b) {
          const int left = exterior[a];
          const int right = exterior[b];
          const int pair_edge = edge_id(left,right);
          std::vector<std::pair<int,int>> missed_terms;
          std::vector<std::pair<int,int>> inside_terms;
          for (int vertex : core) missed_terms.push_back({-1,missed_ids.at({left,right,vertex})});
          for (std::size_t i = 0; i < core.size(); ++i) {
            for (std::size_t j = i+1; j < core.size(); ++j) {
              inside_terms.push_back({1,inside_ids.at({left,right,core[i],core[j]})});
            }
          }
          auto terms = missed_terms;
          terms.push_back({root.common-5,pair_edge});
          terms.push_back({-(root.common-5),selector});
          check_row(opb_row(terms,-root.common));

          terms = inside_terms;
          terms.insert(terms.end(),missed_terms.begin(),missed_terms.end());
          terms.push_back({root.common-2,pair_edge});
          terms.push_back({-(root.common-2),selector});
          check_row(opb_row(terms,-root.common));

          terms = inside_terms;
          for (auto& term : missed_terms) term.first = -3;
          terms.insert(terms.end(),missed_terms.begin(),missed_terms.end());
          terms.push_back({3*root.common-10,pair_edge});
          terms.push_back({-(3*root.common-10),selector});
          check_row(opb_row(terms,-3*root.common));
        }
      }
    }
    std::string extra;
    require(!std::getline(suffix, extra), "suffix has extra rows");
    require(rows_checked == 838874, "suffix row total");

    check_logic();
    const auto minima = enumerate_min_edges();
    check_sharpness(minima);
    if (argc == 5) compare_formula(argv[3], argv[4], argv[2]);

    std::cout << "{\"definition_rows\":329888,\"final_variables\":98758,"
              << "\"full_formula\":" << (argc == 5 ? "true" : "false") << ','
              << "\"missed_keys\":10612,\"red_inside_keys\":74513,"
              << "\"root_pairs\":169662,\"rows_checked\":" << rows_checked
              << ",\"sharp_min_edges\":[0,0,0,1,2,5],\"status\":\"PASS\"}\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
