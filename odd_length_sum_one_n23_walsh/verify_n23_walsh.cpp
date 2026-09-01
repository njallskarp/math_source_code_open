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

constexpr int N = 23;
constexpr int DIM = 11;
constexpr int SYNDROMES = 1 << DIM;
constexpr std::uint32_t FULL = (std::uint32_t{1} << N) - 1;
constexpr std::uint16_t NORMAL = (std::uint16_t{1} << DIM) - 1;

std::array<std::array<std::int64_t, N + 1>, N + 1> binomial{};

std::uint32_t rotate(std::uint32_t mask) {
  return ((mask << 1) | (mask >> (N - 1))) & FULL;
}

std::array<std::uint32_t, DIM> d_rows(std::uint32_t b) {
  std::array<std::uint32_t, DIM> rows{};
  for (int shift = 1; shift <= DIM; ++shift) {
    for (int index = 0; index < N; ++index) {
      const int plus = (index + shift) % N;
      const int minus = (index - shift + N) % N;
      rows[shift - 1] |= (((b >> plus) ^ (b >> minus)) & 1u) << index;
    }
  }
  return rows;
}

std::array<std::uint16_t, N> d_columns(
    const std::array<std::uint32_t, DIM>& rows) {
  std::array<std::uint16_t, N> columns{};
  for (int index = 0; index < N; ++index) {
    for (int row = 0; row < DIM; ++row) {
      columns[index] |= ((rows[row] >> index) & 1u) << row;
    }
  }
  return columns;
}

std::vector<std::uint16_t> column_basis(
    const std::array<std::uint16_t, N>& columns) {
  std::array<std::uint16_t, DIM> pivots{};
  std::vector<std::uint16_t> basis;
  for (const auto original : columns) {
    auto value = original;
    while (value) {
      const int pivot = std::bit_width(value) - 1;
      if (pivots[pivot]) {
        value ^= pivots[pivot];
      } else {
        pivots[pivot] = value;
        basis.push_back(value);
        break;
      }
    }
  }
  return basis;
}

std::array<bool, SYNDROMES> image_from_basis(
    const std::vector<std::uint16_t>& basis) {
  std::array<bool, SYNDROMES> image{};
  std::vector<std::uint16_t> values{0};
  for (const auto vector : basis) {
    const auto size = values.size();
    for (std::size_t i = 0; i < size; ++i) values.push_back(values[i] ^ vector);
  }
  for (const auto value : values) image[value] = true;
  return image;
}

std::int64_t krawtchouk(int n, int marked, int choose) {
  std::int64_t result = 0;
  for (int selected_marked = 0; selected_marked <= choose; ++selected_marked) {
    const int selected_unmarked = choose - selected_marked;
    if (selected_marked > marked || selected_unmarked > n - marked) continue;
    const auto term = binomial[marked][selected_marked] *
                      binomial[n - marked][selected_unmarked];
    result += (selected_marked & 1) ? -term : term;
  }
  return result;
}

void walsh_hadamard(std::array<std::int64_t, SYNDROMES>& values) {
  for (int width = 1; width < SYNDROMES; width <<= 1) {
    for (int start = 0; start < SYNDROMES; start += 2 * width) {
      for (int offset = 0; offset < width; ++offset) {
        const auto left = values[start + offset];
        const auto right = values[start + width + offset];
        values[start + offset] = left + right;
        values[start + width + offset] = left - right;
      }
    }
  }
}

std::array<std::int64_t, SYNDROMES> exact_sum_one_fibers(
    std::uint32_t b, const std::array<std::uint32_t, DIM>& rows) {
  const int imaginary = std::popcount(b);
  if (imaginary & 1) throw std::runtime_error("odd axis weight");
  const int real = N - imaginary;
  const int negative_real = (real - 1) / 2;
  const int negative_imaginary = imaginary / 2;

  std::array<std::uint32_t, SYNDROMES> pullback{};
  std::array<std::int64_t, SYNDROMES> transform{};
  for (int character = 1; character < SYNDROMES; ++character) {
    const unsigned least = std::countr_zero(static_cast<unsigned>(character));
    pullback[character] = pullback[character ^ (1 << least)] ^ rows[least];
  }
  for (int character = 0; character < SYNDROMES; ++character) {
    const auto q = pullback[character];
    transform[character] =
        krawtchouk(real, std::popcount(q & (FULL ^ b)), negative_real) *
        krawtchouk(imaginary, std::popcount(q & b), negative_imaginary);
  }
  walsh_hadamard(transform);
  for (auto& value : transform) {
    if (value % SYNDROMES != 0) throw std::runtime_error("nonintegral fiber");
    value /= SYNDROMES;
    if (value < 0) throw std::runtime_error("negative fiber");
  }
  return transform;
}

