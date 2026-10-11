#pragma once
#include "../eterLib/FuncObject.h"
#include "../eterlib/NetStream.h"
#include "../eterLib/NetPacketHeaderMap.h"
#include "InsultChecker.h"
#include "packet.h"
#ifdef ENABLE_SWITCHBOT
#include "PythonSwitchbot.h"
#endif

class CInstanceBase;
class CNetworkActorManager;
struct SNetworkActorData;
struct SNetworkUpdateActorData;

class CPythonNetworkStream : public CNetworkStream, public CSingleton<CPythonNetworkStream>
{
public:
	enum
	{
		SERVER_COMMAND_LOG_OUT = 0,
		SERVER_COMMAND_RETURN_TO_SELECT_CHARACTER = 1,
		SERVER_COMMAND_QUIT = 2,

		MAX_ACCOUNT_PLAYER
	};

	enum
	{
		ERROR_NONE,
		ERROR_UNKNOWN,
		ERROR_CONNECT_MARK_SERVER,
		ERROR_LOAD_MARK,
		ERROR_MARK_WIDTH,
		ERROR_MARK_HEIGHT,

		// MARK_BUG_FIX
		ERROR_MARK_UPLOAD_NEED_RECONNECT,
		ERROR_MARK_CHECK_NEED_RECONNECT,
		// END_OF_MARK_BUG_FIX
	};

	enum
	{
		ACCOUNT_CHARACTER_SLOT_ID,
		ACCOUNT_CHARACTER_SLOT_NAME,
		ACCOUNT_CHARACTER_SLOT_RACE,
		ACCOUNT_CHARACTER_SLOT_LEVEL,
		ACCOUNT_CHARACTER_SLOT_STR,
		ACCOUNT_CHARACTER_SLOT_DEX,
		ACCOUNT_CHARACTER_SLOT_HTH,
		ACCOUNT_CHARACTER_SLOT_INT,
		ACCOUNT_CHARACTER_SLOT_PLAYTIME,
		ACCOUNT_CHARACTER_SLOT_FORM,
		ACCOUNT_CHARACTER_SLOT_ADDR,
		ACCOUNT_CHARACTER_SLOT_PORT,
		ACCOUNT_CHARACTER_SLOT_GUILD_ID,
		ACCOUNT_CHARACTER_SLOT_GUILD_NAME,
		ACCOUNT_CHARACTER_SLOT_CHANGE_NAME_FLAG,
		ACCOUNT_CHARACTER_SLOT_HAIR,
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
		ACCOUNT_CHARACTER_SLOT_ACCE,
#endif
#ifdef ENABLE_OFFICAL_CHARACTER_SCREEN
		ACCOUNT_CHARACTER_SLOT_LAST_PLAYTIME,
#endif
	};

	enum GamePhases: BYTE
	{
		GAME_PHASE_OFFLINE,
		GAME_PHASE_LOGIN,
		GAME_PHASE_HANDSHAKE,
		GAME_PHASE_SELECT,
		GAME_PHASE_EMPIRE_SELECT,
		GAME_PHASE_CREATE,
		GAME_PHASE_LOADING,
		GAME_PHASE_GAME,
		GAME_MAX_PHASE_NUM
	};

	enum
	{
		PHASE_WINDOW_LOGIN,
		PHASE_WINDOW_SELECT,
		PHASE_WINDOW_CREATE,
		PHASE_WINDOW_LOAD,
		PHASE_WINDOW_GAME,
		PHASE_WINDOW_EMPIRE,
		PHASE_WINDOW_NUM,
	};

#if defined(ENABLE_DISCORD_RPC)
	enum DiscordStates { DISCORD_NOSTATE, DISCORD_LOGIN, DISCORD_SELECTPHASE, DISCORD_LOADINGPHASE, DISCORD_GAMEPHASE, };
#endif

public:
	CPythonNetworkStream();
	virtual ~CPythonNetworkStream();

	bool SendSpecial(int nLen, void* pvBuf);

	void StartGame();
	void Warp(LONG lGlobalX, LONG lGlobalY);

	void NotifyHack(const char* c_szMsg);
	void SetWaitFlag();
#if defined(ENABLE_DISCORD_RPC)
	void Discord_Start();
	void Discord_Close();
	void Discord_Update(int PHASE_STATE);
#endif
	void SendEmoticon(UINT eEmoticon);

	void ExitApplication();
	void ExitGame();
	void LogOutGame();
	void AbsoluteExitGame();
	void AbsoluteExitApplication();

	void EnableChatInsultFilter(bool isEnable);
	bool IsChatInsultIn(const char* c_szMsg);
	bool IsInsultIn(const char* c_szMsg);

	DWORD GetGuildID();

	UINT UploadMark(const char* c_szImageFileName);
	UINT UploadSymbol(const char* c_szImageFileName);

