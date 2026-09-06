#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

struct Rat {
  std::int64_t n = 0;
  std::int64_t d = 1;
  Rat() = default;
  Rat(std::int64_t value) : n(value), d(1) {}
  Rat(std::int64_t num, std::int64_t den) : n(num), d(den) { normalize(); }
  void normalize() {
    if (d == 0) throw std::runtime_error("zero denominator");
    if (d < 0) { n = -n; d = -d; }
    const auto g = std::gcd(n < 0 ? -n : n, d);
    n /= g; d /= g;
  }
  std::string text() const { return d == 1 ? std::to_string(n) : std::to_string(n)+"/"+std::to_string(d); }
};
std::int64_t mul_checked(std::int64_t a,std::int64_t b) {
  std::int64_t result=0;
  if (__builtin_mul_overflow(a,b,&result)) throw std::runtime_error("rational multiplication overflow");
  return result;
}
std::int64_t add_checked(std::int64_t a,std::int64_t b) {
  std::int64_t result=0;
  if (__builtin_add_overflow(a,b,&result)) throw std::runtime_error("rational addition overflow");
  return result;
}
Rat operator+(const Rat& a, const Rat& b) {
  const auto g=std::gcd(a.d,b.d),ad=a.d/g,bd=b.d/g;
  return Rat(add_checked(mul_checked(a.n,bd),mul_checked(b.n,ad)),mul_checked(ad,b.d));
}
Rat operator-(const Rat& a, const Rat& b) {
  return a+Rat(-b.n,b.d);
}
Rat operator-(const Rat& a) { return Rat(-a.n,a.d); }
Rat operator*(const Rat& a, std::int64_t b) {
  const auto absolute=b<0?-b:b,g=std::gcd(absolute,a.d);
  return Rat(mul_checked(a.n,b/g),a.d/g);
}
Rat operator*(std::int64_t b, const Rat& a) { return a*b; }
bool operator==(const Rat& a,const Rat& b) { return a.n==b.n && a.d==b.d; }
bool operator<(const Rat& a,const Rat& b) {
  return mul_checked(a.n,b.d) < mul_checked(b.n,a.d);
}
bool operator<=(const Rat& a,const Rat& b) { return !(b<a); }
Rat maxrat(const Rat& a,const Rat& b) { return a<b ? b:a; }
Rat minrat(const Rat& a,const Rat& b) { return b<a ? b:a; }
Rat parse_rat(const std::string& text) {
  const auto slash=text.find('/');
  return slash==std::string::npos ? Rat(std::stoll(text))
    : Rat(std::stoll(text.substr(0,slash)),std::stoll(text.substr(slash+1)));
}

void require(bool condition,const std::string& message) {
  if (!condition) throw std::runtime_error(message);
}

constexpr int N=43;
constexpr int SELECTOR_FIRST=13245;
constexpr int MISSED_FIRST=13634;
const std::array<std::string,5> FAMILIES={"E8","E77","C8","C77","C77partition"};
const std::map<std::string,std::vector<std::string>> PATTERNS={
  {"E8",{"H","A"}},{"E77",{"BB","BO","OO"}},{"C8",{"B","O"}},
  {"C77",{"BB","BO","OO"}},{"C77partition",{"HO","AB"}}
};

