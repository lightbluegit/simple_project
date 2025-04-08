/*给两个整数数组 A 和 B ，返回两个数组中公共的、长度最长的子数组的长度*/
#include<bits/stdc++.h>
using namespace std;
int max(int a, int b){return a>b ? a:b;}
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int n; cin >> n;
    vector<int>num1(n),num2(n);
    vector<vector<int>>dp(n + 1, vector<int>(n + 1, 0));//dp[i][j] = k 以下标i-1结尾和以j-1结尾的子序列的最长重合为k
    for(int i = 0;i < n; i++){
        scanf("%d", &num1[i]);
    }
    for(int i = 0;i < n; i++){
        scanf("%d", &num2[i]);
    }
    int rst = 0;
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= n; j++){
            if(num1[i - 1] == num2[j - 1]){
                dp[i][j] = dp[i - 1][j - 1] + 1;
            }
            rst = max(rst, dp[i][j]);
        }
    }
    cout << rst;
    return 0;
}
/*
5
1 2 3 2 1
3 2 1 4 7
ans:3
*/