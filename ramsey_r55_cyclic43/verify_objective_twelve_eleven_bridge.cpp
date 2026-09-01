#define main verify_objective_ten_frontier_embedded_main
#include "verify_objective_ten_frontier.cpp"
#undef main

namespace {

struct DirectBridgeInfo {
    std::uint64_t incidence = 0;
    std::unordered_set<std::size_t> target_indices;
};

struct DirectDisjointSet {
    std::vector<std::size_t> parent;
    std::vector<std::size_t> size;

    explicit DirectDisjointSet(std::size_t count)
        : parent(count), size(count, 1) {
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
    std::ostream& output, const std::map<Key, std::uint64_t>& histogram
) {
    bool separator = false;
    for (const auto& [value, count] : histogram) {
        if (separator) output << ',';
        output << "\n    \"" << value << "\": " << count;
        separator = true;
    }
    output << "\n  }";
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 5) {
        std::cerr
            << "usage: verify_objective_twelve_eleven_bridge "
               "OBJECTIVE-TWELVE-SHADOW.json OBJECTIVE-ELEVEN-FRONTIER.json "
               "BRIDGE.json OUTPUT.json\n";
        return 2;
    }
    const std::vector<State> targets = load_states(
        argv[1], "objective_twelve_shadow_frontier_rotation_representatives"
    );
    const std::vector<State> first_frontier = load_states(
        argv[2], "objective_eleven_rotation_representatives"
    );
    const auto first_frontier_signatures = load_integer_arrays(
        argv[2], "objective_eleven_incidence_signatures_2_through_10"
    );
    const std::vector<State> claimed_bridge = load_states(
        argv[3], "objective_eleven_bridge_rotation_representatives"
    );
    const auto claimed_flags = load_integer_arrays(
        argv[3], "bridge_in_first_frontier_flags"
    );
    const auto claimed_target_degrees = load_integer_arrays(
        argv[3], "target_distinct_bridge_degrees"
    );
    const auto claimed_target_frontier_degrees = load_integer_arrays(
        argv[3], "target_first_frontier_bridge_degrees"
    );
    const auto claimed_target_outside_degrees = load_integer_arrays(
        argv[3], "target_outside_first_frontier_bridge_degrees"
    );
    const auto claimed_target_incidences = load_integer_arrays(
        argv[3], "target_bridge_quotient_incidences"
    );
    const auto claimed_bridge_degrees = load_integer_arrays(
        argv[3], "bridge_distinct_target_degrees"
    );
    const auto claimed_bridge_incidences = load_integer_arrays(
        argv[3], "bridge_quotient_incidences"
    );
    if (targets.size() != 2823 || first_frontier.size() != 372974 ||
        claimed_bridge.size() != 8696 || first_frontier_signatures.size() != 372974 ||
        claimed_flags.size() != 1 || claimed_target_degrees.size() != 1 ||
        claimed_target_frontier_degrees.size() != 1 ||
        claimed_target_outside_degrees.size() != 1 ||
        claimed_target_incidences.size() != 1 || claimed_bridge_degrees.size() != 1 ||
        claimed_bridge_incidences.size() != 1 ||
        claimed_flags[0].size() != claimed_bridge.size() ||
        claimed_target_degrees[0].size() != targets.size() ||
        claimed_target_frontier_degrees[0].size() != targets.size() ||
        claimed_target_outside_degrees[0].size() != targets.size() ||
        claimed_target_incidences[0].size() != targets.size() ||
        claimed_bridge_degrees[0].size() != claimed_bridge.size() ||
        claimed_bridge_incidences[0].size() != claimed_bridge.size())
        throw std::runtime_error("bridge input cardinality mismatch");
    for (const auto& signature : first_frontier_signatures)
        if (signature.size() != 9)
            throw std::runtime_error("first-frontier signature width mismatch");

    Model model;
    std::unordered_map<State, std::size_t, StateHash> first_frontier_index;
    std::unordered_map<State, std::size_t, StateHash> claimed_bridge_index;
    first_frontier_index.reserve(400000);
    claimed_bridge_index.reserve(10000);
    for (std::size_t index = 0; index < first_frontier.size(); ++index)
        if (!first_frontier_index.emplace(first_frontier[index], index).second)
            throw std::runtime_error("duplicate first-frontier state");
    for (std::size_t index = 0; index < claimed_bridge.size(); ++index)
        if (!claimed_bridge_index.emplace(claimed_bridge[index], index).second)
            throw std::runtime_error("duplicate claimed bridge state");
    for (const State& target : targets)
        if (!(model.canonical(target) == target) || !model.is_free(target))
            throw std::runtime_error("noncanonical or nonfree q12 target");

