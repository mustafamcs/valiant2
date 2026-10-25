#pragma once
#ifdef ENABLE_CLIENT_OPTIMISATION
#include "PythonItem.h"
#include "PythonSkill.h"
#include "InstanceBase.h"
#include "../GameLib/FlyingObjectManager.h"
#include "GameType.h"
#include "../GameLib/RaceData.h"
#include "../GameLib/RaceMotionData.h"
#include "../GameLib/RaceManager.h"


#include <chrono>

struct FTimer {
	std::chrono::steady_clock::time_point startTime;
	double elapsedTime;
	const char* funcName;

	FTimer(const char* f) : funcName(f)
	{
		Start();
	}

	~FTimer() {
		Stop();
	}

	void Start() {
		startTime = std::chrono::steady_clock::now();
	}

	void Stop() {
		std::chrono::steady_clock::time_point endTime = std::chrono::steady_clock::now();
		std::chrono::duration<double, std::milli> duration = endTime - startTime;
		elapsedTime = duration.count();
		double elapsedSeconds = elapsedTime / 1000.0;

		TraceError("Function '%s' took %f seconds to load!", funcName, elapsedSeconds);
	}
};


constexpr auto NPC_LIST_FILE_NAME = "general/npclist.txt";

class CPythonOptimizationBoost : public CSingleton<CPythonOptimizationBoost>
{
public:
	CPythonOptimizationBoost() = default;
	virtual ~CPythonOptimizationBoost() = default;

	void LoadMisc();
	void Load();

	void __RegisterCacheMotionData(CRaceData* pRaceData, const uint16_t wMotionMode, const uint16_t wMotionIndex, const char* c_szFileName, const uint8_t byPercentage = 100);
	void __SetGeneralMotions(CRaceData* pRaceData, const uint16_t wMotionMode, std::string_view c_rstrFolderName);
/*#ifdef ENABLE_WOLFMAN_CHARACTER
	void __SetWolfmanMotions(CRaceData* pRaceData, const uint16_t &wMotionMode, const std::string& c_rstrFolderName);
#endif*/
	void __LoadComboRace(CRaceData* pRaceData, const uint16_t wMotionMode, std::string_view c_rstrFolderName);
	void __LoadCombo(CRaceData* pRaceData, const uint16_t wMotionMode);
	void __LoadGameWarriorEx(const DWORD raceNum, const std::string& c_rstrFolderName);
	void __LoadGameAssassinEx(const DWORD raceNum, const std::string& c_rstrFolderName);
	void __LoadGameSuraEx(const DWORD raceNum, const std::string& c_rstrFolderName);
	void __LoadGameShamanEx(const DWORD raceNum, const std::string& c_rstrFolderName);
/*#ifdef ENABLE_WOLFMAN_CHARACTER
	void __LoadGameWolfmanEx(CRaceData* pRaceData, const std::string& c_rstrFolderName);
#endif*/
	void __LoadGameRace(CRaceData* pRaceData, const std::string& c_rstrFolderName);
	void __LoadFishing(CRaceData* pRaceData, const std::string& c_rstrFolderName);
	void __LoadWedding(CRaceData* pRaceData, const std::string& c_rstrFolderName);
	void __LoadActions(CRaceData* pRaceData, const std::string& c_rstrFolderName);
	void __LoadGuildSkill(CRaceData* pRaceData, const std::string& c_rstrFolderName);
	void __LoadGameEffects();
	void __LoadGameInit();
	void __LoadGameNPC();
	void __RegisterMisc();
};

static const std::pair<int, std::string> effectEmoticonStrings[] = {
	{ CInstanceBase::EFFECT_EMOTICON + 0, "sweat" },
	{ CInstanceBase::EFFECT_EMOTICON + 1, "money" },
	{ CInstanceBase::EFFECT_EMOTICON + 2, "happy" },
	{ CInstanceBase::EFFECT_EMOTICON + 3, "love_s" },
	{ CInstanceBase::EFFECT_EMOTICON + 4, "love_l" },
	{ CInstanceBase::EFFECT_EMOTICON + 5, "angry" },
	{ CInstanceBase::EFFECT_EMOTICON + 6, "aha" },
	{ CInstanceBase::EFFECT_EMOTICON + 7, "gloom" },
	{ CInstanceBase::EFFECT_EMOTICON + 8, "sorry" },
	{ CInstanceBase::EFFECT_EMOTICON + 10, "question" },
	{ CInstanceBase::EFFECT_EMOTICON + 11, "fish" }
};

