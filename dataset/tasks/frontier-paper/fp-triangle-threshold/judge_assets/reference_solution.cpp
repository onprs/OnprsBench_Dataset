// 参考解：阈值三角计数算法的逐步模拟。
//
// 读入 m 与阈值 Q 以及 m 条边（随机顺序的简单图边表），按来源论文
// arXiv:2609.15848 的 Algorithm 1 逐步插入边：先统计新边的公共邻居数
// （即该边闭合的三角形数），再插入边；累计三角形数首次达到 Q 时停止，
// 输出停止长度 S 与估计值 Q * m^3 / S^3（约分后的分数 p/q）。
//
// 仅依赖标准库，从 stdin 读入、stdout 输出。
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef __int128 lll;

static lll gcd128(lll a, lll b) {
    while (b != 0) {
        lll t = a % b;
        a = b;
        b = t;
    }
    return a;
}

static string to_string128(lll v) {
    if (v == 0) return "0";
    bool neg = v < 0;
    if (neg) v = -v;
    string s;
    while (v > 0) {
        s.push_back(char('0' + (int)(v % 10)));
        v /= 10;
    }
    if (neg) s.push_back('-');
    reverse(s.begin(), s.end());
    return s;
}

int main() {
    ll T;
    if (scanf("%lld", &T) != 1) return 0;
    while (T-- > 0) {
        ll m, Q;
        scanf("%lld %lld", &m, &Q);
        unordered_map<ll, int> vid;
        vid.reserve((size_t)(2 * m) + 16);
        vector<unordered_set<int>> adj;
        ll cnt = 0, S = 0;
        bool stopped = false;
        for (ll i = 0; i < m; ++i) {
            ll u, v;
            scanf("%lld %lld", &u, &v);
            if (stopped) continue;  // 继续消费输入，但不模拟
            auto it = vid.find(u);
            int a;
            if (it == vid.end()) { a = (int)adj.size(); vid.emplace(u, a); adj.emplace_back(); }
            else a = it->second;
            it = vid.find(v);
            int b;
            if (it == vid.end()) { b = (int)adj.size(); vid.emplace(v, b); adj.emplace_back(); }
            else b = it->second;
            const unordered_set<int> &A = adj[a], &B = adj[b];
            if (A.size() <= B.size()) {
                for (int w : A) if (B.count(w)) ++cnt;
            } else {
                for (int w : B) if (A.count(w)) ++cnt;
            }
            adj[a].insert(b);
            adj[b].insert(a);
            ++S;
            if (cnt >= Q) stopped = true;
        }
        lll p = (lll)Q * (lll)m * (lll)m * (lll)m;
        lll q = (lll)S * (lll)S * (lll)S;
        lll g = gcd128(p, q);
        if (g != 0) { p /= g; q /= g; }
        printf("%lld %s %s\n", S, to_string128(p).c_str(), to_string128(q).c_str());
    }
    return 0;
}