	bool LoadInsultList(const char* c_szInsultListFileName);
	bool LoadConvertTable(DWORD dwEmpireID, const char* c_szFileName);

	UINT		GetAccountCharacterSlotDatau(UINT iSlot, UINT eType);
	const char* GetAccountCharacterSlotDataz(UINT iSlot, UINT eType);

	bool IsSelectedEmpire();

	void ToggleGameDebugInfo();

	void SetMarkServer(const char* c_szAddr, UINT uPort);
	void ConnectLoginServer(const char* c_szAddr, UINT uPort);
	void ConnectGameServer(UINT iChrSlot);

	void SetLoginInfo(const char* c_szID, const char* c_szPassword);
#ifdef ENABLE_OFFICAL_CHARACTER_SCREEN
	std::string GetLoginID() const { return m_stID; }
#endif
	void SetLoginKey(DWORD dwLoginKey);
	void ClearLoginInfo(void);

	void SetHandler(PyObject* poHandler);
	void SetPhaseWindow(UINT ePhaseWnd, PyObject* poPhaseWnd);
	void ClearPhaseWindow(UINT ePhaseWnd, PyObject* poPhaseWnd);
	void SetServerCommandParserWindow(PyObject* poPhaseWnd);

	bool SendSyncPositionElementPacket(DWORD dwVictimVID, DWORD dwVictimX, DWORD dwVictimY);

	bool SendAttackPacket(UINT uMotAttack, DWORD dwVIDVictim);
	bool SendCharacterStatePacket(const TPixelPosition& c_rkPPosDst, float fDstRot, UINT eFunc, UINT uArg);
	bool SendUseSkillPacket(DWORD dwSkillIndex, DWORD dwTargetVID = 0);
	bool SendTargetPacket(DWORD dwVID);
#ifdef ENABLE_SKILL_COLOR_SYSTEM
		bool SendSkillColorPacket(BYTE skill, DWORD col1, DWORD col2, DWORD col3, DWORD col4, DWORD col5);
#endif

	// OLDCODE:
	bool SendCharacterStartWalkingPacket(float fRotation, long lx, long ly);
	bool SendCharacterEndWalkingPacket(float fRotation, long lx, long ly);
	bool SendCharacterCheckWalkingPacket(float fRotation, long lx, long ly);

	bool SendCharacterPositionPacket(BYTE iPosition);

	bool SendItemUsePacket(TItemPos pos
#ifdef ENABLE_CHEST_OPEN_RENEWAL
		, MAX_COUNT item_open_count = 0
#endif
	);
	bool SendItemUseToItemPacket(TItemPos source_pos, TItemPos target_pos);
#ifdef ENABLE_DROP_DIALOG_EXTENDED_SYSTEM
	bool SendItemDeletePacket(TItemPos item_pos);
	bool SendItemSellPacket(TItemPos item_pos);
#else
	bool SendItemDropPacket(TItemPos pos, DWORD elk);
	bool SendItemDropPacketNew(TItemPos pos, DWORD elk, DWORD count);
#endif
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	bool SendItemMovePacket(TItemPos pos, TItemPos change_pos, MAX_COUNT num);
#else
	bool SendItemMovePacket(TItemPos pos, TItemPos change_pos, BYTE num);
#endif
	bool SendItemPickUpPacket(DWORD vid);

	bool SendQuickSlotAddPacket(BYTE wpos, BYTE type, BYTE pos);
	bool SendQuickSlotDelPacket(BYTE wpos);
	bool SendQuickSlotMovePacket(BYTE wpos, BYTE change_pos);

	bool SendPointResetPacket();

	// Shop
	bool SendShopEndPacket();
	bool SendShopBuyPacket(BYTE byCount);
#ifdef ENABLE_MULTIPLE_BUY_ITEMS
	bool SendShopBuyMultiplePacket(uint8_t p, uint8_t c);
#endif
	bool SendShopSellPacket(BYTE bySlot);
#ifdef ENABLE_SPECIAL_STORAGE
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	bool SendShopSellPacketNew(BYTE bySlot, MAX_COUNT byCount, BYTE byType);
#else
	bool SendShopSellPacketNew(BYTE bySlot, BYTE byCount, BYTE byType);
#endif
#else
	bool SendShopSellPacketNew(BYTE bySlot, BYTE byCount);
#endif
#ifdef ENABLE_LEADERSHIP_EXTENSION
	bool SendRequestPartyBonus(BYTE bBonusID);
#endif

	// Exchange
	bool SendExchangeStartPacket(DWORD vid);
#if defined(ENABLE_CHECKINOUT_UPDATE)
	bool SendExchangeItemAddPacket(TItemPos ItemPos, BYTE byDisplayPos, bool SelectPosAuto);
#else
	bool SendExchangeItemAddPacket(TItemPos ItemPos, BYTE byDisplayPos);
#endif
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	bool SendExchangeElkAddPacket(int64_t elk);
#else
	bool SendExchangeElkAddPacket(DWORD elk);
#endif
	bool SendExchangeItemDelPacket(BYTE pos);
	bool SendExchangeAcceptPacket();
	bool SendExchangeExitPacket();

