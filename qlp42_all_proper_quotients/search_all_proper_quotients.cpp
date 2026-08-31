#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>

// Search for actual length-42 fourth-root arrays satisfying every proper
// divisor quotient-correlation equation forced by a quaternary Legendre pair.
// It is enough to impose d=6,14,21; all other proper divisors coarsen these.

struct G {
  int x;
  int y;
};

constexpr G operator+(G a, G b) { return {a.x + b.x, a.y + b.y}; }
constexpr G operator-(G a, G b) { return {a.x - b.x, a.y - b.y}; }
constexpr G operator-(G a) { return {-a.x, -a.y}; }
constexpr G conj(G a) { return {a.x, -a.y}; }
constexpr G operator*(G a, G b) {
  return {a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x};
}

constexpr std::array<G, 4> kRoots{{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}};
constexpr char kChars[5] = "1i-j";
using Phases = std::array<int, 42>;

template <std::size_t D>
struct QuotientData {
  std::array<G, D> q{};
  std::array<G, D> paf{};
};

template <std::size_t D>
QuotientData<D> make_quotient(const Phases& phases) {
  QuotientData<D> out;
  for (int j = 0; j < 42; ++j) {
    out.q[j % D] = out.q[j % D] + kRoots[phases[j]];
  }
  for (std::size_t s = 0; s < D; ++s) {
    for (std::size_t r = 0; r < D; ++r) {
      out.paf[s] = out.paf[s] + out.q[r] * conj(out.q[(r + s) % D]);
    }
  }
  return out;
}

template <std::size_t D>
void update_quotient(QuotientData<D>& data, int i, int j, G old_i, G old_j,
                     G new_i, G new_j) {
  const int ri = i % D;
  const int rj = j % D;
  if (ri == rj) return;

  const G di = new_i - old_i;
  const G dj = new_j - old_j;
  const std::array<int, 2> pos{{ri, rj}};
  const std::array<G, 2> delta{{di, dj}};

  for (int s = 0; s < static_cast<int>(D); ++s) {
    G change{0, 0};
    for (int a = 0; a < 2; ++a) {
      change = change + delta[a] * conj(data.q[(pos[a] + s) % D]);
      const int left = (pos[a] - s + static_cast<int>(D)) % D;
      change = change + data.q[left] * conj(delta[a]);
      for (int b = 0; b < 2; ++b) {
        if ((pos[a] + s) % D == pos[b]) {
          change = change + delta[a] * conj(delta[b]);
        }
      }
    }
    data.paf[s] = data.paf[s] + change;
  }
  data.q[ri] = data.q[ri] + di;
  data.q[rj] = data.q[rj] + dj;
}

struct State {
  Phases phases{};
  QuotientData<6> q6;
  QuotientData<14> q14;
  QuotientData<21> q21;
};

State make_state(const Phases& phases) {
  return {phases, make_quotient<6>(phases), make_quotient<14>(phases),
          make_quotient<21>(phases)};
}

void apply_swap(State& state, int i, int j) {
  const int pi = state.phases[i];
  const int pj = state.phases[j];
  update_quotient(state.q6, i, j, kRoots[pi], kRoots[pj], kRoots[pj],
                  kRoots[pi]);
  update_quotient(state.q14, i, j, kRoots[pi], kRoots[pj], kRoots[pj],
                  kRoots[pi]);
  update_quotient(state.q21, i, j, kRoots[pi], kRoots[pj], kRoots[pj],
                  kRoots[pi]);
  std::swap(state.phases[i], state.phases[j]);
}

void apply_set_pair(State& state, int i, int new_i, int j, int new_j) {
  const int old_i = state.phases[i];
  const int old_j = state.phases[j];
  update_quotient(state.q6, i, j, kRoots[old_i], kRoots[old_j], kRoots[new_i],
                  kRoots[new_j]);
  update_quotient(state.q14, i, j, kRoots[old_i], kRoots[old_j], kRoots[new_i],
                  kRoots[new_j]);
  update_quotient(state.q21, i, j, kRoots[old_i], kRoots[old_j], kRoots[new_i],
                  kRoots[new_j]);
  state.phases[i] = new_i;
  state.phases[j] = new_j;
}

template <std::size_t D>
std::int64_t quotient_score(const QuotientData<D>& a,
                            const QuotientData<D>& b) {
  constexpr int class_length = 42 / D;
  std::int64_t score = 0;
  for (std::size_t s = 0; s < D; ++s) {
    const int target = s == 0 ? 86 - 2 * class_length : -2 * class_length;
    const G residual = a.paf[s] + b.paf[s] - G{target, 0};
    score += std::int64_t(residual.x) * residual.x +
             std::int64_t(residual.y) * residual.y;
  }
  return score;
}

