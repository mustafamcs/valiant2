#pragma once

//        Icon, Model (droped on ground), Game Data

#include "../eterLib/GrpSubImage.h"
#include "../eterGrnLib/Thing.h"
#include "GameLibDefines.h"

class CItemData
{
public:
	enum
	{
		ITEM_NAME_MAX_LEN = 64,//@Lightwork36
		ITEM_LIMIT_MAX_NUM = 2,
		ITEM_VALUES_MAX_NUM = 6,
		ITEM_SMALL_DESCR_MAX_LEN = 256,
#ifdef ENABLE_ITEM_PROTO_APPLY_LIMIT
		ITEM_APPLY_MAX_NUM = 5,
#else
		ITEM_APPLY_MAX_NUM = 3,
#endif
		ITEM_SOCKET_MAX_NUM = 3,
#ifdef ENABLE_SHINING_SYSTEM
		ITEM_SHINING_MAX_COUNT = 3,
#endif
	};

	enum EItemType
	{
		ITEM_TYPE_NONE			= 0,
		ITEM_TYPE_WEAPON		= 1,
		ITEM_TYPE_ARMOR			= 2,
		ITEM_TYPE_USE			= 3,
		ITEM_TYPE_AUTOUSE		= 4,
		ITEM_TYPE_MATERIAL		= 5,
		ITEM_TYPE_SPECIAL		= 6,
		ITEM_TYPE_TOOL			= 7,
		ITEM_TYPE_ELK			= 8,
		ITEM_TYPE_METIN			= 9,
		ITEM_TYPE_CONTAINER		= 10,
		ITEM_TYPE_FISH			= 11,
		ITEM_TYPE_ROD			= 12,
		ITEM_TYPE_RESOURCE		= 13,
		ITEM_TYPE_CAMPFIRE		= 14,
		ITEM_TYPE_UNIQUE		= 15,
		ITEM_TYPE_SKILLBOOK		= 16,
		ITEM_TYPE_QUEST			= 17,
		ITEM_TYPE_POLYMORPH		= 18,
		ITEM_TYPE_TREASURE_BOX	= 19,
		ITEM_TYPE_TREASURE_KEY	= 20,
		ITEM_TYPE_SKILLFORGET	= 21,
		ITEM_TYPE_GIFTBOX		= 22,
		ITEM_TYPE_PICK			= 23,
		ITEM_TYPE_HAIR			= 24,
		ITEM_TYPE_TOTEM			= 25,
		ITEM_TYPE_BLEND			= 26,
		ITEM_TYPE_COSTUME		= 27,
		ITEM_TYPE_DS			= 28,
		ITEM_TYPE_SPECIAL_DS	= 29,
		ITEM_TYPE_EXTRACT		= 30,
		ITEM_TYPE_SECONDARY_COIN= 31,
		ITEM_TYPE_RING			= 32,
		ITEM_TYPE_BELT			= 33,
#ifdef ENABLE_PET_COSTUME_SYSTEM
		ITEM_TYPE_PET			= 34,
#endif
#ifdef ENABLE_MOUNT_SKIN
		ITEM_MOUNT_SKIN			= 35,
#endif
#ifdef ENABLE_PET_SKIN
		ITEM_PET_SKIN			= 36,
#endif
#ifdef ENABLE_CROWN_SYSTEM
		ITEM_TYPE_CROWN			= 37,
#endif
#ifdef ENABLE_ITEMS_SHINING
		ITEM_TYPE_SHINING		= 38,
#endif
#ifdef ENABLE_BOOSTER_ITEM
		ITEM_BOOSTER			= 39,
#endif
#ifdef ENABLE_PENDANT_ITEM
		ITEM_PENDANT			= 40,
#endif
#ifdef ENABLE_GLOVE_ITEM
		ITEM_GLOVE			= 41,
#endif
#ifdef ENABLE_RINGS
		ITEM_RINGS			= 42,
#endif
#ifdef ENABLE_AURA_SKIN
		ITEM_AURA_SKIN		= 43,
#endif
#ifdef ENABLE_DREAMSOUL
		ITEM_DREAMSOUL			= 44,
#endif
		ITEM_TYPE_MAX_NUM
	};

	enum EWeaponSubTypes
	{
		WEAPON_SWORD, //0
		WEAPON_DAGGER,
		WEAPON_BOW, //2
		WEAPON_TWO_HANDED, //3
		WEAPON_BELL, //4
		WEAPON_FAN, //5
		WEAPON_ARROW, //6
		WEAPON_MOUNT_SPEAR, //7
#ifdef ENABLE_WOLFMAN_CHARACTER
		WEAPON_CLAW = 8, //8
#endif
#ifdef ENABLE_QUIVER_SYSTEM
		WEAPON_QUIVER = 9, //9
#endif
		WEAPON_NUM_TYPES, //11 2015/11/12