	// Quest
	bool SendScriptAnswerPacket(int iAnswer);
	bool SendScriptButtonPacket(unsigned int iIndex);
	bool SendAnswerMakeGuildPacket(const char* c_szName);
	bool SendQuestInputStringPacket(const char* c_szString);
	bool SendQuestConfirmPacket(BYTE byAnswer, DWORD dwPID);

	// Event
	bool SendOnClickPacket(DWORD vid);
#ifdef ENABLE_MINI_GAME_OKEY_NORMAL
	bool SendMiniGameRumiStart(int safemode);
	bool SendMiniGameRumiExit();
	bool SendMiniGameRumiDeckCardClick();
	bool SendMiniGameRumiHandCardClick(int index);
	bool SendMiniGameRumiFieldCardClick(int index);
	bool SendMiniGameRumiDestroy(int index);
	bool RecvMiniGameOkeyCardPacket();
#endif
	// Fly
	bool SendFlyTargetingPacket(DWORD dwTargetVID, const TPixelPosition& kPPosTarget);
	bool SendAddFlyTargetingPacket(DWORD dwTargetVID, const TPixelPosition& kPPosTarget);
	bool SendShootPacket(UINT uSkill);

	// Command
	bool ClientCommand(const char* c_szCommand);
	void ServerCommand(char* c_szCommand);

	// Emoticon
	void RegisterEmoticonString(const char* pcEmoticonString);

	// Party
	bool SendPartyInvitePacket(DWORD dwVID);
	bool SendPartyInviteAnswerPacket(DWORD dwLeaderVID, BYTE byAccept);
	bool SendPartyRemovePacket(DWORD dwPID);
	bool SendPartySetStatePacket(DWORD dwVID, BYTE byState, BYTE byFlag);
	bool SendPartyUseSkillPacket(BYTE bySkillIndex, DWORD dwVID);
	bool SendPartyParameterPacket(BYTE byDistributeMode);

	// SafeBox
	bool SendSafeBoxMoneyPacket(BYTE byState, DWORD dwMoney);
	bool SendSafeBoxCheckinPacket(TItemPos InventoryPos, BYTE bySafeBoxPos);
	bool SendSafeBoxCheckoutPacket(BYTE bySafeBoxPos, TItemPos InventoryPos);
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	bool SendSafeBoxItemMovePacket(BYTE bySourcePos, BYTE byTargetPos, MAX_COUNT byCount);
#else
	bool SendSafeBoxItemMovePacket(BYTE bySourcePos, BYTE byTargetPos, BYTE byCount);
#endif

	// Mall
	bool SendMallCheckoutPacket(TItemPos InventoryPos);

	// Guild
	bool SendGuildAddMemberPacket(DWORD dwVID);
	bool SendGuildRemoveMemberPacket(DWORD dwPID);
	bool SendGuildChangeGradeNamePacket(BYTE byGradeNumber, const char* c_szName);
	bool SendGuildChangeGradeAuthorityPacket(BYTE byGradeNumber, BYTE byAuthority);
	bool SendGuildOfferPacket(DWORD dwExperience);
	bool SendGuildPostCommentPacket(const char* c_szMessage);
	bool SendGuildDeleteCommentPacket(DWORD dwIndex);
	bool SendGuildRefreshCommentsPacket(DWORD dwHighestIndex);
	bool SendGuildChangeMemberGradePacket(DWORD dwPID, BYTE byGrade);
	bool SendGuildUseSkillPacket(DWORD dwSkillID, DWORD dwTargetVID);
	bool SendGuildChangeMemberGeneralPacket(DWORD dwPID, BYTE byFlag);
	bool SendGuildInvitePacket(DWORD dwVID);
	bool SendGuildInviteAnswerPacket(DWORD dwGuildID, BYTE byAnswer);
	bool SendGuildChargeGSPPacket(DWORD dwMoney);
	bool SendGuildDepositMoneyPacket(DWORD dwMoney);
	bool SendGuildWithdrawMoneyPacket(DWORD dwMoney);
#ifdef ENABLE_OFFLINE_SHOP
	bool RecvOfflineshopPacket();
	bool RecvOfflineshopShopList();
	bool RecvOfflineshopShopOpen();
	bool RecvOfflineshopShopOpenOwner();
	bool RecvOfflineshopShopOpenOwnerNoShop();
	bool RecvOfflineshopShopClose();
	bool RecvOfflineshopShopFilterResult();
	bool RecvOfflineshopShopSafeboxRefresh();
	bool RecvOfflineshopShopBuyItemFromSearch();
#ifdef ENABLE_SHOP_IN_CITIES
	bool RecvOfflineshopInsertEntity();
	bool RecvOfflineshopRemoveEntity();
	void SendOfflineshopOnClickShopEntity(DWORD dwPickedShopVID);
#endif
#ifdef ENABLE_OFFLINESHOP_NOTIFICATION
	bool RecvOfflineshopNotification();
#endif
#ifdef ENABLE_AVERAGE_PRICE
	bool RecvOfflineshopAveragePrice();
#endif
	void SendOfflineshopShopCreate(const offlineshop::TShopInfo& shopInfo, const std::vector<offlineshop::TShopItemInfo>& items);
	void SendOfflineshopChangeName(const char* szName);
	void SendOfflineshopForceCloseShop();
	void SendOfflineshopRequestShopList();
	void SendOfflineshopOpenShop(DWORD dwOwnerID);
	void SendOfflineshopOpenShopOwner();
	void SendOfflineshopBuyItem(DWORD dwOwnerID, DWORD dwItemID, bool isSearch);
	void SendOfflineshopAddItem(offlineshop::TShopItemInfo& itemInfo);
	void SendOfflineshopRemoveItem(DWORD dwItemID);
	void SendOfflineShopEditItem(DWORD dwItemID, const offlineshop::TPriceInfo& price, bool allEdit);
	void SendOfflineshopFilterRequest(const offlineshop::TFilterInfo& filter);
	void SendOfflineshopSafeboxOpen();
	void SendOfflineshopSafeboxGetItem(DWORD dwItemID);
	void SendOfflineshopSafeboxGetValutes(const unsigned long long& valutes);
	void SendOfflineshopSafeboxClose();
	void SendOfflineshopCloseBoard();
#ifdef ENABLE_OFFLINESHOP_EXTEND_TIME
	void SendOfflineshopExtendTime(DWORD dwTime);
#endif
#ifdef ENABLE_AVERAGE_PRICE
	void SendOfflineShopAveragePrice(DWORD vnum);
#endif
#endif

