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
#include <unordered_map>
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

std::vector<std::vector<int>> load_integer_arrays(
    const std::string& path, const std::string& key
) {
    const std::string array = keyed_array(read_text(path), key);
    const std::regex list_pattern(R"(\[([^\[\]]*)\])");
    const std::regex integer_pattern(R"(([0-9]+))");
    std::vector<std::vector<int>> result;
    for (std::sregex_iterator it(array.begin(), array.end(), list_pattern), last;
         it != last; ++it) {
        std::vector<int> values;
        const std::string inner = (*it)[1];
        for (std::sregex_iterator jt(
                 inner.begin(), inner.end(), integer_pattern
             ), integer_last;
             jt != integer_last; ++jt) {
            values.push_back(std::stoi((*jt)[1]));
        }
        result.push_back(std::move(values));
    }
    return result;
}

std::vector<State> load_representatives(
    const std::string& path, const std::string& key
) {
    std::vector<State> result;
    for (const std::vector<int>& values : load_integer_arrays(path, key)) {
        State state;
        for (int id : values) {
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

    static void write_state(std::ostream& output, const State& state) {
        output << '[';
        bool separator = false;
        for (int id = 0; id < edge_count; ++id) {
            if (!state.contains(id)) continue;
            if (separator) output << ',';
            output << id;
            separator = true;
        }
        output << ']';
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

    struct FrontierSummary {
        std::array<std::uint64_t, 7> incidence_by_source{};
        std::uint64_t verified_representatives = 0;
        std::uint64_t noncanonical_representatives = 0;
        std::uint64_t nonfree_representatives = 0;
        std::uint64_t objective_mismatches = 0;
        std::uint64_t missing_lower_neighbors = 0;
        std::uint64_t signature_mismatches = 0;
    };

    FrontierSummary verify_frontier_one(
        const State& state,
        const std::array<std::unordered_set<State, StateHash>, 7>& lower_sets,
        const std::vector<int>& expected_signature
    ) const {
        FrontierSummary result;
        result.verified_representatives = 1;
        if (!(canonical(state) == state)) ++result.noncanonical_representatives;
        if (rotate(state, 1) == state) ++result.nonfree_representatives;

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
        if (monochromatic != 7) {
            ++result.objective_mismatches;
            return result;
        }

        std::array<std::uint64_t, 7> local_incidence{};
        for (int id = 0; id < edge_count; ++id) {
            const int objective = monochromatic + delta[id];
            if (objective > 6) continue;
            State neighbor = state;
            neighbor.toggle(id);
            const State key = canonical(neighbor);
            if (objective < 2 || !lower_sets[objective].contains(key)) {
                ++result.missing_lower_neighbors;
                continue;
            }
            ++local_incidence[objective];
        }
        for (int objective = 2; objective <= 6; ++objective) {
            result.incidence_by_source[objective] = local_incidence[objective];
            if (expected_signature.size() != 5 ||
                static_cast<std::uint64_t>(expected_signature[objective - 2]) !=
                    local_incidence[objective])
                ++result.signature_mismatches;
        }
        return result;
    }

    void write_frontier_json(
        const std::string& frontier_path, std::ostream& output
    ) const {
        std::array<std::unordered_set<State, StateHash>, 7> lower_sets;
        for (int objective = 2; objective <= 6; ++objective) {
            const auto states = load_representatives(
                frontier_path,
                "objective_" + std::to_string(objective) +
                    "_rotation_representatives"
            );
            for (const State& state : states) {
                if (!(canonical(state) == state))
                    throw std::runtime_error(
                        "noncanonical lower-layer representative"
                    );
                lower_sets[objective].insert(state);
            }
        }
        if (lower_sets[2].size() != 2 || lower_sets[3].size() != 17 ||
            lower_sets[4].size() != 78 || lower_sets[5].size() != 306 ||
            lower_sets[6].size() != 1183)
            throw std::runtime_error("lower-layer representative count mismatch");

        const std::vector<State> targets = load_representatives(
            frontier_path, "objective_seven_rotation_representatives"
        );
        const std::vector<std::vector<int>> signatures = load_integer_arrays(
            frontier_path,
            "objective_seven_incidence_signatures_2_through_6"
        );
        if (targets.empty() || targets.size() != signatures.size())
            throw std::runtime_error("frontier/signature count mismatch");
        std::unordered_set<State, StateHash> target_set;
        for (const State& target : targets)
            if (!target_set.insert(target).second)
                throw std::runtime_error("duplicate objective-seven representative");

        const int thread_count = omp_get_max_threads();
        std::vector<FrontierSummary> thread_summaries(thread_count);
        std::string error;
#pragma omp parallel for schedule(dynamic, 1)
        for (std::size_t index = 0; index < targets.size(); ++index) {
            try {
                const FrontierSummary local = verify_frontier_one(
                    targets[index], lower_sets, signatures[index]
                );
                FrontierSummary& destination =
                    thread_summaries[omp_get_thread_num()];
                for (int objective = 2; objective <= 6; ++objective)
                    destination.incidence_by_source[objective] +=
                        local.incidence_by_source[objective];
                destination.verified_representatives +=
                    local.verified_representatives;
                destination.noncanonical_representatives +=
                    local.noncanonical_representatives;
                destination.nonfree_representatives +=
                    local.nonfree_representatives;
                destination.objective_mismatches += local.objective_mismatches;
                destination.missing_lower_neighbors +=
                    local.missing_lower_neighbors;
                destination.signature_mismatches += local.signature_mismatches;
            } catch (const std::exception& exception) {
#pragma omp critical
                {
                    if (error.empty()) error = exception.what();
                }
            }
        }
        if (!error.empty()) throw std::runtime_error(error);

        FrontierSummary total;
        for (const FrontierSummary& source : thread_summaries) {
            for (int objective = 2; objective <= 6; ++objective)
                total.incidence_by_source[objective] +=
                    source.incidence_by_source[objective];
            total.verified_representatives += source.verified_representatives;
            total.noncanonical_representatives +=
                source.noncanonical_representatives;
            total.nonfree_representatives += source.nonfree_representatives;
            total.objective_mismatches += source.objective_mismatches;
            total.missing_lower_neighbors += source.missing_lower_neighbors;
            total.signature_mismatches += source.signature_mismatches;
        }
        if (total.verified_representatives != targets.size() ||
            total.noncanonical_representatives ||
            total.nonfree_representatives || total.objective_mismatches ||
            total.missing_lower_neighbors || total.signature_mismatches)
            throw std::runtime_error("objective-seven frontier verification failed");

        output << "{\n";
        output << "  \"independent_direct_recount_representative_count\": "
               << total.verified_representatives << ",\n";
        output << "  \"all_representatives_have_objective_seven\": true,\n";
        output << "  \"all_representatives_are_canonical_and_free\": true,\n";
        output << "  \"missing_lower_neighbor_count\": 0,\n";
        output << "  \"incidence_signature_mismatch_count\": 0,\n";
        output << "  \"directed_incidence_by_source_objective\": {";
        for (int objective = 2; objective <= 6; ++objective) {
            if (objective != 2) output << ',';
            output << "\n    \"" << objective << "\": "
                   << order * total.incidence_by_source[objective];
        }
        output << "\n  },\n";
        output << "  \"method\": \"parallel independent direct five-set recount and fresh lower-neighbor membership check\",\n";
        output << "  \"openmp_max_threads\": " << omp_get_max_threads()
               << "\n}\n";
    }

    struct ComponentSummary {
        std::map<int, std::uint64_t> histogram;
        std::uint64_t verified_representatives = 0;
        std::uint64_t noncanonical_representatives = 0;
        std::uint64_t nonfree_representatives = 0;
        std::uint64_t objective_mismatches = 0;
        std::uint64_t missing_accepted_neighbors = 0;
    };

    ComponentSummary verify_component_one(
        const State& state,
        const std::array<std::unordered_set<State, StateHash>, 7>& lower_sets,
        const std::unordered_set<State, StateHash>& component_set
    ) const {
        ComponentSummary result;
        result.verified_representatives = 1;
        if (!(canonical(state) == state)) ++result.noncanonical_representatives;
        if (rotate(state, 1) == state) ++result.nonfree_representatives;

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
        if (monochromatic != 7) {
            ++result.objective_mismatches;
            return result;
        }

        for (int id = 0; id < edge_count; ++id) {
            const int objective = monochromatic + delta[id];
            ++result.histogram[objective];
            if (objective > 7) continue;
            State neighbor = state;
            neighbor.toggle(id);
            const State key = canonical(neighbor);
            const bool present = objective == 7
                ? component_set.contains(key)
                : objective >= 2 && lower_sets[objective].contains(key);
            if (!present) ++result.missing_accepted_neighbors;
        }
        return result;
    }

    void write_component_json(
        const std::string& component_path,
        const std::string& lower_path,
        std::ostream& output
    ) const {
        std::array<std::unordered_set<State, StateHash>, 7> lower_sets;
        for (int objective = 2; objective <= 6; ++objective) {
            const auto states = load_representatives(
                lower_path,
                "objective_" + std::to_string(objective) +
                    "_rotation_representatives"
            );
            for (const State& state : states)
                if (!lower_sets[objective].insert(state).second)
                    throw std::runtime_error("duplicate lower representative");
        }
        if (lower_sets[2].size() != 2 || lower_sets[3].size() != 17 ||
            lower_sets[4].size() != 78 || lower_sets[5].size() != 306 ||
            lower_sets[6].size() != 1183)
            throw std::runtime_error("lower-layer representative count mismatch");

        const std::vector<State> component = load_representatives(
            component_path,
            "objective_seven_component_rotation_representatives"
        );
        std::unordered_set<State, StateHash> component_set;
        for (const State& state : component)
            if (!component_set.insert(state).second)
                throw std::runtime_error("duplicate component representative");
        if (component.size() != 4217)
            throw std::runtime_error("objective-seven component count mismatch");

        const int thread_count = omp_get_max_threads();
        std::vector<ComponentSummary> thread_summaries(thread_count);
        std::string error;
#pragma omp parallel for schedule(dynamic, 1)
        for (std::size_t index = 0; index < component.size(); ++index) {
            try {
                const ComponentSummary local = verify_component_one(
                    component[index], lower_sets, component_set
                );
                ComponentSummary& destination =
                    thread_summaries[omp_get_thread_num()];
                for (const auto& [objective, count] : local.histogram)
                    destination.histogram[objective] += count;
                destination.verified_representatives +=
                    local.verified_representatives;
                destination.noncanonical_representatives +=
                    local.noncanonical_representatives;
                destination.nonfree_representatives +=
                    local.nonfree_representatives;
                destination.objective_mismatches += local.objective_mismatches;
                destination.missing_accepted_neighbors +=
                    local.missing_accepted_neighbors;
            } catch (const std::exception& exception) {
#pragma omp critical
                {
                    if (error.empty()) error = exception.what();
                }
            }
        }
        if (!error.empty()) throw std::runtime_error(error);

        ComponentSummary total;
        for (const ComponentSummary& source : thread_summaries) {
            for (const auto& [objective, count] : source.histogram)
                total.histogram[objective] += count;
            total.verified_representatives += source.verified_representatives;
            total.noncanonical_representatives +=
                source.noncanonical_representatives;
            total.nonfree_representatives += source.nonfree_representatives;
            total.objective_mismatches += source.objective_mismatches;
            total.missing_accepted_neighbors +=
                source.missing_accepted_neighbors;
        }
        if (total.verified_representatives != component.size() ||
            total.noncanonical_representatives ||
            total.nonfree_representatives || total.objective_mismatches ||
            total.missing_accepted_neighbors)
            throw std::runtime_error("objective-seven component verification failed");
        if (order * total.histogram[7] != 2 * 219988)
            throw std::runtime_error("objective-seven induced edge mismatch");

        int escape_level = -1;
        for (const auto& [objective, count] : total.histogram) {
            if (objective > 7 && count) {
                escape_level = objective;
                break;
            }
        }
        if (escape_level != 8)
            throw std::runtime_error("objective-seven escape mismatch");

        output << "{\n";
        output << "  \"independent_direct_recount_representative_count\": "
               << total.verified_representatives << ",\n";
        output << "  \"all_representatives_have_objective_seven\": true,\n";
        output << "  \"all_representatives_are_canonical_and_free\": true,\n";
        output << "  \"missing_objective_at_most_seven_neighbor_count\": 0,\n";
        output << "  \"objective_seven_component_is_closed\": true,\n";
        output << "  \"objective_seven_induced_edge_count\": 219988,\n";
        output << "  \"exact_one_flip_escape_level\": " << escape_level
               << ",\n";
        output << "  \"aggregate_neighbor_objective_histogram\": {";
        bool separator = false;
        for (const auto& [objective, count] : total.histogram) {
            if (separator) output << ',';
            output << "\n    \"" << objective << "\": " << order * count;
            separator = true;
        }
        output << "\n  },\n";
        output << "  \"method\": \"parallel independent direct five-set recount with full threshold-seven membership checks\",\n";
        output << "  \"openmp_max_threads\": " << omp_get_max_threads()
               << "\n}\n";
    }

    ComponentSummary verify_objective_eight_component_one(
        const State& state,
        const std::array<std::unordered_set<State, StateHash>, 7>& lower_sets,
        const std::unordered_set<State, StateHash>& objective_seven_set,
        const std::unordered_set<State, StateHash>& objective_eight_set
    ) const {
        ComponentSummary result;
        result.verified_representatives = 1;
        if (!(canonical(state) == state)) ++result.noncanonical_representatives;
        if (rotate(state, 1) == state) ++result.nonfree_representatives;

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
        if (monochromatic != 8) {
            ++result.objective_mismatches;
            return result;
        }

        for (int id = 0; id < edge_count; ++id) {
            const int objective = monochromatic + delta[id];
            ++result.histogram[objective];
            if (objective > 8) continue;
            State neighbor = state;
            neighbor.toggle(id);
            const State key = canonical(neighbor);
            bool present = false;
            if (objective == 8)
                present = objective_eight_set.contains(key);
            else if (objective == 7)
                present = objective_seven_set.contains(key);
            else if (objective >= 2)
                present = lower_sets[objective].contains(key);
            if (!present) ++result.missing_accepted_neighbors;
        }
        return result;
    }

    void write_objective_eight_component_json(
        const std::string& component_path,
        const std::string& objective_seven_path,
        const std::string& lower_path,
        std::ostream& output
    ) const {
        std::array<std::unordered_set<State, StateHash>, 7> lower_sets;
        for (int objective = 2; objective <= 6; ++objective) {
            const auto states = load_representatives(
                lower_path,
                "objective_" + std::to_string(objective) +
                    "_rotation_representatives"
            );
            for (const State& state : states)
                if (!lower_sets[objective].insert(state).second)
                    throw std::runtime_error("duplicate lower representative");
        }
        if (lower_sets[2].size() != 2 || lower_sets[3].size() != 17 ||
            lower_sets[4].size() != 78 || lower_sets[5].size() != 306 ||
            lower_sets[6].size() != 1183)
            throw std::runtime_error("lower-layer representative count mismatch");

        const std::vector<State> objective_seven = load_representatives(
            objective_seven_path,
            "objective_seven_component_rotation_representatives"
        );
        std::unordered_set<State, StateHash> objective_seven_set;
        for (const State& state : objective_seven)
            if (!objective_seven_set.insert(state).second)
                throw std::runtime_error("duplicate objective-seven representative");
        if (objective_seven_set.size() != 4217)
            throw std::runtime_error("objective-seven representative count mismatch");

        const std::vector<State> component = load_representatives(
            component_path,
            "objective_eight_component_rotation_representatives"
        );
        std::unordered_set<State, StateHash> component_set;
        for (const State& state : component)
            if (!component_set.insert(state).second)
                throw std::runtime_error("duplicate objective-eight representative");
        if (component.size() != 13738)
            throw std::runtime_error("objective-eight component count mismatch");

        const int thread_count = omp_get_max_threads();
        std::vector<ComponentSummary> thread_summaries(thread_count);
        std::string error;
#pragma omp parallel for schedule(dynamic, 1)
        for (std::size_t index = 0; index < component.size(); ++index) {
            try {
                const ComponentSummary local =
                    verify_objective_eight_component_one(
                        component[index], lower_sets, objective_seven_set,
                        component_set
                    );
                ComponentSummary& destination =
                    thread_summaries[omp_get_thread_num()];
                for (const auto& [objective, count] : local.histogram)
                    destination.histogram[objective] += count;
                destination.verified_representatives +=
                    local.verified_representatives;
                destination.noncanonical_representatives +=
                    local.noncanonical_representatives;
                destination.nonfree_representatives +=
                    local.nonfree_representatives;
                destination.objective_mismatches += local.objective_mismatches;
                destination.missing_accepted_neighbors +=
                    local.missing_accepted_neighbors;
            } catch (const std::exception& exception) {
#pragma omp critical
                {
                    if (error.empty()) error = exception.what();
                }
            }
        }
        if (!error.empty()) throw std::runtime_error(error);

        ComponentSummary total;
        for (const ComponentSummary& source : thread_summaries) {
            for (const auto& [objective, count] : source.histogram)
                total.histogram[objective] += count;
            total.verified_representatives += source.verified_representatives;
            total.noncanonical_representatives +=
                source.noncanonical_representatives;
            total.nonfree_representatives += source.nonfree_representatives;
            total.objective_mismatches += source.objective_mismatches;
            total.missing_accepted_neighbors +=
                source.missing_accepted_neighbors;
        }
        if (total.verified_representatives != component.size() ||
            total.noncanonical_representatives ||
            total.nonfree_representatives || total.objective_mismatches ||
            total.missing_accepted_neighbors)
            throw std::runtime_error("objective-eight component verification failed");
        if (order * total.histogram[8] != 2 * 764153)
            throw std::runtime_error("objective-eight induced edge mismatch");

        int escape_level = -1;
        for (const auto& [objective, count] : total.histogram) {
            if (objective > 8 && count) {
                escape_level = objective;
                break;
            }
        }
        if (escape_level != 9)
            throw std::runtime_error("objective-eight escape mismatch");

        output << "{\n";
        output << "  \"independent_direct_recount_representative_count\": "
               << total.verified_representatives << ",\n";
        output << "  \"all_representatives_have_objective_eight\": true,\n";
        output << "  \"all_representatives_are_canonical_and_free\": true,\n";
        output << "  \"missing_objective_at_most_eight_neighbor_count\": 0,\n";
        output << "  \"objective_eight_component_is_closed\": true,\n";
        output << "  \"objective_eight_induced_edge_count\": 764153,\n";
        output << "  \"exact_one_flip_escape_level\": " << escape_level
               << ",\n";
        output << "  \"aggregate_neighbor_objective_histogram\": {";
        bool separator = false;
        for (const auto& [objective, count] : total.histogram) {
            if (separator) output << ',';
            output << "\n    \"" << objective << "\": " << order * count;
            separator = true;
        }
        output << "\n  },\n";
        output << "  \"method\": \"parallel independent direct five-set recount with full threshold-eight membership checks\",\n";
        output << "  \"openmp_max_threads\": " << omp_get_max_threads()
               << "\n}\n";
    }

    struct ObjectiveEightSummary {
        std::array<std::uint64_t, 8> incidence_by_source{};
        std::uint64_t verified_representatives = 0;
        std::uint64_t noncanonical_representatives = 0;
        std::uint64_t nonfree_representatives = 0;
        std::uint64_t objective_mismatches = 0;
        std::uint64_t missing_lower_neighbors = 0;
        std::uint64_t signature_mismatches = 0;
    };

    ObjectiveEightSummary verify_objective_eight_one(
        const State& state,
        const std::array<std::unordered_set<State, StateHash>, 7>& lower_sets,
        const std::unordered_set<State, StateHash>& objective_seven_set,
        const std::vector<int>& expected_signature
    ) const {
        ObjectiveEightSummary result;
        result.verified_representatives = 1;
        if (!(canonical(state) == state)) ++result.noncanonical_representatives;
        if (rotate(state, 1) == state) ++result.nonfree_representatives;

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
        if (monochromatic != 8) {
            ++result.objective_mismatches;
            return result;
        }

        std::array<std::uint64_t, 8> local_incidence{};
        for (int id = 0; id < edge_count; ++id) {
            const int objective = monochromatic + delta[id];
            if (objective > 7) continue;
            State neighbor = state;
            neighbor.toggle(id);
            const State key = canonical(neighbor);
            const bool present = objective == 7
                ? objective_seven_set.contains(key)
                : objective >= 2 && lower_sets[objective].contains(key);
            if (!present) {
                ++result.missing_lower_neighbors;
                continue;
            }
            ++local_incidence[objective];
        }
        for (int objective = 2; objective <= 7; ++objective) {
            result.incidence_by_source[objective] = local_incidence[objective];
            if (expected_signature.size() != 6 ||
                static_cast<std::uint64_t>(expected_signature[objective - 2]) !=
                    local_incidence[objective])
                ++result.signature_mismatches;
        }
        return result;
    }

    void write_objective_eight_frontier_json(
        const std::string& objective_eight_path,
        const std::string& objective_seven_path,
        const std::string& lower_path,
        std::ostream& output
    ) const {
        std::array<std::unordered_set<State, StateHash>, 7> lower_sets;
        for (int objective = 2; objective <= 6; ++objective) {
            const auto states = load_representatives(
                lower_path,
                "objective_" + std::to_string(objective) +
                    "_rotation_representatives"
            );
            for (const State& state : states)
                if (!lower_sets[objective].insert(state).second)
                    throw std::runtime_error("duplicate lower representative");
        }
        if (lower_sets[2].size() != 2 || lower_sets[3].size() != 17 ||
            lower_sets[4].size() != 78 || lower_sets[5].size() != 306 ||
            lower_sets[6].size() != 1183)
            throw std::runtime_error("lower-layer representative count mismatch");

        const std::vector<State> objective_seven = load_representatives(
            objective_seven_path,
            "objective_seven_component_rotation_representatives"
        );
        std::unordered_set<State, StateHash> objective_seven_set;
        for (const State& state : objective_seven)
            if (!objective_seven_set.insert(state).second)
                throw std::runtime_error("duplicate objective-seven representative");
        if (objective_seven_set.size() != 4217)
            throw std::runtime_error("objective-seven representative count mismatch");

        const std::vector<State> targets = load_representatives(
            objective_eight_path, "objective_eight_rotation_representatives"
        );
        const std::vector<std::vector<int>> signatures = load_integer_arrays(
            objective_eight_path,
            "objective_eight_incidence_signatures_2_through_7"
        );
        if (targets.size() != 13702 || targets.size() != signatures.size())
            throw std::runtime_error("objective-eight frontier count mismatch");
        std::unordered_set<State, StateHash> target_set;
        for (const State& target : targets)
            if (!target_set.insert(target).second)
                throw std::runtime_error("duplicate objective-eight representative");

        const int thread_count = omp_get_max_threads();
        std::vector<ObjectiveEightSummary> thread_summaries(thread_count);
        std::string error;
#pragma omp parallel for schedule(dynamic, 1)
        for (std::size_t index = 0; index < targets.size(); ++index) {
            try {
                const ObjectiveEightSummary local = verify_objective_eight_one(
                    targets[index], lower_sets, objective_seven_set,
                    signatures[index]
                );
                ObjectiveEightSummary& destination =
                    thread_summaries[omp_get_thread_num()];
                for (int objective = 2; objective <= 7; ++objective)
                    destination.incidence_by_source[objective] +=
                        local.incidence_by_source[objective];
                destination.verified_representatives +=
                    local.verified_representatives;
                destination.noncanonical_representatives +=
                    local.noncanonical_representatives;
                destination.nonfree_representatives +=
                    local.nonfree_representatives;
                destination.objective_mismatches += local.objective_mismatches;
                destination.missing_lower_neighbors +=
                    local.missing_lower_neighbors;
                destination.signature_mismatches += local.signature_mismatches;
            } catch (const std::exception& exception) {
#pragma omp critical
                {
                    if (error.empty()) error = exception.what();
                }
            }
        }
        if (!error.empty()) throw std::runtime_error(error);

        ObjectiveEightSummary total;
        for (const ObjectiveEightSummary& source : thread_summaries) {
            for (int objective = 2; objective <= 7; ++objective)
                total.incidence_by_source[objective] +=
                    source.incidence_by_source[objective];
            total.verified_representatives += source.verified_representatives;
            total.noncanonical_representatives +=
                source.noncanonical_representatives;
            total.nonfree_representatives += source.nonfree_representatives;
            total.objective_mismatches += source.objective_mismatches;
            total.missing_lower_neighbors += source.missing_lower_neighbors;
            total.signature_mismatches += source.signature_mismatches;
        }
        if (total.verified_representatives != targets.size() ||
            total.noncanonical_representatives ||
            total.nonfree_representatives || total.objective_mismatches ||
            total.missing_lower_neighbors || total.signature_mismatches)
            throw std::runtime_error("objective-eight frontier verification failed");

        output << "{\n";
        output << "  \"independent_direct_recount_representative_count\": "
               << total.verified_representatives << ",\n";
        output << "  \"all_representatives_have_objective_eight\": true,\n";
        output << "  \"all_representatives_are_canonical_and_free\": true,\n";
        output << "  \"missing_lower_neighbor_count\": 0,\n";
        output << "  \"incidence_signature_mismatch_count\": 0,\n";
        output << "  \"directed_incidence_by_source_objective\": {";
        for (int objective = 2; objective <= 7; ++objective) {
            if (objective != 2) output << ',';
            output << "\n    \"" << objective << "\": "
                   << order * total.incidence_by_source[objective];
        }
        output << "\n  },\n";
        output << "  \"method\": \"parallel independent direct five-set recount and fresh sublevel-seven membership check\",\n";
        output << "  \"openmp_max_threads\": " << omp_get_max_threads()
               << "\n}\n";
    }

    struct ObjectiveNineSummary {
        std::array<std::uint64_t, 9> incidence_by_source{};
        std::array<std::uint64_t, 9> outside_incidence_by_objective{};
        std::array<std::unordered_set<State, StateHash>, 9>
            outside_orbits_by_objective;
        std::uint64_t verified_representatives = 0;
        std::uint64_t noncanonical_representatives = 0;
        std::uint64_t nonfree_representatives = 0;
        std::uint64_t objective_mismatches = 0;
        std::uint64_t missing_lower_neighbors = 0;
        std::uint64_t signature_mismatches = 0;
    };

    ObjectiveNineSummary verify_objective_nine_one(
        const State& state,
        const std::array<std::unordered_set<State, StateHash>, 7>& lower_sets,
        const std::unordered_set<State, StateHash>& objective_seven_set,
        const std::unordered_set<State, StateHash>& objective_eight_set,
        const std::vector<int>& expected_signature
    ) const {
        ObjectiveNineSummary result;
        result.verified_representatives = 1;
        if (!(canonical(state) == state)) ++result.noncanonical_representatives;
        if (rotate(state, 1) == state) ++result.nonfree_representatives;

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
        if (monochromatic != 9) {
            ++result.objective_mismatches;
            return result;
        }

        std::array<std::uint64_t, 9> local_incidence{};
        for (int id = 0; id < edge_count; ++id) {
            const int objective = monochromatic + delta[id];
            if (objective > 8) continue;
            State neighbor = state;
            neighbor.toggle(id);
            const State key = canonical(neighbor);
            bool present = false;
            if (objective == 8)
                present = objective_eight_set.contains(key);
            else if (objective == 7)
                present = objective_seven_set.contains(key);
            else if (objective >= 2)
                present = lower_sets[objective].contains(key);
            if (!present) {
                ++result.missing_lower_neighbors;
                ++result.outside_incidence_by_objective[objective];
                result.outside_orbits_by_objective[objective].insert(key);
                continue;
            }
            ++local_incidence[objective];
        }
        for (int objective = 2; objective <= 8; ++objective) {
            result.incidence_by_source[objective] = local_incidence[objective];
            if (expected_signature.size() != 7 ||
                static_cast<std::uint64_t>(expected_signature[objective - 2]) !=
                    local_incidence[objective])
                ++result.signature_mismatches;
        }
        return result;
    }

    void write_objective_nine_frontier_json(
        const std::string& objective_nine_path,
        const std::string& objective_eight_path,
        const std::string& objective_seven_path,
        const std::string& lower_path,
        std::ostream& output
    ) const {
        std::array<std::unordered_set<State, StateHash>, 7> lower_sets;
        for (int objective = 2; objective <= 6; ++objective) {
            const auto states = load_representatives(
                lower_path,
                "objective_" + std::to_string(objective) +
                    "_rotation_representatives"
            );
            for (const State& state : states)
                if (!lower_sets[objective].insert(state).second)
                    throw std::runtime_error("duplicate lower representative");
        }

        const std::vector<State> objective_seven = load_representatives(
            objective_seven_path,
            "objective_seven_component_rotation_representatives"
        );
        std::unordered_set<State, StateHash> objective_seven_set;
        for (const State& state : objective_seven)
            if (!objective_seven_set.insert(state).second)
                throw std::runtime_error("duplicate objective-seven representative");
        if (objective_seven_set.size() != 4217)
            throw std::runtime_error("objective-seven representative count mismatch");

        const std::vector<State> objective_eight = load_representatives(
            objective_eight_path,
            "objective_eight_component_rotation_representatives"
        );
        std::unordered_set<State, StateHash> objective_eight_set;
        for (const State& state : objective_eight)
            if (!objective_eight_set.insert(state).second)
                throw std::runtime_error("duplicate objective-eight representative");
        if (objective_eight_set.size() != 13738)
            throw std::runtime_error("objective-eight representative count mismatch");

        const std::vector<State> targets = load_representatives(
            objective_nine_path, "objective_nine_rotation_representatives"
        );
        const std::vector<std::vector<int>> signatures = load_integer_arrays(
            objective_nine_path,
            "objective_nine_incidence_signatures_2_through_8"
        );
        if (targets.size() != 42661 || targets.size() != signatures.size())
            throw std::runtime_error("objective-nine frontier count mismatch");
        std::unordered_set<State, StateHash> target_set;
        for (const State& target : targets)
            if (!target_set.insert(target).second)
                throw std::runtime_error("duplicate objective-nine representative");

        const int thread_count = omp_get_max_threads();
        std::vector<ObjectiveNineSummary> thread_summaries(thread_count);
        std::string error;
#pragma omp parallel for schedule(dynamic, 1)
        for (std::size_t index = 0; index < targets.size(); ++index) {
            try {
                const ObjectiveNineSummary local = verify_objective_nine_one(
                    targets[index], lower_sets, objective_seven_set,
                    objective_eight_set, signatures[index]
                );
                ObjectiveNineSummary& destination =
                    thread_summaries[omp_get_thread_num()];
                for (int objective = 2; objective <= 8; ++objective)
                    destination.incidence_by_source[objective] +=
                        local.incidence_by_source[objective];
                for (int objective = 2; objective <= 8; ++objective) {
                    destination.outside_incidence_by_objective[objective] +=
                        local.outside_incidence_by_objective[objective];
                    destination.outside_orbits_by_objective[objective].insert(
                        local.outside_orbits_by_objective[objective].begin(),
                        local.outside_orbits_by_objective[objective].end()
                    );
                }
                destination.verified_representatives +=
                    local.verified_representatives;
                destination.noncanonical_representatives +=
                    local.noncanonical_representatives;
                destination.nonfree_representatives +=
                    local.nonfree_representatives;
                destination.objective_mismatches += local.objective_mismatches;
                destination.missing_lower_neighbors +=
                    local.missing_lower_neighbors;
                destination.signature_mismatches += local.signature_mismatches;
            } catch (const std::exception& exception) {
#pragma omp critical
                {
                    if (error.empty()) error = exception.what();
                }
            }
        }
        if (!error.empty()) throw std::runtime_error(error);

        ObjectiveNineSummary total;
        for (const ObjectiveNineSummary& source : thread_summaries) {
            for (int objective = 2; objective <= 8; ++objective)
                total.incidence_by_source[objective] +=
                    source.incidence_by_source[objective];
            for (int objective = 2; objective <= 8; ++objective) {
                total.outside_incidence_by_objective[objective] +=
                    source.outside_incidence_by_objective[objective];
                total.outside_orbits_by_objective[objective].insert(
                    source.outside_orbits_by_objective[objective].begin(),
                    source.outside_orbits_by_objective[objective].end()
                );
            }
            total.verified_representatives += source.verified_representatives;
            total.noncanonical_representatives +=
                source.noncanonical_representatives;
            total.nonfree_representatives += source.nonfree_representatives;
            total.objective_mismatches += source.objective_mismatches;
            total.missing_lower_neighbors += source.missing_lower_neighbors;
            total.signature_mismatches += source.signature_mismatches;
        }
        if (total.verified_representatives != targets.size() ||
            total.noncanonical_representatives ||
            total.nonfree_representatives || total.objective_mismatches ||
            total.signature_mismatches)
            throw std::runtime_error(
                "objective-nine frontier verification failed: verified=" +
                std::to_string(total.verified_representatives) +
                " noncanonical=" +
                std::to_string(total.noncanonical_representatives) +
                " nonfree=" + std::to_string(total.nonfree_representatives) +
                " objective_mismatches=" +
                std::to_string(total.objective_mismatches) +
                " missing_lower=" +
                std::to_string(total.missing_lower_neighbors) +
                " signature_mismatches=" +
                std::to_string(total.signature_mismatches)
            );

        output << "{\n";
        output << "  \"independent_direct_recount_representative_count\": "
               << total.verified_representatives << ",\n";
        output << "  \"all_representatives_have_objective_nine\": true,\n";
        output << "  \"all_representatives_are_canonical_and_free\": true,\n";
        output << "  \"out_of_component_lower_neighbor_representative_incidence_count\": "
               << total.missing_lower_neighbors << ",\n";
        output << "  \"out_of_component_lower_neighbor_full_incidence_count\": "
               << order * total.missing_lower_neighbors << ",\n";
        output << "  \"out_of_component_lower_neighbor_incidence_by_objective\": {";
        bool outside_separator = false;
        for (int objective = 2; objective <= 8; ++objective) {
            if (!total.outside_incidence_by_objective[objective]) continue;
            if (outside_separator) output << ',';
            output << "\n    \"" << objective << "\": "
                   << order * total.outside_incidence_by_objective[objective];
            outside_separator = true;
        }
        output << "\n  },\n";
        output << "  \"out_of_component_lower_neighbor_rotation_orbits_by_objective\": {";
        outside_separator = false;
        for (int objective = 2; objective <= 8; ++objective) {
            if (total.outside_orbits_by_objective[objective].empty()) continue;
            if (outside_separator) output << ',';
            output << "\n    \"" << objective << "\": "
                   << total.outside_orbits_by_objective[objective].size();
            outside_separator = true;
        }
        output << "\n  },\n";
        std::vector<State> outside_objective_eight(
            total.outside_orbits_by_objective[8].begin(),
            total.outside_orbits_by_objective[8].end()
        );
        std::sort(outside_objective_eight.begin(), outside_objective_eight.end());
        for (const State& state : outside_objective_eight)
            if (rotate(state, 1) == state)
                throw std::runtime_error("nonfree external objective-eight orbit");
        output << "  \"out_of_component_objective_eight_rotation_representatives\": [\n";
        for (std::size_t index = 0; index < outside_objective_eight.size(); ++index) {
            if (index) output << ",\n";
            output << "    ";
            write_state(output, outside_objective_eight[index]);
        }
        output << "\n  ],\n";
        output << "  \"incidence_signature_mismatch_count\": 0,\n";
        output << "  \"directed_incidence_by_source_objective\": {";
        for (int objective = 2; objective <= 8; ++objective) {
            if (objective != 2) output << ',';
            output << "\n    \"" << objective << "\": "
                   << order * total.incidence_by_source[objective];
        }
        output << "\n  },\n";
        output << "  \"method\": \"parallel independent direct five-set recount and fresh sublevel-eight membership check\",\n";
        output << "  \"openmp_max_threads\": " << omp_get_max_threads()
               << "\n}\n";
    }

    struct ObjectiveNineComponentSummary {
        std::array<std::map<int, std::uint64_t>, 10> histograms;
        std::vector<std::uint32_t> new_neighbor_indices;
        std::uint64_t verified_representatives = 0;
        std::uint64_t noncanonical_representatives = 0;
        std::uint64_t nonfree_representatives = 0;
        std::uint64_t objective_mismatches = 0;
        std::uint64_t missing_accepted_neighbors = 0;
        std::uint64_t new_internal_directed = 0;
        std::uint64_t new_to_primary_directed = 0;
        int escape_level = -1;
    };

    ObjectiveNineComponentSummary verify_objective_nine_component_one(
        int expected_objective,
        const State& state,
        const std::array<std::unordered_set<State, StateHash>, 10>& primary_sets,
        const std::array<
            std::unordered_map<State, std::uint32_t, StateHash>, 10
        >& new_indices
    ) const {
        ObjectiveNineComponentSummary result;
        result.verified_representatives = 1;
        if (!(canonical(state) == state)) ++result.noncanonical_representatives;
        if (rotate(state, 1) == state) ++result.nonfree_representatives;

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
        if (monochromatic != expected_objective) {
            ++result.objective_mismatches;
            return result;
        }

        for (int id = 0; id < edge_count; ++id) {
            const int target_objective = monochromatic + delta[id];
            ++result.histograms[expected_objective][target_objective];
            if (target_objective > 9) {
                if (result.escape_level < 0 ||
                    target_objective < result.escape_level)
                    result.escape_level = target_objective;
                continue;
            }
            if (target_objective < 0)
                throw std::runtime_error("negative target objective");
            State neighbor = state;
            neighbor.toggle(id);
            const State key = canonical(neighbor);
            const auto new_neighbor = new_indices[target_objective].find(key);
            if (new_neighbor != new_indices[target_objective].end()) {
                ++result.new_internal_directed;
                result.new_neighbor_indices.push_back(new_neighbor->second);
            } else if (primary_sets[target_objective].contains(key))
                ++result.new_to_primary_directed;
            else
                ++result.missing_accepted_neighbors;
        }
        return result;
    }

    void write_objective_nine_component_json(
        const std::string& component_path,
        const std::string& frontier_path,
        const std::string& objective_eight_path,
        const std::string& objective_seven_path,
        const std::string& lower_path,
        std::ostream& output
    ) const {
        std::array<std::unordered_set<State, StateHash>, 10> primary_sets;
        for (int objective = 2; objective <= 6; ++objective) {
            const auto states = load_representatives(
                lower_path,
                "objective_" + std::to_string(objective) +
                    "_rotation_representatives"
            );
            for (const State& state : states)
                if (!primary_sets[objective].insert(state).second)
                    throw std::runtime_error("duplicate primary lower representative");
        }
        for (const State& state : load_representatives(
                 objective_seven_path,
                 "objective_seven_component_rotation_representatives"
             ))
            if (!primary_sets[7].insert(state).second)
                throw std::runtime_error("duplicate primary objective-seven representative");
        for (const State& state : load_representatives(
                 objective_eight_path,
                 "objective_eight_component_rotation_representatives"
             ))
            if (!primary_sets[8].insert(state).second)
                throw std::runtime_error("duplicate primary objective-eight representative");
        const std::array<std::size_t, 9> expected_primary_counts = {
            0, 0, 2, 17, 78, 306, 1183, 4217, 13738
        };
        for (int objective = 2; objective <= 8; ++objective)
            if (primary_sets[objective].size() != expected_primary_counts[objective])
                throw std::runtime_error("primary layer representative count mismatch");

        std::array<std::unordered_set<State, StateHash>, 10> new_sets;
        std::vector<std::pair<int, State>> new_states;
        for (int objective = 7; objective <= 9; ++objective) {
            const auto states = load_representatives(
                component_path,
                "new_objective_" + std::to_string(objective) +
                    "_rotation_representatives"
            );
            for (const State& state : states) {
                if (!new_sets[objective].insert(state).second)
                    throw std::runtime_error("duplicate new representative");
                if (primary_sets[objective].contains(state))
                    throw std::runtime_error("new representative is already primary");
                new_states.push_back({objective, state});
            }
        }
        if (new_sets[7].size() != 1 || new_sets[8].size() != 33 ||
            new_sets[9].size() != 42781 || new_states.size() != 42815)
            throw std::runtime_error("new threshold-nine layer count mismatch");

        std::array<
            std::unordered_map<State, std::uint32_t, StateHash>, 10
        > new_indices;
        for (std::size_t index = 0; index < new_states.size(); ++index) {
            const auto& [objective, state] = new_states[index];
            if (!new_indices[objective]
                     .emplace(state, static_cast<std::uint32_t>(index))
                     .second)
                throw std::runtime_error("duplicate indexed new representative");
        }

        const std::vector<State> first_frontier = load_representatives(
            frontier_path, "objective_nine_rotation_representatives"
        );
        if (first_frontier.size() != 42661)
            throw std::runtime_error("objective-nine first frontier count mismatch");
        for (const State& state : first_frontier)
            if (!new_sets[9].contains(state))
                throw std::runtime_error("first-frontier state missing from closure");

        const int thread_count = omp_get_max_threads();
        std::vector<ObjectiveNineComponentSummary> thread_summaries(thread_count);
        std::vector<std::vector<std::uint32_t>> new_adjacency(new_states.size());
        std::string error;
#pragma omp parallel for schedule(dynamic, 1)
        for (std::size_t index = 0; index < new_states.size(); ++index) {
            try {
                const auto& [objective, state] = new_states[index];
                ObjectiveNineComponentSummary local =
                    verify_objective_nine_component_one(
                        objective, state, primary_sets, new_indices
                    );
                ObjectiveNineComponentSummary& destination =
                    thread_summaries[omp_get_thread_num()];
                for (int source = 0; source <= 9; ++source)
                    for (const auto& [target, count] : local.histograms[source])
                        destination.histograms[source][target] += count;
                destination.verified_representatives +=
                    local.verified_representatives;
                destination.noncanonical_representatives +=
                    local.noncanonical_representatives;
                destination.nonfree_representatives +=
                    local.nonfree_representatives;
                destination.objective_mismatches += local.objective_mismatches;
                destination.missing_accepted_neighbors +=
                    local.missing_accepted_neighbors;
                destination.new_internal_directed +=
                    local.new_internal_directed;
                destination.new_to_primary_directed +=
                    local.new_to_primary_directed;
                if (local.escape_level >= 0 &&
                    (destination.escape_level < 0 ||
                     local.escape_level < destination.escape_level))
                    destination.escape_level = local.escape_level;
                new_adjacency[index] = std::move(local.new_neighbor_indices);
            } catch (const std::exception& exception) {
#pragma omp critical
                {
                    if (error.empty()) error = exception.what();
                }
            }
        }
        if (!error.empty()) throw std::runtime_error(error);

        ObjectiveNineComponentSummary total;
        for (const ObjectiveNineComponentSummary& source_summary : thread_summaries) {
            for (int source = 0; source <= 9; ++source)
                for (const auto& [target, count] : source_summary.histograms[source])
                    total.histograms[source][target] += count;
            total.verified_representatives +=
                source_summary.verified_representatives;
            total.noncanonical_representatives +=
                source_summary.noncanonical_representatives;
            total.nonfree_representatives +=
                source_summary.nonfree_representatives;
            total.objective_mismatches += source_summary.objective_mismatches;
            total.missing_accepted_neighbors +=
                source_summary.missing_accepted_neighbors;
            total.new_internal_directed +=
                source_summary.new_internal_directed;
            total.new_to_primary_directed +=
                source_summary.new_to_primary_directed;
            if (source_summary.escape_level >= 0 &&
                (total.escape_level < 0 ||
                 source_summary.escape_level < total.escape_level))
                total.escape_level = source_summary.escape_level;
        }
        if (total.verified_representatives != new_states.size() ||
            total.noncanonical_representatives || total.nonfree_representatives ||
            total.objective_mismatches || total.missing_accepted_neighbors)
            throw std::runtime_error("objective-nine component verification failed");
        const std::uint64_t internal_edges =
            order * total.new_internal_directed / 2;
        const std::uint64_t to_primary_edges =
            order * total.new_to_primary_directed;
        if (order * total.new_internal_directed % 2 ||
            internal_edges != 2514167 || to_primary_edges != 6603854 ||
            total.escape_level != 10)
            throw std::runtime_error("objective-nine component aggregate mismatch");

        std::vector<int> frontier_distance(new_states.size(), -1);
        std::vector<std::uint32_t> reachability_queue;
        reachability_queue.reserve(new_states.size());
        for (const State& state : first_frontier) {
            const auto found = new_indices[9].find(state);
            if (found == new_indices[9].end())
                throw std::runtime_error("indexed first-frontier state missing");
            if (frontier_distance[found->second] < 0) {
                frontier_distance[found->second] = 0;
                reachability_queue.push_back(found->second);
            }
        }
        for (std::size_t position = 0; position < reachability_queue.size();
             ++position) {
            const std::uint32_t source = reachability_queue[position];
            for (const std::uint32_t target : new_adjacency[source]) {
                if (frontier_distance[target] >= 0) continue;
                frontier_distance[target] = frontier_distance[source] + 1;
                reachability_queue.push_back(target);
            }
        }
        if (reachability_queue.size() != new_states.size())
            throw std::runtime_error(
                "new threshold-nine state is unreachable from first frontier"
            );
        std::map<int, std::uint64_t> reachability_distance_histogram;
        for (const int distance : frontier_distance) {
            if (distance < 0)
                throw std::runtime_error("negative final frontier distance");
            ++reachability_distance_histogram[distance];
        }
        const int maximum_frontier_distance =
            reachability_distance_histogram.rbegin()->first;

        output << "{\n";
        output << "  \"independent_direct_recount_representative_count\": "
               << total.verified_representatives << ",\n";
        output << "  \"all_representatives_have_claimed_objective\": true,\n";
        output << "  \"all_representatives_are_canonical_and_free\": true,\n";
        output << "  \"first_objective_nine_frontier_is_contained\": true,\n";
        output << "  \"all_new_rotation_orbits_reachable_from_first_frontier\": true,\n";
        output << "  \"independent_reachable_rotation_orbit_count\": "
               << reachability_queue.size() << ",\n";
        output << "  \"unreachable_rotation_orbit_count\": 0,\n";
        output << "  \"maximum_quotient_distance_from_first_frontier\": "
               << maximum_frontier_distance << ",\n";
        output << "  \"quotient_distance_from_first_frontier_histogram\": {";
        bool distance_separator = false;
        for (const auto& [distance, count] : reachability_distance_histogram) {
            if (distance_separator) output << ',';
            output << "\n    \"" << distance << "\": " << count;
            distance_separator = true;
        }
        output << "\n  },\n";
        output << "  \"missing_objective_at_most_nine_neighbor_count\": 0,\n";
        output << "  \"complete_threshold_nine_new_rotation_orbit_count\": "
               << new_states.size() << ",\n";
        output << "  \"new_rotation_orbit_count_by_objective\": {\n"
               << "    \"7\": " << new_sets[7].size() << ",\n"
               << "    \"8\": " << new_sets[8].size() << ",\n"
               << "    \"9\": " << new_sets[9].size() << "\n  },\n";
        output << "  \"new_to_primary_sublevel_eight_directed_edge_count\": "
               << to_primary_edges << ",\n";
        output << "  \"new_threshold_nine_internal_edge_count\": "
               << internal_edges << ",\n";
        output << "  \"complete_sublevel_nine_component_vertex_count\": "
               << 840263 + order * new_states.size() << ",\n";
        output << "  \"complete_sublevel_nine_component_edge_count\": "
               << 3676586 + to_primary_edges + internal_edges << ",\n";
        output << "  \"exact_one_flip_escape_level\": " << total.escape_level
               << ",\n";
        output << "  \"aggregate_neighbor_objective_histogram_by_source_objective\": {";
        bool source_separator = false;
        for (int source = 0; source <= 9; ++source) {
            if (total.histograms[source].empty()) continue;
            if (source_separator) output << ',';
            output << "\n    \"" << source << "\": {";
            bool target_separator = false;
            for (const auto& [target, count] : total.histograms[source]) {
                if (target_separator) output << ',';
                output << "\n      \"" << target << "\": "
                       << order * count;
                target_separator = true;
            }
            output << "\n    }";
            source_separator = true;
        }
        output << "\n  },\n";
        output << "  \"method\": \"parallel independent direct five-set recount with fresh per-representative deltas, full threshold-nine membership checks, and explicit quotient BFS from the first frontier\",\n";
        output << "  \"openmp_max_threads\": " << omp_get_max_threads()
               << "\n}\n";
    }
};

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 3 && argc != 5 && argc != 6 && argc != 7 && argc != 8 &&
        argc != 9) {
        std::cerr << "usage: verify_objective_six_component CERTIFICATE.json "
                     "objective-six-component-representatives.json "
                     "[--objective-seven-frontier FRONTIER.json | "
                     "--objective-seven-component COMPONENT.json "
                     "LOWER-REPRESENTATIVES.json | "
                     "--objective-eight-frontier OBJECTIVE-EIGHT.json "
                     "OBJECTIVE-SEVEN.json LOWER-REPRESENTATIVES.json | "
                     "--objective-eight-component COMPONENT.json "
                     "OBJECTIVE-SEVEN.json LOWER-REPRESENTATIVES.json | "
                     "--objective-nine-frontier OBJECTIVE-NINE.json "
                     "OBJECTIVE-EIGHT.json OBJECTIVE-SEVEN.json "
                     "LOWER-REPRESENTATIVES.json | "
                     "--objective-nine-component COMPONENT.json "
                     "OBJECTIVE-NINE-FRONTIER.json OBJECTIVE-EIGHT.json "
                     "OBJECTIVE-SEVEN.json LOWER-REPRESENTATIVES.json]\n";
        return 2;
    }
    Verifier verifier(
        load_flips(argv[1]),
        load_representatives(
            argv[2], "objective_six_rotation_representatives"
        )
    );
    if (argc == 3) {
        verifier.write_json(std::cout);
    } else if (argc == 5) {
        if (std::string(argv[3]) != "--objective-seven-frontier")
            throw std::runtime_error("expected --objective-seven-frontier");
        verifier.write_frontier_json(argv[4], std::cout);
    } else if (argc == 6) {
        if (std::string(argv[3]) != "--objective-seven-component")
            throw std::runtime_error("expected --objective-seven-component");
        verifier.write_component_json(argv[4], argv[5], std::cout);
    } else if (argc == 7) {
        const std::string option = argv[3];
        if (option == "--objective-eight-frontier")
            verifier.write_objective_eight_frontier_json(
                argv[4], argv[5], argv[6], std::cout
            );
        else if (option == "--objective-eight-component")
            verifier.write_objective_eight_component_json(
                argv[4], argv[5], argv[6], std::cout
            );
        else
            throw std::runtime_error("unexpected verification mode");
    } else if (argc == 8) {
        if (std::string(argv[3]) != "--objective-nine-frontier")
            throw std::runtime_error("expected --objective-nine-frontier");
        verifier.write_objective_nine_frontier_json(
            argv[4], argv[5], argv[6], argv[7], std::cout
        );
    } else {
        if (std::string(argv[3]) != "--objective-nine-component")
            throw std::runtime_error("expected --objective-nine-component");
        verifier.write_objective_nine_component_json(
            argv[4], argv[5], argv[6], argv[7], argv[8], std::cout
        );
    }
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
