// Invoke the production row function; the separate Python checker enumerates
// every bounded folding assignment and compares the full row sets.
#define main unused_production_main
#include "lift_match.cpp"
#undef main
#include <algorithm>
template<int N> void emit(std::ifstream& in,std::ofstream& out,int kind,int cap){
 Row<N/2> p{};for(int& v:p)require(bool(in>>v),"row");
 auto rows=lifts<N>(p,kind,cap);std::vector<std::uint64_t> codes;
 for(const auto& row:rows){std::uint64_t word=0;for(int v:row)word=word*static_cast<unsigned>(64/N+1)+static_cast<unsigned>(v+32/N);codes.push_back(word);}
 std::sort(codes.begin(),codes.end());require(std::adjacent_find(codes.begin(),codes.end())==codes.end(),"duplicate row");
 out<<codes.size();for(auto word:codes)out<<' '<<word;out<<'\n';
}
int main(int argc,char** argv){require(argc==3,"input output");std::ifstream in(argv[1]);std::ofstream out(argv[2]);int count=0;require(bool(in>>count),"case count");
 for(int j=0;j<count;++j){int n=0,kind=0,cap=0;require(bool(in>>n>>kind>>cap),"case header");
  if(n==8)emit<8>(in,out,kind,cap);else if(n==16)emit<16>(in,out,kind,cap);else if(n==32)emit<32>(in,out,kind,cap);else throw std::runtime_error("length");
 }std::string extra;require(!(in>>extra),"trailing data");return 0;
}
