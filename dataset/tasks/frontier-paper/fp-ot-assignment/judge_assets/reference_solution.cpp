// 参考解：平衡离散最优传输（等于指派问题）的精确最小费用。
//
// 输入 n 与 n x n 整数费用矩阵 C，输出 min_{排列 pi} sum_i C[i][pi(i)]。
// 使用 Jonker-Volgenant 风格的 O(n^3) 匈牙利算法（对偶势 + 增广路），
// 维护满足 u_i + v_j <= C[i][j] 的对偶势，并在最优匹配的边上取等号。
//
// 仅依赖标准库，从 stdin 读入、stdout 输出。
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T-- > 0) {
        int n;
        scanf("%d", &n);
        vector<vector<ll>> a(n, vector<ll>(n));
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j) scanf("%lld", &a[i][j]);

        const ll INF = (ll)4e18;
        vector<ll> u(n + 1, 0), v(n + 1, 0);
        vector<int> p(n + 1, 0), way(n + 1, 0);
        for (int i = 1; i <= n; ++i) {
            p[0] = i;
            int j0 = 0;
            vector<ll> minv(n + 1, INF);
            vector<char> used(n + 1, 0);
            do {
                used[j0] = 1;
                int i0 = p[j0], j1 = -1;
                ll delta = INF;
                for (int j = 1; j <= n; ++j)
                    if (!used[j]) {
                        ll cur = a[i0 - 1][j - 1] - u[i0] - v[j];
                        if (cur < minv[j]) {
                            minv[j] = cur;
                            way[j] = j0;
                        }
                        if (minv[j] < delta) {
                            delta = minv[j];
                            j1 = j;
                        }
                    }
                for (int j = 0; j <= n; ++j) {
                    if (used[j]) {
                        u[p[j]] += delta;
                        v[j] -= delta;
                    } else {
                        minv[j] -= delta;
                    }
                }
                j0 = j1;
            } while (p[j0] != 0);
            do {
                int j1 = way[j0];
                p[j0] = p[j1];
                j0 = j1;
            } while (j0);
        }
        // 用匹配重建费用（对偶势与匹配边取等号，两者在最优时相等）
        vector<int> colOfRow(n + 1, 0);
        for (int j = 1; j <= n; ++j) colOfRow[p[j]] = j;
        ll primal = 0;
        for (int i = 1; i <= n; ++i) primal += a[i - 1][colOfRow[i] - 1];
        printf("%lld\n", primal);
    }
    return 0;
}
