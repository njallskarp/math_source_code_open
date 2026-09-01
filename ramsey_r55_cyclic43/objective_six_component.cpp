#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <regex>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr int order = 43;
constexpr int edge_count = order * (order - 1) / 2;
constexpr int word_count = (edge_count + 63) / 64;
constexpr std::uint64_t orbit_size = order;

struct State {
    std::array<std::uint64_t, word_count> words{};

    bool operator==(const State&) const = default;
    bool operator<(const State& other) const { return words < other.words; }

    bool contains(int edge) const {
        return (words[edge / 64] >> (edge % 64)) & 1ULL;
    }
    void toggle(int edge) { words[edge / 64] ^= 1ULL << (edge % 64); }
};

struct StateHash {
    std::size_t operator()(const State& state) const noexcept {
        std::uint64_t hash = 0x9e3779b97f4a7c15ULL;
        for (std::uint64_t word : state.words) {
            word ^= word >> 30;
            word *= 0xbf58476d1ce4e5b9ULL;
            word ^= word >> 27;
            word *= 0x94d049bb133111ebULL;
            word ^= word >> 31;
            hash ^= word + 0x9e3779b97f4a7c15ULL + (hash << 6) + (hash >> 2);
        }
        return static_cast<std::size_t>(hash);
    }
};

struct FiveSet {
    std::array<std::uint16_t, 10> edges{};
};

std::string read_text(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open " + path);
    std::ostringstream buffer;
    buffer << input.rdbuf();
    return buffer.str();
}

std::string keyed_array(const std::string& text, const std::string& key) {
    const auto key_position = text.find('"' + key + '"');
    if (key_position == std::string::npos)
        throw std::runtime_error("missing JSON key " + key);
    const auto begin = text.find('[', key_position);
    if (begin == std::string::npos)
        throw std::runtime_error("malformed JSON array " + key);
    std::size_t end = begin;
    int nesting = 0;
    do {
        if (text[end] == '[') ++nesting;
        if (text[end] == ']') --nesting;
        ++end;
    } while (end < text.size() && nesting != 0);
    if (nesting != 0) throw std::runtime_error("unterminated JSON array " + key);
    return text.substr(begin, end - begin);
}

std::set<std::pair<int, int>> load_flips(const std::string& path) {
    const std::string array = keyed_array(read_text(path), "flipped_edges");
    const std::regex pair_pattern(R"(\[\s*([0-9]+)\s*,\s*([0-9]+)\s*\])");
    std::set<std::pair<int, int>> flips;
    for (std::sregex_iterator it(array.begin(), array.end(), pair_pattern), last;
         it != last; ++it) {
        int a = std::stoi((*it)[1]);
        int b = std::stoi((*it)[2]);
        if (a > b) std::swap(a, b);
        if (a < 0 || b >= order || a == b)
            throw std::runtime_error("invalid flipped edge");
        flips.insert({a, b});
    }
    if (flips.empty()) throw std::runtime_error("empty flipped_edges");
    return flips;
}

std::vector<int> load_integer_array(
    const std::string& path, const std::string& key
) {
    const std::string array = keyed_array(read_text(path), key);
    const std::regex integer_pattern(R"(([0-9]+))");
    std::vector<int> result;
    for (std::sregex_iterator it(array.begin(), array.end(), integer_pattern), last;
         it != last; ++it) {
        result.push_back(std::stoi((*it)[1]));
    }
    return result;
}

struct Search {
    std::array<std::array<int, order>, order> edge_id{};
    std::array<std::pair<int, int>, edge_count> edge_vertices{};
    std::array<std::array<std::uint16_t, edge_count>, order> rotated_edge{};
    std::array<bool, edge_count> seed_red{};
    std::array<bool, edge_count> red{};
    State state;
    std::vector<FiveSet> five_sets;
    std::vector<std::vector<std::uint32_t>> incident;
    std::vector<std::uint8_t> red_count;
    std::array<int, edge_count> single_flip_delta{};
    int monochromatic_count = 0;

    std::array<std::unordered_set<State, StateHash>, 9> orbit_states;
    std::unordered_set<State, StateHash> first_objective_six_frontier;
    std::unordered_map<State, std::array<std::uint16_t, 7>, StateHash>
        first_objective_seven_incidence;
    std::unordered_map<State, std::array<std::uint16_t, 8>, StateHash>
        first_objective_eight_incidence;
    std::unordered_map<State, std::array<std::uint16_t, 9>, StateHash>
        first_objective_nine_incidence;
    std::array<std::map<int, std::uint64_t>, 7> aggregate_histogram;
    std::array<std::map<int, std::uint64_t>, 7> directed_to_higher;
    std::array<std::uint64_t, 7> same_layer_directed{};
    std::array<std::array<std::unordered_set<State, StateHash>, 7>, 7>
        lower_neighbor_orbits;

