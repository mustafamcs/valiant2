#include "StdAfx.h"
#include "PythonNetworkStream.h"
#include "Packet.h"

#include "PythonGuild.h"
#include "PythonCharacterManager.h"
#include "PythonPlayer.h"
#include "PythonBackground.h"
#include "PythonMiniMap.h"
#include "PythonTextTail.h"
#include "PythonItem.h"
#include "PythonChat.h"
#include "PythonShop.h"
#include "PythonExchange.h"
#include "PythonQuest.h"
#include "PythonEventManager.h"
#include "PythonMessenger.h"
#include "PythonApplication.h"

#include "../EterFSLib/FileSystemIncl.hpp"
#include "../gamelib/ItemManager.h"

#include "AbstractApplication.h"
#include "AbstractCharacterManager.h"
#include "InstanceBase.h"

#ifdef ENABLE_CUBE_RENEWAL_WORLDARD
#include "PythonCubeRenewal.h"
#endif
#ifdef ENABLE_DUNGEON_NOTIFICATION
#include "dungeon_info.h"
#endif
#include "ProcessCRC.h"

#ifdef ENABLE_CLIENT_OPTIMISATION
#include "PythonOptimizationBoost.h"
#endif

BOOL gs_bEmpireLanuageEnable = TRUE;

void CPythonNetworkStream::__RefreshAlignmentWindow()
{
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshAlignment", Py_BuildValue("()"));
}

void CPythonNetworkStream::__RefreshTargetBoardByVID(DWORD dwVID)
{
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshTargetBoardByVID", Py_BuildValue("(i)", dwVID));
}

void CPythonNetworkStream::__RefreshTargetBoardByName(const char* c_szName)
{
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshTargetBoardByName", Py_BuildValue("(s)", c_szName));
}

void CPythonNetworkStream::__RefreshTargetBoard()
{
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshTargetBoard", Py_BuildValue("()"));
}

void CPythonNetworkStream::__RefreshGuildWindowGradePage()
{
	m_isRefreshGuildWndGradePage = true;
}

void CPythonNetworkStream::__RefreshGuildWindowSkillPage()
{
	m_isRefreshGuildWndSkillPage = true;
}

void CPythonNetworkStream::__RefreshGuildWindowMemberPageGradeComboBox()
{
	m_isRefreshGuildWndMemberPageGradeComboBox = true;
}

void CPythonNetworkStream::__RefreshGuildWindowMemberPage()
{
	m_isRefreshGuildWndMemberPage = true;
}

void CPythonNetworkStream::__RefreshGuildWindowBoardPage()
{
	m_isRefreshGuildWndBoardPage = true;
}

void CPythonNetworkStream::__RefreshGuildWindowInfoPage()
{
	m_isRefreshGuildWndInfoPage = true;
}

void CPythonNetworkStream::__RefreshMessengerWindow()
{
	m_isRefreshMessengerWnd = true;
}

void CPythonNetworkStream::__RefreshSafeboxWindow()
{
	m_isRefreshSafeboxWnd = true;
}

void CPythonNetworkStream::__RefreshMallWindow()
{
	m_isRefreshMallWnd = true;
}

void CPythonNetworkStream::__RefreshSkillWindow()
{
#ifdef ENABLE_REFRESH_CONTROL
	if (m_RefreshControl[REFRESH_SKILL])
	{
		m_isRefreshSkillWnd = true;
	}
#else
	m_isRefreshSkillWnd = true;
#endif
}

void CPythonNetworkStream::__RefreshExchangeWindow()
{
	m_isRefreshExchangeWnd = true;
}

void CPythonNetworkStream::__RefreshStatus()
{
#ifdef ENABLE_REFRESH_CONTROL
	if (m_RefreshControl[REFRESH_POINT])
	{
		m_isRefreshStatus = true;
	}
#else
	m_isRefreshStatus = true;
#endif
}

void CPythonNetworkStream::__RefreshCharacterWindow()
{
	m_isRefreshCharacterWnd = true;
}

void CPythonNetworkStream::__RefreshInventoryWindow()
{
#ifdef ENABLE_REFRESH_CONTROL
	if (m_RefreshControl[REFRESH_INVENTORY])
	{
		m_isRefreshInventoryWnd = true;
	}
#else
	m_isRefreshInventoryWnd = true;
#endif
}

void CPythonNetworkStream::__RefreshEquipmentWindow()
{
	m_isRefreshEquipmentWnd = true;
}

void CPythonNetworkStream::__SetGuildID(DWORD id)
{
	if (m_dwGuildID != id)
	{
		m_dwGuildID = id;
		IAbstractPlayer& rkPlayer = IAbstractPlayer::GetSingleton();

		for (int i = 0; i < PLAYER_PER_ACCOUNT4; ++i)
			if (!strncmp(m_akSimplePlayerInfo[i].szName, rkPlayer.GetName(), CHARACTER_NAME_MAX_LEN))
			{
				m_adwGuildID[i] = id;

				std::string  guildName;
				if (CPythonGuild::Instance().GetGuildName(id, &guildName))
				{
					m_astrGuildName[i] = guildName;
				}
				else
				{
					m_astrGuildName[i] = "";
				}
			}
	}
}

struct PERF_PacketInfo
{
	DWORD dwCount;
	DWORD dwTime;

	PERF_PacketInfo()
	{
		dwCount = 0;
		dwTime = 0;
	}
};

