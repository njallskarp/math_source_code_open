// Independent exact-sum36 full labeled C4-pair decomposition; no orbit pruning.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Mask=std::uint32_t;
using Word=std::uint64_t;
using Bits=std::vector<Word>;
constexpr Mask ALL=(1U<<17)-1;
std::array<Mask,17> red{};
std::vector<Mask> edges,triangles,bluepairs,bluetriples,cols;
std::vector<int> weight;
std::vector<Bits> R,B;
std::array<Bits,9> at_least;
std::size_t words;
bool contains(Mask m,const std::vector<Mask>& family){
    for(auto q:family)if((m&q)==q)return true;
    return false;
}
void grow(int next,Mask m){
    if(std::popcount(m)>=4)cols.push_back(m);
    for(int v=next;v<17;v++){
        if(!contains(m&red[v],edges))grow(v+1,m|(1U<<v));
    }
}
std::vector<int> entries(const Bits& b){
    std::vector<int> ans;
    for(std::size_t w=0;w<b.size();w++){
        Word x=b[w];while(x){int bit=std::countr_zero(x);x&=x-1;ans.push_back(static_cast<int>(64*w)+bit);}
    }
    return ans;
}
Bits intersection(const Bits& x,const Bits& y){
    Bits z(words);for(std::size_t w=0;w<words;w++)z[w]=x[w]&y[w];return z;
}
int main(int argc,char**argv){try{
    if(argc!=3)throw std::runtime_error("usage: audit_dense TYPE OUTPUT");
    std::size_t end=0;const std::string argument(argv[1]);
    const int kind=std::stoi(argument,&end);if(end!=argument.size()||kind!=62)throw std::runtime_error("invalid type");
    std::array<bool,17> square{};for(int x=1;x<17;x++)square[(x*x)%17]=true;
    for(int u=0;u<17;u++)for(int v=u+1;v<17;v++){
        Mask pair=(1U<<u)|(1U<<v);
        if(square[v-u]){red[u]|=1U<<v;red[v]|=1U<<u;edges.push_back(pair);}else bluepairs.push_back(pair);
    }
    for(int a=0;a<17;a++)for(int b=a+1;b<17;b++)for(int c=b+1;c<17;c++){
        Mask m=(1U<<a)|(1U<<b)|(1U<<c);
        if(!contains(m,edges))bluetriples.push_back(m);
    }
    grow(0,0);std::sort(cols.begin(),cols.end());
    if(std::adjacent_find(cols.begin(),cols.end())!=cols.end())throw std::runtime_error("duplicate column");
    int largest=0;for(auto m:cols){weight.push_back(std::popcount(m));largest=std::max(largest,std::popcount(m));}
    if(largest!=8)throw std::runtime_error("unexpected domain");
    words=(cols.size()+63)/64;R.assign(cols.size(),Bits(words));B=R;
    for(auto& a:at_least)a.assign(words,0);
    for(std::size_t i=0;i<cols.size();i++){
        for(int k=0;k<=weight[i];k++)at_least[k][i/64]|=1ULL<<(i%64);
        for(std::size_t j=0;j<cols.size();j++){
            if(!contains(cols[i]&cols[j],edges))R[i][j/64]|=1ULL<<(j%64);
            if(!contains(ALL^(cols[i]|cols[j]),bluetriples))B[i][j/64]|=1ULL<<(j%64);
        }
    }
    std::vector<std::array<Mask,5>> answers;
    std::uint64_t outer_pairs=0,c4_pairs=0;
    for(std::size_t a=0;a<cols.size();a++){
        int need=std::max(0,12-weight[a]);
        for(int b:entries(intersection(B[a],at_least[need]))){
            outer_pairs++;
            Bits pool=intersection(R[a],R[b]);
            Bits fifth=intersection(R[a],kind==126?R[b]:B[b]);
            if(entries(fifth).empty())continue;
            for(int c:entries(pool)){
                int need_d=std::max(0,28-weight[a]-weight[b]-weight[c]);
                if(need_d>8)continue;
                Bits ds=intersection(intersection(pool,B[c]),at_least[need_d]);
                for(int d:entries(ds)){
                    if(d<=c)continue;
                    c4_pairs++;
                    int need_e=std::max(0,36-weight[a]-weight[b]-weight[c]-weight[d]);
                    if(need_e>8)continue;
                    Bits es=intersection(intersection(intersection(fifth,B[c]),B[d]),at_least[need_e]);
                    for(int e:entries(es)){
                        if(weight[a]+weight[b]+weight[c]+weight[d]+weight[e]!=36)continue;
                        if(contains(ALL^(cols[c]|cols[d]|cols[e]),bluepairs))continue;
                        answers.push_back({cols[a],cols[b],cols[c],cols[d],cols[e]});
                        answers.push_back({cols[a],cols[b],cols[d],cols[c],cols[e]});
                    }
                }
            }
        }
    }
    std::sort(answers.begin(),answers.end());
    if(std::adjacent_find(answers.begin(),answers.end())!=answers.end())throw std::runtime_error("duplicate tuple");
    std::ofstream out(argv[2]);if(!out)throw std::runtime_error("output open failed");
    for(auto row:answers){for(int i=0;i<5;i++)out<<row[i]<<(i==4?'\n':' ');}
    if(!out)throw std::runtime_error("output write failed");
    std::cout<<"{\"type\":"<<kind<<",\"columns\":"<<cols.size()<<",\"outer_pairs\":"<<outer_pairs<<",\"c4_pairs\":"<<c4_pairs<<",\"labeled_tuples\":"<<answers.size()<<"}\n";
    return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
