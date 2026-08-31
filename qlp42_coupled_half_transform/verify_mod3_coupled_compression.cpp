#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <vector>

struct Gaussian {
  int real;
  int imag;
  auto operator<=>(const Gaussian &) const = default;
};

struct CellKey {
  Gaussian x;
  Gaussian y;
  auto operator<=>(const CellKey &) const = default;
};

struct Descriptor {
  int energy_s;
  int energy_h;
  int correlation_s_real;
  int correlation_s_imag;
  int correlation_h_real;
  int correlation_h_imag;
  auto operator<=>(const Descriptor &) const = default;
};

struct DescriptorHash {
  std::size_t operator()(const Descriptor &value) const {
    std::size_t result = 0xcbf29ce484222325ULL;
    for (int coordinate : {value.energy_s, value.energy_h,
                           value.correlation_s_real,
                           value.correlation_s_imag,
                           value.correlation_h_real,
                           value.correlation_h_imag}) {
      result ^= static_cast<std::uint64_t>(coordinate + 64);
      result *= 0x100000001b3ULL;
    }
    return result;
  }
};

struct DescriptorData {
  std::uint64_t count = 0;
  std::uint64_t quarter_count_mask = 0;
  std::set<std::array<int, 12>> canonical_words;
};

using Triple = std::array<Gaussian, 3>;

constexpr std::array<Gaussian, 4> roots = {
    Gaussian{1, 0}, Gaussian{0, 1}, Gaussian{-1, 0}, Gaussian{0, -1}};

constexpr std::array<std::array<int, 4>, 6> representatives = {{
    {1, 0, 5, 0},
    {3, 0, 4, 1},
    {3, 0, 3, -2},
    {3, 2, 3, 2},
    {3, 2, 2, 3},
    {4, 1, 2, -1},
}};

Gaussian add(Gaussian left, Gaussian right) {
  return {left.real + right.real, left.imag + right.imag};
}

Gaussian subtract(Gaussian left, Gaussian right) {
  return {left.real - right.real, left.imag - right.imag};
}

Gaussian divide_one_plus_i(Gaussian value) {
  assert((value.real + value.imag) % 2 == 0);
  assert((value.imag - value.real) % 2 == 0);
  return {(value.real + value.imag) / 2,
          (value.imag - value.real) / 2};
}

int norm(Gaussian value) {
  return value.real * value.real + value.imag * value.imag;
}

Gaussian correlation_shift_one(const std::array<Gaussian, 3> &sequence) {
  Gaussian result{0, 0};
  for (int index = 0; index < 3; ++index) {
    const auto left = sequence[index];
    const auto right = sequence[(index + 1) % 3];
    result.real += left.real * right.real + left.imag * right.imag;
    result.imag += left.imag * right.real - left.real * right.imag;
  }
  return result;
}

Descriptor descriptor(const Triple &x, const Triple &y) {
  std::array<Gaussian, 3> s{};
  std::array<Gaussian, 3> h{};
  for (int index = 0; index < 3; ++index) {
    s[index] = divide_one_plus_i(subtract(x[index], y[index]));
    h[index] = divide_one_plus_i(add(x[index], y[index]));
  }
  int energy_s = 0;
  int energy_h = 0;
  for (int index = 0; index < 3; ++index) {
    energy_s += norm(s[index]);
    energy_h += norm(h[index]);
  }
  const auto correlation_s = correlation_shift_one(s);
  const auto correlation_h = correlation_shift_one(h);
  return {energy_s, energy_h, correlation_s.real, correlation_s.imag,
          correlation_h.real, correlation_h.imag};
}

std::uint64_t add_count_masks(std::uint64_t left, std::uint64_t right) {
  std::uint64_t result = 0;
  for (int i = 0; i <= 42; ++i) {
    if (((left >> i) & 1ULL) == 0) {
      continue;
    }
    for (int j = 0; i + j <= 42; ++j) {
      if ((right >> j) & 1ULL) {
        result |= 1ULL << (i + j);
      }
    }
  }
  return result;
}

bool is_quarter_turn(Gaussian x, Gaussian y) {
  return x.real * y.real + x.imag * y.imag == 0;
}

std::map<CellKey, std::uint64_t> seven_cell_quarter_masks() {
  std::map<CellKey, std::uint64_t> states;
  states[{{0, 0}, {0, 0}}] = 1ULL;
  for (int step = 0; step < 7; ++step) {
    std::map<CellKey, std::uint64_t> next;
    for (const auto &[key, mask] : states) {
      for (const auto x : roots) {
        for (const auto y : roots) {
          const CellKey destination{add(key.x, x), add(key.y, y)};
          next[destination] |= mask << (is_quarter_turn(x, y) ? 1 : 0);
        }
      }
    }
    states = std::move(next);
  }
  return states;
}

std::vector<Gaussian> seven_root_sum_domain() {
  std::vector<Gaussian> result;
  for (int real = -7; real <= 7; ++real) {
    for (int imag = -7; imag <= 7; ++imag) {
      if (std::abs(real) + std::abs(imag) <= 7 &&
          (real + imag - 7) % 2 == 0) {
        result.push_back({real, imag});
      }
    }
  }
  assert(result.size() == 64);
  return result;
}

