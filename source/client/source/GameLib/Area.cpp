#include "StdAfx.h"

#ifdef ENABLE_HEAVY_EFFECT_FIX
#include "../UserInterface/StdAfx.h"
#include "../UserInterface/PythonCharacterManager.h"
#include "../UserInterface/PythonBackground.h"
#include "../UserInterface/PythonApplication.h"
#endif

#include "../eterLib/ResourceManager.h"
#include "../eterLib/StateManager.h"
#include "../effectLib/EffectManager.h"
#include "../SpeedTreeLib/SpeedTreeForestDirectX8.h"
#include "../eterBase/Timer.h"

#include "Area.h"
#include "PropertyManager.h"
#include "Property.h"

CMemoryPoolNew<CArea::TObjectInstance>	CArea::ms_ObjectInstancePool;
CMemoryPoolNew<CAttributeInstance>		CArea::ms_AttributeInstancePool;
CMemoryPoolNew<CDungeonBlock>				CArea::ms_DungeonBlockInstancePool;
CMemoryPoolNew<CArea>						CArea::ms_kPool;

void CArea::TObjectData::InitializeRotation()
{
	m_fYaw = m_fPitch = m_fRoll = 0.0f;
}

CArea* CArea::New()
{
	return ms_kPool.Alloc();
}

void CArea::Delete(CArea* pkArea)
{
	pkArea->Clear();
	ms_kPool.Free(pkArea);
}

void CArea::DestroySystem()
{
	ms_kPool.Destroy();

	ms_ObjectInstancePool.Destroy();
	ms_AttributeInstancePool.Destroy();
	ms_DungeonBlockInstancePool.Destroy();
}

void CArea::__UpdateAniThingList()
{
	for (const auto& pkThingInst : m_ThingCloneInstaceVector)
	{
		if (pkThingInst->isShow())
		{
			pkThingInst->UpdateLODLevel();
		}
	}

	for (const auto& aniThing : m_AniThingCloneInstanceVector)
	{
#ifdef ENABLE_ANIMATION_WING
		aniThing->Deform();
#endif
		aniThing->Update();
	}
}

#ifdef ENABLE_HEAVY_EFFECT_FIX
void CArea::__UpdateEffectList()
{
	int peNum;
	float pfStart, pfEnd, pfFarClip;
	CPythonBackground::instance().GetDistanceSetInfo(&peNum, &pfStart, &pfEnd, &pfFarClip);
	CInstanceBase* pInst = CPythonCharacterManager::instance().GetMainInstancePtr();

	if (!pInst)
		return;

	D3DXVECTOR3 chrPos = pInst->GetGraphicThingInstanceRef().GetPosition();
	CEffectManager& rkEftMgr = CEffectManager::Instance();

	for (TEffectInstanceIterator i = m_EffectInstanceMap.begin(); i != m_EffectInstanceMap.end();)
	{
		CEffectInstance* pEffectInstance = i->second;

		const D3DMATRIX& gMatrix = pEffectInstance->GetGlobalMatrix();
		if (pfStart < GetPixelPositionDistance(chrPos, TPixelPosition(gMatrix._41, gMatrix._42, gMatrix._43)))
		{
			pEffectInstance->Hide();
			++i;
			continue;
		}

		pEffectInstance->Show();
		pEffectInstance->Update();

		if (!pEffectInstance->isAlive())
		{
			i = m_EffectInstanceMap.erase(i);
			rkEftMgr.DestroyUnsafeEffectInstance(pEffectInstance);
		}
		else
		{
			++i;
		}
	}
}
#else
void CArea::__UpdateEffectList()
{
	//if (!CEffectManager::InstancePtr())
	//	return;

	CEffectManager& rkEftMgr = CEffectManager::Instance();

	// Effect
	TEffectInstanceIterator i;
	for (i = m_EffectInstanceMap.begin(); i != m_EffectInstanceMap.end();)
	{
		CEffectInstance* pEffectInstance = i->second;

		pEffectInstance->Update();

		if (!pEffectInstance->isAlive())
		{
			i = m_EffectInstanceMap.erase(i);
			rkEftMgr.DestroyUnsafeEffectInstance(pEffectInstance);
		}
		else
			++i;
	}
}
#endif

void CArea::Update(
#ifdef ENABLE_AREA_OPTIMISATION
	D3DXVECTOR3& v3Player
#endif
)
{
#ifdef ENABLE_AREA_OPTIMISATION
	__UpdateLoadedObjectInstances(v3Player);
	__UpdateAniThingList();
	__UpdateEffectList(v3Player);
#else
	__UpdateAniThingList();
#endif
}

struct CArea_LessEffectInstancePtrRenderOrder
{
	bool operator() (CEffectInstance* pkLeft, CEffectInstance* pkRight)
	{
		return pkLeft->LessRenderOrder(pkRight);
	}
};

struct CArea_FEffectInstanceRender
{
	inline void operator () (CEffectInstance* pkEftInst)
	{
		pkEftInst->Render();
	}
};

void CArea::RenderEffect()
{
#ifndef ENABLE_AREA_OPTIMISATION
	__UpdateEffectList();
#endif

	// Effect
	STATEMANAGER.SetTexture(0, NULL);
	STATEMANAGER.SetTexture(1, NULL);

	bool m_isDisableSortRendering = false;

	if (m_isDisableSortRendering)
	{
		for (const auto& effect : m_EffectInstanceMap)
		{
			effect.second->Render();
		}
	}
	else
	{
		static std::vector<CEffectInstance*> s_kVct_pkEftInstSort;
		s_kVct_pkEftInstSort.clear();

		for (auto i = m_EffectInstanceMap.begin(); i != m_EffectInstanceMap.end(); ++i)
			s_kVct_pkEftInstSort.push_back(i->second);

		std::sort(s_kVct_pkEftInstSort.begin(), s_kVct_pkEftInstSort.end(), CArea_LessEffectInstancePtrRenderOrder());
		std::for_each(s_kVct_pkEftInstSort.begin(), s_kVct_pkEftInstSort.end(), CArea_FEffectInstanceRender());
	}
}

DWORD CArea::DEBUG_GetRenderedCRCNum()
{
	return m_kRenderedThingInstanceCRCWithNumberVector.size();
}

