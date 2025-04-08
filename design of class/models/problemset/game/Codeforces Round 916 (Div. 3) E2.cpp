/*Codeforces Round 916 (Div. 3) E2. Game with Marbles
game
两人有ai, bi 张不同种类的牌 轮流操作(A先手) 指定某一堆牌 自己数量-1 对手清0 直到过完n张牌 剩下的A-B(牌数)是多少
每次操作的价值为:清除对方ai张牌 保下自己bi - 1张牌 因此贪心来看 对ai+bi排序从大到小轮流取就行 带入样例四可知ai+bi相等的情况下顺序不影响结果
*/
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int t; cin >> t;
    while (t--)
    {
        int n; cin >> n;
        vector<int>a(n), b(n);
        vector<pair<ll, int>>sum(n);//val, idx
        for(int i = 0; i < n ;i++){
            scanf("%d", &a[i]);
        }
        for(int i = 0; i < n ;i++){
            scanf("%d", &b[i]);
            sum[i] = make_pair(a[i] + b[i], i);
        }
        sort(sum.begin(), sum.end(), 
        [](const pair<ll, int>& a, const pair<ll, int>& b) {
            return a.first > b.first;
        });
        ll rst = 0;
        for(int i = 0; i < n; i++){
            int idx = sum[i].second;
            if(i & 1){
                rst -= b[idx] - 1;
            }
            else{
                rst += a[idx] - 1;
            }
        }
        cout << rst << "\n";
    }
    return 0;
}
/*
5
3
4 2 1
1 2 4
4
1 20 1 20
100 15 10 20
5
1000000000 1000000000 1000000000 1000000000 1000000000
1 1 1 1 1
3
5 6 5
2 1 7
6
3 2 4 2 5 5
9 4 7 9 2 5

ans:
1
-9
2999999997
8
-6

*/