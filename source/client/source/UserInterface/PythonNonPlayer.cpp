#include "stdafx.h"
#include "../EterFSLib/FileSystemIncl.hpp"
#include "pythonnonplayer.h"
#include "InstanceBase.h"
#include "PythonCharacterManager.h"

#ifdef ENABLE_WIKI
#include "PythonWiki.h"
#endif

bool CPythonNonPlayer::LoadNonPlayerData(const char* c_szFileName)
{
	static DWORD s_adwMobProtoKey[4] =
	{
		4813894,
		18955,
		552631,
		6822045
	};

	const auto filename = PackGet(c_szFileName);
	if (!filename)
		return false;

	DWORD dwFourCC, dwElements, dwDataSize;
	CMappedFile file;

	file.AppendDataBlock(filename->get_data(), filename->get_size());
	file.Read(&dwFourCC, sizeof(DWORD));

	if (dwFourCC != MAKEFOURCC('M', 'M', 'P', 'T'))
	{
		TraceError("CPythonNonPlayer::LoadNonPlayerData: invalid Mob proto type %s", c_szFileName);
		return false;
	}

	file.Read(&dwElements, sizeof(DWORD));
	file.Read(&dwDataSize, sizeof(DWORD));

	BYTE* pbData = new BYTE[dwDataSize];
	file.Read(pbData, dwDataSize);
	/////

	CLZObject zObj;

	if (!CLZO::Instance().Decompress(zObj, pbData, s_adwMobProtoKey))
	{
		delete[] pbData;
		return false;
	}

	DWORD structSize = zObj.GetSize() / dwElements;
	DWORD structDiff = zObj.GetSize() % dwElements;
#ifdef ENABLE_PROTOSTRUCT_AUTODETECT
	if (structDiff != 0 && !CPythonNonPlayer::TMobTableAll::IsValidStruct(structSize))
#else
	if ((zObj.GetSize() % sizeof(TMobTable)) != 0)
#endif
	{
		TraceError("CPythonNonPlayer::LoadNonPlayerData: invalid size %u check data format. structSize %u, structDiff %u", zObj.GetSize(), structSize, structDiff);
		return false;
	}

	for (DWORD i = 0; i < dwElements; ++i)
	{
#ifdef ENABLE_PROTOSTRUCT_AUTODETECT
		CPythonNonPlayer::TMobTable t = { 0 };
		CPythonNonPlayer::TMobTableAll::Process(zObj.GetBuffer(), structSize, i, t);
#else
		CPythonNonPlayer::TMobTable& t = *((CPythonNonPlayer::TMobTable*)zObj.GetBuffer() + i);
#endif
		TMobTable* pTable = &t;

		TMobTable* pNonPlayerData = new TMobTable;
		memcpy(pNonPlayerData, pTable, sizeof(TMobTable));
#ifdef ENABLE_WIKI
		CPythonWiki::Instance().LoadMonster(pNonPlayerData);
#endif
		m_NonPlayerDataMap.insert(TNonPlayerDataMap::value_type(pNonPlayerData->dwVnum, pNonPlayerData));
	}
#ifdef ENABLE_WIKI
	CPythonWiki::Instance().ListReverse();
	CPythonWiki::Instance().SetLoadMonster();
#endif
	delete[] pbData;
	return true;
}

bool CPythonNonPlayer::GetName(DWORD dwVnum, const char** c_pszName)
{
	const TMobTable* p = GetTable(dwVnum);

	if (!p)
		return false;

	*c_pszName = p->szLocaleName;

	return true;
}

bool CPythonNonPlayer::GetInstanceType(DWORD dwVnum, BYTE* pbType)
{
	const TMobTable* p = GetTable(dwVnum);

	if (!p)
		return false;

	*pbType = p->bType;

	return true;
}