CArea::TCRCWithNumberVector& CArea::DEBUG_GetRenderedCRCWithNumVector()
{
	return m_kRenderedThingInstanceCRCWithNumberVector;
}

DWORD CArea::DEBUG_GetRenderedGrapphicThingInstanceNum()
{
	return m_kRenderedGrapphicThingInstanceVector.size();
}

void CArea::CollectRenderingObject(std::vector<CGraphicThingInstance*>& rkVct_pkOpaqueThingInst)
{
	for (const auto& pkThingInst : m_ThingCloneInstaceVector)
	{
		if (pkThingInst->isShow() && !pkThingInst->HaveBlendThing())
		{
			rkVct_pkOpaqueThingInst.push_back(pkThingInst);
		}
	}
}

void CArea::CollectBlendRenderingObject(std::vector<CGraphicThingInstance*>& rkVct_pkBlendThingInst)
{
	for (const auto& pkThingInst : m_ThingCloneInstaceVector)
	{
		if (pkThingInst->isShow() && pkThingInst->HaveBlendThing())
		{
			rkVct_pkBlendThingInst.push_back(pkThingInst);
		}
	}
}

void CArea::Render()
{
	for (const auto& pkThingInst : m_AniThingCloneInstanceVector)
		pkThingInst->Deform();

	m_kRenderedThingInstanceCRCWithNumberVector.clear();
	m_kRenderedGrapphicThingInstanceVector.clear();
	m_kRenderedThingInstanceCRCWithNumberVector.reserve(m_ThingCloneInstaceVector.size());
	m_kRenderedGrapphicThingInstanceVector.reserve(m_ThingCloneInstaceVector.size());

	for (CGraphicThingInstance* pkThingInst : m_ThingCloneInstaceVector)
	{
		if (pkThingInst->Render())
		{
			auto aGraphicThingInstanceCRCMapIterator = m_GraphicThingInstanceCRCMap.find(pkThingInst);
			DWORD dwCRC = aGraphicThingInstanceCRCMapIterator->second;

			m_kRenderedGrapphicThingInstanceVector.push_back(pkThingInst);

			auto aCRCWithNumberVectorIterator = std::find_if(m_kRenderedThingInstanceCRCWithNumberVector.begin(), m_kRenderedThingInstanceCRCWithNumberVector.end(), [dwCRC](const TCRCWithNumber& aCRCWithNumber) {
				return aCRCWithNumber.dwCRC == dwCRC;
				});

			if (aCRCWithNumberVectorIterator == m_kRenderedThingInstanceCRCWithNumberVector.end())
			{
				TCRCWithNumber aCRCWithNumber;
				aCRCWithNumber.dwCRC = dwCRC;
				aCRCWithNumber.dwNumber = 1;
				m_kRenderedThingInstanceCRCWithNumberVector.push_back(aCRCWithNumber);
			}
			else
			{
				aCRCWithNumberVectorIterator->dwNumber += 1;
			}
		}
	}

	std::sort(m_kRenderedThingInstanceCRCWithNumberVector.begin(), m_kRenderedThingInstanceCRCWithNumberVector.end(), CRCNumComp());
}


void CArea::RenderCollision()
{
	DWORD i;

	STATEMANAGER.SetTexture(0, NULL);
	STATEMANAGER.SetTexture(1, NULL);

	STATEMANAGER.SaveRenderState(D3DRS_ALPHABLENDENABLE, FALSE);
	STATEMANAGER.SaveRenderState(D3DRS_CULLMODE, D3DCULL_NONE);
	STATEMANAGER.SetRenderState(D3DRS_LIGHTING, FALSE);
	STATEMANAGER.SetRenderState(D3DRS_TEXTUREFACTOR, 0xff000000);
	STATEMANAGER.SetTextureStageState(0, D3DTSS_COLORARG1, D3DTA_TEXTURE);
	STATEMANAGER.SetTextureStageState(0, D3DTSS_COLOROP, D3DTOP_SELECTARG1);
	STATEMANAGER.SetTextureStageState(0, D3DTSS_ALPHAOP, D3DTOP_DISABLE);
	STATEMANAGER.SetTextureStageState(1, D3DTSS_COLOROP, D3DTOP_DISABLE);
	STATEMANAGER.SetTextureStageState(1, D3DTSS_ALPHAOP, D3DTOP_DISABLE);

	for (i = 0; i < GetObjectInstanceCount(); i++)
	{
		const TObjectInstance* po;
		if (GetObjectInstancePointer(i, &po))
		{
			if (po->pTree && po->pTree->isShow())
			{
				DWORD j;
				for (j = 0; j < po->pTree->GetCollisionInstanceCount(); j++)
				{
					po->pTree->GetCollisionInstanceData(j)->Render();
				}
			}
			if (po->pThingInstance && po->pThingInstance->isShow())
			{
				DWORD j;
				for (j = 0; j < po->pThingInstance->GetCollisionInstanceCount(); j++)
				{
					po->pThingInstance->GetCollisionInstanceData(j)->Render();
				}
			}
			if (po->pDungeonBlock && po->pDungeonBlock->isShow())
			{
				DWORD j;
				for (j = 0; j < po->pDungeonBlock->GetCollisionInstanceCount(); j++)
				{
					po->pDungeonBlock->GetCollisionInstanceData(j)->Render();
				}
			}
		}
	}

	STATEMANAGER.RestoreRenderState(D3DRS_ALPHABLENDENABLE);
	STATEMANAGER.RestoreRenderState(D3DRS_CULLMODE);
	STATEMANAGER.SetRenderState(D3DRS_LIGHTING, TRUE);
}

