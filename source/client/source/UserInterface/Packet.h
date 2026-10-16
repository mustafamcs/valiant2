#pragma once

#include "Locale.h"
#include "../gamelib/RaceData.h"
#include "../gamelib/ItemData.h"

typedef BYTE TPacketHeader;

enum ClientToGamePackets
{
	HEADER_CG_LOGIN 				 = 1,
	HEADER_CG_ATTACK			 	 = 2,
	HEADER_CG_CHAT 					 = 3,
	HEADER_CG_PLAYER_CREATE 		 = 4,
	HEADER_CG_PLAYER_DESTROY		 = 5,
	HEADER_CG_PLAYER_SELECT			 = 6,
	HEADER_CG_CHARACTER_MOVE 		 = 7,
	HEADER_CG_SYNC_POSITION			 = 8,
	HEADER_CG_ENTERGAME 			 = 9,
	HEADER_CG_ITEM_USE				 = 10,
	HEADER_CG_ITEM_MOVE 			 = 11,
	HEADER_CG_ITEM_PICKUP			 = 12,
	HEADER_CG_QUICKSLOT_ADD 		 = 13,
	HEADER_CG_QUICKSLOT_DEL 		 = 14,
	HEADER_CG_QUICKSLOT_SWAP		 = 15,
	HEADER_CG_WHISPER 				 = 16,
#ifdef ENABLE_DROP_DIALOG_EXTENDED_SYSTEM
	HEADER_CG_ITEM_DELETE			 = 17,
	HEADER_CG_ITEM_SELL 			 = 18,
#else
	HEADER_CG_ITEM_DROP 			 = 17,
	HEADER_CG_ITEM_DROP2 			 = 18,
#endif
	HEADER_CG_ON_CLICK				 = 19,
	HEADER_CG_EXCHANGE				 = 20,
	HEADER_CG_CHARACTER_POSITION	 = 21,
	HEADER_CG_SCRIPT_ANSWER			 = 22,
	HEADER_CG_QUEST_INPUT_STRING 	 = 23,
	HEADER_CG_QUEST_CONFIRM 		 = 24,
	HEADER_CG_SHOP					 = 25,
	HEADER_CG_FLY_TARGETING 		 = 26,
	HEADER_CG_USE_SKILL				 = 27,
	HEADER_CG_ADD_FLY_TARGETING 	 = 28,
	HEADER_CG_SHOOT					 = 29,
	HEADER_CG_MYSHOP				 = 30,
	HEADER_CG_ITEM_USE_TO_ITEM		 = 31,
	HEADER_CG_TARGET				 = 32,
	HEADER_CG_WARP					 = 33,
	HEADER_CG_SCRIPT_BUTTON			 = 34,
	HEADER_CG_MESSENGER 			 = 35,
	HEADER_CG_MALL_CHECKOUT 		 = 36,
	HEADER_CG_SAFEBOX_CHECKIN 		 = 37,
	HEADER_CG_SAFEBOX_CHECKOUT		 = 38,
	HEADER_CG_PARTY_INVITE 			 = 39,
	HEADER_CG_PARTY_INVITE_ANSWER	 = 40,
	HEADER_CG_PARTY_REMOVE 			 = 41,
	HEADER_CG_PARTY_SET_STATE 		 = 42,
	HEADER_CG_PARTY_USE_SKILL 		 = 43,
	HEADER_CG_SAFEBOX_ITEM_MOVE		 = 44,
	HEADER_CG_PARTY_PARAMETER 		 = 45,
	HEADER_CG_GUILD 				 = 46,
	HEADER_CG_ANSWER_MAKE_GUILD		 = 47,
	HEADER_CG_FISHING				 = 48,
	HEADER_CG_GIVE_ITEM				 = 49,
	HEADER_CG_EMPIRE				 = 50,
	HEADER_CG_REFINE 				 = 51,
	HEADER_CG_MARK_LOGIN 			 = 52,
	HEADER_CG_MARK_CRCLIST			 = 53,
	HEADER_CG_MARK_UPLOAD 			 = 54,
	HEADER_CG_MARK_IDXLIST			 = 55,
	HEADER_CG_HACK					 = 56,
	HEADER_CG_CHANGE_NAME 			 = 57,
	HEADER_CG_LOGIN2 				 = 58,
	HEADER_CG_DUNGEON				 = 59,
	HEADER_CG_LOGIN3 				 = 60,
	HEADER_CG_GUILD_SYMBOL_UPLOAD	 = 61,
	HEADER_CG_GUILD_SYMBOL_CRC		 = 62,
	HEADER_CG_SCRIPT_SELECT_ITEM	 = 63,
	HEADER_CG_DRAGON_SOUL_REFINE	 = 64,
	HEADER_CG_STATE_CHECKER			 = 65,
#ifdef ENABLE_TARGET_INFORMATION_SYSTEM
	HEADER_CG_TARGET_INFO_LOAD		 = 66,
#endif
#ifdef ENABLE_CUBE_RENEWAL_WORLDARD
	HEADER_CG_CUBE_RENEWAL 			 = 67,
#endif
#ifdef ENABLE_OFFLINE_SHOP
	HEADER_CG_NEW_OFFLINESHOP 		 = 68,
#endif
#ifdef ENABLE_SWITCHBOT
	HEADER_CG_SWITCHBOT 			 = 69,
#endif
#ifdef ENABLE_PM_ALL_SEND_SYSTEM
	HEADER_CG_BULK_WHISPER			 = 71,
#endif
#ifdef ENABLE_BIOLOG_SYSTEM
	HEADER_CG_BIOLOG				 = 73,
#endif
#ifdef ENABLE_IN_GAME_LOG_SYSTEM
	HEADER_CG_IN_GAME_LOG				= 75,
#endif
#ifdef ENABLE_ITEM_TRANSACTIONS
	HEADER_CG_ITEM_TRANSACTIONS			= 76,
#endif
#ifdef ENABLE_DUNGEON_INFO
	HEADER_CG_DUNGEON_INFO				= 77,
#endif
#ifdef ENABLE_SKILL_COLOR_SYSTEM
	HEADER_CG_SKILL_COLOR				= 79,
#endif
#ifdef ENABLE_AURA_SYSTEM
	HEADER_CG_AURA						= 80,
#endif
#ifdef ENABLE_NEW_PET_SYSTEM
	HEADER_CG_NEW_PET					= 81,
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	HEADER_CG_CHANGE_LANGUAGE			= 82,
#endif
#ifdef ENABLE_EXTENDED_WHISPER_DETAILS
	HEADER_CG_WHISPER_DETAILS			= 83,
#endif
#ifdef ENABLE_EXTENDED_BATTLE_PASS
	HEADER_CG_EXT_BATTLE_PASS_ACTION	= 84,
	HEADER_CG_EXT_SEND_BP_PREMIUM		= 85,
#endif
#ifdef ENABLE_LEADERSHIP_EXTENSION
	HEADER_CG_REQUEST_PARTY_BONUS		= 86,
#endif
#ifdef ENABLE_6TH_7TH_ATTR
	HEADER_CG_67_ATTR 					= 87,
	HEADER_CG_CLOSE_67_ATTR 			= 88,
#endif
#ifdef ENABLE_BUFFI_SYSTEM
	HEADER_CG_BUFFI						= 89,
#endif
#ifdef ENABLE_MINI_GAME_OKEY_NORMAL
	HEADER_CG_OKEY_CARD					= 90,
#endif
#ifdef ENABLE_MINI_GAME_BNW
	HEADER_CG_MINIGAME_BNW				= 91,
#endif
#ifdef ENABLE_MINI_GAME_CATCH_KING
	HEADER_CG_MINI_GAME_CATCH_KING		= 92,
#endif
	HEADER_CG_KEY_AGREEMENT			= 252,
	HEADER_CG_TIME_SYNC				= 253,
	HEADER_CG_PONG					= 254,
	HEADER_CG_HANDSHAKE				= 255,
};

enum GameToClientPackets
{
	HEADER_GC_CHARACTER_ADD				= 1,
	HEADER_GC_CHARACTER_DEL				= 2,
	HEADER_GC_CHARACTER_MOVE			= 3,
	HEADER_GC_CHAT						= 4,
	HEADER_GC_SYNC_POSITION				= 5,
	HEADER_GC_LOGIN_SUCCESS3			= 6,
	HEADER_GC_LOGIN_FAILURE				= 7,
	HEADER_GC_PLAYER_CREATE_SUCCESS		= 8,
	HEADER_GC_PLAYER_CREATE_FAILURE		= 9,
	HEADER_GC_PLAYER_DELETE_SUCCESS		= 10,
	HEADER_GC_PLAYER_DELETE_WRONG_SOCIAL_ID = 11,
	HEADER_GC_STUN						= 12,
	HEADER_GC_DEAD						= 13,
	HEADER_GC_MAIN_CHARACTER			= 14,
	HEADER_GC_PLAYER_POINTS				= 15,
	HEADER_GC_PLAYER_POINT_CHANGE		= 16,
	HEADER_GC_CHANGE_SPEED				= 17,
	HEADER_GC_CHARACTER_UPDATE			= 18,
	HEADER_GC_ITEM_SET					= 19,
	HEADER_GC_ITEM_SET2					= 20,
	HEADER_GC_ITEM_USE					= 21,
	HEADER_GC_ITEM_DROP					= 22,
	HEADER_GC_ITEM_UPDATE				= 23,
	HEADER_GC_ITEM_GROUND_ADD			= 24,
	HEADER_GC_ITEM_GROUND_DEL			= 25,
	HEADER_GC_QUICKSLOT_ADD				= 26,
	HEADER_GC_QUICKSLOT_DEL				= 27,
	HEADER_GC_QUICKSLOT_SWAP			= 28,
	HEADER_GC_ITEM_OWNERSHIP			= 29,
	HEADER_GC_LOGIN_SUCCESS4			= 30,
	HEADER_GC_WHISPER					= 31,
	HEADER_GC_MOTION					= 32,
	HEADER_GC_SHOP						= 33,
	HEADER_GC_SHOP_SIGN					= 34,
	HEADER_GC_DUEL_START				= 35,
	HEADER_GC_PVP						= 36,
	HEADER_GC_EXCHANGE					= 37,
	HEADER_GC_CHARACTER_POSITION		= 38,
	HEADER_GC_PING						= 39,
	HEADER_GC_SCRIPT					= 40,
	HEADER_GC_QUEST_CONFIRM				= 41,
	HEADER_GC_MOUNT						= 42,
	HEADER_GC_OWNERSHIP					= 43,
	HEADER_GC_TARGET					= 44,
	HEADER_GC_WARP						= 45,
	HEADER_GC_ADD_FLY_TARGETING			= 46,
	HEADER_GC_CREATE_FLY				= 47,
	HEADER_GC_FLY_TARGETING				= 48,
	HEADER_GC_SKILL_LEVEL				= 49,
	HEADER_GC_MESSENGER					= 50,
	HEADER_GC_GUILD						= 51,
	HEADER_GC_SKILL_LEVEL_NEW			= 52,
	HEADER_GC_PARTY_INVITE				= 53,
	HEADER_GC_PARTY_ADD					= 54,
	HEADER_GC_PARTY_UPDATE				= 55,
	HEADER_GC_PARTY_REMOVE				= 56,
	HEADER_GC_QUEST_INFO				= 57,
	HEADER_GC_REQUEST_MAKE_GUILD		= 58,
	HEADER_GC_PARTY_PARAMETER			= 59,
	HEADER_GC_SAFEBOX_SET				= 60,
	HEADER_GC_SAFEBOX_DEL				= 61,
	HEADER_GC_SAFEBOX_WRONG_PASSWORD	= 62,
	HEADER_GC_SAFEBOX_SIZE				= 63,
	HEADER_GC_FISHING					= 64,
	HEADER_GC_EMPIRE					= 65,
	HEADER_GC_PARTY_LINK				= 66,
	HEADER_GC_PARTY_UNLINK				= 67,
	HEADER_GC_REFINE_INFORMATION		= 68,
	HEADER_GC_VIEW_EQUIP				= 69,
	HEADER_GC_MARK_BLOCK				= 70,
	HEADER_GC_MARK_IDXLIST				= 71,
	HEADER_GC_TIME						= 72,
	HEADER_GC_CHANGE_NAME				= 73,
	HEADER_GC_DUNGEON					= 74,
	HEADER_GC_WALK_MODE					= 75,
	HEADER_GC_CHANGE_SKILL_GROUP		= 76,
	HEADER_GC_MAIN_CHARACTER2_EMPIRE	= 77,
	HEADER_GC_SEPCIAL_EFFECT			= 78,
	HEADER_GC_NPC_POSITION				= 79,
	HEADER_GC_LOGIN_KEY					= 80,
	HEADER_GC_REFINE_INFORMATION_NEW	= 81,
	HEADER_GC_CHANNEL					= 82,
	HEADER_GC_MALL_OPEN					= 83,
	HEADER_GC_TARGET_UPDATE				= 84,
	HEADER_GC_TARGET_DELETE				= 85,
	HEADER_GC_TARGET_CREATE_NEW			= 86,
	HEADER_GC_AFFECT_ADD				= 87,
	HEADER_GC_AFFECT_REMOVE				= 88,
	HEADER_GC_MALL_SET					= 89,
	HEADER_GC_MALL_DEL					= 90,
	HEADER_GC_LAND_LIST					= 91,
	HEADER_GC_LOVER_INFO				= 92,
	HEADER_GC_LOVE_POINT_UPDATE			= 93,
	HEADER_GC_GUILD_SYMBOL_DATA			= 94,
	HEADER_GC_DIG_MOTION				= 95,
	HEADER_GC_DAMAGE_INFO				= 96,
	HEADER_GC_CHAR_ADDITIONAL_INFO		= 97,
	HEADER_GC_AUTH_SUCCESS				= 100,
	HEADER_GC_SPECIFIC_EFFECT			= 101,
	HEADER_GC_DRAGON_SOUL_REFINE		= 102,
	HEADER_GC_RESPOND_CHANNELSTATUS		= 103,
#ifdef ENABLE_CUBE_RENEWAL_WORLDARD
	HEADER_GC_CUBE_RENEWAL				= 104,
#endif
#ifdef ENABLE_TARGET_INFORMATION_SYSTEM
	HEADER_GC_TARGET_INFO				= 105,
#endif
#ifdef ENABLE_DS_SET_BONUS
	HEADER_GC_DS_TABLE					= 106,
#endif
#ifdef ENABLE_OFFLINE_SHOP
	HEADER_GC_NEW_OFFLINESHOP			= 107,
#endif
#ifdef ENABLE_SWITCHBOT
	HEADER_GC_SWITCHBOT					= 108,
#endif
#ifdef ENABLE_REFRESH_CONTROL
	HEADER_GC_REFRESH_CONTROL			= 110,
#endif
#ifdef ENABLE_GLOBAL_RANKING
	HEADER_GC_GLOBAL_RANKING			= 111,
#endif
#ifdef ENABLE_PM_ALL_SEND_SYSTEM
	HEADER_GC_BULK_WHISPER				 = 112,
#endif
#ifdef ENABLE_BIOLOG_SYSTEM
	HEADER_GC_BIOLOG					= 114,
#endif
#ifdef ENABLE_CHAR_SETTINGS
	HEADER_GC_CHAR_SETTINGS				= 116,
#endif

#ifdef ENABLE_IN_GAME_LOG_SYSTEM
	HEADER_GC_IN_GAME_LOG				= 117,
#endif
#ifdef ENABLE_DUNGEON_INFO
	HEADER_GC_DUNGEON_INFO				= 118,
#endif
#ifdef ENABLE_EVENT_MANAGER
	HEADER_GC_EVENT_MANAGER				= 119,
#endif
#ifdef ENABLE_ITEMSHOP
	HEADER_GC_ITEMSHOP					= 120,
#endif
#ifdef ENABLE_AURA_SYSTEM
	HEADER_GC_AURA						 = 121,
#endif
#ifdef ENABLE_NEW_PET_SYSTEM
	HEADER_GC_NEW_PET					= 122,
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	HEADER_GC_REQUEST_CHANGE_LANGUAGE	= 123,
#endif
#ifdef ENABLE_EXTENDED_WHISPER_DETAILS
	HEADER_GC_WHISPER_DETAILS			= 124,
#endif
#ifdef ENABLE_EXTENDED_BATTLE_PASS
	HEADER_GC_EXT_BATTLE_PASS_OPEN				= 125,
	HEADER_GC_EXT_BATTLE_PASS_GENERAL_INFO		= 126,
	HEADER_GC_EXT_BATTLE_PASS_MISSION_INFO		= 127,
	HEADER_GC_EXT_BATTLE_PASS_MISSION_UPDATE	= 128,
	HEADER_GC_EXT_BATTLE_PASS_SEND_RANKING		= 129,
#endif
#ifdef ENABLE_6TH_7TH_ATTR
	HEADER_GC_OPEN_67_ATTR 					= 130,
#endif
#ifdef ENABLE_BUFFI_SYSTEM
	HEADER_GC_BUFFI						= 131,
#endif
#ifdef ENABLE_NEW_CHAT
	HEADER_GC_NEW_CHAT					= 132,
#endif
#ifdef ENABLE_MINI_GAME_OKEY_NORMAL
	HEADER_GC_OKEY_CARD					= 133,
#endif
#ifdef ENABLE_MINI_GAME_BNW
	HEADER_GC_MINIGAME_BNW				= 134,
#endif
#ifdef ENABLE_MINI_GAME_CATCH_KING
	HEADER_GC_MINI_GAME_CATCH_KING		= 135,
#endif
	HEADER_GC_SPECIFIC_EFFECT2			= 136,
	HEADER_GC_CHARACTER_DELETE_FAILURE	= 137,
	HEADER_GC_KEY_AGREEMENT_COMPLETED	= 250,
	HEADER_GC_KEY_AGREEMENT				= 251,
	HEADER_GC_HANDSHAKE_OK				= 252,
	HEADER_GC_PHASE						= 253,
	HEADER_GC_BINDUDP					= 254,
	HEADER_GC_HANDSHAKE					= 255,
};

