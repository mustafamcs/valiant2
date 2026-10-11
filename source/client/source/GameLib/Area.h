#pragma once

#include "../SpeedTreeLib/SpeedTreeWrapper.h"
#include "../eterGrnLib/ThingInstance.h"
#include "MapType.h"
#include "DungeonBlock.h"

#ifdef ENABLE_AREA_OPTIMISATION
#define idxEffectInstance 0
#else
#define idxEffectInstance 0xffffffff
#endif

class CMapOutdoor;
class CEffectInstance;

class CArea
{
public:
	enum
	{
		ROTATION_STEP_COUNT = 24,
		ROTATION_STEP_AMOUNT = 360 / ROTATION_STEP_COUNT,
		YAW_STEP_COUNT = 24,
		YAW_STEP_AMOUNT = 360 / YAW_STEP_COUNT,
		PITCH_STEP_COUNT = YAW_STEP_COUNT,
		PITCH_STEP_AMOUNT = YAW_STEP_AMOUNT,
	};

	typedef D3DXVECTOR3 TObjectPosition;

	///////////////////////////////////////////////////////////////////////////////////
	// Object Static Data
	typedef struct SObjectData
	{
		TObjectPosition		Position;
		DWORD				dwCRC;
		BYTE				abyPortalID[PORTAL_ID_MAX_NUM];

		// For Tree
		//  - Nothing

		// For Granny Thing
		float				m_fYaw;
		float				m_fPitch;
		float				m_fRoll;
		float				m_fHeightBias;

		// For Effect
		//  - Nothing
		DWORD				dwRange;
		float				fMaxVolumeAreaPercentage;

		void InitializeRotation();
	} TObjectData;

	struct ObjectDataComp
	{
		bool operator () (TObjectData& lhs, TObjectData& rhs) const
		{
			return lhs.dwCRC < rhs.dwCRC;
		}
	};

	typedef std::vector<TObjectData>				TObjectDataVector;
	typedef TObjectDataVector::iterator				TObjectDataIterator;

	typedef struct SObjectInstance
	{
		DWORD						dwType;
		CAttributeInstance* pAttributeInstance;

		// Data For Tree
		CSpeedTreeWrapper* pTree;

		// Data For Normal Object or Building
		BOOL						isShadowFlag;
		CGraphicThingInstance* pThingInstance;

		// Data for Effect
		DWORD						dwEffectID;
		DWORD						dwEffectInstanceIndex;

		// Dungeon
		CDungeonBlock* pDungeonBlock;

		void Clear()
		{
			if (pTree)
				pTree->Clear();

			if (pThingInstance)
				pThingInstance->Clear();

			if (pAttributeInstance)
				pAttributeInstance->Clear();

			if (pDungeonBlock)
				pDungeonBlock->Clear();

			__Initialize();
		}

		void SetTree(float x, float y, float z, DWORD dwTreeCRC, const char* c_szTreeName);

		void __Initialize()
		{
			dwType = prt::PROPERTY_TYPE_NONE;

			dwEffectID = 0xffffffff;
			dwEffectInstanceIndex = idxEffectInstance;
			isShadowFlag = false;

			pTree = NULL;
			pThingInstance = NULL;
			pAttributeInstance = NULL;
			pDungeonBlock = NULL;
		}

		SObjectInstance()
		{
			__Initialize();
		}
		virtual ~SObjectInstance()
		{
		}
	} TObjectInstance;

	typedef std::vector<CSpeedTreeWrapper*>			TTreeInstanceVector;
	typedef std::vector<CGraphicThingInstance*>		TThingInstanceVector;
	typedef std::vector<CDungeonBlock*>				TDungeonBlockInstanceVector;
	typedef std::vector<TObjectInstance*>				TObjectInstanceVector;
	typedef std::map<CGraphicThingInstance*, DWORD>	TGraphicThingInstanceCRCMap;
	typedef std::set<int>								TShowingPortalIDSet;

	typedef struct SCRCWithNumber
	{
		DWORD dwCRC;
		DWORD dwNumber;
	} TCRCWithNumber;

	typedef std::vector<TCRCWithNumber> TCRCWithNumberVector;

	struct FFindIfCRC
	{
		FFindIfCRC(DWORD dwCRC) { m_dwCRC = dwCRC; }

		bool operator() (TCRCWithNumber& rCRCWithNumber)
		{
			if (rCRCWithNumber.dwCRC == m_dwCRC)
				return true;
			return false;
		}

		DWORD m_dwCRC;
	};

	struct CRCNumComp
	{
		bool operator () (TCRCWithNumber& lhs, TCRCWithNumber& rhs) const
		{
			return lhs.dwNumber > rhs.dwNumber;
		}
	};

public:
	CArea();
	virtual ~CArea();

	void			CollectRenderingObject(std::vector<CGraphicThingInstance*>& rkVct_pkOpaqueThingInst);
	void			CollectBlendRenderingObject(std::vector<CGraphicThingInstance*>& rkVct_pkBlendThingInst);

	void			SetMapOutDoor(CMapOutdoor* pOwnerOutdoorMap);
	void			Clear();

