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

constexpr int MAX_N = 21;
constexpr int MAX_DIM = 10;
constexpr int SYNDROMES = 1 << MAX_DIM;
constexpr int WORDS = SYNDROMES / 64;

struct Bits {
  std::array<std::uint64_t, WORDS> words{};

  void set(int bit) { words[bit >> 6] |= std::uint64_t{1} << (bit & 63); }
  bool test(int bit) const { return (words[bit >> 6] >> (bit & 63)) & 1u; }
  std::uint64_t count() const {
    std::uint64_t result = 0;
    for (auto word : words) result += std::popcount(word);
    return result;
  }
  Bits& operator|=(const Bits& other) {
    for (int i = 0; i < WORDS; ++i) words[i] |= other.words[i];
    return *this;
  }
  bool operator==(const Bits&) const = default;
};

std::uint64_t permute_xor_64(std::uint64_t value, unsigned mask) {
  if (mask & 1u) {
    value = ((value & 0xaaaaaaaaaaaaaaaaULL) >> 1) |
            ((value & 0x5555555555555555ULL) << 1);
  }
  if (mask & 2u) {
    value = ((value & 0xccccccccccccccccULL) >> 2) |
            ((value & 0x3333333333333333ULL) << 2);
  }
  if (mask & 4u) {
    value = ((value & 0xf0f0f0f0f0f0f0f0ULL) >> 4) |
            ((value & 0x0f0f0f0f0f0f0f0fULL) << 4);
  }
  if (mask & 8u) {
    value = ((value & 0xff00ff00ff00ff00ULL) >> 8) |
            ((value & 0x00ff00ff00ff00ffULL) << 8);
  }
  if (mask & 16u) {
    value = ((value & 0xffff0000ffff0000ULL) >> 16) |
            ((value & 0x0000ffff0000ffffULL) << 16);
  }
  if (mask & 32u) return (value >> 32) | (value << 32);
  return value;
}

Bits translate_xor(const Bits& input, std::uint16_t mask) {
  Bits output;
  const int word_mask = mask >> 6;
  const unsigned bit_mask = mask & 63u;
  for (int word = 0; word < WORDS; ++word) {
    output.words[word ^ word_mask] = permute_xor_64(input.words[word], bit_mask);
  }
  return output;
}

std::vector<Bits> subset_xor_by_size(const std::vector<std::uint16_t>& columns) {
  std::vector<Bits> supports(columns.size() + 1);
  supports[0].set(0);
  int used = 0;
  for (const auto column : columns) {
    ++used;
    for (int size = used; size > 0; --size) {
      supports[size] |= translate_xor(supports[size - 1], column);
    }
  }
  return supports;
}

Bits xor_sumset(const Bits& left, const Bits& right) {
  const Bits* sparse = &left;
  const Bits* other = &right;
  if (left.count() > right.count()) std::swap(sparse, other);
  Bits result;
  for (int word = 0; word < WORDS; ++word) {
    auto value = sparse->words[word];
    while (value) {
      const int bit = std::countr_zero(value);
      result |= translate_xor(*other, static_cast<std::uint16_t>(64 * word + bit));
      value &= value - 1;
    }
  }
  return result;
}

std::uint32_t rotate(std::uint32_t mask, int n) {
  const std::uint32_t full = (std::uint32_t{1} << n) - 1;
  return ((mask << 1) | (mask >> (n - 1))) & full;
}

std::vector<std::uint16_t> d_columns(std::uint32_t b, int n) {
  const int dim = (n - 1) / 2;
  std::vector<std::uint16_t> columns;
  columns.reserve(n);
  for (int index = 0; index < n; ++index) {
    std::uint16_t column = 0;
    for (int shift = 1; shift <= dim; ++shift) {
      const int plus = (index + shift) % n;
      const int minus = (index - shift + n) % n;
      column |= (((b >> plus) ^ (b >> minus)) & 1u) << (shift - 1);
    }
    columns.push_back(column);
  }
  return columns;
}

int binary_rank(const std::vector<std::uint16_t>& columns, int dim) {
  std::array<std::uint16_t, MAX_DIM> basis{};
  int rank = 0;
  for (auto value : columns) {
    while (value) {
      const int pivot = std::bit_width(value) - 1;
      if (basis[pivot]) {
        value ^= basis[pivot];
      } else {
        basis[pivot] = value;
        ++rank;
        break;
      }
    }
  }
  if (rank > dim) throw std::runtime_error("rank exceeds syndrome dimension");
  return rank;
}

Bits image_of_d(const std::vector<std::uint16_t>& columns) {
  Bits image;
  image.set(0);
  for (const auto column : columns) image |= translate_xor(image, column);
  return image;
}

Bits exact_sum_one_support(std::uint32_t b, int n,
                           const std::vector<std::uint16_t>& columns) {
  const int weight = std::popcount(b);
  if (weight & 1) throw std::runtime_error("sum one requires even axis weight");
  std::vector<std::uint16_t> real;
  std::vector<std::uint16_t> imaginary;
  for (int index = 0; index < n; ++index) {
    (((b >> index) & 1u) ? imaginary : real).push_back(columns[index]);
  }
  const int negative_real = (n - weight - 1) / 2;
  const int negative_imaginary = weight / 2;
  const auto real_supports = subset_xor_by_size(real);
  const auto imaginary_supports = subset_xor_by_size(imaginary);
  return xor_sumset(real_supports[negative_real],
                    imaginary_supports[negative_imaginary]);
}