const CPythonNonPlayer::TMobTable* CPythonNonPlayer::GetTable(DWORD dwVnum)
{
	TNonPlayerDataMap::iterator itor = m_NonPlayerDataMap.find(dwVnum);

	if (itor == m_NonPlayerDataMap.end())
		return NULL;

	return itor->second;
}

BYTE CPythonNonPlayer::GetEventType(DWORD dwVnum)
{
	const TMobTable* p = GetTable(dwVnum);

	if (!p)
	{
		//Tracef("CPythonNonPlayer::GetEventType - Failed to find virtual number\n");
		return ON_CLICK_EVENT_NONE;
	}

	return p->bOnClickType;
}

#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
bool CPythonNonPlayer::IsAggressive(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return (IS_SET(c_pTable->dwAIFlag, AIFLAG_AGGRESSIVE));
}
#endif

#ifdef ENABLE_GLOBAL_SCALE
uint8_t CPythonNonPlayer::GetMonsterScalePercent(uint32_t dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 100;

	return MINMAX(50, 100, 200);
}
#endif

#ifdef ENABLE_NEW_DISTANCE_CALC
float CPythonNonPlayer::GetMonsterHitRange(uint32_t dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 70.0f;
	/*
	if (c_pTable->fHitRange)
		return c_pTable->fHitRange;
	*/
	return 100.0f;
}
#endif

BYTE CPythonNonPlayer::GetEventTypeByVID(DWORD dwVID)
{
	CInstanceBase* pInstance = CPythonCharacterManager::Instance().GetInstancePtr(dwVID);

	if (NULL == pInstance)
	{
		//Tracef("CPythonNonPlayer::GetEventTypeByVID - There is no Virtual Number\n");
		return ON_CLICK_EVENT_NONE;
	}

	WORD dwVnum = pInstance->GetVirtualNumber();
	return GetEventType(dwVnum);
}

const char* CPythonNonPlayer::GetMonsterName(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		static const char* sc_szEmpty = "";
		return sc_szEmpty;
	}

	return c_pTable->szLocaleName;
}

DWORD CPythonNonPlayer::GetMonsterColor(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return c_pTable->dwMonsterColor;
}


#if defined(WJ_SHOW_MOB_INFO) || defined(ENABLE_TARGET_INFORMATION_SYSTEM)
DWORD CPythonNonPlayer::GetMonsterLevel(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return c_pTable->bLevel;
}
#endif

#ifdef ENABLE_TARGET_INFORMATION_SYSTEM
HP_ULL CPythonNonPlayer::GetMonsterMaxHP(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		HP_ULL dwMaxHP = 0;
		return dwMaxHP;
	}

	return c_pTable->dwMaxHP;
}

DWORD CPythonNonPlayer::GetMonsterRaceFlag(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD dwRaceFlag = 0;
		return dwRaceFlag;
	}

	return c_pTable->dwRaceFlag;
}

DWORD CPythonNonPlayer::GetMonsterDamage1(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD range = 0;
		return range;
	}

	return c_pTable->dwDamageRange[0];
}

DWORD CPythonNonPlayer::GetMonsterDamage2(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD range = 0;
		return range;
	}

	return c_pTable->dwDamageRange[1];
}

DWORD CPythonNonPlayer::GetMonsterExp(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD dwExp = 0;
		return dwExp;
	}

	return c_pTable->dwExp;
}

float CPythonNonPlayer::GetMonsterDamageMultiply(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD fDamMultiply = 0;
		return fDamMultiply;
	}

	return c_pTable->fDamMultiply;
}

DWORD CPythonNonPlayer::GetMonsterST(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD bStr = 0;
		return bStr;
	}

	return c_pTable->bStr;
}

DWORD CPythonNonPlayer::GetMonsterDX(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD bDex = 0;
		return bDex;
	}

	return c_pTable->bDex;
}

bool CPythonNonPlayer::IsMonsterStone(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
	{
		DWORD bType = 0;
		return false;
	}

	return c_pTable->bType == 2;
}
BYTE CPythonNonPlayer::GetMobRegenCycle(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return c_pTable->bRegenCycle;
}

