#include<bits/stdc++.h>
using namespace std;
int max(int a, int b) {return a < b ? b :a;}
int min(int a, int b) {return a > b ? b :a;}
int main(){
    // freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int t; cin >> t;
    while(t--){
        int n, ma = 0, mi = 1005;
        cin >> n;
        vector<int> a(n), cnt(1005);
        for(int i= 0; i < n; i++){
            scanf("%d", &a[i]);
            cnt[a[i]]++;
            ma = max(ma, a[i]);
            mi = min(mi, a[i]);
        }
        long long pluss = 0;
        bool pd = true;
        for(int i = mi; i <= ma; i++){
            if(cnt[i] > 2){
                pluss += cnt[i] - 2;
            }
            else if (cnt[i] < 2)
            {
                if(pluss >= 2 - cnt[i]){
                    pluss -= 2 - cnt[i];
                }
                else{
                    cnt[i] += pluss;
                    if(cnt[i] == 1){
                        pd = false;
                        break;
                    }
                }
            }
            
        }
        if(pd){
            printf("YES\n");
        }
        else{
            printf("NO\n");
        }
    }

    return 0;
}