struct Census {
  std::uint64_t even_words = 0;
  std::uint64_t even_orbits = 0;
  std::uint64_t labeled_syndromes = 0;
  std::uint64_t orbit_syndromes = 0;
  std::uint64_t rhs_zero_orbits = 0;
  std::uint64_t rhs_one_orbits = 0;
  std::map<int, std::uint64_t> rank_orbits;
};

void emit_q41_record(std::uint32_t b, int orbit_size, int rank,
                     std::uint16_t origin, int rhs) {
  std::cout << std::hex << std::setfill('0') << std::setw(6) << b << '\t'
            << std::dec << orbit_size << '\t' << rank << '\t'
            << std::hex << std::setw(3) << origin << '\t' << std::setw(3)
            << ((1u << MAX_DIM) - 1) << '\t' << std::dec << rhs << '\n';
}

Census verify_length(int n, bool stream_q41) {
  const int dim = (n - 1) / 2;
  std::vector<std::uint8_t> seen(std::uint32_t{1} << n, 0);
  Census census;
  for (std::uint32_t mask = 0; mask < (std::uint32_t{1} << n); ++mask) {
    if (seen[mask]) continue;
    std::uint32_t value = mask;
    int orbit_size = 0;
    do {
      seen[value] = 1;
      ++orbit_size;
      value = rotate(value, n);
    } while (value != mask);
    if (std::popcount(mask) & 1) continue;

    const auto columns = d_columns(mask, n);
    std::uint16_t column_xor = 0;
    for (const auto column : columns) column_xor ^= column;
    if (column_xor != 0) throw std::runtime_error("D_b(1) is nonzero");

    const auto image = image_of_d(columns);
    const auto support = exact_sum_one_support(mask, n, columns);
    const int rhs = (std::popcount(mask) / 2) & 1;
    Bits expected;
    std::uint16_t origin = 0;
    bool have_origin = false;
    for (int syndrome = 0; syndrome < (1 << dim); ++syndrome) {
      if (image.test(syndrome) && ((std::popcount(static_cast<unsigned>(syndrome)) & 1) == rhs)) {
        expected.set(syndrome);
        if (!have_origin) {
          origin = static_cast<std::uint16_t>(syndrome);
          have_origin = true;
        }
      }
    }
    if (!(support == expected) || !have_origin) {
      throw std::runtime_error("exact sum-one support is not the parity slice");
    }

    const int rank = binary_rank(columns, dim);
    const auto support_size = support.count();
    const std::uint64_t required = rank == 0 ? 1 : (std::uint64_t{1} << (rank - 1));
    if (support_size != required) throw std::runtime_error("support cardinality mismatch");

    census.even_words += orbit_size;
    ++census.even_orbits;
    census.labeled_syndromes += orbit_size * support_size;
    census.orbit_syndromes += support_size;
    ++census.rank_orbits[rank];
    rhs ? ++census.rhs_one_orbits : ++census.rhs_zero_orbits;
    if (stream_q41) emit_q41_record(mask, orbit_size, rank, origin, rhs);
  }
  if (census.even_words != (std::uint64_t{1} << (n - 1))) {
    throw std::runtime_error("even-word census mismatch");
  }
  return census;
}

}  // namespace

int main(int argc, char** argv) {
  const bool stream = argc == 2 && std::string(argv[1]) == "--q41-stream";
  if (argc > 2 || (argc == 2 && !stream)) {
    std::cerr << "usage: verify_sum_one_subset_xor [--q41-stream]\n";
    return 2;
  }
  if (stream) {
    std::cout << "axis_word\torbit_size\trank\torigin\tnormal\trhs\n";
  }

  Census q41;
  for (int n = 3; n <= MAX_N; n += 2) {
    const auto census = verify_length(n, stream && n == MAX_N);
    if (n == MAX_N) q41 = census;
    if (!stream) {
      std::cout << "n=" << n << " even_axis_words=" << census.even_words
                << " even_axis_rotation_orbits=" << census.even_orbits
                << " labeled_syndromes=" << census.labeled_syndromes
                << " orbit_syndromes=" << census.orbit_syndromes << '\n';
    }
  }

  const std::map<int, std::uint64_t> expected_q41_ranks = {
      {0, 1}, {1, 1}, {3, 9}, {4, 9}, {6, 195}, {7, 585},
      {9, 12285}, {10, 36855}};
  if (q41.even_orbits != 49'940 || q41.labeled_syndromes != 463'228'168 ||
      q41.orbit_syndromes != 22'058'510 || q41.rhs_zero_orbits != 24'946 ||
      q41.rhs_one_orbits != 24'994 || q41.rank_orbits != expected_q41_ranks) {
    throw std::runtime_error("q=41 published census mismatch");
  }
  if (!stream) {
    std::cout << "odd_lengths_verified=3,5,7,9,11,13,15,17,19,21\n";
    std::cout << "q41_direct_subset_xor_orbits=49940\n";
    std::cout << "q41_exact_support_equation=verified\n";
    std::cout << "certificate=verified\n";
  }
}
