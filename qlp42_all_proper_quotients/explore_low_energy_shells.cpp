#include <algorithm>
#include <array>
#include <cmath>
#include <complex>
#include <cstdint>
#include <iostream>
#include <limits>

constexpr int kDimension = 11;
constexpr int kLength = 42;
constexpr int kEnergyLimit = 128;
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
std::array<std::array<long double, kDimension>, kDimension> lower{};
std::array<long double, kDimension> diagonal{};
std::array<std::uint64_t, kEnergyLimit / 16 + 1> shell_count{};
std::array<long double, kEnergyLimit / 16 + 1> best_min_fourier{};
std::array<std::array<int, kDimension>, kEnergyLimit / 16 + 1> best_vectors{};
std::uint64_t enumerated = 0;

std::int64_t exact_energy() {
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

long double minimum_primitive_fourier_value() {
  const auto e = residual();
  constexpr int primitive[12] = {1, 5, 11, 13, 17, 19, 23, 25, 29, 31, 37, 41};
  const long double pi = std::acos(-1.0L);
  long double minimum = std::numeric_limits<long double>::infinity();
  for (int frequency : primitive) {
    std::complex<long double> value{};
    for (int shift = 0; shift < kLength; ++shift) {
      const long double angle = 2.0L * pi * frequency * shift / kLength;
      value += std::complex<long double>(e[shift].real(), e[shift].imag()) *
               std::complex<long double>(std::cos(angle), std::sin(angle));
    }
    if (std::abs(value.imag()) > 1e-12L) std::exit(2);
    minimum = std::min(minimum, value.real());
  }
  return minimum;
}

void record_leaf() {
  if (!canonical_up_to_sign()) return;
  ++enumerated;
  const std::int64_t energy = exact_energy();
  if (energy <= 0 || energy > kEnergyLimit || energy % 16 != 0) return;
  const int shell = static_cast<int>(energy / 16);
  ++shell_count[shell];
  const long double minimum = minimum_primitive_fourier_value();
  if (minimum > best_min_fourier[shell]) {
    best_min_fourier[shell] = minimum;
    best_vectors[shell] = current;
  }
}

void enumerate(int coordinate, long double used) {
  if (coordinate < 0) {
    record_leaf();
    return;
  }
  long double center = 0;
  for (int later = coordinate + 1; later < kDimension; ++later) {
    center += lower[later][coordinate] * current[later];
  }
  const long double remaining = kEnergyLimit - used;
  if (remaining < -1e-12L) return;
  const long double radius = std::sqrt(std::max(0.0L, remaining / diagonal[coordinate]));
  const int first = static_cast<int>(std::ceil(-center - radius - 1e-10L));
  const int last = static_cast<int>(std::floor(-center + radius + 1e-10L));
  for (int value = first; value <= last; ++value) {
    current[coordinate] = value;
    const long double shifted = value + center;
    enumerate(coordinate - 1, used + diagonal[coordinate] * shifted * shifted);
  }
}

void compute_ldl() {
  for (int row = 0; row < kDimension; ++row) {
    lower[row][row] = 1;
    diagonal[row] = kGram[row][row];
    for (int k = 0; k < row; ++k) {
      diagonal[row] -= lower[row][k] * lower[row][k] * diagonal[k];
    }
    for (int future = row + 1; future < kDimension; ++future) {
      long double numerator = kGram[future][row];
      for (int k = 0; k < row; ++k) {
        numerator -= lower[future][k] * lower[row][k] * diagonal[k];
      }
      lower[future][row] = numerator / diagonal[row];
    }
  }
}

int main() {
  best_min_fourier.fill(-std::numeric_limits<long double>::infinity());
  compute_ldl();
  enumerate(kDimension - 1, 0);
  std::cout.precision(20);
  std::cout << "enumerated_nonzero_up_to_sign=" << enumerated << '\n';
  for (int shell = 1; shell <= kEnergyLimit / 16; ++shell) {
    if (!shell_count[shell]) continue;
    std::cout << "energy=" << 16 * shell << " count=" << shell_count[shell]
              << " best_min_primitive_fourier=" << best_min_fourier[shell]
              << " best_vector=[";
    for (int index = 0; index < kDimension; ++index) {
      if (index) std::cout << ',';
      std::cout << best_vectors[shell][index];
    }
    std::cout << "]\n";
  }
}
