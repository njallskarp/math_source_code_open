#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int n = 43;
constexpr int selector_first = 13245;
constexpr std::array<const char*, 5> families = {
    "E8", "E77", "C8", "C77", "C77partition"};

struct Root {
  std::string family;
  int common;
  int exceptional_common;
  std::string pattern;
};

void require(bool condition, const std::string& message) {
  if (!condition) throw std::runtime_error(message);
}

std::vector<std::string> patterns(const std::string& family) {
  if (family == "E8") return {"H", "A"};
  if (family == "E77") return {"BB", "BO", "OO"};
  if (family == "C8") return {"B", "O"};
  if (family == "C77") return {"BB", "BO", "OO"};
  if (family == "C77partition") return {"HO", "AB"};
  throw std::runtime_error("unknown family");
}

int occurrences(const std::string& pattern, char cell) {
  return static_cast<int>(std::count(pattern.begin(), pattern.end(), cell));
}

std::vector<Root> roots() {
  std::vector<Root> result;
  for (const char* family_c : families) {
    const std::string family(family_c);
    for (int common = 9; common <= 13; ++common) {
      for (int k = 0; k <= 6; ++k) {
        const std::array<int, 4> e_sizes = {k, 6-k, 6-k, 1+k};
        const std::array<int, 4> c_sizes = {
            common-k, 14-common+k, 14-common+k, common-k};
        const auto& sizes = family.front() == 'E' ? e_sizes : c_sizes;
        for (const auto& pattern : patterns(family)) {
          constexpr std::array<char, 4> cells = {'H', 'A', 'B', 'O'};
          bool valid = true;
          for (std::size_t i = 0; i < cells.size(); ++i) {
            valid = valid && occurrences(pattern, cells[i]) <= sizes[i];
          }
          if (valid) result.push_back({family, common, k, pattern});
        }
      }
    }
  }
  return result;
}

std::array<std::vector<int>, 8> root_cells(const Root& root) {
  const int c = root.common;
  const int k = root.exceptional_common;
  const std::array<int, 8> sizes = {
      k, 6-k, 6-k, 1+k, c-k, 14-c+k, 14-c+k, c-k};
  std::array<std::vector<int>, 8> cells;
  int cursor = 2;
  for (std::size_t i = 0; i < cells.size(); ++i) {
    for (int j = 0; j < sizes[i]; ++j) cells[i].push_back(cursor++);
  }
  require(cursor == n, "root cells do not partition vertices");
  return cells;
}

int edge_id(int i, int j) {
  if (i > j) std::swap(i, j);
  require(0 <= i && i < j && j < n, "invalid edge");
  return i * (2*n-i-1) / 2 + (j-i-1) + 1;
}

std::string join_vertices(const std::vector<int>& vertices) {
  std::ostringstream output;
  for (std::size_t i = 0; i < vertices.size(); ++i) {
    if (i) output << ',';
    output << vertices[i];
  }
  return output.str();
}

std::string expected_certificate(const std::vector<Root>& all_roots) {
  std::ostringstream output;
  output << "index\tfamily\tc\tk\tpattern\tselector\tbound\tH\texterior\tpair_rows\n";
  for (std::size_t index = 0; index < all_roots.size(); ++index) {
    const Root& root = all_roots[index];
    if (root.common != 9 && root.common != 10) continue;
    const auto cells = root_cells(root);
    std::vector<int> core = cells[0];
    core.insert(core.end(), cells[4].begin(), cells[4].end());
    const int exterior = 41-root.common;
    output << index << '\t' << root.family << '\t' << root.common << '\t'
           << root.exceptional_common << '\t' << root.pattern << '\t'
           << selector_first + static_cast<int>(index) << '\t'
           << root.common - 5 << '\t' << join_vertices(core) << '\t'
           << exterior << '\t' << exterior*(exterior-1)/2 << '\n';
  }
  return output.str();
}

