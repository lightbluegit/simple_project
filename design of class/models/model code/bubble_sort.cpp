#include<bits/stdc++.h>
using namespace std;
void bubble_sort(int st, int ed, int arr[]){
    for(int i = ed; i > st; i--){
        bool swapped = 0;
        for(int j = st; j < i; j++){
            if(arr[j + 1] < arr[j]){//从小到大
                swap(arr[j + 1], arr[j]);
                swapped = 1;
            }
        }
        if(!swapped) return;
    }
}
int main(){
    freopen("test1i.txt", "r", stdin);
    // freopen("test1o.txt", "w", stdout);
    int a[5] = {5, 4 ,3, 2, 1};
    bubble_sort(0, 4, a);
    int n = sizeof(a) / sizeof(a[0]);
    printf("%d",n);
    for(auto i : a){
        cout << i << ' ';
    }
    cout << endl;
    return 0;
}