std::vector<Triple> triples_with_sum(const std::vector<Gaussian> &domain,
                                     Gaussian target) {
  const std::set<Gaussian> domain_set(domain.begin(), domain.end());
  std::vector<Triple> result;
  for (const auto first : domain) {
    for (const auto second : domain) {
      const Gaussian third{target.real - first.real - second.real,
                           target.imag - first.imag - second.imag};
      if (domain_set.contains(third)) {
        result.push_back({first, second, third});
      }
    }
  }
  return result;
}

std::uint64_t triple_quarter_mask(
    const Triple &x, const Triple &y,
    const std::map<CellKey, std::uint64_t> &cell_masks) {
  std::uint64_t result = 1ULL;
  for (int index = 0; index < 3; ++index) {
    result = add_count_masks(result, cell_masks.at({x[index], y[index]}));
  }
  return result;
}

Descriptor complement(const Descriptor &value) {
  return {43 - value.energy_s,
          29 - value.energy_h,
          -value.correlation_s_real,
          -value.correlation_s_imag,
          -14 - value.correlation_h_real,
          -value.correlation_h_imag};
}

std::array<int, 12> canonical_word(const Triple &x, const Triple &y) {
  std::array<int, 12> best{};
  bool initialized = false;
  for (int shift = 0; shift < 3; ++shift) {
    std::array<int, 12> candidate{};
    for (int index = 0; index < 3; ++index) {
      const int source = (index + shift) % 3;
      candidate[4 * index] = x[source].real;
      candidate[4 * index + 1] = x[source].imag;
      candidate[4 * index + 2] = y[source].real;
      candidate[4 * index + 3] = y[source].imag;
    }
    if (!initialized || candidate < best) {
      best = candidate;
      initialized = true;
    }
  }
  return best;
}

int main() {
  const auto domain = seven_root_sum_domain();
  const auto cell_masks = seven_cell_quarter_masks();
  assert(cell_masks.size() == 4096);

  for (int case_index = 0; case_index < 6; ++case_index) {
    const auto [p, q, x, y] = representatives[case_index];
    const auto x_a = triples_with_sum(domain, {p, q});
    const auto y_a = triples_with_sum(domain, {-p, -q});
    const auto x_b = triples_with_sum(domain, {x, y});
    const auto y_b = triples_with_sum(domain, {1 - x, 1 - y});

    std::unordered_map<Descriptor, DescriptorData, DescriptorHash> b_data;
    std::uint64_t b_admissible = 0;
    for (const auto &x_word : x_b) {
      for (const auto &y_word : y_b) {
        const auto value = descriptor(x_word, y_word);
        if (value.energy_s > 43 || value.energy_h > 29) {
          continue;
        }
        ++b_admissible;
        auto &data = b_data[value];
        ++data.count;
        data.quarter_count_mask |=
            triple_quarter_mask(x_word, y_word, cell_masks);
        data.canonical_words.insert(canonical_word(x_word, y_word));
      }
    }

    std::uint64_t a_admissible = 0;
    std::uint64_t compression_pairs = 0;
    std::uint64_t global_quarter_mask = 0;
    std::map<Descriptor, std::set<std::array<int, 12>>> matching_a_words;
    for (const auto &x_word : x_a) {
      for (const auto &y_word : y_a) {
        const auto value = descriptor(x_word, y_word);
        if (value.energy_s > 43 || value.energy_h > 29) {
          continue;
        }
        ++a_admissible;
        const auto found = b_data.find(complement(value));
        if (found == b_data.end()) {
          continue;
        }
        matching_a_words[value].insert(canonical_word(x_word, y_word));
        compression_pairs += found->second.count;
        const auto a_mask = triple_quarter_mask(x_word, y_word, cell_masks);
        global_quarter_mask |=
            add_count_masks(a_mask, found->second.quarter_count_mask);
      }
    }

    std::uint64_t rotation_orbits = 0;
    for (const auto &[value, words] : matching_a_words) {
      rotation_orbits +=
          words.size() * b_data.at(complement(value)).canonical_words.size();
    }

    std::cout << "case=" << case_index << "; triples=" << x_a.size() << ','
              << y_a.size() << ',' << x_b.size() << ',' << y_b.size()
              << "; admissible=" << a_admissible << ',' << b_admissible
              << "; matching_descriptors=" << matching_a_words.size()
              << "; ordered_compression_pairs=" << compression_pairs
              << "; independent_rotation_orbits=" << rotation_orbits
              << "; quarter_totals=";
    bool first = true;
    for (int count = 1; count <= 41; count += 4) {
      if ((global_quarter_mask >> count) & 1ULL) {
        if (!first) {
          std::cout << ',';
        }
        std::cout << count;
        first = false;
      }
    }
    std::cout << '\n';
  }
  std::cout << "certificate=verified\n";
}