	// Mall
	bool RecvMallOpenPacket();
	bool RecvMallItemSetPacket();
	bool RecvMallItemDelPacket();

	// Lover
	bool RecvLoverInfoPacket();
	bool RecvLovePointUpdatePacket();

	// Dig
	bool RecvDigMotionPacket();

	// Fishing
	bool SendFishingPacket(int iRotation);
	bool SendGiveItemPacket(DWORD dwTargetVID, TItemPos ItemPos, int iItemCount);

	// Private Shop
	bool SendBuildPrivateShopPacket(const char* c_szName, const std::vector<TShopItemTable>& c_rSellingItemStock);

	// Refine
	bool SendRefinePacket(BYTE byPos, BYTE byType);
	bool SendSelectItemPacket(DWORD dwItemPos);

	// CRC Report
	bool __SendCRCReportPacket();

	bool SendDragonSoulRefinePacket(BYTE bRefineType, TItemPos* pos);

	// Handshake
	bool RecvHandshakePacket();
	bool RecvHandshakeOKPacket();

#ifdef _IMPROVED_PACKET_ENCRYPTION_
	bool RecvKeyAgreementPacket();
	bool RecvKeyAgreementCompletedPacket();

#endif
	// ETC
	DWORD GetMainActorVID();
	DWORD GetMainActorRace();
	DWORD GetMainActorEmpire();
	DWORD GetMainActorSkillGroup();
	void SetEmpireID(DWORD dwEmpireID);
	DWORD GetEmpireID();
	void __TEST_SetSkillGroupFake(int iIndex);

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	bool	SendAcceClosePacket();
	bool	SendAcceAddPacket(TItemPos tPos, BYTE bPos);
	bool	SendAcceRemovePacket(BYTE bPos);
	bool	SendAcceRefinePacket();
#endif
#ifdef ENABLE_AURA_SYSTEM
	bool	SendAuraClosePacket();
	bool	SendAuraAddPacket(TItemPos tPos, BYTE bPos);
	bool	SendAuraRemovePacket(BYTE bPos);
	bool	SendAuraRefinePacket();
#endif
#ifdef ENABLE_CUBE_RENEWAL_WORLDARD
	bool	CubeRenewalMakeItem(int index_item, int count_item);
	bool	CubeRenewalClose();
	bool	RecvCubeRenewalPacket();
#endif

#ifdef ENABLE_EVENT_MANAGER
	bool RecvEventManager();
#endif

#ifdef ENABLE_ITEMSHOP
	bool RecvItemShop();
#endif

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	// Multi Language
	bool SendChangeLanguagePacket(BYTE bLanguage);
	bool SendChangeLanguage(const char* lang);

	void SetLanguage(BYTE bLanguage) { m_bLanguage = bLanguage; }
	int GetLanguage() const { return m_bLanguage; }
#ifdef ENABLE_EXTENDED_WHISPER_DETAILS
	bool SendWhisperDetails(const char* name);
#endif

protected:
	BYTE m_bLanguage;
#endif

