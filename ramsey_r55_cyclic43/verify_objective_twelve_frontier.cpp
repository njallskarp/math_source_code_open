#define main verify_objective_ten_frontier_embedded_main
#include "verify_objective_ten_frontier.cpp"
#undef main

namespace {

struct DirectThreadData {
    std::vector<State> lower_targets;
    std::vector<State> q11_targets;
    std::array<std::uint64_t, 12> source_count{};
    std::array<std::uint64_t, 12> raw_incidence{};
    std::array<std::uint64_t, 12> distinct_pair_count{};
    std::array<std::map<int, std::uint64_t>, 12> source_degree_histogram;
    std::uint64_t objective_errors = 0;
    std::uint64_t nonfree_target_encounters = 0;
};

void direct_append_sources(
    std::vector<SourceEntry>& sources, int objective,
    const std::string& path, const std::string& key
) {
    for (const State& state : load_states(path, key))
        sources.push_back({objective, state});
}

std::vector<SourceEntry> direct_load_lower_sources(
    const std::string& lower_six_path,
    const std::string& objective_seven_path,
    const std::string& objective_eight_path,
    const std::string& objective_nine_path,
    const std::string& objective_ten_frontier_path,
    const std::string& objective_ten_component_path
) {
    std::vector<SourceEntry> sources;
    for (int objective = 2; objective <= 6; ++objective)
        direct_append_sources(
            sources, objective, lower_six_path,
            "objective_" + std::to_string(objective) +
                "_rotation_representatives"
        );
    direct_append_sources(
        sources, 7, objective_seven_path,
        "objective_seven_component_rotation_representatives"
    );
    direct_append_sources(
        sources, 8, objective_eight_path,
        "objective_eight_component_rotation_representatives"
    );
    direct_append_sources(
        sources, 7, objective_nine_path,
        "new_objective_7_rotation_representatives"
    );
    direct_append_sources(
        sources, 8, objective_nine_path,
        "new_objective_8_rotation_representatives"
    );
    direct_append_sources(
        sources, 9, objective_nine_path,
        "new_objective_9_rotation_representatives"
    );
    direct_append_sources(
        sources, 10, objective_ten_frontier_path,
        "objective_ten_rotation_representatives"
    );
    direct_append_sources(
        sources, 10, objective_ten_component_path,
        "additional_objective_10_rotation_representatives"
    );
    return sources;
}

template <class Key>
void direct_write_histogram(
    std::ostream& output, const std::map<Key, std::uint64_t>& histogram,
    int indentation
) {
    output << '{';
    bool separator = false;
    for (const auto& [key, count] : histogram) {
        if (separator) output << ',';
        output << '\n' << std::string(indentation + 2, ' ') << '"' << key
               << "\": " << count;
        separator = true;
    }
    if (separator) output << '\n' << std::string(indentation, ' ');
    output << '}';
}

void sort_unique(std::vector<State>& states) {
    std::sort(states.begin(), states.end());
    states.erase(std::unique(states.begin(), states.end()), states.end());
}

std::pair<std::uint64_t, std::uint64_t> compare_sorted_states(
    const std::vector<State>& actual, const std::vector<State>& expected
) {
    std::size_t actual_index = 0;
    std::size_t expected_index = 0;
    std::uint64_t unexpected = 0;
    std::uint64_t omitted = 0;
    while (actual_index < actual.size() && expected_index < expected.size()) {
        if (actual[actual_index] < expected[expected_index]) {
            ++unexpected;
            ++actual_index;
        } else if (expected[expected_index] < actual[actual_index]) {
            ++omitted;
            ++expected_index;
        } else {
            ++actual_index;
            ++expected_index;
        }
    }
    unexpected += actual.size() - actual_index;
    omitted += expected.size() - expected_index;
    return {unexpected, omitted};
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 11) {
        std::cerr
            << "usage: verify_objective_twelve_frontier LOWER-SIX.json "
               "OBJECTIVE-SEVEN-COMPONENT.json "
               "OBJECTIVE-EIGHT-COMPONENT.json OBJECTIVE-NINE-COMPONENT.json "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OBJECTIVE-ELEVEN-FRONTIER.json OBJECTIVE-ELEVEN-COMPONENT.json "
               "EXPECTED-TARGETS.json OUTPUT.json\n";
        return 2;
    }

