#include <array>
#include <cmath>
#include <complex>
#include <cstdint>
#include <iostream>
#include <limits>
#include <vector>

constexpr int kDimension = 11;
constexpr int kLength = 42;
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

constexpr int kProperFactor[31] = {
    -1, 1, -1, 0, 0, 0, 0, -1, 1, -1, 0, 0, 0, 0, 0, 0,
    0,  0, 0,  0, 0, 1, -1, 1, 0, 0, 0, 0, 1, -1, 1,
};

std::array<int, kDimension> current{};
std::uint64_t checked = 0;
std::uint64_t shell_count_up_to_sign = 0;
double worst_shell_minimum = std::numeric_limits<double>::infinity();
double best_shell_minimum = -std::numeric_limits<double>::infinity();
std::array<int, kDimension> best_vector{};

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

std::array<std::complex<int>, kLength> residual() {
  std::array<std::complex<int>, 12> g{};
  for (int k = 1; k <= 5; ++k) {
    const int a = current[2 * (k - 1)];
    const int b = current[2 * (k - 1) + 1];
    g[k] = {a, b};
    g[12 - k] = {b, a};
  }
  g[6] = {current[10], current[10]};

  std::array<std::complex<int>, 12> h{};
  for (int k = 0; k < 12; ++k) {
    h[k] = {g[k].real() - g[k].imag(), g[k].real() + g[k].imag()};
  }

  std::array<std::complex<int>, kLength> e{};
  for (int p = 0; p <= 30; ++p) {
    for (int h_index = 0; h_index < 12; ++h_index) {
      e[p + h_index] += kProperFactor[p] * h[h_index];
    }
  }
  return e;
}

double minimum_primitive_fourier_value() {
  const auto e = residual();
  constexpr int primitive[12] = {1, 5, 11, 13, 17, 19, 23, 25, 29, 31, 37, 41};
  const double pi = std::acos(-1.0);
  double minimum = std::numeric_limits<double>::infinity();
  for (int frequency : primitive) {
    std::complex<double> value{};
    for (int shift = 0; shift < kLength; ++shift) {
      const double angle = 2.0 * pi * frequency * shift / kLength;
      value += std::complex<double>(e[shift].real(), e[shift].imag()) *
               std::complex<double>(std::cos(angle), std::sin(angle));
    }
    if (std::abs(value.imag()) > 1e-8) {
      std::cerr << "non-real Fourier value\n";
      std::exit(2);
    }
    minimum = std::min(minimum, value.real());
  }
  return minimum;
}

void enumerate(int coordinate, int remaining_squared_norm) {
  if (coordinate == kDimension) {
    if (!canonical_up_to_sign()) return;
    ++checked;
    if (quadratic_form() != 32) return;
    ++shell_count_up_to_sign;
    const double shell_minimum = minimum_primitive_fourier_value();
    worst_shell_minimum = std::min(worst_shell_minimum, shell_minimum);
    if (shell_minimum > best_shell_minimum) {
      best_shell_minimum = shell_minimum;
      best_vector = current;
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
  std::cout.precision(17);
  std::cout << "vectors_checked_up_to_sign=" << checked << '\n';
  std::cout << "norm_32_vectors_up_to_sign=" << shell_count_up_to_sign << '\n';
  std::cout << "worst_min_primitive_fourier=" << worst_shell_minimum << '\n';
  std::cout << "best_min_primitive_fourier=" << best_shell_minimum << '\n';
  std::cout << "best_vector=[";
  for (int index = 0; index < kDimension; ++index) {
    if (index) std::cout << ',';
    std::cout << best_vector[index];
  }
  std::cout << "]\n";
}
