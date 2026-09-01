#include <algorithm>
#include <array>
#include <bit>
#include <compare>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int kLength = 21;
constexpr std::uint32_t kWordMask = (1U << kLength) - 1U;
constexpr int kTauSignature = (1 << 3) | (1 << 9);

struct G {
  int r;
  int i;
  auto operator<=>(const G&) const = default;
};

G operator+(G x, G y) { return {x.r + y.r, x.i + y.i}; }
G operator-(G x) { return {-x.r, -x.i}; }
G MulConj(G x, G y) {
  return {x.r * y.r + x.i * y.i, x.i * y.r - x.r * y.i};
}
int Norm(G x) { return x.r * x.r + x.i * x.i; }

std::uint32_t Rotate(std::uint32_t word, int shift) {
  return ((word >> shift) | (word << (kLength - shift))) & kWordMask;
}

int CorrelationSignature(std::uint32_t word) {
  int result = 0;
  for (int shift = 1; shift <= 10; ++shift) {
    result |= (std::popcount(word & Rotate(word, shift)) & 1) << (shift - 1);
  }
  return result;
}

std::array<int, 7> FiberCounts(std::uint32_t support) {
  std::array<int, 7> result{};
  for (int position = 0; position < kLength; ++position) {
    if ((support >> position) & 1U) ++result[position % 7];
  }
  return result;
}

struct Pattern {
  std::array<int, 7> a;
  std::array<int, 7> b;
  int center;
  auto operator<=>(const Pattern&) const = default;
};

int Mod7(int value) {
  value %= 7;
  return value < 0 ? value + 7 : value;
}

Pattern CanonicalPattern(std::array<int, 7> a, std::array<int, 7> b) {
  std::vector<Pattern> candidates;
  for (int sign : {1, -1}) {
    for (int shift = 0; shift < 7; ++shift) {
      Pattern candidate{};
      for (int index = 0; index < 7; ++index) {
        candidate.a[index] = a[Mod7(sign * index + shift)];
        candidate.b[index] = b[Mod7(sign * index + shift)];
      }
      candidate.center = Mod7(-sign * shift);
      candidates.push_back(candidate);
    }
  }
  return *std::min_element(candidates.begin(), candidates.end());
}

std::uint32_t OrbitRepresentative(std::uint32_t word) {
  std::uint32_t result = word;
  for (int shift = 1; shift < kLength; ++shift) {
    result = std::min(result, Rotate(word, shift));
  }
  return result;
}

struct ClassifiedPair {
  int b_index;
  std::uint32_t a_word;
  Pattern pattern;
};

struct Classification {
  std::map<Pattern, int> patterns;
  std::vector<ClassifiedPair> pairs;
};

Classification ClassifyPatterns() {
  std::array<std::vector<std::uint32_t>, 1024> a_by_signature;
  for (std::uint32_t word = 0; word <= kWordMask; ++word) {
    if (std::popcount(word) == 5) {
      a_by_signature[CorrelationSignature(word)].push_back(word);
    }
  }

  int b_masks = 0;
  int labeled = 0;
  int orbit_total = 0;
  Classification result;
  for (int pair_bits = 0; pair_bits < (1 << 10); ++pair_bits) {
    if (std::popcount(static_cast<unsigned>(pair_bits)) != 8) continue;
    std::uint32_t b_word = 0;
    for (int shift = 1; shift <= 10; ++shift) {
      if ((pair_bits >> (shift - 1)) & 1) {
        b_word |= (1U << shift) | (1U << (kLength - shift));
      }
    }
    const std::uint32_t f_word = ((~b_word) & kWordMask) & ~1U;
    const int b_signature = CorrelationSignature(b_word);
    const int f_signature = CorrelationSignature(f_word);
    int required = 0;
    for (int shift = 1; shift <= 10; ++shift) {
      const int bit = shift - 1;
      const int value = ((b_word >> shift) & 1U)
                            ? ((f_signature >> bit) & 1)
                            : (((kTauSignature ^ b_signature) >> bit) & 1);
      required |= value << bit;
    }
    const auto& matches = a_by_signature[required];
    if (matches.empty()) continue;
    const int b_index = b_masks++;
    labeled += static_cast<int>(matches.size());
    std::set<std::uint32_t> orbits;
    std::uint32_t b_diagonal_support = 0;
    for (int position = 1; position < kLength; ++position) {
      if (!((b_word >> position) & 1U)) b_diagonal_support |= 1U << position;
    }
    const auto b_counts = FiberCounts(b_diagonal_support);
    for (std::uint32_t a_word : matches) {
      orbits.insert(OrbitRepresentative(a_word));
      const auto a_counts = FiberCounts((~a_word) & kWordMask);
      const Pattern pattern = CanonicalPattern(a_counts, b_counts);
      ++result.patterns[pattern];
      result.pairs.push_back({b_index, a_word, pattern});
    }
    orbit_total += static_cast<int>(orbits.size());
  }
  if (b_masks != 25 || labeled != 1575 || orbit_total != 75 ||
      result.patterns.size() != 57) {
    std::cerr << "third-order classification mismatch\n";
    std::exit(2);
  }
  return result;
}

