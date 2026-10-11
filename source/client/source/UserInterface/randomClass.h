#pragma once
class random32
{
public:
	random32();
	~random32();

private:
	bool m_dalga;
};

random32::random32()
{
}

random32::~random32()
{
}

/*
// #ifdef ENABLE_WIKI
// #include "PythonWiki.h"
// #include "PythonNetworkStream.h"
// #include "PythonPlayer.h"
// #include "../GameLib/ItemManager.h"
// #include <map>
// #include "../EterFSLib/FileSystemIncl.hpp"

// bool printLocalDatainSysser = false;

// static void DecryptionVnum(std::string& vnum)
// {
	// for (auto& str : vnum)
	// {
		// switch (str)
		// {
			// case 's':
			// case 'a': {str = '0'; break; }
			// case 'e':
			// case 'b': {str = '1'; break; }
			// case 'x':
			// case 'c': {str = '2'; break; }
			// case 'p':
			// case 'd': {str = '3'; break; }
			// case 'f':
			// case 'o': {str = '4'; break; }
			// case 'r':
			// case 'k': {str = '5'; break; }
			// case 'n':
			// case 'l': {str = '6'; break; }
			// case 'z':
			// case 'm': {str = '7'; break; }
			// case 'y':
			// case 'q': {str = '8'; break; }
			// case 'g':
			// case 't': {str = '9'; break; }
			// default:    break;
		// }
	// }
// }

// CPythonWiki::CPythonWiki()
// {
	// m_isLoaded = false;
	// m_isLoadedMonster = false;
	// Destroy();
// }

// CPythonWiki::~CPythonWiki()
// {
	// Destroy();
// }

// void CPythonWiki::Destroy()
// {
	// auto it = m_vecRefineTable.begin();

	// while (it != m_vecRefineTable.end())
	// {
		// delete it->second;
		// it = m_vecRefineTable.erase(it);
	// }
	// m_vecRefineTable.clear();
// }

// void CPythonWiki::ReadData(const char* localeFile)
// {
	// if (m_isLoaded)
		// return;

	// if (!LoadRefineTable("general/wikipedia/refine_table.txt"))
		// TraceError("CPythonApplication - CPythonWiki::LoadRefineTable(general/wikipedia/refine_table.txt)");

	// char szItemProto[256]{};

	// snprintf(szItemProto, sizeof(szItemProto), "%s/item_proto", localeFile);

	// if (!LoadItemTable(szItemProto))
		// TraceError("CPythonWiki - LoadItemTable(%s) Error", szItemProto);

	// ReadSpecialDropItemFile("general/wikipedia/special_item_group.txt");
	// ReadMobDropItemFile("general/wikipedia/mob_drop_item.txt");

	// LoadCubeInformations("general/wikipedia/cube.txt");

	// for (const auto& entry : dungeonMobMap)
	// {
		// DWORD category = entry.first;
		// const std::vector<character_data>& dataVector = entry.second;

		// for (const character_data& data : dataVector) {
			// m_vecMonsterCategory[category].emplace_back(data);
		// }
	// }

	// m_isLoaded = true;
// }

// bool CPythonWiki::ReadSpecialDropItemFile(const char* c_pszFileName)
// {
	// const auto file = PackGet(c_pszFileName);
	// if (!file)
		// return false;

	// CMemoryTextFileLoader textFileLoader;
	// textFileLoader.Bind(file->get_size(), file->get_data());

	// CTokenVector tokenVector;
	// std::vector<special_data> vecSpecialData{};
	// DWORD itemVnum = 0;
	// for (DWORD i = 0; i < textFileLoader.GetLineCount(); ++i)
	// {
		// if (!textFileLoader.SplitLine(i, &tokenVector, "\t"))
			// continue;

		// if (tokenVector[0] == "Vnum")
		// {
			// m_vecSpecialDrop.emplace(itemVnum, vecSpecialData);
			// vecSpecialData.clear();
			// DecryptionVnum(tokenVector[1]);
			// itemVnum = std::stoi(tokenVector[1]);
		// }
		// else
		// {
			// DecryptionVnum(tokenVector[1]);
			// DecryptionVnum(tokenVector[2]);
			// vecSpecialData.push_back(special_data(std::stoi(tokenVector[1]), std::stoi(tokenVector[2])));
		// }
	// }
	// m_vecSpecialDrop.emplace(itemVnum, vecSpecialData);
	// return true;
// }

// bool CPythonWiki::ReadMobDropItemFile(const char* c_pszFileName)
// {
	// const auto file = PackGet(c_pszFileName);
	// if (!file)
		// return false;

	// CMemoryTextFileLoader textFileLoader;
	// textFileLoader.Bind(file->get_size(), file->get_data());

	// CTokenVector tokenVector;
	// std::vector<special_data> vecSpecialData{};
	// DWORD mobVnum = 0;
	// for (DWORD i = 0; i < textFileLoader.GetLineCount(); ++i)
	// {
		// if (!textFileLoader.SplitLine(i, &tokenVector, "\t"))
			// continue;

		// if (tokenVector[0] == "Mob")
		// {
			// m_vecMobDrop.emplace(mobVnum, vecSpecialData);
			// vecSpecialData.clear();
			// DecryptionVnum(tokenVector[1]);
			// mobVnum = std::stoi(tokenVector[1]);
		// }
		// else
		// {
			// DecryptionVnum(tokenVector[1]);
			// DecryptionVnum(tokenVector[2]);
			// vecSpecialData.push_back(special_data(std::stoi(tokenVector[1]), std::stoi(tokenVector[2])));
		// }
	// }
	// m_vecMobDrop.emplace(mobVnum, vecSpecialData);
	// return true;
// }

// static bool isHigherLevel(const character_data &i, const character_data &j)
// {
	// return (i.level > j.level);
// }

// bool isLowerLevel(const character_data &i, const character_data &j)
// {
	// return (i.level < j.level);
// }

// bool CPythonWiki::LoadItemTable(const char* c_szFileName)
// {
	// const auto file = PackGet(c_szFileName);
	// if (!file)
		// return false;

	// DWORD dwFourCC{}, dwElements{}, dwDataSize{}, dwVersion{}, dwStride{};

	// DWORD s_adwItemProtoKey[4] =
	// {
		// 173217,
		// 72619434,
		// 408587239,
		// 27973291
	// };

	// CMappedFile mappedFile;
	// mappedFile.AppendDataBlock(file->get_data(), file->get_size());

	// mappedFile.Read(&dwFourCC, sizeof(DWORD));

	// if (dwFourCC == MAKEFOURCC('M', 'I', 'P', 'X'))
	// {
		// mappedFile.Read(&dwVersion, sizeof(DWORD));
		// mappedFile.Read(&dwStride, sizeof(DWORD));
		// if (dwVersion != 1)
		// {
			// TraceError("CPythonItem::LoadItemTable: invalid item_proto[%s] VERSION[%d]", c_szFileName, dwVersion);
			// return false;
		// }
		// if (dwStride != sizeof(CItemData::TItemTable))
		// {
			// TraceError("CPythonItem::LoadItemTable: invalid item_proto[%s] STRIDE[%d] != sizeof(SItemTable)",c_szFileName, dwStride, sizeof(CItemData::TItemTable));
			// return false;
		// }
	// }
	// else if (dwFourCC != MAKEFOURCC('M', 'I', 'P', 'T'))
	// {
		// TraceError("CPythonItem::LoadItemTable: invalid item proto type %s", c_szFileName);
		// return false;
	// }

	// mappedFile.Read(&dwElements, sizeof(DWORD));
	// mappedFile.Read(&dwDataSize, sizeof(DWORD));

	// BYTE* pbData = new BYTE[dwDataSize];
	// mappedFile.Read(pbData, dwDataSize);

	// CLZObject zObj{};

	// if (!CLZO::Instance().Decompress(zObj, pbData, s_adwItemProtoKey))
	// {
		// delete[] pbData;
		// return false;
	// }

	// CItemData::TItemTable* table{ (CItemData::TItemTable*)zObj.GetBuffer() };

	// for (DWORD i{}; i < dwElements; ++i, ++table)
		// LoadItem(table);

	// delete[] pbData;


	// for (DWORD j{}; j < raceNum; j++)
	// {
		// std::sort(m_vecWeapon[j].begin(), m_vecWeapon[j].end(), isHigherLevel);
		// std::sort(m_vecArmor[j].begin(), m_vecArmor[j].end(), isHigherLevel);
		// std::sort(m_vecHelmets[j].begin(), m_vecHelmets[j].end(), isHigherLevel);
		// std::sort(m_vecShields[j].begin(), m_vecShields[j].end(), isHigherLevel);
		// std::sort(m_vecEarrings[j].begin(), m_vecEarrings[j].end(), isHigherLevel);
		// std::sort(m_vecBracelet[j].begin(), m_vecBracelet[j].end(), isHigherLevel);
		// std::sort(m_vecNecklace[j].begin(), m_vecNecklace[j].end(), isHigherLevel);
		// std::sort(m_vecShoes[j].begin(), m_vecShoes[j].end(), isHigherLevel);
		// std::sort(m_vecBelt[j].begin(), m_vecBelt[j].end(), isHigherLevel);
		// std::sort(m_vecPendant[j].begin(), m_vecPendant[j].end(), isHigherLevel);
		// std::sort(m_vecGlove[j].begin(), m_vecGlove[j].end(), isHigherLevel);
	// }

	// return true;
// }

// bool CPythonWiki::BlackList(const DWORD &vnum, const DWORD &type, const DWORD &subtype)
// {
	// for (UINT i{}; i < _countof(showItemList9); ++i)
	// {
		// if (vnum == showItemList9[i])
			// return true;
	// }
return false == not show

// return false;
// }

// BYTE CPythonWiki::GetRefineLevel(const DWORD &vnum, const DWORD &type, const DWORD &subtype)
// {
// #ifdef ENABLE_PENDANT_ITEM
	// if (type == CItemData::ITEM_PENDANT)
		// return 25;
// #endif
	// /*
	Ymir new weapon and armor set!
	// constexpr DWORD darkVnums[] = {
			// 320,
			// 340,
			// 1190,
			// 2210,
			// 3230,
			// 5170,
			// 7310,
			// 12780,
			// 12800,
			// 12820,
			// 12840,
			// 12860,
			// 21210,
			// 21230,
			// 21250,
			// 21270,
			// 13190,
			// 14580,
			// 15480,
			// 16580,
			// 17580,
			// 18100,
			// 24420
	// };
	// for (UINT i = 0; i < _countof(darkVnums); i++)
	// {
		// if (vnum >= darkVnums[i] && vnum <= darkVnums[i] + 15)
			// return 15;
	// }*/
	// return 9;