BYTE CPythonNonPlayer::GetMobRegenPercent(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return c_pTable->bRegenPercent;
}

DWORD CPythonNonPlayer::GetMobGoldMin(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return c_pTable->dwGoldMin;
}

DWORD CPythonNonPlayer::GetMobGoldMax(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	return c_pTable->dwGoldMax;
}

DWORD CPythonNonPlayer::GetMobResist(DWORD dwVnum, BYTE bResistNum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;

	if (bResistNum >= MOB_RESISTS_MAX_NUM)
		return 0;

	return c_pTable->cResists[bResistNum];
}
#endif

void CPythonNonPlayer::GetMatchableMobList(int iLevel, int iInterval, TMobTableList* pMobTableList)
{
	/*
		pMobTableList->clear();

		TNonPlayerDataMap::iterator itor = m_NonPlayerDataMap.begin();
		for (; itor != m_NonPlayerDataMap.end(); ++itor)
		{
			TMobTable * pMobTable = itor->second;

			int iLowerLevelLimit = iLevel-iInterval;
			int iUpperLevelLimit = iLevel+iInterval;

			if ((pMobTable->abLevelRange[0] >= iLowerLevelLimit && pMobTable->abLevelRange[0] <= iUpperLevelLimit) ||
				(pMobTable->abLevelRange[1] >= iLowerLevelLimit && pMobTable->abLevelRange[1] <= iUpperLevelLimit))
			{
				pMobTableList->push_back(pMobTable);
			}
		}
	*/
}

#ifdef ENABLE_GLOBAL_SCALE
bool CPythonNonPlayer::LoadMobScale(const char * c_szFileName)
{
	auto file = PackGet(c_szFileName);
	if (!file)
		return false;
	
	CMemoryTextFileLoader kTextFileLoader;
	kTextFileLoader.Bind(file->get_size(), file->get_data());
	CTokenVector kTokenVector;
	
	for (DWORD i = 0; i < kTextFileLoader.GetLineCount(); ++i)
	{
		if (!kTextFileLoader.SplitLineByTab(i, &kTokenVector))
			continue;
		
		if (kTokenVector.size() < 6)
		{
			TraceError("LoadMobScale: invalid line %d (%s).", i, c_szFileName);
			continue;
		}	
		
		DWORD dwMobNum = atoi(kTokenVector[MOBSCALETABLE_MOB_NUM].c_str());
		float fx = atof(kTokenVector[MOBSCALETABLE_X].c_str());
		float fy = atof(kTokenVector[MOBSCALETABLE_Y].c_str());
		float fz = atof(kTokenVector[MOBSCALETABLE_Z].c_str());
		float ra = atof(kTokenVector[MOBSCALETABLE_RANDOM_A].c_str());
		float rb = atof(kTokenVector[MOBSCALETABLE_RANDOM_B].c_str());
		TMobScaleTable * pMobScale = new TMobScaleTable;
		pMobScale->dwMobNum = dwMobNum;
		pMobScale->fx = fx;
		pMobScale->fy = fy;
		pMobScale->fz = fz;
		pMobScale->ra = ra;
		pMobScale->rb = rb;
		m_NonMobScaleDataMap.insert(TNonMobScaleDataMap::value_type(dwMobNum, pMobScale));
	}
	
	return true;
}

const CPythonNonPlayer::TMobScaleTable * CPythonNonPlayer::GetScaleTable(DWORD dwVnum)
{
	TNonMobScaleDataMap::iterator itor = m_NonMobScaleDataMap.find(dwVnum);

	if (itor == m_NonMobScaleDataMap.end())
		return NULL;

	return itor->second;
}

