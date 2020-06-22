def STP(bridge_Network, LAN_Network):
    change = False
    while not change:
        unchanged = True
        for b in bridge_Network:
            b.forward_messages()#update the receivedConfigs field in each bridge according to graph
        for b in bridge_Network:
            c = b.update_params()#updates Bridge state based on receivedConfigs and returns true if params are NOT changed, also empties receivedConfigs
            unchanged = c and unchanged
        change = not unchanged

def LB(bridge_Network, LAN_Network, data_transfers, host_to_LAN):#data_transfers is a list of tuple(sender_host_id,receiver_host_id)
    for s,r in data_transfers:
        l = host_to_LAN[s]
        l.transferData(tuple([s,r,-1]))
        for b in bridge_Network:
            b.displayFTable()
        print("\n")


class LAN:
    id = -1 #name
    db = -1 #designated bridge
    adj = []#list of tuple(bridge,port no. of bridge)
    hosts = []#list of "H1"

    def __init__(self,name):
        self.id = name
        self.db = -1
        self.adj = []
        self.hosts = []

    "Spanning Tree Protocol Implementation"

    def add_Bridge(self, b, p):
        (self.adj).append(tuple([b,p]))

    def forward_on_all_interfaces(self,msg):
        for bridge,port in self.adj:
            temp = list(msg)
            temp[3] = port
            temp = tuple(temp)
            bridge.receivedConfigs.append(temp)
            # if len(bridge.best_port_configs)!=0:
            # print("Port",port)
            # print(len(bridge.best_port_configs))
            bridge.best_port_configs[port] = min(bridge.best_port_configs[port],temp)
            # else:
            #     bridge.best_port_configs

    def displayAdj(self):
        for bridge,port in self.adj:
            print(bridge.id,port,end=" ")
        print("\n")

    "Bridge Learning Implementation"

    def add_host(self, idx):
        self.hosts.append(idx)

    def displayHosts(self):
        print(hosts)

    def transferData(self, datagram):
        s,r,b = datagram #s host, r host and sender bridge id
        # if r in self.hosts:
        #     #Done!
        #     x11 = 1
        # else:
        for bridge,port in self.adj:
            if bridge.port_type[port]!=0 and bridge.id!=b:
                bridge.transferData(tuple([s,r,port]))







class Bridge:
    "A config is a 4tuple (sender_root,root_distance,sender_id,receiver_port)"
    "Spanning Tree Protocol Implementation"
    id = -1
    root = id
    rd = 0
    rp = -1
    num_ports = 0
    forward_config = tuple([root,rd,id,-1])
    receivedConfigs = [] #stores Configs received in a given iteration of STP
    adj = [] #list of LAN objects, index is port no.
    best_port_configs = [] #index is port no., stores best config received on that port
    port_type = []# 0 = np, 1 = dp, 2=rp default: each port is a dp as each bridge is root
    receivedData = []#data is of the form tuple(sender_host_id,receiver_host_id,receiver_port,sender bridge)
    ftable = {}

    def __init__(self,id1):
        self.id = id1
        self.root = id1
        self.rd = 0
        self.rp = -1
        self.num_ports = 0
        self.forward_config = tuple([self.root,self.rd,self.id,-1])
        self.receivedConfigs = []
        self.adj = []
        self.best_port_configs = []
        self.port_type = []
        self.receivedData = []
        self.ftable = {}

    def update_params(self):
        if len(self.receivedConfigs)!=0:
            best = min(self.receivedConfigs)
            temp = tuple(best[0:3])
            if temp<tuple([self.root,self.rd,self.id]):
                self.rp = best[3]
                self.port_type[self.rp] = 2
                self.root = temp[0]
                self.rd = temp[1]+1
                forward_config = tuple([self.root,self.rd,self.id,-1])
            self.receivedConfigs = []

    def forward_messages(self):
        # print("Bridge config is ",self.forward_config)
        for port in range(self.num_ports):
            # print("Checking port",port)
            # print("Number of ports",self.num_ports)
            # if len(self.best_port_configs)!=0:
            temp = self.best_port_configs[port]
            # print("Best Config at port",port,"is",temp)
            # print("Port type is",self.port_type[port])
            if temp[0:3]<self.forward_config[0:3]:
                # print("Changing port type to 0!")
                self.port_type[port] = 0
            if self.port_type[port]!=0:
                lan1 = self.adj[port]
                msg = self.forward_config
                # msg[3] = port #unncessary
                lan1.forward_on_all_interfaces(msg)
            # else:
            #     if self.port_type[port]!=0:
            #         lan1 = self.adj[port]
            #         msg = self.forward_config
            #         # msg[3] = port #unncessary
            #         lan1.forward_on_all_interfaces(msg)

    def add_LAN(self, l):
        # print("zzzAdding LAN",l.id,"to Bridge",self.id)
        (self.adj).append(l)
        # self.displayAdj()

    def displayAdj(self):
        for l in self.adj:
            print(l.id,end=" ")
        # print("\n")

    def displayPorts(self):
        # a = zip
        print("B"+str(self.id)+":",end=" ")
        l_idx = [self.adj[j].id for j in range(self.num_ports)]
        # print(l_idx)
        t_idx = [self.cnv(self.port_type[j]) for j in range(self.num_ports)]
        # print(t_idx)
        z = sorted(zip(l_idx,t_idx))
        # print(z)
        for l1,t1 in z[0:self.num_ports-1]:
            print(l1+"-"+t1,end=" ")
        print(z[self.num_ports-1][0]+"-"+z[self.num_ports-1][1])

    def cnv(self,i):
        if i==0:
            return "NP"
        elif i==1:
            return "DP"
        else:
            return "RP"

    "Learning Bridges Implementation"
    def displayFTable(self):
        print("B"+str(self.id)+":")
        print("HOST ID | FORWARDING PORT")
        z = sorted([(k,v) for k,v in self.ftable.items()])
        for host,port in z:
            # port = self.ftable[host]
            l_idx = self.adj[port].id
            print(host,"|",l_idx)

    def transferData(self, datagram):
        s,r,p = datagram
        self.ftable[s] = p
        if r in self.ftable.keys():
            tp = self.ftable[r]
            l = self.adj[tp]
            l.transferData(tuple([s,r,self.id]))
            # self.displayFTable()
        else:
            for i in range(self.num_ports):
                if self.port_type[i]!=0 and i!=p:
                    l1 = self.adj[i]
                    l1.transferData(tuple([s,r,self.id]))
                    # self.displayFTable()