		WEAPON_NONE = WEAPON_NUM_TYPES + 1,
	};

	enum EMaterialSubTypes
	{
		MATERIAL_LEATHER,
		MATERIAL_BLOOD,
		MATERIAL_ROOT,
		MATERIAL_NEEDLE,
		MATERIAL_JEWEL,
		MATERIAL_DS_REFINE_NORMAL,
		MATERIAL_DS_REFINE_BLESSED,
		MATERIAL_DS_REFINE_HOLLY,
	};

	enum EArmorSubTypes
	{
		ARMOR_BODY,
		ARMOR_HEAD,
		ARMOR_SHIELD,
		ARMOR_WRIST,
		ARMOR_FOOTS,
		ARMOR_NECK,
		ARMOR_EAR,
		ARMOR_NUM_TYPES
	};

	enum ECostumeSubTypes
	{
		COSTUME_BODY,
		COSTUME_HAIR,
#ifdef ENABLE_MOUNT_COSTUME_SYSTEM
		COSTUME_MOUNT = 2,		//2
#endif
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
		COSTUME_ACCE = 3,		//3
#endif
#ifdef ENABLE_WEAPON_COSTUME_SYSTEM
		COSTUME_WEAPON = 4,		//4
#endif
#ifdef ENABLE_AURA_SYSTEM
		COSTUME_AURA = 5,
#endif
#ifdef ENABLE_ACCE_COSTUME_SKIN
		COSTUME_WING = 6,
#endif
		COSTUME_NUM_TYPES,
	};

	enum EUseSubTypes
	{
		USE_POTION,					// 0
		USE_TALISMAN,
		USE_TUNING,
		USE_MOVE,
		USE_TREASURE_BOX,
		USE_MONEYBAG,
		USE_BAIT,
		USE_ABILITY_UP,
		USE_AFFECT,
		USE_CREATE_STONE,
		USE_SPECIAL,				// 10
		USE_POTION_NODELAY,
		USE_CLEAR,
		USE_INVISIBILITY,
		USE_DETACHMENT,
		USE_BUCKET,
		USE_POTION_CONTINUE,
		USE_CLEAN_SOCKET,
		USE_CHANGE_ATTRIBUTE,
		USE_ADD_ATTRIBUTE,
		USE_ADD_ACCESSORY_SOCKET,	// 20
		USE_PUT_INTO_ACCESSORY_SOCKET,
		USE_ADD_ATTRIBUTE2,
		USE_RECIPE,
		USE_CHANGE_ATTRIBUTE2,
		USE_BIND,
		USE_UNBIND,
		USE_TIME_CHARGE_PER,
		USE_TIME_CHARGE_FIX,				// 28
		USE_PUT_INTO_BELT_SOCKET,
		USE_PUT_INTO_RING_SOCKET,
#ifdef ENABLE_USE_COSTUME_ATTR
		USE_CHANGE_COSTUME_ATTR,			// 31
		USE_RESET_COSTUME_ATTR,				// 32
#endif
#ifdef ENABLE_ATTR_RARE_RENEWAL
		USE_CHANGE_RARE_ATTRIBUTE,
		USE_ADD_RARE_ATTRIBUTE,
#endif
	};

	enum EDragonSoulSubType
	{
		DS_SLOT1,
		DS_SLOT2,
		DS_SLOT3,
		DS_SLOT4,
		DS_SLOT5,
		DS_SLOT6,
		DS_SLOT_NUM_TYPES,
	};

#ifdef ENABLE_EXTENDED_BLEND_AFFECT
	enum EDSSDuration
	{
		MIN_INFINITE_DURATION = 100 * 24 * 60 * 60,
		MAX_INFINITE_DURATION = 60 * 365 * 24 * 60 * 60,
	};
#endif

	enum EMetinSubTypes
	{
		METIN_NORMAL,
		METIN_GOLD,
	};

#ifdef ENABLE_ITEMS_SHINING
	enum EShiningSubTypes
	{
		SHINING_WRIST_LEFT,
		SHINING_WRIST_RIGHT,
		SHINING_ARMOR,
		SHINING_MAX_TYPE,
	};
#endif

	enum ELimitTypes
	{
		LIMIT_NONE,
		LIMIT_LEVEL,
		LIMIT_STR,
		LIMIT_DEX,
		LIMIT_INT,
		LIMIT_CON,
		LIMIT_REAL_TIME,
		LIMIT_REAL_TIME_START_FIRST_USE,
		LIMIT_TIMER_BASED_ON_WEAR,
		LIMIT_MAX_NUM
	};

