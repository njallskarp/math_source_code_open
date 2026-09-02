#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int n = 21;
constexpr std::uint32_t full = (1U << n) - 1;
using U64 = std::uint64_t;

struct Gaussian {
  int real;
  int imag;
};

Gaussian operator+(Gaussian x, Gaussian y) {
  return {x.real + y.real, x.imag + y.imag};
}
Gaussian operator-(Gaussian x, Gaussian y) {
  return {x.real - y.real, x.imag - y.imag};
}
Gaussian operator*(Gaussian x, Gaussian y) {
  return {x.real * y.real - x.imag * y.imag,
          x.real * y.imag + x.imag * y.real};
}
Gaussian conjugate(Gaussian x) { return {x.real, -x.imag}; }

Gaussian divide_pi(Gaussian x) {
  assert(((x.real + x.imag) & 1) == 0);
  return {(x.real + x.imag) / 2, (x.imag - x.real) / 2};
}

int mod_pi(Gaussian x) { return (x.real + x.imag) & 1; }

struct Variable {
  int family;
  int position;
  bool axis;
};

std::vector<Variable> layout(std::uint32_t a, std::uint32_t b) {
  std::vector<Variable> result;
  for (int family = 0; family < 2; ++family) {
    const auto mask = family == 0 ? a : b;
    for (int position = 0; position < n; ++position) {
      if ((mask >> position) & 1U) result.push_back({family, position, true});
    }
  }
  for (int family = 0; family < 2; ++family) {
    const auto mask = family == 0 ? a : b;
    for (int position = 0; position < n; ++position) {
      if (!((mask >> position) & 1U)) result.push_back({family, position, false});
    }
  }
  assert(result.size() == 42);
  return result;
}

Gaussian target(int component, int shift) {
  if (component == 1) return {-2, 0};
  if (shift == 4) return {-2, 0};
  if (shift == 10) return {2, 0};
  return {0, 0};
}

std::uint32_t residue(std::uint32_t a, std::uint32_t b, U64 assignment) {
  const auto variables = layout(a, b);
  std::array<std::array<std::array<Gaussian, n>, 2>, 2> words{};
  for (int family = 0; family < 2; ++family) {
    const auto qmask = family == 0 ? a : b;
    for (int position = 0; position < n; ++position) {
      const auto iterator = std::find_if(
          variables.begin(), variables.end(), [=](const Variable &variable) {
            return variable.family == family && variable.position == position;
          });
      assert(iterator != variables.end());
      const int slot = static_cast<int>(iterator - variables.begin());
      const bool bit = (assignment >> slot) & 1ULL;
      if ((qmask >> position) & 1U) {
        words[family][0][position] = bit ? Gaussian{0, 1} : Gaussian{1, 0};
        words[family][1][position] = bit ? Gaussian{1, 0} : Gaussian{0, 1};
      } else if (bit) {
        words[family][0][position] = {1, -1};
        words[family][1][position] = {0, 0};
      } else {
        words[family][0][position] = {0, 0};
        words[family][1][position] = {1, -1};
      }
    }
  }

  std::uint32_t result = 0;
  for (int component = 0; component < 2; ++component) {
    for (int shift = 1; shift <= 10; ++shift) {
      Gaussian total{0, 0};
      for (int family = 0; family < 2; ++family) {
        for (int position = 0; position < n; ++position) {
          total = total + words[family][component][position] *
                              conjugate(words[family][component]
                                             [(position + shift) % n]);
        }
      }
      const auto quotient = divide_pi(total - target(component, shift));
      result |= static_cast<std::uint32_t>(mod_pi(quotient))
                << (component * 10 + shift - 1);
    }
  }
  return result;
}

struct Affine {
  std::uint32_t base;
  std::vector<std::uint32_t> columns;
  std::vector<Variable> variables;
  int quarter_count;
};

Affine affine(std::uint32_t a, std::uint32_t b) {
  Affine result;
  result.variables = layout(a, b);
  result.quarter_count = std::popcount(a) + std::popcount(b);
  result.base = residue(a, b, 0);
  for (int index = 0; index < 42; ++index) {
    result.columns.push_back(residue(a, b, 1ULL << index) ^ result.base);
  }
  for (int left = 0; left < 42; ++left) {
    for (int right = left + 1; right < 42; ++right) {
      assert(residue(a, b, (1ULL << left) | (1ULL << right)) ==
             (result.base ^ result.columns[left] ^ result.columns[right]));
    }
  }
  return result;
}

