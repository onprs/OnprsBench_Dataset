#include <bits/stdc++.h>

using namespace std;

const int MAXN = 300000;
const int MOD = 998244353;

struct Breakpoint {
    int pos;
    int value;
};

array<int, MAXN + 1> freq, prefixCount, prefix, p2, ip2;
vector<vector<Breakpoint>> rows;

void buildRows() {
    vector<int> rad(MAXN + 1, 1);
    for (int p = 2; p <= MAXN; ++p) {
        if (rad[p] != 1) {
            continue;
        }
        for (int x = p; x <= MAXN; x += p) {
            rad[x] *= p;
        }
    }

    vector<vector<int>> blockers(MAXN + 1);
    for (int y = 2; y <= MAXN; ++y) {
        for (int x = rad[y]; x < y; x += rad[y]) {
            blockers[x].push_back(y);
        }
    }

    rows.resize(MAXN + 1);
    rows[0].push_back({0, 0});
    for (int x = 1; x <= MAXN; ++x) {
        auto &row = rows[x];
        auto &previous = rows[x - 1];
        row.push_back({x, x});

        int ptr = 0;
        for (int y : blockers[x]) {
            while (ptr + 1 < (int)previous.size() &&
                   previous[ptr + 1].pos < y) {
                ++ptr;
            }
            int value = previous[ptr].value;
            if (value != row.back().value) {
                row.push_back({y, value});
            }
        }
    }
}

void buildPowers() {
    const int inv2 = (MOD + 1) / 2;
    p2[0] = ip2[0] = 1;
    for (int i = 1; i <= MAXN; ++i) {
        p2[i] = 2LL * p2[i - 1] % MOD;
        ip2[i] = 1LL * inv2 * ip2[i - 1] % MOD;
    }
}

int rangeSum(int left, int right) {
    if (left > right) {
        return 0;
    }
    return (prefix[right] - prefix[left - 1] + MOD) % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    buildRows();
    buildPowers();

    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> values;
        for (int i = 0; i < n; ++i) {
            int x;
            cin >> x;
            if (freq[x] == 0) {
                values.push_back(x);
            }
            ++freq[x];
        }

        int before = 0, ans = 0;
        prefixCount[0] = prefix[0] = 0;
        for (int x = 1; x <= n; ++x) {
            int ways = p2[freq[x]] - 1;
            int rightWeight = 1LL * ways * p2[before] % MOD;
            prefix[x] = prefix[x - 1] + rightWeight;
            if (prefix[x] >= MOD) {
                prefix[x] -= MOD;
            }
            ans = (ans + 1LL * x * ways) % MOD;
            before += freq[x];
            prefixCount[x] = before;
        }

        for (int x : values) {
            int ways = p2[freq[x]] - 1;
            int leftWeight = 1LL * ways * ip2[prefixCount[x]] % MOD;

            int rowSum = 0;
            auto &row = rows[x];
            for (int i = 0; i < (int)row.size(); ++i) {
                int left = max(x + 1, row[i].pos);
                if (left > n) {
                    break;
                }
                int right = n;
                if (i + 1 < (int)row.size()) {
                    right = min(n, row[i + 1].pos - 1);
                }
                rowSum = (rowSum +
                          1LL * row[i].value * rangeSum(left, right)) % MOD;
            }
            ans = (ans + 1LL * leftWeight * rowSum) % MOD;
        }

        cout << ans << '\n';
        for (int x : values) {
            freq[x] = 0;
        }
    }
}