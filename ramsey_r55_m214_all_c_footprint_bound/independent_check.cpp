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
          bool valid = true;
          constexpr std::array<char, 4> cells = {'H', 'A', 'B', 'O'};
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
  output << "index\tfamily\tc\tk\tpattern\tselector\tbound\tH\texterior_rows\n";
  for (std::size_t index = 0; index < all_roots.size(); ++index) {
    const Root& root = all_roots[index];
    const auto cells = root_cells(root);
    std::vector<int> core = cells[0];
    core.insert(core.end(), cells[4].begin(), cells[4].end());
    require(static_cast<int>(core.size()) == root.common, "core size");
    output << index << '\t' << root.family << '\t' << root.common << '\t'
           << root.exceptional_common << '\t' << root.pattern << '\t'
           << selector_first + static_cast<int>(index) << '\t'
           << root.common - 8 << '\t' << join_vertices(core) << '\t'
           << 41 - root.common << '\n';
  }
  return output.str();
}

std::string expected_suffix(const std::vector<Root>& all_roots) {
  std::ostringstream output;
  for (std::size_t index = 0; index < all_roots.size(); ++index) {
    const Root& root = all_roots[index];
    const auto cells = root_cells(root);
    std::vector<int> core = cells[0];
    core.insert(core.end(), cells[4].begin(), cells[4].end());
    std::array<bool, n> in_core{};
    for (int vertex : core) in_core[vertex] = true;
    for (int vertex = 2; vertex < n; ++vertex) {
      if (in_core[vertex]) continue;
      bool first = true;
      for (int core_vertex : core) {
        if (!first) output << ' ';
        first = false;
        output << "+1 x" << edge_id(vertex, core_vertex);
      }
      output << " -" << root.common - 8 << " x"
             << selector_first + static_cast<int>(index) << " >= 0 ;\n";
    }
  }
  return output.str();
}

std::string read_all(const std::string& path) {
  std::ifstream input(path, std::ios::binary);
  require(static_cast<bool>(input), "cannot open " + path);
  std::ostringstream output;
  output << input.rdbuf();
  require(!input.bad(), "read failure for " + path);
  return output.str();
}

void compare_formula(const std::string& prior_path, const std::string& strong_path,
                     const std::string& expected_suffix) {
  std::ifstream prior(prior_path, std::ios::binary);
  std::ifstream strong(strong_path, std::ios::binary);
  require(static_cast<bool>(prior) && static_cast<bool>(strong), "cannot open formula files");
  std::string prior_header;
  std::string strong_header;
  std::getline(prior, prior_header);
  std::getline(strong, strong_header);
  require(prior_header == "* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64",
          "prior formula header");
  require(strong_header == "* #variable= 13633 #constraint= 2056093 #equal= 87 intsize= 64",
          "strengthened formula header");
  std::vector<char> prior_buffer(1 << 20);
  std::vector<char> strong_buffer(1 << 20);
  while (prior) {
    prior.read(prior_buffer.data(), static_cast<std::streamsize>(prior_buffer.size()));
    const std::streamsize count = prior.gcount();
    if (count == 0) break;
    strong.read(strong_buffer.data(), count);
    require(strong.gcount() == count, "short strengthened prior body");
    require(std::equal(prior_buffer.begin(), prior_buffer.begin() + count,
                       strong_buffer.begin()), "strengthened prior-body mismatch");
  }
  std::ostringstream remainder;
  remainder << strong.rdbuf();
  require(remainder.str() == expected_suffix, "strengthened suffix mismatch");
}

bool red13(int i, int j) {
  const int difference = (i-j+13) % 13;
  return difference == 1 || difference == 5 || difference == 8 || difference == 12;
}

bool independent(std::uint16_t mask) {
  for (int i = 0; i < 13; ++i) {
    if (!(mask & (1u << i))) continue;
    for (int j = i+1; j < 13; ++j) {
      if ((mask & (1u << j)) && red13(i, j)) return false;
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

int independent_four_count(std::uint16_t universe) {
  int count = 0;
  for (std::uint16_t subset = universe;; subset = (subset-1) & universe) {
    if (std::popcount(subset) == 4 && independent(subset)) ++count;
    if (subset == 0) break;
  }
  return count;
}

void check_sharpness(std::array<int, 5>& four_counts) {
  const std::array<int, 8> t_vertices = {0,1,2,3,4,5,8,9};
  const std::array<int, 5> extras = {6,7,10,11,12};
  std::uint16_t t = 0;
  for (int vertex : t_vertices) t |= static_cast<std::uint16_t>(1u << vertex);
  require(independence_number(t) == 3, "sharp T alpha");
  const std::uint16_t all = (1u << 13) - 1;
  require(independence_number(all) == 4, "cyclic alpha");
  for (int i = 0; i < 13; ++i) {
    for (int j = i+1; j < 13; ++j) {
      for (int k = j+1; k < 13; ++k) {
        require(!(red13(i,j) && red13(i,k) && red13(j,k)), "cyclic triangle");
      }
    }
  }
  std::uint16_t core = t;
  std::uint16_t footprint = 0;
  for (int offset = 0; offset < 5; ++offset) {
    footprint |= static_cast<std::uint16_t>(1u << extras[offset]);
    core |= static_cast<std::uint16_t>(1u << extras[offset]);
    require(independence_number(core) == 4, "sharp core alpha");
    four_counts[offset] = independent_four_count(core);
    for (std::uint16_t subset = core;; subset = (subset-1) & core) {
      if (std::popcount(subset) == 4 && independent(subset)) {
        require((subset & footprint) != 0, "footprint misses independent four");
      }
      if (subset == 0) break;
    }
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

    std::array<int, 5> family_counts{};
    std::array<int, 5> common_counts{};
    for (const auto& root : all_roots) {
      for (std::size_t i = 0; i < families.size(); ++i) {
        if (root.family == families[i]) ++family_counts[i];
      }
      ++common_counts[root.common-9];
    }
    std::array<int, 5> four_counts{};
    check_sharpness(four_counts);

    std::cout << "roots " << all_roots.size() << '\n';
    std::cout << "family_counts";
    for (int count : family_counts) std::cout << ' ' << count;
    std::cout << '\n';
    std::cout << "common_counts";
    for (int count : common_counts) std::cout << ' ' << count;
    std::cout << '\n';
    std::cout << "suffix_rows " << std::count(suffix.begin(), suffix.end(), '\n') << '\n';
    std::cout << "sharp_T_alpha 3\n";
    std::cout << "sharp_core_independent_fours";
    for (int count : four_counts) std::cout << ' ' << count;
    std::cout << '\n';
    if (argc == 5) std::cout << "strengthened_formula constraints 2056093\n";
    std::cout << "status PASS\n";
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
