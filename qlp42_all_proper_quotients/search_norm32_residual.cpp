#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>

struct G {
  int x;
  int y;
};

constexpr G operator+(G a, G b) { return {a.x + b.x, a.y + b.y}; }
constexpr G operator-(G a, G b) { return {a.x - b.x, a.y - b.y}; }
constexpr G conj(G a) { return {a.x, -a.y}; }
constexpr G operator*(G a, G b) {
  return {a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x};
}

constexpr int kLength = 42;
constexpr std::array<G, 4> kRoots{{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}};
constexpr char kChars[5] = "1i-j";
using Phases = std::array<int, kLength>;

struct State {
  Phases phases{};
  std::array<G, kLength> paf{};
};

State make_state(const Phases& phases) {
  State out;
  out.phases = phases;
  for (int shift = 0; shift < kLength; ++shift) {
    for (int index = 0; index < kLength; ++index) {
      out.paf[shift] = out.paf[shift] +
          kRoots[phases[index]] * conj(kRoots[phases[(index + shift) % kLength]]);
    }
  }
  return out;
}

void apply_set_pair(State& state, int i, int new_i, int j, int new_j) {
  const int old_i = state.phases[i];
  const int old_j = state.phases[j];
  const std::array<int, 2> positions{{i, j}};
  const std::array<G, 2> delta{{kRoots[new_i] - kRoots[old_i],
                                kRoots[new_j] - kRoots[old_j]}};
  for (int shift = 0; shift < kLength; ++shift) {
    G change{0, 0};
    for (int a = 0; a < 2; ++a) {
      change = change + delta[a] *
          conj(kRoots[state.phases[(positions[a] + shift) % kLength]]);
      const int left = (positions[a] - shift + kLength) % kLength;
      change = change + kRoots[state.phases[left]] * conj(delta[a]);
      for (int b = 0; b < 2; ++b) {
        if ((positions[a] + shift) % kLength == positions[b]) {
          change = change + delta[a] * conj(delta[b]);
        }
      }
    }
    state.paf[shift] = state.paf[shift] + change;
  }
  state.phases[i] = new_i;
  state.phases[j] = new_j;
}

void apply_swap(State& state, int i, int j) {
  apply_set_pair(state, i, state.phases[j], j, state.phases[i]);
}

constexpr std::array<int, kLength> target_residual() {
  std::array<int, kLength> e{};
  for (int shift : {4, 11, 31, 38}) e[shift] = -2;
  for (int shift : {10, 17, 25, 32}) e[shift] = 2;
  return e;
}

constexpr auto kTargetResidual = target_residual();

std::int64_t score(const State& a, const State& b) {
  std::int64_t total = 0;
  for (int shift = 1; shift < kLength; ++shift) {
    const G target{kTargetResidual[shift] - 2, 0};
    const G difference = a.paf[shift] + b.paf[shift] - target;
    total += std::int64_t(difference.x) * difference.x +
             std::int64_t(difference.y) * difference.y;
  }
  return total;
}

Phases parse(const std::string& text) {
  Phases out{};
  if (text.size() != out.size()) throw std::runtime_error("bad seed length");
  for (std::size_t index = 0; index < text.size(); ++index) {
    const auto found = std::string(kChars).find(text[index]);
    if (found == std::string::npos) throw std::runtime_error("bad seed symbol");
    out[index] = static_cast<int>(found);
  }
  return out;
}

void print_phases(const char* name, const Phases& phases) {
  std::cout << name << '=';
  for (int phase : phases) std::cout << kChars[phase];
  std::cout << '\n';
}

int main(int argc, char** argv) {
  const int restarts = argc > 1 ? std::stoi(argv[1]) : 100;
  const int steps = argc > 2 ? std::stoi(argv[2]) : 1000000;
  std::mt19937_64 rng(0x4e4f524d3332514cULL);
  std::uniform_real_distribution<double> unit(0.0, 1.0);
  const Phases base_a = parse("ji111-1j-i--ji-j-ji1jjj-1ijj1jiii-1iij1-ii");
  const Phases base_b = parse("i--j-jj1i--j1-i1i-j1jjiij-iji11j1iii111i-j");

  std::int64_t global_best = std::numeric_limits<std::int64_t>::max();
  for (int restart = 0; restart < restarts; ++restart) {
    Phases pa = base_a;
    Phases pb = base_b;
    std::shuffle(pa.begin(), pa.end(), rng);
    std::shuffle(pb.begin(), pb.end(), rng);
    State a = make_state(pa);
    State b = make_state(pb);
    std::int64_t current = score(a, b);

    for (int step = 0; step < steps; ++step) {
      State& chosen = (rng() & 1) ? a : b;
      const int i = rng() % kLength;
      const int j = rng() % kLength;
      if (i == j || chosen.phases[i] == chosen.phases[j]) continue;
      const int old_i = chosen.phases[i];
      const int old_j = chosen.phases[j];
      int new_i = old_j;
      int new_j = old_i;
      if ((rng() & 3) == 0 && (old_i + 2) % 4 == old_j) {
        if (old_i % 2 == 0) {
          new_i = (rng() & 1) ? 1 : 3;
        } else {
          new_i = (rng() & 1) ? 0 : 2;
        }
        new_j = (new_i + 2) % 4;
      }
      apply_set_pair(chosen, i, new_i, j, new_j);
      const std::int64_t next = score(a, b);
      const double progress = double(step) / std::max(1, steps - 1);
      const double temperature = 120.0 * std::pow(0.05 / 120.0, progress);
      if (next <= current || unit(rng) < std::exp(double(current - next) / temperature)) {
        current = next;
      } else {
        apply_set_pair(chosen, i, old_i, j, old_j);
      }
      if (current < global_best) {
        global_best = current;
        std::cout << "best=" << global_best << " restart=" << restart
                  << " step=" << step << std::endl;
        if (global_best <= 128) {
          print_phases("A_best", a.phases);
          print_phases("B_best", b.phases);
        }
      }
      if (current == 0) {
        std::cout << "status=SAT\n";
        print_phases("A", a.phases);
        print_phases("B", b.phases);
        return 0;
      }
    }
    std::cout << "restart=" << restart << " final=" << current
              << " global_best=" << global_best << std::endl;
  }
  std::cout << "status=NOT_FOUND best=" << global_best << '\n';
  return 1;
}
