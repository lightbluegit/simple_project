/*Codeforces Round 922 (Div. 2) C. XOR-distance
|x异或a - y异或a|最小 a<=r (r要longlong)
首先 复习一下异或的意义 不进位加法 由于存在大小关系 每一位有4种可能(大数 小数):00 11 01 10, 00 11不管怎么操作相减之后都不会变 所以不考虑 要得到最小的差 最理想的情况只需要保留最左边的一位10 其余10全部转化为01 最后求差即可 但是可操作的范围只有0~r 因此应该尽量选择左边的10转换为01 并记录所需花费 倒序遍历省事点
*/
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
ll solve(ll big, ll sma, ll r){
    int rpos = int(log2l(r)), bigpos = int(log2l(big));
    ll smasum = 0, bigsum = 0, curr = 0, curnum = pow(2, bigpos);
    for(int i = bigpos; i >= 0; i--){//当前选中位置
        if(i != bigpos){curnum >>= 1;}//2^18已经很极限了 不能pow(2, bigpos + 1)
        if(((sma >> i) & 1) + ((big >> i) & 1) == 1){//01 || 10
            if(i <= rpos){//可以操作10
                if((big >> i) & 1){//10
                    if(!bigsum){//不可操作的部分没有10出现 需要保证至少有1位10
                        bigsum = curnum;
                    }
                    else{
                        if(curr + curnum <= r){//尝试将10改为01
                            curr += curnum;
                            smasum += curnum;
                        }
                        else{//改不了
                            bigsum += curnum;
                        }
                    }
                }
                else{//01
                    smasum += curnum;
                }
                
            }
            else{//不可操作 直接加
                if((sma >> i) & 1){
                    smasum += curnum;
                }
                else{
                    bigsum += curnum;
                }
            }
        }
    }
    return bigsum - smasum;
}

int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int t; cin >> t;
    while (t--)
    {
        ll x, y, r; cin >> x >> y >> r;
        if(x == y || r == 0){
            cout << abs(y - x) << "\n";
            continue;
        }
        cout << ((x < y) ? solve(y, x, r) : solve(x, y, r)) << "\n";
    }
    return 0;
}
/*
10
4 6 0
0 3 2
9 6 10
92 256 23
165 839 201
1 14 5
2 7 2
96549 34359 13851
853686404475946 283666553522252166 127929199446003072
735268590557942972 916721749674600979 895150420120690183

ans:
2
1
1
164
542
5
3
37102
27934920819538516
104449824168870225
*/