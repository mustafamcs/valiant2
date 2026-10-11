#pragma once

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
#include "Packet.h"

class CPythonAcce : public CSingleton<CPythonAcce>
{
public:
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t	dwPrice;
#else
	DWORD	dwPrice;
#endif
	typedef std::vector<TAcceMaterial> TAcceMaterials;

public:
	CPythonAcce();
	virtual ~CPythonAcce();

	void	Clear();
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	void	AddMaterial(int64_t dwRefPrice, BYTE bPos, TItemPos tPos);
#else
	void	AddMaterial(DWORD dwRefPrice, BYTE bPos, TItemPos tPos);
#endif
	void	AddResult(DWORD dwItemVnum, DWORD dwMinAbs, DWORD dwMaxAbs);
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	void	RemoveMaterial(int64_t dwRefPrice, BYTE bPos);
#else
	void	RemoveMaterial(DWORD dwRefPrice, BYTE bPos);
#endif
#ifdef ENABLE_EXTENDED_YANG_LIMIT
	int64_t	GetPrice() { return dwPrice; }
#else
	DWORD	GetPrice() { return dwPrice; }
#endif
	bool	GetAttachedItem(BYTE bPos, BYTE& bHere, WORD& wCell);
	void	GetResultItem(DWORD& dwItemVnum, DWORD& dwMinAbs, DWORD& dwMaxAbs);

protected:
	TAcceResult	m_vAcceResult;
	TAcceMaterials	m_vAcceMaterials;
};
#endif
