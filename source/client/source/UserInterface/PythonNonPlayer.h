#pragma once
#include "StdAfx.h"
// #define ENABLE_NEW_MOB_PROTO_STRUCT_20141125	// bleeding resistance 2014/11/25
// #define ENABLE_NEW_MOB_PROTO_STRUCT_20151020	// claw resistance 2015/10/20

class CPythonNonPlayer : public CSingleton<CPythonNonPlayer>
{
public:

	enum EMobTypes
	{
		MONSTER,
		NPC,
		STONE,
		WARP,
		DOOR,
		BUILDING,
		PC,
		POLYMORPH_PC,
		HORSE,
		GOTO
	};

#ifdef ENABLE_PRESENT_NPC
	enum presentNPC
	{
		NPC_WEAR_RACE,
		NPC_WEAR_WEAPON,
		NPC_WEAR_ARMOR,
		NPC_WEAR_HAIR,
		NPC_WEAR_ACCE,
		NPC_WEAR_MOUNT,
		NPC_WEAR_SHINING_WEAPON,
		NPC_WEAR_SHINING_ARMOR,
		NPC_WEAR_SHINING_SPECIAL,
		NPC_WEAR_SHINING_WING,
		NPC_WEAR_MAX,
	};
#endif

	enum EClickEvent
	{
		ON_CLICK_EVENT_NONE = 0,
		ON_CLICK_EVENT_BATTLE = 1,
		ON_CLICK_EVENT_SHOP = 2,
		ON_CLICK_EVENT_TALK = 3,
		ON_CLICK_EVENT_VEHICLE = 4,

		ON_CLICK_EVENT_MAX_NUM,
	};

#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
	enum EAIFlags
	{
		AIFLAG_AGGRESSIVE = (1 << 0),
		AIFLAG_NOMOVE = (1 << 1),
		AIFLAG_COWARD = (1 << 2),
		AIFLAG_NOATTACKSHINSU = (1 << 3),
		AIFLAG_NOATTACKJINNO = (1 << 4),
		AIFLAG_NOATTACKCHUNJO = (1 << 5),
		AIFLAG_ATTACKMOB = (1 << 6),
		AIFLAG_BERSERK = (1 << 7),
		AIFLAG_STONESKIN = (1 << 8),
		AIFLAG_GODSPEED = (1 << 9),
		AIFLAG_DEATHBLOW = (1 << 10),
		AIFLAG_REVIVE = (1 << 11),
	};
#endif

	enum EMobEnchants
	{
		MOB_ENCHANT_CURSE,
		MOB_ENCHANT_SLOW,
		MOB_ENCHANT_POISON,
		MOB_ENCHANT_STUN,
		MOB_ENCHANT_CRITICAL,
		MOB_ENCHANT_PENETRATE,
		MOB_ENCHANTS_MAX_NUM
	};
	enum EMobResists
	{
		MOB_RESIST_SWORD,
		MOB_RESIST_TWOHAND,
		MOB_RESIST_DAGGER,
		MOB_RESIST_BELL,
		MOB_RESIST_FAN,
		MOB_RESIST_BOW,
		MOB_RESIST_FIRE,
		MOB_RESIST_ELECT,
		MOB_RESIST_MAGIC,
		MOB_RESIST_WIND,
		MOB_RESIST_POISON,
		MOB_RESISTS_MAX_NUM
	};

	enum EMobRank
	{
		MOB_RANK_PAWN = 0,
		MOB_RANK_S_PAWN = 1,
		MOB_RANK_KNIGHT = 2,
		MOB_RANK_S_KNIGHT = 3,
		MOB_RANK_BOSS = 4,
		MOB_RANK_KING = 5,
	};

	enum EMobMaxNum
	{
		MOB_ATTRIBUTE_MAX_NUM = 12,
		MOB_SKILL_MAX_NUM = 5,
	};


