#include<bits/stdc++.h>
using namespace std;
struct list_node {
    int val;
    list_node* prev; // 新增前驱指针
    list_node* next;
    
    // 构造函数初始化所有成员
    list_node(int x) : 
        val(x), 
        prev(nullptr),  // 初始化prev
        next(nullptr) 
    {}
};

// 构建双向链表
list_node* build_node(int values[], int n) {
    list_node dummy(0);
    list_node* current = &dummy;
    
    for (int i = 0; i < n; ++i) {
        current->next = new list_node(values[i]);
        current->next->prev = current; // 设置前驱指针
        current = current->next;
    }
    
    // 处理实际头节点的prev指针
    if (dummy.next) {
        dummy.next->prev = nullptr;
    }
    return dummy.next;
}

// 安全删除链表（无需修改）
void delete_node(list_node* head) {
    while (head) {
        list_node* temp = head;
        head = head->next;
        delete temp;
        temp = nullptr;
    }
}

// 打印链表（保持单链表输出方式）
void print_node(list_node* head) {
    list_node* current = head;
    cout << "Head->";
    while (current) {
        cout << current->val << "<->";
        current = current->next;
    }
    cout << "NULL" << endl;
}

// 反转双向链表
list_node* reverseList(list_node* head) {
    list_node* pre = nullptr;
    while (head) {
        // 保存后继节点并反转指针
        list_node* next = head->next;
        head->next = pre;
        head->prev = next; // 新prev指向原next
        // 移动指针
        pre = head;
        head = next;
    }
    return pre;
}

int main(){
    int a[3] =  {1, 2, 3};
    list_node* head= build_node(a, 3);
    head = reverseList(head);
    print_node(head);
    delete_node(head);
    return 0;
}
/*
*/