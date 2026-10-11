#include "StdAfx.h"
#include <io.h>
#include "../eterBase/CRC32.h"
#include "../eterBase/Timer.h"
#include "../eterBase/Stl.h"
#include "../EterFSLib/FileSystemIncl.hpp"

#include "ResourceManager.h"
#include "GrpImage.h"

constexpr long c_Deleting_Wait_Time = 30000;
constexpr long c_DeletingCountPerFrame = 30;
constexpr long c_Reference_Decrease_Wait_Time = 30000;

void CResourceManager::LoadStaticCache(const char* c_szFileName)
{
	CResource* pkRes{ GetResourcePointer(c_szFileName) };

	if (!pkRes)
	{
		Lognf(1, "CResourceManager::LoadStaticCache %s - FAILED", c_szFileName);
		return;
	}

	DWORD dwCacheKey{ GetCRC32(c_szFileName, strlen(c_szFileName)) };

	const auto f = m_pCacheMap.find(dwCacheKey);

	if (m_pCacheMap.end() != f)
		return;

	pkRes->AddReference();
	m_pCacheMap.insert(TResourcePointerMap::value_type(dwCacheKey, pkRes));
}

void CResourceManager::__DestroyCacheMap()
{
	for (auto &i = m_pCacheMap.begin(); i != m_pCacheMap.end(); ++i)
	{
		CResource* pResource = i->second;
		pResource->Release();
	}
	m_pCacheMap.clear();
}

void CResourceManager::__DestroyDeletingResourceMap()
{
	for (auto &i = m_ResourceDeletingMap.begin(); i != m_ResourceDeletingMap.end(); ++i)
		(i->first)->Clear();

	m_ResourceDeletingMap.clear();
}

void CResourceManager::__DestroyResourceMap()
{
	for (auto &i = m_pResMap.begin(); i != m_pResMap.end(); ++i)
	{
		CResource* pResource = i->second;
		pResource->Clear();
	}

	stl_wipe_second(m_pResMap);
}

void CResourceManager::DestroyDeletingList()
{
	CResource::SetDeleteImmediately(true);

	__DestroyCacheMap();
	__DestroyDeletingResourceMap();
}

void CResourceManager::Destroy()
{
	assert(m_ResourceDeletingMap.empty() && "CResourceManager::Destroy - YOU MUST CALL DestroyDeletingList");
	__DestroyResourceMap();
}

void CResourceManager::RegisterResourceNewFunctionPointer(const char* c_szFileExt, CResource* (*pNewFunc)(const char* c_szFileName))
{
	m_pResNewFuncMap[c_szFileExt] = pNewFunc;
}

void CResourceManager::RegisterResourceNewFunctionByTypePointer(int iType, CResource* (*pNewFunc) (const char* c_szFileName))
{
	assert(iType >= 0);
	m_pResNewFuncByTypeMap[iType] = pNewFunc;
}

CResource* CResourceManager::InsertResourcePointer(DWORD dwFileCRC, CResource* pResource)
{
	auto itor = m_pResMap.find(dwFileCRC);

	if (m_pResMap.end() != itor)
	{
		TraceError("CResource::InsertResourcePointer: %s is already registered\n", pResource->GetFileName());
		assert(!"CResource::InsertResourcePointer: Resource already resistered");
		delete pResource;
		return itor->second;
	}

	m_pResMap.insert(TResourcePointerMap::value_type(dwFileCRC, pResource));
	return pResource;
}

