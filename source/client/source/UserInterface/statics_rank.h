#pragma once
#include "StdAfx.h"
#ifdef ENABLE_GLOBAL_RANKING
#include "Packet.h"
class CStatisticsRanking : public singleton<CStatisticsRanking>
{
public:
	CStatisticsRanking();
	virtual ~CStatisticsRanking();
	void Destroy();
	void WriteData(TRankingData data, TRankingMeGC data2);
	void OpenTheDoor();

	void SetNextUpdateTime(DWORD time) { m_nextUpdateTime = (timeGetTime() + (time * 1000)); }
	int GetNextUpdateTime();

protected:
	DWORD m_nextUpdateTime;
	TRankingData m_rankingData;
	TRankingMeGC m_rankingData2;

};

#endif
