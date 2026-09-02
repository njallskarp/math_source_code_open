#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int n = 21;
constexpr std::uint32_t full = (1U << n) - 1;

struct G { int r, i; };
G operator+(G a, G b) { return {a.r + b.r, a.i + b.i}; }
G operator-(G a, G b) { return {a.r - b.r, a.i - b.i}; }
G operator*(G a, G b) { return {a.r * b.r - a.i * b.i, a.r * b.i + a.i * b.r}; }
G conj(G a) { return {a.r, -a.i}; }
G div_pi(G a) { assert(((a.r + a.i) & 1) == 0); return {(a.r + a.i) / 2, (a.i - a.r) / 2}; }

enum Kind { equal, opposite, quarter };
struct State { G s, h; Kind kind; };

std::array<State, 16> states() {
  constexpr std::array<G, 4> roots{{{1,0},{0,1},{-1,0},{0,-1}}};
  std::array<State, 16> result{};
  int at = 0;
  for (G x : roots) for (G y : roots) {
    const int dot = x.r * y.r + x.i * y.i;
    result[at++] = {div_pi(x-y), div_pi(x+y), dot == 1 ? equal : dot == -1 ? opposite : quarter};
  }
  return result;
}

constexpr std::array<std::array<int,4>,6> cases{{
  {1,0,5,0},{3,0,4,1},{3,0,3,-2},{3,2,3,2},{3,2,2,3},{4,1,2,-1}
}};

std::uint32_t rotate(std::uint32_t x, int s) { return ((x << s) | (x >> (n-s))) & full; }
std::uint32_t canonical(std::uint32_t x) {
  std::uint32_t answer=x; for(int s=1;s<n;++s) answer=std::min(answer,rotate(x,s)); return answer;
}

std::pair<std::vector<std::pair<std::uint32_t,std::uint32_t>>,
          std::vector<std::pair<std::uint32_t,std::uint32_t>>>
read_supports(const std::string &path) {
  std::ifstream input(path); assert(input); std::string line; std::getline(input,line);
  std::vector<std::pair<std::uint32_t,std::uint32_t>> q5;
  std::set<std::pair<std::uint32_t,std::uint32_t>> q37;
  while(std::getline(input,line)) {
    std::stringstream row(line); std::array<std::string,6> field;
    for(auto &x:field) std::getline(row,x,'\t');
    auto a=static_cast<std::uint32_t>(std::stoul(field[2],nullptr,16));
    auto b=static_cast<std::uint32_t>(std::stoul(field[3],nullptr,16));
    if((std::stoi(field[0])&1)==0) q5.emplace_back(a,b);
    else q37.emplace(canonical(full^a),canonical(full^b));
  }
  std::sort(q5.begin(),q5.end()); assert(q5.size()==18 && q37.size()==18);
  return {q5,{q37.begin(),q37.end()}};
}

int mod_distance(int x) {
  x %= 4; if(x<0) x+=4; return std::min(x,4-x);
}

std::string encode(const std::array<int,42> &z,int family);

struct Search {
  const std::array<State,16> table = states();
  int q_value, case_id;
  std::pair<std::uint32_t,std::uint32_t> support;
  std::array<int,42> z{};
  std::mt19937_64 rng;

  Search(int q, int c, std::pair<std::uint32_t,std::uint32_t> u, std::uint64_t seed)
      : q_value(q), case_id(c), support(u), rng(seed) {}

  bool is_quarter(int index) const {
    int family=index/n, position=index%n;
    return (((family? support.second:support.first)>>position)&1U)!=0;
  }
  int random_state(int index) {
    std::array<int,8> allowed{}; int count=0;
    for(int state=0;state<16;++state) if((table[state].kind==quarter)==is_quarter(index)) allowed[count++]=state;
    return allowed[rng()%count];
  }
  void randomize() { for(int i=0;i<42;++i) z[i]=random_state(i); }