	enum EItemAntiFlag
	{
		ITEM_ANTIFLAG_FEMALE = (1 << 0),
		ITEM_ANTIFLAG_MALE = (1 << 1),
		ITEM_ANTIFLAG_WARRIOR = (1 << 2),
		ITEM_ANTIFLAG_ASSASSIN = (1 << 3),
		ITEM_ANTIFLAG_SURA = (1 << 4),
		ITEM_ANTIFLAG_SHAMAN = (1 << 5),
		ITEM_ANTIFLAG_GET = (1 << 6),
		ITEM_ANTIFLAG_DROP = (1 << 7),
		ITEM_ANTIFLAG_SELL = (1 << 8),
		ITEM_ANTIFLAG_EMPIRE_A = (1 << 9),
		ITEM_ANTIFLAG_EMPIRE_B = (1 << 10),
		ITEM_ANTIFLAG_EMPIRE_R = (1 << 11),
		ITEM_ANTIFLAG_SAVE = (1 << 12),
		ITEM_ANTIFLAG_GIVE = (1 << 13),
		ITEM_ANTIFLAG_PKDROP = (1 << 14),
		ITEM_ANTIFLAG_STACK = (1 << 15),
		ITEM_ANTIFLAG_MYSHOP = (1 << 16),
		ITEM_ANTIFLAG_SAFEBOX = (1 << 17),
#ifdef ENABLE_WOLFMAN_CHARACTER
		ITEM_ANTIFLAG_WOLFMAN = (1 << 18),
#endif
	};

	enum EItemFlag
	{
		ITEM_FLAG_REFINEABLE = (1 << 0),
		ITEM_FLAG_SAVE = (1 << 1),
		ITEM_FLAG_STACKABLE = (1 << 2),
		ITEM_FLAG_COUNT_PER_1GOLD = (1 << 3),
		ITEM_FLAG_SLOW_QUERY = (1 << 4),
		ITEM_FLAG_RARE = (1 << 5),
		ITEM_FLAG_UNIQUE = (1 << 6),
		ITEM_FLAG_MAKECOUNT = (1 << 7),
		ITEM_FLAG_IRREMOVABLE = (1 << 8),
		ITEM_FLAG_CONFIRM_WHEN_USE = (1 << 9),
		ITEM_FLAG_QUEST_USE = (1 << 10),
		ITEM_FLAG_QUEST_USE_MULTIPLE = (1 << 11),
		ITEM_FLAG_QUEST_GIVE = (1 << 12),    // UNUSED03
		ITEM_FLAG_LOG = (1 << 13),
		ITEM_FLAG_APPLICABLE = (1 << 14),
	};

	enum EWearPositions
	{
		WEAR_BODY			 = 0,
		WEAR_HEAD			 = 1,
		WEAR_FOOTS			 = 2,
		WEAR_WRIST			 = 3,
		WEAR_WEAPON			 = 4,
		WEAR_NECK			 = 5,
		WEAR_EAR			 = 6,
		WEAR_UNIQUE1		 = 7,
		WEAR_UNIQUE2		 = 8,
		WEAR_ARROW			 = 9,
		WEAR_SHIELD			 = 10,
		WEAR_COSTUME_BODY	 = 11,
		WEAR_COSTUME_HAIR	 = 12,
#ifdef ENABLE_MOUNT_COSTUME_SYSTEM
		WEAR_COSTUME_MOUNT	 = 13,
#endif
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
		WEAR_COSTUME_ACCE	 = 14,
#endif
		WEAR_BELT			 = 15,
#ifdef ENABLE_WEAPON_COSTUME_SYSTEM
		WEAR_COSTUME_WEAPON	 = 16,
#endif
#ifdef ENABLE_PET_COSTUME_SYSTEM
		WEAR_PET			 = 17,
#endif
#ifdef ENABLE_AURA_SYSTEM
		WEAR_COSTUME_AURA	 = 18,
#endif
#ifdef ENABLE_ACCE_COSTUME_SKIN
		WEAR_COSTUME_WING	 = 19,
#endif
#ifdef ENABLE_MOUNT_SKIN
		WEAR_MOUNT_SKIN		 = 20,
#endif
#ifdef ENABLE_PET_SKIN
		WEAR_PET_SKIN		 = 21,
#endif
#ifdef ENABLE_PET_SKIN
		WEAR_CROWN			 = 22,
#endif
#ifdef ENABLE_ITEMS_SHINING
		WEAR_SHINING_WRIST_LEFT = 23,
		WEAR_SHINING_WRIST_RIGHT = 24,
		WEAR_SHINING_ARMOR	 = 25,
#endif
#ifdef ENABLE_BOOSTER_ITEM
		WEAR_BOOSTER_WEAPON = 26,
		WEAR_BOOSTER_BODY = 27,
		WEAR_BOOSTER_HEAD = 28,
		WEAR_BOOSTER_SASH = 29,
		WEAR_BOOSTER_PET = 30,
		WEAR_BOOSTER_MOUNT = 31,
#endif
#ifdef ENABLE_PENDANT_ITEM
		WEAR_PENDANT			 = 32,
#endif
#ifdef ENABLE_GLOVE_ITEM
		WEAR_GLOVE			 = 33,
#endif
#ifdef ENABLE_RINGS
		WEAR_RING_0			 = 34,
		WEAR_RING_1			 = 35,
		WEAR_RING_2			 = 36,
		WEAR_RING_3			 = 37,
		WEAR_RING_4			 = 38,
		WEAR_RING_5			 = 39,
		WEAR_RING_6			 = 40,
		WEAR_RING_7			 = 41,
#endif
#ifdef ENABLE_AURA_SKIN
		WEAR_AURA_SKIN			 = 42,
#endif
#ifdef ENABLE_DREAMSOUL
		WEAR_DREAMSOUL_RED		= 43,
		WEAR_DREAMSOUL_BLUE		= 44,
#endif
#ifdef ENABLE_NEW_PET_SYSTEM
		WEAR_NEW_PET			= 45,
#endif
		WEAR_EQ_COUNT,
		WEAR_EQ_MAX = WEAR_EQ_COUNT + 1,
		WEAR_MAX_NUM = 64,
	};

