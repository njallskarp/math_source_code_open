#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

#include <omp.h>

namespace {

constexpr int order = 43;
constexpr int edge_count = order * (order - 1) / 2;
constexpr int word_count = (edge_count + 63) / 64;

struct State {
    std::array<std::uint64_t, word_count> words{};
    bool operator==(const State&) const = default;
    bool operator<(const State& other) const { return words < other.words; }
    bool contains(int id) const {
        return (words[id / 64] >> (id % 64)) & 1ULL;
    }
    void toggle(int id) { words[id / 64] ^= 1ULL << (id % 64); }
};

struct StateHash {
    std::size_t operator()(const State& state) const noexcept {
        std::uint64_t hash = 0x517cc1b727220a95ULL;
        for (std::uint64_t word : state.words) {
            hash ^= word + 0x9e3779b97f4a7c15ULL + (hash << 6) + (hash >> 2);
        }
        return static_cast<std::size_t>(hash);
    }
};

struct FiveSet {
    std::array<std::uint16_t, 10> edges{};
};

std::string read_text(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open " + path);
    std::ostringstream buffer;
    buffer << input.rdbuf();
    return buffer.str();
}

std::string keyed_array(const std::string& text, const std::string& key) {
    const auto key_position = text.find('"' + key + '"');
    if (key_position == std::string::npos)
        throw std::runtime_error("missing JSON key " + key);
    const auto begin = text.find('[', key_position);
    if (begin == std::string::npos)
        throw std::runtime_error("malformed JSON array " + key);
    std::size_t end = begin;
    int nesting = 0;
    do {
        if (text[end] == '[') ++nesting;
        if (text[end] == ']') --nesting;
        ++end;
    } while (end < text.size() && nesting != 0);
    if (nesting != 0) throw std::runtime_error("unterminated JSON array " + key);
    return text.substr(begin, end - begin);
}

std::set<std::pair<int, int>> load_flips(const std::string& path) {
    const std::string array = keyed_array(read_text(path), "flipped_edges");
    const std::regex pair_pattern(R"(\[\s*([0-9]+)\s*,\s*([0-9]+)\s*\])");
    std::set<std::pair<int, int>> flips;
    for (std::sregex_iterator it(array.begin(), array.end(), pair_pattern), last;
         it != last; ++it) {
        int a = std::stoi((*it)[1]);
        int b = std::stoi((*it)[2]);
        if (a > b) std::swap(a, b);
        flips.insert({a, b});
    }
    return flips;
}

std::vector<State> load_representatives(const std::string& path) {
    const std::string array = keyed_array(
        read_text(path), "objective_six_rotation_representatives"
    );
    const std::regex list_pattern(R"(\[([^\[\]]*)\])");
    const std::regex integer_pattern(R"(([0-9]+))");
    std::vector<State> result;
    for (std::sregex_iterator it(array.begin(), array.end(), list_pattern), last;
         it != last; ++it) {
        State state;
        const std::string inner = (*it)[1];
        for (std::sregex_iterator jt(
                 inner.begin(), inner.end(), integer_pattern
             ), integer_last;
             jt != integer_last; ++jt) {
            const int id = std::stoi((*jt)[1]);
            if (id < 0 || id >= edge_count)
                throw std::runtime_error("invalid representative edge id");
            state.toggle(id);
        }
        result.push_back(state);
    }
    if (result.empty()) throw std::runtime_error("no representatives");
    return result;
}

struct Verifier {
    std::array<std::array<int, order>, order> edge_id{};
    std::array<std::pair<int, int>, edge_count> edge_vertices{};
    std::array<std::array<std::uint16_t, edge_count>, order> rotated_edge{};
    std::array<bool, edge_count> seed_red{};
    std::vector<FiveSet> five_sets;
    std::vector<State> representatives;
    std::unordered_set<State, StateHash> representative_set;