	//////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////
public:
	void SetOffLinePhase();
	void SetHandShakePhase();
	void SetLoginPhase();
	void SetSelectPhase();
	void SetLoadingPhase();
	void SetGamePhase();
	void ClosePhase();

	// Login Phase
	bool SendLoginPacket(const char* c_szName, const char* c_szPassword);
	bool SendLoginPacketNew(const char* c_szName, const char* c_szPassword);
	bool SendEnterGame();
	bool SendSequence() { return true; }

	// Select Phase
	bool SendSelectEmpirePacket(DWORD dwEmpireID);
	bool SendSelectCharacterPacket(BYTE account_Index);
	bool SendChangeNamePacket(BYTE index, const char* name);
	bool SendCreateCharacterPacket(BYTE index, const char* name, BYTE job, BYTE shape, BYTE byStat1, BYTE byStat2, BYTE byStat3, BYTE byStat4);
	bool SendDestroyCharacterPacket(BYTE index, const char* szPrivateCode);

	// Main Game Phase
	bool SendC2CPacket(DWORD dwSize, void* pData);
	bool SendChatPacket(const char* c_szChat, BYTE byType = CHAT_TYPE_TALKING
#ifdef ENABLE_CHAT_COLOR_SYSTEM
		, bool bEmoticon = false
#endif
	);
	bool SendWhisperPacket(const char* name, const char* c_szChat);
	bool SendMessengerAddByVIDPacket(DWORD vid);
	bool SendMessengerAddByNamePacket(const char* c_szName);
	bool SendMessengerRemovePacket(const char* c_szKey, const char* c_szName);
	void __RefreshInventoryWindow();
#ifdef ENABLE_TELEPORT_TO_A_FRIEND
	bool SendMessengerRequestWarpByNamePacket(const char * c_szName);
	bool SendMessengerSummonByNamePacket(const char * c_szName);
#endif

#ifdef ENABLE_PM_ALL_SEND_SYSTEM
	bool SendBulkWhisperPacket(const char* c_szContent);
#endif
	void SelectCharacterCacheDestroy();

protected:
	bool OnProcess();
	void OffLinePhase();
	void HandShakePhase();
	void LoginPhase();
	void SelectPhase();
	void LoadingPhase();
	void GamePhase();

	bool __IsNotPing();
	void __DownloadMark();
	void __DownloadSymbol(const std::vector<DWORD>& c_rkVec_dwGuildID);

	bool __CanActMainInstance();

	enum REFRESH_WINDOW_TYPE
	{
		RefreshStatus = (1 << 0),
		RefreshAlignmentWindow = (1 << 1),
		RefreshCharacterWindow = (1 << 2),
		RefreshEquipmentWindow = (1 << 3),
		RefreshInventoryWindow = (1 << 4),
		RefreshExchangeWindow = (1 << 5),
		RefreshSkillWindow = (1 << 6),
		RefreshSafeboxWindow = (1 << 7),
		RefreshMessengerWindow = (1 << 8),
		RefreshGuildWindowInfoPage = (1 << 9),
		RefreshGuildWindowBoardPage = (1 << 10),
		RefreshGuildWindowMemberPage = (1 << 11),
		RefreshGuildWindowMemberPageGradeComboBox = (1 << 12),
		RefreshGuildWindowSkillPage = (1 << 13),
		RefreshGuildWindowGradePage = (1 << 14),
		RefreshTargetBoard = (1 << 15),
		RefreshMallWindow = (1 << 16),
	};

	void __RefreshStatus();
	void __RefreshAlignmentWindow();
	void __RefreshCharacterWindow();
	void __RefreshEquipmentWindow();
	void __RefreshExchangeWindow();
	void __RefreshSkillWindow();
	void __RefreshSafeboxWindow();
	void __RefreshMessengerWindow();
	void __RefreshGuildWindowInfoPage();
	void __RefreshGuildWindowBoardPage();
	void __RefreshGuildWindowMemberPage();
	void __RefreshGuildWindowMemberPageGradeComboBox();
	void __RefreshGuildWindowSkillPage();
	void __RefreshGuildWindowGradePage();
	void __RefreshTargetBoardByVID(DWORD dwVID);
	void __RefreshTargetBoardByName(const char* c_szName);
	void __RefreshTargetBoard();
	void __RefreshMallWindow();

	bool __SendHack(const char* c_szMsg);

protected:
	// Common
	bool RecvErrorPacket(int header);
	bool RecvPingPacket();
	bool RecvDefaultPacket(int header);
	bool RecvPhasePacket();

	// Login Phase
	bool __RecvLoginSuccessPacket3();
	bool __RecvLoginSuccessPacket4();
	bool __RecvLoginFailurePacket();
	bool __RecvEmpirePacket();
	bool __RecvLoginKeyPacket();

