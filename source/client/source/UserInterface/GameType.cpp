#include "StdAfx.h"
#include "GameType.h"
#include "Packet.h"

std::string g_strResourcePath = "d:/ymir work/";
std::string g_strImagePath = "d:/ymir work/ui/";

std::string g_strGuildSymbolPathName = "mark/10/";

// DEFAULT_FONT
static std::string gs_strDefaultFontName = "Arial:12.fnt";
static std::string gs_strDefaultItalicFontName = "Arial:12i.fnt";
static CResource* gs_pkDefaultFont = NULL;
static CResource* gs_pkDefaultItalicFont = NULL;

static bool gs_isReloadDefaultFont = false;

void DefaultFont_Startup()
{
	gs_pkDefaultFont = NULL;
}

void DefaultFont_Cleanup()
{
	if (gs_pkDefaultFont)
		gs_pkDefaultFont->Release();
}

void DefaultFont_SetName(const char* c_szFontName)
{
	gs_strDefaultFontName = c_szFontName;
	gs_strDefaultFontName += ".fnt";

	gs_strDefaultItalicFontName = c_szFontName;
	if (strchr(c_szFontName, ':'))
		gs_strDefaultItalicFontName += "i";
	gs_strDefaultItalicFontName += ".fnt";

	gs_isReloadDefaultFont = true;
}

bool ReloadDefaultFonts()
{
	CResourceManager& rkResMgr = CResourceManager::Instance();

	gs_isReloadDefaultFont = false;

	CResource* pkNewFont = rkResMgr.GetResourcePointer(gs_strDefaultFontName.c_str());
	pkNewFont->AddReference();
	if (gs_pkDefaultFont)
		gs_pkDefaultFont->Release();
	gs_pkDefaultFont = pkNewFont;

	CResource* pkNewItalicFont = rkResMgr.GetResourcePointer(gs_strDefaultItalicFontName.c_str());
	pkNewItalicFont->AddReference();
	if (gs_pkDefaultItalicFont)
		gs_pkDefaultItalicFont->Release();
	gs_pkDefaultItalicFont = pkNewItalicFont;

	return true;
}

CResource* DefaultFont_GetResource()
{
	if (!gs_pkDefaultFont || gs_isReloadDefaultFont)
		ReloadDefaultFonts();
	return gs_pkDefaultFont;
}

CResource* DefaultItalicFont_GetResource()
{
	if (!gs_pkDefaultItalicFont || gs_isReloadDefaultFont)
		ReloadDefaultFonts();
	return gs_pkDefaultItalicFont;
}

// END_OF_DEFAULT_FONT

void SetGuildSymbolPath(const char* c_szPathName)
{
	g_strGuildSymbolPathName = "mark/";
	g_strGuildSymbolPathName += c_szPathName;
	g_strGuildSymbolPathName += "/";
}

const char* GetGuildSymbolFileName(DWORD dwGuildID)
{
	return _getf("%s%03d.jpg", g_strGuildSymbolPathName.c_str(), dwGuildID);
}

BYTE c_aSlotTypeToInvenType[SLOT_TYPE_MAX] =
{
	RESERVED_WINDOW,		// SLOT_TYPE_NONE
	INVENTORY,				// SLOT_TYPE_INVENTORY
	RESERVED_WINDOW,		// SLOT_TYPE_SKILL
	RESERVED_WINDOW,		// SLOT_TYPE_EMOTION
	RESERVED_WINDOW,		// SLOT_TYPE_SHOP
	RESERVED_WINDOW,		// SLOT_TYPE_EXCHANGE_OWNER
	RESERVED_WINDOW,		// SLOT_TYPE_EXCHANGE_TARGET
	RESERVED_WINDOW,		// SLOT_TYPE_QUICK_SLOT
	RESERVED_WINDOW,
	RESERVED_WINDOW,		// SLOT_TYPE_PRIVATE_SHOP
	RESERVED_WINDOW,
	DRAGON_SOUL_INVENTORY,	// SLOT_TYPE_DRAGON_SOUL_INVENTORY
#ifdef ENABLE_SPECIAL_STORAGE
	UPGRADE_INVENTORY,		// SLOT_TYPE_UPGRADE_INVENTORY
	BOOK_INVENTORY,			// SLOT_TYPE_BOOK_INVENTORY
	STONE_INVENTORY,		// SLOT_TYPE_STONE_INVENTORY
	CHEST_INVENTORY,		// SLOT_TYPE_CHEST_INVENTORY
#endif
#ifdef ENABLE_SWITCHBOT
	SWITCHBOT,				// SLOT_TYPE_SWITCHBOT
#endif
#ifdef ENABLE_BUFFI_SYSTEM
	BUFFI_INVENTORY,
#endif
};