struct Root { std::string family; int c; int k; std::string pattern; };
int count_char(const std::string& value,char target) {
  return static_cast<int>(std::count(value.begin(),value.end(),target));
}
std::vector<Root> roots() {
  std::vector<Root> result;
  const std::string cells="HABO";
  for (const auto& family:FAMILIES) for (int c=9;c<=13;++c) for (int k=0;k<=6;++k) {
    const std::array<int,4> es={k,6-k,6-k,1+k};
    const std::array<int,4> cs={c-k,14-c+k,14-c+k,c-k};
    const auto& sizes=family[0]=='E'?es:cs;
    for (const auto& pattern:PATTERNS.at(family)) {
      bool ok=true;
      for (int i=0;i<4;++i) ok=ok && count_char(pattern,cells[i])<=sizes[i];
      if (ok) result.push_back({family,c,k,pattern});
    }
  }
  require(result.size()==389,"root count");
  return result;
}
std::array<std::vector<int>,8> root_cells(const Root& root) {
  const std::array<int,8> sizes={root.k,6-root.k,6-root.k,1+root.k,
    root.c-root.k,14-root.c+root.k,14-root.c+root.k,root.c-root.k};
  std::array<std::vector<int>,8> cells;
  int cursor=2;
  for (int i=0;i<8;++i) {
    require(sizes[i]>=0,"negative cell");
    for (int j=0;j<sizes[i];++j) cells[i].push_back(cursor++);
  }
  require(cursor==N,"cell partition");
  return cells;
}
std::pair<std::vector<int>,std::vector<int>> root_data(const Root& root) {
  const auto cells=root_cells(root);
  std::vector<int> core=cells[0]; core.insert(core.end(),cells[4].begin(),cells[4].end());
  std::set<int> core_set(core.begin(),core.end());
  std::vector<int> exterior;
  for (int v=2;v<N;++v) if (!core_set.count(v)) exterior.push_back(v);
  require(static_cast<int>(core.size())==root.c && static_cast<int>(exterior.size())==41-root.c,"root data");
  return {core,exterior};
}
int edge_id(int i,int j) {
  if (i>j) std::swap(i,j);
  require(0<=i && i<j && j<N,"edge id");
  return i*(2*N-i-1)/2+(j-i-1)+1;
}

using MKey=std::tuple<int,int,int>;
using QKey=std::tuple<int,int,int,int>;
std::map<MKey,int> missed_ids(const std::vector<Root>& all_roots) {
  std::set<MKey> support;
  for (const auto& root:all_roots) {
    const auto [core,exterior]=root_data(root);
    for (std::size_t a=0;a<exterior.size();++a) for (std::size_t b=a+1;b<exterior.size();++b)
      for (int h:core) support.emplace(exterior[a],exterior[b],h);
  }
  require(support.size()==10612,"missed support");
  std::map<MKey,int> ids; int next=MISSED_FIRST;
  for (const auto& key:support) ids[key]=next++;
  return ids;
}

std::string opb_row(const std::vector<std::pair<int,int>>& terms,int rhs) {
  std::ostringstream out;
  for (std::size_t i=0;i<terms.size();++i) {
    if (i) out << ' ';
    out << (terms[i].first>=0?"+":"") << terms[i].first << " x" << terms[i].second;
  }
  out << " >= " << rhs << " ;";
  return out.str();
}
struct Hull { int shift; int lo; int hi; std::vector<int> tangents; };
Hull hull(int c,bool exceptional) {
  const int degree=exceptional?20:21, n=41-c;
  Hull result{n-degree+2,0,0,{}};
  result.lo=result.shift+c-9; result.hi=result.shift+4;
  for (int t=result.lo;t<result.hi;++t) result.tangents.push_back(t);
  if (result.tangents.empty()) result.tangents.push_back(result.lo);
  require(result.lo==(exceptional?14:13),"hull lower");
  return result;
}

