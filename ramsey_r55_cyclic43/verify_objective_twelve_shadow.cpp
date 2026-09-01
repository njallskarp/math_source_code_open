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
        output << "\n    \"" << value << "\": " << count;
        separator = true;
    }
    output << "\n  }";
}

struct DirectTargetInfo {
    std::uint64_t incidence = 0;
    std::unordered_set<std::size_t> source_indices;
};

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 5) {
        std::cerr
            << "usage: verify_objective_twelve_shadow "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OBJECTIVE-TWELVE-SHADOW.json OUTPUT.json\n";
        return 2;
    }
    const std::vector<State> first_sources = load_states(
        argv[1], "objective_ten_rotation_representatives"
    );
    const std::vector<State> additions = load_states(
        argv[2], "additional_objective_10_rotation_representatives"
    );
    std::unordered_set<State, StateHash> complete_sources(
        first_sources.begin(), first_sources.end()
    );
    complete_sources.insert(additions.begin(), additions.end());
    if (complete_sources.size() != 128711)
        throw std::runtime_error("complete objective-ten source mismatch");

    const std::vector<State> shadow_sources = load_states(
        argv[3], "objective_ten_shadow_rotation_representatives"
    );
    const std::vector<State> targets = load_states(
        argv[3], "objective_twelve_shadow_frontier_rotation_representatives"
    );
    const auto source_degrees = load_integer_arrays(
        argv[3], "source_distinct_target_degrees"
    );
    const auto source_incidences = load_integer_arrays(
        argv[3], "source_quotient_incidences"
    );
    const auto target_degrees = load_integer_arrays(
        argv[3], "target_distinct_shadow_source_degrees"
    );
    const auto target_incidences = load_integer_arrays(
        argv[3], "target_shadow_quotient_incidences"
    );
    if (shadow_sources.size() != 348 || targets.size() != 2823 ||
        source_degrees.size() != 1 || source_incidences.size() != 1 ||
        target_degrees.size() != 1 || target_incidences.size() != 1 ||
        source_degrees[0].size() != shadow_sources.size() ||
        source_incidences[0].size() != shadow_sources.size() ||
        target_degrees[0].size() != targets.size() ||
        target_incidences[0].size() != targets.size())
        throw std::runtime_error("shadow certificate aligned-array mismatch");

    Model model;
    std::unordered_map<State, std::size_t, StateHash> source_index;
    std::unordered_map<State, std::size_t, StateHash> target_index;
    source_index.reserve(shadow_sources.size());
    target_index.reserve(targets.size());
    for (std::size_t index = 0; index < shadow_sources.size(); ++index) {
        if (!(model.canonical(shadow_sources[index]) == shadow_sources[index]) ||
            !model.is_free(shadow_sources[index]) ||
            !source_index.emplace(shadow_sources[index], index).second)
            throw std::runtime_error("invalid shadow source array");
    }
    for (std::size_t index = 0; index < targets.size(); ++index) {
        if (!(model.canonical(targets[index]) == targets[index]) ||
            !model.is_free(targets[index]) ||
            !target_index.emplace(targets[index], index).second)
            throw std::runtime_error("invalid objective-twelve target array");
    }

    std::vector<std::unordered_map<State, std::uint16_t, StateHash>>
        source_neighbors(shadow_sources.size());
    std::vector<int> source_objectives(shadow_sources.size());
    std::vector<int> source_minimum_above_ten(shadow_sources.size());
