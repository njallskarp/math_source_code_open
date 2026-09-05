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

constexpr int kN = 43;
constexpr int kBaseVariables = 13244;
constexpr int kInputRows = 1974963;
constexpr int kUFirst = kBaseVariables + 1;
constexpr int kWFirst = kUFirst + kN;
constexpr int kQ = kWFirst + kN;
constexpr int kYFirst = kQ + 1;
constexpr int kAddedRows = 638;
constexpr int kProofLines = 1281;

using Coefficients = std::map<int, int>;
using Literal = std::pair<int, bool>;  // variable, positive

const std::array<std::vector<int>, 4> kCells = {
    std::vector<int>{0, 1, 2, 3, 4, 5},
    std::vector<int>{6, 7, 8, 9, 10, 11, 12},
    std::vector<int>{14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28},
    std::vector<int>{29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42},
};

int edge_id(int i, int j) {
    if (i > j) std::swap(i, j);
    if (!(0 <= i && i < j && j < kN)) throw std::runtime_error("invalid edge");
    return i * (2 * kN - i - 1) / 2 + (j - i - 1) + 1;
}

int u_id(int v) { return kUFirst + v; }
int w_id(int v) { return kWFirst + v; }
int y_id(int p) { return kYFirst + p; }

Coefficients a_coefficients(int vertex, int sign = 1) {
    Coefficients result;
    for (int other = 0; other < 13; ++other) {
        if (other != vertex) result[edge_id(vertex, other)] = sign;
    }
    return result;
}

void add_coefficients(Coefficients& destination, const Coefficients& source) {
    for (const auto& [variable, coefficient] : source) {
        destination[variable] += coefficient;
        if (destination[variable] == 0) destination.erase(variable);
    }
}

std::string signed_row(const Coefficients& coefficients, int rhs) {
    std::ostringstream out;
    bool first = true;
    for (const auto& [variable, coefficient] : coefficients) {
        if (coefficient == 0) continue;
        if (!first) out << ' ';
        if (coefficient > 0) out << '+';
        out << coefficient << " x" << variable;
        first = false;
    }
    if (first) throw std::runtime_error("empty row");
    out << " >= " << rhs << " ;";
    return out.str();
}

std::string literal_row(const std::vector<Literal>& literals) {
    std::ostringstream out;
    for (std::size_t i = 0; i < literals.size(); ++i) {
        if (i != 0) out << ' ';
        out << "+1 " << (literals[i].second ? "x" : "~x") << literals[i].first;
    }
    out << " >= 1 ;";
    return out.str();
}

std::string a_row(int vertex, const Coefficients& extra, int rhs, int sign = 1) {
    Coefficients coefficients = a_coefficients(vertex, sign);
    add_coefficients(coefficients, extra);
    return signed_row(coefficients, rhs);
}

std::vector<std::pair<int, int>> adjacent_pairs() {
    std::vector<std::pair<int, int>> result;
    for (const auto& cell : kCells) {
        for (std::size_t i = 0; i + 1 < cell.size(); ++i) {
            result.emplace_back(cell[i], cell[i + 1]);
        }
    }
    if (result.size() != 38) throw std::runtime_error("adjacent pair count");
    return result;
}

struct Pattern {
    std::string name;
    std::vector<Literal> condition;
};

std::vector<Pattern> patterns() {
    std::vector<Pattern> result;
    for (int class_index = 0; class_index < 2; ++class_index) {
        const bool q_positive = class_index == 0;
        const auto& left = kCells[2 * class_index];
        const auto& right = kCells[2 * class_index + 1];
        const std::string prefix = class_index == 0 ? "E" : "C";
        const Literal q_literal{kQ, q_positive};
        result.push_back({prefix + "_left_8", {q_literal, {w_id(left.back()), true}}});
        result.push_back({prefix + "_right_8", {q_literal, {w_id(right.back()), true}}});
        result.push_back({prefix + "_left_7_7", {q_literal, {u_id(left[left.size() - 2]), true}}});
        result.push_back({prefix + "_split_7_7",
                          {q_literal, {u_id(left.back()), true}, {u_id(right.back()), true}}});
        result.push_back({prefix + "_right_7_7", {q_literal, {u_id(right[right.size() - 2]), true}}});
    }
    return result;
}

