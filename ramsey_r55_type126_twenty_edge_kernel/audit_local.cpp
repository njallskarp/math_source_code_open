// Independent complete local audit: literal red-four / blue-five subsets,
// then all 2^20 assignments. No CNF parser, producer, or conflict-graph input.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

int main(int argc, char** argv) { try {
    if (argc != 3) throw std::runtime_error("usage: audit_local MATRIX MODEL_OUTPUT");
    std::ifstream in(argv[1]);
    std::array<std::array<int,22>,22> color{}, variable{};
    int nv = 0;
    for (int u=0; u<22; ++u) for (int v=u+1; v<22; ++v) {
        char c;
        if (!(in >> c) || c<'0' || c>'2') throw std::runtime_error("matrix character/count");
        color[u][v] = c-'0';
        if (c=='2') variable[u][v] = nv++;
    }
    char extra;
    if (in >> extra) throw std::runtime_error("extra matrix data");
    if (nv != 20) throw std::runtime_error("exactly twenty free pairs required");
    std::vector<std::uint32_t> red, blue;
    auto record = [&](const std::vector<int>& q, int target) {
        std::uint32_t mask=0;
        for (std::size_t i=0; i<q.size(); ++i) for (std::size_t j=i+1; j<q.size(); ++j) {
            int u=q[i], v=q[j];
            if (color[u][v] != 2 && color[u][v] != target) return;
            if (color[u][v] == 2) mask |= std::uint32_t(1) << variable[u][v];
        }
        (target ? red : blue).push_back(mask);
    };
    for (int a=0;a<19;++a) for (int b=a+1;b<20;++b)
    for (int c=b+1;c<21;++c) for (int d=c+1;d<22;++d) record({a,b,c,d},1);
    for (int a=0;a<18;++a) for (int b=a+1;b<19;++b)
    for (int c=b+1;c<20;++c) for (int d=c+1;d<21;++d)
    for (int e=d+1;e<22;++e) record({a,b,c,d,e},0);
    for (auto* rows : {&red,&blue}) {
        std::sort(rows->begin(),rows->end());
        rows->erase(std::unique(rows->begin(),rows->end()),rows->end());
    }
    std::ofstream out(argv[2]);
    if (!out) throw std::runtime_error("model output open");
    std::uint64_t count=0;
    std::array<std::uint64_t,232> histogram{};
    bool unique=true;
    for (std::uint32_t mask=0; mask<(std::uint32_t(1)<<20); ++mask) {
        bool bad=false;
        for (auto r:red) if ((mask&r)==r) {bad=true;break;}
        if (bad) continue;
        for (auto b:blue) if ((mask&b)==0) {bad=true;break;}
        if (bad) continue;
        out << mask << '\n'; ++count;
        std::array<int,22> degrees{};
        int edges=0, hubs=0;
        for(int u=0;u<22;++u) for(int v=u+1;v<22;++v) {
            bool is_red=color[u][v]==2 ? ((mask>>variable[u][v])&1) : color[u][v]==1;
            if(is_red) {++degrees[u];++degrees[v];++edges;}
        }
        for(int v=0;v<22;++v) if(degrees[v]==5) {++hubs;if(v!=21)unique=false;}
        if(hubs!=1) unique=false;
        ++histogram[edges];
    }
    if (!out) throw std::runtime_error("model output write");
    std::cout << "{\"complete_assignments\":1048576,\"valid_local_fillings\":" << count
              << ",\"all_unique_hub\":" << (unique?"true":"false") << ",\"density_histogram\":{";
    bool first=true;
    for(int e=0;e<232;++e) if(histogram[e]) {
        if(!first) std::cout<<',';
        first=false;
        std::cout << '\"' << e << "\":" << histogram[e];
    }
    std::cout << "}}\n";
    return 0;
} catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;} }