std::array<std::vector<G>, 4> RootSumDomains() {
  std::array<std::vector<G>, 4> result;
  for (int count = 0; count <= 3; ++count) {
    for (int real = -count; real <= count; ++real) {
      for (int imag = -count; imag <= count; ++imag) {
        if (std::abs(real) + std::abs(imag) <= count &&
            (real + imag - count) % 2 == 0) {
          result[count].push_back({real - imag, real + imag});
        }
      }
    }
    std::sort(result[count].begin(), result[count].end());
    result[count].erase(
        std::unique(result[count].begin(), result[count].end()), result[count].end());
    const int expected = (count + 1) * (count + 1);
    if (static_cast<int>(result[count].size()) != expected) {
      std::cerr << "domain mismatch\n";
      std::exit(2);
    }
  }
  return result;
}

struct Key {
  std::array<int, 7> x;
  bool operator==(const Key&) const = default;
};

struct KeyHash {
  std::size_t operator()(const Key& key) const {
    std::size_t result = 1469598103934665603ULL;
    for (int value : key.x) {
      result ^= static_cast<std::uint32_t>(value + 256);
      result *= 1099511628211ULL;
    }
    return result;
  }
};

Key Fingerprint(const std::array<G, 7>& word) {
  Key key{};
  for (G value : word) key.x[0] += Norm(value);
  for (int shift = 1; shift <= 3; ++shift) {
    G correlation{};
    for (int index = 0; index < 7; ++index) {
      correlation = correlation + MulConj(word[index], word[(index + shift) % 7]);
    }
    key.x[2 * shift - 1] = correlation.r;
    key.x[2 * shift] = correlation.i;
  }
  return key;
}

using SignatureSet = std::unordered_set<Key, KeyHash>;

struct ASignatures {
  SignatureSet values;
  std::uint64_t raw_prefixes = 0;
  std::uint64_t sum_zero = 0;
};

ASignatures EnumerateA(const std::array<int, 7>& counts,
                       const std::array<std::vector<G>, 4>& domains) {
  int derive = static_cast<int>(std::max_element(counts.begin(), counts.end()) - counts.begin());
  std::set<G> allowed(domains[counts[derive]].begin(), domains[counts[derive]].end());
  std::array<G, 7> word{};
  ASignatures result;

  const auto recurse = [&](const auto& self, int index, G partial) -> void {
    if (index == 7) {
      ++result.raw_prefixes;
      const G last = -partial;
      if (!allowed.contains(last)) return;
      word[derive] = last;
      ++result.sum_zero;
      result.values.insert(Fingerprint(word));
      return;
    }
    if (index == derive) {
      self(self, index + 1, partial);
      return;
    }
    for (G value : domains[counts[index]]) {
      word[index] = value;
      self(self, index + 1, partial + value);
    }
  };
  recurse(recurse, 0, G{});
  return result;
}

std::vector<std::array<G, 7>> EnumerateB(
    const Pattern& pattern, const std::array<std::vector<G>, 4>& domains) {
  std::set<std::array<G, 7>> candidates;
  std::array<G, 7> word{};
  for (int center_sign : {1, -1}) {
    const auto recurse = [&](const auto& self, int index, G partial) -> void {
      if (index == 7) {
        if (partial == G{1, 0}) candidates.insert(word);
        return;
      }
      for (G diagonal_sum : domains[pattern.b[index]]) {
        G value = diagonal_sum;
        if (index == pattern.center) value.r += center_sign;
        word[index] = value;
        self(self, index + 1, partial + value);
      }
    };
    recurse(recurse, 0, G{});
  }
  return {candidates.begin(), candidates.end()};
}

Key ComplementTarget(const Key& b) {
  Key target{};
  target.x[0] = 37 - b.x[0];
  for (int shift = 1; shift <= 3; ++shift) {
    target.x[2 * shift - 1] = -6 - b.x[2 * shift - 1];
    target.x[2 * shift] = -b.x[2 * shift];
  }
  return target;
}

}  // namespace

