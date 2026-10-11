#include "Stdafx.h"
#include "SoundBase.h"

#define MA_NO_ENCODING
// COINIT_APARTMENTTHREADED: the main thread already uses COM for DirectShow/D3D.
#define MA_COINIT_VALUE 2
#define MINIAUDIO_IMPLEMENTATION
#include <miniaudio.h>

ma_engine* CSoundBase::ms_pEngine = NULL;
TSoundDataMap CSoundBase::ms_dataMap;
bool CSoundBase::ms_bInitialized = false;
int CSoundBase::ms_iRefCount = 0;

CSoundBase::CSoundBase()
{
}

CSoundBase::~CSoundBase()
{
}

void CSoundBase::Destroy()
{
	if (ms_iRefCount > 1)
	{
		--ms_iRefCount;
		return;
	}

	ms_iRefCount = 0;

	if (!ms_dataMap.empty())
	{
		TSoundDataMap::iterator i;
		for (i = ms_dataMap.begin(); i != ms_dataMap.end(); ++i)
		{
			CSoundData* pSoundData = i->second;
			delete pSoundData;
		}

		ms_dataMap.clear();
	}

	if (ms_pEngine)
	{
		ma_engine_uninit(ms_pEngine);
		delete ms_pEngine;
		ms_pEngine = NULL;
	}
}

void CSoundBase::Initialize()
{
	++ms_iRefCount;

	if (ms_iRefCount > 1)
		return;

	ms_pEngine = new ma_engine;
	if (ma_engine_init(NULL, ms_pEngine) != MA_SUCCESS)
	{
		TraceError("CSoundBase::Initialize - ma_engine_init failed, sound disabled");
		delete ms_pEngine;
		ms_pEngine = NULL;
	}
	ms_dataMap.clear();
}

DWORD CSoundBase::GetFileCRC(const char* filename)
{
	return GetCRC32(filename, strlen(filename));
}

CSoundData* CSoundBase::AddFile(DWORD dwFileCRC, const char* filename)
{
	CSoundData* pSoundData = new CSoundData;
	pSoundData->Assign(filename);
	ms_dataMap.insert(TSoundDataMap::value_type(dwFileCRC, pSoundData));
	return pSoundData;
}