	enum ERaceFlags
	{
		RACE_FLAG_ANIMAL = (1 << 0),
		RACE_FLAG_UNDEAD = (1 << 1),
		RACE_FLAG_DEVIL = (1 << 2),
		RACE_FLAG_HUMAN = (1 << 3),
		RACE_FLAG_ORC = (1 << 4),
		RACE_FLAG_MILGYO = (1 << 5),
		RACE_FLAG_INSECT = (1 << 6),
		RACE_FLAG_FIRE = (1 << 7),
		RACE_FLAG_ICE = (1 << 8),
		RACE_FLAG_DESERT = (1 << 9),
		RACE_FLAG_TREE = (1 << 10),
		RACE_FLAG_ATT_ELEC = (1 << 11),
		RACE_FLAG_ATT_FIRE = (1 << 12),
		RACE_FLAG_ATT_ICE = (1 << 13),
		RACE_FLAG_ATT_WIND = (1 << 14),
		RACE_FLAG_ATT_EARTH = (1 << 15),
		RACE_FLAG_ATT_DARK = (1 << 16),
		RACE_FLAG_ATT_CZ = (1 << 17),
		RACE_FLAG_MAX_NUM	= 18,
	};

#pragma pack(push)
#pragma pack(1)
	typedef struct SMobSkillLevel
	{
		DWORD       dwVnum;
		BYTE        bLevel;
	} TMobSkillLevel;

	typedef struct SMobTable_r235
	{
		enum EMobMaxNum
		{
			MOB_ATTRIBUTE_MAX_NUM = 12,
			MOB_SKILL_MAX_NUM = 1,//r1
		};

		DWORD       dwVnum;
		char        szName[CHARACTER_NAME_MAX_LEN + 1];
		char        szLocaleName[CHARACTER_NAME_MAX_LEN + 1];

		BYTE        bType;                  // Monster, NPC
		BYTE        bRank;                  // PAWN, KNIGHT, KING
		BYTE        bBattleType;            // MELEE, etc..
		BYTE        bLevel;                 // Level
		BYTE        bSize;

		DWORD       dwGoldMin;
		DWORD       dwGoldMax;
		DWORD       dwExp;
		HP_ULL       dwMaxHP;
		BYTE        bRegenCycle;
		BYTE        bRegenPercent;
		WORD        wDef;

		DWORD       dwAIFlag;
		DWORD       dwRaceFlag;
		DWORD       dwImmuneFlag;

		BYTE        bStr, bDex, bCon, bInt;
		DWORD       dwDamageRange[2];

		short       sAttackSpeed;
		short       sMovingSpeed;
		BYTE        bAggresiveHPPct;
		WORD        wAggressiveSight;
		WORD        wAttackRange;

		char        cEnchants[MOB_ENCHANTS_MAX_NUM];
		char        cResists[MOB_RESISTS_MAX_NUM];

		DWORD       dwResurrectionVnum;
		DWORD       dwDropItemVnum;

		BYTE        bMountCapacity;
		BYTE        bOnClickType;

		BYTE        bEmpire;
		char        szFolder[64 + 1];
		float       fDamMultiply;
		DWORD       dwSummonVnum;
		DWORD       dwDrainSP;
		DWORD		dwMonsterColor;
		DWORD       dwPolymorphItemVnum;

		TMobSkillLevel	Skills[SMobTable_r235::MOB_SKILL_MAX_NUM];

		BYTE		bBerserkPoint;
		BYTE		bStoneSkinPoint;
		BYTE		bGodSpeedPoint;
		BYTE		bDeathBlowPoint;
		BYTE		bRevivePoint;
	} TMobTable_r235;

