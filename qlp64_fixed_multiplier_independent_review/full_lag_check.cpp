// Independent final-stage audit: generic orbit constraints and all lags.
// No imports or includes from the reviewed implementation.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

using Word = std::uint64_t;
using Row = std::array<int, 32>;
using Quad = std::array<Row, 4>;
using Assignment = std::vector<int>;

void require(bool condition, const char *message) {
  if (!condition) throw std::runtime_error(message);
}

struct Lift {
  Word word;
  std::array<Word, 32> shifted;
  std::array<int, 32> autocorrelation;
};

int correlation(Word a, Word b) {
  return 64 - 2 * std::popcount(a ^ b);
}

// Use a generic system of negative-count equations on multiplier orbits:
// t_orbit(j) + t_orbit(j+32) = 1-z[j]. This avoids the special-case
// j-parity lift formulas in the reviewed implementation.
std::vector<Lift> enumerate_lifts(const Row &z, int h) {
  std::array<int, 64> orbit;
  orbit.fill(-1);
  std::vector<Word> masks;
  for (int j = 0; j < 64; ++j) {
    if (orbit[j] != -1) continue;
    int id = static_cast<int>(masks.size());
    Word mask = 0;
    int k = j;
    do {
      require(orbit[k] == -1, "overlapping multiplier orbits");
      orbit[k] = id;
      mask |= Word{1} << k;
      k = h*k % 64;
    } while (k != j);
    masks.push_back(mask);
  }
  std::vector<Lift> output;
  auto visit = [&](auto &&self, Assignment a) -> void {
    bool changed = true;
    while (changed) {
      changed = false;
      for (int j = 0; j < 32; ++j) {
        int u = orbit[j], v = orbit[j+32], target = 1-z[j];
        if (u == v) {
          if (target % 2) return;
          int value = target/2;
          if (a[u] != -1 && a[u] != value) return;
          if (a[u] == -1) { a[u] = value; changed = true; }
        } else if (a[u] != -1 && a[v] != -1) {
          if (a[u]+a[v] != target) return;
        } else if (a[u] != -1 || a[v] != -1) {
          int known = a[u] != -1 ? u : v;
          int unknown = known == u ? v : u;
          int value = target-a[known];
          if (value < 0 || value > 1) return;
          a[unknown] = value;
          changed = true;
        } else if (target == 0 || target == 2) {
          a[u] = a[v] = target/2;
          changed = true;
        }
      }
    }
    auto unknown = std::find(a.begin(), a.end(), -1);
    if (unknown != a.end()) {
      std::size_t j = static_cast<std::size_t>(unknown-a.begin());
      a[j] = 0; self(self, a);
      a[j] = 1; self(self, a);
      return;
    }
    Word w = 0;
    for (std::size_t j = 0; j < a.size(); ++j)
      if (a[j]) w |= masks[j];
    for (int j = 0; j < 32; ++j)
      require(1-static_cast<int>((w >> j)&1)-static_cast<int>((w >> (j+32))&1)
                  == z[j], "compression mismatch");
    for (int j = 0; j < 64; ++j)
      require(((w >> j)&1) == ((w >> (h*j%64))&1), "invariance mismatch");
    Lift lifted{};
    lifted.word = w;
    for (int k = 1; k <= 32; ++k) {
      // Explicit shift rather than std::rotr; k is never 0 or 64.
      lifted.shifted[k-1] = (w >> k) | (w << (64-k));
      lifted.autocorrelation[k-1] = correlation(w, lifted.shifted[k-1]);
    }
    output.push_back(lifted);
  };
  visit(visit, Assignment(masks.size(), -1));
  return output;
}

// Unscaled 16-bit integer keys: all 32 real lags and all 31 skew lags.
// Opposite skew orientations are matched explicitly, not canonicalized.
struct Key {
  std::array<std::int16_t, 63> value{};
  bool operator==(const Key &) const = default;
};
struct Hash {
  std::size_t operator()(const Key &key) const {
    std::uint64_t result = 0;
    for (auto x : key.value)
      result = result*1000003ULL + static_cast<std::uint16_t>(x);
    return static_cast<std::size_t>(result);
  }
};
Key key_for(const Lift &a, const Lift &b) {
  Key key;
  for (int k = 0; k < 32; ++k)
    key.value[k] = static_cast<std::int16_t>(a.autocorrelation[k]+b.autocorrelation[k]);
  for (int k = 0; k < 31; ++k)
    key.value[32+k] = static_cast<std::int16_t>(
        correlation(a.word, b.shifted[k])-correlation(b.word, a.shifted[k]));
  return key;
}

