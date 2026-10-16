#include "stdafx.h"
#ifdef ENABLE_NEW_CHAT
#include "NewChatManager.h"
#include "../EterFSLib/FileSystemIncl.hpp"
#include "PythonNetworkStream.h"
#include "../../../server/source/game/src/ChatTable.h"

inline void one_argument(std::string& localeString, CTokenVector& vecFormat)
{
	char tempText[1024];
	snprintf(tempText, sizeof(tempText), localeString.c_str(), vecFormat[0].c_str());
	localeString = tempText;
}

inline void two_arguments(std::string& localeString, CTokenVector& vecFormat)
{
	char tempText[1024];
	snprintf(tempText, sizeof(tempText), localeString.c_str(), vecFormat[0].c_str(), vecFormat[1].c_str());
	localeString = tempText;
}

inline void three_arguments(std::string& localeString, CTokenVector& vecFormat)
{
	char tempText[1024];
	snprintf(tempText, sizeof(tempText), localeString.c_str(), vecFormat[0].c_str(), vecFormat[1].c_str(), vecFormat[2].c_str());
	localeString = tempText;
}

inline void four_arguments(std::string& localeString, CTokenVector& vecFormat)
{
	char tempText[1024];
	snprintf(tempText, sizeof(tempText), localeString.c_str(), vecFormat[0].c_str(), vecFormat[1].c_str(), vecFormat[2].c_str(), vecFormat[3].c_str());
	localeString = tempText;
}

inline void five_arguments(std::string& localeString, CTokenVector& vecFormat)
{
	char tempText[1024];
	snprintf(tempText, sizeof(tempText), localeString.c_str(), vecFormat[0].c_str(), vecFormat[1].c_str(), vecFormat[2].c_str(), vecFormat[3].c_str(), vecFormat[4].c_str());
	localeString = tempText;
}

inline void six_arguments(std::string& localeString, CTokenVector& vecFormat)
{
	char tempText[1024];
	snprintf(tempText, sizeof(tempText), localeString.c_str(), vecFormat[0].c_str(), vecFormat[1].c_str(), vecFormat[2].c_str(), vecFormat[3].c_str(), vecFormat[4].c_str(), vecFormat[5].c_str());
	localeString = tempText;
}

inline int GetLcsIndex(const char* name)
{
	for (int i = 0; i < EChatTable::MAX_CHAT_COUNT; i++)
	{
		if (!strcmp(g_ChatTable[i], name))
			return i;
	}
	return -1;
}

CNewChatManager::CNewChatManager()
{
	Destroy();
}

CNewChatManager::~CNewChatManager()
{
	Destroy();
}

void CNewChatManager::Destroy()
{
	m_mapLocaleString.clear();
	m_isLoad = false;
}

bool CNewChatManager::LoadLocaleStringTable(const char* c_szFileName)
{
	if (IsLoaded())
		return true;

	const auto file = PackGet(c_szFileName);
	if (!file)
		return false;

	CMemoryTextFileLoader textFileLoader;
	textFileLoader.Bind(file->get_size(), file->get_data());

	CTokenVector TokenVector;
	int lineIndex = 0;

	for (DWORD i = 0; i < textFileLoader.GetLineCount() - 1; ++i)
	{
		lineIndex++;

		if (!textFileLoader.SplitLineByTab(i, &TokenVector))
		{
			TraceError("CNewChatManager::LoadLocaleStringTable: Strange Token Strucutre [Line %d]\n", lineIndex);
			continue;
		}

		if (TokenVector.size() != 2)
		{
			TraceError("CNewChatManager::LoadLocaleStringTable(%s) - Strange Token Count [Line:%d / TokenCount:%d]\n", c_szFileName, lineIndex, TokenVector.size());
			continue;
		}

		int stringIndex = GetLcsIndex(TokenVector[0].c_str());
		if (stringIndex == -1)
		{
			TraceError("CNewChatManager::LoadLocaleStringTable stringIndex error:");
			TraceError("Key: %s Value: %s", TokenVector[0].c_str(), TokenVector[1].c_str());
			continue;
		}
		std::string strLocaleString = TokenVector[1];
		strLocaleString += "\n";
		m_mapLocaleString.insert(std::make_pair(static_cast<WORD>(stringIndex), strLocaleString));
	}
	m_isLoad = true;

	return true;
}

bool CNewChatManager::IsItemGainChatID(WORD chatID) const
{
	return (chatID == EChatTable::YOU_GAINED_ITEM ||
		(chatID >= EChatTable::YOU_GAINED_ITEM_INV_TYPE_01 && chatID <= EChatTable::YOU_GAINED_ITEM_INV_TYPE_05) ||
		(chatID >= EChatTable::WINNER_ITEM_01 && chatID <= EChatTable::WINNER_ITEM_06));
}

bool CNewChatManager::FindLocaleString(WORD chatID, std::string& localeString)
{
	auto it = m_mapLocaleString.find(chatID);
	if (it == m_mapLocaleString.end())
	{
		TraceError("Locale String Find Error ID: %d",chatID);
		return false;
	}

	localeString = it->second;
	return true;
}

void CNewChatManager::WriteFormat(std::string& localeString, const char* format)
{
	
	CTokenVector vecFormat;
	BYTE endIndex = 0;
	for (int i = 0; i < strlen(format); i++)
	{
		std::string dalga = "";
		dalga += format[i];
		if (dalga == "|")
		{
			std::string tempStr = "";
			for (int y = endIndex; y < i; y++)
			{
				tempStr += format[y];
			}
			vecFormat.push_back(tempStr);
			endIndex = i + 1;
		}
	}

	std::string tempStr = "";
	for (int y = endIndex; y < strlen(format); y++)
	{
		tempStr += format[y];
	}

	vecFormat.push_back(tempStr);

	switch (vecFormat.size())
	{
		case 1: {	one_argument(localeString, vecFormat);		break;	}
		case 2: {	two_arguments(localeString, vecFormat);		break;	}
		case 3: {	three_arguments(localeString, vecFormat);	break;	}
		case 4: {	four_arguments(localeString, vecFormat);	break;	}
		case 5: {	five_arguments(localeString, vecFormat);	break;	}
		case 6: {	six_arguments(localeString, vecFormat);		break;	}
		default: {	TraceError("WriteFormat Arg Error : %d Local String %s", vecFormat.size(), localeString.c_str()); break; }
	}
	
}
#endif