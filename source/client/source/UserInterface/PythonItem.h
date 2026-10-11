#pragma once

#include "../EterGrnLib/ThingInstance.h"
#ifdef ENABLE_DS_SET_BONUS
#include "Packet.h"
#endif

class CItemData;

class CPythonItem : public CSingleton<CPythonItem>
{
public:
	enum
	{
		INVALID_ID = 0xffffffff,
	};

	enum
	{
		VNUM_MONEY = 1,
	};

	typedef struct SGroundItemInstance
	{
		DWORD					dwVirtualNumber;
		D3DXVECTOR3				v3EndPosition;

		D3DXVECTOR3				v3RotationAxis;
		D3DXQUATERNION			qEnd;
		D3DXVECTOR3				v3Center;
		CGraphicThingInstance	ThingInstance;
		DWORD					dwStartTime;
		DWORD					dwEndTime;

		bool					bAnimEnded;
		bool Update();
		void Clear();

		DWORD					dwEffectInstanceIndex;
		std::string				stOwnership;
		SGroundItemInstance() {}
		virtual ~SGroundItemInstance() {}
	} TGroundItemInstance;

	typedef std::map<DWORD, TGroundItemInstance*>	TGroundItemInstanceMap;

#ifdef ENABLE_DS_SET_BONUS
	typedef struct SDSTable
	{
		float	fWeight;
		int		iApplyCount;
		int		iBasicApplyValue[255];
		int		iAditionalApplyValue[255];
	} TDSTable;

	typedef std::map<int, TDSTable>	TDSTableMap;
#endif

public:
	CPythonItem(void);
	virtual ~CPythonItem(void);

	// Initialize
	void	Destroy();
	void	Create();
	void	GetInfo(std::string* pstInfo);

	void	DeleteAllItems();

	void	Render();
	void	Update(const POINT& c_rkPtMouse);

#ifdef ENABLE_EXTENDED_ITEMNAME_ON_GROUND
	void	CreateItem(DWORD dwVirtualID, DWORD dwVirtualNumber, float x, float y, float z, bool bDrop = true, long alSockets[ITEM_SOCKET_SLOT_MAX_NUM] = {}, TPlayerItemAttribute aAttrs[ITEM_ATTRIBUTE_SLOT_MAX_NUM] = {});
#else
	void	CreateItem(DWORD dwVirtualID, DWORD dwVirtualNumber, float x, float y, float z, bool bDrop = true);
#endif
	void	DeleteItem(DWORD dwVirtualID);
	void	SetOwnership(DWORD dwVID, const char* c_pszName);
	bool	GetOwnership(DWORD dwVID, const char** c_pszName);

	BOOL	GetGroundItemPosition(DWORD dwVirtualID, TPixelPosition* pPosition);

	bool	GetPickedItemID(DWORD* pdwPickedItemID);

	bool	GetCloseItem(const TPixelPosition& c_rPixelPosition, DWORD* pdwItemID, DWORD dwDistance = 300);
	bool	GetCloseMoney(const TPixelPosition& c_rPixelPosition, DWORD* dwItemID, DWORD dwDistance = 300);
#ifdef ENABLE_QUICK_PICKUP
	bool	GetAllCloseItems(const std::string& myName, const TPixelPosition& c_rPixelPosition, std::vector<DWORD>& itemVidList);
#endif

	DWORD	GetVirtualNumberOfGroundItem(DWORD dwVID);

	void	BuildNoGradeNameData(int iType);
	DWORD	GetNoGradeNameDataCount();
	CItemData* GetNoGradeNameDataPtr(DWORD dwIndex);

protected:
	DWORD	__Pick(const POINT& c_rkPtMouse);
protected:
	TGroundItemInstanceMap				m_GroundItemInstanceMap;
	CMemoryPoolNew<TGroundItemInstance>	m_GroundItemInstancePool;

	DWORD m_dwDropItemEffectID;
	DWORD m_dwPickedItemID;

	int m_nMouseX;
	int m_nMouseY;
	std::vector<CItemData*> m_NoGradeNameItemData;

#ifdef ENABLE_DS_SET_BONUS
	TDSTableMap	m_DSTableMap;
public:
	bool	SetDSTable(TPacketDSTable p);
	float	GetDSSetWeight(int iDSType, int iDSGrade);
	int		GetDSBasicApplyCount(int iDSType, int iDSGrade);
	int		GetDSBasicApplyValue(int iDSType, int iDSApplyType);
	int		GetDSAdditionalApplyValue(int iDSType, int iDSApplyType);
#endif
};
