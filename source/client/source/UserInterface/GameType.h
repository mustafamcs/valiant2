#pragma once
#include "../GameLib/ItemData.h"

struct SAffects
{
	enum
	{
		AFFECT_MAX_NUM = 32,
	};

	SAffects() : dwAffects(0) {}
	SAffects(const DWORD& c_rAffects)
	{
		__SetAffects(c_rAffects);
	}
	int operator = (const DWORD& c_rAffects)
	{
		__SetAffects(c_rAffects);
	}

	BOOL IsAffect(BYTE byIndex)
	{
		return dwAffects & (1 << byIndex);
	}

	void __SetAffects(const DWORD& c_rAffects)
	{
		dwAffects = c_rAffects;
	}

	DWORD dwAffects;
};

extern std::string g_strGuildSymbolPathName;

const DWORD c_Name_Max_Length = 64;
const DWORD c_FileName_Max_Length = 128;
const DWORD c_Short_Name_Max_Length = 32;

const DWORD c_Inventory_Page_Column = 5;
const DWORD c_Inventory_Page_Row = 9;
const DWORD c_Inventory_Page_Size = c_Inventory_Page_Column * c_Inventory_Page_Row; // x*y
#ifdef ENABLE_EXTEND_INVEN_SYSTEM
const DWORD c_Inventory_Page_Count = 5;
#else
const DWORD c_Inventory_Page_Count = 2;
#endif
const DWORD c_ItemSlot_Count = c_Inventory_Page_Size * c_Inventory_Page_Count;
const DWORD c_Equipment_Count = CItemData::WEAR_EQ_MAX;

const DWORD c_Equipment_Start = c_ItemSlot_Count;

const DWORD c_Equipment_Body = c_Equipment_Start + CItemData::WEAR_BODY;
const DWORD c_Equipment_Head = c_Equipment_Start + CItemData::WEAR_HEAD;
const DWORD c_Equipment_Shoes = c_Equipment_Start + CItemData::WEAR_FOOTS;
const DWORD c_Equipment_Wrist = c_Equipment_Start + CItemData::WEAR_WRIST;
const DWORD c_Equipment_Weapon = c_Equipment_Start + CItemData::WEAR_WEAPON;
const DWORD c_Equipment_Neck = c_Equipment_Start + CItemData::WEAR_NECK;
const DWORD c_Equipment_Ear = c_Equipment_Start + CItemData::WEAR_EAR;
const DWORD c_Equipment_Unique1 = c_Equipment_Start + CItemData::WEAR_UNIQUE1;
const DWORD c_Equipment_Unique2 = c_Equipment_Start + CItemData::WEAR_UNIQUE2;
const DWORD c_Equipment_Arrow = c_Equipment_Start + CItemData::WEAR_ARROW;
const DWORD c_Equipment_Shield = c_Equipment_Start + CItemData::WEAR_SHIELD;
const DWORD c_Equipment_CostumeBody = c_Equipment_Start + CItemData::WEAR_COSTUME_BODY;
const DWORD c_Equipment_CostumeHair = c_Equipment_Start + CItemData::WEAR_COSTUME_HAIR;
#ifdef ENABLE_MOUNT_COSTUME_SYSTEM
const DWORD c_Equipment_Mount = c_Equipment_Start + CItemData::WEAR_COSTUME_MOUNT;
#endif
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
const DWORD c_Equipment_Acce = c_Equipment_Start + CItemData::WEAR_COSTUME_ACCE;
#endif
#ifdef ENABLE_NEW_EQUIPMENT_SYSTEM
const DWORD c_Equipment_Belt = c_Equipment_Start + CItemData::WEAR_BELT;
#endif
#ifdef ENABLE_WEAPON_COSTUME_SYSTEM
const DWORD c_Equipment_CostumeWeapon = c_Equipment_Start + CItemData::WEAR_COSTUME_WEAPON;
#endif
#ifdef ENABLE_PET_COSTUME_SYSTEM
const DWORD c_Equipment_Pet = c_Equipment_Start + CItemData::WEAR_PET;
#endif
#ifdef ENABLE_AURA_SYSTEM
const DWORD c_Costume_Slot_Aura = c_Equipment_Start + CItemData::WEAR_COSTUME_AURA;
#endif
#ifdef ENABLE_ACCE_COSTUME_SKIN
const DWORD c_Costume_Slot_Wing = c_Equipment_Start + CItemData::WEAR_COSTUME_WING;
#endif
#ifdef ENABLE_MOUNT_SKIN
const DWORD c_Mount_Skin_Slot = c_Equipment_Start + CItemData::WEAR_MOUNT_SKIN;
#endif
#ifdef ENABLE_PET_SKIN
const DWORD c_Pet_Skin_Slot = c_Equipment_Start + CItemData::WEAR_PET_SKIN;
#endif
#ifdef ENABLE_CROWN_SYSTEM
const DWORD c_Equipment_Crown = c_Equipment_Start + CItemData::WEAR_CROWN;
#endif

