#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {
constexpr int n=21;
constexpr std::uint32_t full=(1U<<n)-1;
struct G { int r,i; };
G operator+(G a,G b){return {a.r+b.r,a.i+b.i};}
G operator-(G a,G b){return {a.r-b.r,a.i-b.i};}
G operator*(G a,G b){return {a.r*b.r-a.i*b.i,a.r*b.i+a.i*b.r};}
bool operator==(G a,G b){return a.r==b.r&&a.i==b.i;}
G conj(G a){return {a.r,-a.i};}
G div_pi(G a){assert(((a.r+a.i)&1)==0);return {(a.r+a.i)/2,(a.i-a.r)/2};}
bool divisible_pi3(G a){for(int k=0;k<3;++k){if((a.r+a.i)&1)return false;a=div_pi(a);}return true;}
enum Kind{equal,opposite,quarter};
struct State{G s,h;Kind kind;};
std::array<State,16> make_states(){
  constexpr std::array<G,4> roots{{{1,0},{0,1},{-1,0},{0,-1}}};
  std::array<State,16> answer{};int at=0;
  for(G x:roots)for(G y:roots){int dot=x.r*y.r+x.i*y.i;answer[at++]={div_pi(x-y),div_pi(x+y),dot==1?equal:dot==-1?opposite:quarter};}
  return answer;
}
constexpr std::array<std::array<int,4>,6> cases{{
  {1,0,5,0},{3,0,4,1},{3,0,3,-2},{3,2,3,2},{3,2,2,3},{4,1,2,-1}
}};
std::uint32_t rotate(std::uint32_t x,int s){return ((x<<s)|(x>>(n-s)))&full;}
std::uint32_t canonical(std::uint32_t x){auto a=x;for(int s=1;s<n;++s)a=std::min(a,rotate(x,s));return a;}
using Supports=std::array<std::vector<std::pair<std::uint32_t,std::uint32_t>>,2>;
Supports read_supports(const std::string&path){
  std::ifstream in(path);assert(in);std::string line;std::getline(in,line);
  Supports out;std::set<std::pair<std::uint32_t,std::uint32_t>> q37;
  while(std::getline(in,line)){
    std::stringstream row(line);std::array<std::string,6> f;for(auto&x:f)std::getline(row,x,'\t');
    auto a=static_cast<std::uint32_t>(std::stoul(f[2],nullptr,16));auto b=static_cast<std::uint32_t>(std::stoul(f[3],nullptr,16));
    if((std::stoi(f[0])&1)==0)out[0].emplace_back(a,b);else q37.emplace(canonical(full^a),canonical(full^b));
  }
  std::sort(out[0].begin(),out[0].end());out[1]={q37.begin(),q37.end()};
  assert(out[0].size()==18&&out[1].size()==18);return out;
}
G target(int component,int shift){if(component)return {-2,0};if(shift==4)return {-2,0};if(shift==10)return {2,0};return {0,0};}
std::array<int,n> decode(std::string word){
  if(!word.empty()&&word.back()=='\r')word.pop_back();
  assert(word.size()==n);std::array<int,n> result{};
  for(int j=0;j<n;++j){char c=word[j];result[j]=c<='9'?c-'0':c-'a'+10;assert(result[j]>=0&&result[j]<16);}return result;
}
}

int main(int argc,char**argv){
  assert(argc==3);const auto table=make_states();const auto supports=read_supports(argv[1]);
  std::ifstream in(argv[2]);assert(in);std::string line;std::getline(in,line);
  std::set<std::tuple<int,int,int>> keys;std::array<std::set<int>,2> covered;
  std::array<int,2> branch_rows{};std::array<std::array<int,6>,2> case_rows{};
  while(std::getline(in,line)){
    std::stringstream row(line);std::array<std::string,7> f;for(auto&x:f)std::getline(row,x,'\t');
    int q=std::stoi(f[0]),branch=q==5?0:1,orbit=std::stoi(f[1]),case_id=std::stoi(f[2]);assert(q==5||q==37);
    assert(keys.emplace(q,orbit,case_id).second);covered[branch].insert(orbit);++branch_rows[branch];++case_rows[branch][case_id];
    auto support=supports[branch].at(orbit);assert(support.first==std::stoul(f[3],nullptr,16)&&support.second==std::stoul(f[4],nullptr,16));
    std::array<std::array<int,n>,2> words{{decode(f[5]),decode(f[6])}};int opposites=0;
    for(int family=0;family<2;++family){auto mask=family?support.second:support.first;for(int j=0;j<n;++j){auto kind=table[words[family][j]].kind;assert((kind==quarter)==static_cast<bool>((mask>>j)&1U));opposites+=kind==opposite;}}
    assert(opposites==(q==5?19:3));auto [p,qc,x,y]=cases[case_id];
    std::array<std::array<G,2>,2> wanted{{std::array<G,2>{{{p+qc,qc-p},{0,0}}},std::array<G,2>{{{x+y-1,y-x},{1,0}}}}};
    for(int family=0;family<2;++family)for(int component=0;component<2;++component){G sum{0,0};for(int state:words[family])sum=sum+(component?table[state].h:table[state].s);assert(sum==wanted[family][component]);}
    for(int component=0;component<2;++component)for(int shift=1;shift<=10;++shift){G paf{0,0};for(int family=0;family<2;++family)for(int j=0;j<n;++j){G a=component?table[words[family][j]].h:table[words[family][j]].s;G b=component?table[words[family][(j+shift)%n]].h:table[words[family][(j+shift)%n]].s;paf=paf+a*conj(b);}assert(divisible_pi3(paf-target(component,shift)));}
  }
  const std::array<int,2> expected_branches{108,108};
  const std::array<int,6> expected_q5{18,18,18,18,18,18},expected_q37{18,18,18,18,18,18};
  assert(keys.size()==216&&branch_rows==expected_branches);assert(covered[0].size()==18&&covered[1].size()==18);
  assert(case_rows[0]==expected_q5);assert(case_rows[1]==expected_q37);
  std::cout<<"rows=216;q5_rows=108;q37_rows=108;all_cells=216\nfull_census_certificate=verified\n";
}
