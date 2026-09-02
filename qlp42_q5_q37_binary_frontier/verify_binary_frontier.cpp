#include <array>
#include <bit>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <utility>

namespace {
constexpr unsigned N = 21;
constexpr std::uint32_t Full = (std::uint32_t{1} << N) - 1;

std::uint32_t rotate(std::uint32_t word, unsigned shift, unsigned length = N) {
    const std::uint32_t full = (std::uint32_t{1} << length) - 1;
    shift %= length;
    return ((word << shift) | (word >> (length - shift))) & full;
}

std::uint32_t canonical(std::uint32_t word, unsigned length = N) {
    std::uint32_t result = word;
    for (unsigned shift = 1; shift < length; ++shift) {
        result = std::min(result, rotate(word, shift, length));
    }
    return result;
}

std::uint16_t signature(std::uint32_t word) {
    std::uint16_t result = 0;
    for (unsigned shift = 1; shift <= 10; ++shift) {
        const auto overlap =
            static_cast<unsigned>(std::popcount(word & rotate(word, shift)));
        result |= static_cast<std::uint16_t>((overlap & 1U) << (shift - 1));
    }
    return result;
}

std::uint32_t compress7(std::uint32_t word) {
    std::uint32_t result = 0;
    for (unsigned residue = 0; residue < 7; ++residue) {
        const unsigned parity = ((word >> residue) ^ (word >> (residue + 7)) ^
                                 (word >> (residue + 14))) & 1U;
        result |= parity << residue;
    }
    return result;
}

std::uint64_t pack_pair(std::uint32_t left, std::uint32_t right) {
    return left | (std::uint64_t{right} << N);
}
}  // namespace

int main() {
    std::array<std::uint64_t, 6> raw_by_split{};
    std::array<std::uint64_t, 6> compatible_by_split{};
    std::array<std::set<std::uint64_t>, 6> orbits_by_split;
    std::array<std::uint64_t, 128 * 128> quotient_labeled{};
    std::array<std::set<std::uint64_t>, 128 * 128> quotient_orbits;
    std::set<std::uint64_t> all_orbits;

    std::uint64_t raw = 0;
    std::uint64_t compatible = 0;
    std::uint64_t support = (std::uint64_t{1} << 5) - 1;
    const std::uint64_t limit = std::uint64_t{1} << 42;
    while (support < limit) {
        const auto left = static_cast<std::uint32_t>(support & Full);
        const auto right = static_cast<std::uint32_t>((support >> N) & Full);
        const unsigned left_weight = static_cast<unsigned>(std::popcount(left));
        ++raw;
        ++raw_by_split[left_weight];
        if (signature(left) == signature(right)) {
            ++compatible;
            ++compatible_by_split[left_weight];
            const auto orbit = pack_pair(canonical(left), canonical(right));
            all_orbits.insert(orbit);
            orbits_by_split[left_weight].insert(orbit);
            const auto qleft = canonical(compress7(left), 7);
            const auto qright = canonical(compress7(right), 7);
            const unsigned quotient = (qleft << 7) | qright;
            ++quotient_labeled[quotient];
            quotient_orbits[quotient].insert(orbit);
        }

        const std::uint64_t low = support & (~support + 1);
        const std::uint64_t ripple = support + low;
        support = (((ripple ^ support) >> 2) / low) | ripple;
    }

    if (raw != 850668 || compatible != 10248 || all_orbits.size() != 36) {
        std::cerr << "unexpected frontier totals\n";
        return 1;
    }
    unsigned nonempty_quotients = 0;
    std::uint64_t quotient_labeled_total = 0;
    std::uint64_t quotient_orbit_total = 0;
    for (unsigned quotient = 0; quotient < quotient_labeled.size(); ++quotient) {
        if (!quotient_labeled[quotient]) {
            continue;
        }
        ++nonempty_quotients;
        quotient_labeled_total += quotient_labeled[quotient];
        quotient_orbit_total += quotient_orbits[quotient].size();
    }
    if (nonempty_quotients != 12 || quotient_labeled_total != compatible ||
        quotient_orbit_total != all_orbits.size()) {
        std::cerr << "unexpected quotient totals\n";
        return 1;
    }

    std::ifstream manifest_file(std::filesystem::current_path() / "frontier_orbits.tsv");
    std::string line;
    if (!std::getline(manifest_file, line) ||
        line != "q_a\tq_b\ta_mask_hex\tb_mask_hex\tv_a_hex\tv_b_hex") {
        std::cerr << "invalid manifest header\n";
        return 1;
    }
    std::set<std::uint64_t> manifest_orbits;
    unsigned manifest_rows = 0;
    while (std::getline(manifest_file, line)) {
        std::istringstream row(line);
        std::array<std::string, 6> field;
        for (unsigned index = 0; index < field.size(); ++index) {
            if (!std::getline(row, field[index], '\t')) {
                std::cerr << "invalid manifest row\n";
                return 1;
            }
        }
        const auto qleft = static_cast<unsigned>(std::stoul(field[0]));
        const auto qright = static_cast<unsigned>(std::stoul(field[1]));
        const auto left = static_cast<std::uint32_t>(std::stoul(field[2], nullptr, 16));
        const auto right = static_cast<std::uint32_t>(std::stoul(field[3], nullptr, 16));
        const auto vleft = static_cast<std::uint32_t>(std::stoul(field[4], nullptr, 16));
        const auto vright = static_cast<std::uint32_t>(std::stoul(field[5], nullptr, 16));
        if (std::popcount(left) != static_cast<int>(qleft) ||
            std::popcount(right) != static_cast<int>(qright) ||
            canonical(left) != left || canonical(right) != right ||
            canonical(compress7(left), 7) != vleft ||
            canonical(compress7(right), 7) != vright ||
            !manifest_orbits.insert(pack_pair(left, right)).second) {
            std::cerr << "invalid manifest content\n";
            return 1;
        }
        ++manifest_rows;
    }
    if (manifest_rows != 36 || manifest_orbits != all_orbits) {
        std::cerr << "manifest does not equal computed frontier\n";
        return 1;
    }

    for (std::uint32_t word = 0;; ++word) {
        if (signature(Full ^ word) != (signature(word) ^ 0x3ffU)) {
            std::cerr << "complement identity failure\n";
            return 1;
        }
        if (word == Full) {
            break;
        }
    }

    std::cout << "raw_q5_support_pairs=" << raw << '\n';
    std::cout << "compatible_q5_labeled_pairs=" << compatible << '\n';
    std::cout << "compatible_q5_independent_rotation_orbits=" << all_orbits.size()
              << '\n';
    std::cout << "q5_q37_complement_bijection=verified\n";
    std::cout << "mod7_quotient_orbits=" << nonempty_quotients << '\n';
    std::cout << "canonical_orbit_manifest_rows=" << manifest_rows << '\n';
    for (unsigned left_weight = 0; left_weight <= 5; ++left_weight) {
        std::cout << "split=" << left_weight << ',' << (5 - left_weight)
                  << ";raw=" << raw_by_split[left_weight]
                  << ";compatible=" << compatible_by_split[left_weight]
                  << ";orbits=" << orbits_by_split[left_weight].size() << '\n';
    }
    std::cout << "certificate=verified\n";
}
