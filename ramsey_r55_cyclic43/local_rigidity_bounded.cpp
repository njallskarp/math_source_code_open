#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <regex>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {

constexpr int order = 43;
constexpr int edge_count = order * (order - 1) / 2;
constexpr int maximum_supported_radius = 6;

struct FiveSet {
    std::array<std::uint8_t, 5> vertices{};
    std::array<std::uint16_t, 10> edges{};
};

struct Search {
    std::array<std::array<int, order>, order> edge_id{};
    std::array<std::pair<int, int>, edge_count> edge_vertices{};
    std::array<bool, edge_count> red{};
    std::vector<FiveSet> five_sets;
    std::vector<std::vector<int>> incident;
    std::vector<std::uint8_t> red_count;
    std::set<int> monochromatic;
    int search_radius;
    std::vector<std::unordered_set<std::uint64_t>> visited;
    std::vector<std::uint64_t> expanded;
    std::vector<std::uint64_t> distinct_states;
    std::uint64_t branches = 0;
    std::size_t maximum_mono_count = 0;
    std::vector<int> solution;

    Search(const std::set<std::pair<int, int>>& certificate_flips, int radius)
        : incident(edge_count),
          search_radius(radius),
          visited(radius + 1),
          expanded(radius + 1),
          distinct_states(radius + 1) {
        int next_edge = 0;
        for (int a = 0; a < order; ++a) {
            for (int b = a + 1; b < order; ++b) {
                edge_id[a][b] = edge_id[b][a] = next_edge;
                edge_vertices[next_edge] = {a, b};
                int delta = (a - b) % order;
                if (delta < 0) delta += order;
                const int distance = std::min(delta, order - delta);
                const bool seed_red =
                    distance == 1 || distance == 2 || distance == 7 ||
                    distance == 10 || distance == 12 || distance == 13 ||
                    distance == 14 || distance == 16 || distance == 18 ||
                    distance == 20 || distance == 21;
                red[next_edge] =
                    seed_red && !certificate_flips.contains({a, b});
                ++next_edge;
            }
        }
        if (next_edge != edge_count) throw std::logic_error("edge count");

        five_sets.reserve(962598);
        red_count.reserve(962598);
        for (int a = 0; a < order; ++a)
            for (int b = a + 1; b < order; ++b)
                for (int c = b + 1; c < order; ++c)
                    for (int d = c + 1; d < order; ++d)
                        for (int e = d + 1; e < order; ++e) {
                            FiveSet five;
                            five.vertices = {
                                static_cast<std::uint8_t>(a),
                                static_cast<std::uint8_t>(b),
                                static_cast<std::uint8_t>(c),
                                static_cast<std::uint8_t>(d),
                                static_cast<std::uint8_t>(e),
                            };
                            const std::array<int, 5> v = {a, b, c, d, e};
                            int position = 0;
                            int reds = 0;
                            for (int i = 0; i < 5; ++i) {
                                for (int j = i + 1; j < 5; ++j) {
                                    const int id = edge_id[v[i]][v[j]];
                                    five.edges[position++] =
                                        static_cast<std::uint16_t>(id);
                                    reds += red[id];
                                }
                            }
                            const int id = static_cast<int>(five_sets.size());
                            for (int edge : five.edges) incident[edge].push_back(id);
                            five_sets.push_back(five);
                            red_count.push_back(static_cast<std::uint8_t>(reds));
                            if (reds == 0 || reds == 10) monochromatic.insert(id);
                        }
        if (five_sets.size() != 962598) throw std::logic_error("five-set count");
        if (monochromatic.size() != 2)
            throw std::runtime_error("certificate is not an optimum-2 coloring");
        for (const auto& list : incident)
            if (list.size() != 10660) throw std::logic_error("incidence count");
        maximum_mono_count = monochromatic.size();
    }

    void toggle(int id) {
        const int delta = red[id] ? -1 : 1;
        red[id] = !red[id];
        for (int five_id : incident[id]) {
            const int old_count = red_count[five_id];
            const int new_count = old_count + delta;
            const bool old_mono = old_count == 0 || old_count == 10;
            const bool new_mono = new_count == 0 || new_count == 10;
            if (old_mono && !new_mono) monochromatic.erase(five_id);
            if (!old_mono && new_mono) monochromatic.insert(five_id);
            red_count[five_id] = static_cast<std::uint8_t>(new_count);
        }
        maximum_mono_count = std::max(maximum_mono_count, monochromatic.size());
    }

    static std::uint64_t state_key(std::vector<int> flips) {
        std::sort(flips.begin(), flips.end());
        std::uint64_t key = 0;
        for (int id : flips) key = key * 1024 + static_cast<unsigned>(id + 1);
        return key;
    }