    struct TargetResult {
        int objective = 0;
        std::unordered_map<State, std::uint16_t, StateHash> q11;
    };
    std::vector<TargetResult> target_results(targets.size());
#pragma omp parallel for schedule(dynamic, 1)
    for (std::size_t target_index = 0; target_index < targets.size();
         ++target_index) {
        const Model::Analysis analysis = model.analyze(targets[target_index]);
        TargetResult& result = target_results[target_index];
        result.objective = analysis.objective;
        for (int id = 0; id < edge_count; ++id) {
            if (analysis.objective + analysis.delta[id] != 11) continue;
            State neighbor = targets[target_index];
            neighbor.toggle(id);
            const State key = model.canonical(neighbor);
            ++result.q11[key];
        }
    }

    std::unordered_map<State, DirectBridgeInfo, StateHash> bridge_info;
    bridge_info.reserve(10000);
    std::map<int, std::uint64_t> target_degree_histogram;
    std::map<int, std::uint64_t> target_frontier_degree_histogram;
    std::map<int, std::uint64_t> target_outside_degree_histogram;
    std::uint64_t target_objective_errors = 0;
    std::uint64_t target_alignment_errors = 0;
    std::uint64_t missing_claimed_bridge_states = 0;
    for (std::size_t target_index = 0; target_index < targets.size();
         ++target_index) {
        const TargetResult& result = target_results[target_index];
        if (result.objective != 12) ++target_objective_errors;
        std::size_t frontier_degree = 0;
        std::uint64_t incidence = 0;
        for (const auto& [state, multiplicity] : result.q11) {
            DirectBridgeInfo& info = bridge_info[state];
            info.incidence += multiplicity;
            info.target_indices.insert(target_index);
            incidence += multiplicity;
            if (first_frontier_index.contains(state)) ++frontier_degree;
            if (!claimed_bridge_index.contains(state)) ++missing_claimed_bridge_states;
        }
        const std::size_t outside_degree = result.q11.size() - frontier_degree;
        ++target_degree_histogram[static_cast<int>(result.q11.size())];
        ++target_frontier_degree_histogram[static_cast<int>(frontier_degree)];
        ++target_outside_degree_histogram[static_cast<int>(outside_degree)];
        if (result.q11.size() !=
                static_cast<std::size_t>(claimed_target_degrees[0][target_index]) ||
            frontier_degree != static_cast<std::size_t>(
                claimed_target_frontier_degrees[0][target_index]
            ) ||
            outside_degree != static_cast<std::size_t>(
                claimed_target_outside_degrees[0][target_index]
            ) ||
            incidence != static_cast<std::uint64_t>(
                claimed_target_incidences[0][target_index]
            ))
            ++target_alignment_errors;
    }

    std::vector<State> direct_bridge;
    direct_bridge.reserve(bridge_info.size());
    for (const auto& [state, info] : bridge_info) {
        (void)info;
        direct_bridge.push_back(state);
    }
    std::sort(direct_bridge.begin(), direct_bridge.end());
    std::map<int, std::uint64_t> bridge_degree_histogram;
    std::map<int, std::uint64_t> frontier_minimum_source_histogram;
    std::map<int, std::uint64_t> frontier_p10_degree_histogram;
    std::uint64_t bridge_alignment_errors = 0;
    std::uint64_t frontier_members = 0;
    std::uint64_t quotient_incidence = 0;
    std::uint64_t distinct_pairs = 0;
    for (std::size_t index = 0; index < direct_bridge.size(); ++index) {
        const State& state = direct_bridge[index];
        const DirectBridgeInfo& info = bridge_info.at(state);
        quotient_incidence += info.incidence;
        distinct_pairs += info.target_indices.size();
        ++bridge_degree_histogram[static_cast<int>(info.target_indices.size())];
        const auto claimed = claimed_bridge_index.find(state);
        if (claimed == claimed_bridge_index.end()) {
            ++bridge_alignment_errors;
            continue;
        }
        const bool in_frontier = first_frontier_index.contains(state);
        if (in_frontier) ++frontier_members;
        if (claimed_flags[0][claimed->second] != static_cast<int>(in_frontier) ||
            claimed_bridge_degrees[0][claimed->second] !=
                static_cast<int>(info.target_indices.size()) ||
            claimed_bridge_incidences[0][claimed->second] !=
                static_cast<int>(info.incidence))
            ++bridge_alignment_errors;
        if (!in_frontier) continue;
        const auto& signature = first_frontier_signatures[
            first_frontier_index.at(state)
        ];
        int minimum_source = 11;
        int degree = 0;
        for (int source = 2; source <= 10; ++source) {
            const int value = signature[source - 2];
            if (value) minimum_source = std::min(minimum_source, source);
            degree += value;
        }
        ++frontier_minimum_source_histogram[minimum_source];
        ++frontier_p10_degree_histogram[degree];
    }

