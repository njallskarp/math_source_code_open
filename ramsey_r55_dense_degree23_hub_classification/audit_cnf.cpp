// Literal five-set enumeration from an independently reconstructed physical matrix.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
int main(int argc,char**argv){try{
    if(argc!=3)throw std::runtime_error("usage: audit_cnf MATRIX OUTPUT");
    std::ifstream in(argv[1]);std::array<std::array<int,43>,43> color{},variable{};int nv=0;
    for(int u=0;u<43;u++)for(int v=u+1;v<43;v++){
        char ch;if(!(in>>ch)||ch<'0'||ch>'2')throw std::runtime_error("invalid physical matrix");
        color[u][v]=ch-'0';if(ch=='2')variable[u][v]=++nv;
    }
    char extra;if(in>>extra)throw std::runtime_error("extra matrix input");
    std::vector<std::vector<int>> clauses;
    for(int a=0;a<39;a++)for(int b=a+1;b<40;b++)for(int c=b+1;c<41;c++)for(int d=c+1;d<42;d++)for(int e=d+1;e<43;e++){
        std::array<int,5> q{a,b,c,d,e};bool fixed_red=false,fixed_blue=false;std::vector<int> vars;
        for(int i=0;i<5;i++)for(int j=i+1;j<5;j++){
            int u=q[i],v=q[j];fixed_red|=color[u][v]==1;fixed_blue|=color[u][v]==0;
            if(color[u][v]==2)vars.push_back(variable[u][v]);
        }
        if(!fixed_red)clauses.push_back(vars);
        if(!fixed_blue){for(auto&x:vars)x=-x;clauses.push_back(vars);}
    }
    std::sort(clauses.begin(),clauses.end());clauses.erase(std::unique(clauses.begin(),clauses.end()),clauses.end());
    std::ofstream out(argv[2]);if(!out)throw std::runtime_error("output open failed");
    out<<"p cnf "<<nv<<' '<<clauses.size()<<'\n';
    for(const auto& row:clauses){for(int x:row)out<<x<<' ';out<<"0\n";}
    if(!out)throw std::runtime_error("output write failed");
    return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
