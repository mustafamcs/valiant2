#include "Stdafx.h"
#ifdef ENABLE_CLIENT_OPTIMISATION
#include "InstanceBase.h"
#include "PythonNetworkStream.h"
#include "PythonPlayer.h"
#include "PythonOptimizationBoost.h"
#include "PythonBackground.h"
#include "../EterLib/ResourceManager.h"
#include "../EterFSLib/FileSystemIncl.hpp"
#include "../GameLib/RaceManager.h"

bool isLoadedCharacterData, isLoadedMisc = false;

CRaceMotionData& MotionManager{ CRaceMotionData() };

const char* trim(const char* str)
{
	if (!str)
		return "";

	const size_t length = strlen(str);
	if (length == 0)
		return "";

	size_t first = 0;
	while (str[first] == ' ' && first < length)
		++first;

	if (first == length)
		return "";

	size_t last = length - 1;
	while (str[last] == ' ' && last > first)
		--last;

	return str + first;
}

void CPythonOptimizationBoost::LoadMisc()
{
	if (isLoadedMisc)
		return;

	__LoadGameInit();
	__RegisterMisc();
	__LoadGameEffects();
	__LoadGameNPC();

	PyObject_CallObject(PyObject_GetAttrString(PyImport_ImportModule("playerSettingModule"), "registerData"), nullptr);

	isLoadedMisc = true;
}

void CPythonOptimizationBoost::Load()
{
	if (isLoadedCharacterData)
		return;

	__LoadGameWarriorEx(CRaceData::RACE_WARRIOR_M, "d:/ymir work/pc/warrior/");
	__LoadGameWarriorEx(CRaceData::RACE_WARRIOR_W, "d:/ymir work/pc2/warrior/");


	__LoadGameAssassinEx(CRaceData::RACE_ASSASSIN_W, "d:/ymir work/pc/assassin/");
	__LoadGameAssassinEx(CRaceData::RACE_ASSASSIN_M, "d:/ymir work/pc2/assassin/");

	__LoadGameSuraEx(CRaceData::RACE_SURA_M, "d:/ymir work/pc/sura/" );
	__LoadGameSuraEx(CRaceData::RACE_SURA_W, "d:/ymir work/pc2/sura/");

	__LoadGameShamanEx(CRaceData::RACE_SHAMAN_W,"d:/ymir work/pc/shaman/" );
	__LoadGameShamanEx(CRaceData::RACE_SHAMAN_M,"d:/ymir work/pc2/shaman/");
	
	isLoadedCharacterData = true;
}

void CPythonOptimizationBoost::__RegisterCacheMotionData(CRaceData* pRaceData, const uint16_t wMotionMode, const uint16_t wMotionIndex, const char* c_szFileName, const uint8_t byPercentage)
{

	if (!c_szFileName)
	{
		TraceError("Motion data file name is invalid!");
		return;
	}

	std::string_view strFullFileName = CRaceManager::Instance().GetFullPathFileName(c_szFileName);

	if (strFullFileName.empty())
	{
		TraceError("Motion data file '%s' could not be found!", c_szFileName);
		return;
	}

	const CGraphicThing* pkMotionThing = pRaceData->RegisterMotionData(wMotionMode, wMotionIndex, strFullFileName.data(), byPercentage);
	
	if (pkMotionThing)
		CResourceManager::Instance().LoadStaticCache(pkMotionThing->GetFileName());
	
}

void CPythonOptimizationBoost::__SetGeneralMotions(CRaceData* pRaceData, const uint16_t wMotionMode, std::string_view c_rstrFolderName)
{
	if (!pRaceData)
		return;

	CRaceManager::Instance().SetPathName(c_rstrFolderName.data());
	pRaceData->RegisterMotionMode(wMotionMode);

	for (const auto& generalMotion : vecGeneralMotions)
		__RegisterCacheMotionData(pRaceData, wMotionMode, std::get<0>(generalMotion), std::get<1>(generalMotion), std::get<2>(generalMotion));
}