  int cost() const {
    const auto [p,q,x,y]=cases[case_id];
    const std::array<std::array<G,2>,2> targets{{
      std::array<G,2>{{G{p+q,q-p},G{0,0}}},
      std::array<G,2>{{G{x+y-1,y-x},G{1,0}}}
    }};
    int opposite_count=0, answer=0;
    for(int value:z) opposite_count += table[value].kind==opposite;
    answer += 12*std::abs(opposite_count-(q_value==5?19:3));
    for(int family=0;family<2;++family) for(int component=0;component<2;++component) {
      G sum{0,0}; for(int j=0;j<n;++j) sum=sum+(component?table[z[family*n+j]].h:table[z[family*n+j]].s);
      answer += 4*(std::abs(sum.r-targets[family][component].r)+std::abs(sum.i-targets[family][component].i));
    }
    for(int component=0;component<2;++component) for(int shift=1;shift<=10;++shift) {
      G paf{0,0};
      for(int family=0;family<2;++family) for(int j=0;j<n;++j) {
        G left=component?table[z[family*n+j]].h:table[z[family*n+j]].s;
        G right=component?table[z[family*n+(j+shift)%n]].h:table[z[family*n+(j+shift)%n]].s;
        paf=paf+left*conj(right);
      }
      G wanted = component ? G{-2,0} : shift==4 ? G{-2,0} : shift==10 ? G{2,0} : G{0,0};
      G residual=paf-wanted;
      answer += mod_distance(residual.r+residual.i)+mod_distance(residual.i-residual.r);
    }
    return answer;
  }

  bool allowed(int index, int state) const {
    return (table[state].kind==quarter)==is_quarter(index);
  }

  int polish() {
    int current=cost();
    bool improved=true;
    while(improved && current) {
      improved=false;
      for(int first=0;first<42 && !improved;++first) {
        int old_first=z[first];
        for(int a=0;a<16 && !improved;++a) if(allowed(first,a) && a!=old_first) {
          z[first]=a;
          int one=cost();
          if(one<current) { current=one; improved=true; break; }
          for(int second=first+1;second<42 && !improved;++second) {
            int old_second=z[second];
            for(int b=0;b<16;++b) if(allowed(second,b) && b!=old_second) {
              z[second]=b; int two=cost();
              if(two<current) { current=two; improved=true; break; }
            }
            if(!improved) z[second]=old_second;
          }
          if(!improved) z[first]=old_first;
        }
      }
    }
    return current;
  }

  bool run(std::uint64_t iterations) {
    std::array<int,42> best{};
    int global_best=1000000;
    for(std::uint64_t step=0;step<iterations;++step) {
      if(step%200000==0) randomize();
      int current=cost();
      if(current<global_best) {
        global_best=current; best=z; std::cerr<<"best="<<global_best<<" step="<<step<<'\n';
        if(global_best<=12) {
          int polished=polish();
          if(polished<global_best) { global_best=polished; best=z; std::cerr<<"polished="<<global_best<<'\n'; }
          else z=best;
        }
      }
      if(current==0) return true;
      const int move_size = (rng()%100 < 82) ? 1 : (rng()%100 < 80 ? 2 : 3);
      std::array<int,3> indices{}, old{};
      for(int move=0;move<move_size;++move) {
        indices[move]=rng()%42;
        old[move]=z[indices[move]];
        z[indices[move]]=random_state(indices[move]);
      }
      int next=cost();
      double phase=static_cast<double>(step%200000)/200000.0;
      double temperature=3.0*(1.0-phase)+0.15;
      if(next>current && std::generate_canonical<double,53>(rng)>=std::exp((current-next)/temperature))
        for(int move=move_size-1;move>=0;--move) z[indices[move]]=old[move];
    }
    z=best; std::cerr<<"final_best="<<global_best<<" states_a="<<encode(z,0)
                     <<" states_b="<<encode(z,1)<<'\n'; return false;
  }
};

std::string encode(const std::array<int,42> &z,int family) {
  std::ostringstream out; out<<std::hex;
  for(int j=0;j<n;++j) out<<z[family*n+j];
  return out.str();
}

} // namespace

int main(int argc,char**argv) {
  if(argc!=7) { std::cerr<<"usage: search FRONTIER q orbit case iterations seed\n"; return 2; }
  const auto [q5,q37]=read_supports(argv[1]); int q=std::stoi(argv[2]), orbit=std::stoi(argv[3]), c=std::stoi(argv[4]);
  auto support=(q==5?q5:q37).at(orbit); Search search(q,c,support,std::stoull(argv[6]));
  if(!search.run(std::stoull(argv[5]))) return 1;
  std::cout<<q<<'\t'<<orbit<<'\t'<<c<<'\t'<<std::hex<<std::setw(6)<<std::setfill('0')<<support.first<<'\t'
           <<std::setw(6)<<support.second<<'\t'<<encode(search.z,0)<<'\t'<<encode(search.z,1)<<'\n';
}
