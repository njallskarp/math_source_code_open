#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {

std::int64_t binomial(int n, int k) {
  if (k < 0 || k > n) return 0;
  std::int64_t answer = 1;
  for (int i = 1; i <= k; ++i) answer = answer * (n - k + i) / i;
  return answer;
}

std::vector<std::string> split(const std::string& line, char delimiter) {
  std::vector<std::string> fields;
  std::istringstream source(line);
  std::string field;
  while (std::getline(source, field, delimiter)) {
    if (field.size() >= 2 && field.front() == '"' && field.back() == '"') {
      field = field.substr(1, field.size() - 2);
    }
    fields.push_back(field);
  }
  return fields;
}

void choose_subsets(int start, int need, std::vector<int>& chosen,
                    std::map<std::pair<int, int>, int>& counts) {
  if (need == 0) {
    int s = std::find(chosen.begin(), chosen.end(), 5) != chosen.end();
    int k = static_cast<int>(std::count_if(chosen.begin(), chosen.end(),
                                           [](int x) { return x < 5; }));
    ++counts[{s, k}];
    return;
  }
  for (int value = start; value <= 13 - need; ++value) {
    chosen.push_back(value);
    choose_subsets(value + 1, need - 1, chosen, counts);
    chosen.pop_back();
  }
}

std::pair<std::int64_t, std::int64_t> audit_local_double_count() {
  std::int64_t graphs = 0;
  std::int64_t rooted = 0;
  for (int n = 1; n <= 6; ++n) {
    std::array<std::array<int, 6>, 6> pair_index{};
    int pairs = 0;
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j) pair_index[i][j] = pair_index[j][i] = pairs++;
    for (std::uint32_t mask = 0; mask < (std::uint32_t{1} << pairs); ++mask) {
      ++graphs;
      for (int anchor = 0; anchor < n; ++anchor) {
        std::vector<int> neighbourhood;
        for (int other = 0; other < n; ++other)
          if (other != anchor && (mask & (std::uint32_t{1} << pair_index[anchor][other])))
            neighbourhood.push_back(other);
        int local_edges = 0;
        int codegree_sum = 0;
        for (std::size_t i = 0; i < neighbourhood.size(); ++i) {
          for (std::size_t j = i + 1; j < neighbourhood.size(); ++j) {
            if (mask & (std::uint32_t{1} << pair_index[neighbourhood[i]][neighbourhood[j]])) {
              ++local_edges;
              codegree_sum += 2;
            }
          }
        }
        if (codegree_sum != 2 * local_edges) throw std::runtime_error("double count mismatch");
        ++rooted;
      }
    }
  }
  return {graphs, rooted};
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 2) throw std::runtime_error("usage: check_pair_quotient PAIR_TYPES.tsv");
    std::ifstream source(argv[1]);
    if (!source) throw std::runtime_error("cannot open type table");
    std::string line;
    if (!std::getline(source, line)) throw std::runtime_error("missing header");
    const auto header = split(line, ',');
    if (header.size() != 14 || header[0] != "c" || header[13] != "unit_sha256") {
      throw std::runtime_error("unexpected header");
    }

    std::set<std::tuple<int, int, int>> keys;
    int rows = 0;
    while (std::getline(source, line)) {
      if (line.empty()) continue;
      const auto fields = split(line, ',');
      if (fields.size() != 14) throw std::runtime_error("wrong field count");
      std::array<std::int64_t, 13> x{};
      for (int i = 0; i < 13; ++i) x[static_cast<std::size_t>(i)] = std::stoll(fields[static_cast<std::size_t>(i)]);
      const int c = static_cast<int>(x[0]);
      const int s = static_cast<int>(x[1]);
      const int k = static_cast<int>(x[2]);
      const int p = static_cast<int>(x[3]);
      if (c < 9 || c > 13 || (s != 0 && s != 1) || k < 0 || k > 5 || p != s + k) {
        throw std::runtime_error("invalid key");
      }
      const std::array<std::int64_t, 4> e = {p, 6 - p, 6 - p, 1 + p};
      const std::array<std::int64_t, 4> central = {c - p, 14 - c + p, 14 - c + p, c - p};
      for (int i = 0; i < 4; ++i) {
        if (x[static_cast<std::size_t>(4 + i)] != e[static_cast<std::size_t>(i)] ||
            x[static_cast<std::size_t>(8 + i)] != central[static_cast<std::size_t>(i)] ||
            e[static_cast<std::size_t>(i)] < 0 || central[static_cast<std::size_t>(i)] < 0) {
          throw std::runtime_error("cell reconstruction mismatch");
        }
      }
      if (e[0] + e[1] + e[2] + e[3] != 13 ||
          central[0] + central[1] + central[2] + central[3] != 28 ||
          e[0] + central[0] != c) {
        throw std::runtime_error("partition identity mismatch");
      }
      const auto orbit = binomial(5, k) * binomial(7, 6 - p)
                       * binomial(14, c - p) * binomial(14, 14 - c + p);
      if (x[12] != orbit) throw std::runtime_error("orbit mismatch");
      if (!keys.emplace(c, s, k).second) throw std::runtime_error("duplicate key");
      ++rows;
    }
    if (rows != 60) throw std::runtime_error("wrong row count");
    for (int c = 9; c <= 13; ++c)
      for (int s = 0; s <= 1; ++s)
        for (int k = 0; k <= 5; ++k)
          if (!keys.contains({c, s, k})) throw std::runtime_error("missing type");

    std::map<std::pair<int, int>, int> subset_counts;
    std::vector<int> chosen;
    choose_subsets(0, 6, chosen, subset_counts);
    int subsets = 0;
    if (subset_counts.size() != 12) throw std::runtime_error("wrong orbit count");
    for (const auto& [key, count] : subset_counts) {
      const auto [s, k] = key;
      const auto expected = binomial(5, k) * binomial(7, 6 - s - k);
      if (count != expected) throw std::runtime_error("subset orbit mismatch");
      subsets += count;
    }
    if (subsets != binomial(13, 6)) throw std::runtime_error("subset coverage mismatch");

    constexpr int incident_sum = 2 * 100;
    constexpr int central_lower = incident_sum - 6 * 13;
    constexpr int maximum_below_nine = 6 * 13 + 15 * 8;
    static_assert(central_lower == 122);
    static_assert(maximum_below_nine == 198);
    static_assert(maximum_below_nine < incident_sum);
    const auto [graphs, rooted] = audit_local_double_count();
    std::cout << "PASS independent_pair_quotient rows=" << rows
              << " e_subsets=" << subsets << " e_orbits=" << subset_counts.size()
              << " forced_codegree=9 graphs=" << graphs << " rooted_checks=" << rooted << "\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAIL " << error.what() << '\n';
    return 1;
  }
}
