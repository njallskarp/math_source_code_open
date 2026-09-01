#define main verify_objective_ten_frontier_embedded_main
#include "verify_objective_ten_frontier.cpp"
#undef main

namespace {

template <class Key>
void write_histogram(
    std::ostream& output, const std::map<Key, std::uint64_t>& histogram
) {
    bool separator = false;
    for (const auto& [value, count] : histogram) {
        if (separator) output << ',';
        output << '\n' << "    \"" << value << "\": " << count;
        separator = true;
    }
    output << "\n  }";
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 11) {
        std::cerr
            << "usage: verify_objective_eleven_component LOWER-SIX.json "
               "OBJECTIVE-SEVEN-COMPONENT.json OBJECTIVE-EIGHT-COMPONENT.json "
               "OBJECTIVE-NINE-COMPONENT.json OBJECTIVE-TEN-FRONTIER.json "
               "OBJECTIVE-TEN-COMPONENT.json OBJECTIVE-ELEVEN-FRONTIER.json "
               "FIRST-EXPANSION.json COMPONENT.json OUTPUT.json\n";
        return 2;
    }
    Model model;
    std::array<std::unordered_set<State, StateHash>, 12> primary;
    auto add_primary = [&](int objective, const std::string& path,
                           const std::string& key) {
        for (const State& state : load_states(path, key)) {
            if (!(model.canonical(state) == state) || !model.is_free(state) ||
                !primary[objective].insert(state).second)
                throw std::runtime_error("invalid primary source certificate");
        }
    };
    for (int objective = 2; objective <= 6; ++objective)
        add_primary(
            objective, argv[1],
            "objective_" + std::to_string(objective) +
                "_rotation_representatives"
        );
    add_primary(
        7, argv[2], "objective_seven_component_rotation_representatives"
    );
    add_primary(
        8, argv[3], "objective_eight_component_rotation_representatives"
    );
    add_primary(7, argv[4], "new_objective_7_rotation_representatives");
    add_primary(8, argv[4], "new_objective_8_rotation_representatives");
    add_primary(9, argv[4], "new_objective_9_rotation_representatives");
    add_primary(10, argv[5], "objective_ten_rotation_representatives");
    add_primary(
        10, argv[6], "additional_objective_10_rotation_representatives"
    );

    const std::vector<State> first_frontier = load_states(
        argv[7], "objective_eleven_rotation_representatives"
    );
    if (first_frontier.size() != 372974)
        throw std::runtime_error("objective-eleven first frontier mismatch");
    const std::unordered_set<State, StateHash> first_frontier_set(
        first_frontier.begin(), first_frontier.end()
    );
    if (first_frontier_set.size() != first_frontier.size())
        throw std::runtime_error("duplicate first-frontier state");

    const std::vector<State> seeds = load_states(
        argv[8], "new_objective_11_rotation_representatives"
    );
    const std::vector<State> expected = load_states(
        argv[9], "complete_additional_objective_11_rotation_representatives"
    );
    if (seeds.size() != 148 || expected.size() != 150)
        throw std::runtime_error("closure input count mismatch");
    std::unordered_set<State, StateHash> additions;
    additions.reserve(200);
    std::vector<State> queue;
    for (const State& state : seeds) {
        if (!(model.canonical(state) == state) || !model.is_free(state) ||
            !additions.insert(state).second)
            throw std::runtime_error("invalid closure seed");
        queue.push_back(state);
    }

    std::uint64_t objective_errors = 0;
    std::uint64_t orbit_errors = 0;
    std::uint64_t discovered_after_first_expansion = 0;
    std::size_t next = 0;
    while (next < queue.size()) {
        const State source = queue[next++];
        const Model::Analysis analysis = model.analyze(source);
        if (analysis.objective != 11) ++objective_errors;
        for (int id = 0; id < edge_count; ++id) {
            const int objective = analysis.objective + analysis.delta[id];
            if (objective > 11) continue;
            State neighbor = source;
            neighbor.toggle(id);
            const State key = model.canonical(neighbor);
            if (!model.is_free(neighbor)) ++orbit_errors;
            if (objective <= 10 && primary[objective].contains(key)) continue;
            if (objective == 11 && first_frontier_set.contains(key)) continue;
            if (objective != 11) {
                ++objective_errors;
                continue;
            }
            if (!additions.insert(key).second) continue;
            queue.push_back(key);
            ++discovered_after_first_expansion;
        }
    }

