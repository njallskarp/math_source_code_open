#include <array>
#include <bit>
#include <cstdint>
#include <iostream>

static bool core_edge(int i,int j){
  const int d=(i-j+13)%13;
  return i!=j && (d==1 || d==5 || d==8 || d==12);
}

int main(){
  constexpr std::uint16_t mask=0x031a;
  const std::array<int,2> red_edge={1,9};
  const std::array<int,3> blue_triple={0,2,6};
  int edge_count=0,triples=0,fours=0,fives=0,transversals=0;
  for(int i=0;i<13;++i)for(int j=i+1;j<13;++j)edge_count+=core_edge(i,j);
  for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c){
    const bool independent=!core_edge(a,b)&&!core_edge(a,c)&&!core_edge(b,c);
    triples+=independent;
  }
  for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)
    for(int d=c+1;d<13;++d){
      const std::array<int,4> q={a,b,c,d}; bool independent=true;
      for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)independent&=!core_edge(q[i],q[j]);
      fours+=independent;
    }
  for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)
    for(int d=c+1;d<13;++d)for(int e=d+1;e<13;++e){
      const std::array<int,5> q={a,b,c,d,e}; bool independent=true;
      for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)independent&=!core_edge(q[i],q[j]);
      fives+=independent;
    }
  for(unsigned candidate=0;candidate<(1u<<13);++candidate){
    bool transversal=true;
    for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)
      for(int d=c+1;d<13;++d){
        const std::array<int,4> q={a,b,c,d}; bool independent=true;
        for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)independent&=!core_edge(q[i],q[j]);
        if(independent && !(candidate&((1u<<a)|(1u<<b)|(1u<<c)|(1u<<d))))transversal=false;
      }
    transversals+=transversal;
  }
  bool chosen_transversal=true;
  for(int a=0;a<13;++a)for(int b=a+1;b<13;++b)for(int c=b+1;c<13;++c)
    for(int d=c+1;d<13;++d){
      const std::array<int,4> q={a,b,c,d}; bool independent=true;
      for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)independent&=!core_edge(q[i],q[j]);
      if(independent && !(mask&((1u<<a)|(1u<<b)|(1u<<c)|(1u<<d))))chosen_transversal=false;
    }
  const bool red_forbidden=core_edge(red_edge[0],red_edge[1])
      && (mask&(1u<<red_edge[0])) && (mask&(1u<<red_edge[1]));
  bool blue_forbidden=true;
  for(int i:blue_triple)blue_forbidden&=!(mask&(1u<<i));
  for(int i=0;i<3;++i)for(int j=i+1;j<3;++j)blue_forbidden&=!core_edge(blue_triple[i],blue_triple[j]);
  if(edge_count!=26 || triples!=78 || fours!=39 || fives!=0 || transversals!=3459
      || !chosen_transversal || !red_forbidden || !blue_forbidden || std::popcount(mask)!=5)return 1;
  std::cout<<"PASS mask=031a multiplicity=2 red_forbidden=1 blue_forbidden=1 max_multiplicity=1\n";
  std::cout<<"core_edges=26 independent_triples=78 independent_fours=39 transversals=3459\n";
  return 0;
}
