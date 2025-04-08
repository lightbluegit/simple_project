/*Pinely Round 3 (Div. 1 + Div. 2) C. Heavy Intervals
不是这玩意儿怎么扯得到括号匹配上去啊
对左右括号进行匹配并求出距离 小距离配大val得到sum
*/
#include<bits/stdc++.h>
using namespace std;
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    long long t; cin >> t;
    while(t--){
        long long n; cin >> n;
        vector<long long>c(n);
        vector<pair<long long,char>>line;
        for(long long i = 0; i < n; i++){
            long long zc;
            scanf("%d", &zc);
            line.push_back(make_pair(zc, '('));
        }
        for(long long i = 0; i < n; i++){
            long long zc;
            scanf("%d", &zc);
            line.push_back(make_pair(zc, ')'));
        }
        for(long long i = 0; i < n; i++){
            scanf("%d", &c[i]);
        }
        sort(c.begin(), c.end(), greater<long long>());
        sort(line.begin(), line.end());
        stack<long long>le;
        vector<long long>length;
        long long idx = 0;
        long long summ = 0;
        for(const auto &i : line){
            char ty = i.second;
            long long pos = i.first;
            if(ty == '('){
                le.push(pos);
            }
            else{
                long long lepos = le.top(); le.pop();
                length.push_back(pos - lepos);
            }
        }
        sort(length.begin(), length.end());
        for(long long i = 0; i < n; i++){
            summ += length[i] * c[i];
        }
        cout << summ << "\n";
    }
    return 0;
}
/*
2
2
8 3
12 23
100 100
4
20 1 2 5
30 4 3 10
2 3 2 3

ans:
2400
42

*/