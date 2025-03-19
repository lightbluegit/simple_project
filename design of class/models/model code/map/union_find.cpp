//并查集模版
#include<bits/stdc++.h>
using namespace std;

void init_set(vector<int>& father_vec){
    for(int i = 1; i < father_vec.size(); i++){
        father_vec[i] = i;
    }
}

int find_father(int son, vector<int>& father_vec){//找根
    return father_vec[son] == son ? son : father_vec[son] = find_father(father_vec[son], father_vec);//赋值表达式的返回值是右值
}

void join(int x, int y, vector<int>& father_vec){//将一对数加入并查集
    x = find_father(x, father_vec);
    y = find_father(y, father_vec);
    if(x == y) return;
    father_vec[x] = y;
}

bool is_same_root(int x, int y, vector<int>& father_vec){
    return find_father(x, father_vec) == find_father(y, father_vec);
}

int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int nodecnt, edgecnt;
    cin >> nodecnt >> edgecnt;
    vector<int> father_vec(edgecnt + 1);//1 ~ n
    init_set(father_vec);
    for(int i = 0; i < edgecnt; i++){
        int son, father;
        scanf("%d %d", &son, &father);
        join(son, father, father_vec);
    }
    int st, ed;
    cin >> st >> ed;
    cout << is_same_root(st, ed, father_vec);
    return 0;
}
/*
5 4
1 2
1 3
2 4
3 4
1 4
*/