std::map<std::string,Rat> load_edge_parameters(const std::string& path) {
  std::ifstream in(path); require(static_cast<bool>(in),"edge certificate open");
  std::string line; require(static_cast<bool>(std::getline(in,line)) && line=="name\tvalue","edge header");
  std::map<std::string,Rat> result;
  while (std::getline(in,line)) {
    const auto tab=line.find('\t'); require(tab!=std::string::npos,"edge field");
    require(result.emplace(line.substr(0,tab),parse_rat(line.substr(tab+1))).second,"edge duplicate");
  }
  const std::set<std::string> names={"pA","pB","pO","AA","AB","AO","BB","BO",
    "upA","upB","upO","aA","aB","aO","bA","bB","bO","oA","oB","oO"};
  std::set<std::string> got; for (const auto& item:result) got.insert(item.first);
  require(got==names,"edge names"); return result;
}
bool in(int v,int lo,int hi) { return lo<=v && v<hi; }
std::string type_of(int v) {
  if (v==0) return "u";
  if (v==1) return "v";
  if (v==2) return "p";
  if (in(v,3,8)) return "a";
  if (in(v,8,14)) return "b";
  if (v==14) return "o";
  if (in(v,15,28)) return "h";
  if (v==28) return "ca";
  if (v==29) return "cb";
  if (in(v,30,43)) return "co";
  throw std::runtime_error("vertex type");
}
bool red13(int i,int j) {
  int diff=((i-15)-(j-15))%13; if (diff<0) diff+=13;
  return diff==1 || diff==5 || diff==8 || diff==12;
}
Rat edge_value(int left,int right,const std::map<std::string,Rat>& p) {
  if (left>right) std::swap(left,right);
  require(0<=left && left<right && right<N,"edge value");
  if (left==0 && right==1) return Rat(1);
  if (left==0) return Rat(in(right,15,28)||in(right,2,8)||right==28);
  if (left==1) return Rat(in(right,15,28)||in(right,8,14)||right==29);
  const bool lh=in(left,15,28), rh=in(right,15,28);
  const bool le=in(left,2,15), re=in(right,2,15);
  if (lh&&rh) return Rat(red13(left,right));
  if (lh!=rh) { const int z=lh?right:left; return in(z,2,15)?Rat(6,13):Rat(3,5); }
  const auto lt=type_of(left),rt=type_of(right);
  if (le&&re) {
    if (lt=="p"||rt=="p") {
      const auto other=lt=="p"?rt:lt; return p.at(other=="a"?"pA":other=="b"?"pB":"pO");
    }
    auto pair=std::minmax(lt,rt);
    if (pair.first=="a"&&pair.second=="a") return p.at("AA");
    if (pair.first=="a"&&pair.second=="b") return p.at("AB");
    if (pair.first=="a"&&pair.second=="o") return p.at("AO");
    if (pair.first=="b"&&pair.second=="b") return p.at("BB");
    return p.at("BO");
  }
  if (le!=re) {
    const int e=le?left:right,c=le?right:left; const auto et=type_of(e),ct=type_of(c);
    const std::string row=et=="p"?"up":et;
    const std::string col=ct=="ca"?"A":ct=="cb"?"B":"O";
    return p.at(row+col);
  }
  const bool ls=lt=="ca"||lt=="cb",rs=rt=="ca"||rt=="cb";
  if (ls&&rs) return Rat(1);
  if (ls!=rs) return Rat(2,5);
  return Rat(8,15);
}

const std::array<std::string,10> TYPE_ORDER={"u","v","p","a","b","o","h","ca","cb","co"};
int type_index(const std::string& type) {
  const auto it=std::find(TYPE_ORDER.begin(),TYPE_ORDER.end(),type);
  require(it!=TYPE_ORDER.end(),"type index"); return static_cast<int>(it-TYPE_ORDER.begin());
}
std::string signature(int i,int j,int k,const std::map<std::string,Rat>& p) {
  std::array<std::string,3> types={type_of(i),type_of(j),type_of(k)};
  std::sort(types.begin(),types.end(),[](const auto& a,const auto& b){return type_index(a)<type_index(b);});
  std::array<Rat,3> edges={edge_value(i,j,p),edge_value(i,k,p),edge_value(j,k,p)};
  std::sort(edges.begin(),edges.end());
  return types[0]+","+types[1]+","+types[2]+"|"+edges[0].text()+","+edges[1].text()+","+edges[2].text();
}
struct Orbit { std::int64_t count; Rat lower; Rat upper; Rat z; std::int64_t seen=0; };
std::map<std::string,Orbit> load_orbits(const std::string& path) {
  std::ifstream in(path); require(static_cast<bool>(in),"orbit certificate open");
  std::string line; require(static_cast<bool>(std::getline(in,line))&&line=="signature\ttriples\tlower\tupper\tz","orbit header");
  std::map<std::string,Orbit> result;
  while (std::getline(in,line)) {
    std::vector<std::string> fields; std::size_t start=0;
    while (true) { const auto tab=line.find('\t',start); fields.push_back(line.substr(start,tab-start)); if (tab==std::string::npos) break; start=tab+1; }
    require(fields.size()==5,"orbit fields");
    Orbit o{std::stoll(fields[1]),parse_rat(fields[2]),parse_rat(fields[3]),parse_rat(fields[4]),0};
    require(o.lower<=o.z&&o.z<=o.upper,"orbit z bound");
    require(result.emplace(fields[0],o).second,"orbit duplicate");
  }
  require(result.size()==171,"orbit count"); return result;
}

