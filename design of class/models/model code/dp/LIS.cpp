/*最长递增子序列*/
#include<bits/stdc++.h>
using namespace std;
int max(int a, int b){return a>b ? a:b;}
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    //dp[i] = j 有j种方法可以爬i阶
    int n;
    cin >> n;
    vector<int>num(n), dp(n, 1);//dp[i] = j 以第i个数字结尾的最长递增子序列长度为j
    for(int i = 0;i < n; i++){
        scanf("%d", &num[i]);
    }
    for(int i = 1; i < n; i++){
        for(int j = 0; j < i; j++){
            if(num[i] > num[j]){//递增
                dp[i] = max(dp[i], dp[j] + 1);//最长
            }
        }
    }
    int rst = 0;
    for(const auto& i:dp){
        rst = max(rst, i);
        cout << i << ' ';
    }
    cout << "rst=" << rst;
    // cout << dp[m];
    return 0;
}
/*
8
10 9 2 5 3 7 101 18
ans:4
*/