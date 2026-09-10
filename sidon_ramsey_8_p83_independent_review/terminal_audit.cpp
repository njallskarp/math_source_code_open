// Independent pair-sum enumeration, with no weights, distance bounds,
// reflection normalization, or producer enumeration/query code.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using Mask = uint32_t;
struct Domain {
    std::vector<int> points, chosen;
    std::array<bool, 165> sums{};
    std::vector<Mask> answers;
    void visit(size_t start, int need, Mask selected) {
        if (!need) { answers.push_back(selected); return; }
        for (size_t i=start; i+size_t(need)<=points.size(); ++i) {
            int x=points[i];
            bool good=!sums[size_t(2*x)];
            for (int y:chosen) if(sums[size_t(x+y)]) good=false;
            if(!good) continue;
            // x is greater than all previously chosen values. New sums are
            // mutually distinct, and 2*x is larger than every x+y.
            sums[size_t(2*x)]=true;
            for(int y:chosen) sums[size_t(x+y)]=true;
            chosen.push_back(x);
            visit(i+1,need-1,selected|(Mask(1)<<i));
            chosen.pop_back();
            sums[size_t(2*x)]=false;
            for(int y:chosen) sums[size_t(x+y)]=false;
        }
    }
    std::vector<Mask> enumerate(int k) {
        answers.clear(); chosen.clear(); sums.fill(false);
        visit(0,k,0); std::sort(answers.begin(),answers.end());
        return answers;
    }
    bool sidon(Mask m) const {
        std::array<bool,165> seen{};
        for(size_t i=0;i<points.size();++i) if(m&(Mask(1)<<i))
            for(size_t j=i;j<points.size();++j) if(m&(Mask(1)<<j)) {
                size_t s=size_t(points[i]+points[j]);
                if(seen[s]) return false;
                seen[s]=true;
            }
        return true;
    }
};
int main(int argc,char**argv) {
    try {
        if(argc!=3) throw std::runtime_error("usage: terminal_audit size input.txt (size=0 for 28-profile decisions)");
        int k=std::stoi(argv[1]);
        std::ifstream input(argv[2]); if(!input) throw std::runtime_error("input");
        std::string line; size_t row=0;
        while(std::getline(input,line)) {
            Domain d; std::istringstream fields(line); int p;
            while(fields>>p) d.points.push_back(p);
            if(!fields.eof() || d.points.empty() || d.points.size()>28 ||
               !std::is_sorted(d.points.begin(),d.points.end()) ||
               std::adjacent_find(d.points.begin(),d.points.end())!=d.points.end() ||
               d.points.front()<0 || d.points.back()>82)
                throw std::runtime_error("domain");
            if(k>0) {
                if(k>12) throw std::runtime_error("size");
                auto a=d.enumerate(k);
                std::cout<<row;
                for(Mask m:a) std::cout<<' '<<m;
                std::cout<<'\n';
            } else {
                if(d.points.size()!=28) throw std::runtime_error("profile domain");
                Mask all=(Mask(1)<<28)-1;
                auto tens=d.enumerate(10), elevens=d.enumerate(11), nines=d.enumerate(9);
                std::array<uint64_t,5> count{};
                const std::array<std::array<int,3>,5> shapes={{{10,10,8},{10,9,9},{11,10,7},{11,11,6},{11,9,8}}};
                for(size_t t=0;t<shapes.size();++t) {
                    const auto& a=shapes[t][0]==10?tens:elevens;
                    const auto& b=shapes[t][1]==11?elevens:(shapes[t][1]==10?tens:nines);
                    for(Mask x:a) for(Mask y:b)
                        if(!(x&y) && d.sidon(all^x^y)) ++count[t];
                }
                std::cout<<row<<' '<<tens.size()<<' '<<elevens.size()<<' '<<nines.size();
                for(auto c:count)std::cout<<' '<<c;
                std::cout<<'\n';
            }
            ++row;
        }
        if(!input.eof() || !std::cout) throw std::runtime_error("IO completion");
    } catch(const std::exception&e) { std::cerr<<e.what()<<'\n';return 1; }
}