/*
#ifdef ENABLE_WOLFMAN_CHARACTER
void CPythonOptimizationBoost::__SetWolfmanMotions(CRaceData* pRaceData, const uint16_t wMotionMode, const std::string& c_rstrFolderName)
{
	CRaceManager::Instance().SetPathName(c_rstrFolderName.c_str());
	pRaceData->RegisterMotionMode(wMotionMode);

	for (const auto& generalMotionWolf : vecWolfmanMotions)
		__RegisterCacheMotionData(pRaceData, wMotionMode, std::get<0>(generalMotionWolf), std::get<1>(generalMotionWolf), std::get<2>(generalMotionWolf));
}
#endif*/


void CPythonOptimizationBoost::__LoadComboRace(CRaceData* pRaceData, const uint16_t wMotionMode, std::string_view c_rstrFolderName)
{
	const BYTE RaceIndex = RaceToJob(pRaceData->GetRace());

	CRaceManager::Instance().SetPathName(c_rstrFolderName.data());

	pRaceData->RegisterMotionMode(wMotionMode);

	if (RaceIndex == NRaceData::JOB_WARRIOR)
	{
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WAIT, "wait.msa", 50);
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WAIT, "wait_1.msa", 50);
	}
	else if (RaceIndex == NRaceData::JOB_ASSASSIN)
	{
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WAIT, "wait.msa", 70);
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WAIT, "wait_1.msa", 30);
	}
	else if (RaceIndex == NRaceData::JOB_SURA)
	{
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WAIT, "wait.msa");
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_DAMAGE, "damage.msa");
	}
	else if (RaceIndex == NRaceData::JOB_SHAMAN)
	{
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WAIT, "wait.msa");
	}
	/*
#ifdef ENABLE_WOLFMAN_CHARACTER
	else if (RaceIndex == NRaceData::JOB_WOLFMAN)
	{
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WAIT, "wait.msa");
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WAIT, "wait1.msa");
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WAIT, "wait2.msa");
	}
#endif*/

	__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_WALK, "walk.msa");
	__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_RUN, "run.msa");

	if (RaceIndex != NRaceData::JOB_WOLFMAN) {
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_DAMAGE, "damage.msa", 50);
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_DAMAGE, "damage_1.msa", 50);
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_DAMAGE_BACK, "damage_2.msa", 50);
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_DAMAGE_BACK, "damage_3.msa", 50);
	}

	if (wMotionMode == CRaceMotionData::MODE_BOW)
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack.msa");
	else
	{
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_COMBO_ATTACK_1, "combo_01.msa");
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_COMBO_ATTACK_2, "combo_02.msa");
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_COMBO_ATTACK_3, "combo_03.msa");
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_COMBO_ATTACK_4, "combo_04.msa");
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_COMBO_ATTACK_5, "combo_05.msa");
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_COMBO_ATTACK_6, "combo_06.msa");
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_COMBO_ATTACK_7, "combo_07.msa");
	}
	if (wMotionMode == CRaceMotionData::MODE_DUALHAND_SWORD && RaceIndex != NRaceData::JOB_ASSASSIN)
		__RegisterCacheMotionData(pRaceData, wMotionMode, CRaceMotionData::NAME_COMBO_ATTACK_8, "combo_08.msa");

	__LoadCombo(pRaceData, wMotionMode);
}

