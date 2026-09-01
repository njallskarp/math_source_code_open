#define main objective_six_component_embedded_main
#include "objective_six_component.cpp"
#undef main

namespace {

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

std::uint64_t load_u64_scalar(
    const std::string& path, const std::string& key
) {
    const std::string text = read_text(path);
    const std::regex pattern(
        '"' + key + '"' + std::string(R"(\s*:\s*([0-9]+))")
    );
    std::smatch match;
    if (!std::regex_search(text, match, pattern))
        throw std::runtime_error("missing scalar " + key);
    return std::stoull(match[1]);
}

void write_states(
    std::ostream& output, const std::vector<State>& states, int indentation = 4
) {
    for (std::size_t index = 0; index < states.size(); ++index) {
        if (index) output << ",\n";
        output << std::string(indentation, ' ');
        Search::write_state(output, states[index]);
    }
}

void close_component(
    Search& search, const std::string& lower_six_path,
    const std::string& objective_seven_path,
    const std::string& objective_eight_path,
    const std::string& objective_nine_path,
    const std::string& objective_ten_frontier_path,
    const std::string& objective_ten_component_path,
    const std::string& objective_eleven_frontier_path,
    const std::string& first_expansion_path, const std::string& output_path
) {
    std::array<std::unordered_set<State, StateHash>, 12> primary;
    auto add_primary = [&](int objective, const std::string& path,
                           const std::string& key) {
        for (const State& state : load_state_array(path, key)) {
            if (!(search.canonical(state) == state) ||
                !primary[objective].insert(state).second)
                throw std::runtime_error("invalid primary source certificate");
            search.require_free_orbit(state);
        }
    };
    for (int objective = 2; objective <= 6; ++objective)
        add_primary(
            objective, lower_six_path,
            "objective_" + std::to_string(objective) +
                "_rotation_representatives"
        );
    add_primary(
        7, objective_seven_path,
        "objective_seven_component_rotation_representatives"
    );
    add_primary(
        8, objective_eight_path,
        "objective_eight_component_rotation_representatives"
    );
    add_primary(
        7, objective_nine_path, "new_objective_7_rotation_representatives"
    );
    add_primary(
        8, objective_nine_path, "new_objective_8_rotation_representatives"
    );
    add_primary(
        9, objective_nine_path, "new_objective_9_rotation_representatives"
    );
    add_primary(
        10, objective_ten_frontier_path,
        "objective_ten_rotation_representatives"
    );
    add_primary(
        10, objective_ten_component_path,
        "additional_objective_10_rotation_representatives"
    );

    std::vector<State> first_frontier = load_state_array(
        objective_eleven_frontier_path,
        "objective_eleven_rotation_representatives"
    );
    if (first_frontier.size() != 372974)
        throw std::runtime_error("objective-eleven first frontier mismatch");
    std::unordered_set<State, StateHash> first_frontier_set(
        first_frontier.begin(), first_frontier.end()
    );
    if (first_frontier_set.size() != first_frontier.size())
        throw std::runtime_error("duplicate objective-eleven frontier state");

    std::array<std::unordered_set<State, StateHash>, 12> additions;
    std::vector<std::pair<int, State>> queue;
    const std::string expansion_text = read_text(first_expansion_path);
    for (int objective = 0; objective <= 11; ++objective) {
        const std::string key =
            "new_objective_" + std::to_string(objective) +
            "_rotation_representatives";
        if (expansion_text.find('"' + key + '"') == std::string::npos) continue;
        for (const State& state : load_state_array(first_expansion_path, key)) {
            if (!(search.canonical(state) == state) ||
                !additions[objective].insert(state).second)
                throw std::runtime_error("invalid first-expansion state");
            search.require_free_orbit(state);
            queue.push_back({objective, state});
        }
    }
    const std::size_t initial_addition_count = queue.size();
    if (initial_addition_count != 148 || additions[11].size() != 148)
        throw std::runtime_error("first expansion seed mismatch");

    std::map<int, std::uint64_t> discovery_count_by_objective;
    std::size_t next = 0;
    while (next < queue.size()) {
        if (next && next % 10000 == 0)
            std::cerr << "objective-eleven closure: " << next << '/'
                      << queue.size() << " added states\n";
        const auto [source_objective, source] = queue[next++];
        search.move_to(source);
        if (search.monochromatic_count != source_objective)
            throw std::runtime_error("closure source objective mismatch");
        for (int id = 0; id < edge_count; ++id) {
            const int objective = search.resulting_count(id);
            if (objective > 11) continue;
            State neighbor = search.state;
            neighbor.toggle(id);
            const State key = search.canonical(neighbor);
            search.require_free_orbit(neighbor);
            if (objective <= 10 && primary[objective].contains(key)) continue;
            if (objective == 11 && first_frontier_set.contains(key)) continue;
            if (!additions[objective].insert(key).second) continue;
            queue.push_back({objective, key});
            ++discovery_count_by_objective[objective];
        }
    }

    std::map<int, std::uint64_t> final_addition_count_by_objective;
    std::map<int, std::uint64_t> added_source_minimum_neighbor_histogram;
    std::map<int, std::uint64_t> added_source_external_minimum_histogram;
    std::uint64_t added_to_primary = 0;
    std::uint64_t added_to_first_frontier = 0;
    std::uint64_t directed_inside_addition = 0;
    std::uint64_t directed_outside_above_eleven = 0;
    for (int objective = 0; objective <= 11; ++objective) {
        final_addition_count_by_objective[objective] =
            additions[objective].size();
        if (additions[objective].empty())
            final_addition_count_by_objective.erase(objective);
        for (const State& source : additions[objective]) {
            search.move_to(source);
            if (search.monochromatic_count != objective)
                throw std::runtime_error("addition objective mismatch");
            int minimum_neighbor = std::numeric_limits<int>::max();
            int minimum_external = std::numeric_limits<int>::max();
            for (int id = 0; id < edge_count; ++id) {
                const int target_objective = search.resulting_count(id);
                minimum_neighbor = std::min(minimum_neighbor, target_objective);
                State neighbor = search.state;
                neighbor.toggle(id);
                const State key = search.canonical(neighbor);
                if (target_objective <= 10 &&
                    primary[target_objective].contains(key)) {
                    ++added_to_primary;
                    continue;
                }
                if (target_objective == 11 &&
                    first_frontier_set.contains(key)) {
                    ++added_to_first_frontier;
                    continue;
                }
                if (target_objective <= 11 &&
                    additions[target_objective].contains(key)) {
                    ++directed_inside_addition;
                    continue;
                }
                if (target_objective <= 11)
                    throw std::runtime_error("closure omitted a sublevel state");
                minimum_external = std::min(minimum_external, target_objective);
                ++directed_outside_above_eleven;
            }
            ++added_source_minimum_neighbor_histogram[minimum_neighbor];
            ++added_source_external_minimum_histogram[minimum_external];
        }
    }
    if (directed_inside_addition % 2 != 0)
        throw std::runtime_error("odd internal addition incidence");

    const std::uint64_t frontier_to_primary = load_u64_scalar(
        first_expansion_path,
        "directed_quotient_moves_to_primary_sublevel_ten"
    );
    const std::uint64_t frontier_internal_directed = load_u64_scalar(
        first_expansion_path,
        "directed_quotient_moves_inside_first_frontier"
    );
    const std::uint64_t frontier_to_addition = load_u64_scalar(
        first_expansion_path, "directed_quotient_moves_to_new_states"
    );
    if (frontier_to_addition != added_to_first_frontier)
        throw std::runtime_error("frontier-addition reverse incidence mismatch");

    std::uint64_t addition_orbits = 0;
    for (const auto& [objective, count] : final_addition_count_by_objective) {
        (void)objective;
        addition_orbits += count;
    }
    const std::uint64_t complete_vertex_count =
        8215881 + orbit_size * (first_frontier.size() + addition_orbits);
    const std::uint64_t complete_edge_count =
        42320815 + orbit_size *
            (frontier_to_primary + frontier_internal_directed / 2 +
             added_to_primary + added_to_first_frontier +
             directed_inside_addition / 2);

    std::ofstream output(output_path);
    if (!output) throw std::runtime_error("cannot write " + output_path);
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"initial_first_expansion_rotation_orbit_count\": "
           << initial_addition_count << ",\n";
    output << "  \"additional_discoveries_after_first_expansion_by_objective\": {";
    write_histogram(output, discovery_count_by_objective);
    output << ",\n  \"complete_closure_addition_rotation_orbit_count_by_objective\": {";
    write_histogram(output, final_addition_count_by_objective);
    output << ",\n  \"complete_objective_eleven_rotation_orbit_count\": "
           << first_frontier.size() + additions[11].size() << ",\n";
    output << "  \"complete_objective_eleven_vertex_count\": "
           << orbit_size * (first_frontier.size() + additions[11].size())
           << ",\n";
    output << "  \"complete_primary_sublevel_eleven_vertex_count\": "
           << complete_vertex_count << ",\n";
    output << "  \"complete_primary_sublevel_eleven_edge_count\": "
           << complete_edge_count << ",\n";
    output << "  \"added_to_primary_quotient_incidence\": "
           << added_to_primary << ",\n";
    output << "  \"added_to_first_frontier_quotient_incidence\": "
           << added_to_first_frontier << ",\n";
    output << "  \"directed_inside_addition_quotient_incidence\": "
           << directed_inside_addition << ",\n";
    output << "  \"undirected_inside_addition_quotient_edges\": "
           << directed_inside_addition / 2 << ",\n";
    output << "  \"directed_outside_above_eleven_from_addition\": "
           << directed_outside_above_eleven << ",\n";
    output << "  \"added_source_minimum_neighbor_objective_histogram\": {";
    write_histogram(output, added_source_minimum_neighbor_histogram);
    output << ",\n  \"added_source_external_minimum_objective_histogram\": {";
    write_histogram(output, added_source_external_minimum_histogram);
    output << ",\n  \"exact_escape_objective\": 12,\n";
    bool separator = false;
    for (int objective = 0; objective <= 11; ++objective) {
        if (additions[objective].empty()) continue;
        if (separator) output << ",\n";
        std::vector<State> states(
            additions[objective].begin(), additions[objective].end()
        );
        std::sort(states.begin(), states.end());
        output << "  \"complete_additional_objective_" << objective
               << "_rotation_representatives\": [\n";
        write_states(output, states);
        output << "\n  ]";
        separator = true;
    }
    if (separator) output << ",\n";
    output << "  \"method\": \"exact orbit-canonical breadth-first closure from the complete first-expansion addition under every one-edge move of objective at most eleven, followed by a complete reverse edge recount\",\n";
    output << "  \"scope_note\": \"Complete connected threshold-eleven component through the certified Cyclic(43) optimum; disconnected sublevel-eleven components remain out of scope.\"\n}\n";
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 11) {
        std::cerr
            << "usage: close_objective_eleven_component CERTIFICATE.json "
               "LOWER-SIX.json OBJECTIVE-SEVEN-COMPONENT.json "
               "OBJECTIVE-EIGHT-COMPONENT.json OBJECTIVE-NINE-COMPONENT.json "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OBJECTIVE-ELEVEN-FRONTIER.json FIRST-EXPANSION.json "
               "OUTPUT.json\n";
        return 2;
    }
    Search search(load_flips(argv[1]));
    close_component(
        search, argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8],
        argv[9], argv[10]
    );
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