    explicit Search(const std::set<std::pair<int, int>>& certificate_flips)
        : incident(edge_count) {
        int next_edge = 0;
        for (int a = 0; a < order; ++a) {
            for (int b = a + 1; b < order; ++b) {
                edge_id[a][b] = edge_id[b][a] = next_edge;
                edge_vertices[next_edge] = {a, b};
                int delta = (a - b) % order;
                if (delta < 0) delta += order;
                const int distance = std::min(delta, order - delta);
                seed_red[next_edge] =
                    distance == 1 || distance == 2 || distance == 7 ||
                    distance == 10 || distance == 12 || distance == 13 ||
                    distance == 14 || distance == 16 || distance == 18 ||
                    distance == 20 || distance == 21;
                if (certificate_flips.contains({a, b})) state.toggle(next_edge);
                red[next_edge] = seed_red[next_edge] != state.contains(next_edge);
                ++next_edge;
            }
        }
        if (next_edge != edge_count) throw std::logic_error("edge count");

        for (int offset = 0; offset < order; ++offset) {
            for (int id = 0; id < edge_count; ++id) {
                auto [a, b] = edge_vertices[id];
                a = (a + offset) % order;
                b = (b + offset) % order;
                rotated_edge[offset][id] = static_cast<std::uint16_t>(edge_id[a][b]);
            }
        }

        five_sets.reserve(962598);
        red_count.reserve(962598);
        for (int a = 0; a < order; ++a)
            for (int b = a + 1; b < order; ++b)
                for (int c = b + 1; c < order; ++c)
                    for (int d = c + 1; d < order; ++d)
                        for (int e = d + 1; e < order; ++e) {
                            const std::array<int, 5> vertices = {a, b, c, d, e};
                            FiveSet five;
                            int position = 0;
                            int reds = 0;
                            for (int i = 0; i < 5; ++i) {
                                for (int j = i + 1; j < 5; ++j) {
                                    const int id = edge_id[vertices[i]][vertices[j]];
                                    five.edges[position++] =
                                        static_cast<std::uint16_t>(id);
                                    reds += red[id];
                                }
                            }
                            const auto five_id =
                                static_cast<std::uint32_t>(five_sets.size());
                            for (int id : five.edges) incident[id].push_back(five_id);
                            five_sets.push_back(five);
                            red_count.push_back(static_cast<std::uint8_t>(reds));
                            monochromatic_count += is_monochromatic(reds);
                        }
        if (five_sets.size() != 962598) throw std::logic_error("five-set count");
        if (monochromatic_count != 2)
            throw std::runtime_error("certificate is not objective two");
        for (const auto& list : incident)
            if (list.size() != 10660) throw std::logic_error("incidence count");
        for (std::size_t five_id = 0; five_id < five_sets.size(); ++five_id)
            add_contribution(static_cast<std::uint32_t>(five_id), +1);
    }

    static int is_monochromatic(int count) {
        return count == 0 || count == 10;
    }

    int contribution(int count, int id) const {
        const int direction = red[id] ? -1 : 1;
        return is_monochromatic(count + direction) - is_monochromatic(count);
    }

    void add_contribution(std::uint32_t five_id, int sign) {
        const int count = red_count[five_id];
        for (int id : five_sets[five_id].edges)
            single_flip_delta[id] += sign * contribution(count, id);
    }

    int resulting_count(int id) const {
        return monochromatic_count + single_flip_delta[id];
    }

    void toggle(int id) {
        for (std::uint32_t five_id : incident[id]) add_contribution(five_id, -1);
        const int direction = red[id] ? -1 : 1;
        red[id] = !red[id];
        state.toggle(id);
        for (std::uint32_t five_id : incident[id]) {
            const int old_count = red_count[five_id];
            const int new_count = old_count + direction;
            monochromatic_count +=
                is_monochromatic(new_count) - is_monochromatic(old_count);
            red_count[five_id] = static_cast<std::uint8_t>(new_count);
            add_contribution(five_id, +1);
        }
    }

    State rotate(const State& source, int offset) const {
        State result;
        for (int word_index = 0; word_index < word_count; ++word_index) {
            std::uint64_t word = source.words[word_index];
            while (word) {
                const int bit = std::countr_zero(word);
                const int id = 64 * word_index + bit;
                if (id < edge_count) {
                    const int mapped = rotated_edge[offset][id];
                    result.words[mapped / 64] |= 1ULL << (mapped % 64);
                }
                word &= word - 1;
            }
        }
        return result;
    }

    State canonical(const State& source) const {
        State best = source;
        for (int offset = 1; offset < order; ++offset) {
            State candidate = rotate(source, offset);
            if (candidate < best) best = candidate;
        }
        return best;
    }

    void require_free_orbit(const State& source) const {
        if (rotate(source, 1) == source)
            throw std::runtime_error("non-free rotation orbit encountered");
    }

    int length_one_edge(int position) const {
        if (position < 0 || position >= order)
            throw std::runtime_error("invalid length-one position");
        return position == order - 1 ? edge_id[0][order - 1]
                                     : edge_id[position][position + 1];
    }

    std::vector<int> boundary_positions(int state_index) const {
        const int k = state_index / 2;
        const int last = state_index % 2 ? k : k - 1;
        std::vector<int> positions;
        for (int j = k - 8; j <= last; ++j) {
            int value = (17 * j) % order;
            if (value < 0) value += order;
            positions.push_back(value);
        }
        std::sort(positions.begin(), positions.end());
        return positions;
    }

    void record_lower_neighbor(int level, int objective, int id) {
        State neighbor = state;
        neighbor.toggle(id);
        lower_neighbor_orbits[level][objective].insert(canonical(neighbor));
    }

    void record_objective_seven_neighbor(int source_level, int id) {
        State neighbor = state;
        neighbor.toggle(id);
        const State key = canonical(neighbor);
        require_free_orbit(neighbor);
        auto& incidence = first_objective_seven_incidence[key];
        if (incidence[source_level] ==
            std::numeric_limits<std::uint16_t>::max())
            throw std::runtime_error("objective-seven incidence overflow");
        ++incidence[source_level];
    }

    void record_objective_eight_neighbor(int source_level, int id) {
        State neighbor = state;
        neighbor.toggle(id);
        const State key = canonical(neighbor);
        require_free_orbit(neighbor);
        auto& incidence = first_objective_eight_incidence[key];
        if (incidence[source_level] ==
            std::numeric_limits<std::uint16_t>::max())
            throw std::runtime_error("objective-eight incidence overflow");
        ++incidence[source_level];
    }

    void record_objective_nine_neighbor(int source_level, int id) {
        State neighbor = state;
        neighbor.toggle(id);
        const State key = canonical(neighbor);
        require_free_orbit(neighbor);
        auto& incidence = first_objective_nine_incidence[key];
        if (incidence[source_level] ==
            std::numeric_limits<std::uint16_t>::max())
            throw std::runtime_error("objective-nine incidence overflow");
        ++incidence[source_level];
    }

    void ensure_level(int target, int source_level, int id) {
        State neighbor = state;
        neighbor.toggle(id);
        State key = canonical(neighbor);
        if (target == 6 && source_level <= 5) {
            first_objective_six_frontier.insert(key);
            directed_to_higher[source_level][6] += orbit_size;
        }
        if (target == 5 && source_level <= 4)
            directed_to_higher[source_level][5] += orbit_size;
        if (target == 4 && source_level <= 3)
            directed_to_higher[source_level][4] += orbit_size;

        if (!orbit_states[target].insert(key).second) return;
        require_free_orbit(neighbor);
        toggle(id);
        scan_level(target);
        toggle(id);
    }

