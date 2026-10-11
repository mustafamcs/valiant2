#include "StdAfx.h"
#include "../EterFSLib/FileSystemIncl.hpp"
#include "../eterLib/ResourceManager.h"

#include "ItemManager.h"

static DWORD s_adwItemProtoKey[4] =
{
	173217,
	72619434,
	408587239,
	27973291
};

BOOL CItemManager::SelectItemData(DWORD dwIndex)
{
	TItemMap::iterator f = m_ItemMap.find(dwIndex);

	if (m_ItemMap.end() == f)
	{
		int n = m_vec_ItemRange.size();
		for (int i = 0; i < n; i++)
		{
			CItemData* p = m_vec_ItemRange[i];
			const CItemData::TItemTable* pTable = p->GetTable();
			if ((pTable->dwVnum < dwIndex) &&
				dwIndex < (pTable->dwVnum + pTable->dwVnumRange))
			{
				m_pSelectedItemData = p;
				return TRUE;
			}
		}
		Tracef(" CItemManager::SelectItemData - FIND ERROR [%d]\n", dwIndex);
		return FALSE;
	}

	m_pSelectedItemData = f->second;

	return TRUE;
}

#ifdef ENABLE_OFFLINE_SHOP
void CItemManager::GetItemsNameMap(std::map<DWORD, std::string>& inMap)
{
	inMap.clear();
	for (auto& it : m_ItemMap)
	{
		inMap.insert(std::make_pair(it.first, it.second->GetName()));
	}
}
#endif

CItemData* CItemManager::GetSelectedItemDataPointer()
{
	return m_pSelectedItemData;
}

BOOL CItemManager::GetItemDataPointer(DWORD dwItemID, CItemData** ppItemData)
{
	if (0 == dwItemID)
		return FALSE;

	TItemMap::iterator f = m_ItemMap.find(dwItemID);

	if (m_ItemMap.end() == f)
	{
		int n = m_vec_ItemRange.size();
		for (int i = 0; i < n; i++)
		{
			CItemData* p = m_vec_ItemRange[i];
			const CItemData::TItemTable* pTable = p->GetTable();
			if ((pTable->dwVnum < dwItemID) &&
				dwItemID < (pTable->dwVnum + pTable->dwVnumRange))
			{
				*ppItemData = p;
				return TRUE;
			}
		}
		Tracef(" CItemManager::GetItemDataPointer - FIND ERROR [%d]\n", dwItemID);
		return FALSE;
	}

	*ppItemData = f->second;

	return TRUE;
}

CItemData* CItemManager::MakeItemData(DWORD dwIndex)
{
	TItemMap::iterator f = m_ItemMap.find(dwIndex);

	if (m_ItemMap.end() == f)
	{
		CItemData* pItemData = CItemData::New();

		m_ItemMap.insert(TItemMap::value_type(dwIndex, pItemData));

		return pItemData;
	}

	return f->second;
}

////////////////////////////////////////////////////////////////////////////////////////
// Load Item Table

bool CItemManager::LoadItemList(const char* c_szFileName)
{
	auto file = PackGet(c_szFileName);
	if (!file)
		return false;

	CMemoryTextFileLoader textFileLoader;
	textFileLoader.Bind(file->get_size(), file->get_data());

	CTokenVector TokenVector;
	for (DWORD i = 0; i < textFileLoader.GetLineCount(); ++i)
	{
		if (!textFileLoader.SplitLine(i, &TokenVector, "\t"))
			continue;

		if (!(TokenVector.size() == 3 || TokenVector.size() == 4))
		{
			TraceError(" CItemManager::LoadItemList(%s) - StrangeLine in %d\n", c_szFileName, i);
			continue;
		}

		const std::string& c_rstrID = TokenVector[0];
		const std::string& c_rstrType = TokenVector[1];
		const std::string& c_rstrIcon = TokenVector[2];

		DWORD dwItemVNum = atoi(c_rstrID.c_str());

		CItemData* pItemData = MakeItemData(dwItemVNum);

		if (4 == TokenVector.size())
		{
#ifdef ENABLE_AURA_SYSTEM
			if (!strcmp(c_rstrType.c_str(), "AURA"))
			{
				const std::string& c_rstrAuraEffectFileName = TokenVector[3];
				pItemData->SetAuraEffectID(c_rstrAuraEffectFileName.c_str());
				pItemData->SetDefaultItemData(c_rstrIcon.c_str());
			}
			else
			{
				const std::string& c_rstrModelFileName = TokenVector[3];
				pItemData->SetDefaultItemData(c_rstrIcon.c_str(), c_rstrModelFileName.c_str());
			}
#else
			const std::string& c_rstrModelFileName = TokenVector[3];
			pItemData->SetDefaultItemData(c_rstrIcon.c_str(), c_rstrModelFileName.c_str());
#endif
		}
		else
		{
			pItemData->SetDefaultItemData(c_rstrIcon.c_str());
		}
	}

	return true;
}

