#include<bits/stdc++.h>
using namespace std;
int tlower_bound(int a[], int st, int ed, int aim){
    int ans = -1;
    while(st <= ed){
        // int mid = (st+ ed)/2; //有溢出的可能
        int mid = st + ((ed - st) >> 1);
        if(a[mid] >= aim){
            ans = mid;
            ed = mid - 1;
        }
        else st = mid + 1;
    }
    return ans;
}
int main(){
    // freopen("test1i.txt", "r", stdin);
    // freopen("test1o.txt", "w", stdout);
    int a[8] = {3,6,6,7,9,13,17,27};
    cout << tlower_bound(a, 0, 7, 18);
    // cout << *lower_bound(a, a + 7, 37);// 起始 终止位置 目标数字 返回第一个>=给定值的元素的迭代器
    // cout << *upper_bound(a, a + 7, 37);// upper_bound > 给定值
    //如果数组中所有值都小于目标值 则返回end() 容易造成误判
    return 0;
}