void CArea::RenderDungeon()
{
	STATEMANAGER.SetTextureStageState(0, D3DTSS_COLORARG1, D3DTA_TEXTURE);
	STATEMANAGER.SetTextureStageState(0, D3DTSS_COLOROP, D3DTOP_SELECTARG1);
	STATEMANAGER.SetTextureStageState(0, D3DTSS_ALPHAARG1, D3DTA_TEXTURE);
	STATEMANAGER.SetTextureStageState(0, D3DTSS_COLOROP, D3DTOP_SELECTARG1);
	STATEMANAGER.SetTextureStageState(1, D3DTSS_COLORARG1, D3DTA_TEXTURE);
	STATEMANAGER.SetTextureStageState(1, D3DTSS_COLORARG2, D3DTA_CURRENT);
	STATEMANAGER.SetTextureStageState(1, D3DTSS_COLOROP, D3DTOP_MODULATE);
	STATEMANAGER.SetTextureStageState(1, D3DTSS_ALPHAARG1, D3DTA_TEXTURE);
	STATEMANAGER.SetTextureStageState(1, D3DTSS_ALPHAARG2, D3DTA_CURRENT);
	STATEMANAGER.SetTextureStageState(1, D3DTSS_ALPHAOP, D3DTOP_MODULATE);

	for (const auto& pDungeonBlockInstance : m_DungeonBlockCloneInstanceVector)
		pDungeonBlockInstance->Render();

	STATEMANAGER.SetTextureStageState(1, D3DTSS_COLOROP, D3DTOP_DISABLE);
	STATEMANAGER.SetTextureStageState(1, D3DTSS_ALPHAOP, D3DTOP_DISABLE);
}


#ifdef ENABLE_AREA_OPTIMISATION
void CArea::Refresh(TObjectInstance* pObjectInstance, bool bRemove)
{
	if (!pObjectInstance)
		return;

	if (prt::PROPERTY_TYPE_TREE == pObjectInstance->dwType)
	{
		if (pObjectInstance->pTree)
		{
			if (bRemove)
			{
				auto it = std::find(m_TreeCloneInstaceVector.begin(), m_TreeCloneInstaceVector.end(), pObjectInstance->pTree);
				if (it != m_TreeCloneInstaceVector.end())
					m_TreeCloneInstaceVector.erase(it);
			}
			else
			{
				m_TreeCloneInstaceVector.emplace_back(pObjectInstance->pTree);

				const float* pfPosition;
				pfPosition = pObjectInstance->pTree->GetPosition();
				pObjectInstance->pTree->UpdateBoundingSphere();
				pObjectInstance->pTree->UpdateCollisionData();
			}
		}
	}
	else if (prt::PROPERTY_TYPE_BUILDING == pObjectInstance->dwType)
	{
		if (bRemove)
		{
			auto it = std::find(m_ThingCloneInstaceVector.begin(), m_ThingCloneInstaceVector.end(), pObjectInstance->pThingInstance);
			if (it != m_ThingCloneInstaceVector.end())
				m_ThingCloneInstaceVector.erase(it);

			if (pObjectInstance->pThingInstance->IsMotionThing())
			{
				auto it = std::find(m_AniThingCloneInstanceVector.begin(), m_AniThingCloneInstanceVector.end(), pObjectInstance->pThingInstance);
				if (it != m_AniThingCloneInstanceVector.end())
					m_AniThingCloneInstanceVector.erase(it);
			}

			if (pObjectInstance->isShadowFlag)
			{
				auto it = std::find(m_ShadowThingCloneInstaceVector.begin(), m_ShadowThingCloneInstaceVector.end(), pObjectInstance->pThingInstance);
				if (it != m_ShadowThingCloneInstaceVector.end())
					m_ShadowThingCloneInstaceVector.erase(it);
			}
		}
		else
		{
			pObjectInstance->pThingInstance->Update();
			pObjectInstance->pThingInstance->Transform();
			pObjectInstance->pThingInstance->Show();
			pObjectInstance->pThingInstance->DeformAll();
			m_ThingCloneInstaceVector.emplace_back(pObjectInstance->pThingInstance);

			pObjectInstance->pThingInstance->BuildBoundingSphere();
			pObjectInstance->pThingInstance->UpdateBoundingSphere();

			if (pObjectInstance->pThingInstance->IsMotionThing())
			{
				m_AniThingCloneInstanceVector.emplace_back(pObjectInstance->pThingInstance);
				pObjectInstance->pThingInstance->SetMotion(0);
			}

			if (pObjectInstance->isShadowFlag)
			{
				m_ShadowThingCloneInstaceVector.emplace_back(pObjectInstance->pThingInstance);
			}

			if (pObjectInstance->pAttributeInstance)
			{
				pObjectInstance->pThingInstance->UpdateCollisionData(&pObjectInstance->pAttributeInstance->GetObjectPointer()->GetCollisionDataVector());
				pObjectInstance->pAttributeInstance->RefreshObject(pObjectInstance->pThingInstance->GetTransform());
				pObjectInstance->pThingInstance->UpdateHeightInstance(pObjectInstance->pAttributeInstance);
			}
		}
	}
	else if (prt::PROPERTY_TYPE_EFFECT == pObjectInstance->dwType)
	{
	}
	else if (prt::PROPERTY_TYPE_AMBIENCE == pObjectInstance->dwType)
	{
		return;
	}
	else if (prt::PROPERTY_TYPE_DUNGEON_BLOCK == pObjectInstance->dwType)
	{
		if (bRemove)
		{
			auto it = std::find(m_DungeonBlockCloneInstanceVector.begin(), m_DungeonBlockCloneInstanceVector.end(), pObjectInstance->pDungeonBlock);
			if (it != m_DungeonBlockCloneInstanceVector.end())
				m_DungeonBlockCloneInstanceVector.erase(it);
		}
		else
		{
			pObjectInstance->pDungeonBlock->Update();
			pObjectInstance->pDungeonBlock->Deform();
			pObjectInstance->pDungeonBlock->UpdateBoundingSphere();
			m_DungeonBlockCloneInstanceVector.emplace_back(pObjectInstance->pDungeonBlock);

			if (pObjectInstance->pAttributeInstance)
			{
				pObjectInstance->pDungeonBlock->UpdateCollisionData(&pObjectInstance->pAttributeInstance->GetObjectPointer()->GetCollisionDataVector());
				pObjectInstance->pAttributeInstance->RefreshObject(pObjectInstance->pDungeonBlock->GetTransform());
				pObjectInstance->pDungeonBlock->UpdateHeightInstance(pObjectInstance->pAttributeInstance);
			}
		}
	}
}
#else
void CArea::Refresh()
{
	m_TreeCloneInstaceVector.clear();
	m_ThingCloneInstaceVector.clear();
	m_DungeonBlockCloneInstanceVector.clear();
	m_AniThingCloneInstanceVector.clear();
	m_ShadowThingCloneInstaceVector.clear();

	for (const auto& pObjectInstance : m_ObjectInstanceVector)
	{
		if (prt::PROPERTY_TYPE_TREE == pObjectInstance->dwType)
		{
			if (pObjectInstance->pTree)
			{
				m_TreeCloneInstaceVector.push_back(pObjectInstance->pTree);
				pObjectInstance->pTree->UpdateBoundingSphere();
				pObjectInstance->pTree->UpdateCollisionData();
			}
		}
		else if (prt::PROPERTY_TYPE_BUILDING == pObjectInstance->dwType)
		{
			auto pThingInstance = pObjectInstance->pThingInstance;
			pThingInstance->Update();
			pThingInstance->Transform();
			pThingInstance->Show();
			pThingInstance->DeformAll();
			m_ThingCloneInstaceVector.push_back(pThingInstance);

			pThingInstance->BuildBoundingSphere();
			pThingInstance->UpdateBoundingSphere();

			if (pThingInstance->IsMotionThing())
			{
				m_AniThingCloneInstanceVector.push_back(pThingInstance);
				pThingInstance->SetMotion(0);
			}

			if (pObjectInstance->isShadowFlag)
			{
				m_ShadowThingCloneInstaceVector.push_back(pThingInstance);
			}

			const auto pAttributeInstance = pObjectInstance->pAttributeInstance;
			if (pAttributeInstance)
			{
				pThingInstance->UpdateCollisionData(&pAttributeInstance->GetObjectPointer()->GetCollisionDataVector());
				pAttributeInstance->RefreshObject(pThingInstance->GetTransform());
				pThingInstance->UpdateHeightInstance(pAttributeInstance);
			}
		}
		else if (prt::PROPERTY_TYPE_EFFECT == pObjectInstance->dwType)
		{
			// Effect handling
		}
		else if (prt::PROPERTY_TYPE_AMBIENCE == pObjectInstance->dwType)
		{
			return;
		}
		else if (prt::PROPERTY_TYPE_DUNGEON_BLOCK == pObjectInstance->dwType)
		{
			auto pDungeonBlock = pObjectInstance->pDungeonBlock;
			pDungeonBlock->Update();
			pDungeonBlock->Deform();
			pDungeonBlock->UpdateBoundingSphere();
			m_DungeonBlockCloneInstanceVector.push_back(pDungeonBlock);

			const auto pAttributeInstance = pObjectInstance->pAttributeInstance;
			if (pAttributeInstance)
			{
				pDungeonBlock->UpdateCollisionData(&pAttributeInstance->GetObjectPointer()->GetCollisionDataVector());
				pAttributeInstance->RefreshObject(pDungeonBlock->GetTransform());
				pDungeonBlock->UpdateHeightInstance(pAttributeInstance);
			}
		}
	}
}
#endif