enum eControls
{
	ID_MAX_NUM = 30,
	PASS_MAX_NUM = 16,
	CHAT_MAX_NUM = 128,
	PATH_NODE_MAX_NUM = 64,
	SHOP_SIGN_MAX_LEN = 32,
	PLAYER_PER_ACCOUNT3 = 3,
#ifndef ENABLE_PLAYER_PER_ACCOUNT5
	PLAYER_PER_ACCOUNT4 = 4,
#else
	PLAYER_PER_ACCOUNT4 = 5,
	PLAYER_PER_ACCOUNT5 = 5,
#endif
	PLAYER_ITEM_SLOT_MAX_NUM = 20,
	QUICKSLOT_MAX_LINE = 4,
	QUICKSLOT_MAX_COUNT_PER_LINE = 8,
	QUICKSLOT_MAX_COUNT = QUICKSLOT_MAX_LINE * QUICKSLOT_MAX_COUNT_PER_LINE,
	QUICKSLOT_MAX_NUM = 36,
#ifdef ENABLE_EXTENDED_SHOP_SLOTS
	SHOP_HOST_ITEM_MAX_NUM = 64,
#else
	SHOP_HOST_ITEM_MAX_NUM = 40,
#endif
	METIN_SOCKET_COUNT = 6,
	PARTY_AFFECT_SLOT_MAX_NUM = 7,
	GUILD_GRADE_NAME_MAX_LEN = 8,
	GUILD_NAME_MAX_LEN = 12,
	GUILD_GRADE_COUNT = 15,
	GULID_COMMENT_MAX_LEN = 50,
	MARK_CRC_NUM = 8 * 8,
	MARK_DATA_SIZE = 16 * 12,
	SYMBOL_DATA_SIZE = 128 * 256,
	QUEST_INPUT_STRING_MAX_NUM = 64,
	PRIVATE_CODE_LENGTH = 8,
	REFINE_MATERIAL_MAX_NUM = 5,
	WEAR_MAX_NUM = CItemData::WEAR_MAX_NUM,
	SHOP_TAB_NAME_MAX = 32,
	SHOP_TAB_COUNT_MAX = 3,
};

#pragma pack(push)
#pragma pack(1)

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Mark
typedef struct command_mark_login
{
	BYTE    header;
	DWORD   handle;
	DWORD   random_key;
} TPacketCGMarkLogin;

typedef struct command_mark_upload
{
	BYTE    header;
	DWORD   gid;
	BYTE    image[16 * 12 * 4];
} TPacketCGMarkUpload;

typedef struct command_mark_idxlist
{
	BYTE    header;
} TPacketCGMarkIDXList;

typedef struct command_mark_crclist
{
	BYTE    header;
	BYTE    imgIdx;
	DWORD   crclist[80];
} TPacketCGMarkCRCList;

typedef struct packet_mark_idxlist
{
	BYTE    header;
	DWORD	bufSize;
	WORD    count;
} TPacketGCMarkIDXList;

typedef struct packet_mark_block
{
	BYTE    header;
	DWORD   bufSize;
	BYTE	imgIdx;
	DWORD   count;
} TPacketGCMarkBlock;

typedef struct command_symbol_upload
{
	BYTE	header;
	WORD	size;
	DWORD	handle;
} TPacketCGSymbolUpload;

typedef struct command_symbol_crc
{
	BYTE	header;
	DWORD	dwGuildID;
	DWORD	dwCRC;
	DWORD	dwSize;
} TPacketCGSymbolCRC;

typedef struct packet_symbol_data
{
	BYTE header;
	WORD size;
	DWORD guild_id;
} TPacketGCGuildSymbolData;


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// To Server

typedef struct command_checkin
{
	BYTE header;
	char name[ID_MAX_NUM + 1];
	char pwd[PASS_MAX_NUM + 1];
} TPacketCGCheckin;

typedef struct command_login
{
	BYTE header;
	char name[ID_MAX_NUM + 1];
	char pwd[PASS_MAX_NUM + 1];
} TPacketCGLogin;

typedef struct command_login2
{
	BYTE	header;
	char	name[ID_MAX_NUM + 1];
	DWORD	login_key;
	DWORD	adwClientKey[4];
} TPacketCGLogin2;

typedef struct command_login3
{
	BYTE	header;
	char	name[ID_MAX_NUM + 1];
	char	pwd[PASS_MAX_NUM + 1];
	DWORD	adwClientKey[4];
#ifdef ENABLE_HWID
	char hwid[64 + 1];
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	BYTE bLanguage;
#endif
} TPacketCGLogin3;

typedef struct command_direct_enter
{
	BYTE        bHeader;
	char        login[ID_MAX_NUM + 1];
	char        passwd[PASS_MAX_NUM + 1];
	BYTE        index;
} TPacketCGDirectEnter;

typedef struct command_player_select
{
	BYTE	header;
	BYTE	player_index;
} TPacketCGSelectCharacter;

typedef struct command_attack
{
	BYTE	header;
	BYTE	bType;
	DWORD	dwVictimVID;
	BYTE	bCRCMagicCubeProcPiece;
	BYTE	bCRCMagicCubeFilePiece;
} TPacketCGAttack;

typedef struct command_chat
{
	BYTE	header;
	WORD	length;
	BYTE	type;
#ifdef ENABLE_CHAT_COLOR_SYSTEM
	bool bEmoticon;
#endif
} TPacketCGChat;

typedef struct command_whisper
{
	BYTE        bHeader;
	WORD        wSize;
	char        szNameTo[CHARACTER_NAME_MAX_LEN + 1];
} TPacketCGWhisper;

enum EBattleMode
{
	BATTLEMODE_ATTACK = 0,
	BATTLEMODE_DEFENSE = 1,
};

typedef struct command_EnterFrontGame
{
	BYTE header;
} TPacketCGEnterFrontGame;

typedef struct command_item_use
{
	BYTE header;
	TItemPos pos;
#ifdef ENABLE_CHEST_OPEN_RENEWAL
	MAX_COUNT item_open_count;
#endif
} TPacketCGItemUse;

typedef struct command_item_use_to_item
{
	BYTE header;
	TItemPos source_pos;
	TItemPos target_pos;
} TPacketCGItemUseToItem;

#ifdef ENABLE_DROP_DIALOG_EXTENDED_SYSTEM
typedef struct command_item_delete
{
	BYTE		header;
	TItemPos	item_pos;
} TPacketCGItemDelete;
typedef struct command_item_sell
{
	BYTE		header;
	TItemPos	item_pos;
} TPacketCGItemSell;
#else
typedef struct command_item_drop
{
	BYTE  header;
	TItemPos pos;
	DWORD elk;
} TPacketCGItemDrop;

typedef struct command_item_drop2
{
	BYTE        header;
	TItemPos pos;
	DWORD       gold;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	count;
#else
	BYTE		count;
#endif
} TPacketCGItemDrop2;
#endif

typedef struct command_item_move
{
	BYTE header;
	TItemPos pos;
	TItemPos change_pos;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT num;
#else
	BYTE num;
#endif
} TPacketCGItemMove;

typedef struct command_item_pickup
{
	BYTE header;
	DWORD vid;
} TPacketCGItemPickUp;

typedef struct command_quickslot_add
{
	BYTE        header;
	QS_USHORT        pos;
	TQuickSlot	slot;
}TPacketCGQuickSlotAdd;

typedef struct command_quickslot_del
{
	BYTE        header;
	QS_USHORT        pos;
}TPacketCGQuickSlotDel;

typedef struct command_quickslot_swap
{
	BYTE        header;
	QS_USHORT        pos;
	QS_USHORT        change_pos;
}TPacketCGQuickSlotSwap;

typedef struct command_on_click
{
	BYTE		header;
	DWORD		vid;
} TPacketCGOnClick;

enum
{
	SHOP_SUBHEADER_CG_END,
	SHOP_SUBHEADER_CG_BUY,
	SHOP_SUBHEADER_CG_SELL,
	SHOP_SUBHEADER_CG_SELL2,
#ifdef ENABLE_MULTIPLE_BUY_ITEMS
	SHOP_SUBHEADER_CG_MULTIBUY
#endif
};

typedef struct command_shop
{
	BYTE        header;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	subheader;
#else
	BYTE		subheader;
#endif
} TPacketCGShop;

enum
{
	EXCHANGE_SUBHEADER_CG_START,			// arg1 == vid of target character
	EXCHANGE_SUBHEADER_CG_ITEM_ADD,		// arg1 == position of item
	EXCHANGE_SUBHEADER_CG_ITEM_DEL,		// arg1 == position of item
	EXCHANGE_SUBHEADER_CG_ELK_ADD,			// arg1 == amount of elk
	EXCHANGE_SUBHEADER_CG_ACCEPT,			// arg1 == not used
	EXCHANGE_SUBHEADER_CG_CANCEL,			// arg1 == not used
};

typedef struct command_exchange
{
	BYTE		header;
	BYTE		subheader;
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t		arg1;
#else
	DWORD		arg1;
#endif
	BYTE		arg2;
	TItemPos	Pos;
#if defined(ENABLE_CHECKINOUT_UPDATE)
	bool		SelectPosAuto;
#endif
} TPacketCGExchange;

typedef struct command_position
{
	BYTE        header;
	BYTE        position;
} TPacketCGPosition;

typedef struct command_script_answer
{
	BYTE        header;
	BYTE		answer;
} TPacketCGScriptAnswer;

typedef struct command_script_button
{
	BYTE        header;
	unsigned int			idx;
} TPacketCGScriptButton;

typedef struct command_target
{
	BYTE        header;
	DWORD       dwVID;
} TPacketCGTarget;

typedef struct command_move
{
	BYTE		bHeader;
	BYTE		bFunc;
	BYTE		bArg;
	BYTE		bRot;
	LONG		lX;
	LONG		lY;
	DWORD		dwTime;
} TPacketCGMove;

typedef struct command_sync_position_element
{
	DWORD       dwVID;
	long        lX;
	long        lY;
} TPacketCGSyncPositionElement;

typedef struct command_sync_position
{
	BYTE        bHeader;
	WORD		wSize;
} TPacketCGSyncPosition;

typedef struct command_fly_targeting
{
	BYTE		bHeader;
	DWORD		dwTargetVID;
	long		lX;
	long		lY;
} TPacketCGFlyTargeting;

typedef struct packet_fly_targeting
{
	BYTE        bHeader;
	DWORD		dwShooterVID;
	DWORD		dwTargetVID;
	long		lX;
	long		lY;
} TPacketGCFlyTargeting;

typedef struct packet_shoot
{
	BYTE		bHeader;
	BYTE		bType;
} TPacketCGShoot;

typedef struct command_warp
{
	BYTE			bHeader;
} TPacketCGWarp;

enum
{
	MESSENGER_SUBHEADER_GC_LIST,
	MESSENGER_SUBHEADER_GC_LOGIN,
	MESSENGER_SUBHEADER_GC_LOGOUT,
	MESSENGER_SUBHEADER_GC_INVITE,
#ifdef ENABLE_MESSENGER_TEAM
	MESSENGER_SUBHEADER_GC_TEAM_LIST,
	MESSENGER_SUBHEADER_GC_TEAM_LOGIN,
	MESSENGER_SUBHEADER_GC_TEAM_LOGOUT,
#endif
};

typedef struct packet_messenger
{
	BYTE header;
	WORD size;
	BYTE subheader;
} TPacketGCMessenger;

typedef struct packet_messenger_list_offline
{
	BYTE connected; // always 0
	BYTE length;
} TPacketGCMessengerListOffline;

#ifdef ENABLE_MESSENGER_TEAM
typedef struct packet_messenger_team_list_offline
{
	BYTE connected; // always 0
	BYTE length;
} TPacketGCMessengerTeamListOffline;

typedef struct packet_messenger_team_list_online
{
	BYTE connected; // always 1
	BYTE length;
} TPacketGCMessengerTeamListOnline;
#endif


enum
{
	MESSENGER_CONNECTED_STATE_OFFLINE,
	MESSENGER_CONNECTED_STATE_ONLINE,
};

typedef struct packet_messenger_list_online
{
	BYTE connected;
	BYTE length;
	//BYTE length_char_name;
} TPacketGCMessengerListOnline;

typedef struct packet_messenger_login
{
	//BYTE length_login;
	//BYTE length_char_name;
	BYTE length;
} TPacketGCMessengerLogin;

typedef struct packet_messenger_logout
{
	BYTE length;
} TPacketGCMessengerLogout;

enum
{
	MESSENGER_SUBHEADER_CG_ADD_BY_VID,
	MESSENGER_SUBHEADER_CG_ADD_BY_NAME,
	MESSENGER_SUBHEADER_CG_REMOVE,
#ifdef ENABLE_TELEPORT_TO_A_FRIEND
	MESSENGER_SUBHEADER_CG_REQUEST_WARP_BY_NAME,
	MESSENGER_SUBHEADER_CG_SUMMON_BY_NAME,	
#endif
};

typedef struct command_messenger
{
	BYTE header;
	BYTE subheader;
} TPacketCGMessenger;

typedef struct command_messenger_remove
{
	BYTE length;
} TPacketCGMessengerRemove;

enum
{
	SAFEBOX_MONEY_STATE_SAVE,
	SAFEBOX_MONEY_STATE_WITHDRAW,
};

