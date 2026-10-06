#include <bits/stdc++.h>
 
using namespace std;
 
using i64 = long long;
 
const int mod = 998244353;
const int G = 3;
const int B = 18;
const int N = 200000;
 
int qpow(int a, int b) {
    int r = 1;
    while (b) {
        if (b & 1) r = (i64)r * a % mod;
        a = (i64)a * a % mod;
        b >>= 1;
    }
    return r;
}
 
struct NTT {
    int n;
    vector<int> rev, roots;
 
    NTT(int n) : n(n), rev(n), roots(n) {
        for (int i = 1; i < n; i++) {
            rev[i] = (rev[i >> 1] >> 1) | ((i & 1) ? (n >> 1) : 0);
        }
 
        for (int len = 1; len < n; len <<= 1) {
            int z = qpow(G, (mod - 1) / (len << 1));
            roots[len] = 1;
            for (int i = 1; i < len; i++) {
                roots[len + i] = (i64)roots[len + i - 1] * z % mod;
            }
        }
    }
 
    void transform(vector<int>& a) const {
        for (int i = 0; i < n; i++) {
            if (i < rev[i]) swap(a[i], a[rev[i]]);
        }
 
        for (int len = 1; len < n; len <<= 1) {
            for (int i = 0; i < n; i += len << 1) {
                for (int j = 0; j < len; j++) {
                    int x = a[i + j];
                    int y = (i64)a[i + j + len] * roots[len + j] % mod;
 
                    a[i + j] = x + y;
                    if (a[i + j] >= mod) a[i + j] -= mod;
 
                    a[i + j + len] = x - y;
                    if (a[i + j + len] < 0) a[i + j + len] += mod;
                }
            }
        }
    }
};
 
vector<int> fac(2 * N + 1);
vector<int> ifac(2 * N + 1);
vector<int> catalan(N + 1);
 
void init() {
    fac[0] = 1;
    for (int i = 1; i <= 2 * N; i++) {
        fac[i] = (i64)fac[i - 1] * i % mod;
    }
 
    ifac[2 * N] = qpow(fac[2 * N], mod - 2);
    for (int i = 2 * N; i >= 1; i--) {
        ifac[i - 1] = (i64)ifac[i] * i % mod;
    }
 
    for (int i = 0; i <= N; i++) {
        catalan[i] = (i64)fac[2 * i] * ifac[i] % mod
                   * ifac[i + 1] % mod;
    }
}
 
void solve() {
    int n;
    cin >> n;
 
    vector<int> a(n), pref(n + 1);
    for (int& x : a) cin >> x;
 
    if (n == 1) {
        cout << 0 << '\n';
        return;
    }
 
    for (int i = 1; i <= n; i++) {
        pref[i] = pref[i - 1] ^ a[i - 1];
    }
 
    vector<int> weight(n);
    int W = 0;
 
    for (int d = 1; d < n; d++) {
        weight[d] = (i64)catalan[d] * catalan[n - d] % mod;
        W = (W + (i64)(n - d + 1) * weight[d]) % mod;
    }
 
    int len = 1;
    while (len < 2 * (n + 1)) len <<= 1;
 
    NTT ntt(len);
 
    vector<int> kernel(len);
    for (int d = 1; d < n; d++) {
        kernel[d] = weight[d];
        kernel[len - d] = weight[d];
    }
 
    ntt.transform(kernel);
 
    int answer = (i64)((1 << B) - 1) * W % mod;
    int inv_len = qpow(len, mod - 2);
    int inv_two = (mod + 1) / 2;
    int total_xor = pref[n];
 
    vector<int> seq(len);
 
    for (int b = 0; b < B; b++) {
        if ((total_xor >> b) & 1) continue;
 
        fill(seq.begin(), seq.end(), 0);
 
        for (int i = 0; i <= n; i++) {
            seq[i] = ((pref[i] >> b) & 1) ? mod - 1 : 1;
        }
 
        ntt.transform(seq);
 
        int spectral_sum = 0;
 
        for (int k = 0; k < len; k++) {
            int opposite = (len - k) & (len - 1);
 
            int term = (i64)kernel[k] * seq[k] % mod
                     * seq[opposite] % mod;
 
            spectral_sum += term;
            if (spectral_sum >= mod) spectral_sum -= mod;
        }
 
        int Q = (i64)spectral_sum * inv_len % mod * inv_two % mod;
 
        answer -= (i64)(1 << b) * Q % mod;
        if (answer < 0) answer += mod;
    }
 
    cout << answer << '\n';
}
 
int main() {
    cin.tie(0)->sync_with_stdio(0);
 
    init();
 
    int T;
    cin >> T;
 
    while (T--) solve();
}