// }

// refineTable* CPythonWiki::GetRefineItem(const DWORD &index)
// {
	// const auto it = m_vecRefineTable.find(index);

	// if (it != m_vecRefineTable.end())
		// return it->second;

	// return NULL;
// }

// bool CPythonWiki::LoadRefineTable(const char* c_szFileName)
// {
	// const auto file = PackGet(c_szFileName);
	// if (!file)
		// return false;

	// CMemoryTextFileLoader textFileLoader;
	// textFileLoader.Bind(file->get_size(), file->get_data());

	// CTokenVector TokenVector;

	// for (DWORD i{}; i < textFileLoader.GetLineCount(); ++i)
	// {
		// if (textFileLoader.GetLineString(i)[0] == '#')
			// continue;

		// if (!textFileLoader.SplitLine(i, &TokenVector, "\t"))
			// continue;

		// if (TokenVector.size() != 15)
		// {
			// TraceError("CPythonWiki::LoadRefineTable(%s) - StrangeLine in %d\n", c_szFileName, i);
			// continue;
		// }
		// refineTable* p = new refineTable;
		// memset(p, 0, sizeof(refineTable));

		// p->id = (DWORD)atoi(TokenVector[0].c_str());
		// p->refine_count = 0;

		// int row{1};

		// for (DWORD j{}; j < MAX_REFINE_ITEM; ++j)
		// {
			// p->item_vnums[j] = (DWORD)atoi(TokenVector[row].c_str());

			// if (p->item_vnums[j] != 0){
				// p->refine_count = j + 1;
			// }

			// row += 1;
			// p->item_count[j] = (DWORD)atoi(TokenVector[row].c_str());
			// row += 1;
		// }

		// p->cost = (DWORD)atoi(TokenVector[11].c_str());
		// p->prob = (DWORD)atoi(TokenVector[14].c_str());
		// m_vecRefineTable.insert(std::make_pair(p->id, p));
	// }

	// return true;
