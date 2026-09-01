#define main objective_six_component_embedded_main
#include "objective_six_component.cpp"
#undef main

#include <atomic>
#include <bit>
#include <memory>
#include <omp.h>

namespace {

struct BoundarySource {
    int objective = 0;
    int source_class = 0;
    State state;
};

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

struct BinaryIncidence {
    std::uint32_t source = 0;
    std::uint32_t target = 0;
};

static_assert(sizeof(BinaryIncidence) == 8);

struct StreamThreadData {
    std::vector<BinaryIncidence> incidences;
    std::array<std::uint64_t, 12> incidence_by_source_objective{};
    std::uint64_t objective_errors = 0;
    std::uint64_t missing_targets = 0;
    std::uint64_t nonfree_target_encounters = 0;
};

void write_binary_sources(
    const std::string& state_path, const std::string& objective_path,
    const std::vector<BoundarySource>& sources
) {
    std::ofstream states(state_path, std::ios::binary);
    std::ofstream objectives(objective_path, std::ios::binary);
    if (!states || !objectives)
        throw std::runtime_error("cannot open binary source output");
    for (const BoundarySource& source : sources) {
        states.write(
            reinterpret_cast<const char*>(source.state.words.data()),
            static_cast<std::streamsize>(sizeof(std::uint64_t) * word_count)
        );
        const auto objective = static_cast<std::uint8_t>(source.objective);
        objectives.write(reinterpret_cast<const char*>(&objective), 1);
    }
    if (!states || !objectives)
        throw std::runtime_error("failed to write binary source output");
}

}  // namespace

