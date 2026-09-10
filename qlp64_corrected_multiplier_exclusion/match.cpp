// Exact symmetric half-compression lift and full-key matching for N=64.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using Row = std::array<int,32>;
using Quad = std::array<Row,4>;
using Key = std::array<std::int16_t,17>;
struct Hash {
  std::size_t operator()(const Key& k) const {
    std::uint64_t h=1469598103934665603ULL;
    for(auto v:k) {h^=static_cast<std::uint16_t>(v); h*=1099511628211ULL;}
    return static_cast<std::size_t>(h);
  }
};
struct Candidate { Row row; Key paf; };
Key correlations(const Row& r,int d) {
  Key k{};
  for(int s=0;s<=d/2;++s) {
    int v=0;
    for(int j=0;j<d;++j) v+=r[j]*r[(j+s)%d];
    if(v < -1024 || v>1024) throw std::runtime_error("correlation range");
    k[s]=static_cast<std::int16_t>(v);
  }
  return k;
}
void validate(const Quad& q,int d) {
  Key total{};
  for(int i=0;i<4;++i) {
    int sum=0,b=64/(2*d);
    for(int j=0;j<d;++j) {
      if(std::abs(q[i][j])>b || q[i][j]!=q[i][(d-j)%d])
        throw std::runtime_error("invalid row");
      sum+=q[i][j];
    }
    if(sum!=(i==3) || (q[i][0]-b-(i==3))%2 || (q[i][d/2]-b)%2)
      throw std::runtime_error("invalid sum or endpoint parity");
    auto c=correlations(q[i],d);
    for(int j=0;j<=d/2;++j) total[j]+=c[j];
  }
  for(int j=0;j<=d/2;++j)
    if(total[j]!=(j==0?65-64/d:-64/d))
      throw std::runtime_error("invalid combined correlation");
}
std::vector<Candidate> lift(const Row& p,int d,int s) {
  int b=64/(4*d),m=p[d/2];
  if(m%2 || std::abs(m/2)>b) return {};
  Row r{}; r[d/2]=r[3*d/2]=m/2;
  std::vector<Candidate> out;
  std::function<void(int)> visit=[&](int j) {
    if(j==d/2) {
      auto c=correlations(r,2*d);
      if(c[0]<=65-64/(2*d)) out.push_back({r,c});
      return;
    }
    for(int x=std::max(-b,p[j]-b);x<=std::min(b,p[j]+b);++x) {
      if(j==0) {
        if((x-b-s)%2 || (p[0]-x-b)%2) continue;
        r[0]=x; r[d]=p[0]-x;
      } else {
        r[j]=r[2*d-j]=x; r[d-j]=r[d+j]=p[j]-x;
      }
      visit(j+1);
    }
  };
  visit(0);
  return out;
}
Quad canonical(Quad q,int d) {
  for(int i=0;i<3;++i) {
    Row neg{}; for(int j=0;j<d;++j) neg[j]=-q[i][j];
    q[i]=std::min(q[i],neg);
  }
  std::sort(q.begin(),q.begin()+3); return q;
}
Quad unit_canonical(const Quad& q,int d) {
  Quad best=canonical(q,d);
  for(int u=3;u<d;u+=2) {
    Quad v{};
    for(int i=0;i<4;++i) for(int j=0;j<d;++j) v[i][j]=q[i][u*j%d];
    best=std::min(best,canonical(v,d));
  }
  return best;
}
struct Pair {std::uint32_t x,y; std::int64_t next;};
int main(int argc,char** argv) {
  if(argc<3) throw std::runtime_error("usage: match INPUT OUTPUT [--units] [--begin N] [--end N] [--rows]");
  bool units=false,rows_only=false;
  std::size_t begin=0,end=~std::size_t{0};
  for(int i=3;i<argc;++i) {
    std::string a=argv[i];
    if(a=="--units") units=true;
    else if(a=="--rows") rows_only=true;
    else if(a=="--begin" && i+1<argc) begin=std::stoull(argv[++i]);
    else if(a=="--end" && i+1<argc) end=std::stoull(argv[++i]);
    else throw std::runtime_error("invalid option");
  }
  std::ifstream in(argv[1]);
  int d=0;std::size_t n=0;
  if(!(in>>d>>n) || (d!=4 && d!=8 && d!=16) || n==0)
    throw std::runtime_error("invalid header");
  std::vector<Quad> qs(n);
  for(auto& q:qs) {
    for(auto& r:q) for(int j=0;j<d;++j) if(!(in>>r[j])) throw std::runtime_error("truncated input");
    validate(q,d);
  }
  std::string extra; if(in>>extra) throw std::runtime_error("trailing input");
  end=std::min(end,n); if(begin>=end) throw std::runtime_error("empty partition");
  std::map<std::pair<Row,int>,std::vector<Candidate>> cache;
  auto candidates=[&](const Row& r,int s)->const std::vector<Candidate>& {
    auto key=std::make_pair(r,s); auto it=cache.find(key);
    if(it==cache.end()) it=cache.emplace(key,lift(r,d,s)).first;
    return it->second;
  };
  std::set<Quad> output;
  std::uint64_t pairs=0,matches=0;
  auto start=std::chrono::steady_clock::now();
  for(std::size_t qi=begin;qi<end;++qi) {
    std::array<const std::vector<Candidate>*,4> rr{};
    bool empty=false;
    for(int i=0;i<4;++i) {rr[i]=&candidates(qs[qi][i],i==3); empty|=rr[i]->empty();}
    if(rows_only || empty) continue;
    std::array<int,4> ix{0,1,2,3};
    std::sort(ix.begin(),ix.end(),[&](int a,int b){return std::make_pair(rr[a]->size(),a)<std::make_pair(rr[b]->size(),b);});
    int a=ix[0],b=ix[3],c=ix[1],e=ix[2];
    if(rr[a]->size()*rr[b]->size()>rr[c]->size()*rr[e]->size()) {std::swap(a,c);std::swap(b,e);}
    std::unordered_map<Key,std::int64_t,Hash> table;
    std::vector<Pair> links;
    auto count=rr[a]->size()*rr[b]->size();table.reserve(count);links.reserve(count);
    for(std::size_t x=0;x<rr[a]->size();++x) for(std::size_t y=0;y<rr[b]->size();++y) {
      Key k{};
      for(int j=0;j<=d;++j) k[j]=static_cast<std::int16_t>((*rr[a])[x].paf[j]+(*rr[b])[y].paf[j]);
      auto [it,fresh]=table.try_emplace(k,-1);(void)fresh;
      links.push_back({static_cast<std::uint32_t>(x),static_cast<std::uint32_t>(y),it->second});
      it->second=static_cast<std::int64_t>(links.size()-1);++pairs;
    }
    for(const auto& x:*rr[c]) for(const auto& y:*rr[e]) {
      Key k{};
      for(int j=0;j<=d;++j) k[j]=static_cast<std::int16_t>((j==0?65-64/(2*d):-64/(2*d))-x.paf[j]-y.paf[j]);
      ++pairs;auto it=table.find(k);if(it==table.end()) continue;
      for(auto p=it->second;p>=0;p=links[static_cast<std::size_t>(p)].next) {
        const auto& l=links[static_cast<std::size_t>(p)];
        Quad q{};q[a]=(*rr[a])[l.x].row;q[b]=(*rr[b])[l.y].row;q[c]=x.row;q[e]=y.row;
        ++matches;output.insert(canonical(q,2*d));
      }
    }
    if((qi+1)%64==0) std::cerr<<"progress "<<qi+1<<"/"<<end<<" pairs "<<pairs<<" matches "<<matches<<" unique "<<output.size()<<std::endl;
  }
  std::ofstream out(argv[2]); if(!out) throw std::runtime_error("cannot open output");
  if(rows_only) {
    for(const auto& [key,cs]:cache) {
      out<<key.second;for(int j=0;j<d;++j) out<<' '<<key.first[j];out<<' '<<cs.size()<<'\n';
      for(const auto& c:cs) {for(int j=0;j<2*d;++j) out<<c.row[j]<<' ';out<<'\n';}
    }
  } else {
    const auto before=output.size();
    if(units) {std::set<Quad> reduced;for(const auto& q:output) reduced.insert(unit_canonical(q,2*d));output=std::move(reduced);}
    out<<2*d<<' '<<output.size()<<'\n';
    for(const auto& q:output) {validate(q,2*d);for(const auto& r:q) for(int j=0;j<2*d;++j) out<<r[j]<<' ';out<<'\n';}
    std::cout<<"{\"input_length\":"<<d<<",\"total_input\":"<<n<<",\"begin\":"<<begin<<",\"end\":"<<end
      <<",\"pairs\":"<<pairs<<",\"labelled_matches\":"<<matches<<",\"canonical\":"<<before<<",\"output\":"<<output.size()
      <<",\"unit_reduced\":"<<(units?"true":"false")<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";
  }
  out.close();if(!out) throw std::runtime_error("output failure");
  return 0;
}