	enum EItemWearableFlag
	{
		WEARABLE_BODY = (1 << 0),
		WEARABLE_HEAD = (1 << 1),
		WEARABLE_FOOTS = (1 << 2),
		WEARABLE_WRIST = (1 << 3),
		WEARABLE_WEAPON = (1 << 4),
		WEARABLE_NECK = (1 << 5),
		WEARABLE_EAR = (1 << 6),
		WEARABLE_UNIQUE = (1 << 7),
		WEARABLE_SHIELD = (1 << 8),
		WEARABLE_ARROW = (1 << 9),
#ifdef ENABLE_AURA_SYSTEM
		WEARABLE_COSTUME_AURA = (1 << 10),
#endif
	};

	enum EApplyTypes
	{
		APPLY_NONE						= 0,
		APPLY_MAX_HP					= 1,
		APPLY_MAX_SP					= 2,
		APPLY_CON						= 3,
		APPLY_INT						= 4,
		APPLY_STR						= 5,
		APPLY_DEX						= 6,
		APPLY_ATT_SPEED					= 7,
		APPLY_MOV_SPEED					= 8,
		APPLY_CAST_SPEED				= 9,
		APPLY_HP_REGEN					= 10,
		APPLY_SP_REGEN					= 11,
		APPLY_POISON_PCT				= 12,
		APPLY_STUN_PCT					= 13,
		APPLY_SLOW_PCT					= 14,
		APPLY_CRITICAL_PCT				= 15,
		APPLY_PENETRATE_PCT				= 16,
		APPLY_ATTBONUS_HUMAN			= 17,
		APPLY_ATTBONUS_ANIMAL			= 18,
		APPLY_ATTBONUS_ORC				= 19,
		APPLY_ATTBONUS_MILGYO			= 20,
		APPLY_ATTBONUS_UNDEAD			= 21,
		APPLY_ATTBONUS_DEVIL			= 22,
		APPLY_STEAL_HP					= 23,
		APPLY_STEAL_SP					= 24,
		APPLY_MANA_BURN_PCT				= 25,
		APPLY_DAMAGE_SP_RECOVER			= 26,
		APPLY_BLOCK						= 27,
		APPLY_DODGE						= 28,
		APPLY_RESIST_SWORD				= 29,
		APPLY_RESIST_TWOHAND			= 30,
		APPLY_RESIST_DAGGER				= 31,
		APPLY_RESIST_BELL				= 32,
		APPLY_RESIST_FAN				= 33,
		APPLY_RESIST_BOW				= 34,
		APPLY_RESIST_FIRE				= 35,
		APPLY_RESIST_ELEC				= 36,
		APPLY_RESIST_MAGIC				= 37,
		APPLY_RESIST_WIND				= 38,
		APPLY_REFLECT_MELEE				= 39,
		APPLY_REFLECT_CURSE				= 40,
		APPLY_POISON_REDUCE				= 41,
		APPLY_KILL_SP_RECOVER			= 42,
		APPLY_EXP_DOUBLE_BONUS			= 43,
		APPLY_GOLD_DOUBLE_BONUS			= 44,
		APPLY_ITEM_DROP_BONUS			= 45,
		APPLY_POTION_BONUS				= 46,
		APPLY_KILL_HP_RECOVER			= 47,
		APPLY_IMMUNE_STUN				= 48,
		APPLY_IMMUNE_SLOW				= 49,
		APPLY_IMMUNE_FALL				= 50,
		APPLY_SKILL						= 51,
		APPLY_BOW_DISTANCE				= 52,
		APPLY_ATT_GRADE_BONUS			= 53,
		APPLY_DEF_GRADE_BONUS			= 54,
		APPLY_MAGIC_ATT_GRADE			= 55,
		APPLY_MAGIC_DEF_GRADE			= 56,
		APPLY_CURSE_PCT					= 57,
		APPLY_MAX_STAMINA				= 58,
		APPLY_ATTBONUS_WARRIOR			= 59,
		APPLY_ATTBONUS_ASSASSIN			= 60,
		APPLY_ATTBONUS_SURA				= 61,
		APPLY_ATTBONUS_SHAMAN			= 62,
		APPLY_ATTBONUS_MONSTER			= 63,
		APPLY_MALL_ATTBONUS				= 64,
		APPLY_MALL_DEFBONUS				= 65,
		APPLY_MALL_EXPBONUS				= 66,
		APPLY_MALL_ITEMBONUS			= 67,
		APPLY_MALL_GOLDBONUS			= 68,
		APPLY_MAX_HP_PCT				= 69,
		APPLY_MAX_SP_PCT				= 70,
		APPLY_SKILL_DAMAGE_BONUS		= 71,
		APPLY_NORMAL_HIT_DAMAGE_BONUS	= 72,
		APPLY_SKILL_DEFEND_BONUS		= 73,
		APPLY_NORMAL_HIT_DEFEND_BONUS	= 74,
		APPLY_EXTRACT_HP_PCT			= 75,
		APPLY_RESIST_WARRIOR			= 76,
		APPLY_RESIST_ASSASSIN			= 77,
		APPLY_RESIST_SURA				= 78,
		APPLY_RESIST_SHAMAN				= 79,
		APPLY_ENERGY					= 80,
		APPLY_DEF_GRADE					= 81,
		APPLY_COSTUME_ATTR_BONUS		= 82,
		APPLY_MAGIC_ATTBONUS_PER		= 83,
		APPLY_MELEE_MAGIC_ATTBONUS_PER	= 84,
		APPLY_RESIST_ICE				= 85,
		APPLY_RESIST_EARTH				= 86,
		APPLY_RESIST_DARK				= 87,
		APPLY_ANTI_CRITICAL_PCT			= 88,
		APPLY_ANTI_PENETRATE_PCT		= 89,
#ifdef ENABLE_WOLFMAN_CHARACTER
		APPLY_BLEEDING_REDUCE			= 90,
		APPLY_BLEEDING_PCT				= 91,
		APPLY_ATTBONUS_WOLFMAN			= 92,
		APPLY_RESIST_WOLFMAN			= 93,
		APPLY_RESIST_CLAW				= 94,
#endif
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
		APPLY_ACCEDRAIN_RATE			= 95,
#endif
#ifdef ENABLE_MAGIC_REDUCTION_SYSTEM
		APPLY_RESIST_MAGIC_REDUCTION	= 96,
#endif
#ifdef ENABLE_EXTRA_APPLY_BONUS
		APPLY_ATTBONUS_STONE			= 97,
		APPLY_ATTBONUS_BOSS				= 98,
		APPLY_ATTBONUS_PVM_STR			= 99,
		APPLY_ATTBONUS_PVM_AVG			= 100,
		APPLY_ATTBONUS_PVM_BERSERKER	= 101,
		APPLY_ATTBONUS_ELEMENT			= 102,
		APPLY_DEFBONUS_PVM				= 103,
		APPLY_DEFBONUS_ELEMENT			= 104,
		APPLY_ATTBONUS_PVP				= 105,
		APPLY_DEFBONUS_PVP				= 106,

