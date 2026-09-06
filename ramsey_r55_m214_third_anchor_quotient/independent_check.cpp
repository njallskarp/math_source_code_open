#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int N = 43;
constexpr int SELECTOR_FIRST = 13245;
constexpr long long BASE_CONSTRAINTS = 2044421;
constexpr long long EXPECTED_SUFFIX_ROWS = 13577;
constexpr unsigned long long EXPECTED_ORBITS = 2206343ULL;
constexpr unsigned long long EXPECTED_LABELINGS = 5176895776352ULL;
constexpr char CELLS[] = "HABO";

struct Key {
    std::string family;
    int common;
    int exceptional_common;
    std::string pattern;
};

struct Bucket {
    std::string name;
    char color;
    char cell;
    bool anomalous;
    std::vector<int> vertices;
};

struct Layout {
    Key key;
    int third_anchor;
    int pool_size;
    std::vector<Bucket> buckets;
    std::set<int> partition_pair;
};

struct Counts {
    unsigned long long orbits = 0;
    unsigned long long labelings = 0;
};

void require(bool condition, const std::string& message) {
    if (!condition) throw std::runtime_error(message);
}

int occurrences(const std::string& word, char value) {
    return static_cast<int>(std::count(word.begin(), word.end(), value));
}

std::vector<std::string> patterns(const std::string& family) {
    if (family == "E8") return {"H", "A"};
    if (family == "E77" || family == "C77") return {"BB", "BO", "OO"};
    if (family == "C8") return {"B", "O"};
    if (family == "C77partition") return {"HO", "AB"};
    throw std::runtime_error("unknown family");
}

std::vector<Key> root_keys() {
    const std::array<std::string, 5> families = {
        "E8", "E77", "C8", "C77", "C77partition"
    };
    std::vector<Key> result;
    for (const auto& family : families) {
        for (int common = 9; common <= 13; ++common) {
            for (int k = 0; k <= 6; ++k) {
                const std::array<int, 4> e = {k, 6 - k, 6 - k, 1 + k};
                const std::array<int, 4> c = {
                    common - k, 14 - common + k,
                    14 - common + k, common - k
                };
                const auto& sizes = family.front() == 'E' ? e : c;
                for (const auto& pattern : patterns(family)) {
                    bool fits = true;
                    for (int i = 0; i < 4; ++i) {
                        if (occurrences(pattern, CELLS[i]) > sizes.at(i)) fits = false;
                    }
                    if (fits) result.push_back({family, common, k, pattern});
                }
            }
        }
    }
    require(result.size() == 389, "root count");
    return result;
}

Layout layout(const Key& key) {
    const std::array<int, 8> sizes = {
        key.exceptional_common,
        6 - key.exceptional_common,
        6 - key.exceptional_common,
        1 + key.exceptional_common,
        key.common - key.exceptional_common,
        14 - key.common + key.exceptional_common,
        14 - key.common + key.exceptional_common,
        key.common - key.exceptional_common,
    };
    std::array<std::vector<int>, 8> cells;
    int cursor = 2;
    for (int i = 0; i < 8; ++i) {
        for (int j = 0; j < sizes.at(i); ++j) cells.at(i).push_back(cursor++);
    }
    require(cursor == N, "cell partition");

    const int anomaly_offset = key.family.front() == 'E' ? 0 : 4;
    std::set<int> anomalies;
    for (int i = 0; i < 4; ++i) {
        const int needed = occurrences(key.pattern, CELLS[i]);
        for (int j = 0; j < needed; ++j) anomalies.insert(cells.at(anomaly_offset + i).at(j));
    }

    std::vector<Bucket> buckets;
    for (int color_index = 0; color_index < 2; ++color_index) {
        const char color = color_index == 0 ? 'E' : 'C';
        for (int cell_index = 0; cell_index < 4; ++cell_index) {
            for (int status = 0; status <= 1; ++status) {
                std::vector<int> vertices;
                for (int vertex : cells.at(4 * color_index + cell_index)) {
                    if (static_cast<int>(anomalies.count(vertex)) == status) {
                        vertices.push_back(vertex);
                    }
                }
                if (!vertices.empty()) {
                    std::string name;
                    name.push_back(color);
                    name.push_back(CELLS[cell_index]);
                    name.push_back(status ? 'a' : 'o');
                    buckets.push_back({name, color, CELLS[cell_index], status == 1, vertices});
                }
            }
        }
    }

    int pool_index = -1;
    for (int i = 0; i < static_cast<int>(buckets.size()); ++i) {
        const Bucket& bucket = buckets.at(i);
        if (bucket.color == 'C' && bucket.cell == 'H' && !bucket.anomalous) {
            require(pool_index == -1, "multiple ordinary central-H pools");
            pool_index = i;
        }
    }
    require(pool_index >= 0, "missing ordinary central-H pool");
    Bucket& pool = buckets.at(pool_index);
    const int pool_size = static_cast<int>(pool.vertices.size());
    require(pool_size >= 2, "third-anchor pool lower bound");
    const int third_anchor = *std::min_element(pool.vertices.begin(), pool.vertices.end());
    pool.vertices.erase(std::find(pool.vertices.begin(), pool.vertices.end(), third_anchor));

    int residual = 0;
    for (const auto& bucket : buckets) {
        require(!bucket.vertices.empty(), "empty refined bucket");
        residual += static_cast<int>(bucket.vertices.size());
    }
    require(residual == 40, "residual size");
    const std::set<int> partition_pair =
        key.family == "C77partition" ? anomalies : std::set<int>{};
    if (!partition_pair.empty()) require(partition_pair.size() == 2, "partition pair");
    return {key, third_anchor, pool_size, buckets, partition_pair};
}

