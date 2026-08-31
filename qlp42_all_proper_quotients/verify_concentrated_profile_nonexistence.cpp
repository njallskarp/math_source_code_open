#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>

// Exact quotient certificate for the concentrated-autocorrelation QLP-42
// slice.  The mathematical reduction is documented in README.md.  This
// program proves that the required length-7 Gaussian-integer compression V
// does not exist.  It uses integer arithmetic only.

struct Gaussian {
  int real;
  int imaginary;

  friend bool operator==(Gaussian left, Gaussian right) {
    return left.real == right.real && left.imaginary == right.imaginary;
  }

  friend bool operator<(Gaussian left, Gaussian right) {
    if (left.real != right.real) return left.real < right.real;
    return left.imaginary < right.imaginary;
  }
};

Gaussian operator+(Gaussian left, Gaussian right) {
  return {left.real + right.real, left.imaginary + right.imaginary};
}

Gaussian operator-(Gaussian value) {
  return {-value.real, -value.imaginary};
}

Gaussian multiply_conjugate(Gaussian left, Gaussian right) {
  return {
      left.real * right.real + left.imaginary * right.imaginary,
      left.imaginary * right.real - left.real * right.imaginary,
  };
}

std::vector<Gaussian> sums_of_fourth_roots(int number_of_terms) {
  std::vector<Gaussian> result;
  for (int ones = 0; ones <= number_of_terms; ++ones) {
    for (int imaginaries = 0; imaginaries <= number_of_terms - ones;
         ++imaginaries) {
      for (int minus_ones = 0;
           minus_ones <= number_of_terms - ones - imaginaries;
           ++minus_ones) {
        const int minus_imaginaries =
            number_of_terms - ones - imaginaries - minus_ones;
        result.push_back(
            {ones - minus_ones, imaginaries - minus_imaginaries});
      }
    }
  }
  std::sort(result.begin(), result.end());
  result.erase(std::unique(result.begin(), result.end()), result.end());
  return result;
}

bool contains(const std::vector<Gaussian>& domain, Gaussian value) {
  return std::binary_search(domain.begin(), domain.end(), value);
}

Gaussian periodic_autocorrelation(const std::array<Gaussian, 7>& sequence,
                                  int shift) {
  Gaussian result{0, 0};
  for (int index = 0; index < 7; ++index) {
    result = result + multiply_conjugate(
                          sequence[index], sequence[(index + shift) % 7]);
  }
  return result;
}

int main() {
  const std::vector<Gaussian> sum_two = sums_of_fourth_roots(2);
  const std::vector<Gaussian> sum_three = sums_of_fourth_roots(3);
  assert(sum_two.size() == 9);
  assert(sum_three.size() == 16);

  std::uint64_t assignments_checked = 0;
  std::uint64_t sum_zero_domain_candidates = 0;
  std::uint64_t autocorrelation_candidates = 0;

  // A cyclic shift puts the unique zero of the length-21 sequence T in
  // residue class 0 modulo 7.  Hence V_0 is a sum of two fourth roots and
  // V_1,...,V_6 are sums of three.  Since sum(T)=0, choose V_0,...,V_5
  // and force V_6=-sum_{j=0}^5 V_j.
  for (Gaussian v0 : sum_two) {
    for (Gaussian v1 : sum_three) {
      for (Gaussian v2 : sum_three) {
        for (Gaussian v3 : sum_three) {
          for (Gaussian v4 : sum_three) {
            for (Gaussian v5 : sum_three) {
              ++assignments_checked;
              const Gaussian v6 = -(v0 + v1 + v2 + v3 + v4 + v5);
              if (!contains(sum_three, v6)) continue;
              ++sum_zero_domain_candidates;

              const std::array<Gaussian, 7> candidate{
                  v0, v1, v2, v3, v4, v5, v6};
              bool valid = true;
              for (int shift = 1; shift < 7; ++shift) {
                if (!(periodic_autocorrelation(candidate, shift) ==
                      Gaussian{-3, 0})) {
                  valid = false;
                  break;
                }
              }
              autocorrelation_candidates += valid;
            }
          }
        }
      }
    }
  }

  assert(assignments_checked == 9ULL * 16ULL * 16ULL * 16ULL * 16ULL * 16ULL);
  assert(autocorrelation_candidates == 0);

  std::cout << "sum_two_domain_size=" << sum_two.size() << '\n';
  std::cout << "sum_three_domain_size=" << sum_three.size() << '\n';
  std::cout << "assignments_checked=" << assignments_checked << '\n';
  std::cout << "sum_zero_domain_candidates=" << sum_zero_domain_candidates
            << '\n';
  std::cout << "autocorrelation_candidates=" << autocorrelation_candidates
            << '\n';
  std::cout << "concentrated_profile_qlp42_partner=impossible\n";
  std::cout << "certificate=verified\n";
  return 0;
}
