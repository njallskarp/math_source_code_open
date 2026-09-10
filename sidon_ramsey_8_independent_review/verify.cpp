// Independent referee implementation, 2026-09-10. Standard-library exact
// arithmetic. No producer source or generated catalogue is imported. See
// README.md for proof.
#include <algorithm>
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using Mask = __uint128_t;
void require(bool v, const char *why) {
  if (!v)
    throw std::runtime_error(why);
}
int count(Mask x) {
  return __builtin_popcountll(uint64_t(x)) +
         __builtin_popcountll(uint64_t(x >> 64));
}
int low(Mask x) {
  require(x != 0, "empty low");
  return uint64_t(x) ? __builtin_ctzll(uint64_t(x))
                     : 64 + __builtin_ctzll(uint64_t(x >> 64));
}
std::vector<int> points(Mask s) {
  std::vector<int> a;
  while (s) {
    a.push_back(low(s));
    s &= s - 1;
  }
  return a;
}
bool sidon(Mask m) { // Definition-level diagonal pair-sum check, used outside
                     // generation.
  auto a = points(m);
  std::array<bool, 169> sums{};
  for (size_t i = 0; i < a.size(); ++i)
    for (size_t j = i; j < a.size(); ++j) {
      int s = a[i] + a[j];
      if (sums[size_t(s)])
        return false;
      sums[size_t(s)] = true;
    }
  return true;
}
struct Generator {
  int target, maximum;
  std::array<int, 13> selected{};
  uint64_t nodes = 0;
  std::function<void(Mask)> emit;
  void search(int depth, Mask chosen, Mask differences, Mask candidates) {
    ++nodes;
    int need = target - depth;
    if (!need) {
      emit(chosen);
      return;
    }
    if (count(candidates) < need)
      return;
    // A suffix containing 'need' marks has need*(need-1)/2 distinct
    // differences.
    int last_start = maximum - need * (need - 1) / 2;
    while (candidates) {
      int x = low(candidates);
      candidates &= candidates - 1;
      if (x > last_start)
        break;
      Mask fresh = 0;
      for (int i = 0; i < depth; ++i)
        fresh |= Mask(1) << (x - selected[size_t(i)]);
      require(!(fresh & differences), "generator invariant");
      Mask updated = differences | fresh;
      selected[size_t(depth)] = x;
      // All newly forbidden y>x are x+d for a positive difference d in the new
      // prefix.
      search(depth + 1, chosen | (Mask(1) << x), updated,
             candidates & ~(updated << x));
    }
  }
  void run(Mask domain, int k, const std::function<void(Mask)> &callback) {
    target = k;
    maximum = 0;
    for (auto x : points(domain))
      maximum = x;
    emit = callback;
    search(0, 0, 0, domain);
  }
};
void output_set(std::ostream &out, Mask m) {
  bool first = true;
  for (int x : points(m)) {
    if (!first)
      out << ' ';
    out << x;
    first = false;
  }
  out << '\n';
}
void controls() {
  uint64_t checked = 0;
  for (int n = 1; n <= 12; ++n)
    for (int k = 1; k <= std::min(n, 5); ++k) {
      std::vector<Mask> actual, expected;
      Generator g;
      g.run((Mask(1) << n) - 1, k, [&](Mask m) { actual.push_back(m); });
      for (uint64_t m = 0; m < (uint64_t(1) << n); ++m)
        if (__builtin_popcountll(m) == k && sidon(m))
          expected.push_back(m);
      std::sort(actual.begin(), actual.end());
      require(actual == expected, "small catalogue mismatch");
      ++checked;
    }
  // Arbitrary domains and high pair sums exercise gaps and the 64-bit boundary.
  uint64_t seed = 1234567;
  for (int t = 0; t < 100; ++t) {
    Mask d = 0;
    while (count(d) < 10) {
      seed = seed * 6364136223846793005ULL + 1;
      d |= Mask(1) << (seed % 85);
    }
    auto a = points(d);
    for (int k = 3; k <= 5; ++k) {
      std::vector<Mask> actual, expected;
      Generator g;
      g.run(d, k, [&](Mask m) { actual.push_back(m); });
      for (int bits = 0; bits < 1024; ++bits)
        if (__builtin_popcount(unsigned(bits)) == k) {
          Mask m = 0;
          for (int i = 0; i < 10; ++i)
            if (bits & (1 << i))
              m |= Mask(1) << a[size_t(i)];
          if (sidon(m))
            expected.push_back(m);
        }
      std::sort(actual.begin(), actual.end());
      std::sort(expected.begin(), expected.end());
      require(actual == expected, "gapped catalogue mismatch");
      ++checked;
    }
  }
  require(!sidon((Mask(1) << 0) | (Mask(1) << 1) | (Mask(1) << 2)),
          "diagonal control");
  require(sidon((Mask(1) << 0) | (Mask(1) << 1) | (Mask(1) << 3)),
          "positive control");
  std::cout << "{\"enumeration_controls\":" << checked << "}" << std::endl;
}
struct Residual {
  std::vector<Mask> tens, elevens;
  uint64_t total_tens = 0, total_elevens = 0, tested = 0;
  bool solve(Mask r) {
    require(count(r) == 30, "residual order");
    tens.clear();
    elevens.clear();
    Generator g;
    g.run(r, 10, [&](Mask m) { tens.push_back(m); });
    g.run(r, 11, [&](Mask m) { elevens.push_back(m); });
    total_tens += tens.size();
    total_elevens += elevens.size();
    ++tested;
    // No hash lookup or least-point normalization: directly check leftover
    // sums.
    for (size_t i = 0; i < tens.size(); ++i)
      for (size_t j = i + 1; j < tens.size(); ++j)
        if (!(tens[i] & tens[j]) && sidon(r ^ (tens[i] | tens[j])))
          return true;
    for (Mask a : elevens)
      for (Mask b : tens)
        if (!(a & b) && sidon(r ^ (a | b)))
          return true;
    for (size_t i = 0; i < elevens.size(); ++i)
      for (size_t j = i + 1; j < elevens.size(); ++j)
        if (!(elevens[i] & elevens[j]) && sidon(r ^ (elevens[i] | elevens[j])))
          return true;
    return false;
  }
};
struct Packing {
  std::vector<Mask> sets;
  std::vector<int64_t> weights;
  std::array<int, 5> chosen{};
  int64_t threshold;
  uint64_t nodes = 0;
  std::vector<std::array<int, 5>> tuples;
  void search(const std::vector<int> &candidates, int depth, int64_t sum) {
    ++nodes;
    int need = 5 - depth;
    if (!need) {
      if (sum >= threshold)
        tuples.push_back(chosen);
      return;
    }
    if (candidates.size() < size_t(need))
      return;
    int64_t top = sum;
    for (int i = 0; i < need; ++i)
      top += weights[size_t(candidates[size_t(i)])];
    if (top < threshold)
      return;
    for (size_t p = 0; p + size_t(need) <= candidates.size(); ++p) {
      int a = candidates[p];
      if (sum + need * weights[size_t(a)] < threshold)
        break;
      chosen[size_t(depth)] = a;
      std::vector<int> next;
      if (need > 1)
        for (size_t q = p + 1; q < candidates.size(); ++q)
          if (!(sets[size_t(a)] & sets[size_t(candidates[q])]))
            next.push_back(candidates[q]);
      search(next, depth + 1, sum + weights[size_t(a)]);
    }
  }
};
std::vector<int64_t> read_weights(const std::string &path) {
  std::ifstream f(path);
  require(bool(f), "weight open");
  std::vector<int64_t> w;
  int64_t x;
  while (f >> x) {
    require(x >= 0 && x <= 111111, "weight range");
    w.push_back(x);
  }
  require(f.eof() && w.size() == 85, "weight format");
  require(std::accumulate(w.begin(), w.end(), int64_t(0)) == 7899969,
          "weight sum");
  return w;
}
std::vector<Mask> read_sets(const std::string &path) {
  std::ifstream f(path);
  require(bool(f), "set open");
  std::vector<Mask> a;
  std::string line;
  while (std::getline(f, line)) {
    std::istringstream row(line);
    int x;
    Mask m = 0;
    int prev = -1;
    while (row >> x) {
      require(x > prev && x < 85, "set point");
      prev = x;
      m |= Mask(1) << x;
    }
    require(row.eof() && count(m) == 11 && sidon(m), "set format");
    a.push_back(m);
  }
  require(f.eof() && a.size() == 56110, "set read");
  return a;
}
void generate(const std::string &weights_path, const std::string &directory) {
  controls();
  auto w = read_weights(weights_path);
  Mask universe = (Mask(1) << 85) - 1;
  Packing p;
  for (int k = 10; k <= 12; ++k) {
    uint64_t total = 0;
    int64_t max_weight = 0;
    Generator g;
    // Direct labeled enumeration: no translation, endpoint or reflection
    // normalization.
    g.run(universe, k, [&](Mask m) {
      ++total;
      int64_t v = 0;
      for (int x : points(m))
        v += w[size_t(x)];
      max_weight = std::max(max_weight, v);
      if (k == 11)
        p.sets.push_back(m);
    });
    require(total == (k == 10   ? 49479804ULL
                      : k == 11 ? 56110ULL
                                : 0ULL),
            "global count");
    require(max_weight == (k == 10   ? 999996
                           : k == 11 ? 999995
                                     : 0),
            "global maximum weight");
    std::cout << "{\"k\":" << k << ",\"sets\":" << total
              << ",\"max_weight\":" << max_weight << ",\"nodes\":" << g.nodes
              << "}" << std::endl;
  }
  auto weight = [&](Mask m) {
    int64_t v = 0;
    for (int x : points(m))
      v += w[size_t(x)];
    return v;
  };
  std::sort(p.sets.begin(), p.sets.end(), [&](Mask a, Mask b) {
    auto wa = weight(a), wb = weight(b);
    return wa == wb ? a < b : wa > wb;
  });
  std::ofstream sf(directory + "/ordered_sets.txt");
  require(bool(sf), "set output");
  for (Mask m : p.sets) {
    require(sidon(m), "eleven diagonal check");
    output_set(sf, m);
    p.weights.push_back(weight(m));
  }
  sf.close();
  require(bool(sf), "set write");
  p.threshold = std::accumulate(w.begin(), w.end(), int64_t(0)) - 3000000;
  std::vector<int> all(p.sets.size());
  std::iota(all.begin(), all.end(), 0);
  p.search(all, 0, 0);
  require(p.tuples.size() == 130780, "packing count");
  std::ofstream tf(directory + "/packings.txt");
  require(bool(tf), "tuple output");
  std::vector<Mask> residuals;
  Residual control;
  for (auto ids : p.tuples) {
    Mask used = 0;
    int64_t sum = 0;
    for (int i = 0; i < 5; ++i) {
      int id = ids[size_t(i)];
      require(!(used & p.sets[size_t(id)]), "disjointness");
      used |= p.sets[size_t(id)];
      sum += p.weights[size_t(id)];
      tf << (i ? " " : "") << id;
    }
    require(sum >= p.threshold, "packing weight");
    tf << '\n';
    residuals.push_back(universe ^ used);
  }
  tf.close();
  require(bool(tf), "tuple write");
  std::sort(residuals.begin(), residuals.end());
  require(std::adjacent_find(residuals.begin(), residuals.end()) ==
              residuals.end(),
          "duplicate residual");
  for (auto sizes : std::vector<std::array<int, 3>>{
           {10, 10, 10}, {11, 10, 9}, {11, 11, 8}}) {
    Mask r = 0;
    for (int i = 0; i < 3; ++i) {
      auto a = points(p.sets[size_t(p.tuples[0][size_t(i)])]);
      for (int j = 0; j < sizes[size_t(i)]; ++j)
        r |= Mask(1) << a[size_t(j)];
    }
    require(control.solve(r), "positive residual control");
  }
  std::cout << "{\"packings\":" << p.tuples.size()
            << ",\"unique_residuals\":" << residuals.size()
            << ",\"packing_nodes\":" << p.nodes
            << ",\"positive_residual_controls\":3}" << std::endl;
}
void replay(const std::string &directory, int part, int parts) {
  require(part >= 0 && part < parts && parts <= 64, "batch bounds");
  auto sets = read_sets(directory + "/ordered_sets.txt");
  std::ifstream file(directory + "/packings.txt");
  require(bool(file), "tuple open");
  std::string line;
  uint64_t lines = 0;
  Residual test;
  while (std::getline(file, line)) {
    std::istringstream row(line);
    Mask u = 0;
    int id, prev = -1, k = 0;
    while (row >> id) {
      require(id > prev && size_t(id) < sets.size(), "tuple index");
      prev = id;
      require(!(u & sets[size_t(id)]), "tuple overlap");
      u |= sets[size_t(id)];
      ++k;
    }
    require(row.eof() && k == 5, "tuple format");
    if (int(lines % uint64_t(parts)) == part)
      require(!test.solve(((Mask(1) << 85) - 1) ^ u), "PARTITION FOUND");
    ++lines;
  }
  require(file.eof() && lines == 130780, "tuple read");
  std::cout << "{\"part\":" << part << ",\"parts\":" << parts
            << ",\"tested\":" << test.tested
            << ",\"ten_sets\":" << test.total_tens
            << ",\"eleven_sets\":" << test.total_elevens
            << ",\"completable\":0}" << std::endl;
}
int main(int argc, char **argv) {
  try {
    if (argc == 2 && std::string(argv[1]) == "controls")
      controls();
    else if (argc == 4 && std::string(argv[1]) == "generate")
      generate(argv[2], argv[3]);
    else if (argc == 5 && std::string(argv[1]) == "residual")
      replay(argv[2], std::stoi(argv[3]), std::stoi(argv[4]));
    else
      throw std::runtime_error("usage: verify controls | generate WEIGHTS WORK "
                               "| residual WORK PART PARTS");
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