bool CPythonNonPlayer::GetScale(DWORD dwVnum, float & fx, float & fy, float & fz)
{
	const CPythonNonPlayer::TMobScaleTable * c_pTable = GetScaleTable(dwVnum);

	if (!c_pTable)
	{
		fx = 1.0f;
		fy = 1.0f;
		fz = 1.0f;
	}
	else
	{
		if (c_pTable->ra > 0 && c_pTable->rb > 0)
		{
			float scale = frandom(c_pTable->ra, c_pTable->rb);
			fx = scale;
			fy = scale;
			fz = scale;
		}
		else
		{
			fx = c_pTable->fx;
			fy = c_pTable->fy;
			fz = c_pTable->fz;
		}
	}
	
	return true;
}
#endif

#ifdef ENABLE_PRESENT_NPC
#include "PythonBackground.h"
bool CPythonNonPlayer::LoadPresentNPC(const char* szPresentNPCFile)
{
	m_mapPresentNPC.clear();

	const auto file = PackGet(szPresentNPCFile);
	if (!file)
		return false;

	CMemoryTextFileLoader textFileLoader;
	textFileLoader.Bind(file->get_size(), file->get_data());

	CTokenVector TokenVector;

	for (DWORD i = 0; i < textFileLoader.GetLineCount(); ++i)
	{
		if (!textFileLoader.SplitLine(i, &TokenVector, "\t"))
		{
			continue;
		}
		else if (TokenVector.size() != NPC_WEAR_MAX+2)
		{
			continue;
		}
		if ("//" == TokenVector[0].c_str())
			continue;

		const DWORD npcVnum = atoi(TokenVector[0].c_str());
		std::vector<int> m_vec;
		m_vec.resize(NPC_WEAR_MAX);

		for (BYTE i = 0; i < NPC_WEAR_MAX; ++i)
			m_vec[i] = atoi(TokenVector[i+2].c_str());

		if (m_vec[NPC_WEAR_RACE] > 8)
		{
			continue;
		}

		auto it = m_mapPresentNPC.find(TokenVector[1].c_str());

		if (it != m_mapPresentNPC.end())
		{
			it->second.emplace(npcVnum, m_vec);
		}
		else
		{
			std::map<DWORD, std::vector<int>> m_map;
			m_map.emplace(npcVnum, m_vec);
			m_mapPresentNPC.emplace(TokenVector[1].c_str(), m_map);
		}
	}
	return true;
}
int CPythonNonPlayer::GetPresentNPC(const int raceIndex, const BYTE wearIndex)
{
	if (wearIndex >= NPC_WEAR_MAX)
	{
		return -1;
	}

	CPythonBackground& rkBG = CPythonBackground::Instance();
	const auto itSpecial = m_mapPresentNPC.find(rkBG.GetWarpMapName());

	if (itSpecial != m_mapPresentNPC.end())
	{
		auto itEx = itSpecial->second.find(raceIndex);

		if (itEx != itSpecial->second.end())
		{
			return itEx->second[wearIndex];
		}
	}
	const auto itAll = m_mapPresentNPC.find("all");

	if (itAll != m_mapPresentNPC.end())
	{
		auto itEx = itAll->second.find(raceIndex);
		
		if (itEx != itAll->second.end())
		{
			return itEx->second[wearIndex];
		}
	}
	return -1;
}
#endif