void CPythonOptimizationBoost::__LoadCombo(CRaceData* pRaceData, const uint16_t wMotionMode)
{
	if (wMotionMode == CRaceMotionData::MODE_BOW)
	{
		pRaceData->ReserveComboAttack(CRaceMotionData::MODE_BOW, COMBO_TYPE_1, 1);
		pRaceData->RegisterComboAttack(CRaceMotionData::MODE_BOW, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
		return;
	}

	pRaceData->ReserveComboAttack(wMotionMode, COMBO_TYPE_1, 4);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_1, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_1, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_1, COMBO_INDEX_4, CRaceMotionData::NAME_COMBO_ATTACK_4);


	pRaceData->ReserveComboAttack(wMotionMode, COMBO_TYPE_2, 5);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_2, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_2, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_2, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_2, COMBO_INDEX_4, CRaceMotionData::NAME_COMBO_ATTACK_5);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_2, COMBO_INDEX_5, CRaceMotionData::NAME_COMBO_ATTACK_7);

	pRaceData->ReserveComboAttack(wMotionMode, COMBO_TYPE_3, 6);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_3, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_3, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_3, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_3, COMBO_INDEX_4, CRaceMotionData::NAME_COMBO_ATTACK_5);
	pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_3, COMBO_INDEX_5, CRaceMotionData::NAME_COMBO_ATTACK_6);
	if (wMotionMode == CRaceMotionData::MODE_DUALHAND_SWORD)
		pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_3, COMBO_INDEX_6, CRaceMotionData::NAME_COMBO_ATTACK_8);
	else
		pRaceData->RegisterComboAttack(wMotionMode, COMBO_TYPE_3, COMBO_INDEX_6, CRaceMotionData::NAME_COMBO_ATTACK_4);
}

void CPythonOptimizationBoost::__LoadGameWarriorEx(const DWORD raceNum, const std::string& c_rstrFolderName)
{
	CRaceManager::Instance().SelectRace(raceNum);

	CRaceData* pRaceData = CRaceManager::Instance().GetSelectedRaceDataPointer();

	if (!pRaceData)
		return;

	__SetGeneralMotions(pRaceData, CRaceMotionData::MODE_GENERAL, c_rstrFolderName + "general/");
	pRaceData->SetMotionRandomWeight(CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_WAIT, 0, 70);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack.msa", 50);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack_1.msa", 50);
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "skill/").c_str());

	for (int i{}; i < CPythonSkill::SKILL_EFFECT_COUNT; ++i)
	{
		std::string END_STRING = "";
		if (i != 0)
			END_STRING = "_" + std::to_string(i + 1);

		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 1, std::string("samyeon" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 2, std::string("palbang" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 3, std::string("jeongwi" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 4, std::string("geomgyeong" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 5, std::string("tanhwan" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 6, std::string("gihyeol" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 16, std::string("gigongcham" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 17, std::string("gyeoksan" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 18, std::string("daejin" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 19, std::string("cheongeun" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 20, std::string("geompung" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 21, std::string("noegeom" + END_STRING + ".msa").c_str());
		pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
		pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	}

	__LoadFishing(pRaceData, c_rstrFolderName);
	__LoadGuildSkill(pRaceData, c_rstrFolderName);

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait.msa", 90);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait_1.msa", 9);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait_2.msa", 1);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WALK, "walk.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_RUN, "run.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DAMAGE, "damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DAMAGE_BACK, "damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DEAD, "dead.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_SKILL + 122, "skill_charge.msa");

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse_onehand_sword/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_1, "combo_01.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_2, "combo_02.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_3, "combo_03.msa");
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, 3);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_SKILL + 121, "skill_wildattack.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_SKILL + 123, "skill_splash.msa");

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse_twohand_sword/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE_TWOHAND_SWORD);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_TWOHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_1, "combo_01.msa", 90);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_TWOHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_2, "combo_02.msa", 9);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_TWOHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_3, "combo_03.msa", 1);
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_HORSE_TWOHAND_SWORD, COMBO_TYPE_1, 3);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_TWOHAND_SWORD, CRaceMotionData::NAME_SKILL + 121, "skill_wildattack.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_TWOHAND_SWORD, CRaceMotionData::NAME_SKILL + 123, "skill_splash.msa");

	__LoadWedding(pRaceData, c_rstrFolderName);
	__LoadActions(pRaceData, c_rstrFolderName);
	__LoadComboRace(pRaceData, CRaceMotionData::MODE_ONEHAND_SWORD, c_rstrFolderName + "onehand_sword/");
	__LoadComboRace(pRaceData, CRaceMotionData::MODE_TWOHAND_SWORD, c_rstrFolderName + "twohand_sword/");

	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_WEAPON, "equip_right_hand");
	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_ACCE, "Bip01 Spine2");

}

