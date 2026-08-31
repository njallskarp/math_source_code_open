#include <array>
#include <cstdint>
#include <iostream>
#include <limits>

// The exact verifier proves M-I positive definite for the coefficientwise-even
// residual lattice.  Hence x^T M x <= 48 implies ||x||^2 < 48.  The Gram
// matrix splits into independent 5- and 6-dimensional blocks; the minimum of
// their nonzero minima is the minimum of the full orthogonal direct sum.

constexpr int kCoordinateRadiusSquared = 47;

template <int Dimension>
struct BlockSearch {
  std::array<std::array<std::int64_t, Dimension>, Dimension> gram;
  std::array<int, Dimension> current{};
  std::array<int, Dimension> minimizer{};
  std::uint64_t checked = 0;
  std::uint64_t norm_32_count = 0;
  std::int64_t minimum = std::numeric_limits<std::int64_t>::max();

  std::int64_t quadratic_form() const {
    std::int64_t value = 0;
    for (int row = 0; row < Dimension; ++row) {
      for (int column = 0; column < Dimension; ++column) {
        value += std::int64_t(current[row]) * gram[row][column] * current[column];
      }
    }
    return value;
  }

  bool canonical_up_to_sign() const {
    for (int value : current) {
      if (value != 0) return value > 0;
    }
    return false;
  }

  void enumerate(int coordinate, int remaining_squared_norm) {
    if (coordinate == Dimension) {
      if (!canonical_up_to_sign()) return;
      ++checked;
      const std::int64_t value = quadratic_form();
      if (value == 32) {
        ++norm_32_count;
        std::cout << "norm_32_vector=[";
        for (int index = 0; index < Dimension; ++index) {
          if (index) std::cout << ',';
          std::cout << current[index];
        }
        std::cout << "]\n";
      }
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
};

template <int Dimension>
void print_result(const char* name, const BlockSearch<Dimension>& search) {
  std::cout << name << "_vectors_checked_up_to_sign=" << search.checked << '\n';
  std::cout << name << "_minimum=" << search.minimum << '\n';
  std::cout << name << "_norm_32_count_up_to_sign=" << search.norm_32_count << '\n';
  std::cout << name << "_minimizer=[";
  for (int index = 0; index < Dimension; ++index) {
    if (index) std::cout << ',';
    std::cout << search.minimizer[index];
  }
  std::cout << "]\n";
}

int main() {
  BlockSearch<5> real_block{{{{96, -80, 64, -48, 32},
                              {-80, 128, -112, 64, -16},
                              {64, -112, 128, -80, 32},
                              {-48, 64, -80, 96, -64},
                              {32, -16, 32, -64, 64}}}};
  BlockSearch<6> imaginary_block{{{{96, -48, 0, 48, -32, 16},
                                   {-48, 64, -16, 0, 16, 0},
                                   {0, -16, 64, -48, 32, 0},
                                   {48, 0, -48, 96, -64, 32},
                                   {-32, 16, 32, -64, 128, -64},
                                   {16, 0, 0, 32, -64, 48}}}};
  real_block.enumerate(0, kCoordinateRadiusSquared);
  imaginary_block.enumerate(0, kCoordinateRadiusSquared);
  print_result("real_block", real_block);
  print_result("imaginary_block", imaginary_block);
  const std::int64_t full_minimum = std::min(real_block.minimum, imaginary_block.minimum);
  std::cout << "full_lattice_minimum=" << full_minimum << '\n';
  return full_minimum == 32 ? 0 : 1;
}
