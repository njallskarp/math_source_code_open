#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {

constexpr int order = 28;
constexpr std::int64_t prime = 1'000'000'007LL;
constexpr std::int64_t hadamard_bound = 4'782'969LL;  // 3^14

using Row = std::array<std::int64_t, order>;

std::int64_t power(std::int64_t base, std::int64_t exponent) {
    std::int64_t result = 1;
    while (exponent > 0) {
        if ((exponent & 1LL) != 0) result = result * base % prime;
        base = base * base % prime;
        exponent >>= 1;
    }
    return result;
}

int rank_mod(std::vector<Row> matrix) {
    int rank = 0;
    for (int column = 0; column < order && rank < static_cast<int>(matrix.size()); ++column) {
        int pivot = rank;
        while (pivot < static_cast<int>(matrix.size()) && matrix.at(static_cast<std::size_t>(pivot)).at(static_cast<std::size_t>(column)) == 0) {
            ++pivot;
        }
        if (pivot == static_cast<int>(matrix.size())) continue;
        std::swap(matrix.at(static_cast<std::size_t>(rank)), matrix.at(static_cast<std::size_t>(pivot)));
        const std::int64_t inverse = power(
            matrix.at(static_cast<std::size_t>(rank)).at(static_cast<std::size_t>(column)),
            prime - 2
        );
        for (int j = column; j < order; ++j) {
            auto& entry = matrix.at(static_cast<std::size_t>(rank)).at(static_cast<std::size_t>(j));
            entry = entry * inverse % prime;
        }
        for (int i = 0; i < static_cast<int>(matrix.size()); ++i) {
            if (i == rank) continue;
            const std::int64_t factor = matrix.at(static_cast<std::size_t>(i)).at(static_cast<std::size_t>(column));
            if (factor == 0) continue;
            for (int j = column; j < order; ++j) {
                auto& entry = matrix.at(static_cast<std::size_t>(i)).at(static_cast<std::size_t>(j));
                entry = (entry - factor * matrix.at(static_cast<std::size_t>(rank)).at(static_cast<std::size_t>(j))) % prime;
                if (entry < 0) entry += prime;
            }
        }
        ++rank;
    }
    return rank;
}

std::int64_t determinant_mod(std::vector<Row> matrix) {
    std::int64_t determinant = 1;
    int sign = 1;
    for (int column = 0; column < order; ++column) {
        int pivot = column;
        while (pivot < order && matrix.at(static_cast<std::size_t>(pivot)).at(static_cast<std::size_t>(column)) == 0) ++pivot;
        if (pivot == order) return 0;
        if (pivot != column) {
            std::swap(matrix.at(static_cast<std::size_t>(pivot)), matrix.at(static_cast<std::size_t>(column)));
            sign = -sign;
        }
        const std::int64_t value = matrix.at(static_cast<std::size_t>(column)).at(static_cast<std::size_t>(column));
        determinant = determinant * value % prime;
        const std::int64_t inverse = power(value, prime - 2);
        for (int row = column + 1; row < order; ++row) {
            const std::int64_t factor = matrix.at(static_cast<std::size_t>(row)).at(static_cast<std::size_t>(column)) * inverse % prime;
            for (int j = column; j < order; ++j) {
                auto& entry = matrix.at(static_cast<std::size_t>(row)).at(static_cast<std::size_t>(j));
                entry = (entry - factor * matrix.at(static_cast<std::size_t>(column)).at(static_cast<std::size_t>(j))) % prime;
                if (entry < 0) entry += prime;
            }
        }
    }
    if (sign < 0 && determinant != 0) determinant = prime - determinant;
    return determinant;
}

int blue_from_red(int mark, int pivot, int red_triangles) {
    if ((mark != 0 && mark != 1) || (pivot != 0 && pivot != 1) || pivot > mark) {
        throw std::runtime_error("mark/pivot");
    }
    const int red_degree = 21 - mark;
    const int e_incidence = 6 + 2 * pivot;
    const int red_neighbor_degree_sum = 21 * red_degree - e_incidence;
    const int red_cut = red_neighbor_degree_sum - red_degree - 2 * red_triangles;
    const int blue_neighbor_degree_sum = 890 - red_degree - red_neighbor_degree_sum;
    const int red_inside_blue = (blue_neighbor_degree_sum - red_cut) / 2;
    const int blue_degree = 42 - red_degree;
    return blue_degree * (blue_degree - 1) / 2 - red_inside_blue;
}

}  // namespace

int main() {
    std::vector<Row> cyclic(static_cast<std::size_t>(order));
    for (int vertex = 0; vertex < order; ++vertex) {
        for (int column = 0; column < order; ++column) {
            const bool present = vertex == column || vertex == (column + 1) % order ||
                                 vertex == (column + 2) % order;
            cyclic.at(static_cast<std::size_t>(vertex)).at(static_cast<std::size_t>(column)) = static_cast<int>(present);
        }
    }
    for (int column = 0; column < order; ++column) {
        int weight = 0;
        for (int row = 0; row < order; ++row) {
            weight += static_cast<int>(cyclic.at(static_cast<std::size_t>(row)).at(static_cast<std::size_t>(column)));
        }
        if (weight != 3) throw std::runtime_error("column weight");
    }
    const std::int64_t residue = determinant_mod(cyclic);
    if (residue != 3 || hadamard_bound >= prime / 2) throw std::runtime_error("determinant certificate");

    std::vector<Row> differences;
    for (int i = 0; i < order; ++i) {
        for (int j = i + 1; j < order; ++j) {
            for (int k = j + 1; k < order; ++k) {
                if (i == 0 && j == 1 && k == 2) continue;
                Row row{};
                row.at(0) -= 1;
                row.at(1) -= 1;
                row.at(2) -= 1;
                row.at(static_cast<std::size_t>(i)) += 1;
                row.at(static_cast<std::size_t>(j)) += 1;
                row.at(static_cast<std::size_t>(k)) += 1;
                for (auto& entry : row) if (entry < 0) entry += prime;
                differences.push_back(row);
            }
        }
    }
    const int difference_rank = rank_mod(differences);
    if (difference_rank != 27) throw std::runtime_error("constant-sum kernel");

    if (blue_from_red(0, 0, 100) != 100 ||
        blue_from_red(1, 0, 93) != 107 ||
        blue_from_red(1, 1, 93) != 105) {
        throw std::runtime_error("blue equivalence");
    }

    std::cout << "PASS cyclic_minor order=28 determinant=3 hadamard_bound=4782969\n";
    std::cout << "PASS constant_triple_sum_kernel rank=27 dimension=1\n";
    std::cout << "PASS blue_equivalence unmarked=100 ordinary_marked=107 pivot=105\n";
    std::cout << "STATUS VERIFIED OUTSIDE-STAR RANK BARRIER\n";
}