void CPythonOptimizationBoost::__LoadGameAssassinEx(const DWORD raceNum, const std::string& c_rstrFolderName)
{
	CRaceManager::Instance().SelectRace(raceNum);

	CRaceData* pRaceData = CRaceManager::Instance().GetSelectedRaceDataPointer();
	if (!pRaceData)
		return;

	__SetGeneralMotions(pRaceData, CRaceMotionData::MODE_GENERAL, c_rstrFolderName + "general/");
	pRaceData->SetMotionRandomWeight(CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_WAIT, 0, 70);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack.msa", 50);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack_1.msa", 50);
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "skill/").c_str());

	for (int i{}; i < CPythonSkill::SKILL_EFFECT_COUNT; ++i)
	{
		std::string END_STRING = "";
		if (i != 0)
			END_STRING = "_" + std::to_string(i + 1);

		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 1, std::string("amseup" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 2, std::string("gungsin" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 3, std::string("charyun" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 4, std::string("eunhyeong" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 5, std::string("sangong" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 6, std::string("seomjeon" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 16, std::string("yeonsa" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 17, std::string("gwangyeok" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 18, std::string("hwajo" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 19, std::string("gyeonggong" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 20, std::string("dokgigung" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 21, std::string("seomgwang" + END_STRING + ".msa").c_str());
		pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
		pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);

	}

	__LoadFishing(pRaceData, c_rstrFolderName);
	__LoadGuildSkill(pRaceData, c_rstrFolderName);

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait.msa", 90);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait_1.msa", 9);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait_2.msa", 1);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WALK, "walk.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_RUN, "run.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DAMAGE, "damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DAMAGE_BACK, "damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DEAD, "dead.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_SKILL + 122, "skill_charge.msa");

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse_onehand_sword/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_1, "combo_01.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_2, "combo_02.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_3, "combo_03.msa");
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, 3);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_SKILL + 121, "skill_wildattack.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_SKILL + 123, "skill_splash.msa");

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse_dualhand_sword/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE_DUALHAND_SWORD);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_DUALHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_1, "combo_01.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_DUALHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_2, "combo_02.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_DUALHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_3, "combo_03.msa");
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_HORSE_DUALHAND_SWORD, COMBO_TYPE_1, 3);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_DUALHAND_SWORD, CRaceMotionData::NAME_SKILL + 121, "skill_wildattack.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_DUALHAND_SWORD, CRaceMotionData::NAME_SKILL + 123, "skill_splash.msa");

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse_bow/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE_BOW);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BOW, CRaceMotionData::NAME_WAIT, "wait.msa", 90);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BOW, CRaceMotionData::NAME_WAIT, "wait_1.msa", 9);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BOW, CRaceMotionData::NAME_WAIT, "wait_2.msa", 1);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BOW, CRaceMotionData::NAME_RUN, "run.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BOW, CRaceMotionData::NAME_DAMAGE, "damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BOW, CRaceMotionData::NAME_DEAD, "dead.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BOW, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BOW, CRaceMotionData::NAME_SKILL + 121, "skill_wildattack.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BOW, CRaceMotionData::NAME_SKILL + 123, "skill_splash.msa");
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_HORSE_BOW, COMBO_TYPE_1, 1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_BOW, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);

	__LoadWedding(pRaceData, c_rstrFolderName);
	__LoadActions(pRaceData, c_rstrFolderName);
	__LoadComboRace(pRaceData, CRaceMotionData::MODE_ONEHAND_SWORD, c_rstrFolderName + "onehand_sword/");
	__LoadComboRace(pRaceData, CRaceMotionData::MODE_DUALHAND_SWORD, c_rstrFolderName + "dualhand_sword/");
	__LoadComboRace(pRaceData, CRaceMotionData::MODE_BOW, c_rstrFolderName + "bow/");

	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_WEAPON, "equip_right");
	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_WEAPON_LEFT, "equip_left");
	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_ACCE, "Bip01 Spine2");

}