    std::vector<SourceEntry> sources = direct_load_lower_sources(
        argv[1], argv[2], argv[3], argv[4], argv[5], argv[6]
    );
    const std::size_t lower_source_count = sources.size();
    direct_append_sources(
        sources, 11, argv[7], "objective_eleven_rotation_representatives"
    );
    direct_append_sources(
        sources, 11, argv[8],
        "complete_additional_objective_11_rotation_representatives"
    );
    if (lower_source_count != 191067 ||
        sources.size() - lower_source_count != 373124)
        throw std::runtime_error("source count mismatch");

    std::vector<State> expected = load_states(
        argv[9], "objective_twelve_rotation_representatives"
    );
    if (!std::is_sorted(expected.begin(), expected.end()) ||
        std::adjacent_find(expected.begin(), expected.end()) != expected.end())
        throw std::runtime_error("expected target list is not sorted and unique");

    const int thread_count = omp_get_max_threads();
    std::vector<DirectThreadData> thread_data(thread_count);
#pragma omp parallel
    {
        const int thread_id = omp_get_thread_num();
        DirectThreadData& data = thread_data[thread_id];
        Model model;
        std::vector<State> local_targets;
        local_targets.reserve(80);
#pragma omp for schedule(dynamic, 8)
        for (std::int64_t source_index = 0;
             source_index < static_cast<std::int64_t>(sources.size());
             ++source_index) {
            const SourceEntry& source = sources[source_index];
            const Model::Analysis analysis = model.analyze(source.state);
            if (analysis.objective != source.objective)
                ++data.objective_errors;
            local_targets.clear();
            for (int id = 0; id < edge_count; ++id) {
                if (analysis.objective + analysis.delta[id] != 12) continue;
                State neighbor = source.state;
                neighbor.toggle(id);
                if (!model.is_free(neighbor))
                    ++data.nonfree_target_encounters;
                local_targets.push_back(model.canonical(neighbor));
            }
            ++data.source_count[source.objective];
            data.raw_incidence[source.objective] += local_targets.size();
            std::sort(local_targets.begin(), local_targets.end());
            const auto new_end =
                std::unique(local_targets.begin(), local_targets.end());
            const int degree = static_cast<int>(new_end - local_targets.begin());
            data.distinct_pair_count[source.objective] += degree;
            ++data.source_degree_histogram[source.objective][degree];
            std::vector<State>& destination =
                source_index < static_cast<std::int64_t>(lower_source_count)
                    ? data.lower_targets
                    : data.q11_targets;
            destination.insert(destination.end(), local_targets.begin(), new_end);
        }
    }

    std::array<std::uint64_t, 12> source_count{};
    std::array<std::uint64_t, 12> raw_incidence{};
    std::array<std::uint64_t, 12> distinct_pair_count{};
    std::array<std::map<int, std::uint64_t>, 12> source_degree_histogram;
    std::uint64_t objective_errors = 0;
    std::uint64_t nonfree_target_encounters = 0;
    std::size_t lower_pair_count = 0;
    std::size_t q11_pair_count = 0;
    for (const DirectThreadData& data : thread_data) {
        lower_pair_count += data.lower_targets.size();
        q11_pair_count += data.q11_targets.size();
    }
    std::vector<State> lower_targets;
    std::vector<State> q11_targets;
    lower_targets.reserve(lower_pair_count);
    q11_targets.reserve(q11_pair_count);
    for (DirectThreadData& data : thread_data) {
        for (int objective = 0; objective <= 11; ++objective) {
            source_count[objective] += data.source_count[objective];
            raw_incidence[objective] += data.raw_incidence[objective];
            distinct_pair_count[objective] +=
                data.distinct_pair_count[objective];
            for (const auto& [degree, count] :
                 data.source_degree_histogram[objective])
                source_degree_histogram[objective][degree] += count;
        }
        objective_errors += data.objective_errors;
        nonfree_target_encounters += data.nonfree_target_encounters;
        lower_targets.insert(
            lower_targets.end(),
            std::make_move_iterator(data.lower_targets.begin()),
            std::make_move_iterator(data.lower_targets.end())
        );
        q11_targets.insert(
            q11_targets.end(),
            std::make_move_iterator(data.q11_targets.begin()),
            std::make_move_iterator(data.q11_targets.end())
        );
        std::vector<State>().swap(data.lower_targets);
        std::vector<State>().swap(data.q11_targets);
    }
    sort_unique(lower_targets);
    sort_unique(q11_targets);

