#include<bits/stdc++.h>
using namespace std;
int solve(int l, int r){//返回一个数从l一直 & r的值
    while(r > l){
        r -= r & (-r);
    }
    return r;
}
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int l, r;
    cin >> l >> r;
    int rst = solve(l, r);
    int ans = l;
    for(int i = l + 1; i <= r;i++){
        ans &= i;
    }
    printf("rst=%d, ans=%d",rst, ans);
    return 0;
}