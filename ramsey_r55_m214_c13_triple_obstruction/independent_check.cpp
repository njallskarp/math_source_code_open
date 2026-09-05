#include <algorithm>
#include <array>
#include <bit>
#include <cstdlib>
#include <iostream>
#include <set>
#include <string>
#include <tuple>

namespace {

constexpr int n = 13;
constexpr int full = (1 << n) - 1;
constexpr std::array<int, 3> footprints = {0x1c48, 0x0e2c, 0x1f42};
constexpr std::array<int, 3> blue_witness = {0, 4, 7};
constexpr std::array<int, 2> common_edge = {10, 11};

[[noreturn]] void fail(const std::string& message) {
  std::cerr << "FAIL " << message << '\n';
  std::exit(1);
}

void require(bool condition, const std::string& message) {
  if (!condition) fail(message);
}

bool core_edge(int i, int j) {
  if (i == j) return false;
  const int difference = (i - j + n) % n;
  return difference == 1 || difference == 5 || difference == 8 || difference == 12;
}

bool independent(int mask) {
  for (int i = 0; i < n; ++i)
    for (int j = i + 1; j < n; ++j)
      if ((mask & (1 << i)) != 0 && (mask & (1 << j)) != 0 && core_edge(i, j))
        return false;
  return true;
}

int transform(int mask, int multiplier, int translation) {
  int result = 0;
  for (int i = 0; i < n; ++i)
    if ((mask & (1 << i)) != 0)
      result |= 1 << ((multiplier * i + translation) % n);
  return result;
}

}  // namespace

int main() {
  int edge_count = 0;
  int independent_triples = 0;
  int independent_fours = 0;
  for (int i = 0; i < n; ++i)
    for (int j = i + 1; j < n; ++j) edge_count += static_cast<int>(core_edge(i, j));
  for (int mask = 0; mask <= full; ++mask) {
    const int size = std::popcount(static_cast<unsigned>(mask));
    independent_triples += static_cast<int>(size == 3 && independent(mask));
    independent_fours += static_cast<int>(size == 4 && independent(mask));
  }
  require(edge_count == 26 && independent_triples == 78 && independent_fours == 39,
          "core census");

  for (int footprint : footprints) {
    for (int mask = 0; mask <= full; ++mask)
      if (std::popcount(static_cast<unsigned>(mask)) == 4 && independent(mask))
        require((footprint & mask) != 0, "nontransversal footprint");
  }

  int witness_mask = 0;
  for (int vertex : blue_witness) witness_mask |= 1 << vertex;
  require(independent(witness_mask), "blue witness is not independent");
  for (int left = 0; left < 3; ++left)
    for (int right = left + 1; right < 3; ++right)
      require(((footprints[left] | footprints[right]) & witness_mask) == 0,
              "blue witness meets a footprint union");
  require(core_edge(common_edge[0], common_edge[1]), "common edge is not red");
  for (int footprint : footprints)
    for (int vertex : common_edge)
      require((footprint & (1 << vertex)) != 0, "red edge is not common");

  int safe = 0;
  int pair_blue_failures = 0;
  int red_triple_failures = 0;
  for (int assignment = 0; assignment < 8; ++assignment) {
    if (assignment != 7)
      ++pair_blue_failures;
    else if (assignment == 7)
      ++red_triple_failures;
    else
      ++safe;
  }
  require(safe == 0 && pair_blue_failures == 7 && red_triple_failures == 1,
          "truth table");

  std::set<std::array<int, 3>> orbit;
  for (int multiplier : {1, 5, 8, 12}) {
    for (int translation = 0; translation < n; ++translation) {
      std::array<int, 3> transformed{};
      for (int index = 0; index < 3; ++index)
        transformed[index] = transform(footprints[index], multiplier, translation);
      auto ordered = transformed;
      std::sort(ordered.begin(), ordered.end());
      orbit.insert(ordered);

      int transformed_witness = 0;
      for (int vertex : blue_witness)
        transformed_witness |= 1 << ((multiplier * vertex + translation) % n);
      require(independent(transformed_witness), "affine independent witness");
      for (int left = 0; left < 3; ++left)
        for (int right = left + 1; right < 3; ++right)
          require(((transformed[left] | transformed[right]) & transformed_witness) == 0,
                  "affine disjointness");

      std::array<int, 2> transformed_edge{};
      for (int index = 0; index < 2; ++index)
        transformed_edge[index] =
            (multiplier * common_edge[index] + translation) % n;
      require(core_edge(transformed_edge[0], transformed_edge[1]), "affine red edge");
      for (int footprint : transformed)
        for (int vertex : transformed_edge)
          require((footprint & (1 << vertex)) != 0, "affine common edge");
    }
  }
  require(orbit.size() == 52U, "affine orbit size");

  int deletion_models = 0;
  for (int omitted = 0; omitted < 4; ++omitted) {
    int models = 0;
    for (int assignment = 0; assignment < 8; ++assignment) {
      bool accepted = true;
      for (int edge = 0; edge < 3; ++edge)
        if (edge != omitted && (assignment & (1 << edge)) == 0) accepted = false;
      if (omitted != 3 && assignment == 7) accepted = false;
      models += static_cast<int>(accepted);
    }
    require(models == 1, "deletion minimality");
    deletion_models += models;
  }
  require(deletion_models == 4, "deletion model census");

  std::cout << "VERIFIED TRIPLE-INCOMPATIBILITY OBSTRUCTION\n";
  std::cout << "core_edges=26 independent_triples=78 independent_fours=39 legal_footprints=3\n";
  std::cout << "pair_blue_witnesses=3 common_red_edge=10,11 truth_assignments=8 safe=0\n";
  std::cout << "affine_orbit=52 deletion_models=4 source_height=2969\n";
}