    void scan_level(int level) {
        if (monochromatic_count != level)
            throw std::logic_error("scan level objective mismatch");

        for (int id = 0; id < edge_count; ++id)
            aggregate_histogram[level][resulting_count(id)] += orbit_size;

        for (int id = 0; id < edge_count; ++id) {
            const int objective = resulting_count(id);
            if (objective == 7) record_objective_seven_neighbor(level, id);
            if (objective == 8) record_objective_eight_neighbor(level, id);
            if (objective == 9) record_objective_nine_neighbor(level, id);
            if (objective < level) {
                record_lower_neighbor(level, objective, id);
            } else if (objective == level) {
                same_layer_directed[level] += orbit_size;
                ensure_level(level, level, id);
            } else if (objective <= 6) {
                ensure_level(objective, level, id);
            }
        }
    }

    void scan_source(int level) {
        if (monochromatic_count != level)
            throw std::logic_error("source objective mismatch");
        const State key = canonical(state);
        require_free_orbit(state);
        orbit_states[level].insert(key);
        for (int id = 0; id < edge_count; ++id) {
            const int objective = resulting_count(id);
            if (objective == 7) record_objective_seven_neighbor(level, id);
            if (objective == 8) record_objective_eight_neighbor(level, id);
            if (objective == 9) record_objective_nine_neighbor(level, id);
            if (objective >= 4 && objective <= 6)
                ensure_level(objective, level, id);
        }
    }

    bool known_at_objective(int objective, const State& key) const {
        if (objective < 2 || objective > 5) return false;
        return orbit_states[objective].contains(key);
    }

    void verify_lower_neighbors() const {
        for (int level = 4; level <= 6; ++level) {
            for (int objective = 0; objective < level; ++objective) {
                for (const State& key : lower_neighbor_orbits[level][objective]) {
                    if (!known_at_objective(objective, key))
                        throw std::runtime_error(
                            "new lower-objective orbit found from level " +
                            std::to_string(level) + " to " +
                            std::to_string(objective)
                        );
                }
            }
        }
    }

    void run(const std::vector<int>& transport_positions) {
        if (transport_positions.size() != 2 * order)
            throw std::runtime_error("cycle must contain 86 transport positions");

        std::vector<State> centers;
        centers.reserve(2 * order);
        State active = state;
        for (int position : transport_positions) {
            centers.push_back(active);
            active.toggle(length_one_edge(position));
        }
        if (!(active == state)) throw std::runtime_error("transport does not close");

        for (std::size_t state_index = 0; state_index < centers.size(); ++state_index) {
            const State& center = centers[state_index];
            orbit_states[2].insert(canonical(center));
            for (int position : boundary_positions(static_cast<int>(state_index))) {
                State boundary = center;
                boundary.toggle(length_one_edge(position));
                orbit_states[3].insert(canonical(boundary));
            }
        }
        if (orbit_states[2].size() != 2 || orbit_states[3].size() != 17)
            throw std::runtime_error("unexpected sublevel-three orbit counts");

        for (int parity = 0; parity < 2; ++parity) {
            State target = centers[parity];
            State difference;
            for (int word = 0; word < word_count; ++word)
                difference.words[word] = state.words[word] ^ target.words[word];
            for (int word = 0; word < word_count; ++word) {
                std::uint64_t bits = difference.words[word];
                while (bits) {
                    const int bit = std::countr_zero(bits);
                    toggle(64 * word + bit);
                    bits &= bits - 1;
                }
            }
            scan_source(2);
            for (int position : boundary_positions(parity)) {
                const int id = length_one_edge(position);
                toggle(id);
                scan_source(3);
                toggle(id);
            }
        }
        verify_lower_neighbors();
        validate_known_layers();
    }

    std::uint64_t directed_sum(int target) const {
        std::uint64_t result = 0;
        for (int source = 2; source < target; ++source) {
            auto it = directed_to_higher[source].find(target);
            if (it != directed_to_higher[source].end()) result += it->second;
        }
        return result;
    }

    void validate_known_layers() const {
        if (orbit_states[4].size() != 78)
            throw std::runtime_error("objective-four orbit mismatch");
        if (orbit_states[5].size() != 306)
            throw std::runtime_error("objective-five orbit mismatch");
        if (first_objective_six_frontier.size() != 1144)
            throw std::runtime_error("objective-six first-frontier mismatch");
        if (directed_sum(4) != 5934)
            throw std::runtime_error("objective-four lower-incidence mismatch");
        if (directed_sum(5) != 29541)
            throw std::runtime_error("objective-five lower-incidence mismatch");
        if (directed_sum(6) != 129473)
            throw std::runtime_error("objective-six lower-incidence mismatch");
        if (same_layer_directed[4] != 2 * 3182)
            throw std::runtime_error("objective-four induced-edge mismatch");
        if (same_layer_directed[5] != 2 * 12728)
            throw std::runtime_error("objective-five induced-edge mismatch");
    }

    void write_representatives(const std::string& path) const {
        std::vector<State> representatives(
            orbit_states[6].begin(), orbit_states[6].end()
        );
        std::sort(representatives.begin(), representatives.end());
        std::ofstream output(path);
        if (!output) throw std::runtime_error("cannot write " + path);
        output << "{\n  \"order\": 43,\n";
        output << "  \"edge_order\": \"lexicographic pairs (a,b), 0<=a<b<43\",\n";
        output << "  \"objective_six_rotation_representatives\": [\n";
        for (std::size_t index = 0; index < representatives.size(); ++index) {
            if (index) output << ",\n";
            output << "    [";
            bool separator = false;
            for (int id = 0; id < edge_count; ++id) {
                if (!representatives[index].contains(id)) continue;
                if (separator) output << ',';
                output << id;
                separator = true;
            }
            output << ']';
        }
        output << "\n  ]\n}\n";
    }