		APPLY_ATTBONUS_FIRE				= 107,
		APPLY_ATTBONUS_ICE				= 108,
		APPLY_ATTBONUS_WIND				= 109,
		APPLY_ATTBONUS_EARTH			= 110,
		APPLY_ATTBONUS_DARK				= 111,
		APPLY_ATTBONUS_ELEC				= 112,
#endif
		MAX_APPLY_NUM,
	};

	enum EImmuneFlags
	{
		IMMUNE_PARA = (1 << 0),
		IMMUNE_CURSE = (1 << 1),
		IMMUNE_STUN = (1 << 2),
		IMMUNE_SLEEP = (1 << 3),
		IMMUNE_SLOW = (1 << 4),
		IMMUNE_POISON = (1 << 5),
		IMMUNE_TERROR = (1 << 6),
		IMMUNE_FLAG_MAX_NUM = 7
	};

#pragma pack(push)
#pragma pack(1)
	typedef struct SItemLimit
	{
		BYTE        bType;
		long        lValue;
	} TItemLimit;

	typedef struct SItemApply
	{
		BYTE        bType;
		long        lValue;
	} TItemApply;

	typedef struct SItemTable_r152
	{
		DWORD       dwVnum;
		char        szName[ITEM_NAME_MAX_LEN + 1];
		char        szLocaleName[ITEM_NAME_MAX_LEN + 1];
		BYTE        bType;
		BYTE        bSubType;

		BYTE        bWeight;
		BYTE        bSize;

		DWORD       dwAntiFlags;
		DWORD       dwFlags;
		DWORD       dwWearFlags;
		DWORD       dwImmuneFlag;

#ifdef ENABLE_EXTENDED_YANG_LIMIT
		int64_t		dwIBuyItemPrice;
		int64_t		dwISellItemPrice;
#else
		DWORD		dwIBuyItemPrice;
		DWORD		dwISellItemPrice;
#endif

		TItemLimit  aLimits[ITEM_LIMIT_MAX_NUM];
		TItemApply  aApplies[ITEM_APPLY_MAX_NUM];
		long        alValues[ITEM_VALUES_MAX_NUM];
		long        alSockets[ITEM_SOCKET_MAX_NUM];
		DWORD       dwRefinedVnum;
		WORD		wRefineSet;
		BYTE        bAlterToMagicItemPct;
		BYTE		bSpecular;
		BYTE        bGainSocketPct;
	} TItemTable_r152;

