/*2024-2025 ICPC, NERC, Southern and Volga Russian Regional Contest
分类讨论
2份2+1份1(无损耗) + 1份2+2份1(损耗3个)可以消耗完3份物品1 2
2份3用来消耗物品3
剩下的就是n%3个物品1 2 n%2个物品3
分类讨论:0 0 == 0
0 1 or 1 0 == 1
剩下的要2个新板子才能凑出来
rst加上对应的剩余部分再输出
*/
#include<bits/stdc++.h>
using namespace std;
int main(){
    // freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int n; cin >> n;
    int rst = (n/3)*2+(n/2);
    int l = n % 3, r = n % 2;
    if(!l && !r){
        cout << rst;
    }
    else{
        if((l == 1 && !r) || (r == 1 && !l)){
            cout << rst + 1;
        }
        else{
            cout << rst + 2;
        }
    }
    return 0;
}
/*
1
ans:2

3
ans:4
*/