	bool			Load(const char* c_szPathName);

	DWORD			GetObjectDataCount();
	bool			GetObjectDataPointer(DWORD dwIndex, const TObjectData** ppObjectData) const;

	const DWORD		GetObjectInstanceCount() const;
	const bool		GetObjectInstancePointer(const DWORD& dwIndex, const TObjectInstance** ppObjectInstance) const;

	void			EnablePortal(BOOL bFlag = TRUE);
	void			ClearPortal();
	void			AddShowingPortalID(int iNum);
	void			RefreshPortal();

	//////////////////////////////////////////////////////////////////////////

	void			Update(
#ifdef ENABLE_AREA_OPTIMISATION
		D3DXVECTOR3& v3Player
#endif
	);
	void			Render();
	void			RenderEffect();
	void			RenderCollision();
	void			RenderDungeon();
	void			Refresh(
#ifdef ENABLE_AREA_OPTIMISATION
		TObjectInstance* pObjectInstance, bool bRemove
#endif
	);

	//////////////////////////////////////////////////////////////////////////

	void			SetCoordinate(const WORD& c_usCoordX, const WORD& c_usCoordY);
	void			GetCoordinate(WORD* usCoordX, WORD* usCoordY);

	//////////////////////////////////////////////////////////////////////////

	DWORD			DEBUG_GetRenderedCRCNum();
	TCRCWithNumberVector& DEBUG_GetRenderedCRCWithNumVector();
	DWORD			DEBUG_GetRenderedGrapphicThingInstanceNum();

	CMapOutdoor* GetOwner() { return m_pOwnerOutdoorMap; }

protected:

	bool			CheckObjectIndex(DWORD dwIndex) const;

	bool			__Load_LoadObject(const char* c_szFileName);
	void			__Load_BuildObjectInstances();

	void			__UpdateAniThingList();
	void			__UpdateEffectList();
#ifdef ENABLE_AREA_OPTIMISATION
	void			__UpdateLoadedObjectInstances(D3DXVECTOR3& v3Player);
	void			__UpdateEffectList(D3DXVECTOR3& v3Player);
	float			GetMaxLoadingDistanceSqr() const;
#endif
	void			__LoadAttribute(TObjectInstance* pObjectInstance, const char* c_szAttributeFileName);

protected:
	void			__Clear_DestroyObjectInstance(TObjectInstance* pObjectInstance);

	void			__SetObjectInstance(TObjectInstance* pObjectInstance, const TObjectData* c_pData);
	void			__SetObjectInstance_SetTree(TObjectInstance* pObjectInstance, const TObjectData* c_pData, CProperty* pProperty);
	void			__SetObjectInstance_SetBuilding(TObjectInstance* pObjectInstance, const TObjectData* c_pData, CProperty* pProperty);
	void			__SetObjectInstance_SetEffect(TObjectInstance* pObjectInstance, const TObjectData* c_pData, CProperty* pProperty);
	void			__SetObjectInstance_SetDungeonBlock(TObjectInstance* pObjectInstance, const TObjectData* c_pData, CProperty* pProperty);

protected:
	// Static Data
	TObjectDataVector				m_ObjectDataVector;

	// Rendering Instances
	TObjectInstanceVector			m_ObjectInstanceVector;

	// Clone Instance Vector
	TTreeInstanceVector				m_TreeCloneInstaceVector;
	TThingInstanceVector			m_ThingCloneInstaceVector;
	TDungeonBlockInstanceVector		m_DungeonBlockCloneInstanceVector;
	TThingInstanceVector			m_AniThingCloneInstanceVector;
	TThingInstanceVector			m_ShadowThingCloneInstaceVector;
	TGraphicThingInstanceCRCMap		m_GraphicThingInstanceCRCMap;
	TCRCWithNumberVector			m_kRenderedThingInstanceCRCWithNumberVector;
	TThingInstanceVector			m_kRenderedGrapphicThingInstanceVector;

	WORD							m_wX;
	WORD							m_wY;

	// Owner COutdoorMap poineter
	CMapOutdoor* m_pOwnerOutdoorMap;

protected:
	static CMemoryPoolNew<TObjectInstance>			ms_ObjectInstancePool;
	static CMemoryPoolNew<CAttributeInstance>			ms_AttributeInstancePool;
	static CMemoryPoolNew<CDungeonBlock>				ms_DungeonBlockInstancePool;

	typedef std::map<DWORD, CEffectInstance*>		TEffectInstanceMap;
	typedef TEffectInstanceMap::iterator			TEffectInstanceIterator;
	TEffectInstanceMap								m_EffectInstanceMap;

	BOOL											m_bPortalEnable;
	TShowingPortalIDSet								m_kSet_ShowingPortalID;

#ifdef ENABLE_AREA_OPTIMISATION
	std::vector<CEffectInstance*>					m_kVct_pkEftInstSort; // for rendering
	int32_t											m_iUpdateCount;
#endif

public:
	static void DestroySystem();

	static CArea* New();
	static void Delete(CArea* pkArea);

	static CMemoryPoolNew<CArea>		ms_kPool;
};
