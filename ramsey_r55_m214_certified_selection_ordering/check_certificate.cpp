#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
constexpr int N = 43;
constexpr int EDGE_COUNT = N * (N - 1) / 2;
constexpr int TRIANGLE_COUNT = N * (N - 1) * (N - 2) / 6;
constexpr int VARIABLE_COUNT = EDGE_COUNT + TRIANGLE_COUNT;
constexpr int BASE_ROWS = 1974731;
constexpr int BASE_EQUALITIES = 128;
constexpr int BASE_INTERNAL_CONSTRAINTS = BASE_ROWS + BASE_EQUALITIES;
constexpr std::array<std::pair<int, int>, 4> CELLS{{{0, 6}, {6, 13}, {14, 29}, {29, 43}}};
constexpr std::array<int, 4> CELL_WEIGHTS{{4352, 4096, 16, 1}};
constexpr int ORDER_ROWS = 232;
constexpr int OUTPUT_ROWS = BASE_ROWS + ORDER_ROWS;

int edge_id(int i, int j) {
  if (i > j) std::swap(i, j);
  if (!(0 <= i && i < j && j < N)) throw std::runtime_error("invalid edge");
  return i * (2 * N - i - 1) / 2 + (j - i - 1) + 1;
}

using TriangleIds = std::array<std::array<std::array<int, N>, N>, N>;

TriangleIds build_triangle_ids() {
  TriangleIds ids{};
  int rank = 0;
  for (int i = 0; i < N; ++i)
    for (int j = i + 1; j < N; ++j)
      for (int k = j + 1; k < N; ++k) ids[i][j][k] = EDGE_COUNT + (++rank);
  if (rank != TRIANGLE_COUNT) throw std::runtime_error("triangle count mismatch");
  return ids;
}

int swapped_vertex(int vertex, int left, int right) {
  if (vertex == left) return right;
  if (vertex == right) return left;
  return vertex;
}

std::map<int, int> key_terms(int vertex, int sign) {
  std::map<int, int> terms;
  for (std::size_t index = 0; index < CELLS.size(); ++index) {
    const auto [begin, end] = CELLS[index];
    for (int other = begin; other < end; ++other) {
      if (other == vertex) continue;
      terms[edge_id(vertex, other)] += sign * CELL_WEIGHTS[index];
    }
  }
  return terms;
}

std::string order_row(int left, int right) {
  std::map<int, int> coefficients = key_terms(right, 1);
  for (const auto& [variable, coefficient] : key_terms(left, -1)) coefficients[variable] += coefficient;
  std::ostringstream out;
  bool first = true;
  for (const auto& [variable, coefficient] : coefficients) {
    if (coefficient == 0) continue;
    if (!first) out << ' ';
    first = false;
    if (coefficient >= 0) out << '+';
    out << coefficient << " x" << variable;
  }
  out << " >= 0 ;";
  return out.str();
}

std::vector<std::pair<int, int>> transposition(int left, int right, const TriangleIds& triangle_ids) {
  std::vector<std::pair<int, int>> result;
  for (int i = 0; i < N; ++i) {
    for (int j = i + 1; j < N; ++j) {
      std::array<int, 2> mapped{{swapped_vertex(i, left, right), swapped_vertex(j, left, right)}};
      std::sort(mapped.begin(), mapped.end());
      const int source = edge_id(i, j);
      const int target = edge_id(mapped[0], mapped[1]);
      if (source != target) result.push_back({source, target});
    }
  }
  for (int i = 0; i < N; ++i) {
    for (int j = i + 1; j < N; ++j) {
      for (int k = j + 1; k < N; ++k) {
        std::array<int, 3> mapped{{swapped_vertex(i, left, right), swapped_vertex(j, left, right),
                                   swapped_vertex(k, left, right)}};
        std::sort(mapped.begin(), mapped.end());
        const int source = triangle_ids[i][j][k];
        const int target = triangle_ids[mapped[0]][mapped[1]][mapped[2]];
        if (source != target) result.push_back({source, target});
      }
    }
  }
  std::sort(result.begin(), result.end());
  if (result.size() != 1722) throw std::runtime_error("transposition support mismatch");
  std::vector<int> sources, targets;
  for (const auto& [source, target] : result) {
    sources.push_back(source);
    targets.push_back(target);
  }
  std::sort(targets.begin(), targets.end());
  if (sources != targets) throw std::runtime_error("transposition is not a permutation");
  return result;
}

std::string witness(int left, int right, const TriangleIds& triangle_ids) {
  std::ostringstream out;
  bool first = true;
  for (const auto& [source, target] : transposition(left, right, triangle_ids)) {
    if (!first) out << ' ';
    first = false;
    out << 'x' << source << " -> x" << target;
  }
  return out.str();
}

