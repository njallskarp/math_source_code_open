#include <algorithm>
#include <array>
#include <bit>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <tuple>
#include <vector>

namespace {

constexpr int n = 13;
constexpr int full = (1 << n) - 1;
constexpr std::array<int, 28> marked = {
    1, 1, 1, 1, 1, 1, 0,
    1, 1, 1, 1, 1, 1, 0,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};

bool core_edge(int i, int j) {
  int d = (i - j + n) % n;
  return d == 1 || d == 5 || d == 8 || d == 12;
}

std::array<bool, 1 << n> make_has_edge() {
  std::array<bool, 1 << n> answer{};
  for (int mask = 0; mask <= full; ++mask) {
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        if ((mask & (1 << i)) && (mask & (1 << j)) && core_edge(i, j)) {
          answer[mask] = true;
        }
      }
    }
  }
  return answer;
}

std::array<bool, 1 << n> make_has_independent_triple() {
  std::array<bool, 1 << n> answer{};
  for (int mask = 0; mask <= full; ++mask) {
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        for (int k = j + 1; k < n; ++k) {
          if ((mask & (1 << i)) && (mask & (1 << j)) && (mask & (1 << k)) &&
              !core_edge(i, j) && !core_edge(i, k) && !core_edge(j, k)) {
            answer[mask] = true;
          }
        }
      }
    }
  }
  return answer;
}

struct Evaluation {
  int conflicts{};
  int violations{};
  int individual_violations{};
  int lower{};
  int upper{};
  int ia{};
  int ib{};
  int ma{};
  int mb{};
  int red_forbidden_a{};
  int red_forbidden_b{};
  int forced_a{};
  int forced_b{};
  int forced_o{};
  int forced_ab{};
  int forced_ao{};
  int forced_bo{};

  int energy() const { return 10000 * conflicts + 100 * violations; }
};