unsigned long long binomial(int n, int k) {
    if (k < 0 || k > n) return 0;
    k = std::min(k, n - k);
    unsigned long long result = 1;
    for (int i = 1; i <= k; ++i) {
        result = result * static_cast<unsigned long long>(n - k + i)
                 / static_cast<unsigned long long>(i);
    }
    return result;
}

void recurse_counts(
    const Layout& root,
    std::size_t index,
    int red_e,
    int red_c,
    int red_h,
    int red_a,
    int red_b,
    int partition_red,
    unsigned long long labeling_weight,
    Counts& result
) {
    if (red_e > 6 || red_c > 13) return;
    if (index == root.buckets.size()) {
        if (red_e != 6 || red_c != 13) return;
        if (red_h < root.key.common - 9 || red_h > 4) return;
        if (red_h + red_a > 12 || red_h + red_b > 12) return;
        if (!root.partition_pair.empty() && partition_red != 1) return;
        ++result.orbits;
        result.labelings += labeling_weight;
        return;
    }
    const Bucket& bucket = root.buckets.at(index);
    const int size = static_cast<int>(bucket.vertices.size());
    int marked = 0;
    for (int vertex : bucket.vertices) marked += root.partition_pair.count(vertex);
    require(marked == 0 || (marked == size && size == 1), "partition bucket split");
    for (int chosen = 0; chosen <= size; ++chosen) {
        recurse_counts(
            root,
            index + 1,
            red_e + (bucket.color == 'E' ? chosen : 0),
            red_c + (bucket.color == 'C' ? chosen : 0),
            red_h + (bucket.cell == 'H' ? chosen : 0),
            red_a + (bucket.cell == 'A' ? chosen : 0),
            red_b + (bucket.cell == 'B' ? chosen : 0),
            partition_red + (marked ? chosen : 0),
            labeling_weight * binomial(size, chosen),
            result
        );
    }
}

Counts count_rows(const Layout& root) {
    Counts result;
    recurse_counts(root, 0, 0, 0, 0, 0, 0, 0, 1, result);
    require(result.orbits > 0 && result.labelings >= result.orbits, "row quotient");
    return result;
}

int edge_id(int i, int j) {
    if (i > j) std::swap(i, j);
    require(0 <= i && i < j && j < N, "edge ID input");
    return i * (2 * N - i - 1) / 2 + (j - i - 1) + 1;
}

std::string term(int coefficient, int variable) {
    std::ostringstream out;
    if (coefficient >= 0) out << '+';
    out << coefficient << " x" << variable;
    return out.str();
}

std::string row(const std::vector<std::pair<int, int>>& terms, int rhs) {
    require(!terms.empty(), "empty OPB row");
    std::ostringstream out;
    for (std::size_t i = 0; i < terms.size(); ++i) {
        if (i) out << ' ';
        out << term(terms.at(i).first, terms.at(i).second);
    }
    out << " >= " << rhs << " ;\n";
    return out.str();
}

