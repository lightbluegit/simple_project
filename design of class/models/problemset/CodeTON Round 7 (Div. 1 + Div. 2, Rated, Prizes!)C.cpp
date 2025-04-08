/*CodeTON Round 7 (Div. 1 + Div. 2, Rated, Prizes!)C. Matching Arrays
ai > bi的个数记作cnt 任意重排b的数字可否达到cnt == k?可以输出一个合法b序列
由于b可以重排 相当于a也可以重排 因为无论a怎么变 b都可以对应起来 但是由于输出的是原a顺序的b序列 因此用aa来sort 对于b的最低构造 将b排序后最小的k个数从小到大放到最后与a对应 此时ab都为上升序列 如果该情况满足要求 就可以成功构造(选择b中最小的对应a中最大的 因此a中小数就与b中的大数相对应)此时扫一遍aa 用图和队列存储a中值对应的数 由于顺序随意 队列和栈都可以 且不用去重
*/
#include<bits/stdc++.h>
using namespace std;
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int t; cin >> t;
    while(t--){
        int n, k; cin >> n >> k;
        vector<int>a(n), b(n), aa(n), rst(n);
        for(int i = 0; i < n; i++){
            scanf("%d", &a[i]);
            aa[i] = a[i];
        }
        for(int i = 0; i < n; i++){
            scanf("%d", &b[i]);
        }
        sort(aa.begin(), aa.end());
        sort(b.begin(), b.end());
        rotate(b.begin(), b.begin() + k, b.end()); //b = b[k::] + b[:k:]
        map<int, queue<int>>matchab;
        for(int i = 0; i < n; i++){
            if(aa[i] > b[i]){
                k--;
            }
            matchab[aa[i]].push(b[i]);
        }
        if(k == 0){
            printf("YES\n");
            for(int i = 0; i < n; i++){
                printf("%d ", matchab[a[i]].front());
                matchab[a[i]].pop();
            }
            cout << "\n";
        }
        else{
            cout << "NO\n";
        }
    }
    return 0;
}

/*
7
1 0
1
2
1 1
1
2
3 0
2 4 3
4 1 2
3 1
2 4 3
4 1 2
3 2
2 4 3
4 1 2
3 3
2 4 3
4 1 2
5 2
6 4 5 6 2
9 7 9 1 1

ans:
YES
2 
NO
NO
YES
2 1 4 
YES
4 2 1 
NO
YES
1 9 9 1 7

*/