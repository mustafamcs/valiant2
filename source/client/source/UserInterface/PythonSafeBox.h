#pragma once

class CPythonSafeBox : public CSingleton<CPythonSafeBox>
{
public:
	enum
	{
		SAFEBOX_SLOT_X_COUNT = 5,
		SAFEBOX_SLOT_Y_COUNT = 9,
		SAFEBOX_PAGE_SIZE = SAFEBOX_SLOT_X_COUNT * SAFEBOX_SLOT_Y_COUNT,
	};
	typedef std::vector<TItemData> TItemInstanceVector;

public:
	CPythonSafeBox();
	virtual ~CPythonSafeBox();

	void OpenSafeBox(int iSize);
	void SetItemData(DWORD dwSlotIndex, const TItemData& rItemData);
	void DelItemData(DWORD dwSlotIndex);

	void SetMoney(DWORD dwMoney);
	DWORD GetMoney();

	BOOL GetSlotItemID(DWORD dwSlotIndex, DWORD* pdwItemID);

	int GetCurrentSafeBoxSize();
	BOOL GetItemDataPtr(DWORD dwSlotIndex, TItemData** ppInstance);

	// MALL
	void OpenMall(int iSize);
	void SetMallItemData(DWORD dwSlotIndex, const TItemData& rItemData);
	void DelMallItemData(DWORD dwSlotIndex);
	BOOL GetMallItemDataPtr(DWORD dwSlotIndex, TItemData** ppInstance);
	BOOL GetSlotMallItemID(DWORD dwSlotIndex, DWORD* pdwItemID);
	DWORD GetMallSize();
#ifdef ENABLE_CHECK_IF_SAFEBOX_OPEN
	bool isOpen();
	void Close();
#endif
#ifdef ENABLE_CHECK_IF_MALL_OPEN
	bool isOpenMall();
#endif

protected:
	TItemInstanceVector m_ItemInstanceVector;
	TItemInstanceVector m_MallItemInstanceVector;
	DWORD m_dwMoney;
#ifdef ENABLE_CHECK_IF_SAFEBOX_OPEN
	bool	m_isOpenSafebox;
#endif
#ifdef ENABLE_CHECK_IF_MALL_OPEN
	bool	m_isOpenMall;
#endif
};