int rank(const std::vector<std::uint32_t> &columns) {
  std::array<std::uint32_t, 20> basis{};
  int answer = 0;
  for (auto value : columns) {
    while (value) {
      const int pivot = 31 - std::countl_zero(value);
      if (basis[pivot]) value ^= basis[pivot];
      else {
        basis[pivot] = value;
        ++answer;
        break;
      }
    }
  }
  return answer;
}

using Distribution = std::map<std::pair<int, std::uint32_t>, U64>;

Distribution distribution(const std::vector<std::uint32_t> &columns) {
  Distribution current{{{0, 0}, 1}};
  for (const auto column : columns) {
    auto next = current;
    for (const auto &[key, count] : current) {
      next[{key.first + 1, key.second ^ column}] += count;
    }
    current.swap(next);
  }
  return current;
}

bool signed_sum(int terms, int wanted) {
  return std::abs(wanted) <= terms && ((wanted - terms) & 1) == 0;
}

using Case = std::array<int, 4>;
constexpr std::array<Case, 6> cases{{
    {1, 0, 5, 0}, {3, 0, 4, 1}, {3, 0, 3, -2},
    {3, 2, 3, 2}, {3, 2, 2, 3}, {4, 1, 2, -1},
}};

bool sums_feasible(int qa, int qb, int oa, int ob, int beta_a, int beta_b,
                   Case value) {
  const int za = n - qa - oa;
  const int zb = n - qb - ob;
  if (std::min({oa, ob, za, zb}) < 0) return false;
  const auto [p, q, x, y] = value;
  const std::array<std::array<int, 5>, 4> tests{{
      {oa, qa - beta_a, beta_a, p + q, q - p},
      {za, beta_a, qa - beta_a, 0, 0},
      {ob, qb - beta_b, beta_b, x + y - 1, y - x},
      {zb, beta_b, qb - beta_b, 1, 0},
  }};
  for (const auto &test : tests) {
    if (!signed_sum(test[0] + test[1], test[3]) ||
        !signed_sum(test[0] + test[2], test[4])) return false;
  }
  return true;
}

U64 lookup(const Distribution &values, int weight, std::uint32_t syndrome) {
  const auto iterator = values.find({weight, syndrome});
  return iterator == values.end() ? 0 : iterator->second;
}

struct Counts {
  U64 all = 0;
  std::array<U64, 6> cases{};
};

Counts count_q5(const Affine &system) {
  assert(system.quarter_count == 5);
  std::vector<std::uint32_t> a_types, b_types;
  for (int index = 5; index < 42; ++index) {
    (system.variables[index].family == 0 ? a_types : b_types)
        .push_back(system.columns[index]);
  }
  const auto a_dist = distribution(a_types);
  const auto b_dist = distribution(b_types);
  const int qa = std::count_if(system.variables.begin(), system.variables.begin() + 5,
                               [](Variable v) { return v.family == 0; });
  const int qb = 5 - qa;
  Counts result;
  for (int mask = 0; mask < 32; ++mask) {
    std::uint32_t syndrome = 0;
    int beta_a = 0, beta_b = 0;
    for (int index = 0; index < 5; ++index) {
      if ((mask >> index) & 1) {
        syndrome ^= system.columns[index];
        (system.variables[index].family == 0 ? beta_a : beta_b)++;
      }
    }
    const auto wanted = system.base ^ syndrome;
    for (const auto &[key, multiplicity] : a_dist) {
      const int oa = key.first;
      const int ob = 19 - oa;
      const U64 matching = lookup(b_dist, ob, wanted ^ key.second);
      result.all += multiplicity * matching;
      for (int case_id = 0; case_id < 6; ++case_id) {
        if (sums_feasible(qa, qb, oa, ob, beta_a, beta_b, cases[case_id]))
          result.cases[case_id] += multiplicity * matching;
      }
    }
  }
  return result;
}