	// Select Phase
	bool __RecvPlayerCreateSuccessPacket();
	bool __RecvPlayerCreateFailurePacket();
	bool __RecvPlayerDestroySuccessPacket();
	bool __RecvPlayerDestroyFailurePacket();
	bool __RecvPreserveItemPacket();
	bool __RecvPlayerPoints();
	bool __RecvChangeName();

	// Loading Phase
	bool RecvMainCharacter();
	bool RecvMainCharacter2_EMPIRE();

	// Main Game Phase
	bool RecvWarpPacket();
	bool RecvPVPPacket();
	bool RecvDuelStartPacket();
	bool RecvGlobalTimePacket();
	bool RecvCharacterAppendPacket();
	bool RecvCharacterAdditionalInfo();
	bool RecvCharacterUpdatePacket();
	bool RecvCharacterDeletePacket();
	bool RecvChatPacket();
	bool RecvOwnerShipPacket();
	bool RecvSyncPositionPacket();
	bool RecvWhisperPacket();
	bool RecvPointChange();					// Alarm to python
	bool RecvChangeSpeedPacket();
#ifdef ENABLE_PM_ALL_SEND_SYSTEM
	bool RecvBulkWhisperPacket();
#endif
	bool RecvStunPacket();
	bool RecvDeadPacket();
	bool RecvCharacterMovePacket();

	bool RecvItemSetPacket();					// Alarm to python
	bool RecvItemSetPacket2();					// Alarm to python
	bool RecvItemUsePacket();					// Alarm to python
	bool RecvItemUpdatePacket();				// Alarm to python
	bool RecvItemGroundAddPacket();
	bool RecvItemGroundDelPacket();
	bool RecvItemOwnership();
	bool RecvQuickSlotAddPacket();				// Alarm to python
	bool RecvQuickSlotDelPacket();				// Alarm to python
	bool RecvQuickSlotMovePacket();				// Alarm to python

	bool RecvCharacterPositionPacket();
	bool RecvMotionPacket();

	bool RecvShopPacket();
	bool RecvShopSignPacket();
	bool RecvExchangePacket();

	// Quest
	bool RecvScriptPacket();
	bool RecvQuestInfoPacket();
	bool RecvQuestConfirmPacket();
	bool RecvRequestMakeGuild();

	// Skill
	bool RecvSkillLevel();
	bool RecvSkillLevelNew();

	// Target
	bool RecvTargetPacket();
	bool RecvViewEquipPacket();
	bool RecvDamageInfoPacket();
#ifdef ENABLE_TARGET_INFORMATION_SYSTEM
	bool RecvTargetInfoPacket();

public:
	bool SendTargetInfoLoadPacket(DWORD dwVID);
#endif
	// Mount
	bool RecvMountPacket();

	// Fly
	bool RecvCreateFlyPacket();
	bool RecvFlyTargetingPacket();
	bool RecvAddFlyTargetingPacket();

	// Messenger
	bool RecvMessenger();

	// Guild
	bool RecvGuild();

	// Party
	bool RecvPartyInvite();
	bool RecvPartyAdd();
	bool RecvPartyUpdate();
	bool RecvPartyRemove();
	bool RecvPartyLink();
	bool RecvPartyUnlink();
	bool RecvPartyParameter();

	// SafeBox
	bool RecvSafeBoxSetPacket();
	bool RecvSafeBoxDelPacket();
	bool RecvSafeBoxWrongPasswordPacket();
	bool RecvSafeBoxSizePacket();

	// Fishing
	bool RecvFishing();

	// Dungeon
	bool RecvDungeon();

	// Time
	bool RecvTimePacket();

	// WalkMode
	bool RecvWalkModePacket();

	// ChangeSkillGroup
	bool RecvChangeSkillGroupPacket();

	// Refine
	bool RecvRefineInformationPacket();
	bool RecvRefineInformationPacketNew();

	// Use Potion
	bool RecvSpecialEffect();

	bool RecvSpecificEffect();
	bool RecvSpecificEffect2();

	bool RecvDragonSoulRefine();

	// MiniMap Info
	bool RecvNPCList();
	bool RecvLandPacket();
	bool RecvTargetCreatePacket();
	bool RecvTargetCreatePacketNew();
	bool RecvTargetUpdatePacket();
	bool RecvTargetDeletePacket();

	// Affect
	bool RecvAffectAddPacket();
	bool RecvAffectRemovePacket();

	// Channel
	bool RecvChannelPacket();

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	bool	RecvAccePacket(bool bReturn = false);
#endif
#ifdef ENABLE_AURA_SYSTEM
	bool	RecvAuraPacket(bool bReturn = false);
#endif

#ifdef ENABLE_DS_SET_BONUS
	bool	RecvDSTablePacket();
#endif

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	// Multi Language
	bool RecvRequestChangeLanguage();
#endif

#ifdef ENABLE_EXTENDED_WHISPER_DETAILS
	// Whisper Details
	bool RecvWhisperDetails();
#endif

