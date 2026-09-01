#include <array>
#include <bit>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int N = 21;
constexpr int DIM = 10;
constexpr std::uint32_t FULL = (1u << N) - 1;
constexpr std::uint16_t UNIVERSAL_NORMAL = (1u << DIM) - 1;

std::array<std::array<std::int64_t, 22>, 22> binomial{};

std::uint32_t rotate(std::uint32_t mask, int shift) {
  return ((mask << shift) | (mask >> (N - shift))) & FULL;
}

int binary_rank(std::vector<std::uint32_t> rows) {
  int rank = 0;
  for (int column = N - 1; column >= 0; --column) {
    int pivot = -1;
    for (int row = rank; row < static_cast<int>(rows.size()); ++row) {
      if ((rows[row] >> column) & 1u) {
        pivot = row;
        break;
      }
    }
    if (pivot < 0) continue;
    std::swap(rows[rank], rows[pivot]);
    for (int row = 0; row < static_cast<int>(rows.size()); ++row) {
      if (row != rank && ((rows[row] >> column) & 1u)) rows[row] ^= rows[rank];
    }
    ++rank;
  }
  return rank;
}

std::vector<std::uint32_t> d_rows(std::uint32_t b) {
  std::vector<std::uint32_t> rows;
  rows.reserve(DIM);
  for (int shift = 1; shift <= DIM; ++shift) {
    std::uint32_t row = 0;
    for (int index = 0; index < N; ++index) {
      const int plus = (index + shift) % N;
      const int minus = (index - shift + N) % N;
      const std::uint32_t bit = ((b >> plus) ^ (b >> minus)) & 1u;
      row |= bit << index;
    }
    rows.push_back(row);
  }
  return rows;
}

std::array<bool, 1 << DIM> image_of_d(const std::vector<std::uint32_t>& rows) {
  std::array<bool, 1 << DIM> image{};
  image[0] = true;
  for (int index = 0; index < N; ++index) {
    std::uint16_t column = 0;
    for (int shift = 0; shift < DIM; ++shift) {
      column |= ((rows[shift] >> index) & 1u) << shift;
    }
    const auto before = image;
    for (int value = 0; value < (1 << DIM); ++value) {
      if (before[value]) image[value ^ column] = true;
    }
  }
  return image;
}

std::int64_t krawtchouk(int n, int negatives, int choose) {
  std::int64_t result = 0;
  for (int selected_negative = 0; selected_negative <= choose; ++selected_negative) {
    const int selected_positive = choose - selected_negative;
    if (selected_negative > negatives || selected_positive > n - negatives) continue;
    const std::int64_t term = binomial[negatives][selected_negative] *
                              binomial[n - negatives][selected_positive];
    result += (selected_negative & 1) ? -term : term;
  }
  return result;
}

void walsh_hadamard(std::array<std::int64_t, 1 << DIM>& values) {
  for (int width = 1; width < (1 << DIM); width <<= 1) {
    for (int start = 0; start < (1 << DIM); start += 2 * width) {
      for (int offset = 0; offset < width; ++offset) {
        const auto left = values[start + offset];
        const auto right = values[start + width + offset];
        values[start + offset] = left + right;
        values[start + width + offset] = left - right;
      }
    }
  }
}

std::array<std::int64_t, 1 << DIM> exact_sum_one_fibers(
    std::uint32_t b, const std::vector<std::uint32_t>& rows) {
  const int imaginary = std::popcount(b);
  if (imaginary & 1) throw std::runtime_error("odd axis weight");
  const int real = N - imaginary;
  const int negative_real = (real - 1) / 2;
  const int negative_imaginary = imaginary / 2;

  std::array<std::int64_t, 1 << DIM> transform{};
  for (int character = 0; character < (1 << DIM); ++character) {
    std::uint32_t pullback = 0;
    for (int bit = 0; bit < DIM; ++bit) {
      if ((character >> bit) & 1) pullback ^= rows[bit];
    }
    transform[character] =
        krawtchouk(real, std::popcount(pullback & (FULL ^ b)), negative_real) *
        krawtchouk(imaginary, std::popcount(pullback & b), negative_imaginary);
  }
  walsh_hadamard(transform);
  for (auto& value : transform) {
    if (value % (1 << DIM) != 0) throw std::runtime_error("nonintegral fiber");
    value /= (1 << DIM);
    if (value < 0) throw std::runtime_error("negative fiber");
  }
  return transform;
}

