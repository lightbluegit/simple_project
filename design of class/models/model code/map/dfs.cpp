//输出从起点到终点的所有路径
#include<bits/stdc++.h>
using namespace std;
vector<vector<int>> result; // 收集符合条件的路径
vector<int> path; // 1节点到终点的路径

void dfs (const vector<list<int>>& graph, int x, int n) {
    if (x == n) { // 找到符合条件的一条路径
        result.push_back(path);
        return;
    }
    for (int i : graph[x]) { // 找到 x指向的节点
        path.push_back(i); // 遍历到的节点加入到路径中来
        dfs(graph, i, n); // 进入下一层递归
        path.pop_back(); // 回溯，撤销本节点
    }
}

int main() {
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int n, m, s, t;
    cin >> n >> m;
    // 节点编号从1到n，所以申请 n+1 这么大的数组
    vector<list<int>> graph(n + 1); // 邻接表写法
    while (m--) {
        cin >> s >> t;
        graph[s].push_back(t);// 使用邻接表 ，表示 s -> t 是相连的
    }
    path.push_back(1); // 无论什么路径已经是从0节点出发
    dfs(graph, 1, n); // 开始遍历

    if (result.size() == 0) cout << -1 << endl;
    for (const vector<int> &pa : result) {
        for (int i = 0; i < pa.size() - 1; i++) {
            cout << pa[i] << " ";
        }
        cout << pa[pa.size() - 1]  << endl;
    }
}
/*
6
2 7 4 1 8 1

graph存储数据:
1:3->2
2:4
3:5
4:5
5:
*/
/*邻接矩阵
void dfs (const vector<vector<int>>& graph, int x, int n) {
    if (x == n) { // 找到符合条件的一条路径
        result.push_back(path);
        for(const auto& i : path){
            cout << i << ' ';
        }
        cout << endl;
        return;
    }
    for(int i = 0; i < graph[x].size(); i++){
        if(graph[x][i]){
            path.push_back(i);
            dfs(graph, i, n);
            path.pop_back();
        }
    }
}

int main() {
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int n, m, s, t;
    cin >> n >> m;

    // 节点编号从1到n，所以申请 n+1 这么大的数组
    vector<vector<int>> graph(n + 1, vector<int>(n + 1)); // 邻接矩阵
    while (m--) {
        cin >> s >> t;
        graph[s][t] = 1;
    }
    path.push_back(1); // 无论什么路径已经是从0节点出发
    dfs(graph, 1, n); // 开始遍历
}
*/