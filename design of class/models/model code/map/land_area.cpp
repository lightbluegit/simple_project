#include<bits/stdc++.h>
using namespace std;
int dir[4][2] = {{1,0},{0,1},{-1,0},{0,-1}};
int rst = 0;
int bfs(int x, int y,const vector<vector<int>>& ma, vector<vector<int>>& visited){
    int row = ma.size(), col = ma[0].size(), area = 1;
    visited[x][y] = 1;
    queue<pair<int, int>>qu;
    qu.push(make_pair(x, y));
    while(!qu.empty()){
        int size = qu.size();
        for(int i = 0; i < size ;i++){
            pair<int, int>cur = qu.front();
            qu.pop();
            int x = cur.first, y = cur.second;
            // printf("基础%d %d\n", x,y);
            for(int diri = 0; diri < 4; diri++){
                x += dir[diri][0], y += dir[diri][1];
                if(x < 0 || x >= row || y < 0 || y >= col || (ma[x][y] && visited[x][y]) || !ma[x][y]) {
                    x -= dir[diri][0], y -= dir[diri][1];
                    continue;
                }
                // printf("合法%d %d\n", x,y);
                area++;
                // printf("area=%d\n",area);
                visited[x][y] = 1;
                qu.push(make_pair(x, y));
                x -= dir[diri][0], y -= dir[diri][1];
            }
        }
    }
    return area;
}

void dfs(int x, int y,const vector<vector<int>>& ma, vector<vector<int>>& visited, int area){
    int row = ma.size(), col = ma[0].size();
    visited[x][y] = 1;
    for(int i = 0; i < 4; i++){
        if(x + dir[i][0] < 0 || x + dir[i][0] >= row || y + dir[i][1] < 0 || y + dir[i][1] >= col || visited[x + dir[i][0]][y + dir[i][1]] || !ma[x + dir[i][0]][y + dir[i][1]])continue;
        visited[x + dir[i][0]][y + dir[i][1]] = 1;
        rst = max(area + 1, rst);
        dfs(x + dir[i][0], y + dir[i][1], ma, visited, area + 1);
    }
}
int max(int a, int b){return a > b ? a : b;}
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int row, col;
    cin >> row >> col;
    vector<vector<int>> ma (row, vector<int>(col)), visited(row, vector<int>(col));
    for(int i = 0;i < row; i++){
        for(int j = 0; j < col; j++){
            scanf("%d", &ma[i][j]);
        }
    }
    for(int i = 0;i < row; i++){
        for(int j = 0; j < col; j++){
            if(ma[i][j] == 1 && visited[i][j] == 0){
                // int zc = bfs(i, j, ma, visited);
                // cout << "zc=" << zc <<endl;
                rst = max(rst, bfs(i, j, ma, visited));
            }
        }
    }
    cout << "rst= "<< rst;
    return 0;
}