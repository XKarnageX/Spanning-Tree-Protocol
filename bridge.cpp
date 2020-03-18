#include <bits/stdc++.h>
using namespace std;

class Bridge{
public:
	int id,root_id,root_port,root_distance;
	vector<LAN> LANs;
	vector<int> ports; //if ports[i]=0 then port_i is a RP, =1 then DP for LAN LANs[i], =2 unassigned/disabled?
	vector<int> ftable;//ftable[i]=j => to send to Host(i+1), send the message to the jth port

	Bridge(){
		id = -1;
		root_id = id;
		root_port = -1;
		root_distance = 0;
	}

	void add_lan()


};