// }

// bool CPythonWiki::LoadCubeInformations(const char* c_szFileName)
// {
	// m_vecCube.clear();

	// const auto file = PackGet(c_szFileName);
	// if (!file)
		// return false;

	// cubeTable cubeT{};
	// cubeT.resetAllData();

	// CMemoryTextFileLoader textFileLoader;
	// textFileLoader.Bind(file->get_size(), file->get_data());
	// CTokenVector TokenVector;

	// int index{0};

	// for (DWORD i{}; i < textFileLoader.GetLineCount(); ++i)
	// {
		// if (!textFileLoader.SplitLine(i, &TokenVector, "\t"))
			// continue;

		// if (strcmp(TokenVector[0].c_str(), "//") == 0)
			// continue;

		// else if (strcmp(TokenVector[0].c_str(), "#") == 0)
			// continue;

		// else if (strcmp(TokenVector[0].c_str(), "section") == 0) // start
		// {
			// cubeT.resetAllData();
			// continue;
		// }

		// else if (strcmp(TokenVector[0].c_str(), "end") == 0) // end
		// {
			// m_vecCube.push_back(cubeT);
			// cubeT.upgradeVec.clear();
			// continue;
		// }

		// else if (strcmp(TokenVector[0].c_str(), "npc") == 0) // end
		// {
			// if (TokenVector.size() < 2)
				// continue;

			// cubeT.npcVnum = std::stoi(TokenVector[1].c_str());
			// continue;
		// }

		// else if (strcmp(TokenVector[0].c_str(), "item") == 0) // end
		// {
			// if (TokenVector.size() < 3)
				// continue;

			// if (cubeT.upgradeVec.size() == 10)
				// continue;

			// DWORD itemVnum{ static_cast<DWORD>(std::stoi(TokenVector[1].c_str())) };
			// DWORD itemCount{ static_cast<DWORD>(std::stoi(TokenVector[2].c_str())) };

			// cubeT.upgradeVec.push_back({ itemVnum, itemCount });
			// continue;

		// }
		// else if (strcmp(TokenVector[0].c_str(), "reward") == 0) // end
		// {
			// if (TokenVector.size() < 3)
				// continue;

			// cubeT.vnum_reward = std::stoi(TokenVector[1].c_str());
			// cubeT.count_reward = std::stoi(TokenVector[2].c_str());
			// continue;
		// }

		// else if (strcmp(TokenVector[0].c_str(), "gold") == 0) // end
		// {
			// if (TokenVector.size() < 2)
				// continue;

			// cubeT.itemCost = std::stoll(TokenVector[1].c_str());
			// continue;
		// }

		// else if (strcmp(TokenVector[0].c_str(), "percent") == 0) // end
		// {
			// if (TokenVector.size() < 2)
				// continue;

			// cubeT.upgradeChange = std::stoi(TokenVector[1].c_str());
			// continue;
		// }

		// else if (strcmp(TokenVector[0].c_str(), "gem") == 0) // end
		// {
			// if (TokenVector.size() < 2)
				// continue;

			// cubeT.gemCost = std::stoi(TokenVector[1].c_str());
			// continue;
		// }
	// }

	// return true;
// }


// bool isLastItem(DWORD &itemVnum, const char* szname, BYTE &itemType, BYTE &itemSubtype)
// {

// DWORD maxRefine = CPythonWiki::Instance().GetRefineLevel(itemVnum, itemType, itemSubtype);
// std::string strrefine = "+";
// strrefine += std::to_string(maxRefine);
// if (str.find(strrefine.c_str()) != std::string::npos)
	// return true;

// return false;
// }

// void CPythonWiki::ListReverse()
// {
	// if (m_isLoadedMonster)
		// return;

	// for (DWORD j{}; j < 3; j++)
	// {
		// std::stable_sort(m_vecStoneCategory[j].begin(), m_vecStoneCategory[j].end(), isLowerLevel);
		// std::stable_sort(m_vecBossCategory[j].begin(), m_vecBossCategory[j].end(), isLowerLevel);
		// std::stable_sort(m_vecMonsterCategory[j].begin(), m_vecMonsterCategory[j].end(), isLowerLevel);
	// }
// }

// bool BlackListMonster(const DWORD &vnum)
// {
	// for (UINT i{}; i < _countof(showMobList); ++i)
	// {
		// if (vnum == showMobList[i])
			// return false;
// }

// void CPythonWiki::LoadMonster(CPythonNonPlayer::TMobTable* monster)
// {
	// if (m_isLoadedMonster)
		// return;

	// if (BlackListMonster(monster->dwVnum))
		// return;

	// if (monster->bType == 0 || monster->bType == 2) // monster & stone
	// {
		// if (monster->bLevel >= 1 && monster->bLevel <= 99)
		// {
			// if (monster->bType == 2)
				// m_vecStoneCategory[0].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			// else if (monster->bRank >= CPythonNonPlayer::MOB_RANK_BOSS)
				// m_vecBossCategory[0].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			// else
				// m_vecMonsterCategory[0].emplace_back(character_data(monster->dwVnum, monster->bLevel));
		// }
		// else if (monster->bLevel >= 100 && monster->bLevel <= 120)
		// {
			// if (monster->bType == 2)
				// m_vecStoneCategory[1].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			// else if (monster->bRank >= CPythonNonPlayer::MOB_RANK_BOSS)
				// m_vecBossCategory[1].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			// else
				// m_vecMonsterCategory[1].emplace_back(character_data(monster->dwVnum, monster->bLevel));
		// }
		// else if (monster->bLevel >= 121)
		// {
			// if (monster->bType == 2)
				// m_vecStoneCategory[2].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			// else if (monster->bRank >= CPythonNonPlayer::MOB_RANK_BOSS)
				// m_vecBossCategory[2].emplace_back(character_data(monster->dwVnum, monster->bLevel));
			// else
				// m_vecMonsterCategory[2].emplace_back(character_data(monster->dwVnum, monster->bLevel));
		// }
	// }
