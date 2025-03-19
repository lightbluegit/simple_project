/*
给定一个整型数组, 你的任务是找到所有该数组的递增子序列，递增子序列的长度至少是2。
示例:
输入: [4, 6, 7, 7]
输出: [[4, 6], [4, 7], [4, 6, 7], [4, 6, 7, 7], [6, 7], [6, 7, 7], [7,7], [4,7,7]]
说明:
给定数组的长度不会超过15。
数组中的整数范围是 [-100,100]。
给定数组中可能包含重复数字，相等的数字应该被视为递增的一种情况
*/
#include<bits/stdc++.h>
using namespace std;
void print(auto a){
    try
    {
        for(const auto& i : a){
            cout << i;
        }
        cout <<'\n';
    }
    catch(...)
    {
        cerr <<"错误";
    }
}

void bg(int st_idx, vector<int>& rst, vector<int>& a){
    if(rst.size() > 1)
        print(rst);//纵向移动结束
    int n = a.size();
    vector<int> used(100, 0);//存储本层使用情况
    for(int i = st_idx; i < n; i++){//树层横向移动
        if((!rst.empty() && rst[rst.size()-1] > a[i])||(i && a[i] == a[i-1] && used[a[i]])) continue;
        rst.push_back(a[i]);
        used[a[i]] = 1;
        bg(i + 1, rst,a);//出来无需恢复 不然无法去到去重作用
        rst.pop_back();
    }
}

int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int n; cin >> n;
    // int k; cin >> k;
    // int t; cin >> t;
    vector<int> a(n);
    for(int i = 0; i < n; i++){
        cin >> a[i];
    }
    vector<int> rst;
    bg(0, rst,a);
    return 0;
}