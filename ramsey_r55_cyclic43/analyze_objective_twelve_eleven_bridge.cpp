#define main objective_six_component_embedded_main
#include "objective_six_component.cpp"
#undef main

#include <tuple>

namespace {

struct BridgeInfo {
    std::uint64_t quotient_incidence = 0;
    std::unordered_set<std::size_t> target_indices;
};

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

template <class Key>
void write_histogram(
    std::ostream& output, const std::map<Key, std::uint64_t>& histogram,
    int indentation = 4
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

void write_states(std::ostream& output, const std::vector<State>& states) {
    for (std::size_t index = 0; index < states.size(); ++index) {
        if (index) output << ",\n";
        output << "    ";
        Search::write_state(output, states[index]);
    }
}

struct ComponentSummary {
    std::uint64_t target_orbits = 0;
    std::uint64_t bridge_orbits = 0;
    std::uint64_t first_frontier_orbits = 0;
    std::uint64_t outside_first_frontier_orbits = 0;
    std::uint64_t distinct_edges = 0;
};

void analyze_bridge(
    Search& search, const std::string& shadow_path,
    const std::string& objective_eleven_path, const std::string& output_path
) {
    const std::vector<State> targets = load_state_array(
        shadow_path,
        "objective_twelve_shadow_frontier_rotation_representatives"
    );
    if (targets.size() != 2823 || !std::is_sorted(targets.begin(), targets.end()))
        throw std::runtime_error("objective-twelve target certificate mismatch");

    const std::vector<State> first_frontier = load_state_array(
        objective_eleven_path, "objective_eleven_rotation_representatives"
    );
    const std::vector<int> flattened_signatures = load_integer_array(
        objective_eleven_path,
        "objective_eleven_incidence_signatures_2_through_10"
    );
    if (first_frontier.size() != 372974 ||
        !std::is_sorted(first_frontier.begin(), first_frontier.end()) ||
        flattened_signatures.size() != 9 * first_frontier.size())
        throw std::runtime_error("objective-eleven first-frontier mismatch");
    std::unordered_map<State, std::size_t, StateHash> first_frontier_index;
    first_frontier_index.reserve(400000);
    for (std::size_t index = 0; index < first_frontier.size(); ++index)
        if (!first_frontier_index.emplace(first_frontier[index], index).second)
            throw std::runtime_error("duplicate objective-eleven representative");

    std::unordered_map<State, BridgeInfo, StateHash> bridge_info;
    bridge_info.reserve(10000);
    std::vector<std::size_t> target_bridge_degrees(targets.size());
    std::vector<std::size_t> target_first_frontier_degrees(targets.size());
    std::vector<std::size_t> target_outside_degrees(targets.size());
    std::vector<std::uint64_t> target_bridge_incidences(targets.size());
    std::map<int, std::uint64_t> target_bridge_degree_histogram;
    std::map<int, std::uint64_t> target_first_frontier_degree_histogram;
    std::map<int, std::uint64_t> target_outside_degree_histogram;
    std::map<int, std::uint64_t> target_bridge_incidence_histogram;
    for (std::size_t target_index = 0; target_index < targets.size();
         ++target_index) {
        if (target_index && target_index % 1000 == 0)
            std::cerr << "objective-twelve/eleven bridge scan: " << target_index
                      << '/' << targets.size() << " targets\n";
        search.move_to(targets[target_index]);
        if (search.monochromatic_count != 12)
            throw std::runtime_error("bridge source is not objective twelve");
        std::unordered_map<State, std::uint16_t, StateHash> local;
        for (int id = 0; id < edge_count; ++id) {
            if (search.resulting_count(id) != 11) continue;
            State neighbor = search.state;
            neighbor.toggle(id);
            const State key = search.canonical(neighbor);
            search.require_free_orbit(neighbor);
            if (local[key] == std::numeric_limits<std::uint16_t>::max())
                throw std::runtime_error("bridge incidence overflow");
            ++local[key];
        }
        if (local.empty())
            throw std::runtime_error("objective-twelve target has no q11 neighbor");
        target_bridge_degrees[target_index] = local.size();
        for (const auto& [neighbor, multiplicity] : local) {
            BridgeInfo& info = bridge_info[neighbor];
            info.quotient_incidence += multiplicity;
            info.target_indices.insert(target_index);
            target_bridge_incidences[target_index] += multiplicity;
            if (first_frontier_index.contains(neighbor))
                ++target_first_frontier_degrees[target_index];
            else
                ++target_outside_degrees[target_index];
        }
        ++target_bridge_degree_histogram[static_cast<int>(local.size())];
        ++target_first_frontier_degree_histogram[
            static_cast<int>(target_first_frontier_degrees[target_index])
        ];
        ++target_outside_degree_histogram[
            static_cast<int>(target_outside_degrees[target_index])
        ];
        ++target_bridge_incidence_histogram[
            static_cast<int>(target_bridge_incidences[target_index])
        ];
    }
    if (bridge_info.size() != 8696)
        throw std::runtime_error("objective-eleven bridge cardinality mismatch");

    std::vector<State> bridge;
    bridge.reserve(bridge_info.size());
    for (const auto& [state, info] : bridge_info) {
        (void)info;
        bridge.push_back(state);
    }
    std::sort(bridge.begin(), bridge.end());
    std::unordered_map<State, std::size_t, StateHash> bridge_index;
    bridge_index.reserve(bridge.size());
    for (std::size_t index = 0; index < bridge.size(); ++index)
        bridge_index.emplace(bridge[index], index);

    std::vector<State> overlap;
    std::vector<State> outside;
    std::vector<std::size_t> bridge_target_degrees(bridge.size());
    std::vector<std::uint64_t> bridge_incidences(bridge.size());
    std::map<int, std::uint64_t> bridge_target_degree_histogram;
    std::map<int, std::uint64_t> bridge_incidence_histogram;
    std::map<int, std::uint64_t> overlap_target_degree_histogram;
    std::map<int, std::uint64_t> outside_target_degree_histogram;
    std::map<int, std::uint64_t> first_frontier_minimum_source_histogram;
    std::map<int, std::uint64_t> first_frontier_p10_degree_histogram;
    std::uint64_t quotient_incidence = 0;
    std::uint64_t distinct_pairs = 0;
    for (std::size_t index = 0; index < bridge.size(); ++index) {
        const State& state = bridge[index];
        const BridgeInfo& info = bridge_info.at(state);
        bridge_target_degrees[index] = info.target_indices.size();
        bridge_incidences[index] = info.quotient_incidence;
        quotient_incidence += info.quotient_incidence;
        distinct_pairs += info.target_indices.size();
        ++bridge_target_degree_histogram[
            static_cast<int>(info.target_indices.size())
        ];
        ++bridge_incidence_histogram[static_cast<int>(info.quotient_incidence)];
        const auto frontier_position = first_frontier_index.find(state);
        if (frontier_position == first_frontier_index.end()) {
            outside.push_back(state);
            ++outside_target_degree_histogram[
                static_cast<int>(info.target_indices.size())
            ];
            continue;
        }
        overlap.push_back(state);
        ++overlap_target_degree_histogram[
            static_cast<int>(info.target_indices.size())
        ];
        const std::size_t signature_offset = 9 * frontier_position->second;
        int minimum_source = 11;
        int degree = 0;
        for (int source = 2; source <= 10; ++source) {
            const int value = flattened_signatures[
                signature_offset + static_cast<std::size_t>(source - 2)
            ];
            if (value) minimum_source = std::min(minimum_source, source);
            degree += value;
        }
        if (minimum_source == 11 || degree == 0)
            throw std::runtime_error("empty first-frontier signature");
        ++first_frontier_minimum_source_histogram[minimum_source];
        ++first_frontier_p10_degree_histogram[degree];
    }

    DisjointSet components(targets.size() + bridge.size());
    for (std::size_t bridge_position = 0; bridge_position < bridge.size();
         ++bridge_position)
        for (std::size_t target_index :
             bridge_info.at(bridge[bridge_position]).target_indices)
            components.unite(target_index, targets.size() + bridge_position);
    std::unordered_map<std::size_t, ComponentSummary> summary_by_root;
    for (std::size_t target_index = 0; target_index < targets.size();
         ++target_index)
        ++summary_by_root[components.find(target_index)].target_orbits;
    for (std::size_t bridge_position = 0; bridge_position < bridge.size();
         ++bridge_position) {
        ComponentSummary& item = summary_by_root[
            components.find(targets.size() + bridge_position)
        ];
        ++item.bridge_orbits;
        item.distinct_edges +=
            bridge_info.at(bridge[bridge_position]).target_indices.size();
        if (first_frontier_index.contains(bridge[bridge_position]))
            ++item.first_frontier_orbits;
        else
            ++item.outside_first_frontier_orbits;
    }
    std::vector<ComponentSummary> component_summaries;
    for (const auto& [root, summary] : summary_by_root) {
        (void)root;
        component_summaries.push_back(summary);
    }
    std::sort(
        component_summaries.begin(), component_summaries.end(),
        [](const ComponentSummary& left, const ComponentSummary& right) {
            return std::tie(
                       left.target_orbits, left.bridge_orbits,
                       left.distinct_edges
                   ) >
                   std::tie(
                       right.target_orbits, right.bridge_orbits,
                       right.distinct_edges
                   );
        }
    );
    std::uint64_t cycle_rank = 0;
    for (const ComponentSummary& item : component_summaries)
        cycle_rank += item.distinct_edges - item.target_orbits -
                      item.bridge_orbits + 1;
    using ComponentProfile = std::array<std::uint64_t, 6>;
    std::map<ComponentProfile, std::uint64_t> component_profile_histogram;
    for (const ComponentSummary& item : component_summaries)
        ++component_profile_histogram[{
            item.target_orbits,
            item.bridge_orbits,
            item.first_frontier_orbits,
            item.outside_first_frontier_orbits,
            item.distinct_edges,
            item.distinct_edges - item.target_orbits - item.bridge_orbits + 1,
        }];

    std::ofstream output(output_path);
    if (!output) throw std::runtime_error("cannot write " + output_path);
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"objective_twelve_shadow_boundary_rotation_orbit_count\": "
           << targets.size() << ",\n";
    output << "  \"objective_eleven_first_frontier_rotation_orbit_count\": "
           << first_frontier.size() << ",\n";
    output << "  \"distinct_objective_eleven_bridge_rotation_orbit_count\": "
           << bridge.size() << ",\n";
    output << "  \"bridge_in_first_objective_eleven_frontier_rotation_orbit_count\": "
           << overlap.size() << ",\n";
    output << "  \"bridge_outside_first_objective_eleven_frontier_rotation_orbit_count\": "
           << outside.size() << ",\n";
    output << "  \"objective_twelve_to_eleven_quotient_incidence\": "
           << quotient_incidence << ",\n";
    output << "  \"objective_twelve_to_eleven_labeled_incidence\": "
           << orbit_size * quotient_incidence << ",\n";
    output << "  \"distinct_objective_twelve_eleven_pairs\": "
           << distinct_pairs << ",\n";
    output << "  \"objective_twelve_eleven_parallel_edge_excess\": "
           << quotient_incidence - distinct_pairs << ",\n";
    output << "  \"target_distinct_bridge_degree_histogram\": {";
    write_histogram(output, target_bridge_degree_histogram);
    output << ",\n  \"target_first_frontier_bridge_degree_histogram\": {";
    write_histogram(output, target_first_frontier_degree_histogram);
    output << ",\n  \"target_outside_first_frontier_bridge_degree_histogram\": {";
    write_histogram(output, target_outside_degree_histogram);
    output << ",\n  \"target_bridge_incidence_histogram\": {";
    write_histogram(output, target_bridge_incidence_histogram);
    output << ",\n  \"bridge_distinct_target_degree_histogram\": {";
    write_histogram(output, bridge_target_degree_histogram);
    output << ",\n  \"bridge_incidence_histogram\": {";
    write_histogram(output, bridge_incidence_histogram);
    output << ",\n  \"first_frontier_bridge_distinct_target_degree_histogram\": {";
    write_histogram(output, overlap_target_degree_histogram);
    output << ",\n  \"outside_first_frontier_bridge_distinct_target_degree_histogram\": {";
    write_histogram(output, outside_target_degree_histogram);
    output << ",\n  \"first_frontier_bridge_minimum_p10_source_objective_histogram\": {";
    write_histogram(output, first_frontier_minimum_source_histogram);
    output << ",\n  \"first_frontier_bridge_p10_incidence_degree_histogram\": {";
    write_histogram(output, first_frontier_p10_degree_histogram);
    output << ",\n  \"bridge_bipartite_component_count\": "
           << component_summaries.size() << ",\n";
    output << "  \"bridge_bipartite_cycle_rank\": " << cycle_rank << ",\n";
    const ComponentSummary& largest = component_summaries.front();
    output << "  \"largest_bridge_bipartite_component\": {"
           << "\"objective_twelve_orbits\":" << largest.target_orbits
           << ",\"objective_eleven_orbits\":" << largest.bridge_orbits
           << ",\"first_frontier_orbits\":" << largest.first_frontier_orbits
           << ",\"outside_first_frontier_orbits\":"
           << largest.outside_first_frontier_orbits
           << ",\"distinct_edges\":" << largest.distinct_edges
           << ",\"cycle_rank\":"
           << largest.distinct_edges - largest.target_orbits -
                  largest.bridge_orbits + 1
           << "},\n";
    output << "  \"bridge_bipartite_component_profile_histogram\": [\n";
    bool profile_separator = false;
    for (const auto& [profile, count] : component_profile_histogram) {
        if (profile_separator) output << ",\n";
        output << "    {\"objective_twelve_orbits\":" << profile[0]
               << ",\"objective_eleven_orbits\":" << profile[1]
               << ",\"first_frontier_orbits\":" << profile[2]
               << ",\"outside_first_frontier_orbits\":" << profile[3]
               << ",\"distinct_edges\":" << profile[4]
               << ",\"cycle_rank\":" << profile[5]
               << ",\"component_count\":" << count << '}';
        profile_separator = true;
    }
    output << "\n  ],\n  \"objective_eleven_bridge_rotation_representatives\": [\n";
    write_states(output, bridge);
    output << "\n  ],\n  \"bridge_in_first_frontier_flags\": [";
    for (std::size_t index = 0; index < bridge.size(); ++index) {
        if (index) output << ',';
        output << (first_frontier_index.contains(bridge[index]) ? 1 : 0);
    }
    output << "],\n  \"target_distinct_bridge_degrees\": [";
    for (std::size_t index = 0; index < target_bridge_degrees.size(); ++index) {
        if (index) output << ',';
        output << target_bridge_degrees[index];
    }
    output << "],\n  \"target_first_frontier_bridge_degrees\": [";
    for (std::size_t index = 0; index < target_first_frontier_degrees.size();
         ++index) {
        if (index) output << ',';
        output << target_first_frontier_degrees[index];
    }
    output << "],\n  \"target_outside_first_frontier_bridge_degrees\": [";
    for (std::size_t index = 0; index < target_outside_degrees.size(); ++index) {
        if (index) output << ',';
        output << target_outside_degrees[index];
    }
    output << "],\n  \"target_bridge_quotient_incidences\": [";
    for (std::size_t index = 0; index < target_bridge_incidences.size(); ++index) {
        if (index) output << ',';
        output << target_bridge_incidences[index];
    }
    output << "],\n  \"bridge_distinct_target_degrees\": [";
    for (std::size_t index = 0; index < bridge_target_degrees.size(); ++index) {
        if (index) output << ',';
        output << bridge_target_degrees[index];
    }
    output << "],\n  \"bridge_quotient_incidences\": [";
    for (std::size_t index = 0; index < bridge_incidences.size(); ++index) {
        if (index) output << ',';
        output << bridge_incidences[index];
    }
    output << "],\n";
    output << "  \"method\": \"incremental exact five-set-delta scan of every objective-twelve shadow-boundary target, exact cyclic canonicalization, and set intersection with the complete certified first objective-eleven frontier\",\n";
    output << "  \"scope_note\": \"Classifies the two-step q10-shadow to q12 to q11 interface relative to the certified first q11 frontier; it does not assert threshold-eleven closure or reachability of q11 bridge orbits outside that first frontier.\"\n}\n";
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 5) {
        std::cerr
            << "usage: analyze_objective_twelve_eleven_bridge CERTIFICATE.json "
               "OBJECTIVE-TWELVE-SHADOW.json OBJECTIVE-ELEVEN-FRONTIER.json "
               "OUTPUT.json\n";
        return 2;
    }
    Search search(load_flips(argv[1]));
    analyze_bridge(search, argv[2], argv[3], argv[4]);
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
