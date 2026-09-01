#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
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
        std::uint64_t hash = 0xd6e8feb86659fd93ULL;
        for (std::uint64_t word : state.words) {
            word ^= word >> 32;
            word *= 0xd6e8feb86659fd93ULL;
            word ^= word >> 32;
            hash ^= word + 0x9e3779b97f4a7c15ULL + (hash << 6) +
                    (hash >> 2);
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
    if (nesting != 0)
        throw std::runtime_error("unterminated JSON array " + key);
    return text.substr(begin, end - begin);
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
             jt != integer_last; ++jt)
            values.push_back(std::stoi((*jt)[1]));
        result.push_back(std::move(values));
    }
    return result;
}

std::vector<State> load_states(
    const std::string& path, const std::string& key
) {
    std::vector<State> result;
    for (const std::vector<int>& edges : load_integer_arrays(path, key)) {
        State state;
        for (int id : edges) {
            if (id < 0 || id >= edge_count || state.contains(id))
                throw std::runtime_error("invalid state edge in " + key);
            state.toggle(id);
        }
        result.push_back(state);
    }
    if (result.empty()) throw std::runtime_error("empty state array " + key);
    return result;
}

void write_state(std::ostream& output, const State& state) {
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

struct Model {
    std::array<std::array<int, order>, order> edge_id{};
    std::array<std::pair<int, int>, edge_count> edge_vertices{};
    std::array<std::array<std::uint16_t, edge_count>, order> rotated_edge{};
    std::array<bool, edge_count> seed_red{};
    std::vector<FiveSet> five_sets;

    Model() {
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
        if (next_edge != edge_count) throw std::logic_error("edge count");

        for (int offset = 0; offset < order; ++offset) {
            for (int id = 0; id < edge_count; ++id) {
                auto [a, b] = edge_vertices[id];
                a = (a + offset) % order;
                b = (b + offset) % order;
                rotated_edge[offset][id] =
                    static_cast<std::uint16_t>(edge_id[a][b]);
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
                                    five.edges[position++] =
                                        static_cast<std::uint16_t>(
                                            edge_id[vertices[i]][vertices[j]]
                                        );
                            five_sets.push_back(five);
                        }
        if (five_sets.size() != 962598)
            throw std::logic_error("five-set count");
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
            const State candidate = rotate(source, offset);
            if (candidate < best) best = candidate;
        }
        return best;
    }

    bool is_free(const State& state) const {
        return !(rotate(state, 1) == state);
    }

    struct Analysis {
        int objective = 0;
        std::array<int, edge_count> delta{};
    };

    Analysis analyze(const State& state) const {
        std::array<bool, edge_count> red{};
        for (int id = 0; id < edge_count; ++id)
            red[id] = seed_red[id] != state.contains(id);

        Analysis result;
        for (const FiveSet& five : five_sets) {
            int red_edges = 0;
            for (int id : five.edges) red_edges += red[id];
            if (red_edges == 0 || red_edges == 10) {
                ++result.objective;
                for (int id : five.edges) --result.delta[id];
            } else if (red_edges == 1) {
                for (int id : five.edges) {
                    if (red[id]) {
                        ++result.delta[id];
                        break;
                    }
                }
            } else if (red_edges == 9) {
                for (int id : five.edges) {
                    if (!red[id]) {
                        ++result.delta[id];
                        break;
                    }
                }
            }
        }
        return result;
    }
};

struct SourceEntry {
    int objective = 0;
    State state;
};

struct Counters {
    std::array<std::uint64_t, 10> incidence{};
    std::map<int, std::uint64_t> target_neighbor_objective_histogram;
    std::uint64_t verified = 0;
    std::uint64_t objective_mismatch = 0;
    std::uint64_t noncanonical = 0;
    std::uint64_t nonfree = 0;
    std::uint64_t missing_frontier = 0;
    std::uint64_t signature_mismatch = 0;
};

struct ExpansionSummary {
    std::array<std::unordered_set<State, StateHash>, 11> new_orbits;
    std::uint64_t internal_objective_ten_directed_incidence = 0;
    std::uint64_t internal_objective_ten_distinct_directed_pairs = 0;
    std::uint64_t internal_objective_ten_self_orbit_pairs = 0;
    std::uint64_t nonfree_new_orbits = 0;
};

void add(Counters& destination, const Counters& source) {
    for (int objective = 2; objective <= 9; ++objective)
        destination.incidence[objective] += source.incidence[objective];
    for (const auto& [objective, count] :
         source.target_neighbor_objective_histogram)
        destination.target_neighbor_objective_histogram[objective] += count;
    destination.verified += source.verified;
    destination.objective_mismatch += source.objective_mismatch;
    destination.noncanonical += source.noncanonical;
    destination.nonfree += source.nonfree;
    destination.missing_frontier += source.missing_frontier;
    destination.signature_mismatch += source.signature_mismatch;
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 6) {
        std::cerr
            << "usage: verify_objective_ten_frontier LOWER-SIX.json "
               "OBJECTIVE-SEVEN-COMPONENT.json OBJECTIVE-EIGHT-COMPONENT.json "
               "OBJECTIVE-NINE-COMPONENT.json OBJECTIVE-TEN-FRONTIER.json\n";
        return 2;
    }

    Model model;
    std::array<std::unordered_set<State, StateHash>, 10> source_sets;
    std::vector<SourceEntry> sources;
    std::unordered_map<State, std::size_t, StateHash> source_index;
    source_index.reserve(130000);
    auto add_source_layer = [&](int objective, const std::vector<State>& states) {
        for (const State& state : states) {
            if (!(model.canonical(state) == state) || !model.is_free(state))
                throw std::runtime_error("noncanonical or nonfree source");
            if (!source_sets[objective].insert(state).second)
                throw std::runtime_error("duplicate source representative");
            if (!source_index.emplace(state, sources.size()).second)
                throw std::runtime_error(
                    "source representative occurs in multiple layers"
                );
            sources.push_back({objective, state});
        }
    };

    for (int objective = 2; objective <= 6; ++objective)
        add_source_layer(
            objective,
            load_states(
                argv[1], "objective_" + std::to_string(objective) +
                             "_rotation_representatives"
            )
        );
    add_source_layer(
        7,
        load_states(argv[2], "objective_seven_component_rotation_representatives")
    );
    add_source_layer(
        8,
        load_states(argv[3], "objective_eight_component_rotation_representatives")
    );
    add_source_layer(
        7, load_states(argv[4], "new_objective_7_rotation_representatives")
    );
    add_source_layer(
        8, load_states(argv[4], "new_objective_8_rotation_representatives")
    );
    add_source_layer(
        9, load_states(argv[4], "new_objective_9_rotation_representatives")
    );

    const std::array<std::size_t, 10> expected_source_counts = {
        0, 0, 2, 17, 78, 306, 1183, 4218, 13771, 42781
    };
    for (int objective = 2; objective <= 9; ++objective)
        if (source_sets[objective].size() != expected_source_counts[objective])
            throw std::runtime_error(
                "source layer count mismatch at objective " +
                std::to_string(objective)
            );
    if (sources.size() != 62356)
        throw std::runtime_error("complete source count mismatch");

    const std::vector<State> targets = load_states(
        argv[5], "objective_ten_rotation_representatives"
    );
    const std::vector<std::vector<int>> signatures = load_integer_arrays(
        argv[5], "objective_ten_incidence_signatures_2_through_9"
    );
    if (targets.size() != 128184 || signatures.size() != targets.size())
        throw std::runtime_error("objective-ten frontier count mismatch");
    std::unordered_map<State, std::size_t, StateHash> target_index;
    target_index.reserve(2 * targets.size());
    for (std::size_t index = 0; index < targets.size(); ++index)
        if (!target_index.emplace(targets[index], index).second)
            throw std::runtime_error("duplicate objective-ten representative");

    const int thread_count = omp_get_max_threads();
    std::vector<Counters> target_thread_counters(thread_count);
    std::vector<ExpansionSummary> target_thread_expansions(thread_count);
    std::vector<std::array<std::uint16_t, 10>> recounted_signatures(
        targets.size()
    );
    std::vector<std::uint16_t> target_distinct_source_orbit_degrees(
        targets.size()
    );
    std::vector<std::uint16_t> target_parallel_incidence_excess(targets.size());
    std::vector<std::uint16_t> target_max_source_orbit_multiplicity(
        targets.size()
    );
    std::vector<std::uint16_t> target_objective_ten_move_counts(targets.size());
    std::vector<std::uint16_t> target_minimum_above_ten_objectives(
        targets.size()
    );
    std::string error;
#pragma omp parallel for schedule(dynamic, 1)
    for (std::size_t index = 0; index < targets.size(); ++index) {
        try {
            Counters local;
            local.verified = 1;
            const State& target = targets[index];
            if (!(model.canonical(target) == target)) ++local.noncanonical;
            if (!model.is_free(target)) ++local.nonfree;
            const Model::Analysis analysis = model.analyze(target);
            if (analysis.objective != 10) {
                ++local.objective_mismatch;
            } else {
                std::unordered_map<std::size_t, std::uint16_t>
                    source_orbit_multiplicity;
                std::unordered_set<std::size_t> internal_objective_ten_neighbors;
                int objective_ten_move_count = 0;
                int minimum_above_ten_objective =
                    std::numeric_limits<int>::max();
                for (int id = 0; id < edge_count; ++id) {
                    const int objective = analysis.objective + analysis.delta[id];
                    ++local.target_neighbor_objective_histogram[objective];
                    if (objective == 10) ++objective_ten_move_count;
                    if (objective > 10)
                        minimum_above_ten_objective = std::min(
                            minimum_above_ten_objective, objective
                        );
                    if (objective < 2 || objective > 10) continue;
                    State neighbor = target;
                    neighbor.toggle(id);
                    const State key = model.canonical(neighbor);
                    ExpansionSummary& expansion =
                        target_thread_expansions[omp_get_thread_num()];
                    if (objective == 10) {
                        const auto internal_target = target_index.find(key);
                        if (internal_target != target_index.end()) {
                            ++expansion.internal_objective_ten_directed_incidence;
                            internal_objective_ten_neighbors.insert(
                                internal_target->second
                            );
                        } else {
                            if (!model.is_free(key))
                                ++expansion.nonfree_new_orbits;
                            expansion.new_orbits[10].insert(key);
                        }
                        continue;
                    }
                    if (!source_sets[objective].contains(key)) {
                        if (!model.is_free(key))
                            ++expansion.nonfree_new_orbits;
                        expansion.new_orbits[objective].insert(key);
                        continue;
                    }
                    const auto source_it = source_index.find(key);
                    if (source_it == source_index.end() ||
                        sources[source_it->second].objective != objective)
                        throw std::runtime_error(
                            "source index disagrees with objective layer"
                        );
                    ++source_orbit_multiplicity[source_it->second];
                    ++local.incidence[objective];
                    ++recounted_signatures[index][objective];
                }
                ExpansionSummary& expansion =
                    target_thread_expansions[omp_get_thread_num()];
                expansion.internal_objective_ten_distinct_directed_pairs +=
                    internal_objective_ten_neighbors.size();
                if (internal_objective_ten_neighbors.contains(index))
                    ++expansion.internal_objective_ten_self_orbit_pairs;
                target_distinct_source_orbit_degrees[index] =
                    static_cast<std::uint16_t>(source_orbit_multiplicity.size());
                std::uint16_t incidence_degree = 0;
                std::uint16_t maximum_multiplicity = 0;
                for (const auto& [source_index, multiplicity] :
                     source_orbit_multiplicity) {
                    (void)source_index;
                    incidence_degree += multiplicity;
                    maximum_multiplicity =
                        std::max(maximum_multiplicity, multiplicity);
                }
                target_parallel_incidence_excess[index] =
                    incidence_degree - source_orbit_multiplicity.size();
                target_max_source_orbit_multiplicity[index] =
                    maximum_multiplicity;
                target_objective_ten_move_counts[index] =
                    static_cast<std::uint16_t>(objective_ten_move_count);
                if (minimum_above_ten_objective ==
                    std::numeric_limits<int>::max())
                    throw std::runtime_error(
                        "objective-ten target has no higher-objective neighbor"
                    );
                target_minimum_above_ten_objectives[index] =
                    static_cast<std::uint16_t>(minimum_above_ten_objective);
                if (signatures[index].size() != 8) {
                    ++local.signature_mismatch;
                } else {
                    for (int objective = 2; objective <= 9; ++objective)
                        if (recounted_signatures[index][objective] !=
                            signatures[index][objective - 2])
                            ++local.signature_mismatch;
                }
            }
            add(target_thread_counters[omp_get_thread_num()], local);
        } catch (const std::exception& exception) {
#pragma omp critical
            {
                if (error.empty()) error = exception.what();
            }
        }
    }
    if (!error.empty()) throw std::runtime_error(error);

    Counters target_total;
    for (const Counters& counters : target_thread_counters)
        add(target_total, counters);
    if (target_total.verified != targets.size() ||
        target_total.objective_mismatch || target_total.noncanonical ||
        target_total.nonfree || target_total.signature_mismatch)
        throw std::runtime_error("objective-ten target verification failed");

    ExpansionSummary expansion_total;
    for (const ExpansionSummary& expansion : target_thread_expansions) {
        expansion_total.internal_objective_ten_directed_incidence +=
            expansion.internal_objective_ten_directed_incidence;
        expansion_total.internal_objective_ten_distinct_directed_pairs +=
            expansion.internal_objective_ten_distinct_directed_pairs;
        expansion_total.internal_objective_ten_self_orbit_pairs +=
            expansion.internal_objective_ten_self_orbit_pairs;
        expansion_total.nonfree_new_orbits += expansion.nonfree_new_orbits;
        for (int objective = 0; objective <= 10; ++objective)
            expansion_total.new_orbits[objective].insert(
                expansion.new_orbits[objective].begin(),
                expansion.new_orbits[objective].end()
            );
    }
    if (expansion_total.nonfree_new_orbits)
        throw std::runtime_error("nonfree newly exposed orbit");

    std::vector<Counters> source_thread_counters(thread_count);
    std::vector<std::uint16_t> source_distinct_target_orbit_degrees(
        sources.size()
    );
    std::vector<std::uint16_t> source_minimum_external_objectives(
        sources.size()
    );
#pragma omp parallel for schedule(dynamic, 1)
    for (std::size_t index = 0; index < sources.size(); ++index) {
        try {
            Counters local;
            local.verified = 1;
            const SourceEntry& source = sources[index];
            const Model::Analysis analysis = model.analyze(source.state);
            if (analysis.objective != source.objective) {
                ++local.objective_mismatch;
            } else {
                std::unordered_set<std::size_t> distinct_target_orbits;
                int minimum_external_objective =
                    std::numeric_limits<int>::max();
                for (int id = 0; id < edge_count; ++id) {
                    const int neighbor_objective =
                        analysis.objective + analysis.delta[id];
                    if (neighbor_objective > 9)
                        minimum_external_objective = std::min(
                            minimum_external_objective, neighbor_objective
                        );
                    if (neighbor_objective != 10) continue;
                    State neighbor = source.state;
                    neighbor.toggle(id);
                    const State key = model.canonical(neighbor);
                    const auto target_it = target_index.find(key);
                    if (target_it == target_index.end()) {
                        ++local.missing_frontier;
                        continue;
                    }
                    distinct_target_orbits.insert(target_it->second);
                    ++local.incidence[source.objective];
                }
                source_distinct_target_orbit_degrees[index] =
                    static_cast<std::uint16_t>(distinct_target_orbits.size());
                if (minimum_external_objective ==
                    std::numeric_limits<int>::max())
                    throw std::runtime_error(
                        "source has no external one-flip neighbor"
                    );
                source_minimum_external_objectives[index] =
                    static_cast<std::uint16_t>(minimum_external_objective);
            }
            add(source_thread_counters[omp_get_thread_num()], local);
        } catch (const std::exception& exception) {
#pragma omp critical
            {
                if (error.empty()) error = exception.what();
            }
        }
    }
    if (!error.empty()) throw std::runtime_error(error);

    Counters source_total;
    for (const Counters& counters : source_thread_counters)
        add(source_total, counters);
    if (source_total.verified != sources.size() ||
        source_total.objective_mismatch || source_total.missing_frontier)
        throw std::runtime_error("objective-ten source verification failed");
    if (source_total.incidence != target_total.incidence)
        throw std::runtime_error("source-target incidence mismatch");

    std::array<std::unordered_set<State, StateHash>, 11> threshold_ten_sets;
    for (int objective = 2; objective <= 9; ++objective)
        threshold_ten_sets[objective].insert(
            source_sets[objective].begin(), source_sets[objective].end()
        );
    threshold_ten_sets[10].insert(targets.begin(), targets.end());
    std::array<std::unordered_set<State, StateHash>, 11> additional_sets;
    std::vector<SourceEntry> closure_queue;
    for (int objective = 2; objective <= 10; ++objective) {
        for (const State& state : expansion_total.new_orbits[objective]) {
            if (!threshold_ten_sets[objective].insert(state).second)
                throw std::runtime_error("second-shell state is already known");
            additional_sets[objective].insert(state);
            closure_queue.push_back({objective, state});
        }
    }

    for (std::size_t position = 0; position < closure_queue.size(); ++position) {
        if (position && position % 10000 == 0)
            std::cerr << "threshold-ten direct closure: " << position << '/'
                      << closure_queue.size() << " states\n";
        const SourceEntry& source = closure_queue[position];
        const Model::Analysis analysis = model.analyze(source.state);
        if (analysis.objective != source.objective)
            throw std::runtime_error("threshold-ten closure objective mismatch");
        for (int id = 0; id < edge_count; ++id) {
            const int objective = analysis.objective + analysis.delta[id];
            if (objective > 10) continue;
            if (objective < 0)
                throw std::runtime_error("negative threshold-ten objective");
            State neighbor = source.state;
            neighbor.toggle(id);
            const State key = model.canonical(neighbor);
            if (!threshold_ten_sets[objective].insert(key).second) continue;
            if (!model.is_free(key))
                throw std::runtime_error("nonfree threshold-ten closure orbit");
            additional_sets[objective].insert(key);
            closure_queue.push_back({objective, key});
        }
    }

    std::array<std::map<int, std::uint64_t>, 11>
        additional_neighbor_histograms;
    std::uint64_t additional_internal_directed = 0;
    std::uint64_t additional_to_known_directed = 0;
    int additional_escape_level = std::numeric_limits<int>::max();
    for (std::size_t position = 0; position < closure_queue.size(); ++position) {
        const SourceEntry& source = closure_queue[position];
        const Model::Analysis analysis = model.analyze(source.state);
        if (analysis.objective != source.objective)
            throw std::runtime_error("threshold-ten recount objective mismatch");
        for (int id = 0; id < edge_count; ++id) {
            const int objective = analysis.objective + analysis.delta[id];
            additional_neighbor_histograms[source.objective][objective] += order;
            if (objective > 10) {
                additional_escape_level = std::min(
                    additional_escape_level, objective
                );
                continue;
            }
            if (objective < 0)
                throw std::runtime_error("negative threshold-ten recount objective");
            State neighbor = source.state;
            neighbor.toggle(id);
            const State key = model.canonical(neighbor);
            if (!threshold_ten_sets[objective].contains(key))
                throw std::runtime_error("threshold-ten accepted neighbor missing");
            if (additional_sets[objective].contains(key))
                additional_internal_directed += order;
            else
                additional_to_known_directed += order;
        }
    }
    if (additional_internal_directed % 2 ||
        additional_escape_level == std::numeric_limits<int>::max())
        throw std::runtime_error("invalid threshold-ten closure aggregate");

    std::uint64_t additional_orbit_count = 0;
    for (int objective = 0; objective <= 10; ++objective)
        additional_orbit_count += additional_sets[objective].size();
    const std::uint64_t additional_vertex_count = order * additional_orbit_count;
    const std::uint64_t additional_internal_edges =
        additional_internal_directed / 2;
    const std::uint64_t frontier_internal_edges =
        order * expansion_total.internal_objective_ten_directed_incidence / 2;
    const std::uint64_t complete_threshold_ten_vertex_count =
        2681308 + order * targets.size() + additional_vertex_count;
    const std::uint64_t complete_threshold_ten_edge_count =
        12794607 + 21517200 + frontier_internal_edges +
        additional_to_known_directed + additional_internal_edges;

    std::map<std::array<std::uint16_t, 10>, std::uint64_t> signature_histogram;
    std::map<int, std::uint64_t> incidence_degree_histogram;
    std::map<int, std::uint64_t> target_distinct_orbit_degree_histogram;
    std::map<int, std::uint64_t> source_distinct_orbit_degree_histogram;
    std::map<int, std::uint64_t> target_parallel_incidence_excess_histogram;
    std::map<int, std::uint64_t>
        target_max_source_orbit_multiplicity_histogram;
    std::array<std::map<int, std::uint64_t>, 10>
        source_distinct_orbit_degree_by_objective;
    std::map<int, std::uint64_t> source_minimum_external_objective_histogram;
    std::map<int, std::uint64_t> target_objective_ten_move_count_histogram;
    std::map<int, std::uint64_t>
        target_minimum_above_ten_objective_histogram;
    std::array<std::uint64_t, 10>
        sources_without_objective_ten_exit_by_objective{};
    std::vector<std::size_t>
        objective_nine_layer_indices_without_objective_ten_exit;
    std::vector<std::size_t>
        objective_ten_layer_indices_with_parallel_boundary_incidence;
    std::array<std::size_t, 10> source_layer_indices{};
    std::uint64_t target_distinct_orbit_edge_total = 0;
    std::uint64_t source_distinct_orbit_edge_total = 0;
    for (const auto& signature : recounted_signatures) {
        ++signature_histogram[signature];
        int degree = 0;
        for (int objective = 2; objective <= 9; ++objective)
            degree += signature[objective];
        ++incidence_degree_histogram[degree];
    }
    std::uint64_t parallel_incidence_excess_total = 0;
    for (std::size_t index = 0; index < targets.size(); ++index) {
        const int degree = target_distinct_source_orbit_degrees[index];
        ++target_distinct_orbit_degree_histogram[degree];
        target_distinct_orbit_edge_total += degree;
        const int excess = target_parallel_incidence_excess[index];
        ++target_parallel_incidence_excess_histogram[excess];
        ++target_max_source_orbit_multiplicity_histogram
            [target_max_source_orbit_multiplicity[index]];
        parallel_incidence_excess_total += excess;
        if (excess)
            objective_ten_layer_indices_with_parallel_boundary_incidence
                .push_back(index);
        ++target_objective_ten_move_count_histogram
            [target_objective_ten_move_counts[index]];
        ++target_minimum_above_ten_objective_histogram
            [target_minimum_above_ten_objectives[index]];
    }
    for (std::size_t index = 0; index < sources.size(); ++index) {
        const int degree = source_distinct_target_orbit_degrees[index];
        const int objective = sources[index].objective;
        const std::size_t layer_index = source_layer_indices[objective]++;
        ++source_distinct_orbit_degree_histogram[degree];
        ++source_distinct_orbit_degree_by_objective[objective][degree];
        ++source_minimum_external_objective_histogram
            [source_minimum_external_objectives[index]];
        if (degree == 0) {
            ++sources_without_objective_ten_exit_by_objective[objective];
            if (objective == 9)
                objective_nine_layer_indices_without_objective_ten_exit.push_back(
                    layer_index
                );
        }
        source_distinct_orbit_edge_total += degree;
    }
    if (source_distinct_orbit_edge_total != target_distinct_orbit_edge_total)
        throw std::runtime_error("simple quotient boundary edge mismatch");
    std::uint64_t quotient_incidence_total = 0;
    for (int objective = 2; objective <= 9; ++objective)
        quotient_incidence_total += source_total.incidence[objective];
    if (quotient_incidence_total !=
        source_distinct_orbit_edge_total + parallel_incidence_excess_total)
        throw std::runtime_error("quotient boundary multiplicity mismatch");

    std::cout << "{\n";
    std::cout << "  \"independent_source_recount_representative_count\": "
              << source_total.verified << ",\n";
    std::cout << "  \"independent_target_recount_representative_count\": "
              << target_total.verified << ",\n";
    std::cout << "  \"all_sources_have_expected_objective\": true,\n";
    std::cout << "  \"all_targets_have_objective_ten\": true,\n";
    std::cout << "  \"all_targets_are_canonical_and_free\": true,\n";
    std::cout << "  \"missing_objective_ten_frontier_neighbor_count\": 0,\n";
    std::cout << "  \"incidence_signature_mismatch_count\": 0,\n";
    std::cout << "  \"source_target_incidence_totals_agree\": true,\n";
    std::cout << "  \"incidence_signature_count\": "
              << signature_histogram.size() << ",\n";
    std::cout << "  \"frontier_incidence_degree_histogram\": {";
    bool degree_separator = false;
    for (const auto& [degree, count] : incidence_degree_histogram) {
        if (degree_separator) std::cout << ',';
        std::cout << "\n    \"" << degree << "\": " << count;
        degree_separator = true;
    }
    std::cout << "\n  },\n";
    auto write_histogram = [](const std::map<int, std::uint64_t>& histogram) {
        bool separator = false;
        for (const auto& [degree, count] : histogram) {
            if (separator) std::cout << ',';
            std::cout << "\n    \"" << degree << "\": " << count;
            separator = true;
        }
        std::cout << "\n  }";
    };
    std::cout << "  \"target_distinct_source_orbit_degree_histogram\": {";
    write_histogram(target_distinct_orbit_degree_histogram);
    std::cout << ",\n";
    std::cout << "  \"source_distinct_target_orbit_degree_histogram\": {";
    write_histogram(source_distinct_orbit_degree_histogram);
    std::cout << ",\n";
    std::cout << "  \"source_distinct_target_orbit_degree_by_objective\": {";
    for (int objective = 2; objective <= 9; ++objective) {
        if (objective != 2) std::cout << ',';
        std::cout << "\n    \"" << objective << "\": {";
        bool separator = false;
        for (const auto& [degree, count] :
             source_distinct_orbit_degree_by_objective[objective]) {
            if (separator) std::cout << ',';
            std::cout << "\n      \"" << degree << "\": " << count;
            separator = true;
        }
        std::cout << "\n    }";
    }
    std::cout << "\n  },\n";
    std::cout << "  \"simple_quotient_boundary_edge_count\": "
              << source_distinct_orbit_edge_total << ",\n";
    std::cout << "  \"quotient_boundary_incidence_count\": "
              << quotient_incidence_total << ",\n";
    std::cout << "  \"parallel_quotient_incidence_excess\": "
              << parallel_incidence_excess_total << ",\n";
    std::cout << "  \"target_parallel_incidence_excess_histogram\": {";
    write_histogram(target_parallel_incidence_excess_histogram);
    std::cout << ",\n";
    std::cout
        << "  \"target_max_source_orbit_multiplicity_histogram\": {";
    write_histogram(target_max_source_orbit_multiplicity_histogram);
    std::cout << ",\n";
    std::cout
        << "  \"objective_ten_layer_indices_with_parallel_boundary_incidence\": [";
    for (std::size_t index = 0;
         index <
         objective_ten_layer_indices_with_parallel_boundary_incidence.size();
         ++index) {
        if (index) std::cout << ',';
        std::cout << objective_ten_layer_indices_with_parallel_boundary_incidence
                         [index];
    }
    std::cout << "],\n";
    std::cout << "  \"source_minimum_external_objective_histogram\": {";
    write_histogram(source_minimum_external_objective_histogram);
    std::cout << ",\n";
    std::cout << "  \"sources_without_objective_ten_exit_by_objective\": {";
    bool missing_separator = false;
    for (int objective = 2; objective <= 9; ++objective) {
        if (!sources_without_objective_ten_exit_by_objective[objective])
            continue;
        if (missing_separator) std::cout << ',';
        std::cout << "\n    \"" << objective << "\": "
                  << sources_without_objective_ten_exit_by_objective[objective];
        missing_separator = true;
    }
    std::cout << "\n  },\n";
    std::cout
        << "  \"objective_nine_layer_indices_without_objective_ten_exit\": [";
    for (std::size_t index = 0;
         index < objective_nine_layer_indices_without_objective_ten_exit.size();
         ++index) {
        if (index) std::cout << ',';
        if (index % 12 == 0) std::cout << "\n    ";
        std::cout << objective_nine_layer_indices_without_objective_ten_exit[index];
    }
    std::cout << "\n  ],\n";
    std::cout << "  \"all_source_orbits_have_objective_ten_exit\": "
              << (source_distinct_orbit_degree_histogram.contains(0)
                      ? "false"
                      : "true")
              << ",\n";
    std::cout << "  \"aggregate_objective_ten_frontier_neighbor_objective_histogram\": {";
    bool objective_separator = false;
    for (const auto& [objective, count] :
         target_total.target_neighbor_objective_histogram) {
        if (objective_separator) std::cout << ',';
        std::cout << "\n    \"" << objective << "\": " << order * count;
        objective_separator = true;
    }
    std::cout << "\n  },\n";
    std::cout << "  \"objective_ten_move_count_per_target_orbit_histogram\": {";
    write_histogram(target_objective_ten_move_count_histogram);
    std::cout << ",\n";
    std::cout << "  \"minimum_above_ten_objective_per_target_orbit_histogram\": {";
    write_histogram(target_minimum_above_ten_objective_histogram);
    std::cout << ",\n";
    std::cout << "  \"objective_ten_frontier_internal_directed_incidence\": "
              << expansion_total.internal_objective_ten_directed_incidence
              << ",\n";
    std::cout << "  \"objective_ten_frontier_internal_distinct_directed_pairs\": "
              << expansion_total.internal_objective_ten_distinct_directed_pairs
              << ",\n";
    std::cout << "  \"objective_ten_frontier_self_orbit_pair_count\": "
              << expansion_total.internal_objective_ten_self_orbit_pairs
              << ",\n";
    std::cout << "  \"newly_exposed_rotation_orbit_count_by_objective\": {";
    bool new_layer_separator = false;
    for (int objective = 0; objective <= 10; ++objective) {
        if (expansion_total.new_orbits[objective].empty()) continue;
        if (new_layer_separator) std::cout << ',';
        std::cout << "\n    \"" << objective << "\": "
                  << expansion_total.new_orbits[objective].size();
        new_layer_separator = true;
    }
    std::cout << "\n  },\n";
    for (int objective = 0; objective <= 10; ++objective) {
        if (expansion_total.new_orbits[objective].empty()) continue;
        std::vector<State> representatives(
            expansion_total.new_orbits[objective].begin(),
            expansion_total.new_orbits[objective].end()
        );
        std::sort(representatives.begin(), representatives.end());
        std::cout << "  \"newly_exposed_objective_" << objective
                  << "_rotation_representatives\": [\n";
        for (std::size_t index = 0; index < representatives.size(); ++index) {
            if (index) std::cout << ",\n";
            std::cout << "    ";
            write_state(std::cout, representatives[index]);
        }
        std::cout << "\n  ],\n";
    }
    std::cout << "  \"directed_incidence_by_source_objective\": {";
    std::uint64_t total_incidence = 0;
    for (int objective = 2; objective <= 9; ++objective) {
        if (objective != 2) std::cout << ',';
        const std::uint64_t lifted = order * source_total.incidence[objective];
        total_incidence += lifted;
        std::cout << "\n    \"" << objective << "\": " << lifted;
    }
    std::cout << "\n  },\n";
    std::cout << "  \"total_directed_sublevel_nine_incidence\": "
              << total_incidence << ",\n";
    std::cout << "  \"complete_threshold_ten_additional_rotation_orbit_count\": "
              << additional_orbit_count << ",\n";
    std::cout << "  \"complete_threshold_ten_additional_vertex_count\": "
              << additional_vertex_count << ",\n";
    std::cout << "  \"additional_rotation_orbit_count_by_objective\": {";
    bool additional_separator = false;
    for (int objective = 0; objective <= 10; ++objective) {
        if (additional_sets[objective].empty()) continue;
        if (additional_separator) std::cout << ',';
        std::cout << "\n    \"" << objective << "\": "
                  << additional_sets[objective].size();
        additional_separator = true;
    }
    std::cout << "\n  },\n";
    std::cout << "  \"additional_to_known_directed_edge_count\": "
              << additional_to_known_directed << ",\n";
    std::cout << "  \"additional_internal_edge_count\": "
              << additional_internal_edges << ",\n";
    std::cout << "  \"complete_sublevel_ten_component_vertex_count\": "
              << complete_threshold_ten_vertex_count << ",\n";
    std::cout << "  \"complete_sublevel_ten_component_edge_count\": "
              << complete_threshold_ten_edge_count << ",\n";
    std::cout << "  \"complete_sublevel_ten_component_is_closed\": true,\n";
    std::cout << "  \"exact_one_flip_escape_level_from_sublevel_ten_component\": "
              << std::min(11, additional_escape_level) << ",\n";
    std::cout << "  \"additional_neighbor_objective_histogram_by_source_objective\": {";
    bool source_histogram_separator = false;
    for (int source = 0; source <= 10; ++source) {
        if (additional_neighbor_histograms[source].empty()) continue;
        if (source_histogram_separator) std::cout << ',';
        std::cout << "\n    \"" << source << "\": {";
        bool target_histogram_separator = false;
        for (const auto& [target, count] :
             additional_neighbor_histograms[source]) {
            if (target_histogram_separator) std::cout << ',';
            std::cout << "\n      \"" << target << "\": " << count;
            target_histogram_separator = true;
        }
        std::cout << "\n    }";
        source_histogram_separator = true;
    }
    std::cout << "\n  },\n";
    for (int objective = 0; objective <= 10; ++objective) {
        if (additional_sets[objective].empty()) continue;
        std::vector<State> representatives(
            additional_sets[objective].begin(),
            additional_sets[objective].end()
        );
        std::sort(representatives.begin(), representatives.end());
        std::cout << "  \"complete_threshold_ten_additional_objective_"
                  << objective << "_rotation_representatives\": [\n";
        for (std::size_t index = 0; index < representatives.size(); ++index) {
            if (index) std::cout << ",\n";
            std::cout << "    ";
            write_state(std::cout, representatives[index]);
        }
        std::cout << "\n  ],\n";
    }
    std::cout << "  \"method\": \"independent bidirectional direct five-set recount: all complete sublevel-nine sources scanned for objective-ten exits and every listed target scanned for exact lower-layer incidence\",\n";
    std::cout << "  \"openmp_max_threads\": " << omp_get_max_threads()
              << "\n}\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