    static void write_state(std::ostream& output, const State& state) {
        output << '[';
        bool separator = false;
        for (int id = 0; id < edge_count; ++id) {
            if (!state.contains(id)) continue;
            if (separator) output << ',';
            output << id;
            separator = true;
        }
        output << ']';
    }

    void write_objective_seven_frontier(const std::string& path) const {
        std::vector<State> frontier;
        frontier.reserve(first_objective_seven_incidence.size());
        for (const auto& [state, incidence] : first_objective_seven_incidence) {
            (void)incidence;
            frontier.push_back(state);
        }
        std::sort(frontier.begin(), frontier.end());

        std::array<std::uint64_t, 7> directed_by_source{};
        std::map<std::array<std::uint16_t, 7>, std::uint64_t> signatures;
        for (const State& target : frontier) {
            const auto& incidence = first_objective_seven_incidence.at(target);
            ++signatures[incidence];
            for (int source = 2; source <= 6; ++source)
                directed_by_source[source] += orbit_size * incidence[source];
        }
        if (directed_by_source[6] != 294808)
            throw std::runtime_error(
                "objective-seven incidence from objective six mismatch"
            );

        std::ofstream output(path);
        if (!output) throw std::runtime_error("cannot write " + path);
        output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
        output << "  \"source_sublevel_six_component_vertex_count\": 68198,\n";
        output << "  \"objective_seven_first_frontier_rotation_orbit_count\": "
               << frontier.size() << ",\n";
        output << "  \"objective_seven_first_frontier_vertex_count\": "
               << orbit_size * frontier.size() << ",\n";
        output << "  \"directed_incidence_by_source_objective\": {";
        for (int source = 2; source <= 6; ++source) {
            if (source != 2) output << ',';
            output << "\n    \"" << source << "\": "
                   << directed_by_source[source];
        }
        output << "\n  },\n";
        output << "  \"total_directed_sublevel_six_incidence\": "
               << std::accumulate(
                      directed_by_source.begin(), directed_by_source.end(),
                      std::uint64_t{0}
                  )
               << ",\n";
        output << "  \"incidence_signature_count\": " << signatures.size()
               << ",\n";
        output << "  \"incidence_signature_histogram\": [\n";
        bool signature_separator = false;
        for (const auto& [signature, count] : signatures) {
            if (signature_separator) output << ",\n";
            output << "    {\"signature_2_through_6\":[";
            for (int source = 2; source <= 6; ++source) {
                if (source != 2) output << ',';
                output << signature[source];
            }
            output << "],\"orbit_count\":" << count << '}';
            signature_separator = true;
        }
        output << "\n  ],\n";

        for (int objective = 2; objective <= 6; ++objective) {
            std::vector<State> lower(
                orbit_states[objective].begin(), orbit_states[objective].end()
            );
            std::sort(lower.begin(), lower.end());
            output << "  \"objective_" << objective
                   << "_rotation_representatives\": [\n";
            for (std::size_t index = 0; index < lower.size(); ++index) {
                if (index) output << ",\n";
                output << "    ";
                write_state(output, lower[index]);
            }
            output << "\n  ],\n";
        }

        output << "  \"objective_seven_rotation_representatives\": [\n";
        for (std::size_t index = 0; index < frontier.size(); ++index) {
            if (index) output << ",\n";
            output << "    ";
            write_state(output, frontier[index]);
        }
        output << "\n  ],\n";
        output << "  \"objective_seven_incidence_signatures_2_through_6\": [\n";
        for (std::size_t index = 0; index < frontier.size(); ++index) {
            if (index) output << ",\n";
            const auto& incidence = first_objective_seven_incidence.at(frontier[index]);
            output << "    [";
            for (int source = 2; source <= 6; ++source) {
                if (source != 2) output << ',';
                output << incidence[source];
            }
            output << ']';
        }
        output << "\n  ],\n";
        output << "  \"method\": \"exact orbit-canonical enumeration of every one-flip objective-seven neighbor of the complete sublevel-six component\",\n";
        output << "  \"scope_note\": \"This is the complete first objective-seven frontier only; it does not assert closure of the objective-seven layer.\"\n";
        output << "}\n";
    }

    void move_to(const State& target) {
        State difference;
        for (int word = 0; word < word_count; ++word)
            difference.words[word] = state.words[word] ^ target.words[word];
        for (int word = 0; word < word_count; ++word) {
            std::uint64_t bits = difference.words[word];
            while (bits) {
                const int bit = std::countr_zero(bits);
                const int id = 64 * word + bit;
                if (id < edge_count) toggle(id);
                bits &= bits - 1;
            }
        }
        if (!(state == target)) throw std::logic_error("state move failed");
    }