	typedef struct SItemTable_r156
	{
		DWORD       dwVnum;
		DWORD       dwVnumRange;
		char        szName[ITEM_NAME_MAX_LEN + 1];
		char        szLocaleName[ITEM_NAME_MAX_LEN + 1];
		BYTE        bType;
		BYTE        bSubType;

		BYTE        bWeight;
		BYTE        bSize;

		DWORD       dwAntiFlags;
		DWORD       dwFlags;
		DWORD       dwWearFlags;
		DWORD       dwImmuneFlag;

#ifdef ENABLE_EXTENDED_YANG_LIMIT
		int64_t		dwIBuyItemPrice;
		int64_t		dwISellItemPrice;
#else
		DWORD		dwIBuyItemPrice;
		DWORD		dwISellItemPrice;
#endif

		TItemLimit  aLimits[ITEM_LIMIT_MAX_NUM];
		TItemApply  aApplies[ITEM_APPLY_MAX_NUM];
		long        alValues[ITEM_VALUES_MAX_NUM];
		long        alSockets[ITEM_SOCKET_MAX_NUM];
		DWORD       dwRefinedVnum;
		WORD		wRefineSet;
		BYTE        bAlterToMagicItemPct;
		BYTE		bSpecular;
		BYTE        bGainSocketPct;
	} TItemTable_r156;

	typedef struct SItemTable_r158
	{
		DWORD       dwVnum;
		DWORD       dwVnumRange;
		char        szName[ITEM_NAME_MAX_LEN + 1];
		char        szLocaleName[ITEM_NAME_MAX_LEN + 1];
		BYTE        bType;
		BYTE        bSubType;

		BYTE        bWeight;
		BYTE        bSize;

		DWORD       dwAntiFlags;
		DWORD       dwFlags;
		DWORD       dwWearFlags;
		DWORD       dwImmuneFlag;

#ifdef ENABLE_EXTENDED_YANG_LIMIT
		int64_t		dwIBuyItemPrice;
		int64_t		dwISellItemPrice;
#else
		DWORD		dwIBuyItemPrice;
		DWORD		dwISellItemPrice;
#endif

		TItemLimit  aLimits[ITEM_LIMIT_MAX_NUM];
		TItemApply  aApplies[ITEM_APPLY_MAX_NUM];
		long        alValues[ITEM_VALUES_MAX_NUM];
		long        alSockets[ITEM_SOCKET_MAX_NUM];
		DWORD       dwRefinedVnum;
		WORD		wRefineSet;
		BYTE        bAlterToMagicItemPct;
		BYTE		bSpecular;
		BYTE        bGainSocketPct;
		WORD		wWearableFlag;
	} TItemTable_r158;

	typedef SItemTable_r156 SItemTable, TItemTable;

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	struct SScaleInfo
	{
		float	fScaleX, fScaleY, fScaleZ;
		float	fPositionX, fPositionY, fPositionZ;
	};

