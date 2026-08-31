// Exact-vs-binary64 prefix audit of Hercher's Corollary 29 search.
//
// This is an optimized mirror of audit_prefix.py.  Exact means and correction
// factors are represented by compact integer invariants rather than normalized
// general-purpose rational objects.

#include <boost/multiprecision/cpp_int.hpp>

#include <algorithm>
#include <cassert>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using boost::multiprecision::cpp_int;

namespace {

const cpp_int kA("4370000000000000000000");
constexpr unsigned kDefaultC = 1536;
const double kMeanThreshold = 1.0 / (4.37e21);
const double kSecondBranchLimit = 1.0 / kMeanThreshold;

std::vector<cpp_int> pow2_exact;
std::vector<cpp_int> pow3_exact;
std::vector<double> pow2_float;

struct PowRatio {
  unsigned exponent2 = 0;
  unsigned exponent3 = 0;
};

struct Correction {
  PowRatio exact;
  double floating = 1.0;
};

unsigned mod_small(const cpp_int& value, unsigned modulus) {
  return (value % modulus).convert_to<unsigned>();
}

bool ratio_less(const PowRatio& left, const PowRatio& right) {
  return pow2_exact[left.exponent2] * pow3_exact[right.exponent3]
       < pow2_exact[right.exponent2] * pow3_exact[left.exponent3];
}

Correction correction_factor(unsigned odd, const cpp_int& rest,
                             bool last_step_odd) {
  Correction best;
  const unsigned residue = mod_small(rest, 729);

  auto consider = [&](unsigned odd_cost, unsigned exponent2,
                      unsigned exponent3, unsigned divisor,
                      unsigned multiplier, unsigned offset,
                      double floating_factor) {
    Correction tail = correction_factor(
        odd - odd_cost, rest / divisor * multiplier + offset, false);
    tail.exact.exponent2 += exponent2;
    tail.exact.exponent3 += exponent3;
    tail.floating *= floating_factor;
    if (ratio_less(tail.exact, best.exact)) {
      best.exact = tail.exact;
    }
    if (tail.floating < best.floating) {
      best.floating = tail.floating;
    }
  };

  if (odd >= 1 && !last_step_odd && residue % 3 == 2) {
    consider(1, 1, 1, 3, 2, 1, 2.0 / 3.0);
  }
  if (odd >= 2 && residue % 9 == 4) {
    consider(2, 3, 2, 9, 8, 3, 8.0 / 9.0);
  }
  if (odd >= 4 && residue % 81 == 10) {
    consider(4, 6, 4, 81, 64, 7, 64.0 / 81.0);
  }
  if (odd >= 5 && residue % 243 == 182) {
    consider(5, 7, 5, 243, 128, 95, 128.0 / 243.0);
  }
  if (odd >= 6) {
    unsigned predecessor = 0;
    switch (residue) {
      case 91: predecessor = 63; break;
      case 410: predecessor = 287; break;
      case 433: predecessor = 303; break;
      case 524: predecessor = 367; break;
      case 587: predecessor = 411; break;
      case 604: predecessor = 423; break;
      case 661: predecessor = 463; break;
      case 695: predecessor = 487; break;
      default: break;
    }
    if (predecessor != 0) {
      consider(6, 9, 6, 729, 512, predecessor, 512.0 / 729.0);
    }
  }
  return best;
}

struct State {
  cpp_int rest_start;
  unsigned odd;
  cpp_int rest_it;

  // mean_sum = mean_sum_scaled / 3^odd.
  cpp_int mean_sum_scaled;
  cpp_int mean_min_num;
  cpp_int mean_min_den;

  cpp_int min_factor_num;
  cpp_int min_factor_den;

  double mean_float;
  double mean_min_float;
  double factor_float;
  double min_factor_float;
  double rest_start_float;
};

struct Audit {
  std::uint64_t generated = 0;
  std::uint64_t pruned_exact = 0;
  std::uint64_t frontier = 0;
  std::uint64_t decision_disagreements = 0;
  std::uint64_t corrected_multiplier_disagreements = 0;
  std::uint64_t float_multiplier_below_exact = 0;
  std::uint64_t float_multiplier_above_exact = 0;
  cpp_int maximum_multiplier_error = 0;
  std::uint64_t second_branch_disagreements = 0;
  bool has_margin = false;
  cpp_int minimum_margin_num;
  cpp_int minimum_margin_den;