std::string expected_suffix(const std::vector<Root>& all_roots) {
  std::ostringstream output;
  for (std::size_t index = 0; index < all_roots.size(); ++index) {
    const Root& root = all_roots[index];
    if (root.common != 9 && root.common != 10) continue;
    const auto cells = root_cells(root);
    std::vector<int> core = cells[0];
    core.insert(core.end(), cells[4].begin(), cells[4].end());
    std::array<bool, n> in_core{};
    for (int vertex : core) in_core[vertex] = true;
    std::vector<int> exterior;
    for (int vertex = 2; vertex < n; ++vertex) {
      if (!in_core[vertex]) exterior.push_back(vertex);
    }
    const int bound = root.common-5;
    for (std::size_t left_index = 0; left_index < exterior.size(); ++left_index) {
      for (std::size_t right_index = left_index+1; right_index < exterior.size(); ++right_index) {
        const int left = exterior[left_index];
        const int right = exterior[right_index];
        bool first = true;
        for (int vertex : core) {
          if (!first) output << ' ';
          first = false;
          output << "+1 x" << edge_id(left, vertex);
        }
        for (int vertex : core) output << " +1 x" << edge_id(right, vertex);
        output << " +" << bound << " x" << edge_id(left, right)
               << " -" << bound << " x" << selector_first + static_cast<int>(index)
               << " >= 0 ;\n";
      }
    }
  }
  return output.str();
}

std::string read_all(const std::string& filename) {
  std::ifstream input(filename, std::ios::binary);
  require(static_cast<bool>(input), "cannot open " + filename);
  std::ostringstream output;
  output << input.rdbuf();
  require(!input.bad(), "read failure for " + filename);
  return output.str();
}

void compare_formula(const std::string& prior_name, const std::string& strong_name,
                     const std::string& expected_suffix_text) {
  std::ifstream prior(prior_name, std::ios::binary);
  std::ifstream strong(strong_name, std::ios::binary);
  require(static_cast<bool>(prior) && static_cast<bool>(strong), "cannot open formula files");
  std::string prior_header;
  std::string strong_header;
  std::getline(prior, prior_header);
  std::getline(strong, strong_header);
  require(prior_header == "* #variable= 13633 #constraint= 2056093 #equal= 87 intsize= 64",
          "prior formula header");
  require(strong_header == "* #variable= 13633 #constraint= 2131051 #equal= 87 intsize= 64",
          "strengthened formula header");
  std::vector<char> prior_buffer(1 << 20);
  std::vector<char> strong_buffer(1 << 20);
  while (prior) {
    prior.read(prior_buffer.data(), static_cast<std::streamsize>(prior_buffer.size()));
    const std::streamsize count = prior.gcount();
    if (count == 0) break;
    strong.read(strong_buffer.data(), count);
    require(strong.gcount() == count, "short strengthened prior body");
    require(std::equal(prior_buffer.begin(), prior_buffer.begin()+count,
                       strong_buffer.begin()), "strengthened prior-body mismatch");
  }
  std::ostringstream remainder;
  remainder << strong.rdbuf();
  require(remainder.str() == expected_suffix_text, "strengthened suffix mismatch");
}

bool red13(int i, int j) {
  const int difference = (i-j+13) % 13;
  return difference == 1 || difference == 5 || difference == 8 || difference == 12;
}

bool independent(std::uint16_t mask) {
  for (int i = 0; i < 13; ++i) {
    if (!(mask & (1u << i))) continue;
    for (int j = i+1; j < 13; ++j) {
      if ((mask & (1u << j)) && red13(i,j)) return false;
    }
  }
  return true;
}

int independence_number(std::uint16_t universe) {
  int maximum = 0;
  for (std::uint16_t subset = universe;; subset = (subset-1) & universe) {
    if (independent(subset)) maximum = std::max(maximum, std::popcount(subset));
    if (subset == 0) break;
  }
  return maximum;
}

bool hits_independent(std::uint16_t footprint, std::uint16_t universe, int size) {
  for (std::uint16_t subset = universe;; subset = (subset-1) & universe) {
    if (std::popcount(subset) == size && independent(subset) && !(subset & footprint)) {
      return false;
    }
    if (subset == 0) break;
  }
  return true;
}