void emit_record(std::uint32_t b, int orbit_size, int rank,
                 std::uint16_t origin, int rhs) {
  std::cout << std::hex << std::setfill('0') << std::setw(6) << b << '\t'
            << std::dec << orbit_size << '\t' << rank << '\t'
            << std::hex << std::setw(3) << origin << '\t' << std::setw(3)
            << NORMAL << '\t' << std::dec << rhs << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  const bool stream = argc == 2 && std::string(argv[1]) == "--stream";
  if (argc > 2 || (argc == 2 && !stream)) {
    std::cerr << "usage: verify_n23_walsh [--stream]\n";
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

  std::vector<std::uint8_t> seen(std::uint32_t{1} << N, 0);
  std::map<int, std::uint64_t> rank_orbits;
  std::uint64_t even_words = 0;
  std::uint64_t even_orbits = 0;
  std::uint64_t labeled_syndromes = 0;
  std::uint64_t orbit_syndromes = 0;
  std::uint64_t exact_sign_words = 0;
  std::uint64_t rhs_zero_orbits = 0;
  std::uint64_t rhs_one_orbits = 0;

  for (std::uint32_t mask = 0; mask < (std::uint32_t{1} << N); ++mask) {
    if (seen[mask]) continue;
    std::uint32_t value = mask;
    int orbit_size = 0;
    do {
      seen[value] = 1;
      ++orbit_size;
      value = rotate(value);
    } while (value != mask);
    if (std::popcount(mask) & 1) continue;

    const auto rows = d_rows(mask);
    std::uint32_t row_xor = 0;
    for (const auto row : rows) row_xor ^= row;
    if (row_xor != mask) throw std::runtime_error("universal parity normal failed");
    const auto columns = d_columns(rows);
    const auto basis = column_basis(columns);
    const int rank = static_cast<int>(basis.size());
    if ((mask == 0 && rank != 0) || (mask != 0 && rank != DIM)) {
      throw std::runtime_error("prime-23 rank dichotomy failed");
    }
    const auto image = image_from_basis(basis);
    const auto fibers = exact_sum_one_fibers(mask, rows);
    const int rhs = (std::popcount(mask) / 2) & 1;
    std::uint64_t support_size = 0;
    std::uint64_t fiber_total = 0;
    std::uint16_t origin = 0;
    bool have_origin = false;
    for (int syndrome = 0; syndrome < SYNDROMES; ++syndrome) {
      const bool expected = image[syndrome] &&
          ((std::popcount(static_cast<unsigned>(syndrome)) & 1) == rhs);
      const bool present = fibers[syndrome] > 0;
      if (present != expected) throw std::runtime_error("sum-one slice failed");
      fiber_total += fibers[syndrome];
      if (present) {
        ++support_size;
        if (!have_origin) {
          have_origin = true;
          origin = static_cast<std::uint16_t>(syndrome);
        }
      }
    }
    const int weight = std::popcount(mask);
    const auto expected_fiber_total = static_cast<std::uint64_t>(
        binomial[N - weight][(N - weight - 1) / 2] *
        binomial[weight][weight / 2]);
    if (!have_origin || fiber_total != expected_fiber_total) {
      throw std::runtime_error("fixed-cardinality total failed");
    }

    even_words += orbit_size;
    ++even_orbits;
    labeled_syndromes += orbit_size * support_size;
    orbit_syndromes += support_size;
    exact_sign_words += orbit_size * fiber_total;
    ++rank_orbits[rank];
    rhs ? ++rhs_one_orbits : ++rhs_zero_orbits;
    if (stream) emit_record(mask, orbit_size, rank, origin, rhs);
  }

  const std::map<int, std::uint64_t> expected_ranks = {{0, 1}, {11, 182'361}};
  if (even_words != 4'194'304 || even_orbits != 182'362 ||
      labeled_syndromes != 4'294'966'273ULL ||
      orbit_syndromes != 186'737'665 || rank_orbits != expected_ranks) {
    throw std::runtime_error("published n=23 census mismatch");
  }
  if (!stream) {
    std::cout << "even_axis_words=" << even_words << '\n';
    std::cout << "even_axis_rotation_orbits=" << even_orbits << '\n';
    std::cout << "rank_0_orbits=" << rank_orbits[0] << '\n';
    std::cout << "rank_11_orbits=" << rank_orbits[11] << '\n';
    std::cout << "rhs_zero_orbits=" << rhs_zero_orbits << '\n';
    std::cout << "rhs_one_orbits=" << rhs_one_orbits << '\n';
    std::cout << "labeled_syndromes=" << labeled_syndromes << '\n';
    std::cout << "orbit_syndromes=" << orbit_syndromes << '\n';
    std::cout << "exact_sum_one_sign_words=" << exact_sign_words << '\n';
    std::cout << "prime_23_rank_dichotomy=verified\n";
    std::cout << "exact_support_equation=verified\n";
    std::cout << "certificate=verified\n";
  }
}