	PyObject* GetGameWindow() { return m_apoPhaseWnd[PHASE_WINDOW_GAME]; }
protected:
	bool ParseEmoticon(const char* pChatMsg, DWORD* pdwEmoticon);

	void OnConnectFailure();
	void OnScriptEventStart(int iSkin, int iIndex);

	void OnRemoteDisconnect();
	void OnDisconnect();

	void SetGameOnline();
	void SetGameOffline();
	BOOL IsGameOnline();

#ifdef ENABLE_EXTENDED_BATTLE_PASS
public:
	bool SendExtBattlePassAction(BYTE bAction);
	bool SendExtBattlePassPremium(bool premium);

protected:
	bool RecvExtBattlePassOpenPacket();
	bool RecvExtBattlePassGeneralInfoPacket();
	bool RecvExtBattlePassMissionInfoPacket();
	bool RecvExtBattlePassMissionUpdatePacket();
	bool RecvExtBattlePassRankingPacket();
#endif

protected:
	bool CheckPacket(TPacketHeader* pRetHeader);

	void __InitializeGamePhase();
	void __InitializeMarkAuth();
	void __GlobalPositionToLocalPosition(LONG& rGlobalX, LONG& rGlobalY);
	void __LocalPositionToGlobalPosition(LONG& rLocalX, LONG& rLocalY);

	bool __IsPlayerAttacking();
	bool __IsEquipItemInSlot(TItemPos Cell);

	void __ShowMapName(LONG lLocalX, LONG lLocalY);

	void __LeaveOfflinePhase() {}
	void __LeaveHandshakePhase() {}
	void __LeaveLoginPhase() {}
	void __LeaveSelectPhase() {}
	void __LeaveLoadingPhase() {}
	void __LeaveGamePhase();

	void __ClearNetworkActorManager();

	void __ClearSelectCharacterData();

	// DELETEME
	//void __SendWarpPacket();

	void __ConvertEmpireText(DWORD dwEmpireID, char* szText);

	void __RecvCharacterAppendPacket(SNetworkActorData* pkNetActorData);
	void __RecvCharacterUpdatePacket(SNetworkUpdateActorData* pkNetUpdateActorData);

	void __FilterInsult(char* szLine, UINT uLineLen);

	void __SetGuildID(DWORD id);
protected:
	TPacketGCHandshake m_HandshakeData;
	DWORD m_dwBindupRetryCount;
	DWORD m_dwMainActorVID;
	DWORD m_dwMainActorRace;
	DWORD m_dwMainActorEmpire;
	DWORD m_dwMainActorSkillGroup;
	BOOL m_isGameOnline;
	BOOL m_isStartGame;

	DWORD m_dwGuildID;
	DWORD m_dwEmpireID;

	struct SServerTimeSync
	{
		DWORD m_dwChangeServerTime;
		DWORD m_dwChangeClientTime;
	} m_kServerTimeSync;

	void __ServerTimeSync_Initialize();
	//DWORD m_dwBaseServerTime;
	//DWORD m_dwBaseClientTime;

	DWORD m_dwLastGamePingTime;

	std::string	m_stID;
	std::string	m_stPassword;
	std::string	m_strLastCommand;
	GamePhases	m_gamePhase;
	DWORD m_dwLoginKey;
	BOOL m_isWaitLoginKey;

	std::string m_stMarkIP;

	CFuncObject<CPythonNetworkStream>	m_phaseProcessFunc;
	CFuncObject<CPythonNetworkStream>	m_phaseLeaveFunc;

	PyObject* m_poHandler;
	PyObject* m_apoPhaseWnd[PHASE_WINDOW_NUM];
	PyObject* m_poSerCommandParserWnd;

	TSimplePlayerInformation			m_akSimplePlayerInfo[PLAYER_PER_ACCOUNT4];
	DWORD								m_adwGuildID[PLAYER_PER_ACCOUNT4];
	std::string							m_astrGuildName[PLAYER_PER_ACCOUNT4];
	bool m_bSimplePlayerInfo;

	CRef<CNetworkActorManager>			m_rokNetActorMgr;

	bool m_isRefreshStatus;
	bool m_isRefreshCharacterWnd;
	bool m_isRefreshEquipmentWnd;
	bool m_isRefreshInventoryWnd;
	bool m_isRefreshExchangeWnd;
	bool m_isRefreshSkillWnd;
	bool m_isRefreshSafeboxWnd;
	bool m_isRefreshMallWnd;
	bool m_isRefreshMessengerWnd;
	bool m_isRefreshGuildWndInfoPage;
	bool m_isRefreshGuildWndBoardPage;
	bool m_isRefreshGuildWndMemberPage;
	bool m_isRefreshGuildWndMemberPageGradeComboBox;
	bool m_isRefreshGuildWndSkillPage;
	bool m_isRefreshGuildWndGradePage;