#ifdef ENABLE_AREA_OPTIMISATION
void CArea::__Load_BuildObjectInstances()
{
	m_ObjectInstanceVector.clear();
	m_ObjectInstanceVector.resize(GetObjectDataCount(), nullptr);

	m_GraphicThingInstanceCRCMap.clear();

	std::sort(m_ObjectDataVector.begin(), m_ObjectDataVector.end(), ObjectDataComp());
}
#else
void CArea::__Load_BuildObjectInstances()
{
	m_ObjectInstanceVector.resize(GetObjectDataCount());
	m_GraphicThingInstanceCRCMap.clear();
	
	std::sort(m_ObjectDataVector.begin(), m_ObjectDataVector.end(), ObjectDataComp());
	
	TObjectInstanceVector::iterator it = m_ObjectInstanceVector.begin();
	for (const TObjectData& objectData : m_ObjectDataVector)
	{
		TObjectInstance* objectInstance = ms_ObjectInstancePool.Alloc();
		objectInstance->Clear();
	
		__SetObjectInstance(objectInstance, &objectData);
	
		if (objectInstance->dwType == prt::PROPERTY_TYPE_BUILDING)
			m_GraphicThingInstanceCRCMap.insert({ objectInstance->pThingInstance, objectData.dwCRC });
	
		*it++ = objectInstance;
	}
	
	Refresh();

}
#endif

void CArea::__SetObjectInstance(TObjectInstance* pObjectInstance, const TObjectData* c_pData)
{
	CProperty* pProperty = nullptr;
	if (!CPropertyManager::Instance().Get(c_pData->dwCRC, &pProperty))
		return;

	const char* c_szPropertyType;

	if (!pProperty->GetString("PropertyType", &c_szPropertyType))
		return;

	switch (prt::GetPropertyType(c_szPropertyType))
	{
	case prt::PROPERTY_TYPE_TREE:
		__SetObjectInstance_SetTree(pObjectInstance, c_pData, pProperty);
		break;

	case prt::PROPERTY_TYPE_BUILDING:
		__SetObjectInstance_SetBuilding(pObjectInstance, c_pData, pProperty);
		break;

	case prt::PROPERTY_TYPE_EFFECT:
		__SetObjectInstance_SetEffect(pObjectInstance, c_pData, pProperty);
		break;

	case prt::PROPERTY_TYPE_AMBIENCE:
		break;

	case prt::PROPERTY_TYPE_DUNGEON_BLOCK:
		__SetObjectInstance_SetDungeonBlock(pObjectInstance, c_pData, pProperty);
		break;
	}
}

void CArea::__SetObjectInstance_SetEffect(TObjectInstance* pObjectInstance, const TObjectData* c_pData, CProperty* pProperty)
{
	prt::TPropertyEffect Data;
	if (!prt::PropertyEffectStringToData(pProperty, &Data))
		return;

	pObjectInstance->dwType = prt::PROPERTY_TYPE_EFFECT;
	pObjectInstance->dwEffectID = GetCaseCRC32(Data.strFileName.c_str(), Data.strFileName.size());
	CEffectManager& rem = CEffectManager::Instance();
	CEffectData* pData;
	if (!rem.GetEffectData(pObjectInstance->dwEffectID, &pData))
	{
		if (!rem.RegisterEffect(Data.strFileName.c_str()))
		{
			pObjectInstance->dwEffectID = 0xffffffff;
			TraceError("CArea::SetEffect effect register error %s\n", Data.strFileName.c_str());
			return;
		}
	}

	CEffectInstance* pEffectInstance;
	rem.CreateUnsafeEffectInstance(pObjectInstance->dwEffectID, &pEffectInstance);

	D3DXMATRIX mat;
	D3DXMatrixRotationYawPitchRoll(&mat,
		D3DXToRadian(c_pData->m_fYaw),
		D3DXToRadian(c_pData->m_fPitch),
		D3DXToRadian(c_pData->m_fRoll)
	);

	mat._41 = c_pData->Position.x;
	mat._42 = c_pData->Position.y;
	mat._43 = c_pData->Position.z + c_pData->m_fHeightBias;

	pEffectInstance->SetGlobalMatrix(mat);

#ifdef ENABLE_AREA_OPTIMISATION
	pObjectInstance->dwEffectInstanceIndex = reinterpret_cast<uint32_t>(pEffectInstance);
#else
	pObjectInstance->dwEffectInstanceIndex = static_cast<uint32_t>(m_EffectInstanceMap.size());
#endif

	m_EffectInstanceMap.emplace(pObjectInstance->dwEffectInstanceIndex, pEffectInstance);
}

