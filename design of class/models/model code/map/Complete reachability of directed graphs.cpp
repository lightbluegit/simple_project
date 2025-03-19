#include<bits/stdc++.h>
using namespace std;
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int n, k;
    cin >> n >> k;
    vector<list<int>>line(n + 1);
    for(int i = 0; i < k; i++){
        int zc, zcline;
        scanf("%d %d", & zc, & zcline);
        line[zc].push_back(zcline);
    }
    vector<bool>visited(n + 1, false);
    queue<int>qu;
    qu.push(1);
    visited[1] = true;
    while(!qu.empty()){
        int size = qu.size();
        for(int i = 0; i < size; i++){
            int cur = qu.front(); qu.pop();
            list<int>curline = line[cur];
            for(const auto& j:curline ){
                if(!visited[j]){
                    visited[j] = true;
                    qu.push(j);
                }
            }
        }
    }
    bool pd = true;
    for(int i = 1; i <= n; i++){
        if(!visited[i]){
            cout << "-1";
            break;
        }
    }
    if(pd){
        cout << 1;
    }
    return 0;
}
/*
4 4
1 2
2 1
1 3
2 4
*/