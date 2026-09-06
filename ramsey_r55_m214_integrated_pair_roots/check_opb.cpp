#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {
constexpr int N = 43;
constexpr int EDGE_COUNT = N * (N - 1) / 2;
constexpr int TRIANGLE_COUNT = N * (N - 1) * (N - 2) / 6;
constexpr int BASE_VARIABLE_COUNT = EDGE_COUNT + TRIANGLE_COUNT;
constexpr int FIVE_SET_COUNT = N * (N - 1) * (N - 2) * (N - 3) * (N - 4) / 120;
constexpr int ROOT_COUNT = 389;
constexpr int PARTITION_ROOT_COUNT = 70;
constexpr int VARIABLE_COUNT = BASE_VARIABLE_COUNT + ROOT_COUNT;
constexpr int BASE_CONSTRAINT_COUNT = 2 * FIVE_SET_COUNT + 4 * TRIANGLE_COUNT + 3 * N;
constexpr int SELECTOR_ROWS = ROOT_COUNT * (83 + 2 * N) + PARTITION_ROOT_COUNT * (1 + 2 * 28) + 1;
constexpr int CONSTRAINT_COUNT = BASE_CONSTRAINT_COUNT + SELECTOR_ROWS;
constexpr int EQUALITY_COUNT = 2 * N + 1;
constexpr int SELECTOR_FIRST = BASE_VARIABLE_COUNT + 1;

struct RootKey {
  int family;
  int common;
  int exceptional_common;
  std::string pattern;
};

struct RootRecord {
  std::array<int, N> a_targets{};
  std::vector<int> anomalies;
  std::vector<std::tuple<int, int, int>> units;
  bool is_partition = false;
  int p = -1;
  int q = -1;
  std::vector<int> partition_vertices;
};

bool exceptional(int vertex) { return 2 <= vertex && vertex <= 14; }

std::int64_t choose2(std::int64_t value) { return value * (value - 1) / 2; }

int edge_id(int i, int j) {
  if (i > j) std::swap(i, j);
  if (!(0 <= i && i < j && j < N)) throw std::runtime_error("bad edge");
  return i * (2 * N - i - 1) / 2 + (j - i - 1) + 1;
}

int triangle_id(int i, int j, int k) {
  std::array<int, 3> vertices{i, j, k};
  std::sort(vertices.begin(), vertices.end());
  if (!(0 <= vertices[0] && vertices[0] < vertices[1] &&
        vertices[1] < vertices[2] && vertices[2] < N))
    throw std::runtime_error("bad triangle");
  std::int64_t rank = 0;
  for (int a = 0; a < vertices[0]; ++a) rank += choose2(N - a - 1);
  for (int b = vertices[0] + 1; b < vertices[1]; ++b) rank += N - b - 1;
  rank += vertices[2] - vertices[1] - 1;
  return EDGE_COUNT + static_cast<int>(rank) + 1;
}

