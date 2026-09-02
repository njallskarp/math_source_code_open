#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <optional>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr int n = 21;
constexpr std::uint32_t full = (std::uint32_t{1} << n) - 1;

struct G {
  int r{};
  int i{};
  auto operator<=>(const G &) const = default;
};

G operator+(G a, G b) { return {a.r + b.r, a.i + b.i}; }
G operator-(G a, G b) { return {a.r - b.r, a.i - b.i}; }
G operator*(G a, G b) {
  return {a.r * b.r - a.i * b.i, a.r * b.i + a.i * b.r};
}
G conj(G a) { return {a.r, -a.i}; }

struct Aggregate {
  G s;
  G h;
  auto operator<=>(const Aggregate &) const = default;
};

Aggregate operator+(Aggregate a, Aggregate b) {
  return {a.s + b.s, a.h + b.h};
}
Aggregate operator-(Aggregate a, Aggregate b) {
  return {a.s - b.s, a.h - b.h};
}

enum class Kind { quarter, equal, opposite };

struct State {
  G s;
  G h;
  Kind kind;
};

const std::array<G, 4> roots{{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}};

G divide_pi(G value) {
  assert(((value.r + value.i) & 1) == 0);
  return {(value.r + value.i) / 2, (value.i - value.r) / 2};
}

std::vector<State> make_states() {
  std::vector<State> states;
  for (G x : roots) {
    for (G y : roots) {
      G s = divide_pi(x - y);
      G h = divide_pi(x + y);
      int dot = x.r * y.r + x.i * y.i;
      Kind kind = dot == 0 ? Kind::quarter
                          : dot == 1 ? Kind::equal : Kind::opposite;
      states.push_back({s, h, kind});
    }
  }
  assert(states.size() == 16);
  return states;
}

const std::vector<State> states = make_states();

using Domain = std::map<Aggregate, std::vector<int>>;

struct DomainKey {
  int q{};
  int e{};
  int o{};
  auto operator<=>(const DomainKey &) const = default;
};

std::map<DomainKey, Domain> domain_cache;

Domain build_domain(int q, int e, int o) {
  Domain current;
  current[{G{0, 0}, G{0, 0}}] = {};
  const std::array<std::pair<Kind, int>, 3> stages{{
      {Kind::quarter, q}, {Kind::equal, e}, {Kind::opposite, o}}};
  for (const auto &[kind, count] : stages) {
    for (int repeat = 0; repeat < count; ++repeat) {
      Domain next;
      for (const auto &[aggregate, word] : current) {
        for (int index = 0; index < static_cast<int>(states.size()); ++index) {
          if (states[index].kind != kind) continue;
          Aggregate image = aggregate + Aggregate{states[index].s, states[index].h};
          if (!next.contains(image)) {
            auto extended = word;
            extended.push_back(index);
            next.emplace(image, std::move(extended));
          }
        }
      }
      current = std::move(next);
    }
  }
  return current;
}

const Domain &domain(int q, int e) {
  DomainKey key{q, e, 7 - q - e};
  auto [it, inserted] = domain_cache.try_emplace(key);
  if (inserted) it->second = build_domain(key.q, key.e, key.o);
  return it->second;
}

std::array<G, 3> paf3(const std::array<G, 3> &word) {
  std::array<G, 3> result{};
  for (int shift = 0; shift < 3; ++shift) {
    for (int j = 0; j < 3; ++j) {
      result[shift] = result[shift] + word[j] * conj(word[(j + shift) % 3]);
    }
  }
  return result;
}

// For a three-section word, exact total sum and the shift-zero energy determine
// the real part of the shift-one autocorrelation.  The shift-two coordinate is
// its conjugate.  Thus these five integers are a lossless feasibility key once
// the family sum target is fixed.  The packed form keeps the exact frontier
// compact enough to regenerate on an ordinary workstation.
struct Signature {
  int equal_total{};
  int s_energy{};
  int s_imaginary{};
  int h_energy{};
  int h_imaginary{};
};

struct FamilyWitness {
  std::array<int, 3> equal_counts{};
  std::array<Aggregate, 3> sections{};
};

