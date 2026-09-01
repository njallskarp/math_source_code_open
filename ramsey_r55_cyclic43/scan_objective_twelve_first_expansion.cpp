#define main objective_six_component_embedded_main
#include "objective_six_component.cpp"
#undef main

#include <atomic>
#include <memory>
#include <omp.h>

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
    std::uint64_t distinct_sources = 0;
};

struct ThreadData {
    std::unordered_map<State, TargetInfo, StateHash> additions;
    std::map<int, std::uint64_t> directed_neighbor_objective_histogram;
    std::map<int, std::uint64_t> source_minimum_neighbor_histogram;
    std::map<int, std::uint64_t> source_distinct_new_degree_histogram;
    std::map<int, std::uint64_t> source_new_incidence_histogram;
    std::uint64_t directed_to_primary = 0;
    std::uint64_t directed_inside_frontier = 0;
    std::uint64_t directed_to_new = 0;
    std::uint64_t new_lower_incidence = 0;
    std::uint64_t new_twelve_incidence = 0;
    std::uint64_t objective_errors = 0;
    std::uint64_t canonical_errors = 0;
};

template <class Map>
void merge_histogram(Map& destination, const Map& source) {
    for (const auto& [key, value] : source) destination[key] += value;
}

void add_layer(
    Search& search,
    std::array<std::unordered_set<State, StateHash>, 13>& primary,
    int objective, const std::string& path, const std::string& key
) {
    for (const State& state : load_state_array(path, key)) {
        if (!(search.canonical(state) == state) ||
            !primary[objective].insert(state).second)
            throw std::runtime_error("invalid primary source certificate");
        search.require_free_orbit(state);
    }
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 12) {
        std::cerr
            << "usage: scan_objective_twelve_first_expansion CERTIFICATE.json "
               "LOWER-SIX.json OBJECTIVE-SEVEN-COMPONENT.json "
               "OBJECTIVE-EIGHT-COMPONENT.json OBJECTIVE-NINE-COMPONENT.json "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OBJECTIVE-ELEVEN-FRONTIER.json "
               "OBJECTIVE-ELEVEN-COMPONENT.json "
               "OBJECTIVE-TWELVE-FRONTIER.json OUTPUT.json\n";
        return 2;
    }

    const std::set<std::pair<int, int>> certificate_flips = load_flips(argv[1]);
    Search validator(certificate_flips);
    std::array<std::unordered_set<State, StateHash>, 13> primary;
    for (int objective = 2; objective <= 6; ++objective)
        add_layer(
            validator, primary, objective, argv[2],
            "objective_" + std::to_string(objective) +
                "_rotation_representatives"
        );
    add_layer(
        validator, primary, 7, argv[3],
        "objective_seven_component_rotation_representatives"
    );
    add_layer(
        validator, primary, 8, argv[4],
        "objective_eight_component_rotation_representatives"
    );
    add_layer(
        validator, primary, 7, argv[5],
        "new_objective_7_rotation_representatives"
    );
    add_layer(
        validator, primary, 8, argv[5],
        "new_objective_8_rotation_representatives"
    );
    add_layer(
        validator, primary, 9, argv[5],
        "new_objective_9_rotation_representatives"
    );
    add_layer(
        validator, primary, 10, argv[6],
        "objective_ten_rotation_representatives"
    );
    add_layer(
        validator, primary, 10, argv[7],
        "additional_objective_10_rotation_representatives"
    );
    add_layer(
        validator, primary, 11, argv[8],
        "objective_eleven_rotation_representatives"
    );
    add_layer(
        validator, primary, 11, argv[9],
        "complete_additional_objective_11_rotation_representatives"
    );
    const std::array<std::size_t, 12> expected_primary = {
        0, 0, 2, 17, 78, 306, 1183, 4218, 13771, 42781, 128711, 373124
    };
    for (int objective = 2; objective <= 11; ++objective)
        if (primary[objective].size() != expected_primary[objective])
            throw std::runtime_error("primary source layer count mismatch");

    std::vector<State> sources = load_state_array(
        argv[10], "objective_twelve_rotation_representatives"
    );
    if (sources.size() != 1041887 ||
        !std::is_sorted(sources.begin(), sources.end()) ||
        std::adjacent_find(sources.begin(), sources.end()) != sources.end())
        throw std::runtime_error("invalid objective-twelve frontier array");
    std::unordered_set<State, StateHash> frontier(sources.begin(), sources.end());
    if (frontier.size() != sources.size())
        throw std::runtime_error("objective-twelve frontier set mismatch");

    const int thread_count = omp_get_max_threads();
    std::vector<std::unique_ptr<Search>> engines;
    engines.reserve(thread_count);
    for (int thread = 0; thread < thread_count; ++thread)
        engines.push_back(std::make_unique<Search>(certificate_flips));
    std::vector<ThreadData> thread_data(thread_count);
    for (ThreadData& data : thread_data) data.additions.reserve(100000);
    std::atomic<std::uint64_t> processed = 0;