int main(int argc, char **argv) {
  require(argc == 3, "usage: full_lag_check COMPRESSED_INPUT MULTIPLIER");
  const int h = std::stoi(argv[2]);
  require(h == 31 || h == 63, "unsupported multiplier");
  std::ifstream file(argv[1]);
  std::size_t count = 0;
  require(bool(file >> count) && count == 1472, "unexpected parent count");
  std::vector<Quad> quads(count);
  std::map<Row, std::vector<Lift>> rows;
  for (auto &q : quads) {
    for (std::size_t r = 0; r < 4; ++r) {
      int sum = 0;
      for (int &v : q[r]) {
        require(bool(file >> v) && v >= -1 && v <= 1, "invalid input entry");
        sum += v;
      }
      require(sum == (r == 3 ? 1 : 0), "invalid row sum");
      require(q[r][16] != 0 && (q[r][0] == 0) == (r == 3), "endpoint parity");
      for (int j = 0; j < 32; ++j)
        require(q[r][j] == q[r][(32-j)%32], "nonsymmetric input row");
      rows.try_emplace(q[r]);
    }
    for (int k = 0; k < 32; ++k) {
      int sum = 0;
      for (const auto &r : q)
        for (int j = 0; j < 32; ++j) sum += r[j]*r[(j+k)%32];
      require(sum == (k ? -2 : 63), "invalid compressed autocorrelations");
    }
  }
  std::string trailing;
  require(!(file >> trailing), "trailing input");
  std::uint64_t words = 0;
  for (auto &[row, lifts] : rows) {
    lifts = enumerate_lifts(row, h);
    require(!lifts.empty(), "empty lift set");
    words += lifts.size();
  }
  std::uint64_t pairs = 0, stored = 0;
  for (std::size_t qi = 0; qi < count; ++qi) {
    std::array<const std::vector<Lift> *, 4> lifted{};
    for (int r = 0; r < 4; ++r) lifted[r] = &rows.at(quads[qi][r]);
    // For 63, both paired rows are reversible, so every skew term is zero.
    // Still compute every skew term; only the redundant pairings are omitted.
    for (int mate = 0; mate < (h == 31 ? 3 : 1); ++mate) {
      std::vector<int> other;
      for (int r = 0; r < 3; ++r) if (r != mate) other.push_back(r);
      int a = mate, b = 3, c = other[0], d = other[1];
      if (lifted[a]->size()*lifted[b]->size() > lifted[c]->size()*lifted[d]->size()) {
        std::swap(a,c); std::swap(b,d);
      }
      std::unordered_set<Key, Hash> table;
      table.reserve(lifted[a]->size()*lifted[b]->size());
      for (const auto &x : *lifted[a]) for (const auto &y : *lifted[b]) {
        auto key = key_for(x,y);
        if (h == 63) for (int k = 32; k < 63; ++k)
          require(key.value[k] == 0, "reversible pair has skew correlation");
        table.insert(key);
        ++pairs;
      }
      stored += table.size();
      for (const auto &x : *lifted[c]) for (const auto &y : *lifted[d]) {
        auto wanted = key_for(x,y);
        if (h == 63) for (int k = 32; k < 63; ++k)
          require(wanted.value[k] == 0, "reversible pair has skew correlation");
        for (int k = 0; k < 32; ++k) wanted.value[k] = static_cast<std::int16_t>(-4-wanted.value[k]);
        require(!table.contains(wanted), "compatible full-lag pair found (same skew)");
        for (int k = 32; k < 63; ++k) wanted.value[k] = static_cast<std::int16_t>(-wanted.value[k]);
        require(!table.contains(wanted), "compatible full-lag pair found (opposite skew)");
        ++pairs;
      }
    }
    if ((qi+1)%128 == 0) std::cerr << "checked " << qi+1 << "/" << count << " parents\n";
  }
  std::cout << "{\"multiplier\":" << h << ",\"parents\":" << count
            << ",\"distinct_rows\":" << rows.size() << ",\"full_words\":" << words
            << ",\"row_pairs\":" << pairs << ",\"stored_signed_keys\":" << stored
            << ",\"witnesses\":0,\"status\":\"PASS\"}\n";
}
