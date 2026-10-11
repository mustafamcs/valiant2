#include "StdAfx.h"
#include "PythonNetworkStream.h"
#include "Packet.h"
#include "PythonApplication.h"
#include "NetworkActorManager.h"

#include "AbstractPlayer.h"
#include "../EterFSLib/FileSystemIncl.hpp"

void CPythonNetworkStream::EnableChatInsultFilter(bool isEnable)
{
	m_isEnableChatInsultFilter = isEnable;
}

void CPythonNetworkStream::__FilterInsult(char* szLine, UINT uLineLen)
{
	m_kInsultChecker.FilterInsult(szLine, uLineLen);
}

bool CPythonNetworkStream::IsChatInsultIn(const char* c_szMsg)
{
	if (m_isEnableChatInsultFilter)
		return false;

	return IsInsultIn(c_szMsg);
}

bool CPythonNetworkStream::IsInsultIn(const char* c_szMsg)
{
	return m_kInsultChecker.IsInsultIn(c_szMsg, strlen(c_szMsg));
}

bool CPythonNetworkStream::LoadInsultList(const char* c_szInsultListFileName)
{
	auto file = PackGet(c_szInsultListFileName);
	if (!file)
		return false;

	CMemoryTextFileLoader kMemTextFileLoader;
	kMemTextFileLoader.Bind(file->get_size(), file->get_data());

	m_kInsultChecker.Clear();
	for (DWORD dwLineIndex = 0; dwLineIndex < kMemTextFileLoader.GetLineCount(); ++dwLineIndex)
	{
		const std::string& c_rstLine = kMemTextFileLoader.GetLineString(dwLineIndex);
		m_kInsultChecker.AppendInsult(c_rstLine);
	}
	return true;
}

bool CPythonNetworkStream::LoadConvertTable(DWORD dwEmpireID, const char* c_szFileName)
{
	if (dwEmpireID < 1 || dwEmpireID >= 4)
		return false;

	auto file = PackGet(c_szFileName);
	if (!file)
		return false;

	DWORD dwEngCount = 26;
	DWORD dwHanCount = (0xc8 - 0xb0 + 1) * (0xfe - 0xa1 + 1);
	DWORD dwHanSize = dwHanCount * 2;
	DWORD dwFileSize = dwEngCount * 2 + dwHanSize;

	if (file->get_size() < dwFileSize)
		return false;

	char* pcData = (char*)file->get_data();

	STextConvertTable& rkTextConvTable = m_aTextConvTable[dwEmpireID - 1];
	memcpy(rkTextConvTable.acUpper, pcData, dwEngCount); pcData += dwEngCount;
	memcpy(rkTextConvTable.acLower, pcData, dwEngCount); pcData += dwEngCount;
	memcpy(rkTextConvTable.aacHan, pcData, dwHanSize);
	return true;
}