	typedef struct SScaleTable
	{
		SScaleInfo	tInfo[10];
	} TScaleTable;
#endif

#ifdef ENABLE_PROTOSTRUCT_AUTODETECT
	typedef struct SItemTableAll
	{
		static bool IsValidStruct(DWORD structSize)
		{
			switch (structSize)
			{
				case sizeof(TItemTable_r152) :
					case sizeof(TItemTable_r156) :
					case sizeof(TItemTable_r158) :
					return true;
					break;
			}
			return false;
		}

		static void Process(void* obj, DWORD structSize, DWORD i, CItemData::TItemTable& t)
		{
#define ITABLE_COPY_STR(x) strncpy_s(t.##x##, sizeof(t.##x##), r.##x##, _TRUNCATE)
#define ITABLE_COPY_INT(x) t.##x## = r.##x
#define ITABLE_ZERO_STR(x) memset(t.##x##, 0, sizeof(t.##x##));
#define ITABLE_ZERO_INT(x) t.##x## = 0
#define ITABLE_COUNT(x) _countof(t.##x##)
#define ITABLE_PROCESS(len)\
					CItemData::TItemTable_r##len## & r = *((CItemData::TItemTable_r##len## *) obj + i);\
					ITABLE_COPY_INT(dwVnum);\
					ITABLE_COPY_STR(szName);\
					ITABLE_COPY_STR(szLocaleName);\
					ITABLE_COPY_INT(bType);\
					ITABLE_COPY_INT(bSubType);\
					ITABLE_COPY_INT(bWeight);\
					ITABLE_COPY_INT(bSize);\
					ITABLE_COPY_INT(dwAntiFlags);\
					ITABLE_COPY_INT(dwFlags);\
					ITABLE_COPY_INT(dwWearFlags);\
					ITABLE_COPY_INT(dwImmuneFlag);\
					ITABLE_COPY_INT(dwIBuyItemPrice);\
					ITABLE_COPY_INT(dwISellItemPrice);\
					for (size_t i=0; i<ITABLE_COUNT(aLimits); ++i)\
					{\
						ITABLE_COPY_INT(aLimits[i].bType);\
						ITABLE_COPY_INT(aLimits[i].lValue);\
					}\
					for (size_t i=0; i<CItemData::ITEM_APPLY_MAX_NUM; ++i)\
					{\
						ITABLE_COPY_INT(aApplies[i].bType);\
						ITABLE_COPY_INT(aApplies[i].lValue);\
					}\
					for (size_t i=0; i<CItemData::ITEM_VALUES_MAX_NUM; ++i)\
					{\
						ITABLE_COPY_INT(alValues[i]);\
					}\
					for (size_t i=0; i<CItemData::ITEM_SOCKET_MAX_NUM; ++i)\
					{\
						ITABLE_COPY_INT(alSockets[i]);\
					}\
					ITABLE_COPY_INT(dwRefinedVnum);\
					ITABLE_COPY_INT(wRefineSet);\
					ITABLE_COPY_INT(bAlterToMagicItemPct);\
					ITABLE_COPY_INT(bSpecular);\
					ITABLE_COPY_INT(bGainSocketPct);

			switch (structSize)
			{
				case sizeof(TItemTable_r152) :
				{
					ITABLE_PROCESS(152);
					ITABLE_ZERO_INT(dwVnumRange);
				}
				break;
				case sizeof(TItemTable_r156) :
				{
					ITABLE_PROCESS(156);
					ITABLE_COPY_INT(dwVnumRange);
				}
				break;
				case sizeof(TItemTable_r158) :
				{
					ITABLE_PROCESS(158);
					ITABLE_COPY_INT(dwVnumRange);
				}
				break;
			}
		}
	} TItemTableAll;
#endif //ENABLE_PROTOSTRUCT_AUTODETECT

#pragma pack(pop)

public:
	CItemData();
	virtual ~CItemData();

	void Clear();
	void SetSummary(const std::string& c_rstSumm);
#ifdef ENABLE_COLORFUL_DESCRIPTIONS
	void SetRed(const std::string& c_rstRed);
	void SetBlue(const std::string& c_rstBlue);
	void SetGreen(const std::string& c_rstGreen);
	void SetYellow(const std::string& c_rstYellow);
	void SetOrange(const std::string& c_rstOrange);
	void SetPink(const std::string& c_rstPink);
	void SetPurple(const std::string& c_rstPurple);
#endif
	void SetDescription(const std::string& c_rstDesc);

	CGraphicThing* GetModelThing();
	CGraphicThing* GetSubModelThing();
	CGraphicThing* GetDropModelThing();
	CGraphicSubImage* GetIconImage();

	DWORD GetLODModelThingCount();
	BOOL GetLODModelThingPointer(DWORD dwIndex, CGraphicThing** ppModelThing);

	DWORD GetAttachingDataCount();
	BOOL GetCollisionDataPointer(DWORD dwIndex, const NRaceData::TAttachingData** c_ppAttachingData);
	BOOL GetAttachingDataPointer(DWORD dwIndex, const NRaceData::TAttachingData** c_ppAttachingData);

	/////
	const TItemTable* GetTable() const;
	DWORD GetIndex() const;

	const char* GetName() const;
	const char* GetDescription() const;
	const char* GetSummary() const;
#ifdef ENABLE_COLORFUL_DESCRIPTIONS
	const char * GetRed() const;
	const char * GetBlue() const;
	const char * GetGreen() const;
	const char * GetYellow() const;
	const char * GetOrange() const;
	const char * GetPink() const;
	const char * GetPurple() const;
#endif
	BYTE GetType() const;
	BYTE GetSubType() const;
	UINT GetRefine() const;
	const char* GetUseTypeString() const;
	DWORD GetWeaponType() const;
	BYTE GetSize() const;
	BOOL IsAntiFlag(DWORD dwFlag) const;
	BOOL IsFlag(DWORD dwFlag) const;
	BOOL IsWearableFlag(DWORD dwFlag) const;
	BOOL HasNextGrade() const;
#ifdef ENABLE_WIKI
	WORD GetRefinedSet() const;
	WORD GetRefinedVnum() const;
#endif
	DWORD GetWearFlags() const;
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t GetIBuyItemPrice() const;
	int64_t GetISellItemPrice() const;
#else
	DWORD GetIBuyItemPrice() const;
	DWORD GetISellItemPrice() const;
#endif
	BOOL GetLimit(BYTE byIndex, TItemLimit* pItemLimit) const;
	BOOL GetApply(BYTE byIndex, TItemApply* pItemApply) const;
	long GetValue(BYTE byIndex) const;
	long GetSocket(BYTE byIndex) const;
	long SetSocket(BYTE byIndex, DWORD value);
	int GetSocketCount() const;
	DWORD GetIconNumber() const;