typedef struct SMotion
{
	int wMotionIndex;
	char stName[70];
	BYTE byPercentage;
} TMotion;

typedef struct SRaceData
{
	DWORD dwRace;
	char stMSM[70];
	char stIntroMotion[70];
} TRaceData;

static std::vector<SMotion> waitMotions =
{
	{ CRaceMotionData::EName::NAME_INTRO_WAIT, "wait.msa", 0 },
	{ CRaceMotionData::EName::NAME_INTRO_SELECTED, "selected.msa", 0 },
	{ CRaceMotionData::EName::NAME_INTRO_NOT_SELECTED, "not_selected.msa", 0 },
};

static std::vector<TRaceData> m_vecRaceData =
{
	{ CRaceData::RACE_WARRIOR_M, "msm/warrior_m", "d:/ymir work/pc/warrior/intro/" },
	{ CRaceData::RACE_WARRIOR_W, "msm/warrior_w", "d:/ymir work/pc2/warrior/intro/" },

	{ CRaceData::RACE_ASSASSIN_W, "msm/assassin_w", "d:/ymir work/pc/assassin/intro/" },
	{ CRaceData::RACE_ASSASSIN_M, "msm/assassin_m", "d:/ymir work/pc2/assassin/intro/" },

	{ CRaceData::RACE_SURA_M, "msm/sura_m", "d:/ymir work/pc/sura/intro/" },
	{ CRaceData::RACE_SURA_W, "msm/sura_w", "d:/ymir work/pc2/sura/intro/" },

	{ CRaceData::RACE_SHAMAN_W, "msm/shaman_w", "d:/ymir work/pc/shaman/intro/" },
	{ CRaceData::RACE_SHAMAN_M, "msm/shaman_m", "d:/ymir work/pc2/shaman/intro/" },
};


static const char* dungeonMapNames[] = {
	"metin2_map_spiderdungeon",
	"metin2_map_monkeydungeon",
	"metin2_map_monkeydungeon_02",
	"metin2_map_monkeydungeon_03",
	"metin2_map_deviltower1"
};

typedef std::tuple<DWORD, const char*, const uint8_t> TGMotionList;
static const std::vector<TGMotionList> vecGeneralMotions =
{
	{ CRaceMotionData::NAME_WAIT,   "wait.msa", 100 },
	{ CRaceMotionData::NAME_WALK,   "walk.msa", 100 },
	{ CRaceMotionData::NAME_RUN,	"run.msa", 100 },
	{ CRaceMotionData::NAME_DAMAGE,   "damage.msa", 50 },
	{ CRaceMotionData::NAME_DAMAGE,   "damage_1.msa", 50 },
	{ CRaceMotionData::NAME_DAMAGE_BACK,   "damage_2.msa", 50 },
	{ CRaceMotionData::NAME_DAMAGE_BACK,   "damage_3.msa", 50 },
	{ CRaceMotionData::NAME_DAMAGE_FLYING,   "damage_flying.msa", 100 },
	{ CRaceMotionData::NAME_STAND_UP,   "falling_stand.msa", 100 },
	{ CRaceMotionData::NAME_DAMAGE_FLYING_BACK,   "back_damage_flying.msa", 100 },
	{ CRaceMotionData::NAME_STAND_UP_BACK,   "back_falling_stand.msa", 100 },
	{ CRaceMotionData::NAME_DEAD,   "dead.msa", 100 },
	{ CRaceMotionData::NAME_DIG,   "dig.msa", 100 },
};

/*
#ifdef ENABLE_WOLFMAN_CHARACTER
typedef std::tuple<DWORD, const char*, const uint8_t> TGWMotionList;
static const std::vector<TGWMotionList> vecWolfmanMotions =
{
	{CRaceMotionData::NAME_WAIT, "wait.msa", 100},
	{CRaceMotionData::NAME_WALK, "walk.msa", 100},
	{CRaceMotionData::NAME_RUN, "run.msa", 100},
	{CRaceMotionData::NAME_DAMAGE_FLYING_BACK, "back_damage_flying.msa", 100},
	{CRaceMotionData::NAME_STAND_UP_BACK, "back_falling_standup.msa", 100},
	{CRaceMotionData::NAME_DEAD, "dead.msa", 100},
	{CRaceMotionData::NAME_DIG, "dig.msa", 100},
};

#endif*/