#pragma omp parallel
    {
        const int thread_id = omp_get_thread_num();
        Search& search = *engines[thread_id];
        ThreadData& data = thread_data[thread_id];
        const std::size_t begin =
            sources.size() * static_cast<std::size_t>(thread_id) /
            static_cast<std::size_t>(thread_count);
        const std::size_t end =
            sources.size() * static_cast<std::size_t>(thread_id + 1) /
            static_cast<std::size_t>(thread_count);
        for (std::size_t source_index = begin; source_index < end;
             ++source_index) {
            const State& source = sources[source_index];
            if (!(search.canonical(source) == source))
                ++data.canonical_errors;
            search.require_free_orbit(source);
            search.move_to(source);
            if (search.monochromatic_count != 12) ++data.objective_errors;

            int minimum_neighbor = std::numeric_limits<int>::max();
            std::unordered_map<State, std::pair<int, std::uint16_t>, StateHash>
                local_new;
            for (int id = 0; id < edge_count; ++id) {
                const int objective = search.resulting_count(id);
                ++data.directed_neighbor_objective_histogram[objective];
                minimum_neighbor = std::min(minimum_neighbor, objective);
                if (objective > 12) continue;
                State neighbor = source;
                neighbor.toggle(id);
                const State key = search.canonical(neighbor);
                search.require_free_orbit(neighbor);
                if (objective <= 11 && primary[objective].contains(key)) {
                    ++data.directed_to_primary;
                    continue;
                }
                if (objective == 12 && frontier.contains(key)) {
                    ++data.directed_inside_frontier;
                    continue;
                }
                auto [it, inserted] = local_new.try_emplace(
                    key, std::pair<int, std::uint16_t>{objective, 0}
                );
                if (it->second.first != objective) ++data.objective_errors;
                if (it->second.second ==
                    std::numeric_limits<std::uint16_t>::max())
                    ++data.objective_errors;
                else
                    ++it->second.second;
                ++data.directed_to_new;
                if (objective == 12)
                    ++data.new_twelve_incidence;
                else
                    ++data.new_lower_incidence;
            }
            std::uint64_t local_incidence = 0;
            for (const auto& [target, objective_and_multiplicity] : local_new) {
                const auto [objective, multiplicity] =
                    objective_and_multiplicity;
                TargetInfo& info = data.additions[target];
                if (info.objective < 0) info.objective = objective;
                if (info.objective != objective) ++data.objective_errors;
                info.quotient_incidence += multiplicity;
                ++info.distinct_sources;
                local_incidence += multiplicity;
            }
            ++data.source_minimum_neighbor_histogram[minimum_neighbor];
            ++data.source_distinct_new_degree_histogram[
                static_cast<int>(local_new.size())
            ];
            ++data.source_new_incidence_histogram[
                static_cast<int>(local_incidence)
            ];
            const auto done = ++processed;
            if (thread_id == 0 && done % 50000 == 0)
                std::cerr << "objective-twelve first expansion: " << done
                          << '/' << sources.size() << " sources\n";
        }
    }

    ThreadData merged;
    merged.additions.reserve(1000000);
    for (const ThreadData& data : thread_data) {
        merge_histogram(
            merged.directed_neighbor_objective_histogram,
            data.directed_neighbor_objective_histogram
        );
        merge_histogram(
            merged.source_minimum_neighbor_histogram,
            data.source_minimum_neighbor_histogram
        );
        merge_histogram(
            merged.source_distinct_new_degree_histogram,
            data.source_distinct_new_degree_histogram
        );
        merge_histogram(
            merged.source_new_incidence_histogram,
            data.source_new_incidence_histogram
        );
        merged.directed_to_primary += data.directed_to_primary;
        merged.directed_inside_frontier += data.directed_inside_frontier;
        merged.directed_to_new += data.directed_to_new;
        merged.new_lower_incidence += data.new_lower_incidence;
        merged.new_twelve_incidence += data.new_twelve_incidence;
        merged.objective_errors += data.objective_errors;
        merged.canonical_errors += data.canonical_errors;
        for (const auto& [target, local] : data.additions) {
            TargetInfo& global = merged.additions[target];
            if (global.objective < 0) global.objective = local.objective;
            if (global.objective != local.objective) ++merged.objective_errors;
            global.quotient_incidence += local.quotient_incidence;
            global.distinct_sources += local.distinct_sources;
        }
    }

    std::array<std::vector<State>, 13> additions_by_objective;
    std::map<int, std::uint64_t> addition_count_by_objective;
    std::map<int, std::uint64_t> target_source_degree_histogram;
    std::map<int, std::uint64_t> target_incidence_histogram;
    std::uint64_t target_incidence_sum = 0;
    std::uint64_t distinct_source_target_pairs = 0;
    for (const auto& [target, info] : merged.additions) {
        if (info.objective < 0 || info.objective > 12)
            throw std::runtime_error("invalid addition objective");
        additions_by_objective[info.objective].push_back(target);
        ++addition_count_by_objective[info.objective];
        ++target_source_degree_histogram[info.distinct_sources];
        ++target_incidence_histogram[info.quotient_incidence];
        target_incidence_sum += info.quotient_incidence;
        distinct_source_target_pairs += info.distinct_sources;
    }
    for (auto& states : additions_by_objective)
        std::sort(states.begin(), states.end());
    if (target_incidence_sum != merged.directed_to_new)
        throw std::runtime_error("addition incidence sum mismatch");
    if (merged.directed_inside_frontier % 2 != 0)
        throw std::runtime_error("odd internal directed incidence");
    if (merged.objective_errors || merged.canonical_errors)
        throw std::runtime_error("objective or canonical validation failure");

    std::ofstream output(argv[11]);
    if (!output) throw std::runtime_error("cannot write output");
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"objective_twelve_first_frontier_rotation_orbit_count\": "
           << sources.size() << ",\n";
    output << "  \"first_expansion_new_rotation_orbit_count\": "
           << merged.additions.size() << ",\n";
    output << "  \"first_expansion_new_vertex_count\": "
           << orbit_size * merged.additions.size() << ",\n";
    output << "  \"new_rotation_orbit_count_by_objective\": {";
    write_histogram(output, addition_count_by_objective);
    output << ",\n  \"directed_quotient_moves_to_primary_sublevel_eleven\": "
           << merged.directed_to_primary << ",\n";
    output << "  \"directed_quotient_moves_inside_first_frontier\": "
           << merged.directed_inside_frontier << ",\n";
    output << "  \"undirected_quotient_edges_inside_first_frontier\": "
           << merged.directed_inside_frontier / 2 << ",\n";
    output << "  \"directed_quotient_moves_to_new_states\": "
           << merged.directed_to_new << ",\n";
    output << "  \"directed_quotient_moves_to_new_lower_states\": "
           << merged.new_lower_incidence << ",\n";
    output << "  \"directed_quotient_moves_to_new_objective_twelve_states\": "
           << merged.new_twelve_incidence << ",\n";
    output << "  \"distinct_source_target_pairs\": "
           << distinct_source_target_pairs << ",\n";
    output << "  \"objective_errors\": " << merged.objective_errors << ",\n";
    output << "  \"canonical_errors\": " << merged.canonical_errors << ",\n";
    output << "  \"directed_neighbor_objective_histogram\": {";
    write_histogram(output, merged.directed_neighbor_objective_histogram);
    output << ",\n  \"source_minimum_neighbor_objective_histogram\": {";
    write_histogram(output, merged.source_minimum_neighbor_histogram);
    output << ",\n  \"source_distinct_new_target_degree_histogram\": {";
    write_histogram(output, merged.source_distinct_new_degree_histogram);
    output << ",\n  \"source_new_target_incidence_histogram\": {";
    write_histogram(output, merged.source_new_incidence_histogram);
    output << ",\n  \"target_distinct_first_frontier_source_degree_histogram\": {";
    write_histogram(output, target_source_degree_histogram);
    output << ",\n  \"target_first_frontier_incidence_histogram\": {";
    write_histogram(output, target_incidence_histogram);
    output << ",\n";
    bool wrote_array = false;
    for (int objective = 0; objective <= 12; ++objective) {
        if (additions_by_objective[objective].empty()) continue;
        if (wrote_array) output << ",\n";
        output << "  \"new_objective_" << objective
               << "_rotation_representatives\": [\n";
        write_states(output, additions_by_objective[objective]);
        output << "\n  ]";
        wrote_array = true;
    }
    if (wrote_array) output << ",\n";
    output << "  \"method\": \"exact incremental monochromatic-five-set deltas, cyclic canonicalization, static OpenMP source partitioning, and source-local multiplicity aggregation for all 903 one-edge moves from every representative in the complete first objective-twelve frontier\",\n";
    output << "  \"scope_note\": \"Exact first expansion of the complete objective-twelve frontier only; it does not by itself close the threshold-twelve component or classify disconnected sublevel-eleven components.\"\n}\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
