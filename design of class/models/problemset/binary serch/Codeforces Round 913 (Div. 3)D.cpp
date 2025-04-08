/*Codeforces Round 913 (Div. 3)D. Jumping Through Segments
二分答案法
维护一个能到达的区域区间 画两条线 ll = max(ll - k, l[i]); rr = min(rr + k, r[i]); [ll, rr]就是必定能到达的区域 在这个区域之上再拓展k就是下一步可以到达的区域 再尝试与下一个区间相交 如果为空 该k就无解 否则继续找最小有解的k
*/
#include<bits/stdc++.h>
using namespace std;
int min(int a, int b){return a<b?a:b;}
int max(int a, int b){return a>b?a:b;}
bool check(int k,const vector<int>& l,const vector<int>& r){
    int ll = 0, rr = 0;
    for(int i = 0; i < l.size(); i++){
        ll = max(ll - k, l[i]);
        rr = min(rr + k, r[i]);
        if(ll > rr){return false;}
    }
    return true;
}
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int t; cin >> t;
    while(t--){
        int n; cin >> n;
        vector<int>l(n), r(n);
        int ll,rr;
        for(int i = 0;i < n; i++){
            scanf("%d %d", &l[i], &r[i]);
            ll = min(ll, l[i]);
            rr = max(rr, r[i]);
        }
        int rst = 0;
        while(ll <= rr){
            int mid = ll + ((rr - ll) >> 1);
            if(check(mid, l, r)){
                rst = mid;
                rr = mid - 1;
            }
            else{
                ll = mid + 1;
            }
        }
        printf("%d\n", rst);
    }
    return 0;
}
/*
4
5
1 5
3 4
5 6
8 10
0 1
3
0 2
0 1
0 3
3
3 8
10 18
6 11
4
10 20
0 5
15 17
2 2

ans:
7
0
5
13

*/