CResource* CResourceManager::GetTypeResourcePointer(const char* c_szFileName, int iType)
{
	if (!c_szFileName || !*c_szFileName)
	{
		assert(c_szFileName != nullptr && *c_szFileName != '\0');
		return nullptr;
	}

	const char* c_pszFile{};

	DWORD dwFileCRC{ __GetFileCRC(c_szFileName, &c_pszFile) };
	CResource* pResource{ FindResourcePointer(dwFileCRC) };

	if (pResource)
		return pResource;

	CResource* (*newFunc) (const char*) = nullptr;

	if (iType != -1)
	{
		TResourceNewFunctionByTypePointerMap::iterator f = m_pResNewFuncByTypeMap.find(iType);

		if (m_pResNewFuncByTypeMap.end() != f)
			newFunc = f->second;
	}
	else
	{
		const char* pcFileExt = strrchr(c_pszFile, '.');

		if (pcFileExt)
		{
			static char s_szFileExt[8 + 1];
			strncpy(s_szFileExt, pcFileExt + 1, 8);

			TResourceNewFunctionPointerMap::iterator f = m_pResNewFuncMap.find(s_szFileExt);

			if (m_pResNewFuncMap.end() != f)
				newFunc = f->second;
		}
	}

	if (!newFunc)
	{
		TraceError("ResourceManager::GetResourcePointer: NOT SUPPORT FILE %s", c_pszFile);
		return nullptr;
	}

	pResource = InsertResourcePointer(dwFileCRC, newFunc(c_pszFile));
	return pResource;
}

CResource* CResourceManager::GetResourcePointer(const char* c_szFileName)
{
	if (!c_szFileName || !*c_szFileName)
	{
		TraceError("CResourceManager::GetResourcePointer: filename error!");
		return nullptr;
	}

	const char* c_pszFile;
	DWORD dwFileCRC = __GetFileCRC(c_szFileName, &c_pszFile);
	CResource* pResource = FindResourcePointer(dwFileCRC);

	if (pResource)
		return pResource;

	const char* pcFileExt = strrchr(c_pszFile, '.');

#ifdef ENABLE_DEV_RESOURCE_DIAGNOSTICS
	if (!IsFileExist(c_szFileName))
	{
		if (pcFileExt == NULL || (stricmp(pcFileExt, ".fnt") != 0))
		{
			TraceError("CResourceManager::GetResourcePointer: File not exist %s", c_szFileName);
		}
	}
#endif

	CResource* (*newFunc) (const char*) = nullptr;

	if (pcFileExt)
	{
		static char s_szFileExt[8 + 1];
		strncpy(s_szFileExt, pcFileExt + 1, 8);

		TResourceNewFunctionPointerMap::iterator f = m_pResNewFuncMap.find(s_szFileExt);

		if (m_pResNewFuncMap.end() != f)
			newFunc = f->second;
	}

	if (!newFunc)
	{
		TraceError("ResourceManager::GetResourcePointer: NOT SUPPORT FILE %s", c_pszFile);
		return NULL;
	}

	pResource = InsertResourcePointer(dwFileCRC, newFunc(c_pszFile));
	return pResource;
}

CResource* CResourceManager::FindResourcePointer(DWORD dwFileCRC)
{
	auto itor = m_pResMap.find(dwFileCRC);

	if (m_pResMap.end() == itor)
		return NULL;

	return itor->second;
}

bool CResourceManager::isResourcePointerData(DWORD dwFileCRC)
{
	auto itor = m_pResMap.find(dwFileCRC);

	if (m_pResMap.end() == itor)
		return NULL;

	return (itor->second)->IsData();
}

DWORD CResourceManager::__GetFileCRC(const char* c_szFileName, const char** c_ppszLowerFileName)
{
	static char s_szFullPathFileName[MAX_PATH]{};
	const char* src{ c_szFileName };
	char* dst{ s_szFullPathFileName };
	int	len{};

	while (src[len])
	{
		if (src[len] == '/')
			dst[len] = '\\';
		else
			dst[len] = (char)korean_tolower(src[len]);

		++len;
	}

	dst[len] = '\0';

	if (c_ppszLowerFileName)
		*c_ppszLowerFileName = &s_szFullPathFileName[0];

	return (GetCRC32(s_szFullPathFileName, len));
}

typedef struct SDumpData
{
	const char* filename;
	float			KB;
	DWORD			cost;
} TDumpData;

