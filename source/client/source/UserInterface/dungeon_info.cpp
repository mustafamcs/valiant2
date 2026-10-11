#include "stdafx.h"
#ifdef ENABLE_DUNGEON_INFO
#include "dungeon_info.h"
#include "PythonNetworkStream.h"
#include "Packet.h"
#include <json.hpp>
#include <fstream>
#include "PythonPlayer.h"
CDungeonInfo::CDungeonInfo()
{
	Initialize();
}

CDungeonInfo::~CDungeonInfo()
{
	Initialize();
}

void CDungeonInfo::Initialize()
{
	m_MaxDungeon = 0;
	m_InfoMap.clear();
	m_dungeonTime.clear();
#ifdef ENABLE_DUNGEON_NOTIFICATION
	m_notificationIndex.clear();
#endif
}

void CDungeonInfo::Destroy()
{
#ifdef ENABLE_DUNGEON_NOTIFICATION
	m_notificationIndex.clear();
#endif
	m_dungeonTime.clear();
}

bool CDungeonInfo::LoadDungeonInfo()
{
	using js = nlohmann::json;
	char file_name[256 + 1];
	snprintf(file_name, sizeof(file_name), "lib/json/dungeon_info.json");
	std::ifstream ifs(file_name);
	if (!ifs.is_open()) { return false; }
	try
	{
		js jf = js::parse(ifs);
		js& arr = jf["dungeon_info"];
		for (const auto& i : arr)
		{
			BYTE dungeonIndex = 0;
			TDungeonInfoTable info = {};
			i.at("dungeon_index").get_to(dungeonIndex);
			i.at("cooldown").get_to(info.cooldown);
			i.at("boss_vnum").get_to(info.bossVnum);
			i.at("ticket_vnum").get_to(info.ticketVnum);
			i.at("min_level").get_to(info.minLevel);
			i.at("max_level").get_to(info.maxLevel);
			i.at("chest_vnum").get_to(info.chestVnum);

			m_InfoMap.insert(std::make_pair(dungeonIndex, info));
		}
		ifs.close();
		m_MaxDungeon = static_cast<BYTE>(m_InfoMap.size());
	}
	catch (const std::exception& e)
	{
		TraceError("Dungeon Info error : %s - file : %s", e.what(), file_name);
		return false;
	}
	return true;
}

TDungeonInfoTable* CDungeonInfo::GetDungonInfoTable(BYTE idx)
{
	InfoMap::iterator it = m_InfoMap.find(idx);
	if (it != m_InfoMap.end())
	{
		return &it->second;
	}

	return nullptr;
}

void CDungeonInfo::TimeRequest()
{
	//Zindan sürelerini sadece ilk giriþte çekmesini saðlar
	if (m_dungeonTime.empty())
	{	
		TPacketDungeonInfoCG packet;
		packet.header = HEADER_CG_DUNGEON_INFO;
		packet.subHeader = SUB_HEADER_CG_TIME_REQUEST;

		CPythonNetworkStream& net = CPythonNetworkStream::Instance();
		if (!net.Send(sizeof(packet), &packet))
			return;
	}
}

void CDungeonInfo::DungeonLoginRequest(BYTE idx)
{
	TDungeonInfoTable* t = GetDungonInfoTable(idx);
	CPythonPlayer& player = CPythonPlayer::Instance();

	if (!t->levelControl(player.GetStatus(POINT_LEVEL)))
	{
		DungeonErrorMessage(DungeonInfoError::DUNGEON_ERROR_LEVEL);
		return;
	}

	if (player.GetItemCountByVnum(t->ticketVnum) < 1)
	{
		DungeonErrorMessage(DungeonInfoError::DUNGEON_ERROR_TICKET);
		return;
	}

	int time = TimeVectorGetTime(idx);
	if (time != 0 && time > timeGetTime())
	{
		DungeonErrorMessage(DungeonInfoError::DUNGEON_ERROR_QTIME);
		return;
	}

	CPythonNetworkStream& net = CPythonNetworkStream::instance();
	TPacketDungeonInfoCG p;
	p.header = HEADER_CG_DUNGEON_INFO;
	p.subHeader = SUB_HEADER_CG_DUNGEON_LOGIN_REQUEST;

	if (net.Send(sizeof(TPacketDungeonInfoCG), &p))
		net.Send(sizeof(BYTE), &idx);

}

