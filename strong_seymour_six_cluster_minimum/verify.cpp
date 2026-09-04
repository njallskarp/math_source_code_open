#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string_view>
#include <vector>

using Rows = std::vector<std::uint64_t>;

Rows blowup(const std::array<int, 6>& sizes, std::uint16_t quotient) {
    std::array<int, 6> starts{};
    int n = 0;
    for (int i = 0; i < 6; ++i) {
        starts[i] = n;
        n += sizes[i];
    }
    if (n > 63) {
        std::abort();
    }
    Rows rows(static_cast<std::size_t>(n), 0);
    for (int i = 0; i < 6; ++i) {
        for (int a = starts[i]; a < starts[i] + sizes[i]; ++a) {
            for (int b = a + 1; b < starts[i] + sizes[i]; ++b) {
                rows[static_cast<std::size_t>(a)] |= std::uint64_t{1} << b;
            }
        }
    }
    int bit = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j = i + 1; j < 6; ++j, ++bit) {
            const bool i_beats_j = ((quotient >> bit) & 1U) != 0;
            const int source = i_beats_j ? i : j;
            const int target = i_beats_j ? j : i;
            const std::uint64_t target_mask =
                ((std::uint64_t{1} << sizes[target]) - 1) << starts[target];
            for (int a = starts[source]; a < starts[source] + sizes[source]; ++a) {
                rows[static_cast<std::size_t>(a)] |= target_mask;
            }
        }
    }
    return rows;
}

bool augment(int left, std::uint64_t right, const Rows& rows,
             std::array<int, 64>& matched_to, std::uint64_t& seen) {
    std::uint64_t candidates = rows[static_cast<std::size_t>(left)] & right & ~seen;
    while (candidates != 0) {
        const int head = std::countr_zero(candidates);
        const std::uint64_t head_bit = std::uint64_t{1} << head;
        candidates ^= head_bit;
        seen |= head_bit;
        if (matched_to[static_cast<std::size_t>(head)] == -1 ||
            augment(matched_to[static_cast<std::size_t>(head)], right, rows, matched_to, seen)) {
            matched_to[static_cast<std::size_t>(head)] = left;
            return true;
        }
    }
    return false;
}

bool is_strong_vertex(int x, const Rows& rows) {
    const int n = static_cast<int>(rows.size());
    const std::uint64_t universe = (std::uint64_t{1} << n) - 1;
    const std::uint64_t first = rows[static_cast<std::size_t>(x)];
    std::uint64_t reachable = 0;
    std::uint64_t work = first;
    while (work != 0) {
        const int y = std::countr_zero(work);
        work ^= std::uint64_t{1} << y;
        reachable |= rows[static_cast<std::size_t>(y)];
    }
    const std::uint64_t second = reachable & ~(first | (std::uint64_t{1} << x)) & universe;
    if (std::popcount(first) > std::popcount(second)) {
        return false;
    }
    std::array<int, 64> matched_to{};
    matched_to.fill(-1);
    int matching = 0;
    work = first;
    while (work != 0) {
        const int y = std::countr_zero(work);
        work ^= std::uint64_t{1} << y;
        std::uint64_t seen = 0;
        matching += augment(y, second, rows, matched_to, seen) ? 1 : 0;
    }
    return matching == std::popcount(first);
}

bool has_no_strong_vertex(const Rows& rows) {
    for (int x = 0; x < static_cast<int>(rows.size()); ++x) {
        if (is_strong_vertex(x, rows)) {
            return false;
        }
    }
    return true;
}

int pair_index(int a, int b) {
    if (a == b) {
        std::abort();
    }
    if (a > b) {
        std::swap(a, b);
    }
    int answer = 0;
    for (int i = 0; i < a; ++i) {
        answer += 5 - i;
    }
    return answer + (b - a - 1);
}

std::uint16_t relabel(std::uint16_t quotient, const std::array<int, 6>& permutation) {
    std::uint16_t answer = 0;
    int bit = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j = i + 1; j < 6; ++j, ++bit) {
            int source = ((quotient >> bit) & 1U) != 0 ? i : j;
            int target = source == i ? j : i;
            source = permutation[static_cast<std::size_t>(source)];
            target = permutation[static_cast<std::size_t>(target)];
            const int new_bit = pair_index(source, target);
            if (source < target) {
                answer |= static_cast<std::uint16_t>(std::uint32_t{1} << new_bit);
            }
        }
    }
    return answer;
}

std::vector<std::uint16_t> quotient_representatives() {
    std::vector<std::uint16_t> representatives;
    for (std::uint32_t quotient = 0; quotient < (1U << 15); ++quotient) {
        std::array<int, 6> permutation = {0, 1, 2, 3, 4, 5};
        std::uint16_t minimum = static_cast<std::uint16_t>(quotient);
        do {
            minimum = std::min(minimum, relabel(static_cast<std::uint16_t>(quotient), permutation));
        } while (std::next_permutation(permutation.begin(), permutation.end()));
        if (minimum == quotient) {
            representatives.push_back(minimum);
        }
    }
    return representatives;
}

std::uint16_t published_quotient() {
    constexpr std::array<std::uint8_t, 6> out = {
        0b110010,  // 0 -> 1,4,5
        0b111000,  // 1 -> 3,4,5
        0b001011,  // 2 -> 0,1,3
        0b010001,  // 3 -> 0,4
        0b100100,  // 4 -> 2,5
        0b001100,  // 5 -> 2,3
    };
    std::uint16_t answer = 0;
    int bit = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j = i + 1; j < 6; ++j, ++bit) {
            if (((out[static_cast<std::size_t>(i)] >> j) & 1U) != 0) {
                answer |= static_cast<std::uint16_t>(std::uint32_t{1} << bit);
            }
        }
    }
    return answer;
}

