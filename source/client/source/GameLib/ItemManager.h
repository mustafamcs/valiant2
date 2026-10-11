#pragma once

#include "ItemData.h"

class CItemManager : public CSingleton<CItemManager>
{
public:
	enum EItemDescCol
	{
		ITEMDESC_COL_VNUM,
		ITEMDESC_COL_NAME,
		ITEMDESC_COL_DESC,
		ITEMDESC_COL_SUMM,
#ifdef ENABLE_COLORFUL_DESCRIPTIONS
		ITEMDESC_COL_RED,
		ITEMDESC_COL_BLUE,
		ITEMDESC_COL_GREEN,
		ITEMDESC_COL_YELLOW,
		ITEMDESC_COL_ORANGE,
		ITEMDESC_COL_PINK,
		ITEMDESC_COL_PURPLE,
#endif
		ITEMDESC_COL_NUM,
	};

#ifdef ENABLE_GLOBAL_SCALE
	enum EItemScaleCol
	{
		ITEM_SCALE_COL_VNUM,
		ITEM_SCALE_COL_JOB,
		ITEM_SCALE_COL_SEX,
		ITEM_SCALE_COL_MESH_SCALE_X,
		ITEM_SCALE_COL_MESH_SCALE_Y,
		ITEM_SCALE_COL_MESH_SCALE_Z,
		ITEM_SCALE_COL_PARTICLE_SCALE,
		ITEM_SCALE_COL_NUM
	};
#endif

public:
	typedef std::map<DWORD, CItemData*> TItemMap;
	typedef std::map<std::string, CItemData*> TItemNameMap;

#ifdef ENABLE_OFFLINE_SHOP
public:
	std::tuple<const char*, int> SelectByNamePart(const char* namePart);
#endif

public:
	CItemManager();
	virtual ~CItemManager();

	void			Destroy();

	BOOL			SelectItemData(DWORD dwIndex);
	CItemData* GetSelectedItemDataPointer();
#ifdef ENABLE_OFFLINE_SHOP
	void			GetItemsNameMap(std::map<DWORD, std::string>& inMap);
	TItemMap		GetItems() const { return m_ItemMap; }
#endif
	BOOL			GetItemDataPointer(DWORD dwItemID, CItemData** ppItemData);

	/////
	bool			LoadItemDesc(const char* c_szFileName);
	bool			LoadItemList(const char* c_szFileName);
	bool			LoadItemTable(const char* c_szFileName);
	CItemData* MakeItemData(DWORD dwIndex);

#ifdef ENABLE_GLOBAL_SCALE
	bool LoadItemScale(const char* szItemScale);
#endif

#ifdef ENABLE_SHINING_SYSTEM
	bool			LoadShiningTable(const char* c_szFileName);
#endif

protected:
	TItemMap m_ItemMap;
	std::vector<CItemData*>  m_vec_ItemRange;
	CItemData* m_pSelectedItemData;
};
