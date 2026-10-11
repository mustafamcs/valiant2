#include "Stdafx.h"
#include "SoundManager3D.h"
#include <miniaudio.h>

CSoundManager3D::CSoundManager3D()
{
	m_bInit = false;
}

CSoundManager3D::~CSoundManager3D()
{
}

bool CSoundManager3D::Initialize()
{
	CSoundBase::Initialize();

	if (m_bInit)
		return true;

	if (!ms_pEngine)
	{
		CSoundBase::Destroy();
		return false;
	}

	SetListenerPosition(0.0f, 0.0f, 0.0f);

	for (int i = 0; i < INSTANCE_MAX_COUNT; ++i)
	{
		m_Instances[i].Initialize();
		m_bLockingFlag[i] = false;
	}

	m_bInit = true;
	return true;
}

void CSoundManager3D::Destroy()
{
	if (!m_bInit)
		return;

	for (int i = 0; i < INSTANCE_MAX_COUNT; ++i)
		m_Instances[i].Destroy();


	CSoundBase::Destroy();
	m_bInit = false;
}

void CSoundManager3D::SetListenerDirection(float fxDir, float fyDir, float fzDir, float fxUp, float fyUp, float fzUp)
{
	if (!ms_pEngine)
		return;
	ma_engine_listener_set_direction(ms_pEngine, 0, fxDir, fyDir, fzDir);
	ma_engine_listener_set_world_up(ms_pEngine, 0, fxUp, fyUp, fzUp);
}

void CSoundManager3D::SetListenerPosition(float fX, float fY, float fZ)
{
	if (!ms_pEngine)
		return;
	ma_engine_listener_set_position(ms_pEngine, 0, fX, fY, fZ);
}

void CSoundManager3D::SetListenerVelocity(float fDistanceX, float fDistanceY, float fDistanceZ, float fNagnitude)
{
}

int CSoundManager3D::SetInstance(const char* c_pszFileName)
{
	DWORD dwFileCRC = GetFileCRC(c_pszFileName);
	TSoundDataMap::iterator itor = ms_dataMap.find(dwFileCRC);

	CSoundData* pkSoundData;

	if (itor == ms_dataMap.end())
		pkSoundData = AddFile(dwFileCRC, c_pszFileName); // CSoundBase::AddFile
	else
		pkSoundData = itor->second;

	assert(pkSoundData != NULL);

	static DWORD k = 0;

	DWORD start = k++;
	DWORD end = start + INSTANCE_MAX_COUNT;

	while (start < end)
	{
		CSoundInstance3D* pkInst = &m_Instances[start % INSTANCE_MAX_COUNT];

		if (pkInst->IsDone())
		{
			if (!pkInst->SetSound(pkSoundData))
			{
				TraceError("CSoundManager3D::GetInstance (filename: %s)", c_pszFileName);
				return -1;
			}

			return (start % INSTANCE_MAX_COUNT);
		}

		++start;

		if (start > 50000)
		{
			start = 0;
			return -1;
		}
	}

	return -1;
}

ISoundInstance* CSoundManager3D::GetInstance(DWORD dwIndex)
{
	if (dwIndex >= INSTANCE_MAX_COUNT)
	{
		assert(dwIndex < INSTANCE_MAX_COUNT);
		return NULL;
	}
	return &m_Instances[dwIndex];
}

__forceinline bool CSoundManager3D::IsValidInstanceIndex(int iIndex)
{
	if (iIndex >= 0 && iIndex < INSTANCE_MAX_COUNT)
		return true;

	return false;
}

void CSoundManager3D::Lock(int iIndex)
{
	if (!IsValidInstanceIndex(iIndex))
		return;

	m_bLockingFlag[iIndex] = true;
}

void CSoundManager3D::Unlock(int iIndex)
{
	if (!IsValidInstanceIndex(iIndex))
		return;

	m_bLockingFlag[iIndex] = false;
}
