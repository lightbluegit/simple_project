#include<bits/stdc++.h>
using namespace std;

void heapinsert(int arr[], int pos){
    while(arr[pos] > arr[(pos - 1) / 2]){
        swap(arr[pos], arr[(pos - 1) / 2]);
        pos = (pos - 1) / 2;
    }
    for(int i = 0; i < 6;i++){
        cout << arr[i] << ' ';
    }
    cout << endl;
}

void heapify(int arr[], int i, int size){
    int l = i * 2 + 1;
    while (l < size){
        int best = l + 1 < size && arr[l + 1] > arr[l] ? l + 1 : l;
        best = arr[best] > arr[i] ? best : i;
        if(best == i) break;
        swap(arr[best], arr[i]);
        i = best;
        l = i * 2 + 1; 
    }
}

void heapsort(int arr[], int n){
    for(int i = 0; i < n; i++){
        heapinsert(arr, i);
    }
    
    int size = n;
    while(size > 1){
        swap(arr[0], arr[--size]);
        heapify(arr, 0, size);
    }
    for(int i = 0; i < n; i++){
        cout << arr[i] << ' ';
    }
}
int main(){
    int a[6] = {3,5,4,2,1,6};
    heapsort(a, 6);
    return 0;
}
/*
父 (i-1)/2 
左 i*2+1
右 i*2+2
*/