std::vector<std::string> expected_added_rows() {
    std::vector<std::string> rows;
    Coefficients sum_a;
    for (int v = 0; v < kN; ++v) add_coefficients(sum_a, a_coefficients(v));
    rows.push_back(signed_row(sum_a, 260));
    Coefficients minus_sum_a;
    for (const auto& [variable, coefficient] : sum_a) minus_sum_a[variable] = -coefficient;
    rows.push_back(signed_row(minus_sum_a, -260));

    for (int v = 0; v < kN; ++v) rows.push_back(a_row(v, {}, -8, -1));

    for (const auto& [left, right] : adjacent_pairs()) {
        Coefficients coefficients = a_coefficients(right);
        add_coefficients(coefficients, a_coefficients(left, -1));
        rows.push_back(signed_row(coefficients, 0));
    }

    for (int v = 0; v < kN; ++v) {
        const int maximum = v < 13 ? 12 : 13;
        rows.push_back(a_row(v, {{u_id(v), -7}}, 0));
        rows.push_back(a_row(v, {{u_id(v), maximum - 6}}, -6, -1));
        rows.push_back(a_row(v, {{w_id(v), -8}}, 0));
        rows.push_back(a_row(v, {{w_id(v), maximum - 7}}, -7, -1));
    }

    for (int v = 0; v < kN; ++v) {
        rows.push_back(a_row(v, {{u_id(v), -1}}, 6));
        rows.push_back(a_row(v, {{w_id(v), 1}}, -7, -1));
        rows.push_back(literal_row({{w_id(v), false}, {u_id(v), true}}));
        rows.push_back(a_row(v, {{u_id(v), -1}, {w_id(v), -1}}, 6));
        rows.push_back(a_row(v, {{u_id(v), 1}, {w_id(v), 1}}, -6, -1));
    }

    for (const auto& [left, right] : adjacent_pairs()) {
        rows.push_back(literal_row({{u_id(left), false}, {u_id(right), true}}));
        rows.push_back(literal_row({{w_id(left), false}, {w_id(right), true}}));
    }

    Coefficients thresholds;
    for (int v = 0; v < kN; ++v) {
        thresholds[u_id(v)] = 1;
        thresholds[w_id(v)] = 1;
    }
    rows.push_back(signed_row(thresholds, 2));
    Coefficients minus_thresholds;
    for (const auto& [variable, coefficient] : thresholds) minus_thresholds[variable] = -coefficient;
    rows.push_back(signed_row(minus_thresholds, -2));

    Coefficients incidence;
    for (int i = 0; i < 13; ++i) {
        for (int j = i + 1; j < 13; ++j) incidence[edge_id(i, j)] = 2;
        incidence[u_id(i)] = -1;
        incidence[w_id(i)] = -1;
    }
    rows.push_back(signed_row(incidence, 78));
    Coefficients minus_incidence;
    for (const auto& [variable, coefficient] : incidence) minus_incidence[variable] = -coefficient;
    rows.push_back(signed_row(minus_incidence, -78));

    const int left_tail = u_id(kCells[0].back());
    const int right_tail = u_id(kCells[1].back());
    rows.push_back(literal_row({{kQ, false}, {left_tail, true}, {right_tail, true}}));
    rows.push_back(literal_row({{left_tail, false}, {kQ, true}}));
    rows.push_back(literal_row({{right_tail, false}, {kQ, true}}));

    const auto all_patterns = patterns();
    for (int p = 0; p < 10; ++p) {
        std::vector<Literal> antecedents;
        if (p < 9) {
            antecedents = all_patterns[static_cast<std::size_t>(p)].condition;
            for (int earlier = 0; earlier < p; ++earlier) {
                antecedents.emplace_back(y_id(earlier), false);
            }
        } else {
            for (int earlier = 0; earlier < p; ++earlier) {
                antecedents.emplace_back(y_id(earlier), false);
            }
        }
        for (const auto& literal : antecedents) {
            rows.push_back(literal_row({{y_id(p), false}, literal}));
        }
        std::vector<Literal> reverse{{y_id(p), true}};
        for (const auto& [variable, positive] : antecedents) {
            reverse.emplace_back(variable, !positive);
        }
        rows.push_back(literal_row(reverse));
    }

    for (int final_index = 1; final_index < 10; ++final_index) {
        Coefficients prefix;
        for (int p = 0; p <= final_index; ++p) prefix[y_id(p)] = -1;
        rows.push_back(signed_row(prefix, -1));
    }
    Coefficients at_least_one;
    for (int p = 0; p < 10; ++p) at_least_one[y_id(p)] = 1;
    rows.push_back(signed_row(at_least_one, 1));

    if (rows.size() != kAddedRows) throw std::runtime_error("added row count");
    return rows;
}