	typedef struct SMobTable_r255
	{
		DWORD       dwVnum;
		char        szName[CHARACTER_NAME_MAX_LEN + 1];
		char        szLocaleName[CHARACTER_NAME_MAX_LEN + 1];

		BYTE        bType;                  // Monster, NPC
		BYTE        bRank;                  // PAWN, KNIGHT, KING
		BYTE        bBattleType;            // MELEE, etc..
		BYTE        bLevel;                 // Level
		BYTE        bSize;

		DWORD       dwGoldMin;
		DWORD       dwGoldMax;
		DWORD       dwExp;
		HP_ULL       dwMaxHP;
		BYTE        bRegenCycle;
		BYTE        bRegenPercent;
		WORD        wDef;

		DWORD       dwAIFlag;
		DWORD       dwRaceFlag;
		DWORD       dwImmuneFlag;

		BYTE        bStr, bDex, bCon, bInt;
		DWORD       dwDamageRange[2];

		short       sAttackSpeed;
		short       sMovingSpeed;
		BYTE        bAggresiveHPPct;
		WORD        wAggressiveSight;
		WORD        wAttackRange;

		char        cEnchants[MOB_ENCHANTS_MAX_NUM];
		char        cResists[MOB_RESISTS_MAX_NUM];

		DWORD       dwResurrectionVnum;
		DWORD       dwDropItemVnum;

		BYTE        bMountCapacity;
		BYTE        bOnClickType;

		BYTE        bEmpire;
		char        szFolder[64 + 1];
		float       fDamMultiply;
		DWORD       dwSummonVnum;
		DWORD       dwDrainSP;
		DWORD		dwMonsterColor;
		DWORD       dwPolymorphItemVnum;

		TMobSkillLevel	Skills[MOB_SKILL_MAX_NUM];

		BYTE		bBerserkPoint;
		BYTE		bStoneSkinPoint;
		BYTE		bGodSpeedPoint;
		BYTE		bDeathBlowPoint;
		BYTE		bRevivePoint;
	} TMobTable_r255;

	typedef struct SMobTable_r256
	{
		enum EMobResists_r3
		{
			MOB_RESIST_SWORD,
			MOB_RESIST_TWOHAND,
			MOB_RESIST_DAGGER,
			MOB_RESIST_BELL,
			MOB_RESIST_FAN,
			MOB_RESIST_BOW,
			MOB_RESIST_FIRE,
			MOB_RESIST_ELECT,
			MOB_RESIST_MAGIC,
			MOB_RESIST_WIND,
			MOB_RESIST_POISON,
			MOB_RESIST_BLEEDING,//r3
			MOB_RESISTS_MAX_NUM
		};

		DWORD       dwVnum;
		char        szName[CHARACTER_NAME_MAX_LEN + 1];
		char        szLocaleName[CHARACTER_NAME_MAX_LEN + 1];

		BYTE        bType;                  // Monster, NPC
		BYTE        bRank;                  // PAWN, KNIGHT, KING
		BYTE        bBattleType;            // MELEE, etc..
		BYTE        bLevel;                 // Level
		BYTE        bSize;

		DWORD       dwGoldMin;
		DWORD       dwGoldMax;
		DWORD       dwExp;
		HP_ULL       dwMaxHP;
		BYTE        bRegenCycle;
		BYTE        bRegenPercent;
		WORD        wDef;

		DWORD       dwAIFlag;
		DWORD       dwRaceFlag;
		DWORD       dwImmuneFlag;

		BYTE        bStr, bDex, bCon, bInt;
		DWORD       dwDamageRange[2];

		short       sAttackSpeed;
		short       sMovingSpeed;
		BYTE        bAggresiveHPPct;
		WORD        wAggressiveSight;
		WORD        wAttackRange;

		char        cEnchants[MOB_ENCHANTS_MAX_NUM];
		char        cResists[SMobTable_r256::MOB_RESISTS_MAX_NUM];

		DWORD       dwResurrectionVnum;
		DWORD       dwDropItemVnum;

		BYTE        bMountCapacity;
		BYTE        bOnClickType;

		BYTE        bEmpire;
		char        szFolder[64 + 1];
		float       fDamMultiply;
		DWORD       dwSummonVnum;
		DWORD       dwDrainSP;
		DWORD		dwMonsterColor;
		DWORD       dwPolymorphItemVnum;

		TMobSkillLevel	Skills[MOB_SKILL_MAX_NUM];

		BYTE		bBerserkPoint;
		BYTE		bStoneSkinPoint;
		BYTE		bGodSpeedPoint;
		BYTE		bDeathBlowPoint;
		BYTE		bRevivePoint;
	} TMobTable_r256;

