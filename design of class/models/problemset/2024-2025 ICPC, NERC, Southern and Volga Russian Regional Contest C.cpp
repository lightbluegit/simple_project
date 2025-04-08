/*2024-2025 ICPC, NERC, Southern and Volga Russian Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams) C
推理*/
#include<bits/stdc++.h>
using namespace std;
int main(){
    // freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int t; cin >> t;
    while(t--){
        int n, ava_cnt = 0;
        cin >> n;
        map<int, int> num_cnt;
        for(int i = 0; i < n; i++){
            int zc;
            scanf("%d", &zc);
            num_cnt[zc]++;
            if((num_cnt[zc] & 1) == 0){
                ava_cnt++;
            }
        }
        if(ava_cnt < 4){
            cout <<"NO\n";
            continue;
        }
        vector<int> rst;
        for(auto i : num_cnt){
            while(rst.size() < 2 && i.second >= 2){
                rst.push_back(i.first);
                i.second -= 2;
            }
        }
        for(auto it=num_cnt.rbegin(); it!=num_cnt.rend(); it++){
            while(rst.size() < 4 && it->second >= 2){
                rst.push_back(it->first);
                it->second -= 2;
            }
        }
        printf("YES\n%d %d %d %d %d %d %d %d\n", rst[0], rst[1], rst[0], rst[2], rst[3], rst[1], rst[3], rst[2]);
    }
}