void print_sizes(const std::array<int, 6>& sizes) {
    std::cout << '[';
    for (int i = 0; i < 6; ++i) {
        if (i != 0) {
            std::cout << ',';
        }
        std::cout << sizes[static_cast<std::size_t>(i)];
    }
    std::cout << ']';
}

int shell_search() {
    constexpr std::array<int, 6> base = {7, 3, 11, 3, 9, 3};
    const std::uint16_t known = published_quotient();
    if (!has_no_strong_vertex(blowup(base, known))) {
        std::cerr << "published construction sanity check failed\n";
        return 2;
    }

    std::uint64_t checked = 0;
    std::uint64_t solutions = 0;
    for (int removed_cluster = -1; removed_cluster < 6; ++removed_cluster) {
        auto sizes = base;
        if (removed_cluster >= 0) {
            --sizes[static_cast<std::size_t>(removed_cluster)];
        }
        std::uint64_t shell_solutions = 0;
        std::uint16_t first = 0;
        for (std::uint32_t quotient = 0; quotient < (1U << 15); ++quotient) {
            ++checked;
            if (has_no_strong_vertex(blowup(sizes, static_cast<std::uint16_t>(quotient)))) {
                if (shell_solutions == 0) {
                    first = static_cast<std::uint16_t>(quotient);
                }
                ++shell_solutions;
            }
        }
        solutions += shell_solutions;
        std::cout << "shell=" << removed_cluster << " sizes=";
        print_sizes(sizes);
        std::cout << " quotients=32768 no_strong=" << shell_solutions;
        if (shell_solutions != 0) {
            std::cout << " first_mask=" << first;
        }
        std::cout << '\n';
    }
    std::cout << "checked=" << checked << " total_no_strong=" << solutions << '\n';
    return 0;
}

int all_six_cluster_search(bool use_degree_filter) {
    const auto representatives = quotient_representatives();
    if (representatives.size() != 56) {
        std::cerr << "expected 56 unlabeled six-vertex tournaments, found "
                  << representatives.size() << '\n';
        return 2;
    }
    constexpr std::array<int, 6> published_sizes = {7, 3, 11, 3, 9, 3};
    if (!has_no_strong_vertex(blowup(published_sizes, published_quotient()))) {
        std::cerr << "published construction sanity check failed\n";
        return 2;
    }

    std::uint64_t total_configurations = 0;
    std::uint64_t degree_eligible = 0;
    std::uint64_t checksum = 1469598103934665603ULL;
    std::uint64_t representative_checksum = 1469598103934665603ULL;
    for (const std::uint16_t quotient : representatives) {
        representative_checksum ^= static_cast<std::uint64_t>(quotient);
        representative_checksum *= 1099511628211ULL;
    }
    for (int total = 6; total <= 35; ++total) {
        std::uint64_t configurations = 0;
        std::uint64_t eligible = 0;
        for (int a = 1; a <= total - 5; ++a) {
            for (int b = 1; b <= total - a - 4; ++b) {
                for (int c = 1; c <= total - a - b - 3; ++c) {
                    for (int d = 1; d <= total - a - b - c - 2; ++d) {
                        for (int e = 1; e <= total - a - b - c - d - 1; ++e) {
                            const int f = total - a - b - c - d - e;
                            const std::array<int, 6> sizes = {a, b, c, d, e, f};
                            for (const std::uint16_t quotient : representatives) {
                                ++configurations;
                                const Rows rows = blowup(sizes, quotient);
                                bool minimum_degree_six = true;
                                for (const std::uint64_t row : rows) {
                                    minimum_degree_six &= std::popcount(row) >= 6;
                                }
                                if (use_degree_filter && !minimum_degree_six) {
                                    continue;
                                }
                                ++eligible;
                                checksum ^= static_cast<std::uint64_t>(quotient);
                                checksum *= 1099511628211ULL;
                                for (const int size : sizes) {
                                    checksum ^= static_cast<std::uint64_t>(size);
                                    checksum *= 1099511628211ULL;
                                }
                                if (has_no_strong_vertex(rows)) {
                                    std::cout << "FOUND total=" << total << " sizes=";
                                    print_sizes(sizes);
                                    std::cout << " quotient_mask=" << quotient << '\n';
                                    return 1;
                                }
                            }
                        }
                    }
                }
            }
        }
        total_configurations += configurations;
        degree_eligible += eligible;
        std::cout << "total=" << total << " configurations=" << configurations
                  << " matching_tested=" << eligible << '\n';
    }
    std::cout << "VERIFIED SIX-CLUSTER OBSTRUCTION; quotient_classes="
              << representatives.size() << " total_configurations=" << total_configurations
              << " matching_tested=" << degree_eligible
              << " degree_filter=" << (use_degree_filter ? "on" : "off")
              << " quotient_fnv64=" << representative_checksum
              << " checksum_fnv64=" << checksum << '\n';
    return 0;
}

int main(int argc, char** argv) {
    if (argc == 1 || (argc == 2 && std::string_view(argv[1]) == "--shell")) {
        return shell_search();
    }
    if (argc == 2 && std::string_view(argv[1]) == "--all") {
        return all_six_cluster_search(true);
    }
    if (argc == 2 && std::string_view(argv[1]) == "--all-direct") {
        return all_six_cluster_search(false);
    }
    std::cerr << "usage: verify [--shell|--all|--all-direct]\n";
    return 2;
}