std::uint64_t pack_signature(Signature value) {
  assert(0 <= value.equal_total && value.equal_total < 32);
  assert(0 <= value.s_energy && value.s_energy < 1024);
  assert(-512 <= value.s_imaginary && value.s_imaginary < 512);
  assert(0 <= value.h_energy && value.h_energy < 1024);
  assert(-512 <= value.h_imaginary && value.h_imaginary < 512);
  std::uint64_t result = static_cast<unsigned>(value.equal_total);
  result |= static_cast<std::uint64_t>(value.s_energy) << 5;
  result |= static_cast<std::uint64_t>(value.s_imaginary + 512) << 15;
  result |= static_cast<std::uint64_t>(value.h_energy) << 25;
  result |= static_cast<std::uint64_t>(value.h_imaginary + 512) << 35;
  return result;
}

Signature unpack_signature(std::uint64_t value) {
  return {static_cast<int>(value & 31),
          static_cast<int>((value >> 5) & 1023),
          static_cast<int>((value >> 15) & 1023) - 512,
          static_cast<int>((value >> 25) & 1023),
          static_cast<int>((value >> 35) & 1023) - 512};
}

std::uint64_t signature(int equal_total, const std::array<Aggregate, 3> &sections) {
  std::array<G, 3> s{}, h{};
  for (int r = 0; r < 3; ++r) {
    s[r] = sections[r].s;
    h[r] = sections[r].h;
  }
  auto ps = paf3(s);
  auto ph = paf3(h);
  assert(ps[0].i == 0 && ph[0].i == 0);
  return pack_signature({equal_total, ps[0].r, ps[1].i, ph[0].r, ph[1].i});
}

std::uint64_t pack_witness(const FamilyWitness &witness) {
  std::uint64_t result = 0;
  int shift = 0;
  for (int value : witness.equal_counts) {
    assert(0 <= value && value < 8);
    result |= static_cast<std::uint64_t>(value) << shift;
    shift += 3;
  }
  for (const Aggregate &aggregate : witness.sections) {
    for (int value : {aggregate.s.r, aggregate.s.i, aggregate.h.r, aggregate.h.i}) {
      assert(-7 <= value && value <= 7);
      result |= static_cast<std::uint64_t>(value + 7) << shift;
      shift += 4;
    }
  }
  return result;
}

FamilyWitness unpack_witness(std::uint64_t value) {
  FamilyWitness result;
  int shift = 0;
  for (int &entry : result.equal_counts) {
    entry = static_cast<int>((value >> shift) & 7);
    shift += 3;
  }
  for (Aggregate &aggregate : result.sections) {
    for (int *entry : {&aggregate.s.r, &aggregate.s.i, &aggregate.h.r, &aggregate.h.i}) {
      *entry = static_cast<int>((value >> shift) & 15) - 7;
      shift += 4;
    }
  }
  return result;
}

struct FamilyKey {
  std::array<int, 3> quarter_counts{};
  Aggregate target{};
  int equal_cap{};
  auto operator<=>(const FamilyKey &) const = default;
};

using Frontier = std::unordered_map<std::uint64_t, std::uint64_t>;
std::map<FamilyKey, Frontier> family_cache;

const Frontier &family_frontier(
    std::array<int, 3> quarter_counts, Aggregate target, int equal_cap) {
  FamilyKey key{quarter_counts, target, equal_cap};
  auto [cache_it, inserted] = family_cache.try_emplace(key);
  if (!inserted) return cache_it->second;
  auto &frontier = cache_it->second;

  for (int e0 = 0; e0 <= 7 - quarter_counts[0]; ++e0) {
    for (int e1 = 0; e1 <= 7 - quarter_counts[1]; ++e1) {
      for (int e2 = 0; e2 <= 7 - quarter_counts[2]; ++e2) {
        if (e0 + e1 + e2 > equal_cap) continue;
        const Domain &d0 = domain(quarter_counts[0], e0);
        const Domain &d1 = domain(quarter_counts[1], e1);
        const Domain &d2 = domain(quarter_counts[2], e2);
        for (const auto &[a0, ignored0] : d0) {
          (void)ignored0;
          for (const auto &[a1, ignored1] : d1) {
            (void)ignored1;
            Aggregate a2 = target - a0 - a1;
            if (!d2.contains(a2)) continue;
            std::array<Aggregate, 3> sections{a0, a1, a2};
            std::uint64_t sig = signature(e0 + e1 + e2, sections);
            Signature values = unpack_signature(sig);
            if (values.s_energy > 43 || values.h_energy > 29) continue;
            frontier.try_emplace(
                sig, pack_witness(FamilyWitness{{e0, e1, e2}, sections}));
          }
        }
      }
    }
  }
  return frontier;
}