tr = bool(input().strip())
n = int(input().strip())

bridge_Network = []
bridge_idx = []
LAN_Network = []
LAN_idx = []
host_to_LAN = {}
data_transfers = []

for i in range(n):
    bridge_Network.append(Bridge(i+1))
    line = input().strip()
    # print(line)
    l = len(line)
    for j in range(4,l,2):
        temp_LAN_id = line[j]
        if temp_LAN_id not in LAN_idx:
            LAN_idx.append(temp_LAN_id)
            tempLAN = LAN(temp_LAN_id)
            # print("Adding LAN",temp_LAN_id,"to Bridge", str(i+1))
            bridge_Network[i].add_LAN(tempLAN)
            tempLAN.add_Bridge(bridge_Network[i],bridge_Network[i].num_ports)
            bridge_Network[i].num_ports = bridge_Network[i].num_ports + 1
            bridge_Network[i].port_type.append(1)
            bridge_Network[i].best_port_configs.append(bridge_Network[i].forward_config)
            LAN_Network.append(tempLAN)
        else:
            idx = LAN_idx.index(temp_LAN_id)
            tempLAN = LAN_Network[idx]
            # print("Adding LAN",temp_LAN_id,"to Bridge", str(i+1))
            bridge_Network[i].add_LAN(tempLAN)
            tempLAN.add_Bridge(bridge_Network[i],bridge_Network[i].num_ports)
            bridge_Network[i].num_ports = bridge_Network[i].num_ports + 1
            bridge_Network[i].port_type.append(1)
            bridge_Network[i].best_port_configs.append(bridge_Network[i].forward_config)

STP(bridge_Network,LAN_Network)

for b in bridge_Network:
    b.displayPorts()

for i in range(len(LAN_idx)):
    line = input().strip()
    l = len(line)

    l_id = line[0]
    lan = LAN_Network[LAN_idx.index(l_id)]
    hosts1 = line.split(":")[1]
    hosts1 = hosts1.split(" ")[1:]
    for host in hosts1:
        lan.add_host(host)
        host_to_LAN[host]=lan

nd = int(input().strip())

for i in range(nd):
    line = input().strip()
    x = tuple(line.split(" "))
    data_transfers.append(x)

LB(bridge_Network,LAN_Network,data_transfers,host_to_LAN)