typedef std::pair<DWORD, const char*> TWeddingList;
static const std::vector<TWeddingList> vecWeddingList =
{
	{ CRaceMotionData::NAME_WAIT,   "wait.msa"},
	{ CRaceMotionData::NAME_WALK,   "walk.msa"},
	{ CRaceMotionData::NAME_RUN,   "walk.msa"},
};

typedef std::pair<DWORD, const char*> TActionsList;
static const std::vector<TActionsList> vecActionsList =
{
	{ CRaceMotionData::NAME_CLAP,   "clap.msa"},
	{ CRaceMotionData::NAME_CHEERS_1,   "cheers_1.msa"},
	{ CRaceMotionData::NAME_CHEERS_2,   "cheers_2.msa"},
	{ CRaceMotionData::NAME_DANCE_1,   "dance_1.msa"},
	{ CRaceMotionData::NAME_DANCE_2,   "dance_2.msa"},
	{ CRaceMotionData::NAME_DANCE_3,   "dance_3.msa"},
	{ CRaceMotionData::NAME_DANCE_4,   "dance_4.msa"},
	{ CRaceMotionData::NAME_DANCE_5,   "dance_5.msa"},
	{ CRaceMotionData::NAME_DANCE_6,   "dance_6.msa"},
	{ CRaceMotionData::NAME_CONGRATULATION,   "congratulation.msa"},
	{ CRaceMotionData::NAME_FORGIVE,   "forgive.msa"},
	{ CRaceMotionData::NAME_ANGRY,   "angry.msa"},
	{ CRaceMotionData::NAME_ATTRACTIVE,   "attractive.msa"},
	{ CRaceMotionData::NAME_SAD,   "sad.msa"},
	{ CRaceMotionData::NAME_SHY,   "shy.msa"},
	{ CRaceMotionData::NAME_CHEERUP,   "cheerup.msa"},
	{ CRaceMotionData::NAME_BANTER,   "banter.msa"},
	{ CRaceMotionData::NAME_JOY,   "joy.msa"},
	{ CRaceMotionData::NAME_FRENCH_KISS_WITH_WARRIOR,   "french_kiss_with_warrior.msa"},
	{ CRaceMotionData::NAME_FRENCH_KISS_WITH_ASSASSIN,   "french_kiss_with_assassin.msa"},
	{ CRaceMotionData::NAME_FRENCH_KISS_WITH_SURA,   "french_kiss_with_sura.msa"},
	{ CRaceMotionData::NAME_FRENCH_KISS_WITH_SHAMAN, "french_kiss_with_shaman.msa"},
/*#ifdef ENABLE_WOLFMAN_CHARACTER
	{ CRaceMotionData::NAME_FRENCH_KISS_WITH_WOLFMAN, "french_kiss_with_wolfman.msa"},
#endif*/
	{ CRaceMotionData::NAME_KISS_WITH_WARRIOR,   "kiss_with_warrior.msa"},
	{ CRaceMotionData::NAME_KISS_WITH_ASSASSIN,   "kiss_with_assassin.msa"},
	{ CRaceMotionData::NAME_KISS_WITH_SURA,   "kiss_with_sura.msa"},
	{ CRaceMotionData::NAME_KISS_WITH_SHAMAN,   "kiss_with_shaman.msa"},
/*#ifdef ENABLE_WOLFMAN_CHARACTER
	{ CRaceMotionData::NAME_KISS_WITH_WOLFMAN, "kiss_with_wolfman.msa"},
#endif*/
	{ CRaceMotionData::NAME_SLAP_HIT_WITH_WARRIOR,   "slap_hit.msa"},
	{ CRaceMotionData::NAME_SLAP_HIT_WITH_ASSASSIN,   "slap_hit.msa"},
	{ CRaceMotionData::NAME_SLAP_HIT_WITH_SURA,   "slap_hit.msa"},
	{ CRaceMotionData::NAME_SLAP_HIT_WITH_SHAMAN,   "slap_hit.msa"},
/*#ifdef ENABLE_WOLFMAN_CHARACTER
	{ CRaceMotionData::NAME_SLAP_HIT_WITH_WOLFMAN, "slap_hit.msa"},
#endif*/
	{ CRaceMotionData::NAME_SLAP_HURT_WITH_WARRIOR,   "slap_hurt.msa"},
	{ CRaceMotionData::NAME_SLAP_HURT_WITH_ASSASSIN,   "slap_hurt.msa"},
	{ CRaceMotionData::NAME_SLAP_HURT_WITH_SURA,   "slap_hurt.msa"},
	{ CRaceMotionData::NAME_SLAP_HURT_WITH_SHAMAN,   "slap_hurt.msa"},
/*#ifdef ENABLE_WOLFMAN_CHARACTER
	{ CRaceMotionData::NAME_SLAP_HURT_WITH_WOLFMAN, "slap_hurt.msa"},
#endif*/
};

