#include<bits/stdc++.h> //万能头
using namespace std;
void print(auto a){//快速输出单层容器内容
    try{
        for(const auto& i : a){
            cout << i;
        }
        cout <<'\n';
    }
    catch(...){
        cerr <<"错误";
    }
}

vector<int> removeElement(vector<int>& nums, int val) {//不用额外空间移除指定元素
    int slowIndex = 0;//慢指针指向待填充位置
    for (int fastIndex = 0; fastIndex < nums.size(); fastIndex++) {//快指针指向待处理位置
        if (val != nums[fastIndex]) {
            nums[slowIndex++] = nums[fastIndex];
        }
    }
    for(int i = slowIndex; i <= nums.size(); i++){//将多余的位置删掉 slowindex比真实位置多一位 所以是 <=
        nums.pop_back();
    }
    return nums;
}

void slid_window(vector<int>& a, int s) {//滑动窗口找到数组中和>=指定值的最小子区间
    int i = 0, allsum = 0, rst = a.size();
    for(int j = 0; j < a.size(); j++){
        allsum += a[j];
        while(allsum >= s){
            cout << i << ' ' << j << '\n';
            rst = min(rst, j - i);
            allsum -= a[i++];
        }
    }
    cout << rst;
}

void test(){

    
}
int main(){
    // freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    // freopen("E:/kafuyuno/code/c++/test1o.txt", "w", stdout);
    test();
    return 0;

    int a[5] = {5, 4 ,3, 2, 1};
    int n = sizeof(a) / sizeof(a[0]);//计算数组元素个数
    swap(a[1], a[0]);//原理:三次拷贝构造/赋值 O(1)
    printf("%d",n);

    for(const auto& i : a){// 使用范围循环输出（C++11特性）
        cout << i << ' ';
    }
    cout << '\n';
    // & 取址符号 
    int aa = 3;
    int* pa = &aa;// int* 代表该变量是int类型的指针变量 存储地址 每个指针8个字节
    cout << *pa << '\n';//*解引用输出值

    int pbv = 4;
    const int* pb = &pbv;//常量指针 不可修改值 但可以改变地址
    // *pb = 5
    pb = &aa;

    int* pc = new int(5);//动态分配内存 记得delete
    cout << *pc << '\n';
    delete pc;
    pc = nullptr;

    int* pd = new int(0);
    // cout << *pd;//不能对空指针解引用 会报错
    delete pd;//但是可以正常删除
    pd = nullptr;

    //野指针 定义时没有初始化 动态分配内存 delete后虽然内存被释放 但是指针仍然指向一个无效地址 指针指向的变量已经超过变量的作用域 被回收了 规避: 初始化为nullptr delete后赋值为nullptr 不返回局部变量的地址
    int listp[3] = {0,1,2};
    int* lp = listp;
    cout << *(lp + 1) << '\n';//可以使用指针指向一维数组的第一个数据 然后通过+运算并解引用获得一维数组中的值

    int* clp = new int[5];//动态创建一维数组 int a[100]是在栈上创建内存 空间很小 但是new是在堆上创建 空间可以到10亿
    for(int i = 0; i < 5; i++){
        clp[i] = i;//可以用正常的数组语法
        cout << *(clp + i) << ' ';//也可以解引用写
    }
    delete []clp;//不要用[]删除非 new []申请的空间 不要多次删除

    //异或运算就是无进位相加(1+1=10->0) 满足交换律 结合律 0^n=0 n^n=0 (a^b=c -> a=b^c) n&(-n)可以取出最右侧的1
    //其他的数字都出现了m次 只有一个数字出现了n < m次 统计每一个数的每一位的数 如果最后这一位对m取余!=0 则这位是1 最后将01拼起来就可以得到出现次数不足的那个数字
    //判断一个数是不是3的幂:用一个足够大的3的幂取模 结果为0就是 非零就不是 
    //
    //(a+b-1)/b适用于向上取整
    string s = "123456";
    auto sub = s.substr(s.size()-3, 2);//起始位置 字符数量
    cout << sub;
    //'\n'比endl性能好 for(const auto& i : s)更快
    reverse(s.begin() + 3, s.begin() + 4 );
    return 0;
}