// }

// void CPythonWiki::LoadItem(CItemData::TItemTable* item)
// {
	// if (isLastItem(item->dwVnum, item->szLocaleName, item->bType, item->bSubType))
	// {
		// if (!BlackList(item->dwVnum, item->bType, item->bSubType))
			// return;

		// DWORD itemLevel{};

		// for (DWORD j{}; j < CItemData::ITEM_LIMIT_MAX_NUM; j++)
		// {
			// if (item->aLimits[j].bType == CItemData::LIMIT_LEVEL)
			// {
				// itemLevel = item->aLimits[j].lValue;
				// break;
			// }
		// }

		// switch (item->bType)
		// {
		// case CItemData::ITEM_TYPE_WEAPON:
		// {
			// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
			// {
				// if (!(item->dwAntiFlags & flagList[j]))
					// m_vecWeapon[j].emplace_back(character_data(item->dwVnum, itemLevel));	
			// }
			// break;
		// }
		// case CItemData::ITEM_TYPE_ARMOR:
		// {
			// switch (item->bSubType)
			// {
			// case CItemData::ARMOR_BODY:
			// {
				// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
				// {
					// if (!(item->dwAntiFlags & flagList[j]))
						// m_vecArmor[j].emplace_back(character_data(item->dwVnum, itemLevel));
				// }
				// break;
			// }
			// case CItemData::ARMOR_HEAD:
			// {
				// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
				// {
					// if (!(item->dwAntiFlags & flagList[j]))
						// m_vecHelmets[j].emplace_back(character_data(item->dwVnum, itemLevel));
				// }
				// break;
			// }

			// case CItemData::ARMOR_SHIELD:
			// {
				// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
				// {
					// if (!(item->dwAntiFlags & flagList[j]))
						// m_vecShields[j].emplace_back(character_data(item->dwVnum, itemLevel));
				// }
				// break;
			// }

			// case CItemData::ARMOR_WRIST:
			// {
				// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
				// {
					// if (!(item->dwAntiFlags & flagList[j]))
						// m_vecBracelet[j].emplace_back(character_data(item->dwVnum, itemLevel));
				// }
				// break;
			// }

			// case CItemData::ARMOR_FOOTS:
			// {
				// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
				// {
					// if (!(item->dwAntiFlags & flagList[j]))
						// m_vecShoes[j].emplace_back(character_data(item->dwVnum, itemLevel));
				// }
				// break;
			// }

			// case CItemData::ARMOR_NECK:
			// {
				// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
				// {
					// if (!(item->dwAntiFlags & flagList[j]))
						// m_vecNecklace[j].emplace_back(character_data(item->dwVnum, itemLevel));
				// }
				// break;
			// }

			// case CItemData::ARMOR_EAR:
			// {
				// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
				// {
					// if (!(item->dwAntiFlags & flagList[j]))
						// m_vecEarrings[j].emplace_back(character_data(item->dwVnum, itemLevel));
				// }
				// break;
			// }

			// default:
				// break;
			// }
		// }

		// case CItemData::ITEM_TYPE_BELT:
		// {
			// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
			// {
				// if (item->bType == CItemData::ITEM_TYPE_BELT)
				// {
					// if (!(item->dwAntiFlags & flagList[j]))
					// {
						// m_vecBelt[j].emplace_back(character_data(item->dwVnum, itemLevel));
					// }
				// }


			// }
			// break;
		// }

		// case CItemData::ITEM_PENDANT:
		// {
			// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
			// {
				// if (!(item->dwAntiFlags & flagList[j]))
					// m_vecPendant[j].emplace_back(character_data(item->dwVnum, itemLevel));
			// }
			// break;
		// }

		// case CItemData::ITEM_GLOVE:
		// {
			// for (BYTE j{}; j < JOB_MAX_NUM; ++j)
			// {
				// if (!(item->dwAntiFlags & flagList[j]))
					// m_vecGlove[j].emplace_back(character_data(item->dwVnum, itemLevel));
			// }
			// break;
		// }

		// default:
			// break;
		// }
	// }

// }

// PyObject* wikiGetRefineItems(PyObject* poSelf, PyObject* poArgs)
// {
	// int iRefineIndex{};

	// if (!PyTuple_GetInteger(poArgs, 0, &iRefineIndex))
		// return Py_BadArgument();

	// const auto item{ CPythonWiki::Instance().GetRefineItem(iRefineIndex) };

	// if (!item)
		// return Py_BuildValue("i", 0);

	// return Py_BuildValue("iiiiiiiiiiiiii", item->id,item->item_vnums[0], item->item_count[0],item->item_vnums[1], item->item_count[1],item->item_vnums[2], item->item_count[2],item->item_vnums[3], item->item_count[3],item->item_vnums[4], item->item_count[4],item->cost, item->prob, item->refine_count);
// }

// PyObject* wikiIsBlackList(PyObject* poSelf, PyObject* poArgs)
// {
	// int iItemVnum{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		// return Py_BadArgument();

	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iItemVnum))
		// return Py_BadArgument();

	// int iSubtype{};
	// if (!PyTuple_GetInteger(poArgs, 2, &iItemVnum))
		// return Py_BadArgument();
	// return Py_BuildValue("i", CPythonWiki::Instance().BlackList(iItemVnum, iType, iSubtype));
// }

// PyObject* wikiGetCategorySize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// int iCategoryType{};

	// if (!PyTuple_GetInteger(poArgs, 1, &iCategoryType))
		// return Py_BadArgument();

	// if (iType >= 0 && iType <= JOB_MAX_NUM)
	// {
		// if (iCategoryType == WIKI_WEAPONS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecWeapon[iType].size());
		// else if (iCategoryType == WIKI_ARMORS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecArmor[iType].size());
		// else if (iCategoryType == WIKI_HELMETS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecHelmets[iType].size());
		// else if (iCategoryType == WIKI_SHIELDS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecShields[iType].size());
		// else if (iCategoryType == WIKI_EARRINGS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecEarrings[iType].size());
		// else if (iCategoryType == WIKI_BRACELETS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecBracelet[iType].size());
		// else if (iCategoryType == WIKI_NECKLACES)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecNecklace[iType].size());
		// else if (iCategoryType == WIKI_SHOES)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecShoes[iType].size());
		// else if (iCategoryType == WIKI_BELTS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecBelt[iType].size());
		// else if (iCategoryType == WIKI_PENDANTS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecPendant[iType].size());
		// else if (iCategoryType == WIKI_GLOVES)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecGlove[iType].size());
	// }


	// return Py_BuildValue("i", WIKI_WEAPONS);