std::string row(const std::vector<std::pair<int, int>>& terms,
                const char* relation, int rhs) {
  if (terms.empty()) throw std::runtime_error("empty row");
  std::ostringstream output;
  bool first = true;
  for (auto [coefficient, variable] : terms) {
    if (!first) output << ' ';
    first = false;
    if (coefficient >= 0) output << '+';
    output << coefficient << " x" << variable;
  }
  output << ' ' << relation << ' ' << rhs << " ;";
  return output.str();
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
    if (actual != wanted)
      throw std::runtime_error("line " + std::to_string(line_) + " mismatch\nexpected: " +
                               wanted + "\nactual:   " + actual);
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

std::vector<std::string> patterns(int family) {
  if (family == 0) return {"H", "A"};
  if (family == 1 || family == 3) return {"BB", "BO", "OO"};
  if (family == 2) return {"B", "O"};
  return {"HO", "AB"};
}

std::vector<RootKey> root_keys() {
  std::vector<RootKey> result;
  for (int family = 0; family < 5; ++family)
    for (int common = 9; common <= 13; ++common)
      for (int k = 0; k <= 6; ++k) {
        const std::array<int, 4> e{k, 6 - k, 6 - k, 1 + k};
        const std::array<int, 4> c{common - k, 14 - common + k,
                                   14 - common + k, common - k};
        for (const std::string& pattern : patterns(family)) {
          bool fits = true;
          const std::string names = "HABO";
          for (int index = 0; index < 4; ++index) {
            const int used = static_cast<int>(std::count(pattern.begin(), pattern.end(), names[index]));
            const int available = family <= 1 ? e[index] : c[index];
            if (used > available) fits = false;
          }
          if (fits) result.push_back({family, common, k, pattern});
        }
      }
  return result;
}

RootRecord make_record(const RootKey& key) {
  const std::array<int, 4> e{key.exceptional_common, 6 - key.exceptional_common,
                              6 - key.exceptional_common, 1 + key.exceptional_common};
  const std::array<int, 4> c{key.common - key.exceptional_common,
                              14 - key.common + key.exceptional_common,
                              14 - key.common + key.exceptional_common,
                              key.common - key.exceptional_common};
  std::array<std::vector<int>, 8> cells;
  int cursor = 2;
  for (int index = 0; index < 8; ++index) {
    const int size = index < 4 ? e[index] : c[index - 4];
    for (int count = 0; count < size; ++count) cells[index].push_back(cursor++);
  }
  if (cursor != N) throw std::runtime_error("cell partition mismatch");

  RootRecord record;
  const int anomaly_offset = key.family <= 1 ? 0 : 4;
  const std::string names = "HABO";
  for (int index = 0; index < 4; ++index) {
    const int count = static_cast<int>(std::count(key.pattern.begin(), key.pattern.end(), names[index]));
    for (int position = 0; position < count; ++position)
      record.anomalies.push_back(cells[anomaly_offset + index][position]);
  }
  const int excess = (key.family == 0 || key.family == 2) ? 2 : 1;
  for (int vertex = 0; vertex < N; ++vertex)
    record.a_targets[vertex] = 6 +
        (std::find(record.anomalies.begin(), record.anomalies.end(), vertex) !=
         record.anomalies.end() ? excess : 0);

  record.units.push_back({0, 1, 1});
  const std::array<std::pair<int, int>, 4> bits{{{1, 1}, {1, 0}, {0, 1}, {0, 0}}};
  for (int index = 0; index < 8; ++index)
    for (int vertex : cells[index]) {
      record.units.push_back({0, vertex, bits[index % 4].first});
      record.units.push_back({1, vertex, bits[index % 4].second});
    }
  std::sort(record.units.begin(), record.units.end());
  if (record.units.size() != 83) throw std::runtime_error("anchor-unit count");

  if (key.family == 4) {
    if (record.anomalies.size() != 2) throw std::runtime_error("partition anomalies");
    record.is_partition = true;
    record.p = record.anomalies[0];
    record.q = record.anomalies[1];
    record.partition_vertices = {0, 1};
    for (int vertex = 15; vertex < N; ++vertex)
      if (vertex != record.p && vertex != record.q)
        record.partition_vertices.push_back(vertex);
    if (record.partition_vertices.size() != 28)
      throw std::runtime_error("partition vertex count");
  }
  return record;
}

void expect_guarded_unit(StreamChecker& check, int edge, int value, int selector) {
  if (value == 1)
    check.expect(row({{1, edge}, {-1, selector}}, ">=", 0));
  else
    check.expect(row({{-1, edge}, {-1, selector}}, ">=", -1));
}

void expect_guarded_equality(StreamChecker& check, const std::vector<int>& variables,
                             int target, int selector, int maximum) {
  std::vector<std::pair<int, int>> lower, upper;
  for (int variable : variables) {
    lower.push_back({1, variable});
    upper.push_back({-1, variable});
  }
  lower.push_back({-target, selector});
  upper.push_back({-(maximum - target), selector});
  check.expect(row(lower, ">=", 0));
  check.expect(row(upper, ">=", -maximum));
}
}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 2) {
      std::cerr << "usage: check_opb FORMULA.opb\n";
      return 2;
    }
    const std::vector<RootKey> keys = root_keys();
    if (keys.size() != ROOT_COUNT) throw std::runtime_error("root census");
    std::array<int, 5> family_counts{};
    for (const RootKey& key : keys) ++family_counts[key.family];
    if (family_counts != std::array<int, 5>{60, 85, 70, 104, 70})
      throw std::runtime_error("family census");

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
                  const int edge = edge_id(vertices[i], vertices[j]);
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
          const int z = triangle_id(i, j, k);
          const std::array<int, 3> edges{edge_id(i, j), edge_id(i, k), edge_id(j, k)};
          for (int edge : edges) check.expect(row({{-1, z}, {1, edge}}, ">=", 0));
          check.expect(row({{1, z}, {-1, edges[0]}, {-1, edges[1]}, {-1, edges[2]}},
                           ">=", -2));
          constraints += 4;
        }

    for (int vertex = 0; vertex < N; ++vertex) {
      std::vector<std::pair<int, int>> terms;
      for (int other = 0; other < N; ++other)
        if (other != vertex) terms.push_back({1, edge_id(vertex, other)});
      check.expect(row(terms, "=", exceptional(vertex) ? 20 : 21));
      ++constraints;
    }

    for (int vertex = 0; vertex < N; ++vertex) {
      std::vector<std::pair<int, int>> terms;
      for (int i = 0; i < N; ++i)
        if (i != vertex)
          for (int j = i + 1; j < N; ++j)
            if (j != vertex) terms.push_back({1, triangle_id(vertex, i, j)});
      check.expect(row(terms, "=", exceptional(vertex) ? 93 : 100));
      ++constraints;
    }

    for (int vertex = 0; vertex < N; ++vertex) {
      std::vector<std::pair<int, int>> terms;
      for (int other = 2; other <= 14; ++other)
        if (other != vertex) terms.push_back({1, edge_id(vertex, other)});
      check.expect(row(terms, ">=", 6));
      ++constraints;
    }

    std::vector<std::pair<int, int>> one_hot;
    for (int index = 0; index < ROOT_COUNT; ++index)
      one_hot.push_back({1, SELECTOR_FIRST + index});
    check.expect(row(one_hot, "=", 1));
    ++constraints;

    int partition_roots = 0;
    for (int root_index = 0; root_index < ROOT_COUNT; ++root_index) {
      const int selector = SELECTOR_FIRST + root_index;
      const RootRecord record = make_record(keys[root_index]);
      for (auto [i, j, value] : record.units) {
        expect_guarded_unit(check, edge_id(i, j), value, selector);
        ++constraints;
      }
      for (int vertex = 0; vertex < N; ++vertex) {
        std::vector<int> variables;
        for (int other = 2; other <= 14; ++other)
          if (other != vertex) variables.push_back(edge_id(vertex, other));
        expect_guarded_equality(check, variables, record.a_targets[vertex], selector, 13);
        constraints += 2;
      }
      if (record.is_partition) {
        ++partition_roots;
        expect_guarded_unit(check, edge_id(record.p, record.q), 0, selector);
        ++constraints;
        for (int vertex : record.partition_vertices) {
          expect_guarded_equality(check,
                                  {edge_id(vertex, record.p), edge_id(vertex, record.q)},
                                  1, selector, 2);
          constraints += 2;
        }
      }
    }

    check.finish();
    if (partition_roots != PARTITION_ROOT_COUNT || constraints != CONSTRAINT_COUNT ||
        check.line() != CONSTRAINT_COUNT + 1)
      throw std::runtime_error("final count mismatch");

    std::cout << "PASS integrated_opb variables=" << VARIABLE_COUNT
              << " constraints=" << CONSTRAINT_COUNT << " equalities=" << EQUALITY_COUNT
              << " base_rows=" << BASE_CONSTRAINT_COUNT << " selector_rows=" << SELECTOR_ROWS
              << "\n";
    std::cout << "PASS roots=389 families=60,85,70,104,70 partition_roots=70"
              << " anchor_units_per_root=83 a_equalities_per_root=43\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAIL " << error.what() << "\n";
    return 1;
  }
}