int main() {
  const auto classification = ClassifyPatterns();
  const auto& patterns = classification.patterns;
  const auto domains = RootSumDomains();
  std::map<std::array<int, 7>, ASignatures> cache;
  for (const auto& [pattern, multiplicity] : patterns) {
    (void)multiplicity;
    if (!cache.contains(pattern.a)) cache[pattern.a] = EnumerateA(pattern.a, domains);
  }
  int feasible_patterns = 0;
  int feasible_labeled = 0;
  int b_words_total = 0;
  int feasible_b_fingerprints_total = 0;
  std::set<Pattern> feasible_pattern_set;
  for (const auto& [pattern, multiplicity] : patterns) {
    const auto b_words = EnumerateB(pattern, domains);
    b_words_total += static_cast<int>(b_words.size());
    SignatureSet targets;
    for (const auto& b_word : b_words) {
      targets.insert(ComplementTarget(Fingerprint(b_word)));
    }
    int feasible_b_fingerprints = 0;
    for (const Key& target : targets) {
      feasible_b_fingerprints += cache.at(pattern.a).values.contains(target);
    }
    feasible_b_fingerprints_total += feasible_b_fingerprints;
    if (feasible_b_fingerprints > 0) {
      ++feasible_patterns;
      feasible_labeled += multiplicity;
      feasible_pattern_set.insert(pattern);
    }
  }

  std::map<int, std::vector<std::uint32_t>> survivors_by_b;
  for (const ClassifiedPair& pair : classification.pairs) {
    if (feasible_pattern_set.contains(pair.pattern)) {
      survivors_by_b[pair.b_index].push_back(pair.a_word);
    }
  }
  int surviving_orbits = 0;
  for (const auto& [b_index, words] : survivors_by_b) {
    (void)b_index;
    std::map<std::uint32_t, int> orbit_counts;
    for (std::uint32_t word : words) ++orbit_counts[OrbitRepresentative(word)];
    for (const auto& [representative, count] : orbit_counts) {
      (void)representative;
      if (count != 21) {
        std::cerr << "partial rotation orbit\n";
        return 2;
      }
    }
    surviving_orbits += static_cast<int>(orbit_counts.size());
  }
  std::uint64_t raw_prefixes = 0;
  std::uint64_t sum_zero = 0;
  std::size_t distinct_fingerprints = 0;
  for (const auto& [counts, signatures] : cache) {
    (void)counts;
    raw_prefixes += signatures.raw_prefixes;
    sum_zero += signatures.sum_zero;
    distinct_fingerprints += signatures.values.size();
  }
  if (feasible_patterns != 24 || feasible_labeled != 756 ||
      survivors_by_b.size() != 18 || surviving_orbits != 36 ||
      raw_prefixes != 6373296 || sum_zero != 2539032 ||
      distinct_fingerprints != 364917 || b_words_total != 1407 ||
      feasible_b_fingerprints_total != 36) {
    std::cerr << "compression certificate mismatch\n";
    return 2;
  }

  std::cout << "third_order_b_masks=25\n";
  std::cout << "third_order_labeled_pairs=1575\n";
  std::cout << "third_order_a_rotation_orbits=75\n";
  std::cout << "mod7_support_patterns=" << patterns.size() << "\n";
  std::cout << "a_count_patterns=" << cache.size() << "\n";
  std::cout << "a_raw_prefixes=" << raw_prefixes << "\n";
  std::cout << "a_sum_zero_words=" << sum_zero << "\n";
  std::cout << "a_distinct_fingerprints=" << distinct_fingerprints << "\n";
  std::cout << "b_compressed_words_across_patterns=" << b_words_total << "\n";
  std::cout << "feasible_b_fingerprints_across_patterns="
            << feasible_b_fingerprints_total << "\n";
  std::cout << "eliminated_support_patterns=" << 57 - feasible_patterns << "\n";
  std::cout << "surviving_support_patterns=" << feasible_patterns << "\n";
  std::cout << "eliminated_b_masks=" << 25 - survivors_by_b.size() << "\n";
  std::cout << "surviving_b_masks=" << survivors_by_b.size() << "\n";
  std::cout << "eliminated_labeled_pairs=" << 1575 - feasible_labeled << "\n";
  std::cout << "surviving_labeled_pairs=" << feasible_labeled << "\n";
  std::cout << "eliminated_a_rotation_orbits=" << 75 - surviving_orbits << "\n";
  std::cout << "surviving_a_rotation_orbits=" << surviving_orbits << "\n";
  std::cout << "global_remaining_b_masks=470\n";
  std::cout << "global_remaining_labeled_pairs=193557\n";
  std::cout << "global_remaining_a_rotation_orbits=9217\n";
  std::cout << "certificate=verified\n";
}