void compare_sources(const std::vector<Root>& all_roots,const std::map<MKey,int>& mids,
                     const std::string& cert_path,const std::string& suffix_path) {
  std::ifstream cert(cert_path),suffix(suffix_path); require(cert&&suffix,"source inputs");
  std::string line;
  require(std::getline(cert,line)&&line=="index\tfamily\tc\tk\tpattern\tselector\tH\texterior\tE_columns\tC_columns\trows","root header");
  std::int64_t rows=0;
  for (std::size_t ri=0;ri<all_roots.size();++ri) {
    const auto& root=all_roots[ri]; const auto [core,exterior]=root_data(root);
    int ek=0,root_rows=0; std::ostringstream hs;
    for (std::size_t q=0;q<core.size();++q) { if(q)hs<<',';hs<<core[q];if(in(core[q],2,15))++ek; root_rows+=static_cast<int>(hull(root.c,in(core[q],2,15)).tangents.size())+1; }
    std::ostringstream expected;
    expected<<ri<<'\t'<<root.family<<'\t'<<root.c<<'\t'<<root.k<<'\t'<<root.pattern<<'\t'<<SELECTOR_FIRST+ri<<'\t'<<hs.str()<<'\t'<<exterior.size()<<'\t'<<ek<<'\t'<<root.c-ek<<'\t'<<root_rows;
    require(std::getline(cert,line)&&line==expected.str(),"root certificate mismatch");
    const int pairs=static_cast<int>(exterior.size()*(exterior.size()-1)/2);
    for (int h:core) {
      std::vector<int> ms,internal;
      for (std::size_t a=0;a<exterior.size();++a) for (std::size_t b=a+1;b<exterior.size();++b) ms.push_back(mids.at({exterior[a],exterior[b],h}));
      for (int other:core) if (other!=h) internal.push_back(edge_id(h,other));
      const auto hp=hull(root.c,in(h,2,15));
      for (int t:hp.tangents) {
        const int active=t*hp.shift-t*(t+1)/2,guard=active+t*(root.c-1);
        std::vector<std::pair<int,int>> terms; for(int v:ms)terms.push_back({1,v});for(int v:internal)terms.push_back({-t,v});terms.push_back({-guard,SELECTOR_FIRST+static_cast<int>(ri)});
        require(std::getline(suffix,line)&&line==opb_row(terms,-t*(root.c-1)),"suffix lower mismatch"); ++rows;
      }
      const int slope=hp.lo+hp.hi-1,active=hp.lo*hp.hi-slope*hp.shift,guard=active+2*pairs;
      std::vector<std::pair<int,int>> terms;for(int v:ms)terms.push_back({-2,v});for(int v:internal)terms.push_back({slope,v});terms.push_back({-guard,SELECTOR_FIRST+static_cast<int>(ri)});
      require(std::getline(suffix,line)&&line==opb_row(terms,-2*pairs),"suffix upper mismatch"); ++rows;
    }
  }
  require(!std::getline(cert,line),"trailing root certificate"); require(!std::getline(suffix,line),"trailing suffix"); require(rows==13078,"suffix row count");
}