Counts count_q37(const Affine &system) {
  assert(system.quarter_count == 37);
  std::vector<std::uint32_t> a_axes, b_axes;
  for (int index = 0; index < 37; ++index) {
    (system.variables[index].family == 0 ? a_axes : b_axes)
        .push_back(system.columns[index]);
  }
  const auto a_dist = distribution(a_axes);
  const auto b_dist = distribution(b_axes);
  const int qa = static_cast<int>(a_axes.size());
  const int qb = static_cast<int>(b_axes.size());
  Counts result;
  for (int mask = 0; mask < 32; ++mask) {
    if (std::popcount(static_cast<unsigned>(mask)) != 3) continue;
    std::uint32_t type_syndrome = 0;
    int oa = 0;
    for (int index = 0; index < 5; ++index) {
      if ((mask >> index) & 1) {
        type_syndrome ^= system.columns[37 + index];
        oa += system.variables[37 + index].family == 0;
      }
    }
    const int ob = 3 - oa;
    const auto wanted = system.base ^ type_syndrome;
    for (const auto &[a_key, a_count] : a_dist) {
      const auto matching = wanted ^ a_key.second;
      for (int beta_b = 0; beta_b <= qb; ++beta_b) {
        const U64 b_count = lookup(b_dist, beta_b, matching);
        const U64 product = a_count * b_count;
        result.all += product;
        for (int case_id = 0; case_id < 6; ++case_id)
          if (sums_feasible(qa, qb, oa, ob, a_key.first, beta_b,
                            cases[case_id])) result.cases[case_id] += product;
      }
    }
  }
  return result;
}

std::uint32_t rotate(std::uint32_t mask, int shift) {
  return ((mask << shift) | (mask >> (n - shift))) & full;
}

std::uint32_t canonical(std::uint32_t mask) {
  auto answer = mask;
  for (int shift = 1; shift < n; ++shift) answer = std::min(answer, rotate(mask, shift));
  return answer;
}

std::pair<std::vector<std::pair<std::uint32_t, std::uint32_t>>,
          std::vector<std::pair<std::uint32_t, std::uint32_t>>>
read_branches(const std::string &path) {
  std::ifstream input(path);
  assert(input);
  std::string line;
  std::getline(input, line);
  std::vector<std::pair<std::uint32_t, std::uint32_t>> q5;
  std::set<std::pair<std::uint32_t, std::uint32_t>> q37;
  while (std::getline(input, line)) {
    std::stringstream row(line);
    std::string qa, qb, a, b, va, vb;
    std::getline(row, qa, '\t'); std::getline(row, qb, '\t');
    std::getline(row, a, '\t'); std::getline(row, b, '\t');
    std::getline(row, va, '\t'); std::getline(row, vb, '\t');
    const auto a_mask = static_cast<std::uint32_t>(std::stoul(a, nullptr, 16));
    const auto b_mask = static_cast<std::uint32_t>(std::stoul(b, nullptr, 16));
    if ((std::stoi(qa) & 1) == 0) q5.emplace_back(a_mask, b_mask);
    else q37.emplace(canonical(full ^ a_mask), canonical(full ^ b_mask));
  }
  std::sort(q5.begin(), q5.end());
  assert(q5.size() == 18 && q37.size() == 18);
  return {q5, {q37.begin(), q37.end()}};
}

}  // namespace

int main(int argc, char **argv) {
  assert(argc == 2);
  const auto [q5, q37] = read_branches(argv[1]);

  const std::array<U64, 2> expected_all{9998086928ULL, 22280142848ULL};
  const std::array<std::array<U64, 6>, 2> expected_cases{{
      {4998889150ULL, 4999037012ULL, 4998893762ULL, 4998982000ULL,
       4998982000ULL, 4998988120ULL},
      {11127703552ULL, 11137966104ULL, 11129476680ULL, 11127112942ULL,
       11127112942ULL, 11128782484ULL},
  }};

  for (int branch = 0; branch < 2; ++branch) {
    const auto &supports = branch == 0 ? q5 : q37;
    Counts total;
    for (const auto &[a, b] : supports) {
      const auto system = affine(a, b);
      assert(rank(system.columns) == 10);
      const auto local = branch == 0 ? count_q5(system) : count_q37(system);
      assert(local.all > 0);
      for (const auto value : local.cases) assert(value > 0);
      total.all += local.all;
      for (int index = 0; index < 6; ++index) total.cases[index] += local.cases[index];
    }
    assert(total.all == expected_all[branch]);
    assert(total.cases == expected_cases[branch]);
    std::cout << "q=" << (branch == 0 ? 5 : 37) << ";orbits=18;rank=10;all="
              << total.all << ";cases=";
    for (int index = 0; index < 6; ++index)
      std::cout << (index ? "," : "") << total.cases[index];
    std::cout << '\n';
  }
  std::cout << "independent_certificate=verified\n";
}