	typedef struct SMobTable_r262
	{
		enum EMobResists_r4
		{
			MOB_RESIST_SWORD,
			MOB_RESIST_TWOHAND,
			MOB_RESIST_DAGGER,
			MOB_RESIST_BELL,
			MOB_RESIST_FAN,
			MOB_RESIST_BOW,
			MOB_RESIST_CLAW,//r4
			MOB_RESIST_FIRE,
			MOB_RESIST_ELECT,
			MOB_RESIST_MAGIC,
			MOB_RESIST_WIND,
			MOB_RESIST_POISON,
			MOB_RESIST_BLEEDING,//r3
			MOB_RESISTS_MAX_NUM
		};

		DWORD       dwVnum;
		char        szName[CHARACTER_NAME_MAX_LEN + 1];
		char        szLocaleName[CHARACTER_NAME_MAX_LEN + 1];

		BYTE        bType;                  // Monster, NPC
		BYTE        bRank;                  // PAWN, KNIGHT, KING
		BYTE        bBattleType;            // MELEE, etc..
		BYTE        bLevel;                 // Level
		BYTE		bLvlPct;
		BYTE        bSize;//r4

		DWORD       dwGoldMin;
		DWORD       dwGoldMax;
		DWORD       dwExp;
		HP_ULL       dwMaxHP;
		BYTE        bRegenCycle;
		BYTE        bRegenPercent;
		WORD        wDef;

		DWORD       dwAIFlag;
		DWORD       dwRaceFlag;
		DWORD       dwImmuneFlag;

		BYTE        bStr, bDex, bCon, bInt;
		DWORD       dwDamageRange[2];

		short       sAttackSpeed;
		short       sMovingSpeed;
		BYTE        bAggresiveHPPct;
		WORD        wAggressiveSight;
		WORD        wAttackRange;

		char        cEnchants[MOB_ENCHANTS_MAX_NUM];
		char        cResists[SMobTable_r262::MOB_RESISTS_MAX_NUM];

		DWORD       dwResurrectionVnum;
		DWORD       dwDropItemVnum;

		BYTE        bMountCapacity;
		BYTE        bOnClickType;

		BYTE        bEmpire;
		char        szFolder[64 + 1];
		float       fDamMultiply;
		DWORD       dwSummonVnum;
		DWORD       dwDrainSP;
		DWORD		dwMonsterColor;
		DWORD       dwPolymorphItemVnum;

		TMobSkillLevel	Skills[MOB_SKILL_MAX_NUM];

		BYTE		bBerserkPoint;
		BYTE		bStoneSkinPoint;
		BYTE		bGodSpeedPoint;
		BYTE		bDeathBlowPoint;
		BYTE		bRevivePoint;

		DWORD		dwHealerPoint;//r4
	} TMobTable_r262;

	typedef struct SMobTable_r263
	{
		enum EMobResists_r5
		{
			MOB_RESIST_SWORD,
			MOB_RESIST_TWOHAND,
			MOB_RESIST_DAGGER,
			MOB_RESIST_BELL,
			MOB_RESIST_FAN,
			MOB_RESIST_BOW,
			MOB_RESIST_CLAW,//r4
			MOB_RESIST_FIRE,
			MOB_RESIST_ELECT,
			MOB_RESIST_MAGIC,
			MOB_RESIST_WIND,
			MOB_RESIST_POISON,
			MOB_RESIST_BLEEDING,//r3
			MOB_RESISTS_MAX_NUM
		};

		DWORD       dwVnum;
		char        szName[CHARACTER_NAME_MAX_LEN + 1];
		char        szLocaleName[CHARACTER_NAME_MAX_LEN + 1];

		BYTE        bType;                  // Monster, NPC
		BYTE        bRank;                  // PAWN, KNIGHT, KING
		BYTE        bBattleType;            // MELEE, etc..
		BYTE        bLevel;                 // Level
		BYTE		bLvlPct;
		BYTE        bSize;//r4

		DWORD       dwGoldMin;
		DWORD       dwGoldMax;
		DWORD       dwExp;
		HP_ULL       dwMaxHP;
		BYTE        bRegenCycle;
		BYTE        bRegenPercent;
		WORD        wDef;

		DWORD       dwAIFlag;
		DWORD       dwRaceFlag;
		DWORD       dwImmuneFlag;

		BYTE        bStr, bDex, bCon, bInt;
		DWORD       dwDamageRange[2];

		short       sAttackSpeed;
		short       sMovingSpeed;
		BYTE        bAggresiveHPPct;
		WORD        wAggressiveSight;
		WORD        wAttackRange;

		char        cEnchants[MOB_ENCHANTS_MAX_NUM];
		char        cResists[SMobTable_r263::MOB_RESISTS_MAX_NUM];

		DWORD       dwResurrectionVnum;
		DWORD       dwDropItemVnum;

		BYTE        bMountCapacity;
		BYTE        bOnClickType;

		BYTE        bEmpire;
		char        szFolder[64 + 1];
		float       fDamMultiply;
		DWORD       dwSummonVnum;
		DWORD       dwDrainSP;
		DWORD		dwMonsterColor;
		DWORD       dwPolymorphItemVnum;

		TMobSkillLevel	Skills[MOB_SKILL_MAX_NUM];

		BYTE		bBerserkPoint;
		BYTE		bStoneSkinPoint;
		BYTE		bGodSpeedPoint;
		BYTE		bDeathBlowPoint;
		BYTE		bRevivePoint;

		DWORD		dwHealerPoint;//r5
		BYTE		bUnk263;//r5
	} TMobTable_r263; //brazilian only 2016/08