std::uint32_t rotate(std::uint32_t mask, int shift) {
  return ((mask << shift) | (mask >> (n - shift))) & full;
}

std::uint32_t canonical(std::uint32_t mask) {
  std::uint32_t answer = mask;
  for (int shift = 1; shift < n; ++shift) answer = std::min(answer, rotate(mask, shift));
  return answer;
}

std::uint32_t parse_hex(const std::string &text) {
  return static_cast<std::uint32_t>(std::stoul(text, nullptr, 16));
}

std::vector<std::pair<std::uint32_t, std::uint32_t>> read_q5_supports(
    const std::string &path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open support manifest: " + path);
  std::string line;
  std::getline(input, line);
  std::vector<std::pair<std::uint32_t, std::uint32_t>> result;
  while (std::getline(input, line)) {
    std::istringstream row(line);
    std::string q_a, q_b, a, b, v_a, v_b;
    std::getline(row, q_a, '\t');
    std::getline(row, q_b, '\t');
    std::getline(row, a, '\t');
    std::getline(row, b, '\t');
    std::getline(row, v_a, '\t');
    std::getline(row, v_b, '\t');
    if ((std::stoi(q_a) & 1) == 0) result.emplace_back(parse_hex(a), parse_hex(b));
  }
  std::sort(result.begin(), result.end());
  assert(result.size() == 18);
  return result;
}

std::vector<std::pair<std::uint32_t, std::uint32_t>> read_q37_supports(
    const std::string &path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open support manifest: " + path);
  std::string line;
  std::getline(input, line);
  std::set<std::pair<std::uint32_t, std::uint32_t>> result;
  while (std::getline(input, line)) {
    std::istringstream row(line);
    std::string q_a, q_b, a, b, v_a, v_b;
    std::getline(row, q_a, '\t');
    std::getline(row, q_b, '\t');
    std::getline(row, a, '\t');
    std::getline(row, b, '\t');
    std::getline(row, v_a, '\t');
    std::getline(row, v_b, '\t');
    if ((std::stoi(q_a) & 1) == 1) {
      result.emplace(canonical(full ^ parse_hex(a)), canonical(full ^ parse_hex(b)));
    }
  }
  assert(result.size() == 18);
  return {result.begin(), result.end()};
}

std::array<int, 3> section_quarters(std::uint32_t mask) {
  std::array<int, 3> result{};
  for (int position = 0; position < n; ++position) {
    if ((mask >> position) & 1U) ++result[position % 3];
  }
  return result;
}

std::string build_word(std::uint32_t mask, const FamilyWitness &witness) {
  std::string word(n, '?');
  for (int residue = 0; residue < 3; ++residue) {
    std::vector<int> quarter_positions, other_positions;
    for (int position = residue; position < n; position += 3) {
      (((mask >> position) & 1U) ? quarter_positions : other_positions).push_back(position);
    }
    int e = witness.equal_counts[residue];
    const Domain &d = domain(static_cast<int>(quarter_positions.size()), e);
    const auto &indices = d.at(witness.sections[residue]);
    std::size_t cursor = 0;
    for (int position : quarter_positions) {
      int index = indices.at(cursor++);
      assert(states[index].kind == Kind::quarter);
      word[position] = "0123456789abcdef"[index];
    }
    for (int j = 0; j < static_cast<int>(other_positions.size()); ++j) {
      int index = indices.at(cursor++);
      assert(states[index].kind == (j < e ? Kind::equal : Kind::opposite));
      word[other_positions[j]] = "0123456789abcdef"[index];
    }
    assert(cursor == indices.size());
  }
  assert(word.find('?') == std::string::npos);
  return word;
}

