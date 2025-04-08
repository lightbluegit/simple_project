/*2024-2025 ICPC Asia Jakarta Regional Contest (Unrated, Online Mirror, ICPC Rules, Teams Preferred) C.saga
字符串拼接
*/
#include<bits/stdc++.h>
using namespace std;
int max(int a, int b){return a>b ? a:b;}
int main(){
    // freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    string s1, s2, rsts;
    getline(cin, s1);
    getline(cin, s2);
    map<char, int>pre;//每个字符第一次出现位置 重合点下标(最短前缀)
    int rst = s1.size() + s2.size();
    for(int i = 1; i < s1.size(); i++){//前后缀非空 重合点不可能为第一个字母
        if(!pre[s1[i]]){
            pre[s1[i]] = i + 1;
        }
    }
    int l = 0, r = 0;//substr是个O(n)的时间复杂度
    for(int i = 0; i < s2.size() - 1; i++){
        if(pre[s2[i]] > 1){//1 2串都有的字母 并且在1串前面可以有前缀
            int len = pre[s2[i]] + s2.size() - i - 1;
            if(len < rst){
                rst = len;
                l = pre[s2[i]], r = i;
            }
        }
    }
    if(l)
        cout << s1.substr(0, l) + s2.substr(r + 1, s2.size() - r) << endl;
    else
        cout << -1 << endl;
    return 0;
}
/*
sarana
olahraga
ans:saga

icpc
jakarta
ans:-1
*/