    std::vector<State> all_targets;
    all_targets.reserve(lower_targets.size() + q11_targets.size());
    std::set_union(
        lower_targets.begin(), lower_targets.end(), q11_targets.begin(),
        q11_targets.end(), std::back_inserter(all_targets)
    );
    std::vector<State> intersection;
    intersection.reserve(std::min(lower_targets.size(), q11_targets.size()));
    std::set_intersection(
        lower_targets.begin(), lower_targets.end(), q11_targets.begin(),
        q11_targets.end(), std::back_inserter(intersection)
    );
    const auto [unexpected_targets, omitted_targets] =
        compare_sorted_states(all_targets, expected);

    const std::uint64_t total_raw = std::accumulate(
        raw_incidence.begin(), raw_incidence.end(), std::uint64_t{0}
    );
    const std::uint64_t total_pairs = std::accumulate(
        distinct_pair_count.begin(), distinct_pair_count.end(),
        std::uint64_t{0}
    );
    std::ofstream output(argv[10]);
    if (!output) throw std::runtime_error("cannot write direct output");
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"direct_source_rotation_orbit_count\": "
           << sources.size() << ",\n";
    output << "  \"direct_lower_source_rotation_orbit_count\": "
           << lower_source_count << ",\n";
    output << "  \"direct_q11_source_rotation_orbit_count\": "
           << sources.size() - lower_source_count << ",\n";
    output << "  \"direct_frontier_rotation_orbit_count\": "
           << all_targets.size() << ",\n";
    output << "  \"expected_frontier_rotation_orbit_count\": "
           << expected.size() << ",\n";
    output << "  \"direct_frontier_quotient_incidence\": "
           << total_raw << ",\n";
    output << "  \"direct_distinct_source_target_pairs\": "
           << total_pairs << ",\n";
    output << "  \"direct_source_target_parallel_edge_excess\": "
           << total_raw - total_pairs << ",\n";
    output << "  \"direct_lower_derived_target_count\": "
           << lower_targets.size() << ",\n";
    output << "  \"direct_q11_derived_target_count\": "
           << q11_targets.size() << ",\n";
    output << "  \"direct_mixed_lower_q11_target_count\": "
           << intersection.size() << ",\n";
    output << "  \"direct_lower_only_target_count\": "
           << lower_targets.size() - intersection.size() << ",\n";
    output << "  \"direct_q11_only_target_count\": "
           << q11_targets.size() - intersection.size() << ",\n";
    output << "  \"unexpected_targets\": " << unexpected_targets
           << ",\n";
    output << "  \"omitted_targets\": " << omitted_targets << ",\n";
    output << "  \"objective_errors\": " << objective_errors << ",\n";
    output << "  \"nonfree_target_encounters\": "
           << nonfree_target_encounters << ",\n";
    output << "  \"raw_incidence_by_source_objective\": {";
    bool separator = false;
    for (int objective = 0; objective <= 11; ++objective) {
        if (source_count[objective] == 0) continue;
        if (separator) output << ',';
        output << "\n    \"" << objective << "\": "
               << raw_incidence[objective];
        separator = true;
    }
    output << "\n  },\n  \"distinct_pair_count_by_source_objective\": {";
    separator = false;
    for (int objective = 0; objective <= 11; ++objective) {
        if (source_count[objective] == 0) continue;
        if (separator) output << ',';
        output << "\n    \"" << objective << "\": "
               << distinct_pair_count[objective];
        separator = true;
    }
    output << "\n  },\n  \"source_distinct_target_degree_histogram_by_objective\": {\n";
    separator = false;
    for (int objective = 0; objective <= 11; ++objective) {
        if (source_count[objective] == 0) continue;
        if (separator) output << ",\n";
        output << "    \"" << objective << "\": ";
        direct_write_histogram(
            output, source_degree_histogram[objective], 4
        );
        separator = true;
    }
    output << "\n  },\n  \"all_direct_checks_pass\": "
           << ((unexpected_targets == 0 && omitted_targets == 0 &&
                objective_errors == 0 && nonfree_target_encounters == 0)
                   ? "true"
                   : "false")
           << ",\n";
    output << "  \"method\": \"independent direct enumeration of all 962,598 five-sets at all 564,191 source representatives, independent one-edge objective deltas and cyclic canonicalization, and entry-for-entry comparison with the optimized frontier\"\n}\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
