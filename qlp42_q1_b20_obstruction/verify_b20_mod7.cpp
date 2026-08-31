#include <array>
#include <cassert>
#include <compare>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <vector>

struct Gaussian {
  int real;
  int imag;
  auto operator<=>(const Gaussian &) const = default;
};

using Word = std::array<Gaussian, 7>;

constexpr std::array<Gaussian, 4> roots = {
    Gaussian{1, 0}, Gaussian{0, 1}, Gaussian{-1, 0}, Gaussian{0, -1}};

Gaussian add(Gaussian left, Gaussian right) {
  return {left.real + right.real, left.imag + right.imag};
}

Gaussian multiply_conjugate(Gaussian left, Gaussian right) {
  return {left.real * right.real + left.imag * right.imag,
          left.imag * right.real - left.real * right.imag};
}

std::vector<Gaussian> root_sum_domain(int count) {
  std::set<Gaussian> formula;
  for (int real = -count; real <= count; ++real) {
    for (int imag = -count; imag <= count; ++imag) {
      if (std::abs(real) + std::abs(imag) <= count &&
          (real + imag - count) % 2 == 0) {
        formula.insert({real, imag});
      }
    }
  }
  std::set<Gaussian> reachable = {Gaussian{0, 0}};
  for (int step = 0; step < count; ++step) {
    std::set<Gaussian> next;
    for (const auto partial : reachable) {
      for (const auto root : roots) {
        next.insert(add(partial, root));
      }
    }
    reachable = std::move(next);
  }
  assert(formula == reachable);
  return {formula.begin(), formula.end()};
}

Gaussian periodic_correlation(const Word &word, int shift) {
  Gaussian result{0, 0};
  for (int index = 0; index < 7; ++index) {
    result = add(result,
                 multiply_conjugate(word[index], word[(index + shift) % 7]));
  }
  return result;
}

int main() {
  const auto d2 = root_sum_domain(2);
  const auto d3 = root_sum_domain(3);
  const std::set<Gaussian> d3_set(d3.begin(), d3.end());
  assert(d2.size() == 9);
  assert(d3.size() == 16);

  std::uint64_t sum_zero = 0;
  std::uint64_t energy_18 = 0;
  std::uint64_t shift_1 = 0;
  std::uint64_t shifts_1_2 = 0;
  Word word{};
  for (const auto a : d2) {
    word[0] = a;
    for (const auto b : d3) {
      word[1] = b;
      for (const auto c : d3) {
        word[2] = c;
        for (const auto d : d3) {
          word[3] = d;
          for (const auto e : d3) {
            word[4] = e;
            for (const auto f : d3) {
              word[5] = f;
              Gaussian partial{0, 0};
              for (int index = 0; index < 6; ++index) {
                partial = add(partial, word[index]);
              }
              word[6] = {-partial.real, -partial.imag};
              if (!d3_set.contains(word[6])) {
                continue;
              }
              ++sum_zero;
              int energy = 0;
              for (const auto value : word) {
                energy += value.real * value.real + value.imag * value.imag;
              }
              if (energy != 18) {
                continue;
              }
              ++energy_18;
              if (periodic_correlation(word, 1) != Gaussian{-3, 0}) {
                continue;
              }
              ++shift_1;
              if (periodic_correlation(word, 2) != Gaussian{-3, 0}) {
                continue;
              }
              ++shifts_1_2;
            }
          }
        }
      }
    }
  }

  assert(sum_zero == 2'795'584);
  assert(energy_18 == 60'024);
  assert(shift_1 == 656);
  assert(shifts_1_2 == 0);
  std::cout << "d2_size=9\n"
            << "d3_size=16\n"
            << "raw_domain_tuples=150994944\n"
            << "sum_zero_tuples=" << sum_zero << '\n'
            << "energy_18_tuples=" << energy_18 << '\n'
            << "shift_1_tuples=" << shift_1 << '\n'
            << "shifts_1_2_tuples=" << shifts_1_2 << '\n'
            << "solutions=0\n"
            << "certificate=verified\n";
}
