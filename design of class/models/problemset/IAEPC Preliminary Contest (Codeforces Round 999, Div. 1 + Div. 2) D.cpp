/*IAEPC Preliminary Contest (Codeforces Round 999, Div. 1 + Div. 2) D
模拟题 从小的数字合成大的数字不好做 但是大的数字拆分成两个小的数字只有一种拆法 所以可以递归算
*/
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
bool divide(int num, int cnt, map<int, int>& cnta, map<int, int>& cntb){//是否存在将cnt个num拆分的方法
    if(num <= 1){return false;}//1没法拆了 无解
    int l = num / 2, r = (num + 1) / 2;//奇偶数都能用的拆分
    if(cnta[l] >= cnt){//有足够的数字储备量
        cnta[l] -= cnt;
    }
    else{
        bool rsta = divide(l, cnt - cnta[l], cnta, cntb);//尝试向下拆分
        cnta[l] = 0;
        if(!rsta){return false;}
    }
    if(cnta[r] >= cnt){
        cnta[r] -= cnt;
    }
    else{
        bool rsta = divide(r, cnt - cnta[r], cnta, cntb);
        cnta[r] = 0;
        if(!rsta){return false;}
    }
    cntb[num] = 0;
    return true;
}
int main(){
    // freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int t; cin >> t;
    while(t--){
        int n, m;
        cin >> n >> m;
        ll summ = 0;
        map<int, int>cnta, cntb;
        for(int i = 0; i < n; i++){
            int zc;
            scanf("%d", &zc);
            summ += zc;
            cnta[zc]++;//可用的数字及出现次数
        }
        for(int i = 0; i < m; i++){
            int zc;
            scanf("%d", &zc);
            summ -= zc;
            if(cnta[zc] >= 1){//已经有了的数字不用拆分
                cnta[zc]--;
            }
            else{
                cntb[zc]++;//需要拆分的数字及个数
            }
        }
        // for(auto& i : cnta){
        //     cout << i.first<<" " << i.second << endl;
        // }
        // for(auto& i : cntb){
        //     cout << i.first<<" " << i.second << endl;
        // }
        if(summ != 0){
            cout << "NO\n";
            continue;
        }
        bool rst = true;
        for(auto& i : cntb){
            int num = i.first, cnt = i.second;
            rst = divide(num, cnt, cnta, cntb);
            if(!rst){
                break;
            }
        }
        if(rst){
            printf("YES\n");
        }
        else{
            printf("NO\n");
        }
    }
    return 0;
}
/*
9

2 1
4 5
9

2 1
3 6
9

4 2
1 2 2 2
3 4

4 2
1 1 3 3
3 5

4 2
1 2 3 4
3 5

5 5
1 2 3 4 5
5 4 3 2 1

4 2
1 1 1 1
1 1

4 4
1 1 1 1
1 1 1 2

1 1
1
1000000000

Yes
No
Yes
Yes
No
Yes
No
No
No
*/