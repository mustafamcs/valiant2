#pragma once

#include "../eterBase/Singleton.h"

class CPythonTextTail : public CSingleton<CPythonTextTail>
{
public:
	typedef struct STextTail
	{
		CGraphicTextInstance* pTextInstance;
		CGraphicTextInstance* pOwnerTextInstance;

		CGraphicMarkInstance* pMarkInstance;
		CGraphicTextInstance* pGuildNameTextInstance;

		CGraphicTextInstance* pTitleTextInstance;
		CGraphicTextInstance* pLevelTextInstance;
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
		CGraphicImageInstance* pLanguageInstance;
#endif


		CGraphicObjectInstance* pOwner;

		DWORD							dwVirtualID;

		float							x, y, z;
		float							fDistanceFromPlayer;
		D3DXCOLOR						Color;
		BOOL							bNameFlag;

		float							xStart, yStart;
		float							xEnd, yEnd;

		DWORD							LivingTime;

		float							fHeight;

#ifdef ENABLE_OFFLINE_SHOP
#ifdef ENABLE_SHOP_IN_CITIES
		bool							bIsShop;
		bool							bRender;
#endif
#endif

		STextTail() {}
		virtual ~STextTail() {}
	} TTextTail;

	typedef std::map<DWORD, TTextTail*>		TTextTailMap;
	typedef std::list<TTextTail*>			TTextTailList;
	typedef TTextTailMap					TChatTailMap;

public:
	CPythonTextTail(void);
	virtual ~CPythonTextTail(void);

	void GetInfo(std::string* pstInfo);

	void Initialize();
	void Destroy();
	void Clear();
#ifdef ENABLE_SHOP_IN_CITIES
	void RegisterShopInstanceTextTail(DWORD dwVirtualID, const char* c_szName, CGraphicObjectInstance* pOwner);
	void DeleteShopTextTail(DWORD VirtualID);
	TTextTail* RegisterShopTextTail(DWORD dwVirtualID, const char* c_szText, CGraphicObjectInstance* pOwner);
	bool GetPickedNewShop(DWORD* pdwVID);
#endif
	void UpdateAllTextTail();
	void UpdateShowingTextTail();
	void Render();

	void ArrangeTextTail();
	void HideAllTextTail();
	void ShowAllTextTail();
	void ShowCharacterTextTail(DWORD VirtualID);
	void ShowItemTextTail(DWORD VirtualID);

	void RegisterCharacterTextTail(DWORD dwGuildID, DWORD dwVirtualID, const D3DXCOLOR& c_rColor, float fAddHeight = 10.0f);
	void RegisterItemTextTail(DWORD VirtualID, const char* c_szText, CGraphicObjectInstance* pOwner
#ifdef ENABLE_EXTENDED_ITEMNAME_ON_GROUND
		, bool bHasAttr = false
#endif
	);
	void RegisterChatTail(DWORD VirtualID, const char* c_szChat);
	void RegisterInfoTail(DWORD VirtualID, const char* c_szChat);
	void SetCharacterTextTailColor(DWORD VirtualID, const D3DXCOLOR& c_rColor);
	void SetItemTextTailOwner(DWORD dwVID, const char* c_szName);
	void DeleteCharacterTextTail(DWORD VirtualID);
	void DeleteItemTextTail(DWORD VirtualID);

	int Pick(int ixMouse, int iyMouse);
	void SelectItemName(DWORD dwVirtualID);

	bool GetTextTailPosition(DWORD dwVID, float* px, float* py, float* pz);
	bool IsChatTextTail(DWORD dwVID);

	void EnablePKTitle(BOOL bFlag);
	void AttachTitle(DWORD dwVID, const char* c_szName, const D3DXCOLOR& c_rColor);
	void DetachTitle(DWORD dwVID);
	
	void AttachLevel(DWORD dwVID, const char* c_szText, const D3DXCOLOR& c_rColor);
	void DetachLevel(DWORD dwVID);
#ifdef ENABLE_METIN_SCALE
	void TextTailHeightRefresh();
#endif
protected:
	TTextTail* RegisterTextTail(DWORD dwVirtualID, const char* c_szText, CGraphicObjectInstance* pOwner, float fHeight, const D3DXCOLOR& c_rColor);
	void DeleteTextTail(TTextTail* pTextTail);

	void UpdateTextTail(TTextTail* pTextTail);
	void RenderTextTailBox(TTextTail* pTextTail);
	void RenderTextTailName(TTextTail* pTextTail);
	void UpdateDistance(const TPixelPosition& c_rCenterPosition, TTextTail* pTextTail);

	bool isIn(TTextTail* pSource, TTextTail* pTarget);

protected:
	TTextTailMap				m_CharacterTextTailMap;
	TTextTailMap				m_ItemTextTailMap;
	TChatTailMap				m_ChatTailMap;

	TTextTailList				m_CharacterTextTailList;
	TTextTailList				m_ItemTextTailList;
#ifdef ENABLE_SHOP_IN_CITIES
	TTextTailMap				m_ShopTextTailMap;
#endif

private:
	CMemoryPoolNew<STextTail>		m_TextTailPool;
};