	typedef TMobTable_r255 SMobTable, TMobTable;

#ifdef ENABLE_PROTOSTRUCT_AUTODETECT
	typedef struct SMobTableAll
	{
		static bool IsValidStruct(DWORD structSize)
		{
			switch (structSize)
			{
				case sizeof(TMobTable_r235) :
					case sizeof(TMobTable_r255) :
					case sizeof(TMobTable_r256) :
					case sizeof(TMobTable_r262) :
					case sizeof(TMobTable_r263) :
					return true;
					break;
			}
			return false;
		}

		static void Process(void* obj, DWORD structSize, DWORD i, CPythonNonPlayer::TMobTable& t)
		{
#define MTABLE_COPY_STR(x) strncpy_s(t.##x##, sizeof(t.##x##), r.##x##, _TRUNCATE)
#define MTABLE_COPY_INT(x) t.##x## = r.##x
#define MTABLE_COPY_FLT(x) t.##x## = r.##x
#define MTABLE_COUNT(x) _countof(t.##x##)
#define MTABLE_PROCESS(len)\
					CPythonNonPlayer::TMobTable_r##len## & r = *((CPythonNonPlayer::TMobTable_r##len## *) obj + i);\
					MTABLE_COPY_INT(dwVnum);\
					MTABLE_COPY_STR(szName);\
					MTABLE_COPY_STR(szLocaleName);\
					MTABLE_COPY_INT(bType);\
					MTABLE_COPY_INT(bRank);\
					MTABLE_COPY_INT(bBattleType);\
					MTABLE_COPY_INT(bLevel);\
					MTABLE_COPY_INT(bSize);\
					MTABLE_COPY_INT(dwGoldMin);\
					MTABLE_COPY_INT(dwGoldMax);\
					MTABLE_COPY_INT(dwExp);\
					MTABLE_COPY_INT(dwMaxHP);\
					MTABLE_COPY_INT(bRegenCycle);\
					MTABLE_COPY_INT(bRegenPercent);\
					MTABLE_COPY_INT(wDef);\
					MTABLE_COPY_INT(dwAIFlag);\
					MTABLE_COPY_INT(dwRaceFlag);\
					MTABLE_COPY_INT(dwImmuneFlag);\
					MTABLE_COPY_INT(bStr);\
					MTABLE_COPY_INT(bDex);\
					MTABLE_COPY_INT(bCon);\
					MTABLE_COPY_INT(bInt);\
					for (size_t i=0; i<MTABLE_COUNT(dwDamageRange); ++i)\
					{\
						MTABLE_COPY_INT(dwDamageRange[i]);\
					}\
					MTABLE_COPY_INT(sAttackSpeed);\
					MTABLE_COPY_INT(sMovingSpeed);\
					MTABLE_COPY_INT(bAggresiveHPPct);\
					MTABLE_COPY_INT(wAggressiveSight);\
					MTABLE_COPY_INT(wAttackRange);\
					for (size_t i=0; i<MTABLE_COUNT(cEnchants); ++i)\
					{\
						MTABLE_COPY_INT(cEnchants[i]);\
					}\
					for (size_t i=0; i<MTABLE_COUNT(cResists); ++i)\
					{\
						MTABLE_COPY_INT(cResists[i]);\
					}\
					MTABLE_COPY_INT(dwResurrectionVnum);\
					MTABLE_COPY_INT(dwDropItemVnum);\
					MTABLE_COPY_INT(bMountCapacity);\
					MTABLE_COPY_INT(bOnClickType);\
					MTABLE_COPY_INT(bEmpire);\
					MTABLE_COPY_STR(szFolder);\
					MTABLE_COPY_FLT(fDamMultiply);\
					MTABLE_COPY_INT(dwSummonVnum);\
					MTABLE_COPY_INT(dwDrainSP);\
					MTABLE_COPY_INT(dwMonsterColor);\
					MTABLE_COPY_INT(dwPolymorphItemVnum);\
					for (size_t i=0; i<MTABLE_COUNT(Skills); ++i)\
					{\
						MTABLE_COPY_INT(Skills[i].dwVnum);\
						MTABLE_COPY_INT(Skills[i].bLevel);\
					}\
					MTABLE_COPY_INT(bBerserkPoint);\
					MTABLE_COPY_INT(bStoneSkinPoint);\
					MTABLE_COPY_INT(bGodSpeedPoint);\
					MTABLE_COPY_INT(bDeathBlowPoint);\
					MTABLE_COPY_INT(bRevivePoint);

			switch (structSize)
			{
				case sizeof(TMobTable_r235) :
				{
					MTABLE_PROCESS(235);
				}
				break;
				case sizeof(TMobTable_r255) :
				{
					MTABLE_PROCESS(255);
				}
				break;
				case sizeof(TMobTable_r256) :
				{
					MTABLE_PROCESS(256);
				}
				break;
				case sizeof(TMobTable_r262) :
				{
					MTABLE_PROCESS(262);
				}
				break;
				case sizeof(TMobTable_r263) :
				{
					MTABLE_PROCESS(263);
				}
				break;
			}
		}
	} TMobTableAll;
#endif //ENABLE_PROTOSTRUCT_AUTODETECT

#pragma pack(pop)

#ifdef ENABLE_GLOBAL_SCALE
		typedef struct SMobScaleTable
		{
			DWORD	dwMobNum;
			float	fx;
			float	fy;
			float	fz;
			float	ra;
			float	rb;
		} TMobScaleTable;
		