Evaluation evaluate(const std::array<int, 28>& rows,
                    const std::array<bool, 1 << n>& has_edge,
                    const std::array<bool, 1 << n>& has_independent_triple) {
  Evaluation e;
  for (int x = 0; x < 7; ++x) e.ia += std::popcount(static_cast<unsigned>(rows[x]));
  for (int x = 7; x < 14; ++x) e.ib += std::popcount(static_cast<unsigned>(rows[x]));
  e.ma = 61 - e.ia;
  e.mb = 61 - e.ib;

  auto classify = [&](int x, int y, int& forced, int* forbidden) {
    bool blue_forbidden = has_independent_triple[full ^ (rows[x] | rows[y])];
    bool red_forbidden = forbidden != nullptr && has_edge[rows[x] & rows[y]];
    forced += blue_forbidden;
    if (forbidden != nullptr) *forbidden += red_forbidden;
    if (blue_forbidden && red_forbidden) ++e.conflicts;
  };
  for (int x = 0; x < 7; ++x)
    for (int y = x + 1; y < 7; ++y)
      classify(x, y, e.forced_a, &e.red_forbidden_a);
  for (int x = 7; x < 14; ++x)
    for (int y = x + 1; y < 14; ++y)
      classify(x, y, e.forced_b, &e.red_forbidden_b);
  for (int x = 14; x < 28; ++x)
    for (int y = x + 1; y < 28; ++y)
      classify(x, y, e.forced_o, nullptr);
  for (int x = 0; x < 7; ++x)
    for (int y = 7; y < 14; ++y)
      classify(x, y, e.forced_ab, nullptr);
  for (int x = 0; x < 7; ++x)
    for (int y = 14; y < 28; ++y)
      classify(x, y, e.forced_ao, nullptr);
  for (int x = 7; x < 14; ++x)
    for (int y = 14; y < 28; ++y)
      classify(x, y, e.forced_bo, nullptr);

  auto add_lower = [&](int value) { e.lower = std::max(e.lower, value); };
  e.lower = 18;
  add_lower(37);
  add_lower(e.forced_o);
  add_lower(37 + e.forced_ab);
  add_lower(e.ia + e.ib - 67); // lower bound 18 on G[A union B]
  add_lower(e.ia - 49);        // m_AO <= 98
  add_lower(e.ib - 49);        // m_BO <= 98

  e.upper = 73;
  e.upper = std::min(e.upper, 86); // m_AB <= 49
  e.upper = std::min(e.upper, 49 + e.ia - e.forced_ao);
  e.upper = std::min(e.upper, 49 + e.ib - e.forced_bo);
  e.upper = std::min(e.upper, e.ia + e.ib - 12); // upper bound 73 on G[A union B]

  auto shortfall = [](int value, int lower, int upper) {
    return value < lower ? lower - value : value > upper ? value - upper : 0;
  };
  e.violations += shortfall(e.ma, 3, 16);
  e.violations += shortfall(e.mb, 3, 16);
  e.violations += std::max(0, e.forced_a - e.ma);
  e.violations += std::max(0, e.ma - (21 - e.red_forbidden_a));
  e.violations += std::max(0, e.forced_b - e.mb);
  e.violations += std::max(0, e.mb - (21 - e.red_forbidden_b));
  e.violations += std::max(0, e.lower - e.upper);

  auto blue_forbidden = [&](int x, int y) {
    return has_independent_triple[full ^ (rows[x] | rows[y])];
  };
  auto red_forbidden = [&](int x, int y) {
    bool same_a = x < 7 && y < 7;
    bool same_b = 7 <= x && x < 14 && 7 <= y && y < 14;
    return (same_a || same_b) && has_edge[rows[x] & rows[y]];
  };
  for (int x = 0; x < 28; ++x) {
    int outside_degree = 21 - marked[x] - (x < 14) -
                         std::popcount(static_cast<unsigned>(rows[x]));
    int e_degree = 6 + 2 * (x == 0);
    int unmarked_degree = outside_degree - e_degree;
    int forced_all = 0, allowed_all = 0;
    int forced_marked = 0, allowed_marked = 0;
    int forced_unmarked = 0, allowed_unmarked = 0;
    for (int y = 0; y < 28; ++y) {
      if (x == y) continue;
      bool forced = blue_forbidden(x, y);
      bool allowed = !red_forbidden(x, y);
      forced_all += forced;
      allowed_all += allowed;
      if (marked[y]) {
        forced_marked += forced;
        allowed_marked += allowed;
      } else {
        forced_unmarked += forced;
        allowed_unmarked += allowed;
      }
    }
    int violation = 0;
    violation += shortfall(outside_degree, forced_all, allowed_all);
    violation += shortfall(e_degree, forced_marked, allowed_marked);
    violation += shortfall(unmarked_degree, forced_unmarked, allowed_unmarked);

    if (x < 14) {
      int first = x < 7 ? 0 : 7;
      int last = first + 7;
      int cell_target = x < 7 ? e.ma : e.mb;
      int noncontributing_capacity = 0;
      for (int left = first; left < last; ++left) {
        for (int right = left + 1; right < last; ++right) {
          if (red_forbidden(left, right)) continue;
          bool contributes_to_x = (left == x && marked[right]) ||
                                  (right == x && marked[left]);
          if (!contributes_to_x) ++noncontributing_capacity;
        }
      }
      int forced_external_marked = 0;
      for (int y = 0; y < 28; ++y)
        if (y != x && marked[y] && (y < first || y >= last) && blue_forbidden(x, y))
          ++forced_external_marked;
      int lower_e_load = forced_external_marked +
                         std::max(0, cell_target - noncontributing_capacity);
      violation += std::max(0, lower_e_load - e_degree);
    }
    e.individual_violations += violation;
  }
  e.violations += e.individual_violations;
  return e;
}

bool legal_mask(int mask, const std::vector<int>& independent_fours) {
  return std::all_of(independent_fours.begin(), independent_fours.end(),
                     [&](int four) { return (mask & four) != 0; });
}

std::vector<int> make_independent_fours() {
  std::vector<int> result;
  for (int i = 0; i < n; ++i)
    for (int j = i + 1; j < n; ++j)
      for (int k = j + 1; k < n; ++k)
        for (int l = k + 1; l < n; ++l)
          if (!core_edge(i, j) && !core_edge(i, k) && !core_edge(i, l) &&
              !core_edge(j, k) && !core_edge(j, l) && !core_edge(k, l))
            result.push_back((1 << i) | (1 << j) | (1 << k) | (1 << l));
  return result;
}

void print_rows(const std::array<int, 28>& rows, const Evaluation& e) {
  std::cout << "FOUND energy=" << e.energy() << " IA=" << e.ia << " IB=" << e.ib
            << " mA=" << e.ma << " mB=" << e.mb << " mO_interval=[" << e.lower
            << ',' << e.upper << "]\n";
  std::cout << "rows";
  for (int mask : rows)
    std::cout << ' ' << std::hex << std::setw(4) << std::setfill('0') << mask;
  std::cout << std::dec << '\n';
  std::cout << "forced A/B/O/AB/AO/BO=" << e.forced_a << '/' << e.forced_b << '/'
            << e.forced_o << '/' << e.forced_ab << '/' << e.forced_ao << '/'
            << e.forced_bo << " red_forbidden_A/B=" << e.red_forbidden_a << '/'
            << e.red_forbidden_b << '\n';
  std::cout << "individual_violations=" << e.individual_violations << '\n';
}

} // namespace

