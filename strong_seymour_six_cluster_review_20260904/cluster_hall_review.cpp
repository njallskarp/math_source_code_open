#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <tuple>
#include <vector>

using Sizes = std::array<int, 6>;

int pair_index(int n, int a, int b) {
    if (a == b) {
        std::abort();
    }
    if (a > b) {
        std::swap(a, b);
    }
    int answer = 0;
    for (int i = 0; i < a; ++i) {
        answer += n - 1 - i;
    }
    return answer + b - a - 1;
}

bool arc(std::uint16_t tournament, int n, int source, int target) {
    if (source == target) {
        return false;
    }
    const int low = std::min(source, target);
    const int high = std::max(source, target);
    const bool low_beats_high =
        ((tournament >> pair_index(n, low, high)) & 1U) != 0;
    return source == low ? low_beats_high : !low_beats_high;
}

std::uint16_t relabel(std::uint16_t tournament, int n,
                      const std::array<int, 6>& old_to_new) {
    std::uint16_t answer = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            const int source = arc(tournament, n, i, j) ? i : j;
            const int target = source == i ? j : i;
            const int new_source = old_to_new[static_cast<std::size_t>(source)];
            const int new_target = old_to_new[static_cast<std::size_t>(target)];
            if (new_source < new_target) {
                answer |= static_cast<std::uint16_t>(
                    std::uint32_t{1} << pair_index(n, new_source, new_target));
            }
        }
    }
    return answer;
}

std::uint16_t canonical(std::uint16_t tournament, int n) {
    std::array<int, 6> permutation = {0, 1, 2, 3, 4, 5};
    std::uint16_t answer = tournament;
    do {
        answer = std::min(answer, relabel(tournament, n, permutation));
    } while (std::next_permutation(permutation.begin(),
                                  permutation.begin() + n));
    return answer;
}

std::vector<std::uint16_t> incremental_representatives() {
    std::vector<std::uint16_t> representatives = {0};
    constexpr std::array<std::size_t, 6> expected = {1, 1, 2, 4, 12, 56};
    for (int n = 1; n < 6; ++n) {
        std::set<std::uint16_t> next;
        for (const std::uint16_t smaller : representatives) {
            for (std::uint32_t attachment = 0; attachment < (1U << n);
                 ++attachment) {
                std::uint16_t candidate = 0;
                for (int i = 0; i < n; ++i) {
                    for (int j = i + 1; j < n; ++j) {
                        if (arc(smaller, n, i, j)) {
                            candidate |= static_cast<std::uint16_t>(
                                std::uint32_t{1} << pair_index(n + 1, i, j));
                        }
                    }
                    if (((attachment >> i) & 1U) != 0) {
                        candidate |= static_cast<std::uint16_t>(
                            std::uint32_t{1} << pair_index(n + 1, i, n));
                    }
                }
                next.insert(canonical(candidate, n + 1));
            }
        }
        representatives.assign(next.begin(), next.end());
        if (representatives.size() != expected[static_cast<std::size_t>(n)]) {
            std::cerr << "unexpected tournament count at order " << n + 1
                      << '\n';
            std::exit(2);
        }
    }
    return representatives;
}

bool terminal_is_strong(std::uint16_t quotient, const Sizes& sizes, int root) {
    unsigned out_clusters = 0;
    for (int j = 0; j < 6; ++j) {
        if (arc(quotient, 6, root, j)) {
            out_clusters |= 1U << j;
        }
    }

    // Vertices inside one source cluster have the same allowed sink clusters.
    // It therefore suffices in Hall's condition to take whole source clusters.
    for (unsigned chosen = out_clusters; chosen != 0;
         chosen = (chosen - 1) & out_clusters) {
        int source_capacity = 0;
        unsigned reachable_sink_clusters = 0;
        for (int j = 0; j < 6; ++j) {
            if (((chosen >> j) & 1U) == 0) {
                continue;
            }
            source_capacity += sizes[static_cast<std::size_t>(j)];
            for (int k = 0; k < 6; ++k) {
                if (arc(quotient, 6, k, root) && arc(quotient, 6, j, k)) {
                    reachable_sink_clusters |= 1U << k;
                }
            }
        }
        int sink_capacity = 0;
        for (int k = 0; k < 6; ++k) {
            if (((reachable_sink_clusters >> k) & 1U) != 0) {
                sink_capacity += sizes[static_cast<std::size_t>(k)];
            }
        }
        if (source_capacity > sink_capacity) {
            return false;
        }
    }
    return true;
}

bool has_strong_vertex(std::uint16_t quotient, const Sizes& sizes) {
    // In a transitive fiber, every nonsink vertex has a later out-neighbor.
    // That later vertex cannot reach any in-neighbor fiber of the root in one
    // more step, so it has no allowed head in the exact second neighborhood.
    // Hence only the six fiber sinks need the capacitated Hall test above.
    for (int root = 0; root < 6; ++root) {
        if (terminal_is_strong(quotient, sizes, root)) {
            return true;
        }
    }
    return false;
}