#ifdef ENABLE_ITEMS_SHINING
const DWORD c_Shining_Wrist_Left = c_Equipment_Start + CItemData::WEAR_SHINING_WRIST_LEFT;
const DWORD c_Shining_Wrist_Right = c_Equipment_Start + CItemData::WEAR_SHINING_WRIST_RIGHT;
const DWORD c_Shining_Armor = c_Equipment_Start + CItemData::WEAR_SHINING_ARMOR;
#endif

#ifdef ENABLE_BOOSTER_ITEM
const DWORD c_Booster_Weapon = c_Equipment_Start + CItemData::WEAR_BOOSTER_WEAPON;
const DWORD c_Booster_Body = c_Equipment_Start + CItemData::WEAR_BOOSTER_BODY;
const DWORD c_Booster_Head = c_Equipment_Start + CItemData::WEAR_BOOSTER_HEAD;
const DWORD c_Booster_Sash = c_Equipment_Start + CItemData::WEAR_BOOSTER_SASH;
const DWORD c_Booster_Pet = c_Equipment_Start + CItemData::WEAR_BOOSTER_PET;
const DWORD c_Booster_Mount = c_Equipment_Start + CItemData::WEAR_BOOSTER_MOUNT;
#endif

#ifdef ENABLE_NEW_PET_SYSTEM
const DWORD c_NewPet = c_Equipment_Start + CItemData::WEAR_NEW_PET;
#endif

#ifdef ENABLE_PENDANT_ITEM
const DWORD c_Equipment_Pendant = c_Equipment_Start + CItemData::WEAR_PENDANT;
#endif
#ifdef ENABLE_GLOVE_ITEM
const DWORD c_Equipment_Glove = c_Equipment_Start + CItemData::WEAR_GLOVE;
#endif

#ifdef ENABLE_RINGS
const DWORD c_Equipment_Rings_0 = c_Equipment_Start + CItemData::WEAR_RING_0;
const DWORD c_Equipment_Rings_1 = c_Equipment_Start + CItemData::WEAR_RING_1;
const DWORD c_Equipment_Rings_2 = c_Equipment_Start + CItemData::WEAR_RING_2;
const DWORD c_Equipment_Rings_3 = c_Equipment_Start + CItemData::WEAR_RING_3;
const DWORD c_Equipment_Rings_4 = c_Equipment_Start + CItemData::WEAR_RING_4;
const DWORD c_Equipment_Rings_5 = c_Equipment_Start + CItemData::WEAR_RING_5;
const DWORD c_Equipment_Rings_6 = c_Equipment_Start + CItemData::WEAR_RING_6;
const DWORD c_Equipment_Rings_7 = c_Equipment_Start + CItemData::WEAR_RING_7;
#endif

#ifdef ENABLE_AURA_SKIN
const DWORD c_Equipment_AuraSkin = c_Equipment_Start + CItemData::WEAR_AURA_SKIN;
#endif

#ifdef ENABLE_DREAMSOUL
const DWORD c_DreamSoul_Red = c_Equipment_Start + CItemData::WEAR_DREAMSOUL_RED;
const DWORD c_DreamSoul_Blue = c_Equipment_Start + CItemData::WEAR_DREAMSOUL_BLUE;
#endif

