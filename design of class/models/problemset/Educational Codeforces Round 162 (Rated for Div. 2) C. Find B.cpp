/*Educational Codeforces Round 162 (Rated for Div. 2) C. Find B
数学题
是否可以找到一个序列使得其所有元素之和等于询问的子串的所有元素之和并且每位的数都不一样(都是正数)
如果某一位的数>1那么就可以拆成1和x-1 分别加在不同地方 但是如果x==1就只能变成其他的数 最小的可能就是2 而>1的数都变成1就可以了 多出来的部分随便放在一个数的位置都可以使其成为不同的序列
*/
#include<bits/stdc++.h>
using namespace std;
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int t; cin >> t;
    while (t--)
    {
        int n, q; cin >> n >> q;
        vector<int>cnt(n + 1);
        vector<long long>sum(n + 1);
        for(int i = 1; i <= n; i++){
            int zc;
            scanf("%d", &zc);
            if(zc == 1){
                cnt[i] = cnt[i - 1] + 1;
            }
            else{
                cnt[i] = cnt[i - 1];
            }
            sum[i] = sum[i - 1] + zc;
        }
        for(int i = 0; i < q; i++){
            int l, r;
            scanf("%d %d", &l, &r);
            if(l == r){
                printf("NO\n");
                continue;
            }
            int cnt1 = cnt[r] - cnt[l - 1];
            long long need_sum = cnt1 + (r - l + 1), actu_sum = sum[r] - sum[l - 1];
            if(need_sum <= actu_sum){
                printf("YES\n");
            }
            else{
                printf("NO\n");
            }
        }
    }
    return 0;
}
/*
1
5 4
1 2 1 4 5
1 5
4 4
3 4
1 3

ans:
YES
NO
YES
NO
*/