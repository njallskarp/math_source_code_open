#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {

constexpr int N = 21;
constexpr int DIM = 10;
constexpr std::uint32_t FULL = (1u << N) - 1;
constexpr std::array<int, 6> TARGET_REAL = {4, 4, 0, 4, 4, 0};
constexpr std::array<int, 6> TARGET_IMAG = {-5, -3, -5, -1, 1, -3};

std::array<std::array<std::int64_t, 22>, 22> binomial{};

std::uint32_t rotate(std::uint32_t mask) {
  return ((mask << 1) | (mask >> (N - 1))) & FULL;
}

std::vector<std::uint32_t> d_rows(std::uint32_t b) {
  std::vector<std::uint32_t> rows;
  for (int shift = 1; shift <= DIM; ++shift) {
    std::uint32_t row = 0;
    for (int j = 0; j < N; ++j) {
      const int plus = (j + shift) % N;
      const int minus = (j - shift + N) % N;
      row |= (((b >> plus) ^ (b >> minus)) & 1u) << j;
    }
    rows.push_back(row);
  }
  return rows;
}

int binary_rank(std::vector<std::uint32_t> values, int columns) {
  int rank = 0;
  for (int column = columns - 1; column >= 0; --column) {
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

std::array<bool, 1 << DIM> image_of_d(const std::vector<std::uint32_t>& rows) {
  std::array<bool, 1 << DIM> image{};
  image[0] = true;
  for (int j = 0; j < N; ++j) {
    std::uint16_t column = 0;
    for (int s = 0; s < DIM; ++s) column |= ((rows[s] >> j) & 1u) << s;
    const auto before = image;
    for (int value = 0; value < (1 << DIM); ++value) {
      if (before[value]) image[value ^ column] = true;
    }
  }
  return image;
}

std::int64_t krawtchouk(int n, int marked, int choose) {
  if (choose < 0 || choose > n) return 0;
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

void walsh(std::array<std::int64_t, 1 << DIM>& values) {
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

struct Support {
  std::array<std::uint64_t, 16> bits{};
  int size{};
  int affine_dimension{-1};
  bool affine{};
};

Support target_support(std::uint32_t b, const std::vector<std::uint32_t>& rows,
                       const std::array<bool, 1 << DIM>& image, int target_real,
                       int target_imag) {
  const int real = std::popcount(b);
  const int imaginary = N - real;
  if ((real - target_real) & 1 || (imaginary - target_imag) & 1) return {};
  const int negative_real = (real - target_real) / 2;
  const int negative_imaginary = (imaginary - target_imag) / 2;
  if (negative_real < 0 || negative_real > real || negative_imaginary < 0 ||
      negative_imaginary > imaginary) {
    return {};
  }

  std::array<std::int64_t, 1 << DIM> transform{};
  for (int character = 0; character < (1 << DIM); ++character) {
    std::uint32_t pullback = 0;
    for (int bit = 0; bit < DIM; ++bit) {
      if ((character >> bit) & 1) pullback ^= rows[bit];
    }
    transform[character] =
        krawtchouk(real, std::popcount(pullback & b), negative_real) *
        krawtchouk(imaginary, std::popcount(pullback & (FULL ^ b)),
                    negative_imaginary);
  }
  walsh(transform);

  Support result;
  std::vector<std::uint32_t> points;
  for (int syndrome = 0; syndrome < (1 << DIM); ++syndrome) {
    if (transform[syndrome] % (1 << DIM) != 0) throw std::runtime_error("nonintegral fiber");
    transform[syndrome] /= (1 << DIM);
    if (transform[syndrome] < 0) throw std::runtime_error("negative fiber");
    if (transform[syndrome] == 0) continue;
    if (!image[syndrome]) throw std::runtime_error("support outside image");
    if (std::popcount(static_cast<unsigned>(syndrome)) & 1) {
      throw std::runtime_error("odd-parity S_B syndrome");
    }
    result.bits[syndrome >> 6] |= std::uint64_t{1} << (syndrome & 63);
    points.push_back(static_cast<std::uint32_t>(syndrome));
  }
  result.size = static_cast<int>(points.size());
  if (points.empty()) return result;
  const auto origin = points.front();
  for (auto& point : points) point ^= origin;
  result.affine_dimension = binary_rank(points, DIM);
  result.affine = result.size == (1 << result.affine_dimension);
  return result;
}

struct Stratum {
  std::uint64_t words{};
  std::uint64_t orbits{};
};

using Key = std::tuple<int, int, int, int, int, int>;

void emit_support_hex(const Support& support) {
  std::cout << std::hex << std::setfill('0');
  for (int block = 15; block >= 0; --block) std::cout << std::setw(16) << support.bits[block];
  std::cout << std::dec;
}

}  // namespace

int main(int argc, char** argv) {
  const bool stream = argc == 2 && std::string(argv[1]) == "--stream";
  const bool sample_stream = argc == 2 && std::string(argv[1]) == "--sample-stream";
  const bool table = argc == 2 && std::string(argv[1]) == "--table";
  if (argc > 2 || (argc == 2 && !stream && !sample_stream && !table)) {
    std::cerr << "usage: classify_s_b_syndromes [--stream|--sample-stream|--table]\n";
    return 2;
  }

  binomial[0][0] = 1;
  for (int n = 1; n <= N; ++n) {
    binomial[n][0] = binomial[n][n] = 1;
    for (int k = 1; k < n; ++k) {
      binomial[n][k] = binomial[n - 1][k - 1] + binomial[n - 1][k];
    }
  }

  if (stream || sample_stream) {
    std::cout << "axis_word\torbit_size\tweight\trank\tcase\tsupport\n";
  }
  std::vector<std::uint8_t> seen(1u << N, 0);
  std::map<Key, Stratum> strata;
  std::array<std::uint64_t, 6> full_orbits{};
  std::array<std::uint64_t, 6> defective_orbits{};
  std::array<std::uint64_t, 6> empty_orbits{};
  std::array<std::uint64_t, 6> full_words{};
  std::array<std::uint64_t, 6> defective_words{};
  std::array<std::uint64_t, 6> empty_words{};
  std::array<int, 6> max_defect{};
  std::array<bool, DIM + 1> sampled_rank{};
  std::uint64_t processed_orbits = 0;
  std::uint64_t processed_words = 0;

  for (std::uint32_t mask = 0; mask < (1u << N); ++mask) {
    if (seen[mask]) continue;
    std::vector<std::uint32_t> orbit;
    auto value = mask;
    do {
      orbit.push_back(value);
      seen[value] = 1;
      value = rotate(value);
    } while (value != mask);
    if (std::popcount(mask) % 4 != 0) continue;

    const auto rows = d_rows(mask);
    const int rank = binary_rank(rows, N);
    const int weight = std::popcount(mask);
    const auto image = image_of_d(rows);
    const bool emit_sample = sample_stream &&
                             (processed_orbits % 49 == 0 || !sampled_rank[rank]);
    if (emit_sample) sampled_rank[rank] = true;
    std::array<Support, 6> supports;
    for (int target_case = 0; target_case < 6; ++target_case) {
      supports[target_case] = target_support(mask, rows, image, TARGET_REAL[target_case],
                                             TARGET_IMAG[target_case]);
      const auto& support = supports[target_case];
      const int half_image = rank == 0 ? 1 : (1 << (rank - 1));
      const int defect = half_image - support.size;
      if (support.size == 0) {
        ++empty_orbits[target_case];
        empty_words[target_case] += orbit.size();
      } else if (defect == 0) {
        ++full_orbits[target_case];
        full_words[target_case] += orbit.size();
      } else {
        ++defective_orbits[target_case];
        defective_words[target_case] += orbit.size();
        max_defect[target_case] = std::max(max_defect[target_case], defect);
      }
      const Key key{target_case, weight, rank, support.size, support.affine_dimension,
                    support.affine ? 1 : 0};
      strata[key].words += orbit.size();
      strata[key].orbits += 1;
      if (stream || emit_sample) {
        std::cout << std::hex << std::setfill('0') << std::setw(6) << mask << std::dec << '\t'
                  << orbit.size() << '\t' << weight << '\t' << rank << '\t' << target_case
                  << '\t';
        emit_support_hex(support);
        std::cout << '\n';
      }
    }
    if (supports[3].bits != supports[4].bits) {
      throw std::runtime_error("imaginary-sign symmetry failed for cases 3 and 4");
    }
    ++processed_orbits;
    processed_words += orbit.size();
  }

  if (processed_orbits != 24'946 || processed_words != 523'776) {
    throw std::runtime_error("weight-zero-mod-four census mismatch");
  }

  if (table) {
    std::cout << "case\tweight\trank\tsupport_size\taffine_dimension\taffine\twords\torbits\n";
    for (const auto& [key, value] : strata) {
      const auto [target_case, weight, rank, size, dimension, affine] = key;
      std::cout << target_case << '\t' << weight << '\t' << rank << '\t' << size << '\t'
                << dimension << '\t' << affine << '\t' << value.words << '\t' << value.orbits
                << '\n';
    }
  } else if (!stream && !sample_stream) {
    std::cout << "b_words_wt_0_mod_4=" << processed_words << '\n';
    std::cout << "b_rotation_orbits_wt_0_mod_4=" << processed_orbits << '\n';
    std::cout << "support_strata=" << strata.size() << '\n';
    for (int target_case = 0; target_case < 6; ++target_case) {
      std::cout << "case_" << target_case << "_full_orbits=" << full_orbits[target_case] << '\n';
      std::cout << "case_" << target_case << "_full_words=" << full_words[target_case] << '\n';
      std::cout << "case_" << target_case << "_defective_orbits="
                << defective_orbits[target_case] << '\n';
      std::cout << "case_" << target_case << "_defective_words="
                << defective_words[target_case] << '\n';
      std::cout << "case_" << target_case << "_empty_orbits=" << empty_orbits[target_case]
                << '\n';
      std::cout << "case_" << target_case << "_empty_words=" << empty_words[target_case] << '\n';
      std::cout << "case_" << target_case << "_max_defect=" << max_defect[target_case] << '\n';
    }
    std::cout << "all_supports_in_even_parity_half_image=verified\n";
    std::cout << "case_3_case_4_support_identity=verified\n";
    std::cout << "certificate=verified\n";
  }
}