typedef struct command_safebox_money
{
	BYTE        bHeader;
	BYTE        bState;
	DWORD       dwMoney;
} TPacketCGSafeboxMoney;

typedef struct command_safebox_checkout
{
	BYTE        bHeader;
	BYTE        bSafePos;
	TItemPos	ItemPos;
} TPacketCGSafeboxCheckout;

typedef struct command_safebox_checkin
{
	BYTE        bHeader;
	BYTE        bSafePos;
	TItemPos	ItemPos;
} TPacketCGSafeboxCheckin;

typedef struct command_mall_checkout
{
	BYTE        bHeader;
	BYTE        bMallPos;
	TItemPos	ItemPos;
} TPacketCGMallCheckout;

///////////////////////////////////////////////////////////////////////////////////
// Party

typedef struct command_use_skill
{
	BYTE                bHeader;
	DWORD               dwVnum;
	DWORD				dwTargetVID;
} TPacketCGUseSkill;

typedef struct command_party_invite
{
	BYTE header;
	DWORD vid;
} TPacketCGPartyInvite;

typedef struct command_party_invite_answer
{
	BYTE header;
	DWORD leader_pid;
	BYTE accept;
} TPacketCGPartyInviteAnswer;

typedef struct command_party_remove
{
	BYTE header;
	DWORD pid;
} TPacketCGPartyRemove;

typedef struct command_party_set_state
{
	BYTE byHeader;
	DWORD dwVID;
	BYTE byState;
	BYTE byFlag;
} TPacketCGPartySetState;

typedef struct packet_party_link
{
	BYTE header;
	DWORD pid;
	DWORD vid;
} TPacketGCPartyLink;

typedef struct packet_party_unlink
{
	BYTE header;
	DWORD pid;
	DWORD vid;
} TPacketGCPartyUnlink;

typedef struct command_party_use_skill
{
	BYTE byHeader;
	BYTE bySkillIndex;
	DWORD dwTargetVID;
} TPacketCGPartyUseSkill;

enum
{
	GUILD_SUBHEADER_CG_ADD_MEMBER,
	GUILD_SUBHEADER_CG_REMOVE_MEMBER,
	GUILD_SUBHEADER_CG_CHANGE_GRADE_NAME,
	GUILD_SUBHEADER_CG_CHANGE_GRADE_AUTHORITY,
	GUILD_SUBHEADER_CG_OFFER,
	GUILD_SUBHEADER_CG_POST_COMMENT,
	GUILD_SUBHEADER_CG_DELETE_COMMENT,
	GUILD_SUBHEADER_CG_REFRESH_COMMENT,
	GUILD_SUBHEADER_CG_CHANGE_MEMBER_GRADE,
	GUILD_SUBHEADER_CG_USE_SKILL,
	GUILD_SUBHEADER_CG_CHANGE_MEMBER_GENERAL,
	GUILD_SUBHEADER_CG_GUILD_INVITE_ANSWER,
	GUILD_SUBHEADER_CG_CHARGE_GSP,
	GUILD_SUBHEADER_CG_DEPOSIT_MONEY,
	GUILD_SUBHEADER_CG_WITHDRAW_MONEY,
};

typedef struct command_guild
{
	BYTE byHeader;
	BYTE bySubHeader;
} TPacketCGGuild;

typedef struct command_guild_answer_make_guild
{
	BYTE header;
	char guild_name[GUILD_NAME_MAX_LEN + 1];
} TPacketCGAnswerMakeGuild;

typedef struct command_give_item
{
	BYTE byHeader;
	DWORD dwTargetVID;
	TItemPos ItemPos;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT byItemCount;
#else
	BYTE byItemCount;
#endif
} TPacketCGGiveItem;

typedef struct SPacketCGHack
{
	BYTE        bHeader;
	char        szBuf[255 + 1];
} TPacketCGHack;

typedef struct command_dungeon
{
	BYTE		bHeader;
	WORD		size;
} TPacketCGDungeon;

#ifdef ENABLE_BUY_WITH_ITEMS
typedef struct SShopItemPrice
{
	uint32_t		vnum;
	uint32_t		count;
} TShopItemPrice;
#endif

// Private Shop
typedef struct SShopItemTable
{
	DWORD		vnum;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	count;
#else
	BYTE		count;
#endif
#ifdef ENABLE_BUY_WITH_ITEMS
	TShopItemPrice	itemPrice[MAX_SHOP_PRICES];
#endif
	TItemPos	pos;
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t		price;
#else
	DWORD		price;
#endif
	BYTE		display_pos;
} TShopItemTable;

typedef struct SPacketCGMyShop
{
	BYTE        bHeader;
	char        szSign[SHOP_SIGN_MAX_LEN + 1];
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	bCount;
#else
	BYTE		bCount; // count of TShopItemTable, max 39
#endif
} TPacketCGMyShop;

typedef struct SPacketCGRefine
{
	BYTE		header;
	BYTE		pos;
	BYTE		type;
} TPacketCGRefine;

typedef struct SPacketCGChangeName
{
	BYTE header;
	BYTE index;
	char name[CHARACTER_NAME_MAX_LEN + 1];
} TPacketCGChangeName;

enum EPartyExpDistributionType
{
	PARTY_EXP_DISTRIBUTION_NON_PARITY,
	PARTY_EXP_DISTRIBUTION_PARITY,
};

typedef struct command_party_parameter
{
	BYTE        bHeader;
	BYTE        bDistributeMode;
} TPacketCGPartyParameter;

typedef struct command_quest_input_string
{
	BYTE        bHeader;
	char		szString[QUEST_INPUT_STRING_MAX_NUM + 1];
} TPacketCGQuestInputString;

typedef struct command_quest_confirm
{
	BYTE header;
	BYTE answer;
	DWORD requestPID;
} TPacketCGQuestConfirm;

typedef struct command_script_select_item
{
	BYTE header;
	DWORD selection;
} TPacketCGScriptSelectItem;

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// From Server
enum EPhase
{
	PHASE_CLOSE,
	PHASE_HANDSHAKE,
	PHASE_LOGIN,
	PHASE_SELECT,
	PHASE_LOADING,
	PHASE_GAME,
	PHASE_DEAD,

	PHASE_DBCLIENT_CONNECTING,
	PHASE_DBCLIENT,
	PHASE_P2P,
	PHASE_AUTH,
};

typedef struct packet_phase
{
	BYTE        header;
	BYTE        phase;
} TPacketGCPhase;

typedef struct packet_blank
{
	BYTE		header;
} TPacketGCBlank;

typedef struct packet_blank_dynamic
{
	BYTE		header;
	WORD		size;
} TPacketGCBlankDynamic;

typedef struct packet_header_handshake
{
	BYTE		header;
	DWORD		dwHandshake;
	DWORD		dwTime;
	LONG		lDelta;
} TPacketGCHandshake;

typedef struct packet_header_bindudp
{
	BYTE		header;
	DWORD		addr;
	WORD		port;
} TPacketGCBindUDP;

typedef struct packet_header_dynamic_size
{
	BYTE		header;
	WORD		size;
} TDynamicSizePacketHeader;

#ifdef ENABLE_LARGE_DYNAMIC_PACKET
typedef struct SLargeDynamicSizePacketHeader
{
	BYTE		header;
	int			size;
} TLargeDynamicSizePacketHeader;
#endif

typedef struct SSimplePlayerInformation
{
	DWORD               dwID;
	char                szName[CHARACTER_NAME_MAX_LEN + 1];
	BYTE                byJob;
	BYTE                byLevel;
	DWORD               dwPlayMinutes;
#ifdef ENABLE_OFFICAL_CHARACTER_SCREEN
	DWORD				dwLastPlayTime;
#endif
	BYTE                byST, byHT, byDX, byIQ;
	DWORD                wMainPart;
	BYTE                bChangeName;
	DWORD				wHairPart;
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	DWORD				wAccePart;
#endif
	BYTE                bDummy[4];
	long				x, y;
	LONG				lAddr;
	WORD				wPort;
	BYTE				bySkillGroup;
} TSimplePlayerInformation;

typedef struct packet_login_success3
{
	BYTE						header;
	TSimplePlayerInformation	akSimplePlayerInformation[PLAYER_PER_ACCOUNT3];
	DWORD						guild_id[PLAYER_PER_ACCOUNT3];
	char						guild_name[PLAYER_PER_ACCOUNT3][GUILD_NAME_MAX_LEN + 1];
	DWORD handle;
	DWORD random_key;
} TPacketGCLoginSuccess3;

typedef struct packet_login_success4
{
	BYTE						header;
	TSimplePlayerInformation	akSimplePlayerInformation[PLAYER_PER_ACCOUNT4];
	DWORD						guild_id[PLAYER_PER_ACCOUNT4];
	char						guild_name[PLAYER_PER_ACCOUNT4][GUILD_NAME_MAX_LEN + 1];
	DWORD handle;
	DWORD random_key;
} TPacketGCLoginSuccess4;

#ifdef ENABLE_PLAYER_PER_ACCOUNT5
typedef struct packet_login_success5
{
	BYTE						header;
	TSimplePlayerInformation	akSimplePlayerInformation[PLAYER_PER_ACCOUNT5];
	DWORD						guild_id[PLAYER_PER_ACCOUNT5];
	char						guild_name[PLAYER_PER_ACCOUNT5][GUILD_NAME_MAX_LEN + 1];
	DWORD handle;
	DWORD random_key;
} TPacketGCLoginSuccess5;
#endif

enum { LOGIN_STATUS_MAX_LEN = 8 };
typedef struct packet_login_failure
{
	BYTE	header;
	char	szStatus[LOGIN_STATUS_MAX_LEN + 1];
} TPacketGCLoginFailure;

typedef struct command_player_create
{
	BYTE        header;
	BYTE        index;
	char        name[CHARACTER_NAME_MAX_LEN + 1];
	WORD        job;
	BYTE		shape;
	BYTE		CON;
	BYTE		INT;
	BYTE		STR;
	BYTE		DEX;
} TPacketCGCreateCharacter;

typedef struct command_player_create_success
{
	BYTE						header;
	BYTE						bAccountCharacterSlot;
	TSimplePlayerInformation	kSimplePlayerInfomation;
} TPacketGCPlayerCreateSuccess;

typedef struct command_create_failure
{
	BYTE	header;
	BYTE	bType;
} TPacketGCCreateFailure;

typedef struct command_player_delete
{
	BYTE        header;
	BYTE        index;
	char		szPrivateCode[PRIVATE_CODE_LENGTH];
} TPacketCGDestroyCharacter;

typedef struct packet_character_delete_failure
{
	BYTE        header;
	BYTE        error_code;
} TPacketGCCharacterDeleteFailure;

typedef struct packet_player_delete_success
{
	BYTE        header;
	BYTE        account_index;
} TPacketGCDestroyCharacterSuccess;

enum
{
	ADD_CHARACTER_STATE_DEAD = (1 << 0),
	ADD_CHARACTER_STATE_SPAWN = (1 << 1),
	ADD_CHARACTER_STATE_GUNGON = (1 << 2),
	ADD_CHARACTER_STATE_KILLER = (1 << 3),
	ADD_CHARACTER_STATE_PARTY = (1 << 4),
};

enum EPKModes
{
	PK_MODE_PEACE,
	PK_MODE_REVENGE,
	PK_MODE_FREE,
	PK_MODE_PROTECT,
	PK_MODE_GUILD,
	PK_MODE_MAX_NUM,
};

enum ECharacterEquipmentPart
{
	CHR_EQUIPPART_ARMOR,
	CHR_EQUIPPART_WEAPON,
	CHR_EQUIPPART_HEAD,
	CHR_EQUIPPART_HAIR,
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	CHR_EQUIPPART_ACCE,
#endif
#ifdef ENABLE_AURA_SYSTEM
	CHR_EQUIPPART_AURA,
#endif
#ifdef ENABLE_CROWN_SYSTEM
	CHR_EQUIPPART_CROWN,
#endif
	CHR_EQUIPPART_NUM,
};

#ifdef ENABLE_ITEMS_SHINING
enum EShiningParts
{
	CHR_SHINING_WRIST_LEFT,
	CHR_SHINING_WRIST_RIGHT,
	CHR_SHINING_ARMOR,
	CHR_SHINING_NUM,
};
#endif

typedef struct packet_char_additional_info
{
	BYTE    header;
	DWORD   dwVID;
	char    name[CHARACTER_NAME_MAX_LEN + 1];
	DWORD    awPart[CHR_EQUIPPART_NUM];
#ifdef ENABLE_ITEMS_SHINING
	DWORD	adwShining[CHR_SHINING_NUM];
#endif
	BYTE	bEmpire;
	DWORD   dwGuildID;
	DWORD   dwLevel;
#ifdef ENABLE_ALIGNMENT_SYSTEM
	int		sAlignment;
#else
	short	sAlignment;
#endif
	BYTE    bPKMode;
	DWORD   dwMountVnum;
#ifdef ENABLE_SKILL_COLOR_SYSTEM
	DWORD	dwSkillColor[NRaceData::MAX_SKILL_COUNT + NRaceData::MAX_BUFF_COUNT][NRaceData::MAX_EFFECT_COUNT];
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	BYTE bLanguage;
#endif
} TPacketGCCharacterAdditionalInfo;

typedef struct packet_add_char
{
	BYTE		header;
	DWORD		dwVID;
	float		angle;
	long		x;
	long		y;
	long		z;
	BYTE		bType;
	WORD		wRaceNum;
	BYTE		bMovingSpeed;
	BYTE		bAttackSpeed;

	BYTE		bStateFlag;
	DWORD		dwAffectFlag[2];
} TPacketGCCharacterAdd;

typedef struct packet_update_char
{
	BYTE		header;
	DWORD		dwVID;
	DWORD		awPart[CHR_EQUIPPART_NUM];
#ifdef ENABLE_ITEMS_SHINING
	DWORD		adwShining[CHR_SHINING_NUM];
#endif
	BYTE		bMovingSpeed;
	BYTE		bAttackSpeed;

	BYTE		bStateFlag;
	DWORD		dwAffectFlag[2];

	DWORD		dwGuildID;
#ifdef ENABLE_ALIGNMENT_SYSTEM
	int			sAlignment;
#else
	short		sAlignment;
#endif
	BYTE		bPKMode;
	DWORD		dwMountVnum;
#ifdef ENABLE_NEW_PET_SYSTEM
	DWORD		dwLevel;
#endif
#ifdef ENABLE_SKILL_COLOR_SYSTEM
	DWORD		dwSkillColor[NRaceData::MAX_SKILL_COUNT + NRaceData::MAX_BUFF_COUNT][NRaceData::MAX_EFFECT_COUNT];
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	BYTE bLanguage;
#endif
} TPacketGCCharacterUpdate;

typedef struct packet_del_char
{
	BYTE	header;
	DWORD	dwVID;
} TPacketGCCharacterDelete;

typedef struct packet_GlobalTime
{
	BYTE	header;
	float	GlobalTime;
} TPacketGCGlobalTime;

enum EChatType
{
	CHAT_TYPE_TALKING,
	CHAT_TYPE_INFO,
	CHAT_TYPE_NOTICE,
	CHAT_TYPE_PARTY,
	CHAT_TYPE_GUILD,
	CHAT_TYPE_COMMAND,
	CHAT_TYPE_SHOUT,
	CHAT_TYPE_WHISPER,
	CHAT_TYPE_BIG_NOTICE,
#ifdef ENABLE_DICE_SYSTEM
	CHAT_TYPE_DICE_INFO, //11
#endif
#ifdef ENABLE_ZODIAC_TEMPLE_CHAT
	CHAT_TYPE_ZODIAC_NOTICE,
	CHAT_TYPE_ZODIAC_SUB_NOTICE,
	CHAT_TYPE_ZODIAC_NOTICE_CLEAR,
#endif
#ifdef ENABLE_DUNGEON_MODULES
	CHAT_TYPE_MISSION,
#endif
#ifdef ENABLE_DROP_INFO_WINDOW
	CHAT_TYPE_ITEM_INFO,
	CHAT_TYPE_MONEY_INFO,
#endif
	CHAT_TYPE_MAX_NUM,
};

