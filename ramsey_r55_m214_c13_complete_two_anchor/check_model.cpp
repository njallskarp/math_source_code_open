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
constexpr int n = 43;
constexpr int u = 13;
constexpr int v = 14;
using Matrix = std::array<std::array<bool, n>, n>;

template <std::size_t K, class Predicate>
int count_subsets(const std::vector<int>& ground, Predicate predicate) {
  std::array<int, K> chosen{};
  int count = 0;
  const auto visit = [&](auto&& self, int at, int used) -> void {
    if (used == static_cast<int>(K)) {
      count += predicate(chosen) ? 1 : 0;
      return;
    }
    const int need = static_cast<int>(K) - used;
    for (int i = at; i <= static_cast<int>(ground.size()) - need; ++i) {
      chosen[static_cast<std::size_t>(used)] = ground[static_cast<std::size_t>(i)];
      self(self, i + 1, used + 1);
    }
  };
  visit(visit, 0, 0);
  return count;
}

template <std::size_t K>
bool monochromatic(const Matrix& red, const std::array<int, K>& vertices, bool colour) {
  for (std::size_t i = 0; i < K; ++i)
    for (std::size_t j = i + 1; j < K; ++j)
      if (red[vertices[i]][vertices[j]] != colour) return false;
  return true;
}

Matrix read_model(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open model");
  Matrix red{};
  std::set<std::pair<int, int>> seen;
  std::string line;
  while (std::getline(input, line)) {
    std::istringstream row(line);
    int i = -1;
    int j = -1;
    std::string extra;
    if (!(row >> i >> j) || (row >> extra) || i < 0 || i >= j || j >= n ||
        !seen.emplace(i, j).second)
      throw std::runtime_error("malformed model row");
    red[i][j] = red[j][i] = true;
  }
  if (seen.size() != 445U) throw std::runtime_error("wrong edge count");
  return red;
}

std::vector<int> neighbors(const Matrix& red, int vertex, bool colour) {
  std::vector<int> result;
  for (int other = 0; other < n; ++other)
    if (other != vertex && red[vertex][other] == colour) result.push_back(other);
  return result;
}

int induced_edges(const Matrix& red, const std::vector<int>& vertices, bool colour = true) {
  int result = 0;
  for (std::size_t i = 0; i < vertices.size(); ++i)
    for (std::size_t j = i + 1; j < vertices.size(); ++j)
      result += red[vertices[i]][vertices[j]] == colour ? 1 : 0;
  return result;
}

int cross_edges(const Matrix& red, const std::vector<int>& left, const std::vector<int>& right) {
  int result = 0;
  for (int i : left) for (int j : right) result += red[i][j] ? 1 : 0;
  return result;
}