// }

// PyObject* wikiGetCategoryData(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// int iCategoryType{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iCategoryType))
		// return Py_BadArgument();
	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 2, &iIndex))
		// return Py_BadArgument();

	// if (iType >= 0 && iType <= JOB_MAX_NUM)
	// {
		// if (iCategoryType == WIKI_WEAPONS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecWeapon[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_ARMORS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecArmor[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_HELMETS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecHelmets[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_SHIELDS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecShields[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_EARRINGS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecEarrings[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_BRACELETS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecBracelet[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_NECKLACES)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecNecklace[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_SHOES)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecShoes[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_BELTS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecBelt[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_PENDANTS)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecPendant[iType][iIndex].itemVnum);
		// else if (iCategoryType == WIKI_GLOVES)
			// return Py_BuildValue("i", CPythonWiki::Instance().m_vecGlove[iType][iIndex].itemVnum);
	// }
	// return Py_BuildValue("i", 0);
// }

// PyObject* wikiGetRefineMaxLevel(PyObject* poSelf, PyObject* poArgs)
// {
	// int iItemVnum{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		// return Py_BuildException();

	// CItemManager::Instance().SelectItemData(iItemVnum);
	// CItemData* pItemData{ CItemManager::Instance().GetSelectedItemDataPointer() };

	// if (!pItemData)
		// return Py_BuildValue("i", CPythonWiki::Instance().GetRefineLevel(iItemVnum, 0, 0));

	// return Py_BuildValue("i", CPythonWiki::Instance().GetRefineLevel(iItemVnum, pItemData->GetType(), pItemData->GetSubType()));
// }

// PyObject* wikiGetChestSize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BuildException();

	// if (iType == BOSS_CHEST)
		// return Py_BuildValue("i", _countof(bossChests));
	// else if (iType == DUNGEON_CHEST)
		// return Py_BuildValue("i", _countof(dungeonChests));
	// else if (iType == OTHER_CHEST)
		// return Py_BuildValue("i", _countof(otherChests));
	// else if (iType == EVENT_CHEST)
		// return Py_BuildValue("i", _countof(eventChests));

	// return Py_BuildValue("i", 0);
// }

// PyObject* wikiGetChestData(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BuildException();

	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		// return Py_BuildException();

	// if (iType == BOSS_CHEST)
		// return Py_BuildValue("ii", bossChests[iIndex][0], bossChests[iIndex][1]);
	// else if (iType == DUNGEON_CHEST)
		// return Py_BuildValue("ii", dungeonChests[iIndex][0], dungeonChests[iIndex][1]);
	// else if (iType == OTHER_CHEST)
		// return Py_BuildValue("ii", otherChests[iIndex][0], otherChests[iIndex][1]);
	// else if (iType == EVENT_CHEST)
		// return Py_BuildValue("ii", eventChests[iIndex][0], eventChests[iIndex][1]);

	// return Py_BuildValue("ii", 0, 0);
// }

// PyObject* wikiGetSpecialInfoSize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iItemVnum{};

	// if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		// return Py_BuildException();

	// const auto it{ CPythonWiki::Instance().m_vecSpecialDrop.find(iItemVnum) };

	// if (it != CPythonWiki::Instance().m_vecSpecialDrop.end())
		// return Py_BuildValue("i", it->second.size());

	// return Py_BuildValue("i", 0);
// }

// PyObject* wikiGetSpecialInfoData(PyObject* poSelf, PyObject* poArgs)
// {
	// int iItemVnum{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		// return Py_BuildException();

	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		// return Py_BuildException();

	// const auto it { CPythonWiki::Instance().m_vecSpecialDrop.find(iItemVnum)};

	// if (it != CPythonWiki::Instance().m_vecSpecialDrop.end())
		// return Py_BuildValue("ii", it->second[iIndex].itemVnum, it->second[iIndex].count);

	// return Py_BuildValue("ii", 0, 0);
// }

// PyObject* wikiGetMobInfoSize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iItemVnum{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		// return Py_BuildException();

	// const auto it {CPythonWiki::Instance().m_vecMobDrop.find(iItemVnum)};

	// if (it != CPythonWiki::Instance().m_vecMobDrop.end())
		// return Py_BuildValue("i", it->second.size());
	// return Py_BuildValue("i", 0);
// }

// PyObject* wikiGetMobInfoData(PyObject* poSelf, PyObject* poArgs)
// {
	// int iItemVnum{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		// return Py_BuildException();

	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		// return Py_BuildException();

	// const auto it{ CPythonWiki::Instance().m_vecMobDrop.find(iItemVnum) } ;
	// if (it == CPythonWiki::Instance().m_vecMobDrop.end())
		// return Py_BuildValue("ii",0,0);
	// return Py_BuildValue("ii", it->second[iIndex].itemVnum, it->second[iIndex].count);
// }

// PyObject* wikiGetBossSize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// if (iType == 3) // event boss
		// return Py_BuildValue("i", sizeof(eventBoss) / sizeof(eventBoss[0]));

	// return Py_BuildValue("i", CPythonWiki::Instance().m_vecBossCategory[iType].size());
// }

// PyObject* wikiGetBossData(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		// return Py_BadArgument();

	// if (iType == 3) // event boss
		// return Py_BuildValue("i", eventBoss[iIndex]);

	// return Py_BuildValue("i", CPythonWiki::Instance().m_vecBossCategory[iType][iIndex]);
// }

// PyObject* wikiCostumeSize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// const auto it{ m_CostumeData.find(iType) };

	// if (it != m_CostumeData.end())
		// return Py_BuildValue("i", it->second.size());

	// return Py_BuildValue("i", 0);