    std::unordered_set<State, StateHash> expected_set(
        expected.begin(), expected.end()
    );
    std::uint64_t omitted_expected_states = 0;
    std::uint64_t unexpected_states = 0;
    for (const State& state : expected_set)
        if (!additions.contains(state)) ++omitted_expected_states;
    for (const State& state : additions)
        if (!expected_set.contains(state)) ++unexpected_states;

    std::uint64_t to_primary = 0;
    std::uint64_t to_first_frontier = 0;
    std::uint64_t directed_inside_addition = 0;
    std::uint64_t outside_above_eleven = 0;
    std::uint64_t omitted_sublevel_neighbors = 0;
    std::map<int, std::uint64_t> minimum_neighbor_histogram;
    std::map<int, std::uint64_t> external_minimum_histogram;
    for (const State& source : additions) {
        const Model::Analysis analysis = model.analyze(source);
        if (analysis.objective != 11) ++objective_errors;
        int minimum_neighbor = std::numeric_limits<int>::max();
        int minimum_external = std::numeric_limits<int>::max();
        for (int id = 0; id < edge_count; ++id) {
            const int objective = analysis.objective + analysis.delta[id];
            minimum_neighbor = std::min(minimum_neighbor, objective);
            State neighbor = source;
            neighbor.toggle(id);
            const State key = model.canonical(neighbor);
            if (objective <= 10 && primary[objective].contains(key)) {
                ++to_primary;
                continue;
            }
            if (objective == 11 && first_frontier_set.contains(key)) {
                ++to_first_frontier;
                continue;
            }
            if (objective == 11 && additions.contains(key)) {
                ++directed_inside_addition;
                continue;
            }
            if (objective <= 11) {
                ++omitted_sublevel_neighbors;
                continue;
            }
            minimum_external = std::min(minimum_external, objective);
            ++outside_above_eleven;
        }
        ++minimum_neighbor_histogram[minimum_neighbor];
        ++external_minimum_histogram[minimum_external];
    }

    std::ofstream output(argv[10]);
    if (!output) throw std::runtime_error("cannot write direct output");
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"direct_five_set_recount_seed_count\": " << seeds.size()
           << ",\n";
    output << "  \"direct_closure_addition_rotation_orbit_count\": "
           << additions.size() << ",\n";
    output << "  \"discovered_after_first_expansion\": "
           << discovered_after_first_expansion << ",\n";
    output << "  \"added_to_primary_quotient_incidence\": " << to_primary
           << ",\n";
    output << "  \"added_to_first_frontier_quotient_incidence\": "
           << to_first_frontier << ",\n";
    output << "  \"directed_inside_addition_quotient_incidence\": "
           << directed_inside_addition << ",\n";
    output << "  \"directed_outside_above_eleven_from_addition\": "
           << outside_above_eleven << ",\n";
    output << "  \"added_source_minimum_neighbor_objective_histogram\": {";
    write_histogram(output, minimum_neighbor_histogram);
    output << ",\n  \"added_source_external_minimum_objective_histogram\": {";
    write_histogram(output, external_minimum_histogram);
    output << ",\n  \"omitted_expected_states\": " << omitted_expected_states
           << ",\n";
    output << "  \"unexpected_states\": " << unexpected_states << ",\n";
    output << "  \"omitted_sublevel_neighbors\": "
           << omitted_sublevel_neighbors << ",\n";
    output << "  \"objective_errors\": " << objective_errors << ",\n";
    output << "  \"canonical_or_orbit_errors\": " << orbit_errors << ",\n";
    output << "  \"all_direct_checks_pass\": "
           << ((omitted_expected_states == 0 && unexpected_states == 0 &&
                omitted_sublevel_neighbors == 0 && objective_errors == 0 &&
                orbit_errors == 0 && additions.size() == 150 &&
                discovered_after_first_expansion == 2)
                   ? "true"
                   : "false")
           << ",\n";
    output << "  \"method\": \"independent direct enumeration of all 962,598 five-sets at every closure-addition source, followed by a separately implemented exact cyclic breadth-first closure and complete representative-set comparison\"\n}\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