class Reader {
 public:
  explicit Reader(const std::string& path) : path_(path), input_(path) {
    if (!input_) throw std::runtime_error("cannot open " + path);
  }

  std::string next() {
    std::string line;
    if (!std::getline(input_, line))
      throw std::runtime_error(path_ + ": unexpected EOF before line " + std::to_string(line_ + 1));
    ++line_;
    if (!line.empty() && line.back() == '\r') line.pop_back();
    return line;
  }

  void expect(const std::string& wanted) {
    const std::string actual = next();
    if (actual != wanted) {
      throw std::runtime_error(path_ + ": line " + std::to_string(line_) + " mismatch\nexpected: " +
                               wanted.substr(0, 300) + "\nactual:   " + actual.substr(0, 300));
    }
  }

  void finish() {
    std::string extra;
    if (std::getline(input_, extra))
      throw std::runtime_error(path_ + ": unexpected extra line " + std::to_string(line_ + 1));
  }

 private:
  std::string path_;
  std::ifstream input_;
  std::int64_t line_ = 0;
};

struct Prior {
  int right;
  std::int64_t constraint_id;
};
}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 4) {
      std::cerr << "usage: check_certificate BASE.opb ORDERED.opb PROOF.pbp\n";
      return 2;
    }
    const TriangleIds triangle_ids = build_triangle_ids();
    Reader base(argv[1]);
    Reader ordered(argv[2]);
    Reader proof(argv[3]);
    base.expect("* #variable= " + std::to_string(VARIABLE_COUNT) + " #constraint= " +
                std::to_string(BASE_ROWS) + " #equal= " + std::to_string(BASE_EQUALITIES) +
                " intsize= 64");
    ordered.expect("* #variable= " + std::to_string(VARIABLE_COUNT) + " #constraint= " +
                   std::to_string(OUTPUT_ROWS) + " #equal= " + std::to_string(BASE_EQUALITIES) +
                   " intsize= 64");
    for (int row_index = 0; row_index < BASE_ROWS; ++row_index) {
      const std::string wanted = base.next();
      const std::string actual = ordered.next();
      if (wanted != actual)
        throw std::runtime_error("ordered formula changes base row " + std::to_string(row_index + 1));
    }
    base.finish();

    proof.expect("pseudo-Boolean proof version 3.0");
    proof.expect("f " + std::to_string(BASE_INTERNAL_CONSTRAINTS) + ";");
    std::array<std::vector<Prior>, N> earlier{};
    std::int64_t next_constraint_id = BASE_INTERNAL_CONSTRAINTS + 1LL;
    int order_rows = 0;
    int explicit_goals = 0;
    for (const auto& [begin, end] : CELLS) {
      for (int left = begin; left < end; ++left) {
        for (int right = left + 1; right < end; ++right) {
          const std::string row = order_row(left, right);
          ordered.expect(row);
          const std::string constraint = row.substr(0, row.size() - 2);
          const std::string prefix = "red " + constraint + " : " + witness(left, right, triangle_ids);
          std::int64_t current_constraint_id;
          if (earlier[left].empty()) {
            proof.expect(prefix + ";");
            current_constraint_id = next_constraint_id++;
          } else {
            proof.expect(prefix + " : subproof");
            const std::int64_t inversion_premise_id = next_constraint_id;
            current_constraint_id = inversion_premise_id + 1 + 2 * earlier[left].size();
            next_constraint_id = current_constraint_id + 1;
            for (const Prior& prior : earlier[left]) {
              proof.expect("  proofgoal " + std::to_string(prior.constraint_id));
              proof.expect("    pol " + std::to_string(prior.constraint_id) + " " +
                           std::to_string(inversion_premise_id) + " + -1 +;");
              proof.expect("  qed;");
              ++explicit_goals;
            }
            proof.expect("qed;");
          }
          proof.expect("core id -1;");
          earlier[left].push_back({right, current_constraint_id});
          ++order_rows;
        }
      }
    }
    ordered.finish();
    proof.expect("output EQUISATISFIABLE FILE;");
    proof.expect("conclusion NONE;");
    proof.expect("end pseudo-Boolean proof;");
    proof.finish();
    if (order_rows != ORDER_ROWS || explicit_goals != 874)
      throw std::runtime_error("proof-count invariant failed");

    std::cout << "PASS independent_stream base_rows=" << BASE_ROWS << " order_rows=" << order_rows
              << " output_rows=" << OUTPUT_ROWS << "\n";
    std::cout << "PASS proof_structure substitutions=" << order_rows
              << " mappings_each=1722 explicit_cp_goals=" << explicit_goals << "\n";
    std::cout << "PASS selection_order cells=4 all_pairs=232\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAIL " << error.what() << "\n";
    return 1;
  }
}
