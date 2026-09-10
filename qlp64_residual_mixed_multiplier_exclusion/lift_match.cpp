// Complete bounded folding lifts; no equivalence reduction.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

void require(bool b,const char* m){if(!b)throw std::runtime_error(m);}
template<int N> using Row=std::array<int,N>;
template<int N> using Key=std::array<int,N/2+1>;
template<int N> Key<N> paf(const Row<N>& r){Key<N> k{};for(int h=0;h<=N/2;++h)for(int j=0;j<N;++j)k[h]+=r[j]*r[(j+h)%N];return k;}
template<int N> struct Hash{std::size_t operator()(const Key<N>& k)const{
 std::uint64_t h=1469598103934665603ULL;for(int v:k){h^=static_cast<std::uint64_t>(v);h*=1099511628211ULL;}return static_cast<std::size_t>(h);}};
template<int N> bool amicable(const Row<N>& r,const Row<N>& s){
 for(int k=1;k<N/2;++k){int a=0;for(int j=0;j<N;++j)a+=r[j]*s[(j+k)%N]-s[j]*r[(j+k)%N];if(a)return false;}return true;}
template<int N> std::vector<Row<N>> lifts(const Row<N/2>& parent,int kind,int cap_override=-1){
 constexpr int D=N/2,B=32/N;int cap=cap_override>=0?cap_override:(65-64/N)/(kind==0?2:1);
 Row<N> row{};std::vector<Row<N>> out;
 auto visit=[&](auto&& self,int j,int norm)->void{
  if(norm>cap)return;
  if(j==D){out.push_back(row);return;}
  for(int a=-B;a<=B;++a){int b=parent[j]-a;if(b < -B || b>B)continue;
   if(kind && j%2 && ((a-B)%2 || (b-B)%2))continue;
   row[j]=a;row[j+D]=b;self(self,j+1,norm+a*a+b*b);
  }
 };visit(visit,0,0);return out;
}
template<int N> void run(std::ifstream& in,int count,std::ofstream& out,bool preflight){
 std::uint64_t pairs=0,insertions=0,real_matches=0,children=0,viable=0;
 for(int ci=0;ci<count;++ci){
  std::array<Row<N/2>,3> q{};for(auto& r:q)for(int& v:r)require(bool(in>>v),"parent row");
  int pc=-1,rcap=-1,scap=-1;
  if constexpr(N==32){
   int lp=0,lr=16,ls=16;for(int v:q[0])lp+=std::abs(v);
   for(int j=0;j<N/2;j+=2){lr+=std::abs(q[1][j]);ls+=std::abs(q[2][j]);}
   if(2*lp+lr+ls>63){if(preflight)out<<ci<<" 0 0 0\n";continue;}
   pc=(63-lr-ls)/2;rcap=63-2*lp-ls;scap=63-2*lp-lr;
  }
  auto ps=lifts<N>(q[0],0,pc),rs=lifts<N>(q[1],1,rcap),ss=lifts<N>(q[2],2,scap);
  if(preflight){out<<ci<<' '<<ps.size()<<' '<<rs.size()<<' '<<ss.size()<<'\n';if constexpr(N==32){pairs+=ps.size()*std::min(rs.size(),ss.size());insertions+=std::max(rs.size(),ss.size());}else{pairs+=rs.size()*ss.size();insertions+=ps.size();}continue;}
  if(ps.empty() || rs.empty() || ss.empty())continue;++viable;
  if constexpr(N==32){
   bool rsmall=rs.size()<=ss.size();const auto& small=rsmall?rs:ss;const auto& large=rsmall?ss:rs;
   std::unordered_map<Key<N>,std::vector<int>,Hash<N>> table;
   for(std::size_t j=0;j<large.size();++j)table[paf<N>(large[j])].push_back(static_cast<int>(j));
   insertions+=large.size();std::vector<Key<N>> sc;for(const auto& row:small)sc.push_back(paf<N>(row));
   for(const auto& p:ps){auto pk=paf<N>(p);for(std::size_t j=0;j<small.size();++j){
    ++pairs;Key<N> key{};for(int k=0;k<=N/2;++k)key[k]=(k==0?65-64/N:-64/N)-2*pk[k]-sc[j][k];
    auto it=table.find(key);if(it==table.end())continue;real_matches+=it->second.size();
    for(int index:it->second){const auto& r=rsmall?small[j]:large[index];const auto& ssrow=rsmall?large[index]:small[j];
     if(!amicable<N>(r,ssrow))continue;++children;for(const auto& row:{p,r,ssrow})for(int v:row)out<<v<<' ';out<<'\n';
    }
   }}
   continue;
  }
  std::unordered_map<Key<N>,std::vector<int>,Hash<N>> table;
  for(std::size_t j=0;j<ps.size();++j){auto key=paf<N>(ps[j]);for(int k=0;k<=N/2;++k)key[k]=(k==0?65-64/N:-64/N)-2*key[k];table[key].push_back(static_cast<int>(j));}
  insertions+=ps.size();std::vector<Key<N>> rc,sc;
  for(const auto& r:rs)rc.push_back(paf<N>(r));for(const auto& s:ss)sc.push_back(paf<N>(s));
  for(std::size_t a=0;a<rs.size();++a)for(std::size_t b=0;b<ss.size();++b){
   ++pairs;Key<N> k{};for(int j=0;j<=N/2;++j)k[j]=rc[a][j]+sc[b][j];
   auto it=table.find(k);if(it==table.end())continue;real_matches+=it->second.size();
   if(!amicable<N>(rs[a],ss[b]))continue;
   for(int index:it->second){++children;for(const auto& r:{ps[index],rs[a],ss[b]})for(int v:r)out<<v<<' ';out<<'\n';}
  }
  if((ci+1)%16==0)std::cerr<<"parents "<<ci+1<<'/'<<count<<" children "<<children<<" pairs "<<pairs<<'\n';
 }
 std::string extra;require(!(in>>extra),"trailing input");
 std::cout<<"{\"length\":"<<N<<",\"parents\":"<<count<<",\"viable\":"<<viable<<",\"table_rows\":"<<insertions
 <<",\"pair_operations\":"<<pairs<<",\"pairing\":\""<<(N==32?"P_min_R_S":"R_S")<<"\",\"real_matches_before_amicability\":"<<real_matches<<",\"children\":"<<children<<",\"complete\":"<<(preflight?"false":"true")<<"}\n";
}
int main(int argc,char** argv){require(argc==3 || (argc==4 && std::string(argv[3])=="--preflight"),"input output [--preflight]");bool preflight=argc==4;std::ifstream in(argv[1]);std::ofstream out(argv[2]);int d=0,count=0;require(bool(in>>d>>count),"header");
 if(d==4)run<8>(in,count,out,preflight);else if(d==8)run<16>(in,count,out,preflight);else if(d==16)run<32>(in,count,out,preflight);else throw std::runtime_error("parent length must be 4,8,16");return 0;}
