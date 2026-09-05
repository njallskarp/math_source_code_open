#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int N = 43;
constexpr int EXCEPTIONAL_COUNT = 13;
constexpr int ANCHOR = 13;
constexpr int EDGE_COUNT = N * (N - 1) / 2;
constexpr int TRIANGLE_COUNT = N * (N - 1) * (N - 2) / 6;
constexpr int VARIABLE_COUNT = EDGE_COUNT + TRIANGLE_COUNT;
constexpr int FIVE_SET_COUNT = N * (N - 1) * (N - 2) * (N - 3) * (N - 4) / 120;
constexpr int EQUALITY_COUNT = 2 * N + (N - 1);
constexpr int CONSTRAINT_COUNT = 2 * FIVE_SET_COUNT + 4 * TRIANGLE_COUNT + 4 * N - 1;

std::int64_t choose2(std::int64_t n) { return n * (n - 1) / 2; }

int edge_id(int i, int j) {
  if (i > j) std::swap(i, j);
  if (!(0 <= i && i < j && j < N)) throw std::runtime_error("bad edge");
  return i * (2 * N - i - 1) / 2 + (j - i - 1) + 1;
}

int triangle_id(int i, int j, int k) {
  std::array<int, 3> v{i, j, k};
  if (v[0] > v[1]) std::swap(v[0], v[1]);
  if (v[1] > v[2]) std::swap(v[1], v[2]);
  if (v[0] > v[1]) std::swap(v[0], v[1]);
  if (!(0 <= v[0] && v[0] < v[1] && v[1] < v[2] && v[2] < N))
    throw std::runtime_error("bad triangle");
  std::int64_t rank = 0;
  for (int a = 0; a < v[0]; ++a) rank += choose2(N - a - 1);
  for (int b = v[0] + 1; b < v[1]; ++b) rank += N - b - 1;
  rank += v[2] - v[1] - 1;
  return EDGE_COUNT + static_cast<int>(rank) + 1;
}

std::string row(const std::vector<std::pair<int, int>>& terms,
                const char* relation, int rhs) {
  std::ostringstream out;
  bool first = true;
  for (auto [coefficient, variable] : terms) {
    if (!first) out << ' ';
    first = false;
    if (coefficient >= 0) out << '+';
    out << coefficient << " x" << variable;
  }
  out << ' ' << relation << ' ' << rhs << " ;";
  return out.str();
}

class StreamChecker {
 public:
  explicit StreamChecker(const std::string& path) : input_(path) {
    if (!input_) throw std::runtime_error("cannot open OPB file: " + path);
  }

  void expect(const std::string& wanted) {
    std::string actual;
    if (!std::getline(input_, actual))
      throw std::runtime_error("unexpected EOF before line " + std::to_string(line_ + 1));
    ++line_;
    if (!actual.empty() && actual.back() == '\r') actual.pop_back();
    if (actual != wanted) {
      throw std::runtime_error("line " + std::to_string(line_) + " mismatch\nexpected: " +
                               wanted + "\nactual:   " + actual);
    }
  }

  void finish() {
    std::string extra;
    if (std::getline(input_, extra))
      throw std::runtime_error("unexpected extra line " + std::to_string(line_ + 1));
  }

  std::int64_t line() const { return line_; }

 private:
  std::ifstream input_;
  std::int64_t line_ = 0;
};

bool anchor_red(int v) {
  return (0 <= v && v <= 5) || (14 <= v && v <= 28);
}
}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 2) {
      std::cerr << "usage: check_opb FORMULA.opb\n";
      return 2;
    }
    StreamChecker check(argv[1]);
    check.expect("* #variable= " + std::to_string(VARIABLE_COUNT) +
                 " #constraint= " + std::to_string(CONSTRAINT_COUNT) +
                 " #equal= " + std::to_string(EQUALITY_COUNT) + " intsize= 64");

    std::int64_t constraints = 0;
    for (int a = 0; a < N; ++a)
      for (int b = a + 1; b < N; ++b)
        for (int c = b + 1; c < N; ++c)
          for (int d = c + 1; d < N; ++d)
            for (int e = d + 1; e < N; ++e) {
              const std::array<int, 5> vertices{a, b, c, d, e};
              std::vector<std::pair<int, int>> positive, negative;
              for (int i = 0; i < 5; ++i)
                for (int j = i + 1; j < 5; ++j) {
                  int edge = edge_id(vertices[i], vertices[j]);
                  positive.push_back({1, edge});
                  negative.push_back({-1, edge});
                }
              check.expect(row(positive, ">=", 1));
              check.expect(row(negative, ">=", -9));
              constraints += 2;
            }

    for (int i = 0; i < N; ++i)
      for (int j = i + 1; j < N; ++j)
        for (int k = j + 1; k < N; ++k) {
          int z = triangle_id(i, j, k);
          std::array<int, 3> edges{edge_id(i, j), edge_id(i, k), edge_id(j, k)};
          for (int edge : edges) check.expect(row({{-1, z}, {1, edge}}, ">=", 0));
          check.expect(row({{1, z}, {-1, edges[0]}, {-1, edges[1]}, {-1, edges[2]}},
                           ">=", -2));
          constraints += 4;
        }

    for (int v = 0; v < N; ++v) {
      std::vector<std::pair<int, int>> terms;
      for (int w = 0; w < N; ++w)
        if (w != v) terms.push_back({1, edge_id(v, w)});
      check.expect(row(terms, "=", v < EXCEPTIONAL_COUNT ? 20 : 21));
      ++constraints;
    }

    for (int v = 0; v < N; ++v) {
      std::vector<std::pair<int, int>> terms;
      for (int i = 0; i < N; ++i)
        if (i != v)
          for (int j = i + 1; j < N; ++j)
            if (j != v) terms.push_back({1, triangle_id(v, i, j)});
      check.expect(row(terms, "=", v < EXCEPTIONAL_COUNT ? 93 : 100));
      ++constraints;
    }

    for (int v = 0; v < N; ++v) {
      std::vector<std::pair<int, int>> terms;
      for (int w = 0; w < EXCEPTIONAL_COUNT; ++w)
        if (w != v) terms.push_back({1, edge_id(v, w)});
      check.expect(row(terms, ">=", 6));
      ++constraints;
    }

    for (int w = 0; w < N; ++w) {
      if (w == ANCHOR) continue;
      check.expect(row({{1, edge_id(ANCHOR, w)}}, "=", anchor_red(w) ? 1 : 0));
      ++constraints;
    }

    check.finish();
    if (constraints != CONSTRAINT_COUNT || check.line() != CONSTRAINT_COUNT + 1)
      throw std::runtime_error("internal count mismatch");

    const std::int64_t degree_sum = 13 * 20 + 30 * 21;
    const std::int64_t red_edges = degree_sum / 2;
    const std::int64_t exceptional_incidence = 13 * 20;
    const std::int64_t blue_excess = exceptional_incidence - 43 * 6;
    if (degree_sum != 890 || red_edges != 445 || blue_excess != 2)
      throw std::runtime_error("branch arithmetic mismatch");

    std::cout << "PASS canonical_opb variables=" << VARIABLE_COUNT
              << " constraints=" << CONSTRAINT_COUNT << " five_sets=" << FIVE_SET_COUNT
              << " triangles=" << TRIANGLE_COUNT << "\n";
    std::cout << "PASS branch_arithmetic red_edges=" << red_edges
              << " exceptional_incidence=" << exceptional_incidence
              << " blue_excess=" << blue_excess << " exact_anchors=28..30\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAIL " << error.what() << "\n";
    return 1;
  }
}