void CArea::__SetObjectInstance_SetTree(TObjectInstance* pObjectInstance, const TObjectData* c_pData, CProperty* pProperty)
{
	const char* c_szTreeName;
	if (!pProperty->GetString("TreeFile", &c_szTreeName))
		return;

	pObjectInstance->SetTree(
		c_pData->Position.x,
		c_pData->Position.y,
		c_pData->Position.z + c_pData->m_fHeightBias,
		c_pData->dwCRC,
		c_szTreeName
	);
}

void CArea::TObjectInstance::SetTree(float x, float y, float z, DWORD dwTreeCRC, const char* c_szTreeName)
{
	CSpeedTreeForestDirectX8& rkForest = CSpeedTreeForestDirectX8::Instance();
	pTree = rkForest.CreateInstance(x, y, z, dwTreeCRC, c_szTreeName);
	dwType = prt::PROPERTY_TYPE_TREE;
}

void CArea::__SetObjectInstance_SetBuilding(TObjectInstance* pObjectInstance, const TObjectData* c_pData, CProperty* pProperty)
{
	prt::TPropertyBuilding Data;
	if (!prt::PropertyBuildingStringToData(pProperty, &Data))
		return;

	CResourceManager& rkResMgr = CResourceManager::Instance();

	CGraphicThing* pThing = static_cast<CGraphicThing*>(rkResMgr.GetResourcePointer(Data.strFileName.c_str()));
	pThing->AddReference();

	if (!pThing || pThing->IsEmpty())
	{
#ifdef _DEBUG
		TraceError("CArea::SetBuilding: There is no data: %s", Data.strFileName.c_str());
#endif
		return;
	}

	int iModelCount = pThing->GetModelCount();
	int iMotionCount = pThing->GetMotionCount();

	pObjectInstance->dwType = prt::PROPERTY_TYPE_BUILDING;
	pObjectInstance->pThingInstance = CGraphicThingInstance::New();
	pObjectInstance->pThingInstance->Initialize();
	pObjectInstance->pThingInstance->ReserveModelThing(iModelCount);
	pObjectInstance->pThingInstance->ReserveModelInstance(iModelCount);
	pObjectInstance->pThingInstance->RegisterModelThing(0, pThing);
	for (int j = 0; j < PORTAL_ID_MAX_NUM; ++j)
	{
		if (c_pData->abyPortalID[j] != 0)
			pObjectInstance->pThingInstance->SetPortal(j, c_pData->abyPortalID[j]);
	}

	std::string stSrcModelFileName = Data.strFileName;
	std::string stLODModelFileName;

	char szLODModelFileNameEnd[256];
	for (UINT uLODIndex = 1; uLODIndex <= 3; ++uLODIndex)
	{
		sprintf_s(szLODModelFileNameEnd, "_lod_%.2d.gr2", uLODIndex);
		stLODModelFileName = CFileNameHelper::NoExtension(stSrcModelFileName) + szLODModelFileNameEnd;
		if (!rkResMgr.IsFileExist(stLODModelFileName.c_str()))
			break;

		CGraphicThing* pLODModelThing = static_cast<CGraphicThing*>(rkResMgr.GetResourcePointer(stLODModelFileName.c_str()));
		if (!pLODModelThing)
			break;

		pObjectInstance->pThingInstance->RegisterLODThing(0, pLODModelThing);
	}

	for (int i = 0; i < iModelCount; ++i)
		pObjectInstance->pThingInstance->SetModelInstance(i, 0, i);

	if (iMotionCount)
	{
		pObjectInstance->pThingInstance->RegisterMotionThing(0, pThing);
	}

	pObjectInstance->pThingInstance->SetPosition(c_pData->Position.x, c_pData->Position.y, c_pData->Position.z + c_pData->m_fHeightBias);
	pObjectInstance->pThingInstance->SetRotation(
		c_pData->m_fYaw,
		c_pData->m_fPitch,
		c_pData->m_fRoll
	);

    pObjectInstance->isShadowFlag = Data.isShadowFlag;
    pObjectInstance->pThingInstance->RegisterBoundingSphere();
    __LoadAttribute(pObjectInstance, Data.strAttributeDataFileName.c_str());

	pThing->Release();
}

void CArea::__SetObjectInstance_SetDungeonBlock(TObjectInstance* pObjectInstance, const TObjectData* c_pData, CProperty* pProperty)
{
	prt::TPropertyDungeonBlock Data;
	if (!prt::PropertyDungeonBlockStringToData(pProperty, &Data))
		return;

	pObjectInstance->dwType = prt::PROPERTY_TYPE_DUNGEON_BLOCK;
	pObjectInstance->pDungeonBlock = ms_DungeonBlockInstancePool.Alloc();
	pObjectInstance->pDungeonBlock->Load(Data.strFileName.c_str());
	pObjectInstance->pDungeonBlock->SetPosition(c_pData->Position.x, c_pData->Position.y, c_pData->Position.z + c_pData->m_fHeightBias);
	pObjectInstance->pDungeonBlock->SetRotation(
		c_pData->m_fYaw,
		c_pData->m_fPitch,
		c_pData->m_fRoll
	);
	pObjectInstance->pDungeonBlock->Update();
	pObjectInstance->pDungeonBlock->BuildBoundingSphere();
	pObjectInstance->pDungeonBlock->RegisterBoundingSphere();
	for (int j = 0; j < PORTAL_ID_MAX_NUM; ++j)
		if (0 != c_pData->abyPortalID[j])
			pObjectInstance->pDungeonBlock->SetPortal(j, c_pData->abyPortalID[j]);
	__LoadAttribute(pObjectInstance, Data.strAttributeDataFileName.c_str());
}

