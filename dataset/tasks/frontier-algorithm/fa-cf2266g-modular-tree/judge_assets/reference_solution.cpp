#include <bits/stdc++.h>
using namespace std;

void dfs(long long node, long long par, vector<long long> &A, vector<long long> &B, vector<long long> &g, vector<vector<long long>> &adj) {
    long long gc = 0;
    long long tt = 0;
    for (auto x : adj[node]) {
        if (x != par) {
            dfs(x,node,A,B,g,adj);
            if (g[x]!=B[x]) {gc=gcd(gc,g[x]);}
            tt+=A[x];
        }
    }
    gc=gcd(gc,tt);
    gc=gcd(gc,B[node]);
    g[node]=gc;
}

void solve() {
    long long N; cin >> N;
    vector<long long> A; A.push_back(-1);
    vector<long long> B; B.push_back(-1);
    vector<vector<long long>> adj(N+1);
    for (long long i = 0; i < N; i++) {
        long long a; cin >> a;
        A.push_back(a);
    }
    for (long long i = 0; i < N; i++) {
        long long a; cin >> a;
        B.push_back(a);
    }
    for (long long i = 0; i < N-1; i++) {
        long long a, b; cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    vector<long long> g(N+1); //init to 0 for identity gcd
    dfs(1,0,A,B,g,adj);
    long long aa = 0;
    for (long long i = 1; i <= N; i++) {aa+=((B[i]-A[i]-1)/g[i])*g[i]+A[i];}
    cout << aa << endl;
}

int main() {
    long long T; cin >> T;
    while (T--) {solve();}
}