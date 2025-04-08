/*Codeforces Round 941 (Div. 1) A. Everything Nim
博弈论 找到必赢状态 多举几个例子 尝试分析关系
一堆石子分为2种状态 1个和多个 1个的话只能强制拿1个 多个的话可以选择拿到只剩1个或全拿走 也就意味着当前的人可以第一手处理每一堆石子(每次都只剩下1个石子让对方拿) 处于必赢状态 因此谁先到达这个点谁就赢 但是如果每堆石子的数量组成了全排列 那么双方都只能拿1个石子 看的是石头堆数
*/
#include<bits/stdc++.h>
using namespace std;
int max(int a, int b){return a > b ? a : b;}
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int t; cin >> t;
    while(t--){
        int n; cin >> n;
        set<int>num;
        int maxx = 0;
        for(int i = 0; i < n; i++){
            int zc;
            scanf("%d", &zc);
            num.insert(zc);//一次消掉一堆 set去重+排序
            maxx = max(maxx, zc);
        }
        // for(auto i : num){
        //     cout << i << ' ';
        // }
        // cout << endl;
        if(n == 1){
            printf("Alice\n");
            continue;
        }
        int mex = 1;
        for(const auto& i : num){
            if(i == mex){
                mex++;
            }
            else{
                break;
            }
        }
        if(mex > maxx){
            if(maxx & 1){
                printf("Alice\n");
            }
            else{
                printf("Bob\n");
            }
        }
        else{
            if(mex & 1){
                printf("Alice\n");
            }
            else{
                printf("Bob\n");
            }
        }
    }
    return 0;
}
/*
7
5
3 3 3 3 3
2
1 7
7
1 3 9 7 4 2 100
3
1 2 3
6
2 1 3 4 2 4
8
5 7 2 9 6 3 3 2
1
1000000000

ans:
Alice
Bob
Alice
Alice
Bob
Alice
Alice

*/