typedef std::pair<DWORD, const char*> TIMotionList;
static const std::vector<TIMotionList> vecIntroMotions =
{
	{ CRaceMotionData::NAME_INTRO_WAIT, "wait.msa" },
	{ CRaceMotionData::NAME_INTRO_SELECTED, "selected.msa" },
	{ CRaceMotionData::NAME_INTRO_NOT_SELECTED, "not_selected.msa" },
};

typedef std::pair<DWORD, const char*> TFishing;
static const std::vector<TFishing> vecFishing =
{
	{ CRaceMotionData::NAME_WAIT, "wait.msa" },
	{ CRaceMotionData::NAME_WALK, "walk.msa" },
	{ CRaceMotionData::NAME_FISHING_THROW, "throw.msa" },
	{ CRaceMotionData::NAME_FISHING_WAIT, "fishing_wait.msa" },
	{ CRaceMotionData::NAME_FISHING_STOP, "fishing_cancel.msa" },
	{ CRaceMotionData::NAME_FISHING_REACT, "fishing_react.msa" },
	{ CRaceMotionData::NAME_FISHING_CATCH, "fishing_catch.msa" },
	{ CRaceMotionData::NAME_FISHING_FAIL, "fishing_fail.msa" },
};

typedef std::pair<DWORD, const char*> TGuildSkill;
static const std::vector<TGuildSkill> vecGuildSkill =
{
	{ CRaceMotionData::NAME_SKILL + 101, "guild_yongsinuipi.msa" },
	{ CRaceMotionData::NAME_SKILL + 102, "guild_yongsinuichukbok.msa" },
	{ CRaceMotionData::NAME_SKILL + 103, "guild_seonghwigap.msa" },
	{ CRaceMotionData::NAME_SKILL + 104, "guild_gasokhwa.msa" },
	{ CRaceMotionData::NAME_SKILL + 105, "guild_yongsinuibunno.msa" },
	{ CRaceMotionData::NAME_SKILL + 106, "guild_jumunsul.msa" },
};

enum ComboType
{
	COMBO_TYPE_1,
	COMBO_TYPE_2,
	COMBO_TYPE_3,
};

enum ComboIndex
{
	COMBO_INDEX_1,
	COMBO_INDEX_2,
	COMBO_INDEX_3,
	COMBO_INDEX_4,
	COMBO_INDEX_5,
	COMBO_INDEX_6,
};

