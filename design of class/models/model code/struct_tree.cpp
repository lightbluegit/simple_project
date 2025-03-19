// 结构化与反结构化
#include<bits/stdc++.h>
using namespace std;
struct treenode
{
    char val;
    treenode* left;
    treenode* right;
    treenode(char val): val(val), left(nullptr), right(nullptr){}
};

int idx = 0;
treenode* fstruct_pre(vector<char>& pre_list){//反结构化
    if(pre_list[idx] == '#'){
        idx++;
        return nullptr;
    }
    treenode* root = new treenode(pre_list[idx++]);
    root->left = fstruct_pre(pre_list);
    root->right = fstruct_pre(pre_list);
    return root;
}

treenode* fstruct_ceng(vector<char>& ceng_list){//1 2 3 # # # 4 # #
    queue<treenode*>qu;
    treenode* root = new treenode(ceng_list[idx++]);
    qu.push(root);
    while(!qu.empty()){
        int size = qu.size();
        for(int i = 0; i < size; i++){
            treenode* cur = qu.front();
            qu.pop();
            if(ceng_list[idx] != '#'){
                treenode* left = new treenode(ceng_list[idx]);
                cur->left = left;
                qu.push(left);
            }
            idx++;
            if(ceng_list[idx] != '#'){
                treenode* right = new treenode(ceng_list[idx]);
                cur->right = right;
                qu.push(right);
            }
            idx++;
        }
    }
    return root;
}

string rst = "";
void struct_tree_pre(treenode* root){//结构化
    if(root == nullptr){
        rst += "# ";
    }
    else{
        rst += root->val;
        rst += ' ';
        struct_tree_pre(root->left);
        struct_tree_pre(root->right);
    }
}

void struct_tree_ceng(treenode* root){
    queue<treenode*> ceng;
    ceng.push(root);
    while(!ceng.empty()){
        int size = ceng.size();
        for(int i = 0; i < size; i++){
            treenode* cur = ceng.front();
            ceng.pop();
            if(cur == nullptr){
                rst += "# ";
                continue;
            }
            rst += cur->val;
            rst += ' ';
            if(cur->left){ceng.push(cur->left);}
            else{ceng.push(nullptr);}
            if(cur->right){ceng.push(cur->right);}
            else{ceng.push(nullptr);}
        }
    }
}

void ceng(treenode* root){
    queue<treenode*> qu;
    qu.push(root);
    while(!qu.empty()){
        int size = qu.size();
        for(int i = 0; i < size; i++){
            treenode* cur = qu.front();
            qu.pop();
            cout << cur->val << ' ';
            if(cur->left){qu.push(cur->left);}
            if(cur->right){qu.push(cur->right);}
        }
        cout <<endl;
    }
}

void pre_bl(treenode* root){
    if(root == nullptr){return;}
    cout << root->val << ' ';
    pre_bl(root->left);
    pre_bl(root->right);
}

int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io+
    int n; cin >> n;
    vector<char> pre_list(n);
    for(int i = 0; i < n; i++){
        cin >> pre_list[i];
    }
    // treenode* root = fstruct_pre(pre_list);
    treenode* root = fstruct_ceng(pre_list);
    ceng(root);
    // pre_bl(root);
    cout << endl;
    struct_tree_ceng(root);
    // struct_tree_pre(root);
    cout << rst;
    return 0;
}
/*
序列化：将树转化成字符串的形式存储
反序列化：将字符串还原为树
先序 后序 按层遍历可以实现
先序
9
1 2 # # 3 # 4 # #
层序
9
1 2 3 # # # 4 # #
*/