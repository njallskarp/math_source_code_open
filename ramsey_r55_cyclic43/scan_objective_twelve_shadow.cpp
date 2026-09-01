#define main objective_six_component_embedded_main
#include "objective_six_component.cpp"
#undef main

#include <tuple>

namespace {

struct DisjointSet {
    std::vector<std::size_t> parent;
    std::vector<std::size_t> size;

    explicit DisjointSet(std::size_t count) : parent(count), size(count, 1) {
        std::iota(parent.begin(), parent.end(), std::size_t{0});
    }

    std::size_t find(std::size_t value) {
        while (parent[value] != value) {
            parent[value] = parent[parent[value]];
            value = parent[value];
        }
        return value;
    }

    void unite(std::size_t left, std::size_t right) {
        left = find(left);
        right = find(right);
        if (left == right) return;
        if (size[left] < size[right]) std::swap(left, right);
        parent[right] = left;
        size[left] += size[right];
    }
};

struct TargetInfo {
    std::uint64_t quotient_incidence = 0;
    std::unordered_set<std::size_t> source_indices;
};

template <class Key>
void write_histogram(
    std::ostream& output, const std::map<Key, std::uint64_t>& histogram,
    int indentation = 2
) {
    bool separator = false;
    for (const auto& [value, count] : histogram) {
        if (separator) output << ',';
        output << '\n' << std::string(indentation, ' ') << '"' << value
               << "\": " << count;
        separator = true;
    }
    output << '\n' << std::string(indentation - 2, ' ') << '}';
}

void write_state_array(
    std::ostream& output, const std::vector<State>& states, int indentation = 4
) {
    for (std::size_t index = 0; index < states.size(); ++index) {
        if (index) output << ",\n";
        output << std::string(indentation, ' ');
        Search::write_state(output, states[index]);
    }
}

void scan_objective_twelve_shadow(
    Search& search, const std::string& frontier_path,
    const std::string& component_path, const std::string& output_path
) {
    std::vector<State> all_sources = load_state_array(
        frontier_path, "objective_ten_rotation_representatives"
    );
    std::vector<State> additions = load_state_array(
        component_path, "additional_objective_10_rotation_representatives"
    );
    all_sources.insert(all_sources.end(), additions.begin(), additions.end());
    if (all_sources.size() != 128711)
        throw std::runtime_error("complete objective-ten source count mismatch");

    std::unordered_set<State, StateHash> complete_source_set;
    complete_source_set.reserve(140000);
    std::vector<State> shadow_sources;
    shadow_sources.reserve(348);
    std::map<int, std::uint64_t> minimum_above_ten_histogram;
    for (std::size_t index = 0; index < all_sources.size(); ++index) {
        if (index && index % 10000 == 0)
            std::cerr << "objective-twelve shadow detection: " << index << '/'
                      << all_sources.size() << " objective-ten sources\n";
        const State& source = all_sources[index];
        if (!(search.canonical(source) == source))
            throw std::runtime_error("noncanonical objective-ten source");
        search.require_free_orbit(source);
        if (!complete_source_set.insert(source).second)
            throw std::runtime_error("duplicate objective-ten source");
        search.move_to(source);
        if (search.monochromatic_count != 10)
            throw std::runtime_error("objective-ten source objective mismatch");
        int minimum = std::numeric_limits<int>::max();
        for (int id = 0; id < edge_count; ++id) {
            const int objective = search.resulting_count(id);
            if (objective > 10) minimum = std::min(minimum, objective);
        }
        if (minimum == std::numeric_limits<int>::max())
            throw std::runtime_error("objective-ten source has no higher exit");
        ++minimum_above_ten_histogram[minimum];
        if (minimum > 11) shadow_sources.push_back(source);
    }
    std::sort(shadow_sources.begin(), shadow_sources.end());
    if (shadow_sources.size() != 348 || minimum_above_ten_histogram[11] != 128363 ||
        minimum_above_ten_histogram[12] != 348 ||
        minimum_above_ten_histogram.size() != 2)
        throw std::runtime_error("objective-ten shadow census mismatch");

    std::unordered_set<State, StateHash> shadow_set(
        shadow_sources.begin(), shadow_sources.end()
    );
    std::unordered_map<State, TargetInfo, StateHash> target_info;
    target_info.reserve(10000);
    std::vector<std::size_t> source_distinct_degrees(shadow_sources.size());
    std::vector<std::uint64_t> source_quotient_incidences(shadow_sources.size());
    std::map<int, std::uint64_t> source_distinct_degree_histogram;
    std::map<int, std::uint64_t> source_incidence_histogram;
    for (std::size_t source_index = 0; source_index < shadow_sources.size();
         ++source_index) {
        search.move_to(shadow_sources[source_index]);
        std::unordered_map<State, std::uint16_t, StateHash> local;
        for (int id = 0; id < edge_count; ++id) {
            if (search.resulting_count(id) != 12) continue;
            State neighbor = search.state;
            neighbor.toggle(id);
            const State target = search.canonical(neighbor);
            search.require_free_orbit(neighbor);
            if (local[target] == std::numeric_limits<std::uint16_t>::max())
                throw std::runtime_error("source-target incidence overflow");
            ++local[target];
        }
        if (local.empty())
            throw std::runtime_error("shadow source has no objective-twelve exit");
        source_distinct_degrees[source_index] = local.size();
        for (const auto& [target, multiplicity] : local) {
            TargetInfo& info = target_info[target];
            info.quotient_incidence += multiplicity;
            info.source_indices.insert(source_index);
            source_quotient_incidences[source_index] += multiplicity;
        }
        ++source_distinct_degree_histogram[static_cast<int>(local.size())];
        ++source_incidence_histogram[
            static_cast<int>(source_quotient_incidences[source_index])
        ];
    }

    std::vector<State> targets;
    targets.reserve(target_info.size());
    for (const auto& [target, info] : target_info) {
        (void)info;
        targets.push_back(target);
    }
    std::sort(targets.begin(), targets.end());
    std::unordered_map<State, std::size_t, StateHash> target_indices;
    target_indices.reserve(targets.size());
    for (std::size_t index = 0; index < targets.size(); ++index)
        target_indices.emplace(targets[index], index);

    std::uint64_t quotient_incidence = 0;
    std::uint64_t unique_source_target_pairs = 0;
    std::vector<std::uint64_t> target_quotient_incidences(targets.size());
    std::vector<std::size_t> target_distinct_shadow_degrees(targets.size());
    std::map<int, std::uint64_t> target_shadow_degree_histogram;
    std::map<int, std::uint64_t> target_incidence_histogram;
    for (std::size_t index = 0; index < targets.size(); ++index) {
        const TargetInfo& info = target_info.at(targets[index]);
        target_quotient_incidences[index] = info.quotient_incidence;
        target_distinct_shadow_degrees[index] = info.source_indices.size();
        quotient_incidence += info.quotient_incidence;
        unique_source_target_pairs += info.source_indices.size();
        ++target_shadow_degree_histogram[
            static_cast<int>(info.source_indices.size())
        ];
        ++target_incidence_histogram[static_cast<int>(info.quotient_incidence)];
    }

    std::unordered_set<State, StateHash> all_objective_eleven_neighbors;
    std::unordered_set<State, StateHash> external_objective_ten_neighbors;
    std::unordered_set<State, StateHash> primary_nonshadow_neighbors;
    std::map<int, std::uint64_t> target_minimum_neighbor_histogram;
    std::map<int, std::uint64_t> target_distinct_q10_degree_histogram;
    std::map<int, std::uint64_t> target_primary_q10_degree_histogram;
    std::map<int, std::uint64_t> target_shadow_q10_degree_histogram;
    std::map<int, std::uint64_t> target_distinct_q11_degree_histogram;
    for (std::size_t target_index = 0; target_index < targets.size();
         ++target_index) {
        if (target_index && target_index % 1000 == 0)
            std::cerr << "objective-twelve target reverse scan: " << target_index
                      << '/' << targets.size() << " targets\n";
        const State& target = targets[target_index];
        search.move_to(target);
        if (search.monochromatic_count != 12)
            throw std::runtime_error("objective-twelve target objective mismatch");
        std::unordered_map<State, std::uint16_t, StateHash> reverse_shadow;
        std::unordered_set<State, StateHash> q10_neighbors;
        std::unordered_set<State, StateHash> primary_q10_neighbors;
        std::unordered_set<State, StateHash> q11_neighbors;
        int minimum_neighbor = std::numeric_limits<int>::max();
        for (int id = 0; id < edge_count; ++id) {
            const int objective = search.resulting_count(id);
            minimum_neighbor = std::min(minimum_neighbor, objective);
            if (objective != 10 && objective != 11) continue;
            State neighbor = search.state;
            neighbor.toggle(id);
            const State key = search.canonical(neighbor);
            search.require_free_orbit(neighbor);
            if (objective == 11) {
                q11_neighbors.insert(key);
                all_objective_eleven_neighbors.insert(key);
                continue;
            }
            q10_neighbors.insert(key);
            if (complete_source_set.contains(key)) {
                primary_q10_neighbors.insert(key);
                if (shadow_set.contains(key)) {
                    if (reverse_shadow[key] ==
                        std::numeric_limits<std::uint16_t>::max())
                        throw std::runtime_error("reverse incidence overflow");
                    ++reverse_shadow[key];
                } else {
                    primary_nonshadow_neighbors.insert(key);
                }
            } else {
                external_objective_ten_neighbors.insert(key);
            }
        }
        const TargetInfo& expected = target_info.at(target);
        if (reverse_shadow.size() != expected.source_indices.size())
            throw std::runtime_error("reverse shadow degree mismatch");
        std::uint64_t reverse_incidence = 0;
        for (const auto& [source, multiplicity] : reverse_shadow) {
            const auto position = std::lower_bound(
                shadow_sources.begin(), shadow_sources.end(), source
            );
            if (position == shadow_sources.end() || !(*position == source))
                throw std::runtime_error("reverse shadow source missing");
            const std::size_t source_index = position - shadow_sources.begin();
            if (!expected.source_indices.contains(source_index))
                throw std::runtime_error("reverse shadow source-set mismatch");
            reverse_incidence += multiplicity;
        }
        if (reverse_incidence != expected.quotient_incidence)
            throw std::runtime_error("reverse quotient incidence mismatch");
        ++target_minimum_neighbor_histogram[minimum_neighbor];
        ++target_distinct_q10_degree_histogram[
            static_cast<int>(q10_neighbors.size())
        ];
        ++target_primary_q10_degree_histogram[
            static_cast<int>(primary_q10_neighbors.size())
        ];
        ++target_shadow_q10_degree_histogram[
            static_cast<int>(reverse_shadow.size())
        ];
        ++target_distinct_q11_degree_histogram[
            static_cast<int>(q11_neighbors.size())
        ];
    }

    DisjointSet components(shadow_sources.size() + targets.size());
    for (std::size_t target_index = 0; target_index < targets.size();
         ++target_index)
        for (std::size_t source_index :
             target_info.at(targets[target_index]).source_indices)
            components.unite(
                source_index, shadow_sources.size() + target_index
            );
    struct ComponentSummary {
        std::uint64_t sources = 0;
        std::uint64_t targets = 0;
        std::uint64_t edges = 0;
    };
    std::unordered_map<std::size_t, ComponentSummary> component_by_root;
    for (std::size_t source_index = 0; source_index < shadow_sources.size();
         ++source_index)
        ++component_by_root[components.find(source_index)].sources;
    for (std::size_t target_index = 0; target_index < targets.size();
         ++target_index) {
        const std::size_t root = components.find(
            shadow_sources.size() + target_index
        );
        ComponentSummary& summary = component_by_root[root];
        ++summary.targets;
        summary.edges += target_info.at(targets[target_index]).source_indices.size();
    }
    std::vector<ComponentSummary> component_summaries;
    for (const auto& [root, summary] : component_by_root) {
        (void)root;
        component_summaries.push_back(summary);
    }
    std::sort(
        component_summaries.begin(), component_summaries.end(),
        [](const ComponentSummary& left, const ComponentSummary& right) {
            return std::tie(left.sources, left.targets, left.edges) >
                   std::tie(right.sources, right.targets, right.edges);
        }
    );
    std::uint64_t bipartite_cycle_rank = 0;
    for (const ComponentSummary& summary : component_summaries)
        bipartite_cycle_rank +=
            summary.edges - summary.sources - summary.targets + 1;

    std::ofstream output(output_path);
    if (!output) throw std::runtime_error("cannot write " + output_path);
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"complete_objective_ten_source_rotation_orbit_count\": "
           << all_sources.size() << ",\n";
    output << "  \"source_minimum_above_ten_objective_histogram\": {";
    write_histogram(output, minimum_above_ten_histogram, 4);
    output << ",\n  \"objective_ten_shadow_source_rotation_orbit_count\": "
           << shadow_sources.size() << ",\n";
    output << "  \"objective_ten_shadow_source_vertex_count\": "
           << orbit_size * shadow_sources.size() << ",\n";
    output << "  \"exact_shadow_one_flip_escape_objective\": 12,\n";
    output << "  \"objective_twelve_shadow_frontier_rotation_orbit_count\": "
           << targets.size() << ",\n";
    output << "  \"objective_twelve_shadow_frontier_vertex_count\": "
           << orbit_size * targets.size() << ",\n";
    output << "  \"shadow_to_objective_twelve_quotient_incidence\": "
           << quotient_incidence << ",\n";
    output << "  \"shadow_to_objective_twelve_labeled_incidence\": "
           << orbit_size * quotient_incidence << ",\n";
    output << "  \"distinct_shadow_source_target_pairs\": "
           << unique_source_target_pairs << ",\n";
    output << "  \"source_target_parallel_edge_excess\": "
           << quotient_incidence - unique_source_target_pairs << ",\n";
    output << "  \"source_distinct_objective_twelve_degree_histogram\": {";
    write_histogram(output, source_distinct_degree_histogram, 4);
    output << ",\n  \"source_objective_twelve_incidence_histogram\": {";
    write_histogram(output, source_incidence_histogram, 4);
    output << ",\n  \"target_distinct_shadow_source_degree_histogram\": {";
    write_histogram(output, target_shadow_degree_histogram, 4);
    output << ",\n  \"target_shadow_incidence_histogram\": {";
    write_histogram(output, target_incidence_histogram, 4);
    output << ",\n  \"target_minimum_one_flip_objective_histogram\": {";
    write_histogram(output, target_minimum_neighbor_histogram, 4);
    output << ",\n  \"target_distinct_objective_ten_neighbor_degree_histogram\": {";
    write_histogram(output, target_distinct_q10_degree_histogram, 4);
    output << ",\n  \"target_distinct_primary_objective_ten_neighbor_degree_histogram\": {";
    write_histogram(output, target_primary_q10_degree_histogram, 4);
    output << ",\n  \"target_distinct_shadow_neighbor_degree_histogram\": {";
    write_histogram(output, target_shadow_q10_degree_histogram, 4);
    output << ",\n  \"target_distinct_objective_eleven_neighbor_degree_histogram\": {";
    write_histogram(output, target_distinct_q11_degree_histogram, 4);
    output << ",\n  \"distinct_objective_eleven_neighbor_rotation_orbit_count\": "
           << all_objective_eleven_neighbors.size() << ",\n";
    output << "  \"distinct_primary_nonshadow_objective_ten_neighbor_rotation_orbit_count\": "
           << primary_nonshadow_neighbors.size() << ",\n";
    output << "  \"distinct_external_objective_ten_neighbor_rotation_orbit_count\": "
           << external_objective_ten_neighbors.size() << ",\n";
    output << "  \"shadow_boundary_bipartite_component_count\": "
           << component_summaries.size() << ",\n";
    output << "  \"shadow_boundary_bipartite_cycle_rank\": "
           << bipartite_cycle_rank << ",\n";
    output << "  \"shadow_boundary_bipartite_components\": [\n";
    for (std::size_t index = 0; index < component_summaries.size(); ++index) {
        if (index) output << ",\n";
        const ComponentSummary& item = component_summaries[index];
        output << "    {\"source_orbits\":" << item.sources
               << ",\"target_orbits\":" << item.targets
               << ",\"distinct_edges\":" << item.edges
               << ",\"cycle_rank\":"
               << item.edges - item.sources - item.targets + 1 << '}';
    }
    output << "\n  ],\n  \"objective_ten_shadow_rotation_representatives\": [\n";
    write_state_array(output, shadow_sources);
    output << "\n  ],\n  \"objective_twelve_shadow_frontier_rotation_representatives\": [\n";
    write_state_array(output, targets);
    output << "\n  ],\n  \"source_distinct_target_degrees\": [";
    for (std::size_t index = 0; index < source_distinct_degrees.size(); ++index) {
        if (index) output << ',';
        output << source_distinct_degrees[index];
    }
    output << "],\n  \"source_quotient_incidences\": [";
    for (std::size_t index = 0; index < source_quotient_incidences.size(); ++index) {
        if (index) output << ',';
        output << source_quotient_incidences[index];
    }
    output << "],\n  \"target_distinct_shadow_source_degrees\": [";
    for (std::size_t index = 0; index < target_distinct_shadow_degrees.size();
         ++index) {
        if (index) output << ',';
        output << target_distinct_shadow_degrees[index];
    }
    output << "],\n  \"target_shadow_quotient_incidences\": [";
    for (std::size_t index = 0; index < target_quotient_incidences.size();
         ++index) {
        if (index) output << ',';
        output << target_quotient_incidences[index];
    }
    output << "],\n";
    output << "  \"all_targets_reverse_verified\": true,\n";
    output << "  \"method\": \"incremental exact five-set deltas over every complete-P10 objective-ten source, followed by exact cyclic canonicalization and a reverse scan of every objective-twelve target\",\n";
    output << "  \"scope_note\": \"Complete one-flip objective-twelve boundary of the 348 objective-ten orbits in the certified primary threshold-ten component that have no objective-eleven exit; no threshold-twelve closure or classification of other objective-ten components is claimed.\"\n}\n";
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 5) {
        std::cerr
            << "usage: scan_objective_twelve_shadow CERTIFICATE.json "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OUTPUT.json\n";
        return 2;
    }
    Search search(load_flips(argv[1]));
    scan_objective_twelve_shadow(search, argv[2], argv[3], argv[4]);
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
