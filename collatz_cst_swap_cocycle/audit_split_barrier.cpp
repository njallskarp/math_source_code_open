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

struct ShadowPrefixStats {
  unsigned position = 0;
  u64 prefix_bits = 0;
  u64 lift_mod_four = 0;
  u64 shadow_value = 0;
  unsigned crossing = 0;
  u64 edges = 0;
  u64 certified = 0;
  u64 unresolved = 0;
  unsigned maximum_raw_bits = 0;
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
  bool emit_ladder = false;
  u64 first_crossings = 0;
  u64 candidate_edges = 0;
  u64 wrapped_edges = 0;
  u64 nonpositive_prefix_surplus = 0;
  u64 positive_prefix_surplus = 0;
  u64 low_two_bit_certificates = 0;
  u64 base_shadow_certificates = 0;
  u64 unresolved_after_base_shadow = 0;
  u64 adaptive_shadow_certificates = 0;
  u64 excluded_lift_ladder_certificates = 0;
  u64 excluded_lift_ladder_candidates = 0;
  u64 excluded_lift_ladder_parity_bits = 0;
  u64 maximum_excluded_lift_ladder_steps = 0;
  unsigned maximum_excluded_lift_mismatch_depth = 0;
  unsigned maximum_excluded_lift_ladder_length = 0;
  unsigned maximum_excluded_lift_ladder_position = 0;
  std::string maximum_excluded_lift_ladder_word;
  unsigned maximum_excluded_lift_mismatch_length = 0;
  unsigned maximum_excluded_lift_mismatch_position = 0;
  std::string maximum_excluded_lift_mismatch_word;
  u64 descent_failures = 0;
  std::map<unsigned, u64> residual_by_prefix_length;
  std::map<unsigned, u64> wrapped_by_prefix_length;
  std::map<unsigned, u64> certificate_bits;
  std::map<unsigned, u64> symbolic_certificate_bits;
  unsigned maximum_certificate_bits = 0;
  unsigned maximum_certificate_length = 0;
  unsigned maximum_certificate_position = 0;
  std::string maximum_certificate_word;
  unsigned maximum_symbolic_certificate_bits = 0;
  unsigned maximum_symbolic_certificate_length = 0;
  unsigned maximum_symbolic_certificate_position = 0;
  std::string maximum_symbolic_certificate_word;
  unsigned first_residual_prefix_at_least_six_length = 0;
  unsigned first_residual_prefix_at_least_six_position = 0;
  std::string first_residual_prefix_at_least_six_word;
  std::int64_t minimum_margin = std::numeric_limits<std::int64_t>::max();
  unsigned minimum_margin_length = 0;
  std::string minimum_margin_word;
  std::map<std::pair<unsigned, u64>, unsigned> shadow_crossing_cache;
  std::map<std::pair<unsigned, u64>, ShadowPrefixStats> shadow_prefix_stats;
};

std::string signed_decimal(i128 value) {
  if (value == 0) return "0";
  const bool negative = value < 0;
  u128 magnitude = negative ? static_cast<u128>(-value)
                            : static_cast<u128>(value);
  std::string digits;
  while (magnitude != 0) {
    digits.push_back(static_cast<char>('0' + magnitude % 10));
    magnitude /= 10;
  }
  if (negative) digits.push_back('-');
  std::reverse(digits.begin(), digits.end());
  return digits;
}

unsigned relative_coefficient_crossing(const Cylinder &prefix,
                                       u64 candidate_lift) {
  const u64 prefix_power = 3 * prefix.pow3;
  const u128 numerator = static_cast<u128>(prefix_power) * candidate_lift +
                         3 * static_cast<u128>(prefix.endpoint) + 1;
  if (numerator % 4 != 0) {
    throw std::runtime_error("the p10 base lift is not integral");
  }
  u128 value = numerator / 4;
  u128 left = prefix_power;
  u128 right = 4 * static_cast<u128>(prefix.pow2);
  constexpr u128 maximum = ~u128{0};
  for (unsigned length = 1; length <= 80; ++length) {
    if ((value & 1U) != 0) {
      if (value > (maximum - 1) / 3 || left > maximum / 3) return 0;
      value = (3 * value + 1) / 2;
      left *= 3;
    } else {
      value /= 2;
    }
    if (right > maximum / 2) return 0;
    right *= 2;
    if (left < right) return length;
  }
  return 0;
}

