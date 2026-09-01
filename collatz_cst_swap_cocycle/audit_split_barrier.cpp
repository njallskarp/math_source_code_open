#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using u64 = std::uint64_t;
using u128 = unsigned __int128;
using i128 = __int128;

struct Cylinder {
  unsigned length = 0;
  unsigned odd_count = 0;
  u64 residue = 0;
  u64 endpoint = 0;
  u64 pow2 = 1;
  u64 pow3 = 1;

  Cylinder extend(unsigned bit) const {
    const u64 lift = bit == 0 ? (endpoint & 1U) : ((1U - endpoint) & 1U);
    const u128 intermediate = static_cast<u128>(endpoint) +
                              static_cast<u128>(pow3) * lift;
    if ((static_cast<unsigned>(intermediate & 1U)) != bit) {
      throw std::runtime_error("parity-cylinder extension failed");
    }
    Cylinder result;
    result.length = length + 1;
    result.odd_count = odd_count + bit;
    result.residue = residue + pow2 * lift;
    result.endpoint = bit == 0
                          ? static_cast<u64>(intermediate / 2)
                          : static_cast<u64>((3 * intermediate + 1) / 2);
    result.pow2 = 2 * pow2;
    result.pow3 = bit == 0 ? pow3 : 3 * pow3;
    return result;
  }

  u64 numerator() const {
    const u128 left = static_cast<u128>(pow2) * endpoint;
    const u128 right = static_cast<u128>(pow3) * residue;
    if (left < right) throw std::runtime_error("negative affine numerator");
    return static_cast<u64>(left - right);
  }

  std::int64_t margin() const {
    return static_cast<std::int64_t>(residue) -
           static_cast<std::int64_t>(endpoint);
  }
};

u64 inverse_odd_mod_power_two(u64 odd, u64 modulus) {
  if ((odd & 1U) == 0 || modulus == 0 || (modulus & (modulus - 1)) != 0) {
    throw std::runtime_error("invalid inverse modulus");
  }
  // Newton iteration doubles the number of correct low bits each time.
  u64 inverse = odd;
  for (unsigned iteration = 0; iteration < 6; ++iteration) {
    inverse *= 2 - odd * inverse;
  }
  return inverse & (modulus - 1);
}

std::string chronological_word(u64 bits, unsigned length) {
  std::string result;
  result.reserve(length);
  for (unsigned position = 0; position < length; ++position) {
    result.push_back(((bits >> position) & 1U) ? '1' : '0');
  }
  return result;
}

struct Counts {
  u64 first_crossings = 0;
  u64 candidate_edges = 0;
  u64 wrapped_edges = 0;
  u64 nonpositive_prefix_surplus = 0;
  u64 positive_prefix_surplus = 0;
  u64 descent_failures = 0;
  std::map<unsigned, u64> residual_by_prefix_length;
  std::map<unsigned, u64> wrapped_by_prefix_length;
  std::map<unsigned, u64> certificate_bits;
  unsigned maximum_certificate_bits = 0;
  unsigned maximum_certificate_length = 0;
  unsigned maximum_certificate_position = 0;
  std::string maximum_certificate_word;
  unsigned first_residual_prefix_at_least_six_length = 0;
  unsigned first_residual_prefix_at_least_six_position = 0;
  std::string first_residual_prefix_at_least_six_word;
  std::int64_t minimum_margin = std::numeric_limits<std::int64_t>::max();
  unsigned minimum_margin_length = 0;
  std::string minimum_margin_word;
};

