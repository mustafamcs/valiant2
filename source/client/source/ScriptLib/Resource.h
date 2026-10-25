#pragma once

#include "../EffectLib/StdAfx.h"
#include "../eterlib/Resource.h"
#include "../eterlib/ResourceManager.h"
#include "../eterlib/GrpImage.h"

enum EResourceTypes
{
	RES_TYPE_UNKNOWN,
};

class CPythonResource : public CSingleton<CPythonResource>
{
public:
	CPythonResource();
	virtual ~CPythonResource();

	void Destroy();

	void DumpFileList(const char* c_szFileName);
	void PinPhaseChangeResources();

protected:
	CResourceManager m_resManager;
	std::vector<CGraphicImage::TRef> m_pinnedResources;
};
