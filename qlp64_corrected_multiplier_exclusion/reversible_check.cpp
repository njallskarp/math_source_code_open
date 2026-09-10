// The generic orbit-constraint generator below is reused from the independent
// review package, commit e494f4aa9e1e87130838181f6b74d285c4a98135.
// This checker extends its input scope and deduplicates exact autocorrelation
// vectors. Only h=63 is covered: reversibility makes all skew terms zero.
// Independent final-stage audit: generic orbit constraints and all lags.
// No imports or includes from the reviewed implementation.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

using Word = std::uint64_t;
using Row = std::array<int, 32>;
using Quad = std::array<Row, 4>;
using Assignment = std::vector<int>;

void require(bool condition, const char *message) {
  if (!condition) throw std::runtime_error(message);
}

struct Lift {
  Word word;
  std::array<Word, 32> shifted;
  std::array<int, 32> autocorrelation;
};

int correlation(Word a, Word b) {
  return 64 - 2 * std::popcount(a ^ b);
}

// Use a generic system of negative-count equations on multiplier orbits:
// t_orbit(j) + t_orbit(j+32) = 1-z[j]. This avoids the special-case
// j-parity lift formulas in the reviewed implementation.
std::vector<Lift> enumerate_lifts(const Row &z, int h) {
  std::array<int, 64> orbit;
  orbit.fill(-1);
  std::vector<Word> masks;
  for (int j = 0; j < 64; ++j) {
    if (orbit[j] != -1) continue;
    int id = static_cast<int>(masks.size());
    Word mask = 0;
    int k = j;
    do {
      require(orbit[k] == -1, "overlapping multiplier orbits");
      orbit[k] = id;
      mask |= Word{1} << k;
      k = h*k % 64;
    } while (k != j);
    masks.push_back(mask);
  }
  std::vector<Lift> output;
  auto visit = [&](auto &&self, Assignment a) -> void {
    bool changed = true;
    while (changed) {
      changed = false;
      for (int j = 0; j < 32; ++j) {
        int u = orbit[j], v = orbit[j+32], target = 1-z[j];
        if (u == v) {
          if (target % 2) return;
          int value = target/2;
          if (a[u] != -1 && a[u] != value) return;
          if (a[u] == -1) { a[u] = value; changed = true; }
        } else if (a[u] != -1 && a[v] != -1) {
          if (a[u]+a[v] != target) return;
        } else if (a[u] != -1 || a[v] != -1) {
          int known = a[u] != -1 ? u : v;
          int unknown = known == u ? v : u;
          int value = target-a[known];
          if (value < 0 || value > 1) return;
          a[unknown] = value;
          changed = true;
        } else if (target == 0 || target == 2) {
          a[u] = a[v] = target/2;
          changed = true;
        }
      }
    }
    auto unknown = std::find(a.begin(), a.end(), -1);
    if (unknown != a.end()) {
      std::size_t j = static_cast<std::size_t>(unknown-a.begin());
      a[j] = 0; self(self, a);
      a[j] = 1; self(self, a);
      return;
    }
    Word w = 0;
    for (std::size_t j = 0; j < a.size(); ++j)
      if (a[j]) w |= masks[j];
    for (int j = 0; j < 32; ++j)
      require(1-static_cast<int>((w >> j)&1)-static_cast<int>((w >> (j+32))&1)
                  == z[j], "compression mismatch");
    for (int j = 0; j < 64; ++j)
      require(((w >> j)&1) == ((w >> (h*j%64))&1), "invariance mismatch");
    Lift lifted{};
    lifted.word = w;
    for (int k = 1; k <= 32; ++k) {
      // Explicit shift rather than std::rotr; k is never 0 or 64.
      lifted.shifted[k-1] = (w >> k) | (w << (64-k));
      lifted.autocorrelation[k-1] = correlation(w, lifted.shifted[k-1]);
    }
    output.push_back(lifted);
  };
  visit(visit, Assignment(masks.size(), -1));
  return output;
}

