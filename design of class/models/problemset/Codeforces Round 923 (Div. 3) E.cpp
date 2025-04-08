/*Codeforces Round 923 (Div. 3) E. Klever Permutation
构造题 样例说明有点问题
构造一个长度为n的全排列 使得任意2个长度为k的子串的差值不超过1
减去左边，加上右边来移动子串位置 按照左边+1=右边 右边+1=左边 的顺序循环往复 观察样例的构造方式按照位置的奇偶分成增和减两个序列 依次for循环生成
*/
#include<bits/stdc++.h>
using namespace std;
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int t; cin >> t;
    while (t--)
    {
        int n, k; cin >> n >> k;
        vector<int>a(n);
        int num = 1, idx = 0;
        for(int i = 0; i < k; i += 2){//确定起点位置
            idx = i;
            while(idx < n){//按照指定步数生成
                a[idx] = num++;
                idx += k;
            }
        }
        
        num = n, idx = 1;
        for(int i = 1; i < k; i += 2){
            idx = i;
            while(idx < n){
                a[idx] = num--;
                idx += k;
            }
        }
        for(const auto& i : a){
            cout << i << ' ';
        }
        cout <<"\n";
    }
    
    return 0;
}
/*
5
2 2
3 2
10 4
13 4
7 4

ans:
1 2 
1 3 2 
1 10 4 7 2 9 5 6 3 8 
1 13 5 10 2 12 6 9 3 11 7 8 4 
1 7 3 5 2 6 4 
*/