// }
// PyObject* wikiCostumeData(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		// return Py_BadArgument();

	// const auto it{ m_CostumeData.find(iType) } ;
	// if (it != m_CostumeData.end())
		// return Py_BuildValue("i", it->second[iIndex]);
	// return Py_BuildValue("i", 0);
// }

// PyObject* wikiGetMonsterSize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// return Py_BuildValue("i", CPythonWiki::Instance().m_vecMonsterCategory[iType].size());
// }

// PyObject* wikiGetMonsterData(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		// return Py_BadArgument();

	// return Py_BuildValue("i", CPythonWiki::Instance().m_vecMonsterCategory[iType][iIndex]);
// }

// PyObject* wikiGetStoneSize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// return Py_BuildValue("i", CPythonWiki::Instance().m_vecStoneCategory[iType].size());
// }

// PyObject* wikiGetStoneData(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BadArgument();

	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		// return Py_BadArgument();

	// return Py_BuildValue("i", CPythonWiki::Instance().m_vecStoneCategory[iType][iIndex]);
// }

// PyObject* wikiGetItemDropFromChest(PyObject* poSelf, PyObject* poArgs)
// {
	// int szItemVnum{};
	// if (!PyTuple_GetInteger(poArgs, 0, &szItemVnum))
		// return Py_BadArgument();

	// bool szIsRefineItem{false};
	// if (!PyTuple_GetBoolean(poArgs, 1, &szIsRefineItem))
		// return Py_BadArgument();

	// PyObject* poList{ PyList_New(0) };

	// const BYTE refineLevel = szIsRefineItem ? CPythonWiki::Instance().GetRefineLevel(szItemVnum, 0, 0) : 0 ;
	// const auto m_vec_ItemRange{ CPythonWiki::Instance().GetSpecialDrop() };

	// for (const auto& [chestVnum, chestData] : m_vec_ItemRange)
	// {
		// if (chestData.size())
		// {
			// if (szIsRefineItem)
			// {
				// for (const auto& dataItem : chestData)
				// {
					// if (szItemVnum >= dataItem.itemVnum && szItemVnum <= dataItem.itemVnum + refineLevel)
					// {
						// const auto obj{ Py_BuildValue("i", chestVnum) };
						// PyList_Append(poList, obj);
// #ifdef ENABLE_LEAK_FIX
						// fix_leak.push_back(obj);
// #endif
						// break;
					// }
				// }
			// }
			// else
			// {
				// for (const auto& dataItem : chestData)
				// {
					// if (szItemVnum == dataItem.itemVnum)
					// {
						// const auto obj{ Py_BuildValue("i", chestVnum) };
						// PyList_Append(poList, obj);
// #ifdef ENABLE_LEAK_FIX
						// fix_leak.push_back(obj);
// #endif
						// break;
					// }

				// }
			// }

		// }
	// }
// #ifdef ENABLE_LEAK_FIX
	// fix_leak.push_back(poList);
// #endif
	// return Py_BuildValue("O", poList);
// }


// PyObject* wikiGetItemDropFromMonster(PyObject* poSelf, PyObject* poArgs)
// {
	// int szItemVnum{};
	// if (!PyTuple_GetInteger(poArgs, 0, &szItemVnum))
		// return Py_BadArgument();

	// bool szIsRefineItem{ false };
	// if (!PyTuple_GetBoolean(poArgs, 1, &szIsRefineItem))
		// return Py_BadArgument();

	// PyObject* poList{ PyList_New(0) };

	// const BYTE refineLevel = szIsRefineItem ? CPythonWiki::Instance().GetRefineLevel(szItemVnum, 0, 0) : 0 ;
	// const auto m_vec_ItemRange{ CPythonWiki::Instance().GetMobDrop() };

	// for (const auto& [mobVnum, mobData] : m_vec_ItemRange)
	// {
		// if (mobData.size())
		// {
			// if (szIsRefineItem)
			// {
				// for (const auto& dataItem : mobData)
				// {
					// if (szItemVnum >= dataItem.itemVnum && szItemVnum <= dataItem.itemVnum + refineLevel)
					// {
						// const auto obj = Py_BuildValue("i", mobVnum);
						// PyList_Append(poList, obj);
// #ifdef ENABLE_LEAK_FIX
						// fix_leak.push_back(obj);
// #endif

						// break;
					// }
				// }
			// }
			// else
			// {
				// for (const auto& dataItem : mobData)
				// {
					// if (szItemVnum == dataItem.itemVnum)
					// {
						// const auto obj = Py_BuildValue("i", mobVnum);
						// PyList_Append(poList, obj);
// #ifdef ENABLE_LEAK_FIX
						// fix_leak.push_back(obj);
// #endif
						// break;
					// }

				// }
			// }
		// }
	// }
// #ifdef ENABLE_LEAK_FIX
	// fix_leak.push_back(poList);
// #endif
	// return Py_BuildValue("O", poList);
// }

// PyObject* wikiGetItemInfosCube(PyObject* poSelf, PyObject* poArgs)
// {
	// int szItemVnum{};
	// if (!PyTuple_GetInteger(poArgs, 0, &szItemVnum))
		// return Py_BadArgument();

	// PyObject* poList{ PyList_New(0) };

	// const auto& m_vec_ItemRange{ CPythonWiki::Instance().GetCubeInformations() };

	// for (const auto& informations : m_vec_ItemRange)
	// {
		// sCube cubeData;
		// cubeData.vnum_reward = informations.vnum_reward;
		// cubeData.count_reward = informations.count_reward;
		// cubeData.upgradeVec = informations.upgradeVec;
		// cubeData.npcVnum = informations.npcVnum;

		// PyObject* poCubeDict = PyDict_New();

		// PyObject* poVnumReward = PyLong_FromLong(cubeData.vnum_reward);
		// PyDict_SetItemString(poCubeDict, "vnum_reward", poVnumReward);
		// Py_DECREF(poVnumReward);

		// PyObject* poCountReward = PyLong_FromLong(cubeData.count_reward);
		// PyDict_SetItemString(poCubeDict, "count_reward", poCountReward);
		// Py_DECREF(poCountReward);

		// PyObject* poUpgradeVec = PyList_New(cubeData.upgradeVec.size());

		// for (size_t i = 0; i < cubeData.upgradeVec.size(); ++i)
		// {
			// const special_data& upgradeData = cubeData.upgradeVec[i];

			// PyObject* poUpgradeData = PyDict_New();

			// PyObject* poUpgradeVnum = PyLong_FromLong(upgradeData.itemVnum);
			// PyDict_SetItemString(poUpgradeData, "upgradeVnum", poUpgradeVnum);
			// Py_DECREF(poUpgradeVnum);

			// PyObject* poUpgradeCount = PyLong_FromLong(upgradeData.count);
			// PyDict_SetItemString(poUpgradeData, "upgradeCount", poUpgradeCount);
			// Py_DECREF(poUpgradeCount);

			// PyList_SetItem(poUpgradeVec, i, poUpgradeData);
		// }
		// PyDict_SetItemString(poCubeDict, "upgradeVec", poUpgradeVec);
		// Py_DECREF(poUpgradeVec);

		// PyObject* poNpcVnum = PyLong_FromLong(cubeData.npcVnum);
		// PyDict_SetItemString(poCubeDict, "npcVnum", poNpcVnum);
		// Py_DECREF(poNpcVnum);

		// PyList_Append(poList, poCubeDict);
		// Py_DECREF(poCubeDict);
	// }

	// return Py_BuildValue("O", poList);
