#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iomanip>
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

std::vector<std::size_t> load_flat_indices(
    const std::string& path, const std::string& key
) {
    const std::string array = keyed_array(read_text(path), key);
    const std::regex integer_pattern(R"(([0-9]+))");
    std::vector<std::size_t> result;
    for (std::sregex_iterator it(
             array.begin(), array.end(), integer_pattern
         ), last;
         it != last; ++it)
        result.push_back(std::stoull((*it)[1]));
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

struct Model {
    std::array<std::array<int, order>, order> edge_id{};
    std::array<std::pair<int, int>, edge_count> edge_vertices{};
    std::array<std::array<std::uint16_t, edge_count>, order> rotated_edge{};
    std::array<std::uint16_t, edge_count> reflected_edge{};
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
        for (int id = 0; id < edge_count; ++id) {
            auto [a, b] = edge_vertices[id];
            a = (order - a) % order;
            b = (order - b) % order;
            reflected_edge[id] = static_cast<std::uint16_t>(edge_id[a][b]);
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

    State reflect(const State& source) const {
        State result;
        for (int word_index = 0; word_index < word_count; ++word_index) {
            std::uint64_t word = source.words[word_index];
            while (word) {
                const int bit = std::countr_zero(word);
                const int id = 64 * word_index + bit;
                if (id < edge_count) {
                    const int mapped = reflected_edge[id];
                    result.words[mapped / 64] |= 1ULL << (mapped % 64);
                }
                word &= word - 1;
            }
        }
        return result;
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

void write_histogram(const std::map<int, std::uint64_t>& histogram) {
    bool separator = false;
    for (const auto& [key, value] : histogram) {
        if (separator) std::cout << ',';
        std::cout << "\n    \"" << key << "\": " << value;
        separator = true;
    }
    std::cout << "\n  }";
}

std::string fingerprint(const std::vector<State>& states) {
    std::uint64_t hash = 1469598103934665603ULL;
    for (const State& state : states) {
        for (std::uint64_t word : state.words) {
            hash ^= word;
            hash *= 1099511628211ULL;
        }
        hash ^= 0xff;
        hash *= 1099511628211ULL;
    }
    std::ostringstream output;
    output << std::hex << std::setfill('0') << std::setw(16) << hash;
    return output.str();
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 3) {
        std::cerr
            << "usage: verify_objective_eleven_shadow "
               "OBJECTIVE-NINE-COMPONENT.json "
               "OBJECTIVE-TEN-INDEPENDENT.json\n";
        return 2;
    }

    Model model;
    const std::vector<State> objective_nine = load_states(
        argv[1], "new_objective_9_rotation_representatives"
    );
    const std::vector<std::size_t> exceptional_indices = load_flat_indices(
        argv[2], "objective_nine_layer_indices_without_objective_ten_exit"
    );
    if (objective_nine.size() != 42781 || exceptional_indices.size() != 65)
        throw std::runtime_error("unexpected source certificate size");

    std::unordered_set<State, StateHash> complete_objective_nine_set;
    complete_objective_nine_set.reserve(2 * objective_nine.size());
    for (const State& state : objective_nine)
        if (!complete_objective_nine_set.insert(state).second)
            throw std::runtime_error("duplicate objective-nine representative");

    std::vector<State> sources;
    std::unordered_set<State, StateHash> exceptional_source_set;
    exceptional_source_set.reserve(2 * exceptional_indices.size());
    std::set<std::size_t> distinct_indices;
    for (std::size_t index : exceptional_indices) {
        if (index >= objective_nine.size() || !distinct_indices.insert(index).second)
            throw std::runtime_error("invalid exceptional source index");
        const State& source = objective_nine[index];
        if (!exceptional_source_set.insert(source).second)
            throw std::runtime_error("duplicate exceptional source");
        sources.push_back(source);
    }

    std::unordered_map<State, std::uint32_t, StateHash>
        target_shadow_incidence;
    std::unordered_map<State, std::uint16_t, StateHash>
        target_distinct_shadow_sources;
    std::map<int, std::uint64_t> source_incidence_degree_histogram;
    std::map<int, std::uint64_t> source_distinct_target_degree_histogram;
    std::map<int, std::uint64_t> pair_multiplicity_histogram;
    std::uint64_t quotient_incidence_count = 0;
    std::uint64_t simple_quotient_edge_count = 0;
    std::vector<std::vector<State>> source_target_states(sources.size());

    for (std::size_t source_index = 0; source_index < sources.size();
         ++source_index) {
        const State& source = sources[source_index];
        if (!(model.canonical(source) == source) || !model.is_free(source))
            throw std::runtime_error("exceptional source is noncanonical or nonfree");
        const Model::Analysis analysis = model.analyze(source);
        if (analysis.objective != 9)
            throw std::runtime_error("exceptional source objective mismatch");
        int minimum_external_objective = std::numeric_limits<int>::max();
        int objective_ten_neighbor_count = 0;
        std::unordered_map<State, std::uint16_t, StateHash> local_targets;
        for (int id = 0; id < edge_count; ++id) {
            const int objective = analysis.objective + analysis.delta[id];
            if (objective > 9)
                minimum_external_objective =
                    std::min(minimum_external_objective, objective);
            if (objective == 10) ++objective_ten_neighbor_count;
            if (objective != 11) continue;
            State target = source;
            target.toggle(id);
            ++local_targets[model.canonical(target)];
        }
        if (objective_ten_neighbor_count || minimum_external_objective != 11)
            throw std::runtime_error("source is not in the level-ten shadow");
        int incidence_degree = 0;
        for (const auto& [target, multiplicity] : local_targets) {
            incidence_degree += multiplicity;
            target_shadow_incidence[target] += multiplicity;
            ++target_distinct_shadow_sources[target];
            ++pair_multiplicity_histogram[multiplicity];
            source_target_states[source_index].push_back(target);
        }
        ++source_incidence_degree_histogram[incidence_degree];
        ++source_distinct_target_degree_histogram[local_targets.size()];
        quotient_incidence_count += incidence_degree;
        simple_quotient_edge_count += local_targets.size();
    }

    std::vector<State> targets;
    targets.reserve(target_shadow_incidence.size());
    for (const auto& [target, incidence] : target_shadow_incidence) {
        (void)incidence;
        targets.push_back(target);
    }
    std::sort(targets.begin(), targets.end());

    std::vector<int> target_shadow_incidence_recount(targets.size());
    std::vector<int> target_distinct_shadow_sources_recount(targets.size());
    std::vector<int> target_all_primary_nine_incidence(targets.size());
    std::vector<int> target_distinct_primary_nine_sources(targets.size());
    std::vector<bool> target_has_nonshadow_primary_nine_source(targets.size());
    std::string error;
#pragma omp parallel for schedule(dynamic, 1)
    for (std::size_t index = 0; index < targets.size(); ++index) {
        try {
            const State& target = targets[index];
            if (!(model.canonical(target) == target) || !model.is_free(target))
                throw std::runtime_error("target is noncanonical or nonfree");
            const Model::Analysis analysis = model.analyze(target);
            if (analysis.objective != 11)
                throw std::runtime_error("target objective mismatch");
            std::unordered_set<State, StateHash> distinct_shadow_sources;
            std::unordered_set<State, StateHash> distinct_primary_nine_sources;
            for (int id = 0; id < edge_count; ++id) {
                if (analysis.objective + analysis.delta[id] != 9) continue;
                State neighbor = target;
                neighbor.toggle(id);
                const State key = model.canonical(neighbor);
                if (!complete_objective_nine_set.contains(key)) continue;
                ++target_all_primary_nine_incidence[index];
                distinct_primary_nine_sources.insert(key);
                if (exceptional_source_set.contains(key)) {
                    ++target_shadow_incidence_recount[index];
                    distinct_shadow_sources.insert(key);
                } else {
                    target_has_nonshadow_primary_nine_source[index] = true;
                }
            }
            target_distinct_shadow_sources_recount[index] =
                distinct_shadow_sources.size();
            target_distinct_primary_nine_sources[index] =
                distinct_primary_nine_sources.size();
            if (target_shadow_incidence_recount[index] !=
                    static_cast<int>(target_shadow_incidence.at(target)) ||
                target_distinct_shadow_sources_recount[index] !=
                    static_cast<int>(target_distinct_shadow_sources.at(target)))
                throw std::runtime_error("bidirectional incidence mismatch");
        } catch (const std::exception& exception) {
#pragma omp critical
            {
                if (error.empty()) error = exception.what();
            }
        }
    }
    if (!error.empty()) throw std::runtime_error(error);

    std::unordered_map<State, std::size_t, StateHash> target_index;
    target_index.reserve(2 * targets.size());
    for (std::size_t index = 0; index < targets.size(); ++index)
        if (!target_index.emplace(targets[index], index).second)
            throw std::runtime_error("duplicate sorted target");
    const std::size_t bipartite_vertex_count = sources.size() + targets.size();
    std::vector<std::size_t> parent(bipartite_vertex_count);
    std::vector<std::size_t> rank(bipartite_vertex_count);
    for (std::size_t index = 0; index < parent.size(); ++index)
        parent[index] = index;
    auto find_root = [&](std::size_t vertex) {
        std::size_t root = vertex;
        while (parent[root] != root) root = parent[root];
        while (parent[vertex] != vertex) {
            const std::size_t next = parent[vertex];
            parent[vertex] = root;
            vertex = next;
        }
        return root;
    };
    auto unite = [&](std::size_t first, std::size_t second) {
        std::size_t first_root = find_root(first);
        std::size_t second_root = find_root(second);
        if (first_root == second_root) return;
        if (rank[first_root] < rank[second_root])
            std::swap(first_root, second_root);
        parent[second_root] = first_root;
        if (rank[first_root] == rank[second_root]) ++rank[first_root];
    };
    for (std::size_t source_index = 0;
         source_index < source_target_states.size(); ++source_index)
        for (const State& target : source_target_states[source_index])
            unite(source_index, sources.size() + target_index.at(target));

    struct ComponentProfile {
        std::size_t root = 0;
        std::uint64_t sources = 0;
        std::uint64_t targets = 0;
        std::uint64_t edges = 0;
    };
    std::unordered_map<std::size_t, ComponentProfile> component_map;
    for (std::size_t index = 0; index < sources.size(); ++index)
        ++component_map[find_root(index)].sources;
    for (std::size_t index = 0; index < targets.size(); ++index)
        ++component_map[find_root(sources.size() + index)].targets;
    for (std::size_t source_index = 0;
         source_index < source_target_states.size(); ++source_index)
        component_map[find_root(source_index)].edges +=
            source_target_states[source_index].size();
    std::vector<ComponentProfile> component_profiles;
    for (const auto& [root, profile] : component_map) {
        ComponentProfile rooted_profile = profile;
        rooted_profile.root = root;
        component_profiles.push_back(rooted_profile);
    }
    std::sort(
        component_profiles.begin(), component_profiles.end(),
        [](const ComponentProfile& first, const ComponentProfile& second) {
            return std::array{
                       first.sources + first.targets, first.sources,
                       first.targets, first.edges
                   } >
                   std::array{
                       second.sources + second.targets, second.sources,
                       second.targets, second.edges
                   };
        }
    );
    const std::uint64_t bipartite_cycle_rank =
        simple_quotient_edge_count - bipartite_vertex_count +
        component_profiles.size();

    std::unordered_map<State, std::size_t, StateHash> exceptional_source_index;
    exceptional_source_index.reserve(2 * sources.size());
    for (std::size_t index = 0; index < sources.size(); ++index)
        if (!exceptional_source_index.emplace(sources[index], index).second)
            throw std::runtime_error("duplicate indexed exceptional source");
    std::unordered_map<std::size_t, std::size_t> root_to_profile_index;
    for (std::size_t index = 0; index < component_profiles.size(); ++index)
        root_to_profile_index.emplace(component_profiles[index].root, index);
    std::vector<std::size_t> component_reflection_partner(
        component_profiles.size(), component_profiles.size()
    );
    std::uint64_t reflection_fixed_sources = 0;
    std::uint64_t reflection_fixed_targets = 0;
    auto record_component_reflection = [&](std::size_t vertex,
                                           std::size_t reflected_vertex) {
        const std::size_t component =
            root_to_profile_index.at(find_root(vertex));
        const std::size_t partner =
            root_to_profile_index.at(find_root(reflected_vertex));
        if (component_reflection_partner[component] !=
                component_profiles.size() &&
            component_reflection_partner[component] != partner)
            throw std::runtime_error("inconsistent component reflection");
        component_reflection_partner[component] = partner;
    };
    for (std::size_t index = 0; index < sources.size(); ++index) {
        const State reflected = model.canonical(model.reflect(sources[index]));
        const auto reflected_it = exceptional_source_index.find(reflected);
        if (reflected_it == exceptional_source_index.end())
            throw std::runtime_error("shadow source set is not reflection invariant");
        reflection_fixed_sources += reflected == sources[index];
        record_component_reflection(index, reflected_it->second);
    }
    for (std::size_t index = 0; index < targets.size(); ++index) {
        const State reflected = model.canonical(model.reflect(targets[index]));
        const auto reflected_it = target_index.find(reflected);
        if (reflected_it == target_index.end())
            throw std::runtime_error("shadow target set is not reflection invariant");
        reflection_fixed_targets += reflected == targets[index];
        record_component_reflection(
            sources.size() + index, sources.size() + reflected_it->second
        );
    }
    std::uint64_t reflection_fixed_components = 0;
    for (std::size_t index = 0; index < component_reflection_partner.size();
         ++index) {
        if (component_reflection_partner[index] == component_profiles.size() ||
            component_reflection_partner
                [component_reflection_partner[index]] != index)
            throw std::runtime_error("component reflection is not an involution");
        reflection_fixed_components +=
            component_reflection_partner[index] == index;
    }

    std::map<int, std::uint64_t> target_shadow_incidence_degree_histogram;
    std::map<int, std::uint64_t>
        target_distinct_shadow_source_degree_histogram;
    std::map<int, std::uint64_t> target_primary_nine_incidence_histogram;
    std::map<int, std::uint64_t>
        target_distinct_primary_nine_source_histogram;
    std::uint64_t targets_with_nonshadow_primary_nine_source = 0;
    std::uint64_t total_primary_nine_incidence = 0;
    for (std::size_t index = 0; index < targets.size(); ++index) {
        ++target_shadow_incidence_degree_histogram
            [target_shadow_incidence_recount[index]];
        ++target_distinct_shadow_source_degree_histogram
            [target_distinct_shadow_sources_recount[index]];
        ++target_primary_nine_incidence_histogram
            [target_all_primary_nine_incidence[index]];
        ++target_distinct_primary_nine_source_histogram
            [target_distinct_primary_nine_sources[index]];
        targets_with_nonshadow_primary_nine_source +=
            target_has_nonshadow_primary_nine_source[index];
        total_primary_nine_incidence += target_all_primary_nine_incidence[index];
    }

    std::cout << "{\n";
    std::cout << "  \"order\": 43,\n";
    std::cout << "  \"exceptional_objective_nine_source_orbit_count\": "
              << sources.size() << ",\n";
    std::cout << "  \"all_sources_are_canonical_free_objective_nine\": true,\n";
    std::cout << "  \"all_sources_have_zero_objective_ten_neighbors\": true,\n";
    std::cout << "  \"all_sources_have_minimum_external_objective_eleven\": true,\n";
    std::cout << "  \"objective_eleven_shadow_target_orbit_count\": "
              << targets.size() << ",\n";
    std::cout << "  \"objective_eleven_shadow_target_vertex_count\": "
              << order * targets.size() << ",\n";
    std::cout << "  \"all_targets_are_canonical_free_objective_eleven\": true,\n";
    std::cout << "  \"quotient_shadow_incidence_count\": "
              << quotient_incidence_count << ",\n";
    std::cout << "  \"labeled_shadow_incidence_count\": "
              << order * quotient_incidence_count << ",\n";
    std::cout << "  \"simple_shadow_quotient_edge_count\": "
              << simple_quotient_edge_count << ",\n";
    std::cout << "  \"parallel_shadow_incidence_excess\": "
              << quotient_incidence_count - simple_quotient_edge_count << ",\n";
    std::cout << "  \"source_objective_eleven_incidence_degree_histogram\": {";
    write_histogram(source_incidence_degree_histogram);
    std::cout << ",\n";
    std::cout << "  \"source_distinct_target_orbit_degree_histogram\": {";
    write_histogram(source_distinct_target_degree_histogram);
    std::cout << ",\n";
    std::cout << "  \"source_target_orbit_pair_multiplicity_histogram\": {";
    write_histogram(pair_multiplicity_histogram);
    std::cout << ",\n";
    std::cout << "  \"target_shadow_incidence_degree_histogram\": {";
    write_histogram(target_shadow_incidence_degree_histogram);
    std::cout << ",\n";
    std::cout << "  \"target_distinct_shadow_source_degree_histogram\": {";
    write_histogram(target_distinct_shadow_source_degree_histogram);
    std::cout << ",\n";
    std::cout << "  \"target_primary_objective_nine_incidence_histogram\": {";
    write_histogram(target_primary_nine_incidence_histogram);
    std::cout << ",\n";
    std::cout << "  \"target_distinct_primary_objective_nine_source_histogram\": {";
    write_histogram(target_distinct_primary_nine_source_histogram);
    std::cout << ",\n";
    std::cout << "  \"targets_with_nonshadow_primary_objective_nine_source\": "
              << targets_with_nonshadow_primary_nine_source << ",\n";
    std::cout << "  \"total_primary_objective_nine_incidence_to_shadow_targets\": "
              << total_primary_nine_incidence << ",\n";
    std::cout << "  \"shadow_incidence_bipartite_component_count\": "
              << component_profiles.size() << ",\n";
    std::cout << "  \"shadow_incidence_bipartite_cycle_rank\": "
              << bipartite_cycle_rank << ",\n";
    std::cout << "  \"shadow_incidence_bipartite_component_profiles\": [";
    for (std::size_t index = 0; index < component_profiles.size(); ++index) {
        const ComponentProfile& profile = component_profiles[index];
        if (index) std::cout << ',';
        std::cout << "\n    {\"source_orbits\":" << profile.sources
                  << ",\"target_orbits\":" << profile.targets
                  << ",\"edges\":" << profile.edges << '}';
    }
    std::cout << "\n  ],\n";
    std::cout << "  \"component_reflection_partner_indices\": [";
    for (std::size_t index = 0; index < component_reflection_partner.size();
         ++index) {
        if (index) std::cout << ',';
        std::cout << component_reflection_partner[index];
    }
    std::cout << "],\n";
    std::cout << "  \"reflection_fixed_component_count\": "
              << reflection_fixed_components << ",\n";
    std::cout << "  \"reflection_paired_component_pair_count\": "
              << (component_profiles.size() - reflection_fixed_components) / 2
              << ",\n";
    std::cout << "  \"reflection_fixed_source_orbit_count\": "
              << reflection_fixed_sources << ",\n";
    std::cout << "  \"reflection_fixed_target_orbit_count\": "
              << reflection_fixed_targets << ",\n";
    std::cout << "  \"dihedral_shadow_source_orbit_count\": "
              << (sources.size() + reflection_fixed_sources) / 2 << ",\n";
    std::cout << "  \"dihedral_shadow_target_orbit_count\": "
              << (targets.size() + reflection_fixed_targets) / 2 << ",\n";
    std::cout << "  \"sorted_target_state_fnv1a64\": \""
              << fingerprint(targets) << "\",\n";
    std::cout << "  \"bidirectional_shadow_incidence_totals_agree\": true,\n";
    std::cout << "  \"method\": \"independent direct five-set recount at all 65 shadow sources and every deduplicated objective-eleven target, with cyclic canonicalization and bidirectional incidence comparison\",\n";
    std::cout << "  \"scope_note\": \"Exact first objective-eleven neighborhood of the 65 certified level-ten-shadow source orbits only; not the complete objective-eleven frontier of the threshold-ten component.\",\n";
    std::cout << "  \"openmp_max_threads\": " << omp_get_max_threads()
              << "\n}\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