bool DumpKBCompare(const TDumpData& lhs, const TDumpData& rhs)
{
	return (lhs.KB > rhs.KB) ? true : false;
}

bool DumpCostCompare(const TDumpData& lhs, const TDumpData& rhs)
{
	return (lhs.cost > rhs.cost) ? true : false;
}

struct FDumpPrint
{
	FILE* m_fp;
	static float m_totalKB;

	void operator () (TDumpData& data)
	{
		m_totalKB += data.KB;
		fprintf(m_fp, "%6.1f %s\n", data.KB, data.filename);
	}
};

float FDumpPrint::m_totalKB;

struct FDumpCostPrint
{
	FILE* m_fp;

	void operator() (TDumpData& data)
	{
		fprintf(m_fp, "%-4d %s\n", data.cost, data.filename);
	}
};

void CResourceManager::DumpFileListToTextFile(const char* c_szFileName)
{
	std::vector<TDumpData> dumpVector;

	for (auto &i = m_pResMap.begin(); i != m_pResMap.end(); ++i)
	{
		CResource* pResource = i->second;
		TDumpData data{};

		if (pResource->IsEmpty())
			continue;

		data.filename = pResource->GetFileName();

		int filesize{};

		const char* ext = strrchr(data.filename, '.');

		if (pResource->IsType(CGraphicImage::Type()) && strnicmp(ext, ".sub", 4))
			filesize = ((CGraphicImage*)pResource)->GetWidth() * ((CGraphicImage*)pResource)->GetHeight() * 4;
		else
		{
			FILE* fp2 = fopen(data.filename, "rb");

			if (fp2)
			{
				fseek(fp2, 0L, SEEK_END);
				filesize = ftell(fp2);
				fclose(fp2);
			}
			else
				filesize = 0;
		}

		data.KB = (float)filesize / (float)1024;
		data.cost = pResource->GetLoadCostMilliSecond();

		dumpVector.push_back(data);
	}

	FILE* fp = fopen(c_szFileName, "w");

	if (fp)
	{
		std::sort(dumpVector.begin(), dumpVector.end(), DumpKBCompare);

		FDumpPrint DumpPrint;
		DumpPrint.m_fp = fp;
		DumpPrint.m_totalKB = 0;

		std::for_each(dumpVector.begin(), dumpVector.end(), DumpPrint);
		fprintf(fp, "total: %.2fmb", DumpPrint.m_totalKB / 1024.0f);

		FDumpCostPrint DumpCostPrint;
		DumpCostPrint.m_fp = fp;

		std::sort(dumpVector.begin(), dumpVector.end(), DumpCostCompare);
		std::for_each(dumpVector.begin(), dumpVector.end(), DumpCostPrint);
		fprintf(fp, "total: %.2fmb", DumpPrint.m_totalKB / 1024.0f);

		fclose(fp);
	}
}

bool CResourceManager::IsFileExist(const char* c_szFileName)
{
	return FileSystem::FileSystemManager::Instance().DoesFileExist(c_szFileName);
}

void CResourceManager::Update()
{
	DWORD CurrentTime{ ELTimer_GetMSec() };
	CResource* pResource{nullptr};
	int Count{};

	auto itor = m_ResourceDeletingMap.begin();

	while (itor != m_ResourceDeletingMap.end())
	{
		pResource = itor->first;

		if (CurrentTime >= itor->second)
		{
			if (pResource->canDestroy())
			{
				pResource->Clear();
			}

			itor = m_ResourceDeletingMap.erase(itor);

			if (++Count >= c_DeletingCountPerFrame)
				break;
		}
		else
			++itor;
	}

}

void CResourceManager::ReserveDeletingResource(CResource* pResource)
{
	DWORD dwCurrentTime{ ELTimer_GetMSec() };
	m_ResourceDeletingMap.insert(TResourceDeletingMap::value_type(pResource, dwCurrentTime + c_Deleting_Wait_Time));
}

CResourceManager::CResourceManager() = default;

CResourceManager::~CResourceManager()
{
	Destroy();
}