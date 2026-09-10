// Direct complete symmetric boxes, independent of the doubling parametrization.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>

void require(bool ok,const char* message){if(!ok)throw std::runtime_error(message);}
template<int N> std::uint64_t encode(const std::array<int,N>& r,int bound){
  std::uint64_t w=0;for(int x:r)w=w*static_cast<unsigned>(2*bound+1)+static_cast<unsigned>(x+bound);return w;
}
template<int N> void check(std::ifstream& in,int count,int bound,int cap){
  constexpr int D=N/2;
  std::unordered_map<std::uint64_t,std::unordered_set<std::uint64_t>> remaining;
  std::uint64_t supplied=0;int empty=0;
  for(int ci=0;ci<count;++ci){
    std::array<int,D> p{};int sum=0;
    for(int& v:p){require(bool(in>>v) && v>=-2*bound && v<=2*bound,"parent entry");sum+=v;}
    require(sum==0 || sum==1,"parent sum");
    for(int j=0;j<D;++j)require(p[j]==p[(D-j)%D],"parent symmetry");
    auto [it,fresh]=remaining.try_emplace(encode<D>(p,2*bound));require(fresh,"duplicate parent");
    std::size_t n=0;require(bool(in>>n),"child count");supplied+=n;empty+=(n==0);
    for(std::size_t j=0;j<n;++j){std::uint64_t word=0;require(bool(in>>word) && it->second.insert(word).second,"child code");}
  }
  std::string extra;require(!(in>>extra),"trailing input");
  std::array<int,N> r{};std::uint64_t interiors=0,eligible=0,matched=0;
  auto visit=[&](auto&& self,int j,int sum,int norm)->void{
    if(j==D){
      ++interiors;
      for(int a=-bound;a<=bound;++a)for(int b=-bound;b<=bound;++b){
        int s=2*sum+a+b;
        if((s!=0 && s!=1) || (a-bound-s)%2 || (b-bound)%2 || 2*norm+a*a+b*b>cap)continue;
        r[0]=a;r[D]=b;++eligible;
        std::array<int,D> parent{};for(int k=0;k<D;++k)parent[k]=r[k]+r[k+D];
        auto it=remaining.find(encode<D>(parent,2*bound));if(it==remaining.end())continue;
        require(it->second.erase(encode<N>(r,bound))==1,"omitted direct symmetric child");++matched;
      }
      return;
    }
    for(int x=-bound;x<=bound;++x){r[j]=r[N-j]=x;self(self,j+1,sum+x,norm+x*x);}
  };
  visit(visit,1,0,0);
  for(const auto& [key,rows]:remaining){(void)key;require(rows.empty(),"extra production child");}
  require(matched==supplied,"count disagreement");
  std::cout<<"{\"child_length\":"<<N<<",\"parents\":"<<count<<",\"empty_fibers\":"<<empty
    <<",\"interior_box\":"<<interiors<<",\"globally_eligible\":"<<eligible
    <<",\"matched_children\":"<<matched<<",\"complete_sets_equal\":true}\n";
}
int main(int argc,char** argv){
  require(argc==2,"usage: symmetric_oracle INPUT");std::ifstream in(argv[1]);int n=0,count=0,b=0,cap=0;
  require(bool(in>>n>>count>>b>>cap) && count>0,"header");
  require((n==8 || n==16 || n==32) && b==64/(2*n) && cap==65-64/n,"bounds");
  if(n==8)check<8>(in,count,b,cap);if(n==16)check<16>(in,count,b,cap);if(n==32)check<32>(in,count,b,cap);
  return 0;
}
