#include <bits/stdc++.h>
using namespace std;

inline bool good(int x) {
    return __builtin_popcount(x) % 2 == 0;
}

int32_t main() {
    cin.tie(0);
    cout.tie(0);
    ios_base::sync_with_stdio(0);

    int tc;
    cin >> tc;

    while (tc--) {
        int n, q;
        cin >> n >> q;

        vector<int> a(n);
        int answer = 0;

        for (int &x : a) {
            cin >> x;
            answer += good(x);
        }

        cout << answer;

        while (q--) {
            int p, x;
            cin >> p >> x;
            --p;

            answer -= good(a[p]);
            a[p] = x;
            answer += good(a[p]);

            cout << ' ' << answer;
        }

        cout << '\n';
    }

    return 0;
}