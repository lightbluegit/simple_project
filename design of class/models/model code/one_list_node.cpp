#include<bits/stdc++.h>
using namespace std;
struct list_node {
    // 成员变量声明
    int val;
    list_node* next;
    // 创建结构体或类的实例时自动调用构造函数 必须与类或结构体同名 这样编译器才能识别它为构造函数
    list_node(int x):        // 1. 参数列表
          val(x),         // 2. 成员初始化列表（冒号开头）
          next(nullptr)   //    （逗号分隔成员初始化）
    {}                    // 3. 函数体（可为空）
};

list_node* build_node(int values[], int n) {
    list_node dummy(0);      // 空节点简化操作
    list_node* current = &dummy;
    
    for (int validx = 0; validx < n; validx ++) {
        current->next = new list_node(values[validx]);
        current = current->next;
    }
    
    return dummy.next;  // 返回实际头节点
}

// 安全删除函数（防御性编程）
void delete_node(list_node* head) {
    while (head) {
        list_node* temp = head;       // 保存当前节点地址
        head = head->next;           // 移动指针到下一节点
        delete temp;                 // 安全释放当前节点
        temp = nullptr;              // 防御性置空 防止野指针
    }
}

void print_node(list_node* head) {
    list_node* current = head;
    cout << "Head->";
    while (current) {
        cout << current -> val << "->";
        current = current->next;
    }
    cout << "NULL" << endl;
}

list_node* reverseList(list_node* head) {
    list_node* pre = nullptr;//从后改成前应该指向哪
    list_node* next = nullptr;//head的下一个节点在哪
    while (head != nullptr) {
        next = head->next;
        head->next = pre;//反转next节点
        pre = head;//pre向后移动
        head = next;//head向后移动
    }
    return pre;//prev最终指向新链表头
}

list_node* merge_node_list(list_node* head1, list_node* head2){
    list_node* head = head1->val < head2->val ? head1:head2;
    list_node* current1 = (head == head1? head1->next : head1);
    list_node* current2 = (head == head1? head2 : head2->next);
    list_node* total_current = head;
    while(current1 != nullptr && current2 != nullptr){
        if(current1->val <= current2->val){
            total_current->next = current1;
            current1 = current1->next;
        }
        else{
            total_current->next = current2;
            current2 = current2->next;
        }
        total_current = total_current->next;
    }
    total_current->next = (current1 == nullptr?current2 : current1);
    return head;
}

list_node* find_same_node(list_node* h1, list_node* h2){//既然必然在同一个地方结束 那么去掉较长链的前几个节点 使得两个链表一样长 然后一起向下搜索 必然会遇到交点
    if(h1 == nullptr || h2 == nullptr) return nullptr;
    int diff = 0;//h1比h2多的节点个数
    list_node* h0 = h1;
    while(h0){
        h0 = h0->next;
        diff++;
    }
    h0 = h2;
    while(h0){
        h0 = h0->next;
        diff--;
    }
    list_node* h3 = nullptr;
    if(diff){
        h0 = h1;
        h3 = h2;
    }
    else{
        h0 = h2;
        h3 = h1;
    }
    diff = abs(diff);
    printf("开始去头\n");
    for(int i = 0; i < diff; i++){
        printf("%d ", h0->val);
        h0 = h0->next;
    }
    printf("去头结束\n");
    while(h0){
        printf("h0=%d ", h0->val);
        printf("h3=%d\n", h3->val);
        h0 = h0->next;
        h3 = h3->next;
        if(h0 == h3){
            return h0;
        }
    }
}

list_node* delete_count_backwards(list_node* head, int n){//删除倒数第n个节点
    list_node* fast = head->next;
    list_node* slow = head;
    for(int i = 0; i < n; i++){
        fast = fast->next;
    }
    while(fast){
        fast = fast->next;
        slow = slow->next;
    }
    list_node* next = slow->next->next;
    delete slow->next;
    slow->next = next;
    return head;
}

int main(){
    // freopen("test1i.txt", "r", stdin);
    // freopen("test1o.txt", "w", stdout);
    int nodea[5] = {1,2,3,4,5};
    list_node* headnode = build_node(nodea, 5);
    print_node(headnode);
    list_node* pre = reverseList(headnode);
    print_node(pre);
    delete_node(pre);
    
    int a[4] =  {3,5,9,10}, b[4]={2,7,8,13};
    list_node* heada= build_node(a, 4);
    list_node* headb = build_node(b, 4);
    list_node* total_head = merge_node_list(heada, headb);
    print_node(total_head);
    delete_node(total_head);
    return 0;
}
/*
新标准C++程序设计
978-7-5766-0287-6
*/