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

struct DirectTargetInfo {
    int objective = -1;
    std::uint64_t quotient_incidence = 0;
    std::uint64_t distinct_sources = 0;
};

struct ThreadResult {
    std::unordered_map<State, DirectTargetInfo, StateHash> additions;
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

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 12) {
        std::cerr
            << "usage: verify_objective_twelve_first_expansion "
               "LOWER-SIX.json OBJECTIVE-SEVEN-COMPONENT.json "
               "OBJECTIVE-EIGHT-COMPONENT.json OBJECTIVE-NINE-COMPONENT.json "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OBJECTIVE-ELEVEN-FRONTIER.json "
               "OBJECTIVE-ELEVEN-COMPONENT.json "
               "OBJECTIVE-TWELVE-FRONTIER.json FIRST-EXPANSION.json "
               "OUTPUT.json\n";
        return 2;
    }
    Model model;
    std::array<std::unordered_set<State, StateHash>, 13> primary;
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
    add_primary(
        11, argv[7], "objective_eleven_rotation_representatives"
    );
    add_primary(
        11, argv[8],
        "complete_additional_objective_11_rotation_representatives"
    );
    const std::array<std::size_t, 12> expected_primary = {
        0, 0, 2, 17, 78, 306, 1183, 4218, 13771, 42781, 128711, 373124
    };
    for (int objective = 2; objective <= 11; ++objective)
        if (primary[objective].size() != expected_primary[objective])
            throw std::runtime_error("primary source layer count mismatch");

    const std::vector<State> sources = load_states(
        argv[9], "objective_twelve_rotation_representatives"
    );
    if (sources.size() != 1041887 ||
        !std::is_sorted(sources.begin(), sources.end()) ||
        std::adjacent_find(sources.begin(), sources.end()) != sources.end())
        throw std::runtime_error("invalid objective-twelve frontier array");
    const std::unordered_set<State, StateHash> frontier(
        sources.begin(), sources.end()
    );

    std::array<std::unordered_set<State, StateHash>, 13> expected_additions;
    const std::string expected_text = read_text(argv[10]);
    for (int objective = 0; objective <= 12; ++objective) {
        const std::string key =
            "new_objective_" + std::to_string(objective) +
            "_rotation_representatives";
        if (expected_text.find('"' + key + '"') == std::string::npos) continue;
        for (const State& state : load_states(argv[10], key)) {
            if (!(model.canonical(state) == state) || !model.is_free(state) ||
                !expected_additions[objective].insert(state).second)
                throw std::runtime_error("invalid expected addition array");
        }
    }

    const int thread_count = omp_get_max_threads();
    std::vector<ThreadResult> thread_results(thread_count);
    for (ThreadResult& result : thread_results)
        result.additions.reserve(50000);