void analyze_word(u64 bits, unsigned length, Counts &counts) {
  ++counts.first_crossings;
  std::vector<Cylinder> prefixes(length + 1);
  for (unsigned position = 0; position < length; ++position) {
    prefixes[position + 1] =
        prefixes[position].extend(static_cast<unsigned>((bits >> position) & 1U));
  }
  const Cylinder &target = prefixes[length];
  const std::int64_t margin = target.margin();
  if (length > 2 &&
      (margin < counts.minimum_margin ||
       (margin == counts.minimum_margin &&
        length < counts.minimum_margin_length))) {
    counts.minimum_margin = margin;
    counts.minimum_margin_length = length;
    counts.minimum_margin_word = chronological_word(bits, length);
  }
  if (length > 2 && margin <= 0) ++counts.descent_failures;

  std::vector<u64> suffix_power(length + 1, 1);
  std::vector<u64> suffix_numerator(length + 1, 0);
  for (unsigned start = length; start-- > 0;) {
    const unsigned bit = static_cast<unsigned>((bits >> start) & 1U);
    suffix_numerator[start] =
        2 * suffix_numerator[start + 1] + (bit ? suffix_power[start + 1] : 0);
    suffix_power[start] = suffix_power[start + 1] * (bit ? 3 : 1);
  }

  const u64 modulus = u64{1} << length;
  const u64 gap = modulus - target.pow3;
  for (unsigned position = 0; position + 1 < length; ++position) {
    // Target has p10s; its reverse adjacent swap is p01s.
    if (((bits >> position) & 3U) != 1U) continue;
    const Cylinder &prefix = prefixes[position];
    // The reverse-swapped source is first-crossing exactly when p0 is still
    // coefficient-safe.  Every other prefix is inherited from the target.
    if (prefix.pow3 < 2 * prefix.pow2) continue;
    ++counts.candidate_edges;

    const u64 scale = u64{1} << position;
    const u64 local_modulus = u64{1} << (length - position);
    if (target.residue < prefix.residue ||
        (target.residue - prefix.residue) % scale != 0) {
      throw std::runtime_error("target does not lift its prefix");
    }
    const u64 target_lift = (target.residue - prefix.residue) / scale;
    const u64 prefix_power = 3 * prefix.pow3;
    const u64 inverse = inverse_odd_mod_power_two(prefix_power, local_modulus);
    // x<u is equivalent to the reverse source wrapping when it moves 01->10.
    if (target_lift >= inverse) continue;
    ++counts.wrapped_edges;
    ++counts.wrapped_by_prefix_length[position];

    const u64 suffix_e = suffix_power[position + 2];
    const u64 suffix_b = suffix_numerator[position + 2];
    const i128 prefix_surplus =
        static_cast<i128>(local_modulus) * prefix.residue -
        static_cast<i128>(suffix_e) * (3 * static_cast<i128>(prefix.endpoint) + 1) -
        4 * static_cast<i128>(suffix_b);
    const i128 reconstructed = static_cast<i128>(gap) * target_lift + prefix_surplus;
    if (reconstructed != static_cast<i128>(local_modulus) * margin) {
      throw std::runtime_error("split barrier identity failed");
    }
    if (prefix_surplus > 0) {
      ++counts.positive_prefix_surplus;
      ++counts.certificate_bits[0];
    } else {
      ++counts.nonpositive_prefix_surplus;
      ++counts.residual_by_prefix_length[position];
      if (position >= 6 &&
          counts.first_residual_prefix_at_least_six_word.empty()) {
        counts.first_residual_prefix_at_least_six_length = length;
        counts.first_residual_prefix_at_least_six_position = position;
        counts.first_residual_prefix_at_least_six_word =
            chronological_word(bits, length);
      }
      unsigned required_bits = 0;
      const unsigned local_bits = length - position;
      for (unsigned bits_used = 2; bits_used <= local_bits; ++bits_used) {
        const u64 mask = (u64{1} << bits_used) - 1;
        const u64 lift_lower_bound = target_lift & mask;
        if (static_cast<i128>(gap) * lift_lower_bound + prefix_surplus > 0) {
          required_bits = bits_used;
          break;
        }
      }
      if (required_bits == 0) {
        throw std::runtime_error("full split coordinate did not certify descent");
      }
      ++counts.certificate_bits[required_bits];
      if (required_bits > counts.maximum_certificate_bits) {
        counts.maximum_certificate_bits = required_bits;
        counts.maximum_certificate_length = length;
        counts.maximum_certificate_position = position;
        counts.maximum_certificate_word = chronological_word(bits, length);
      }
    }
  }
}

void enumerate(u64 bits, const Cylinder &state, unsigned max_length,
               Counts &counts) {
  if (state.length == max_length) return;
  for (unsigned bit = 0; bit <= 1; ++bit) {
    const Cylinder next = state.extend(bit);
    const u64 next_bits = bits | (static_cast<u64>(bit) << state.length);
    if (next.pow3 < next.pow2) {
      analyze_word(next_bits, next.length, counts);
    } else {
      enumerate(next_bits, next, max_length, counts);
    }
  }
}

int main(int argc, char **argv) {
  const unsigned max_length =
      argc > 1 ? static_cast<unsigned>(std::stoul(argv[1])) : 32;
  if (max_length < 2 || max_length > 40) {
    std::cerr << "max_length must lie in [2,40]\n";
    return EXIT_FAILURE;
  }
  Counts counts;
  enumerate(0, Cylinder{}, max_length, counts);
  std::cout << "max_length=" << max_length << '\n'
            << "first_crossings=" << counts.first_crossings << '\n'
            << "candidate_edges=" << counts.candidate_edges << '\n'
            << "wrapped_edges=" << counts.wrapped_edges << '\n'
            << "positive_prefix_surplus=" << counts.positive_prefix_surplus << '\n'
            << "nonpositive_prefix_surplus=" << counts.nonpositive_prefix_surplus << '\n'
            << "descent_failures=" << counts.descent_failures << '\n'
            << "minimum_margin=" << counts.minimum_margin << '\n'
            << "minimum_margin_length=" << counts.minimum_margin_length << '\n'
            << "minimum_margin_word=" << counts.minimum_margin_word << '\n';
  for (const auto &[bits_used, count] : counts.certificate_bits) {
    std::cout << "certificate_bits=" << bits_used << ",edges=" << count << '\n';
  }
  std::cout << "maximum_certificate_bits=" << counts.maximum_certificate_bits
            << '\n'
            << "maximum_certificate_example=K:"
            << counts.maximum_certificate_length
            << ",j:" << counts.maximum_certificate_position
            << ",word:" << counts.maximum_certificate_word << '\n';
  for (const auto &[position, count] : counts.wrapped_by_prefix_length) {
    std::cout << "prefix_j=" << position << ",wrapped=" << count
              << ",residual=" << counts.residual_by_prefix_length[position] << '\n';
  }
  if (counts.first_residual_prefix_at_least_six_word.empty()) {
    std::cout << "first_residual_prefix_at_least_six=none\n";
  } else {
    std::cout << "first_residual_prefix_at_least_six=K:"
              << counts.first_residual_prefix_at_least_six_length
              << ",j:" << counts.first_residual_prefix_at_least_six_position
              << ",word:" << counts.first_residual_prefix_at_least_six_word << '\n';
  }
  std::cout << "status=exact split-barrier audit passed\n";
}
