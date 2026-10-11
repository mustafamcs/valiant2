#pragma once

#include "GrpImage.h"
#include "GrpIndexBuffer.h"
#include "GrpVertexBufferDynamic.h"
#include "Pool.h"
#include "../Controls.h"

class CGraphicImageInstance
{
public:
	static DWORD Type();
	BOOL IsType(DWORD dwType);

public:
	CGraphicImageInstance();
	virtual ~CGraphicImageInstance();

	void Destroy();
	void Render(
#if defined(ENABLE_CLIP_MASK)
	RECT* pClipRect = NULL
#endif
	);

	void SetDiffuseColor(float fr, float fg, float fb, float fa);
	void SetPosition(float fx, float fy);
	void SetScale(float fx, float fy);
	void SetImagePointer(CGraphicImage* pImage);
	void ReloadImagePointer(CGraphicImage* pImage);
	bool IsEmpty() const;

	int GetWidth();
	int GetHeight();

	CGraphicTexture* GetTexturePointer();
	const CGraphicTexture& GetTextureReference() const;
	CGraphicImage* GetGraphicImagePointer();

	bool operator == (const CGraphicImageInstance& rhs) const;

#ifdef ENABLE_DUNGEON_MODULES
	void RenderCoolTime(float fCoolTime);
	virtual void OnRenderCoolTime(float fCoolTime);
#endif

protected:
	void Initialize();
	virtual void OnRender(
#if defined(ENABLE_CLIP_MASK)
	RECT* pClipRect
#endif
	);
	virtual void OnSetImagePointer();
	virtual BOOL OnIsType(DWORD dwType);

protected:
	D3DXCOLOR m_DiffuseColor;
	D3DXVECTOR2 m_v2Position;
	D3DXVECTOR2 m_v2Scale; // Enabled for ENABLE_RENDER_TARGET

	CGraphicImage::TRef m_roImage;

public:
	static void CreateSystem(UINT uCapacity);
	static void DestroySystem();

	static CGraphicImageInstance* New();
	static void Delete(CGraphicImageInstance* pkImgInst);

	static CMemoryPoolNew<CGraphicImageInstance>		ms_kPool;
};