BYTE SlotTypeToInvenType(BYTE bSlotType)
{
	if (bSlotType >= SLOT_TYPE_MAX)
		return RESERVED_WINDOW;
	else
		return c_aSlotTypeToInvenType[bSlotType];
}

typedef struct SApplyInfo
{
	BYTE	bPointType; // APPLY -> POINT
} TApplyInfo;

const TApplyInfo aApplyInfo[CItemData::MAX_APPLY_NUM] =
{
	{POINT_NONE				,},		//APPLY_NONE				= 0,
	{POINT_MAX_HP			,},		//APPLY_MAX_HP				= 1,
	{POINT_MAX_SP			,},		//APPLY_MAX_SP				= 2,
	{POINT_HT				,},		//APPLY_CON					= 3,
	{POINT_IQ				,},		//APPLY_INT					= 4,
	{POINT_ST				,},		//APPLY_STR					= 5,
	{POINT_DX				,},		//APPLY_DEX					= 6,
	{POINT_ATT_SPEED		,},		//APPLY_ATT_SPEED			= 7,
	{POINT_MOV_SPEED		,},		//APPLY_MOV_SPEED			= 8,
	{POINT_CASTING_SPEED	,},		//APPLY_CAST_SPEED			= 9,
	{POINT_HP_REGEN			,},		//APPLY_HP_REGEN			= 10,
	{POINT_SP_REGEN			,},		//APPLY_SP_REGEN			= 11,
	{POINT_POISON_PCT		,},		//APPLY_POISON_PCT			= 12,
	{POINT_STUN_PCT			,},		//APPLY_STUN_PCT			= 13,
	{POINT_SLOW_PCT			,},		//APPLY_SLOW_PCT			= 14,
	{POINT_CRITICAL_PCT		,},		//APPLY_CRITICAL_PCT		= 15,
	{POINT_PENETRATE_PCT	,},		//APPLY_PENETRATE_PCT		= 16,
	{POINT_ATTBONUS_HUMAN	,},		//APPLY_ATTBONUS_HUMAN		= 17,
	{POINT_ATTBONUS_ANIMAL	,},		//APPLY_ATTBONUS_ANIMAL		= 18,
	{POINT_ATTBONUS_ORC		,},		//APPLY_ATTBONUS_ORC		= 19,
	{POINT_ATTBONUS_MILGYO	,},		//APPLY_ATTBONUS_MILGYO		= 20,
	{POINT_ATTBONUS_UNDEAD	,},		//APPLY_ATTBONUS_UNDEAD		= 21,
	{POINT_ATTBONUS_DEVIL	,},		//APPLY_ATTBONUS_DEVIL		= 22,
	{POINT_STEAL_HP			,},		//APPLY_STEAL_HP			= 23,
	{POINT_STEAL_SP			,},		//APPLY_STEAL_SP			= 24,
	{POINT_MANA_BURN_PCT	,},		//APPLY_MANA_BURN_PCT		= 25,
	{POINT_DAMAGE_SP_RECOVER,},		//APPLY_DAMAGE_SP_RECOVER	= 26,
	{POINT_BLOCK			,},		//APPLY_BLOCK				= 27,
	{POINT_DODGE			,},		//APPLY_DODGE				= 28,
	{POINT_RESIST_SWORD		,},		//APPLY_RESIST_SWORD		= 29,
	{POINT_RESIST_TWOHAND	,},		//APPLY_RESIST_TWOHAND		= 30,
	{POINT_RESIST_DAGGER	,},		//APPLY_RESIST_DAGGER		= 31,
	{POINT_RESIST_BELL		,},		//APPLY_RESIST_BELL			= 32,
	{POINT_RESIST_FAN		,},		//APPLY_RESIST_FAN			= 33,
	{POINT_RESIST_BOW		,},		//APPLY_RESIST_BOW			= 34,
	{POINT_RESIST_FIRE		,},		//APPLY_RESIST_FIRE			= 35,
	{POINT_RESIST_ELEC		,},		//APPLY_RESIST_ELEC			= 36,
	{POINT_RESIST_MAGIC		,},		//APPLY_RESIST_MAGIC		= 37,
	{POINT_RESIST_WIND		,},		//APPLY_RESIST_WIND			= 38,
	{POINT_REFLECT_MELEE	,},		//APPLY_REFLECT_MELEE		= 39,
	{POINT_REFLECT_CURSE	,},		//APPLY_REFLECT_CURSE		= 40,
	{POINT_POISON_REDUCE	,},		//APPLY_POISON_REDUCE		= 41,
	{POINT_KILL_SP_RECOVER	,},		//APPLY_KILL_SP_RECOVER		= 42,
	{POINT_EXP_DOUBLE_BONUS	,},		//APPLY_EXP_DOUBLE_BONUS	= 43,
	{POINT_GOLD_DOUBLE_BONUS,},		//APPLY_GOLD_DOUBLE_BONUS	= 44,
	{POINT_ITEM_DROP_BONUS	,},		//APPLY_ITEM_DROP_BONUS		= 45,
	{POINT_POTION_BONUS		,},		//APPLY_POTION_BONUS		= 46,
	{POINT_KILL_HP_RECOVERY	,},		//APPLY_KILL_HP_RECOVER		= 47,
	{POINT_IMMUNE_STUN		,},		//APPLY_IMMUNE_STUN			= 48,
	{POINT_IMMUNE_SLOW		,},		//APPLY_IMMUNE_SLOW			= 49,
	{POINT_IMMUNE_FALL		,},		//APPLY_IMMUNE_FALL			= 50,
	{POINT_NONE				,},		//APPLY_SKILL				= 51,
	{POINT_BOW_DISTANCE		,},		//APPLY_BOW_DISTANCE		= 52,
	{POINT_ATT_GRADE_BONUS	,},		//APPLY_ATT_GRADE_BONUS		= 53,
	{POINT_DEF_GRADE_BONUS	,},		//APPLY_DEF_GRADE_BONUS		= 54,
	{POINT_MAGIC_ATT_GRADE_BONUS,},	//APPLY_MAGIC_ATT_GRADE		= 55,
	{POINT_MAGIC_DEF_GRADE_BONUS,},	//APPLY_MAGIC_DEF_GRADE		= 56,
	{POINT_CURSE_PCT		,},		//APPLY_CURSE_PCT			= 57,
	{POINT_MAX_STAMINA		,},		//APPLY_MAX_STAMINA			= 58,
	{POINT_ATTBONUS_WARRIOR	,},		//APPLY_ATTBONUS_WARRIOR	= 59,
	{POINT_ATTBONUS_ASSASSIN,},		//APPLY_ATTBONUS_ASSASSIN	= 60,
	{POINT_ATTBONUS_SURA	,},		//APPLY_ATTBONUS_SURA		= 61,
	{POINT_ATTBONUS_SHAMAN	,},		//APPLY_ATTBONUS_SHAMAN		= 62,
	{POINT_ATTBONUS_MONSTER	,},		//APPLY_ATTBONUS_MONSTER	= 63,
	{POINT_ATT_BONUS		,},		//APPLY_MALL_ATTBONUS		= 64,
	{POINT_MALL_DEFBONUS	,},		//APPLY_MALL_DEFBONUS		= 65,
	{POINT_MALL_EXPBONUS	,},		//APPLY_MALL_EXPBONUS		= 66,
	{POINT_MALL_ITEMBONUS	,},		//APPLY_MALL_ITEMBONUS		= 67,
	{POINT_MALL_GOLDBONUS	,},		//APPLY_MALL_GOLDBONUS		= 68,
	{POINT_MAX_HP_PCT		,},		//APPLY_MAX_HP_PCT			= 69,
	{POINT_MAX_SP_PCT		,},		//APPLY_MAX_SP_PCT			= 70,
	{POINT_SKILL_DAMAGE_BONUS,},	//APPLY_SKILL_DAMAGE_BONUS	= 71,
	{POINT_NORMAL_HIT_DAMAGE_BONUS,},//APPLY_NORMAL_HIT_DAMAGE_BONUS= 72,
	{POINT_SKILL_DEFEND_BONUS,},	//APPLY_SKILL_DEFEND_BONUS	= 73,
	{POINT_NORMAL_HIT_DEFEND_BONUS,},//APPLY_NORMAL_HIT_DEFEND_BONUS= 74,
	{POINT_NONE				,},		//APPLY_EXTRACT_HP_PCT		= 75,
	{POINT_RESIST_WARRIOR	,},		//APPLY_RESIST_WARRIOR		= 76,
	{POINT_RESIST_ASSASSIN	,},		//APPLY_RESIST_ASSASSIN		= 77,
	{POINT_RESIST_SURA		,},		//APPLY_RESIST_SURA			= 78,
	{POINT_RESIST_SHAMAN	,},		//APPLY_RESIST_SHAMAN		= 79,
	{POINT_ENERGY			,},		//APPLY_ENERGY				= 80,
	{POINT_DEF_GRADE		,},		//APPLY_DEF_GRADE			= 81,
	{POINT_COSTUME_ATTR_BONUS,},	//APPLY_COSTUME_ATTR_BONUS	= 82,
	{POINT_MAGIC_ATT_BONUS_PER,},	//APPLY_MAGIC_ATTBONUS_PER	= 83,
	{POINT_MELEE_MAGIC_ATT_BONUS_PER,},//APPLY_MELEE_MAGIC_ATTBONUS_PER= 84,
	{POINT_RESIST_ICE		,},		//APPLY_RESIST_ICE			= 85,
	{POINT_RESIST_EARTH		,},		//APPLY_RESIST_EARTH		= 86,
	{POINT_RESIST_DARK		,},		//APPLY_RESIST_DARK			= 87,
	{POINT_RESIST_CRITICAL	,},		//APPLY_ANTI_CRITICAL_PCT	= 88,
	{POINT_RESIST_PENETRATE	,},		//APPLY_ANTI_PENETRATE_PCT	= 89,
#ifdef ENABLE_WOLFMAN_CHARACTER
	{POINT_BLEEDING_REDUCE	,},		//APPLY_BLEEDING_REDUCE		= 90,
	{POINT_BLEEDING_PCT		,},		//APPLY_BLEEDING_PCT		= 91,
	{POINT_ATTBONUS_WOLFMAN	,},		//APPLY_ATTBONUS_WOLFMAN	= 92,
	{POINT_RESIST_WOLFMAN	,},		//APPLY_RESIST_WOLFMAN		= 93,
	{POINT_RESIST_CLAW		,},		//APPLY_RESIST_CLAW			= 94,
#endif
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	{POINT_ACCEDRAIN_RATE	,},		//APPLY_ACCEDRAIN_RATE		= 95,
#endif
#ifdef ENABLE_MAGIC_REDUCTION_SYSTEM
	{POINT_RESIST_MAGIC_REDUCTION,},//APPLY_RESIST_MAGIC_REDUCTION = 96,
#endif
#ifdef ENABLE_EXTRA_APPLY_BONUS
	{ POINT_ATTBONUS_STONE, },	//APPLY_ATTBONUS_STONE			= 97,
	{ POINT_ATTBONUS_BOSS, },	//APPLY_ATTBONUS_BOSS			= 98,
	{ POINT_ATTBONUS_PVM_STR, },	//APPLY_ATTBONUS_PVM_STR		= 99,
	{ POINT_ATTBONUS_PVM_AVG, },	//APPLY_ATTBONUS_PVM_AVG		= 100,
	{ POINT_ATTBONUS_PVM_BERSERKER, },//APPLY_ATTBONUS_PVM_BERSERKER	= 101,
	{ POINT_ATTBONUS_ELEMENT, },	//APPLY_ATTBONUS_ELEMENT			= 102,
	{ POINT_DEFBONUS_PVM, },	//APPLY_DEFBONUS_PVM				= 103,
	{ POINT_DEFBONUS_ELEMENT, },	//APPLY_DEFBONUS_ELEMENT			= 104,
	{ POINT_ATTBONUS_PVP, },	//APPLY_ATTBONUS_PVP				= 105,
	{ POINT_DEFBONUS_PVP, },	//APPLY_DEFBONUS_PVP				= 106,

	{ POINT_ATT_FIRE, },	//APPLY_ATTBONUS_FIRE				= 107,
	{ POINT_ATT_ICE, },	//APPLY_ATTBONUS_ICE				= 108,
	{ POINT_ATT_WIND, },	//APPLY_ATTBONUS_WIND				= 109,
	{ POINT_ATT_EARTH, },	//APPLY_ATTBONUS_EARTH				= 110,
	{ POINT_ATT_DARK, },	//APPLY_ATTBONUS_DARK				= 111,
	{ POINT_ATT_ELEC, },	//APPLY_ATTBONUS_ELEC				= 112,
#endif
};

