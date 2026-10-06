// 参考解：字母表 {a,...,} 下的字典序最小最短缺失子串。
//
// 读入 n、sigma 与字符串 S（字符为 'a'..'a'+sigma-1）。在 S 的后缀自动机上
// 从初始状态做 BFS：若某状态在字母 c 上没有转移，则到达该状态的（最短且
// 字典序最小的）BFS 标签拼接 c 即为字典序最小的最短缺失子串。
//
// 仅依赖标准库，从 stdin 读入、stdout 输出。
#include <bits/stdc++.h>
using namespace std;

struct SAM {
    vector<int> link, len;
    vector<int> nxt;  // 扁平化：state * sigma + c
    int sigma, last, sz;
    SAM(int sigma_, int n) : sigma(sigma_) {
        int cap = 2 * n + 2;
        link.assign(cap, -1);
        len.assign(cap, 0);
        nxt.assign((size_t)cap * sigma, -1);
        sz = 1; last = 0;
    }
    int new_state() { return sz++; }
    void extend(int c) {
        int cur = new_state();
        len[cur] = len[last] + 1;
        int p = last;
        while (p != -1 && nxt[(size_t)p * sigma + c] == -1) {
            nxt[(size_t)p * sigma + c] = cur;
            p = link[p];
        }
        if (p == -1) {
            link[cur] = 0;
        } else {
            int q = nxt[(size_t)p * sigma + c];
            if (len[p] + 1 == len[q]) {
                link[cur] = q;
            } else {
                int clone = new_state();
                len[clone] = len[p] + 1;
                link[clone] = link[q];
                for (int i = 0; i < sigma; ++i)
                    nxt[(size_t)clone * sigma + i] = nxt[(size_t)q * sigma + i];
                while (p != -1 && nxt[(size_t)p * sigma + c] == q) {
                    nxt[(size_t)p * sigma + c] = clone;
                    p = link[p];
                }
                link[q] = link[cur] = clone;
            }
        }
        last = cur;
    }
};

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T-- > 0) {
        int n, sigma;
        scanf("%d %d", &n, &sigma);
        vector<char> buf(n + 2);
        scanf("%s", buf.data());
        SAM sam(sigma, n);
        for (int i = 0; i < n; ++i) sam.extend(buf[i] - 'a');

        vector<int> parent(sam.sz, -1), pchar(sam.sz, -1);
        vector<char> visited(sam.sz, 0);
        vector<int> queue;
        queue.reserve(sam.sz);
        visited[0] = 1;
        queue.push_back(0);
        string answer;
        bool found = false;
        for (size_t qi = 0; qi < queue.size() && !found; ++qi) {
            int u = queue[qi];
            for (int c = 0; c < sigma; ++c) {
                int v = sam.nxt[(size_t)u * sigma + c];
                if (v == -1) {
                    // 重构 u 的标签并拼接 c
                    string label;
                    int x = u;
                    while (x != 0) {
                        label.push_back((char)('a' + pchar[x]));
                        x = parent[x];
                    }
                    reverse(label.begin(), label.end());
                    label.push_back((char)('a' + c));
                    answer = label;
                    found = true;
                    break;
                }
                if (!visited[v]) {
                    visited[v] = 1;
                    parent[v] = u;
                    pchar[v] = c;
                    queue.push_back(v);
                }
            }
        }
        printf("%s\n", answer.c_str());
    }
    return 0;
}
