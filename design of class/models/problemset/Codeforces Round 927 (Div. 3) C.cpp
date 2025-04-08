/*Codeforces Round 927 (Div. 3) C. LR-remainders
你以为这题在考逆元?不不不 这只是个1400 所以我们要反向思考 用同余做
*/
#include<bits/stdc++.h>
using namespace std;
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int t; cin >> t;
    while(t--){
        int n, m; cin >> n >> m;
        vector<int>a(n);
        for(int i = 0; i < n;i ++){
            scanf("%d", &a[i]);
        }
        int l = 0, r = n - 1;
        string s; cin >> s;
        for(int i = 0; i < n - 1;i++){
            if(s[i] == 'L'){
                l++;
            }
        }
        r = l;
        stack<int>ans;
        int rst = a[l] % m;
        ans.push(rst);

        for(int i = n - 2; i >= 0;i--){
            if(s[i] == 'L'){
                l--;
                rst = (rst * a[l]) % m;
            }
            else{
                r++;
                rst = (rst * a[r]) % m;
            }
            ans.push(rst);
        }
        while(!ans.empty()){
            cout << ans.top() << " ";
            ans.pop();
        }
        cout << "\n";
    }
    return 0;
}
/*
4
4 6
3 1 4 2
LRRL
5 1
1 1 1 1 1
LLLLL
6 8
1 2 3 4 5 6
RLLLRR
1 10000
10000
R

ans
0 2 4 1 
0 0 0 0 0 
0 0 0 4 4 4 
0
*/