void CPythonOptimizationBoost::__LoadGameSuraEx(const DWORD raceNum, const std::string& c_rstrFolderName)
{
	CRaceManager::Instance().SelectRace(raceNum);

	CRaceData* pRaceData = CRaceManager::Instance().GetSelectedRaceDataPointer();
	if (!pRaceData)
		return;

	__SetGeneralMotions(pRaceData, CRaceMotionData::MODE_GENERAL, c_rstrFolderName + "general/");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack.msa", 50);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack_1.msa", 50);
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "skill/").c_str());

	for (int i{}; i < CPythonSkill::SKILL_EFFECT_COUNT; ++i)
	{
		std::string END_STRING = "";
		if (i != 0)
			END_STRING = "_" + std::to_string(i + 1);

		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 1, std::string("swaeryeong" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 2, std::string("yonggwon" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 3, std::string("gwigeom" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 4, std::string("gongpo" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 5, std::string("jumagap" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 6, std::string("pabeop" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 16, std::string("maryeong" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 17, std::string("hwayeom" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 18, std::string("muyeong" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 19, std::string("heuksin" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 20, std::string("tusok" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 21, std::string("mahwan" + END_STRING + ".msa").c_str());
		pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
		pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);

	}
	__LoadGuildSkill(pRaceData, c_rstrFolderName);
	__LoadFishing(pRaceData, c_rstrFolderName);


	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait.msa", 90);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait_1.msa", 9);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait_2.msa", 1);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WALK, "walk.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_RUN, "run.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DAMAGE, "damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DAMAGE_BACK, "damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DEAD, "dead.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_SKILL + 122, "skill_charge.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_SKILL + 123, "skill_splash.msa");

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse_onehand_sword/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_1, "combo_01.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_2, "combo_02.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_COMBO_ATTACK_3, "combo_03.msa");
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, 3);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_ONEHAND_SWORD, CRaceMotionData::NAME_SKILL + 121, "skill_wildattack.msa");

	__LoadWedding(pRaceData, c_rstrFolderName);
	__LoadActions(pRaceData, c_rstrFolderName);
	__LoadComboRace(pRaceData, CRaceMotionData::MODE_ONEHAND_SWORD, c_rstrFolderName + "onehand_sword/");

	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_WEAPON, "equip_right");
	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_ACCE, "Bip01 Spine2");

}

void CPythonOptimizationBoost::__LoadGameShamanEx(const DWORD raceNum, const std::string& c_rstrFolderName)
{
	CRaceManager::Instance().SelectRace(raceNum);

	CRaceData* pRaceData = CRaceManager::Instance().GetSelectedRaceDataPointer();
	if (!pRaceData)
		return;

	__SetGeneralMotions(pRaceData, CRaceMotionData::MODE_GENERAL, c_rstrFolderName + "general/");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack.msa", 50);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack_1.msa", 50);
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "skill/").c_str());

	for (int i{1}; i < CPythonSkill::SKILL_EFFECT_COUNT; ++i)
	{
		std::string END_STRING = "";
		END_STRING = "_" + std::to_string(i + 1);

		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 1, std::string("bipabu" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 2, std::string("yongpa" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 3, std::string("paeryong" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 4, std::string("hosin" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 5, std::string("boho" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 6, std::string("gicheon" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 16, std::string("noejeon" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 17, std::string("byeorak" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 18, std::string("pokroe" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 19, std::string("jeongeop" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 20, std::string("kwaesok" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 21, std::string("jeungryeok" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 1, "bipabu.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 2, "yongpa.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 3, "paeryong.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 4, "hosin_target.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 5, "boho_target.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 6, "gicheon_target.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 16, "noejeon.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 17, "byeorak.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 18, "pokroe.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 19, "jeongeop_target.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 20, "kwaesok_target.msa");
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 21, "jeungryeok_target.msa");
		pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
		pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);

	}

	__LoadGuildSkill(pRaceData, c_rstrFolderName);
	__LoadFishing(pRaceData, c_rstrFolderName);

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait.msa", 90);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait_1.msa", 9);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait_2.msa", 1);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WALK, "walk.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_RUN, "run.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DAMAGE, "damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DAMAGE_BACK, "damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DEAD, "dead.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_SKILL + 122, "skill_charge.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_SKILL + 123, "skill_splash.msa");

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse_fan/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE_FAN);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_FAN, CRaceMotionData::NAME_COMBO_ATTACK_1, "combo_01.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_FAN, CRaceMotionData::NAME_COMBO_ATTACK_2, "combo_02.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_FAN, CRaceMotionData::NAME_COMBO_ATTACK_3, "combo_03.msa");
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_HORSE_FAN, COMBO_TYPE_1, 3);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_FAN, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_FAN, COMBO_TYPE_1, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_FAN, COMBO_TYPE_1, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_FAN, CRaceMotionData::NAME_SKILL + 121, "skill_wildattack.msa");

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse_bell/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE_BELL);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BELL, CRaceMotionData::NAME_COMBO_ATTACK_1, "combo_01.msa", 90);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BELL, CRaceMotionData::NAME_COMBO_ATTACK_2, "combo_02.msa", 9);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BELL, CRaceMotionData::NAME_COMBO_ATTACK_3, "combo_03.msa", 1);
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_HORSE_BELL, COMBO_TYPE_1, 3);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_BELL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_BELL, COMBO_TYPE_1, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_BELL, COMBO_TYPE_1, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_BELL, CRaceMotionData::NAME_SKILL + 121, "skill_wildattack.msa");

	__LoadWedding(pRaceData, c_rstrFolderName);
	__LoadActions(pRaceData, c_rstrFolderName);
	__LoadComboRace(pRaceData, CRaceMotionData::MODE_FAN, c_rstrFolderName + "fan/");
	__LoadComboRace(pRaceData, CRaceMotionData::MODE_BELL, c_rstrFolderName + "Bell/");

	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_WEAPON, "equip_right");
	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_WEAPON_LEFT, "equip_left");
	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_ACCE, "Bip01 Spine2");

}