std::string suffix(const std::vector<Key>& keys) {
    std::string result;
    for (std::size_t root_index = 0; root_index < keys.size(); ++root_index) {
        const Layout root = layout(keys.at(root_index));
        const int selector = SELECTOR_FIRST + static_cast<int>(root_index);
        for (const auto& bucket : root.buckets) {
            for (std::size_t i = 1; i < bucket.vertices.size(); ++i) {
                result += row({
                    {1, edge_id(root.third_anchor, bucket.vertices.at(i - 1))},
                    {-1, edge_id(root.third_anchor, bucket.vertices.at(i))},
                    {-1, selector},
                }, -1);
            }
        }
        std::map<char, std::vector<int>> by_cell;
        for (const auto& bucket : root.buckets) {
            auto& cell = by_cell[bucket.cell];
            cell.insert(cell.end(), bucket.vertices.begin(), bucket.vertices.end());
        }
        const auto& h = by_cell['H'];
        const auto& a = by_cell['A'];
        const auto& b = by_cell['B'];
        require(static_cast<int>(h.size()) == root.key.common - 1, "H size");
        require(static_cast<int>(a.size()) == 20 - root.key.common, "A size");
        require(static_cast<int>(b.size()) == 20 - root.key.common, "B size");
        if (root.key.common > 9) {
            std::vector<std::pair<int, int>> terms;
            for (int vertex : h) terms.push_back({1, edge_id(root.third_anchor, vertex)});
            terms.push_back({-(root.key.common - 9), selector});
            result += row(terms, 0);
        }
        {
            std::vector<std::pair<int, int>> terms;
            for (int vertex : h) terms.push_back({-1, edge_id(root.third_anchor, vertex)});
            terms.push_back({-(root.key.common - 5), selector});
            result += row(terms, -(root.key.common - 1));
        }
        for (const auto& side : {a, b}) {
            std::vector<std::pair<int, int>> terms;
            for (int vertex : h) terms.push_back({-1, edge_id(root.third_anchor, vertex)});
            for (int vertex : side) terms.push_back({-1, edge_id(root.third_anchor, vertex)});
            terms.push_back({-7, selector});
            result += row(terms, -19);
        }
    }
    return result;
}

std::string certificate(
    const std::vector<Key>& keys,
    std::array<unsigned long long, 5>& family_orbits,
    std::array<unsigned long long, 5>& family_labelings,
    int& ordering_rows,
    int& pool_min,
    int& pool_max,
    unsigned long long& minimum_numerator,
    unsigned long long& minimum_denominator,
    Key& minimum_key
) {
    const std::array<std::string, 5> families = {
        "E8", "E77", "C8", "C77", "C77partition"
    };
    std::ostringstream out;
    out << "family\tc\tk\tpattern\tthird_anchor\tpool_size\tbuckets_after_anchor"
           "\tordering_rows\torbit_rows\tlabeled_rows\n";
    for (const auto& key : keys) {
        const Layout root = layout(key);
        const Counts counts = count_rows(root);
        int root_ordering = 0;
        for (const auto& bucket : root.buckets) {
            root_ordering += static_cast<int>(bucket.vertices.size()) - 1;
        }
        out << key.family << '\t' << key.common << '\t' << key.exceptional_common
            << '\t' << key.pattern << '\t' << root.third_anchor << '\t'
            << root.pool_size << '\t';
        for (std::size_t i = 0; i < root.buckets.size(); ++i) {
            if (i) out << ',';
            out << root.buckets.at(i).name << ':' << root.buckets.at(i).vertices.size();
        }
        out << '\t' << root_ordering << '\t' << counts.orbits << '\t'
            << counts.labelings << '\n';

        const auto family_it = std::find(families.begin(), families.end(), key.family);
        require(family_it != families.end(), "family index");
        const std::size_t family_index = static_cast<std::size_t>(family_it - families.begin());
        family_orbits.at(family_index) += counts.orbits;
        family_labelings.at(family_index) += counts.labelings;
        ordering_rows += root_ordering;
        pool_min = std::min(pool_min, root.pool_size);
        pool_max = std::max(pool_max, root.pool_size);
        if (minimum_denominator == 0
            || counts.labelings * minimum_denominator
               < minimum_numerator * counts.orbits) {
            minimum_numerator = counts.labelings;
            minimum_denominator = counts.orbits;
            minimum_key = key;
        }
    }
    return out.str();
}

std::string read_file(const std::string& path) {
    std::ifstream input(path, std::ios::binary);
    require(input.good(), "cannot open " + path);
    std::ostringstream out;
    out << input.rdbuf();
    require(input.good() || input.eof(), "cannot read " + path);
    return out.str();
}