void check_sharpness() {
  const std::array<int, 8> t_vertices = {0,1,2,3,4,5,8,9};
  const std::array<int, 5> extras = {6,7,10,11,12};
  std::uint16_t core = 0;
  for (int vertex : t_vertices) core |= static_cast<std::uint16_t>(1u << vertex);
  const std::uint16_t missed_c5 =
      (1u<<0) | (1u<<1) | (1u<<2) | (1u<<3) | (1u<<8);
  for (int i = 0; i < 13; ++i) {
    for (int j = i+1; j < 13; ++j) {
      for (int k = j+1; k < 13; ++k) {
        require(!(red13(i,j) && red13(i,k) && red13(j,k)), "cyclic triangle");
      }
    }
  }
  require(independence_number(missed_c5) == 2, "missed C5 alpha");
  for (int offset = 0; offset < 5; ++offset) {
    core |= static_cast<std::uint16_t>(1u << extras[offset]);
    const int common = 9+offset;
    const std::uint16_t union_sharp = core & ~missed_c5;
    require(std::popcount(union_sharp) == common-5, "union sharp size");
    require(hits_independent(union_sharp, core, 4), "union unary validity");
    require(hits_independent(union_sharp, core, 3), "union pair validity");
  }

  const std::array<std::uint16_t, 2> left = {
      static_cast<std::uint16_t>((1u<<0)|(1u<<4)),
      static_cast<std::uint16_t>((1u<<0)|(1u<<4)|(1u<<5))};
  const std::array<std::uint16_t, 2> right = {
      static_cast<std::uint16_t>((1u<<5)|(1u<<6)),
      static_cast<std::uint16_t>((1u<<2)|(1u<<3))};
  const std::array<std::uint16_t, 2> individual = {
      static_cast<std::uint16_t>(1u<<6),
      static_cast<std::uint16_t>((1u<<6)|(1u<<7))};
  core = 0;
  for (int vertex : t_vertices) core |= static_cast<std::uint16_t>(1u << vertex);
  for (int offset = 0; offset < 2; ++offset) {
    core |= static_cast<std::uint16_t>(1u << extras[offset]);
    const int common = 9+offset;
    require((left[offset] & right[offset]) == 0, "sum sharp overlap");
    require(std::popcount(left[offset]) + std::popcount(right[offset]) == common-5,
            "sum sharp total");
    require(hits_independent(left[offset], core, 4) &&
            hits_independent(right[offset], core, 4), "sum sharp unary validity");
    require(hits_independent(left[offset] | right[offset], core, 3),
            "sum sharp pair validity");
    require(std::popcount(individual[offset]) == common-8, "individual footprint size");
    require(hits_independent(individual[offset], core, 4), "individual unary validity");
    require(!hits_independent(individual[offset], core, 3), "individual pair violation");
  }
}

}  // namespace

int main(int argc, char** argv) {
  try {
    require(argc == 3 || argc == 5,
            "usage: independent_check ROOTS_TSV SUFFIX [PRIOR_OPB STRONG_OPB]");
    const auto all_roots = roots();
    require(all_roots.size() == 389, "root count");
    const std::string certificate = expected_certificate(all_roots);
    const std::string suffix = expected_suffix(all_roots);
    require(certificate == read_all(argv[1]), "certificate byte mismatch");
    require(suffix == read_all(argv[2]), "suffix byte mismatch");
    if (argc == 5) compare_formula(argv[3], argv[4], suffix);
    check_sharpness();

    std::array<int, 5> family_counts{};
    std::array<int, 2> common_counts{};
    int active_roots = 0;
    for (const auto& root : all_roots) {
      if (root.common != 9 && root.common != 10) continue;
      ++active_roots;
      ++common_counts[root.common-9];
      for (std::size_t index = 0; index < families.size(); ++index) {
        if (root.family == families[index]) ++family_counts[index];
      }
    }
    std::cout << "roots " << all_roots.size() << '\n';
    std::cout << "active_roots " << active_roots << '\n';
    std::cout << "family_counts";
    for (int count : family_counts) std::cout << ' ' << count;
    std::cout << "\ncommon_counts " << common_counts[0] << ' ' << common_counts[1] << '\n';
    std::cout << "suffix_rows " << std::count(suffix.begin(), suffix.end(), '\n') << '\n';
    std::cout << "sharp_union_bounds 4 5 6 7 8\n";
    std::cout << "sharp_sum_witnesses 4 5\n";
    std::cout << "individual_only_violations 2 4\n";
    if (argc == 5) std::cout << "strengthened_formula constraints 2131051\n";
    std::cout << "status PASS\n";
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
