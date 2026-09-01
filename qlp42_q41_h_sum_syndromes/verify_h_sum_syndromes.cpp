#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int N = 21;
constexpr int DIM = 10;
constexpr std::uint32_t FULL = (1u << N) - 1;

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

int syndrome_rank(std::vector<std::uint16_t> values) {
  int rank = 0;
  for (int column = DIM - 1; column >= 0; --column) {
    int pivot = -1;
    for (int row = rank; row < static_cast<int>(values.size()); ++row) {
      if ((values[row] >> column) & 1u) {
        pivot = row;
        break;
      }
    }
    if (pivot < 0) continue;
    std::swap(values[rank], values[pivot]);
    for (int row = 0; row < static_cast<int>(values.size()); ++row) {
      if (row != rank && ((values[row] >> column) & 1u)) values[row] ^= values[rank];
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

std::int64_t krawtchouk(int n, int negatives, int choose) {
  std::int64_t result = 0;
  for (int taken_negative = 0; taken_negative <= choose; ++taken_negative) {
    const int taken_positive = choose - taken_negative;
    if (taken_negative > negatives || taken_positive > n - negatives) continue;
    const std::int64_t term =
        binomial[negatives][taken_negative] * binomial[n - negatives][taken_positive];
    result += (taken_negative & 1) ? -term : term;
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

struct SyndromeResult {
  int map_rank{};
  int support_size{};
  int affine_dimension{};
  std::uint64_t sign_words{};
};

SyndromeResult exact_sum_one_syndromes(std::uint32_t b) {
  const int imaginary = std::popcount(b);
  if (imaginary & 1) throw std::runtime_error("sum one requires even imaginary-axis weight");
  const int real = N - imaginary;
  const int negative_real = (real - 1) / 2;
  const int negative_imaginary = imaginary / 2;
  const auto rows = d_rows(b);
  const int map_rank = binary_rank(rows);

  std::array<std::int64_t, 1 << DIM> transform{};
  for (int character = 0; character < (1 << DIM); ++character) {
    std::uint32_t pullback = 0;
    for (int bit = 0; bit < DIM; ++bit) {
      if ((character >> bit) & 1) pullback ^= rows[bit];
    }
    const int imaginary_negatives = std::popcount(pullback & b);
    const int real_negatives = std::popcount(pullback & (FULL ^ b));
    transform[character] =
        krawtchouk(real, real_negatives, negative_real) *
        krawtchouk(imaginary, imaginary_negatives, negative_imaginary);
  }

  walsh_hadamard(transform);
  std::vector<std::uint16_t> support;
  std::uint64_t sign_words = 0;
  for (int syndrome = 0; syndrome < (1 << DIM); ++syndrome) {
    if (transform[syndrome] % (1 << DIM) != 0)
      throw std::runtime_error("nonintegral inverse Walsh coefficient");
    transform[syndrome] /= (1 << DIM);
    if (transform[syndrome] < 0)
      throw std::runtime_error("negative exact-sum fiber count");
    sign_words += static_cast<std::uint64_t>(transform[syndrome]);
    if (transform[syndrome] > 0) support.push_back(static_cast<std::uint16_t>(syndrome));
  }

  const std::uint64_t expected_sign_words =
      binomial[real][negative_real] * binomial[imaginary][negative_imaginary];
  if (sign_words != expected_sign_words) throw std::runtime_error("sign-word total mismatch");

  const auto origin = support.front();
  std::vector<std::uint16_t> differences;
  differences.reserve(support.size());
  for (const auto value : support) differences.push_back(value ^ origin);
  const int affine_dimension = syndrome_rank(differences);
  if (support.size() != (std::size_t{1} << affine_dimension))
    throw std::runtime_error("syndrome support is not affine");
  const int expected_dimension = map_rank == 0 ? 0 : map_rank - 1;
  if (affine_dimension != expected_dimension)
    throw std::runtime_error("unexpected exact-sum affine dimension");

  return {map_rank, static_cast<int>(support.size()), affine_dimension, sign_words};
}

struct RankStats {
  std::uint64_t words{};
  std::uint64_t orbits{};
  int support_size{-1};
  int affine_dimension{-1};
  std::uint64_t word_syndrome_pairs{};
  std::uint64_t orbit_syndrome_pairs{};
  std::uint64_t exact_sign_words{};
};

std::string make_table(const std::map<int, RankStats>& stats) {
  std::ostringstream output;
  output << "rank\teven_axis_words\teven_axis_orbits\taffine_dimension\t"
            "syndrome_set_size\tword_syndrome_pairs\torbit_syndrome_pairs\n";
  for (const auto& [rank, row] : stats) {
    output << rank << '\t' << row.words << '\t' << row.orbits << '\t'
           << row.affine_dimension << '\t' << row.support_size << '\t'
           << row.word_syndrome_pairs << '\t' << row.orbit_syndrome_pairs << '\n';
  }
  return output.str();
}

std::string read_file(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open " + path);
  std::ostringstream data;
  data << input.rdbuf();
  return data.str();
}

}  // namespace

int main() {
  binomial[0][0] = 1;
  for (int n = 1; n <= N; ++n) {
    binomial[n][0] = binomial[n][n] = 1;
    for (int k = 1; k < n; ++k) binomial[n][k] = binomial[n - 1][k - 1] + binomial[n - 1][k];
  }

  std::vector<std::uint8_t> seen(1u << N, 0);
  std::map<int, RankStats> stats;
  std::uint64_t processed_orbits = 0;
  std::uint64_t total_exact_sign_words = 0;
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
    const auto result = exact_sum_one_syndromes(mask);
    auto& row = stats[result.map_rank];
    row.words += orbit.size();
    row.orbits += 1;
    row.word_syndrome_pairs += orbit.size() * result.support_size;
    row.orbit_syndrome_pairs += result.support_size;
    row.exact_sign_words += orbit.size() * result.sign_words;
    total_exact_sign_words += orbit.size() * result.sign_words;
    if (row.support_size < 0) {
      row.support_size = result.support_size;
      row.affine_dimension = result.affine_dimension;
    } else if (row.support_size != result.support_size ||
               row.affine_dimension != result.affine_dimension) {
      throw std::runtime_error("rank stratum has inconsistent syndrome geometry");
    }
    ++processed_orbits;
  }

  const std::map<int, std::uint64_t> expected_words = {
      {0, 1}, {1, 3}, {3, 63}, {4, 189}, {6, 4095}, {7, 12285},
      {9, 257985}, {10, 773955}};
  const std::map<int, std::uint64_t> expected_orbits = {
      {0, 1}, {1, 1}, {3, 9}, {4, 9}, {6, 195}, {7, 585},
      {9, 12285}, {10, 36855}};
  for (const auto& [rank, words] : expected_words) {
    if (stats.at(rank).words != words || stats.at(rank).orbits != expected_orbits.at(rank))
      throw std::runtime_error("rank-stratum word/orbit mismatch");
  }
  if (processed_orbits != 49'940) throw std::runtime_error("even-orbit total mismatch");

  const auto table = make_table(stats);
  if (table != read_file("rank_syndrome_table.tsv"))
    throw std::runtime_error("rank_syndrome_table.tsv mismatch");

  std::uint64_t word_syndrome_pairs = 0;
  std::uint64_t orbit_syndrome_pairs = 0;
  for (const auto& [rank, row] : stats) {
    (void)rank;
    word_syndrome_pairs += row.word_syndrome_pairs;
    orbit_syndrome_pairs += row.orbit_syndrome_pairs;
  }

  std::cout << "even_axis_words=" << (1u << 20) << '\n';
  std::cout << "even_axis_rotation_orbits=" << processed_orbits << '\n';
  std::cout << "rank_strata=" << stats.size() << '\n';
  std::cout << "word_syndrome_pairs=" << word_syndrome_pairs << '\n';
  std::cout << "orbit_syndrome_pairs=" << orbit_syndrome_pairs << '\n';
  std::cout << "exact_sum_one_sign_words=" << total_exact_sign_words << '\n';
  std::cout << "all_supports_affine=verified\n";
  std::cout << "codimension_one_for_positive_rank=verified\n";
  std::cout << "rank_syndrome_table=verified\n";
  std::cout << "certificate=verified\n";
}
