// Exact fixed-multiplier lift at length 64. See README.md for coverage.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using Word = std::uint64_t;
using Row = std::array<int, 32>;
using Quad = std::array<Row, 4>;
int multiplier = 31;
struct Candidate {
  Word word;
  std::array<int, 15> real;
  std::array<Word, 8> odd;
};
struct Key {
  std::array<std::int8_t, 15> v{};
  bool operator==(const Key &) const = default;
};
struct Hash {
  std::size_t operator()(const Key &k) const {
    std::uint64_t h = 1469598103934665603ULL;
    for (auto v : k.v) {
      h ^= static_cast<std::uint8_t>(v);
      h *= 1099511628211ULL;
    }
    return static_cast<std::size_t>(h);
  }
};
struct Pair {
  Word x, y;
  int sign;
};
struct SignedKey {
  Key key;
  int sign;
};
int corr(Word x, Word y, int shift) {
  return 64 - 2 * std::popcount(x ^ std::rotr(y, shift));
}
std::vector<Candidate> lift(const Row &z) {
  Word base = 0;
  std::vector<std::array<Word, 2>> choices;
  for (int j = 0; j < 32; ++j)
    if (z[j] == -1)
      base |= (Word{1} << j) | (Word{1} << (j + 32));
  if (z[0] == 0)
    choices.push_back({Word{1}, Word{1} << 32});
  for (int j = 1; j < 16; ++j)
    if (z[j] == 0) {
      int t = 32 - j;
      if (multiplier == 31 && j % 2)
        choices.push_back({(Word{1} << j) | (Word{1} << t),
                           (Word{1} << (j + 32)) | (Word{1} << (t + 32))});
      else
        choices.push_back({(Word{1} << j) | (Word{1} << (t + 32)),
                           (Word{1} << (j + 32)) | (Word{1} << t)});
    }
  std::vector<Word> words{base};
  for (auto c : choices) {
    std::vector<Word> next;
    next.reserve(2 * words.size());
    for (Word w : words) {
      next.push_back(w | c[0]);
      next.push_back(w | c[1]);
    }
    words = std::move(next);
  }
  std::vector<Candidate> result;
  result.reserve(words.size());
  for (Word w : words) {
    Candidate c{};
    c.word = w;
    for (int j = 0; j < 15; ++j)
      c.real[j] = corr(w, w, j + 1);
    for (int j = 0; j < 8; ++j)
      c.odd[j] = std::rotr(w, 2 * j + 1);
    result.push_back(c);
  }
  return result;
}
SignedKey pair_key(const Candidate &x, const Candidate &y) {
  SignedKey out{};
  out.sign = 1;
  if (multiplier == 63) {
    for (int j = 0; j < 15; ++j)
      out.key.v[j] = static_cast<std::int8_t>((x.real[j] + y.real[j]) / 4);
    return out;
  }
  for (int j = 0; j < 7; ++j)
    out.key.v[j] =
        static_cast<std::int8_t>((x.real[2 * j + 1] + y.real[2 * j + 1]) / 4);
  bool first = true;
  for (int j = 0; j < 8; ++j) {
    int skew =
        (std::popcount(y.word ^ x.odd[j]) - std::popcount(x.word ^ y.odd[j])) /
        2;
    if (first && skew) {
      out.sign = skew > 0 ? 1 : -1;
      first = false;
    }
    out.key.v[7 + j] = static_cast<std::int8_t>(skew);
  }
  for (int j = 7; j < 15; ++j)
    out.key.v[j] = static_cast<std::int8_t>(out.sign * out.key.v[j]);
  return out;
}
bool verify(Word x, Word y, Word z, Word w) {
  if (std::popcount(x) != 32 || std::popcount(y) != 32 ||
      std::popcount(z) != 32 || std::popcount(w) != 31)
    return false;
  for (int k = 1; k < 64; ++k) {
    if (corr(x, x, k) + corr(y, y, k) + corr(z, z, k) + corr(w, w, k) != -4)
      return false;
    if (corr(x, y, k) - corr(y, x, k) + corr(w, z, k) - corr(z, w, k) != 0)
      return false;
  }
  for (auto a : {x, y, z, w})
    for (int j = 0; j < 64; ++j)
      if (((a >> j) & 1U) != ((a >> ((multiplier * j) % 64)) & 1U))
        return false;
  return true;
}
void validate(const Quad &q) {
  for (int i = 0; i < 4; ++i) {
    int total = 0;
    for (int j = 0; j < 32; ++j) {
      if (q[i][j] < -1 || q[i][j] > 1 || q[i][j] != q[i][(32 - j) % 32])
        throw std::runtime_error("invalid symmetric compressed row");
      total += q[i][j];
    }
    if (total != (i == 3 ? 1 : 0) || q[i][16] == 0 ||
        (q[i][0] == 0) != (i == 3))
      throw std::runtime_error("invalid sum or endpoint parity");
  }
  for (int k = 0; k <= 16; ++k) {
    int total = 0;
    for (const auto &r : q)
      for (int j = 0; j < 32; ++j)
        total += r[j] * r[(j + k) % 32];
    if (total != (k == 0 ? 63 : -2))
      throw std::runtime_error("invalid compressed correlation");
  }
}