enum EDragonSoulDeckType
{
	DS_DECK_1,
	DS_DECK_2,
	DS_DECK_MAX_NUM = 2,
};

enum EDragonSoulGradeTypes
{
	DRAGON_SOUL_GRADE_NORMAL,
	DRAGON_SOUL_GRADE_BRILLIANT,
	DRAGON_SOUL_GRADE_RARE,
	DRAGON_SOUL_GRADE_ANCIENT,
	DRAGON_SOUL_GRADE_LEGENDARY,
#ifdef ENABLE_DS_GRADE_MYTH
	DRAGON_SOUL_GRADE_MYTH,
#endif
	DRAGON_SOUL_GRADE_MAX,
};

enum EDragonSoulStepTypes
{
	DRAGON_SOUL_STEP_LOWEST,
	DRAGON_SOUL_STEP_LOW,
	DRAGON_SOUL_STEP_MID,
	DRAGON_SOUL_STEP_HIGH,
	DRAGON_SOUL_STEP_HIGHEST,
	DRAGON_SOUL_STEP_MAX,
};

#ifdef WJ_ENABLE_TRADABLE_ICON
enum ETopWindowTypes
{
	ON_TOP_WND_NONE,
	ON_TOP_WND_SHOP,
	ON_TOP_WND_EXCHANGE,
	ON_TOP_WND_SAFEBOX,
	ON_TOP_WND_PRIVATE_SHOP,
#ifdef ENABLE_FISH_EVENT
	ON_TOP_WND_FISH_EVENT,
#endif
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	ON_TOP_WND_ACCE_COMBINE,
	ON_TOP_WND_ACCE_ABSORB,
#endif
#ifdef ENABLE_OFFLINE_SHOP
	ON_TOP_WND_OFFLINE_SHOP,
#endif
	ON_TOP_WND_DICE,
	ON_TOP_WND_DRAGON_SOUL,
#ifdef ENABLE_6TH_7TH_ATTR
	ON_TOP_WND_ATTR_67,
#endif
	ON_TOP_WND_MAX,
};
#endif

const DWORD c_Wear_Max = CItemData::WEAR_MAX_NUM;
const DWORD c_DragonSoul_Equip_Start = c_ItemSlot_Count + c_Wear_Max;
const DWORD c_DragonSoul_Equip_Slot_Max = 6;
const DWORD c_DragonSoul_Equip_End = c_DragonSoul_Equip_Start + c_DragonSoul_Equip_Slot_Max * DS_DECK_MAX_NUM;

const DWORD c_DragonSoul_Equip_Reserved_Count = c_DragonSoul_Equip_Slot_Max * 3;

#ifdef ENABLE_NEW_EQUIPMENT_SYSTEM
const DWORD c_Belt_Inventory_Slot_Start = c_DragonSoul_Equip_End + c_DragonSoul_Equip_Reserved_Count;
const DWORD c_Belt_Inventory_Width = 4;
const DWORD c_Belt_Inventory_Height = 4;
const DWORD c_Belt_Inventory_Slot_Count = c_Belt_Inventory_Width * c_Belt_Inventory_Height;
const DWORD c_Belt_Inventory_Slot_End = c_Belt_Inventory_Slot_Start + c_Belt_Inventory_Slot_Count;

const DWORD c_Inventory_Count = c_Belt_Inventory_Slot_End;
#else
const DWORD c_Inventory_Count = c_DragonSoul_Equip_End;
#endif

const DWORD c_DragonSoul_Inventory_Start = 0;
const DWORD c_DragonSoul_Inventory_Box_Size = 32;
const DWORD c_DragonSoul_Inventory_Count = CItemData::DS_SLOT_NUM_TYPES * DRAGON_SOUL_GRADE_MAX * c_DragonSoul_Inventory_Box_Size;
const DWORD c_DragonSoul_Inventory_End = c_DragonSoul_Inventory_Start + c_DragonSoul_Inventory_Count;