// }


// PyObject* wikiGetCubeData(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BuildException();

	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		// return Py_BuildException();

	// const auto& m_vecCube = CPythonWiki::Instance().m_vecCube;

	// long long cubeCost{};
	// int gemCost{};
	// unsigned char upgradeChange{};

	// if (iType == CUBE_CAT)
	// {
		// for (const auto& cubeItem : m_vecCube)
		// {
			// if (cubeItem.vnum_reward == cubeNpcVnums[iIndex][0])
			// {
				// cubeCost = cubeItem.itemCost;
				// upgradeChange = cubeItem.upgradeChange;
				// gemCost = cubeItem.gemCost;
				// break;
			// }
		// }

		// return Py_BuildValue("iiLii", cubeNpcVnums[iIndex][0], cubeNpcVnums[iIndex][1], cubeCost, gemCost, upgradeChange);

	// }

	// else if (iType == CUBE_CAT2)
	// {
		// for (const auto& cubeItem : m_vecCube)
		// {
			// if (cubeItem.vnum_reward == cubeNpcVnums2[iIndex][0])
			// {
				// cubeCost = cubeItem.itemCost;
				// upgradeChange = cubeItem.upgradeChange;
				// gemCost = cubeItem.gemCost;
				// break;
			// }
		// }

		// return Py_BuildValue("iiLii", cubeNpcVnums2[iIndex][0], cubeNpcVnums2[iIndex][1], cubeCost, gemCost, upgradeChange);

	// }

	// else if (iType == CUBE_CAT3)
	// {
		// for (const auto& cubeItem : m_vecCube)
		// {
			// if (cubeItem.vnum_reward == cubeNpcVnums3[iIndex][0])
			// {
				// cubeCost = cubeItem.itemCost;
				// upgradeChange = cubeItem.upgradeChange;
				// gemCost = cubeItem.gemCost;
				// break;
			// }
		// }

		// return Py_BuildValue("iiLii", cubeNpcVnums3[iIndex][0], cubeNpcVnums3[iIndex][1], cubeCost, gemCost, upgradeChange);

	// }
	// else if (iType == CUBE_CAT4)
	// {
		// for (const auto& cubeItem : m_vecCube)
		// {
			// if (cubeItem.vnum_reward == cubeNpcVnums4[iIndex][0])
			// {
				// cubeCost = cubeItem.itemCost;
				// upgradeChange = cubeItem.upgradeChange;
				// gemCost = cubeItem.gemCost;
				// break;
			// }
		// }

		// return Py_BuildValue("iiLii", cubeNpcVnums4[iIndex][0], cubeNpcVnums4[iIndex][1], cubeCost, gemCost, upgradeChange);

	// }
	// else if (iType == CUBE_CAT5)
	// {
		// for (const auto& cubeItem : m_vecCube)
		// {
			// if (cubeItem.vnum_reward == cubeNpcVnums5[iIndex][0])
			// {
				// cubeCost = cubeItem.itemCost;
				// upgradeChange = cubeItem.upgradeChange;
				// gemCost = cubeItem.gemCost;
				// break;
			// }
		// }

		// return Py_BuildValue("iiLii", cubeNpcVnums5[iIndex][0], cubeNpcVnums5[iIndex][1], cubeCost, gemCost, upgradeChange);

	// }
	// else if (iType == CUBE_CAT6)
	// {
		// for (const auto& cubeItem : m_vecCube)
		// {
			// if (cubeItem.vnum_reward == cubeNpcVnums6[iIndex][0])
			// {
				// cubeCost = cubeItem.itemCost;
				// upgradeChange = cubeItem.upgradeChange;
				// gemCost = cubeItem.gemCost;
				// break;
			// }
		// }

		// return Py_BuildValue("iiLii", cubeNpcVnums6[iIndex][0], cubeNpcVnums6[iIndex][1], cubeCost, gemCost, upgradeChange);

	// }
	// else if (iType == CUBE_CAT7)
	// {
		// for (const auto& cubeItem : m_vecCube)
		// {
			// if (cubeItem.vnum_reward == cubeNpcVnums7[iIndex][0])
			// {
				// cubeCost = cubeItem.itemCost;
				// upgradeChange = cubeItem.upgradeChange;
				// gemCost = cubeItem.gemCost;
				// break;
			// }
		// }

		// return Py_BuildValue("iiLii", cubeNpcVnums7[iIndex][0], cubeNpcVnums7[iIndex][1], cubeCost, gemCost, upgradeChange);

	// }
	// else if (iType == CUBE_CAT8)
	// {
		// for (const auto& cubeItem : m_vecCube)
		// {
			// if (cubeItem.vnum_reward == cubeNpcVnums8[iIndex][0])
			// {
				// cubeCost = cubeItem.itemCost;
				// upgradeChange = cubeItem.upgradeChange;
				// gemCost = cubeItem.gemCost;
				// break;
			// }
		// }

		// return Py_BuildValue("iiLii", cubeNpcVnums8[iIndex][0], cubeNpcVnums8[iIndex][1], cubeCost, gemCost, upgradeChange);

		// }
	// else if (iType == CUBE_CAT9)
	// {
		// for (const auto& cubeItem : m_vecCube)
		// {
			// if (cubeItem.vnum_reward == cubeNpcVnums9[iIndex][0])
			// {
				// cubeCost = cubeItem.itemCost;
				// upgradeChange = cubeItem.upgradeChange;
				// gemCost = cubeItem.gemCost;
				// break;
			// }
		// }

		// return Py_BuildValue("iiLii", cubeNpcVnums9[iIndex][0], cubeNpcVnums9[iIndex][1], cubeCost, gemCost, upgradeChange);

	// }

	// return Py_BuildValue("iiLii", 0, 0, 0 ,0 ,0);