int main(int argc, char** argv) try {
    if (argc != 15) {
        std::cerr
            << "usage: stream_objective_twelve_incidence CERTIFICATE.json "
               "LOWER-SIX.json OBJECTIVE-SEVEN-COMPONENT.json "
               "OBJECTIVE-EIGHT-COMPONENT.json OBJECTIVE-NINE-COMPONENT.json "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OBJECTIVE-ELEVEN-FRONTIER.json OBJECTIVE-ELEVEN-COMPONENT.json "
               "OBJECTIVE-TWELVE-TARGETS.json INCIDENCE.bin SOURCE-STATES.bin "
               "SOURCE-OBJECTIVES.bin METADATA.json\n";
        return 2;
    }
    if (std::endian::native != std::endian::little)
        throw std::runtime_error("binary stream requires little-endian host");

    const std::set<std::pair<int, int>> flips = load_flips(argv[1]);
    std::vector<BoundarySource> sources = load_lower_sources(
        argv[2], argv[3], argv[4], argv[5], argv[6], argv[7]
    );
    const std::size_t lower_source_count = sources.size();
    append_sources(
        sources, 11, 1, argv[8],
        "objective_eleven_rotation_representatives"
    );
    append_sources(
        sources, 11, 2, argv[9],
        "complete_additional_objective_11_rotation_representatives"
    );
    if (lower_source_count != 191067 || sources.size() != 564191)
        throw std::runtime_error("source count mismatch");

    const std::vector<State> targets = load_state_array(
        argv[10], "objective_twelve_rotation_representatives"
    );
    if (targets.size() != 1041887 ||
        !std::is_sorted(targets.begin(), targets.end()) ||
        std::adjacent_find(targets.begin(), targets.end()) != targets.end())
        throw std::runtime_error("target array is not sorted and unique");
    std::unordered_map<State, std::uint32_t, StateHash> target_ids;
    target_ids.reserve(targets.size() * 2);
    for (std::size_t index = 0; index < targets.size(); ++index) {
        if (!target_ids.emplace(
                targets[index], static_cast<std::uint32_t>(index)
            ).second)
            throw std::runtime_error("duplicate target state");
    }

    write_binary_sources(argv[12], argv[13], sources);

    const int thread_count = omp_get_max_threads();
    std::vector<std::unique_ptr<Search>> engines;
    engines.reserve(thread_count);
    for (int thread = 0; thread < thread_count; ++thread)
        engines.push_back(std::make_unique<Search>(flips));
    std::vector<StreamThreadData> thread_data(thread_count);
    for (StreamThreadData& data : thread_data)
        data.incidences.reserve(500000);
    std::atomic<std::uint64_t> processed = 0;

#pragma omp parallel
    {
        const int thread_id = omp_get_thread_num();
        Search& search = *engines[thread_id];
        StreamThreadData& data = thread_data[thread_id];
        const std::size_t begin =
            sources.size() * static_cast<std::size_t>(thread_id) /
            static_cast<std::size_t>(thread_count);
        const std::size_t end =
            sources.size() * static_cast<std::size_t>(thread_id + 1) /
            static_cast<std::size_t>(thread_count);
        for (std::size_t source_index = begin; source_index < end;
             ++source_index) {
            const BoundarySource& source = sources[source_index];
            search.move_to(source.state);
            if (search.monochromatic_count != source.objective)
                ++data.objective_errors;
            for (int id = 0; id < edge_count; ++id) {
                if (search.resulting_count(id) != 12) continue;
                State neighbor = search.state;
                neighbor.toggle(id);
                if (search.rotate(neighbor, 1) == neighbor)
                    ++data.nonfree_target_encounters;
                const State key = search.canonical(neighbor);
                const auto found = target_ids.find(key);
                if (found == target_ids.end()) {
                    ++data.missing_targets;
                    continue;
                }
                data.incidences.push_back(
                    {static_cast<std::uint32_t>(source_index), found->second}
                );
                ++data.incidence_by_source_objective[source.objective];
            }
            const auto done = ++processed;
            if (thread_id == 0 && done % 50000 == 0)
                std::cerr << "objective-twelve incidence stream: " << done
                          << '/' << sources.size() << " sources\n";
        }
    }

    std::ofstream incidence_output(argv[11], std::ios::binary);
    if (!incidence_output)
        throw std::runtime_error("cannot open incidence output");
    std::array<std::uint64_t, 12> incidence_by_source_objective{};
    std::uint64_t objective_errors = 0;
    std::uint64_t missing_targets = 0;
    std::uint64_t nonfree_target_encounters = 0;
    std::uint64_t incidence_count = 0;
    for (const StreamThreadData& data : thread_data) {
        incidence_output.write(
            reinterpret_cast<const char*>(data.incidences.data()),
            static_cast<std::streamsize>(
                sizeof(BinaryIncidence) * data.incidences.size()
            )
        );
        incidence_count += data.incidences.size();
        for (int objective = 0; objective <= 11; ++objective)
            incidence_by_source_objective[objective] +=
                data.incidence_by_source_objective[objective];
        objective_errors += data.objective_errors;
        missing_targets += data.missing_targets;
        nonfree_target_encounters += data.nonfree_target_encounters;
    }
    if (!incidence_output)
        throw std::runtime_error("failed to write incidence output");

    std::ofstream metadata(argv[14]);
    if (!metadata) throw std::runtime_error("cannot open metadata output");
    metadata << "{\n  \"format\": \"little-endian uint32 source_id, "
                "uint32 target_id records\",\n";
    metadata << "  \"source_state_format\": \"little-endian 15 x uint64 "
                "words per source\",\n";
    metadata << "  \"source_objective_format\": \"one uint8 per source\",\n";
    metadata << "  \"source_count\": " << sources.size() << ",\n";
    metadata << "  \"lower_source_count\": " << lower_source_count << ",\n";
    metadata << "  \"q11_source_count\": "
             << sources.size() - lower_source_count << ",\n";
    metadata << "  \"target_count\": " << targets.size() << ",\n";
    metadata << "  \"incidence_count\": " << incidence_count << ",\n";
    metadata << "  \"incidence_by_source_objective\": {";
    bool separator = false;
    for (int objective = 0; objective <= 11; ++objective) {
        if (incidence_by_source_objective[objective] == 0) continue;
        if (separator) metadata << ',';
        metadata << "\n    \"" << objective << "\": "
                 << incidence_by_source_objective[objective];
        separator = true;
    }
    metadata << "\n  },\n";
    metadata << "  \"objective_errors\": " << objective_errors << ",\n";
    metadata << "  \"missing_targets\": " << missing_targets << ",\n";
    metadata << "  \"nonfree_target_encounters\": "
             << nonfree_target_encounters << ",\n";
    metadata << "  \"all_stream_checks_pass\": "
             << ((incidence_count == 4656506 && objective_errors == 0 &&
                  missing_targets == 0 && nonfree_target_encounters == 0)
                     ? "true"
                     : "false")
             << ",\n";
    metadata << "  \"method\": \"complete rescan of every source-edge "
                "pair with exact incremental clique deltas and lookup into "
                "the independently verified sorted q12 target array\"\n}\n";
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