    Verifier(
        const std::set<std::pair<int, int>>& certificate_flips,
        std::vector<State> loaded_representatives
    ) : representatives(std::move(loaded_representatives)) {
        int next_edge = 0;
        for (int a = 0; a < order; ++a) {
            for (int b = a + 1; b < order; ++b) {
                edge_id[a][b] = edge_id[b][a] = next_edge;
                edge_vertices[next_edge] = {a, b};
                int delta = (a - b) % order;
                if (delta < 0) delta += order;
                const int distance = std::min(delta, order - delta);
                seed_red[next_edge] =
                    distance == 1 || distance == 2 || distance == 7 ||
                    distance == 10 || distance == 12 || distance == 13 ||
                    distance == 14 || distance == 16 || distance == 18 ||
                    distance == 20 || distance == 21;
                ++next_edge;
            }
        }
        for (int offset = 0; offset < order; ++offset) {
            for (int id = 0; id < edge_count; ++id) {
                auto [a, b] = edge_vertices[id];
                a = (a + offset) % order;
                b = (b + offset) % order;
                rotated_edge[offset][id] = static_cast<std::uint16_t>(edge_id[a][b]);
            }
        }
        five_sets.reserve(962598);
        for (int a = 0; a < order; ++a)
            for (int b = a + 1; b < order; ++b)
                for (int c = b + 1; c < order; ++c)
                    for (int d = c + 1; d < order; ++d)
                        for (int e = d + 1; e < order; ++e) {
                            const std::array<int, 5> vertices = {a, b, c, d, e};
                            FiveSet five;
                            int position = 0;
                            for (int i = 0; i < 5; ++i)
                                for (int j = i + 1; j < 5; ++j)
                                    five.edges[position++] = static_cast<std::uint16_t>(
                                        edge_id[vertices[i]][vertices[j]]
                                    );
                            five_sets.push_back(five);
                        }
        if (five_sets.size() != 962598)
            throw std::runtime_error("five-set count mismatch");

        State certificate;
        for (const auto& changed : certificate_flips)
            certificate.toggle(edge_id[changed.first][changed.second]);
        if (certificate.words == State{}.words)
            throw std::runtime_error("empty certificate state");

        for (const State& state : representatives) {
            if (!(canonical(state) == state))
                throw std::runtime_error("representative is not canonical");
            if (rotate(state, 1) == state)
                throw std::runtime_error("representative has rotation stabilizer");
            if (!representative_set.insert(state).second)
                throw std::runtime_error("duplicate representative");
        }
    }

    State rotate(const State& source, int offset) const {
        State result;
        for (int word_index = 0; word_index < word_count; ++word_index) {
            std::uint64_t word = source.words[word_index];
            while (word) {
                const int bit = std::countr_zero(word);
                const int id = 64 * word_index + bit;
                if (id < edge_count) {
                    const int mapped = rotated_edge[offset][id];
                    result.words[mapped / 64] |= 1ULL << (mapped % 64);
                }
                word &= word - 1;
            }
        }
        return result;
    }

    State canonical(const State& source) const {
        State best = source;
        for (int offset = 1; offset < order; ++offset) {
            State candidate = rotate(source, offset);
            if (candidate < best) best = candidate;
        }
        return best;
    }

    struct ThreadSummary {
        std::map<int, std::uint64_t> histogram;
        std::map<int, std::uint64_t> lower_histogram;
        std::uint64_t same_layer_directed = 0;
        std::uint64_t verified_representatives = 0;
        std::uint64_t missing_same_layer_neighbors = 0;
    };

    ThreadSummary verify_one(const State& state) const {
        std::array<bool, edge_count> red{};
        for (int id = 0; id < edge_count; ++id)
            red[id] = seed_red[id] != state.contains(id);
        std::array<int, edge_count> delta{};
        int monochromatic = 0;
        for (const FiveSet& five : five_sets) {
            int count = 0;
            for (int id : five.edges) count += red[id];
            if (count == 0 || count == 10) {
                ++monochromatic;
                for (int id : five.edges) --delta[id];
            } else if (count == 1) {
                for (int id : five.edges) {
                    if (red[id]) {
                        ++delta[id];
                        break;
                    }
                }
            } else if (count == 9) {
                for (int id : five.edges) {
                    if (!red[id]) {
                        ++delta[id];
                        break;
                    }
                }
            }
        }
        if (monochromatic != 6)
            throw std::runtime_error("representative direct recount is not six");

        ThreadSummary result;
        result.verified_representatives = 1;
        for (int id = 0; id < edge_count; ++id) {
            const int objective = monochromatic + delta[id];
            ++result.histogram[objective];
            if (objective < 6) ++result.lower_histogram[objective];
            if (objective != 6) continue;
            ++result.same_layer_directed;
            State neighbor = state;
            neighbor.toggle(id);
            if (!representative_set.contains(canonical(neighbor)))
                ++result.missing_same_layer_neighbors;
        }
        return result;
    }

