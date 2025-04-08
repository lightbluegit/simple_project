/*计算陆地周长*/
#include<bits/stdc++.h>
using namespace std;
int dir[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int row, col;
    cin >> row >> col;
    vector<vector<int>>grid(row, vector<int>(col, 0));
    for(int i = 0; i < row; i++){
        for(int j = 0; j < col; j++){
            scanf("%d", &grid[i][j]);
        }
    }
    int edge_cnt = 0;
    for(int i = 0; i < row; i++){
        for(int j = 0; j < col; j++){
            if(grid[i][j]){//找到陆地
                for(int k = 0; k < 4; k++){//四向探索 除了遇到陆地都将周长+1
                    if(i + dir[k][0] && i + dir[k][0] < row && j + dir[k][1] && j + dir[k][1] < col && grid[i + dir[k][0]][j + dir[k][1]]){continue;}
                    edge_cnt++;
                }
            }
        }
    }
    cout << edge_cnt;
    return 0;
}
/*
5 5
0 0 0 0 0
0 1 0 1 0
0 1 1 1 0
0 1 1 1 0
0 0 0 0 1

ans:18
*/