void check_local(const Matrix& red, const std::vector<int>& vertices, int red_order, int blue_order) {
  const int bad_red = red_order == 4
      ? count_subsets<4>(vertices, [&](const auto& s) { return monochromatic(red, s, true); })
      : count_subsets<5>(vertices, [&](const auto& s) { return monochromatic(red, s, true); });
  const int bad_blue = blue_order == 4
      ? count_subsets<4>(vertices, [&](const auto& s) { return monochromatic(red, s, false); })
      : count_subsets<5>(vertices, [&](const auto& s) { return monochromatic(red, s, false); });
  if (bad_red || bad_blue) throw std::runtime_error("local Ramsey violation");
}
}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 2) throw std::runtime_error("usage: check_model EDGE_LIST");
    const Matrix red = read_model(argv[1]);
    std::vector<int> all(n);
    for (int i = 0; i < n; ++i) all[static_cast<std::size_t>(i)] = i;

    for (int vertex = 0; vertex < n; ++vertex) {
      const auto nr = neighbors(red, vertex, true);
      const int expected_degree = vertex < 13 ? 20 : 21;
      if (static_cast<int>(nr.size()) != expected_degree) throw std::runtime_error("degree mismatch");
      int e_incidence = 0;
      for (int other = 0; other < 13; ++other)
        if (other != vertex) e_incidence += red[vertex][other] ? 1 : 0;
      if (e_incidence != (vertex == 5 ? 8 : 6)) throw std::runtime_error("E-incidence mismatch");
    }

    const auto nru = neighbors(red, u, true);
    const auto nbu = neighbors(red, u, false);
    const auto nrv = neighbors(red, v, true);
    const auto nbv = neighbors(red, v, false);
    std::vector<int> expected_u_red{0,1,2,3,4,5,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28};
    if (nru != expected_u_red || !red[u][v]) throw std::runtime_error("anchor normalization");
    int codegree = 0;
    for (int w = 0; w < n; ++w)
      if (w != u && w != v && red[u][w] && red[v][w]) ++codegree;
    if (codegree != 13) throw std::runtime_error("codegree mismatch");

    check_local(red, nru, 4, 5);
    check_local(red, nbu, 5, 4);
    check_local(red, nrv, 4, 5);
    check_local(red, nbv, 5, 4);
    if (induced_edges(red, nru) != 100 || induced_edges(red, nrv) != 100 ||
        induced_edges(red, nbu, false) != 100 || induced_edges(red, nbv, false) != 100)
      throw std::runtime_error("local total mismatch");

    std::vector<int> r, a, b, d;
    for (int w = 0; w < n; ++w) {
      if (w == u || w == v) continue;
      if (red[u][w] && red[v][w]) r.push_back(w);
      else if (red[u][w]) a.push_back(w);
      else if (red[v][w]) b.push_back(w);
      else d.push_back(w);
    }
    if (std::array<std::size_t,4>{r.size(),a.size(),b.size(),d.size()} !=
        std::array<std::size_t,4>{13,7,7,14}) throw std::runtime_error("cell sizes");
    const auto e_size = [](const std::vector<int>& cell) {
      return static_cast<int>(
          std::count_if(cell.begin(), cell.end(), [](int x) { return x < 13; }));
    };
    if (std::array<int,4>{e_size(r),e_size(a),e_size(b),e_size(d)} !=
        std::array<int,4>{3,3,3,4}) throw std::runtime_error("E cell sizes");
    const std::array<int,4> internal{
      induced_edges(red,r),induced_edges(red,a),induced_edges(red,b),induced_edges(red,d)};
    const std::array<int,6> cross{
      cross_edges(red,r,a),cross_edges(red,r,b),cross_edges(red,a,d),
      cross_edges(red,b,d),cross_edges(red,r,d),cross_edges(red,a,b)};
    if (internal != std::array<int,4>{26,9,8,45} ||
        cross != std::array<int,6>{52,53,56,57,87,11})
      throw std::runtime_error("quotient edge mismatch");
    if (cross[4] + cross[5] != internal[0] + internal[1] + internal[2] + internal[3] + 10)
      throw std::runtime_error("diagonal identity");

    const int red_fives = count_subsets<5>(all, [&](const auto& s) { return monochromatic(red, s, true); });
    const int blue_fives = count_subsets<5>(all, [&](const auto& s) { return monochromatic(red, s, false); });
    if (red_fives != 180 || blue_fives != 513) throw std::runtime_error("global K5 census");

    std::cout << "PASS cpp_c13_complete_two_anchor_model n=43 edges=445 degrees=20^13,21^30 E_incidence=6^42,8^1\n";
    std::cout << "anchors=u13,v14 codegree=13 local_red_edges=100,100 local_blue_edges=100,100\n";
    std::cout << "cells=R13,A7,B7,D14 E_cells=3,3,3,4 C_cells=10,4,4,10\n";
    std::cout << "internal=eR26,eA9,eB8,eD45 cross=eRA52,eRB53,eAD56,eBD57,eRD87,eAB11\n";
    std::cout << "global_outside_obstruction=redK5:" << red_fives << ",blueK5:" << blue_fives << '\n';
  } catch (const std::exception& error) {
    std::cerr << "FAIL " << error.what() << '\n';
    return 1;
  }
}
