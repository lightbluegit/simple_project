/*拓扑排序*/
#include<bits/stdc++.h>
using namespace std;
int main() {
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int node_cnt, edge_cnt;
    cin >> node_cnt >> edge_cnt;
    vector<int> path, indegree(node_cnt);//indegree入度
    vector<vector<int>>ma(node_cnt);
    for(int i = 0; i < edge_cnt; i++){
        int x, y;
        scanf("%d %d", &x, &y);
        ma[x].push_back(y);//x -> y
        indegree[y]++;//记录入度
    }
    queue<int>zero;//0入度的点
    for(int i = 0; i < node_cnt; i++){
        if(!indegree[i]){
            zero.push(i);
        }
    }
    while(zero.size()){
        int cur = zero.front(); zero.pop();
        path.push_back(cur);
        vector<int> zc = ma[cur];//当前点的连接点入度-1
        for(auto& i : zc){
            if(! --indegree[i]){
                zero.push(i);
            }
        } 
    }
    if(path.size() == node_cnt) {
        for (const auto& i :path){
            cout << i << " ";
        }
    }
    else{ 
        cout << -1 << endl;
    }
    return 0;
}
/*
5 4
0 1
0 2
1 3
2 4
*/