const std::string& __SnapString(const std::string& c_rstSrc, std::string& rstTemp)
{
	UINT uSrcLen = c_rstSrc.length();
	if (uSrcLen < 2)
		return c_rstSrc;

	if (c_rstSrc[0] != '"')
		return c_rstSrc;

	UINT uLeftCut = 1;

	UINT uRightCut = uSrcLen;
	if (c_rstSrc[uSrcLen - 1] == '"')
		uRightCut = uSrcLen - 1;

	rstTemp = c_rstSrc.substr(uLeftCut, uRightCut - uLeftCut);
	return rstTemp;
}

bool CItemManager::LoadItemDesc(const char* c_szFileName)
{
	const auto file = PackGet(c_szFileName);
	if (!file)
	{
		Tracenf("CItemManager::LoadItemDesc(c_szFileName=%s) - Load Error", c_szFileName);
		return false;
	}

	CMemoryTextFileLoader kTextFileLoader;
	kTextFileLoader.Bind(file->get_size(), file->get_data());

	std::string stTemp;

	CTokenVector kTokenVector;
	for (DWORD i = 0; i < kTextFileLoader.GetLineCount(); ++i)
	{
		if (!kTextFileLoader.SplitLineByTab(i, &kTokenVector))
			continue;

		while (kTokenVector.size() < ITEMDESC_COL_NUM)
			kTokenVector.push_back("");

		//assert(kTokenVector.size()==ITEMDESC_COL_NUM);

		DWORD dwVnum = atoi(kTokenVector[ITEMDESC_COL_VNUM].c_str());
		const std::string& c_rstDesc = kTokenVector[ITEMDESC_COL_DESC];
		const std::string& c_rstSumm = kTokenVector[ITEMDESC_COL_SUMM];
#ifdef ENABLE_COLORFUL_DESCRIPTIONS
		const std::string& c_rstRed=kTokenVector[ITEMDESC_COL_RED];
		const std::string& c_rstBlue=kTokenVector[ITEMDESC_COL_BLUE];
		const std::string& c_rstGreen=kTokenVector[ITEMDESC_COL_GREEN];
		const std::string& c_rstYellow=kTokenVector[ITEMDESC_COL_YELLOW];
		const std::string& c_rstOrange=kTokenVector[ITEMDESC_COL_ORANGE];
		const std::string& c_rstPink=kTokenVector[ITEMDESC_COL_PINK];
		const std::string& c_rstPurple=kTokenVector[ITEMDESC_COL_PURPLE];
#endif
		TItemMap::iterator f = m_ItemMap.find(dwVnum);
		if (m_ItemMap.end() == f)
			continue;

		CItemData* pkItemDataFind = f->second;

		pkItemDataFind->SetDescription(__SnapString(c_rstDesc, stTemp));
		pkItemDataFind->SetSummary(__SnapString(c_rstSumm, stTemp));
#ifdef ENABLE_COLORFUL_DESCRIPTIONS
		pkItemDataFind->SetRed(__SnapString(c_rstRed, stTemp));
		pkItemDataFind->SetBlue(__SnapString(c_rstBlue, stTemp));
		pkItemDataFind->SetGreen(__SnapString(c_rstGreen, stTemp));
		pkItemDataFind->SetYellow(__SnapString(c_rstYellow, stTemp));
		pkItemDataFind->SetOrange(__SnapString(c_rstOrange, stTemp));
		pkItemDataFind->SetPink(__SnapString(c_rstPink, stTemp));
		pkItemDataFind->SetPurple(__SnapString(c_rstPurple, stTemp));
#endif
	}
	return true;
}

