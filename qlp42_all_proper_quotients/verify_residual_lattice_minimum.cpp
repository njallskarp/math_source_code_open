#include <array>
#include <cstdint>
#include <iostream>
#include <limits>

// Exact finite verification of the shortest nonzero vector in the residual
// lattice described in primitive_quotient_kernel.md.  A separate exact
// rational LDL check proves M-I positive definite.  Therefore x^T M x < 32
// implies ||x||^2 <= 31, which is the finite region enumerated here.

constexpr int kDimension = 11;
constexpr std::int64_t kGram[kDimension][kDimension] = {
    {48, 0, -32, 8, 16, -16, 0, 24, 0, -16, 8},
    {0, 48, 8, -32, -16, 16, 24, 0, -16, 0, 8},
    {-32, 8, 48, -16, -32, 24, 16, -16, 0, 8, 0},
    {8, -32, -16, 48, 24, -32, -16, 16, 8, 0, 0},
    {16, -16, -32, 24, 48, -16, -32, 8, 16, 0, 0},
    {-16, 16, 24, -32, -16, 48, 8, -32, 0, 16, 0},
    {0, 24, 16, -16, -32, 8, 48, 0, -32, 0, 16},
    {24, 0, -16, 16, 8, -32, 0, 48, 0, -32, 16},
    {0, -16, 0, 8, 16, 0, -32, 0, 48, 16, -32},
    {-16, 0, 8, 0, 0, 16, 0, -32, 16, 48, -32},
    {8, 8, 0, 0, 0, 0, 16, 16, -32, -32, 48},
};

std::array<int, kDimension> current{};
std::array<int, kDimension> minimizer{};
std::uint64_t checked = 0;
std::int64_t minimum = std::numeric_limits<std::int64_t>::max();

std::int64_t quadratic_form() {
  std::int64_t value = 0;
  for (int row = 0; row < kDimension; ++row) {
    for (int column = 0; column < kDimension; ++column) {
      value += std::int64_t(current[row]) * kGram[row][column] * current[column];
    }
  }
  return value;
}

bool canonical_up_to_sign() {
  for (int value : current) {
    if (value != 0) return value > 0;
  }
  return false;
}

void enumerate(int coordinate, int remaining_squared_norm) {
  if (coordinate == kDimension) {
    if (!canonical_up_to_sign()) return;
    ++checked;
    const std::int64_t value = quadratic_form();
    if (value < minimum) {
      minimum = value;
      minimizer = current;
    }
    return;
  }

  int radius = 0;
  while ((radius + 1) * (radius + 1) <= remaining_squared_norm) ++radius;
  for (int value = -radius; value <= radius; ++value) {
    current[coordinate] = value;
    enumerate(coordinate + 1, remaining_squared_norm - value * value);
  }
}

int main() {
  enumerate(0, 31);
  std::cout << "vectors_checked_up_to_sign=" << checked << '\n';
  std::cout << "minimum=" << minimum << '\n';
  std::cout << "minimizer=[";
  for (int index = 0; index < kDimension; ++index) {
    if (index) std::cout << ',';
    std::cout << minimizer[index];
  }
  std::cout << "]\n";
  if (minimum != 32) return 1;
  return 0;
}