    void write_objective_seven_component(const std::string& path) {
        std::array<std::unordered_set<State, StateHash>, 8> new_orbits;
        std::vector<std::pair<int, State>> queue;
        queue.reserve(first_objective_seven_incidence.size());
        for (const auto& [target, incidence] : first_objective_seven_incidence) {
            (void)incidence;
            if (orbit_states[7].insert(target).second) {
                new_orbits[7].insert(target);
                queue.push_back({7, target});
            }
        }
        const std::uint64_t first_frontier_orbits = queue.size();
        if (first_frontier_orbits != 4217)
            throw std::runtime_error("objective-seven first frontier mismatch");

        for (std::size_t position = 0; position < queue.size(); ++position) {
            const auto [objective, source] = queue[position];
            move_to(source);
            if (monochromatic_count != objective)
                throw std::runtime_error("closure queue objective mismatch");
            for (int id = 0; id < edge_count; ++id) {
                const int target_objective = resulting_count(id);
                if (target_objective > 7) continue;
                if (target_objective < 0)
                    throw std::runtime_error("negative objective");
                State neighbor = state;
                neighbor.toggle(id);
                const State key = canonical(neighbor);
                if (!orbit_states[target_objective].insert(key).second) continue;
                require_free_orbit(neighbor);
                new_orbits[target_objective].insert(key);
                queue.push_back({target_objective, key});
            }
        }

        std::array<std::map<int, std::uint64_t>, 8> histograms;
        std::uint64_t new_to_known_directed = 0;
        std::uint64_t new_internal_directed = 0;
        int escape_level = -1;
        for (const auto& [objective, source] : queue) {
            move_to(source);
            if (monochromatic_count != objective)
                throw std::runtime_error("closure recount objective mismatch");
            for (int id = 0; id < edge_count; ++id) {
                const int target_objective = resulting_count(id);
                histograms[objective][target_objective] += orbit_size;
                if (target_objective == 8)
                    record_objective_eight_neighbor(objective, id);
                if (target_objective == 9)
                    record_objective_nine_neighbor(objective, id);
                if (target_objective > 7) {
                    if (escape_level < 0 || target_objective < escape_level)
                        escape_level = target_objective;
                    continue;
                }
                State neighbor = state;
                neighbor.toggle(id);
                const State key = canonical(neighbor);
                if (!orbit_states[target_objective].contains(key))
                    throw std::runtime_error("accepted closure neighbor missing");
                if (new_orbits[target_objective].contains(key))
                    new_internal_directed += orbit_size;
                else
                    new_to_known_directed += orbit_size;
            }
        }
        if (new_internal_directed % 2 || escape_level < 0)
            throw std::runtime_error("invalid objective-seven closure aggregate");
        if (new_to_known_directed != 525202)
            throw std::runtime_error("objective-seven lower incidence mismatch");

        std::uint64_t new_orbit_count = 0;
        std::uint64_t new_lower_orbit_count = 0;
        for (int objective = 0; objective <= 7; ++objective) {
            new_orbit_count += new_orbits[objective].size();
            if (objective < 7) new_lower_orbit_count += new_orbits[objective].size();
        }
        const std::uint64_t new_vertex_count = orbit_size * new_orbit_count;
        const std::uint64_t new_internal_edges = new_internal_directed / 2;
        const std::uint64_t complete_vertices = 68198 + new_vertex_count;
        const std::uint64_t complete_edges =
            237489 + new_to_known_directed + new_internal_edges;

        std::vector<State> objective_seven_representatives(
            new_orbits[7].begin(), new_orbits[7].end()
        );
        std::sort(
            objective_seven_representatives.begin(),
            objective_seven_representatives.end()
        );

        std::ofstream output(path);
        if (!output) throw std::runtime_error("cannot write " + path);
        output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
        output << "  \"objective_seven_first_frontier_rotation_orbit_count\": "
               << first_frontier_orbits << ",\n";
        output << "  \"complete_threshold_seven_new_rotation_orbit_count\": "
               << new_orbit_count << ",\n";
        output << "  \"complete_objective_seven_rotation_orbit_count\": "
               << new_orbits[7].size() << ",\n";
        output << "  \"additional_objective_seven_rotation_orbit_count\": "
               << new_orbits[7].size() - first_frontier_orbits << ",\n";
        output << "  \"new_objective_at_most_six_rotation_orbit_count\": "
               << new_lower_orbit_count << ",\n";
        output << "  \"complete_objective_seven_vertex_count\": "
               << orbit_size * new_orbits[7].size() << ",\n";
        output << "  \"new_to_sublevel_six_directed_edge_count\": "
               << new_to_known_directed << ",\n";
        output << "  \"new_threshold_seven_internal_edge_count\": "
               << new_internal_edges << ",\n";
        output << "  \"complete_sublevel_seven_component_vertex_count\": "
               << complete_vertices << ",\n";
        output << "  \"complete_sublevel_seven_component_edge_count\": "
               << complete_edges << ",\n";
        output << "  \"complete_sublevel_seven_component_is_closed\": true,\n";
        output << "  \"exact_one_flip_escape_level_from_sublevel_seven_component\": "
               << escape_level << ",\n";
        output << "  \"new_rotation_representative_neighbor_checks\": "
               << new_orbit_count * edge_count << ",\n";
        output << "  \"new_symmetry_lifted_neighbor_checks\": "
               << new_vertex_count * edge_count << ",\n";
        output << "  \"new_state_neighbor_objective_histogram_by_source_objective\": {";
        bool source_separator = false;
        for (int objective = 0; objective <= 7; ++objective) {
            if (histograms[objective].empty()) continue;
            if (source_separator) output << ',';
            output << "\n    \"" << objective << "\": {";
            bool target_separator = false;
            for (const auto& [target, count] : histograms[objective]) {
                if (target_separator) output << ',';
                output << "\n      \"" << target << "\": " << count;
                target_separator = true;
            }
            output << "\n    }";
            source_separator = true;
        }
        output << "\n  },\n";
        output << "  \"objective_seven_component_rotation_representatives\": [\n";
        for (std::size_t index = 0;
             index < objective_seven_representatives.size(); ++index) {
            if (index) output << ",\n";
            output << "    ";
            write_state(output, objective_seven_representatives[index]);
        }
        output << "\n  ],\n";
        output << "  \"method\": \"iterative exact orbit closure under all one-edge moves with objective at most seven\",\n";
        output << "  \"scope_note\": \"Complete connected threshold-seven component through the certified Cyclic(43) optimum; disconnected components remain out of scope.\"\n";
        output << "}\n";
    }

