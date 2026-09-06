// Independent literal 21-bit census; no producer data or structural buckets.
#include <array>
#include <cstdint>
#include <iostream>
int main() {
    std::array<int,21> left{},right{};
    int k=0;
    for(int i=0;i<7;++i) for(int j=i+1;j<7;++j) {
        left[k]=i;right[k]=j;++k;
    }
    for(std::uint32_t mask=0;mask<(std::uint32_t{1}<<21);++mask) {
        bool a[7][7]={};
        for(int bit=0;bit<21;++bit) if((mask>>bit)&1U)
            a[left[bit]][right[bit]]=a[right[bit]][left[bit]]=true;
        int sum=0;bool good=true;
        for(int v=0;v<7;++v) {
            int weighted=0;
            for(int u=0;u<7;++u) if(a[v][u]) weighted += u<2 ? 2 : 1;
            int slack=weighted-(v<2 ? 5 : 4);
            if(slack<0) { good=false;break; }
            sum+=slack;
        }
        if(!good || sum>2) continue;
        for(int i=0;i<7 && good;++i)
        for(int j=i+1;j<7 && good;++j)
        for(int h=j+1;h<7 && good;++h)
        for(int l=h+1;l<7 && good;++l)
        for(int m=l+1;m<7 && good;++m) {
            int vs[5]={i,j,h,l,m};int edges=0;
            for(int u=0;u<5;++u) for(int v=u+1;v<5;++v) edges+=a[vs[u]][vs[v]];
            if(edges==0 || edges==10) good=false;
        }
        if(good) std::cout<<mask<<"\n";
    }
}