// Loading ---------------------------------------------------------------------------
void CPythonNetworkStream::LoadingPhase()
{
	TPacketHeader header;

	if (!CheckPacket(&header))
		return;

#if defined(_DEBUG) && defined(ENABLE_PRINT_RECV_PACKET_DEBUG)
	Tracenf("RECV HEADER : %u , phase num %u ", header, m_gamePhase);
#endif

	switch (header)
	{
	case HEADER_GC_PHASE:
		if (RecvPhasePacket())
			return;
		break;

	case HEADER_GC_MAIN_CHARACTER:
		if (RecvMainCharacter())
			return;
		break;

		// SUPPORT_BGM
	case HEADER_GC_MAIN_CHARACTER2_EMPIRE:
		if (RecvMainCharacter2_EMPIRE())
			return;
		break;

	case HEADER_GC_CHARACTER_UPDATE:
		if (RecvCharacterUpdatePacket())
			return;
		break;

	case HEADER_GC_PLAYER_POINTS:
		if (__RecvPlayerPoints())
			return;
		break;

	case HEADER_GC_PLAYER_POINT_CHANGE:
		if (RecvPointChange())
			return;
		break;

	case HEADER_GC_ITEM_SET:
		if (RecvItemSetPacket())
			return;
		break;

	case HEADER_GC_PING:
		if (RecvPingPacket())
			return;
		break;

	case HEADER_GC_QUICKSLOT_ADD:
		if (RecvQuickSlotAddPacket())
			return;
		break;

#ifdef ENABLE_OFFLINE_SHOP
	case HEADER_GC_NEW_OFFLINESHOP:
		RecvOfflineshopPacket();
		return;
#endif

	default:
		GamePhase();
		return;
		break;
	}

	RecvErrorPacket(header);
}
#if defined(ENABLE_CLIENT_OPTIMISATION)
#include "PythonOptimizationBoost.h"
#endif
void CPythonNetworkStream::SetLoadingPhase()
{
	if (m_gamePhase != GAME_PHASE_LOADING)
		m_phaseLeaveFunc.Run();

	m_gamePhase = GAME_PHASE_LOADING;

	m_phaseProcessFunc.Set(this, &CPythonNetworkStream::LoadingPhase);

#if defined(ENABLE_CLIENT_OPTIMISATION)
	CPythonOptimizationBoost::Instance().Load();
#endif

	m_phaseLeaveFunc.Set(this, &CPythonNetworkStream::__LeaveLoadingPhase);

	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();
	rkPlayer.Clear();

	CFlyingManager::Instance().DeleteAllInstances();
	CEffectManager::Instance().DeleteAllInstances();

	__DirectEnterMode_Initialize();
}

bool CPythonNetworkStream::RecvMainCharacter()
{
	TPacketGCMainCharacter MainChrPacket;
	if (!Recv(sizeof(TPacketGCMainCharacter), &MainChrPacket))
		return false;

	m_dwMainActorVID = MainChrPacket.dwVID;
	m_dwMainActorRace = MainChrPacket.wRaceNum;
	m_dwMainActorEmpire = MainChrPacket.empire; /*@Lightwork5 */
	m_dwMainActorSkillGroup = MainChrPacket.bySkillGroup;

	m_rokNetActorMgr->SetMainActorVID(m_dwMainActorVID);

	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();
	rkPlayer.SetName(MainChrPacket.szName);
	rkPlayer.SetMainCharacterIndex(GetMainActorVID());
	Warp(MainChrPacket.lX, MainChrPacket.lY);/*@Lightwork6 */
	return true;
}

// SUPPORT_BGM
bool CPythonNetworkStream::RecvMainCharacter2_EMPIRE()
{
	TPacketGCMainCharacter2_EMPIRE mainChrPacket;
	if (!Recv(sizeof(mainChrPacket), &mainChrPacket))
		return false;

	m_dwMainActorVID = mainChrPacket.dwVID;
	m_dwMainActorRace = mainChrPacket.wRaceNum;
	m_dwMainActorEmpire = mainChrPacket.byEmpire;
	m_dwMainActorSkillGroup = mainChrPacket.bySkillGroup;

	m_rokNetActorMgr->SetMainActorVID(m_dwMainActorVID);

	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();
	rkPlayer.SetName(mainChrPacket.szName);
	rkPlayer.SetMainCharacterIndex(GetMainActorVID());
	Warp(mainChrPacket.lX, mainChrPacket.lY);/*@Lightwork6 */
	return true;
}


bool CPythonNetworkStream::__RecvPlayerPoints()
{
	TPacketGCPoints PointsPacket;

	if (!Recv(sizeof(TPacketGCPoints), &PointsPacket))
		return false;

	for (DWORD i = 0; i < POINT_MAX_NUM; ++i)
		CPythonPlayer::Instance().SetStatus(i, PointsPacket.points[i]);

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshStatus", Py_BuildValue("()"));
	return true;
}

void CPythonNetworkStream::StartGame()
{
	m_isStartGame = TRUE;
}

bool CPythonNetworkStream::SendEnterGame()
{
	TPacketCGEnterFrontGame EnterFrontGamePacket;

	EnterFrontGamePacket.header = HEADER_CG_ENTERGAME;

	if (!Send(sizeof(EnterFrontGamePacket), &EnterFrontGamePacket))
	{
		Tracen("Send EnterFrontGamePacket");
		return false;
	}

	if (!SendSequence())
		return false;

	__SendInternalBuffer();
	return true;
}