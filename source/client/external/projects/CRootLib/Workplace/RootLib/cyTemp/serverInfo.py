# -*- coding: cp949 -*-
#-116616648
import app, localeInfo

app.ServerName = None

SERVER_NAME = "VALIANT2"
SERVER_IP = "213.254.136.100"

SERVER_NAME_2 = "DevServer"
SERVER_IP_2 = "127.0.0.1"

SRVS = {
	1 : {
		"name":SERVER_NAME,
		"HOST":SERVER_IP,
		"AUTH":30001,
		"CH1":30003,
		"CH2":30011,
		"CH3":30019,
		"CH4":30027,
		"CH5":30035,
		"CH6":30043,
	},
	2 : {
		"name":SERVER_NAME_2,
		"HOST":SERVER_IP_2,
		"AUTH":30001,
		"CH1":30003,
		"CH2":30011,
		"CH3":30019,
		"CH4":30027,
		"CH5":30035,
		"CH6":30043,
	}
}

CLIENT_VERSION = "52"

STATE_NONE = "|cFFdadada" + localeInfo.CHANNEL_STATUS_NOT_KNOWN

STATE_DICT = {
	0 : "|cFFffffff" + localeInfo.CHANNEL_STATUS_OFFLINE,
	1 : "|cFF00ff00" + localeInfo.CHANNEL_STATUS_RECOMMENDED,
	2 : "|cFFffc000" + localeInfo.CHANNEL_STATUS_BUSY,
	3 : "|cFFff0000" + localeInfo.CHANNEL_STATUS_BUSY,
	4 : "|cFFff0000" + localeInfo.CHANNEL_STATUS_FULL,
}

SERVER1_CHANNEL_DICT = {
	1:{"key":11,"name":"CH1","ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH1"],"udp_port":SRVS[1]["CH1"],"state":STATE_NONE,},
	2:{"key":12,"name":"CH2","ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH2"],"udp_port":SRVS[1]["CH2"],"state":STATE_NONE,},
	3:{"key":13,"name":"CH3","ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH3"],"udp_port":SRVS[1]["CH3"],"state":STATE_NONE,},
	4:{"key":14,"name":"CH4","ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH4"],"udp_port":SRVS[1]["CH4"],"state":STATE_NONE,},
	5:{"key":15,"name":"CH5","ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH5"],"udp_port":SRVS[1]["CH5"],"state":STATE_NONE,},
	6:{"key":16,"name":"CH6","ip":SRVS[1]["HOST"],"tcp_port":SRVS[1]["CH6"],"udp_port":SRVS[1]["CH6"],"state":STATE_NONE,},
}

SERVER2_CHANNEL_DICT = {
	1:{"key":21,"name":"CH1","ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH1"],"udp_port":SRVS[2]["CH1"],"state":STATE_NONE,},
	2:{"key":22,"name":"CH2","ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH2"],"udp_port":SRVS[2]["CH2"],"state":STATE_NONE,},
	3:{"key":23,"name":"CH3","ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH3"],"udp_port":SRVS[2]["CH3"],"state":STATE_NONE,},
	4:{"key":24,"name":"CH4","ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH4"],"udp_port":SRVS[2]["CH4"],"state":STATE_NONE,},
	5:{"key":25,"name":"CH5","ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH5"],"udp_port":SRVS[2]["CH5"],"state":STATE_NONE,},
	6:{"key":26,"name":"CH6","ip":SRVS[2]["HOST"],"tcp_port":SRVS[2]["CH6"],"udp_port":SRVS[2]["CH6"],"state":STATE_NONE,},
}

REGION_NAME_DICT = {
	0 : SRVS[1]["name"],
	1 : SRVS[2]["name"],
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { "ip":SRVS[1]["HOST"], "port":SRVS[1]["AUTH"], },
		2 : { "ip":SRVS[2]["HOST"], "port":SRVS[2]["AUTH"], },
	}
}

REGION_DICT = {
	0 : {
		1 : { "name" : SRVS[1]["name"], "channel" : SERVER1_CHANNEL_DICT, },
		2 : { "name" : SRVS[2]["name"], "channel" : SERVER2_CHANNEL_DICT, },
	},
}

MARKADDR_DICT = {
	10 : { "ip" : SRVS[1]["HOST"], "tcp_port" : SRVS[1]["CH1"], "mark" : "10.tga", "symbol_path" : "10", },
	20 : { "ip" : SRVS[2]["HOST"], "tcp_port" : SRVS[2]["CH1"], "mark" : "10.tga", "symbol_path" : "10", },
}