#ifdef ENABLE_SPECIAL_STORAGE
const DWORD c_Special_Inventory_Page_Size = 5 * 9;
const DWORD c_Special_Inventory_Page_Count = 5;
const DWORD c_Special_ItemSlot_Count = c_Special_Inventory_Page_Size * c_Special_Inventory_Page_Count;
#endif

enum ESlotType
{
	SLOT_TYPE_NONE,
	SLOT_TYPE_INVENTORY,
	SLOT_TYPE_SKILL,
	SLOT_TYPE_EMOTION,
	SLOT_TYPE_SHOP,
	SLOT_TYPE_EXCHANGE_OWNER,
	SLOT_TYPE_EXCHANGE_TARGET,
	SLOT_TYPE_QUICK_SLOT,
	SLOT_TYPE_SAFEBOX,
	SLOT_TYPE_PRIVATE_SHOP,
	SLOT_TYPE_MALL,
	SLOT_TYPE_DRAGON_SOUL_INVENTORY,
#ifdef ENABLE_SPECIAL_STORAGE
	SLOT_TYPE_UPGRADE_INVENTORY,
	SLOT_TYPE_BOOK_INVENTORY,
	SLOT_TYPE_STONE_INVENTORY,
	SLOT_TYPE_CHEST_INVENTORY,
#endif
#ifdef ENABLE_SWITCHBOT
	SLOT_TYPE_SWITCHBOT,
#endif
#ifdef ENABLE_BUFFI_SYSTEM
	SLOT_TYPE_BUFFI_INVENTORY,
#endif
	SLOT_TYPE_MAX,
};

enum EWindows
{
	RESERVED_WINDOW,
	INVENTORY,
	EQUIPMENT,
	SAFEBOX,
	MALL,
	DRAGON_SOUL_INVENTORY,
#ifdef ENABLE_SPECIAL_STORAGE
	UPGRADE_INVENTORY,
	BOOK_INVENTORY,
	STONE_INVENTORY,
	CHEST_INVENTORY,
#endif
#ifdef ENABLE_SWITCHBOT
	SWITCHBOT,
#endif
#ifdef ENABLE_6TH_7TH_ATTR
	ATTR_INVENTORY,
#endif
	BELT_INVENTORY,
#ifdef ENABLE_BUFFI_SYSTEM
	BUFFI_INVENTORY,
#endif
	GROUND,
#ifdef ENABLE_OFFLINE_SHOP
	NEW_OFFSHOP,
	SHOP_SAFEBOX,
#endif
	WINDOW_TYPE_MAX,
};

enum EDSInventoryMaxNum
{
	DS_INVENTORY_MAX_NUM = c_DragonSoul_Inventory_Count,
	DS_REFINE_WINDOW_MAX_NUM = 15,
};

#pragma pack (push, 1)
#define WORD_MAX 0xffff

#ifdef ENABLE_SWITCHBOT
enum ESwitchbotValues
{
	SWITCHBOT_SLOT_COUNT = 5,
	SWITCHBOT_ALTERNATIVE_COUNT = 2,
	MAX_NORM_ATTR_NUM = 5,
};

enum EAttributeSet
{
	ATTRIBUTE_SET_WEAPON,
	ATTRIBUTE_SET_BODY,
	ATTRIBUTE_SET_WRIST,
	ATTRIBUTE_SET_FOOTS,
	ATTRIBUTE_SET_NECK,
	ATTRIBUTE_SET_HEAD,
	ATTRIBUTE_SET_SHIELD,
	ATTRIBUTE_SET_EAR,
	ATTRIBUTE_SET_MAX_NUM,
};

#endif

#ifdef ENABLE_BUFFI_SYSTEM
enum EBuffiWindow
{
	BUFFI_WEAPON_SLOT,
	BUFFI_BODY_SLOT,
	BUFFI_HAIR_SLOT,
	BUFFI_ACCE_SLOT,
	BUFFI_AURA_SLOT,
	BUFFI_MAX_SLOT
};
#endif