    void write_objective_eight_frontier(const std::string& path) const {
        std::vector<State> frontier;
        frontier.reserve(first_objective_eight_incidence.size());
        for (const auto& [state, incidence] : first_objective_eight_incidence) {
            (void)incidence;
            frontier.push_back(state);
        }
        std::sort(frontier.begin(), frontier.end());

        std::array<std::uint64_t, 8> directed_by_source{};
        std::map<std::array<std::uint16_t, 8>, std::uint64_t> signatures;
        for (const State& target : frontier) {
            const auto& incidence = first_objective_eight_incidence.at(target);
            ++signatures[incidence];
            for (int source = 2; source <= 7; ++source)
                directed_by_source[source] += orbit_size * incidence[source];
        }
        if (directed_by_source[7] != 1020906)
            throw std::runtime_error(
                "objective-eight incidence from objective seven mismatch"
            );

        std::ofstream output(path);
        if (!output) throw std::runtime_error("cannot write " + path);
        output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
        output << "  \"source_sublevel_seven_component_vertex_count\": 249529,\n";
        output << "  \"objective_eight_first_frontier_rotation_orbit_count\": "
               << frontier.size() << ",\n";
        output << "  \"objective_eight_first_frontier_vertex_count\": "
               << orbit_size * frontier.size() << ",\n";
        output << "  \"directed_incidence_by_source_objective\": {";
        for (int source = 2; source <= 7; ++source) {
            if (source != 2) output << ',';
            output << "\n    \"" << source << "\": "
                   << directed_by_source[source];
        }
        output << "\n  },\n";
        output << "  \"total_directed_sublevel_seven_incidence\": "
               << std::accumulate(
                      directed_by_source.begin(), directed_by_source.end(),
                      std::uint64_t{0}
                  )
               << ",\n";
        output << "  \"incidence_signature_count\": " << signatures.size()
               << ",\n";
        output << "  \"incidence_signature_histogram\": [\n";
        bool signature_separator = false;
        for (const auto& [signature, count] : signatures) {
            if (signature_separator) output << ",\n";
            output << "    {\"signature_2_through_7\":[";
            for (int source = 2; source <= 7; ++source) {
                if (source != 2) output << ',';
                output << signature[source];
            }
            output << "],\"orbit_count\":" << count << '}';
            signature_separator = true;
        }
        output << "\n  ],\n";
        output << "  \"objective_eight_rotation_representatives\": [\n";
        for (std::size_t index = 0; index < frontier.size(); ++index) {
            if (index) output << ",\n";
            output << "    ";
            write_state(output, frontier[index]);
        }
        output << "\n  ],\n";
        output << "  \"objective_eight_incidence_signatures_2_through_7\": [\n";
        for (std::size_t index = 0; index < frontier.size(); ++index) {
            if (index) output << ",\n";
            const auto& incidence = first_objective_eight_incidence.at(frontier[index]);
            output << "    [";
            for (int source = 2; source <= 7; ++source) {
                if (source != 2) output << ',';
                output << incidence[source];
            }
            output << ']';
        }
        output << "\n  ],\n";
        output << "  \"method\": \"exact orbit-canonical enumeration of every one-flip objective-eight neighbor of the complete sublevel-seven component\",\n";
        output << "  \"scope_note\": \"This is the complete first objective-eight frontier only; it does not assert closure of the objective-eight layer.\"\n";
        output << "}\n";
    }

    void write_objective_eight_component(const std::string& path) {
        std::array<std::unordered_set<State, StateHash>, 9> new_orbits;
        std::vector<std::pair<int, State>> queue;
        queue.reserve(first_objective_eight_incidence.size());
        for (const auto& [target, incidence] : first_objective_eight_incidence) {
            (void)incidence;
            if (orbit_states[8].insert(target).second) {
                new_orbits[8].insert(target);
                queue.push_back({8, target});
            }
        }
        const std::uint64_t first_frontier_orbits = queue.size();
        if (first_frontier_orbits != 13702)
            throw std::runtime_error("objective-eight first frontier mismatch");

        for (std::size_t position = 0; position < queue.size(); ++position) {
            const auto [objective, source] = queue[position];
            move_to(source);
            if (monochromatic_count != objective)
                throw std::runtime_error("threshold-eight queue objective mismatch");
            for (int id = 0; id < edge_count; ++id) {
                const int target_objective = resulting_count(id);
                if (target_objective > 8) continue;
                if (target_objective < 0)
                    throw std::runtime_error("negative objective");
                State neighbor = state;
                neighbor.toggle(id);
                const State key = canonical(neighbor);
                if (!orbit_states[target_objective].insert(key).second) continue;
                require_free_orbit(neighbor);
                new_orbits[target_objective].insert(key);
                queue.push_back({target_objective, key});
            }
        }

        std::array<std::map<int, std::uint64_t>, 9> histograms;
        std::uint64_t new_to_known_directed = 0;
        std::uint64_t new_internal_directed = 0;
        int escape_level = -1;
        for (const auto& [objective, source] : queue) {
            move_to(source);
            if (monochromatic_count != objective)
                throw std::runtime_error("threshold-eight recount objective mismatch");
            for (int id = 0; id < edge_count; ++id) {
                const int target_objective = resulting_count(id);
                histograms[objective][target_objective] += orbit_size;
                if (target_objective == 9)
                    record_objective_nine_neighbor(objective, id);
                if (target_objective > 8) {
                    if (escape_level < 0 || target_objective < escape_level)
                        escape_level = target_objective;
                    continue;
                }
                State neighbor = state;
                neighbor.toggle(id);
                const State key = canonical(neighbor);
                if (!orbit_states[target_objective].contains(key))
                    throw std::runtime_error("accepted threshold-eight neighbor missing");
                if (new_orbits[target_objective].contains(key))
                    new_internal_directed += orbit_size;
                else
                    new_to_known_directed += orbit_size;
            }
        }
        if (new_internal_directed % 2 || escape_level < 0)
            throw std::runtime_error("invalid objective-eight closure aggregate");

        std::uint64_t new_orbit_count = 0;
        std::uint64_t new_lower_orbit_count = 0;
        for (int objective = 0; objective <= 8; ++objective) {
            new_orbit_count += new_orbits[objective].size();
            if (objective < 8) new_lower_orbit_count += new_orbits[objective].size();
        }
        if (new_lower_orbit_count == 0 && new_to_known_directed != 1929754)
            throw std::runtime_error("objective-eight lower incidence mismatch");

        const std::uint64_t new_vertex_count = orbit_size * new_orbit_count;
        const std::uint64_t new_internal_edges = new_internal_directed / 2;
        const std::uint64_t complete_vertices = 249529 + new_vertex_count;
        const std::uint64_t complete_edges =
            982679 + new_to_known_directed + new_internal_edges;

        std::vector<State> objective_eight_representatives(
            new_orbits[8].begin(), new_orbits[8].end()
        );
        std::sort(
            objective_eight_representatives.begin(),
            objective_eight_representatives.end()
        );

        std::ofstream output(path);
        if (!output) throw std::runtime_error("cannot write " + path);
        output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
        output << "  \"objective_eight_first_frontier_rotation_orbit_count\": "
               << first_frontier_orbits << ",\n";
        output << "  \"complete_threshold_eight_new_rotation_orbit_count\": "
               << new_orbit_count << ",\n";
        output << "  \"complete_objective_eight_rotation_orbit_count\": "
               << new_orbits[8].size() << ",\n";
        output << "  \"additional_objective_eight_rotation_orbit_count\": "
               << new_orbits[8].size() - first_frontier_orbits << ",\n";
        output << "  \"new_objective_at_most_seven_rotation_orbit_count\": "
               << new_lower_orbit_count << ",\n";
        output << "  \"complete_objective_eight_vertex_count\": "
               << orbit_size * new_orbits[8].size() << ",\n";
        output << "  \"new_to_sublevel_seven_directed_edge_count\": "
               << new_to_known_directed << ",\n";
        output << "  \"new_threshold_eight_internal_edge_count\": "
               << new_internal_edges << ",\n";
        output << "  \"complete_sublevel_eight_component_vertex_count\": "
               << complete_vertices << ",\n";
        output << "  \"complete_sublevel_eight_component_edge_count\": "
               << complete_edges << ",\n";
        output << "  \"complete_sublevel_eight_component_is_closed\": true,\n";
        output << "  \"exact_one_flip_escape_level_from_sublevel_eight_component\": "
               << escape_level << ",\n";
        output << "  \"new_rotation_representative_neighbor_checks\": "
               << new_orbit_count * edge_count << ",\n";
        output << "  \"new_symmetry_lifted_neighbor_checks\": "
               << new_vertex_count * edge_count << ",\n";
        output << "  \"new_state_neighbor_objective_histogram_by_source_objective\": {";
        bool source_separator = false;
        for (int objective = 0; objective <= 8; ++objective) {
            if (histograms[objective].empty()) continue;
            if (source_separator) output << ',';
            output << "\n    \"" << objective << "\": {";
            bool target_separator = false;
            for (const auto& [target, count] : histograms[objective]) {
                if (target_separator) output << ',';
                output << "\n      \"" << target << "\": " << count;
                target_separator = true;
            }
            output << "\n    }";
            source_separator = true;
        }
        output << "\n  },\n";
        output << "  \"objective_eight_component_rotation_representatives\": [\n";
        for (std::size_t index = 0;
             index < objective_eight_representatives.size(); ++index) {
            if (index) output << ",\n";
            output << "    ";
            write_state(output, objective_eight_representatives[index]);
        }
        output << "\n  ],\n";
        output << "  \"method\": \"iterative exact orbit closure under all one-edge moves with objective at most eight\",\n";
        output << "  \"scope_note\": \"Complete connected threshold-eight component through the certified Cyclic(43) optimum; disconnected components remain out of scope.\"\n";
        output << "}\n";
    }