/*
#ifdef ENABLE_WOLFMAN_CHARACTER
void CPythonOptimizationBoost::__LoadGameWolfmanEx(CRaceData* pRaceData, const std::string& c_rstrFolderName)
{
	if (!pRaceData)
		return;

	__SetWolfmanMotions(pRaceData, CRaceMotionData::MODE_GENERAL, c_rstrFolderName + "general/");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack1.msa", 50);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_COMBO_ATTACK_1, "attack2.msa", 50);
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "skill/").c_str());

	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 1, "split_slash.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 2, "wind_death.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 3, "reef_attack.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 4, "wreckage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 5, "red_possession.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + 6, "blue_possession.msa");


#ifdef ENABLE_SKILLS_LEVEL_OVER_P
	std::vector<int> skillList{ 1, 2, 3, 4, 5};
#else
	std::vector<int> skillList{ 1, 2, 3 };
#endif

	for (const auto& i : skillList)
	{
		std::string END_STRING = "_" + std::to_string(i + 1);

		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 1, std::string("split_slash" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 2, std::string("wind_death" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 3, std::string("reef_attack" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 4, std::string("wreckage" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 5, std::string("red_possession" + END_STRING + ".msa").c_str());
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, CRaceMotionData::NAME_SKILL + (i * CPythonSkill::SKILL_GRADEGAP) + 6, std::string("blue_possession" + END_STRING + ".msa").c_str());
		pRaceData->ReserveComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, 1);
		pRaceData->RegisterComboAttack(CRaceMotionData::MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	}

	__LoadGuildSkill(pRaceData, c_rstrFolderName);
	__LoadFishing(pRaceData, c_rstrFolderName);

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait.msa", 50);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait1.msa", 30);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WAIT, "wait2.msa", 20);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_WALK, "walk.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_RUN, "run.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DAMAGE, "front_damage.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_DEAD, "dead.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_SKILL + 122, "skill_charge.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE, CRaceMotionData::NAME_SKILL + 123, "skill_splash.msa");

	CRaceManager::Instance().SetPathName((c_rstrFolderName + "horse_claw/").c_str());

	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_HORSE_CLAW);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_CLAW, CRaceMotionData::NAME_COMBO_ATTACK_1, "combo_01.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_CLAW, CRaceMotionData::NAME_COMBO_ATTACK_2, "combo_02.msa");
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_CLAW, CRaceMotionData::NAME_COMBO_ATTACK_3, "combo_03.msa");
	pRaceData->ReserveComboAttack(CRaceMotionData::MODE_HORSE_CLAW, COMBO_TYPE_1, 3);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_CLAW, COMBO_TYPE_1, COMBO_INDEX_1, CRaceMotionData::NAME_COMBO_ATTACK_1);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_CLAW, COMBO_TYPE_1, COMBO_INDEX_2, CRaceMotionData::NAME_COMBO_ATTACK_2);
	pRaceData->RegisterComboAttack(CRaceMotionData::MODE_HORSE_CLAW, COMBO_TYPE_1, COMBO_INDEX_3, CRaceMotionData::NAME_COMBO_ATTACK_3);
	__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_HORSE_CLAW, CRaceMotionData::NAME_SKILL + 121, "skill_wildattack.msa");

	__LoadWedding(pRaceData, c_rstrFolderName);
	__LoadActions(pRaceData, c_rstrFolderName);
	__LoadComboRace(pRaceData, CRaceMotionData::MODE_CLAW, c_rstrFolderName + "claw/");

	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_WEAPON, "equip_right_weapon");
	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_WEAPON_LEFT, "equip_left_weapon");
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	pRaceData->RegisterAttachingBoneName(CRaceData::EParts::PART_ACCE, "Bip01 Spine2");
#endif

}
#endif*/