#pragma omp parallel for schedule(dynamic, 1)
    for (std::size_t index = 0; index < shadow_sources.size(); ++index) {
        const Model::Analysis analysis = model.analyze(shadow_sources[index]);
        source_objectives[index] = analysis.objective;
        int minimum = std::numeric_limits<int>::max();
        auto& local = source_neighbors[index];
        for (int id = 0; id < edge_count; ++id) {
            const int objective = analysis.objective + analysis.delta[id];
            if (objective > 10) minimum = std::min(minimum, objective);
            if (objective != 12) continue;
            State neighbor = shadow_sources[index];
            neighbor.toggle(id);
            const State key = model.canonical(neighbor);
            if (local[key] == std::numeric_limits<std::uint16_t>::max())
                throw std::runtime_error("direct source incidence overflow");
            ++local[key];
        }
        source_minimum_above_ten[index] = minimum;
    }

    std::unordered_map<State, DirectTargetInfo, StateHash> direct_target_info;
    direct_target_info.reserve(targets.size());
    std::map<int, std::uint64_t> source_degree_histogram;
    std::uint64_t quotient_incidence = 0;
    std::uint64_t omissions = 0;
    std::uint64_t source_alignment_errors = 0;
    for (std::size_t index = 0; index < shadow_sources.size(); ++index) {
        if (source_objectives[index] != 10 || source_minimum_above_ten[index] != 12)
            throw std::runtime_error("direct shadow source objective mismatch");
        std::uint64_t local_incidence = 0;
        for (const auto& [target, multiplicity] : source_neighbors[index]) {
            if (!target_index.contains(target)) ++omissions;
            DirectTargetInfo& info = direct_target_info[target];
            info.incidence += multiplicity;
            info.source_indices.insert(index);
            local_incidence += multiplicity;
        }
        ++source_degree_histogram[
            static_cast<int>(source_neighbors[index].size())
        ];
        quotient_incidence += local_incidence;
        if (source_neighbors[index].size() !=
                static_cast<std::size_t>(source_degrees[0][index]) ||
            local_incidence !=
                static_cast<std::uint64_t>(source_incidences[0][index]))
            ++source_alignment_errors;
    }
    if (direct_target_info.size() != targets.size())
        throw std::runtime_error("direct target-set cardinality mismatch");

    struct TargetResult {
        int objective = 0;
        int minimum_neighbor = std::numeric_limits<int>::max();
        std::unordered_map<State, std::uint16_t, StateHash> reverse_shadow;
        std::unordered_set<State, StateHash> q10;
        std::unordered_set<State, StateHash> primary_q10;
        std::unordered_set<State, StateHash> q11;
    };
    std::vector<TargetResult> target_results(targets.size());