    ThreadSummary verify_all() const {
        const int thread_count = omp_get_max_threads();
        std::vector<ThreadSummary> summaries(thread_count);
        std::string error;

#pragma omp parallel for schedule(dynamic, 1)
        for (std::size_t index = 0; index < representatives.size(); ++index) {
            try {
                ThreadSummary local = verify_one(representatives[index]);
                ThreadSummary& destination = summaries[omp_get_thread_num()];
                for (const auto& [objective, count] : local.histogram)
                    destination.histogram[objective] += count;
                for (const auto& [objective, count] : local.lower_histogram)
                    destination.lower_histogram[objective] += count;
                destination.same_layer_directed += local.same_layer_directed;
                destination.verified_representatives +=
                    local.verified_representatives;
                destination.missing_same_layer_neighbors +=
                    local.missing_same_layer_neighbors;
            } catch (const std::exception& exception) {
#pragma omp critical
                {
                    if (error.empty()) error = exception.what();
                }
            }
        }
        if (!error.empty()) throw std::runtime_error(error);

        ThreadSummary total;
        for (const ThreadSummary& source : summaries) {
            for (const auto& [objective, count] : source.histogram)
                total.histogram[objective] += count;
            for (const auto& [objective, count] : source.lower_histogram)
                total.lower_histogram[objective] += count;
            total.same_layer_directed += source.same_layer_directed;
            total.verified_representatives += source.verified_representatives;
            total.missing_same_layer_neighbors +=
                source.missing_same_layer_neighbors;
        }
        return total;
    }

    void write_json(std::ostream& output) const {
        const ThreadSummary summary = verify_all();
        if (summary.verified_representatives != representatives.size())
            throw std::runtime_error("not all representatives were verified");
        if (summary.missing_same_layer_neighbors)
            throw std::runtime_error("objective-six closure failure");

        output << "{\n";
        output << "  \"independent_direct_recount_representative_count\": "
               << summary.verified_representatives << ",\n";
        output << "  \"rotation_orbit_count\": " << representatives.size()
               << ",\n";
        output << "  \"same_layer_directed_edge_count\": "
               << order * summary.same_layer_directed << ",\n";
        output << "  \"missing_same_layer_neighbor_count\": 0,\n";
        output << "  \"lower_neighbor_histogram\": {";
        bool separator = false;
        for (const auto& [objective, count] : summary.lower_histogram) {
            if (separator) output << ',';
            output << "\n    \"" << objective << "\": " << order * count;
            separator = true;
        }
        if (separator) output << '\n';
        output << "  },\n";
        output << "  \"aggregate_neighbor_objective_histogram\": {";
        separator = false;
        for (const auto& [objective, count] : summary.histogram) {
            if (separator) output << ',';
            output << "\n    \"" << objective << "\": " << order * count;
            separator = true;
        }
        if (separator) output << '\n';
        output << "  },\n";
        output << "  \"method\": \"parallel independent direct five-set recount with fresh per-representative deltas\",\n";
        output << "  \"openmp_max_threads\": " << omp_get_max_threads() << "\n";
        output << "}\n";
    }
};

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 3) {
        std::cerr << "usage: verify_objective_six_component CERTIFICATE.json "
                     "objective-six-component-representatives.json\n";
        return 2;
    }
    Verifier verifier(load_flips(argv[1]), load_representatives(argv[2]));
    verifier.write_json(std::cout);
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