typedef struct SItemPos
{
	BYTE window_type;
	WORD cell;
	SItemPos()
	{
		window_type = INVENTORY;
		cell = WORD_MAX;
	}
	SItemPos(BYTE _window_type, WORD _cell)
	{
		window_type = _window_type;
		cell = _cell;
	}

	bool IsValidCell()
	{
		switch (window_type)
		{
		case INVENTORY:
			return cell < c_Inventory_Count;
			break;
		case EQUIPMENT:
			return cell < c_DragonSoul_Equip_End;
			break;
		case DRAGON_SOUL_INVENTORY:
			return cell < (DS_INVENTORY_MAX_NUM);
			break;
#ifdef ENABLE_SPECIAL_STORAGE
		case UPGRADE_INVENTORY:
			return cell < c_Special_ItemSlot_Count;
			break;
		case BOOK_INVENTORY:
			return cell < c_Special_ItemSlot_Count;
			break;
		case STONE_INVENTORY:
			return cell < c_Special_ItemSlot_Count;
			break;
		case CHEST_INVENTORY:
			return cell < c_Special_ItemSlot_Count;
			break;
#endif
#ifdef ENABLE_SWITCHBOT
		case SWITCHBOT:
			return cell < SWITCHBOT_SLOT_COUNT;
			break;
#endif
#ifdef ENABLE_BUFFI_SYSTEM
		case BUFFI_INVENTORY:
			return cell < BUFFI_MAX_SLOT;
			break;
#endif
		default:
			return false;
		}
	}
	bool IsEquipCell()
	{
		switch (window_type)
		{
		case INVENTORY:
		case EQUIPMENT:
			return (c_Equipment_Start + c_Wear_Max > cell) && (c_Equipment_Start <= cell);
			break;

		case BELT_INVENTORY:
		case DRAGON_SOUL_INVENTORY:
#ifdef ENABLE_SPECIAL_STORAGE
		case UPGRADE_INVENTORY:
		case BOOK_INVENTORY:
		case STONE_INVENTORY:
		case CHEST_INVENTORY:
#endif
			return false;
			break;

		default:
			return false;
		}
	}

#ifdef ENABLE_NEW_EQUIPMENT_SYSTEM
	bool IsBeltInventoryCell()
	{
		bool bResult = c_Belt_Inventory_Slot_Start <= cell && c_Belt_Inventory_Slot_End > cell;
		return bResult;
	}
#endif

	bool operator==(const struct SItemPos& rhs) const
	{
		return (window_type == rhs.window_type) && (cell == rhs.cell);
	}

	bool operator<(const struct SItemPos& rhs) const
	{
		return (window_type < rhs.window_type) || ((window_type == rhs.window_type) && (cell < rhs.cell));
	}
} TItemPos;
#pragma pack(pop)

const DWORD c_QuickBar_Line_Count = 3;
const DWORD c_QuickBar_Slot_Count = 12;

const float c_Idle_WaitTime = 5.0f;

const int c_Monster_Race_Start_Number = 6;
const int c_Monster_Model_Start_Number = 20001;

const float c_fAttack_Delay_Time = 0.2f;
const float c_fHit_Delay_Time = 0.1f;
const float c_fCrash_Wave_Time = 0.2f;
const float c_fCrash_Wave_Distance = 3.0f;

const float c_fHeight_Step_Distance = 50.0f;

enum
{
	DISTANCE_TYPE_FOUR_WAY,
	DISTANCE_TYPE_EIGHT_WAY,
	DISTANCE_TYPE_ONE_WAY,
	DISTANCE_TYPE_MAX_NUM,
};

const float c_fMagic_Script_Version = 1.0f;
const float c_fSkill_Script_Version = 1.0f;
const float c_fBattleCommand_Script_Version = 1.0f;
const float c_fEmotionCommand_Script_Version = 1.0f;
const float c_fActive_Script_Version = 1.0f;
const float c_fPassive_Script_Version = 1.0f;

// Used by PushMove
const float c_fWalkDistance = 175.0f;
const float c_fRunDistance = 310.0f;

#define FILE_MAX_LEN 128