DWORD GetHashCode(const char* pString)
{
	unsigned long i, len;
	unsigned long ch;
	unsigned long result;

	len = strlen(pString);
	result = 5381;
	for (i = 0; i < len; i++)
	{
		ch = (unsigned long)pString[i];
		result = ((result << 5) + result) + ch; // hash * 33 + ch
	}

	return result;
}

bool CItemManager::LoadItemTable(const char* c_szFileName)
{
	const auto file = PackGet(c_szFileName);
	if (!file)
		return false;

	DWORD dwFourCC, dwElements, dwDataSize;
	DWORD dwVersion = 0;
	DWORD dwStride = 0;

	CMappedFile mappedFile;
	mappedFile.AppendDataBlock(file->get_data(), file->get_size());

	mappedFile.Read(&dwFourCC, sizeof(DWORD));

	if (dwFourCC == MAKEFOURCC('M', 'I', 'P', 'X'))
	{
		mappedFile.Read(&dwVersion, sizeof(DWORD));
		mappedFile.Read(&dwStride, sizeof(DWORD));

		if (dwVersion != 1)
		{
			TraceError("CPythonItem::LoadItemTable: invalid item_proto[%s] VERSION[%d]", c_szFileName, dwVersion);
			return false;
		}

#ifdef ENABLE_PROTOSTRUCT_AUTODETECT
		if (!CItemData::TItemTableAll::IsValidStruct(dwStride))
#else
		if (dwStride != sizeof(CItemData::TItemTable))
#endif
		{
			TraceError("CPythonItem::LoadItemTable: invalid item_proto[%s] STRIDE[%d] != sizeof(SItemTable)",
				c_szFileName, dwStride, sizeof(CItemData::TItemTable));
			return false;
		}
	}
	else if (dwFourCC != MAKEFOURCC('M', 'I', 'P', 'T'))
	{
		TraceError("CPythonItem::LoadItemTable: invalid item proto type %s", c_szFileName);
		return false;
	}

	mappedFile.Read(&dwElements, sizeof(DWORD));
	mappedFile.Read(&dwDataSize, sizeof(DWORD));

	BYTE * pbData = new BYTE[dwDataSize];
	mappedFile.Read(pbData, dwDataSize);

	/////

	CLZObject zObj;

	if (!CLZO::Instance().Decompress(zObj, pbData, s_adwItemProtoKey))
	{
		delete[] pbData;
		return false;
	}

	/////

	char szName[64 + 1];
	std::map<DWORD, DWORD> itemNameMap;

	for (DWORD i = 0; i < dwElements; ++i)
	{
#ifdef ENABLE_PROTOSTRUCT_AUTODETECT
		CItemData::TItemTable t = { 0 };
		CItemData::TItemTableAll::Process(zObj.GetBuffer(), dwStride, i, t);
#else
		CItemData::TItemTable& t = *((CItemData::TItemTable*)zObj.GetBuffer() + i);
#endif
		CItemData::TItemTable* table = &t;

		CItemData* pItemData;
		DWORD dwVnum = table->dwVnum;

		TItemMap::iterator f = m_ItemMap.find(dwVnum);
		if (m_ItemMap.end() == f)
		{
			_snprintf(szName, sizeof(szName), "icon/item/%05d.tga", dwVnum);

			if (CResourceManager::Instance().IsFileExist(szName) == false)
			{

				std::map<DWORD, DWORD>::iterator itVnum = itemNameMap.find(GetHashCode(table->szName));

				if (itVnum != itemNameMap.end())
					_snprintf(szName, sizeof(szName), "icon/item/%05d.tga", itVnum->second);
				else
					_snprintf(szName, sizeof(szName), "icon/item/%05d.tga", dwVnum - dwVnum % 10);

				if (CResourceManager::Instance().IsFileExist(szName) == false)
				{
#ifdef _DEBUG
					TraceError("%16s(#%-5d) cannot find icon file. setting to default.", table->szName, dwVnum);
#endif
					const DWORD EmptyBowl = 27995;
					_snprintf(szName, sizeof(szName), "icon/item/%05d.tga", EmptyBowl);
				}
			}

			pItemData = CItemData::New();

			pItemData->SetDefaultItemData(szName);
			m_ItemMap.insert(TItemMap::value_type(dwVnum, pItemData));
		}
		else
		{
			pItemData = f->second;
		}
		if (itemNameMap.find(GetHashCode(table->szName)) == itemNameMap.end())
			itemNameMap.insert(std::map<DWORD, DWORD>::value_type(GetHashCode(table->szName), table->dwVnum));
		pItemData->SetItemTableData(table);

		if (0 != table->dwVnumRange)
		{
			m_vec_ItemRange.push_back(pItemData);
		}
	}

	delete[] pbData;
	return true;
}


