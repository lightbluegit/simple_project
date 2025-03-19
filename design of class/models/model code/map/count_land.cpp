#include<bits/stdc++.h>
using namespace std;
int dir[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
void dfs(int x, int y, vector<vector<int>>& ma, vector<vector<int>>& visited){
    for(int i = 0; i < 4; i++){
        int dx = dir[i][0], dy = dir[i][1];
        if(x + dx < 0 || x + dx >= ma.size() || y + dy < 0 || y + dy >= ma[0].size() || (ma[x + dx][y + dy] == 1 && visited[x + dx][y + dy] == 1) || ma[x + dx][y + dy] == 0) continue;
        x += dx, y += dy;
        visited[x][y] = 1;
        dfs(x, y, ma, visited);
        x -= dx, y -= dy;
    }
}

void bfs(int x, int y, vector<vector<int>>& ma, vector<vector<int>>& visited){
    visited[x][y] = 1;
    queue<pair<int, int>> qu;
    pair<int, int>cur(x, y);
    qu.push(cur);//当前区域入队
    while(!qu.empty()){
        int size = qu.size();
        pair<int,int>cur = qu.front();
        qu.pop();
        x = cur.first, y = cur.second;
        for(int i = 0; i < 4; i++){
            int dx = dir[i][0], dy = dir[i][1];
            if(x + dx < 0 || x + dx >= ma.size() || y + dy < 0 || y + dy >= ma[0].size() || (ma[x + dx][y + dy] == 1 && visited[x + dx][y + dy] == 1) || ma[x + dx][y + dy] == 0) continue;
            x += dx; y += dy;
            visited[x][y] = 1;
            qu.push(make_pair(x, y));
            x -= dx, y -= dy;
        }
    }
}

int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int row, col;
    cin >> row >> col;
    vector<vector<int>> ma(row, vector<int>(col)), visited(row, vector<int>(col));
    for(int i = 0; i < row; i++){
        for(int j = 0; j < col; j++){
            scanf("%d", &ma[i][j]);
        }
    }
    int rst = 0;
    for(int i = 0; i < row; i++){
        for(int j = 0; j < col; j++){
            if(ma[i][j] == 1 && visited[i][j] == 0){
                bfs(i, j, ma, visited);
                // dfs(i, j, ma, visited);
                rst++;
            }
        }
    }
    cout << rst;
    return 0;
}
/*
4 5
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
*/