    void write_objective_nine_frontier(const std::string& path) const {
        std::vector<State> frontier;
        frontier.reserve(first_objective_nine_incidence.size());
        for (const auto& [state, incidence] : first_objective_nine_incidence) {
            (void)incidence;
            frontier.push_back(state);
        }
        std::sort(frontier.begin(), frontier.end());

        std::array<std::uint64_t, 9> directed_by_source{};
        std::map<std::array<std::uint16_t, 9>, std::uint64_t> signatures;
        for (const State& target : frontier) {
            const auto& incidence = first_objective_nine_incidence.at(target);
            ++signatures[incidence];
            for (int source = 2; source <= 8; ++source)
                directed_by_source[source] += orbit_size * incidence[source];
        }

        std::ofstream output(path);
        if (!output) throw std::runtime_error("cannot write " + path);
        output << "{\n  \"order\": 43,\n  \"edge_count\": 903,\n";
        output << "  \"objective_nine_first_frontier_rotation_orbit_count\": "
               << frontier.size() << ",\n";
        output << "  \"objective_nine_first_frontier_vertex_count\": "
               << orbit_size * frontier.size() << ",\n";
        output << "  \"directed_incidence_by_source_objective\": {";
        for (int source = 2; source <= 8; ++source) {
            if (source != 2) output << ',';
            output << "\n    \"" << source << "\": "
                   << directed_by_source[source];
        }
        output << "\n  },\n";
        output << "  \"total_directed_sublevel_eight_incidence\": "
               << std::accumulate(
                      directed_by_source.begin(), directed_by_source.end(),
                      std::uint64_t{0}
                  )
               << ",\n";
        output << "  \"incidence_signature_count\": " << signatures.size()
               << ",\n";
        output << "  \"incidence_signature_histogram\": [\n";
        bool signature_separator = false;
        for (const auto& [signature, count] : signatures) {
            if (signature_separator) output << ",\n";
            output << "    {\"signature_2_through_8\":[";
            for (int source = 2; source <= 8; ++source) {
                if (source != 2) output << ',';
                output << signature[source];
            }
            output << "],\"orbit_count\":" << count << '}';
            signature_separator = true;
        }
        output << "\n  ],\n";
        output << "  \"objective_nine_rotation_representatives\": [\n";
        for (std::size_t index = 0; index < frontier.size(); ++index) {
            if (index) output << ",\n";
            output << "    ";
            write_state(output, frontier[index]);
        }
        output << "\n  ],\n";
        output << "  \"objective_nine_incidence_signatures_2_through_8\": [\n";
        for (std::size_t index = 0; index < frontier.size(); ++index) {
            if (index) output << ",\n";
            const auto& incidence = first_objective_nine_incidence.at(frontier[index]);
            output << "    [";
            for (int source = 2; source <= 8; ++source) {
                if (source != 2) output << ',';
                output << incidence[source];
            }
            output << ']';
        }
        output << "\n  ],\n";
        output << "  \"method\": \"exact orbit-canonical enumeration of every one-flip objective-nine neighbor of the complete sublevel-eight component\",\n";
        output << "  \"scope_note\": \"This is the complete first objective-nine frontier only; it does not assert closure of the objective-nine layer.\"\n";
        output << "}\n";
    }