#include <set>
using Spectrum=std::array<std::int16_t,32>;
struct SpectrumHash {
  std::size_t operator()(const Spectrum& c) const {
    std::uint64_t x=0;
    for(auto v:c) x=x*1000003ULL+static_cast<std::uint16_t>(v);
    return static_cast<std::size_t>(x);
  }
};
int main(int argc,char** argv) {
  require(argc==2,"usage: reversible_check COMPRESSED_INPUT");
  std::ifstream in(argv[1]);std::size_t n=0;
  require(bool(in>>n) && n>0,"invalid parent count");
  std::vector<Quad> qs(n);
  std::map<Row,std::vector<Spectrum>> rows;
  for(auto& q:qs) {
    for(int i=0;i<4;++i) {
      int s=0;
      for(int& v:q[i]) {require(bool(in>>v) && v>=-1 && v<=1,"entry");s+=v;}
      require(s==(i==3),"sum");
      require(q[i][16]!=0 && (q[i][0]==0)==(i==3),"endpoint");
      for(int j=0;j<32;++j) require(q[i][j]==q[i][(32-j)%32],"symmetry");
      rows.try_emplace(q[i]);
    }
    for(int k=0;k<32;++k) {
      int s=0;
      for(const auto& r:q) for(int j=0;j<32;++j) s+=r[j]*r[(j+k)%32];
      require(s==(k==0?63:-2),"compressed correlations");
    }
  }
  std::string extra;require(!(in>>extra),"trailing input");
  std::uint64_t words=0,spectra=0,pairs=0,keys=0;
  for(auto& [z,out]:rows) {
    auto full=enumerate_lifts(z,63);
    std::set<Spectrum> distinct;
    for(const auto& x:full) {
      Spectrum c{};
      for(int k=0;k<32;++k) c[k]=static_cast<std::int16_t>(x.autocorrelation[k]);
      distinct.insert(c);
    }
    require(!distinct.empty(),"empty lift fiber");
    words+=full.size();spectra+=distinct.size();out.assign(distinct.begin(),distinct.end());
  }
  std::cerr<<"generated "<<rows.size()<<" row sets, "<<words<<" words, "<<spectra<<" spectra\n";
  for(std::size_t qi=0;qi<n;++qi) {
    std::array<const std::vector<Spectrum>*,4> v{};
    for(int j=0;j<4;++j) v[j]=&rows.at(qs[qi][j]);
    std::array<int,4> ix{0,1,2,3};
    std::sort(ix.begin(),ix.end(),[&](int a,int b){return std::make_pair(v[a]->size(),a)<std::make_pair(v[b]->size(),b);});
    int a=ix[0],b=ix[3],c=ix[1],d=ix[2];
    if(v[a]->size()*v[b]->size()>v[c]->size()*v[d]->size()) {std::swap(a,c);std::swap(b,d);}
    std::unordered_set<Spectrum,SpectrumHash> table;
    table.reserve(v[a]->size()*v[b]->size());
    for(const auto& x:*v[a]) for(const auto& y:*v[b]) {
      Spectrum k{};for(int j=0;j<32;++j) k[j]=static_cast<std::int16_t>(x[j]+y[j]);
      table.insert(k);++pairs;
    }
    keys+=table.size();
    for(const auto& x:*v[c]) for(const auto& y:*v[d]) {
      Spectrum k{};for(int j=0;j<32;++j) k[j]=static_cast<std::int16_t>(-4-x[j]-y[j]);
      require(!table.contains(k),"compatible reversible full-lag tuple found");++pairs;
    }
    if((qi+1)%1024==0) std::cerr<<"checked "<<qi+1<<"/"<<n<<" parents\n";
  }
  std::cout<<"{\"multiplier\":63,\"parents\":"<<n<<",\"distinct_rows\":"<<rows.size()
    <<",\"full_words\":"<<words<<",\"distinct_row_spectra\":"<<spectra
    <<",\"spectrum_pairs\":"<<pairs<<",\"stored_keys\":"<<keys
    <<",\"witnesses\":0,\"status\":\"PASS\"}\n";
  return 0;
}