void emit_stream_record(std::uint32_t b, int orbit_size, int rank,
                        std::uint16_t origin, int rhs) {
  std::cout << std::hex << std::setfill('0') << std::setw(6) << b << '\t'
            << std::dec << orbit_size << '\t' << rank << '\t'
            << std::hex << std::setw(3) << origin << '\t' << std::setw(3)
            << UNIVERSAL_NORMAL << '\t' << std::dec << rhs << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  const bool stream = argc == 2 && std::string(argv[1]) == "--stream";
  if (argc > 2 || (argc == 2 && !stream)) {
    std::cerr << "usage: verify_hyperplane_equation [--stream]\n";
    return 2;
  }

  binomial[0][0] = 1;
  for (int n = 1; n <= N; ++n) {
    binomial[n][0] = binomial[n][n] = 1;
    for (int k = 1; k < n; ++k) {
      binomial[n][k] = binomial[n - 1][k - 1] + binomial[n - 1][k];
    }
  }

  if (stream) {
    std::cout << "axis_word\torbit_size\trank\torigin\tnormal\trhs\n";
  }

  std::vector<std::uint8_t> seen(1u << N, 0);
  std::map<int, std::uint64_t> rank_orbits;
  std::uint64_t even_words = 0;
  std::uint64_t even_orbits = 0;
  std::uint64_t rhs_zero_orbits = 0;
  std::uint64_t rhs_one_orbits = 0;

  for (std::uint32_t mask = 0; mask < (1u << N); ++mask) {
    if (seen[mask]) continue;
    std::vector<std::uint32_t> orbit;
    std::uint32_t value = mask;
    do {
      orbit.push_back(value);
      seen[value] = 1;
      value = rotate(value, 1);
    } while (value != mask);

    if (std::popcount(mask) & 1) continue;
    const auto rows = d_rows(mask);
    std::uint32_t row_xor = 0;
    for (const auto row : rows) row_xor ^= row;
    if (row_xor != mask) throw std::runtime_error("universal-normal identity failed");

    const int rank = binary_rank(rows);
    const int rhs = (std::popcount(mask) / 2) & 1;
    const auto image = image_of_d(rows);
    const auto fibers = exact_sum_one_fibers(mask, rows);
    std::uint16_t origin = 0;
    bool have_origin = false;
    int expected_support_size = 0;
    for (int syndrome = 0; syndrome < (1 << DIM); ++syndrome) {
      const bool expected =
          image[syndrome] && ((std::popcount(static_cast<unsigned>(syndrome)) & 1) == rhs);
      const bool present = fibers[syndrome] > 0;
      if (present != expected) throw std::runtime_error("hyperplane equation failed");
      if (expected) {
        ++expected_support_size;
        if (!have_origin) {
          origin = static_cast<std::uint16_t>(syndrome);
          have_origin = true;
        }
      }
    }
    const int required_size = rank == 0 ? 1 : (1 << (rank - 1));
    if (!have_origin || expected_support_size != required_size) {
      throw std::runtime_error("hyperplane cardinality failed");
    }

    even_words += orbit.size();
    ++even_orbits;
    ++rank_orbits[rank];
    rhs ? ++rhs_one_orbits : ++rhs_zero_orbits;
    if (stream) emit_stream_record(mask, static_cast<int>(orbit.size()), rank, origin, rhs);
  }

  const std::map<int, std::uint64_t> expected_rank_orbits = {
      {0, 1}, {1, 1}, {3, 9}, {4, 9}, {6, 195}, {7, 585},
      {9, 12285}, {10, 36855}};
  if (even_words != (1u << 20) || even_orbits != 49'940 ||
      rank_orbits != expected_rank_orbits) {
    throw std::runtime_error("orbit census mismatch");
  }

  if (!stream) {
    std::cout << "even_axis_words=" << even_words << '\n';
    std::cout << "even_axis_rotation_orbits=" << even_orbits << '\n';
    std::cout << "rhs_zero_orbits=" << rhs_zero_orbits << '\n';
    std::cout << "rhs_one_orbits=" << rhs_one_orbits << '\n';
    std::cout << "universal_normal=3ff\n";
    std::cout << "row_xor_equals_axis_word=verified\n";
    std::cout << "exact_support_equation=verified\n";
    std::cout << "canonical_stream_records=" << even_orbits << '\n';
    std::cout << "certificate=verified\n";
  }
}