void audit(const std::vector<Quad> &quads) {
  std::set<Row> seen;
  for (std::size_t qi = 0; qi < quads.size(); ++qi) {
    std::array<std::vector<Candidate>, 4> rows;
    for (int i = 0; i < 4; ++i) {
      rows[i] = lift(quads[qi][i]);
      if (seen.insert(quads[qi][i]).second) {
        std::cout << "R";
        for (int v : quads[qi][i])
          std::cout << " " << v;
        std::cout << " " << rows[i].size();
        for (const auto &c : rows[i])
          std::cout << " " << c.word;
        std::cout << "\n";
      }
    }
    if (qi % 37 == 0)
      for (int i = 0; i < 4; ++i)
        for (int j = i + 1; j < 4; ++j)
          for (int position = 0; position < 3; ++position) {
            const auto &x = rows[i][position * (rows[i].size() - 1) / 2];
            const auto &y = rows[j][position * (rows[j].size() - 1) / 2];
            auto k = pair_key(x, y);
            std::cout << "K " << x.word << " " << y.word << " " << k.sign;
            for (auto v : k.key.v)
              std::cout << " " << static_cast<int>(v);
            std::cout << "\n";
          }
  }
}

int main(int argc, char **argv) {
  if (argc < 3) {
    std::cerr << "usage: lift64 INPUT MULTIPLIER [LIMIT|--audit]\n";
    return 2;
  }
  std::ifstream in(argv[1]);
  if (!in)
    throw std::runtime_error("cannot open input");
  std::size_t n = 0;
  if (!(in >> n) || n == 0)
    throw std::runtime_error("invalid count");
  std::vector<Quad> quads(n);
  for (auto &q : quads)
    for (auto &r : q)
      for (int &v : r)
        if (!(in >> v))
          throw std::runtime_error("truncated input");
  std::string extra;
  if (in >> extra)
    throw std::runtime_error("trailing input");
  for (const auto &q : quads)
    validate(q);
  multiplier = std::stoi(argv[2]);
  if (multiplier != 31 && multiplier != 63)
    throw std::runtime_error("multiplier must be 31 or 63");
  if (argc > 3 && std::string(argv[3]) == "--audit") {
    audit(quads);
    return 0;
  }
  std::size_t limit = argc > 3 ? std::stoull(argv[3]) : n;
  limit = std::min(limit, n);
  std::unordered_map<std::string, std::vector<Candidate>> cache;
  auto candidates = [&](const Row &r) -> const std::vector<Candidate> & {
    std::string k;
    for (int v : r)
      k.push_back(static_cast<char>(v + 1));
    auto it = cache.find(k);
    if (it == cache.end())
      it = cache.emplace(k, lift(r)).first;
    return it->second;
  };
  std::uint64_t pairs = 0, unique = 0;
  for (std::size_t qi = 0; qi < limit; ++qi) {
    const Quad &q = quads[qi];
    std::array<const std::vector<Candidate> *, 4> rows{};
    for (int i = 0; i < 4; ++i)
      rows[i] = &candidates(q[i]);
    for (int third = 0; third < (multiplier == 31 ? 3 : 1); ++third) {
      int a = (third + 1) % 3, b = (third + 2) % 3;
      bool table_left = rows[a]->size() * rows[b]->size() <=
                        rows[third]->size() * rows[3]->size();
      int ti = table_left ? a : third, tj = table_left ? b : 3,
          pi = table_left ? third : a, pj = table_left ? 3 : b;
      std::unordered_map<Key, Pair, Hash> table;
      table.reserve(rows[ti]->size() * rows[tj]->size());
      for (const auto &x : *rows[ti])
        for (const auto &y : *rows[tj]) {
          auto k = pair_key(x, y);
          table.try_emplace(k.key, Pair{x.word, y.word, k.sign});
          ++pairs;
        }
      unique += table.size();
      for (const auto &x : *rows[pi])
        for (const auto &y : *rows[pj]) {
          auto k = pair_key(x, y);
          ++pairs;
          for (int j = 0; j < (multiplier == 31 ? 7 : 15); ++j)
            k.key.v[j] = static_cast<std::int8_t>(-1 - k.key.v[j]);
          auto found = table.find(k.key);
          if (found == table.end())
            continue;
          Pair probe{x.word, y.word, k.sign};
          Pair left = table_left ? found->second : probe,
               right = table_left ? probe : found->second;
          if (left.sign != right.sign)
            left.x = ~left.x;
          if (!verify(left.x, left.y, right.x, right.y))
            throw std::runtime_error("independent full check failed");
          std::cout << "WITNESS " << qi << " " << left.x << " " << left.y << " "
                    << right.x << " " << right.y << "\n";
          return 0;
        }
    }
    if ((qi + 1) % 32 == 0)
      std::cout << "progress " << qi + 1 << " pairs " << pairs
                << " unique_table_keys " << unique << std::endl;
  }
  std::cout << "COMPLETE multiplier " << multiplier << " parents " << limit
            << " total_input " << n << " pairs " << pairs
            << " unique_table_keys " << unique << " witnesses 0\n";
}