/* Game Phase */
void CPythonNetworkStream::GamePhase()
{
	if (!m_kQue_stHack.empty())
	{
		__SendHack(m_kQue_stHack.front().c_str());
		m_kQue_stHack.pop_front();
	}

	TPacketHeader header = 0;
	bool ret = true;

	const DWORD MAX_RECV_COUNT = 32; // @warme669 default 8 @lightwork88
	const DWORD SAFE_RECV_BUFSIZE = 8192;
	DWORD dwRecvCount = 0;

	while (ret)
	{
		if (dwRecvCount++ >= MAX_RECV_COUNT - 1 && GetRecvBufferSize() < SAFE_RECV_BUFSIZE
			&& m_gamePhase == GAME_PHASE_GAME)
			break;

		if (!CheckPacket(&header))
			break;

#if defined(_DEBUG) && defined(ENABLE_PRINT_RECV_PACKET_DEBUG)
		Tracenf("RECV HEADER : %u , phase %u ", header, m_gamePhase);
#endif
		// TraceError("RECV HEADER : %u , phase %s ", header, m_gamePhase.c_str());

		switch (header)
		{
		case HEADER_GC_WARP:
			ret = RecvWarpPacket();
			break;

		case HEADER_GC_PHASE:
			ret = RecvPhasePacket();
			return;
			break;

		case HEADER_GC_PVP:
			ret = RecvPVPPacket();
			break;

		case HEADER_GC_DUEL_START:
			ret = RecvDuelStartPacket();
			break;

		case HEADER_GC_CHARACTER_ADD:
			ret = RecvCharacterAppendPacket();
			break;

		case HEADER_GC_CHAR_ADDITIONAL_INFO:
			ret = RecvCharacterAdditionalInfo();
			break;

		case HEADER_GC_CHARACTER_UPDATE:
			ret = RecvCharacterUpdatePacket();
			break;

		case HEADER_GC_CHARACTER_DEL:
			ret = RecvCharacterDeletePacket();
			break;

		case HEADER_GC_CHAT:
			ret = RecvChatPacket();
			break;

		case HEADER_GC_SYNC_POSITION:
			ret = RecvSyncPositionPacket();
			break;

		case HEADER_GC_OWNERSHIP:
			ret = RecvOwnerShipPacket();
			break;

		case HEADER_GC_WHISPER:
			ret = RecvWhisperPacket();
			break;

		case HEADER_GC_CHARACTER_MOVE:
			ret = RecvCharacterMovePacket();
			break;

			// Position
		case HEADER_GC_CHARACTER_POSITION:
			ret = RecvCharacterPositionPacket();
			break;

			// Battle Packet
		case HEADER_GC_STUN:
			ret = RecvStunPacket();
			break;

		case HEADER_GC_DEAD:
			ret = RecvDeadPacket();
			break;

		case HEADER_GC_PLAYER_POINT_CHANGE:
			ret = RecvPointChange();
			break;

			// item packet.
		case HEADER_GC_ITEM_SET:
			ret = RecvItemSetPacket();
			break;

		case HEADER_GC_ITEM_SET2:
			ret = RecvItemSetPacket2();
			break;

		case HEADER_GC_ITEM_USE:
			ret = RecvItemUsePacket();
			break;

		case HEADER_GC_ITEM_UPDATE:
			ret = RecvItemUpdatePacket();
			break;

		case HEADER_GC_ITEM_GROUND_ADD:
			ret = RecvItemGroundAddPacket();
			break;

		case HEADER_GC_ITEM_GROUND_DEL:
			ret = RecvItemGroundDelPacket();
			break;

		case HEADER_GC_ITEM_OWNERSHIP:
			ret = RecvItemOwnership();
			break;

		case HEADER_GC_QUICKSLOT_ADD:
			ret = RecvQuickSlotAddPacket();
			break;

		case HEADER_GC_QUICKSLOT_DEL:
			ret = RecvQuickSlotDelPacket();
			break;

		case HEADER_GC_QUICKSLOT_SWAP:
			ret = RecvQuickSlotMovePacket();
			break;

		case HEADER_GC_MOTION:
			ret = RecvMotionPacket();
			break;

		case HEADER_GC_SHOP:
			ret = RecvShopPacket();
			break;

		case HEADER_GC_SHOP_SIGN:
			ret = RecvShopSignPacket();
			break;

		case HEADER_GC_EXCHANGE:
			ret = RecvExchangePacket();
			break;

		case HEADER_GC_QUEST_INFO:
			ret = RecvQuestInfoPacket();
			break;

		case HEADER_GC_REQUEST_MAKE_GUILD:
			ret = RecvRequestMakeGuild();
			break;

		case HEADER_GC_PING:
			ret = RecvPingPacket();
			break;

		case HEADER_GC_SCRIPT:
			ret = RecvScriptPacket();
			break;

		case HEADER_GC_QUEST_CONFIRM:
			ret = RecvQuestConfirmPacket();
			break;

		case HEADER_GC_TARGET:
			ret = RecvTargetPacket();
			break;

		case HEADER_GC_DAMAGE_INFO:
			ret = RecvDamageInfoPacket();
			break;

		case HEADER_GC_MOUNT:
			ret = RecvMountPacket();
			break;

		case HEADER_GC_CHANGE_SPEED:
			ret = RecvChangeSpeedPacket();
			break;

		case HEADER_GC_PLAYER_POINTS:
			ret = __RecvPlayerPoints();
			break;

		case HEADER_GC_CREATE_FLY:
			ret = RecvCreateFlyPacket();
			break;

		case HEADER_GC_FLY_TARGETING:
			ret = RecvFlyTargetingPacket();
			break;

		case HEADER_GC_ADD_FLY_TARGETING:
			ret = RecvAddFlyTargetingPacket();
			break;

		case HEADER_GC_SKILL_LEVEL:
			ret = RecvSkillLevel();
			break;

		case HEADER_GC_SKILL_LEVEL_NEW:
			ret = RecvSkillLevelNew();
			break;

		case HEADER_GC_MESSENGER:
			ret = RecvMessenger();
			break;

		case HEADER_GC_GUILD:
			ret = RecvGuild();
			break;

		case HEADER_GC_PARTY_INVITE:
			ret = RecvPartyInvite();
			break;

		case HEADER_GC_PARTY_ADD:
			ret = RecvPartyAdd();
			break;

		case HEADER_GC_PARTY_UPDATE:
			ret = RecvPartyUpdate();
			break;

		case HEADER_GC_PARTY_REMOVE:
			ret = RecvPartyRemove();
			break;

		case HEADER_GC_PARTY_LINK:
			ret = RecvPartyLink();
			break;

		case HEADER_GC_PARTY_UNLINK:
			ret = RecvPartyUnlink();
			break;

		case HEADER_GC_PARTY_PARAMETER:
			ret = RecvPartyParameter();
			break;

		case HEADER_GC_SAFEBOX_SET:
			ret = RecvSafeBoxSetPacket();
			break;

		case HEADER_GC_SAFEBOX_DEL:
			ret = RecvSafeBoxDelPacket();
			break;

		case HEADER_GC_SAFEBOX_WRONG_PASSWORD:
			ret = RecvSafeBoxWrongPasswordPacket();
			break;

		case HEADER_GC_SAFEBOX_SIZE:
			ret = RecvSafeBoxSizePacket();
			break;

		case HEADER_GC_FISHING:
			ret = RecvFishing();
			break;

		case HEADER_GC_DUNGEON:
			ret = RecvDungeon();
			break;

		case HEADER_GC_TIME:
			ret = RecvTimePacket();
			break;

		case HEADER_GC_WALK_MODE:
			ret = RecvWalkModePacket();
			break;

		case HEADER_GC_CHANGE_SKILL_GROUP:
			ret = RecvChangeSkillGroupPacket();
			break;

		case HEADER_GC_REFINE_INFORMATION:
			ret = RecvRefineInformationPacket();
			break;

		case HEADER_GC_REFINE_INFORMATION_NEW:
			ret = RecvRefineInformationPacketNew();
			break;

		case HEADER_GC_SEPCIAL_EFFECT:
			ret = RecvSpecialEffect();
			break;

		case HEADER_GC_NPC_POSITION:
			ret = RecvNPCList();
			break;

		case HEADER_GC_CHANNEL:
			ret = RecvChannelPacket();
			break;

		case HEADER_GC_VIEW_EQUIP:
			ret = RecvViewEquipPacket();
			break;

		case HEADER_GC_LAND_LIST:
			ret = RecvLandPacket();
			break;

		case HEADER_GC_TARGET_CREATE_NEW:
			ret = RecvTargetCreatePacketNew();
			break;

		case HEADER_GC_TARGET_UPDATE:
			ret = RecvTargetUpdatePacket();
			break;

		case HEADER_GC_TARGET_DELETE:
			ret = RecvTargetDeletePacket();
			break;

		case HEADER_GC_AFFECT_ADD:
			ret = RecvAffectAddPacket();
			break;

		case HEADER_GC_AFFECT_REMOVE:
			ret = RecvAffectRemovePacket();
			break;

		case HEADER_GC_MALL_OPEN:
			ret = RecvMallOpenPacket();
			break;

		case HEADER_GC_MALL_SET:
			ret = RecvMallItemSetPacket();
			break;

		case HEADER_GC_MALL_DEL:
			ret = RecvMallItemDelPacket();
			break;

		case HEADER_GC_LOVER_INFO:
			ret = RecvLoverInfoPacket();
			break;

		case HEADER_GC_LOVE_POINT_UPDATE:
			ret = RecvLovePointUpdatePacket();
			break;

		case HEADER_GC_DIG_MOTION:
			ret = RecvDigMotionPacket();
			break;

		case HEADER_GC_HANDSHAKE:
			RecvHandshakePacket();
			return;
			break;

		case HEADER_GC_HANDSHAKE_OK:
			RecvHandshakeOKPacket();
			return;
			break;

#ifdef _IMPROVED_PACKET_ENCRYPTION_
		case HEADER_GC_KEY_AGREEMENT:
			RecvKeyAgreementPacket();
			return;
			break;

		case HEADER_GC_KEY_AGREEMENT_COMPLETED:
			RecvKeyAgreementCompletedPacket();
			return;
			break;
#endif

		case HEADER_GC_SPECIFIC_EFFECT:
			ret = RecvSpecificEffect();
			break;

		case HEADER_GC_SPECIFIC_EFFECT2:
			ret = RecvSpecificEffect2();
			break;

		case HEADER_GC_DRAGON_SOUL_REFINE:
			ret = RecvDragonSoulRefine();
			break;
#ifdef ENABLE_MINI_GAME_OKEY_NORMAL
		case HEADER_GC_OKEY_CARD:
			ret = RecvMiniGameOkeyCardPacket();
			break;
#endif
#ifdef ENABLE_MINI_GAME_BNW
		case HEADER_GC_MINIGAME_BNW:
			ret = RecvMinigameBnw();
			break;
#endif
#ifdef ENABLE_MINI_GAME_CATCH_KING
		case HEADER_GC_MINI_GAME_CATCH_KING:
			ret = RecvMiniGameCatchKingPacket();
			break;
#endif
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
		case HEADER_GC_ACCE:
			ret = RecvAccePacket();
			break;
#endif

#ifdef ENABLE_TARGET_INFORMATION_SYSTEM
#ifndef ENABLE_TARGET_INFORMATION_RENEWAL
		case HEADER_GC_TARGET_INFO:
			ret = RecvTargetInfoPacket();
			break;
#endif
#endif

#ifdef ENABLE_CUBE_RENEWAL_WORLDARD
		case HEADER_GC_CUBE_RENEWAL:
			ret = RecvCubeRenewalPacket();
			break;
#endif

#ifdef ENABLE_DS_SET_BONUS
		case HEADER_GC_DS_TABLE:
			ret = RecvDSTablePacket();
			break;
#endif

#ifdef ENABLE_OFFLINE_SHOP
		case HEADER_GC_NEW_OFFLINESHOP:
			ret = RecvOfflineshopPacket();
			break;
#endif

#ifdef ENABLE_SWITCHBOT
		case HEADER_GC_SWITCHBOT:
			ret = RecvSwitchbotPacket();
			break;
#endif
#ifdef ENABLE_REFRESH_CONTROL
		case HEADER_GC_REFRESH_CONTROL:
			ret = RecvRefreshControl();
			break;
#endif
#ifdef ENABLE_GLOBAL_RANKING
		case HEADER_GC_GLOBAL_RANKING:
			ret = RecvGlobalRankingPacket();
			break;
#endif
#ifdef ENABLE_BIOLOG_SYSTEM
		case HEADER_GC_BIOLOG:
			ret = RecvBiologPacket();
			break;
#endif
#ifdef ENABLE_CHAR_SETTINGS
		case HEADER_GC_CHAR_SETTINGS:
			ret = RecvCharSettings();
			break;
#endif
#ifdef ENABLE_IN_GAME_LOG_SYSTEM
		case HEADER_GC_IN_GAME_LOG:
			ret = RecvInGameLog();
			break;
#endif
#ifdef ENABLE_PM_ALL_SEND_SYSTEM
		case HEADER_GC_BULK_WHISPER:
			ret = RecvBulkWhisperPacket();
			break;
#endif
#ifdef ENABLE_DUNGEON_INFO
		case HEADER_GC_DUNGEON_INFO:
			ret = RecvDungeonInfo();
			break;
#endif

#ifdef ENABLE_EVENT_MANAGER
		case HEADER_GC_EVENT_MANAGER:
			ret = RecvEventManager();
			break;
#endif

#ifdef ENABLE_ITEMSHOP
		case HEADER_GC_ITEMSHOP:
			ret = RecvItemShop();
			break;
#endif

#ifdef ENABLE_AURA_SYSTEM
		case HEADER_GC_AURA:
			ret = RecvAuraPacket();
			break;
#endif
#ifdef ENABLE_NEW_PET_SYSTEM
		case HEADER_GC_NEW_PET:
			ret = RecvNewPet();
			break;
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
		case HEADER_GC_REQUEST_CHANGE_LANGUAGE:
			ret = RecvRequestChangeLanguage();
			break;
#endif
#ifdef ENABLE_EXTENDED_WHISPER_DETAILS
		case HEADER_GC_WHISPER_DETAILS:
			ret = RecvWhisperDetails();
			break;
#endif
#ifdef ENABLE_EXTENDED_BATTLE_PASS
		case HEADER_GC_EXT_BATTLE_PASS_OPEN:
			ret = RecvExtBattlePassOpenPacket();
			break;

		case HEADER_GC_EXT_BATTLE_PASS_GENERAL_INFO:
			ret = RecvExtBattlePassGeneralInfoPacket();
			break;

		case HEADER_GC_EXT_BATTLE_PASS_MISSION_INFO:
			ret = RecvExtBattlePassMissionInfoPacket();
			break;

		case HEADER_GC_EXT_BATTLE_PASS_MISSION_UPDATE:
			ret = RecvExtBattlePassMissionUpdatePacket();
			break;

		case HEADER_GC_EXT_BATTLE_PASS_SEND_RANKING:
			ret = RecvExtBattlePassRankingPacket();
			break;
#endif
#ifdef ENABLE_6TH_7TH_ATTR
		case HEADER_GC_OPEN_67_ATTR:
			ret = Recv67AttrOpenPacket();
			break;
#endif
#ifdef ENABLE_NEW_CHAT
		case HEADER_GC_NEW_CHAT:
			ret = RecvNewChatPacket();
			break;
#endif
#ifdef ENABLE_BUFFI_SYSTEM
		case HEADER_GC_BUFFI:
			ret = RecvBuffiSkillPacket();
			break;
#endif
		default:
			ret = RecvDefaultPacket(header);
			break;
		}
	}

	if (!ret)
		RecvErrorPacket(header);

	static DWORD s_nextRefreshTime = ELTimer_GetMSec();

	DWORD curTime = ELTimer_GetMSec();
	if (s_nextRefreshTime > curTime)
		return;

	if (m_isRefreshCharacterWnd)
	{
		m_isRefreshCharacterWnd = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshCharacter", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshEquipmentWnd)
	{
		m_isRefreshEquipmentWnd = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshEquipment", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshInventoryWnd == true)
	{
		m_isRefreshInventoryWnd = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshInventory", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshExchangeWnd)
	{
		m_isRefreshExchangeWnd = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshExchange", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshSkillWnd)
	{
		m_isRefreshSkillWnd = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshSkill", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshSafeboxWnd)
	{
		m_isRefreshSafeboxWnd = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshSafebox", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshMallWnd)
	{
		m_isRefreshMallWnd = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshMall", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshStatus)
	{
		m_isRefreshStatus = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshStatus", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshMessengerWnd)
	{
		m_isRefreshMessengerWnd = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshMessenger", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshGuildWndInfoPage)
	{
		m_isRefreshGuildWndInfoPage = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshGuildInfoPage", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshGuildWndBoardPage)
	{
		m_isRefreshGuildWndBoardPage = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshGuildBoardPage", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshGuildWndMemberPage)
	{
		m_isRefreshGuildWndMemberPage = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshGuildMemberPage", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshGuildWndMemberPageGradeComboBox)
	{
		m_isRefreshGuildWndMemberPageGradeComboBox = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshGuildMemberPageGradeComboBox", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshGuildWndSkillPage)
	{
		m_isRefreshGuildWndSkillPage = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshGuildSkillPage", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}

	if (m_isRefreshGuildWndGradePage)
	{
		m_isRefreshGuildWndGradePage = false;
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshGuildGradePage", Py_BuildValue("()"));
		s_nextRefreshTime = curTime + 300;
	}
#ifdef ENABLE_DUNGEON_NOTIFICATION
	CDungeonInfo::Instance().NotificationCheck();
#endif
#ifdef ENABLE_METIN_QUEUE
	if (CPythonPlayer::Instance().GetQueue())
	{
		CPythonPlayer::Instance().UpdateQueue();
		s_nextRefreshTime = curTime + 300;
	}
#endif
}

void CPythonNetworkStream::__InitializeGamePhase()
{
	__ServerTimeSync_Initialize();

	m_isRefreshStatus = false;
	m_isRefreshCharacterWnd = false;
	m_isRefreshEquipmentWnd = false;
	m_isRefreshInventoryWnd = false;
	m_isRefreshExchangeWnd = false;
	m_isRefreshSkillWnd = false;
	m_isRefreshSafeboxWnd = false;
	m_isRefreshMallWnd = false;
	m_isRefreshMessengerWnd = false;
	m_isRefreshGuildWndInfoPage = false;
	m_isRefreshGuildWndBoardPage = false;
	m_isRefreshGuildWndMemberPage = false;
	m_isRefreshGuildWndMemberPageGradeComboBox = false;
	m_isRefreshGuildWndSkillPage = false;
	m_isRefreshGuildWndGradePage = false;
	m_EmoticonStringVector.clear();
#ifdef ENABLE_REFRESH_CONTROL
	memset(&m_RefreshControl, true, sizeof(m_RefreshControl));
#endif
	m_pInstTarget = NULL;
}

void CPythonNetworkStream::Warp(LONG lGlobalX, LONG lGlobalY)
{
	CPythonBackground& rkBgMgr = CPythonBackground::Instance();
	rkBgMgr.Destroy();
	rkBgMgr.Create();
	rkBgMgr.Warp(lGlobalX, lGlobalY);
	rkBgMgr.RefreshShadowLevel();
	LONG lLocalX = lGlobalX;
	LONG lLocalY = lGlobalY;
	__GlobalPositionToLocalPosition(lLocalX, lLocalY);
	float fHeight = CPythonBackground::Instance().GetHeight(float(lLocalX), float(lLocalY));
	IAbstractApplication& rkApp = IAbstractApplication::GetSingleton();
	rkApp.SetCenterPosition(float(lLocalX), float(lLocalY), fHeight);
	__ShowMapName(lLocalX, lLocalY);
#ifdef ENABLE_CLIENT_OPTIMISATION
	StartGame();
#endif
}

void CPythonNetworkStream::__ShowMapName(LONG lLocalX, LONG lLocalY)
{
	const std::string& c_rstrMapFileName = CPythonBackground::Instance().GetWarpMapName();
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ShowMapName", Py_BuildValue("(sii)", c_rstrMapFileName.c_str(), lLocalX, lLocalY));
}

void CPythonNetworkStream::__LeaveGamePhase()
{
	CInstanceBase::ClearPVPKeySystem();
	__ClearNetworkActorManager();
	m_bComboSkillFlag = FALSE;
	IAbstractCharacterManager& rkChrMgr = IAbstractCharacterManager::GetSingleton();
	rkChrMgr.Destroy();
	CPythonItem& rkItemMgr = CPythonItem::Instance();
	rkItemMgr.Destroy();

#ifdef ENABLE_OFFLINE_SHOP
#	ifdef ENABLE_SHOP_IN_CITIES
	CPythonOfflineshop::instance().DeleteEntities();
#	endif
#endif
}

void CPythonNetworkStream::SetGamePhase()
{
	if (m_gamePhase != GAME_PHASE_GAME)
		m_phaseLeaveFunc.Run();

	m_gamePhase = GAME_PHASE_GAME;

	m_phaseProcessFunc.Set(this, &CPythonNetworkStream::GamePhase);
	m_phaseLeaveFunc.Set(this, &CPythonNetworkStream::__LeaveGamePhase);
	IAbstractPlayer& rkPlayer = IAbstractPlayer::GetSingleton();
	rkPlayer.SetMainCharacterIndex(GetMainActorVID());
	__RefreshStatus();
}

#ifdef ENABLE_TARGET_INFORMATION_SYSTEM
bool CPythonNetworkStream::SendTargetInfoLoadPacket(DWORD dwVID)
{
#ifdef ENABLE_TARGET_INFORMATION_RENEWAL
	CInstanceBase* pInstPlayer = CPythonCharacterManager::Instance().GetMainInstancePtr();
	CInstanceBase* pInstTarget = CPythonCharacterManager::Instance().GetInstancePtr(dwVID);
	if (pInstPlayer && pInstTarget)
	{
		if (!pInstTarget->IsDead())
		{
			if (pInstTarget->IsEnemy() || pInstTarget->IsStone())
			{
				const auto& it = CPythonWiki::Instance().m_vecMobDrop.find(pInstTarget->GetRace());

				if (it == CPythonWiki::Instance().m_vecMobDrop.end())
					return false;					

				for (const auto& iter : (*it).second)
				{
					PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_AddTargetMonsterDropInfo",
						Py_BuildValue("(iii)", pInstTarget->GetRace(), iter.itemVnum, iter.count));
				}

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_RefreshTargetMonsterDropInfo", Py_BuildValue("(i)", pInstTarget->GetRace()));
			}
			else
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "CloseTargetBoard", Py_BuildValue("()"));
		}
	}
	else
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "CloseTargetBoard", Py_BuildValue("()"));
	}
	return true;
#else
	TPacketCGTargetInfoLoad TargetInfoLoadPacket;
	TargetInfoLoadPacket.header = HEADER_CG_TARGET_INFO_LOAD;
	TargetInfoLoadPacket.dwVID = dwVID;
	if (!Send(sizeof(TargetInfoLoadPacket), &TargetInfoLoadPacket))
		return false;
	return true;
#endif
}
#endif

bool CPythonNetworkStream::RecvWarpPacket()
{
	TPacketGCWarp kWarpPacket;

	if (!Recv(sizeof(kWarpPacket), &kWarpPacket))
		return false;

	__DirectEnterMode_Set(m_dwSelectedCharacterIndex);

	CNetworkStream::Connect((DWORD)kWarpPacket.lAddr, kWarpPacket.wPort);

	return true;
}

bool CPythonNetworkStream::RecvDuelStartPacket()
{
	TPacketGCDuelStart kDuelStartPacket;
	if (!Recv(sizeof(kDuelStartPacket), &kDuelStartPacket))
		return false;

	DWORD count = (kDuelStartPacket.wSize - sizeof(kDuelStartPacket)) / sizeof(DWORD);

	CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();

	CInstanceBase* pkInstMain = rkChrMgr.GetMainInstancePtr();
	if (!pkInstMain)
	{
		TraceError("CPythonNetworkStream::RecvDuelStartPacket - MainCharacter is NULL");
		return false;
	}
	DWORD dwVIDSrc = pkInstMain->GetVirtualID();
	DWORD dwVIDDest;

	for (DWORD i = 0; i < count; i++)
	{
		Recv(sizeof(dwVIDDest), &dwVIDDest);
		CInstanceBase::InsertDUELKey(dwVIDSrc, dwVIDDest);
	}

	if (count == 0)
		pkInstMain->SetDuelMode(CInstanceBase::DUEL_CANNOTATTACK);
	else
		pkInstMain->SetDuelMode(CInstanceBase::DUEL_START);

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "CloseTargetBoard", Py_BuildValue("()"));

	rkChrMgr.RefreshAllPCTextTail();

	return true;
}

bool CPythonNetworkStream::RecvPVPPacket()
{
	TPacketGCPVP kPVPPacket;
	if (!Recv(sizeof(kPVPPacket), &kPVPPacket))
		return false;

	CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();
	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();

	switch (kPVPPacket.bMode)
	{
	case PVP_MODE_AGREE:
		rkChrMgr.RemovePVPKey(kPVPPacket.dwVIDSrc, kPVPPacket.dwVIDDst);

		if (rkPlayer.IsMainCharacterIndex(kPVPPacket.dwVIDDst))
			rkPlayer.RememberChallengeInstance(kPVPPacket.dwVIDSrc);

		if (rkPlayer.IsMainCharacterIndex(kPVPPacket.dwVIDSrc))
			rkPlayer.RememberCantFightInstance(kPVPPacket.dwVIDDst);
		break;
	case PVP_MODE_REVENGE:
	{
		rkChrMgr.RemovePVPKey(kPVPPacket.dwVIDSrc, kPVPPacket.dwVIDDst);

		DWORD dwKiller = kPVPPacket.dwVIDSrc;
		DWORD dwVictim = kPVPPacket.dwVIDDst;

		if (rkPlayer.IsMainCharacterIndex(dwVictim))
			rkPlayer.RememberRevengeInstance(dwKiller);

		if (rkPlayer.IsMainCharacterIndex(dwKiller))
			rkPlayer.RememberCantFightInstance(dwVictim);
		break;
	}

	case PVP_MODE_FIGHT:
		rkChrMgr.InsertPVPKey(kPVPPacket.dwVIDSrc, kPVPPacket.dwVIDDst);
		rkPlayer.ForgetInstance(kPVPPacket.dwVIDSrc);
		rkPlayer.ForgetInstance(kPVPPacket.dwVIDDst);
		break;
	case PVP_MODE_NONE:
		rkChrMgr.RemovePVPKey(kPVPPacket.dwVIDSrc, kPVPPacket.dwVIDDst);
		rkPlayer.ForgetInstance(kPVPPacket.dwVIDSrc);
		rkPlayer.ForgetInstance(kPVPPacket.dwVIDDst);
		break;
	}

	__RefreshTargetBoardByVID(kPVPPacket.dwVIDSrc);
	__RefreshTargetBoardByVID(kPVPPacket.dwVIDDst);

	return true;
}



void CPythonNetworkStream::NotifyHack(const char* c_szMsg)
{
	if (!m_kQue_stHack.empty())
		if (c_szMsg == m_kQue_stHack.back())
			return;

	m_kQue_stHack.push_back(c_szMsg);
}

bool CPythonNetworkStream::__SendHack(const char* c_szMsg)
{
	Tracen(c_szMsg);

	TPacketCGHack kPacketHack;
	kPacketHack.bHeader = HEADER_CG_HACK;
	strncpy(kPacketHack.szBuf, c_szMsg, sizeof(kPacketHack.szBuf) - 1);

	if (!Send(sizeof(kPacketHack), &kPacketHack))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendMessengerAddByVIDPacket(DWORD vid)
{
	TPacketCGMessenger packet;
	packet.header = HEADER_CG_MESSENGER;
	packet.subheader = MESSENGER_SUBHEADER_CG_ADD_BY_VID;
	if (!Send(sizeof(packet), &packet))
		return false;
	if (!Send(sizeof(vid), &vid))
		return false;
	return SendSequence();
}

bool CPythonNetworkStream::SendMessengerAddByNamePacket(const char* c_szName)
{
	TPacketCGMessenger packet;
	packet.header = HEADER_CG_MESSENGER;
	packet.subheader = MESSENGER_SUBHEADER_CG_ADD_BY_NAME;
	if (!Send(sizeof(packet), &packet))
		return false;
	char szName[CHARACTER_NAME_MAX_LEN];
	strncpy(szName, c_szName, CHARACTER_NAME_MAX_LEN - 1);
	szName[CHARACTER_NAME_MAX_LEN - 1] = '\0';

	if (!Send(sizeof(szName), &szName))
		return false;
	Tracef(" SendMessengerAddByNamePacket : %s\n", c_szName);
	return SendSequence();
}

bool CPythonNetworkStream::SendMessengerRemovePacket(const char* c_szKey, const char* c_szName)
{
	TPacketCGMessenger packet;
	packet.header = HEADER_CG_MESSENGER;
	packet.subheader = MESSENGER_SUBHEADER_CG_REMOVE;
	if (!Send(sizeof(packet), &packet))
		return false;
	char szKey[CHARACTER_NAME_MAX_LEN];
	strncpy(szKey, c_szKey, CHARACTER_NAME_MAX_LEN - 1);
	if (!Send(sizeof(szKey), &szKey))
		return false;
	__RefreshTargetBoardByName(c_szName);
	return SendSequence();
}

bool CPythonNetworkStream::SendCharacterStatePacket(const TPixelPosition& c_rkPPosDst, float fDstRot, UINT eFunc, UINT uArg)
{
	NANOBEGIN
		if (!__CanActMainInstance())
			return true;

	if (fDstRot < 0.0f)
		fDstRot = 360 + fDstRot;
	else if (fDstRot > 360.0f)
		fDstRot = fmodf(fDstRot, 360.0f);

	TPacketCGMove kStatePacket;
	kStatePacket.bHeader = HEADER_CG_CHARACTER_MOVE;
	kStatePacket.bFunc = eFunc;
	kStatePacket.bArg = uArg;
	kStatePacket.bRot = fDstRot / 5.0f;
	kStatePacket.lX = long(c_rkPPosDst.x);
	kStatePacket.lY = long(c_rkPPosDst.y);
	kStatePacket.dwTime = ELTimer_GetServerMSec();

	assert(kStatePacket.lX >= 0 && kStatePacket.lX < 204800);

	__LocalPositionToGlobalPosition(kStatePacket.lX, kStatePacket.lY);

	if (!Send(sizeof(kStatePacket), &kStatePacket))
	{
		Tracenf("CPythonNetworkStream::SendCharacterStatePacket(dwCmdTime=%u, fDstPos=(%f, %f), fDstRot=%f, eFunc=%d uArg=%d) - PACKET SEND ERROR",
			kStatePacket.dwTime,
			float(kStatePacket.lX),
			float(kStatePacket.lY),
			fDstRot,
			kStatePacket.bFunc,
			kStatePacket.bArg);
		return false;
	}
	NANOEND
		return SendSequence();
}

bool CPythonNetworkStream::SendUseSkillPacket(DWORD dwSkillIndex, DWORD dwTargetVID)
{
	CInstanceBase* victim = CPythonCharacterManager::Instance().GetInstancePtr(dwTargetVID);

	if (dwSkillIndex == 35 && victim && !victim->IsPC())
		return true;

	TPacketCGUseSkill UseSkillPacket;
	UseSkillPacket.bHeader = HEADER_CG_USE_SKILL;
	UseSkillPacket.dwVnum = dwSkillIndex;
	UseSkillPacket.dwTargetVID = dwTargetVID;
	if (!Send(sizeof(TPacketCGUseSkill), &UseSkillPacket))
	{
		Tracen("CPythonNetworkStream::SendUseSkillPacket - SEND PACKET ERROR");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendChatPacket(const char* c_szChat, BYTE byType
#ifdef ENABLE_CHAT_COLOR_SYSTEM
	, bool bEmoticon
#endif
)
{
	if (strlen(c_szChat) == 0)
		return true;

	if (strlen(c_szChat) >= 512)
		return true;

	if (c_szChat[0] == '/')
	{
		if (1 == strlen(c_szChat))
		{
			if (!m_strLastCommand.empty())
				c_szChat = m_strLastCommand.c_str();
		}
		else
		{
			m_strLastCommand = c_szChat;
		}
	}

	if (ClientCommand(c_szChat))
		return true;

	int iTextLen = strlen(c_szChat) + 1;
	TPacketCGChat ChatPacket;
	ChatPacket.header = HEADER_CG_CHAT;
	ChatPacket.length = sizeof(ChatPacket) + iTextLen;
	ChatPacket.type = byType;
#ifdef ENABLE_CHAT_COLOR_SYSTEM
	ChatPacket.bEmoticon = bEmoticon;
#endif

	if (!Send(sizeof(ChatPacket), &ChatPacket))
		return false;

	if (!Send(iTextLen, c_szChat))
		return false;

	return SendSequence();
}

//////////////////////////////////////////////////////////////////////////
// Emoticon
void CPythonNetworkStream::RegisterEmoticonString(const char* pcEmoticonString)
{
	if (m_EmoticonStringVector.size() >= CInstanceBase::EMOTICON_NUM)
	{
		TraceError("Can't register emoticon string... vector is full (size:%d)", m_EmoticonStringVector.size());
		return;
	}
	m_EmoticonStringVector.push_back(pcEmoticonString);
}

bool CPythonNetworkStream::ParseEmoticon(const char* pChatMsg, DWORD* pdwEmoticon)
{
	for (DWORD dwEmoticonIndex = 0; dwEmoticonIndex < m_EmoticonStringVector.size(); ++dwEmoticonIndex)
	{
		if (strlen(pChatMsg) > m_EmoticonStringVector[dwEmoticonIndex].size())
			continue;

		const char* pcFind = strstr(pChatMsg, m_EmoticonStringVector[dwEmoticonIndex].c_str());

		if (pcFind != pChatMsg)
			continue;

		*pdwEmoticon = dwEmoticonIndex;

		return true;
	}

	return false;
}
// Emoticon
//////////////////////////////////////////////////////////////////////////

void CPythonNetworkStream::__ConvertEmpireText(DWORD dwEmpireID, char* szText)
{
	if (dwEmpireID < 1 || dwEmpireID>3)
		return;

	UINT uHanPos;

	STextConvertTable& rkTextConvTable = m_aTextConvTable[dwEmpireID - 1];

	BYTE* pbText = (BYTE*)szText;
	while (*pbText)
	{
		if (*pbText & 0x80)
		{
			if (pbText[0] >= 0xb0 && pbText[0] <= 0xc8 && pbText[1] >= 0xa1 && pbText[1] <= 0xfe)
			{
				uHanPos = (pbText[0] - 0xb0) * (0xfe - 0xa1 + 1) + (pbText[1] - 0xa1);
				pbText[0] = rkTextConvTable.aacHan[uHanPos][0];
				pbText[1] = rkTextConvTable.aacHan[uHanPos][1];
			}
			pbText += 2;
		}
		else
		{
			if (*pbText >= 'a' && *pbText <= 'z')
			{
				*pbText = rkTextConvTable.acLower[*pbText - 'a'];
			}
			else if (*pbText >= 'A' && *pbText <= 'Z')
			{
				*pbText = rkTextConvTable.acUpper[*pbText - 'A'];
			}
			pbText++;
		}
	}
}

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
static std::string SBS(const std::string& c_str, const std::string& c_strStartDelim, const std::string& c_strEndDelim)
{
	unsigned u_strFirstDelimPos = c_str.find(c_strStartDelim);
	unsigned u_strEndPosFirstDelim = u_strFirstDelimPos + c_strStartDelim.length();
	unsigned u_strLastDelimPos = c_str.find_first_of(c_strEndDelim, u_strEndPosFirstDelim);
	return c_str.substr(u_strEndPosFirstDelim, u_strLastDelimPos - u_strEndPosFirstDelim);
}

static const char* FilterChat(const char* c_pszBuffer)
{
	std::string strChatBuf = c_pszBuffer;
	std::string strHyperItemLink = "|cffffc700|H";

	int iFound = 0;
	std::string::size_type zPos = 0;
	while ((zPos = strChatBuf.find(strHyperItemLink, zPos)) != std::string::npos)
	{
		++iFound;
		zPos += strHyperItemLink.length();

		std::string strElement = strChatBuf.substr(zPos, strChatBuf.length());
		std::string strItemLink = SBS(strElement, "", "|h"); // ITEM
		std::string strItemVnum = SBS(strElement, "item:", ":");
		int32_t dwItemVnum = htoi(strItemVnum.c_str()); // VNUM
		std::string strItemName = SBS(strElement, "[", "]").c_str(); // ITEM NAME

		CItemManager::Instance().SelectItemData(dwItemVnum);
		CItemData* pItemData = CItemManager::Instance().GetSelectedItemDataPointer();
		if (!pItemData)
			return c_pszBuffer;

		const char* c_pszItemName = pItemData->GetName();

		char szSearchBuf[255];
		snprintf(szSearchBuf, sizeof(szSearchBuf), "[%s]", strItemName.c_str());
		std::string strReplace(szSearchBuf);

		char szReplaceBuf[255];
		snprintf(szReplaceBuf, sizeof(szReplaceBuf), "[%s]", c_pszItemName); // Replace VNUM w/ NAME

		size_t pos = strChatBuf.find(strReplace);
		strChatBuf.replace(pos, strReplace.length(), szReplaceBuf); // Replace
	}

	char szFilteredChat[1024];
	snprintf(szFilteredChat, sizeof(szFilteredChat), "%s", strChatBuf.c_str());
	return szFilteredChat;
}
#endif


bool CPythonNetworkStream::RecvChatPacket()
{
	TPacketGCChat kChat;
	char buf[1024 + 1];
	char line[1024 + 1];

	if (!Recv(sizeof(kChat), &kChat))
		return false;

	UINT uChatSize = kChat.size - sizeof(kChat);

	if (!Recv(uChatSize, buf))
		return false;

	buf[uChatSize] = '\0';

	if (LocaleService_IsEUROPE() && GetDefaultCodePage() == 1256)
	{
		char* p = strchr(buf, ':');
		if (p && p[1] == ' ')
			p[1] = 0x08;
	}

	if (kChat.type >= CHAT_TYPE_MAX_NUM)
		return true;

	if (CHAT_TYPE_COMMAND == kChat.type)
	{
		ServerCommand(buf);
		return true;
	}

	if (kChat.dwVID != 0)
	{
		CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();
		CInstanceBase* pkInstChatter = rkChrMgr.GetInstancePtr(kChat.dwVID);
		if (NULL == pkInstChatter)
			return true;

		switch (kChat.type)
		{
		case CHAT_TYPE_TALKING:
		case CHAT_TYPE_PARTY:
		case CHAT_TYPE_GUILD:
		case CHAT_TYPE_SHOUT:
		case CHAT_TYPE_WHISPER:
		{
			char* p = strchr(buf, ':');

			if (p)
				p += 2;
			else
				p = buf;

			DWORD dwEmoticon;

			if (ParseEmoticon(p, &dwEmoticon))
			{
				pkInstChatter->SetEmoticon(dwEmoticon);
				return true;
			}
			else
			{
				if (gs_bEmpireLanuageEnable)
				{
					CInstanceBase* pkInstMain = rkChrMgr.GetMainInstancePtr();
					if (pkInstMain)
						if (!pkInstMain->IsSameEmpire(*pkInstChatter))
							__ConvertEmpireText(pkInstChatter->GetEmpireID(), p);
				}

				if (m_isEnableChatInsultFilter)
				{
					if (false == pkInstChatter->IsNPC() && false == pkInstChatter->IsEnemy())
					{
						__FilterInsult(p, strlen(p));
					}
				}

				_snprintf(line, sizeof(line), "%s", p);
			}
		}
		break;
		case CHAT_TYPE_COMMAND:
		case CHAT_TYPE_INFO:
		case CHAT_TYPE_NOTICE:
		case CHAT_TYPE_BIG_NOTICE:
			// case CHAT_TYPE_UNK_10:
#ifdef ENABLE_DICE_SYSTEM
		case CHAT_TYPE_DICE_INFO:
#endif
#ifdef ENABLE_ZODIAC_TEMPLE_CHAT
		case CHAT_TYPE_ZODIAC_NOTICE:
		case CHAT_TYPE_ZODIAC_SUB_NOTICE:
		case CHAT_TYPE_ZODIAC_NOTICE_CLEAR:
#endif
#ifdef ENABLE_DUNGEON_MODULES
		case CHAT_TYPE_MISSION:
#endif
		case CHAT_TYPE_MAX_NUM:
		default:
			_snprintf(line, sizeof(line), "%s", buf);
			break;
		}

		if (CHAT_TYPE_SHOUT != kChat.type)
		{
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
			CPythonTextTail::Instance().RegisterChatTail(kChat.dwVID, FilterChat(line));
#else
			CPythonTextTail::Instance().RegisterChatTail(kChat.dwVID, line);
#endif
		}

#ifdef ENABLE_ZODIAC_TEMPLE_CHAT
		if (pkInstChatter->IsPC() && (CHAT_TYPE_ZODIAC_NOTICE != kChat.type && CHAT_TYPE_ZODIAC_SUB_NOTICE != kChat.type && CHAT_TYPE_ZODIAC_NOTICE_CLEAR != kChat.type))
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
			CPythonChat::Instance().AppendChat(kChat.type, FilterChat(buf));
#else
			CPythonChat::Instance().AppendChat(kChat.type, buf);
#endif
#else
		if (pkInstChatter->IsPC())
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
			CPythonChat::Instance().AppendChat(kChat.type, FilterChat(buf));
#else
			CPythonChat::Instance().AppendChat(kChat.type, buf);
#endif
#endif
	}
	else
	{
		if (CHAT_TYPE_NOTICE == kChat.type)
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_SetTipMessage", Py_BuildValue("(s)", buf));
		}
		else if (CHAT_TYPE_BIG_NOTICE == kChat.type)
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_SetBigMessage", Py_BuildValue("(s)", buf));
		}
#ifdef ENABLE_DUNGEON_MODULES
		else if (CHAT_TYPE_MISSION == kChat.type)
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_SetMissionMessage", Py_BuildValue("(s)", buf));
		}
#endif
		else if (CHAT_TYPE_SHOUT == kChat.type)
		{
			char* p = strchr(buf, ':');

			if (p)
			{
				if (m_isEnableChatInsultFilter)
					__FilterInsult(p, strlen(p));
			}
		}
#ifdef ENABLE_ZODIAC_TEMPLE_CHAT
		else if (CHAT_TYPE_ZODIAC_NOTICE == kChat.type)
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_SetMissionMessage", Py_BuildValue("(s)", buf));
			return true;
		}
		else if (CHAT_TYPE_ZODIAC_SUB_NOTICE == kChat.type)
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_SetSubMissionMessage", Py_BuildValue("(s)", buf));
			return true;
		}
		else if (CHAT_TYPE_ZODIAC_NOTICE_CLEAR == kChat.type)
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_CleanMissionMessage", Py_BuildValue("()"));
			return true;
		}
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
		CPythonChat::Instance().AppendChat(kChat.type, FilterChat(buf));
#else
		CPythonChat::Instance().AppendChat(kChat.type, buf);
#endif
	}
	return true;
}

bool CPythonNetworkStream::RecvWhisperPacket()
{
	TPacketGCWhisper whisperPacket;
	char buf[512 + 1];

	if (!Recv(sizeof(whisperPacket), &whisperPacket))
		return false;

	assert(whisperPacket.wSize - sizeof(whisperPacket) < 512);

	if (!Recv(whisperPacket.wSize - sizeof(whisperPacket), &buf))
		return false;

	buf[whisperPacket.wSize - sizeof(whisperPacket)] = '\0';

	static char line[256];
	if (CPythonChat::WHISPER_TYPE_CHAT == whisperPacket.bType || CPythonChat::WHISPER_TYPE_GM == whisperPacket.bType)
	{
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
		_snprintf(line, sizeof(line), "%s : %s", whisperPacket.szNameFrom, FilterChat(buf));
#else
		_snprintf(line, sizeof(line), "%s : %s", whisperPacket.szNameFrom, buf);
#endif
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnRecvWhisper", Py_BuildValue("(iss)", (int)whisperPacket.bType, whisperPacket.szNameFrom, line));
	}
	else if (CPythonChat::WHISPER_TYPE_SYSTEM == whisperPacket.bType || CPythonChat::WHISPER_TYPE_ERROR == whisperPacket.bType)
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnRecvWhisperSystemMessage", Py_BuildValue("(iss)", (int)whisperPacket.bType, whisperPacket.szNameFrom, buf));
	}
	else
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnRecvWhisperError", Py_BuildValue("(iss)", (int)whisperPacket.bType, whisperPacket.szNameFrom, buf));
	}

	return true;
}

bool CPythonNetworkStream::SendWhisperPacket(const char* name, const char* c_szChat)
{
	if (strlen(c_szChat) >= 255)
		return true;

	int iTextLen = strlen(c_szChat) + 1;
	TPacketCGWhisper WhisperPacket;
	WhisperPacket.bHeader = HEADER_CG_WHISPER;
	WhisperPacket.wSize = sizeof(WhisperPacket) + iTextLen;

	strncpy(WhisperPacket.szNameTo, name, sizeof(WhisperPacket.szNameTo) - 1);

	if (!Send(sizeof(WhisperPacket), &WhisperPacket))
		return false;

	if (!Send(iTextLen, c_szChat))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::RecvPointChange()
{
	TPacketGCPointChange PointChange;

	if (!Recv(sizeof(TPacketGCPointChange), &PointChange))
	{
		Tracen("Recv Point Change Packet Error");
		return false;
	}

	CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();
	rkChrMgr.ShowPointEffect(PointChange.Type, PointChange.dwVID);

	CInstanceBase* pInstance = CPythonCharacterManager::Instance().GetMainInstancePtr();

	if (pInstance && PointChange.dwVID == pInstance->GetVirtualID())
	{
		CPythonPlayer& rkPlayer = CPythonPlayer::Instance();
		rkPlayer.SetStatus(PointChange.Type, PointChange.value);

		switch (PointChange.Type)
		{
		case POINT_STAT_RESET_COUNT:
			__RefreshStatus();
			break;
		case POINT_LEVEL:
		case POINT_ST:
		case POINT_DX:
		case POINT_HT:
		case POINT_IQ:
			__RefreshStatus();
			__RefreshSkillWindow();
			break;
		case POINT_SKILL:
		case POINT_SUB_SKILL:
		case POINT_HORSE_SKILL:
			__RefreshSkillWindow();
			break;
		case POINT_ENERGY:
			if (PointChange.value == 0)
			{
				rkPlayer.SetStatus(POINT_ENERGY_END_TIME, 0);
			}
			__RefreshStatus();
			break;
		default:
			__RefreshStatus();
			break;
		}

		if (POINT_GOLD == PointChange.Type)
		{
			if (PointChange.amount > 0)
			{
#ifdef ENABLE_DROP_INFO_WINDOW
#ifdef ENABLE_EXTENDED_YANG_LIMIT
				PyObject* args = PyTuple_New(1);
				PyTuple_SetItem(args, 0, PyLong_FromLongLong(PointChange.amount));
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnPickMoney", args);
#else
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnPickMoney", Py_BuildValue("(i)", PointChange.amount));
#endif
#endif
			}
		}
	}
#ifdef ENABLE_TEXT_LEVEL_REFRESH
	else
	{
		// the /advance command will provide no global refresh! it sends the pointchange only to the specific player and not all
		pInstance = CPythonCharacterManager::Instance().GetInstancePtr(PointChange.dwVID);
		if (pInstance && PointChange.Type == POINT_LEVEL)
		{
			pInstance->SetLevel(PointChange.value);
			pInstance->UpdateTextTailLevel(PointChange.value);
		}
	}
#endif
	return true;
}

bool CPythonNetworkStream::RecvStunPacket()
{
	TPacketGCStun StunPacket;

	if (!Recv(sizeof(StunPacket), &StunPacket))
	{
		Tracen("CPythonNetworkStream::RecvStunPacket Error");
		return false;
	}

	//Tracef("RecvStunPacket %d\n", StunPacket.vid);

	CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();
	CInstanceBase* pkInstSel = rkChrMgr.GetInstancePtr(StunPacket.vid);

	if (pkInstSel)
	{
		if (CPythonCharacterManager::Instance().GetMainInstancePtr() == pkInstSel)
			pkInstSel->Die();
		else
			pkInstSel->Stun();
	}

	return true;
}

bool CPythonNetworkStream::RecvDeadPacket()
{
	TPacketGCDead DeadPacket;
	if (!Recv(sizeof(DeadPacket), &DeadPacket))
	{
		Tracen("CPythonNetworkStream::RecvDeadPacket Error");
		return false;
	}

	CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();
	CInstanceBase* pkChrInstSel = rkChrMgr.GetInstancePtr(DeadPacket.vid);
	if (pkChrInstSel)
	{
		CInstanceBase* pkInstMain = rkChrMgr.GetMainInstancePtr();
		if (pkInstMain == pkChrInstSel)
		{
			Tracenf("On MainActor");
			if (false == pkInstMain->GetDuelMode())
			{
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnGameOver", Py_BuildValue("()"));
			}
			CPythonPlayer::Instance().NotifyDeadMainCharacter();
		}

		pkChrInstSel->Die();
	}

	return true;
}

bool CPythonNetworkStream::SendCharacterPositionPacket(BYTE iPosition)
{
	TPacketCGPosition PositionPacket;

	PositionPacket.header = HEADER_CG_CHARACTER_POSITION;
	PositionPacket.position = iPosition;

	if (!Send(sizeof(TPacketCGPosition), &PositionPacket))
	{
		Tracen("Send Character Position Packet Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendOnClickPacket(DWORD vid)
{
	TPacketCGOnClick OnClickPacket;
	OnClickPacket.header = HEADER_CG_ON_CLICK;
	OnClickPacket.vid = vid;

	if (!Send(sizeof(OnClickPacket), &OnClickPacket))
	{
		Tracen("Send On_Click Packet Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::RecvCharacterPositionPacket()
{
	TPacketGCPosition PositionPacket;

	if (!Recv(sizeof(TPacketGCPosition), &PositionPacket))
		return false;

	CInstanceBase* pChrInstance = CPythonCharacterManager::Instance().GetInstancePtr(PositionPacket.vid);

	if (!pChrInstance)
		return true;

	//pChrInstance->UpdatePosition(PositionPacket.position);

	return true;
}

bool CPythonNetworkStream::RecvMotionPacket()
{
	TPacketGCMotion MotionPacket;

	if (!Recv(sizeof(TPacketGCMotion), &MotionPacket))
		return false;

	CInstanceBase* pMainInstance = CPythonCharacterManager::Instance().GetInstancePtr(MotionPacket.vid);
	CInstanceBase* pVictimInstance = NULL;

	if (0 != MotionPacket.victim_vid)
		pVictimInstance = CPythonCharacterManager::Instance().GetInstancePtr(MotionPacket.victim_vid);

	if (!pMainInstance)
		return false;

	return true;
}

bool CPythonNetworkStream::RecvShopPacket()
{
	std::vector<char> vecBuffer;
	vecBuffer.clear();

	TPacketGCShop  packet_shop;
	if (!Recv(sizeof(packet_shop), &packet_shop))
		return false;

	int iSize = packet_shop.size - sizeof(packet_shop);
	if (iSize > 0)
	{
		vecBuffer.resize(iSize);
		if (!Recv(iSize, &vecBuffer[0]))
			return false;
	}

	switch (packet_shop.subheader)
	{
	case SHOP_SUBHEADER_GC_START:
	{
		CPythonShop::Instance().Clear();

		DWORD dwVID = *(DWORD*)&vecBuffer[0];

		TPacketGCShopStart* pShopStartPacket = (TPacketGCShopStart*)&vecBuffer[4];
		for (BYTE iItemIndex = 0; iItemIndex < SHOP_HOST_ITEM_MAX_NUM; ++iItemIndex)
		{
			CPythonShop::Instance().SetItemData(iItemIndex, pShopStartPacket->items[iItemIndex]);
		}

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "StartShop", Py_BuildValue("(i)", dwVID));
	}
	break;

	case SHOP_SUBHEADER_GC_START_EX:
	{
		CPythonShop::Instance().Clear();

		TPacketGCShopStartEx* pShopStartPacket = (TPacketGCShopStartEx*)&vecBuffer[0];
		size_t read_point = sizeof(TPacketGCShopStartEx);

		DWORD dwVID = pShopStartPacket->owner_vid;
		BYTE shop_tab_count = pShopStartPacket->shop_tab_count;

		CPythonShop::instance().SetTabCount(shop_tab_count);

		for (BYTE i = 0; i < shop_tab_count; i++)
		{
			TPacketGCShopStartEx::TSubPacketShopTab* pPackTab = (TPacketGCShopStartEx::TSubPacketShopTab*)&vecBuffer[read_point];
			read_point += sizeof(TPacketGCShopStartEx::TSubPacketShopTab);

			CPythonShop::instance().SetTabCoinType(i, pPackTab->coin_type);
			CPythonShop::instance().SetTabName(i, pPackTab->name);

			struct packet_shop_item* item = &pPackTab->items[0];

			for (BYTE j{}; j < SHOP_HOST_ITEM_MAX_NUM; j++)
			{
				TShopItemData* itemData = (item + j);
				CPythonShop::Instance().SetItemData(i, j, *itemData);
			}
		}

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "StartShop", Py_BuildValue("(i)", dwVID));
	}
	break;

	case SHOP_SUBHEADER_GC_END:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "EndShop", Py_BuildValue("()"));
		break;

	case SHOP_SUBHEADER_GC_UPDATE_ITEM:
	{
		TPacketGCShopUpdateItem* pShopUpdateItemPacket = (TPacketGCShopUpdateItem*)&vecBuffer[0];
		CPythonShop::Instance().SetItemData(pShopUpdateItemPacket->pos, pShopUpdateItemPacket->item);
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshShop", Py_BuildValue("()"));
	}
	break;
	case SHOP_SUBHEADER_GC_UPDATE_PRICE:
	{
#ifdef ENABLE_EXTENDED_YANG_LIMIT
		PyObject* args = PyTuple_New(1);
		PyTuple_SetItem(args, 0, PyLong_FromLongLong(*(int64_t*)&vecBuffer[0]));
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetShopSellingPrice", args);
#else
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetShopSellingPrice", Py_BuildValue("(i)", *(int*)&vecBuffer[0]));
#endif
	}
	break;

	case SHOP_SUBHEADER_GC_NOT_ENOUGH_MONEY:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnShopError", Py_BuildValue("(s)", "NOT_ENOUGH_MONEY"));
		break;

#ifdef ENABLE_BUY_WITH_ITEMS
	case SHOP_SUBHEADER_GC_NOT_ENOUGH_ITEM:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnShopError", Py_BuildValue("(s)", "NOT_ENOUGH_ITEM"));
		break;
#endif

	case SHOP_SUBHEADER_GC_NOT_ENOUGH_MONEY_EX:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnShopError", Py_BuildValue("(s)", "NOT_ENOUGH_MONEY_EX"));
		break;

	case SHOP_SUBHEADER_GC_SOLDOUT:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnShopError", Py_BuildValue("(s)", "SOLDOUT"));
		break;

	case SHOP_SUBHEADER_GC_INVENTORY_FULL:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnShopError", Py_BuildValue("(s)", "INVENTORY_FULL"));
		break;

	case SHOP_SUBHEADER_GC_INVALID_POS:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnShopError", Py_BuildValue("(s)", "INVALID_POS"));
		break;

	default:
		TraceError("CPythonNetworkStream::RecvShopPacket: Unknown subheader\n");
		break;
	}

	return true;
}

bool CPythonNetworkStream::RecvExchangePacket()
{
	TPacketGCExchange exchange_packet;

	if (!Recv(sizeof(exchange_packet), &exchange_packet))
		return false;

	switch (exchange_packet.subheader)
	{
	case EXCHANGE_SUBHEADER_GC_START:
		CPythonExchange::Instance().Clear();
		CPythonExchange::Instance().Start();
		CPythonExchange::Instance().SetSelfName(CPythonPlayer::Instance().GetName());
#ifdef ENABLE_EXCHANGE_WINDOW_RENEWAL
		CPythonExchange::Instance().SetSelfRace(CPythonPlayer::Instance().GetRace());
#endif
#ifdef ENABLE_LEVEL_IN_TRADE
		//CPythonExchange::Instance().SetSelfLevel(CPythonPlayer::Instance().GetLevel());
		CPythonExchange::Instance().SetSelfLevel(CPythonPlayer::Instance().GetStatus(POINT_LEVEL));
#endif

		{
			CInstanceBase* pCharacterInstance = CPythonCharacterManager::Instance().GetInstancePtr(exchange_packet.arg1);

			if (pCharacterInstance)
			{
				CPythonExchange::Instance().SetTargetName(pCharacterInstance->GetNameString());
#ifdef ENABLE_EXCHANGE_WINDOW_RENEWAL
				CPythonExchange::Instance().SetTargetRace(pCharacterInstance->GetRace());
#endif
#ifdef ENABLE_LEVEL_IN_TRADE
				CPythonExchange::Instance().SetTargetLevel(pCharacterInstance->GetLevel());
#endif
			}
		}

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "StartExchange", Py_BuildValue("()"));
		break;

	case EXCHANGE_SUBHEADER_GC_ITEM_ADD:
		if (exchange_packet.is_me)
		{
			int iSlotIndex = exchange_packet.arg2.cell;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
			CPythonExchange::Instance().SetItemToSelf(iSlotIndex, exchange_packet.arg1, (MAX_COUNT)exchange_packet.arg3);
#else
			CPythonExchange::Instance().SetItemToSelf(iSlotIndex, exchange_packet.arg1, (BYTE)exchange_packet.arg3);
#endif
			for (int i = 0; i < ITEM_SOCKET_SLOT_MAX_NUM; ++i)
				CPythonExchange::Instance().SetItemMetinSocketToSelf(iSlotIndex, i, exchange_packet.alValues[i]);
			for (int j = 0; j < ITEM_ATTRIBUTE_SLOT_MAX_NUM; ++j)
				CPythonExchange::Instance().SetItemAttributeToSelf(iSlotIndex, j, exchange_packet.aAttr[j].bType, exchange_packet.aAttr[j].sValue);
#ifdef WJ_ENABLE_TRADABLE_ICON
			PyObject* args = PyTuple_New(3);
			PyTuple_SetItem(args, 0, PyInt_FromLong(exchange_packet.arg4.window_type));
			PyTuple_SetItem(args, 1, PyInt_FromLong(exchange_packet.arg4.cell));
			PyTuple_SetItem(args, 2, PyInt_FromLong(iSlotIndex));
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_AddItemToExchange", args);
#endif
		}
		else
		{
			int iSlotIndex = exchange_packet.arg2.cell;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
			CPythonExchange::Instance().SetItemToTarget(iSlotIndex, exchange_packet.arg1, (MAX_COUNT)exchange_packet.arg3);
#else
			CPythonExchange::Instance().SetItemToTarget(iSlotIndex, exchange_packet.arg1, (BYTE)exchange_packet.arg3);
#endif
			for (int i = 0; i < ITEM_SOCKET_SLOT_MAX_NUM; ++i)
				CPythonExchange::Instance().SetItemMetinSocketToTarget(iSlotIndex, i, exchange_packet.alValues[i]);
			for (int j = 0; j < ITEM_ATTRIBUTE_SLOT_MAX_NUM; ++j)
				CPythonExchange::Instance().SetItemAttributeToTarget(iSlotIndex, j, exchange_packet.aAttr[j].bType, exchange_packet.aAttr[j].sValue);
		}

		__RefreshExchangeWindow();
		__RefreshInventoryWindow();
		break;

	case EXCHANGE_SUBHEADER_GC_ITEM_DEL:
		if (exchange_packet.is_me)
		{
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
			CPythonExchange::Instance().DelItemOfSelf((MAX_COUNT)exchange_packet.arg1);
#else
			CPythonExchange::Instance().DelItemOfSelf((BYTE)exchange_packet.arg1);
#endif
		}
		else
		{
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
			CPythonExchange::Instance().DelItemOfTarget((MAX_COUNT)exchange_packet.arg1);
#else
			CPythonExchange::Instance().DelItemOfTarget((BYTE)exchange_packet.arg1);
#endif
		}
		__RefreshExchangeWindow();
		__RefreshInventoryWindow();
		break;

	case EXCHANGE_SUBHEADER_GC_ELK_ADD:
		if (exchange_packet.is_me)
			CPythonExchange::Instance().SetElkToSelf(exchange_packet.arg1);
		else
			CPythonExchange::Instance().SetElkToTarget(exchange_packet.arg1);

		__RefreshExchangeWindow();
		break;

	case EXCHANGE_SUBHEADER_GC_ACCEPT:
		if (exchange_packet.is_me)
		{
			CPythonExchange::Instance().SetAcceptToSelf((BYTE)exchange_packet.arg1);
		}
		else
		{
			CPythonExchange::Instance().SetAcceptToTarget((BYTE)exchange_packet.arg1);
		}
		__RefreshExchangeWindow();
		break;

	case EXCHANGE_SUBHEADER_GC_END:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "EndExchange", Py_BuildValue("()"));
		__RefreshInventoryWindow();
		CPythonExchange::Instance().End();
		break;

	case EXCHANGE_SUBHEADER_GC_ALREADY:
		Tracef("trade_already");
		break;

	case EXCHANGE_SUBHEADER_GC_LESS_ELK:
		Tracef("trade_less_elk");
		break;
	};

	return true;
}

bool CPythonNetworkStream::RecvQuestInfoPacket()
{
	TPacketGCQuestInfo QuestInfo;

	if (!Peek(sizeof(TPacketGCQuestInfo), &QuestInfo))
	{
		Tracen("Recv Quest Info Packet Error #1");
		return false;
	}

	if (!Peek(QuestInfo.size))
	{
		Tracen("Recv Quest Info Packet Error #2");
		return false;
	}

	Recv(sizeof(TPacketGCQuestInfo));

	const BYTE& c_rFlag = QuestInfo.flag;

	enum
	{
		QUEST_PACKET_TYPE_NONE,
		QUEST_PACKET_TYPE_BEGIN,
		QUEST_PACKET_TYPE_UPDATE,
		QUEST_PACKET_TYPE_END,
	};

	BYTE byQuestPacketType = QUEST_PACKET_TYPE_NONE;

	if (0 != (c_rFlag & QUEST_SEND_IS_BEGIN))
	{
		BYTE isBegin;
		if (!Recv(sizeof(isBegin), &isBegin))
			return false;

		if (isBegin)
			byQuestPacketType = QUEST_PACKET_TYPE_BEGIN;
		else
			byQuestPacketType = QUEST_PACKET_TYPE_END;
	}
	else
	{
		byQuestPacketType = QUEST_PACKET_TYPE_UPDATE;
	}

	// Recv Data Start
	char szTitle[30 + 1] = "";
	char szClockName[16 + 1] = "";
	int iClockValue = 0;
	char szCounterName[16 + 1] = "";
	int iCounterValue = 0;
	char szIconFileName[24 + 1] = "";

	if (0 != (c_rFlag & QUEST_SEND_TITLE))
	{
		if (!Recv(sizeof(szTitle), &szTitle))
			return false;

		szTitle[30] = '\0';
	}
	if (0 != (c_rFlag & QUEST_SEND_CLOCK_NAME))
	{
		if (!Recv(sizeof(szClockName), &szClockName))
			return false;

		szClockName[16] = '\0';
	}
	if (0 != (c_rFlag & QUEST_SEND_CLOCK_VALUE))
	{
		if (!Recv(sizeof(iClockValue), &iClockValue))
			return false;
	}
	if (0 != (c_rFlag & QUEST_SEND_COUNTER_NAME))
	{
		if (!Recv(sizeof(szCounterName), &szCounterName))
			return false;

		szCounterName[16] = '\0';
	}
	if (0 != (c_rFlag & QUEST_SEND_COUNTER_VALUE))
	{
		if (!Recv(sizeof(iCounterValue), &iCounterValue))
			return false;
	}
	if (0 != (c_rFlag & QUEST_SEND_ICON_FILE))
	{
		if (!Recv(sizeof(szIconFileName), &szIconFileName))
			return false;

		szIconFileName[24] = '\0';
	}
	// Recv Data End

	CPythonQuest& rkQuest = CPythonQuest::Instance();

	// Process Start
	if (QUEST_PACKET_TYPE_END == byQuestPacketType)
	{
		rkQuest.DeleteQuestInstance(QuestInfo.index);
	}
	else if (QUEST_PACKET_TYPE_UPDATE == byQuestPacketType)
	{
		if (!rkQuest.IsQuest(QuestInfo.index))
		{
#ifdef ENABLE_QUEST_CATEGORY
			rkQuest.MakeQuest(QuestInfo.index, QuestInfo.c_index);
#else
			rkQuest.MakeQuest(QuestInfo.index);
#endif
		}

		if (strlen(szTitle) > 0)
			rkQuest.SetQuestTitle(QuestInfo.index, szTitle);
		if (strlen(szClockName) > 0)
			rkQuest.SetQuestClockName(QuestInfo.index, szClockName);
		if (strlen(szCounterName) > 0)
			rkQuest.SetQuestCounterName(QuestInfo.index, szCounterName);
		if (strlen(szIconFileName) > 0)
			rkQuest.SetQuestIconFileName(QuestInfo.index, szIconFileName);

		if (c_rFlag & QUEST_SEND_CLOCK_VALUE)
			rkQuest.SetQuestClockValue(QuestInfo.index, iClockValue);
		if (c_rFlag & QUEST_SEND_COUNTER_VALUE)
			rkQuest.SetQuestCounterValue(QuestInfo.index, iCounterValue);
	}
	else if (QUEST_PACKET_TYPE_BEGIN == byQuestPacketType)
	{
		CPythonQuest::SQuestInstance QuestInstance;
		QuestInstance.dwIndex = QuestInfo.index;
		QuestInstance.strTitle = szTitle;
		QuestInstance.strClockName = szClockName;
		QuestInstance.iClockValue = iClockValue;
		QuestInstance.strCounterName = szCounterName;
		QuestInstance.iCounterValue = iCounterValue;
		QuestInstance.strIconFileName = szIconFileName;
		CPythonQuest::Instance().RegisterQuestInstance(QuestInstance);
	}
	// Process Start End

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshQuest", Py_BuildValue("()"));
	return true;
}

bool CPythonNetworkStream::RecvQuestConfirmPacket()
{
	TPacketGCQuestConfirm kQuestConfirmPacket;
	if (!Recv(sizeof(kQuestConfirmPacket), &kQuestConfirmPacket))
	{
		Tracen("RecvQuestConfirmPacket Error");
		return false;
	}

	PyObject* poArg = Py_BuildValue("(sii)", kQuestConfirmPacket.msg, kQuestConfirmPacket.timeout, kQuestConfirmPacket.requestPID);
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_OnQuestConfirm", poArg);
	return true;
}

bool CPythonNetworkStream::RecvRequestMakeGuild()
{
	TPacketGCBlank blank;
	if (!Recv(sizeof(blank), &blank))
	{
		Tracen("RecvRequestMakeGuild Packet Error");
		return false;
	}

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "AskGuildName", Py_BuildValue("()"));

	return true;
}

void CPythonNetworkStream::ToggleGameDebugInfo()
{
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ToggleDebugInfo", Py_BuildValue("()"));
}

bool CPythonNetworkStream::SendExchangeStartPacket(DWORD vid)
{
	if (!__CanActMainInstance())
		return true;

	TPacketCGExchange	packet;

	packet.header = HEADER_CG_EXCHANGE;
	packet.subheader = EXCHANGE_SUBHEADER_CG_START;
	packet.arg1 = vid;

	if (!Send(sizeof(packet), &packet))
	{
		Tracef("send_trade_start_packet Error\n");
		return false;
	}

	Tracef("send_trade_start_packet   vid %d \n", vid);
	return SendSequence();
}

#ifdef ENABLE_EXTENDED_YANG_LIMIT
bool CPythonNetworkStream::SendExchangeElkAddPacket(int64_t elk)
#else
bool CPythonNetworkStream::SendExchangeElkAddPacket(DWORD elk)
#endif
{
	if (!__CanActMainInstance())
		return true;

	TPacketCGExchange	packet;

	packet.header = HEADER_CG_EXCHANGE;
	packet.subheader = EXCHANGE_SUBHEADER_CG_ELK_ADD;
	packet.arg1 = elk;

	if (!Send(sizeof(packet), &packet))
	{
		Tracef("send_trade_elk_add_packet Error\n");
		return false;
	}

	return SendSequence();
}

#if defined(ENABLE_CHECKINOUT_UPDATE)
bool CPythonNetworkStream::SendExchangeItemAddPacket(TItemPos ItemPos, BYTE byDisplayPos, bool SelectPosAuto)
#else
bool CPythonNetworkStream::SendExchangeItemAddPacket(TItemPos ItemPos, BYTE byDisplayPos)
#endif
{
	if (!__CanActMainInstance())
		return true;

	TPacketCGExchange	packet;

	packet.header = HEADER_CG_EXCHANGE;
	packet.subheader = EXCHANGE_SUBHEADER_CG_ITEM_ADD;
	packet.Pos = ItemPos;
	packet.arg2 = byDisplayPos;
#if defined(ENABLE_CHECKINOUT_UPDATE)
	packet.SelectPosAuto = SelectPosAuto;
#endif

	if (!Send(sizeof(packet), &packet))
	{
		Tracef("send_trade_item_add_packet Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendExchangeItemDelPacket(BYTE pos)
{
	assert(!"Can't be called function - CPythonNetworkStream::SendExchangeItemDelPacket");
	return true;

	if (!__CanActMainInstance())
		return true;

	TPacketCGExchange	packet;

	packet.header = HEADER_CG_EXCHANGE;
	packet.subheader = EXCHANGE_SUBHEADER_CG_ITEM_DEL;
	packet.arg1 = pos;

	if (!Send(sizeof(packet), &packet))
	{
		Tracef("send_trade_item_del_packet Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendExchangeAcceptPacket()
{
	if (!__CanActMainInstance())
		return true;

	TPacketCGExchange	packet;

	packet.header = HEADER_CG_EXCHANGE;
	packet.subheader = EXCHANGE_SUBHEADER_CG_ACCEPT;

	if (!Send(sizeof(packet), &packet))
	{
		Tracef("send_trade_accept_packet Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendExchangeExitPacket()
{
	if (!__CanActMainInstance())
		return true;

	TPacketCGExchange	packet;

	packet.header = HEADER_CG_EXCHANGE;
	packet.subheader = EXCHANGE_SUBHEADER_CG_CANCEL;

	if (!Send(sizeof(packet), &packet))
	{
		Tracef("send_trade_exit_packet Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendPointResetPacket()
{
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "StartPointReset", Py_BuildValue("()"));
	return true;
}

bool CPythonNetworkStream::__IsPlayerAttacking()
{
	CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();
	CInstanceBase* pkInstMain = rkChrMgr.GetMainInstancePtr();
	if (!pkInstMain)
		return false;

	if (!pkInstMain->IsAttacking())
		return false;

	return true;
}

bool CPythonNetworkStream::RecvScriptPacket()
{
	TPacketGCScript ScriptPacket;

	if (!Recv(sizeof(TPacketGCScript), &ScriptPacket))
	{
		TraceError("RecvScriptPacket_RecvError");
		return false;
	}

	if (ScriptPacket.size < sizeof(TPacketGCScript))
	{
		TraceError("RecvScriptPacket_SizeError");
		return false;
	}

	ScriptPacket.size -= sizeof(TPacketGCScript);

	static string str;
	str = "";
	str.resize(ScriptPacket.size + 1);

	if (!Recv(ScriptPacket.size, &str[0]))
		return false;

	str[str.size() - 1] = '\0';

	int iIndex = CPythonEventManager::Instance().RegisterEventSetFromString(str);

	if (-1 != iIndex)
	{
		CPythonEventManager::Instance().SetVisibleLineCount(iIndex, 30);
		CPythonNetworkStream::Instance().OnScriptEventStart(ScriptPacket.skin, iIndex);
	}

	return true;
}

bool CPythonNetworkStream::SendScriptAnswerPacket(int iAnswer)
{
	TPacketCGScriptAnswer ScriptAnswer;

	ScriptAnswer.header = HEADER_CG_SCRIPT_ANSWER;
	ScriptAnswer.answer = (BYTE)iAnswer;
	if (!Send(sizeof(TPacketCGScriptAnswer), &ScriptAnswer))
	{
		Tracen("Send Script Answer Packet Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendScriptButtonPacket(unsigned int iIndex)
{
	TPacketCGScriptButton ScriptButton;

	ScriptButton.header = HEADER_CG_SCRIPT_BUTTON;
	ScriptButton.idx = iIndex;
	if (!Send(sizeof(TPacketCGScriptButton), &ScriptButton))
	{
		Tracen("Send Script Button Packet Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendAnswerMakeGuildPacket(const char* c_szName)
{
	TPacketCGAnswerMakeGuild Packet;

	Packet.header = HEADER_CG_ANSWER_MAKE_GUILD;
	strncpy(Packet.guild_name, c_szName, GUILD_NAME_MAX_LEN);
	Packet.guild_name[GUILD_NAME_MAX_LEN] = '\0';

	if (!Send(sizeof(Packet), &Packet))
	{
		Tracen("SendAnswerMakeGuild Packet Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendQuestInputStringPacket(const char* c_szString)
{
	TPacketCGQuestInputString Packet;
	Packet.bHeader = HEADER_CG_QUEST_INPUT_STRING;
	strncpy(Packet.szString, c_szString, QUEST_INPUT_STRING_MAX_NUM);

	if (!Send(sizeof(Packet), &Packet))
	{
		Tracen("SendQuestInputStringPacket Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendQuestConfirmPacket(BYTE byAnswer, DWORD dwPID)
{
	TPacketCGQuestConfirm kPacket;
	kPacket.header = HEADER_CG_QUEST_CONFIRM;
	kPacket.answer = byAnswer;
	kPacket.requestPID = dwPID;

	if (!Send(sizeof(kPacket), &kPacket))
	{
		Tracen("SendQuestConfirmPacket Error");
		return false;
	}

	Tracenf(" SendQuestConfirmPacket : %d, %d", byAnswer, dwPID);
	return SendSequence();
}


bool CPythonNetworkStream::RecvSkillLevel()
{
	assert(!"CPythonNetworkStream::RecvSkillLevel - Don't use this function");
	TPacketGCSkillLevel packet;
	if (!Recv(sizeof(TPacketGCSkillLevel), &packet))
	{
		Tracen("CPythonNetworkStream::RecvSkillLevel - RecvError");
		return false;
	}

	DWORD dwSlotIndex;

	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();
	for (int i = 0; i < SKILL_MAX_NUM; ++i)
	{
		if (rkPlayer.GetSkillSlotIndex(i, &dwSlotIndex))
			rkPlayer.SetSkillLevel(dwSlotIndex, packet.abSkillLevels[i]);
	}

	__RefreshSkillWindow();
	__RefreshStatus();
	Tracef(" >> RecvSkillLevel\n");
	return true;
}

bool CPythonNetworkStream::RecvSkillLevelNew()
{
	TPacketGCSkillLevelNew packet;

	if (!Recv(sizeof(TPacketGCSkillLevelNew), &packet))
	{
		Tracen("CPythonNetworkStream::RecvSkillLevelNew - RecvError");
		return false;
	}

	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();

	rkPlayer.SetSkill(7, 0);
	rkPlayer.SetSkill(8, 0);

	for (int i = 0; i < SKILL_MAX_NUM; ++i)
	{
		TPlayerSkill& rPlayerSkill = packet.skills[i];

		if (i >= 112 && i <= 115 && rPlayerSkill.bLevel)
			rkPlayer.SetSkill(7, i);

		if (i >= 116 && i <= 119 && rPlayerSkill.bLevel)
			rkPlayer.SetSkill(8, i);

		rkPlayer.SetSkillLevel_(i, rPlayerSkill.bMasterType, rPlayerSkill.bLevel);
	}

	__RefreshSkillWindow();
	__RefreshStatus();
	//Tracef(" >> RecvSkillLevelNew\n");
	return true;
}

bool CPythonNetworkStream::RecvDamageInfoPacket()
{
	TPacketGCDamageInfo DamageInfoPacket;

	if (!Recv(sizeof(TPacketGCDamageInfo), &DamageInfoPacket))
	{
		Tracen("Recv Target Packet Error");
		return false;
	}

	CInstanceBase* pInstTarget = CPythonCharacterManager::Instance().GetInstancePtr(DamageInfoPacket.dwVID);
	bool bSelf = (pInstTarget == CPythonCharacterManager::Instance().GetMainInstancePtr());
	bool bTarget = (pInstTarget == m_pInstTarget);
	if (pInstTarget)
	{
		if (DamageInfoPacket.damage >= 0)
			pInstTarget->AddDamageEffect(DamageInfoPacket.damage, DamageInfoPacket.flag, bSelf, bTarget);
		else
			TraceError("Damage is equal or below 0.");
	}

	return true;
}
bool CPythonNetworkStream::RecvTargetPacket()
{
	TPacketGCTarget TargetPacket;

	if (!Recv(sizeof(TPacketGCTarget), &TargetPacket))
	{
		Tracen("Recv Target Packet Error");
		return false;
	}

	CInstanceBase* pInstPlayer = CPythonCharacterManager::Instance().GetMainInstancePtr();
	CInstanceBase* pInstTarget = CPythonCharacterManager::Instance().GetInstancePtr(TargetPacket.dwVID);
	if (pInstPlayer && pInstTarget)
	{
		if (!pInstTarget->IsDead())
		{
			if (pInstTarget->IsPC() || pInstTarget->IsBuilding())
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "CloseTargetBoardIfDifferent", Py_BuildValue("(i)", TargetPacket.dwVID));
			else if (pInstPlayer->CanViewTargetHP(*pInstTarget))
#ifdef ENABLE_ELEMENT_ADD
#ifdef ENABLE_SHOW_TARGET_HP
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetHPTargetBoard", Py_BuildValue("(iiLi)", TargetPacket.dwVID, TargetPacket.bHPPercent, TargetPacket.hpTarget, TargetPacket.bElement));
#else
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetHPTargetBoard", Py_BuildValue("(iiL)", TargetPacket.dwVID, TargetPacket.bHPPercent, TargetPacket.bElement));
#endif
#else
#ifdef ENABLE_SHOW_TARGET_HP
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetHPTargetBoard", Py_BuildValue("(iiL)", TargetPacket.dwVID, TargetPacket.bHPPercent, TargetPacket.hpTarget));
#else
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetHPTargetBoard", Py_BuildValue("(ii)", TargetPacket.dwVID, TargetPacket.bHPPercent));
#endif
#endif
			else
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "CloseTargetBoard", Py_BuildValue("()"));

			m_pInstTarget = pInstTarget;
		}
	}
	else
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "CloseTargetBoard", Py_BuildValue("()"));
	}

	return true;
}

#ifdef ENABLE_TARGET_INFORMATION_SYSTEM
bool CPythonNetworkStream::RecvTargetInfoPacket()
{
	TPacketGCTargetInfo pInfoTargetPacket;
	if (!Recv(sizeof(TPacketGCTargetInfo), &pInfoTargetPacket))
	{
		Tracen("Recv Info Target Packet Error");
		return false;
	}
	CInstanceBase* pInstPlayer = CPythonCharacterManager::Instance().GetMainInstancePtr();
	CInstanceBase* pInstTarget = CPythonCharacterManager::Instance().GetInstancePtr(pInfoTargetPacket.dwVID);
	if (pInstPlayer && pInstTarget)
	{
		if (!pInstTarget->IsDead())
		{
			if (pInstTarget->IsEnemy() || pInstTarget->IsStone())
			{
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_AddTargetMonsterDropInfo",
					Py_BuildValue("(iii)", pInfoTargetPacket.race, pInfoTargetPacket.dwVnum, pInfoTargetPacket.count));
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_RefreshTargetMonsterDropInfo", Py_BuildValue("(i)", pInfoTargetPacket.race));
			}
			else
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "CloseTargetBoard", Py_BuildValue("()"));
		}
	}
	else
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "CloseTargetBoard", Py_BuildValue("()"));
	}

	return true;
}
#endif

bool CPythonNetworkStream::RecvMountPacket()
{
	TPacketGCMount MountPacket;

	if (!Recv(sizeof(TPacketGCMount), &MountPacket))
	{
		Tracen("Recv Mount Packet Error");
		return false;
	}

	CInstanceBase* pInstance = CPythonCharacterManager::Instance().GetInstancePtr(MountPacket.vid);

	if (pInstance)
	{
		// Mount
		if (0 != MountPacket.mount_vid)
		{
			//			pInstance->Ride(MountPacket.pos, MountPacket.mount_vid);
		}
		// Unmount
		else
		{
			//			pInstance->Unride(MountPacket.pos, MountPacket.x, MountPacket.y);
		}
	}

	if (CPythonPlayer::Instance().IsMainCharacterIndex(MountPacket.vid))
	{
		//		CPythonPlayer::Instance().SetRidingVehicleIndex(MountPacket.mount_vid);
	}

	return true;
}

bool CPythonNetworkStream::RecvChangeSpeedPacket()
{
	TPacketGCChangeSpeed SpeedPacket;

	if (!Recv(sizeof(TPacketGCChangeSpeed), &SpeedPacket))
	{
		Tracen("Recv Speed Packet Error");
		return false;
	}

	CInstanceBase* pInstance = CPythonCharacterManager::Instance().GetInstancePtr(SpeedPacket.vid);

	if (!pInstance)
		return true;

	//	pInstance->SetWalkSpeed(SpeedPacket.walking_speed);
	//	pInstance->SetRunSpeed(SpeedPacket.running_speed);
	return true;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
// Recv

bool CPythonNetworkStream::SendAttackPacket(UINT uMotAttack, DWORD dwVIDVictim)
{
	if (!__CanActMainInstance())
		return true;

#ifdef ENABLE_BOT_CONTROL
	CInstanceBase* pInstance = CPythonCharacterManager::Instance().GetInstancePtr(dwVIDVictim);
	if (!pInstance)
		return true;

	if (!pInstance->IsPC() && !pInstance->IsNPC())
	{
		CPythonPlayer& rkPlayer = CPythonPlayer::Instance();
		if (rkPlayer.GetBotControlState())
		{
			if (rkPlayer.GetBotControlWindow())
				return true;

			rkPlayer.SetBotControWindow(true);
			rkPlayer.OpenBotControlWindow();
			return true;
		}
	}
#endif

	TPacketCGAttack kPacketAtk;

	kPacketAtk.header = HEADER_CG_ATTACK;
	kPacketAtk.bType = uMotAttack;
	kPacketAtk.dwVictimVID = dwVIDVictim;

#ifdef ENABLE_SHOW_STROKE_INFO
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RegisterStroke", Py_BuildValue("(i)", dwVIDVictim));
#endif
	if (!SendSpecial(sizeof(kPacketAtk), &kPacketAtk))
	{
		Tracen("Send Battle Attack Packet Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendSpecial(int nLen, void* pvBuf)
{
	BYTE bHeader = *(BYTE*)pvBuf;

	switch (bHeader)
	{
	case HEADER_CG_ATTACK:
	{
		TPacketCGAttack* pkPacketAtk = (TPacketCGAttack*)pvBuf;
		pkPacketAtk->bCRCMagicCubeProcPiece = GetProcessCRCMagicCubePiece();
		pkPacketAtk->bCRCMagicCubeFilePiece = GetProcessCRCMagicCubePiece();
		return Send(nLen, pvBuf);
	}
	break;
	}

	return Send(nLen, pvBuf);
}

bool CPythonNetworkStream::RecvAddFlyTargetingPacket()
{
	TPacketGCFlyTargeting kPacket;
	if (!Recv(sizeof(kPacket), &kPacket))
		return false;

	__GlobalPositionToLocalPosition(kPacket.lX, kPacket.lY);

	Tracef("VID [%d] Added to target settings\n", kPacket.dwShooterVID);

	CPythonCharacterManager& rpcm = CPythonCharacterManager::Instance();

	CInstanceBase* pShooter = rpcm.GetInstancePtr(kPacket.dwShooterVID);

	if (!pShooter)
	{
#ifndef _DEBUG
		TraceError("CPythonNetworkStream::RecvFlyTargetingPacket() - dwShooterVID[%d] NOT EXIST", kPacket.dwShooterVID);
#endif
		return true;
	}

	CInstanceBase* pTarget = rpcm.GetInstancePtr(kPacket.dwTargetVID);

	if (kPacket.dwTargetVID && pTarget)
	{
		pShooter->GetGraphicThingInstancePtr()->AddFlyTarget(pTarget->GetGraphicThingInstancePtr());
	}
	else
	{
		float h = CPythonBackground::Instance().GetHeight(kPacket.lX, kPacket.lY) + 60.0f; // TEMPORARY HEIGHT
		pShooter->GetGraphicThingInstancePtr()->AddFlyTarget(D3DXVECTOR3(kPacket.lX, kPacket.lY, h));
		//pShooter->GetGraphicThingInstancePtr()->SetFlyTarget(kPacket.kPPosTarget.x,kPacket.kPPosTarget.y,);
	}

	return true;
}

bool CPythonNetworkStream::RecvFlyTargetingPacket()
{
	TPacketGCFlyTargeting kPacket;
	if (!Recv(sizeof(kPacket), &kPacket))
		return false;

	__GlobalPositionToLocalPosition(kPacket.lX, kPacket.lY);

	//Tracef("CPythonNetworkStream::RecvFlyTargetingPacket - VID [%d]\n",kPacket.dwShooterVID);

	CPythonCharacterManager& rpcm = CPythonCharacterManager::Instance();

	CInstanceBase* pShooter = rpcm.GetInstancePtr(kPacket.dwShooterVID);

	if (!pShooter)
	{
#ifdef _DEBUG
		TraceError("CPythonNetworkStream::RecvFlyTargetingPacket() - dwShooterVID[%d] NOT EXIST", kPacket.dwShooterVID);
#endif
		return true;
	}

	CInstanceBase* pTarget = rpcm.GetInstancePtr(kPacket.dwTargetVID);

	if (kPacket.dwTargetVID && pTarget)
	{
		pShooter->GetGraphicThingInstancePtr()->SetFlyTarget(pTarget->GetGraphicThingInstancePtr());
	}
	else
	{
		float h = CPythonBackground::Instance().GetHeight(kPacket.lX, kPacket.lY) + 60.0f; // TEMPORARY HEIGHT
		pShooter->GetGraphicThingInstancePtr()->SetFlyTarget(D3DXVECTOR3(kPacket.lX, kPacket.lY, h));
		//pShooter->GetGraphicThingInstancePtr()->SetFlyTarget(kPacket.kPPosTarget.x,kPacket.kPPosTarget.y,);
	}

	return true;
}

bool CPythonNetworkStream::SendShootPacket(UINT uSkill)
{
	TPacketCGShoot kPacketShoot;
	kPacketShoot.bHeader = HEADER_CG_SHOOT;
	kPacketShoot.bType = uSkill;

	if (!Send(sizeof(kPacketShoot), &kPacketShoot))
	{
		Tracen("SendShootPacket Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendAddFlyTargetingPacket(DWORD dwTargetVID, const TPixelPosition& kPPosTarget)
{
	TPacketCGFlyTargeting packet;

	//CPythonCharacterManager & rpcm = CPythonCharacterManager::Instance();

	packet.bHeader = HEADER_CG_ADD_FLY_TARGETING;
	packet.dwTargetVID = dwTargetVID;
	packet.lX = kPPosTarget.x;
	packet.lY = kPPosTarget.y;

	__LocalPositionToGlobalPosition(packet.lX, packet.lY);

	if (!Send(sizeof(packet), &packet))
	{
		Tracen("Send FlyTargeting Packet Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendFlyTargetingPacket(DWORD dwTargetVID, const TPixelPosition& kPPosTarget)
{
	TPacketCGFlyTargeting packet;

	//CPythonCharacterManager & rpcm = CPythonCharacterManager::Instance();

	packet.bHeader = HEADER_CG_FLY_TARGETING;
	packet.dwTargetVID = dwTargetVID;
	packet.lX = kPPosTarget.x;
	packet.lY = kPPosTarget.y;

	__LocalPositionToGlobalPosition(packet.lX, packet.lY);

	if (!Send(sizeof(packet), &packet))
	{
		Tracen("Send FlyTargeting Packet Error");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::RecvCreateFlyPacket()
{
	TPacketGCCreateFly kPacket;
	if (!Recv(sizeof(TPacketGCCreateFly), &kPacket))
		return false;

	CFlyingManager& rkFlyMgr = CFlyingManager::Instance();
	CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();

	CInstanceBase* pkStartInst = rkChrMgr.GetInstancePtr(kPacket.dwStartVID);
	CInstanceBase* pkEndInst = rkChrMgr.GetInstancePtr(kPacket.dwEndVID);
	if (!pkStartInst || !pkEndInst)
		return true;

	rkFlyMgr.CreateIndexedFly(kPacket.bType, pkStartInst->GetGraphicThingInstancePtr(), pkEndInst->GetGraphicThingInstancePtr());

	return true;
}

bool CPythonNetworkStream::SendTargetPacket(DWORD dwVID)
{
	TPacketCGTarget packet;
	packet.header = HEADER_CG_TARGET;
	packet.dwVID = dwVID;

	if (!Send(sizeof(packet), &packet))
	{
		Tracen("Send Target Packet Error");
		return false;
	}

	return SendSequence();
}

#ifdef ENABLE_SKILL_COLOR_SYSTEM
bool CPythonNetworkStream::SendSkillColorPacket(BYTE skill, DWORD col1, DWORD col2, DWORD col3, DWORD col4, DWORD col5)
{
	TPacketCGSkillColor pack;
	pack.bheader = HEADER_CG_SKILL_COLOR;
	pack.skill = skill;
	pack.col1 = col1;
	pack.col2 = col2;
	pack.col3 = col3;
	pack.col4 = col4;
	pack.col5 = col5;

	if (!Send(sizeof(pack), &pack))
	{
		Tracen("Send Skill Color Packet Error");
		return false;
	}

	return true;
}
#endif

bool CPythonNetworkStream::SendSyncPositionElementPacket(DWORD dwVictimVID, DWORD dwVictimX, DWORD dwVictimY)
{
	TPacketCGSyncPositionElement kSyncPos;
	kSyncPos.dwVID = dwVictimVID;
	kSyncPos.lX = dwVictimX;
	kSyncPos.lY = dwVictimY;

	__LocalPositionToGlobalPosition(kSyncPos.lX, kSyncPos.lY);

	if (!Send(sizeof(kSyncPos), &kSyncPos))
	{
		Tracen("CPythonNetworkStream::SendSyncPositionElementPacket - ERROR");
		return false;
	}

	return true;
}

bool CPythonNetworkStream::RecvMessenger()
{
	TPacketGCMessenger p;
	if (!Recv(sizeof(p), &p))
		return false;

	int iSize = p.size - sizeof(p);
	char char_name[24 + 1];

	switch (p.subheader)
	{
	case MESSENGER_SUBHEADER_GC_LIST:
	{
		TPacketGCMessengerListOnline on;
		while (iSize)
		{
			if (!Recv(sizeof(TPacketGCMessengerListOffline), &on))
				return false;

			if (!Recv(on.length, char_name))
				return false;

			char_name[on.length] = 0;

			if (on.connected & MESSENGER_CONNECTED_STATE_ONLINE)
				CPythonMessenger::Instance().OnFriendLogin(char_name);
			else
				CPythonMessenger::Instance().OnFriendLogout(char_name);

			iSize -= sizeof(TPacketGCMessengerListOffline);
			iSize -= on.length;
		}
		break;
	}

	case MESSENGER_SUBHEADER_GC_LOGIN:
	{
		TPacketGCMessengerLogin p;
		if (!Recv(sizeof(p), &p))
			return false;
		if (!Recv(p.length, char_name))
			return false;
		char_name[p.length] = 0;
		CPythonMessenger::Instance().OnFriendLogin(char_name);
		__RefreshTargetBoardByName(char_name);
		break;
	}

	case MESSENGER_SUBHEADER_GC_LOGOUT:
	{
		TPacketGCMessengerLogout logout;
		if (!Recv(sizeof(logout), &logout))
			return false;
		if (!Recv(logout.length, char_name))
			return false;
		char_name[logout.length] = 0;
		CPythonMessenger::Instance().OnFriendLogout(char_name);
		break;
	}

#ifdef ENABLE_MESSENGER_TEAM
	case MESSENGER_SUBHEADER_GC_TEAM_LIST:
	{
		TPacketGCMessengerTeamListOnline on;
		while (iSize)
		{
			if (!Recv(sizeof(TPacketGCMessengerTeamListOffline), &on))
				return false;

			if (!Recv(on.length, char_name))
				return false;

			char_name[on.length] = 0;

			if (on.connected & MESSENGER_CONNECTED_STATE_ONLINE)
				CPythonMessenger::Instance().OnTeamLogin(char_name);
			else
				CPythonMessenger::Instance().OnTeamLogout(char_name);

			iSize -= sizeof(TPacketGCMessengerTeamListOffline);
			iSize -= on.length;
		}
		break;
	}

	case MESSENGER_SUBHEADER_GC_TEAM_LOGIN:
	{
		TPacketGCMessengerLogin p;
		if (!Recv(sizeof(p), &p))
			return false;
		if (!Recv(p.length, char_name))
			return false;
		char_name[p.length] = 0;
		CPythonMessenger::Instance().OnTeamLogin(char_name);
		__RefreshTargetBoardByName(char_name);
		break;
	}

	case MESSENGER_SUBHEADER_GC_TEAM_LOGOUT:
	{
		TPacketGCMessengerLogout logout;
		if (!Recv(sizeof(logout), &logout))
			return false;
		if (!Recv(logout.length, char_name))
			return false;
		char_name[logout.length] = 0;
		CPythonMessenger::Instance().OnTeamLogout(char_name);
		break;
	}
#endif


	}
	return true;
}

//////////////////////////////////////////////////////////////////////////
// Party

bool CPythonNetworkStream::SendPartyInvitePacket(DWORD dwVID)
{
	TPacketCGPartyInvite kPartyInvitePacket;
	kPartyInvitePacket.header = HEADER_CG_PARTY_INVITE;
	kPartyInvitePacket.vid = dwVID;

	if (!Send(sizeof(kPartyInvitePacket), &kPartyInvitePacket))
	{
		Tracenf("CPythonNetworkStream::SendPartyInvitePacket [%ud] - PACKET SEND ERROR", dwVID);
		return false;
	}

	Tracef(" << SendPartyInvitePacket : %d\n", dwVID);
	return SendSequence();
}

bool CPythonNetworkStream::SendPartyInviteAnswerPacket(DWORD dwLeaderVID, BYTE byAnswer)
{
	TPacketCGPartyInviteAnswer kPartyInviteAnswerPacket;
	kPartyInviteAnswerPacket.header = HEADER_CG_PARTY_INVITE_ANSWER;
	kPartyInviteAnswerPacket.leader_pid = dwLeaderVID;
	kPartyInviteAnswerPacket.accept = byAnswer;

	if (!Send(sizeof(kPartyInviteAnswerPacket), &kPartyInviteAnswerPacket))
	{
		Tracenf("CPythonNetworkStream::SendPartyInviteAnswerPacket [%ud %ud] - PACKET SEND ERROR", dwLeaderVID, byAnswer);
		return false;
	}

	Tracef(" << SendPartyInviteAnswerPacket : %d, %d\n", dwLeaderVID, byAnswer);
	return SendSequence();
}

bool CPythonNetworkStream::SendPartyRemovePacket(DWORD dwPID)
{
	TPacketCGPartyRemove kPartyInviteRemove;
	kPartyInviteRemove.header = HEADER_CG_PARTY_REMOVE;
	kPartyInviteRemove.pid = dwPID;

	if (!Send(sizeof(kPartyInviteRemove), &kPartyInviteRemove))
	{
		Tracenf("CPythonNetworkStream::SendPartyRemovePacket [%ud] - PACKET SEND ERROR", dwPID);
		return false;
	}

	Tracef(" << SendPartyRemovePacket : %d\n", dwPID);
	return SendSequence();
}

bool CPythonNetworkStream::SendPartySetStatePacket(DWORD dwVID, BYTE byState, BYTE byFlag)
{
	TPacketCGPartySetState kPartySetState;
	kPartySetState.byHeader = HEADER_CG_PARTY_SET_STATE;
	kPartySetState.dwVID = dwVID;
	kPartySetState.byState = byState;
	kPartySetState.byFlag = byFlag;

	if (!Send(sizeof(kPartySetState), &kPartySetState))
	{
		Tracenf("CPythonNetworkStream::SendPartySetStatePacket(%ud, %ud) - PACKET SEND ERROR", dwVID, byState);
		return false;
	}

	Tracef(" << SendPartySetStatePacket : %d, %d, %d\n", dwVID, byState, byFlag);
	return SendSequence();
}

bool CPythonNetworkStream::SendPartyUseSkillPacket(BYTE bySkillIndex, DWORD dwVID)
{
	TPacketCGPartyUseSkill kPartyUseSkill;
	kPartyUseSkill.byHeader = HEADER_CG_PARTY_USE_SKILL;
	kPartyUseSkill.bySkillIndex = bySkillIndex;
	kPartyUseSkill.dwTargetVID = dwVID;

	if (!Send(sizeof(kPartyUseSkill), &kPartyUseSkill))
	{
		Tracenf("CPythonNetworkStream::SendPartyUseSkillPacket(%ud, %ud) - PACKET SEND ERROR", bySkillIndex, dwVID);
		return false;
	}

	Tracef(" << SendPartyUseSkillPacket : %d, %d\n", bySkillIndex, dwVID);
	return SendSequence();
}

bool CPythonNetworkStream::SendPartyParameterPacket(BYTE byDistributeMode)
{
	TPacketCGPartyParameter kPartyParameter;
	kPartyParameter.bHeader = HEADER_CG_PARTY_PARAMETER;
	kPartyParameter.bDistributeMode = byDistributeMode;

	if (!Send(sizeof(kPartyParameter), &kPartyParameter))
	{
		Tracenf("CPythonNetworkStream::SendPartyParameterPacket(%d) - PACKET SEND ERROR", byDistributeMode);
		return false;
	}

	Tracef(" << SendPartyParameterPacket : %d\n", byDistributeMode);
	return SendSequence();
}

bool CPythonNetworkStream::RecvPartyInvite()
{
	TPacketGCPartyInvite kPartyInvitePacket;
	if (!Recv(sizeof(kPartyInvitePacket), &kPartyInvitePacket))
		return false;

	CInstanceBase* pInstance = CPythonCharacterManager::Instance().GetInstancePtr(kPartyInvitePacket.leader_pid);
	if (!pInstance)
	{
		TraceError(" CPythonNetworkStream::RecvPartyInvite - Failed to find leader instance [%d]\n", kPartyInvitePacket.leader_pid);
		return true;
	}

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RecvPartyInviteQuestion", Py_BuildValue("(is)", kPartyInvitePacket.leader_pid, pInstance->GetNameString()));
	Tracef(" >> RecvPartyInvite : %d, %s\n", kPartyInvitePacket.leader_pid, pInstance->GetNameString());

	return true;
}

bool CPythonNetworkStream::RecvPartyAdd()
{
	TPacketGCPartyAdd kPartyAddPacket;
	if (!Recv(sizeof(kPartyAddPacket), &kPartyAddPacket))
		return false;

	CPythonPlayer::Instance().AppendPartyMember(kPartyAddPacket.pid, kPartyAddPacket.name);
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "AddPartyMember", Py_BuildValue("(is)", kPartyAddPacket.pid, kPartyAddPacket.name));
	Tracef(" >> RecvPartyAdd : %d, %s\n", kPartyAddPacket.pid, kPartyAddPacket.name);

	return true;
}

bool CPythonNetworkStream::RecvPartyUpdate()
{
	TPacketGCPartyUpdate kPartyUpdatePacket;
	if (!Recv(sizeof(kPartyUpdatePacket), &kPartyUpdatePacket))
		return false;

	CPythonPlayer::TPartyMemberInfo* pPartyMemberInfo;
	if (!CPythonPlayer::Instance().GetPartyMemberPtr(kPartyUpdatePacket.pid, &pPartyMemberInfo))
		return true;

	BYTE byOldState = pPartyMemberInfo->byState;

	CPythonPlayer::Instance().UpdatePartyMemberInfo(kPartyUpdatePacket.pid, kPartyUpdatePacket.state, kPartyUpdatePacket.percent_hp);
	for (int i = 0; i < PARTY_AFFECT_SLOT_MAX_NUM; ++i)
	{
		CPythonPlayer::Instance().UpdatePartyMemberAffect(kPartyUpdatePacket.pid, i, kPartyUpdatePacket.affects[i]);
	}

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "UpdatePartyMemberInfo", Py_BuildValue("(i)", kPartyUpdatePacket.pid));

	DWORD dwVID;
	if (CPythonPlayer::Instance().PartyMemberPIDToVID(kPartyUpdatePacket.pid, &dwVID))
		if (byOldState != kPartyUpdatePacket.state)
		{
			__RefreshTargetBoardByVID(dwVID);
		}

	// 	Tracef(" >> RecvPartyUpdate : %d, %d, %d\n", kPartyUpdatePacket.pid, kPartyUpdatePacket.state, kPartyUpdatePacket.percent_hp);

	return true;
}

bool CPythonNetworkStream::RecvPartyRemove()
{
	TPacketGCPartyRemove kPartyRemovePacket;
	if (!Recv(sizeof(kPartyRemovePacket), &kPartyRemovePacket))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RemovePartyMember", Py_BuildValue("(i)", kPartyRemovePacket.pid));
	Tracef(" >> RecvPartyRemove : %d\n", kPartyRemovePacket.pid);

	return true;
}

bool CPythonNetworkStream::RecvPartyLink()
{
	TPacketGCPartyLink kPartyLinkPacket;
	if (!Recv(sizeof(kPartyLinkPacket), &kPartyLinkPacket))
		return false;

	CPythonPlayer::Instance().LinkPartyMember(kPartyLinkPacket.pid, kPartyLinkPacket.vid);
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "LinkPartyMember", Py_BuildValue("(ii)", kPartyLinkPacket.pid, kPartyLinkPacket.vid));
	Tracef(" >> RecvPartyLink : %d, %d\n", kPartyLinkPacket.pid, kPartyLinkPacket.vid);

	return true;
}

bool CPythonNetworkStream::RecvPartyUnlink()
{
	TPacketGCPartyUnlink kPartyUnlinkPacket;
	if (!Recv(sizeof(kPartyUnlinkPacket), &kPartyUnlinkPacket))
		return false;

	CPythonPlayer::Instance().UnlinkPartyMember(kPartyUnlinkPacket.pid);

	if (CPythonPlayer::Instance().IsMainCharacterIndex(kPartyUnlinkPacket.vid))
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "UnlinkAllPartyMember", Py_BuildValue("()"));
	}
	else
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "UnlinkPartyMember", Py_BuildValue("(i)", kPartyUnlinkPacket.pid));
	}

	Tracef(" >> RecvPartyUnlink : %d, %d\n", kPartyUnlinkPacket.pid, kPartyUnlinkPacket.vid);

	return true;
}

bool CPythonNetworkStream::RecvPartyParameter()
{
	TPacketGCPartyParameter kPartyParameterPacket;
	if (!Recv(sizeof(kPartyParameterPacket), &kPartyParameterPacket))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ChangePartyParameter", Py_BuildValue("(i)", kPartyParameterPacket.bDistributeMode));
	Tracef(" >> RecvPartyParameter : %d\n", kPartyParameterPacket.bDistributeMode);

	return true;
}

// Party
//////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////
// Guild

bool CPythonNetworkStream::SendGuildAddMemberPacket(DWORD dwVID)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_ADD_MEMBER;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;
	if (!Send(sizeof(dwVID), &dwVID))
		return false;

	Tracef(" SendGuildAddMemberPacket\n", dwVID);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildRemoveMemberPacket(DWORD dwPID)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_REMOVE_MEMBER;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;
	if (!Send(sizeof(dwPID), &dwPID))
		return false;

	Tracef(" SendGuildRemoveMemberPacket %d\n", dwPID);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildChangeGradeNamePacket(BYTE byGradeNumber, const char* c_szName)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_CHANGE_GRADE_NAME;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;
	if (!Send(sizeof(byGradeNumber), &byGradeNumber))
		return false;

	char szName[GUILD_GRADE_NAME_MAX_LEN + 1];
	strncpy(szName, c_szName, GUILD_GRADE_NAME_MAX_LEN);
	szName[GUILD_GRADE_NAME_MAX_LEN] = '\0';

	if (!Send(sizeof(szName), &szName))
		return false;

	Tracef(" SendGuildChangeGradeNamePacket %d, %s\n", byGradeNumber, c_szName);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildChangeGradeAuthorityPacket(BYTE byGradeNumber, BYTE byAuthority)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_CHANGE_GRADE_AUTHORITY;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;
	if (!Send(sizeof(byGradeNumber), &byGradeNumber))
		return false;
	if (!Send(sizeof(byAuthority), &byAuthority))
		return false;

	Tracef(" SendGuildChangeGradeAuthorityPacket %d, %d\n", byGradeNumber, byAuthority);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildOfferPacket(DWORD dwExperience)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_OFFER;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;
	if (!Send(sizeof(dwExperience), &dwExperience))
		return false;

	Tracef(" SendGuildOfferPacket %d\n", dwExperience);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildPostCommentPacket(const char* c_szMessage)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_POST_COMMENT;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;

	BYTE bySize = BYTE(strlen(c_szMessage)) + 1;
	if (!Send(sizeof(bySize), &bySize))
		return false;
	if (!Send(bySize, c_szMessage))
		return false;

	Tracef(" SendGuildPostCommentPacket %d, %s\n", bySize, c_szMessage);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildDeleteCommentPacket(DWORD dwIndex)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_DELETE_COMMENT;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;

	if (!Send(sizeof(dwIndex), &dwIndex))
		return false;

	Tracef(" SendGuildDeleteCommentPacket %d\n", dwIndex);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildRefreshCommentsPacket(DWORD dwHighestIndex)
{
	static DWORD s_LastTime = timeGetTime() - 1001;

	if (timeGetTime() - s_LastTime < 1000)
		return true;
	s_LastTime = timeGetTime();

	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_REFRESH_COMMENT;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;

	Tracef(" SendGuildRefreshCommentPacket %d\n", dwHighestIndex);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildChangeMemberGradePacket(DWORD dwPID, BYTE byGrade)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_CHANGE_MEMBER_GRADE;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;

	if (!Send(sizeof(dwPID), &dwPID))
		return false;
	if (!Send(sizeof(byGrade), &byGrade))
		return false;

	Tracef(" SendGuildChangeMemberGradePacket %d, %d\n", dwPID, byGrade);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildUseSkillPacket(DWORD dwSkillID, DWORD dwTargetVID)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_USE_SKILL;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;

	if (!Send(sizeof(dwSkillID), &dwSkillID))
		return false;
	if (!Send(sizeof(dwTargetVID), &dwTargetVID))
		return false;

	Tracef(" SendGuildUseSkillPacket %d, %d\n", dwSkillID, dwTargetVID);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildChangeMemberGeneralPacket(DWORD dwPID, BYTE byFlag)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_CHANGE_MEMBER_GENERAL;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;

	if (!Send(sizeof(dwPID), &dwPID))
		return false;
	if (!Send(sizeof(byFlag), &byFlag))
		return false;

	Tracef(" SendGuildChangeMemberGeneralFlagPacket %d, %d\n", dwPID, byFlag);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildInviteAnswerPacket(DWORD dwGuildID, BYTE byAnswer)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_GUILD_INVITE_ANSWER;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;

	if (!Send(sizeof(dwGuildID), &dwGuildID))
		return false;
	if (!Send(sizeof(byAnswer), &byAnswer))
		return false;

	Tracef(" SendGuildInviteAnswerPacket %d, %d\n", dwGuildID, byAnswer);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildChargeGSPPacket(DWORD dwMoney)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_CHARGE_GSP;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;

	if (!Send(sizeof(dwMoney), &dwMoney))
		return false;

	Tracef(" SendGuildChargeGSPPacket %d\n", dwMoney);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildDepositMoneyPacket(DWORD dwMoney)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_DEPOSIT_MONEY;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;
	if (!Send(sizeof(dwMoney), &dwMoney))
		return false;

	Tracef(" SendGuildDepositMoneyPacket %d\n", dwMoney);
	return SendSequence();
}

bool CPythonNetworkStream::SendGuildWithdrawMoneyPacket(DWORD dwMoney)
{
	TPacketCGGuild GuildPacket;
	GuildPacket.byHeader = HEADER_CG_GUILD;
	GuildPacket.bySubHeader = GUILD_SUBHEADER_CG_WITHDRAW_MONEY;
	if (!Send(sizeof(GuildPacket), &GuildPacket))
		return false;
	if (!Send(sizeof(dwMoney), &dwMoney))
		return false;

	Tracef(" SendGuildWithdrawMoneyPacket %d\n", dwMoney);
	return SendSequence();
}

bool CPythonNetworkStream::RecvGuild()
{
	TPacketGCGuild GuildPacket;
	if (!Recv(sizeof(GuildPacket), &GuildPacket))
		return false;

	switch (GuildPacket.subheader)
	{
	case GUILD_SUBHEADER_GC_LOGIN:
	{
		DWORD dwPID;
		if (!Recv(sizeof(DWORD), &dwPID))
			return false;

		// Messenger
		CPythonGuild::TGuildMemberData* pGuildMemberData;
		if (CPythonGuild::Instance().GetMemberDataPtrByPID(dwPID, &pGuildMemberData))
			if (0 != pGuildMemberData->strName.compare(CPythonPlayer::Instance().GetName()))
				CPythonMessenger::Instance().LoginGuildMember(pGuildMemberData->strName.c_str());

		//Tracef(" <Login> %d\n", dwPID);
		break;
	}
	case GUILD_SUBHEADER_GC_LOGOUT:
	{
		DWORD dwPID;
		if (!Recv(sizeof(DWORD), &dwPID))
			return false;

		// Messenger
		CPythonGuild::TGuildMemberData* pGuildMemberData;
		if (CPythonGuild::Instance().GetMemberDataPtrByPID(dwPID, &pGuildMemberData))
			if (0 != pGuildMemberData->strName.compare(CPythonPlayer::Instance().GetName()))
				CPythonMessenger::Instance().LogoutGuildMember(pGuildMemberData->strName.c_str());

		//Tracef(" <Logout> %d\n", dwPID);
		break;
	}
	case GUILD_SUBHEADER_GC_REMOVE:
	{
		DWORD dwPID;
		if (!Recv(sizeof(dwPID), &dwPID))
			return false;

		if (CPythonGuild::Instance().IsMainPlayer(dwPID))
		{
			CPythonGuild::Instance().Destroy();
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "DeleteGuild", Py_BuildValue("()"));
			CPythonMessenger::Instance().RemoveAllGuildMember();
			__SetGuildID(0);
			__RefreshMessengerWindow();
			__RefreshTargetBoard();
			__RefreshCharacterWindow();
		}
		else
		{
			// Get Member Name
			std::string strMemberName = "";
			CPythonGuild::TGuildMemberData* pData;
			if (CPythonGuild::Instance().GetMemberDataPtrByPID(dwPID, &pData))
			{
				strMemberName = pData->strName;
				CPythonMessenger::Instance().RemoveGuildMember(pData->strName.c_str());
			}

			CPythonGuild::Instance().RemoveMember(dwPID);

			// Refresh
			__RefreshTargetBoardByName(strMemberName.c_str());
			__RefreshGuildWindowMemberPage();
		}

		Tracef(" <Remove> %d\n", dwPID);
		break;
	}
	case GUILD_SUBHEADER_GC_LIST:
	{
		int iPacketSize = int(GuildPacket.size) - sizeof(GuildPacket);

		for (; iPacketSize > 0;)
		{
			TPacketGCGuildSubMember memberPacket;
			if (!Recv(sizeof(memberPacket), &memberPacket))
				return false;

			char szName[CHARACTER_NAME_MAX_LEN + 1] = "";
			if (memberPacket.byNameFlag)
			{
				if (!Recv(sizeof(szName), &szName))
					return false;

				iPacketSize -= CHARACTER_NAME_MAX_LEN + 1;
			}
			else
			{
				CPythonGuild::TGuildMemberData* pMemberData;
				if (CPythonGuild::Instance().GetMemberDataPtrByPID(memberPacket.pid, &pMemberData))
				{
					strncpy(szName, pMemberData->strName.c_str(), CHARACTER_NAME_MAX_LEN);
				}
			}

			//Tracef(" <List> %d : %s, %d (%d, %d, %d)\n", memberPacket.pid, szName, memberPacket.byGrade, memberPacket.byJob, memberPacket.byLevel, memberPacket.dwOffer);

			CPythonGuild::SGuildMemberData GuildMemberData;
			GuildMemberData.dwPID = memberPacket.pid;
			GuildMemberData.byGrade = memberPacket.byGrade;
			GuildMemberData.strName = szName;
			GuildMemberData.byJob = memberPacket.byJob;
			GuildMemberData.byLevel = memberPacket.byLevel;
			GuildMemberData.dwOffer = memberPacket.dwOffer;
			GuildMemberData.byGeneralFlag = memberPacket.byIsGeneral;
			CPythonGuild::Instance().RegisterMember(GuildMemberData);

			// Messenger
			if (strcmp(szName, CPythonPlayer::Instance().GetName()))
				CPythonMessenger::Instance().AppendGuildMember(szName);

			__RefreshTargetBoardByName(szName);

			iPacketSize -= sizeof(memberPacket);
		}

		__RefreshGuildWindowInfoPage();
		__RefreshGuildWindowMemberPage();
		__RefreshMessengerWindow();
		__RefreshCharacterWindow();
		break;
	}
	case GUILD_SUBHEADER_GC_GRADE:
	{
		BYTE byCount;
		if (!Recv(sizeof(byCount), &byCount))
			return false;

		for (BYTE i = 0; i < byCount; ++i)
		{
			BYTE byIndex;
			if (!Recv(sizeof(byCount), &byIndex))
				return false;
			TPacketGCGuildSubGrade GradePacket;
			if (!Recv(sizeof(GradePacket), &GradePacket))
				return false;

			CPythonGuild::Instance().SetGradeData(byIndex, CPythonGuild::SGuildGradeData(GradePacket.auth_flag, GradePacket.grade_name));
			//Tracef(" <Grade> [%d/%d] : %s, %d\n", byIndex, byCount, GradePacket.grade_name, GradePacket.auth_flag);
		}
		__RefreshGuildWindowGradePage();
		__RefreshGuildWindowMemberPageGradeComboBox();
		break;
	}
	case GUILD_SUBHEADER_GC_GRADE_NAME:
	{
		BYTE byGradeNumber;
		if (!Recv(sizeof(byGradeNumber), &byGradeNumber))
			return false;

		char szGradeName[GUILD_GRADE_NAME_MAX_LEN + 1] = "";
		if (!Recv(sizeof(szGradeName), &szGradeName))
			return false;

		CPythonGuild::Instance().SetGradeName(byGradeNumber, szGradeName);
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshGuildGrade", Py_BuildValue("()"));

		Tracef(" <Change Grade Name> %d, %s\n", byGradeNumber, szGradeName);
		__RefreshGuildWindowGradePage();
		__RefreshGuildWindowMemberPageGradeComboBox();
		break;
	}
	case GUILD_SUBHEADER_GC_GRADE_AUTH:
	{
		BYTE byGradeNumber;
		if (!Recv(sizeof(byGradeNumber), &byGradeNumber))
			return false;
		BYTE byAuthorityFlag;
		if (!Recv(sizeof(byAuthorityFlag), &byAuthorityFlag))
			return false;

		CPythonGuild::Instance().SetGradeAuthority(byGradeNumber, byAuthorityFlag);
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshGuildGrade", Py_BuildValue("()"));

		Tracef(" <Change Grade Authority> %d, %d\n", byGradeNumber, byAuthorityFlag);
		__RefreshGuildWindowGradePage();
		break;
	}
	case GUILD_SUBHEADER_GC_INFO:
	{
		TPacketGCGuildInfo GuildInfo;
		if (!Recv(sizeof(GuildInfo), &GuildInfo))
			return false;

		CPythonGuild::Instance().EnableGuild();
		CPythonGuild::TGuildInfo& rGuildInfo = CPythonGuild::Instance().GetGuildInfoRef();
		strncpy(rGuildInfo.szGuildName, GuildInfo.name, GUILD_NAME_MAX_LEN);
		rGuildInfo.szGuildName[GUILD_NAME_MAX_LEN] = '\0';

		rGuildInfo.dwGuildID = GuildInfo.guild_id;
		rGuildInfo.dwMasterPID = GuildInfo.master_pid;
		rGuildInfo.dwGuildLevel = GuildInfo.level;
		rGuildInfo.dwCurrentExperience = GuildInfo.exp;
		rGuildInfo.dwCurrentMemberCount = GuildInfo.member_count;
		rGuildInfo.dwMaxMemberCount = GuildInfo.max_member_count;
		rGuildInfo.dwGuildMoney = GuildInfo.gold;
		rGuildInfo.bHasLand = GuildInfo.hasLand;

		//Tracef(" <Info> %s, %d, %d : %d\n", GuildInfo.name, GuildInfo.master_pid, GuildInfo.level, rGuildInfo.bHasLand);
		__RefreshGuildWindowInfoPage();
		break;
	}
	case GUILD_SUBHEADER_GC_COMMENTS:
	{
		BYTE byCount;
		if (!Recv(sizeof(byCount), &byCount))
			return false;

		CPythonGuild::Instance().ClearComment();
		//Tracef(" >>> Comments Count : %d\n", byCount);

		for (BYTE i = 0; i < byCount; ++i)
		{
			DWORD dwCommentID;
			if (!Recv(sizeof(dwCommentID), &dwCommentID))
				return false;

			char szName[CHARACTER_NAME_MAX_LEN + 1] = "";
			if (!Recv(sizeof(szName), &szName))
				return false;

			char szComment[GULID_COMMENT_MAX_LEN + 1] = "";
			if (!Recv(sizeof(szComment), &szComment))
				return false;

			//Tracef(" [Comment-%d] : %s, %s\n", dwCommentID, szName, szComment);
			CPythonGuild::Instance().RegisterComment(dwCommentID, szName, szComment);
		}

		__RefreshGuildWindowBoardPage();
		break;
	}
	case GUILD_SUBHEADER_GC_CHANGE_EXP:
	{
		BYTE byLevel;
		if (!Recv(sizeof(byLevel), &byLevel))
			return false;
		DWORD dwEXP;
		if (!Recv(sizeof(dwEXP), &dwEXP))
			return false;
		CPythonGuild::Instance().SetGuildEXP(byLevel, dwEXP);
		Tracef(" <ChangeEXP> %d, %d\n", byLevel, dwEXP);
		__RefreshGuildWindowInfoPage();
		break;
	}
	case GUILD_SUBHEADER_GC_CHANGE_MEMBER_GRADE:
	{
		DWORD dwPID;
		if (!Recv(sizeof(dwPID), &dwPID))
			return false;
		BYTE byGrade;
		if (!Recv(sizeof(byGrade), &byGrade))
			return false;
		CPythonGuild::Instance().ChangeGuildMemberGrade(dwPID, byGrade);
		Tracef(" <ChangeMemberGrade> %d, %d\n", dwPID, byGrade);
		__RefreshGuildWindowMemberPage();
		break;
	}
	case GUILD_SUBHEADER_GC_SKILL_INFO:
	{
		CPythonGuild::TGuildSkillData& rSkillData = CPythonGuild::Instance().GetGuildSkillDataRef();
		if (!Recv(sizeof(rSkillData.bySkillPoint), &rSkillData.bySkillPoint))
			return false;
		if (!Recv(sizeof(rSkillData.bySkillLevel), rSkillData.bySkillLevel))
			return false;
		if (!Recv(sizeof(rSkillData.wGuildPoint), &rSkillData.wGuildPoint))
			return false;
		if (!Recv(sizeof(rSkillData.wMaxGuildPoint), &rSkillData.wMaxGuildPoint))
			return false;

		Tracef(" <SkillInfo> %d / %d, %d\n", rSkillData.bySkillPoint, rSkillData.wGuildPoint, rSkillData.wMaxGuildPoint);
		__RefreshGuildWindowSkillPage();
		break;
	}
	case GUILD_SUBHEADER_GC_CHANGE_MEMBER_GENERAL:
	{
		DWORD dwPID;
		if (!Recv(sizeof(dwPID), &dwPID))
			return false;
		BYTE byFlag;
		if (!Recv(sizeof(byFlag), &byFlag))
			return false;

		CPythonGuild::Instance().ChangeGuildMemberGeneralFlag(dwPID, byFlag);
		Tracef(" <ChangeMemberGeneralFlag> %d, %d\n", dwPID, byFlag);
		__RefreshGuildWindowMemberPage();
		break;
	}
	case GUILD_SUBHEADER_GC_GUILD_INVITE:
	{
		DWORD dwGuildID;
		if (!Recv(sizeof(dwGuildID), &dwGuildID))
			return false;
		char szGuildName[GUILD_NAME_MAX_LEN + 1];
		if (!Recv(GUILD_NAME_MAX_LEN, &szGuildName))
			return false;

		szGuildName[GUILD_NAME_MAX_LEN] = 0;

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RecvGuildInviteQuestion", Py_BuildValue("(is)", dwGuildID, szGuildName));
		Tracef(" <Guild Invite> %d, %s\n", dwGuildID, szGuildName);
		break;
	}
	case GUILD_SUBHEADER_GC_WAR:
	{
		TPacketGCGuildWar kGuildWar;
		if (!Recv(sizeof(kGuildWar), &kGuildWar))
			return false;

		switch (kGuildWar.bWarState)
		{
		case GUILD_WAR_SEND_DECLARE:
			Tracef(" >> GUILD_SUBHEADER_GC_WAR : GUILD_WAR_SEND_DECLARE\n");
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
				"BINARY_GuildWar_OnSendDeclare",
				Py_BuildValue("(i)", kGuildWar.dwGuildOpp)
			);
			break;
		case GUILD_WAR_RECV_DECLARE:
			Tracef(" >> GUILD_SUBHEADER_GC_WAR : GUILD_WAR_RECV_DECLARE\n");
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
				"BINARY_GuildWar_OnRecvDeclare",
				Py_BuildValue("(ii)", kGuildWar.dwGuildOpp, kGuildWar.bType)
			);
			break;
		case GUILD_WAR_ON_WAR:
			Tracef(" >> GUILD_SUBHEADER_GC_WAR : GUILD_WAR_ON_WAR : %d, %d\n", kGuildWar.dwGuildSelf, kGuildWar.dwGuildOpp);
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
				"BINARY_GuildWar_OnStart",
				Py_BuildValue("(ii)", kGuildWar.dwGuildSelf, kGuildWar.dwGuildOpp)
			);
			CPythonGuild::Instance().StartGuildWar(kGuildWar.dwGuildOpp);
			break;
		case GUILD_WAR_END:
			Tracef(" >> GUILD_SUBHEADER_GC_WAR : GUILD_WAR_END\n");
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
				"BINARY_GuildWar_OnEnd",
				Py_BuildValue("(ii)", kGuildWar.dwGuildSelf, kGuildWar.dwGuildOpp)
			);
			CPythonGuild::Instance().EndGuildWar(kGuildWar.dwGuildOpp);
			break;
		}
		break;
	}
	case GUILD_SUBHEADER_GC_GUILD_NAME:
	{
		DWORD dwID;
		char szGuildName[GUILD_NAME_MAX_LEN + 1];

		int iPacketSize = int(GuildPacket.size) - sizeof(GuildPacket);

		int nItemSize = sizeof(dwID) + GUILD_NAME_MAX_LEN;

		assert(iPacketSize % nItemSize == 0 && "GUILD_SUBHEADER_GC_GUILD_NAME");

		for (; iPacketSize > 0;)
		{
			if (!Recv(sizeof(dwID), &dwID))
				return false;

			if (!Recv(GUILD_NAME_MAX_LEN, &szGuildName))
				return false;

			szGuildName[GUILD_NAME_MAX_LEN] = 0;

			//Tracef(" >> GulidName [%d : %s]\n", dwID, szGuildName);
			CPythonGuild::Instance().RegisterGuildName(dwID, szGuildName);
			iPacketSize -= nItemSize;
		}
		break;
	}
	case GUILD_SUBHEADER_GC_GUILD_WAR_LIST:
	{
		DWORD dwSrcGuildID;
		DWORD dwDstGuildID;

		int iPacketSize = int(GuildPacket.size) - sizeof(GuildPacket);
		int nItemSize = sizeof(dwSrcGuildID) + sizeof(dwDstGuildID);

		assert(iPacketSize % nItemSize == 0 && "GUILD_SUBHEADER_GC_GUILD_WAR_LIST");

		for (; iPacketSize > 0;)
		{
			if (!Recv(sizeof(dwSrcGuildID), &dwSrcGuildID))
				return false;

			if (!Recv(sizeof(dwDstGuildID), &dwDstGuildID))
				return false;

			Tracef(" >> GulidWarList [%d vs %d]\n", dwSrcGuildID, dwDstGuildID);
			CInstanceBase::InsertGVGKey(dwSrcGuildID, dwDstGuildID);
			CPythonCharacterManager::Instance().ChangeGVG(dwSrcGuildID, dwDstGuildID);
			iPacketSize -= nItemSize;
		}
		break;
	}
	case GUILD_SUBHEADER_GC_GUILD_WAR_END_LIST:
	{
		DWORD dwSrcGuildID;
		DWORD dwDstGuildID;

		int iPacketSize = int(GuildPacket.size) - sizeof(GuildPacket);
		int nItemSize = sizeof(dwSrcGuildID) + sizeof(dwDstGuildID);

		assert(iPacketSize % nItemSize == 0 && "GUILD_SUBHEADER_GC_GUILD_WAR_END_LIST");

		for (; iPacketSize > 0;)
		{
			if (!Recv(sizeof(dwSrcGuildID), &dwSrcGuildID))
				return false;

			if (!Recv(sizeof(dwDstGuildID), &dwDstGuildID))
				return false;

			Tracef(" >> GulidWarEndList [%d vs %d]\n", dwSrcGuildID, dwDstGuildID);
			CInstanceBase::RemoveGVGKey(dwSrcGuildID, dwDstGuildID);
			CPythonCharacterManager::Instance().ChangeGVG(dwSrcGuildID, dwDstGuildID);
			iPacketSize -= nItemSize;
		}
		break;
	}
	case GUILD_SUBHEADER_GC_WAR_POINT:
	{
		TPacketGuildWarPoint GuildWarPoint;
		if (!Recv(sizeof(GuildWarPoint), &GuildWarPoint))
			return false;

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
			"BINARY_GuildWar_OnRecvPoint",
			Py_BuildValue("(iii)", GuildWarPoint.dwGainGuildID, GuildWarPoint.dwOpponentGuildID, GuildWarPoint.lPoint)
		);
		break;
	}
	case GUILD_SUBHEADER_GC_MONEY_CHANGE:
	{
		DWORD dwMoney;
		if (!Recv(sizeof(dwMoney), &dwMoney))
			return false;

		CPythonGuild::Instance().SetGuildMoney(dwMoney);

		__RefreshGuildWindowInfoPage();
		Tracef(" >> Guild Money Change : %d\n", dwMoney);
		break;
	}
	}

	return true;
}

// Guild
//////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////
// Fishing

bool CPythonNetworkStream::SendFishingPacket(int iRotation)
{
#ifdef ENABLE_BOT_CONTROL
	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();
	if (rkPlayer.GetBotControlState())
	{
		if (rkPlayer.GetBotControlWindow())
			return true;

		rkPlayer.SetBotControWindow(true);
		rkPlayer.OpenBotControlWindow();
		return true;
	}
#endif

	BYTE byHeader = HEADER_CG_FISHING;
	if (!Send(sizeof(byHeader), &byHeader))
		return false;
	BYTE byPacketRotation = iRotation / 5;
	if (!Send(sizeof(BYTE), &byPacketRotation))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendGiveItemPacket(DWORD dwTargetVID, TItemPos ItemPos, int iItemCount)
{
	TPacketCGGiveItem GiveItemPacket;
	GiveItemPacket.byHeader = HEADER_CG_GIVE_ITEM;
	GiveItemPacket.dwTargetVID = dwTargetVID;
	GiveItemPacket.ItemPos = ItemPos;
	GiveItemPacket.byItemCount = iItemCount;

	if (!Send(sizeof(GiveItemPacket), &GiveItemPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::RecvFishing()
{
	TPacketGCFishing FishingPacket;
	if (!Recv(sizeof(FishingPacket), &FishingPacket))
		return false;

	CInstanceBase* pFishingInstance = NULL;
	if (FISHING_SUBHEADER_GC_FISH != FishingPacket.subheader)
	{
		pFishingInstance = CPythonCharacterManager::Instance().GetInstancePtr(FishingPacket.info);
		if (!pFishingInstance)
			return true;
	}

	switch (FishingPacket.subheader)
	{
	case FISHING_SUBHEADER_GC_START:
		pFishingInstance->StartFishing(float(FishingPacket.dir) * 5.0f);
		break;
	case FISHING_SUBHEADER_GC_STOP:
		if (pFishingInstance->IsFishing())
			pFishingInstance->StopFishing();
		break;
	case FISHING_SUBHEADER_GC_REACT:
		if (pFishingInstance->IsFishing())
		{
			pFishingInstance->SetFishEmoticon(); // Fish Emoticon
			pFishingInstance->ReactFishing();
		}
		break;
	case FISHING_SUBHEADER_GC_SUCCESS:
		pFishingInstance->CatchSuccess();
		break;
	case FISHING_SUBHEADER_GC_FAIL:
		pFishingInstance->CatchFail();
		if (pFishingInstance == CPythonCharacterManager::Instance().GetMainInstancePtr())
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnFishingFailure", Py_BuildValue("()"));
		}
		break;
	case FISHING_SUBHEADER_GC_FISH:
	{
		DWORD dwFishID = FishingPacket.info;

		if (0 == FishingPacket.info)
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnFishingNotifyUnknown", Py_BuildValue("()"));
			return true;
		}

		CItemData* pItemData;
		if (!CItemManager::Instance().GetItemDataPointer(dwFishID, &pItemData))
			return true;

		CInstanceBase* pMainInstance = CPythonCharacterManager::Instance().GetMainInstancePtr();
		if (!pMainInstance)
			return true;

		if (pMainInstance->IsFishing())
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnFishingNotify", Py_BuildValue("(is)", CItemData::ITEM_TYPE_FISH == pItemData->GetType(), pItemData->GetName()));
		}
		else
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnFishingSuccess", Py_BuildValue("(is)", CItemData::ITEM_TYPE_FISH == pItemData->GetType(), pItemData->GetName()));
		}
		break;
	}
	}

	return true;
}
// Fishing
/////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////
// Dungeon
bool CPythonNetworkStream::RecvDungeon()
{
	TPacketGCDungeon DungeonPacket;
	if (!Recv(sizeof(DungeonPacket), &DungeonPacket))
		return false;

	switch (DungeonPacket.subheader)
	{
	case DUNGEON_SUBHEADER_GC_TIME_ATTACK_START:
	{
		break;
	}
	case DUNGEON_SUBHEADER_GC_DESTINATION_POSITION:
	{
		unsigned long ulx, uly;
		if (!Recv(sizeof(ulx), &ulx))
			return false;
		if (!Recv(sizeof(uly), &uly))
			return false;

		CPythonPlayer::Instance().SetDungeonDestinationPosition(ulx, uly);
		break;
	}
	}

	return true;
}
// Dungeon
/////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////
// MyShop
bool CPythonNetworkStream::SendBuildPrivateShopPacket(const char* c_szName, const std::vector<TShopItemTable>& c_rSellingItemStock)
{
	TPacketCGMyShop packet;
	packet.bHeader = HEADER_CG_MYSHOP;
	strncpy(packet.szSign, c_szName, SHOP_SIGN_MAX_LEN);
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	packet.bCount = static_cast<MAX_COUNT>(c_rSellingItemStock.size());
#else
	packet.bCount = static_cast<BYTE>(c_rSellingItemStock.size());
#endif
	if (!Send(sizeof(packet), &packet))
		return false;

	for (std::vector<TShopItemTable>::const_iterator itor = c_rSellingItemStock.begin(); itor < c_rSellingItemStock.end(); ++itor)
	{
		const TShopItemTable& c_rItem = *itor;
		if (!Send(sizeof(c_rItem), &c_rItem))
			return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::RecvShopSignPacket()
{
	TPacketGCShopSign p;
	if (!Recv(sizeof(TPacketGCShopSign), &p))
		return false;

	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();

	if (0 == strlen(p.szSign))
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
			"BINARY_PrivateShop_Disappear",
			Py_BuildValue("(i)", p.dwVID)
		);

		if (rkPlayer.IsMainCharacterIndex(p.dwVID))
			rkPlayer.ClosePrivateShop();
	}
	else
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
			"BINARY_PrivateShop_Appear",
			Py_BuildValue("(is)", p.dwVID, p.szSign)
		);

		if (rkPlayer.IsMainCharacterIndex(p.dwVID))
			rkPlayer.OpenPrivateShop();
	}

	return true;
}
/////////////////////////////////////////////////////////////////////////

bool CPythonNetworkStream::RecvTimePacket()
{
	TPacketGCTime TimePacket;
	if (!Recv(sizeof(TimePacket), &TimePacket))
		return false;

	IAbstractApplication& rkApp = IAbstractApplication::GetSingleton();
	rkApp.SetServerTime(TimePacket.time);

	return true;
}

bool CPythonNetworkStream::RecvWalkModePacket()
{
	TPacketGCWalkMode WalkModePacket;
	if (!Recv(sizeof(WalkModePacket), &WalkModePacket))
		return false;

	CInstanceBase* pInstance = CPythonCharacterManager::Instance().GetInstancePtr(WalkModePacket.vid);
	if (pInstance)
	{
		if (WALKMODE_RUN == WalkModePacket.mode)
		{
			pInstance->SetRunMode();
		}
		else
		{
			pInstance->SetWalkMode();
		}
	}

	return true;
}

bool CPythonNetworkStream::RecvChangeSkillGroupPacket()
{
	TPacketGCChangeSkillGroup ChangeSkillGroup;
	if (!Recv(sizeof(ChangeSkillGroup), &ChangeSkillGroup))
		return false;

	m_dwMainActorSkillGroup = ChangeSkillGroup.skill_group;

	CPythonPlayer::Instance().NEW_ClearSkillData();
	__RefreshCharacterWindow();
	return true;
}

void CPythonNetworkStream::__TEST_SetSkillGroupFake(int iIndex)
{
	m_dwMainActorSkillGroup = DWORD(iIndex);

	CPythonPlayer::Instance().NEW_ClearSkillData();
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshCharacter", Py_BuildValue("()"));
}

bool CPythonNetworkStream::SendRefinePacket(BYTE byPos, BYTE byType)
{
	TPacketCGRefine kRefinePacket;
	kRefinePacket.header = HEADER_CG_REFINE;
	kRefinePacket.pos = byPos;
	kRefinePacket.type = byType;

	if (!Send(sizeof(kRefinePacket), &kRefinePacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendSelectItemPacket(DWORD dwItemPos)
{
	TPacketCGScriptSelectItem kScriptSelectItem;
	kScriptSelectItem.header = HEADER_CG_SCRIPT_SELECT_ITEM;
	kScriptSelectItem.selection = dwItemPos;

	if (!Send(sizeof(kScriptSelectItem), &kScriptSelectItem))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::RecvRefineInformationPacket()
{
	TPacketGCRefineInformation kRefineInfoPacket;
	if (!Recv(sizeof(kRefineInfoPacket), &kRefineInfoPacket))
		return false;

	TRefineTable& rkRefineTable = kRefineInfoPacket.refine_table;
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
		"OpenRefineDialog",
#ifdef ENABLE_EXTENDED_YANG_LIMIT
		Py_BuildValue("(iiLi)",
#else
			Py_BuildValue("(iiii)",
#endif
				kRefineInfoPacket.pos,
				kRefineInfoPacket.refine_table.result_vnum,
				rkRefineTable.cost,
				rkRefineTable.prob));

	for (int i = 0; i < rkRefineTable.material_count; ++i)
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "AppendMaterialToRefineDialog", Py_BuildValue("(ii)", rkRefineTable.materials[i].vnum, rkRefineTable.materials[i].count));
	}

#ifdef _DEBUG
	Tracef(" >> RecvRefineInformationPacket(pos=%d, result_vnum=%d, cost=%d, prob=%d)\n",
		kRefineInfoPacket.pos,
		kRefineInfoPacket.refine_table.result_vnum,
		rkRefineTable.cost,
		rkRefineTable.prob);
#endif

	return true;
}

bool CPythonNetworkStream::RecvRefineInformationPacketNew()
{
	TPacketGCRefineInformationNew kRefineInfoPacket;
	if (!Recv(sizeof(kRefineInfoPacket), &kRefineInfoPacket))
		return false;

	TRefineTable& rkRefineTable = kRefineInfoPacket.refine_table;
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
		"OpenRefineDialog",
#ifdef ENABLE_EXTENDED_YANG_LIMIT
		Py_BuildValue("(iiLii)",
#else
			Py_BuildValue("(iiiii)",
#endif
				kRefineInfoPacket.pos,
				kRefineInfoPacket.refine_table.result_vnum,
				rkRefineTable.cost,
				rkRefineTable.prob,
				kRefineInfoPacket.type)
		);

	for (int i = 0; i < rkRefineTable.material_count; ++i)
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "AppendMaterialToRefineDialog", Py_BuildValue("(ii)", rkRefineTable.materials[i].vnum, rkRefineTable.materials[i].count));
	}

#ifdef _DEBUG
	Tracef(" >> RecvRefineInformationPacketNew(pos=%d, result_vnum=%d, cost=%d, prob=%d, type=%d)\n",
		kRefineInfoPacket.pos,
		kRefineInfoPacket.refine_table.result_vnum,
		rkRefineTable.cost,
		rkRefineTable.prob,
		kRefineInfoPacket.type);
#endif

	return true;
}

bool CPythonNetworkStream::RecvNPCList()
{
	TPacketGCNPCPosition kNPCPosition;
	if (!Recv(sizeof(kNPCPosition), &kNPCPosition))
		return false;

	assert(int(kNPCPosition.size) - sizeof(kNPCPosition) == kNPCPosition.count * sizeof(TNPCPosition) && "HEADER_GC_NPC_POSITION");

	CPythonMiniMap::Instance().ClearAtlasMarkInfo();

	for (int i = 0; i < kNPCPosition.count; ++i)
	{
		TNPCPosition NPCPosition;
		if (!Recv(sizeof(TNPCPosition), &NPCPosition))
			return false;

		CPythonMiniMap::Instance().RegisterAtlasMark(NPCPosition.bType, NPCPosition.name, NPCPosition.x, NPCPosition.y);
	}

	return true;
}

bool CPythonNetworkStream::__SendCRCReportPacket()
{
	return true;
}

bool CPythonNetworkStream::RecvAffectAddPacket()
{
	TPacketGCAffectAdd kAffectAdd;
	if (!Recv(sizeof(kAffectAdd), &kAffectAdd))
		return false;

	TPacketAffectElement& rkElement = kAffectAdd.elem;
	if (rkElement.bPointIdxApplyOn == POINT_ENERGY)
	{
		CPythonPlayer::instance().SetStatus(POINT_ENERGY_END_TIME, CPythonApplication::Instance().GetServerTimeStamp() + rkElement.lDuration);
		__RefreshStatus();
	}

#ifdef ENABLE_CHECK_EFFECT
	CPythonPlayer::instance().AddAffect(rkElement.dwType, kAffectAdd.elem);
#endif

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_NEW_AddAffect", Py_BuildValue("(iiii)", rkElement.dwType, rkElement.bPointIdxApplyOn, rkElement.lApplyValue, rkElement.lDuration));

	return true;
}

bool CPythonNetworkStream::RecvAffectRemovePacket()
{
	TPacketGCAffectRemove kAffectRemove;
	if (!Recv(sizeof(kAffectRemove), &kAffectRemove))
		return false;

#ifdef ENABLE_CHECK_EFFECT
	CPythonPlayer::instance().RemoveAffect(kAffectRemove.dwType, kAffectRemove.bApplyOn);
#endif

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_NEW_RemoveAffect", Py_BuildValue("(ii)", kAffectRemove.dwType, kAffectRemove.bApplyOn));

	return true;
}

bool CPythonNetworkStream::RecvChannelPacket()
{
	TPacketGCChannel kChannelPacket;
	if (!Recv(sizeof(kChannelPacket), &kChannelPacket))
		return false;

	//Tracef(" >> CPythonNetworkStream::RecvChannelPacket(channel=%d)\n", kChannelPacket.channel);
#ifdef ENABLE_CHANNEL_INFO_UPDATE
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ReceiveChannel", Py_BuildValue("(i)", kChannelPacket.channel));
#endif
	return true;
}

bool CPythonNetworkStream::RecvViewEquipPacket()
{
	TPacketGCViewEquip kViewEquipPacket;
	if (!Recv(sizeof(kViewEquipPacket), &kViewEquipPacket))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OpenEquipmentDialog", Py_BuildValue("(i)", kViewEquipPacket.dwVID));

	for (int i = 0; i < WEAR_MAX_NUM; ++i)
	{
		TEquipmentItemSet& rItemSet = kViewEquipPacket.equips[i];
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetEquipmentDialogItem", Py_BuildValue("(iiii)", kViewEquipPacket.dwVID, i, rItemSet.vnum, rItemSet.count));

		for (int j = 0; j < ITEM_SOCKET_SLOT_MAX_NUM; ++j)
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetEquipmentDialogSocket", Py_BuildValue("(iiii)", kViewEquipPacket.dwVID, i, j, rItemSet.alSockets[j]));

		for (int k = 0; k < ITEM_ATTRIBUTE_SLOT_MAX_NUM; ++k)
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetEquipmentDialogAttr", Py_BuildValue("(iiiii)", kViewEquipPacket.dwVID, i, k, rItemSet.aAttr[k].bType, rItemSet.aAttr[k].sValue));
	}

	return true;
}

bool CPythonNetworkStream::RecvLandPacket()
{
	TPacketGCLandList kLandList;
	if (!Recv(sizeof(kLandList), &kLandList))
		return false;

	std::vector<DWORD> kVec_dwGuildID;

	CPythonMiniMap& rkMiniMap = CPythonMiniMap::Instance();
	CPythonBackground& rkBG = CPythonBackground::Instance();
	CInstanceBase* pMainInstance = CPythonPlayer::Instance().NEW_GetMainActorPtr();

	rkMiniMap.ClearGuildArea();
	rkBG.ClearGuildArea();

	int iPacketSize = (kLandList.size - sizeof(TPacketGCLandList));
	for (; iPacketSize > 0; iPacketSize -= sizeof(TLandPacketElement))
	{
		TLandPacketElement kElement;
		if (!Recv(sizeof(TLandPacketElement), &kElement))
			return false;

		rkMiniMap.RegisterGuildArea(kElement.dwID,
			kElement.dwGuildID,
			kElement.x,
			kElement.y,
			kElement.width,
			kElement.height);

		if (pMainInstance)
			if (kElement.dwGuildID == pMainInstance->GetGuildID())
			{
				rkBG.RegisterGuildArea(kElement.x,
					kElement.y,
					kElement.x + kElement.width,
					kElement.y + kElement.height);
			}

		if (0 != kElement.dwGuildID)
			kVec_dwGuildID.push_back(kElement.dwGuildID);
	}
	// @fixme006
	if (kVec_dwGuildID.size() > 0)
		__DownloadSymbol(kVec_dwGuildID);

	return true;
}

bool CPythonNetworkStream::RecvTargetCreatePacket()
{
	TPacketGCTargetCreate kTargetCreate;
	if (!Recv(sizeof(kTargetCreate), &kTargetCreate))
		return false;

	CPythonMiniMap& rkpyMiniMap = CPythonMiniMap::Instance();
	rkpyMiniMap.CreateTarget(kTargetCreate.lID, kTargetCreate.szTargetName);

	//#ifdef _DEBUG
	//	char szBuf[256+1];
	//	CPythonChat::Instance().AppendChat(CHAT_TYPE_NOTICE, szBuf);
	//	Tracef(" >> RecvTargetCreatePacket %d : %s\n", kTargetCreate.lID, kTargetCreate.szTargetName);
	//#endif

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_OpenAtlasWindow", Py_BuildValue("()"));
	return true;
}

bool CPythonNetworkStream::RecvTargetCreatePacketNew()
{
	TPacketGCTargetCreateNew kTargetCreate;
	if (!Recv(sizeof(kTargetCreate), &kTargetCreate))
		return false;

	CPythonMiniMap& rkpyMiniMap = CPythonMiniMap::Instance();
	CPythonBackground& rkpyBG = CPythonBackground::Instance();
	if (CREATE_TARGET_TYPE_LOCATION == kTargetCreate.byType)
	{
		rkpyMiniMap.CreateTarget(kTargetCreate.lID, kTargetCreate.szTargetName);
	}
	else
	{
		rkpyMiniMap.CreateTarget(kTargetCreate.lID, kTargetCreate.szTargetName, kTargetCreate.dwVID);
		rkpyBG.CreateTargetEffect(kTargetCreate.lID, kTargetCreate.dwVID);
	}

	//#ifdef _DEBUG
	//	char szBuf[256+1];
	//	CPythonChat::Instance().AppendChat(CHAT_TYPE_NOTICE, szBuf);
	//	Tracef(" >> RecvTargetCreatePacketNew %d : %d/%d\n", kTargetCreate.lID, kTargetCreate.byType, kTargetCreate.dwVID);
	//#endif

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_OpenAtlasWindow", Py_BuildValue("()"));
	return true;
}

bool CPythonNetworkStream::RecvTargetUpdatePacket()
{
	TPacketGCTargetUpdate kTargetUpdate;
	if (!Recv(sizeof(kTargetUpdate), &kTargetUpdate))
		return false;

	CPythonMiniMap& rkpyMiniMap = CPythonMiniMap::Instance();
	rkpyMiniMap.UpdateTarget(kTargetUpdate.lID, kTargetUpdate.lX, kTargetUpdate.lY);

	CPythonBackground& rkpyBG = CPythonBackground::Instance();
	rkpyBG.CreateTargetEffect(kTargetUpdate.lID, kTargetUpdate.lX, kTargetUpdate.lY);

	//#ifdef _DEBUG
	//	char szBuf[256+1];
	//	CPythonChat::Instance().AppendChat(CHAT_TYPE_NOTICE, szBuf);
	//	Tracef(" >> RecvTargetUpdatePacket %d : %d, %d\n", kTargetUpdate.lID, kTargetUpdate.lX, kTargetUpdate.lY);
	//#endif

	return true;
}

bool CPythonNetworkStream::RecvTargetDeletePacket()
{
	TPacketGCTargetDelete kTargetDelete;
	if (!Recv(sizeof(kTargetDelete), &kTargetDelete))
		return false;

	CPythonMiniMap& rkpyMiniMap = CPythonMiniMap::Instance();
	rkpyMiniMap.DeleteTarget(kTargetDelete.lID);

	CPythonBackground& rkpyBG = CPythonBackground::Instance();
	rkpyBG.DeleteTargetEffect(kTargetDelete.lID);

	//#ifdef _DEBUG
	//	Tracef(" >> RecvTargetDeletePacket %d\n", kTargetDelete.lID);
	//#endif

	return true;
}

bool CPythonNetworkStream::RecvLoverInfoPacket()
{
	TPacketGCLoverInfo kLoverInfo;
	if (!Recv(sizeof(kLoverInfo), &kLoverInfo))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_LoverInfo", Py_BuildValue("(si)", kLoverInfo.szName, kLoverInfo.byLovePoint));
#ifdef _DEBUG
	Tracef("RECV LOVER INFO : %s, %d\n", kLoverInfo.szName, kLoverInfo.byLovePoint);
#endif
	return true;
}

bool CPythonNetworkStream::RecvLovePointUpdatePacket()
{
	TPacketGCLovePointUpdate kLovePointUpdate;
	if (!Recv(sizeof(kLovePointUpdate), &kLovePointUpdate))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_UpdateLovePoint", Py_BuildValue("(i)", kLovePointUpdate.byLovePoint));
#ifdef _DEBUG
	Tracef("RECV LOVE POINT UPDATE : %d\n", kLovePointUpdate.byLovePoint);
#endif
	return true;
}

bool CPythonNetworkStream::RecvDigMotionPacket()
{
	TPacketGCDigMotion kDigMotion;
	if (!Recv(sizeof(kDigMotion), &kDigMotion))
		return false;

#ifdef _DEBUG
	Tracef(" Dig Motion [%d/%d]\n", kDigMotion.vid, kDigMotion.count);
#endif

	IAbstractCharacterManager& rkChrMgr = IAbstractCharacterManager::GetSingleton();
	CInstanceBase* pkInstMain = rkChrMgr.GetInstancePtr(kDigMotion.vid);
	CInstanceBase* pkInstTarget = rkChrMgr.GetInstancePtr(kDigMotion.target_vid);

	if (pkInstMain == nullptr || pkInstTarget == nullptr) // lightwork correction if not target or miner exists, does not receives dig packet
		return true;

	if (pkInstTarget)
		pkInstMain->NEW_LookAtDestInstance(*pkInstTarget);

#ifndef ENABLE_MINING_RENEWAL
	for (int i = 0; i < kDigMotion.count; ++i)
#endif
	pkInstMain->PushOnceMotion(CRaceMotionData::NAME_DIG);

	return true;
}

bool CPythonNetworkStream::SendDragonSoulRefinePacket(BYTE bRefineType, TItemPos* pos)
{
	TPacketCGDragonSoulRefine pk;
	pk.header = HEADER_CG_DRAGON_SOUL_REFINE;
	pk.bSubType = bRefineType;
	memcpy(pk.ItemGrid, pos, sizeof(TItemPos) * DS_REFINE_WINDOW_MAX_NUM);
	if (!Send(sizeof(pk), &pk))
	{
		return false;
	}
	return true;
}

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
bool CPythonNetworkStream::RecvAccePacket(bool bReturn)
{
	TPacketAcce sPacket;
	if (!Recv(sizeof(sPacket), &sPacket))
		return bReturn;

	bReturn = true;
	switch (sPacket.subheader)
	{
	case ACCE_SUBHEADER_GC_OPEN:
		CPythonAcce::Instance().Clear();
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAcce", Py_BuildValue("(ib)", 1, sPacket.bWindow));
		break;

	case ACCE_SUBHEADER_GC_CLOSE:
		CPythonAcce::Instance().Clear();
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAcce", Py_BuildValue("(ib)", 2, sPacket.bWindow));
		break;

	case ACCE_SUBHEADER_GC_ADDED:
		CPythonAcce::Instance().AddMaterial(sPacket.dwPrice, sPacket.bPos, sPacket.tPos);
		if (sPacket.bPos == 1)
		{
			CPythonAcce::Instance().AddResult(sPacket.dwItemVnum, sPacket.dwMinAbs, sPacket.dwMaxAbs);
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "AlertAcce", Py_BuildValue("(b)", sPacket.bWindow));
		}

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAcce", Py_BuildValue("(ib)", 3, sPacket.bWindow));
		break;

	case ACCE_SUBHEADER_GC_REMOVED:
		CPythonAcce::Instance().RemoveMaterial(sPacket.dwPrice, sPacket.bPos);
		if (sPacket.bPos == 0)
			CPythonAcce::Instance().RemoveMaterial(sPacket.dwPrice, 1);

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAcce", Py_BuildValue("(ib)", 4, sPacket.bWindow));
		break;

	case ACCE_SUBHEADER_CG_REFINED:
		if (sPacket.dwMaxAbs == 0)
			CPythonAcce::Instance().RemoveMaterial(sPacket.dwPrice, 1);
		else
		{
			CPythonAcce::Instance().RemoveMaterial(sPacket.dwPrice, 0);
			CPythonAcce::Instance().RemoveMaterial(sPacket.dwPrice, 1);
		}

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAcce", Py_BuildValue("(ib)", 4, sPacket.bWindow));
		break;

	default:
		TraceError("CPythonNetworkStream::RecvAccePacket: unknown subheader %d\n.", sPacket.subheader);
		break;
	}

	return bReturn;
}

bool CPythonNetworkStream::SendAcceClosePacket()
{
	if (!__CanActMainInstance())
		return true;

	TItemPos tPos;
	tPos.window_type = INVENTORY;
	tPos.cell = 0;

	TPacketAcce sPacket;
	sPacket.header = HEADER_CG_ACCE;
	sPacket.subheader = ACCE_SUBHEADER_CG_CLOSE;
	sPacket.dwPrice = 0;
	sPacket.bPos = 0;
	sPacket.tPos = tPos;
	sPacket.dwItemVnum = 0;
	sPacket.dwMinAbs = 0;
	sPacket.dwMaxAbs = 0;

	if (!Send(sizeof(sPacket), &sPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendAcceAddPacket(TItemPos tPos, BYTE bPos)
{
	if (!__CanActMainInstance())
		return true;

	TPacketAcce sPacket;
	sPacket.header = HEADER_CG_ACCE;
	sPacket.subheader = ACCE_SUBHEADER_CG_ADD;
	sPacket.dwPrice = 0;
	sPacket.bPos = bPos;
	sPacket.tPos = tPos;
	sPacket.dwItemVnum = 0;
	sPacket.dwMinAbs = 0;
	sPacket.dwMaxAbs = 0;

	if (!Send(sizeof(sPacket), &sPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendAcceRemovePacket(BYTE bPos)
{
	if (!__CanActMainInstance())
		return true;

	TItemPos tPos;
	tPos.window_type = INVENTORY;
	tPos.cell = 0;

	TPacketAcce sPacket;
	sPacket.header = HEADER_CG_ACCE;
	sPacket.subheader = ACCE_SUBHEADER_CG_REMOVE;
	sPacket.dwPrice = 0;
	sPacket.bPos = bPos;
	sPacket.tPos = tPos;
	sPacket.dwItemVnum = 0;
	sPacket.dwMinAbs = 0;
	sPacket.dwMaxAbs = 0;

	if (!Send(sizeof(sPacket), &sPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendAcceRefinePacket()
{
	if (!__CanActMainInstance())
		return true;

	TItemPos tPos;
	tPos.window_type = INVENTORY;
	tPos.cell = 0;

	TPacketAcce sPacket;
	sPacket.header = HEADER_CG_ACCE;
	sPacket.subheader = ACCE_SUBHEADER_CG_REFINE;
	sPacket.dwPrice = 0;
	sPacket.bPos = 0;
	sPacket.tPos = tPos;
	sPacket.dwItemVnum = 0;
	sPacket.dwMinAbs = 0;
	sPacket.dwMaxAbs = 0;

	if (!Send(sizeof(sPacket), &sPacket))
		return false;

	return SendSequence();
}
#endif

#ifdef ENABLE_CUBE_RENEWAL_WORLDARD
bool CPythonNetworkStream::CubeRenewalMakeItem(int index_item, int count_item)
{
	if (!__CanActMainInstance())
		return true;

	TPacketCGCubeRenewalSend	packet;

	packet.header = HEADER_CG_CUBE_RENEWAL;
	packet.subheader = CUBE_RENEWAL_SUB_HEADER_MAKE_ITEM;
	packet.index_item = index_item;
	packet.count_item = count_item;

	if (!Send(sizeof(TPacketCGCubeRenewalSend), &packet))
	{
		Tracef("CPythonNetworkStream::CubeRenewalMakeItem Error\n");
		return false;
	}

	return true;
}

bool CPythonNetworkStream::CubeRenewalClose()
{
	if (!__CanActMainInstance())
		return true;

	TPacketCGCubeRenewalSend	packet;

	packet.header = HEADER_CG_CUBE_RENEWAL;
	packet.subheader = CUBE_RENEWAL_SUB_HEADER_CLOSE;

	if (!Send(sizeof(TPacketCGCubeRenewalSend), &packet))
	{
		Tracef("CPythonNetworkStream::CubeRenewalClose Error\n");
		return false;
	}

	return true;
}

bool CPythonNetworkStream::RecvCubeRenewalPacket()
{
	TPacketGCCubeRenewalReceive CubeRenewalPacket;

	if (!Recv(sizeof(CubeRenewalPacket), &CubeRenewalPacket))
		return false;

	switch (CubeRenewalPacket.subheader)
	{
	case CUBE_RENEWAL_SUB_HEADER_OPEN_RECEIVE:
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_CUBE_RENEWAL_OPEN", Py_BuildValue("()"));
	}
	break;

	case CUBE_RENEWAL_SUB_HEADER_DATES_RECEIVE:
	{
		CPythonCubeRenewal::Instance().ReceiveList(CubeRenewalPacket.date_cube_renewal);
	}
	break;

	case CUBE_RENEWAL_SUB_HEADER_DATES_LOADING:
	{
		CPythonCubeRenewal::Instance().LoadingList();
	}
	break;

	case CUBE_RENEWAL_SUB_HEADER_CLEAR_DATES_RECEIVE:
	{
		CPythonCubeRenewal::Instance().ClearList();
	}
	break;
	}

	return true;
}

#endif

#if defined(ENABLE_DISCORD_RPC)
#include "discord_rpc.h"
#ifdef _DEBUG
#pragma comment(lib, "discord_rpc_d.lib")
#else
#pragma comment(lib, "discord_rpc_r.lib")
#endif
static int64_t StartTime;
void CPythonNetworkStream::Discord_Start()
{
	auto DiscordClientID = CLIENT_ID;

	StartTime = time(0);
	DiscordEventHandlers handlers;
	memset(&handlers, 0, sizeof(handlers));
	Discord_Initialize(DiscordClientID, &handlers, 1, nullptr);
	Discord_Update(false);
}

void CPythonNetworkStream::Discord_Close()
{
	Discord_Shutdown();
}

void CPythonNetworkStream::Discord_Update(int PHASE_STATE)
{
	DiscordRichPresence discordPresence;
	memset(&discordPresence, 0, sizeof(discordPresence));
	discordPresence.startTimestamp = StartTime;

	std::string state(IMAGE_OVER_IN);
	std::string details = "State";

	const auto pInstance = CPythonCharacterManager::Instance().GetMainInstancePtr();

	switch (PHASE_STATE)
	{
		case DISCORD_NOSTATE:
		{
			state = "Waiting to login...";
			break;
		}

		case DISCORD_LOGIN:
		{
			state = "Logging in...";
			break;
		}

		case DISCORD_SELECTPHASE:
		{
			state = "Selecting character...";
			break;
		}

		case DISCORD_LOADINGPHASE:
		{
			state = "Loading phase...";
			break;
		}

		case DISCORD_GAMEPHASE:
		{
			if (!pInstance) {
				break;
			}
			/*
			const BYTE bLanguage = pInstance->GetLanguage();

			std::string langName = "en";

			if (bLanguage == 1)
				langName = "en";
			else if (bLanguage == 2)
				langName = "pt";
			else if (bLanguage == 3)
				langName = "es";
			else if (bLanguage == 4)
				langName = "fr";
			else if (bLanguage == 5)
				langName = "de";
			else if (bLanguage == 6)
				langName = "ro";
			else if (bLanguage == 7)
				langName = "pl";
			else if (bLanguage == 8)
				langName = "it";
			else if (bLanguage == 9)
				langName = "cz";
			else if (bLanguage == 10)
				langName = "hu";
			else if (bLanguage == 11)
				langName = "tr";
			else
				langName = "eu"; // en
				*/
			const auto pLevel = pInstance->GetLevel();
	#ifdef ENABLE_CONQUEROR_LEVEL
			const auto pConquerorLevel pInstance->GetConquerorLevel();
	#endif

	#ifdef ENABLE_CONQUEROR_LEVEL
			details = std::string(CPythonPlayer::Instance().GetName()) + " | " + (pConquerorLevel ? "Conqu. Lv." + std::to_string(pConquerorLevel) : "Lv. " + std::to_string(pLevel));
	#else
			details = std::string(CPythonPlayer::Instance().GetName()) + " | " + "Lv." + std::to_string(pLevel);
	#endif

			state = WEB_URL;
			break;
		}
	}

	discordPresence.state = state.c_str();
	discordPresence.details = details.c_str();

	discordPresence.largeImageKey = IMAGE_NAME;
	discordPresence.largeImageText = IMAGE_OVER_IN;

	discordPresence.buttonLabel = BUTTON_NAME;
	discordPresence.buttonURL = DISCORD_URL;

	Discord_UpdatePresence(&discordPresence);
}
#endif

#ifdef ENABLE_SWITCHBOT
bool CPythonNetworkStream::RecvSwitchbotPacket()
{
	TPacketGCSwitchbot pack;
	if (!Recv(sizeof(pack), &pack))
	{
		return false;
	}

	size_t packet_size = int32_t(pack.size) - sizeof(TPacketGCSwitchbot);
	if (pack.subheader == SUBHEADER_GC_SWITCHBOT_UPDATE)
	{
		if (packet_size != sizeof(CPythonSwitchbot::TSwitchbotTable))
		{
			return false;
		}

		CPythonSwitchbot::TSwitchbotTable table;
		if (!Recv(sizeof(table), &table))
		{
			return false;
		}

		CPythonSwitchbot::Instance().Update(table);
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshSwitchbotWindow", Py_BuildValue("()"));
	}
	else if (pack.subheader == SUBHEADER_GC_SWITCHBOT_UPDATE_ITEM)
	{
		if (packet_size != sizeof(TSwitchbotUpdateItem))
		{
			return false;
		}

		TSwitchbotUpdateItem update;
		if (!Recv(sizeof(update), &update))
		{
			return false;
		}
		TItemPos pos(SWITCHBOT, update.slot);

		IAbstractPlayer& rkPlayer = IAbstractPlayer::GetSingleton();
		rkPlayer.SetItemCount(pos, update.count);

		for (int32_t i = 0; i < ITEM_SOCKET_SLOT_MAX_NUM; ++i)
		{
			rkPlayer.SetItemMetinSocket(pos, i, update.alSockets[i]);
		}

		for (int32_t j = 0; j < ITEM_ATTRIBUTE_SLOT_MAX_NUM; ++j)
		{
			rkPlayer.SetItemAttribute(pos, j, update.aAttr[j].bType, update.aAttr[j].sValue);
		}

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshSwitchbotItem", Py_BuildValue("(i)", update.slot));
		return true;
	}
	else if (pack.subheader == SUBHEADER_GC_SWITCHBOT_SEND_ATTRIBUTE_INFORMATION)
	{
		CPythonSwitchbot::Instance().ClearAttributeMap();

		size_t table_size = sizeof(CPythonSwitchbot::TSwitchbottAttributeTable);
		while (packet_size >= table_size)
		{
			CPythonSwitchbot::TSwitchbottAttributeTable table;
			if (!Recv(table_size, &table))
			{
				return false;
			}

			CPythonSwitchbot::Instance().AddAttributeToMap(table);
			packet_size -= table_size;
		}
	}

	return true;
}
bool CPythonNetworkStream::SendSwitchbotStartPacket(uint8_t slot, std::vector<CPythonSwitchbot::TSwitchbotAttributeAlternativeTable> alternatives)
{
	TPacketCGSwitchbot pack;
	pack.header = HEADER_CG_SWITCHBOT;
	pack.subheader = SUBHEADER_CG_SWITCHBOT_START;
	pack.size = sizeof(TPacketCGSwitchbot) + sizeof(CPythonSwitchbot::TSwitchbotAttributeAlternativeTable) * SWITCHBOT_ALTERNATIVE_COUNT;
	pack.slot = slot;

	if (!Send(sizeof(pack), &pack))
	{
		return false;
	}

	for (const auto& it : alternatives)
	{
		if (!Send(sizeof(it), &it))
		{
			return false;
		}
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendSwitchbotStopPacket(uint8_t slot)
{
	TPacketCGSwitchbot pack;
	pack.header = HEADER_CG_SWITCHBOT;
	pack.subheader = SUBHEADER_CG_SWITCHBOT_STOP;
	pack.size = sizeof(TPacketCGSwitchbot);
	pack.slot = slot;

	if (!Send(sizeof(pack), &pack))
	{
		return false;
	}

	return SendSequence();
}
#endif

#ifdef ENABLE_REFRESH_CONTROL
bool CPythonNetworkStream::RecvRefreshControl()
{
	TPacketGCRefreshControl pack;
	if (!Recv(sizeof(TPacketGCRefreshControl), &pack))
		return false;

	m_RefreshControl[pack.SubHeader] = pack.state;

	if (pack.update == true)
	{
		switch (pack.SubHeader)
		{
			case REFRESH_INVENTORY:
			{
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshInventory", Py_BuildValue("()"));
				break;
			}
			case REFRESH_SKILL:
			{
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshSkill", Py_BuildValue("()"));
				break;
			}
			case REFRESH_POINT:
			{
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshStatus", Py_BuildValue("()"));
				break;
			}
			default: break;
		}
	}
	return true;
}
#endif

#ifdef ENABLE_GLOBAL_RANKING
bool CPythonNetworkStream::RecvGlobalRankingPacket()
{
	TRankingGCPacket packet;
	if (!Recv(sizeof(packet), &packet))
		return false;

	packet.wSize -= sizeof(TRankingGCPacket);
	if (((packet.wSize - sizeof(TRankingMeGC)) % sizeof(TRankingData)) != 0)
		return false;

	TRankingData packet2;
	if (!Recv(sizeof(packet2), &packet2))
		return false;

	packet.wSize -= sizeof(TRankingData);

	if ((packet.wSize % sizeof(TRankingMeGC)) != 0)
		return false;

	TRankingMeGC packet3;
	if (!Recv(sizeof(packet3), &packet3))
		return false;

	CStatisticsRanking& rank = CStatisticsRanking::Instance();
	rank.Destroy();
	rank.SetNextUpdateTime(packet.next_update_second);
	rank.WriteData(packet2, packet3);
	rank.OpenTheDoor();
	return true;
}
#endif

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
bool CPythonNetworkStream::SendChangeLanguagePacket(BYTE bLanguage)
{
	TPacketChangeLanguage packet;
	packet.bHeader = HEADER_CG_CHANGE_LANGUAGE;
	packet.bLanguage = bLanguage;

	if (!Send(sizeof(packet), &packet))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::RecvRequestChangeLanguage()
{
	TPacketChangeLanguage packet;
	if (!Recv(sizeof(packet), &packet))
		return false;

	CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();
	CInstanceBase* pkInstMain = rkChrMgr.GetMainInstancePtr();

	if (!pkInstMain)
	{
		TraceError("CPythonNetworkStream::RecvRequestChangeLanguage - MainCharacter is NULL");
		return false;
	}

	pkInstMain->SetLanguage(packet.bLanguage);
	pkInstMain->Update();

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_RequestChangeLanguage", Py_BuildValue("(i)", packet.bLanguage));

	return true;
}
#endif

#ifdef ENABLE_EXTENDED_WHISPER_DETAILS
bool CPythonNetworkStream::SendWhisperDetails(const char* name)
{
	TPacketCGWhisperDetails packet;
	packet.header = HEADER_CG_WHISPER_DETAILS;
	strncpy(packet.name, name, sizeof(packet.name) - 1);
	if (!Send(sizeof(packet), &packet))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::RecvWhisperDetails()
{
	TPacketGCWhisperDetails packet;
	if (!Recv(sizeof(packet), &packet))
		return false;

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_RecieveWhisperDetails", Py_BuildValue("(si)", packet.name, packet.bLanguage));
#else
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_RecieveWhisperDetails", Py_BuildValue("(s)", packet.name));
#endif

	return true;
}
#endif


#ifdef ENABLE_CHAR_SETTINGS
bool CPythonNetworkStream::RecvCharSettings()
{
	TPacketGCCharSettings packet;
	if (!Recv(sizeof(packet), &packet))
	{
		TraceError("Char Settings Recovery Error");
		return false;
	}

	CPythonPlayer::Instance().SetCharSettings(packet.data);
	if (packet.type != 31)
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshCharSettings", Py_BuildValue("(i)", packet.type));
	}
	else
	{
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "SetCharSettings", Py_BuildValue("()"));
	}
	return true;
}
#endif

#ifdef ENABLE_BIOLOG_SYSTEM
bool CPythonNetworkStream::RecvBiologPacket()
{
	TPacketGCBiolog packet;
	if (!Recv(sizeof(packet), &packet))
	{
		TraceError("Biolog Packet Recovery Error");
		return false;
	}

	BiologSystem& bio = BiologSystem::Instance();
	switch (packet.sub_header)
	{
		case SUBHEADER_GC_BIOLOG_LEVEL_UPDATE:
		case SUBHEADER_GC_BIOLOG_OPEN:
		{
			TPacketGCBiologInformations bioinfo;
			if (!Recv(sizeof(bioinfo), &bioinfo))
			{
				TraceError("Biolog Sub Packet %d Recvery Error bioinfo", packet.sub_header);
				return false;
			}

			TPacketGCBiologUpdate biostate;
			if (!Recv(sizeof(biostate), &biostate))
			{
				TraceError("Biolog Sub Packet %d Recvery Error biostate", packet.sub_header);
				return false;
			}

			bio.LoadBiologInformations(&bioinfo);
			bio.LoadBiologState(&biostate);

			if (packet.sub_header == SUBHEADER_GC_BIOLOG_OPEN)
			{
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BIOLOG_OpenWindow", Py_BuildValue("()"));
			}
			else
			{
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BIOLOG_UpdateLevel", Py_BuildValue("()"));
			}
			break;
		}
		case SUBHEADER_GC_BIOLOG_COUNT_UPDATE:
		{
			TPacketGCBiologUpdate biostate;
			if (!Recv(sizeof(biostate), &biostate))
			{
				TraceError("Biolog Sub Packet %d Recvery Error", packet.sub_header);
				return false;
			}
			bio.LoadBiologState(&biostate);
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BIOLOG_UpdateCount", Py_BuildValue("()"));
			break;
		}
		case SUBHEADER_GC_BIOLOG_MAX_LEVEL:
		{
			bio.SetMaxLevel(true);
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BIOLOG_MAX_LEVEL", Py_BuildValue("()"));
			break;
		}
		default:
			break;
	}

	return true;
}
#endif

#ifdef ENABLE_PM_ALL_SEND_SYSTEM
bool CPythonNetworkStream::SendBulkWhisperPacket(const char* c_szContent)
{
	if (strlen(c_szContent) == 0)
		return true;

	if (strlen(c_szContent) >= 512)
		return true;

	int iTextLen = strlen(c_szContent) + 1;
	TPacketCGBulkWhisper WhisperPacket;
	WhisperPacket.header = HEADER_CG_BULK_WHISPER;
	strncpy(WhisperPacket.szText, c_szContent, sizeof(WhisperPacket.szText) - 1);

	if (!Send(sizeof(WhisperPacket), &WhisperPacket))
		return false;

	return true;
}
bool CPythonNetworkStream::RecvBulkWhisperPacket()
{
	TPacketGCBulkWhisper kWhisper;
	char buf[1024 + 1];

	if (!Recv(sizeof(kWhisper), &kWhisper))
		return false;

	UINT uWhisperSize = kWhisper.size - sizeof(kWhisper);

	if (!Recv(uWhisperSize, buf))
		return false;

	buf[uWhisperSize] = '\0';

	TraceError("CPythonNetworkStream::RecvBulkWhisperPacket - %s", buf);

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_OnRecvBulkWhisper", Py_BuildValue("(s)", buf));
	return true;
}
#endif


#ifdef ENABLE_EVENT_MANAGER
bool CPythonNetworkStream::RecvEventManager()
{
	TPacketGCEventManager p;
	if (!Recv(sizeof(TPacketGCEventManager), &p))
		return false;

	BYTE subIndex;
	if (!Recv(sizeof(BYTE), &subIndex))
		return false;

	if (subIndex == EVENT_MANAGER_LOAD)
	{
		BYTE dayCount;
		if (!Recv(sizeof(BYTE), &dayCount))
			return false;
	
		int serverTime;
		if (!Recv(sizeof(int), &serverTime))
			return false;
	
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ClearEventManager", Py_BuildValue("()"));

		for (BYTE j{}; j < dayCount; ++j)
		{
			BYTE dayIndex;
			if (!Recv(sizeof(BYTE), &dayIndex))
				return false;
	
			BYTE dayEventCount;
			if (!Recv(sizeof(BYTE), &dayEventCount))
				return false;
	
			if (dayEventCount > 0)
			{
				std::vector<TEventManagerData> m_vec;
				m_vec.resize(dayEventCount);
	
				if (!Recv(dayEventCount * sizeof(TEventManagerData), &m_vec[0]))
					return false;
		
				for (const auto& eventPtr : m_vec)
					PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "AppendEvent", Py_BuildValue("(iiissiiiiiiiii)", dayIndex, eventPtr.eventID, eventPtr.eventIndex, eventPtr.startTimeText, eventPtr.endTimeText, eventPtr.empireFlag, eventPtr.channelFlag, eventPtr.value[0], eventPtr.value[1], eventPtr.value[2], eventPtr.value[3], eventPtr.startTime - serverTime, eventPtr.endTime == 0 ? 0 : eventPtr.endTime - serverTime, eventPtr.eventStatus));
			}
		}
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshEventManager", Py_BuildValue("()"));
	}
	else if (subIndex == EVENT_MANAGER_EVENT_STATUS)
	{
		WORD eventID;
		if (!Recv(sizeof(WORD), &eventID))
			return false;

		bool eventStatus;
		if (!Recv(sizeof(bool), &eventStatus))
			return false;

		int endTime;
		if (!Recv(sizeof(int), &endTime))
			return false;

		char endTimeText[25];
		if (!Recv(sizeof(endTimeText), &endTimeText))
			return false;

		int serverTime;
		if (!Recv(sizeof(int), &serverTime))
			return false;

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshEventStatus", Py_BuildValue("(iiis)", eventID, eventStatus, endTime == 0 ? 0 : endTime - serverTime, endTimeText));
	}
	return true;
}
#endif


#ifdef ENABLE_ITEMSHOP
bool CPythonNetworkStream::RecvItemShop()
{
	TPacketGCItemShop p;
	if (!Recv(sizeof(TPacketGCItemShop), &p))
		return false;
	
	BYTE subIndex;
	if (!Recv(sizeof(BYTE), &subIndex))
		return false;

	switch (subIndex)
	{
		case ITEMSHOP_DRAGONCOIN:
		{
			long long dragonCoin;
			if (!Recv(sizeof(long long), &dragonCoin))
				return false;
			bool isLogOpen;
			if (!Recv(sizeof(bool), &isLogOpen))
				return false;

			if (isLogOpen)
			{
				TIShopLogData logData;
				if (!Recv(sizeof(TIShopLogData), &logData))
					return false;
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopAppendLog", Py_BuildValue("(sissiiL)", logData.buyDate, logData.buyTime, logData.playerName, logData.ipAdress, logData.itemVnum, logData.itemCount, logData.itemPrice));
			}

			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopSetDragonCoin", Py_BuildValue("(L)", dragonCoin));
		}
		break;
		
		case ITEMSHOP_LOG:
		{
			int logCount;
			if (!Recv(sizeof(int), &logCount))
				return false;
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopHideLoading", Py_BuildValue("()"));
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopLogClear", Py_BuildValue("()"));
			if (logCount)
			{
				std::vector<TIShopLogData> m_vec;
				m_vec.resize(logCount);
				if (!Recv(sizeof(TIShopLogData)*logCount, &m_vec[0]))
					return false;
				for (DWORD j = 0; j < m_vec.size(); ++j)
					PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopAppendLog", Py_BuildValue("(sissiiL)", m_vec[j].buyDate, m_vec[j].buyTime, m_vec[j].playerName, m_vec[j].ipAdress, m_vec[j].itemVnum, m_vec[j].itemCount, m_vec[j].itemPrice));
			}
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopPurchasesWindow", Py_BuildValue("()"));
		}
		break;
		
		case ITEMSHOP_UPDATE_ITEM:
		{
			TIShopData updateItem;
			if (!Recv(sizeof(TIShopData), &updateItem))
				return false;
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopUpdateItem", Py_BuildValue("(iiLiiiiLiL)",
				updateItem.id, updateItem.itemVnum, updateItem.itemPrice, updateItem.discount, updateItem.offerTime, updateItem.topSellingIndex, updateItem.addedTime,
				updateItem.sellCount, updateItem.maxSellCount, updateItem.itemUntradeablePrice));
		}
		break;
		
		case ITEMSHOP_LOAD:
		{
			
			long long dragonCoin;
			if (!Recv(sizeof(long long), &dragonCoin))
				return false;
			int updateTime;
			if (!Recv(sizeof(int), &updateTime))
				return false;
				
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopSetDragonCoin", Py_BuildValue("(L)", dragonCoin));
			
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopHideLoading", Py_BuildValue("()"));
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopClear", Py_BuildValue("(i)", updateTime));
			
			int categoryTotalSize;
			if (!Recv(sizeof(int), &categoryTotalSize))
				return false;

			if (categoryTotalSize == 9999)
			{
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopOpenMainPage", Py_BuildValue("()"));
				return true;
			}


			for (DWORD j = 0; j < categoryTotalSize; ++j)
			{
				BYTE categoryIndex, categorySize;
				if (!Recv(sizeof(BYTE), &categoryIndex))
					return false;
				if (!Recv(sizeof(BYTE), &categorySize))
					return false;
				for (DWORD x = 0; x < categorySize; ++x)
				{
					BYTE categorySubIndex, categorySubSize=0;
					if (!Recv(sizeof(BYTE), &categorySubIndex))
						return false;
					if (!Recv(sizeof(BYTE), &categorySubSize))
						return false;

					
					if (categorySubSize)
					{
						for (DWORD k = 0; k < categorySubSize; ++k)
						{
							TIShopData shopData;
							if (!Recv(sizeof(TIShopData),&shopData))
								return false;
							PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopAppendItem", Py_BuildValue("(iiiiLiiiiLiL)",
								categoryIndex, categorySubIndex,  shopData.id, shopData.itemVnum, shopData.itemPrice, shopData.discount, shopData.offerTime, shopData.topSellingIndex, shopData.addedTime,
								shopData.sellCount, shopData.maxSellCount, shopData.itemUntradeablePrice));
						}

						/*
						std::vector<TIShopData> m_vec;
						m_vec.resize(categorySubSize);
					
						if (!Recv(sizeof(TIShopData) * categorySubSize, m_vec.data()))
							return false;
						
						for (DWORD k = 0; k < m_vec.size(); ++k)
						{
							const TIShopData& shopData = m_vec[k];
							PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopAppendItem", Py_BuildValue("(iiiiLiiiiL)",
								categoryIndex, categorySubIndex,  shopData.id, shopData.itemVnum, shopData.itemPrice, shopData.discount, shopData.offerTime, shopData.topSellingIndex, shopData.addedTime,
								shopData.sellCount));
						}
						*/
					}

	
				}
				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ItemShopOpenMainPage", Py_BuildValue("()"));
			}
			
		}
		break;
	}

	return true;
}
#endif


#ifdef ENABLE_TELEPORT_TO_A_FRIEND
bool CPythonNetworkStream::SendMessengerRequestWarpByNamePacket(const char* c_szName)
{
	TPacketCGMessenger packet;
	packet.header = HEADER_CG_MESSENGER;
	packet.subheader = MESSENGER_SUBHEADER_CG_REQUEST_WARP_BY_NAME;

	if (!Send(sizeof(packet), &packet))
	{
		return false;
	}

	char szName[CHARACTER_NAME_MAX_LEN];
	strncpy(szName, c_szName, CHARACTER_NAME_MAX_LEN - 1);
	szName[CHARACTER_NAME_MAX_LEN - 1] = '\0';

	if (!Send(sizeof(szName), &szName))
	{
		return false;
	}

	return true;
}

bool CPythonNetworkStream::SendMessengerSummonByNamePacket(const char* c_szName)
{
	TPacketCGMessenger packet;
	packet.header = HEADER_CG_MESSENGER;
	packet.subheader = MESSENGER_SUBHEADER_CG_SUMMON_BY_NAME;

	if (!Send(sizeof(packet), &packet))
	{
		return false;
	}

	char szName[CHARACTER_NAME_MAX_LEN];
	strncpy(szName, c_szName, CHARACTER_NAME_MAX_LEN - 1);
	szName[CHARACTER_NAME_MAX_LEN - 1] = '\0';

	if (!Send(sizeof(szName), &szName))
	{
		return false;
	}

	return true;
}
#endif

#ifdef ENABLE_AURA_SYSTEM
bool CPythonNetworkStream::RecvAuraPacket(bool bReturn)
{
	TPacketAura sPacket;
	if (!Recv(sizeof(sPacket), &sPacket))
		return bReturn;

	bReturn = true;
	switch (sPacket.subheader)
	{
	case AURA_SUBHEADER_GC_OPEN:
	{
		CPythonAura::Instance().Clear();
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAura", Py_BuildValue("(ib)", 1, sPacket.bWindow));
	}
	break;
	case AURA_SUBHEADER_GC_CLOSE:
	{
		CPythonAura::Instance().Clear();
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAura", Py_BuildValue("(ib)", 2, sPacket.bWindow));
	}
	break;
	case AURA_SUBHEADER_GC_ADDED:
	{
		CPythonAura::Instance().AddMaterial(sPacket.dwPrice, sPacket.bPos, sPacket.tPos);
		if (sPacket.bPos == 1)
		{
			CPythonAura::Instance().AddResult(sPacket.dwItemVnum, sPacket.dwMinAbs, sPacket.dwMaxAbs);
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "AlertAura", Py_BuildValue("(b)", sPacket.bWindow));
		}

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAura", Py_BuildValue("(ib)", 3, sPacket.bWindow));
	}
	break;
	case AURA_SUBHEADER_GC_REMOVED:
	{
		CPythonAura::Instance().RemoveMaterial(sPacket.dwPrice, sPacket.bPos);
		if (sPacket.bPos == 0)
			CPythonAura::Instance().RemoveMaterial(sPacket.dwPrice, 1);

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAura", Py_BuildValue("(ib)", 4, sPacket.bWindow));
	}
	break;
	case AURA_SUBHEADER_GC_REFINED:
	{
		if (sPacket.bPos != 255)
		{
			if (sPacket.dwMaxAbs == 0)
				CPythonAura::Instance().RemoveMaterial(sPacket.dwPrice, 1);
			else
			{
				CPythonAura::Instance().RemoveMaterial(sPacket.dwPrice, 0);
				CPythonAura::Instance().RemoveMaterial(sPacket.dwPrice, 1);
			}
		}

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "ActAura", Py_BuildValue("(ib)", 4, sPacket.bWindow));
	}
	break;
	default:
		TraceError("CPythonNetworkStream::RecvAuraPacket: unknown subheader %d\n.", sPacket.subheader);
		break;
	}

	return bReturn;
}

bool CPythonNetworkStream::SendAuraClosePacket()
{
	if (!__CanActMainInstance())
		return true;

	TItemPos tPos;
	tPos.window_type = INVENTORY;
	tPos.cell = 0;

	TPacketAura sPacket;
	sPacket.header = HEADER_CG_AURA;
	sPacket.subheader = AURA_SUBHEADER_CG_CLOSE;
	sPacket.dwPrice = 0;
	sPacket.bPos = 0;
	sPacket.tPos = tPos;
	sPacket.dwItemVnum = 0;
	sPacket.dwMinAbs = 0;
	sPacket.dwMaxAbs = 0;
	if (!Send(sizeof(sPacket), &sPacket))
		return false;

	return true;
}

bool CPythonNetworkStream::SendAuraAddPacket(TItemPos tPos, BYTE bPos)
{
	if (!__CanActMainInstance())
		return true;

	TPacketAura sPacket;
	sPacket.header = HEADER_CG_AURA;
	sPacket.subheader = AURA_SUBHEADER_CG_ADD;
	sPacket.dwPrice = 0;
	sPacket.bPos = bPos;
	sPacket.tPos = tPos;
	sPacket.dwItemVnum = 0;
	sPacket.dwMinAbs = 0;
	sPacket.dwMaxAbs = 0;
	if (!Send(sizeof(sPacket), &sPacket))
		return false;

	return true;
}

bool CPythonNetworkStream::SendAuraRemovePacket(BYTE bPos)
{
	if (!__CanActMainInstance())
		return true;

	TItemPos tPos;
	tPos.window_type = INVENTORY;
	tPos.cell = 0;

	TPacketAura sPacket;
	sPacket.header = HEADER_CG_AURA;
	sPacket.subheader = AURA_SUBHEADER_CG_REMOVE;
	sPacket.dwPrice = 0;
	sPacket.bPos = bPos;
	sPacket.tPos = tPos;
	sPacket.dwItemVnum = 0;
	sPacket.dwMinAbs = 0;
	sPacket.dwMaxAbs = 0;
	if (!Send(sizeof(sPacket), &sPacket))
		return false;

	return true;
}

bool CPythonNetworkStream::SendAuraRefinePacket()
{
	if (!__CanActMainInstance())
		return true;

	TItemPos tPos;
	tPos.window_type = INVENTORY;
	tPos.cell = 0;

	TPacketAura sPacket;
	sPacket.header = HEADER_CG_AURA;
	sPacket.subheader = AURA_SUBHEADER_CG_REFINE;
	sPacket.dwPrice = 0;
	sPacket.bPos = 0;
	sPacket.tPos = tPos;
	sPacket.dwItemVnum = 0;
	sPacket.dwMinAbs = 0;
	sPacket.dwMaxAbs = 0;
	if (!Send(sizeof(sPacket), &sPacket))
		return false;

	return true;
}
#endif

#ifdef ENABLE_EXTENDED_BATTLE_PASS
bool CPythonNetworkStream::SendExtBattlePassAction(BYTE bAction)
{
	if (!__CanActMainInstance())
		return true;

	TPacketCGExtBattlePassAction packet;
	packet.bHeader = HEADER_CG_EXT_BATTLE_PASS_ACTION;
	packet.bAction = bAction;

	if (!Send(sizeof(TPacketCGExtBattlePassAction), &packet))
	{
		Tracef("SendExtBattlePassAction Send Packet Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendExtBattlePassPremium(bool premium)
{
	if (!__CanActMainInstance())
		return true;

	TPacketCGExtBattlePassSendPremium packet;
	packet.bHeader = HEADER_CG_EXT_SEND_BP_PREMIUM;
	packet.premium = premium;

	if (!Send(sizeof(TPacketCGExtBattlePassSendPremium), &packet))
	{
		Tracef("SendExtBattlePassPremium Send Packet Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::RecvExtBattlePassOpenPacket()
{
	SPacketGCExtBattlePassOpen packet;
	if (!Recv(sizeof(packet), &packet))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ExtOpenBattlePass", Py_BuildValue("()"));

	return true;
}

bool CPythonNetworkStream::RecvExtBattlePassGeneralInfoPacket()
{
	TPacketGCExtBattlePassGeneralInfo packet;
	if (!Recv(sizeof(packet), &packet))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ExtBattlePassAddGeneralInfo", Py_BuildValue("(isiii)", packet.bBattlePassType, packet.szSeasonName, packet.dwBattlePassID, packet.dwBattlePassStartTime, packet.dwBattlePassEndTime));

	return true;
}

bool CPythonNetworkStream::RecvExtBattlePassMissionInfoPacket()
{
	TPacketGCExtBattlePassMissionInfo packet;
	if (!Recv(sizeof(packet), &packet))
		return false;

	packet.wSize -= sizeof(packet);

	while (packet.wSize > 0)
	{
		TExtBattlePassMissionInfo missionInfo;
		if (!Recv(sizeof(missionInfo), &missionInfo))
			return false;

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ExtBattlePassAddMission", Py_BuildValue("(iiiiiii)",
			packet.bBattlePassType, packet.dwBattlePassID, missionInfo.bMissionIndex, missionInfo.bMissionType, missionInfo.dwMissionInfo[0], missionInfo.dwMissionInfo[1], missionInfo.dwMissionInfo[2]));

		for (int i = 0; i < 3; ++i)
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ExtBattlePassAddMissionReward", Py_BuildValue("(iiiiii)",
				packet.bBattlePassType, packet.dwBattlePassID, missionInfo.bMissionIndex, missionInfo.bMissionType, missionInfo.aRewardList[i].dwVnum, missionInfo.aRewardList[i].bCount));

		packet.wSize -= sizeof(missionInfo);
	}

	while (packet.wRewardSize > 0)
	{
		TExtBattlePassRewardItem rewardInfo;
		if (!Recv(sizeof(rewardInfo), &rewardInfo))
			return false;

		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ExtBattlePassAddReward", Py_BuildValue("(iiii)", packet.bBattlePassType, packet.dwBattlePassID, rewardInfo.dwVnum, rewardInfo.bCount));

		packet.wRewardSize -= sizeof(rewardInfo);
	}
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ExtOpenBattlePass", Py_BuildValue("()"));

	return true;
}

bool CPythonNetworkStream::RecvExtBattlePassMissionUpdatePacket()
{
	TPacketGCExtBattlePassMissionUpdate packet;
	if (!Recv(sizeof(packet), &packet))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ExtBattlePassUpdate", Py_BuildValue("(iiii)", packet.bBattlePassType, packet.bMissionIndex, packet.bMissionType, packet.dwNewProgress));

	return true;
}

bool CPythonNetworkStream::RecvExtBattlePassRankingPacket()
{
	TPacketGCExtBattlePassRanking packet;
	if (!Recv(sizeof(packet), &packet))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ExtBattlePassAddRanklistEntry", Py_BuildValue("(siiii)",
		packet.szPlayerName, packet.bBattlePassType, packet.bBattlePassID, packet.dwStartTime, packet.dwEndTime
	));

	return true;
}
#endif

#ifdef ENABLE_LEADERSHIP_EXTENSION
bool CPythonNetworkStream::SendRequestPartyBonus(BYTE bBonusID)
{
	if (!__CanActMainInstance())
		return true;
	
	TPacketCGRequestPartyBonus packet;
	packet.bHeader = HEADER_CG_REQUEST_PARTY_BONUS;
	packet.bBonusID = bBonusID;

	if (!Send(sizeof(TPacketCGRequestPartyBonus), &packet))
	{
		Tracen("SendRequestPartyBonus Error");
		return false;
	}

	return true;
}
#endif

#ifdef ENABLE_6TH_7TH_ATTR
bool CPythonNetworkStream::Send67AttrPacket(int iMaterialCount, int iSupportCount, int iSupportPos, int iItemPos)
{
	TPacketCG67Attr p =
	{
		static_cast<BYTE>(HEADER_CG_67_ATTR),
		static_cast<BYTE>(iMaterialCount),
		static_cast<BYTE>(iSupportCount),
		static_cast<short>(iSupportPos),
		static_cast<short>(iItemPos),
	};

	if (!Send(sizeof(p), &p))
	{
		Tracef("Send67AttrPacket Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::Send67AttrClosePacket()
{
	TPacket67AttrOpenClose p;
	p.bHeader = HEADER_CG_CLOSE_67_ATTR;

	if (!Send(sizeof(p), &p))
	{
		Tracef("Send67AttrClosePacket Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::Recv67AttrOpenPacket()
{
	TPacket67AttrOpenClose p;

	if (!Recv(sizeof(p), &p))
		return false;

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OpenAttr67AddDlg", Py_BuildValue("()"));

	return true;
}
#endif

#ifdef ENABLE_NEW_CHAT
bool CPythonNetworkStream::RecvNewChatPacket()
{
	TPacketNewChat p;

	if (!Recv(sizeof(p), &p))
		return false;

	CNewChatManager& chatmgr = CNewChatManager::Instance();
	std::string localeString = "";

	if (p.size != sizeof(TPacketNewChat))
	{
		if (!chatmgr.FindLocaleString(p.chatID, localeString))
		{
			CPythonNetworkStream& rns = CPythonNetworkStream::Instance();
			rns.ClearRecvBuffer();
			return false;
		}

		char buf[512];
		WORD chatSize = p.size - sizeof(TPacketNewChat);

		if (!Recv(chatSize, buf))
			return false;

		buf[chatSize] = '\0';

		chatmgr.WriteFormat(localeString, buf);
		localeString += '\0';
	}
	else
	{
		if (!chatmgr.FindLocaleString(p.chatID, localeString))
			return false;
	}

	if (!localeString.empty())
	{
#ifdef ENABLE_ZODIAC_TEMPLE_CHAT
		if (CHAT_TYPE_ZODIAC_NOTICE == p.chatType)
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_SetMissionMessage", Py_BuildValue("(s)", localeString.c_str()));
		}
#endif
		else if (CHAT_TYPE_NOTICE == p.chatType)
		{
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_SetTipMessage", Py_BuildValue("(s)", localeString.c_str()));
		}
		else
		{
			BYTE bActualType = p.chatType;
#ifdef ENABLE_DROP_INFO_WINDOW
			if (chatmgr.IsItemGainChatID(p.chatID))
			{
				bActualType = CHAT_TYPE_ITEM_INFO;
			}
#endif
			CPythonChat::Instance().AppendChat(bActualType, localeString.c_str());
		}
	}


	return true;
}
#endif

#ifdef ENABLE_BUFFI_SYSTEM
bool CPythonNetworkStream::RecvBuffiSkillPacket()
{
	TPGCBuffiSkill packet;
	if (!Recv(sizeof(TPGCBuffiSkill), &packet))
	{
		TraceError("Buffi Skill Packet Error");
		return false;
	}

	CInstanceBase* buffiInst = CPythonCharacterManager::Instance().GetInstancePtr(packet.vid);
	if (buffiInst)
	{
		DWORD skillIdx = packet.skillVnum;
		CPythonSkill::TSkillData* skillData;

		if (!CPythonSkill::Instance().GetSkillData(skillIdx, &skillData))
			return false;

		DWORD motIdx = skillData->GetSkillMotionIndex(4);

		if (!buffiInst->NEW_UseSkill(skillIdx, motIdx, 1, false))
			TraceError("Buffi skill dalgayi yedi %d", skillIdx);
	}
	else
	{
		TraceError("Buffi VID Error");
	}
	return true;
}
#endif

#ifdef ENABLE_MINI_GAME_OKEY_NORMAL
bool CPythonNetworkStream::SendMiniGameRumiStart(int safemode)
{
	TPacketCGMiniGameOkeyCard kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameOkeyCard) + sizeof(TSubPacketCGMiniGameCardOpenClose);
	kMiniGamePacket.bSubHeader = SUBHEADER_CG_RUMI_START;

	TSubPacketCGMiniGameCardOpenClose kMiniGameSubPacket;
	kMiniGameSubPacket.bSafeMode = safemode;

	if (!Send(sizeof(TPacketCGMiniGameOkeyCard), &kMiniGamePacket))
		return false;

	if (!Send(sizeof(TSubPacketCGMiniGameCardOpenClose), &kMiniGameSubPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendMiniGameRumiExit()
{
	TPacketCGMiniGameOkeyCard kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameOkeyCard);
	kMiniGamePacket.bSubHeader = SUBHEADER_CG_RUMI_EXIT;

	if (!Send(sizeof(TPacketCGMiniGameOkeyCard), &kMiniGamePacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendMiniGameRumiDeckCardClick()
{
	TPacketCGMiniGameOkeyCard kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameOkeyCard);
	kMiniGamePacket.bSubHeader = SUBHEADER_CG_RUMI_DECKCARD_CLICK;

	if (!Send(sizeof(TPacketCGMiniGameOkeyCard), &kMiniGamePacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendMiniGameRumiHandCardClick(int index)
{
	TPacketCGMiniGameOkeyCard kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameOkeyCard) + sizeof(TSubPacketCGMiniGameHandCardClick);
	kMiniGamePacket.bSubHeader = SUBHEADER_CG_RUMI_HANDCARD_CLICK;

	TSubPacketCGMiniGameHandCardClick kMiniGameSubPacket;
	kMiniGameSubPacket.index = index;

	if (!Send(sizeof(TPacketCGMiniGameOkeyCard), &kMiniGamePacket))
		return false;

	if (!Send(sizeof(TSubPacketCGMiniGameHandCardClick), &kMiniGameSubPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendMiniGameRumiFieldCardClick(int index)
{
	TPacketCGMiniGameOkeyCard kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameOkeyCard) + sizeof(TSubPacketCGMiniGameFieldCardClick);
	kMiniGamePacket.bSubHeader = SUBHEADER_CG_RUMI_FIELDCARD_CLICK;

	TSubPacketCGMiniGameFieldCardClick kMiniGameSubPacket;
	kMiniGameSubPacket.index = index;

	if (!Send(sizeof(TPacketCGMiniGameOkeyCard), &kMiniGamePacket))
		return false;

	if (!Send(sizeof(TSubPacketCGMiniGameFieldCardClick), &kMiniGameSubPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendMiniGameRumiDestroy(int index)
{
	TPacketCGMiniGameOkeyCard kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameOkeyCard) + sizeof(TSubPacketCGMiniGameDestroy);
	kMiniGamePacket.bSubHeader = SUBHEADER_CG_RUMI_DESTROY;

	TSubPacketCGMiniGameDestroy kMiniGameSubPacket;
	kMiniGameSubPacket.index = index;

	if (!Send(sizeof(TPacketCGMiniGameOkeyCard), &kMiniGamePacket))
		return false;

	if (!Send(sizeof(TSubPacketCGMiniGameDestroy), &kMiniGameSubPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::RecvMiniGameOkeyCardPacket()
{
	TPacketGCMiniGameOkeyCard kMiniGamePacket;
	if (!Recv(sizeof(TPacketGCMiniGameOkeyCard), &kMiniGamePacket))
	{
		Tracef("MiniGame Packet Error SubHeader %u\n", kMiniGamePacket.bSubHeader);
		return false;
	}

	int iPacketSize = int(kMiniGamePacket.wSize) - sizeof(TPacketGCMiniGameOkeyCard);

	switch (kMiniGamePacket.bSubHeader)
	{
		case SUBHEADER_GC_RUMI_OPEN:
		{
			if (iPacketSize > 0)
			{
				TSubPacketGCMiniGameCardOpenClose kSubPacket;
				assert(iPacketSize % sizeof(TSubPacketGCMiniGameCardOpenClose) == 0 && "MINI_GAME_RUMI_OPENCLOSE");
				if (!Recv(sizeof(TSubPacketGCMiniGameCardOpenClose), &kSubPacket))
					return false;

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MiniGameStart", Py_BuildValue("(i)", kSubPacket.bSafeMode));
			}
			else
				TraceError(" RecvMiniGamePacket Error 0x04100%u0F", kMiniGamePacket.bSubHeader);

			break;
		}

		case SUBHEADER_GC_RUMI_CARD_UPDATE:
		{
			if (iPacketSize > 0)
			{
				TSubPacketGCMiniGameCardsInfo kSubPacket;
				assert(iPacketSize % sizeof(TSubPacketGCMiniGameCardsInfo) == 0 && "MINI_GAME_RUMI_CARD_UPDATE");
				if (!Recv(sizeof(TSubPacketGCMiniGameCardsInfo), &kSubPacket))
					return false;

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_Cards_UpdateInfo", Py_BuildValue("(iiiiiiiiiiii)",
					kSubPacket.cardHandType[0], kSubPacket.cardHandValue[0], kSubPacket.cardHandType[1], kSubPacket.cardHandValue[1], kSubPacket.cardHandType[2], kSubPacket.cardHandValue[2], kSubPacket.cardHandType[3], kSubPacket.cardHandValue[3], kSubPacket.cardHandType[4], kSubPacket.cardHandValue[4], kSubPacket.cardHandLeft, kSubPacket.cHandPoint));

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_Cards_FieldUpdateInfo", Py_BuildValue("(iiiiiii)", kSubPacket.cardFieldType[0], kSubPacket.cardFieldValue[0], kSubPacket.cardFieldType[1], kSubPacket.cardFieldValue[1], kSubPacket.cardFieldType[2], kSubPacket.cardFieldValue[2], kSubPacket.cFieldPoint));
			}
			else
				TraceError(" RecvMiniGamePacket Error 0x040%uBABE", kMiniGamePacket.bSubHeader);
			break;
		}

		case SUBHEADER_GC_RUMI_CARD_REWARD:
		{
			if (iPacketSize > 0)
			{
				TSubPacketGCMiniGameCardsReward kSubPacket;
				assert(iPacketSize % sizeof(TSubPacketGCMiniGameCardsReward) == 0 && "MINI_GAME_RUMI_CARD_REWARD");
				if (!Recv(sizeof(TSubPacketGCMiniGameCardsReward), &kSubPacket))
					return false;

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_Cards_PutReward", Py_BuildValue("(iiiiiii)", kSubPacket.cardType[0], kSubPacket.cardValue[0], kSubPacket.cardType[1], kSubPacket.cardValue[1], kSubPacket.cardType[2], kSubPacket.cardValue[2], kSubPacket.cPoint));
			}
			else
				TraceError(" RecvMiniGamePacket Error 0x040%uBEBA", kMiniGamePacket.bSubHeader);
			break;
		}
	}

	return true;
}
#endif

#ifdef ENABLE_MINI_GAME_BNW
bool CPythonNetworkStream::SendMinigameBnwStart()
{
	TPacketCGMinigameBnw packet;
	packet.header = HEADER_CG_MINIGAME_BNW;
	packet.subheader = MINIGAME_BNW_SUBHEADER_CG_START;

	if (!Send(sizeof(packet), &packet))
	{
		Tracen("SendMinigameBnwStart Error");
		return false;
	}
	return SendSequence();
}

bool CPythonNetworkStream::SendMinigameBnwCardSelected(BYTE bCard)
{
	TPacketCGMinigameBnw packet;
	packet.header = HEADER_CG_MINIGAME_BNW;
	packet.subheader = MINIGAME_BNW_SUBHEADER_CG_SELECTED_CARD;

	if (!Send(sizeof(packet), &packet))
	{
		Tracen("SendMinigameBnwCardSelected Error");
		return false;
	}

	if (!Send(sizeof(BYTE), &bCard))
	{
		Tracen("SendMinigameBnwCardSelected Error2");
		return false;
	}

	Tracenf("SendMinigameBnwCardSelected");
	return SendSequence();
}

bool CPythonNetworkStream::SendMinigameBnwFinished()
{
	TPacketCGMinigameBnw packet;
	packet.header = HEADER_CG_MINIGAME_BNW;
	packet.subheader = MINIGAME_BNW_SUBHEADER_CG_FINISHED;

	if (!Send(sizeof(packet), &packet))
	{
		Tracen("SendMinigameBnwFinished Error");
		return false;
	}
	return SendSequence();
}

bool CPythonNetworkStream::RecvMinigameBnw()
{
	TPacketCGMinigameBnw p;
	if (!Recv(sizeof(p), &p))
		return false;

	switch (p.subheader)
	{
		case MINIGAME_BNW_SUBHEADER_GC_START:
		{
			Tracef("RecvMinigameBnw MINIGAME_BNW_SUBHEADER_GC_START\n");
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_MinigameBnwStart", Py_BuildValue("()"));
			break;
		}
		case MINIGAME_BNW_SUBHEADER_GC_DRAW_RESULT:
		{
			Tracef("RecvMinigameBnw MINIGAME_BNW_SUBHEADER_GC_DRAW_RESULT\n");
			TPacketGCMinigameBnwDrawResult result;
			if (!Recv(sizeof(TPacketGCMinigameBnwDrawResult), &result))
				return false;
			PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_MinigameBnwDrawResult", Py_BuildValue("(iii)", result.result, result.playerPoints, result.enemyPoints));
			break;
		}
	}
	return true;
}

#endif

#ifdef ENABLE_MINI_GAME_CATCH_KING
bool CPythonNetworkStream::SendMiniGameCatchKingStart(int ibetNumber)
{
	TPacketCGMiniGameCatchKing kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameCatchKing) + sizeof(TSubPacketCGMiniGameCatchKingStart);
	kMiniGamePacket.bSubheader = SUBHEADER_CG_CATCH_KING_START;

	TSubPacketCGMiniGameCatchKingStart kMiniGameSubPacket;
	kMiniGameSubPacket.betNumber = ibetNumber;

	if (!Send(sizeof(TPacketCGMiniGameCatchKing), &kMiniGamePacket))
		return false;

	if (!Send(sizeof(TSubPacketCGMiniGameCatchKingStart), &kMiniGameSubPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendMiniGameCatchKingDeckCardClick()
{
	TPacketCGMiniGameCatchKing kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameCatchKing);
	kMiniGamePacket.bSubheader = SUBHEADER_CG_CATCH_KING_DECKCARD_CLICK;

	if (!Send(sizeof(TPacketCGMiniGameCatchKing), &kMiniGamePacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendMiniGameCatchKingFieldCardClick(int icardNumber)
{
	TPacketCGMiniGameCatchKing kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameCatchKing) + sizeof(TSubPacketCGMiniGameCatchKingFieldCardClick);
	kMiniGamePacket.bSubheader = SUBHEADER_CG_CATCH_KING_FIELDCARD_CLICK;

	TSubPacketCGMiniGameCatchKingFieldCardClick kMiniGameSubPacket;
	kMiniGameSubPacket.cardNumber = icardNumber;

	if (!Send(sizeof(TPacketCGMiniGameCatchKing), &kMiniGamePacket))
		return false;

	if (!Send(sizeof(TSubPacketCGMiniGameCatchKingFieldCardClick), &kMiniGameSubPacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendMiniGameCatchKingReward()
{
	TPacketCGMiniGameCatchKing kMiniGamePacket;
	kMiniGamePacket.wSize = sizeof(TPacketCGMiniGameCatchKing);
	kMiniGamePacket.bSubheader = SUBHEADER_CG_CATCH_KING_REWARD;

	if (!Send(sizeof(TPacketCGMiniGameCatchKing), &kMiniGamePacket))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::RecvMiniGameCatchKingPacket()
{
	TPacketGCMiniGameCatchKing kMiniGamePacket;
	if (!Recv(sizeof(TPacketGCMiniGameCatchKing), &kMiniGamePacket))
	{
		Tracef("MiniGame Packet Error SubHeader %u\n", kMiniGamePacket.bSubheader);
		return false;
	}

	int iPacketSize = int(kMiniGamePacket.wSize) - sizeof(TPacketGCMiniGameCatchKing);

	switch (kMiniGamePacket.bSubheader)
	{
		case SUBHEADER_GC_CATCH_KING_EVENT_INFO:
		{
			if (iPacketSize > 0)
			{
				TSubPacketGCCatchKingEventInfo kSubPacket;
				assert(iPacketSize % sizeof(TSubPacketGCCatchKingEventInfo) == 0 && "MINI_GAME_RUMI_CARD_REWARD");
				if (!Recv(sizeof(TSubPacketGCCatchKingEventInfo), &kSubPacket))
					return false;

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MiniGameCatchKingEvent", Py_BuildValue("(b)", kSubPacket.bIsEnable));
			}
			else
				TraceError(" RecvMiniGamePacket Error 0x040%uBEBC1", kMiniGamePacket.bSubheader);
			break;
		}

		case SUBHEADER_GC_CATCH_KING_START:
		{
			if (iPacketSize > 0)
			{
				TSubPacketGCCatchKingStart kSubPacket;
				assert(iPacketSize % sizeof(TSubPacketGCCatchKingStart) == 0 && "MINI_GAME_RUMI_CARD_REWARD");
				if (!Recv(sizeof(TSubPacketGCCatchKingStart), &kSubPacket))
					return false;

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MiniGameCatchKingEventStart", Py_BuildValue("(i)", kSubPacket.dwBigScore));
			}
			else
				TraceError(" RecvMiniGamePacket Error 0x040%uBEBC2", kMiniGamePacket.bSubheader);
			break;
		}

		case SUBHEADER_GC_CATCH_KING_SET_CARD:
		{
			if (iPacketSize > 0)
			{
				TSubPacketGCCatchKingSetCard kSubPacket;
				assert(iPacketSize % sizeof(TSubPacketGCCatchKingSetCard) == 0 && "MINI_GAME_RUMI_CARD_REWARD");
				if (!Recv(sizeof(TSubPacketGCCatchKingSetCard), &kSubPacket))
					return false;

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MiniGameCatchKingSetHandCard", Py_BuildValue("(i)", kSubPacket.bCardInHand));
			}
			else
				TraceError(" RecvMiniGamePacket Error 0x040%uBEBC3", kMiniGamePacket.bSubheader);
			break;
		}

		case SUBHEADER_GC_CATCH_KING_RESULT_FIELD:
		{
			if (iPacketSize > 0)
			{
				TSubPacketGCCatchKingResult kSubPacket;
				assert(iPacketSize % sizeof(TSubPacketGCCatchKingResult) == 0 && "MINI_GAME_RUMI_CARD_REWARD");
				if (!Recv(sizeof(TSubPacketGCCatchKingResult), &kSubPacket))
					return false;

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MiniGameCatchKingResultField", Py_BuildValue("(iiiibbbb)",
					kSubPacket.dwPoints, kSubPacket.bRowType, kSubPacket.bCardPos, kSubPacket.bCardValue,
					kSubPacket.bKeepFieldCard, kSubPacket.bDestroyHandCard, kSubPacket.bGetReward, kSubPacket.bIsFiveNearBy));
			}
			else
				TraceError(" RecvMiniGamePacket Error 0x040%uBEBC4", kMiniGamePacket.bSubheader);
			break;
		}

		case SUBHEADER_GC_CATCH_KING_SET_END_CARD:
		{
			if (iPacketSize > 0)
			{
				TSubPacketGCCatchKingSetEndCard kSubPacket;
				assert(iPacketSize % sizeof(TSubPacketGCCatchKingSetEndCard) == 0 && "MINI_GAME_RUMI_CARD_REWARD");
				if (!Recv(sizeof(TSubPacketGCCatchKingSetEndCard), &kSubPacket))
					return false;

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MiniGameCatchKingSetEndCard", Py_BuildValue("(ii)", kSubPacket.bCardPos, kSubPacket.bCardValue));
			}
			else
				TraceError(" RecvMiniGamePacket Error 0x040%uBEBC5", kMiniGamePacket.bSubheader);
			break;
		}

		case SUBHEADER_GC_CATCH_KING_REWARD:
		{
			if (iPacketSize > 0)
			{
				TSubPacketGCCatchKingReward kSubPacket;
				assert(iPacketSize % sizeof(TSubPacketGCCatchKingReward) == 0 && "MINI_GAME_RUMI_CARD_REWARD");
				if (!Recv(sizeof(TSubPacketGCCatchKingReward), &kSubPacket))
					return false;

				PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MiniGameCatchKingReward", Py_BuildValue("(i)", kSubPacket.bReturnCode));
			}
			else
				TraceError(" RecvMiniGamePacket Error 0x040%uBEBC6", kMiniGamePacket.bSubheader);
			break;
		}
	}

	return true;
}
#endif