  void record_margin(const cpp_int& mean_num, const cpp_int& mean_den,
                     const cpp_int& corrected_start) {
    cpp_int difference = kA * mean_num - mean_den * corrected_start;
    if (difference < 0) difference = -difference;
    cpp_int denominator = mean_den * corrected_start;
    if (!has_margin ||
        difference * minimum_margin_den < minimum_margin_num * denominator) {
      has_margin = true;
      minimum_margin_num = std::move(difference);
      minimum_margin_den = std::move(denominator);
    }
  }
};

cpp_int ceil_div_positive(const cpp_int& numerator,
                          const cpp_int& denominator) {
  assert(numerator > 0);
  assert(denominator > 0);
  return (numerator + denominator - 1) / denominator;
}

cpp_int gcd(cpp_int left, cpp_int right) {
  if (left < 0) left = -left;
  if (right < 0) right = -right;
  while (right != 0) {
    cpp_int remainder = left % right;
    left = std::move(right);
    right = std::move(remainder);
  }
  return left;
}

struct ChildResult {
  State state;
  bool exact_keep;
  bool float_keep;
};

ChildResult child_state(const State& parent, unsigned nr, bool second_branch,
                        const cpp_int& convergence_bound,
                        double convergence_bound_float, Audit& audit) {
  State child = parent;
  const unsigned next_nr = nr + 1;
  if (second_branch) {
    child.rest_start += pow2_exact[nr];
    child.rest_start_float += pow2_float[nr];
    child.rest_it += pow3_exact[parent.odd];
  }

  bool last_step_odd;
  if ((child.rest_it & 1) == 0) {
    child.rest_it >>= 1;
    child.factor_float = parent.factor_float * 0.5;
    last_step_odd = false;
  } else {
    child.odd = parent.odd + 1;
    child.rest_it = child.rest_it + (child.rest_it >> 1) + 1;
    child.mean_sum_scaled =
        3 * (parent.mean_sum_scaled + pow2_exact[nr]);
    const cpp_int current_den =
        cpp_int(child.odd) * pow3_exact[child.odd];
    if (child.mean_sum_scaled * parent.mean_min_den <
        parent.mean_min_num * current_den) {
      child.mean_min_num = child.mean_sum_scaled;
      child.mean_min_den = current_den;
    }
    child.mean_float =
        (parent.mean_float * parent.odd + 1.0 / parent.factor_float) /
        child.odd;
    child.mean_min_float =
        std::min(parent.mean_min_float, child.mean_float);
    child.factor_float = parent.factor_float * 1.5;
    last_step_odd = true;
  }

  const Correction correction =
      correction_factor(child.odd, child.rest_it, last_step_odd);
  assert(correction.exact.exponent3 <= child.odd);
  cpp_int candidate_num =
      pow2_exact[correction.exact.exponent2] *
      pow3_exact[child.odd - correction.exact.exponent3];
  cpp_int candidate_den = pow2_exact[next_nr];
  if (candidate_num * parent.min_factor_den <
      parent.min_factor_num * candidate_den) {
    child.min_factor_num = std::move(candidate_num);
    child.min_factor_den = std::move(candidate_den);
  }
  child.min_factor_float = std::min(
      parent.min_factor_float, child.factor_float * correction.floating);

  cpp_int exact_corrected_start = child.rest_start;
  cpp_int exact_multiplier = 0;
  if (child.rest_start * child.min_factor_num <
      convergence_bound * child.min_factor_den) {
    const cpp_int numerator = convergence_bound * child.min_factor_den -
                              child.rest_start * child.min_factor_num;
    const cpp_int denominator =
        child.min_factor_num * pow2_exact[next_nr];
    exact_multiplier = ceil_div_positive(numerator, denominator);
    exact_corrected_start += exact_multiplier * pow2_exact[next_nr];
  }

  double float_corrected_start = child.rest_start_float;
  double float_multiplier_value = 0.0;
  if (child.rest_start_float * child.min_factor_float <
      convergence_bound_float) {
    float_multiplier_value = std::ceil(
        (convergence_bound_float / child.min_factor_float -
         child.rest_start_float) /
        pow2_float[next_nr]);
    float_corrected_start +=
        float_multiplier_value * pow2_float[next_nr];
  }
  const cpp_int float_multiplier(float_multiplier_value);

  if (exact_multiplier != float_multiplier) {
    ++audit.corrected_multiplier_disagreements;
    if (float_multiplier < exact_multiplier) {
      ++audit.float_multiplier_below_exact;
    } else {
      ++audit.float_multiplier_above_exact;
    }
    cpp_int error = exact_multiplier - float_multiplier;
    if (error < 0) error = -error;
    if (error > audit.maximum_multiplier_error) {
      audit.maximum_multiplier_error = std::move(error);
    }
  }

  const bool exact_keep =
      kA * child.mean_min_num >= child.mean_min_den * exact_corrected_start;
  const double local_mean_float =
      child.mean_min_float / float_corrected_start;
  const bool float_keep = local_mean_float >= kMeanThreshold;
  if (exact_keep != float_keep) {
    ++audit.decision_disagreements;
  }
  audit.record_margin(child.mean_min_num, child.mean_min_den,
                      exact_corrected_start);

  return {std::move(child), exact_keep, float_keep};
}

void visit(const State& state, unsigned nr, unsigned depth,
           const cpp_int& convergence_bound, double convergence_bound_float,
           Audit& audit) {
  const bool second_exact = state.rest_start + pow2_exact[nr] <= kA;
  const bool second_float =
      state.rest_start_float + pow2_float[nr] <= kSecondBranchLimit;
  if (second_exact != second_float) {
    ++audit.second_branch_disagreements;
  }

  for (bool second_branch : {false, true}) {
    if (second_branch && !second_exact) continue;
    ++audit.generated;
    ChildResult result = child_state(
        state, nr, second_branch, convergence_bound,
        convergence_bound_float, audit);
    if (!result.exact_keep) {
      ++audit.pruned_exact;
    } else if (nr + 1 == depth) {
      ++audit.frontier;
    } else {
      visit(result.state, nr + 1, depth, convergence_bound,
            convergence_bound_float, audit);
    }
  }
}

Audit audit_prefix(unsigned depth, unsigned c) {
  if (depth < 2 || depth > 300) {
    throw std::invalid_argument("depth must lie between 2 and 300");
  }
  const unsigned table_size = std::max(2 * depth + 16, 64U);
  pow2_exact.assign(table_size, 1);
  pow3_exact.assign(table_size, 1);
  pow2_float.assign(table_size, 1.0);
  for (unsigned i = 1; i < table_size; ++i) {
    pow2_exact[i] = 2 * pow2_exact[i - 1];
    pow3_exact[i] = 3 * pow3_exact[i - 1];
    pow2_float[i] = 2.0 * pow2_float[i - 1];
  }

  const cpp_int convergence_bound = cpp_int(c) * pow2_exact[60];
  const double convergence_bound_float =
      static_cast<double>(c) * std::ldexp(1.0, 60);
  State start{
      cpp_int(1), 1, cpp_int(2), cpp_int(3), cpp_int(1), cpp_int(1),
      cpp_int(1), cpp_int(1), 1.0, 1.0, 1.5, 1.0, 1.0};
  Audit audit;
  visit(start, 1, depth, convergence_bound, convergence_bound_float, audit);
  return audit;
}

}  // namespace