		enum EMobScale
		{
			MOBSCALETABLE_MOB_NUM,
			MOBSCALETABLE_X,
			MOBSCALETABLE_Y,
			MOBSCALETABLE_Z,
			MOBSCALETABLE_RANDOM_A,
			MOBSCALETABLE_RANDOM_B,
			MOBSCALETABLE_MAX_NUM,
		};
		
		typedef std::map<DWORD, TMobScaleTable *> TNonMobScaleDataMap;
#endif

	typedef std::list<TMobTable*> TMobTableList;
	typedef std::map<DWORD, TMobTable*> TNonPlayerDataMap;

public:
	CPythonNonPlayer(void);
	virtual ~CPythonNonPlayer(void);

	void Clear();
	void Destroy();

	bool				LoadNonPlayerData(const char* c_szFileName);
#ifdef ENABLE_GLOBAL_SCALE
	bool				LoadMobScale(const char * c_szFileName);
	const TMobScaleTable *	GetScaleTable(DWORD dwVnum);
	bool				GetScale(DWORD dwVnum, float & fx, float & fy, float & fz);
#endif

	const TMobTable* GetTable(DWORD dwVnum);
	bool				GetName(DWORD dwVnum, const char** c_pszName);
	bool				GetInstanceType(DWORD dwVnum, BYTE* pbType);
	BYTE				GetEventType(DWORD dwVnum);
	BYTE				GetEventTypeByVID(DWORD dwVID);
	DWORD				GetMonsterColor(DWORD dwVnum);
	const char* GetMonsterName(DWORD dwVnum);

#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
	bool				IsAggressive(DWORD dwVnum);
#endif
#ifdef ENABLE_GLOBAL_SCALE
	uint8_t				GetMonsterScalePercent(uint32_t dwVnum);
#endif
#ifdef ENABLE_NEW_DISTANCE_CALC
	float				GetMonsterHitRange(uint32_t dwVnum);
#endif
#if defined(WJ_SHOW_MOB_INFO) || defined(ENABLE_TARGET_INFORMATION_SYSTEM)
	DWORD				GetMonsterLevel(DWORD dwVnum);
#endif
#ifdef ENABLE_TARGET_INFORMATION_SYSTEM
	HP_ULL				GetMonsterMaxHP(DWORD dwVnum);
	DWORD				GetMonsterRaceFlag(DWORD dwVnum);
	DWORD				GetMonsterDamage1(DWORD dwVnum);
	DWORD				GetMonsterDamage2(DWORD dwVnum);
	DWORD				GetMonsterExp(DWORD dwVnum);
	float				GetMonsterDamageMultiply(DWORD dwVnum);
	DWORD				GetMonsterST(DWORD dwVnum);
	DWORD				GetMonsterDX(DWORD dwVnum);
	bool				IsMonsterStone(DWORD dwVnum);
	DWORD				GetMobResist(DWORD dwVnum, BYTE bResistNum);
	BYTE				GetMobRegenCycle(DWORD dwVnum);
	BYTE				GetMobRegenPercent(DWORD dwVnum);
	DWORD				GetMobGoldMin(DWORD dwVnum);
	DWORD				GetMobGoldMax(DWORD dwVnum);
#endif

#ifdef ENABLE_WIKI
	DWORD				GetMonsterPrice1(DWORD dwVnum);
	DWORD				GetMonsterPrice2(DWORD dwVnum);
	TNonPlayerDataMap	GetMonsterData() {return m_NonPlayerDataMap;}
	char				GetMonsterResist(DWORD dwVnum, BYTE byResist);
#endif

