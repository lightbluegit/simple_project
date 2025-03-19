/*prim最小生成树算法 维护的是节点*/
#include<bits/stdc++.h>
using namespace std;
int main() {
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int node, edge, x, y, k;
    cin >> node >> edge;
    vector<vector<int>> grid(node + 1, vector<int>(node + 1, 10001));
    for(int i = 0; i < edge; i++){
        cin >> x >> y >> k;
        grid[x][y] = k;
        grid[y][x] = k;
    }
    vector<bool>is_in_tree(node + 1, false);
    vector<int>mindis(node + 1, 10002), path(node + 1, -1);//mindis[i]=j i到最小生成树的最短距离是j
    for(int i = 0; i < node; i++){//每一轮将一个数字加入最小生成树
        int cur = -1;//选择哪个数加入最小生成树
        int min_val = 10003;//目前选中的节点到最小生成树的最短距离
        for(int j = 1; j <= node; j++){//遍历所有节点(默认标号1~n)
            if(!is_in_tree[j] && mindis[j] < min_val){//寻找不在树上且距离比现有距离更短的节点(minval的初始值必须大于mindis的初始值 这样初始状态才可以选中1节点)
                min_val = mindis[j];//更新
                cur = j;
            }
        }
        is_in_tree[cur] = true;//将选中的节点加入最小生成树
        for(int j = 1; j <= node ;j++){//再次遍历节点
            if(!is_in_tree[j] && grid[cur][j] < mindis[j]){//寻找不在树上且到最后加入的节点(同时也是最小生成树)的距离比记录更短的节点
                mindis[j] = grid[cur][j];//更新mindis数组
                path[j] = cur;//只能是path[j] = cur 不能写反了
            }
        }
    }
    for(int i = 1; i <= node; i++){
        cout << i << ' ' << path[i] << "\n";
    }
    cout << endl;
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
*/