int main(int argc, char** argv) {
  unsigned depth = 20;
  unsigned c = kDefaultC;
  for (int i = 1; i < argc; ++i) {
    const std::string argument = argv[i];
    if (argument == "--depth" && i + 1 < argc) {
      depth = static_cast<unsigned>(std::stoul(argv[++i]));
    } else if (argument == "--c" && i + 1 < argc) {
      c = static_cast<unsigned>(std::stoul(argv[++i]));
    } else {
      std::cerr << "usage: " << argv[0] << " [--depth N] [--c N]\n";
      return EXIT_FAILURE;
    }
  }

  try {
    const auto started = std::chrono::steady_clock::now();
    Audit audit = audit_prefix(depth, c);
    const double elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - started).count();
    assert(audit.has_margin);
    cpp_int divisor = gcd(audit.minimum_margin_num, audit.minimum_margin_den);
    audit.minimum_margin_num /= divisor;
    audit.minimum_margin_den /= divisor;

    std::cout << "depth=" << depth << '\n';
    std::cout << "c=" << c << '\n';
    std::cout << "generated=" << audit.generated << '\n';
    std::cout << "pruned_exact=" << audit.pruned_exact << '\n';
    std::cout << "frontier=" << audit.frontier << '\n';
    std::cout << "decision_disagreements="
              << audit.decision_disagreements << '\n';
    std::cout << "corrected_multiplier_disagreements="
              << audit.corrected_multiplier_disagreements << '\n';
    std::cout << "float_multiplier_below_exact="
              << audit.float_multiplier_below_exact << '\n';
    std::cout << "float_multiplier_above_exact="
              << audit.float_multiplier_above_exact << '\n';
    std::cout << "maximum_multiplier_error="
              << audit.maximum_multiplier_error << '\n';
    std::cout << "second_branch_disagreements="
              << audit.second_branch_disagreements << '\n';
    std::cout << "minimum_scaled_margin=" << audit.minimum_margin_num
              << '/' << audit.minimum_margin_den << '\n';
    std::cout << "elapsed_seconds=" << elapsed << '\n';
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
