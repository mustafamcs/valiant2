#include "stdafx.h"
#include "SoundManager3D.h"
#include "../eterBase/Timer.h"

#include "MaInstance.h"
void CSoundInstance3D::Pause() const
{
	if (m_pImpl)
		MaInstance_Pause(*m_pImpl);
}

void CSoundInstance3D::Resume() const
{
	if (m_pImpl)
		MaInstance_Resume(*m_pImpl);
}

void CSoundInstance3D::Stop()
{
	if (m_pImpl)
		MaInstance_Stop(*m_pImpl);
}

bool CSoundInstance3D::IsDone() const
{
	return !m_pImpl || MaInstance_IsDone(*m_pImpl);
}

void CSoundInstance3D::GetVolume(float& rfVolume) const
{
	rfVolume = (m_pImpl && m_pImpl->bInit) ? ma_sound_get_volume(&m_pImpl->sound) : 0.0f;
}

void CSoundInstance3D::SetVolume(float volume) const
{
	volume = max(0.0f, min(1.0f, volume));

	if (m_pImpl && m_pImpl->bInit)
		ma_sound_set_volume(&m_pImpl->sound, volume);
}

void CSoundInstance3D::Destroy()
{
	if (m_pImpl)
	{
		MaInstance_Release(*m_pImpl);
		delete m_pImpl;
		m_pImpl = NULL;
	}

	SAFE_RELEASE(m_pSoundData);
}

bool CSoundInstance3D::Initialize()
{
	if (!m_pImpl)
		m_pImpl = new SMaInstance;

	return true;
}

CSoundInstance3D::CSoundInstance3D()
	: m_pImpl(NULL),
	  m_pSoundData(NULL)
{
}

CSoundInstance3D::~CSoundInstance3D()
{
	Destroy();
}
bool CSoundInstance3D::SetSound(CSoundData* pSoundData)
{
	assert(m_pImpl != NULL && pSoundData != NULL);

	pSoundData->Get();
	bool bSet = MaInstance_Set(ms_pEngine, *m_pImpl, pSoundData, true);

	SAFE_RELEASE(m_pSoundData);

	if (!bSet)
	{
		pSoundData->Release();
		if (ms_pEngine)
			TraceError("CSoundInstance3D::SetSound - cannot play %s", pSoundData->GetFileName());
		return false;
	}

	m_pSoundData = pSoundData;

	// Miles 3D sample defaults: min distance 1, max distance 200, inverse falloff, no doppler.
	ma_sound* pSound = &m_pImpl->sound;
	ma_sound_set_attenuation_model(pSound, ma_attenuation_model_inverse);
	ma_sound_set_min_distance(pSound, 1.0f);
	ma_sound_set_max_distance(pSound, 200.0f);
	ma_sound_set_rolloff(pSound, 1.0f);
	ma_sound_set_doppler_factor(pSound, 0.0f);
	ma_sound_set_position(pSound, 0.0f, 0.0f, 0.0f);
	return true;
}

void CSoundInstance3D::Play(int iLoopCount, DWORD dwPlayCycleTimeLimit) const
{
	if (!m_pSoundData || !m_pImpl)
		return;

	DWORD dwCurTime = ELTimer_GetMSec();

	if (dwCurTime - m_pSoundData->GetPlayTime() < dwPlayCycleTimeLimit)
		return;

	m_pSoundData->SetPlayTime(dwCurTime);

	MaInstance_Play(ms_pEngine, *m_pImpl, iLoopCount);
}

void CSoundInstance3D::SetPosition(float x, float y, float z) const
{
	// Miles is left-handed and got -z; miniaudio is right-handed, so the game z goes in unchanged.
	if (m_pImpl && m_pImpl->bInit)
		ma_sound_set_position(&m_pImpl->sound, x, y, z);
}

void CSoundInstance3D::SetOrientation(float x_face, float y_face, float z_face,
	float x_normal, float y_normal, float z_normal) const
{
	assert(!" CSoundInstance3D::SetOrientation - Don't use this function");
}

void CSoundInstance3D::SetVelocity(float fDistanceX, float fDistanceY, float fDistanceZ, float fNagnitude) const
{
}

void CSoundInstance3D::UpdatePosition(float fElapsedTime)
{
}