	// Function for outer
	void				GetMatchableMobList(int iLevel, int iInterval, TMobTableList* pMobTableList);

protected:
	TNonPlayerDataMap	m_NonPlayerDataMap;
#ifdef ENABLE_GLOBAL_SCALE
	TNonMobScaleDataMap	m_NonMobScaleDataMap;
#endif

#ifdef ENABLE_PRESENT_NPC
public:
	bool		LoadPresentNPC(const char* szPresentNPCFile);
	int			GetPresentNPC(const int raceIndex, const BYTE wearIndex);
protected:
	std::map<std::string, std::map<DWORD, std::vector<int>>> m_mapPresentNPC;
#endif

#ifdef ENABLE_ALIGNMENT_SYSTEM
public:
	typedef struct SAlignmentTable
	{
		int minPoint, maxPoint;
		std::vector<std::pair<BYTE, WORD>>bonus;
		SAlignmentTable()
		{
			bonus.clear();
		}
	}TAlignmentTable;
	using ALIGN_MAP = std::map<BYTE, TAlignmentTable>;
	bool LoadAlignmentProto();
	UINT GetAlignmentLevel(int align);

	BYTE GetAlignmentBonusCount(BYTE level);
	std::pair<BYTE, WORD>GetAlignmentBonusInfo(BYTE level, BYTE idx);

	BYTE GetAlignTitleNoneLevel() { return m_titleNoneAlignLevel; }
private:
	ALIGN_MAP m_alignMap;
	BYTE m_titleNoneAlignLevel;
#endif

#ifdef ENABLE_MONSTER_SPECULAR

public:
	typedef struct SMobSpecularTable
	{
		DWORD	dwMobNum;
		float	specular;
	} TMobSpecularTable;

	bool LoadSpecularTable(const char* c_szFileName);
	const TMobSpecularTable* GetSpecularTable(DWORD dwVnum);
	float  GetSpecularMob(DWORD dwVnum);

private:
	typedef std::map<DWORD, TMobSpecularTable*> TNonMobSpecularDataMap;
	TNonMobSpecularDataMap	m_NonMobSpecularDataMap;
#endif


#ifdef ENABLE_HAIR_SPECULAR

public:
	typedef struct SHairSpecularTable
	{
		DWORD	dwItemVnum;
		float	specular;
	} THairSpecularTable;

	bool LoadHairSpecularTable(const char* c_szFileName);
	const THairSpecularTable* GetHairSpecularTable(DWORD dwVnum);
	float  GetHairSpecular(DWORD dwVnum);

private:
	typedef std::map<DWORD, THairSpecularTable*> m_NoHairSpecularDataMap;
	m_NoHairSpecularDataMap	m_NonHairSpecularDataMap;
#endif

};
