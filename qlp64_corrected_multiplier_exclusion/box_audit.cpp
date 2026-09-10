// Definition-level full ternary box oracle for EVERY input row's lift fiber.
// Including match.cpp exposes the production lift being tested, not the oracle.
#define main production_main
#include "match.cpp"
#undef main
#include <unordered_set>
std::uint64_t code(const Row& r,int d,int base,int offset) {
  std::uint64_t x=0;
  for(int j=0;j<d;++j) x=x*static_cast<unsigned>(base)+static_cast<unsigned>(r[j]+offset);
  return x;
}
int main(int argc,char** argv) {
  if(argc!=2) throw std::runtime_error("usage: box_audit INPUT16");
  std::ifstream in(argv[1]);int d=0;std::size_t n=0;
  if(!(in>>d>>n) || d!=16 || n==0) throw std::runtime_error("input");
  std::map<std::pair<Row,int>,std::vector<Candidate>> fibers;
  for(std::size_t i=0;i<n;++i) {
    Quad q{};for(auto& r:q) for(int j=0;j<d;++j) if(!(in>>r[j])) throw std::runtime_error("truncated");
    validate(q,d);
    for(int j=0;j<4;++j) fibers.try_emplace({q[j],j==3});
  }
  std::string extra;if(in>>extra) throw std::runtime_error("trailing");
  std::unordered_map<std::uint64_t,std::unordered_set<std::uint64_t>> remaining;
  std::uint64_t generated=0;
  for(auto& [key,cs]:fibers) {
    cs=lift(key.first,d,key.second);
    auto& set=remaining[code(key.first,16,5,2)];
    for(const auto& c:cs) if(!set.insert(code(c.row,32,3,1)).second) throw std::runtime_error("duplicate child");
    generated+=cs.size();
  }
  Row r{};std::uint64_t interior_tuples=0,eligible=0,matched=0;
  auto visit=[&](auto&& self,int j,int sum)->void {
    if(j==16) {
      ++interior_tuples;
      for(int a=-1;a<=1;++a) for(int b:{-1,1}) {
        int s=2*sum+a+b;
        if((s!=0 && s!=1) || (a==0)!=(s==1)) continue;
        r[0]=a;r[16]=b;
        ++eligible;
        Row p{};for(int k=0;k<16;++k) p[k]=r[k]+r[k+16];
        auto it=remaining.find(code(p,16,5,2));if(it==remaining.end()) continue;
        // Every ternary length-32 row has energy <=32<63, so the norm test is vacuous.
        if(it->second.erase(code(r,32,3,1))!=1) throw std::runtime_error("omitted or repeated direct-box child");
        ++matched;
      }
      return;
    }
    for(int x=-1;x<=1;++x) {r[j]=r[32-j]=x;self(self,j+1,sum+x);}
  };
  visit(visit,1,0);
  for(const auto& [k,s]:remaining) { (void)k;if(!s.empty()) throw std::runtime_error("extra production child"); }
  if(generated!=matched) throw std::runtime_error("count mismatch");
  std::cout<<"{\"full_interior_box\":"<<interior_tuples<<",\"eligible_rows\":"<<eligible
    <<",\"parent_fibers\":"<<fibers.size()<<",\"matched_children\":"<<matched
    <<",\"complete_sets_equal\":true}\n";
}
