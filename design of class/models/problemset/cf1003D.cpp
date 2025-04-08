/*Codeforces Round 1003 (Div. 4) D
构式long long... 
前缀和以及前缀和的前缀和 贪心从大到小排一遍前缀和的前缀和 然后数学分析一下每个下标对应的系数
前缀和直接优化进读取里面去 数组记得开long long...
*/
#include<bits/stdc++.h>
using namespace std;
int main(){
    // freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int t; cin >> t;
    while(t--){
        int n, m;
        long long rst = 0;
        cin >> m >> n;
        vector<long long> linesum(m);
        for(int i = 0; i < m; i++){
            for(int j= 0; j < n; j++){
                int zc;
                scanf("%d", &zc);
                linesum[i] += zc;
                rst += linesum[i];
            }
        }
        sort(linesum.begin(), linesum.end(),greater<long long>());
        for(int i=0 ; i < m; i++){
            rst += linesum[i] * n * (m - 1 - i);
        }
        printf("%lld\n", rst);
    }
    return 0;
}