#ifdef ENABLE_ALIGNMENT_SYSTEM
#include <json.hpp>
#include <fstream>
bool CPythonNonPlayer::LoadAlignmentProto()
{
	using js = nlohmann::json;
	char file_name[256 + 1];
	snprintf(file_name, sizeof(file_name), "lib/json/alignment_proto.json");
	std::ifstream ifs(file_name);
	if (!ifs.is_open()) { return false; }
	try
	{
		js jf = js::parse(ifs);
		js& arr = jf["alignment"];
		std::vector<char> v_titleName;
		v_titleName.clear();
		for (const auto& i : arr)
		{
			BYTE level = 0;
			TAlignmentTable info = {};

			i.at("level").get_to(level);
			level--;
			i.at("min_point").get_to(info.minPoint);
			i.at("max_point").get_to(info.maxPoint);

			for (const auto& y : i["bonus"])
			{
				std::string str_applyType;
				WORD applyValue;
				y.at("type").get_to(str_applyType);
				y.at("value").get_to(applyValue);

				std::pair<BYTE, BYTE> bonus = StringApplyToPoint(str_applyType.c_str());
				const BYTE applyType = bonus.first;
				if (applyType == CItemData::APPLY_NONE)
				{
					TraceError("Unknow apply type : %s", str_applyType.c_str());
					break; 
				}

				info.bonus.push_back(std::make_pair(applyType, applyValue));
			}

			m_alignMap.insert(std::make_pair(level, info));
		}
		ifs.close();
		m_titleNoneAlignLevel = static_cast<BYTE> (m_alignMap.size());

		ALIGN_MAP::iterator& it = m_alignMap.find(static_cast<BYTE>(m_alignMap.size()) - 1);
		if (it != m_alignMap.end())
			it->second.maxPoint += 1;
	}
	catch (const std::exception& e)
	{
		TraceError("ReadAlignmentProto error : %s ", e.what());
		return false;
	}
	return true;
}

UINT CPythonNonPlayer::GetAlignmentLevel(int align)
{
	for (ALIGN_MAP::iterator it = m_alignMap.begin(); it != m_alignMap.end(); it++)
	{
		if (align >= it->second.minPoint && align < it->second.maxPoint)
		{
			return m_alignMap.size() - 1 - it->first;
		}
	}

	if (align >= 0)
		return m_alignMap.size();
	else if (align > -4000)
		return m_alignMap.size() + 1;
	else if (align > -8000)
		return m_alignMap.size() + 2;
	else if (align > -12000)
		return m_alignMap.size() + 3;
	else
		return m_alignMap.size() + 4;
}

BYTE CPythonNonPlayer::GetAlignmentBonusCount(BYTE level)
{
	ALIGN_MAP::const_iterator it = m_alignMap.find(static_cast<BYTE>(m_alignMap.size()) - level - 1);
	if (it != m_alignMap.end())
	{
		return static_cast<BYTE>(it->second.bonus.size());
	}
	return 0;
}

std::pair<BYTE, WORD> CPythonNonPlayer::GetAlignmentBonusInfo(BYTE level, BYTE idx)
{
	ALIGN_MAP::const_iterator it = m_alignMap.find(static_cast<BYTE>(m_alignMap.size()) - level - 1);
	if (it != m_alignMap.end())
	{
		if (it->second.bonus[idx].second != CItemData::APPLY_NONE)
			return it->second.bonus[idx];
	}
	return std::make_pair(0, 0);
}
#endif

#ifdef ENABLE_MONSTER_SPECULAR
bool CPythonNonPlayer::LoadSpecularTable(const char* c_szFileName)
{
	const auto file = PackGet(c_szFileName);
	if (!file)
		return false;

	CMemoryTextFileLoader kTextFileLoader;
	kTextFileLoader.Bind(file->get_size(), file->get_data());

	CTokenVector kTokenVector;

	for (DWORD i = 0; i < kTextFileLoader.GetLineCount(); ++i)
	{
		if (!kTextFileLoader.SplitLineByTab(i, &kTokenVector))
			continue;

		if (kTokenVector.size() < 2)
		{
			TraceError("LoadSpecularTable: invalid line %d (%s).", i, c_szFileName);
			continue;
		}

		DWORD dwMobNum = atoi(kTokenVector[0].c_str());
		float specular = atof(kTokenVector[1].c_str());

		TMobSpecularTable* pMobSpecular = new TMobSpecularTable;
		pMobSpecular->dwMobNum = dwMobNum;
		pMobSpecular->specular = specular;
		m_NonMobSpecularDataMap.insert(TNonMobSpecularDataMap::value_type(dwMobNum, pMobSpecular));
	}

	return true;
}