void CArea::__LoadAttribute(TObjectInstance* pObjectInstance, const char* c_szAttributeFileName)
{
	const bool bFileExist = CResourceManager::Instance().IsFileExist(c_szAttributeFileName);

	CAttributeData* pAttributeData = static_cast<CAttributeData*>(CResourceManager::Instance().GetResourcePointer(c_szAttributeFileName));

	CAttributeInstance* pAttrInstance = ms_AttributeInstancePool.Alloc();
	pAttrInstance->Clear();
	pAttrInstance->SetObjectPointer(pAttributeData);

	if (!bFileExist)
	{
		std::string attrFileName(c_szAttributeFileName);
		std::transform(attrFileName.begin(), attrFileName.end(), attrFileName.begin(), [](unsigned char c) { return std::tolower(c); });
		const bool bIsDungeonObject = (std::string::npos != attrFileName.find("/dungeon/")) || (std::string::npos != attrFileName.find("\\dungeon\\"));

		if (pAttributeData->IsEmpty() && !bIsDungeonObject)
		{
			if (pObjectInstance && pObjectInstance->pThingInstance)
			{
				CGraphicThingInstance* object = pObjectInstance->pThingInstance;
				D3DXVECTOR3 v3Min, v3Max;
				object->GetBoundingAABB(v3Min, v3Max);

				CStaticCollisionData collision;
				collision.dwType = COLLISION_TYPE_OBB;
				D3DXQuaternionRotationYawPitchRoll(&collision.quatRotation, object->GetYaw(), object->GetPitch(), object->GetRoll());
				strncpy_s(collision.szName, sizeof(collision.szName), "DummyCollisionOBB", sizeof(collision.szName) - 1);
				collision.v3Position = (v3Min + v3Max) * 0.5f;

				D3DXVECTOR3 vDelta = (v3Max - v3Min);
				collision.fDimensions[0] = vDelta.x * 0.5f;
				collision.fDimensions[1] = vDelta.y * 0.5f;
				collision.fDimensions[2] = vDelta.z * 0.5f;

				pAttributeData->AddCollisionData(collision);
			}
		}
	}

	if (!pAttributeData->IsEmpty())
	{
		pObjectInstance->pAttributeInstance = pAttrInstance;
	}
	else
	{
		pAttrInstance->Clear();
		ms_AttributeInstancePool.Free(pAttrInstance);
	}
}

bool CArea::Load(const char* c_szPathName)
{
	Clear();

	std::string strObjectDataFileName = std::string(c_szPathName) + "AreaData.txt";

	__Load_LoadObject(strObjectDataFileName.c_str());
	__Load_BuildObjectInstances();

	return true;
}

bool CArea::__Load_LoadObject(const char* c_szFileName)
{
	CTokenVectorMap stTokenVectorMap;

	if (!LoadMultipleTextData(c_szFileName, stTokenVectorMap))
	{
		TraceError(" CArea::Load File Load %s ERROR", c_szFileName);
		return false;
	}

	if (stTokenVectorMap.end() == stTokenVectorMap.find("areadatafile"))
	{
		TraceError(" CArea::__LoadObject File Format %s ERROR 1", c_szFileName);
		return false;
	}

	if (stTokenVectorMap.end() == stTokenVectorMap.find("objectcount"))
	{
		TraceError(" CArea::__LoadObject File Format %s ERROR 2", c_szFileName);
		return false;
	}

	const std::string& c_rstrCount = stTokenVectorMap["objectcount"][0];

	DWORD dwCount = atoi(c_rstrCount.c_str());

	char szObjectName[32 + 1];

	for (DWORD i = 0; i < dwCount; ++i)
	{
		_snprintf(szObjectName, sizeof(szObjectName), "object%03d", i);

		if (stTokenVectorMap.end() == stTokenVectorMap.find(szObjectName))
			continue;

		const CTokenVector& rVector = stTokenVectorMap[szObjectName];

		const std::string& c_rstrxPosition = rVector[0].c_str();
		const std::string& c_rstryPosition = rVector[1].c_str();
		const std::string& c_rstrzPosition = rVector[2].c_str();
		const std::string& c_rstrCRC = rVector[3].c_str();

		TObjectData ObjectData;
		ZeroMemory(&ObjectData, sizeof(ObjectData));
		ObjectData.Position.x = atof(c_rstrxPosition.c_str());
		ObjectData.Position.y = atof(c_rstryPosition.c_str());
		ObjectData.Position.z = atof(c_rstrzPosition.c_str());
		ObjectData.dwCRC = atoi(c_rstrCRC.c_str());

		ObjectData.InitializeRotation(); //ObjectData.m_fYaw = ObjectData.m_fPitch = ObjectData.m_fRoll = 0;
		if (rVector.size() > 4)
		{
			std::string::size_type s = rVector[4].find('#');
			if (s != rVector[4].npos)
			{
				ObjectData.m_fYaw = atoi(rVector[4].substr(0, s - 1).c_str());
				int p = s + 1;
				s = rVector[4].find('#', p);
				ObjectData.m_fPitch = atoi(rVector[4].substr(p, s - 1 - p + 1).c_str());
				ObjectData.m_fRoll = atoi(rVector[4].substr(s + 1).c_str());
			}
			else
			{
				ObjectData.m_fYaw = 0.0f;
				ObjectData.m_fPitch = 0.0f;
				ObjectData.m_fRoll = atoi(rVector[4].c_str());
			}
		}

		ObjectData.m_fHeightBias = 0.0f;
		if (rVector.size() > 5)
		{
			ObjectData.m_fHeightBias = atof(rVector[5].c_str());
		}

		if (rVector.size() > 6)
		{
			for (int portalIdx = 0; portalIdx < min(rVector.size() - 6, PORTAL_ID_MAX_NUM); ++portalIdx)
			{
				ObjectData.abyPortalID[portalIdx] = atoi(rVector[6 + portalIdx].c_str());
			}
		}

		// If data is not inside property, then delete it.
		CProperty* pProperty;
		if (!CPropertyManager::Instance().Get(ObjectData.dwCRC, &pProperty))
		{
			TraceError(" CArea::LoadObject Property(%u) Load ERROR", ObjectData.dwCRC);
			continue;
		}

		m_ObjectDataVector.push_back(ObjectData);
	}

	return true;
}

