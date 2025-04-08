/*给定不同面额的硬币和一个总金额。写出函数来计算可以凑成总金额的硬币组合数。假设每一种面额的硬币有无限个*/
#include<bits/stdc++.h>
using namespace std;
int dir[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    //dp[i] = j 有j种方法可以装满重量为i的背包
    int n, aim;
    cin >> n >> aim;
    vector<int>coin(n), dp(aim + 1);
    for(int i = 0; i < n; i++){
        cin >> coin[i];
    }
    //递推公式 dp[i] = dp[i] + dp[i - coin[j]]不装 + 装
    dp[0] = 1;//初始化 有1种情况可以装满重量为0的背包(不装东西)
    for(int i = 0; i < n; i++){//先物品后重量的是组合数 先重量后物品的是排列数
        for(int j = coin[i]; j <= aim; j++){
            dp[j] += dp[j - coin[i]];
        }
    }
    for(const auto& i:dp){
        cout << i << ' ';
    }
    // cout << dp[aim];
    return 0;
}
/*
3 4
1 2 3

1 1 2 3 4
1 1 2 4 7)
ans:4
*/