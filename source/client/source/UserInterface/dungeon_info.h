#pragma once
#ifdef ENABLE_DUNGEON_INFO
#include "packet.h"

enum DungeonInfoError
{
	DUNGEON_ERROR_LEVEL,
	DUNGEON_ERROR_TICKET,
	DUNGEON_ERROR_QTIME,//Quest time
	DUNGEON_ERROR_HTIME,//Hwid time
	DUNGEON_ERROR_BUSY,//
	DUNGEON_ERROR_UNKNOWN
};

#pragma pack(1)
typedef struct SDungeonInfoTable
{
	int cooldown;
	DWORD bossVnum;
	DWORD ticketVnum;
	BYTE minLevel;
	BYTE maxLevel;
	DWORD chestVnum;
	SDungeonInfoTable()
	{
		cooldown = 0;
		bossVnum = 0;
		ticketVnum = 0;
		minLevel = 0;
		maxLevel = 0;
		chestVnum = 0;
	}
	bool levelControl(BYTE level) const
	{
		if (level < minLevel || level > maxLevel)
			return false;
		return true;
	}
}TDungeonInfoTable;
#pragma pack()

class CDungeonInfo : public singleton<CDungeonInfo>
{
public:
	using InfoMap = std::unordered_map<BYTE, TDungeonInfoTable>;
	using TimeVect = std::vector<int>;

	CDungeonInfo();
	~CDungeonInfo();
	void Destroy();
	void Initialize();
	bool LoadDungeonInfo();

	BYTE GetMaxDungeon() { return m_MaxDungeon; }

	TDungeonInfoTable* GetDungonInfoTable(BYTE idx);
	void DungeonLoginRequest(BYTE idx);
	void DungeonErrorMessage(BYTE messageID);

	//Time
	void TimeRequest();
	inline void TimeVectorClear() { m_dungeonTime.clear(); }
	inline void TimeVectorReserve(BYTE count) { m_dungeonTime.reserve(count); }
	inline void TimeVectorAddData(int time) { m_dungeonTime.push_back(time); }
	inline void TimeVectorUpdateData(BYTE idx,int time) { m_dungeonTime[idx] = time; }
	int	TimeVectorGetTime(BYTE idx);

private:
	InfoMap m_InfoMap;
	BYTE m_MaxDungeon;
	TimeVect m_dungeonTime;

#ifdef ENABLE_DUNGEON_NOTIFICATION
public:
	void AddNotificationIndex(BYTE idx) { m_notificationIndex.push_back(idx); }
	void NotificationCheck();
	void NotificationUpdate();
	void NotificationSendMessage(BYTE idx);
private:
	std::vector<BYTE>m_notificationIndex;
#endif
};

#endif