std::int64_t score(const State& a, const State& b) {
  return quotient_score(a.q6, b.q6) + quotient_score(a.q14, b.q14) +
         quotient_score(a.q21, b.q21);
}

Phases parse(const std::string& text) {
  Phases out{};
  if (text.size() != out.size()) throw std::runtime_error("bad seed length");
  for (std::size_t j = 0; j < text.size(); ++j) {
    const auto found = std::string(kChars).find(text[j]);
    if (found == std::string::npos) throw std::runtime_error("bad seed symbol");
    out[j] = static_cast<int>(found);
  }
  return out;
}

void print_phases(const char* name, const Phases& phases) {
  std::cout << name << '=';
  for (int phase : phases) std::cout << kChars[phase];
  std::cout << '\n';
}

template <std::size_t D>
void print_combined(const char* name, const QuotientData<D>& a,
                    const QuotientData<D>& b) {
  std::cout << name << "=[";
  for (std::size_t s = 0; s < D; ++s) {
    if (s) std::cout << ',';
    const G z = a.paf[s] + b.paf[s];
    std::cout << '(' << z.x << ',' << z.y << ')';
  }
  std::cout << "]\n";
}

int main(int argc, char** argv) {
  const int restarts = argc > 1 ? std::stoi(argv[1]) : 200;
  const int steps = argc > 2 ? std::stoi(argv[2]) : 2000000;
  std::mt19937_64 rng(0x414c4c51554f5432ULL);
  std::uniform_real_distribution<double> unit(0.0, 1.0);

  const std::string seed_a = "ji111-1j-i--ji-j-ji1jjj-1ijj1jiii-1iij1-ii";
  const std::string seed_b = "i--j-jj1i--j1-i1i-j1jjiij-iji11j1iii111i-j";
  Phases base_a = parse(seed_a);
  Phases base_b = parse(seed_b);

  std::int64_t global_best = std::numeric_limits<std::int64_t>::max();
  for (int restart = 0; restart < restarts; ++restart) {
    Phases pa = base_a;
    Phases pb = base_b;
    if (restart != 0) {
      std::shuffle(pa.begin(), pa.end(), rng);
      std::shuffle(pb.begin(), pb.end(), rng);
    }
    State a = make_state(pa);
    State b = make_state(pb);
    std::int64_t current = score(a, b);

    for (int step = 0; step < steps; ++step) {
      State& chosen = (rng() & 1) ? a : b;
      const int i = rng() % 42;
      const int j = rng() % 42;
      if (i == j || chosen.phases[i] == chosen.phases[j]) continue;

      const int old_i = chosen.phases[i];
      const int old_j = chosen.phases[j];
      bool conversion = false;
      int new_i = old_j;
      int new_j = old_i;
      if ((rng() & 3) == 0 && (old_i + 2) % 4 == old_j) {
        conversion = true;
        if (old_i % 2 == 0) {
          new_i = (rng() & 1) ? 1 : 3;
          new_j = (new_i + 2) % 4;
        } else {
          new_i = (rng() & 1) ? 0 : 2;
          new_j = (new_i + 2) % 4;
        }
        apply_set_pair(chosen, i, new_i, j, new_j);
      } else {
        apply_swap(chosen, i, j);
      }
      const std::int64_t next = score(a, b);
      const double progress = double(step) / std::max(1, steps - 1);
      const double temperature = 80.0 * std::pow(0.02 / 80.0, progress);
      if (next <= current || unit(rng) < std::exp(double(current - next) / temperature)) {
        current = next;
      } else {
        if (conversion) {
          apply_set_pair(chosen, i, old_i, j, old_j);
        } else {
          apply_swap(chosen, i, j);
        }
      }

      if (current < global_best) {
        global_best = current;
        std::cout << "best=" << global_best << " restart=" << restart
                  << " step=" << step << std::endl;
        if (global_best <= 256) {
          print_phases("A_best", a.phases);
          print_phases("B_best", b.phases);
        }
      }
      if (current == 0) {
        std::cout << "status=SAT restart=" << restart << " step=" << step << '\n';
        print_phases("A", a.phases);
        print_phases("B", b.phases);
        print_combined("C6", a.q6, b.q6);
        print_combined("C14", a.q14, b.q14);
        print_combined("C21", a.q21, b.q21);
        return 0;
      }
    }
    std::cout << "restart=" << restart << " final=" << current
              << " global_best=" << global_best << std::endl;
  }
  std::cout << "status=NOT_FOUND best=" << global_best << '\n';
  return 1;
}