enum
{
#ifdef ENABLE_SOCKET_LIMIT_5
	ITEM_SOCKET_SLOT_MAX_NUM = 6,
#else
	ITEM_SOCKET_SLOT_MAX_NUM = 3,
#endif
	// refactored attribute slot begin
	ITEM_ATTRIBUTE_SLOT_NORM_NUM = 5,
	ITEM_ATTRIBUTE_SLOT_RARE_NUM = 2,

	ITEM_ATTRIBUTE_SLOT_NORM_START = 0,
	ITEM_ATTRIBUTE_SLOT_NORM_END = ITEM_ATTRIBUTE_SLOT_NORM_START + ITEM_ATTRIBUTE_SLOT_NORM_NUM,

	ITEM_ATTRIBUTE_SLOT_RARE_START = ITEM_ATTRIBUTE_SLOT_NORM_END,
	ITEM_ATTRIBUTE_SLOT_RARE_END = ITEM_ATTRIBUTE_SLOT_RARE_START + ITEM_ATTRIBUTE_SLOT_RARE_NUM,

#ifdef ENABLE_ITEM_TABLE_ATTR_LIMIT
	ITEM_ATTRIBUTE_SLOT_MAX_NUM = 10, // 7
#else
	ITEM_ATTRIBUTE_SLOT_MAX_NUM = ITEM_ATTRIBUTE_SLOT_RARE_END, // 7
#endif
	// refactored attribute slot end
};

#pragma pack(push)
#pragma pack(1)

typedef struct SQuickSlot
{
	BYTE Type;
	QS_USHORT Position;
} TQuickSlot;

typedef struct TPlayerItemAttribute
{
	BYTE        bType;
	short       sValue;
} TPlayerItemAttribute;

typedef struct packet_item
{
	DWORD       vnum;
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	count;
#else
	BYTE		count;
#endif
	DWORD		flags;
	DWORD		anti_flags;
	long		alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
} TItemData;

#ifdef ENABLE_BUY_WITH_ITEMS
typedef struct SShopItemPriceData
{
	uint32_t		vnum;
	uint32_t		count;
} TShopItemPriceData;
#endif

typedef struct packet_shop_item
{
	DWORD		vnum;
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t		price;
#else
	DWORD		price;
#endif
#ifdef ENABLE_EXTENDED_COUNT_ITEMS
	MAX_COUNT	count;
#else
	BYTE		count;
#endif
#ifdef ENABLE_BUY_WITH_ITEMS
	TShopItemPriceData	itemPrice[MAX_SHOP_PRICES];
#endif
	BYTE		display_pos;
	long		alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
} TShopItemData;

#ifdef ENABLE_EXTENDED_BATTLE_PASS
typedef struct SExtBattlePassRewardItem
{
	DWORD dwVnum;
	BYTE bCount;
} TExtBattlePassRewardItem;

typedef struct SExtBattlePassMissionInfo
{
	BYTE bMissionIndex;
	BYTE bMissionType;
	DWORD dwMissionInfo[3];
	TExtBattlePassRewardItem aRewardList[3];
} TExtBattlePassMissionInfo;

typedef struct SExtBattlePassRanking
{
	BYTE bPos;
	char playerName[24 + 1];
	DWORD dwFinishTime;
} TExtBattlePassRanking;
#endif

#pragma pack(pop)

inline float GetSqrtDistance(int ix1, int iy1, int ix2, int iy2) // By sqrt
{
	float dx, dy;

	dx = float(ix1 - ix2);
	dy = float(iy1 - iy2);

	return sqrtf(dx * dx + dy * dy);
}

// DEFAULT_FONT
void DefaultFont_Startup();
void DefaultFont_Cleanup();
void DefaultFont_SetName(const char* c_szFontName);
CResource* DefaultFont_GetResource();
CResource* DefaultItalicFont_GetResource();
// END_OF_DEFAULT_FONT

void SetGuildSymbolPath(const char* c_szPathName);
const char* GetGuildSymbolFileName(DWORD dwGuildID);
BYTE ApplyTypeToPointType(BYTE bApplyType);
BYTE SlotTypeToInvenType(BYTE bSlotType);
std::pair<BYTE, BYTE> StringApplyToPoint(const char* apply_type_string);