void CPythonOptimizationBoost::__LoadFishing(CRaceData* pRaceData, const std::string& c_rstrFolderName)
{
	CRaceManager::Instance().SetPathName((c_rstrFolderName + "fishing/").c_str());
	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_FISHING);
	for (const auto& fishingMotions : vecFishing)
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_FISHING, std::get<0>(fishingMotions), std::get<1>(fishingMotions));
}

void CPythonOptimizationBoost::__LoadWedding(CRaceData* pRaceData, const std::string& c_rstrFolderName)
{
	CRaceManager::Instance().SetPathName((c_rstrFolderName + "wedding/").c_str());
	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_WEDDING_DRESS);
	for (const auto& weddingMotion : vecWeddingList)
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_WEDDING_DRESS, std::get<0>(weddingMotion), std::get<1>(weddingMotion));
}

void CPythonOptimizationBoost::__LoadGuildSkill(CRaceData* pRaceData, const std::string& c_rstrFolderName)
{
	CRaceManager::Instance().SetPathName((c_rstrFolderName + "skill/").c_str());
	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_GENERAL);
	for (const auto& GuildSkillData : vecGuildSkill)
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, std::get<0>(GuildSkillData), std::get<1>(GuildSkillData));
}

void CPythonOptimizationBoost::__LoadActions(CRaceData* pRaceData, const std::string& c_rstrFolderName)
{
	CRaceManager::Instance().SetPathName((c_rstrFolderName + "action/").c_str());
	pRaceData->RegisterMotionMode(CRaceMotionData::MODE_GENERAL);
	for (const auto& actionMotions : vecActionsList)
		__RegisterCacheMotionData(pRaceData, CRaceMotionData::MODE_GENERAL, std::get<0>(actionMotions), std::get<1>(actionMotions));
}

