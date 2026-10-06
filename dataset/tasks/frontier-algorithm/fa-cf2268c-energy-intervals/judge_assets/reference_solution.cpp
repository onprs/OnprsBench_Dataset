#include <bits/stdc++.h>
 
using namespace std;
 
typedef long long ll;
typedef long double ld;
typedef pair<int,int> pii;
typedef pair<ll,ll> pll;
 
#define F first
#define S second
#define endl '\n'
#define Mp make_pair
#define pb push_back
#define pf push_front
#define size(x) (ll)x.size()
#define all(x) x.begin(), x.end()
 
const int N = 2e5 + 100, lg = 18;
const ll Mod = 1e9 + 7;
const ll inf = 1e18 + 10;
 
ll MOD(ll a, ll mod=Mod) {
    a%=mod; (a<0)&&(a+=mod); return a;
}
ll poww(ll a, ll b, ll mod=Mod) {
    ll res = 1;
    while(b > 0) {
        if(b%2 == 1) res = MOD(res * a, mod);
        b /= 2;
        a = MOD(a * a, mod);
    }
    return res;
}
 
int t, n, a[N], par[lg][N], pref[N], cnt[N * 2], answ = 0, maxi = 0;
 
int getmx(int l, int r) {
    int res = l;
    for(int i=lg-1; i>=0; i--) {
        if(l + (1<<i) - 1 <= r) {
            res = (a[par[i][l]] > a[res] ? par[i][l] : res);
            l += (1<<i);
        }
    }
    return res;
}
 
void divide(int l, int r) {
    if(l > r) return;
    if(l == r) {
        cnt[pref[l]] ++;
        return;
    }
    if(l == r-1) {
        cnt[pref[l]] ++;
        cnt[pref[r]] ++;
        if((max(a[l], a[r]) & answ) == answ) {
            maxi = max(maxi, pref[l-1] ^ pref[r]);
        }
        return;
    }
 
    int mid = getmx(l, r);
 
    if(r-mid > mid-l) {
        divide(l, mid-1);
        for(int i=l; i<mid; i++) cnt[pref[i]] --;
        divide(mid+1, r);

        for(int i=mid-1; i>=l-1; i--) {
            if(cnt[(answ ^ pref[i])] > 0 && (a[mid]&answ) == answ) maxi = answ;
            if (i == mid-1) cnt[pref[mid]] ++;
        }
        for(int i=mid-1; i>=l; i--) cnt[pref[i]] ++;
    } else {
        divide(mid+1, r);
        for(int i=mid+1; i<=r; i++) cnt[pref[i]] --;
        divide(l, mid-1);
 
        cnt[pref[mid-1]] --;
        cnt[pref[l-1]] ++;
        for(int i=mid; i<=r; i++) {
            if(cnt[(answ ^ pref[i])] > 0  && (a[mid]&answ) == answ) maxi = answ;
            if(i == mid) cnt[pref[mid-1]] ++;
        }
        cnt[pref[l-1]] --;
 
        for(int i=mid; i<=r; i++) cnt[pref[i]] ++; 
    }
}
 
bool check() {
    maxi = 0;
    for(int j=1; j<=n; j++) {
        pref[j] = pref[j-1] ^ (a[j] & answ);
    }
 
    divide(1, n);
 
    for(int i=1; i<=n; i++) {
        cnt[pref[i]] = 0;
    }
 
    if(maxi == answ) return 1;
    return 0;
}
 
void work() {
    cin>>n;
 
    int mxtmp = 0, anstmp = 0;
    for(int i=1; i<=n; i++) {
        cin>>a[i];
        mxtmp = max(mxtmp, a[i]);
        par[0][i] = i;
    }
 
    for(int i=1; i<=n; i++) anstmp ^= (a[i] & mxtmp);
 
    for(int i=n; i>=1; i--) {
        for(int j=1; j<lg; j++) {
            int x = par[j-1][i], y = par[j-1][min(n, i + (1<<(j-1)))];
            if(a[x] > a[y]) par[j][i] = x;
            else par[j][i] = y;
        }
    }
 
    for(int i=lg-1; i>=0; i--) {
        answ += (1 << i);
 
        if(check() == 0) {
            answ -= (1 << i);
        }
    }
 
    cout<<max(answ, anstmp)<<endl;
}
 
void reset_work() {
    answ = 0;
    for(int i=1; i<=n; i++) a[i] = 0, pref[i] = 0;
    return;
}
 
int main() {
    ios_base::sync_with_stdio(false), cin.tie(0);
 
    // freopen("inp.txt", "r", stdin);
    // freopen("out-m.txt", "w", stdout);
 
 
    cin>>t;
    // t = 1;
    while(t --) {
        work();
        reset_work();
    }
 
    return 0;
}