#pragma omp parallel for schedule(dynamic, 1)
    for (std::size_t index = 0; index < targets.size(); ++index) {
        const Model::Analysis analysis = model.analyze(targets[index]);
        TargetResult& result = target_results[index];
        result.objective = analysis.objective;
        for (int id = 0; id < edge_count; ++id) {
            const int objective = analysis.objective + analysis.delta[id];
            result.minimum_neighbor = std::min(result.minimum_neighbor, objective);
            if (objective != 10 && objective != 11) continue;
            State neighbor = targets[index];
            neighbor.toggle(id);
            const State key = model.canonical(neighbor);
            if (objective == 11) {
                result.q11.insert(key);
                continue;
            }
            result.q10.insert(key);
            if (complete_sources.contains(key)) result.primary_q10.insert(key);
            if (source_index.contains(key)) ++result.reverse_shadow[key];
        }
    }

    std::map<int, std::uint64_t> target_shadow_degree_histogram;
    std::map<int, std::uint64_t> target_minimum_histogram;
    std::map<int, std::uint64_t> target_q10_degree_histogram;
    std::map<int, std::uint64_t> target_primary_q10_degree_histogram;
    std::map<int, std::uint64_t> target_q11_degree_histogram;
    std::unordered_set<State, StateHash> all_q11;
    std::unordered_set<State, StateHash> primary_nonshadow;
    std::unordered_set<State, StateHash> external_q10;
    std::uint64_t target_alignment_errors = 0;
    std::uint64_t reverse_errors = 0;
    for (std::size_t index = 0; index < targets.size(); ++index) {
        const TargetResult& result = target_results[index];
        if (result.objective != 12)
            throw std::runtime_error("direct target objective mismatch");
        const DirectTargetInfo& expected = direct_target_info.at(targets[index]);
        std::uint64_t reverse_incidence = 0;
        for (const auto& [source, multiplicity] : result.reverse_shadow) {
            reverse_incidence += multiplicity;
            if (!expected.source_indices.contains(source_index.at(source)))
                ++reverse_errors;
        }
        if (result.reverse_shadow.size() != expected.source_indices.size() ||
            reverse_incidence != expected.incidence)
            ++reverse_errors;
        if (expected.source_indices.size() !=
                static_cast<std::size_t>(target_degrees[0][index]) ||
            expected.incidence !=
                static_cast<std::uint64_t>(target_incidences[0][index]))
            ++target_alignment_errors;
        ++target_shadow_degree_histogram[
            static_cast<int>(result.reverse_shadow.size())
        ];
        ++target_minimum_histogram[result.minimum_neighbor];
        ++target_q10_degree_histogram[static_cast<int>(result.q10.size())];
        ++target_primary_q10_degree_histogram[
            static_cast<int>(result.primary_q10.size())
        ];
        ++target_q11_degree_histogram[static_cast<int>(result.q11.size())];
        all_q11.insert(result.q11.begin(), result.q11.end());
        for (const State& source : result.q10) {
            if (!complete_sources.contains(source)) external_q10.insert(source);
            else if (!source_index.contains(source)) primary_nonshadow.insert(source);
        }
    }

    std::ofstream output(argv[4]);
    if (!output) throw std::runtime_error("cannot write direct verification");
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"direct_five_set_recount_source_count\": "
           << shadow_sources.size() << ",\n";
    output << "  \"direct_five_set_recount_target_count\": " << targets.size()
           << ",\n";
    output << "  \"shadow_to_objective_twelve_quotient_incidence\": "
           << quotient_incidence << ",\n";
    output << "  \"source_distinct_objective_twelve_degree_histogram\": {";
    write_histogram(output, source_degree_histogram);
    output << ",\n  \"target_distinct_shadow_source_degree_histogram\": {";
    write_histogram(output, target_shadow_degree_histogram);
    output << ",\n  \"target_minimum_one_flip_objective_histogram\": {";
    write_histogram(output, target_minimum_histogram);
    output << ",\n  \"target_distinct_objective_ten_neighbor_degree_histogram\": {";
    write_histogram(output, target_q10_degree_histogram);
    output << ",\n  \"target_distinct_primary_objective_ten_neighbor_degree_histogram\": {";
    write_histogram(output, target_primary_q10_degree_histogram);
    output << ",\n  \"target_distinct_objective_eleven_neighbor_degree_histogram\": {";
    write_histogram(output, target_q11_degree_histogram);
    output << ",\n  \"distinct_objective_eleven_neighbor_rotation_orbit_count\": "
           << all_q11.size() << ",\n";
    output << "  \"distinct_primary_nonshadow_objective_ten_neighbor_rotation_orbit_count\": "
           << primary_nonshadow.size() << ",\n";
    output << "  \"distinct_external_objective_ten_neighbor_rotation_orbit_count\": "
           << external_q10.size() << ",\n";
    output << "  \"omitted_objective_twelve_targets\": " << omissions << ",\n";
    output << "  \"source_aligned_array_errors\": " << source_alignment_errors
           << ",\n";
    output << "  \"target_aligned_array_errors\": " << target_alignment_errors
           << ",\n";
    output << "  \"reverse_adjacency_errors\": " << reverse_errors << ",\n";
    output << "  \"all_direct_checks_pass\": "
           << ((omissions == 0 && source_alignment_errors == 0 &&
                target_alignment_errors == 0 && reverse_errors == 0)
                   ? "true"
                   : "false")
           << ",\n";
    output << "  \"method\": \"independent direct recount of all 962598 five-vertex sets at every shadow source and every listed objective-twelve target, with exact cyclic canonicalization and bidirectional adjacency reconstruction\"\n}\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
