// Direct folding-box oracle. No cyclotomic branch equations generate candidates.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>

void require(bool ok,const char* message) {if(!ok) throw std::runtime_error(message);}
template<int N> bool axis(const std::array<int,N>& r) {
  for(int k=1;k<N/2;++k) {
    int left=0,right=0;
    for(int j=0;j<N;++j) {
      left+=r[j]*r[(k+N-j)&(N-1)];
      right+=r[j]*r[(2*N-k-j)&(N-1)];
    }
    if(left!=right)return false;
  }
  return true;
}
template<int N> std::uint64_t encode(const std::array<int,N>& r,int bound) {
  std::uint64_t word=0;
  for(int x:r)word=word*static_cast<unsigned>(2*bound+1)+static_cast<unsigned>(x+bound);
  return word;
}
template<int N> void check(std::ifstream& in,int count,int bound,int cap) {
  constexpr int D=N/2;
  std::uint64_t box=0,eligible=0,accepted=0;
  std::size_t empty=0;
  std::set<std::array<int,D>> parents;
  for(int ci=0;ci<count;++ci) {
    std::array<int,D> parent{};int sum=0;
    for(int& x:parent){require(bool(in>>x) && x>=-2*bound && x<=2*bound,"parent entry");sum+=x;}
    require(sum==0 && axis<D>(parent),"parent hypothesis");
    require(parents.insert(parent).second,"duplicate parent");
    std::size_t n=0;require(bool(in>>n),"child count");
    empty+=(n==0);
    std::unordered_set<std::uint64_t> remaining;
    for(std::size_t j=0;j<n;++j){std::uint64_t w=0;require(bool(in>>w),"child code");require(remaining.insert(w).second,"duplicate production child");}
    std::array<int,N> r{};
    auto visit=[&](auto&& self,int j,int norm)->void {
      if(j==D) {
        ++box;
        if(norm>cap)return;
        ++eligible;
        if(!axis<N>(r))return;
        ++accepted;
        require(remaining.erase(encode<N>(r,bound))==1,"omitted direct-box child");
        return;
      }
      for(int x=-bound;x<=bound;++x) {
        int y=parent[j]-x;
        if(y < -bound || y>bound)continue;
        r[j]=x;r[j+D]=y;self(self,j+1,norm+x*x+y*y);
      }
    };
    visit(visit,0,0);
    require(remaining.empty(),"production child absent from direct oracle");
    if((ci+1)%16==0)std::cerr<<"audited "<<ci+1<<"/"<<count<<" parents, box "<<box<<"\n";
  }
  std::string extra;require(!(in>>extra),"trailing input");
  std::cout<<"{\"child_length\":"<<N<<",\"parents\":"<<count<<",\"empty_fibers\":"<<empty
    <<",\"unrestricted_folded_box\":"<<box<<",\"norm_eligible\":"<<eligible
    <<",\"axis_children\":"<<accepted<<",\"complete_sets_equal\":true}\n";
}
int main(int argc,char** argv) {
  require(argc==2,"usage: axis_oracle INPUT");
  std::ifstream in(argv[1]);int n=0,count=0,b=0,cap=0;
  require(bool(in>>n>>count>>b>>cap) && count>0,"header");
  require((n==8 || n==16 || n==32) && b==64/(2*n) && cap==(65-64/n)/2,"bounds");
  if(n==8)check<8>(in,count,b,cap);
  if(n==16)check<16>(in,count,b,cap);
  if(n==32)check<32>(in,count,b,cap);
  return 0;
}