typedef struct packet_chatting
{
	BYTE	header;
	WORD	size;
	BYTE	type;
	DWORD	dwVID;
	BYTE	bEmpire;
} TPacketGCChat;

typedef struct packet_whisper
{
	BYTE        bHeader;
	WORD        wSize;
	BYTE        bType;
	char        szNameFrom[CHARACTER_NAME_MAX_LEN + 1];
} TPacketGCWhisper;

typedef struct packet_stun
{
	BYTE		header;
	DWORD		vid;
} TPacketGCStun;

typedef struct packet_dead
{
	BYTE		header;
	DWORD		vid;
} TPacketGCDead;

typedef struct packet_main_character
{
	BYTE        header;
	DWORD       dwVID;
	WORD		wRaceNum;
	char        szName[CHARACTER_NAME_MAX_LEN + 1];
	long        lX, lY, lZ;
	BYTE		empire; /* @Lightwork5 */
	BYTE		bySkillGroup;
} TPacketGCMainCharacter;

// SUPPORT_BGM
typedef struct packet_main_character2_empire
{
	BYTE        header;
	DWORD       dwVID;
	WORD		wRaceNum;
	char        szName[CHARACTER_NAME_MAX_LEN + 1];
	long        lX, lY, lZ;
	BYTE		byEmpire;
	BYTE		bySkillGroup;
} TPacketGCMainCharacter2_EMPIRE;


enum EPointTypes
{
	POINT_NONE					= 0,
	POINT_LEVEL					= 1,
	POINT_VOICE					= 2,
	POINT_EXP					= 3,
	POINT_NEXT_EXP				= 4,
	POINT_HP					= 5,
	POINT_MAX_HP				= 6,
	POINT_SP					= 7,
	POINT_MAX_SP				= 8,
	POINT_STAMINA				= 9,
	POINT_MAX_STAMINA			= 10,
	POINT_GOLD					= 11,
	POINT_ST					= 12,
	POINT_HT					= 13,
	POINT_DX					= 14,
	POINT_IQ					= 15,
	POINT_ATT_POWER				= 16,
	POINT_ATT_SPEED				= 17,
	POINT_ATT_GRADE				= 18,
	POINT_MOV_SPEED				= 19,
	POINT_DEF_GRADE				= 20,
	POINT_CASTING_SPEED			= 21,
	POINT_MAGIC_ATT_GRADE		= 22,
	POINT_MAGIC_DEF_GRADE		= 23,
	POINT_EMPIRE_POINT			= 24,
	POINT_LEVEL_STEP			= 25,
	POINT_STAT					= 26,
	POINT_SUB_SKILL				= 27,
	POINT_SKILL					= 28,
	POINT_WEAPON_MIN			= 29,
	POINT_WEAPON_MAX			= 30,
	POINT_PLAYTIME				= 31,
	POINT_HP_REGEN				= 32,
	POINT_SP_REGEN				= 33,
	POINT_BOW_DISTANCE			= 34,
	POINT_HP_RECOVERY			= 35,
	POINT_SP_RECOVERY			= 36,
	POINT_POISON_PCT			= 37,
	POINT_STUN_PCT				= 38,
	POINT_SLOW_PCT				= 39,
	POINT_CRITICAL_PCT			= 40,
	POINT_PENETRATE_PCT			= 41,
	POINT_CURSE_PCT				= 42,
	POINT_ATTBONUS_HUMAN		= 43,
	POINT_ATTBONUS_ANIMAL		= 44,
	POINT_ATTBONUS_ORC			= 45,
	POINT_ATTBONUS_MILGYO		= 46,
	POINT_ATTBONUS_UNDEAD		= 47,
	POINT_ATTBONUS_DEVIL		= 48,
	POINT_ATTBONUS_INSECT		= 49,
	POINT_ATTBONUS_FIRE			= 50,
	POINT_ATTBONUS_ICE			= 51,
	POINT_ATTBONUS_DESERT		= 52,
	POINT_ATTBONUS_MONSTER		= 53,
	POINT_ATTBONUS_WARRIOR		= 54,
	POINT_ATTBONUS_ASSASSIN		= 55,
	POINT_ATTBONUS_SURA			= 56,
	POINT_ATTBONUS_SHAMAN		= 57,
	POINT_ATTBONUS_TREE			= 58,
	POINT_RESIST_WARRIOR		= 59,
	POINT_RESIST_ASSASSIN		= 60,
	POINT_RESIST_SURA			= 61,
	POINT_RESIST_SHAMAN			= 62,
	POINT_STEAL_HP				= 63,
	POINT_STEAL_SP				= 64,
	POINT_MANA_BURN_PCT			= 65,
	POINT_DAMAGE_SP_RECOVER		= 66,
	POINT_BLOCK					= 67,
	POINT_DODGE					= 68,
	POINT_RESIST_SWORD			= 69,
	POINT_RESIST_TWOHAND		= 70,
	POINT_RESIST_DAGGER			= 80,
	POINT_RESIST_BELL			= 81,
	POINT_RESIST_FAN			= 82,
	POINT_RESIST_BOW			= 83,
	POINT_RESIST_FIRE			= 84,
	POINT_RESIST_ELEC			= 85,
	POINT_RESIST_MAGIC			= 86,
	POINT_RESIST_WIND			= 87,
	POINT_REFLECT_MELEE			= 88,
	POINT_REFLECT_CURSE			= 89,
	POINT_POISON_REDUCE			= 90,
	POINT_KILL_SP_RECOVER		= 91,
	POINT_EXP_DOUBLE_BONUS		= 92,
	POINT_GOLD_DOUBLE_BONUS		= 93,
	POINT_ITEM_DROP_BONUS		= 94,
	POINT_POTION_BONUS			= 95,
	POINT_KILL_HP_RECOVERY		= 96,
	POINT_IMMUNE_STUN			= 97,
	POINT_IMMUNE_SLOW			= 98,
	POINT_IMMUNE_FALL			= 99,
	POINT_PARTY_ATTACKER_BONUS	= 100,
	POINT_PARTY_TANKER_BONUS	= 101,
	POINT_ATT_BONUS				= 102,
	POINT_DEF_BONUS				= 103,
	POINT_ATT_GRADE_BONUS		= 104,
	POINT_DEF_GRADE_BONUS		= 105,
	POINT_MAGIC_ATT_GRADE_BONUS	= 106,
	POINT_MAGIC_DEF_GRADE_BONUS	= 107,
	POINT_RESIST_NORMAL_DAMAGE	= 108,
	POINT_HIT_HP_RECOVERY		= 109,
	POINT_HIT_SP_RECOVERY		= 110,
	POINT_MANASHIELD			= 111,
	POINT_PARTY_BUFFER_BONUS	= 112,
	POINT_PARTY_SKILL_MASTER_BONUS = 113,
	POINT_HP_RECOVER_CONTINUE	= 114,
	POINT_SP_RECOVER_CONTINUE	= 115,
	POINT_STEAL_GOLD			= 116,
	POINT_POLYMORPH				= 117,
	POINT_MOUNT					= 118,
	POINT_PARTY_HASTE_BONUS		= 119,
	POINT_PARTY_DEFENDER_BONUS	= 120,
	POINT_STAT_RESET_COUNT		= 121,
	POINT_HORSE_SKILL			= 122,
	POINT_MALL_ATTBONUS			= 123,
	POINT_MALL_DEFBONUS			= 124,
	POINT_MALL_EXPBONUS			= 125,
	POINT_MALL_ITEMBONUS		= 126,
	POINT_MALL_GOLDBONUS		= 127,
	POINT_MAX_HP_PCT			= 128,
	POINT_MAX_SP_PCT			= 129,
	POINT_SKILL_DAMAGE_BONUS	= 130,
	POINT_NORMAL_HIT_DAMAGE_BONUS = 131,
	POINT_SKILL_DEFEND_BONUS	= 132,
	POINT_NORMAL_HIT_DEFEND_BONUS = 133,
	POINT_RAMADAN_CANDY_BONUS_EXP = 134,
	POINT_ENERGY				= 135,
	POINT_ENERGY_END_TIME		= 136,
	POINT_COSTUME_ATTR_BONUS	= 137,
	POINT_MAGIC_ATT_BONUS_PER	= 138,
	POINT_MELEE_MAGIC_ATT_BONUS_PER = 139,
	POINT_RESIST_ICE			= 140,
	POINT_RESIST_EARTH			= 141,
	POINT_RESIST_DARK			= 142,
	POINT_RESIST_CRITICAL		= 143,
	POINT_RESIST_PENETRATE		= 144,

#ifdef ENABLE_WOLFMAN_CHARACTER
	POINT_BLEEDING_REDUCE		= 145,
	POINT_BLEEDING_PCT			= 146,
	POINT_ATTBONUS_WOLFMAN		= 147,
	POINT_RESIST_WOLFMAN		= 148,
	POINT_RESIST_CLAW			= 149,
#endif
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	POINT_ACCEDRAIN_RATE		= 150,
#endif
#ifdef ENABLE_MAGIC_REDUCTION_SYSTEM
	POINT_RESIST_MAGIC_REDUCTION = 151,
#endif
#ifdef ENABLE_EXTRA_APPLY_BONUS
	POINT_ATTBONUS_STONE		= 152,
	POINT_ATTBONUS_BOSS			= 153,
	POINT_ATTBONUS_PVM_STR		= 154,
	POINT_ATTBONUS_PVM_AVG		= 155,
	POINT_ATTBONUS_PVM_BERSERKER= 156,
	POINT_ATTBONUS_ELEMENT		= 157,
	POINT_DEFBONUS_PVM			= 158,
	POINT_DEFBONUS_ELEMENT		= 159,
	POINT_ATTBONUS_PVP			= 160,
	POINT_DEFBONUS_PVP			= 161,

	POINT_ATT_FIRE				= 162,
	POINT_ATT_ICE				= 163,
	POINT_ATT_WIND				= 164,
	POINT_ATT_EARTH				= 165,
	POINT_ATT_DARK				= 166,
	POINT_ATT_ELEC				= 167,
#endif
	POINT_REFRESH_MAX,

#ifdef ENABLE_EXTENDED_BATTLE_PASS
	POINT_BATTLE_PASS_PREMIUM_ID,
#endif
#ifdef ENABLE_PLAYER_STATS_SYSTEM
#ifdef ENABLE_POWER_RANKING
	POINT_POWER_RANK,
#endif

	POINT_MONSTER_KILLED,
	POINT_STONE_KILLED,
	POINT_BOSS_KILLED,
	POINT_PLAYER_KILLED,

	POINT_MONSTER_DAMAGE,
	POINT_STONE_DAMAGE,
	POINT_BOSS_DAMAGE,
	POINT_PLAYER_DAMAGE,

	POINT_OPENED_CHEST,
	POINT_FISHING,
	POINT_MINING,
	POINT_COMPLATE_DUNGEON,
	POINT_UPGRADE_ITEM,
	POINT_USE_ENCHANTED_ITEM,
#endif

	//SONDA KALICAK HERZAMAN
	POINT_MIN_WEP,
	POINT_MAX_WEP,
	POINT_MIN_MAGIC_WEP,
	POINT_MAX_MAGIC_WEP,
	POINT_HIT_RATE,
};

typedef struct packet_points
{
	BYTE		header;
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t		points[POINT_MAX_NUM];
#else
	long		points[POINT_MAX_NUM];
#endif
} TPacketGCPoints;

typedef struct packet_point_change
{
	int			header;
	DWORD		dwVID;
	BYTE		Type;
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t		amount;
	int64_t		value;
#else
	long		amount;
	long		value;
#endif
} TPacketGCPointChange;

typedef struct packet_motion
{
	BYTE		header;
	DWORD		vid;
	DWORD		victim_vid;
	WORD		motion;
} TPacketGCMotion;

typedef struct packet_set_item
{
	BYTE		header;
	TItemPos	Cell;
	DWORD		vnum;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	count;
#else
	BYTE		count;
#endif
	long		alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
} TPacketGCItemSet;

typedef struct packet_set_item2
{
	BYTE		header;
	TItemPos	Cell;
	DWORD		vnum;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	count;
#else
	BYTE		count;
#endif
	DWORD		flags;
	DWORD		anti_flags;
	bool		highlight;
	long		alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
} TPacketGCItemSet2;

typedef struct packet_item_del
{
	BYTE        header;
	BYTE        pos;
} TPacketGCItemDel;

typedef struct packet_use_item
{
	BYTE		header;
	TItemPos	Cell;
	DWORD		ch_vid;
	DWORD		victim_vid;

	DWORD		vnum;
} TPacketGCItemUse;

typedef struct packet_update_item
{
	BYTE		header;
	TItemPos	Cell;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	count;
#else
	BYTE		count;
#endif
	long		alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
} TPacketGCItemUpdate;