void CDungeonInfo::DungeonErrorMessage(BYTE messageID)
{
	PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "DungeonInfoErrorMessage", Py_BuildValue("(i)", messageID));
}

int	CDungeonInfo::TimeVectorGetTime(BYTE idx)
{
	if (idx >= m_MaxDungeon)
		return 0;
	return m_dungeonTime[idx];
}

#ifdef ENABLE_DUNGEON_NOTIFICATION
void CDungeonInfo::NotificationCheck()
{
	if (m_notificationIndex.size() < 1)
		return;

	bool update = false;
	for (int i = 0; i < m_notificationIndex.size(); i++)
	{
		int time = TimeVectorGetTime(m_notificationIndex.at(i));
		if (time < timeGetTime())
		{
			NotificationSendMessage(m_notificationIndex.at(i));
			update = true;
		}
	}
	if (update)
	{
		NotificationUpdate();
	}
}

void CDungeonInfo::NotificationUpdate()
{
	m_notificationIndex.clear();
	for (int i = 0; i < m_dungeonTime.size(); i++)
	{
		int time = TimeVectorGetTime(i);
		if (time > timeGetTime())
		{
			m_notificationIndex.push_back(i);
		}
	}
}

void CDungeonInfo::NotificationSendMessage(BYTE idx)
{
	DWORD bossVnum = GetDungonInfoTable(idx)->bossVnum;
	PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "DungeonNotificationMessage", Py_BuildValue("(i)", bossVnum));
}
#endif

/**************************************************************
					PYTHON NETWORK STREAM
**************************************************************/

bool CPythonNetworkStream::RecvDungeonInfo()
{
	TPacketDungeonInfoGC packet;
	if (!Recv(sizeof(TPacketDungeonInfoGC), &packet))
	{
		TraceError("DungeonInfo Packet Recovery Error");
		return false;
	}

	WORD buffersize = packet.size - sizeof(TPacketDungeonInfoGC);
	bool ret = true;

	switch (packet.subHeader)
	{
		case SUB_HEADER_GC_TIME_REQUEST: { ret = RecvDungeonTime(buffersize); break; }
		case SUB_HEADER_GC_TIME_UPDATE: { ret = RecvDungeonTime(buffersize, true); break; }
		case SUB_HEADER_GC_DUNGEON_MESSAGE: { ret = RecvDungeonMessage(buffersize); break; }
		default: { TraceError("Dungon Info noting sub header %d", packet.subHeader); ret = false;  break; }
	}
	return ret;
}

bool CPythonNetworkStream::RecvDungeonTime(WORD bufferSize, bool update)
{
	BYTE dungeonCount;
	if (!Recv(sizeof(BYTE), &dungeonCount))
	{
		return false;
	}

	bufferSize -= sizeof(BYTE);

	if (!update && bufferSize % (sizeof(int) * dungeonCount) != 0)
	{
		TraceError("DungeonTime Buffer size error buffersize: %u dungeon count %u", bufferSize, dungeonCount);
		return false;
	}

	CDungeonInfo& dungeon = CDungeonInfo::instance();

	int dungeonTime;
	if (update)
	{
		if (!Recv(sizeof(int), &dungeonTime))
		{
			return false;
		}
		BYTE dungeonIndex;
		if (!Recv(sizeof(BYTE), &dungeonIndex))
		{
			return false;
		}
		if (dungeonTime != 0)
		{
			dungeonTime *= 1000;
			dungeonTime += timeGetTime();
		}
		dungeon.TimeVectorUpdateData(dungeonIndex, dungeonTime);
		dungeon.NotificationUpdate();
		return true;
	}

	dungeon.TimeVectorClear();
	dungeon.TimeVectorReserve(dungeonCount);
	for (int i = 0; i < dungeonCount; i++)
	{
		if (!Recv(sizeof(int), &dungeonTime))
		{
			return false;
		}

		if (dungeonTime != 0)
		{
			dungeonTime *= 1000;
			dungeonTime += timeGetTime();
		}
		dungeon.TimeVectorAddData(dungeonTime);
	}
	dungeon.NotificationUpdate();
	return true;
}

bool CPythonNetworkStream::RecvDungeonMessage(WORD bufferSize)
{
	BYTE messageID;
	if (!Recv(sizeof(BYTE), &messageID))
	{
		return false;
	}

	bufferSize -= sizeof(BYTE);
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "DungeonInfoErrorMessage", Py_BuildValue("(i)", messageID));
	
	return true;
}

#endif