void compare_formula(const std::string& base_path, const std::string& strong_path,
                     const std::string& expected_suffix) {
    std::ifstream base(base_path, std::ios::binary);
    std::ifstream strong(strong_path, std::ios::binary);
    require(base.good() && strong.good(), "cannot open formula files");
    std::string base_header;
    std::string strong_header;
    std::getline(base, base_header);
    std::getline(strong, strong_header);
    require(base_header == "* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64",
            "base header");
    require(strong_header == "* #variable= 13633 #constraint= 2057998 #equal= 87 intsize= 64",
            "strengthened header");
    std::vector<char> base_buffer(1 << 20);
    std::vector<char> strong_buffer(1 << 20);
    while (base) {
        base.read(base_buffer.data(), static_cast<std::streamsize>(base_buffer.size()));
        const std::streamsize count = base.gcount();
        if (count == 0) break;
        strong.read(strong_buffer.data(), count);
        require(strong.gcount() == count, "short strengthened base body");
        require(std::equal(base_buffer.begin(), base_buffer.begin() + count,
                           strong_buffer.begin()), "strengthened base-body mismatch");
    }
    std::ostringstream remainder;
    remainder << strong.rdbuf();
    require(remainder.str() == expected_suffix, "strengthened suffix mismatch");
}

}  // namespace

int main(int argc, char** argv) {
    try {
        require(argc == 3 || argc == 5,
                "usage: independent_check CERTIFICATE SUFFIX [BASE_OPB STRONG_OPB]");
        const auto keys = root_keys();
        std::array<unsigned long long, 5> family_orbits{};
        std::array<unsigned long long, 5> family_labelings{};
        int ordering_rows = 0;
        int pool_min = std::numeric_limits<int>::max();
        int pool_max = 0;
        unsigned long long minimum_numerator = 0;
        unsigned long long minimum_denominator = 0;
        Key minimum_key;
        const std::string expected_certificate = certificate(
            keys, family_orbits, family_labelings, ordering_rows, pool_min, pool_max,
            minimum_numerator, minimum_denominator, minimum_key
        );
        const std::string expected_suffix = suffix(keys);
        require(read_file(argv[1]) == expected_certificate, "certificate byte mismatch");
        require(read_file(argv[2]) == expected_suffix, "suffix byte mismatch");
        if (argc == 5) compare_formula(argv[3], argv[4], expected_suffix);

        const unsigned long long total_orbits =
            std::accumulate(family_orbits.begin(), family_orbits.end(), 0ULL);
        const unsigned long long total_labelings =
            std::accumulate(family_labelings.begin(), family_labelings.end(), 0ULL);
        require(total_orbits == EXPECTED_ORBITS, "total orbit count");
        require(total_labelings == EXPECTED_LABELINGS, "total labeling count");
        require(ordering_rows == 12099, "ordering row count");
        require(pool_min == 2 && pool_max == 13, "pool extrema");
        require(expected_certificate.size() == 35697, "certificate byte count");
        require(static_cast<long long>(std::count(expected_suffix.begin(), expected_suffix.end(), '\n'))
                == EXPECTED_SUFFIX_ROWS, "suffix row count");
        require(expected_suffix.size() == 612502, "suffix byte count");
        require(minimum_numerator / minimum_denominator == 782213,
                "minimum compression floor");
        require(minimum_key.family == "C77partition" && minimum_key.common == 11
                && minimum_key.exceptional_common == 3 && minimum_key.pattern == "HO",
                "minimum compression key");

        std::cout << "PASS roots=389 pools=2..13 ordering_rows=" << ordering_rows << '\n';
        std::cout << "PASS orbit_rows=" << total_orbits
                  << " labeled_rows=" << total_labelings
                  << " min_compression_floor=" << minimum_numerator / minimum_denominator
                  << '\n';
        std::cout << "PASS family_orbits=";
        for (std::size_t i = 0; i < family_orbits.size(); ++i) {
            if (i) std::cout << ',';
            std::cout << family_orbits.at(i);
        }
        std::cout << '\n';
        std::cout << "PASS certificate_bytes=" << expected_certificate.size()
                  << " suffix_rows=" << EXPECTED_SUFFIX_ROWS
                  << " suffix_bytes=" << expected_suffix.size() << '\n';
        if (argc == 5) {
            std::cout << "PASS strengthened_formula constraints="
                      << BASE_CONSTRAINTS + EXPECTED_SUFFIX_ROWS << '\n';
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL " << error.what() << '\n';
        return 1;
    }
}