int main(int argc, char** argv) {
  std::uint64_t seed = argc > 1 ? std::stoull(argv[1]) : 48001;
  std::uint64_t iterations = argc > 2 ? std::stoull(argv[2]) : 20000000;
  std::mt19937_64 rng(seed);
  auto has_edge = make_has_edge();
  auto has_independent_triple = make_has_independent_triple();
  auto independent_fours = make_independent_fours();
  if (independent_fours.size() != 39) return 2;

  std::array<int, 28> initial = {
      0x1123, 0x0e34, 0x18d2, 0x078c, 0x091e, 0x18e3, 0x1ffe,
      0x1cc0, 0x0247, 0x078c, 0x038f, 0x1879, 0x1479, 0x1fff,
      0x0730, 0x10bb, 0x036f, 0x15c7, 0x19fc, 0x07b9, 0x1f32,
      0x1cd0, 0x1a97, 0x0647, 0x02c6, 0x0f48, 0x0d2d, 0x1839,
  };
  for (int mask : initial)
    if (!legal_mask(mask, independent_fours)) return 3;

  auto current = initial;
  auto current_eval = evaluate(current, has_edge, has_independent_triple);
  auto best = current;
  auto best_eval = current_eval;
  std::uniform_real_distribution<double> real(0.0, 1.0);
  std::vector<int> mark_classes[2];
  for (int x = 0; x < 28; ++x) mark_classes[marked[x]].push_back(x);

  for (std::uint64_t step = 0; step < iterations; ++step) {
    if (current_eval.energy() == 0) {
      print_rows(current, current_eval);
      return 0;
    }
    int mark = static_cast<int>(rng() & 1U);
    const auto& choices = mark_classes[mark];
    std::uint64_t arity_choice = rng() % 10;
    int arity = arity_choice == 0 ? 4 : arity_choice < 3 ? 3 : 2;
    std::array<int, 4> positions{};
    for (int z = 0; z < arity; ++z) {
      do positions[z] = choices[rng() % choices.size()];
      while (std::find(positions.begin(), positions.begin() + z, positions[z]) != positions.begin() + z);
    }
    auto candidate = current;
    for (int bit = 0; bit < n; ++bit) {
      int count = 0;
      for (int z = 0; z < arity; ++z) count += (current[positions[z]] >> bit) & 1;
      std::array<int, 4> order{0, 1, 2, 3};
      std::shuffle(order.begin(), order.begin() + arity, rng);
      for (int z = 0; z < arity; ++z) candidate[positions[z]] &= ~(1 << bit);
      for (int z = 0; z < count; ++z) candidate[positions[order[z]]] |= 1 << bit;
    }
    bool legal = true;
    for (int z = 0; z < arity; ++z)
      legal = legal && legal_mask(candidate[positions[z]], independent_fours);
    if (!legal) continue;
    auto candidate_eval = evaluate(candidate, has_edge, has_independent_triple);
    int delta = candidate_eval.energy() - current_eval.energy();
    double temperature = 250.0 * (1.0 - static_cast<double>(step % 200000) / 200000.0) + 0.25;
    if (delta <= 0 || real(rng) < std::exp(-static_cast<double>(delta) / temperature)) {
      current = candidate;
      current_eval = candidate_eval;
    }
    if (std::tie(current_eval.conflicts, current_eval.violations) <
        std::tie(best_eval.conflicts, best_eval.violations)) {
      best = current;
      best_eval = current_eval;
      std::cerr << "best step=" << step << " conflicts=" << best_eval.conflicts
                << " violations=" << best_eval.violations << " energy=" << best_eval.energy() << '\n';
    }
    if ((step + 1) % 200000 == 0 && current_eval.energy() != 0) {
      current = best;
      current_eval = best_eval;
      for (int kick = 0; kick < 8; ++kick) {
        int x = rng() % 28;
        int y;
        do y = rng() % 28; while (y == x || marked[y] != marked[x]);
        int diff = current[x] ^ current[y];
        int split = static_cast<int>(rng()) & diff;
        int common = current[x] & current[y];
        int nx = common | split;
        int ny = common | (diff ^ split);
        if (legal_mask(nx, independent_fours) && legal_mask(ny, independent_fours)) {
          current[x] = nx;
          current[y] = ny;
        }
      }
      current_eval = evaluate(current, has_edge, has_independent_triple);
    }
  }
  std::cerr << "NO_WITNESS seed=" << seed << " iterations=" << iterations << '\n';
  print_rows(best, best_eval);
  return 1;
}