    DirectDisjointSet components(targets.size() + direct_bridge.size());
    for (std::size_t bridge_position = 0; bridge_position < direct_bridge.size();
         ++bridge_position)
        for (std::size_t target_index :
             bridge_info.at(direct_bridge[bridge_position]).target_indices)
            components.unite(target_index, targets.size() + bridge_position);
    std::unordered_set<std::size_t> component_roots;
    for (std::size_t index = 0; index < targets.size() + direct_bridge.size();
         ++index)
        component_roots.insert(components.find(index));
    const std::uint64_t cycle_rank = distinct_pairs - targets.size() -
                                     direct_bridge.size() +
                                     component_roots.size();

    const bool direct_set_agrees = direct_bridge == claimed_bridge;
    std::ofstream output(argv[4]);
    if (!output) throw std::runtime_error("cannot write direct bridge result");
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"direct_five_set_recount_target_count\": " << targets.size()
           << ",\n";
    output << "  \"distinct_objective_eleven_bridge_rotation_orbit_count\": "
           << direct_bridge.size() << ",\n";
    output << "  \"bridge_in_first_objective_eleven_frontier_rotation_orbit_count\": "
           << frontier_members << ",\n";
    output << "  \"bridge_outside_first_objective_eleven_frontier_rotation_orbit_count\": "
           << direct_bridge.size() - frontier_members << ",\n";
    output << "  \"objective_twelve_to_eleven_quotient_incidence\": "
           << quotient_incidence << ",\n";
    output << "  \"distinct_objective_twelve_eleven_pairs\": "
           << distinct_pairs << ",\n";
    output << "  \"objective_twelve_eleven_parallel_edge_excess\": "
           << quotient_incidence - distinct_pairs << ",\n";
    output << "  \"target_distinct_bridge_degree_histogram\": {";
    write_histogram(output, target_degree_histogram);
    output << ",\n  \"target_first_frontier_bridge_degree_histogram\": {";
    write_histogram(output, target_frontier_degree_histogram);
    output << ",\n  \"target_outside_first_frontier_bridge_degree_histogram\": {";
    write_histogram(output, target_outside_degree_histogram);
    output << ",\n  \"bridge_distinct_target_degree_histogram\": {";
    write_histogram(output, bridge_degree_histogram);
    output << ",\n  \"first_frontier_bridge_minimum_p10_source_objective_histogram\": {";
    write_histogram(output, frontier_minimum_source_histogram);
    output << ",\n  \"first_frontier_bridge_p10_incidence_degree_histogram\": {";
    write_histogram(output, frontier_p10_degree_histogram);
    output << ",\n  \"bridge_bipartite_component_count\": "
           << component_roots.size() << ",\n";
    output << "  \"bridge_bipartite_cycle_rank\": " << cycle_rank << ",\n";
    output << "  \"target_objective_errors\": " << target_objective_errors
           << ",\n";
    output << "  \"missing_claimed_bridge_states\": "
           << missing_claimed_bridge_states << ",\n";
    output << "  \"target_aligned_array_errors\": " << target_alignment_errors
           << ",\n";
    output << "  \"bridge_aligned_array_errors\": " << bridge_alignment_errors
           << ",\n";
    output << "  \"direct_bridge_array_agrees_entry_for_entry\": "
           << (direct_set_agrees ? "true" : "false") << ",\n";
    output << "  \"all_direct_checks_pass\": "
           << ((target_objective_errors == 0 &&
                missing_claimed_bridge_states == 0 &&
                target_alignment_errors == 0 && bridge_alignment_errors == 0 &&
                direct_set_agrees)
                   ? "true"
                   : "false")
           << ",\n";
    output << "  \"method\": \"independent direct recount of all 962598 five-vertex sets at every objective-twelve target, followed by exact cyclic canonicalization, bridge reconstruction, and first-frontier set intersection\"\n}\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