void compare_formula_streams(const std::string& prior_path,const std::string& suffix_path,
                             const std::string& final_path) {
  std::ifstream prior(prior_path),suffix(suffix_path),final(final_path);
  require(prior&&suffix&&final,"formula stream inputs");
  std::string old_line,new_line,suffix_line;
  require(std::getline(prior,old_line)&&old_line=="* #variable= 98758 #constraint= 2969925 #equal= 87 intsize= 64","prior formula header");
  require(std::getline(final,new_line)&&new_line=="* #variable= 98758 #constraint= 2983003 #equal= 87 intsize= 64","final formula header");
  std::int64_t prior_body=0,suffix_rows=0;
  while(std::getline(prior,old_line)) {require(std::getline(final,new_line)&&new_line==old_line,"prior body mismatch");++prior_body;}
  while(std::getline(suffix,suffix_line)) {require(std::getline(final,new_line)&&new_line==suffix_line,"final suffix mismatch");++suffix_rows;}
  require(!std::getline(final,new_line),"trailing final formula");
  require(prior_body==2969925&&suffix_rows==13078,"formula stream row counts");
}

void check_fractional(const std::vector<Root>& all_roots,const std::map<MKey,int>&,
                      const std::map<std::string,Rat>& p,std::map<std::string,Orbit>& orbits) {
  auto edge=[&](int i,int j){return edge_value(i,j,p);};
  const std::set<int> exceptional={2,3,4,5,6,7,8,9,10,11,12,13,14};
  for(int v=0;v<N;++v){Rat degree,einc;for(int w=0;w<N;++w)if(w!=v){degree=degree+edge(v,w);if(exceptional.count(w))einc=einc+edge(v,w);}require(degree==Rat(exceptional.count(v)?20:21),"fractional degree");require(einc==Rat(v==2?8:6),"fractional E incidence");}
  std::int64_t five_count=0;Rat five_min(10),five_max;
  for(int a=0;a<N;++a)for(int b=a+1;b<N;++b)for(int c=b+1;c<N;++c)for(int d=c+1;d<N;++d)for(int e=d+1;e<N;++e){std::array<int,5> v={a,b,c,d,e};Rat total;for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)total=total+edge(v[i],v[j]);require(Rat(1)<=total&&total<=Rat(9),"fractional K5 row");five_min=minrat(five_min,total);five_max=maxrat(five_max,total);++five_count;}
  require(five_count==962598&&five_min==Rat(1)&&five_max==Rat(9),"five-set census");
  std::array<Rat,N> local{};std::int64_t triangle_count=0;
  for(int i=0;i<N;++i)for(int j=i+1;j<N;++j)for(int k=j+1;k<N;++k){auto key=signature(i,j,k,p);auto it=orbits.find(key);require(it!=orbits.end(),"missing orbit");Rat sum=edge(i,j)+edge(i,k)+edge(j,k);Rat lo=maxrat(Rat(0),sum-Rat(2)),hi=minrat(edge(i,j),minrat(edge(i,k),edge(j,k)));require(lo==it->second.lower&&hi==it->second.upper,"orbit bounds");require(lo<=it->second.z&&it->second.z<=hi,"triangle conjunction");++it->second.seen;local[i]=local[i]+it->second.z;local[j]=local[j]+it->second.z;local[k]=local[k]+it->second.z;++triangle_count;}
  for(const auto& [key,o]:orbits) require(o.seen==o.count,"orbit multiplicity");
  for(int v=0;v<N;++v) require(local[v]==Rat(exceptional.count(v)?93:100),"local triangle sum");
  require(triangle_count==12341,"triangle count");

  std::int64_t selector_rows=1,unary_rows=0,projected_rows=0;
  const std::string cell_names="HABO";
  for(std::size_t ri=0;ri<all_roots.size();++ri) {
    const auto& root=all_roots[ri]; const auto cells=root_cells(root);
    const Rat y(ri==48?1:0); const int anomaly_offset=root.family[0]=='E'?0:4;
    std::vector<int> anomalies;
    for(int ci=0;ci<4;++ci) for(int q=0;q<count_char(root.pattern,cell_names[ci]);++q)
      anomalies.push_back(cells[anomaly_offset+ci][static_cast<std::size_t>(q)]);
    const int excess=(root.family=="E8"||root.family=="C8")?2:1;
    auto unit=[&](int i,int j,int target){Rat value=edge(i,j);require(target ? Rat(0)<=value-y : Rat(-1)<=-value-y,"guarded root unit");++selector_rows;};
    unit(0,1,1);
    const std::array<std::pair<int,int>,4> bits={std::pair{1,1},{1,0},{0,1},{0,0}};
    for(int ci=0;ci<8;++ci) for(int vertex:cells[ci]) {unit(0,vertex,bits[ci%4].first);unit(1,vertex,bits[ci%4].second);}
    for(int vertex=0;vertex<N;++vertex) {
      Rat total;for(int other:exceptional)if(other!=vertex)total=total+edge(vertex,other);
      const int target=6+(std::find(anomalies.begin(),anomalies.end(),vertex)!=anomalies.end()?excess:0);
      require(Rat(0)<=total-target*y&&Rat(-13)<=-total-(13-target)*y,"guarded a equality");selector_rows+=2;
    }
    if(root.family=="C77partition") {
      require(anomalies.size()==2,"partition anomalies");const int p0=anomalies[0],p1=anomalies[1];
      require(Rat(-1)<=-edge(p0,p1)-y,"partition edge");++selector_rows;
      for(int vertex=0;vertex<N;++vertex) if(vertex==0||vertex==1||(in(vertex,15,43)&&vertex!=p0&&vertex!=p1)) {
        Rat total=edge(vertex,p0)+edge(vertex,p1);require(Rat(0)<=total-y&&Rat(-2)<=-total-y,"partition equality");selector_rows+=2;
      }
    }
    const auto [core,exterior]=root_data(root);
    for(int vertex:exterior){Rat total;for(int h:core)total=total+edge(vertex,h);require(Rat(0)<=total-(root.c-8)*y,"unary footprint");++unary_rows;}
    if(root.c==9||root.c==10) for(std::size_t a=0;a<exterior.size();++a)for(std::size_t b=a+1;b<exterior.size();++b){Rat total;for(int h:core)total=total+edge(exterior[a],h)+edge(exterior[b],h);total=total+(root.c-5)*edge(exterior[a],exterior[b])-(root.c-5)*y;require(Rat(0)<=total,"projected pair");++projected_rows;}
  }
  require(selector_rows==69732&&unary_rows==11672&&projected_rows==74958,"prior root rows");

  // Exact McCormick minima on the shared supports.
  std::map<MKey,Rat> m;
  std::set<QKey> qsupport;
  for(const auto& root:all_roots){const auto [core,exterior]=root_data(root);for(std::size_t a=0;a<exterior.size();++a)for(std::size_t b=a+1;b<exterior.size();++b){for(int h:core){MKey key={exterior[a],exterior[b],h};if(!m.count(key)){Rat value=maxrat(Rat(0),Rat(1)-edge(exterior[a],h)-edge(exterior[b],h));require(value+edge(exterior[a],h)<=Rat(1)&&value+edge(exterior[b],h)<=Rat(1)&&Rat(1)<=value+edge(exterior[a],h)+edge(exterior[b],h),"m definition");m[key]=value;}}for(std::size_t i=0;i<core.size();++i)for(std::size_t j=i+1;j<core.size();++j)qsupport.emplace(exterior[a],exterior[b],core[i],core[j]);}}
  require(m.size()==10612&&qsupport.size()==74513,"aux support");
  std::map<QKey,Rat> q;
  for(const auto& key:qsupport){const auto [l,r,i,j]=key;Rat value=maxrat(Rat(0),m.at({l,r,i})+m.at({l,r,j})+edge(i,j)-Rat(2));require(value<=m.at({l,r,i})&&value<=m.at({l,r,j})&&value<=edge(i,j)&&m.at({l,r,i})+m.at({l,r,j})+edge(i,j)-Rat(2)<=value,"q definition");q[key]=value;}
  std::int64_t local_rows=0;int new_violations=0;Rat minimum_slack;
  for(std::size_t ri=0;ri<all_roots.size();++ri){const auto& root=all_roots[ri];const auto [core,exterior]=root_data(root);Rat y(ri==48?1:0);for(std::size_t a=0;a<exterior.size();++a)for(std::size_t b=a+1;b<exterior.size();++b){int l=exterior[a],r=exterior[b];Rat ms,qs;for(int h:core)ms=ms+m.at({l,r,h});for(std::size_t i=0;i<core.size();++i)for(std::size_t j=i+1;j<core.size();++j)qs=qs+q.at({l,r,core[i],core[j]});Rat pe=edge(l,r);require(Rat(-root.c)<=-ms+(root.c-5)*pe-(root.c-5)*y,"local m row");require(Rat(-root.c)<=qs-ms+(root.c-2)*pe-(root.c-2)*y,"local first row");require(Rat(-3*root.c)<=qs-3*ms+(3*root.c-10)*pe-(3*root.c-10)*y,"local second row");local_rows+=3;}
    const int pairs=static_cast<int>(exterior.size()*(exterior.size()-1)/2);for(int h:core){Rat adeg,ms;for(int other:core)if(other!=h)adeg=adeg+edge(h,other);for(std::size_t a=0;a<exterior.size();++a)for(std::size_t b=a+1;b<exterior.size();++b)ms=ms+m.at({exterior[a],exterior[b],h});const auto hp=hull(root.c,exceptional.count(h));for(int t:hp.tangents){int active=t*hp.shift-t*(t+1)/2,guard=active+t*(root.c-1);Rat slack=ms-t*adeg-guard*y+Rat(t*(root.c-1));if(slack<Rat(0)){++new_violations;if(new_violations==1||slack<minimum_slack)minimum_slack=slack;require(ri==48&&t==13&&slack==Rat(-72),"unexpected hull violation");}}int slope=hp.lo+hp.hi-1,active=hp.lo*hp.hi-slope*hp.shift,guard=active+2*pairs;Rat slack=-2*ms+slope*adeg-guard*y+Rat(2*pairs);require(!(slack<Rat(0)),"upper hull violation");}}
  require(local_rows==508986&&new_violations==13&&minimum_slack==Rat(-72),"fractional separation");
}

}  // namespace

int main(int argc,char** argv) {
  try {
    require(argc==6||argc==8,"usage: independent_check roots.tsv suffix edge_parameters.tsv triangle_orbits.tsv expected_suffix_rows [prior.opb final.opb]");
    const auto all_roots=roots();const auto mids=missed_ids(all_roots);
    compare_sources(all_roots,mids,argv[1],argv[2]);
    auto parameters=load_edge_parameters(argv[3]);auto orbits=load_orbits(argv[4]);
    check_fractional(all_roots,mids,parameters,orbits);
    require(std::stoll(argv[5])==13078,"expected suffix rows");
    if(argc==8) compare_formula_streams(argv[6],argv[2],argv[7]);
    std::cout<<"PASS roots=389 missed_keys=10612 suffix_rows=13078 triangle_orbits=171 "
             <<"five_sets=962598 local_pair_rows=508986 hull_violations=13 minimum_slack=-72\n";
    return 0;
  } catch(const std::exception& error) { std::cerr<<"FAIL "<<error.what()<<'\n';return 1; }
}