BYTE ApplyTypeToPointType(BYTE bApplyType)
{
	if (bApplyType >= CItemData::MAX_APPLY_NUM)
		return POINT_NONE;
	else
		return aApplyInfo[bApplyType].bPointType;
}

typedef struct SPointValueName
{
	const char* c_pszName;
	BYTE		apply;
	BYTE		point;
} TPointValueName;

TPointValueName ApplyNameToPoint[] =
{
	{ "ATT_NONE",				CItemData::APPLY_NONE,					POINT_NONE				},
	{ "ATT_GRADE_BONUS",		CItemData::APPLY_ATT_GRADE_BONUS,		POINT_ATT_GRADE_BONUS	},
	{ "ATT_MONSTER",			CItemData::APPLY_ATTBONUS_MONSTER,		POINT_ATTBONUS_MONSTER	},
	{ "ATT_AVG",				CItemData::APPLY_NORMAL_HIT_DAMAGE_BONUS, POINT_NORMAL_HIT_DAMAGE_BONUS},
	{ "ATT_SKILL_DAMAGE_BONUS",	CItemData::APPLY_SKILL_DAMAGE_BONUS,	POINT_SKILL_DAMAGE_BONUS},
	{ "MAX_HP",					CItemData::APPLY_MAX_HP,				POINT_MAX_HP			},
	{ "ATT_HALF_HUMANS",		CItemData::APPLY_ATTBONUS_HUMAN,		POINT_ATTBONUS_HUMAN	},
	{ "MELEE_MAGIC_ATTBONUS",	CItemData::APPLY_MELEE_MAGIC_ATTBONUS_PER, POINT_MELEE_MAGIC_ATT_BONUS_PER},
	{ "ATT_SPEED",				CItemData::APPLY_ATT_SPEED,			POINT_ATT_SPEED			},

#ifdef ENABLE_EXTRA_APPLY_BONUS
	{ "ATT_STONE",				CItemData::APPLY_ATTBONUS_STONE,		POINT_ATTBONUS_STONE	},
	{ "ATT_BOSS",				CItemData::APPLY_ATTBONUS_BOSS,		POINT_ATTBONUS_BOSS		},
	{ "ATT_PVM_STR",			CItemData::APPLY_ATTBONUS_PVM_STR,		POINT_ATTBONUS_PVM_STR},
	{ "ATT_PVM_AVG",			CItemData::APPLY_ATTBONUS_PVM_AVG,		POINT_ATTBONUS_PVM_AVG},
	{ "ATT_PVM_BERSERKER",		CItemData::APPLY_ATTBONUS_PVM_BERSERKER,POINT_ATTBONUS_PVM_BERSERKER },
	{ "ATT_ELEMENT",			CItemData::APPLY_ATTBONUS_ELEMENT,		POINT_ATTBONUS_ELEMENT},
	{ "DEF_PVM",				CItemData::APPLY_DEFBONUS_PVM,			POINT_DEFBONUS_PVM},
	{ "DEF_ELEMENT",			CItemData::APPLY_DEFBONUS_ELEMENT,		POINT_DEFBONUS_ELEMENT},
	{ "ATT_JOB",				CItemData::APPLY_ATTBONUS_PVP,			POINT_ATTBONUS_PVP},
	{ "RESIST_JOB",				CItemData::APPLY_DEFBONUS_PVP,			POINT_DEFBONUS_PVP},
#endif
	{ NULL,						0,										0						}
};

std::pair<BYTE, BYTE> StringApplyToPoint(const char* apply_type_string)
{
	TPointValueName* value_name;
	for (value_name = ApplyNameToPoint; value_name->c_pszName; ++value_name)
	{
		if (0 == stricmp(value_name->c_pszName, apply_type_string))
			return std::make_pair(value_name->apply, value_name->point);
	}
	return std::make_pair(0, 0);
}
