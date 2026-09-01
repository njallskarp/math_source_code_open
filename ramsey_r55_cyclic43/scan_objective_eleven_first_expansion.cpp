#define main objective_six_component_embedded_main
#include "objective_six_component.cpp"
#undef main

#include <tuple>

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

void write_states(
    std::ostream& output, const std::vector<State>& states, int indentation = 4
) {
    for (std::size_t index = 0; index < states.size(); ++index) {
        if (index) output << ",\n";
        output << std::string(indentation, ' ');
        Search::write_state(output, states[index]);
    }
}

struct TargetInfo {
    int objective = -1;
    std::uint64_t quotient_incidence = 0;
    std::unordered_set<std::size_t> sources;
};

void scan_first_expansion(
    Search& search, const std::string& lower_six_path,
    const std::string& objective_seven_path,
    const std::string& objective_eight_path,
    const std::string& objective_nine_path,
    const std::string& objective_ten_frontier_path,
    const std::string& objective_ten_component_path,
    const std::string& objective_eleven_frontier_path,
    const std::string& output_path
) {
    std::array<std::unordered_set<State, StateHash>, 11> primary;
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
    const std::array<std::size_t, 11> expected = {
        0, 0, 2, 17, 78, 306, 1183, 4218, 13771, 42781, 128711
    };
    for (int objective = 2; objective <= 10; ++objective)
        if (primary[objective].size() != expected[objective])
            throw std::runtime_error("primary source layer count mismatch");

    std::vector<State> sources = load_state_array(
        objective_eleven_frontier_path,
        "objective_eleven_rotation_representatives"
    );
    if (sources.size() != 372974)
        throw std::runtime_error("objective-eleven frontier count mismatch");
    if (!std::is_sorted(sources.begin(), sources.end()) ||
        std::adjacent_find(sources.begin(), sources.end()) != sources.end())
        throw std::runtime_error("objective-eleven frontier is not sorted unique");
    std::unordered_set<State, StateHash> frontier(sources.begin(), sources.end());
    if (frontier.size() != sources.size())
        throw std::runtime_error("objective-eleven frontier set mismatch");

    std::unordered_map<State, TargetInfo, StateHash> additions;
    additions.reserve(100000);
    std::map<int, std::uint64_t> directed_neighbor_objective_histogram;
    std::map<int, std::uint64_t> source_minimum_neighbor_histogram;
    std::map<int, std::uint64_t> source_distinct_new_degree_histogram;
    std::map<int, std::uint64_t> source_new_incidence_histogram;
    std::uint64_t directed_to_primary = 0;
    std::uint64_t directed_inside_frontier = 0;
    std::uint64_t directed_to_new = 0;
    std::uint64_t new_lower_incidence = 0;
    std::uint64_t new_eleven_incidence = 0;

    for (std::size_t source_index = 0; source_index < sources.size();
         ++source_index) {
        if (source_index && source_index % 10000 == 0)
            std::cerr << "objective-eleven first expansion: " << source_index
                      << '/' << sources.size() << " sources\n";
        const State& source = sources[source_index];
        if (!(search.canonical(source) == source))
            throw std::runtime_error("noncanonical objective-eleven source");
        search.require_free_orbit(source);
        search.move_to(source);
        if (search.monochromatic_count != 11)
            throw std::runtime_error("objective-eleven source objective mismatch");

        int minimum_neighbor = std::numeric_limits<int>::max();
        std::unordered_map<State, std::uint16_t, StateHash> local_new;
        for (int id = 0; id < edge_count; ++id) {
            const int objective = search.resulting_count(id);
            ++directed_neighbor_objective_histogram[objective];
            minimum_neighbor = std::min(minimum_neighbor, objective);
            if (objective > 11) continue;
            State neighbor = search.state;
            neighbor.toggle(id);
            const State key = search.canonical(neighbor);
            search.require_free_orbit(neighbor);
            if (objective <= 10 && primary[objective].contains(key)) {
                ++directed_to_primary;
                continue;
            }
            if (objective == 11 && frontier.contains(key)) {
                ++directed_inside_frontier;
                continue;
            }
            auto [it, inserted] = additions.try_emplace(key);
            TargetInfo& info = it->second;
            if (inserted) info.objective = objective;
            if (info.objective != objective)
                throw std::runtime_error("addition objective inconsistency");
            ++info.quotient_incidence;
            info.sources.insert(source_index);
            if (local_new[key] == std::numeric_limits<std::uint16_t>::max())
                throw std::runtime_error("local addition incidence overflow");
            ++local_new[key];
            ++directed_to_new;
            if (objective == 11) ++new_eleven_incidence;
            else ++new_lower_incidence;
        }
        std::uint64_t local_incidence = 0;
        for (const auto& [target, multiplicity] : local_new) {
            (void)target;
            local_incidence += multiplicity;
        }
        ++source_minimum_neighbor_histogram[minimum_neighbor];
        ++source_distinct_new_degree_histogram[
            static_cast<int>(local_new.size())
        ];
        ++source_new_incidence_histogram[static_cast<int>(local_incidence)];
    }

    std::array<std::vector<State>, 12> additions_by_objective;
    std::map<int, std::uint64_t> addition_orbit_count_by_objective;
    std::map<int, std::uint64_t> target_distinct_source_degree_histogram;
    std::map<int, std::uint64_t> target_incidence_histogram;
    std::uint64_t target_incidence_sum = 0;
    std::uint64_t distinct_source_target_pairs = 0;
    for (const auto& [target, info] : additions) {
        if (info.objective < 0 || info.objective > 11)
            throw std::runtime_error("invalid addition objective");
        additions_by_objective[info.objective].push_back(target);
        ++addition_orbit_count_by_objective[info.objective];
        ++target_distinct_source_degree_histogram[
            static_cast<int>(info.sources.size())
        ];
        ++target_incidence_histogram[
            static_cast<int>(info.quotient_incidence)
        ];
        target_incidence_sum += info.quotient_incidence;
        distinct_source_target_pairs += info.sources.size();
    }
    for (auto& states : additions_by_objective)
        std::sort(states.begin(), states.end());
    if (target_incidence_sum != directed_to_new)
        throw std::runtime_error("addition incidence sum mismatch");
    if (directed_inside_frontier % 2 != 0)
        throw std::runtime_error("odd internal directed incidence");

    std::ofstream output(output_path);
    if (!output) throw std::runtime_error("cannot write " + output_path);
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"objective_eleven_first_frontier_rotation_orbit_count\": "
           << sources.size() << ",\n";
    output << "  \"first_expansion_new_rotation_orbit_count\": "
           << additions.size() << ",\n";
    output << "  \"first_expansion_new_vertex_count\": "
           << orbit_size * additions.size() << ",\n";
    output << "  \"new_rotation_orbit_count_by_objective\": {";
    write_histogram(output, addition_orbit_count_by_objective);
    output << ",\n  \"directed_quotient_moves_to_primary_sublevel_ten\": "
           << directed_to_primary << ",\n";
    output << "  \"directed_quotient_moves_inside_first_frontier\": "
           << directed_inside_frontier << ",\n";
    output << "  \"undirected_quotient_edges_inside_first_frontier\": "
           << directed_inside_frontier / 2 << ",\n";
    output << "  \"directed_quotient_moves_to_new_states\": "
           << directed_to_new << ",\n";
    output << "  \"directed_quotient_moves_to_new_lower_states\": "
           << new_lower_incidence << ",\n";
    output << "  \"directed_quotient_moves_to_new_objective_eleven_states\": "
           << new_eleven_incidence << ",\n";
    output << "  \"distinct_source_target_pairs\": "
           << distinct_source_target_pairs << ",\n";
    output << "  \"directed_neighbor_objective_histogram\": {";
    write_histogram(output, directed_neighbor_objective_histogram);
    output << ",\n  \"source_minimum_neighbor_objective_histogram\": {";
    write_histogram(output, source_minimum_neighbor_histogram);
    output << ",\n  \"source_distinct_new_target_degree_histogram\": {";
    write_histogram(output, source_distinct_new_degree_histogram);
    output << ",\n  \"source_new_target_incidence_histogram\": {";
    write_histogram(output, source_new_incidence_histogram);
    output << ",\n  \"target_distinct_first_frontier_source_degree_histogram\": {";
    write_histogram(output, target_distinct_source_degree_histogram);
    output << ",\n  \"target_first_frontier_incidence_histogram\": {";
    write_histogram(output, target_incidence_histogram);
    output << ",\n";
    bool wrote_array = false;
    for (int objective = 0; objective <= 11; ++objective) {
        if (additions_by_objective[objective].empty()) continue;
        if (wrote_array) output << ",\n";
        output << "  \"new_objective_" << objective
               << "_rotation_representatives\": [\n";
        write_states(output, additions_by_objective[objective]);
        output << "\n  ]";
        wrote_array = true;
    }
    if (wrote_array) output << ",\n";
    output << "  \"method\": \"exact incremental monochromatic-five-set deltas and cyclic canonicalization for all 903 one-edge moves from every representative in the complete first objective-eleven frontier\",\n";
    output << "  \"scope_note\": \"Exact first expansion of the first objective-eleven frontier only; it does not close the threshold-eleven component or classify disconnected sublevel-ten components.\"\n}\n";
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 10) {
        std::cerr
            << "usage: scan_objective_eleven_first_expansion CERTIFICATE.json "
               "LOWER-SIX.json OBJECTIVE-SEVEN-COMPONENT.json "
               "OBJECTIVE-EIGHT-COMPONENT.json OBJECTIVE-NINE-COMPONENT.json "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OBJECTIVE-ELEVEN-FRONTIER.json OUTPUT.json\n";
        return 2;
    }
    Search search(load_flips(argv[1]));
    scan_first_expansion(
        search, argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8],
        argv[9]
    );
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
