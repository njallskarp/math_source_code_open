#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int n = 21;
using Matrix = std::array<std::array<bool, n>, n>;

template <std::size_t K, class Predicate>
int count_subsets(const std::vector<int>& ground, Predicate predicate) {
  std::array<int, K> chosen{};
  int count = 0;
  const auto visit = [&](auto&& self, int at, int used) -> void {
    if (used == K) {
      count += predicate(chosen) ? 1 : 0;
      return;
    }
    for (int i = at; i <= static_cast<int>(ground.size()) - (static_cast<int>(K) - used); ++i) {
      chosen[used] = ground[i];
      self(self, i + 1, used + 1);
    }
  };
  visit(visit, 0, 0);
  return count;
}

template <std::size_t K>
bool monochromatic(const Matrix& red, const std::array<int, K>& vertices, bool colour) {
  for (std::size_t i = 0; i < K; ++i) {
    for (std::size_t j = i + 1; j < K; ++j) {
      if (red[vertices[i]][vertices[j]] != colour) return false;
    }
  }
  return true;
}

Matrix read_certificate(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open certificate");
  Matrix red{};
  std::set<std::pair<int, int>> observed;
  std::string line;
  while (std::getline(input, line)) {
    std::istringstream row(line);
    int i = -1;
    int j = -1;
    std::string extra;
    if (!(row >> i >> j) || (row >> extra) || i < 0 || i >= j || j >= 20 ||
        !observed.emplace(i, j).second) {
      throw std::runtime_error("malformed certificate row");
    }
    red[i][j] = red[j][i] = true;
  }
  if (observed.size() != 87U) throw std::runtime_error("wrong H edge count");
  for (int i = 0; i < 13; ++i) red[i][20] = red[20][i] = true;
  return red;
}
}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 2) throw std::runtime_error("usage: check_extension EDGE_LIST");
    const Matrix red = read_certificate(argv[1]);
    std::vector<int> all(n), r(13), a(7);
    for (int i = 0; i < n; ++i) all[i] = i;
    for (int i = 0; i < 13; ++i) r[i] = i;
    for (int i = 0; i < 7; ++i) a[i] = i + 13;

    if (count_subsets<4>(all, [&](const auto& s) { return monochromatic(red, s, true); }) != 0)
      throw std::runtime_error("red K4");
    if (count_subsets<5>(all, [&](const auto& s) { return monochromatic(red, s, false); }) != 0)
      throw std::runtime_error("blue K5");
    if (count_subsets<3>(r, [&](const auto& s) { return monochromatic(red, s, true); }) != 0)
      throw std::runtime_error("red triangle in R");
    if (count_subsets<5>(r, [&](const auto& s) { return monochromatic(red, s, false); }) != 0)
      throw std::runtime_error("blue K5 in R");
    if (count_subsets<4>(a, [&](const auto& s) { return monochromatic(red, s, true); }) != 0 ||
        count_subsets<4>(a, [&](const auto& s) { return monochromatic(red, s, false); }) != 0)
      throw std::runtime_error("A is not Ramsey(4,4;7)");

    const int red_triangles = count_subsets<3>(all, [&](const auto& s) { return monochromatic(red, s, true); });
    const int blue_fours = count_subsets<4>(all, [&](const auto& s) { return monochromatic(red, s, false); });
    std::vector<int> degrees;
    int edge_count = 0;
    for (int i = 0; i < n; ++i) {
      int degree = 0;
      for (int j = 0; j < n; ++j) degree += red[i][j] ? 1 : 0;
      degrees.push_back(degree);
      for (int j = i + 1; j < n; ++j) edge_count += red[i][j] ? 1 : 0;
    }
    std::sort(degrees.rbegin(), degrees.rend());
    if (edge_count != 100 || degrees.front() != 13) throw std::runtime_error("wrong totals");
    std::cout << "PASS cpp_c13_one_neighborhood_counterexample n=21 edges=" << edge_count
              << " partner_degree=13 red_triangles=" << red_triangles
              << " blue_independent_4sets=" << blue_fours << '\n';
    std::cout << "degree_sequence=";
    for (std::size_t i = 0; i < degrees.size(); ++i)
      std::cout << (i ? "," : "") << degrees[i];
    std::cout << '\n';
  } catch (const std::exception& error) {
    std::cerr << "FAIL " << error.what() << '\n';
    return 1;
  }
}