	UINT	GetSpecularPoweru() const;
	float	GetSpecularPowerf() const;

	/////

	BOOL IsEquipment() const;

	/////

	//BOOL LoadItemData(const char * c_szFileName);
	void SetDefaultItemData(const char* c_szIconFileName, const char* c_szModelFileName = NULL);
	void SetItemTableData(TItemTable* pItemTable);

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	void SetItemScale(const std::string strJob, const std::string strSex, const std::string strScaleX, const std::string strScaleY, const std::string strScaleZ, const std::string strPositionX, const std::string strPositionY, const std::string strPositionZ);
	bool GetItemScale(DWORD dwPos, float& fScaleX, float& fScaleY, float& fScaleZ, float& fPositionX, float& fPositionY, float& fPositionZ);
#endif

#ifdef ENABLE_SHINING_SYSTEM
	typedef struct SItemShiningTable
	{
		char szShinings[ITEM_SHINING_MAX_COUNT][256];
	public:
		//Checking if any shining is set for this item.
		bool Any() const
		{
			for (int i = 0; i < CItemData::ITEM_SHINING_MAX_COUNT; i++)
			{
				if (strcmp(szShinings[i], ""))
				{
					return true;
				}
			}
			return false;
		}
	} TItemShiningTable;

	void SetItemShiningTableData(BYTE bIndex, const char* szEffectname);
	CItemData::TItemShiningTable GetItemShiningTable() { return m_ItemShiningTable; }
#endif

#ifdef ENABLE_AURA_SYSTEM
protected:
	DWORD m_dwAuraEffectID;
public:
	void SetAuraEffectID(const char* szAuraEffectPath);
	DWORD GetAuraEffectID() const { return m_dwAuraEffectID; }

	enum EAuraMisc
	{
		AURA_GRADE_MAX_NUM = 6,
	};
#endif

protected:
	void __LoadFiles();
	void __SetIconImage(const char* c_szFileName);

protected:
	std::string m_strModelFileName;
	std::string m_strSubModelFileName;
	std::string m_strDropModelFileName;
	std::string m_strIconFileName;
	std::string m_strDescription;
	std::string m_strSummary;
#ifdef ENABLE_COLORFUL_DESCRIPTIONS
	std::string m_strRed;
	std::string m_strBlue;
	std::string m_strGreen;
	std::string m_strYellow;
	std::string m_strOrange;
	std::string m_strPink;
	std::string m_strPurple;
#endif
	std::vector<std::string> m_strLODModelFileNameVector;

	CGraphicThing* m_pModelThing;
	CGraphicThing* m_pSubModelThing;
	CGraphicThing* m_pDropModelThing;
	CGraphicSubImage* m_pIconImage;
	std::vector<CGraphicThing*> m_pLODModelThingVector;

	NRaceData::TAttachingDataVector m_AttachingDataVector;
	DWORD		m_dwVnum;
	TItemTable m_ItemTable;
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	TScaleTable	m_ScaleTable;
#endif
#ifdef ENABLE_SHINING_SYSTEM
	TItemShiningTable m_ItemShiningTable;
#endif

public:
	static void DestroySystem();

	static CItemData* New();
	static void Delete(CItemData* pkItemData);

	static CMemoryPoolNew<CItemData>		ms_kPool;


#ifdef ENABLE_GLOBAL_SCALE
protected:
	typedef struct SItemScaleTable
	{
		D3DXVECTOR3 v3MeshScale[NRaceData::SEX_MAX_NUM][NRaceData::JOB_MAX_NUM];
		float fParticleScale[NRaceData::SEX_MAX_NUM][NRaceData::JOB_MAX_NUM];
	} TItemScaleTable;
	TItemScaleTable m_ItemScaleTable;

public:
	float GetItemParticleScale(uint8_t byJob, uint8_t bySex);
	void SetItemTableScaleData(uint8_t byJob, uint8_t bySex, float fMeshScaleX, float fMeshScaleY, float fMeshScaleZ, float fParticleScale);
	D3DXVECTOR3& GetItemScaleVector(uint8_t byJob, uint8_t bySex);
#endif

};