    void write_json(std::ostream& output, double elapsed_seconds) const {
        const std::uint64_t component_orbits = orbit_states[6].size();
        const std::uint64_t component_vertices = component_orbits * orbit_size;
        const std::uint64_t induced_edges = same_layer_directed[6] / 2;
        const std::uint64_t component_vertices_with_lower = 17329 + component_vertices;
        const std::uint64_t component_edges = 52890 + 129473 + induced_edges;
        int escape_level = -1;
        for (const auto& [objective, count] : aggregate_histogram[6]) {
            if (objective > 6 && count) {
                escape_level = objective;
                break;
            }
        }
        if (same_layer_directed[6] % 2 || escape_level < 0)
            throw std::runtime_error("invalid objective-six closure aggregates");

        output << "{\n";
        output << "  \"order\": 43,\n";
        output << "  \"edge_count\": 903,\n";
        output << "  \"objective_six_first_frontier_rotation_orbit_count\": "
               << first_objective_six_frontier.size() << ",\n";
        output << "  \"objective_six_component_rotation_orbit_count\": "
               << component_orbits << ",\n";
        output << "  \"additional_objective_six_rotation_orbit_count\": "
               << component_orbits - first_objective_six_frontier.size() << ",\n";
        output << "  \"objective_six_component_vertex_count\": "
               << component_vertices << ",\n";
        output << "  \"objective_six_component_induced_edge_count\": "
               << induced_edges << ",\n";
        output << "  \"objective_six_directed_sublevel_five_edge_count\": "
               << directed_sum(6) << ",\n";
        output << "  \"objective_six_component_rotation_representative_neighbor_checks\": "
               << component_orbits * edge_count << ",\n";
        output << "  \"objective_six_component_symmetry_lifted_neighbor_checks\": "
               << component_vertices * edge_count << ",\n";
        output << "  \"complete_sublevel_six_component_is_closed\": true,\n";
        output << "  \"complete_sublevel_six_component_vertex_count\": "
               << component_vertices_with_lower << ",\n";
        output << "  \"complete_sublevel_six_component_edge_count\": "
               << component_edges << ",\n";
        output << "  \"exact_one_flip_escape_level_from_sublevel_six_component\": "
               << escape_level << ",\n";
        output << "  \"aggregate_objective_six_component_neighbor_objective_histogram\": {";
        bool separator = false;
        for (const auto& [objective, count] : aggregate_histogram[6]) {
            if (separator) output << ',';
            output << "\n    \"" << objective << "\": " << count;
            separator = true;
        }
        if (separator) output << '\n';
        output << "  },\n";
        output << "  \"new_objective_at_most_five_rotation_orbit_count\": 0,\n";
        output << "  \"elapsed_seconds\": " << elapsed_seconds << ",\n";
        output << "  \"method\": \"bit-packed orbit DFS with incrementally maintained exact single-flip deltas\",\n";
        output << "  \"scope_note\": \"Complete connected sublevel-six component through the certified Cyclic(43) optimum; disconnected components remain out of scope.\"\n";
        output << "}\n";
    }
};

}  // namespace

int main(int argc, char** argv) try {
    if (argc < 3 || argc > 15 || argc % 2 == 0) {
        std::cerr
            << "usage: objective_six_component CERTIFICATE.json defect-cycle.json "
               "[--representatives OUTPUT.json] "
               "[--objective-seven-frontier OUTPUT.json] "
               "[--objective-seven-component OUTPUT.json] "
               "[--objective-eight-frontier OUTPUT.json] "
               "[--objective-eight-component OUTPUT.json] "
               "[--objective-nine-frontier OUTPUT.json]\n";
        return 2;
    }
    std::string representative_path;
    std::string objective_seven_frontier_path;
    std::string objective_seven_component_path;
    std::string objective_eight_frontier_path;
    std::string objective_eight_component_path;
    std::string objective_nine_frontier_path;
    for (int argument = 3; argument < argc; argument += 2) {
        const std::string option = argv[argument];
        if (option == "--representatives")
            representative_path = argv[argument + 1];
        else if (option == "--objective-seven-frontier")
            objective_seven_frontier_path = argv[argument + 1];
        else if (option == "--objective-seven-component")
            objective_seven_component_path = argv[argument + 1];
        else if (option == "--objective-eight-frontier")
            objective_eight_frontier_path = argv[argument + 1];
        else if (option == "--objective-eight-component")
            objective_eight_component_path = argv[argument + 1];
        else if (option == "--objective-nine-frontier")
            objective_nine_frontier_path = argv[argument + 1];
        else
            throw std::runtime_error("unknown output option " + option);
    }
    const auto start = std::chrono::steady_clock::now();
    Search search(load_flips(argv[1]));
    search.run(load_integer_array(argv[2], "edge_positions"));
    const double elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - start
    ).count();
    if (!representative_path.empty())
        search.write_representatives(representative_path);
    if (!objective_seven_frontier_path.empty())
        search.write_objective_seven_frontier(objective_seven_frontier_path);
    if (!objective_seven_component_path.empty())
        search.write_objective_seven_component(objective_seven_component_path);
    if (!objective_eight_frontier_path.empty()) {
        if (objective_seven_component_path.empty())
            throw std::runtime_error(
                "objective-eight frontier requires objective-seven closure"
            );
        search.write_objective_eight_frontier(objective_eight_frontier_path);
    }
    if (!objective_eight_component_path.empty()) {
        if (objective_seven_component_path.empty())
            throw std::runtime_error(
                "objective-eight component requires objective-seven closure"
            );
        search.write_objective_eight_component(objective_eight_component_path);
    }
    if (!objective_nine_frontier_path.empty()) {
        if (objective_eight_component_path.empty())
            throw std::runtime_error(
                "objective-nine frontier requires objective-eight closure"
            );
        search.write_objective_nine_frontier(objective_nine_frontier_path);
    }
    search.write_json(std::cout, elapsed);
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
