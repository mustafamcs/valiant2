#include "stdafx.h"
#include "SoundManager2D.h"

#include "MaInstance.h"
void CSoundInstance2D::Pause() const
{
	if (m_pImpl)
		MaInstance_Pause(*m_pImpl);
}

void CSoundInstance2D::Resume() const
{
	if (m_pImpl)
		MaInstance_Resume(*m_pImpl);
}

void CSoundInstance2D::Stop()
{
	if (m_pImpl)
		MaInstance_Stop(*m_pImpl);
}

bool CSoundInstance2D::IsDone() const
{
	return !m_pImpl || MaInstance_IsDone(*m_pImpl);
}

void CSoundInstance2D::GetVolume(float& rfVolume) const
{
	rfVolume = (m_pImpl && m_pImpl->bInit) ? ma_sound_get_volume(&m_pImpl->sound) : 0.0f;
}

void CSoundInstance2D::SetVolume(float volume) const
{
	volume = max(0.0f, min(1.0f, volume));

	if (m_pImpl && m_pImpl->bInit)
		ma_sound_set_volume(&m_pImpl->sound, volume);
}

void CSoundInstance2D::Destroy()
{
	if (m_pImpl)
	{
		MaInstance_Release(*m_pImpl);
		delete m_pImpl;
		m_pImpl = NULL;
	}

	SAFE_RELEASE(m_pSoundData);
}

bool CSoundInstance2D::Initialize()
{
	if (!m_pImpl)
		m_pImpl = new SMaInstance;

	return true;
}

CSoundInstance2D::CSoundInstance2D()
	: m_pImpl(NULL),
	  m_pSoundData(NULL)
{
}

CSoundInstance2D::~CSoundInstance2D()
{
	Destroy();
}
bool CSoundInstance2D::SetSound(CSoundData* pSoundData)
{
	assert(m_pImpl != NULL && pSoundData != NULL);

	pSoundData->Get();
	bool bSet = MaInstance_Set(ms_pEngine, *m_pImpl, pSoundData, false);

	SAFE_RELEASE(m_pSoundData);

	if (!bSet)
	{
		pSoundData->Release();
		if (ms_pEngine)
			TraceError("CSoundInstance2D::SetSound - cannot play %s", pSoundData->GetFileName());
		return false;
	}

	m_pSoundData = pSoundData;
	return true;
}

void CSoundInstance2D::Play(int iLoopCount, DWORD dwPlayCycleTimeLimit) const
{
	if (m_pImpl)
		MaInstance_Play(ms_pEngine, *m_pImpl, iLoopCount);
}

void CSoundInstance2D::SetPosition(float x, float y, float z) const
{
	assert(!"must not call this method");
}

void CSoundInstance2D::SetOrientation(float x_face, float y_face, float z_face,
	float x_normal, float y_normal, float z_normal) const
{
	assert(!"must not call this method");
}

void CSoundInstance2D::SetVelocity(float fx, float fy, float fz, float fMagnitude) const
{
	assert(!"must not call this method");
}