unsigned first_suffix_parity_mismatch(const Cylinder &prefix,
                                      u64 candidate_lift, u64 suffix_bits,
                                      unsigned suffix_length) {
  const u64 prefix_power = 3 * prefix.pow3;
  const u128 numerator = static_cast<u128>(prefix_power) * candidate_lift +
                         3 * static_cast<u128>(prefix.endpoint) + 1;
  if (numerator % 4 != 0) {
    throw std::runtime_error("the p10 candidate lift is not integral");
  }
  u128 value = numerator / 4;
  for (unsigned index = 0; index < suffix_length; ++index) {
    const unsigned observed = static_cast<unsigned>(value & 1U);
    const unsigned expected =
        static_cast<unsigned>((suffix_bits >> index) & 1U);
    if (observed != expected) return index + 1;
    value = observed == 0 ? value / 2 : (3 * value + 1) / 2;
  }
  return 0;
}

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
      ++counts.symbolic_certificate_bits[0];
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
      const u64 lift_mod_four = target_lift & 3U;
      const i128 base_barrier =
          static_cast<i128>(gap) * lift_mod_four + prefix_surplus;
      if (base_barrier <= 0) {
        const i128 step_gain = 4 * static_cast<i128>(gap);
        const u64 ladder_steps =
            static_cast<u64>((-base_barrier) / step_gain + 1);
        const u64 forced_lower_bound = lift_mod_four + 4 * ladder_steps;
        if (forced_lower_bound > target_lift) {
          throw std::runtime_error(
              "excluded-lift ladder overshot the true lift");
        }
        if (static_cast<i128>(gap) * forced_lower_bound + prefix_surplus <=
            0) {
          throw std::runtime_error(
              "excluded-lift ladder did not clear the barrier");
        }
        const unsigned suffix_length = length - position - 2;
        const u64 suffix_bits = bits >> (position + 2);
        std::vector<unsigned> mismatch_depths;
        mismatch_depths.reserve(static_cast<std::size_t>(ladder_steps));
        for (u64 rank = 0; rank < ladder_steps; ++rank) {
          const u64 candidate_lift = lift_mod_four + 4 * rank;
          const unsigned mismatch = first_suffix_parity_mismatch(
              prefix, candidate_lift, suffix_bits, suffix_length);
          if (mismatch == 0) {
            throw std::runtime_error(
                "a strictly lower candidate matched the full suffix");
          }
          ++counts.excluded_lift_ladder_candidates;
          counts.excluded_lift_ladder_parity_bits += mismatch;
          mismatch_depths.push_back(mismatch);
          if (mismatch > counts.maximum_excluded_lift_mismatch_depth) {
            counts.maximum_excluded_lift_mismatch_depth = mismatch;
            counts.maximum_excluded_lift_mismatch_length = length;
            counts.maximum_excluded_lift_mismatch_position = position;
            counts.maximum_excluded_lift_mismatch_word =
                chronological_word(bits, length);
          }
        }
        if (counts.emit_ladder) {
          std::cout << "ladder=K:" << length
                    << ",word:" << chronological_word(bits, length)
                    << ",j:" << position << ",gap:" << gap
                    << ",Q:" << signed_decimal(prefix_surplus)
                    << ",chi2:" << lift_mod_four
                    << ",steps:" << ladder_steps << ",mismatches:";
          for (std::size_t index = 0; index < mismatch_depths.size(); ++index) {
            if (index != 0) std::cout << ';';
            std::cout << mismatch_depths[index];
          }
          std::cout << '\n';
        }
        ++counts.excluded_lift_ladder_certificates;
        if (ladder_steps > counts.maximum_excluded_lift_ladder_steps) {
          counts.maximum_excluded_lift_ladder_steps = ladder_steps;
          counts.maximum_excluded_lift_ladder_length = length;
          counts.maximum_excluded_lift_ladder_position = position;
          counts.maximum_excluded_lift_ladder_word =
              chronological_word(bits, length);
        }
      }
      bool base_shadow_certified = false;
      if (static_cast<i128>(gap) * lift_mod_four + prefix_surplus > 0) {
        ++counts.low_two_bit_certificates;
      } else {
        const auto cache_key = std::make_pair(
            position, (bits & ((u64{1} << position) - 1)) |
                          (lift_mod_four << position));
        auto crossing_iterator = counts.shadow_crossing_cache.find(cache_key);
        if (crossing_iterator == counts.shadow_crossing_cache.end()) {
          crossing_iterator = counts.shadow_crossing_cache
                                  .emplace(cache_key,
                                           relative_coefficient_crossing(
                                               prefix, lift_mod_four))
                                  .first;
        }
        const unsigned crossing = crossing_iterator->second;
        auto &prefix_stats = counts.shadow_prefix_stats[cache_key];
        prefix_stats.position = position;
        prefix_stats.prefix_bits = bits & ((u64{1} << position) - 1);
        prefix_stats.lift_mod_four = lift_mod_four;
        prefix_stats.shadow_value =
            (3 * prefix.pow3 * lift_mod_four + 3 * prefix.endpoint + 1) / 4;
        prefix_stats.crossing = crossing;
        ++prefix_stats.edges;
        prefix_stats.maximum_raw_bits =
            std::max(prefix_stats.maximum_raw_bits, required_bits);
        const unsigned suffix_length = length - position - 2;
        const u64 forced_lower_bound = lift_mod_four + 4;
        if (crossing != 0 && suffix_length > crossing) {
          if (forced_lower_bound > target_lift) {
            throw std::runtime_error(
                "shadow forcing did not lower-bound the lift");
          }
          if (static_cast<i128>(gap) * forced_lower_bound + prefix_surplus >
              0) {
            ++counts.base_shadow_certificates;
            ++prefix_stats.certified;
            base_shadow_certified = true;
          } else {
            ++counts.unresolved_after_base_shadow;
            ++prefix_stats.unresolved;
          }
        } else {
          ++counts.unresolved_after_base_shadow;
          ++prefix_stats.unresolved;
        }
      }
      unsigned symbolic_bits = required_bits;
      if (required_bits == 2) {
        symbolic_bits = 2;
      } else if (base_shadow_certified) {
        symbolic_bits = 2;
        ++counts.adaptive_shadow_certificates;
      } else {
        const unsigned suffix_length = length - position - 2;
        for (unsigned bits_used = 3; bits_used < required_bits; ++bits_used) {
          const u64 mask = (u64{1} << bits_used) - 1;
          const u64 lift_lower_bound = target_lift & mask;
          const unsigned crossing =
              relative_coefficient_crossing(prefix, lift_lower_bound);
          const u64 forced_lower_bound =
              lift_lower_bound + (u64{1} << bits_used);
          if (crossing != 0 && suffix_length > crossing &&
              static_cast<i128>(gap) * forced_lower_bound + prefix_surplus >
                  0) {
            if (forced_lower_bound > target_lift) {
              throw std::runtime_error(
                  "adaptive shadow forcing did not lower-bound the lift");
            }
            symbolic_bits = bits_used;
            ++counts.adaptive_shadow_certificates;
            break;
          }
        }
      }
      ++counts.certificate_bits[required_bits];
      ++counts.symbolic_certificate_bits[symbolic_bits];
      if (symbolic_bits > counts.maximum_symbolic_certificate_bits) {
        counts.maximum_symbolic_certificate_bits = symbolic_bits;
        counts.maximum_symbolic_certificate_length = length;
        counts.maximum_symbolic_certificate_position = position;
        counts.maximum_symbolic_certificate_word =
            chronological_word(bits, length);
      }
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
  if (argc > 2) {
    if (std::string(argv[2]) != "--emit-ladder") {
      std::cerr << "second argument, when present, must be --emit-ladder\n";
      return EXIT_FAILURE;
    }
    counts.emit_ladder = true;
  }
  enumerate(0, Cylinder{}, max_length, counts);
  std::cout << "max_length=" << max_length << '\n'
            << "first_crossings=" << counts.first_crossings << '\n'
            << "candidate_edges=" << counts.candidate_edges << '\n'
            << "wrapped_edges=" << counts.wrapped_edges << '\n'
            << "positive_prefix_surplus=" << counts.positive_prefix_surplus << '\n'
            << "nonpositive_prefix_surplus=" << counts.nonpositive_prefix_surplus << '\n'
            << "low_two_bit_certificates="
            << counts.low_two_bit_certificates << '\n'
            << "base_shadow_certificates="
            << counts.base_shadow_certificates << '\n'
            << "base_shadow_prefixes="
            << counts.shadow_crossing_cache.size() << '\n'
            << "unresolved_after_base_shadow="
            << counts.unresolved_after_base_shadow << '\n'
            << "adaptive_shadow_certificates="
            << counts.adaptive_shadow_certificates << '\n'
            << "excluded_lift_ladder_certificates="
            << counts.excluded_lift_ladder_certificates << '\n'
            << "excluded_lift_ladder_candidates="
            << counts.excluded_lift_ladder_candidates << '\n'
            << "excluded_lift_ladder_parity_bits="
            << counts.excluded_lift_ladder_parity_bits << '\n'
            << "maximum_excluded_lift_ladder_steps="
            << counts.maximum_excluded_lift_ladder_steps << '\n'
            << "maximum_excluded_lift_ladder_example=K:"
            << counts.maximum_excluded_lift_ladder_length
            << ",j:" << counts.maximum_excluded_lift_ladder_position
            << ",word:" << counts.maximum_excluded_lift_ladder_word << '\n'
            << "maximum_excluded_lift_mismatch_depth="
            << counts.maximum_excluded_lift_mismatch_depth << '\n'
            << "maximum_excluded_lift_mismatch_example=K:"
            << counts.maximum_excluded_lift_mismatch_length
            << ",j:" << counts.maximum_excluded_lift_mismatch_position
            << ",word:" << counts.maximum_excluded_lift_mismatch_word << '\n'
            << "descent_failures=" << counts.descent_failures << '\n'
            << "minimum_margin=" << counts.minimum_margin << '\n'
            << "minimum_margin_length=" << counts.minimum_margin_length << '\n'
            << "minimum_margin_word=" << counts.minimum_margin_word << '\n';
  for (const auto &[bits_used, count] : counts.certificate_bits) {
    std::cout << "certificate_bits=" << bits_used << ",edges=" << count << '\n';
  }
  for (const auto &[bits_used, count] : counts.symbolic_certificate_bits) {
    std::cout << "symbolic_certificate_bits=" << bits_used
              << ",edges=" << count << '\n';
  }
  std::cout << "maximum_certificate_bits=" << counts.maximum_certificate_bits
            << '\n'
            << "maximum_certificate_example=K:"
            << counts.maximum_certificate_length
            << ",j:" << counts.maximum_certificate_position
            << ",word:" << counts.maximum_certificate_word << '\n';
  std::cout << "maximum_symbolic_certificate_bits="
            << counts.maximum_symbolic_certificate_bits << '\n'
            << "maximum_symbolic_certificate_example=K:"
            << counts.maximum_symbolic_certificate_length
            << ",j:" << counts.maximum_symbolic_certificate_position
            << ",word:" << counts.maximum_symbolic_certificate_word << '\n';
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
  for (const auto &[key, stats] : counts.shadow_prefix_stats) {
    static_cast<void>(key);
    std::cout << "shadow_prefix=j:" << stats.position
              << ",word:"
              << chronological_word(stats.prefix_bits, stats.position)
              << ",chi2:" << stats.lift_mod_four
              << ",y2:" << stats.shadow_value
              << ",sigma:" << stats.crossing
              << ",edges:" << stats.edges
              << ",certified:" << stats.certified
              << ",unresolved:" << stats.unresolved
              << ",maximum_raw_bits:" << stats.maximum_raw_bits << '\n';
  }
  std::cout << "status=exact split-barrier audit passed\n";
}