typedef std::tuple<uint32_t, const char*, const char*, bool> TEffectList;
static const std::vector<TEffectList> vecEffectList =
{
	//{ CInstanceBase::EFFECT_SPAWN_APPEAR, "Bip01", "d:/ymir work/effect/etc/appear_die/monster_appear.mse", true},
	//{ CInstanceBase::EFFECT_SPAWN_DISAPPEAR, "Bip01", "d:/ymir work/effect/etc/appear_die/monster_die.mse", true},
	{ CInstanceBase::EFFECT_FLAME_ATTACK, "equip_right_hand", "d:/ymir work/effect/hit/blow_flame/flame_3_weapon.mse", true},
	{ CInstanceBase::EFFECT_FLAME_HIT, "", "d:/ymir work/effect/hit/blow_flame/flame_3_blow.mse", true},
	{ CInstanceBase::EFFECT_FLAME_ATTACH, "", "d:/ymir work/effect/hit/blow_flame/flame_3_body.mse", true},
	{ CInstanceBase::EFFECT_ELECTRIC_ATTACK, "equip_right", "d:/ymir work/effect/hit/blow_electric/light_1_weapon.mse", true},
	{ CInstanceBase::EFFECT_ELECTRIC_HIT, "", "d:/ymir work/effect/hit/blow_electric/light_1_blow.mse", true},
	{ CInstanceBase::EFFECT_ELECTRIC_ATTACH, "", "d:/ymir work/effect/hit/blow_electric/light_1_body.mse", true},
	{ CInstanceBase::EFFECT_LEVELUP, "", "d:/ymir work/effect/etc/levelup_1/level_up.mse", true},
	{ CInstanceBase::EFFECT_SKILLUP, "", "d:/ymir work/effect/etc/skillup/skillup_1.mse", true},
	{ CInstanceBase::EFFECT_EMPIRE + 1, "Bip01", "d:/ymir work/effect/etc/empire/empire_A.mse", true},
	{ CInstanceBase::EFFECT_EMPIRE + 2, "Bip01", "d:/ymir work/effect/etc/empire/empire_B.mse", true},
	{ CInstanceBase::EFFECT_EMPIRE + 3, "Bip01", "d:/ymir work/effect/etc/empire/empire_C.mse", true},
	{ CInstanceBase::EFFECT_WEAPON + 1, "equip_right_hand", "d:/ymir work/pc/warrior/effect/geom_sword_loop.mse", true},
	{ CInstanceBase::EFFECT_WEAPON + 2, "equip_right_hand", "d:/ymir work/pc/warrior/effect/geom_spear_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_YMIR, "Bip01", "locale/common/effect/gm.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_POISON, "Bip01", "d:/ymir work/effect/hit/blow_poison/poison_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_SLOW, "", "d:/ymir work/effect/affect/slow.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_STUN, "Bip01 Head", "d:/ymir work/effect/etc/stun/stun_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_DUNGEON_READY, "", "d:/ymir work/effect/etc/ready/ready.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_CHEONGEUN, "", "d:/ymir work/pc/warrior/effect/gyeokgongjang_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_GYEONGGONG, "", "d:/ymir work/pc/assassin/effect/gyeonggong_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_GWIGEOM, "Bip01 R Finger2", "d:/ymir work/pc/sura/effect/gwigeom_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_GONGPO, "", "d:/ymir work/pc/sura/effect/fear_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_JUMAGAP, "", "d:/ymir work/pc/sura/effect/jumagap_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_HOSIN, "", "d:/ymir work/pc/shaman/effect/3hosin_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_BOHO, "", "d:/ymir work/pc/shaman/effect/boho_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_KWAESOK, "", "d:/ymir work/pc/shaman/effect/10kwaesok_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_HEUKSIN, "", "d:/ymir work/pc/sura/effect/heuksin_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_MUYEONG, "", "d:/ymir work/pc/sura/effect/muyeong_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_FIRE, "Bip01", "d:/ymir work/effect/hit/blow_flame/flame_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_GICHEON, "Bip01 R Hand", "d:/ymir work/pc/shaman/effect/6gicheon_hand.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_JEUNGRYEOK, "Bip01 L Hand", "d:/ymir work/pc/shaman/effect/jeungryeok_hand.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_PABEOP, "Bip01 Head", "d:/ymir work/pc/sura/effect/pabeop_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_FALLEN_CHEONGEUN, "", "d:/ymir work/pc/warrior/effect/gyeokgongjang_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_WAR_FLAG1, "", "d:/ymir work/effect/etc/guild_war_flag/flag_red.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_WAR_FLAG2, "", "d:/ymir work/effect/etc/guild_war_flag/flag_blue.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_WAR_FLAG3, "", "d:/ymir work/effect/etc/guild_war_flag/flag_yellow.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_BLEEDING, "Bip01", "d:/ymir work/effect/hit/blow_poison/bleeding_loop.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_RED_POSSESSION, "Bip01", "d:/ymir work/effect/hit/blow_flame/flame_loop_w.mse", true},
	{ CInstanceBase::EFFECT_AFFECT +CInstanceBase::AFFECT_BLUE_POSSESSION, "", "d:/ymir work/pc3/common/effect/gyeokgongjang_loop_w.mse", true},

#ifdef ENABLE_AURA_SYSTEM
	{ CInstanceBase::EFFECT_AFFECT + CInstanceBase::AFFECT_AURA1, "Bip01 Spine2", "d:/ymir work/pc/common/effect/aura/aura_01_49_001.mse", true },
	{ CInstanceBase::EFFECT_AFFECT + CInstanceBase::AFFECT_AURA2, "Bip01 Spine2", "d:/ymir work/pc/common/effect/aura/aura_50_99_002.mse", true },
	{ CInstanceBase::EFFECT_AFFECT + CInstanceBase::AFFECT_AURA3, "Bip01 Spine2", "d:/ymir work/pc/common/effect/aura/aura_100_149_003.mse", true },
	{ CInstanceBase::EFFECT_AFFECT + CInstanceBase::AFFECT_AURA4, "Bip01 Spine2", "d:/ymir work/pc/common/effect/aura/aura_150_199_004.mse", true },
	{ CInstanceBase::EFFECT_AFFECT + CInstanceBase::AFFECT_AURA5, "Bip01 Spine2", "d:/ymir work/pc/common/effect/aura/aura_200_249_005.mse", true },
	{ CInstanceBase::EFFECT_AFFECT + CInstanceBase::AFFECT_AURA6, "Bip01 Spine1", "d:/ymir work/pc/common/effect/aura/aura_250_006.mse", true },
#endif

	{ CInstanceBase::EFFECT_REFINED + 1, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_7.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 2, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_8.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 3, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_9.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 4, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_7_b.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 5, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_8_b.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 6, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_9_b.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 7, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_7_f.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 8, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_8_f.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 9, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_9_f.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 10, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_7_s.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 11, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_8_s.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 12, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_9_s.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 13, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_7_s.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 14, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_8_s.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 15, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_9_s.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 16, "Bip01", "D:/ymir work/pc/common/effect/armor/armor_7.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 17, "Bip01", "D:/ymir work/pc/common/effect/armor/armor_8.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 18, "Bip01", "D:/ymir work/pc/common/effect/armor/armor_9.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 19, "Bip01", "D:/ymir work/pc/common/effect/armor/armor-4-2-1.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 20, "Bip01", "D:/ymir work/pc/common/effect/armor/armor-4-2-2.mse", true},
	{ CInstanceBase::EFFECT_REFINED + 21, "Bip01", "D:/ymir work/pc/common/effect/armor/armor-5-1.mse", true},
	{ CInstanceBase::EFFECT_DUST, "", "d:/ymir work/effect/etc/dust/dust.mse", true},
	{ CInstanceBase::EFFECT_HORSE_DUST, "", "d:/ymir work/effect/etc/dust/running_dust.mse", true},
	{ CInstanceBase::EFFECT_HIT, "", "d:/ymir work/effect/hit/blow_1/blow_1_low.mse", true},
	{ CInstanceBase::EFFECT_HPUP_RED, "", "d:/ymir work/effect/etc/recuperation/drugup_red.mse", true},
	{ CInstanceBase::EFFECT_SPUP_BLUE, "", "d:/ymir work/effect/etc/recuperation/drugup_blue.mse", true},
	{ CInstanceBase::EFFECT_SPEEDUP_GREEN, "", "d:/ymir work/effect/etc/recuperation/drugup_green.mse", true},
	{ CInstanceBase::EFFECT_DXUP_PURPLE, "", "d:/ymir work/effect/etc/recuperation/drugup_purple.mse", true},
	{ CInstanceBase::EFFECT_AUTO_HPUP, "", "d:/ymir work/effect/etc/recuperation/autodrugup_red.mse", true},
	{ CInstanceBase::EFFECT_AUTO_SPUP, "", "d:/ymir work/effect/etc/recuperation/autodrugup_blue.mse", true},
	{ CInstanceBase::EFFECT_HALLOWEEN_CANDY_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item2.mse", true},
	{ CInstanceBase::EFFECT_HAPPINESS_RING_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item3.mse", true},
	{ CInstanceBase::EFFECT_LOVE_PENDANT_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item4.mse", true},
	{ CInstanceBase::EFFECT_FIRECRACKER, "", "d:/ymir work/effect/etc/firecracker/newyear_firecracker.mse", true},
	{ CInstanceBase::EFFECT_SPIN_TOP, "", "d:/ymir work/effect/etc/firecracker/paing_i.mse", true},
	{ CInstanceBase::EFFECT_SELECT, "", "d:/ymir work/effect/etc/click/click_select.mse", true},
	{ CInstanceBase::EFFECT_TARGET, "", "d:/ymir work/effect/etc/click/click_glow_select.mse", true},
	{ CInstanceBase::EFFECT_STUN, "Bip01 Head", "d:/ymir work/effect/etc/stun/stun.mse", true},
	{ CInstanceBase::EFFECT_CRITICAL, "Bip01 R Hand", "d:/ymir work/effect/hit/critical.mse", true},
	{ CInstanceBase::EFFECT_DAMAGE_TARGET, "", "d:/ymir work/effect/affect/damagevalue/target.mse", true},
	{ CInstanceBase::EFFECT_DAMAGE_NOT_TARGET, "", "d:/ymir work/effect/affect/damagevalue/nontarget.mse", true},
	{ CInstanceBase::EFFECT_DAMAGE_SELFDAMAGE, "", "d:/ymir work/effect/affect/damagevalue/damage.mse", true},
	{ CInstanceBase::EFFECT_DAMAGE_SELFDAMAGE2, "", "d:/ymir work/effect/affect/damagevalue/damage_1.mse", true},
	{ CInstanceBase::EFFECT_DAMAGE_POISON, "", "d:/ymir work/effect/affect/damagevalue/poison.mse", true},

	{ CInstanceBase::EFFECT_DAMAGE_MISS, "", "d:/ymir work/effect/affect/damagevalue/miss.mse", true},
	{ CInstanceBase::EFFECT_DAMAGE_TARGETMISS, "", "d:/ymir work/effect/affect/damagevalue/target_miss.mse", true},

	{ CInstanceBase::EFFECT_LEVELUP_ON_14_FOR_GERMANY, "", "d:/ymir work/effect/paymessage_warning.mse", true},
	{ CInstanceBase::EFFECT_LEVELUP_UNDER_15_FOR_GERMANY, "", "d:/ymir work/effect/paymessage_decide.mse", true},
	{ CInstanceBase::EFFECT_PERCENT_DAMAGE1, "", "d:/ymir work/effect/hit/percent_damage1.mse", true},
	{ CInstanceBase::EFFECT_PERCENT_DAMAGE2, "", "d:/ymir work/effect/hit/percent_damage2.mse", true},
	{ CInstanceBase::EFFECT_PERCENT_DAMAGE3, "", "d:/ymir work/effect/hit/percent_damage3.mse", true},
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	{ CInstanceBase::EFFECT_ACCE_SUCCEDED, "", "d:/ymir work/effect/etc/buff/buff_item6.mse", true},
	{ CInstanceBase::EFFECT_ACCE_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item7.mse", true},
#endif

#ifdef ENABLE_BOSS_EFFECT_ON_BOSS
	{ CInstanceBase::EFFECT_BOSS_LOW, "", "d:/ymir work/effect/boss/boss_icon.mse", true},
	{ CInstanceBase::EFFECT_BOSS_HIGH, "", "d:/ymir work/effect/boss/boss_icon.mse", true},
#endif

#ifdef ENABLE_EXTENDED_BATTLE_PASS
	{ CInstanceBase::EFFECT_BP_NORMAL_MISSION_COMPLETED, "", "d:/ymir work/effect/battlepass/normal_mission_complete.mse", true },
	{ CInstanceBase::EFFECT_BP_PREMIUM_MISSION_COMPLETED, "", "d:/ymir work/effect/battlepass/premium_mission_complete.mse", true },
	{ CInstanceBase::EFFECT_BP_EVENT_MISSION_COMPLETED, "", "d:/ymir work/effect/battlepass/event_mission_complete.mse", true },
	{ CInstanceBase::EFFECT_BP_NORMAL_BATTLEPASS_COMPLETED, "", "d:/ymir work/effect/battlepass/normal_battlepass_complete.mse", true },
	{ CInstanceBase::EFFECT_BP_PREMIUM_BATTLEPASS_COMPLETED, "",  "d:/ymir work/effect/battlepass/premium_battlepass_complete.mse", true },
	{ CInstanceBase::EFFECT_BP_EVENT_BATTLEPASS_COMPLETED, "", "d:/ymir work/effect/battlepass/event_battlepass_complete.mse", true },
#endif

#ifdef ENABLE_METIN_QUEUE
	{ CInstanceBase::EFFECT_METIN_QUEUE, "", "d:/ymir work/effect/etc/myshop/2.mse", true },
#endif
};
#endif