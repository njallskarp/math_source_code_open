// Separate complete matcher on independently audited row sets. Direct indexed
// buckets replace hashing; candidate imaginary parts use Gaussian coordinates.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <utility>
#include <vector>

using Parent=std::array<int,8>;
using Row=std::array<int,16>;
using Key=std::array<int,9>;
void need(bool b,const char* s){if(!b)throw std::runtime_error(s);}
Key correlation(const Row& row){Key a{};for(int k=0;k<9;++k)for(int j=0;j<16;++j)a[k]+=row[j]*row[(j+k)%16];return a;}
bool gaussian_real(const Row& r,const Row& s){
 std::array<int,16> x{},y{};for(int j=0;j<16;++j){x[j]=s[j]+r[j];y[j]=s[j]-r[j];}
 for(int k=1;k<8;++k){int z=0;for(int j=0;j<16;++j)z+=y[j]*x[(j+k)%16]-x[j]*y[(j+k)%16];if(z)return false;}return true;
}
unsigned bucket(const Key& key){
 need(key[0]>=0 && key[0]<64 && key[1]>=-128 && key[1]<128 && key[2]>=-128 && key[2]<128,"bucket bounds");
 return (static_cast<unsigned>(key[0])<<16)|(static_cast<unsigned>(key[1]+128)<<8)|static_cast<unsigned>(key[2]+128);
}
int main(int argc,char** argv){
 need(argc==5,"fiber cases, fiber rows, parent triples, output triples");
 std::ifstream ci(argv[1]),fi(argv[2]),pi(argv[3]);std::ofstream output(argv[4]);int nc=0;need(bool(ci>>nc),"case count");
 std::map<std::pair<int,Parent>,std::vector<Row>> fibers;
 for(int i=0;i<nc;++i){int n=0,kind=0,cap=0;need(bool(ci>>n>>kind>>cap),"case");std::vector<int> parent(static_cast<std::size_t>(n/2));for(int& v:parent)need(bool(ci>>v),"parent");
  std::size_t nr=0;need(bool(fi>>nr),"fiber count");
  std::vector<Row> rows;
  for(std::size_t j=0;j<nr;++j){std::uint64_t code=0;need(bool(fi>>code),"code");if(n!=16)continue;Row row{};
   for(int k=15;k>=0;--k){row[k]=static_cast<int>(code%5)-2;code/=5;}need(code==0,"code overflow");
   int norm=0;for(int k=0;k<16;++k){norm+=row[k]*row[k];if(kind && k%2)need(row[k]%2==0,"odd entry");}
   need(norm<=cap,"norm");for(int k=0;k<8;++k)need(row[k]+row[k+8]==parent[k],"fold");rows.push_back(row);
  }
  if(n==16){need(cap==(kind?61:30),"cap");Parent p{};for(int j=0;j<8;++j)p[j]=parent[j];need(fibers.emplace(std::make_pair(kind,p),std::move(rows)).second,"duplicate fiber");}
 }
 int d=0,count=0;need(bool(pi>>d>>count) && d==8,"triple header");std::uint64_t pairs=0,bucket_pairs=0,real=0,accepted=0;
 for(int index=0;index<count;++index){std::array<Parent,3> parent{};for(auto& r:parent)for(int& v:r)need(bool(pi>>v),"triple");
  const auto& ps=fibers.at({0,parent[0]});const auto& rs=fibers.at({1,parent[1]});const auto& ss=fibers.at({1,parent[2]});
  std::vector<int> heads(1U<<22,-1),next(ps.size(),-1);std::vector<Key> keys,rc,sc;
  for(std::size_t j=0;j<ps.size();++j){auto key=correlation(ps[j]);for(int k=0;k<9;++k)key[k]=(k==0?61:-4)-2*key[k];unsigned b=bucket(key);next[j]=heads[b];heads[b]=static_cast<int>(j);keys.push_back(key);}
  for(const auto& r:rs)rc.push_back(correlation(r));for(const auto& s:ss)sc.push_back(correlation(s));
  for(std::size_t a=0;a<rs.size();++a)for(std::size_t b=0;b<ss.size();++b){++pairs;Key key{};key[0]=rc[a][0]+sc[b][0];if(key[0]>=64)continue;
   key[1]=rc[a][1]+sc[b][1];key[2]=rc[a][2]+sc[b][2];int at=heads[bucket(key)];if(at<0)continue;++bucket_pairs;
   for(int k=3;k<9;++k)key[k]=rc[a][k]+sc[b][k];
   for(;at>=0;at=next[static_cast<std::size_t>(at)]){if(keys[static_cast<std::size_t>(at)]!=key)continue;++real;if(!gaussian_real(rs[a],ss[b]))continue;++accepted;
    for(const auto& r:{ps[static_cast<std::size_t>(at)],rs[a],ss[b]})for(int v:r)output<<v<<' ';output<<'\n';
   }
  }
 }
 std::cout<<"{\"parents\":"<<count<<",\"pair_operations\":"<<pairs<<",\"nonempty_bucket_pairs\":"<<bucket_pairs<<",\"real_matches\":"<<real<<",\"children\":"<<accepted<<",\"complete\":true}\n";
 return 0;
}
