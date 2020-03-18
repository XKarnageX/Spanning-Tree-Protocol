#include <bits/stdc++.h>
using namespace std;

int main(){
	int tr; cin>>tr;
	int n;  cin>>n;
	vector<Bridge> bridges; //bridges[i] = B_(i+1)
	for(int i=0;i<n;i++){
		bridges.push_back(Bridge());
		string line;
		getline(cin,line);
		if(line.size()>3){
			for(int j=5;j<=line.size();j+=2){
				bridges[i].add_lan(int(line[j-1])-int("A")+1) //add_lan will add the given lan to Bi's lan vector. port numbers are the indexes
			}
		}
	}
}