#include <bits.stdc++.h>

class Bridge{
public:
	int id,root_id,root_port,root_distance;
	std::vector<LAN> LANs;
	std::vector<int> ports; //if ports[i]=0 then port_i is a RP, =1 then DP for LAN LANs[i], =2 unassigned/disabled?
	std::vector<int> ftable;//ftable[i]=j => to send to Host(i+1), send the message to the jth port

	Bridge();
	Bridge(int id, int root_id, int root_port, int root_distance);
	bool operator<(const Bridge &b1) const;//why const?	

	void add_lan()


};

class LAN{
public:
	int id,dport,dbridge;
	std::vector<int> hosts;
	std::vector<Bridge> cbridges;

	LAN();
	LAN(int id, int dport, Bridge dbridge);
	void addHost(int idx);
	void addBridge(Bridge b);

};

class Config{
	int root_id,root_distance,sender_id;
	Bridge &src;//check & usage
	
	bool operator<(const Config &c1) const;//why const?	compares 2 config messages
};