std::string hex_mask(std::uint32_t mask) {
  std::ostringstream out;
  out << std::hex << std::setw(6) << std::setfill('0') << mask;
  return out.str();
}

std::optional<std::uint64_t> complement(std::uint64_t packed_left, int equal_total) {
  Signature left = unpack_signature(packed_left);
  Signature right{equal_total - left.equal_total,
                  43 - left.s_energy,
                  -left.s_imaginary,
                  29 - left.h_energy,
                  -left.h_imaginary};
  if (right.equal_total < 0 || right.s_energy < 0 || right.h_energy < 0 ||
      right.s_imaginary < -512 || right.s_imaginary >= 512 ||
      right.h_imaginary < -512 || right.h_imaginary >= 512) {
    return std::nullopt;
  }
  return pack_signature(right);
}

const std::array<std::array<int, 4>, 6> cases{{
    {1, 0, 5, 0}, {3, 0, 4, 1}, {3, 0, 3, -2},
    {3, 2, 3, 2}, {3, 2, 2, 3}, {4, 1, 2, -1}}};

Aggregate sum_target(int family, const std::array<int, 4> &c) {
  auto [p, q, x, y] = c;
  if (family == 0) return {G{p + q, q - p}, G{0, 0}};
  return {G{x + y - 1, y - x}, G{1, 0}};
}

}  // namespace

int main(int argc, char **argv) {
  if (argc != 3) {
    std::cerr << "usage: generate_order3_lifts SUPPORT_TSV OUTPUT_TSV\n";
    return 2;
  }
  auto q5 = read_q5_supports(argv[1]);
  auto q37 = read_q37_supports(argv[1]);
  std::ofstream output(argv[2]);
  if (!output) throw std::runtime_error("cannot open output manifest");
  output << "q\torbit\tcase\ta_mask_hex\tb_mask_hex\tstates_a\tstates_b\n";

  int rows = 0;
  for (int q_value : {5, 37}) {
    const auto &supports = q_value == 5 ? q5 : q37;
    int equal_total = (41 - q_value) / 2;
    for (int orbit = 0; orbit < static_cast<int>(supports.size()); ++orbit) {
      auto [a_mask, b_mask] = supports[orbit];
      auto q_a = section_quarters(a_mask);
      auto q_b = section_quarters(b_mask);
      for (int case_id = 0; case_id < static_cast<int>(cases.size()); ++case_id) {
        const auto &frontier_a =
            family_frontier(q_a, sum_target(0, cases[case_id]), equal_total);
        const auto &frontier_b =
            family_frontier(q_b, sum_target(1, cases[case_id]), equal_total);
        bool found = false;
        FamilyWitness witness_a, witness_b;
        for (const auto &[sig_a, packed_a] : frontier_a) {
          auto wanted = complement(sig_a, equal_total);
          if (!wanted) continue;
          auto it = frontier_b.find(*wanted);
          if (it != frontier_b.end()) {
            witness_a = unpack_witness(packed_a);
            witness_b = unpack_witness(it->second);
            found = true;
          }
          if (found) break;
        }
        if (!found) {
          std::cerr << "no quotient lift for q=" << q_value << " orbit=" << orbit
                    << " case=" << case_id << '\n';
          return 1;
        }
        output << q_value << '\t' << orbit << '\t' << case_id << '\t'
               << hex_mask(a_mask) << '\t' << hex_mask(b_mask) << '\t'
               << build_word(a_mask, witness_a) << '\t'
               << build_word(b_mask, witness_b) << '\n';
        ++rows;
      }
    }
  }
  assert(rows == 216);
  std::cout << "rows=216;q5_cells=108;q37_cells=108;"
               "exact_order3_coupled_quotient_lifts=216\n";
}