    bool search(std::vector<int>& flips) {
        const int depth = static_cast<int>(flips.size());
        ++expanded[depth];
        if (monochromatic.size() <= 1) {
            solution = flips;
            return true;
        }
        if (depth == search_radius) return false;

        auto witness = monochromatic.begin();
        const int first = *witness++;
        const int second = *witness;
        std::array<bool, edge_count> candidate_seen{};
        std::vector<int> candidates;
        for (int five_id : {first, second}) {
            for (int id : five_sets[five_id].edges) {
                if (!candidate_seen[id] &&
                    std::find(flips.begin(), flips.end(), id) == flips.end()) {
                    candidate_seen[id] = true;
                    candidates.push_back(id);
                }
            }
        }
        std::sort(candidates.begin(), candidates.end());

        for (int id : candidates) {
            ++branches;
            flips.push_back(id);
            const auto key = state_key(flips);
            if (visited[depth + 1].insert(key).second) {
                ++distinct_states[depth + 1];
                toggle(id);
                if (search(flips)) return true;
                toggle(id);
            }
            flips.pop_back();
        }
        return false;
    }
};

std::set<std::pair<int, int>> load_flips(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open certificate: " + path);
    std::ostringstream buffer;
    buffer << input.rdbuf();
    const std::string text = buffer.str();
    const auto key = text.find("\"flipped_edges\"");
    if (key == std::string::npos) throw std::runtime_error("missing flipped_edges");
    const auto begin = text.find('[', key);
    if (begin == std::string::npos) throw std::runtime_error("malformed flipped_edges");
    std::size_t end = begin;
    int nesting = 0;
    do {
        if (text[end] == '[') ++nesting;
        if (text[end] == ']') --nesting;
        ++end;
    } while (end < text.size() && nesting != 0);
    if (nesting != 0) throw std::runtime_error("unterminated flipped_edges");

    const std::string array = text.substr(begin, end - begin);
    const std::regex pair_pattern(R"(\[\s*([0-9]+)\s*,\s*([0-9]+)\s*\])");
    std::set<std::pair<int, int>> flips;
    for (std::sregex_iterator it(array.begin(), array.end(), pair_pattern), last;
         it != last; ++it) {
        int a = std::stoi((*it)[1]);
        int b = std::stoi((*it)[2]);
        if (a > b) std::swap(a, b);
        if (a < 0 || b >= order || a == b)
            throw std::runtime_error("invalid flipped edge");
        flips.insert({a, b});
    }
    if (flips.empty()) throw std::runtime_error("empty flipped_edges");
    return flips;
}

void write_vertices(std::ostream& out, const FiveSet& five) {
    out << '[';
    for (std::size_t i = 0; i < five.vertices.size(); ++i) {
        if (i) out << ',';
        out << static_cast<int>(five.vertices[i]);
    }
    out << ']';
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc < 2 || argc > 3) {
        std::cerr << "usage: local_rigidity_bounded CERTIFICATE.json [RADIUS]\n";
        return 2;
    }
    const int radius = argc == 3 ? std::stoi(argv[2]) : 4;
    if (radius < 1 || radius > maximum_supported_radius)
        throw std::runtime_error("radius must be between 1 and 6");
    const auto flips = load_flips(argv[1]);
    Search instance(flips, radius);
    std::vector<int> path;
    const bool improvement_found = instance.search(path);

    std::cout << "{\n";
    std::cout << "  \"certificate\": \"" << argv[1] << "\",\n";
    std::cout << "  \"base_monochromatic_k5_count\": 2,\n";
    std::cout << "  \"base_monochromatic_k5\": [";
    bool separator = false;
    for (int id : instance.monochromatic) {
        if (separator) std::cout << ',';
        write_vertices(std::cout, instance.five_sets[id]);
        separator = true;
    }
    std::cout << "],\n";
    std::cout << "  \"radius\": " << instance.search_radius << ",\n";
    std::cout << "  \"target_monochromatic_k5_count\": 1,\n";
    std::cout << "  \"improvement_found\": "
              << (improvement_found ? "true" : "false") << ",\n";
    std::cout << "  \"exact_minimum_through_requested_radius\": "
              << (improvement_found ? "null" : "2") << ",\n";
    std::cout << "  \"expanded_by_depth\": [";
    for (int depth = 0; depth <= instance.search_radius; ++depth) {
        if (depth) std::cout << ',';
        std::cout << instance.expanded[depth];
    }
    std::cout << "],\n";
    std::cout << "  \"distinct_nonroot_states_by_depth\": [";
    for (int depth = 0; depth <= instance.search_radius; ++depth) {
        if (depth) std::cout << ',';
        std::cout << instance.distinct_states[depth];
    }
    std::cout << "],\n";
    std::cout << "  \"candidate_branches_considered\": "
              << instance.branches << ",\n";
    std::cout << "  \"maximum_intermediate_monochromatic_k5_count\": "
              << instance.maximum_mono_count << ",\n";
    std::cout << "  \"completeness_argument\": "
              << "\"At a state with at least two monochromatic K5s, any extension "
                 "ending with at most one must flip an edge in at least one of two "
                 "chosen witnesses. Branching over their edge union is exhaustive; "
                 "memoization removes only duplicate flip sets.\"\n";
    std::cout << "}\n";
    return improvement_found ? 1 : 0;
} catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 2;
}
