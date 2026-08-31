#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <limits>
#include <random>
#include <string>
#include <vector>

// Heuristic search for exact witnesses of the scaled length-21
// half-difference projection.  Any reported cost-zero state is checked again
// by direct integer autocorrelation before it is printed.  Failure to find a
// state is not evidence of infeasibility.

constexpr int kLength = 21;
constexpr int kScalars = 4;  // Re(S_A), Im(S_A), Re(S_B), Im(S_B).

using Scalar = std::array<int, kLength>;
using State = std::array<Scalar, kScalars>;

constexpr std::array<std::array<int, 4>, 6> kRepresentatives{{
    {{1, 0, 5, 0}},
    {{3, 0, 4, 1}},
    {{3, 0, 3, -2}},
    {{3, 2, 3, 2}},
    {{3, 2, 2, 3}},
    {{4, 1, 2, -1}},
}};

constexpr std::array<int, 11> kTarget{{43, 0, 0, 0, -2, 0, 0, 0, 0, 0, 2}};

std::array<int, kScalars> required_sums(int case_index) {
  const auto [p, q, x, y] = kRepresentatives[case_index];
  return {p + q, q - p, x + y - 1, y - x};
}

std::int64_t score(const State& state) {
  std::int64_t result = 0;
  for (int shift = 1; shift <= 10; ++shift) {
    int real = 0;
    int imaginary = 0;
    for (int j = 0; j < kLength; ++j) {
      const int k = (j + shift) % kLength;
      for (int sequence = 0; sequence < kScalars; ++sequence) {
        real += state[sequence][j] * state[sequence][k];
      }
      imaginary += state[1][j] * state[0][k] -
                   state[0][j] * state[1][k];
      imaginary += state[3][j] * state[2][k] -
                   state[2][j] * state[3][k];
    }
    const int real_error = real - kTarget[shift];
    result += std::int64_t(real_error) * real_error;
    result += std::int64_t(imaginary) * imaginary;
  }
  return result;
}

int support(const Scalar& scalar) {
  return std::count_if(scalar.begin(), scalar.end(),
                       [](int value) { return value != 0; });
}

int unit_cells(const State& state) {
  int result = 0;
  for (int pair = 0; pair < 2; ++pair) {
    for (int j = 0; j < kLength; ++j) {
      const int coordinate_support =
          (state[2 * pair][j] != 0) + (state[2 * pair + 1][j] != 0);
      result += coordinate_support == 1;
    }
  }
  return result;
}

bool exact_check(const State& state, int case_index) {
  const auto sums = required_sums(case_index);
  int total_support = 0;
  for (int sequence = 0; sequence < kScalars; ++sequence) {
    int sum = 0;
    for (int value : state[sequence]) {
      if (value < -1 || value > 1) return false;
      sum += value;
      total_support += value != 0;
    }
    if (sum != sums[sequence]) return false;
  }
  if (total_support != 43) return false;
  return score(state) == 0;
}

State random_state(int case_index, std::mt19937_64& generator) {
  const auto sums = required_sums(case_index);
  std::array<int, kScalars> weights{};
  int total = 0;
  for (int sequence = 0; sequence < kScalars; ++sequence) {
    weights[sequence] = std::abs(sums[sequence]);
    total += weights[sequence];
  }
  std::uniform_int_distribution<int> choose_sequence(0, kScalars - 1);
  while (total < 43) {
    const int sequence = choose_sequence(generator);
    if (weights[sequence] + 2 <= kLength) {
      weights[sequence] += 2;
      total += 2;
    }
  }

  State state{};
  for (int sequence = 0; sequence < kScalars; ++sequence) {
    const int positive = (weights[sequence] + sums[sequence]) / 2;
    const int negative = (weights[sequence] - sums[sequence]) / 2;
    int position = 0;
    for (int count = 0; count < positive; ++count) state[sequence][position++] = 1;
    for (int count = 0; count < negative; ++count) state[sequence][position++] = -1;
    while (position < kLength) state[sequence][position++] = 0;
    std::shuffle(state[sequence].begin(), state[sequence].end(), generator);
  }
  return state;
}

State constrained_random_state(int case_index, std::mt19937_64& generator) {
  while (true) {
    State state = random_state(case_index, generator);
    if (unit_cells(state) % 4 == 1) return state;
  }
}

bool propose_swap(State& state, std::mt19937_64& generator) {
  std::uniform_int_distribution<int> choose_sequence(0, kScalars - 1);
  std::uniform_int_distribution<int> choose_position(0, kLength - 1);
  const int sequence = choose_sequence(generator);
  const int first = choose_position(generator);
  const int second = choose_position(generator);
  if (state[sequence][first] == state[sequence][second]) return false;
  std::swap(state[sequence][first], state[sequence][second]);
  return true;
}

