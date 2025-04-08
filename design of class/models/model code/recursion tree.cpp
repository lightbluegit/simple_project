#include<bits/stdc++.h>
using namespace std;
struct treenode{
    int val;
    treenode* left;
    treenode* right;
    treenode(int val):
        val(val),
        left(nullptr),
        right(nullptr)
        {}
};

treenode* build_tree(const vector<int> val) {
    int size = val.size();
    if(!size) return nullptr;
    vector<treenode*> nodes(size, nullptr);
    nodes[0] = new treenode(val[0]);
    for(int i = 0; i < size; i++){
        int l = (i << 1) + 1;
        if(l < size && val[l]){
            nodes[l] = new treenode(val[l]);
            nodes[i]->left = nodes[l];
        }
        l ++;
        if(l < size && val[l]){
            nodes[l] = new treenode(val[l]);
            nodes[i]->right = nodes[l];
        }
    }
    return nodes[0];
}

void pre_rec(treenode* root){//递归遍历(dfs)
    if(root == nullptr) return;
    cout << root->val << ' ';
    pre_rec(root->left);
    pre_rec(root->right);
}

void mid_rec(treenode* root){
    if(root == nullptr) return;
    mid_rec(root->left);
    cout << root->val << ' ';
    mid_rec(root->right);
}

void mid_iter(treenode* root){//迭代法遍历(bfs)
    if(root == nullptr) return;
    stack<treenode*>tree_stack;
    tree_stack.push(root);//预处理 给到初始状态
    while(!tree_stack.empty()){
        treenode* cur = tree_stack.top();//取出并处理当前节点
        tree_stack.pop();
        if(cur != nullptr){//将该节点作为 '中' 加入左右节点
            if(cur->right) tree_stack.push(cur->right);//入栈 中序遍历的倒序

            tree_stack.push(cur);//第二次加入(只用改变中间两行的顺序就可以实现三种遍历方式)
            tree_stack.push(nullptr);//用nullptr标记该节点已经处理过 可以进行输出

            if(cur->left) tree_stack.push(cur->left);
        }
        else{//输出节点
            cur = tree_stack.top();//获取输出节点
            cout << cur->val << ' ';//处理输出节点
            tree_stack.pop();
        }
    }
}

void lat_rec(treenode* root){
    if(root == nullptr) return;
    lat_rec(root->left);
    lat_rec(root->right);
    cout << root->val << ' ';
}

void cengbl(treenode* root){
    queue<treenode*>rst;
    if(root){
        rst.push(root);
    }
    int ceng_num = 0, min_depth = -1;
    while(!rst.empty()){
        ceng_num++;
        int size = rst.size();//每层节点个数
        for(int i = 0; i < size; i++){
            treenode* cur = rst.front();
            cout << cur->val << ' ';
            rst.pop();
            bool have_child = false;
            if(cur->left){
                rst.push(cur->left);
                have_child = true;
            }
            if(cur->right) {
                rst.push(cur->right);
                have_child = true;    
            }
            if(!have_child && min_depth == -1){
                min_depth = ceng_num;
            }
        }
        cout << "\n";
    }
    cout << "最大深度/树的高度:" << ceng_num << "\n";
    cout << "最小深度:" << min_depth;
}


void reverse_tree(treenode* root){//反转树(层序遍历 + 每个节点反转左右子树)
    if(root == nullptr) return;
    queue<treenode*> que;
    que.push(root);
    while(!que.empty()){
        int size = que.size();
        for(int i = 0; i < size; i ++){
            treenode* cur = que.front();
            que.pop();
            if(cur->left) que.push(cur->left);
            if(cur->right) que.push(cur->right);
            swap(cur->left, cur->right);
        }
    }
}

bool HuiWen_ceng(treenode* root){//判断一个二叉树是否镜像对称
    if(root == nullptr) return true;
    queue<treenode*>rst;
    rst.push(root);
    while(!rst.empty()){
        int size = rst.size();//上层节点个数
        vector<treenode*>ceng;
        for(int i = 0; i < size; i++){
            treenode* cur = rst.front();
            rst.pop();
            if(cur->left) {rst.push(cur->left);
                ceng.push_back(cur->left);
            }
            if(cur->right) {rst.push(cur->right);
            ceng.push_back(cur->right);}
        }
        int l = 0, r = ceng.size() - 1;
        while(l <= r){
            if(ceng[l]->val != ceng[r]->val){
                return false;
            }
            l++;
            r--;
        }
    }
    return true;
}

treenode* mid_lat_to_tree(vector<int>& mid_val, int midl, int midr, vector<int>lat_val, int latl, int latr){//给定中序后序遍历结果 求树
    treenode* root = new treenode(lat_val[latr]);
    if(latr - latl + 1 == 1){return root;}//找到叶子节点
    int root_index = 0;
    for(int i = midl; i <= midr; i++){
        if(mid_val[i] == root->val){
            root_index = i;
            break;
        }
    }
    int latlsize = root_index - midl, latrsize = midr - root_index;
    root->left = mid_lat_to_tree(mid_val, midl, root_index - 1, lat_val, latl, latl + latlsize - 1);
    root->right = mid_lat_to_tree(mid_val, root_index +1, midr, lat_val, latl + latlsize, latl + latlsize + latrsize - 1);
    return root;
}

int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);//文件io
    int n; cin >> n;
    vector<int> tree_val(n);
    for(int i= 0; i < n; i++){
        scanf("%d", &tree_val[i]);
    }
    treenode* root = build_tree(tree_val);
    // pre_rec(root);
    // cout << endl;
    // mid_rec(root);
    // cout << endl;
    mid_iter(root);
    // lat_rec(root);
    // cout << endl;
    // reverse_tree(root); 
    // cengbl(root);
    // bool huiwen = HuiWen_ceng(root);
    // cout << huiwen;
    return 0;
}
 /*
满二叉树：每一层都是满的
完全二叉树：可以从满二叉树的最底层最右侧依次减去子节点得到的树
搜索二叉树 左节点的数比根节点小 右节点的数比根节点大
平衡二叉搜索树（AVL）左右两子树的高度的绝对值相差不超过1且左右都是平衡二叉树
map set multimap multiset底层都是平衡二叉树 因此增删操作时间都是logn
二叉树深度：根节点到当前节点的距离
高度：当前节点到叶子节点的距离
后序遍历的最后一个就是根节点的值

复习；不同二叉搜索树 
*/