	// Emoticon
	std::vector<std::string> m_EmoticonStringVector;

	struct STextConvertTable
	{
		char acUpper[26];
		char acLower[26];
		BYTE aacHan[5000][2];
	} m_aTextConvTable[3];

	struct SMarkAuth
	{
		CNetworkAddress m_kNetAddr;
		DWORD m_dwHandle;
		DWORD m_dwRandomKey;
	} m_kMarkAuth;

	DWORD m_dwSelectedCharacterIndex;

	CInsultChecker m_kInsultChecker;

	bool m_isEnableChatInsultFilter;
	bool m_bComboSkillFlag;

	std::deque<std::string> m_kQue_stHack;

private:
	struct SDirectEnterMode
	{
		bool m_isSet;
		DWORD m_dwChrSlotIndex;
	} m_kDirectEnterMode;

	void __DirectEnterMode_Initialize();
	void __DirectEnterMode_Set(UINT uChrSlotIndex);
	bool __DirectEnterMode_IsSet();

public:
	DWORD EXPORT_GetBettingGuildWarValue(const char* c_szValueName);

private:
	struct SBettingGuildWar
	{
		DWORD m_dwBettingMoney;
		DWORD m_dwObserverCount;
	} m_kBettingGuildWar;

	CInstanceBase* m_pInstTarget;

	void __BettingGuildWar_Initialize();
	void __BettingGuildWar_SetObserverCount(UINT uObserverCount);
	void __BettingGuildWar_SetBettingMoney(UINT uBettingMoney);

#ifdef ENABLE_SWITCHBOT
public:
	bool RecvSwitchbotPacket();

	bool SendSwitchbotStartPacket(uint8_t slot, std::vector<CPythonSwitchbot::TSwitchbotAttributeAlternativeTable> alternatives);
	bool SendSwitchbotStopPacket(uint8_t slot);
#endif

#ifdef ENABLE_REFRESH_CONTROL
public:
	bool	GetRefreshControl(BYTE idx) { return m_RefreshControl[idx]; }
	bool	RecvRefreshControl();
protected:
	bool m_RefreshControl[REFRESH_MAX];
#endif

public:
#ifdef ENABLE_GLOBAL_RANKING
	bool RecvGlobalRankingPacket();
#endif
#ifdef ENABLE_BIOLOG_SYSTEM
	bool RecvBiologPacket();
#endif
#ifdef ENABLE_CHAR_SETTINGS
	bool RecvCharSettings();
#endif
#ifdef ENABLE_IN_GAME_LOG_SYSTEM
	bool RecvInGameLog();
	bool RecvOfflineShopLog(WORD bufferSize);
	bool RecvOfflineShopLogAdd(WORD bufferSize);
	bool RecvTradeLog(WORD bufferSize);
	bool RecvTradeDetailsLog(WORD bufferSize);
#endif
#ifdef ENABLE_ITEM_TRANSACTIONS
	void SendItemTransactions(BYTE transaction, const std::vector<TItemTransactionsInfo>& v_itemInfo);
#endif
#ifdef ENABLE_DUNGEON_INFO
	bool RecvDungeonInfo();
	bool RecvDungeonTime(WORD bufferSize, bool update = false);
	bool RecvDungeonMessage(WORD bufferSize);
#endif

#ifdef ENABLE_NEW_PET_SYSTEM
	bool RecvNewPet();

	void RecvNewPetUnSummon();
	bool RecvNewPetUpdate();
	bool RecvNewPetUpdateExp();

	void SendNewPetPacket(BYTE subHeader);
#endif

#ifdef ENABLE_6TH_7TH_ATTR
	bool Send67AttrPacket(int iMaterialCount, int iSupportCount, int iSupportPos, int iItemPos);
	bool Send67AttrClosePacket();
	bool Recv67AttrOpenPacket();
#endif

#ifdef ENABLE_NEW_CHAT
	bool RecvNewChatPacket();
#endif
#ifdef ENABLE_BUFFI_SYSTEM
	bool RecvBuffiSkillPacket();
#endif

#ifdef ENABLE_MINI_GAME_BNW
public:
	bool SendMinigameBnwStart();
	bool SendMinigameBnwCardSelected(BYTE bCard);
	bool SendMinigameBnwFinished();

protected:
	bool RecvMinigameBnw();
#endif

#ifdef ENABLE_MINI_GAME_CATCH_KING
public:
	bool SendMiniGameCatchKingStart(int ibetNumber);
	bool SendMiniGameCatchKingDeckCardClick();
	bool SendMiniGameCatchKingFieldCardClick(int icardNumber);
	bool SendMiniGameCatchKingReward();
	bool RecvMiniGameCatchKingPacket();
#endif

};