//////////////////////////////////////////////////////////////////////////

bool CArea::CheckObjectIndex(DWORD dwIndex) const
{
	if (dwIndex >= m_ObjectDataVector.size())
		return false;

	return true;
}

DWORD CArea::GetObjectDataCount()
{
	return m_ObjectDataVector.size();
}

bool CArea::GetObjectDataPointer(DWORD dwIndex, const TObjectData** ppObjectData) const
{
	if (!CheckObjectIndex(dwIndex))
	{
		assert(!"Setting Object Index is corrupted!");
		return false;
	}

	*ppObjectData = &m_ObjectDataVector[dwIndex];
	return true;
}

const DWORD CArea::GetObjectInstanceCount() const
{
	return m_ObjectInstanceVector.size();
}

const bool CArea::GetObjectInstancePointer(const DWORD& dwIndex, const TObjectInstance** ppObjectInstance) const
{
	if (dwIndex >= m_ObjectInstanceVector.size())
		return false;

	*ppObjectInstance = m_ObjectInstanceVector[dwIndex];
#ifdef ENABLE_AREA_OPTIMISATION
	return (*ppObjectInstance) != nullptr;
#else
	return true;
#endif
}

void CArea::EnablePortal(BOOL bFlag)
{
	if (m_bPortalEnable == bFlag)
		return;

	m_bPortalEnable = bFlag;
}

void CArea::ClearPortal()
{
	m_kSet_ShowingPortalID.clear();
}

void CArea::AddShowingPortalID(int iNum)
{
	m_kSet_ShowingPortalID.insert(iNum);
}

void CArea::RefreshPortal()
{
	std::set<TObjectInstance*> kSet_ShowingObjectInstance;
	kSet_ShowingObjectInstance.clear();
	for (DWORD i = 0; i < m_ObjectDataVector.size(); ++i)
	{
		TObjectData& rData = m_ObjectDataVector[i];
		TObjectInstance* pInstance = m_ObjectInstanceVector[i];

		if (!pInstance)
			continue;

		for (int j = 0; j < PORTAL_ID_MAX_NUM; ++j)
		{
			BYTE byPortalID = rData.abyPortalID[j];
			if (0 == byPortalID)
				break;

			if (m_kSet_ShowingPortalID.end() == m_kSet_ShowingPortalID.find(byPortalID))
				continue;

			kSet_ShowingObjectInstance.insert(pInstance);
			break;
		}
	}

	///////////////////////////////////////////////////////////////////////////////////////////////

	m_TreeCloneInstaceVector.clear();
	m_ThingCloneInstaceVector.clear();
	m_DungeonBlockCloneInstanceVector.clear();

	TObjectInstanceVector::iterator it;
	for (it = m_ObjectInstanceVector.begin(); it != m_ObjectInstanceVector.end(); ++it)
	{
		TObjectInstance* pObjectInstance = *it;

		if (!pObjectInstance)
			continue;

		if (m_bPortalEnable)
		{
			if (kSet_ShowingObjectInstance.end() == kSet_ShowingObjectInstance.find(pObjectInstance))
				continue;
		}

		if (prt::PROPERTY_TYPE_TREE == pObjectInstance->dwType)
		{
			assert(pObjectInstance->pTree);
			m_TreeCloneInstaceVector.push_back(pObjectInstance->pTree);
		}
		else if (prt::PROPERTY_TYPE_BUILDING == pObjectInstance->dwType)
		{
			assert(pObjectInstance->pThingInstance);
			m_ThingCloneInstaceVector.push_back(pObjectInstance->pThingInstance);
		}
		else if (prt::PROPERTY_TYPE_DUNGEON_BLOCK == pObjectInstance->dwType)
		{
			assert(pObjectInstance->pDungeonBlock);
			m_DungeonBlockCloneInstanceVector.push_back(pObjectInstance->pDungeonBlock);
		}
	}
}

//////////////////////////////////////////////////////////////////////////

void CArea::Clear()
{
	// Real Instances
	TObjectInstanceVector::iterator it;
#ifdef ENABLE_AREA_OPTIMISATION
	for (it = m_ObjectInstanceVector.begin(); it != m_ObjectInstanceVector.end(); ++it)
	{
		if ((*it) != nullptr)
			__Clear_DestroyObjectInstance(*it);
	}
#else
	for (it = m_ObjectInstanceVector.begin(); it != m_ObjectInstanceVector.end(); ++it)
		__Clear_DestroyObjectInstance(*it);
#endif
	m_ObjectDataVector.clear();
	m_ObjectInstanceVector.clear();

	// Clones
	m_TreeCloneInstaceVector.clear();
	m_ThingCloneInstaceVector.clear();
	m_DungeonBlockCloneInstanceVector.clear();
	m_AniThingCloneInstanceVector.clear();
	m_ShadowThingCloneInstaceVector.clear();
	m_GraphicThingInstanceCRCMap.clear();
	m_kRenderedThingInstanceCRCWithNumberVector.clear();
	m_kRenderedGrapphicThingInstanceVector.clear();

	m_bPortalEnable = FALSE;
	ClearPortal();

	CEffectManager& rkEftMgr = CEffectManager::Instance();

	TEffectInstanceIterator i;
	for (i = m_EffectInstanceMap.begin(); i != m_EffectInstanceMap.end(); ++i)
	{
		CEffectInstance* pEffectInstance = i->second;
		rkEftMgr.DestroyUnsafeEffectInstance(pEffectInstance);
	}
	m_EffectInstanceMap.clear();
}

