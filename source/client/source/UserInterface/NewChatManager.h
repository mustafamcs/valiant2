#pragma once
#ifdef ENABLE_NEW_CHAT
extern inline void one_argument(std::string& localeString, CTokenVector& vecFormat);
extern inline void two_arguments(std::string& localeString, CTokenVector& vecFormat);
extern inline void three_arguments(std::string& localeString, CTokenVector& vecFormat);
extern inline void four_arguments(std::string& localeString, CTokenVector& vecFormat);
extern inline void five_arguments(std::string& localeString, CTokenVector& vecFormat);
extern inline void six_arguments(std::string& localeString, CTokenVector& vecFormat);
extern inline int GetLcsIndex();


class CNewChatManager : public singleton<CNewChatManager>
{
public:
	CNewChatManager();
	virtual ~CNewChatManager();
	void Destroy();

	bool FindLocaleString(WORD chatID, std::string& localeString);
	bool LoadLocaleStringTable(const char* c_szFileName);
	bool IsLoaded() { return m_isLoad; }

	void WriteFormat(std::string& localeString, const char* format);

private:
	std::unordered_map<WORD, std::string> m_mapLocaleString;
	bool m_isLoad;
};


#endif
