#include "StdAfx.h"
#ifdef ENABLE_GLOBAL_RANKING
#include "statics_rank.h"
#include "PythonApplication.h"

CStatisticsRanking::CStatisticsRanking()
{
	Destroy();
}

CStatisticsRanking::~CStatisticsRanking()
{
	Destroy();
}

void CStatisticsRanking::Destroy()
{
	memset(&m_rankingData, 0, sizeof(m_rankingData));
	memset(&m_rankingData2, 0, sizeof(m_rankingData2));
	m_nextUpdateTime = 0;
}

void CStatisticsRanking::WriteData(TRankingData data, TRankingMeGC data2)
{
	memcpy(&m_rankingData, &data, sizeof(TRankingData));
	memcpy(&m_rankingData2, &data2, sizeof(TRankingMeGC));
}

int CStatisticsRanking::GetNextUpdateTime()
{
	if (m_nextUpdateTime == 0)
		return 0;

	return (m_nextUpdateTime - timeGetTime()) / 1000;
}

void CStatisticsRanking::OpenTheDoor()
{
	for (int i = 0; i < RANKING_MAX; i++)
	{
		for (int y = 0; y < RANKING_MAX_PLAYER_COUNT; y++)
		{
			if (m_rankingData.rank[i][y].llScore == 0)
				break;

			PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "BINARY_RankingDataCountry", Py_BuildValue("(iii)", i, m_rankingData.rank[i][y].bOrder, m_rankingData.rank[i][y].country));
			PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "BINARY_RankingData", Py_BuildValue("(iisii)", i, m_rankingData.rank[i][y].bOrder, m_rankingData.rank[i][y].szPlayerName, m_rankingData.rank[i][y].llScore, m_rankingData.rank[i][y].playerRace));
		}
		PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "BINARY_RankingDataCountry", Py_BuildValue("(iii)", i, 11, m_rankingData2.country));
		PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "BINARY_RankingData", Py_BuildValue("(iisii)", i, m_rankingData2.rank.order[i] + 11, m_rankingData2.playerName, m_rankingData2.rank.value[i], m_rankingData2.playerRace));
	}

	PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "BINARY_OpenRanking", Py_BuildValue("()"));
}
/**********************PYTHON MODULE***********************************************/
PyObject* rankingUpdateTime(PyObject* poSelf, PyObject* poArgs)
{
	int updatetime = CStatisticsRanking::Instance().GetNextUpdateTime();
	//TraceError("%u time", updatetime);
	return Py_BuildValue("i", updatetime);
}

void initStaticsRank() 
{
	static PyMethodDef s_methods[] =
	{
		{ "updatetime", rankingUpdateTime, METH_VARARGS },
		{nullptr, nullptr, 0 },
	};
	PyObject* poModule = Py_InitModule("ranking", s_methods);
}

#endif