#include "StdAfx.h"
#include "MapBase.h"

CMapBase::CMapBase()
{
	Clear();
}

CMapBase::~CMapBase()
{
	Clear();
}

void CMapBase::Clear()
{
	m_strName = "";
	m_eType = MAPTYPE_INVALID;
	mc_pEnvironmentData = NULL;
	Leave();
}

bool CMapBase::Enter()
{
	m_bReady = true;
	return true;
}

bool CMapBase::Leave()
{
	m_bReady = false;
	return true;
}

void CMapBase::SetEnvironmentDataPtr(const TEnvironmentData* c_pEnvironmentData)
{
	mc_pEnvironmentData = c_pEnvironmentData;
	OnSetEnvironmentDataPtr();
}

void CMapBase::ResetEnvironmentDataPtr(const TEnvironmentData* c_pEnvironmentData)
{
	mc_pEnvironmentData = c_pEnvironmentData;
	OnResetEnvironmentDataPtr();
}

void CMapBase::Render()
{
	if (IsReady())
		OnRender();
}

bool CMapBase::LoadProperty()
{
	std::string strFileName = GetName() + "\\MapProperty.txt";

	CTokenVectorMap stTokenVectorMap;

	if (!LoadMultipleTextData(strFileName.c_str(), stTokenVectorMap))
	{
		TraceError("CMapBase::LoadProperty(FileName=%s) - LoadMultipleTextData ERROR File not found.", strFileName.c_str());
		return false;
	}

	const auto itScriptType = stTokenVectorMap.find("scripttype");
	const auto itMapType = stTokenVectorMap.find("maptype");

	if (itScriptType == stTokenVectorMap.end())
	{
		TraceError("CMapBase::LoadProperty(FileName=%s) - FIND 'scripttype' - FAILED", strFileName.c_str());
		return false;
	}

	if (itMapType == stTokenVectorMap.end())
	{
		TraceError("CMapBase::LoadProperty(FileName=%s) - FIND 'maptype' - FAILED", strFileName.c_str());
		return false;
	}

	std::string_view c_rstrType = itScriptType->second[0];
	std::string_view c_rstrMapType = itMapType->second[0];

	m_strParentMapName = stTokenVectorMap["parentmapname"].empty() ? "" : stTokenVectorMap["parentmapname"][0];

	if (c_rstrType != "MapProperty")
	{
		TraceError("CMapBase::LoadProperty(FileName=%s) - Resourse Type ERROR", strFileName.c_str());
		return false;
	}

	if (c_rstrMapType == "Indoor")
		SetType(MAPTYPE_INDOOR);
	else if (c_rstrMapType == "Outdoor")
		SetType(MAPTYPE_OUTDOOR);
	else if (c_rstrMapType == "Invalid")
		SetType(MAPTYPE_OUTDOOR);

	return true;
}