void CArea::__Clear_DestroyObjectInstance(TObjectInstance* pObjectInstance)
{
	if (pObjectInstance->dwEffectInstanceIndex != idxEffectInstance)
	{
		TEffectInstanceIterator f = m_EffectInstanceMap.find(pObjectInstance->dwEffectInstanceIndex);
		if (m_EffectInstanceMap.end() != f)
		{
			CEffectInstance* pEffectInstance = f->second;
			m_EffectInstanceMap.erase(f);

			if (CEffectManager::InstancePtr())
				CEffectManager::Instance().DestroyUnsafeEffectInstance(pEffectInstance);
		}
		pObjectInstance->dwEffectInstanceIndex = idxEffectInstance;
	}

	if (pObjectInstance->pAttributeInstance)
	{
		pObjectInstance->pAttributeInstance->Clear();
		ms_AttributeInstancePool.Free(pObjectInstance->pAttributeInstance);
		pObjectInstance->pAttributeInstance = NULL;
	}

	if (pObjectInstance->pTree)
	{
		pObjectInstance->pTree->Clear();
		CSpeedTreeForestDirectX8::Instance().DeleteInstance(pObjectInstance->pTree);
		pObjectInstance->pTree = NULL;
	}

	if (pObjectInstance->pThingInstance)
	{
		CGraphicThingInstance::Delete(pObjectInstance->pThingInstance);
		pObjectInstance->pThingInstance = NULL;
	}

	if (pObjectInstance->pDungeonBlock)
	{
		ms_DungeonBlockInstancePool.Free(pObjectInstance->pDungeonBlock);
		pObjectInstance->pDungeonBlock = NULL;
	}

	pObjectInstance->Clear();

	ms_ObjectInstancePool.Free(pObjectInstance);
}

//////////////////////////////////////////////////////////////////////////
void CArea::GetCoordinate(unsigned short* usCoordX, unsigned short* usCoordY)
{
	*usCoordX = m_wX;
	*usCoordY = m_wY;
}

void CArea::SetCoordinate(const unsigned short& usCoordX, const unsigned short& usCoordY)
{
	m_wX = usCoordX;
	m_wY = usCoordY;
}

//////////////////////////////////////////////////////////////////////////

void CArea::SetMapOutDoor(CMapOutdoor* pOwnerOutdoorMap)
{
	m_pOwnerOutdoorMap = pOwnerOutdoorMap;
}

CArea::CArea() : m_pOwnerOutdoorMap(NULL), m_bPortalEnable(0) //@M2Fixme001
{
	m_wX = m_wY = 0xFF;
#ifdef ENABLE_AREA_OPTIMISATION
	m_iUpdateCount = 0;
#endif
}

CArea::~CArea()
{
	Clear();
}

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

#ifdef ENABLE_AREA_OPTIMISATION
void CArea::__UpdateLoadedObjectInstances(D3DXVECTOR3& v3Player)
{
	const float fMaxDist = GetMaxLoadingDistanceSqr();
	const DWORD dwStartTime = ELTimer_GetMSec();

	DWORD i = 0;
	for (auto it = m_ObjectInstanceVector.begin(); it != m_ObjectInstanceVector.end(); ++it, ++i)
	{
		const TObjectData* c_pObjectData;

		if (!GetObjectDataPointer(i, &c_pObjectData))
			continue;

		bool bDidModify = false;
		const float fDist = (v3Player.x - c_pObjectData->Position.x) * (v3Player.x - c_pObjectData->Position.x)
			+ (v3Player.y - c_pObjectData->Position.y) * (v3Player.y - c_pObjectData->Position.y);

		if (fMaxDist > fDist)
		{
			if ((*it) == nullptr)
			{
				*it = ms_ObjectInstancePool.Alloc();
				(*it)->Clear();

				__SetObjectInstance(*it, c_pObjectData);

				if ((*it)->dwType == prt::PROPERTY_TYPE_BUILDING)
					m_GraphicThingInstanceCRCMap.emplace(TGraphicThingInstanceCRCMap::value_type((*it)->pThingInstance, c_pObjectData->dwCRC));

				Refresh(*it, false);
				bDidModify = true;
			}
		}
		else
		{
			if ((*it) != nullptr)
			{
				if ((*it)->dwType == prt::PROPERTY_TYPE_BUILDING)
					m_GraphicThingInstanceCRCMap.erase((*it)->pThingInstance);

				Refresh(*it, true);

				__Clear_DestroyObjectInstance(*it);
				*it = nullptr;
				bDidModify = true;
			}
		}

		if (bDidModify)
		{
			const DWORD dwElapsed = ELTimer_GetMSec() - dwStartTime;
			if (dwElapsed > 2)
				break;
		}
	}
}

void CArea::__UpdateEffectList(D3DXVECTOR3& v3Player)
{
	m_kVct_pkEftInstSort.clear();

	const int iUpdateFPS = MAX(2, CPythonApplication::Instance().GetUpdateFPS());
	const float fMaxDist = GetMaxLoadingDistanceSqr();

	if (CEffectManager* pEffectManager = CEffectManager::InstancePtr())
	{
		// Effect
		for (auto i = m_EffectInstanceMap.begin(); i != m_EffectInstanceMap.end();)
		{
			CEffectInstance* pEffectInstance = i->second;

			const D3DMATRIX& gMatrix = pEffectInstance->GetGlobalMatrix();
			const float fDist = (v3Player.x - gMatrix._41) * (v3Player.x - gMatrix._41) + (v3Player.y - gMatrix._42) * (v3Player.y - gMatrix._42);
			const int iDistRatio = HermiteInterpolation(1, iUpdateFPS / 2, fDist / fMaxDist);

			if (m_iUpdateCount % iDistRatio == 0)
				pEffectInstance->Update();

			if (!pEffectInstance->isAlive())
			{
				i = m_EffectInstanceMap.erase(i);
				pEffectManager->DestroyUnsafeEffectInstance(pEffectInstance);
				continue;
			}

			if (pEffectInstance->isShow())
			{
				m_kVct_pkEftInstSort.emplace_back(pEffectInstance);
			}

			++i;
		}
	}

	++m_iUpdateCount;
	if (m_iUpdateCount > iUpdateFPS)
		m_iUpdateCount = 0;
}

float CArea::GetMaxLoadingDistanceSqr() const
{
	int peNum;
	float pfStart, pfEnd, pfFarClip;
	CPythonBackground::instance().GetDistanceSetInfo(&peNum, &pfStart, &pfEnd, &pfFarClip);

	// you need to get your value for exmaple from CPythonSystem or from whenever you want
	float fRatio = CPythonSystem::instance().GetLoadingDistance();

	// use one of the interpolation functions i provided
	return LinearInterpolation(pfStart * pfStart, pfFarClip * pfFarClip, fRatio);
}
#endif