typedef struct packet_ground_add_item
{
#ifdef ENABLE_EXTENDED_ITEMNAME_ON_GROUND
	packet_ground_add_item()
	{
		memset(&alSockets, 0, sizeof(alSockets));
		memset(&aAttrs, 0, sizeof(aAttrs));
	}
#endif
	BYTE        bHeader;
	long        lX;
	long		lY;
	long		lZ;

	DWORD       dwVID;
	DWORD       dwVnum;
#ifdef ENABLE_EXTENDED_ITEMNAME_ON_GROUND
	long		alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttrs[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
#endif
} TPacketGCItemGroundAdd;

typedef struct packet_ground_del_item
{
	BYTE		header;
	DWORD		vid;
} TPacketGCItemGroundDel;

typedef struct packet_item_ownership
{
	BYTE        bHeader;
	DWORD       dwVID;
	char        szName[CHARACTER_NAME_MAX_LEN + 1];
} TPacketGCItemOwnership;

typedef struct packet_quickslot_add
{
	BYTE        header;
	QS_USHORT   pos;
	TQuickSlot	slot;
} TPacketGCQuickSlotAdd;

typedef struct packet_quickslot_del
{
	BYTE        header;
	QS_USHORT        pos;
} TPacketGCQuickSlotDel;

typedef struct packet_quickslot_swap
{
	BYTE        header;
	QS_USHORT        pos;
	QS_USHORT        change_pos;
} TPacketGCQuickSlotSwap;

typedef struct packet_shop_start
{
	struct packet_shop_item		items[SHOP_HOST_ITEM_MAX_NUM];
} TPacketGCShopStart;

typedef struct packet_shop_start_ex
{
	typedef struct sub_packet_shop_tab
	{
		char name[SHOP_TAB_NAME_MAX];
		BYTE coin_type;
		packet_shop_item items[SHOP_HOST_ITEM_MAX_NUM];
	} TSubPacketShopTab;
	DWORD owner_vid;
	BYTE shop_tab_count;
} TPacketGCShopStartEx;

typedef struct packet_shop_update_item
{
	BYTE						pos;
	struct packet_shop_item		item;
} TPacketGCShopUpdateItem;

typedef struct packet_shop_update_price
{
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t	iElkAmount;
#else
	int		iElkAmount;
#endif
} TPacketGCShopUpdatePrice;

enum EPacketShopSubHeaders
{
	SHOP_SUBHEADER_GC_START,
	SHOP_SUBHEADER_GC_END,
	SHOP_SUBHEADER_GC_UPDATE_ITEM,
	SHOP_SUBHEADER_GC_UPDATE_PRICE,
	SHOP_SUBHEADER_GC_OK,
	SHOP_SUBHEADER_GC_NOT_ENOUGH_MONEY,
#ifdef ENABLE_BUY_WITH_ITEMS
	SHOP_SUBHEADER_GC_NOT_ENOUGH_ITEM,
#endif
	SHOP_SUBHEADER_GC_SOLDOUT,
	SHOP_SUBHEADER_GC_INVENTORY_FULL,
	SHOP_SUBHEADER_GC_INVALID_POS,
	SHOP_SUBHEADER_GC_SOLD_OUT,
	SHOP_SUBHEADER_GC_START_EX,
	SHOP_SUBHEADER_GC_NOT_ENOUGH_MONEY_EX,
};

typedef struct packet_shop
{
	BYTE		header;
	WORD		size;
	BYTE		subheader;
} TPacketGCShop;

typedef struct packet_exchange
{
	BYTE		header;
	BYTE		subheader;
	BYTE		is_me;
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t		arg1;
#else
	DWORD		arg1;
#endif
	TItemPos	arg2;
	DWORD		arg3;
#ifdef WJ_ENABLE_TRADABLE_ICON
	TItemPos	arg4;
#endif
	long		alValues[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
} TPacketGCExchange;

enum
{
	EXCHANGE_SUBHEADER_GC_START,			// arg1 == vid
	EXCHANGE_SUBHEADER_GC_ITEM_ADD,		// arg1 == vnum  arg2 == pos  arg3 == count
	EXCHANGE_SUBHEADER_GC_ITEM_DEL,		// arg1 == pos
	EXCHANGE_SUBHEADER_GC_ELK_ADD,			// arg1 == elk
	EXCHANGE_SUBHEADER_GC_ACCEPT,			// arg1 == accept
	EXCHANGE_SUBHEADER_GC_END,				// arg1 == not used
	EXCHANGE_SUBHEADER_GC_ALREADY,			// arg1 == not used
	EXCHANGE_SUBHEADER_GC_LESS_ELK,		// arg1 == not used
};

typedef struct packet_position
{
	BYTE        header;
	DWORD		vid;
	BYTE        position;
} TPacketGCPosition;

typedef struct packet_ping
{
	BYTE		header;
} TPacketGCPing;

typedef struct packet_pong
{
	BYTE		bHeader;
} TPacketCGPong;

typedef struct packet_script
{
	BYTE		header;
	WORD        size;
	BYTE		skin;
	WORD        src_size;
} TPacketGCScript;

typedef struct packet_target
{
	BYTE        header;
	DWORD       dwVID;
	BYTE        bHPPercent;
#ifdef ENABLE_SHOW_TARGET_HP
	int64_t		hpTarget;
#endif
#ifdef ENABLE_ELEMENT_ADD
	BYTE bElement;
#endif
} TPacketGCTarget;

typedef struct packet_damage_info
{
	BYTE header;
	DWORD dwVID;
	BYTE flag;
	DAM_LL  damage;
} TPacketGCDamageInfo;

typedef struct packet_mount
{
	BYTE        header;
	DWORD       vid;
	DWORD       mount_vid;
	BYTE        pos;
	DWORD		_x, _y;
} TPacketGCMount;

typedef struct packet_change_speed
{
	BYTE		header;
	DWORD		vid;
	WORD		moving_speed;
} TPacketGCChangeSpeed;

typedef struct packet_move
{
	BYTE		bHeader;
	BYTE		bFunc;
	BYTE		bArg;
	BYTE		bRot;
	DWORD		dwVID;
	LONG		lX;
	LONG		lY;
	DWORD		dwTime;
	DWORD		dwDuration;
} TPacketGCMove;

enum
{
	QUEST_SEND_IS_BEGIN = 1 << 0,
	QUEST_SEND_TITLE = 1 << 1,
	QUEST_SEND_CLOCK_NAME = 1 << 2,
	QUEST_SEND_CLOCK_VALUE = 1 << 3,
	QUEST_SEND_COUNTER_NAME = 1 << 4,
	QUEST_SEND_COUNTER_VALUE = 1 << 5,
	QUEST_SEND_ICON_FILE = 1 << 6,
};

typedef struct packet_quest_info
{
	BYTE header;
	WORD size;
	WORD index;
#ifdef ENABLE_QUEST_CATEGORY
	WORD c_index;
#endif
	BYTE flag;
} TPacketGCQuestInfo;

typedef struct packet_quest_confirm
{
	BYTE header;
	char msg[64 + 1];
	long timeout;
	DWORD requestPID;
} TPacketGCQuestConfirm;

typedef struct packet_attack
{
	BYTE        header;
	DWORD       dwVID;
	DWORD       dwVictimVID;
	BYTE        bType;
} TPacketGCAttack;

typedef struct packet_c2c
{
	BYTE		header;
	WORD		wSize;
} TPacketGCC2C;

typedef struct packetd_sync_position_element
{
	DWORD       dwVID;
	long        lX;
	long        lY;
} TPacketGCSyncPositionElement;

typedef struct packetd_sync_position
{
	BYTE        bHeader;
	WORD		wSize;
} TPacketGCSyncPosition;

typedef struct packet_ownership
{
	BYTE                bHeader;
	DWORD               dwOwnerVID;
	DWORD               dwVictimVID;
} TPacketGCOwnership;

#define	SKILL_MAX_NUM 255

typedef struct packet_skill_level
{
	BYTE        bHeader;
	BYTE        abSkillLevels[SKILL_MAX_NUM];
} TPacketGCSkillLevel;

typedef struct SPlayerSkill
{
	BYTE bMasterType;
	BYTE bLevel;
} TPlayerSkill;

typedef struct packet_skill_level_new
{
	BYTE bHeader;
	TPlayerSkill skills[SKILL_MAX_NUM];
} TPacketGCSkillLevelNew;

// fly
typedef struct packet_fly
{
	BYTE        bHeader;
	BYTE        bType;
	DWORD       dwStartVID;
	DWORD       dwEndVID;
} TPacketGCCreateFly;

enum EPVPModes
{
	PVP_MODE_NONE,
	PVP_MODE_AGREE,
	PVP_MODE_FIGHT,
	PVP_MODE_REVENGE,
};

typedef struct packet_duel_start
{
	BYTE	header;
	WORD	wSize;
} TPacketGCDuelStart;

typedef struct packet_pvp
{
	BYTE		header;
	DWORD		dwVIDSrc;
	DWORD		dwVIDDst;
	BYTE		bMode;
} TPacketGCPVP;

typedef struct packet_warp
{
	BYTE			bHeader;
	LONG			lX;
	LONG			lY;
	LONG			lAddr;
	WORD			wPort;
} TPacketGCWarp;

typedef struct packet_party_invite
{
	BYTE header;
	DWORD leader_pid;
} TPacketGCPartyInvite;

typedef struct packet_party_add
{
	BYTE header;
	DWORD pid;
	char name[CHARACTER_NAME_MAX_LEN + 1];
} TPacketGCPartyAdd;

typedef struct packet_party_update
{
	BYTE header;
	DWORD pid;
	BYTE state;
	BYTE percent_hp;
	short affects[PARTY_AFFECT_SLOT_MAX_NUM];
} TPacketGCPartyUpdate;

typedef struct packet_party_remove
{
	BYTE header;
	DWORD pid;
} TPacketGCPartyRemove;

typedef TPacketCGSafeboxCheckout TPacketGCSafeboxCheckout;
typedef TPacketCGSafeboxCheckin TPacketGCSafeboxCheckin;

typedef struct packet_safebox_wrong_password
{
	BYTE        bHeader;
} TPacketGCSafeboxWrongPassword;

typedef struct packet_safebox_size
{
	BYTE bHeader;
	BYTE bSize;
} TPacketGCSafeboxSize;

typedef struct command_empire
{
	BYTE        bHeader;
	BYTE        bEmpire;
} TPacketCGEmpire;

typedef struct packet_empire
{
	BYTE        bHeader;
	BYTE        bEmpire;
} TPacketGCEmpire;

enum
{
	FISHING_SUBHEADER_GC_START,
	FISHING_SUBHEADER_GC_STOP,
	FISHING_SUBHEADER_GC_REACT,
	FISHING_SUBHEADER_GC_SUCCESS,
	FISHING_SUBHEADER_GC_FAIL,
	FISHING_SUBHEADER_GC_FISH,
};

typedef struct packet_fishing
{
	BYTE header;
	BYTE subheader;
	DWORD info;
	BYTE dir;
} TPacketGCFishing;

typedef struct paryt_parameter
{
	BYTE        bHeader;
	BYTE        bDistributeMode;
} TPacketGCPartyParameter;

//////////////////////////////////////////////////////////////////////////
// Guild

enum
{
	GUILD_SUBHEADER_GC_LOGIN,
	GUILD_SUBHEADER_GC_LOGOUT,
	GUILD_SUBHEADER_GC_LIST,
	GUILD_SUBHEADER_GC_GRADE,
	GUILD_SUBHEADER_GC_ADD,
	GUILD_SUBHEADER_GC_REMOVE,
	GUILD_SUBHEADER_GC_GRADE_NAME,
	GUILD_SUBHEADER_GC_GRADE_AUTH,
	GUILD_SUBHEADER_GC_INFO,
	GUILD_SUBHEADER_GC_COMMENTS,
	GUILD_SUBHEADER_GC_CHANGE_EXP,
	GUILD_SUBHEADER_GC_CHANGE_MEMBER_GRADE,
	GUILD_SUBHEADER_GC_SKILL_INFO,
	GUILD_SUBHEADER_GC_CHANGE_MEMBER_GENERAL,
	GUILD_SUBHEADER_GC_GUILD_INVITE,
	GUILD_SUBHEADER_GC_WAR,
	GUILD_SUBHEADER_GC_GUILD_NAME,
	GUILD_SUBHEADER_GC_GUILD_WAR_LIST,
	GUILD_SUBHEADER_GC_GUILD_WAR_END_LIST,
	GUILD_SUBHEADER_GC_WAR_POINT,
	GUILD_SUBHEADER_GC_MONEY_CHANGE,
};

typedef struct packet_guild
{
	BYTE header;
	WORD size;
	BYTE subheader;
} TPacketGCGuild;

// SubHeader - Grade
enum
{
	GUILD_AUTH_ADD_MEMBER = (1 << 0),
	GUILD_AUTH_REMOVE_MEMBER = (1 << 1),
	GUILD_AUTH_NOTICE = (1 << 2),
	GUILD_AUTH_SKILL = (1 << 3),
};

typedef struct packet_guild_sub_grade
{
	char grade_name[GUILD_GRADE_NAME_MAX_LEN + 1];
	BYTE auth_flag;
} TPacketGCGuildSubGrade;

typedef struct packet_guild_sub_member
{
	DWORD pid;
	BYTE byGrade;
	BYTE byIsGeneral;
	BYTE byJob;
	BYTE byLevel;
	DWORD dwOffer;
	BYTE byNameFlag;
} TPacketGCGuildSubMember;

typedef struct packet_guild_sub_info
{
	WORD member_count;
	WORD max_member_count;
	DWORD guild_id;
	DWORD master_pid;
	DWORD exp;
	BYTE level;
	char name[GUILD_NAME_MAX_LEN + 1];
	DWORD gold;
	BYTE hasLand;
} TPacketGCGuildInfo;

enum EGuildWarState
{
	GUILD_WAR_NONE,
	GUILD_WAR_SEND_DECLARE,
	GUILD_WAR_REFUSE,
	GUILD_WAR_RECV_DECLARE,
	GUILD_WAR_WAIT_START,
	GUILD_WAR_CANCEL,
	GUILD_WAR_ON_WAR,
	GUILD_WAR_END,

	GUILD_WAR_DURATION = 2 * 60 * 60,
};

typedef struct packet_guild_war
{
	DWORD       dwGuildSelf;
	DWORD       dwGuildOpp;
	BYTE        bType;
	BYTE        bWarState;
} TPacketGCGuildWar;

typedef struct SPacketGuildWarPoint
{
	DWORD dwGainGuildID;
	DWORD dwOpponentGuildID;
	long lPoint;
} TPacketGuildWarPoint;

// SubHeader - Dungeon
enum
{
	DUNGEON_SUBHEADER_GC_TIME_ATTACK_START = 0,
	DUNGEON_SUBHEADER_GC_DESTINATION_POSITION = 1,
};

typedef struct packet_dungeon
{
	BYTE		bHeader;
	WORD		size;
	BYTE		subheader;
} TPacketGCDungeon;

// Private Shop
typedef struct SPacketGCShopSign
{
	BYTE        bHeader;
	DWORD       dwVID;
	char        szSign[SHOP_SIGN_MAX_LEN + 1];
} TPacketGCShopSign;

typedef struct SPacketGCTime
{
	BYTE        bHeader;
	time_t      time;
} TPacketGCTime;

enum
{
	WALKMODE_RUN,
	WALKMODE_WALK,
};

typedef struct SPacketGCWalkMode
{
	BYTE        header;
	DWORD       vid;
	BYTE        mode;
} TPacketGCWalkMode;

typedef struct SPacketGCChangeSkillGroup
{
	BYTE        header;
	BYTE        skill_group;
} TPacketGCChangeSkillGroup;

struct TMaterial
{
	DWORD vnum;
	DWORD count;
};

typedef struct SRefineTable
{
	DWORD src_vnum;
	DWORD result_vnum;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT material_count;
#else
	BYTE material_count;
#endif
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t cost;
#else
	int cost;
#endif
	int prob;
	TMaterial materials[REFINE_MATERIAL_MAX_NUM];
} TRefineTable;

typedef struct SPacketGCRefineInformation
{
	BYTE			header;
	BYTE			pos;
	TRefineTable	refine_table;
} TPacketGCRefineInformation;

typedef struct SPacketGCRefineInformationNew
{
	BYTE			header;
	BYTE			type;
	BYTE			pos;
	TRefineTable	refine_table;
} TPacketGCRefineInformationNew;

enum SPECIAL_EFFECT
{
	SE_NONE,
	SE_HPUP_RED,
	SE_SPUP_BLUE,
	SE_SPEEDUP_GREEN,
	SE_DXUP_PURPLE,
	SE_CRITICAL,
	SE_PENETRATE,
	SE_BLOCK,
	SE_DODGE,
	SE_CHINA_FIREWORK,
	SE_SPIN_TOP,
	SE_SUCCESS,
	SE_FAIL,
	SE_FR_SUCCESS,
	SE_LEVELUP_ON_14_FOR_GERMANY,
	SE_LEVELUP_UNDER_15_FOR_GERMANY,
	SE_PERCENT_DAMAGE1,
	SE_PERCENT_DAMAGE2,
	SE_PERCENT_DAMAGE3,
	SE_AUTO_HPUP,
	SE_AUTO_SPUP,
	SE_EQUIP_RAMADAN_RING,
	SE_EQUIP_HALLOWEEN_CANDY,
	SE_EQUIP_HAPPINESS_RING,
	SE_EQUIP_LOVE_PENDANT,
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	SE_EFFECT_ACCE_SUCCEDED,
	SE_EFFECT_ACCE_EQUIP,
#endif
#ifdef ENABLE_EXTENDED_BATTLE_PASS
	SE_EFFECT_BP_NORMAL_MISSION_COMPLETED,
	SE_EFFECT_BP_PREMIUM_MISSION_COMPLETED,
	SE_EFFECT_BP_EVENT_MISSION_COMPLETED,
	SE_EFFECT_BP_NORMAL_BATTLEPASS_COMPLETED,
	SE_EFFECT_BP_PREMIUM_BATTLEPASS_COMPLETED,
	SE_EFFECT_BP_EVENT_BATTLEPASS_COMPLETED,
#endif
};

typedef struct SPacketGCSpecialEffect
{
	BYTE header;
	BYTE type;
	DWORD vid;
} TPacketGCSpecialEffect;

typedef struct SPacketGCNPCPosition
{
	BYTE header;
	WORD size;
	WORD count;
} TPacketGCNPCPosition;

struct TNPCPosition
{
	BYTE bType;
	char name[CHARACTER_NAME_MAX_LEN + 1];
	long x;
	long y;
};

typedef struct SPacketGCChangeName
{
	BYTE header;
	DWORD pid;
	char name[CHARACTER_NAME_MAX_LEN + 1];
} TPacketGCChangeName;

enum EBlockAction
{
	BLOCK_EXCHANGE = (1 << 0),
	BLOCK_PARTY_INVITE = (1 << 1),
	BLOCK_GUILD_INVITE = (1 << 2),
	BLOCK_WHISPER = (1 << 3),
	BLOCK_MESSENGER_INVITE = (1 << 4),
	BLOCK_PARTY_REQUEST = (1 << 5),
#ifdef ENABLE_TELEPORT_TO_A_FRIEND
    BLOCK_WARP_REQUEST		= (1 << 6),
#endif
};

typedef struct packet_login_key
{
	BYTE	bHeader;
	DWORD	dwLoginKey;
} TPacketGCLoginKey;

typedef struct packet_auth_success
{
	BYTE        bHeader;
	DWORD       dwLoginKey;
	BYTE        bResult;
} TPacketGCAuthSuccess;

typedef struct packet_channel
{
	BYTE header;
	BYTE channel;
} TPacketGCChannel;

typedef struct SEquipmentItemSet
{
	DWORD   vnum;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	count;
#else
	BYTE	count;
#endif
	long    alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
} TEquipmentItemSet;

typedef struct pakcet_view_equip
{
	BYTE header;
	DWORD dwVID;
	TEquipmentItemSet equips[WEAR_MAX_NUM];
} TPacketGCViewEquip;

typedef struct
{
	DWORD       dwID;
	long        x, y;
	long        width, height;
	DWORD       dwGuildID;
} TLandPacketElement;

typedef struct packet_land_list
{
	BYTE        header;
	WORD        size;
} TPacketGCLandList;

typedef struct
{
	BYTE        bHeader;
	long        lID;
	char        szTargetName[32 + 1];
} TPacketGCTargetCreate;

enum eTargetTypes
{
	CREATE_TARGET_TYPE_NONE,
	CREATE_TARGET_TYPE_LOCATION,
	CREATE_TARGET_TYPE_CHARACTER,
};

typedef struct
{
	BYTE		bHeader;
	long		lID;
	char		szTargetName[32 + 1];
	DWORD		dwVID;
	BYTE		byType;
} TPacketGCTargetCreateNew;

typedef struct
{
	BYTE        bHeader;
	long        lID;
	long        lX, lY;
} TPacketGCTargetUpdate;

typedef struct
{
	BYTE        bHeader;
	long        lID;
} TPacketGCTargetDelete;

typedef struct SPacketAffectElement
{
	DWORD       dwType;
	BYTE        bPointIdxApplyOn;
	long        lApplyValue;
	DWORD       dwFlag;
	long        lDuration;
	long        lSPCost;
} TPacketAffectElement;

typedef struct
{
	BYTE bHeader;
	TPacketAffectElement elem;
} TPacketGCAffectAdd;

typedef struct SPacketGCAffectRemove
{
	BYTE bHeader;
	DWORD dwType;
	BYTE bApplyOn;
} TPacketGCAffectRemove;

typedef struct packet_mall_open
{
	BYTE bHeader;
	BYTE bSize;
} TPacketGCMallOpen;

typedef struct packet_lover_info
{
	BYTE bHeader;
	char szName[CHARACTER_NAME_MAX_LEN + 1];
	BYTE byLovePoint;
} TPacketGCLoverInfo;

typedef struct packet_love_point_update
{
	BYTE bHeader;
	BYTE byLovePoint;
} TPacketGCLovePointUpdate;

typedef struct packet_dig_motion
{
	BYTE header;
	DWORD vid;
	DWORD target_vid;
	BYTE count;
} TPacketGCDigMotion;

typedef struct SPacketGCOnTime
{
	BYTE header;
	int ontime;     // sec
} TPacketGCOnTime;

typedef struct SPacketGCResetOnTime
{
	BYTE header;
} TPacketGCResetOnTime;

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Client To Client

typedef struct packet_state
{
	BYTE			bHeader;
	BYTE			bFunc;
	BYTE			bArg;
	BYTE			bRot;
	DWORD			dwVID;
	DWORD			dwTime;
	TPixelPosition	kPPos;
} TPacketCCState;

#ifdef _IMPROVED_PACKET_ENCRYPTION_
struct TPacketKeyAgreement
{
	static const int MAX_DATA_LEN = 256;
	BYTE bHeader;
	WORD wAgreedLength;
	WORD wDataLength;
	BYTE data[MAX_DATA_LEN];
};

struct TPacketKeyAgreementCompleted
{
	BYTE bHeader;
	BYTE data[3]; // dummy (not used)
};
#endif // _IMPROVED_PACKET_ENCRYPTION_

typedef struct SPacketGCSpecificEffect
{
	BYTE header;
	DWORD vid;
	char effect_file[128];
} TPacketGCSpecificEffect;

typedef struct SPacketGCSpecificEffect2
{
	BYTE header;
	DWORD vid;
	BYTE type;
} TPacketGCSpecificEffect2;

enum EDragonSoulRefineWindowRefineType
{
	DragonSoulRefineWindow_UPGRADE,
	DragonSoulRefineWindow_IMPROVEMENT,
	DragonSoulRefineWindow_REFINE,
};

enum EPacketCGDragonSoulSubHeaderType
{
	DS_SUB_HEADER_OPEN,
	DS_SUB_HEADER_CLOSE,
	DS_SUB_HEADER_DO_UPGRADE,
	DS_SUB_HEADER_DO_IMPROVEMENT,
	DS_SUB_HEADER_DO_REFINE,
	DS_SUB_HEADER_REFINE_FAIL,
	DS_SUB_HEADER_REFINE_FAIL_MAX_REFINE,
	DS_SUB_HEADER_REFINE_FAIL_INVALID_MATERIAL,
	DS_SUB_HEADER_REFINE_FAIL_NOT_ENOUGH_MONEY,
	DS_SUB_HEADER_REFINE_FAIL_NOT_ENOUGH_MATERIAL,
	DS_SUB_HEADER_REFINE_FAIL_TOO_MUCH_MATERIAL,
	DS_SUB_HEADER_REFINE_SUCCEED,
};

typedef struct SPacketCGDragonSoulRefine
{
	SPacketCGDragonSoulRefine() : header(HEADER_CG_DRAGON_SOUL_REFINE), bSubType(0) /*@M2Fixme001*/
	{}
	BYTE header;
	BYTE bSubType;
	TItemPos ItemGrid[DS_REFINE_WINDOW_MAX_NUM];
} TPacketCGDragonSoulRefine;

typedef struct SPacketGCDragonSoulRefine
{
	SPacketGCDragonSoulRefine() : header(HEADER_GC_DRAGON_SOUL_REFINE), bSubType(0) /*@M2Fixme001*/
	{}
	BYTE header;
	BYTE bSubType;
	TItemPos Pos;
} TPacketGCDragonSoulRefine;

typedef struct SChannelStatus
{
	WORD nPort; // @fixme024 (max port limit 32767 to 65535)
	BYTE bStatus;
} TChannelStatus;

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
enum EAcceInfo
{
	ACCE_ABSORPTION_SOCKET = 0,
	ACCE_ABSORBED_SOCKET = 1,
	ACCE_CLEAN_ATTR_VALUE0 = 7,
	ACCE_WINDOW_MAX_MATERIALS = 2,
	ACCE_REVERSAL_VNUM_1 = 39046,
	ACCE_REVERSAL_VNUM_2 = 90000,
};

enum
{
	HEADER_CG_ACCE = 211,
	HEADER_GC_ACCE = 215,
	ACCE_SUBHEADER_GC_OPEN = 0,
	ACCE_SUBHEADER_GC_CLOSE,
	ACCE_SUBHEADER_GC_ADDED,
	ACCE_SUBHEADER_GC_REMOVED,
	ACCE_SUBHEADER_CG_REFINED,
	ACCE_SUBHEADER_CG_CLOSE = 0,
	ACCE_SUBHEADER_CG_ADD,
	ACCE_SUBHEADER_CG_REMOVE,
	ACCE_SUBHEADER_CG_REFINE,
};

typedef struct SPacketAcce
{
	BYTE	header;
	BYTE	subheader;
	bool	bWindow;
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t	dwPrice;
#else
	DWORD	dwPrice;
#endif
	BYTE	bPos;
	TItemPos	tPos;
	DWORD	dwItemVnum;
	DWORD	dwMinAbs;
	DWORD	dwMaxAbs;
} TPacketAcce;

typedef struct SAcceMaterial
{
	BYTE	bHere;
	WORD	wCell;
} TAcceMaterial;

typedef struct SAcceResult
{
	DWORD	dwItemVnum;
	DWORD	dwMinAbs;
	DWORD	dwMaxAbs;
} TAcceResult;
#endif

#ifdef ENABLE_TARGET_INFORMATION_SYSTEM
typedef struct packet_target_info
{
	BYTE	header;
	DWORD	dwVID;
	DWORD	race;
	DWORD	dwVnum;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	count;
#else
	BYTE	count;
#endif
} TPacketGCTargetInfo;
typedef struct packet_target_info_load
{
	BYTE header;
	DWORD dwVID;
} TPacketCGTargetInfoLoad;
#endif

#ifdef ENABLE_CUBE_RENEWAL_WORLDARD
enum
{
	CUBE_RENEWAL_SUB_HEADER_OPEN_RECEIVE,
	CUBE_RENEWAL_SUB_HEADER_CLEAR_DATES_RECEIVE,
	CUBE_RENEWAL_SUB_HEADER_DATES_RECEIVE,
	CUBE_RENEWAL_SUB_HEADER_DATES_LOADING,
	CUBE_RENEWAL_SUB_HEADER_MAKE_ITEM,
	CUBE_RENEWAL_SUB_HEADER_CLOSE,
};

typedef struct  packet_send_cube_renewal
{
	BYTE header;
	BYTE subheader;
	DWORD index_item;
	DWORD count_item;
}TPacketCGCubeRenewalSend;

typedef struct dates_cube_renewal
{
	DWORD npc_vnum;
	DWORD index;

	DWORD	vnum_reward;
	int		count_reward;

	bool 	item_reward_stackable;

	DWORD	vnum_material_1;
	int		count_material_1;

	DWORD	vnum_material_2;
	int		count_material_2;

	DWORD	vnum_material_3;
	int		count_material_3;

	DWORD	vnum_material_4;
	int		count_material_4;

	DWORD	vnum_material_5;
	int		count_material_5;

	DWORD	vnum_material_6;
	int		count_material_6;

	DWORD	vnum_material_7;
	int		count_material_7;

	DWORD	vnum_material_8;
	int		count_material_8;

	DWORD	vnum_material_9;
	int		count_material_9;

	DWORD	vnum_material_10;
	int		count_material_10;

	long long 	gold;
	int 	percent;

	char 	category[100];
}TInfoDateCubeRenewal;

typedef struct packet_receive_cube_renewal
{
	packet_receive_cube_renewal() : header(HEADER_GC_CUBE_RENEWAL)
	{}

	BYTE header;
	BYTE subheader;
	TInfoDateCubeRenewal	date_cube_renewal;
}TPacketGCCubeRenewalReceive;
#endif

#ifdef ENABLE_DS_SET_BONUS
typedef struct STPacketDSTable {
	BYTE	bHeader;
	int		iType, iApplyCount, iBasicApplyValue[255], iAditionalApplyValue[255];
	float	fWeight;
} TPacketDSTable;
#endif

#ifdef ENABLE_OFFLINE_SHOP
typedef struct SPacketGCNewOfflineshop
{
	BYTE bHeader;
#ifdef ENABLE_LARGE_DYNAMIC_PACKET
	int wSize;
#else
	WORD wSize;
#endif
	BYTE bSubHeader;
} TPacketGCNewOfflineshop;

typedef struct SPacketCGNewOfflineShop
{
	BYTE bHeader;
	WORD wSize;
	BYTE bSubHeader;
} TPacketCGNewOfflineShop;

namespace offlineshop
{
	enum class ExpirationType
	{
		EXPIRE_NONE,
		EXPIRE_REAL_TIME,
		EXPIRE_REAL_TIME_FIRST_USE,
	};

	typedef struct SPriceInfo
	{
		long long illYang;
		SPriceInfo() : illYang(0)
		{}
	} TPriceInfo;

#ifdef ENABLE_OFFLINE_SHOP_GRID
	typedef struct SItemDisplayPos
	{
		BYTE pos;
		BYTE page;
	}TItemDisplayPos;
#endif

	typedef struct SItemInfoEx
	{
		DWORD dwVnum;
		DWORD dwCount;
		long alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
		TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
#ifdef ENABLE_CHANGELOOK_SYSTEM
		DWORD dwTransmutation;
#endif
		ExpirationType expiration;
#ifdef ENABLE_OFFLINE_SHOP_GRID
		TItemDisplayPos display_pos;
#endif
	} TItemInfoEx;

	typedef struct SItemInfo
	{
		DWORD dwOwnerID, dwItemID;
		TPriceInfo price;
		TItemInfoEx item;
		char dwOwnerName[CHARACTER_NAME_MAX_LEN + 1];
	} TItemInfo;

	typedef struct SShopInfo
	{
		DWORD dwOwnerID;
		DWORD dwDuration;
		char szName[OFFLINE_SHOP_NAME_MAX_LEN];
#ifdef ENABLE_SHOP_DECORATION
		DWORD	dwShopDecoration;
#endif
		DWORD dwCount;
	} TShopInfo;

	typedef struct SFilterInfo
	{
		BYTE bType;
		BYTE bSubType;
		char szName[OFFLINE_SHOP_ITEM_MAX_LEN];
		TPriceInfo priceStart, priceEnd;
		BYTE iLevelStart, iLevelEnd;
		DWORD dwWearFlag;
		bool FindCharacter;//Finding by character name
		MAX_COUNT minCount, maxCount;
		BYTE minAbs, maxAbs;
		BYTE minAvg;
		BYTE alchemyGrade;
		BYTE alchemyPurity;
		BYTE sashLevel;
	} TFilterInfo;

	typedef struct SShopItemInfo
	{
		TItemPos pos;
		TPriceInfo price;
#ifdef ENABLE_OFFLINE_SHOP_GRID
		TItemDisplayPos display_pos;
#endif
	} TShopItemInfo;

	enum eSubHeaderGC
	{
		SUBHEADER_GC_SHOP_LIST,
		SUBHEADER_GC_SHOP_OPEN,
		SUBHEADER_GC_SHOP_OPEN_OWNER,
		SUBHEADER_GC_SHOP_OPEN_OWNER_NO_SHOP,
		SUBHEADER_GC_SHOP_CLOSE,
		SUBHEADER_GC_SHOP_BUY_ITEM_FROM_SEARCH,
		SUBHEADER_GC_SHOP_FILTER_RESULT,
		SUBHEADER_GC_SHOP_SAFEBOX_REFRESH,
#ifdef ENABLE_SHOP_IN_CITIES
		SUBHEADER_GC_INSERT_SHOP_ENTITY,
		SUBHEADER_GC_REMOVE_SHOP_ENTITY,
#endif
#ifdef ENABLE_OFFLINESHOP_NOTIFICATION
		SUBHEADER_GC_NOTIFICATION,
#endif
#ifdef ENABLE_AVERAGE_PRICE
		SUBHEADER_GC_AVERAGE_PRICE,
#endif
	};

	typedef struct SSubPacketGCShopList
	{
		DWORD dwShopCount;
	} TSubPacketGCShopList;

	typedef struct SSubPacketGCShopOpen
	{
		TShopInfo shop;
	} TSubPacketGCShopOpen;

	typedef struct SSubPacketGCShopOpenOwner
	{
		TShopInfo shop;
	} TSubPacketGCShopOpenOwner;

	typedef struct SSubPacketGCShopFilterResult
	{
		DWORD dwCount;
	} TSubPacketGCShopFilterResult;

	typedef struct SSubPacketGCShopSafeboxRefresh
	{
		unsigned long long valute;
		DWORD dwItemCount;
	} TSubPacketGCShopSafeboxRefresh;

	typedef struct SSubPacketGCShopBuyItemFromSearch
	{
		DWORD dwOwnerID;
		DWORD dwItemID;
	} TSubPacketGCShopBuyItemFromSearch;

#ifdef ENABLE_SHOP_IN_CITIES
	typedef struct SSubPacketGCInsertShopEntity
	{
		DWORD dwVID;
		char szName[OFFLINE_SHOP_NAME_MAX_LEN];
		int iType;
		long x, y, z;
#ifdef ENABLE_SHOP_DECORATION
		DWORD	dwShopDecoration;
#endif
	} TSubPacketGCInsertShopEntity;

	typedef struct SSubPacketGCRemoveShopEntity
	{
		DWORD dwVID;
	} TSubPacketGCRemoveShopEntity;
#endif

#ifdef ENABLE_OFFLINESHOP_EXTEND_TIME
	typedef struct TExtendTime
	{
		DWORD dwTime;
	}TSubPacketCGShopExtendTime;
#endif

#ifdef ENABLE_OFFLINESHOP_NOTIFICATION
	typedef struct LightyNotifications {
		DWORD dwItemID;
		int64_t dwItemPrice; // long long
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
		MAX_COUNT dwItemCount;
#else
		uint8_t dwItemCount;
#endif
	} TSubPacketGCNotification;
#endif


#ifdef ENABLE_AVERAGE_PRICE
	typedef struct SSubPacketAveragePrice
	{
		DWORD vnum;
		long long price;
	}TSubPacketAveragePrice;
#endif

	enum eSubHeaderCG
	{
		SUBHEADER_CG_SHOP_CREATE_NEW,
		SUBHEADER_CG_SHOP_CHANGE_NAME,
		SUBHEADER_CG_SHOP_FORCE_CLOSE,
		SUBHEADER_CG_SHOP_REQUEST_SHOPLIST,
		SUBHEADER_CG_SHOP_OPEN,
		SUBHEADER_CG_SHOP_OPEN_OWNER,
		SUBHEADER_CG_SHOP_BUY_ITEM,
		SUBHEADER_CG_SHOP_ADD_ITEM,
		SUBHEADER_CG_SHOP_REMOVE_ITEM,
		SUBHEADER_CG_SHOP_EDIT_ITEM,
		SUBHEADER_CG_SHOP_FILTER_REQUEST,
		SUBHEADER_CG_SHOP_SAFEBOX_OPEN,
		SUBHEADER_CG_SHOP_SAFEBOX_GET_ITEM,
		SUBHEADER_CG_SHOP_SAFEBOX_GET_VALUTES,
		SUBHEADER_CG_SHOP_SAFEBOX_CLOSE,
		SUBHEADER_CG_CLOSE_BOARD,
#ifdef ENABLE_SHOP_IN_CITIES
		SUBHEADER_CG_CLICK_ENTITY,
#endif
#ifdef ENABLE_OFFLINESHOP_EXTEND_TIME
		SUBHEADER_CG_SHOP_EXTEND_TIME,
#endif
#ifdef ENABLE_AVERAGE_PRICE
		SUBHEADER_CG_AVERAGE_PRICE,
#endif
	};

	typedef struct SSubPacketCGShopCreate
	{
		TShopInfo shop;
	} TSubPacketCGShopCreate;

	typedef struct SSubPacketCGShopChangeName
	{
		char szName[OFFLINE_SHOP_NAME_MAX_LEN];
	} TSubPacketCGShopChangeName;

	typedef struct SSubPacketCGShopOpen
	{
		DWORD dwOwnerID;
	} TSubPacketCGShopOpen;

	typedef struct SSubPacketCGAddItem
	{
		TItemPos pos;
		TPriceInfo price;
#ifdef ENABLE_OFFLINE_SHOP_GRID
		TItemDisplayPos display_pos;
#endif
	} TSubPacketCGAddItem;

	typedef struct SSubPacketCGRemoveItem
	{
		DWORD dwItemID;
	} TSubPacketCGRemoveItem;

	typedef struct SSubPacketCGEditItem
	{
		DWORD dwItemID;
		TPriceInfo price;
		bool allEdit;
	} TSubPacketCGEditItem;

	typedef struct SSubPacketCGFilterRequest
	{
		TFilterInfo filter;
	} TSubPacketCGFilterRequest;

	typedef struct SSubPacketCGShopSafeboxGetItem
	{
		DWORD dwItemID;
	} TSubPacketCGShopSafeboxGetItem;

	typedef struct SSubPacketCGShopSafeboxGetValutes
	{
		unsigned long long gold;
	}TSubPacketCGShopSafeboxGetValutes;

	typedef struct SSubPacketCGShopBuyItem
	{
		DWORD dwOwnerID;
		DWORD dwItemID;
		bool bIsSearch;
	} TSubPacketCGShopBuyItem;


#ifdef ENABLE_SHOP_IN_CITIES
	typedef struct SSubPacketCGShopClickEntity
	{
		DWORD dwShopVID;
	} TSubPacketCGShopClickEntity;
#endif

}
#endif

#ifdef ENABLE_SWITCHBOT
enum ECGSwitchbotSubheader
{
	SUBHEADER_CG_SWITCHBOT_START,
	SUBHEADER_CG_SWITCHBOT_STOP,
};

struct TPacketCGSwitchbot
{
	uint8_t header;
	int32_t size;
	uint8_t subheader;
	uint8_t slot;
};

enum EGCSwitchbotSubheader
{
	SUBHEADER_GC_SWITCHBOT_UPDATE,
	SUBHEADER_GC_SWITCHBOT_UPDATE_ITEM,
	SUBHEADER_GC_SWITCHBOT_SEND_ATTRIBUTE_INFORMATION,
};

struct TPacketGCSwitchbot
{
	uint8_t header;
	int32_t size;
	uint8_t subheader;
	uint8_t slot;
};

struct TSwitchbotUpdateItem
{
	uint8_t	slot;
	uint8_t	vnum;
	uint8_t	count;
	uint32_t	alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
};
#endif

#ifdef ENABLE_REFRESH_CONTROL
typedef struct SPacketGCRefreshControl
{
	BYTE Header;
	BYTE SubHeader;
	bool state;
	bool update;
}TPacketGCRefreshControl;

enum RefreshControlSubPackets
{
	REFRESH_INVENTORY,
	REFRESH_SKILL,
	REFRESH_POINT,
	REFRESH_MAX
};
#endif

#ifdef ENABLE_GLOBAL_RANKING
enum StaticsRankConfing
{
#ifdef ENABLE_POWER_RANKING
	STATS_POWER,
#endif

	STATS_MONSTER_KILLED,
	STATS_STONE_KILLED,
	STATS_BOSS_KILLED,
	STATS_PLAYER_KILLED,

	STATS_MONSTER_DAMAGE,
	STATS_STONE_DAMAGE,
	STATS_BOSS_DAMAGE,
	STATS_PLAYER_DAMAGE,

	STATS_OPENED_CHEST,
	STATS_FISHING,
	STATS_MINING,
	STATS_COMPLATE_DUNGEON,

	STATS_UPGRADE_ITEM,
	STATS_USE_ENCHANTED_ITEM,
	STATS_MAX,

	RANKING_ALIGN = STATS_MAX,
	RANKING_PLAY_TIME = STATS_MAX + 1,
	RANKING_MAX,

	RANKING_MAX_PLAYER_COUNT = 10,
};

typedef struct SRankingGCPacket
{
	BYTE	bHeader;
	WORD	wSize;
	DWORD	next_update_second;
}TRankingGCPacket;

typedef struct SRankingInfo
{
	uint8_t bOrder;
	char szPlayerName[12 + 1];
	DWORD llScore;
	BYTE country;
	BYTE playerRace;
}TRankingInfo;

typedef struct SRankingData
{
	TRankingInfo rank[RANKING_MAX][RANKING_MAX_PLAYER_COUNT];
}TRankingData;

typedef struct SRankingList
{
	WORD order[RANKING_MAX];
	DWORD value[RANKING_MAX];
}TRankingList;

typedef struct SRankingMeGC
{
	char playerName[12 + 1];
	BYTE country;
	BYTE playerRace;
	TRankingList rank;
}TRankingMeGC;
#endif

#ifdef ENABLE_BIOLOG_SYSTEM
enum BiologSubPacket
{
	SUBHEADER_GC_BIOLOG_OPEN,
	SUBHEADER_GC_BIOLOG_LEVEL_UPDATE,
	SUBHEADER_GC_BIOLOG_COUNT_UPDATE,
	SUBHEADER_GC_BIOLOG_MAX_LEVEL,
	SUBHEADER_CG_BIOLOG_OPEN = 0,
	SUBHEADER_CG_BIOLOG_UPGRADE,
};

typedef struct SBiologBonus
{
	BYTE type;
	WORD value;
}TBiologBonus;

typedef struct SPacketGCBiologInformations
{
	BYTE mission_level;
	DWORD mission_vnum;
	DWORD mission_stone_vnum;
	MAX_COUNT mission_count;
	DWORD mission_cooldown;
	TBiologBonus mission_bonus[4];
}TPacketGCBiologInformations;

typedef struct SPacketGCBiologUpdate
{
	BYTE level;
	MAX_COUNT given_count;
	DWORD time;
	bool alert;
	BYTE state;
}TPacketGCBiologUpdate;

typedef struct SPacketCGBiologUpgrade
{
	SPacketCGBiologUpgrade(bool a, bool b, bool c)
	{
		time_reset = a;
		chance = b;
		allgive = c;
	};

	bool time_reset;
	bool chance;
	bool allgive;
}TPacketCGBiologUpgrade;

typedef struct SPacketGCBiolog
{
	BYTE header;
	WORD size;
	BYTE sub_header;
}TPacketGCBiolog;

typedef struct SPacketCGBiolog
{
	BYTE header;
	BYTE sub_header;
}TPacketCGBiolog;
#endif

#ifdef ENABLE_CHAR_SETTINGS
typedef struct SCharSettings
{
	bool antiexp;
#ifdef ENABLE_HIDE_COSTUME_SYSTEM
	bool HIDE_COSTUME_HAIR;
	bool HIDE_COSTUME_BODY;
	bool HIDE_COSTUME_WEAPON;
	bool HIDE_COSTUME_ACCE;
	bool HIDE_COSTUME_AURA;
	bool HIDE_COSTUME_CROWN;
#endif
#ifdef ENABLE_STOP_CHAT
	bool STOP_SHOUT;
#endif
}TCharSettings;

typedef struct SPacketCharSettings
{
	BYTE header;
	TCharSettings data;
	BYTE type;
}TPacketGCCharSettings;
#endif

#ifdef ENABLE_IN_GAME_LOG_SYSTEM
enum InGameLogGCSubHeader
{
	SUBHEADER_GC_OFFLINESHOP_LOG_OPEN,
	SUBHEADER_GC_OFFLINESHOP_LOG_ADD,
	SUBHEADER_GC_TRADE_LOG_OPEN,
	SUBHEADER_GC_TRADE_LOG_DETAILS_OPEN,
};

enum InGameLogCGSubHeader
{
	SUBHEADER_CG_OFFLINESHOP_LOG_OPEN,
	SUBHEADER_CG_TRADE_LOG_OPEN,
	SUBHEADER_CG_TRADE_LOG_DETAILS_OPEN,
};

typedef struct SPacketGCInGameLog
{
	BYTE header;
	WORD size;
	BYTE subHeader;
}TPacketGCInGameLog;

typedef struct SPacketCGInGameLog
{
	BYTE header;
	BYTE subHeader;
	DWORD logID;
}TPacketCGInGameLog;

typedef struct SItemInfo
{
	DWORD dwVnum;
	DWORD dwCount;
	long alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
}TItemInfo;

typedef struct SOfflineShopSoldLog
{
	TItemInfo item;
	unsigned long long sellPrice;
	char buyerName[24];
	char soldDate[24];
}TOfflineShopSoldLog;

typedef struct STradeLogRequestInfo
{
	DWORD logID;
	char victimName[24];
	char tradingDate[32];
}TTradeLogRequestInfo;

typedef struct STradeLogRequestItem
{
	BYTE pos;
	bool isOwner;
	TItemInfo item;
}TTradeLogRequestItem;

typedef struct STradeLogDetailsRequest
{
	DWORD logID;
	BYTE itemCount;
	uint64_t ownerGold;
	uint64_t victimGold;
}TTradeLogDetailsRequest;
#endif


#ifdef ENABLE_ITEM_TRANSACTIONS
typedef struct SItemTransactionsCGPacket
{
	BYTE header;
	BYTE transaction;
	WORD itemCount;
}TItemTransactionsCGPacket;

typedef struct SItemTransactionsInfo
{
	WORD pos;
	BYTE window;
}TItemTransactionsInfo;
#endif

#ifdef ENABLE_PM_ALL_SEND_SYSTEM
typedef struct SPacketCGBulkWhisper
{
	BYTE	header;
	char	szText[512 + 1];
} TPacketCGBulkWhisper;

typedef struct packet_bulk_whisper
{
	BYTE	header;
	WORD	size;
} TPacketGCBulkWhisper;
#endif

#ifdef ENABLE_DUNGEON_INFO
enum EDungeonInfoSubHeader
{
	SUB_HEADER_CG_DUNGEON_LOGIN_REQUEST,
	SUB_HEADER_CG_DUNGEON_TIME_RESET,
	SUB_HEADER_CG_TIME_REQUEST,

	SUB_HEADER_GC_TIME_REQUEST = 0,
	SUB_HEADER_GC_TIME_UPDATE,
	SUB_HEADER_GC_DUNGEON_MESSAGE,
};

typedef struct SPacketDungeonInfoCG
{
	BYTE header;
	BYTE subHeader;
}TPacketDungeonInfoCG;

typedef struct SPacketDungeonInfoGC
{
	BYTE header;
	WORD size;
	BYTE subHeader;
}TPacketDungeonInfoGC;
#endif

#ifdef ENABLE_EVENT_MANAGER
typedef struct SPacketGCEventManager
{
	BYTE	header;
	DWORD	size;
} TPacketGCEventManager;

typedef struct event_struct_
{
	WORD	eventID;
	BYTE	eventIndex;
	int		startTime;
	int		endTime;
	BYTE	empireFlag;
	BYTE	channelFlag;
	DWORD	value[4];
	bool	eventStatus;
	bool	eventTypeOnlyStart;
	char	startTimeText[25];
	char	endTimeText[25];
}TEventManagerData;

enum
{
	EVENT_MANAGER_LOAD,
	EVENT_MANAGER_EVENT_STATUS,
	EVENT_MANAGER_REMOVE_EVENT,
	EVENT_MANAGER_UPDATE,

	DOUBLE_METIN_LOOT_EVENT = 1,
	DOUBLE_BOSS_LOOT_EVENT = 2,

	WHELL_OF_FORTUNE_EVENT = 3,
	EXP_EVENT = 4,

	LETTER_EVENT = 5,
	OKEY_CARD_EVENT = 6,
	CATCH_KING_EVENT = 7,

	BLACK_N_WHITE_EVENT = 8,
	YUTNORI_EVENT = 9,

	MOONLIGHT_EVENT = 10,
	SOCCER_BALL_EVENT = 11,

	HALLOWEEN_EVENT = 12,
	RAMADAN_EVENT = 13,
	SUMMER_EVENT = 14,
	CHRISTMAS_EVENT = 15,
	EASTER_EVENT = 16,
	VALENTINES_EVENT = 17,

	BEGGINER_EVENT = 18,

	EMPTY_PERMANENT_EVENT = 19,
};
#endif


#ifdef ENABLE_ITEMSHOP
enum
{
	ITEMSHOP_LOAD,
	ITEMSHOP_LOG,
	ITEMSHOP_BUY,
	ITEMSHOP_DRAGONCOIN,
	ITEMSHOP_RELOAD,
	ITEMSHOP_LOG_ADD,
	ITEMSHOP_UPDATE_ITEM,
};
typedef struct SIShopData
{
	DWORD	id;
	DWORD	itemVnum;
	long long	itemPrice;
	int		topSellingIndex;
	BYTE	discount;
	int		offerTime;
	int		addedTime;
	long long	sellCount;
	int	week_limit;
	int	month_limit;
	int maxSellCount;
	long long itemUntradeablePrice;
	DWORD itemVnumUntradeable;
}TIShopData;
typedef struct SIShopLogData
{
	DWORD	accountID;
	char	playerName[CHARACTER_NAME_MAX_LEN + 1];
	char	buyDate[21];
	int		buyTime;
	char	ipAdress[16];
	DWORD	itemID;
	DWORD	itemVnum;
	int		itemCount;
	long long	itemPrice;
}TIShopLogData;
typedef struct SPacketGCItemShop
{
	BYTE	header;
	DWORD	size;
} TPacketGCItemShop;
#endif

#ifdef ENABLE_SKILL_COLOR_SYSTEM
typedef struct SPacketCGSkillColor
{
	BYTE bheader;
	BYTE skill;
	DWORD col1;
	DWORD col2;
	DWORD col3;
	DWORD col4;
	DWORD col5;
}TPacketCGSkillColor;
#endif

#ifdef ENABLE_AURA_SYSTEM
enum EAuraInfo
{
	AURA_ABSORPTION_SOCKET = 0,
	AURA_ABSORBED_SOCKET = 1,
	AURA_LEVEL_SOCKET = 2,
	AURA_WINDOW_MAX_MATERIALS = 2,
	AURA_ICE_RUNIC = 49990,
	AURA_ICE_RUNIC2 = 49991,
};

enum
{
	AURA_SUBHEADER_GC_OPEN = 0,
	AURA_SUBHEADER_GC_CLOSE,
	AURA_SUBHEADER_GC_ADDED,
	AURA_SUBHEADER_GC_REMOVED,
	AURA_SUBHEADER_GC_REFINED,
	AURA_SUBHEADER_CG_CLOSE = 0,
	AURA_SUBHEADER_CG_ADD,
	AURA_SUBHEADER_CG_REMOVE,
	AURA_SUBHEADER_CG_REFINE,
};

typedef struct SPacketAura
{
	BYTE    header;
	BYTE    subheader;
	bool    bWindow;
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	unsigned long long	dwPrice;
#else
	DWORD    dwPrice;
#endif
	BYTE    bPos;
	TItemPos    tPos;
	DWORD    dwItemVnum;
	DWORD    dwMinAbs;
	DWORD    dwMaxAbs;
} TPacketAura;

typedef struct SAuraMaterial
{
	BYTE    bHere;
	WORD    wCell;
} TAuraMaterial;

typedef struct SAuraResult
{
	DWORD    dwItemVnum;
	DWORD    dwMinAbs;
	DWORD    dwMaxAbs;
} TAuraResult;
#endif

#ifdef ENABLE_NEW_PET_SYSTEM
enum ENewPetPacket
{
	SUB_GC_UNSUMMON,
	SUB_GC_UPDATE,
	SUB_GC_UPDATE_EXP,

	SUB_CG_STAR_INCREASE = 0,
	SUB_CG_TYPE_INCREASE,
	SUB_CG_EVOLUTION_INCREASE,
	SUB_CG_SKIN_CHANGE,
	SUB_CG_ACTIVATE_SKIN,
	SUB_CG_BONUS_CHANGE,
	SUB_CG_RESET_SKILL,
};

typedef struct SNewPetGCPacket
{
	BYTE header;
	WORD size;
	BYTE subHeader;
}TNewPetGCPacket;

typedef struct SNewPetCGPacket
{
	BYTE header;
	BYTE subHeader;
}TNewPetCGPacket;

typedef struct SPetSkill
{
	BYTE type;
	BYTE level;
}TPetSkill;

typedef struct SNewPetInfo
{
	BYTE level;
	DWORD exp;
	DWORD nextExp;
	BYTE evolution;
	BYTE type;
	BYTE star;
	DWORD skinVnum;
	BYTE skinCount;
	WORD bonus[3];
	TPetSkill skill[8];
}TNewPetInfo;
#endif

#ifdef ENABLE_BOSS_SHOWER_ON_ATLAS
typedef struct sBossAtlas
{
	DWORD mob_vnum;
	long x, y;
	int spawntime;
} TBossAtlas;
#endif

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
typedef struct SPacketChangeLanguage
{
	BYTE bHeader;
	BYTE bLanguage;
} TPacketChangeLanguage;
#endif
#ifdef ENABLE_EXTENDED_WHISPER_DETAILS
typedef struct SPacketCGWhisperDetails
{
	BYTE header;
	char name[CHARACTER_NAME_MAX_LEN + 1];
} TPacketCGWhisperDetails;

typedef struct SPacketGCWhisperDetails
{
	BYTE header;
	char name[CHARACTER_NAME_MAX_LEN + 1];
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	BYTE bLanguage;
#endif
} TPacketGCWhisperDetails;
#endif

#ifdef ENABLE_EXTENDED_BATTLE_PASS
typedef struct SPacketCGExtBattlePassAction
{
	BYTE bHeader;
	BYTE bAction;
} TPacketCGExtBattlePassAction;

typedef struct SPacketCGExtBattlePassSendPremium
{
	uint8_t bHeader;
	bool premium;
} TPacketCGExtBattlePassSendPremium;

typedef struct SPacketGCExtBattlePassOpen
{
	BYTE bHeader;
} TPacketGCExtBattlePassOpen;

typedef struct SPacketGCExtBattlePassGeneralInfo
{
	BYTE bHeader;
	BYTE bBattlePassType;
	char	szSeasonName[64 + 1];
	DWORD dwBattlePassID;
	DWORD dwBattlePassStartTime;
	DWORD dwBattlePassEndTime;
} TPacketGCExtBattlePassGeneralInfo;

typedef struct SPacketGCExtBattlePassMissionInfo
{
	BYTE bHeader;
	WORD wSize;
	WORD wRewardSize;
	BYTE bBattlePassType;
	DWORD dwBattlePassID;
} TPacketGCExtBattlePassMissionInfo;

typedef struct SPacketGCExtBattlePassMissionUpdate
{
	BYTE bHeader;
	BYTE bBattlePassType;
	BYTE bMissionIndex;
	BYTE bMissionType;
	DWORD dwNewProgress;
} TPacketGCExtBattlePassMissionUpdate;

typedef struct SPacketGCExtBattlePassRanking
{
	BYTE bHeader;
	char	szPlayerName[CHARACTER_NAME_MAX_LEN + 1];
	BYTE bBattlePassType;
	BYTE	bBattlePassID;
	DWORD	dwStartTime;
	DWORD	dwEndTime;
} TPacketGCExtBattlePassRanking;
#endif

#ifdef ENABLE_LEADERSHIP_EXTENSION
typedef struct SPacketCGRequestPartyBonus
{
	BYTE		bHeader;
	BYTE		bBonusID;
} TPacketCGRequestPartyBonus;
#endif

#ifdef ENABLE_6TH_7TH_ATTR
typedef struct command_67_attr
{
	BYTE			bHeader;
	BYTE			bMaterialCount;
	BYTE			bSupportCount;
	short			sSupportPos;
	short			sItemPos;
} TPacketCG67Attr;

typedef struct command_67_attr_open_close
{
	BYTE			bHeader;
} TPacket67AttrOpenClose;
#endif

#ifdef ENABLE_NEW_CHAT
typedef struct SPacketNewChat
{
	BYTE header;
	WORD size;
	WORD chatID;
	BYTE chatType;
}TPacketNewChat;
#endif

#ifdef ENABLE_BUFFI_SYSTEM
typedef struct SPGCBuffiSkill
{
	BYTE header;
	BYTE skillVnum;
	DWORD vid;
}TPGCBuffiSkill;

typedef struct SPCGBuffi
{
	BYTE header;
	BYTE subHeader;
}TPCGBuffi;
#endif

#ifdef ENABLE_MINI_GAME_OKEY_NORMAL
/*Client -> Server*/
enum EPacketCGMiniGameSubHeaderOkeyNormal
{
	SUBHEADER_CG_RUMI_START,
	SUBHEADER_CG_RUMI_EXIT,
	SUBHEADER_CG_RUMI_DECKCARD_CLICK,
	SUBHEADER_CG_RUMI_HANDCARD_CLICK,
	SUBHEADER_CG_RUMI_FIELDCARD_CLICK,
	SUBHEADER_CG_RUMI_DESTROY,
};

typedef struct SPacketCGMiniGameOkeyCard
{
	SPacketCGMiniGameOkeyCard() : bHeader(HEADER_CG_OKEY_CARD) {}
	uint8_t bHeader;
	uint16_t wSize;
	uint8_t bSubHeader;
} TPacketCGMiniGameOkeyCard;

typedef struct SSubPacketCGMiniGameCardOpenClose
{
	uint8_t bSafeMode;
} TSubPacketCGMiniGameCardOpenClose;

typedef struct SSubPacketCGMGHandCardClick
{
	int index;
} TSubPacketCGMiniGameHandCardClick;

typedef struct SSubPacketCGMGFieldCardClick
{
	int index;
} TSubPacketCGMiniGameFieldCardClick;

typedef struct SSubPacketCGMGDestroy
{
	int index;
} TSubPacketCGMiniGameDestroy;

/*Server -> Client*/
enum EPacketGCMiniGameSubHeaderOkeyNormal
{
	SUBHEADER_GC_RUMI_OPEN,
	SUBHEADER_GC_RUMI_CARD_UPDATE,
	SUBHEADER_GC_RUMI_CARD_REWARD,
};

typedef struct SPacketGCMiniGameOkeyCard
{
	SPacketGCMiniGameOkeyCard() : bHeader(HEADER_GC_OKEY_CARD) {}
	uint8_t bHeader;
	uint16_t wSize;
	uint8_t bSubHeader;
} TPacketGCMiniGameOkeyCard;

typedef struct SSubPacketGCMiniGameCardOpenClose
{
	uint8_t bSafeMode;
} TSubPacketGCMiniGameCardOpenClose;

typedef struct SSubPacketGCMiniGameCardsInfo
{
	uint32_t cardHandType[5];
	uint32_t cardHandValue[5];
	uint8_t cardHandLeft;
	uint32_t cHandPoint;

	uint32_t cardFieldType[3];
	uint32_t cardFieldValue[3];
	uint32_t cFieldPoint;
} TSubPacketGCMiniGameCardsInfo;

typedef struct SSubPacketGCMiniGameCardsReward
{
	uint32_t cardType[3];
	uint32_t cardValue[3];
	uint32_t cPoint;
} TSubPacketGCMiniGameCardsReward;
#endif

#ifdef ENABLE_MINI_GAME_BNW
typedef struct SPacketCGMinigameBnw
{
	BYTE header;
	BYTE subheader;
} TPacketCGMinigameBnw;

enum
{
	MINIGAME_BNW_SUBHEADER_CG_START,
	MINIGAME_BNW_SUBHEADER_CG_SELECTED_CARD,
	MINIGAME_BNW_SUBHEADER_CG_FINISHED,
};

typedef struct SPacketGCMinigameBnw
{
	BYTE header;
	BYTE subheader;
} TPacketGCMinigameBnw;

enum
{
	MINIGAME_BNW_SUBHEADER_GC_START,
	MINIGAME_BNW_SUBHEADER_GC_DRAW_RESULT,
};

typedef struct SPacketGCMinigameBnwDrawResult
{
	BYTE result;
	BYTE playerPoints;
	BYTE enemyPoints;
} TPacketGCMinigameBnwDrawResult;
#endif

#ifdef ENABLE_MINI_GAME_CATCH_KING
/*Client -> Server*/
enum EPacketCGMiniGameSubHeaderCatchKing
{
	SUBHEADER_CG_CATCH_KING_START,
	SUBHEADER_CG_CATCH_KING_DECKCARD_CLICK,
	SUBHEADER_CG_CATCH_KING_FIELDCARD_CLICK,
	SUBHEADER_CG_CATCH_KING_REWARD,
};

typedef struct SPacketCGMiniGameCatchKing
{
	SPacketCGMiniGameCatchKing() : bHeader(HEADER_CG_MINI_GAME_CATCH_KING) {}
	uint8_t bHeader;
	uint16_t wSize;
	uint8_t bSubheader;
} TPacketCGMiniGameCatchKing;

typedef struct SSubPacketCGMiniGameCatchKingStart {
	uint8_t betNumber;
} TSubPacketCGMiniGameCatchKingStart;

typedef struct SSubPacketCGMiniGameCatchKingFieldCardClick {
	uint8_t cardNumber;
} TSubPacketCGMiniGameCatchKingFieldCardClick;

/*Server -> Client*/
enum EPacketGCMiniGameSubHeaderCatchKing
{
	SUBHEADER_GC_CATCH_KING_EVENT_INFO,
	SUBHEADER_GC_CATCH_KING_START,
	SUBHEADER_GC_CATCH_KING_SET_CARD,
	SUBHEADER_GC_CATCH_KING_RESULT_FIELD,
	SUBHEADER_GC_CATCH_KING_SET_END_CARD,
	SUBHEADER_GC_CATCH_KING_REWARD,
};

typedef struct SPacketGCMiniGameCatchKing
{
	SPacketGCMiniGameCatchKing() : bHeader(HEADER_GC_MINI_GAME_CATCH_KING) {}
	uint8_t bHeader;
	uint16_t wSize;
	uint8_t bSubheader;
} TPacketGCMiniGameCatchKing;

typedef struct SSubPacketGCCatchKingStart
{
	uint32_t dwBigScore;
} TSubPacketGCCatchKingStart;

typedef struct SSubPacketGCCatchKingSetCard
{
	uint8_t bCardInHand;
} TSubPacketGCCatchKingSetCard;

typedef struct SSubPacketGCCatchKingResult
{
	uint32_t dwPoints;
	uint8_t bRowType;
	uint8_t bCardPos;
	uint8_t bCardValue;
	bool bKeepFieldCard;
	bool bDestroyHandCard;
	bool bGetReward;
	bool bIsFiveNearBy;
} TSubPacketGCCatchKingResult;

typedef struct SSubPacketGCCatchKingSetEndCard
{
	uint8_t bCardPos;
	uint8_t bCardValue;
} TSubPacketGCCatchKingSetEndCard;

typedef struct SSubPacketGCCatchKingReward
{
	uint8_t bReturnCode;
} TSubPacketGCCatchKingReward;

typedef struct SSubPacketGCCatchKingEventInfo
{
	uint8_t bIsEnable;
} TSubPacketGCCatchKingEventInfo;
#endif


#pragma pack(pop)