void CPythonOptimizationBoost::__LoadGameEffects()
{
	for (const auto& effectData : vecEffectList)
		CInstanceBase::RegisterEffect(std::get<0>(effectData), std::get<1>(effectData), std::get<2>(effectData), std::get<3>(effectData));

	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_EXP, CFlyingManager::INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_yellow_small2.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_HP_MEDIUM, CFlyingManager::INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_red_small.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_HP_BIG, CFlyingManager::INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_red_big.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_SP_SMALL, CFlyingManager::INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_blue_warrior_small.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_SP_MEDIUM, CFlyingManager::INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_blue_small.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_SP_BIG, CFlyingManager::INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_blue_big.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_FIREWORK1, CFlyingManager::INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_1.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_FIREWORK2, CFlyingManager::INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_2.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_FIREWORK3, CFlyingManager::INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_3.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_FIREWORK4, CFlyingManager::INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_4.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_FIREWORK5, CFlyingManager::INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_5.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_FIREWORK6, CFlyingManager::INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_6.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_FIREWORK_XMAS, CFlyingManager::INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_xmas.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_CHAIN_LIGHTNING, CFlyingManager::INDEX_FLY_TYPE_NORMAL, "d:/ymir work/pc/shaman/effect/pokroe.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_HP_SMALL, CFlyingManager::INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_red_smallest.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_SKILL_MUYEONG, CFlyingManager::INDEX_FLY_TYPE_AUTO_FIRE, "d:/ymir work/pc/sura/effect/muyeong_fly.msf");
	CFlyingManager::Instance().RegisterIndexedFlyData(CFlyingManager::FLY_QUIVER_ATTACK_NORMAL, CFlyingManager::INDEX_FLY_TYPE_NORMAL, "d:/ymir work/pc/assassin/effect/arrow_02.msf");
}

void CPythonOptimizationBoost::__LoadGameInit()
{
	CInstanceBase::SetDustGap(250);
	CInstanceBase::SetHorseDustGap(500);
	CPythonPlayer::Instance().RegisterEffect(CPythonPlayer::EFFECT_PICK, "d:/ymir work/effect/etc/click/click.mse", true);

	CRaceManager& pkManager = CRaceManager::Instance();
	char szFileName[70];

	for (const auto& data : m_vecRaceData)
	{
		pkManager.CreateRace(data.dwRace);
		pkManager.SelectRace(data.dwRace);

		CRaceData* pRaceData = pkManager.GetSelectedRaceDataPointer();
		if (!pRaceData)
			return;

		if (!pRaceData->LoadRaceData(data.stMSM))
			return;

		pRaceData->RegisterMotionMode(MotionManager.MODE_GENERAL);

		for (const auto& motion : waitMotions)
		{
			snprintf(szFileName, sizeof(szFileName), "%s%s", data.stIntroMotion, motion.stName);

			pRaceData->RegisterMotionData(MotionManager.MODE_GENERAL, motion.wMotionIndex, szFileName, motion.byPercentage);
		}
	}
}

void CPythonOptimizationBoost::__LoadGameNPC()
{
	const auto file = PackGet(NPC_LIST_FILE_NAME);
	if (!file)
		return;

	CMemoryTextFileLoader fileLoader;
	fileLoader.Bind(file->get_size(), file->get_data());

	CTokenVector kTokenVector;

	for (size_t i = 0; i < fileLoader.GetLineCount(); ++i)
	{
		if (!fileLoader.SplitLineByTab(i, &kTokenVector))
			continue;

		const uint32_t& vnum = atoi(kTokenVector[0].c_str());
		const char* name = kTokenVector[1].c_str();

		trim(name);

		if (vnum)
		{
			CRaceManager::Instance().RegisterRaceName(vnum, name);
		}
		else
		{
			const char* src = kTokenVector[2].c_str();
			trim(src);
			CRaceManager::Instance().RegisterRaceSrcName(name, src);
		}
	}
}

void CPythonOptimizationBoost::__RegisterMisc()
{
	for (const auto& [effectId, emoticonString] : effectEmoticonStrings) 
	{
		CInstanceBase::RegisterEffect(effectId, "", std::string("d:/ymir work/effect/etc/emoticon/" + emoticonString + ".mse").c_str(), true);
		CPythonNetworkStream::Instance().RegisterEmoticonString(emoticonString.c_str());
	}

	for (const auto& dungeonMapName : dungeonMapNames) {
		CPythonBackground::Instance().RegisterDungeonMapName(dungeonMapName);
	}
}
#endif
