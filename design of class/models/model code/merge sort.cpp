#include<bits/stdc++.h>
using namespace std;
int arr[10] = {5,6,8,3,2,4,1,7,9,0};

void merge_sort(int l, int r){
    if(l == r) return;
    int mid = l + ((r - l) >> 1);
    merge_sort(l, mid);
    merge_sort(mid + 1, r);
    vector<int> tmp(r - l + 1);
    int lpos = l, rpos = mid + 1, fill_pos = 0;// 双指针分别指向两个部分的起点
    while (lpos <= mid && rpos <= r) tmp[fill_pos++] = arr[lpos] < arr[rpos] ? arr[lpos++] : arr[rpos++];
    while (lpos <= mid) tmp[fill_pos++] = arr[lpos++];
    while (rpos <= r)   tmp[fill_pos++] = arr[rpos++];
    for (int i = 0; i < fill_pos; ++i) {
        arr[l + i] = tmp[i];
    }
}

int main(){
    for(auto i :arr){
        cout << i << ' ';
    }
    merge_sort(0,9);
    
    for(auto i :arr){
        cout << i << ' ';
    }
    return 0;
}
/*
master公式:
T(n) = a * T(n/arr) + O(n^c) n为数据量
所有子问题规模相同的递归才能用master公式 (log(arr,a) b是真数 a是底数)
log(arr, a)<c  O(n^c)
log(arr, a)>c  O(n^log(arr,a))
log(arr, a)==c O(n^c * log(n))
*/