bool propose_transfer(State& state, std::mt19937_64& generator) {
  std::array<int, kScalars> source_candidates{};
  std::array<int, kScalars> target_candidates{};
  int source_count = 0;
  int target_count = 0;
  for (int sequence = 0; sequence < kScalars; ++sequence) {
    const int positive = std::count(state[sequence].begin(), state[sequence].end(), 1);
    const int negative = std::count(state[sequence].begin(), state[sequence].end(), -1);
    const int zero = kLength - positive - negative;
    if (positive && negative) source_candidates[source_count++] = sequence;
    if (zero >= 2) target_candidates[target_count++] = sequence;
  }
  if (!source_count || !target_count) return false;
  std::uniform_int_distribution<int> choose_source(0, source_count - 1);
  std::uniform_int_distribution<int> choose_target(0, target_count - 1);
  const int source = source_candidates[choose_source(generator)];
  const int target = target_candidates[choose_target(generator)];
  if (source == target) return false;

  std::vector<int> positive_positions;
  std::vector<int> negative_positions;
  std::vector<int> zero_positions;
  for (int j = 0; j < kLength; ++j) {
    if (state[source][j] == 1) positive_positions.push_back(j);
    if (state[source][j] == -1) negative_positions.push_back(j);
    if (state[target][j] == 0) zero_positions.push_back(j);
  }
  std::shuffle(positive_positions.begin(), positive_positions.end(), generator);
  std::shuffle(negative_positions.begin(), negative_positions.end(), generator);
  std::shuffle(zero_positions.begin(), zero_positions.end(), generator);
  state[source][positive_positions.front()] = 0;
  state[source][negative_positions.front()] = 0;
  state[target][zero_positions[0]] = 1;
  state[target][zero_positions[1]] = -1;
  return true;
}

void print_state(const State& state) {
  constexpr std::array<const char*, kScalars> names{{"A_real", "A_imag", "B_real", "B_imag"}};
  for (int sequence = 0; sequence < kScalars; ++sequence) {
    std::cout << names[sequence] << "=[";
    for (int j = 0; j < kLength; ++j) {
      if (j) std::cout << ',';
      std::cout << state[sequence][j];
    }
    std::cout << "]\n";
  }
}

int main(int argc, char** argv) {
  int case_index = 0;
  int restarts = 100;
  int steps = 200000;
  std::uint64_t seed = 20260831;
  for (int index = 1; index < argc; ++index) {
    const std::string argument = argv[index];
    if (argument == "--case" && index + 1 < argc) case_index = std::stoi(argv[++index]);
    else if (argument == "--restarts" && index + 1 < argc) restarts = std::stoi(argv[++index]);
    else if (argument == "--steps" && index + 1 < argc) steps = std::stoi(argv[++index]);
    else if (argument == "--seed" && index + 1 < argc) seed = std::stoull(argv[++index]);
    else {
      std::cerr << "usage: search [--case 0..5] [--restarts N] [--steps N] [--seed N]\n";
      return 2;
    }
  }
  if (case_index < 0 || case_index >= 6 || restarts <= 0 || steps <= 0) return 2;

  std::mt19937_64 generator(seed);
  std::uniform_real_distribution<double> uniform(0.0, 1.0);
  std::int64_t global_best = std::numeric_limits<std::int64_t>::max();
  State best_state{};

  for (int restart = 0; restart < restarts; ++restart) {
    State state = constrained_random_state(case_index, generator);
    std::int64_t current = score(state);
    for (int step = 0; step < steps; ++step) {
      State candidate = state;
      const bool changed = uniform(generator) < 0.88
                               ? propose_swap(candidate, generator)
                               : propose_transfer(candidate, generator);
      if (!changed) continue;
      if (unit_cells(candidate) % 4 != 1) continue;
      const std::int64_t proposed = score(candidate);
      const double progress = double(step) / steps;
      const double temperature = 8.0 * std::pow(0.01 / 8.0, progress);
      if (proposed <= current ||
          uniform(generator) < std::exp(double(current - proposed) / temperature)) {
        state = candidate;
        current = proposed;
      }
      if (current < global_best) {
        global_best = current;
        best_state = state;
        std::cout << "case=" << case_index << "; restart=" << restart
                  << "; step=" << step << "; best=" << global_best << '\n';
      }
      if (current == 0) {
        if (!exact_check(state, case_index)) return 1;
        print_state(state);
        std::cout << "case=" << case_index << "; exact_projection_witness=verified\n";
        return 0;
      }
    }
  }
  print_state(best_state);
  std::cout << "case=" << case_index << "; best=" << global_best
            << "; witness_found=false\n";
  return 3;
}
