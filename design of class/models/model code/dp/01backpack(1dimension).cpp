#include<bits/stdc++.h>
using namespace std;
void print(const vector<int>& a){
    for(const auto& i:a){
        cout << i << ' ';
    }
    cout << "\n";
}
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int n,max_width;
    cin >> n >> max_width;
    vector<int>width(n), value(n);
    for(int i = 0; i < n; i++){
        cin >> width[i] >> value[i];
    }
    vector<int>dp(max_width + 1);//dp[i]=j 使用重量i能获得的最大价值为j 初始化dp[0]=0 包含在内
    for(int i = 0; i < n; i++){//遍历物品 顺序任意 但是必须是先遍历物品后遍历重量 否则当前状态无法包含哪个物品已经被使用的状态
        for(int j = max_width; j >= width[i]; j--){//遍历重量 由递推公式可知 每个重量都依赖于前面的价值 因此如果先算前面的价值 就无法判断是否已经放了该层物品 导致违反01背包只能放一个物品的含义 所以倒序遍历
            dp[j] = max(dp[j], dp[j - width[i]] + value[i]);//dp[j]可能已经被计算过了 代表的就是不放物品时能达到的最大价值 不用dp[j - 1]
        }
        print(dp);
    }
    cout <<dp[max_width];
    return 0;
}
/*
3 4
1 15
3 20
4 35

每层dp结果
0 15 15 15 15 
0 15 15 20 35 
0 15 15 20 35 
35

遍历物品的顺序可以颠倒吗
物品与重量的顺序可以颠倒吗
为什么遍历物品是倒序遍历
*/