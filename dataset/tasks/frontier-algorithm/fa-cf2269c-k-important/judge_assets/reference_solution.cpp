#include <bits/stdc++.h> 
#define pb push_back 
#define F first 
#define S second 
#define all(a) a.begin(),a.end() 
#define sz(a) (int)a.size() 
#define pii pair<ll,ll>
#define ll long long
#define ld long double
#define rep(i , a , b) for(int i = (a) ; i <= (b) ; i++)
#define per(i , a , b) for(int i = (a) ; i >= (b) ; i--)
using namespace std ;
const int maxn = 5e5 + 10  ;
int a[maxn] ;
signed main(){
  ios::sync_with_stdio(0);cin.tie(0); cout.tie(0);
  int t ;cin >> t ; 
  while(t--){
    int n , k ; cin >> n  >> k; 
    for(int i = 1 ;i <= n ; i++){
       cin >> a[i] ; 
    }
    ll sum = 0 ;
    vector <int> vec;   
    for(int i = 1 ; i <= n ; i++){
      if(i >= k && i <= n-k+1){
        sum += a[i] ;
        continue ; 
      } 
      vec.pb(a[i]) ; 
    }
    int t2 = max(0 , sz(vec)- (k-1)) ;
    int l = 0 , r= sz(vec)-1 ;
    while(t2--){
      sum += max(vec[l] , vec[r]) ;
      l++;
      r--;  
    }
    cout << sum << "\n" ;
  }
}