const CPythonNonPlayer::TMobSpecularTable* CPythonNonPlayer::GetSpecularTable(DWORD dwVnum)
{
	auto it = m_NonMobSpecularDataMap.find(dwVnum);

	if (it == m_NonMobSpecularDataMap.end())
		return nullptr;

	return it->second;
}

float CPythonNonPlayer::GetSpecularMob(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobSpecularTable* c_pTable = GetSpecularTable(dwVnum);

	float specular = 0.0f;

	if (dwVnum > 0 && dwVnum <= 8)
		return specular;

	if (!c_pTable)
		return specular;

	if (c_pTable->specular > 0 && c_pTable->specular != 0.0f)
	{
		specular = c_pTable->specular;
	}

	return specular;
}

#endif

void CPythonNonPlayer::Clear()
{
}

void CPythonNonPlayer::Destroy()
{
	for (TNonPlayerDataMap::iterator itor = m_NonPlayerDataMap.begin(); itor != m_NonPlayerDataMap.end(); ++itor)
	{
		delete itor->second;
	}

	m_NonPlayerDataMap.clear();
}

CPythonNonPlayer::CPythonNonPlayer()
{
	Clear();
}

CPythonNonPlayer::~CPythonNonPlayer(void)
{
	Destroy();
}

#ifdef ENABLE_WIKI
DWORD CPythonNonPlayer::GetMonsterPrice1(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;
	return c_pTable->dwGoldMin;
}
DWORD CPythonNonPlayer::GetMonsterPrice2(DWORD dwVnum)
{
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;
	return c_pTable->dwGoldMax;
}
char CPythonNonPlayer::GetMonsterResist(DWORD dwVnum, BYTE byResist)
{
	if (byResist >= MOB_RESISTS_MAX_NUM)
		return 0;
	const CPythonNonPlayer::TMobTable* c_pTable = GetTable(dwVnum);
	if (!c_pTable)
		return 0;
	return c_pTable->cResists[byResist];
}
#endif

#ifdef ENABLE_HAIR_SPECULAR
bool CPythonNonPlayer::LoadHairSpecularTable(const char* c_szFileName)
{
	const auto file = PackGet(c_szFileName);
	if (!file)
		return false;

	CMemoryTextFileLoader kTextFileLoader;
	kTextFileLoader.Bind(file->get_size(), file->get_data());
	CTokenVector kTokenVector;

	for (DWORD i = 0; i < kTextFileLoader.GetLineCount(); ++i)
	{
		if (!kTextFileLoader.SplitLineByTab(i, &kTokenVector))
			continue;

		if (kTokenVector.size() < 2)
		{
			TraceError("LoadSpecularTable: invalid line %d (%s).", i, c_szFileName);
			continue;
		}

		DWORD dwMobNum = atoi(kTokenVector[0].c_str());
		float specular = atof(kTokenVector[1].c_str());

		THairSpecularTable* hairSpecular = new THairSpecularTable;
		hairSpecular->dwItemVnum = dwMobNum;
		hairSpecular->specular = specular;
		m_NonHairSpecularDataMap.insert(m_NoHairSpecularDataMap::value_type(dwMobNum, hairSpecular));
	}

	return true;
}

const CPythonNonPlayer::THairSpecularTable* CPythonNonPlayer::GetHairSpecularTable(DWORD dwVnum)
{
	const auto it = m_NonHairSpecularDataMap.find(dwVnum);

	if (it != m_NonHairSpecularDataMap.end())
		return it->second;

	return nullptr;
}

float CPythonNonPlayer::GetHairSpecular(DWORD dwVnum)
{
	const CPythonNonPlayer::THairSpecularTable* c_pTable = GetHairSpecularTable(dwVnum);

	if (!c_pTable)
		return 0.0f;

	if (c_pTable->specular > 0 && c_pTable->specular != 0.0f)
		return c_pTable->specular;

	return 0.0f;
}
#endif