std::uint16_t published_quotient() {
    constexpr std::array<unsigned, 6> out = {
        (1U << 1) | (1U << 4) | (1U << 5),
        (1U << 3) | (1U << 4) | (1U << 5),
        (1U << 0) | (1U << 1) | (1U << 3),
        (1U << 0) | (1U << 4),
        (1U << 2) | (1U << 5),
        (1U << 2) | (1U << 3),
    };
    std::uint16_t answer = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j = i + 1; j < 6; ++j) {
            if (((out[static_cast<std::size_t>(i)] >> j) & 1U) != 0) {
                answer |= static_cast<std::uint16_t>(
                    std::uint32_t{1} << pair_index(6, i, j));
            } else if (((out[static_cast<std::size_t>(j)] >> i) & 1U) == 0) {
                std::cerr << "published quotient transcription is incomplete\n";
                std::exit(2);
            }
        }
    }
    return answer;
}

struct WeightedPresentation {
    std::uint16_t quotient{};
    Sizes sizes{};

    auto operator<=>(const WeightedPresentation&) const = default;
};

WeightedPresentation canonical_weighted(std::uint16_t quotient,
                                         const Sizes& sizes) {
    std::array<int, 6> permutation = {0, 1, 2, 3, 4, 5};
    WeightedPresentation answer{quotient, sizes};
    do {
        Sizes moved{};
        for (int old = 0; old < 6; ++old) {
            moved[static_cast<std::size_t>(permutation[static_cast<std::size_t>(old)])] =
                sizes[static_cast<std::size_t>(old)];
        }
        answer = std::min(answer,
                          WeightedPresentation{relabel(quotient, 6, permutation), moved});
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    return answer;
}

void mix(std::uint64_t& hash, std::uint64_t value) {
    hash ^= value;
    hash *= 1099511628211ULL;
}

int main() {
    const auto representatives = incremental_representatives();
    constexpr Sizes published_sizes = {7, 3, 11, 3, 9, 3};
    const std::uint16_t published = published_quotient();
    if (has_strong_vertex(published, published_sizes)) {
        std::cerr << "published order-36 witness unexpectedly has a strong vertex\n";
        return 1;
    }

    std::uint64_t below_36 = 0;
    std::uint64_t order_36 = 0;
    std::uint64_t raw_order_36_obstructions = 0;
    std::uint64_t coverage_hash = 1469598103934665603ULL;
    std::set<WeightedPresentation> obstruction_orbits;

    for (int total = 6; total <= 36; ++total) {
        for (int a = 1; a <= total - 5; ++a) {
            for (int b = 1; b <= total - a - 4; ++b) {
                for (int c = 1; c <= total - a - b - 3; ++c) {
                    for (int d = 1; d <= total - a - b - c - 2; ++d) {
                        for (int e = 1; e <= total - a - b - c - d - 1; ++e) {
                            const Sizes sizes = {
                                a, b, c, d, e, total - a - b - c - d - e};
                            for (const std::uint16_t quotient : representatives) {
                                const bool strong = has_strong_vertex(quotient, sizes);
                                mix(coverage_hash, quotient);
                                for (const int size : sizes) {
                                    mix(coverage_hash,
                                        static_cast<std::uint64_t>(size));
                                }
                                mix(coverage_hash, strong ? 1U : 0U);
                                if (total < 36) {
                                    ++below_36;
                                    if (!strong) {
                                        std::cerr << "counterexample below 36: quotient="
                                                  << quotient << " sizes=";
                                        for (const int size : sizes) {
                                            std::cerr << size << ',';
                                        }
                                        std::cerr << '\n';
                                        return 1;
                                    }
                                } else {
                                    ++order_36;
                                    if (!strong) {
                                        ++raw_order_36_obstructions;
                                        obstruction_orbits.insert(
                                            canonical_weighted(quotient, sizes));
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    if (below_36 != 90'896'960ULL || order_36 != 18'179'392ULL ||
        obstruction_orbits.empty()) {
        std::cerr << "coverage invariant failed\n";
        return 2;
    }

    std::uint64_t obstruction_hash = 1469598103934665603ULL;
    for (const auto& obstruction : obstruction_orbits) {
        mix(obstruction_hash, obstruction.quotient);
        for (const int size : obstruction.sizes) {
            mix(obstruction_hash, static_cast<std::uint64_t>(size));
        }
    }
    const auto& first = *obstruction_orbits.begin();
    std::cout << "VERIFIED cluster-Hall reduction; quotient_classes="
              << representatives.size() << " below36=" << below_36
              << " order36=" << order_36
              << " order36_raw_obstructions=" << raw_order_36_obstructions
              << " order36_weighted_orbits=" << obstruction_orbits.size()
              << " coverage_fnv64=" << coverage_hash
              << " obstruction_fnv64=" << obstruction_hash << '\n';
    std::cout << "first_order36_weighted_orbit quotient=" << first.quotient
              << " sizes=";
    for (std::size_t i = 0; i < first.sizes.size(); ++i) {
        if (i != 0) {
            std::cout << ',';
        }
        std::cout << first.sizes[i];
    }
    std::cout << " published_mask=" << published << '\n';
}