#ifdef ENABLE_SHINING_SYSTEM
bool CItemManager::LoadShiningTable(const char* szShiningTable)
{
	const auto file = PackGet(szShiningTable);
	if (!file)
		return false;

	CMemoryTextFileLoader textFileLoader;
	textFileLoader.Bind(file->get_size(), file->get_data());

	CTokenVector TokenVector;
	for (DWORD i = 0; i < textFileLoader.GetLineCount(); ++i)
	{
		if (!textFileLoader.SplitLine(i, &TokenVector, "\t"))
			continue;
		if (TokenVector.size() > (1 + CItemData::ITEM_SHINING_MAX_COUNT))
		{
			TraceError("CItemManager::LoadShiningTable(%s) - LoadShiningTable in %d\n - RowSize: %d MaxRowSize: %d", szShiningTable, i, TokenVector.size(), CItemData::ITEM_SHINING_MAX_COUNT);
		}
		const std::string & c_rstrID = TokenVector[0];
		int pos = c_rstrID.find("~");
		if (std::string::npos == pos)
		{
			DWORD dwItemVNum = atoi(c_rstrID.c_str());
			CItemData * pItemData = MakeItemData(dwItemVNum);
			if (pItemData)
			{
				for (BYTE i = 0; i < CItemData::ITEM_SHINING_MAX_COUNT; i++)
				{
					if (i < (TokenVector.size() - 1))
					{
						const std::string & c_rstrEffectPath = TokenVector[i + 1];
						pItemData->SetItemShiningTableData(i, c_rstrEffectPath.c_str());
					}
					else
					{
						pItemData->SetItemShiningTableData(i, "");
					}
				}
			}
		}
		else
		{
			std::string s_start_vnum(c_rstrID.substr(0, pos));
			std::string s_end_vnum(c_rstrID.substr(pos + 1));
			int start_vnum = atoi(s_start_vnum.c_str());
			int end_vnum = atoi(s_end_vnum.c_str());
			DWORD vnum = start_vnum;
			while (vnum <= end_vnum)
			{
				CItemData * pItemData = MakeItemData(vnum);
				if (pItemData)
				{
					for (BYTE i = 0; i < CItemData::ITEM_SHINING_MAX_COUNT; i++)
					{
						if (i < (TokenVector.size() - 1))
						{
							const std::string & c_rstrEffectPath = TokenVector[i + 1];
							pItemData->SetItemShiningTableData(i, c_rstrEffectPath.c_str());
						}
						else
						{
							pItemData->SetItemShiningTableData(i, "");
						}
					}
				}
				++vnum;
			}
		}
	}
	return true;
}
#endif

void CItemManager::Destroy()
{
	for (auto i = m_ItemMap.begin(); i != m_ItemMap.end(); ++i)
		CItemData::Delete(i->second);

	m_ItemMap.clear();
}