#pragma omp parallel for schedule(dynamic, 8)
    for (std::size_t source_index = 0; source_index < sources.size();
         ++source_index) {
        ThreadResult& result = thread_results[omp_get_thread_num()];
        const State& source = sources[source_index];
        if (!(model.canonical(source) == source) || !model.is_free(source))
            ++result.canonical_errors;
        const Model::Analysis analysis = model.analyze(source);
        if (analysis.objective != 12) ++result.objective_errors;
        int minimum_neighbor = std::numeric_limits<int>::max();
        std::unordered_map<State, std::pair<int, std::uint16_t>, StateHash>
            local_new;
        for (int id = 0; id < edge_count; ++id) {
            const int objective = analysis.objective + analysis.delta[id];
            ++result.directed_neighbor_objective_histogram[objective];
            minimum_neighbor = std::min(minimum_neighbor, objective);
            if (objective > 12) continue;
            State neighbor = source;
            neighbor.toggle(id);
            const State key = model.canonical(neighbor);
            if (!model.is_free(neighbor)) ++result.canonical_errors;
            if (objective <= 11 && primary[objective].contains(key)) {
                ++result.directed_to_primary;
                continue;
            }
            if (objective == 12 && frontier.contains(key)) {
                ++result.directed_inside_frontier;
                continue;
            }
            auto [it, inserted] = local_new.try_emplace(
                key, std::pair<int, std::uint16_t>{objective, 0}
            );
            if (it->second.first != objective)
                ++result.objective_errors;
            if (it->second.second == std::numeric_limits<std::uint16_t>::max())
                ++result.objective_errors;
            else
                ++it->second.second;
            ++result.directed_to_new;
            if (objective == 12) ++result.new_twelve_incidence;
            else ++result.new_lower_incidence;
        }
        std::uint64_t local_incidence = 0;
        for (const auto& [target, objective_and_multiplicity] : local_new) {
            const auto [objective, multiplicity] = objective_and_multiplicity;
            DirectTargetInfo& info = result.additions[target];
            if (info.objective < 0) info.objective = objective;
            if (info.objective != objective) ++result.objective_errors;
            info.quotient_incidence += multiplicity;
            ++info.distinct_sources;
            local_incidence += multiplicity;
        }
        ++result.source_minimum_neighbor_histogram[minimum_neighbor];
        ++result.source_distinct_new_degree_histogram[
            static_cast<int>(local_new.size())
        ];
        ++result.source_new_incidence_histogram[
            static_cast<int>(local_incidence)
        ];
    }

    ThreadResult merged;
    merged.additions.reserve(500000);
    auto merge_histogram = [](auto& destination, const auto& source) {
        for (const auto& [key, value] : source) destination[key] += value;
    };
    for (const ThreadResult& result : thread_results) {
        merge_histogram(
            merged.directed_neighbor_objective_histogram,
            result.directed_neighbor_objective_histogram
        );
        merge_histogram(
            merged.source_minimum_neighbor_histogram,
            result.source_minimum_neighbor_histogram
        );
        merge_histogram(
            merged.source_distinct_new_degree_histogram,
            result.source_distinct_new_degree_histogram
        );
        merge_histogram(
            merged.source_new_incidence_histogram,
            result.source_new_incidence_histogram
        );
        merged.directed_to_primary += result.directed_to_primary;
        merged.directed_inside_frontier += result.directed_inside_frontier;
        merged.directed_to_new += result.directed_to_new;
        merged.new_lower_incidence += result.new_lower_incidence;
        merged.new_twelve_incidence += result.new_twelve_incidence;
        merged.objective_errors += result.objective_errors;
        merged.canonical_errors += result.canonical_errors;
        for (const auto& [target, local] : result.additions) {
            DirectTargetInfo& global = merged.additions[target];
            if (global.objective < 0) global.objective = local.objective;
            if (global.objective != local.objective) ++merged.objective_errors;
            global.quotient_incidence += local.quotient_incidence;
            global.distinct_sources += local.distinct_sources;
        }
    }

    std::map<int, std::uint64_t> addition_orbit_count_by_objective;
    std::map<int, std::uint64_t> target_degree_histogram;
    std::map<int, std::uint64_t> target_incidence_histogram;
    std::uint64_t omitted_targets = 0;
    std::uint64_t unexpected_targets = 0;
    std::uint64_t objective_mismatches = merged.objective_errors;
    std::uint64_t target_incidence_sum = 0;
    for (const auto& [target, info] : merged.additions) {
        ++addition_orbit_count_by_objective[info.objective];
        ++target_degree_histogram[static_cast<int>(info.distinct_sources)];
        ++target_incidence_histogram[
            static_cast<int>(info.quotient_incidence)
        ];
        target_incidence_sum += info.quotient_incidence;
        if (info.objective < 0 || info.objective > 12 ||
            !expected_additions[info.objective].contains(target))
            ++unexpected_targets;
        if (info.objective >= 0 && info.objective <= 12) {
            const Model::Analysis target_analysis = model.analyze(target);
            if (target_analysis.objective != info.objective)
                ++objective_mismatches;
        }
    }
    for (int objective = 0; objective <= 12; ++objective)
        for (const State& target : expected_additions[objective])
            if (!merged.additions.contains(target)) ++omitted_targets;

    std::ofstream output(argv[11]);
    if (!output) throw std::runtime_error("cannot write direct output");
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"direct_five_set_recount_source_count\": " << sources.size()
           << ",\n";
    output << "  \"first_expansion_new_rotation_orbit_count\": "
           << merged.additions.size() << ",\n";
    output << "  \"new_rotation_orbit_count_by_objective\": {";
    write_histogram(output, addition_orbit_count_by_objective);
    output << ",\n  \"directed_quotient_moves_to_primary_sublevel_eleven\": "
           << merged.directed_to_primary << ",\n";
    output << "  \"directed_quotient_moves_inside_first_frontier\": "
           << merged.directed_inside_frontier << ",\n";
    output << "  \"directed_quotient_moves_to_new_states\": "
           << merged.directed_to_new << ",\n";
    output << "  \"directed_quotient_moves_to_new_lower_states\": "
           << merged.new_lower_incidence << ",\n";
    output << "  \"directed_quotient_moves_to_new_objective_twelve_states\": "
           << merged.new_twelve_incidence << ",\n";
    output << "  \"directed_neighbor_objective_histogram\": {";
    write_histogram(output, merged.directed_neighbor_objective_histogram);
    output << ",\n  \"source_minimum_neighbor_objective_histogram\": {";
    write_histogram(output, merged.source_minimum_neighbor_histogram);
    output << ",\n  \"source_distinct_new_target_degree_histogram\": {";
    write_histogram(output, merged.source_distinct_new_degree_histogram);
    output << ",\n  \"source_new_target_incidence_histogram\": {";
    write_histogram(output, merged.source_new_incidence_histogram);
    output << ",\n  \"target_distinct_first_frontier_source_degree_histogram\": {";
    write_histogram(output, target_degree_histogram);
    output << ",\n  \"target_first_frontier_incidence_histogram\": {";
    write_histogram(output, target_incidence_histogram);
    output << ",\n  \"target_incidence_sum\": " << target_incidence_sum
           << ",\n";
    output << "  \"omitted_expected_targets\": " << omitted_targets << ",\n";
    output << "  \"unexpected_targets\": " << unexpected_targets << ",\n";
    output << "  \"objective_mismatches\": " << objective_mismatches << ",\n";
    output << "  \"canonical_or_orbit_errors\": "
           << merged.canonical_errors << ",\n";
    output << "  \"all_direct_checks_pass\": "
           << ((omitted_targets == 0 && unexpected_targets == 0 &&
                objective_mismatches == 0 && merged.canonical_errors == 0 &&
                target_incidence_sum == merged.directed_to_new)
                   ? "true"
                   : "false")
           << ",\n";
    output << "  \"method\": \"independent OpenMP direct enumeration of all 962,598 five-sets for each objective-twelve source, followed by exact cyclic canonicalization and full target-set comparison\"\n}\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
