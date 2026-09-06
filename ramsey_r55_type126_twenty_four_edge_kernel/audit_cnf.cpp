// Literal five-set audit. Input is every pair in the full universe;
// only the first active vertices generate constraints. No producer import.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
int main(int argc,char**argv){try{
    if(argc!=5)throw std::runtime_error("usage: audit_cnf ORDER ACTIVE MATRIX OUTPUT");
    std::size_t consumed=0;
    const std::string ns(argv[1]),ks(argv[2]);
    const int n=std::stoi(ns,&consumed);
    if(consumed!=ns.size())throw std::runtime_error("order parse");
    const int active=std::stoi(ks,&consumed);
    if(consumed!=ks.size()||active<5||active>n||n>43)throw std::runtime_error("order bounds");
    std::ifstream in(argv[3]);std::array<std::array<int,43>,43> color{},variable{};int nv=0;
    for(int u=0;u<n;u++)for(int v=u+1;v<n;v++){
        char ch;if(!(in>>ch)||ch<'0'||ch>'2')throw std::runtime_error("invalid physical matrix");
        color[u][v]=ch-'0';if(ch=='2')variable[u][v]=++nv;
    }
    char extra;if(in>>extra)throw std::runtime_error("extra matrix input");
    std::vector<std::vector<int>> clauses;
    for(int a=0;a<active-4;a++)for(int b=a+1;b<active-3;b++)
    for(int c=b+1;c<active-2;c++)for(int d=c+1;d<active-1;d++)for(int e=d+1;e<active;e++){
        std::array<int,5> q{a,b,c,d,e};bool fixed_red=false,fixed_blue=false;std::vector<int> vars;
        for(int i=0;i<5;i++)for(int j=i+1;j<5;j++){
            int u=q[i],v=q[j];fixed_red|=color[u][v]==1;fixed_blue|=color[u][v]==0;
            if(color[u][v]==2)vars.push_back(variable[u][v]);
        }
        if(!fixed_red)clauses.push_back(vars);
        if(!fixed_blue){for(auto&x:vars)x=-x;clauses.push_back(vars);}
    }
    std::sort(clauses.begin(),clauses.end());clauses.erase(std::unique(clauses.begin(),clauses.end()),clauses.end());
    std::ofstream out(argv[4]);if(!out)throw std::runtime_error("output open failed");
    out<<"p cnf "<<nv<<' '<<clauses.size()<<'\n';
    for(const auto& row:clauses){for(int x:row)out<<x<<' ';out<<"0\n";}
    if(!out)throw std::runtime_error("output write failed");
    return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
