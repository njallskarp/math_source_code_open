#define main objective_six_component_embedded_main
#include "objective_six_component.cpp"
#undef main

#include <omp.h>

namespace {

struct BoundarySource {
    int objective = 0;
    int source_class = 0;  // 0 = P10, 1 = first F11, 2 = q11 closure addition.
    State state;
};

struct IncidenceRecord {
    State target;
    std::uint32_t source = 0;
    std::uint16_t multiplicity = 0;
};

struct DisjointSet {
    std::vector<std::uint32_t> parent;
    std::vector<std::uint8_t> rank;

    explicit DisjointSet(std::size_t size = 0) : parent(size), rank(size, 0) {
        std::iota(parent.begin(), parent.end(), 0);
    }

    std::uint32_t add() {
        const auto id = static_cast<std::uint32_t>(parent.size());
        parent.push_back(id);
        rank.push_back(0);
        return id;
    }

    std::uint32_t find(std::uint32_t value) {
        std::uint32_t root = value;
        while (parent[root] != root) root = parent[root];
        while (parent[value] != value) {
            const std::uint32_t next = parent[value];
            parent[value] = root;
            value = next;
        }
        return root;
    }

    void unite(std::uint32_t left, std::uint32_t right) {
        left = find(left);
        right = find(right);
        if (left == right) return;
        if (rank[left] < rank[right]) std::swap(left, right);
        parent[right] = left;
        if (rank[left] == rank[right]) ++rank[left];
    }
};

struct ThreadData {
    std::vector<IncidenceRecord> records;
    std::array<std::uint64_t, 12> source_count{};
    std::array<std::uint64_t, 12> raw_incidence{};
    std::array<std::uint64_t, 12> distinct_pair_count{};
    std::array<std::map<int, std::uint64_t>, 12> source_degree_histogram;
    std::uint64_t objective_errors = 0;
    std::uint64_t nonfree_targets = 0;
};

struct TargetAggregate {
    State state;
    std::uint32_t full_id = 0;
    std::uint32_t q11_id = std::numeric_limits<std::uint32_t>::max();
    std::uint64_t raw_incidence = 0;
    std::uint64_t q11_raw_incidence = 0;
    std::uint32_t source_degree = 0;
    std::uint32_t lower_source_degree = 0;
    std::uint32_t q11_source_degree = 0;
    std::uint32_t first_q11_source_degree = 0;
    std::uint32_t added_q11_source_degree = 0;
    int minimum_source_objective = 12;
    bool in_shadow_boundary = false;
};

struct ComponentAggregate {
    std::uint64_t source_vertices = 0;
    std::uint64_t target_vertices = 0;
    std::uint64_t edges = 0;
};

struct ComponentSummary {
    std::uint64_t count = 0;
    std::uint64_t cycle_rank = 0;
    ComponentAggregate largest;
    std::uint64_t largest_cycle_rank = 0;
    std::vector<std::pair<ComponentAggregate, std::uint64_t>> profiles;
};

template <class Key>
void write_histogram(
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

void append_sources(
    std::vector<BoundarySource>& sources, int objective, int source_class,
    const std::string& path, const std::string& key
) {
    for (const State& state : load_state_array(path, key))
        sources.push_back({objective, source_class, state});
}

std::vector<BoundarySource> load_lower_sources(
    const std::string& lower_six_path,
    const std::string& objective_seven_path,
    const std::string& objective_eight_path,
    const std::string& objective_nine_path,
    const std::string& objective_ten_frontier_path,
    const std::string& objective_ten_component_path
) {
    std::vector<BoundarySource> sources;
    for (int objective = 2; objective <= 6; ++objective)
        append_sources(
            sources, objective, 0, lower_six_path,
            "objective_" + std::to_string(objective) +
                "_rotation_representatives"
        );
    append_sources(
        sources, 7, 0, objective_seven_path,
        "objective_seven_component_rotation_representatives"
    );
    append_sources(
        sources, 8, 0, objective_eight_path,
        "objective_eight_component_rotation_representatives"
    );
    append_sources(
        sources, 7, 0, objective_nine_path,
        "new_objective_7_rotation_representatives"
    );
    append_sources(
        sources, 8, 0, objective_nine_path,
        "new_objective_8_rotation_representatives"
    );
    append_sources(
        sources, 9, 0, objective_nine_path,
        "new_objective_9_rotation_representatives"
    );
    append_sources(
        sources, 10, 0, objective_ten_frontier_path,
        "objective_ten_rotation_representatives"
    );
    append_sources(
        sources, 10, 0, objective_ten_component_path,
        "additional_objective_10_rotation_representatives"
    );
    return sources;
}

ComponentSummary summarize_components(
    DisjointSet& dsu, const std::vector<bool>& active_sources,
    const std::vector<TargetAggregate>& targets, bool q11_only,
    std::size_t lower_source_count
) {
    std::unordered_map<std::uint32_t, ComponentAggregate> components;
    components.reserve(targets.size() / 2 + 1);
    if (q11_only) {
        for (std::size_t index = lower_source_count;
             index < active_sources.size(); ++index) {
            if (!active_sources[index]) continue;
            ++components[dsu.find(static_cast<std::uint32_t>(
                index - lower_source_count
            ))].source_vertices;
        }
        for (const TargetAggregate& target : targets) {
            if (target.q11_source_degree == 0) continue;
            auto& component = components[dsu.find(target.q11_id)];
            ++component.target_vertices;
            component.edges += target.q11_raw_incidence;
        }
    } else {
        for (std::size_t index = 0; index < active_sources.size(); ++index) {
            if (!active_sources[index]) continue;
            ++components[dsu.find(static_cast<std::uint32_t>(index))]
                  .source_vertices;
        }
        for (const TargetAggregate& target : targets) {
            auto& component = components[dsu.find(target.full_id)];
            ++component.target_vertices;
            component.edges += target.raw_incidence;
        }
    }

    ComponentSummary summary;
    summary.count = components.size();
    for (const auto& [root, component] : components) {
        (void)root;
        const std::uint64_t rank =
            component.edges - component.source_vertices -
            component.target_vertices + 1;
        summary.cycle_rank += rank;
        summary.profiles.push_back({component, rank});
        const std::uint64_t vertices =
            component.source_vertices + component.target_vertices;
        const std::uint64_t largest_vertices =
            summary.largest.source_vertices + summary.largest.target_vertices;
        if (vertices > largest_vertices ||
            (vertices == largest_vertices &&
             component.edges > summary.largest.edges)) {
            summary.largest = component;
            summary.largest_cycle_rank = rank;
        }
    }
    std::sort(
        summary.profiles.begin(), summary.profiles.end(),
        [](const auto& left, const auto& right) {
            const std::uint64_t left_vertices =
                left.first.source_vertices + left.first.target_vertices;
            const std::uint64_t right_vertices =
                right.first.source_vertices + right.first.target_vertices;
            if (left_vertices != right_vertices)
                return left_vertices > right_vertices;
            return left.first.edges > right.first.edges;
        }
    );
    return summary;
}

void write_component_summary(
    std::ostream& output, const ComponentSummary& summary,
    bool include_profiles = false
) {
    output << "{\n"
           << "    \"component_count\": " << summary.count << ",\n"
           << "    \"cycle_rank\": " << summary.cycle_rank << ",\n"
           << "    \"largest_component_source_vertices\": "
           << summary.largest.source_vertices << ",\n"
           << "    \"largest_component_target_vertices\": "
           << summary.largest.target_vertices << ",\n"
           << "    \"largest_component_edges\": "
           << summary.largest.edges << ",\n"
           << "    \"largest_component_cycle_rank\": "
           << summary.largest_cycle_rank;
    if (include_profiles) {
        output << ",\n    \"components\": [";
        for (std::size_t index = 0; index < summary.profiles.size(); ++index) {
            const auto& [component, rank] = summary.profiles[index];
            if (index) output << ',';
            output << "\n      {\"source_vertices\": "
                   << component.source_vertices
                   << ", \"target_vertices\": "
                   << component.target_vertices << ", \"edges\": "
                   << component.edges << ", \"cycle_rank\": " << rank
                   << '}';
        }
        if (!summary.profiles.empty()) output << '\n';
        output << "    ]";
    }
    output << "\n  }";
}

void write_target_file(
    const std::string& path, const std::vector<TargetAggregate>& targets
) {
    std::ofstream output(path);
    if (!output) throw std::runtime_error("cannot write " + path);
    output << "{\n  \"objective_twelve_rotation_representatives\": [\n";
    for (std::size_t index = 0; index < targets.size(); ++index) {
        if (index) output << ",\n";
        output << "    ";
        Search::write_state(output, targets[index].state);
    }
    output << "\n  ]\n}\n";
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 13) {
        std::cerr
            << "usage: analyze_objective_twelve_frontier CERTIFICATE.json "
               "LOWER-SIX.json OBJECTIVE-SEVEN-COMPONENT.json "
               "OBJECTIVE-EIGHT-COMPONENT.json OBJECTIVE-NINE-COMPONENT.json "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OBJECTIVE-ELEVEN-FRONTIER.json OBJECTIVE-ELEVEN-COMPONENT.json "
               "OBJECTIVE-TWELVE-SHADOW.json SUMMARY.json TARGETS.json\n";
        return 2;
    }

    const std::set<std::pair<int, int>> flips = load_flips(argv[1]);
    std::vector<BoundarySource> sources = load_lower_sources(
        argv[2], argv[3], argv[4], argv[5], argv[6], argv[7]
    );
    const std::size_t lower_source_count = sources.size();
    append_sources(
        sources, 11, 1, argv[8],
        "objective_eleven_rotation_representatives"
    );
    const std::size_t first_q11_count = sources.size() - lower_source_count;
    append_sources(
        sources, 11, 2, argv[9],
        "complete_additional_objective_11_rotation_representatives"
    );
    const std::size_t q11_source_count = sources.size() - lower_source_count;
    if (first_q11_count != 372974 || q11_source_count != 373124)
        throw std::runtime_error("objective-eleven source count mismatch");

    const std::vector<State> shadow_targets = load_state_array(
        argv[10], "objective_twelve_shadow_frontier_rotation_representatives"
    );
    std::unordered_set<State, StateHash> shadow_set(
        shadow_targets.begin(), shadow_targets.end()
    );
    if (shadow_set.size() != 2823)
        throw std::runtime_error("shadow boundary count mismatch");

    const int thread_count = omp_get_max_threads();
    std::vector<ThreadData> thread_data(thread_count);
#pragma omp parallel
    {
        const int thread_id = omp_get_thread_num();
        ThreadData& data = thread_data[thread_id];
        Search search(flips);
        std::vector<State> local_targets;
        local_targets.reserve(32);
#pragma omp for schedule(dynamic, 64)
        for (std::int64_t source_index = 0;
             source_index < static_cast<std::int64_t>(sources.size());
             ++source_index) {
            const BoundarySource& source = sources[source_index];
            search.move_to(source.state);
            if (search.monochromatic_count != source.objective)
                ++data.objective_errors;
            local_targets.clear();
            for (int id = 0; id < edge_count; ++id) {
                if (search.resulting_count(id) != 12) continue;
                State neighbor = search.state;
                neighbor.toggle(id);
                if (search.rotate(neighbor, 1) == neighbor)
                    ++data.nonfree_targets;
                local_targets.push_back(search.canonical(neighbor));
            }
            ++data.source_count[source.objective];
            data.raw_incidence[source.objective] += local_targets.size();
            std::sort(local_targets.begin(), local_targets.end());
            std::size_t next = 0;
            int distinct_degree = 0;
            while (next < local_targets.size()) {
                const std::size_t begin = next++;
                while (next < local_targets.size() &&
                       local_targets[next] == local_targets[begin])
                    ++next;
                const std::size_t multiplicity = next - begin;
                if (multiplicity > std::numeric_limits<std::uint16_t>::max())
                    throw std::runtime_error("incidence multiplicity overflow");
                data.records.push_back(
                    {local_targets[begin],
                     static_cast<std::uint32_t>(source_index),
                     static_cast<std::uint16_t>(multiplicity)}
                );
                ++distinct_degree;
            }
            data.distinct_pair_count[source.objective] += distinct_degree;
            ++data.source_degree_histogram[source.objective][distinct_degree];
        }
    }

    std::array<std::uint64_t, 12> source_count{};
    std::array<std::uint64_t, 12> raw_incidence{};
    std::array<std::uint64_t, 12> distinct_pair_count{};
    std::array<std::map<int, std::uint64_t>, 12> source_degree_histogram;
    std::uint64_t objective_errors = 0;
    std::uint64_t nonfree_targets = 0;
    std::size_t record_count = 0;
    for (const ThreadData& data : thread_data) record_count += data.records.size();
    std::vector<IncidenceRecord> records;
    records.reserve(record_count);
    for (ThreadData& data : thread_data) {
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
        nonfree_targets += data.nonfree_targets;
        records.insert(
            records.end(), std::make_move_iterator(data.records.begin()),
            std::make_move_iterator(data.records.end())
        );
        std::vector<IncidenceRecord>().swap(data.records);
    }
    std::sort(
        records.begin(), records.end(),
        [](const IncidenceRecord& left, const IncidenceRecord& right) {
            if (left.target < right.target) return true;
            if (right.target < left.target) return false;
            return left.source < right.source;
        }
    );

    DisjointSet full_dsu(sources.size());
    DisjointSet q11_dsu(q11_source_count);
    std::vector<bool> active_sources(sources.size(), false);
    std::vector<TargetAggregate> targets;
    targets.reserve(records.size() / 2 + 1);
    std::map<int, std::uint64_t> target_source_degree_histogram;
    std::map<int, std::uint64_t> target_q11_degree_histogram;
    std::map<int, std::uint64_t> target_lower_degree_histogram;
    std::map<int, std::uint64_t> target_minimum_source_objective_histogram;
    std::map<int, std::uint64_t>
        lower_only_target_minimum_source_objective_histogram;
    std::map<int, std::uint64_t> lower_only_target_source_degree_histogram;
    std::uint64_t lower_only_targets = 0;
    std::uint64_t q11_only_targets = 0;
    std::uint64_t mixed_lower_q11_targets = 0;
    std::uint64_t first_only_q11_targets = 0;
    std::uint64_t addition_only_q11_targets = 0;
    std::uint64_t mixed_first_addition_targets = 0;
    std::uint64_t shadow_targets_found = 0;
    std::size_t position = 0;
    while (position < records.size()) {
        const std::size_t begin = position;
        while (position < records.size() &&
               records[position].target == records[begin].target)
            ++position;
        TargetAggregate target;
        target.state = records[begin].target;
        target.full_id = full_dsu.add();
        bool has_q11 = false;
        for (std::size_t index = begin; index < position; ++index) {
            const IncidenceRecord& record = records[index];
            const BoundarySource& source = sources[record.source];
            active_sources[record.source] = true;
            full_dsu.unite(record.source, target.full_id);
            target.raw_incidence += record.multiplicity;
            ++target.source_degree;
            target.minimum_source_objective =
                std::min(target.minimum_source_objective, source.objective);
            if (source.source_class == 0) {
                ++target.lower_source_degree;
            } else {
                if (!has_q11) {
                    target.q11_id = q11_dsu.add();
                    has_q11 = true;
                }
                const auto q11_source = static_cast<std::uint32_t>(
                    record.source - lower_source_count
                );
                q11_dsu.unite(q11_source, target.q11_id);
                target.q11_raw_incidence += record.multiplicity;
                ++target.q11_source_degree;
                if (source.source_class == 1)
                    ++target.first_q11_source_degree;
                else
                    ++target.added_q11_source_degree;
            }
        }
        target.in_shadow_boundary = shadow_set.contains(target.state);
        shadow_targets_found += target.in_shadow_boundary;
        ++target_source_degree_histogram[target.source_degree];
        ++target_q11_degree_histogram[target.q11_source_degree];
        ++target_lower_degree_histogram[target.lower_source_degree];
        ++target_minimum_source_objective_histogram[
            target.minimum_source_objective
        ];
        if (target.q11_source_degree == 0) {
            ++lower_only_targets;
            ++lower_only_target_minimum_source_objective_histogram[
                target.minimum_source_objective
            ];
            ++lower_only_target_source_degree_histogram[
                target.lower_source_degree
            ];
        } else if (target.lower_source_degree == 0)
            ++q11_only_targets;
        else
            ++mixed_lower_q11_targets;
        if (target.q11_source_degree > 0) {
            if (target.added_q11_source_degree == 0)
                ++first_only_q11_targets;
            else if (target.first_q11_source_degree == 0)
                ++addition_only_q11_targets;
            else
                ++mixed_first_addition_targets;
        }
        targets.push_back(std::move(target));
    }

    const ComponentSummary full_components = summarize_components(
        full_dsu, active_sources, targets, false, lower_source_count
    );
    const ComponentSummary q11_components = summarize_components(
        q11_dsu, active_sources, targets, true, lower_source_count
    );

    std::ofstream output(argv[11]);
    if (!output) throw std::runtime_error("cannot write summary");
    const std::uint64_t total_raw = std::accumulate(
        raw_incidence.begin(), raw_incidence.end(), std::uint64_t{0}
    );
    const std::uint64_t total_pairs = std::accumulate(
        distinct_pair_count.begin(), distinct_pair_count.end(),
        std::uint64_t{0}
    );
    output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
    output << "  \"primary_sublevel_ten_source_rotation_orbit_count\": "
           << lower_source_count << ",\n";
    output << "  \"complete_objective_eleven_source_rotation_orbit_count\": "
           << q11_source_count << ",\n";
    output << "  \"objective_twelve_frontier_rotation_orbit_count\": "
           << targets.size() << ",\n";
    output << "  \"objective_twelve_frontier_vertex_count\": "
           << orbit_size * targets.size() << ",\n";
    output << "  \"frontier_quotient_incidence\": " << total_raw << ",\n";
    output << "  \"frontier_labeled_incidence\": "
           << orbit_size * total_raw << ",\n";
    output << "  \"distinct_source_target_pairs\": " << total_pairs
           << ",\n";
    output << "  \"source_target_parallel_edge_excess\": "
           << total_raw - total_pairs << ",\n";
    output << "  \"q11_derived_target_count\": "
           << targets.size() - lower_only_targets << ",\n";
    output << "  \"lower_only_target_count\": " << lower_only_targets
           << ",\n";
    output << "  \"all_boundary_targets_adjacent_to_q11_layer\": "
           << (lower_only_targets == 0 ? "true" : "false") << ",\n";
    output << "  \"q11_only_target_count\": " << q11_only_targets
           << ",\n";
    output << "  \"mixed_lower_q11_target_count\": "
           << mixed_lower_q11_targets << ",\n";
    output << "  \"first_frontier_only_q11_target_count\": "
           << first_only_q11_targets << ",\n";
    output << "  \"addition_only_q11_target_count\": "
           << addition_only_q11_targets << ",\n";
    output << "  \"mixed_first_addition_q11_target_count\": "
           << mixed_first_addition_targets << ",\n";
    output << "  \"shadow_boundary_target_count_expected\": 2823,\n";
    output << "  \"shadow_boundary_target_count_found\": "
           << shadow_targets_found << ",\n";
    output << "  \"objective_errors\": " << objective_errors << ",\n";
    output << "  \"nonfree_target_encounters\": " << nonfree_targets
           << ",\n";
    output << "  \"source_count_by_objective\": {";
    bool separator = false;
    for (int objective = 0; objective <= 11; ++objective) {
        if (source_count[objective] == 0) continue;
        if (separator) output << ',';
        output << "\n    \"" << objective << "\": "
               << source_count[objective];
        separator = true;
    }
    output << "\n  },\n  \"raw_incidence_by_source_objective\": {";
    separator = false;
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
        write_histogram(
            output, source_degree_histogram[objective], 4
        );
        separator = true;
    }
    output << "\n  },\n  \"target_source_degree_histogram\": ";
    write_histogram(output, target_source_degree_histogram, 2);
    output << ",\n  \"target_q11_source_degree_histogram\": ";
    write_histogram(output, target_q11_degree_histogram, 2);
    output << ",\n  \"target_lower_source_degree_histogram\": ";
    write_histogram(output, target_lower_degree_histogram, 2);
    output << ",\n  \"target_minimum_source_objective_histogram\": ";
    write_histogram(output, target_minimum_source_objective_histogram, 2);
    output << ",\n  \"lower_only_target_minimum_source_objective_histogram\": ";
    write_histogram(
        output, lower_only_target_minimum_source_objective_histogram, 2
    );
    output << ",\n  \"lower_only_target_source_degree_histogram\": ";
    write_histogram(output, lower_only_target_source_degree_histogram, 2);
    output << ",\n  \"q11_boundary_bipartite_components\": ";
    write_component_summary(output, q11_components);
    output << ",\n  \"full_boundary_bipartite_components\": ";
    write_component_summary(output, full_components, true);
    output << ",\n  \"all_internal_checks_pass\": "
           << ((objective_errors == 0 && nonfree_targets == 0 &&
                shadow_targets_found == 2823)
                   ? "true"
                   : "false")
           << ",\n";
    output << "  \"method\": \"parallel exact incremental scan of every one-edge move from every rotation-orbit representative in the complete primary sublevel-eleven component, followed by canonical target sorting, complete quotient-incidence reconstruction, and bipartite component analysis\",\n";
    output << "  \"scope_note\": \"Complete objective-twelve one-flip boundary of the connected primary Cyclic(43) sublevel-eleven component; disconnected sublevel-eleven components elsewhere in the full coloring space remain out of scope.\"\n}\n";
    output.close();
    write_target_file(argv[12], targets);
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
