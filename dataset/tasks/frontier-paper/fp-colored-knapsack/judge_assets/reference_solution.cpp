// 参考解：Colored Knapsack 的精确最优值。
//
// 依来源论文 arXiv:2609.17713 的结构：颜色可行性等价于
//   max_c |S_c| <= |S| - max_c |S_c| + 1，
// 其 DP 状态为 (已处理物品, 选中总数 t, 主色选中数 d, 当前颜色选中数 a,
// 已用容量 w)，值为最大收益。本题实现该状态的容量索引变体：
// dp[t][d][a][w] = 最大收益，按颜色连续顺序逐物品转移。
//
// 仅依赖标准库，从 stdin 读入、stdout 输出。
#include <bits/stdc++.h>
using namespace std;

struct Item {
    int w, p, c;
};

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T-- > 0) {
        int n, b;
        scanf("%d %d", &n, &b);
        vector<Item> items(n);
        for (int i = 0; i < n; ++i)
            scanf("%d %d %d", &items[i].w, &items[i].p, &items[i].c);
        stable_sort(items.begin(), items.end(),
                    [](const Item &x, const Item &y) { return x.c < y.c; });

        const int NEG = INT_MIN / 2;
        int T1 = n + 1;
        int D = n + 1;
        int A = n + 1;
        int W = b + 1;
        size_t plane = (size_t)T1 * D * A * W;
        vector<int> cur(plane, NEG), nxt(plane, NEG);
        auto at = [&](int t, int d, int a, int w) -> size_t {
            return (((size_t)t * D + d) * A + a) * W + w;
        };
        cur[at(0, 0, 0, 0)] = 0;
        int prev_color = -1;
        for (int i = 0; i < n; ++i) {
            fill(nxt.begin(), nxt.end(), NEG);
            const Item &it = items[i];
            bool same_color = (i > 0 && it.c == prev_color);
            int tmax = min(i, n);
            for (int t = 0; t <= tmax; ++t) {
                for (int d = 0; d <= t; ++d) {
                    for (int a = 0; a <= d; ++a) {
                        size_t base = (((size_t)t * D + d) * A + a) * W;
                        for (int w = 0; w < W; ++w) {
                            int v = cur[base + w];
                            if (v == NEG) continue;
                            // 不选：颜色变化时当前颜色计数清零
                            int na = same_color ? a : 0;
                            int &slot = nxt[at(t, d, na, w)];
                            if (v > slot) slot = v;
                            // 选：颜色变化时当前颜色计数同样清零，再从 0 开始计入
                            int nw = w + it.w;
                            if (nw < W) {
                                int nd = d + (na == d ? 1 : 0);
                                int &slot2 = nxt[at(t + 1, nd, na + 1, nw)];
                                int nv = v + it.p;
                                if (nv > slot2) slot2 = nv;
                            }
                        }
                    }
                }
            }
            cur.swap(nxt);
            prev_color = it.c;
        }

        int best = 0;  // 空集总是可行，收益 0
        for (int t = 0; t <= n; ++t) {
            for (int d = 0; d <= t; ++d) {
                if (2 * d > t + 1) continue;
                for (int a = 0; a <= d; ++a) {
                    size_t base = (((size_t)t * D + d) * A + a) * W;
                    for (int w = 0; w < W; ++w) {
                        int v = cur[base + w];
                        if (v > best) best = v;
                    }
                }
            }
        }
        printf("%d\n", best);
    }
    return 0;
}
