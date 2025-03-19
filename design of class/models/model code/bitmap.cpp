#include<bits/stdc++.h>
using namespace std;
class Bitmap{//位图适用于存储范围连续且固定的数字
    vector<int>bitmap;
    bool reversed = false;
    int n;
    public:
        Bitmap(int n):
            bitmap((n + 31) / 32),//(a+b-1)/b适用于向上取整
            n(n)
            {}
    public:
        void add(int pos){
            if(reversed){
                bitmap[pos/32] &= ~(1 << pos%32);
            }
            else{
                bitmap[pos/32] |= 1 << pos%32;
            }
        }
    public:
        void remove(int pos){
            if(reversed){
                bitmap[pos/32] |= 1 << pos%32;
            }
            else{
                bitmap[pos/32] &= ~(1 << pos%32);
            }
        }
    public:
        void reverse(int pos){
            bitmap[pos/32] ^= 1 << pos%32;
        }
    public:
        bool find(int pos){
            bool rst = (bitmap[pos/32] >> pos % 32) & 1 == 1;
            return rst ^= reversed ? 1 : 0;
        }
    public:
        void reverse_all(){
            reversed ^= 1;
        }
    public:
        string print(){
            int size = bitmap.size();
            string rst;
            for(int i = 0; i <= size; i++){
                for(int j = 0; j < 32 && i * 32 + j < n; j++){
                    int num = (bitmap[i] >> j) & 1;
                    num ^= reversed? 1:0;
                    rst += to_string(num);
                }
            }
            return rst;
        }
};
int main(){
    freopen("E:/kafuyuno/code/c++/test1i.txt", "r", stdin);
    string rst;
    int l, r, n;
    cin >> n;
    Bitmap bitmap(n);
    cin >> l;
    bitmap.add(l);
    cout << bitmap.print() << endl;
    bitmap.remove(l);
    cout << bitmap.print() << endl;
    bitmap.reverse(l);
    cout << bitmap.print() << endl;
    bitmap.reverse_all();
    cout << bitmap.print() << endl;
    return 0;
}