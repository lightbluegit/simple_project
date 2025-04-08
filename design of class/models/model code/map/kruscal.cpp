/*kruscal最小生成树算法 维护的是边*/
#include<bits/stdc++.h>
using namespace std;

struct edge
{
    int l,r,edge_val;
};

void init(vector<int>& father){
    for(int i = 1; i < father.size(); i++) father[i] = i;
}

int find_root(int x, vector<int>& father){
    return x == father[x] ? x : father[x] = find_root(father[x], father);
}

void join(int x, int y, vector<int>& father){
    x = find_root(x, father);
    y = find_root(y, father);
    if(x == y) return;
    father[x] = y;
}

int main() {
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int node_cnt, edge_cnt, x, y, k;
    cin >> node_cnt >> edge_cnt;
    vector<edge>edg, path;
    vector<int>father(node_cnt + 1);
    for(int i = 0; i < edge_cnt; i++){
        cin >> x >> y >> k;
        edg.push_back({x, y, k});
    }
    sort(edg.begin(), edg.end(), 
        [](const edge& a, const edge& b) {//捕获列表（此处为空，表示不捕获任何外部变量） 参数列表
            return a.edge_val < b.edge_val;// < 就是从小到大
    });
    // for(const auto& i : edg){
    //     cout << i.l << '-' << i.r << endl;
    // }
    init(father);
    for(auto& edgi : edg){
        if(find_root(edgi.l, father) != find_root(edgi.r, father)){
            join(edgi.l, edgi.r, father);
            path.push_back(edgi);
        }
    }
    for(const auto& i : path){
        printf("%d->%d:%d\n", i.l, i.r, i.edge_val);
    }
    return 0;
}
/*
7 11
1 2 1
1 3 1
1 5 2
2 6 1
2 4 2
2 3 2
3 4 1
4 5 1
5 6 2
5 7 1
6 7 1

1->2:1
1->3:1
2->6:1
3->4:1
4->5:1
5->7:1
*/