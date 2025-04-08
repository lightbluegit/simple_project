/*
给定每条线段的起始与结束位置 求覆盖区域最多有几条线段
将每个线段按照起点位置从小到大依次排序
删除ans容器中结尾位置<=当前线段起始位置的数据
遍历依次加入结尾位置并维持ans数组从小到大的排列
当前线段最多覆盖区间为ans数组的数据个数
*/
#include <bits/stdc++.h>
using namespace std;
struct Pair {
    int st;
    int ed;
};

int max(int a, int b){return a < b ? b: a;}

int main() {
    // 原始数据
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    int n; cin >> n;

    vector<int> st(n),ed(n);
    for(int i = 0; i < n; i++){
        cin >> st[i] >> ed[i] ;
    }
    // 1. 合并为结构体数组
    vector<Pair> pairs;
    for (int i = 0; i < n; i++) {
        pairs.push_back({st[i], ed[i]});
    }

    // 2. 按st从小到大排序
    sort(pairs.begin(), pairs.end(), [](const Pair& a, const Pair& b) {//sort(起始迭代器, 结束迭代器, 比较函数)[] 捕获列表：为空表示不捕获外部变量（此处无需访问外部数据）。两个 const 引用参数，避免拷贝且不可修改元素。a.st < b.st 升序排列 True:a在b前面
        return a.st < b.st;
    });
    vector<int> ans;
    deque<int> heap;
    int rst = 0;
    for(auto i : pairs){
        // cout << i.st << ' ' << i.ed <<'\n';
        if(!heap.empty()){
            while(heap.front() <= i.st){
                heap.pop_front();
            }
        }
        heap.push_front(i.ed);
        sort(heap.begin(), heap.end());//sort默认从小到大排序
        // for(auto i : heap){
        //     cout << i <<' ';
        // }
        // cout << endl;
        ans.push_back(heap.size());
        rst = max(rst, heap.size());
    }
    cout << "rst=" <<rst;
    return 0;
}
/*
word转pdf
代码
录屏并介绍
*/