#ifdef ENABLE_GLOBAL_SCALE
bool CItemManager::LoadItemScale(const char* szItemScale)
{
	const auto file = PackGet(szItemScale);
	if (!file)
		return false;

	CMemoryTextFileLoader textFileLoader;
	textFileLoader.Bind(file->get_size(), file->get_data());

	CTokenVector TokenVector;
	for (uint32_t i = 0; i < textFileLoader.GetLineCount(); ++i)
	{
		if (!textFileLoader.SplitLine(i, &TokenVector, "\t"))
			continue;

		if (!(TokenVector.size() == 6 || TokenVector.size() == 7))
		{
			TraceError(" CItemManager::LoadItemScale(%s) - Error on line %d\n", szItemScale, i);
			continue;
		}

		const std::string& c_rstrID = TokenVector[ITEM_SCALE_COL_VNUM];
		const std::string& c_rstrJob = TokenVector[ITEM_SCALE_COL_JOB];
		const std::string& c_rstrSex = TokenVector[ITEM_SCALE_COL_SEX];
		const std::string& c_rstrMeshScaleX = TokenVector[ITEM_SCALE_COL_MESH_SCALE_X];
		const std::string& c_rstrMeshScaleY = TokenVector[ITEM_SCALE_COL_MESH_SCALE_Y];
		const std::string& c_rstrMeshScaleZ = TokenVector[ITEM_SCALE_COL_MESH_SCALE_Z];

		uint32_t dwItemVnum = atoi(c_rstrID.c_str());
		uint8_t byJob = 0;
		if (!strcmp(c_rstrJob.c_str(), "JOB_WARRIOR"))
			byJob = NRaceData::JOB_WARRIOR;
		if (!strcmp(c_rstrJob.c_str(), "JOB_ASSASSIN"))
			byJob = NRaceData::JOB_ASSASSIN;
		if (!strcmp(c_rstrJob.c_str(), "JOB_SURA"))
			byJob = NRaceData::JOB_SURA;
		if (!strcmp(c_rstrJob.c_str(), "JOB_SHAMAN"))
			byJob = NRaceData::JOB_SHAMAN;
#ifdef ENABLE_WOLFMAN_CHARACTER
		if (!strcmp(c_rstrJob.c_str(), "JOB_WOLFMAN"))
			byJob = NRaceData::JOB_WOLFMAN;
#endif
		uint8_t bySex = c_rstrSex[0] == 'M';

		float fMeshScaleX = atof(c_rstrMeshScaleX.c_str()) * 0.01f;
		float fMeshScaleY = atof(c_rstrMeshScaleY.c_str()) * 0.01f;
		float fMeshScaleZ = atof(c_rstrMeshScaleZ.c_str()) * 0.01f;

		float fParticleScale = 1.0f;
		if (TokenVector.size() == 7)
		{
			const std::string& c_rstrParticleScale = TokenVector[ITEM_SCALE_COL_PARTICLE_SCALE];
			fParticleScale = atof(c_rstrParticleScale.c_str());
		}

		CItemData* pItemData = MakeItemData(dwItemVnum);
		uint8_t bGradeMax = 5;
#ifdef ENABLE_AURA_SYSTEM
		if (pItemData->GetType() == CItemData::ITEM_TYPE_COSTUME && pItemData->GetSubType() == CItemData::COSTUME_AURA)
			bGradeMax = 6;
#endif

		for (uint8_t i = 0; i < bGradeMax; ++i)
		{
			pItemData = MakeItemData(dwItemVnum + i);
			if (pItemData)
				pItemData->SetItemTableScaleData(byJob, bySex, fMeshScaleX, fMeshScaleY, fMeshScaleZ, fParticleScale);
		}
	}

	return true;
}
#endif

#if defined(ENABLE_OFFLINE_SHOP) || defined(ENABLE_INGAME_WIKI)
std::tuple<const char*, int> CItemManager::SelectByNamePart(const char* namePart)
{
	char searchName[CItemData::ITEM_NAME_MAX_LEN + 1];
	memcpy(searchName, namePart, sizeof(searchName));
	for (size_t j = 0; j < sizeof(searchName); j++)
	{
		searchName[j] = static_cast<char>(tolower(searchName[j]));
	}

	std::string tempSearchName = searchName;

	for (TItemMap::iterator i = m_ItemMap.begin(); i != m_ItemMap.end(); i++)
	{
		const CItemData::TItemTable* tbl = i->second->GetTable();

		CItemData* itemData = nullptr;
		if (!GetItemDataPointer(i->first, &itemData))
			continue;

		std::string tempName = itemData->GetName();
		if (!tempName.size())
			continue;

		std::transform(tempName.begin(), tempName.end(), tempName.begin(), ::tolower);

		const size_t tempSearchNameLenght = tempSearchName.length();
		if (tempName.length() < tempSearchNameLenght)
			continue;

		if (!tempName.substr(0, tempSearchNameLenght).compare(tempSearchName))
			return std::make_tuple(itemData->GetName(), i->first);
	}

	return std::make_tuple("", -1);
}
#endif


CItemManager::CItemManager() : m_pSelectedItemData(NULL)
{
}
CItemManager::~CItemManager()
{
	Destroy();
}