bool literal_value(const Literal& literal, const std::array<int, kN>& u,
                   const std::array<int, kN>& w, bool q) {
    bool value = false;
    if (literal.first == kQ) {
        value = q;
    } else if (kUFirst <= literal.first && literal.first < kUFirst + kN) {
        value = u[static_cast<std::size_t>(literal.first - kUFirst)] != 0;
    } else if (kWFirst <= literal.first && literal.first < kWFirst + kN) {
        value = w[static_cast<std::size_t>(literal.first - kWFirst)] != 0;
    } else {
        throw std::runtime_error("unexpected abstract literal");
    }
    return literal.second ? value : !value;
}

void audit_abstract_cover() {
    std::array<int, 10> pattern_counts{};
    int valid_states = 0;
    const auto all_patterns = patterns();
    for (int first = 0; first < kN; ++first) {
        for (int second = first; second < kN; ++second) {
            std::array<int, kN> a{};
            a.fill(6);
            ++a[static_cast<std::size_t>(first)];
            ++a[static_cast<std::size_t>(second)];
            if (a[13] != 6) continue;
            int exceptional_sum = 0;
            for (int v = 0; v < 13; ++v) exceptional_sum += a[static_cast<std::size_t>(v)];
            if (exceptional_sum % 2 != 0) continue;
            bool ordered = true;
            for (const auto& cell : kCells) {
                for (std::size_t i = 0; i + 1 < cell.size(); ++i) {
                    if (a[static_cast<std::size_t>(cell[i])] >
                        a[static_cast<std::size_t>(cell[i + 1])]) {
                        ordered = false;
                    }
                }
            }
            if (!ordered) continue;

            std::array<int, kN> u{};
            std::array<int, kN> w{};
            for (int v = 0; v < kN; ++v) {
                u[static_cast<std::size_t>(v)] = a[static_cast<std::size_t>(v)] >= 7;
                w[static_cast<std::size_t>(v)] = a[static_cast<std::size_t>(v)] >= 8;
                if (a[static_cast<std::size_t>(v)] !=
                    6 + u[static_cast<std::size_t>(v)] + w[static_cast<std::size_t>(v)]) {
                    throw std::runtime_error("threshold identity");
                }
            }
            const bool q = u[5] != 0 || u[12] != 0;
            const int exceptional_edges = exceptional_sum / 2;
            if (exceptional_edges != 39 + static_cast<int>(q)) {
                throw std::runtime_error("q/e(E) mismatch");
            }
            int matches = 0;
            int matching_pattern = -1;
            for (int p = 0; p < 10; ++p) {
                bool match = true;
                for (const auto& literal : all_patterns[static_cast<std::size_t>(p)].condition) {
                    match = match && literal_value(literal, u, w, q);
                }
                if (match) {
                    ++matches;
                    matching_pattern = p;
                }
            }
            if (matches != 1) throw std::runtime_error("pattern cover is not exact");
            ++pattern_counts[static_cast<std::size_t>(matching_pattern)];
            ++valid_states;
        }
    }
    if (valid_states != 10) throw std::runtime_error("abstract state count");
    for (int count : pattern_counts) {
        if (count != 1) throw std::runtime_error("pattern multiplicity");
    }
    std::cout << "PASS abstract_cover candidate_placements=946 valid_ordered_states="
              << valid_states << " patterns=10 multiplicity=1\n";
}

