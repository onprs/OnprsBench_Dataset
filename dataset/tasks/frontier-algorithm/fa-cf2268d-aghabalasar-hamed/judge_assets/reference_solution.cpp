#include <bits/stdc++.h>
using namespace std;

using ll = long long;

const int MXN = 1e6+5;

int n, p[MXN], R[MXN], L[MXN];
ll dp[MXN];
vector<int> vec[MXN];
bool mark[MXN];

void solve(int l, int r) {
    dp[r] = r-l;
    int lst=r, cnt=0;
    if(L[r]!=n+1) {
        vec[L[r]].push_back(r);
        mark[r] = 1;
        cnt++;        
    }
    for(int i=r-1; i>=l; i--) {
        while(!mark[lst]) lst--;
        if(lst==R[i]) {
            dp[i] = dp[R[i]] + r-l+1 - 2 - (i-l);
        }
        else {
            int c1 = i-l + 1;
            int c2 = R[i]-i-1 + (R[R[i]]!=n+1) + cnt - 1 - (R[R[i]]!=n+1 && L[R[R[i]]]<=i);
            dp[i] = dp[lst] + 2*(r-l+1) - 3 - 2*c1 - c2 + 1;
        }
        for(int j : vec[i])
            mark[j] = 0,
            cnt--;
        if(L[i]!=n+1) {
            vec[L[i]].push_back(i);
            mark[i] = 1;
            cnt++;
        }
    }

    for(int i=l; i<=r; i++)
        dp[i] += l-1;
}

void Main() {
    cin >> n;
    for(int i=1; i<=n; i++) {
        cin >> p[i];
        vec[i].clear();
        mark[i] = 0;
    }
    fill(L+1, L+n+1, n+1);
    for(int i=n; i>=1; i--) {
        for(R[i]=i+1; R[i]<=n && p[R[i]]<p[i]; R[i]=R[R[i]]);
        L[R[i]] = i;
    }
    int l=1;
    for(int r=1; r<=n; r++)
        if(R[r]==n+1) {
            solve(l, r);
            l = r+1;
        }
    ll ans = 0;
    for(int i=1; i<=n; i++)
        ans += dp[i];
    cout << ans << '\n';
}

int32_t main() {
    cin.tie(0); cout.tie(0); ios_base::sync_with_stdio(0);
    int T;
    cin >> T;
    while(T--) Main();
    return 0;
}