// }

// PyObject* wikiGetCubeSize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iType{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iType))
		// return Py_BuildException();

	// if (iType == CUBE_CAT)
		// return Py_BuildValue("i", _countof(cubeNpcVnums));
	// else if (iType == CUBE_CAT2)
		// return Py_BuildValue("i", _countof(cubeNpcVnums2));
	// else if (iType == CUBE_CAT3)
		// return Py_BuildValue("i", _countof(cubeNpcVnums3));
	// else if (iType == CUBE_CAT4)
		// return Py_BuildValue("i", _countof(cubeNpcVnums4));
	// else if (iType == CUBE_CAT5)
		// return Py_BuildValue("i", _countof(cubeNpcVnums5));
	// else if (iType == CUBE_CAT6)
		// return Py_BuildValue("i", _countof(cubeNpcVnums6));
	// else if (iType == CUBE_CAT7)
		// return Py_BuildValue("i", _countof(cubeNpcVnums7));
	// else if (iType == CUBE_CAT8)
		// return Py_BuildValue("i", _countof(cubeNpcVnums8));
	// else if (iType == CUBE_CAT9)
		// return Py_BuildValue("i", _countof(cubeNpcVnums9));


	// return Py_BuildValue("i", 0);
// }

// PyObject* wikiGetCubeInfoSize(PyObject* poSelf, PyObject* poArgs)
// {
	// int iItemVnum{};

	// if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		// return Py_BuildException();

	// const auto& m_vecCube = CPythonWiki::Instance().m_vecCube;

	// size_t vecSize = 0;

	// for (const auto& cubeItem : m_vecCube)
	// {
		// if (cubeItem.vnum_reward == iItemVnum)
		// {
			// vecSize = cubeItem.upgradeVec.size();
			// break;
		// }
	// }

	// return Py_BuildValue("i", static_cast<int>(vecSize));
// }


// PyObject* wikiGetCubeInfoData(PyObject* poSelf, PyObject* poArgs)
// {

	// int iItemVnum{};
	// if (!PyTuple_GetInteger(poArgs, 0, &iItemVnum))
		// return Py_BuildException();

	// int iIndex{};
	// if (!PyTuple_GetInteger(poArgs, 1, &iIndex))
		// return Py_BuildException();

	// const auto& m_vecCube = CPythonWiki::Instance().m_vecCube;

	// for (const auto& cubeItem : m_vecCube)
	// {
		// if (cubeItem.vnum_reward == iItemVnum && iIndex >= 0 && iIndex < cubeItem.upgradeVec.size())
		// {
			// return Py_BuildValue("ii", cubeItem.upgradeVec[iIndex].itemVnum, cubeItem.upgradeVec[iIndex].count);
		// }
	// }

	// return Py_BuildValue("ii", 0, 0, 0);
// }

// void initWiki()
// {
	// static PyMethodDef s_methods[] =
	// {
		// { "GetRefineItems",	wikiGetRefineItems,	METH_VARARGS },
		// { "IsBlackList",	wikiIsBlackList,	METH_VARARGS },

		// { "GetCategorySize",	wikiGetCategorySize,	METH_VARARGS },
		// { "GetCategoryData",	wikiGetCategoryData,	METH_VARARGS },

		// { "GetBossSize",	wikiGetBossSize,	METH_VARARGS },
		// { "GetBossData",	wikiGetBossData,	METH_VARARGS },

		// { "GetMonsterSize",	wikiGetMonsterSize,	METH_VARARGS },
		// { "GetMonsterData",	wikiGetMonsterData,	METH_VARARGS },

		// { "GetCostumeSize",	wikiCostumeSize,	METH_VARARGS },
		// { "GetCostumeData",	wikiCostumeData,	METH_VARARGS },

		// { "GetStoneSize",	wikiGetStoneSize,	METH_VARARGS },
		// { "GetStoneData",	wikiGetStoneData,	METH_VARARGS },

		// { "GetChestSize",	wikiGetChestSize,	METH_VARARGS },
		// { "GetChestData",	wikiGetChestData,	METH_VARARGS },

		// { "GetSpecialInfoSize",	wikiGetSpecialInfoSize,	METH_VARARGS },
		// { "GetSpecialInfoData",	wikiGetSpecialInfoData,	METH_VARARGS },

		// { "GetMobInfoSize",	wikiGetMobInfoSize,	METH_VARARGS },
		// { "GetMobInfoData",	wikiGetMobInfoData,	METH_VARARGS },

		// { "GetRefineMaxLevel",	wikiGetRefineMaxLevel,	METH_VARARGS },

		// { "GetItemDropFromChest",	wikiGetItemDropFromChest,	METH_VARARGS },
		// { "GetItemDropFromMonster",	wikiGetItemDropFromMonster,	METH_VARARGS },

		// { "GetItemInfosCube",	wikiGetItemInfosCube,	METH_VARARGS },
		// { "GetCubeData",	wikiGetCubeData,	METH_VARARGS },
		// { "GetCubeSize",	wikiGetCubeSize,	METH_VARARGS },
		// { "GetCubeInfoSize",	wikiGetCubeInfoSize,	METH_VARARGS },
		// { "GetCubeInfoData",	wikiGetCubeInfoData,	METH_VARARGS },

		// { NULL, NULL, NULL },
	// };
	// PyObject* poModule = Py_InitModule("wikipedia", s_methods);
// }
// #endif*/