void check_streams(const std::string& input_path, const std::string& output_path,
                   const std::string& proof_path) {
    std::ifstream input(input_path);
    std::ifstream output(output_path);
    std::ifstream proof(proof_path);
    if (!input || !output || !proof) throw std::runtime_error("cannot open input stream");

    const std::string input_header =
        "* #variable= 13244 #constraint= 1974963 #equal= 128 intsize= 64";
    const std::string output_header =
        "* #variable= 13341 #constraint= 1975601 #equal= 128 intsize= 64";
    std::string input_line;
    std::string output_line;
    if (!std::getline(input, input_line) || input_line != input_header) {
        throw std::runtime_error("input header mismatch");
    }
    if (!std::getline(output, output_line) || output_line != output_header) {
        throw std::runtime_error("output header mismatch");
    }
    for (int row = 0; row < kInputRows; ++row) {
        if (!std::getline(input, input_line) || !std::getline(output, output_line)) {
            throw std::runtime_error("premature formula EOF");
        }
        if (input_line != output_line) {
            throw std::runtime_error("copied input row mismatch at " + std::to_string(row + 1));
        }
    }
    if (std::getline(input, input_line)) throw std::runtime_error("extra input row");

    const auto expected = expected_added_rows();
    for (std::size_t index = 0; index < expected.size(); ++index) {
        if (!std::getline(output, output_line)) throw std::runtime_error("missing appended row");
        if (output_line != expected[index]) {
            throw std::runtime_error("appended row mismatch at index " + std::to_string(index));
        }
    }
    if (std::getline(output, output_line)) throw std::runtime_error("extra output row");

    int proof_lines = 0;
    int red_lines = 0;
    int rup_lines = 0;
    int pol_lines = 0;
    int core_lines = 0;
    std::string first_proof_line;
    std::string last_proof_line;
    while (std::getline(proof, input_line)) {
        ++proof_lines;
        if (proof_lines == 1) first_proof_line = input_line;
        last_proof_line = input_line;
        if (input_line.rfind("red ", 0) == 0) ++red_lines;
        if (input_line.rfind("rup ", 0) == 0) ++rup_lines;
        if (input_line.rfind("pol ", 0) == 0) ++pol_lines;
        if (input_line.rfind("core ", 0) == 0) ++core_lines;
    }
    if (proof_lines != kProofLines || red_lines != 465 || rup_lines != 1 ||
        pol_lines != 172 || core_lines != kAddedRows) {
        throw std::runtime_error("proof command census mismatch");
    }
    if (first_proof_line != "pseudo-Boolean proof version 3.0" ||
        last_proof_line != "end pseudo-Boolean proof;") {
        throw std::runtime_error("proof boundary mismatch");
    }
    std::cout << "PASS streams copied_rows=" << kInputRows
              << " appended_rows=" << expected.size() << " proof_lines=" << proof_lines
              << " red/rup/pol=" << red_lines << '/' << rup_lines << '/' << pol_lines << "\n";
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 4) {
            std::cerr << "usage: check_partition ORDERED.opb PARTITION.opb PROOF.pbp\n";
            return 2;
        }
        check_streams(argv[1], argv[2], argv[3]);
        audit_abstract_cover();
        std::cout << "PASS independent_partition_check\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL " << error.what() << '\n';
        return 1;
    }
}
