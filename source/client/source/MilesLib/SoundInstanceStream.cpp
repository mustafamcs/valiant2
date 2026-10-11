#include "stdafx.h"
#include "SoundInstance.h"

#include <miniaudio.h>

struct SMaStream
{
	std::vector<BYTE> file;
	ma_decoder decoder;
	ma_sound sound;
	bool bDecoder;
	bool bSound;
	bool bPaused;

	SMaStream()
		: bDecoder(false),
		  bSound(false),
		  bPaused(false)
	{
	}
};

CSoundInstanceStream::CSoundInstanceStream()
	: m_pImpl(NULL)
{
}

CSoundInstanceStream::~CSoundInstanceStream()
{
	Destroy();
}

void CSoundInstanceStream::Destroy()
{
	if (!m_pImpl)
		return;

	if (m_pImpl->bSound)
		ma_sound_uninit(&m_pImpl->sound);

	if (m_pImpl->bDecoder)
		ma_decoder_uninit(&m_pImpl->decoder);

	delete m_pImpl;
	m_pImpl = NULL;
}

bool CSoundInstanceStream::Initialize()
{
	return true;
}

bool CSoundInstanceStream::Open(const char* c_szFileName)
{
	Destroy();

	if (!ms_pEngine)
		return false;

	SMaStream* pStream = new SMaStream;

	if (!CSoundData::LoadFileData(c_szFileName, pStream->file))
	{
		delete pStream;
		return false;
	}

	ma_decoder_config config = ma_decoder_config_init(ma_format_f32, 0, 0);
	if (ma_decoder_init_memory(&pStream->file[0], pStream->file.size(), &config, &pStream->decoder) != MA_SUCCESS)
	{
		delete pStream;
		return false;
	}

	pStream->bDecoder = true;

	if (ma_sound_init_from_data_source(ms_pEngine, &pStream->decoder, MA_SOUND_FLAG_NO_SPATIALIZATION, NULL, &pStream->sound) != MA_SUCCESS)
	{
		ma_decoder_uninit(&pStream->decoder);
		delete pStream;
		return false;
	}

	pStream->bSound = true;
	m_pImpl = pStream;
	return true;
}

bool CSoundInstanceStream::IsDone() const
{
	if (!IsData())
		return true;

	return !m_pImpl->bPaused && !ma_sound_is_playing(&m_pImpl->sound);
}

bool CSoundInstanceStream::IsData() const
{
	return m_pImpl && m_pImpl->bSound;
}

void CSoundInstanceStream::Play(int count, DWORD dwPlayCycleTimeLimit) const
{
	if (!IsData())
		return;

	ma_sound_stop(&m_pImpl->sound);
	ma_sound_seek_to_pcm_frame(&m_pImpl->sound, 0);
	ma_sound_set_looping(&m_pImpl->sound, count != 1 ? MA_TRUE : MA_FALSE);
	m_pImpl->bPaused = false;
	ma_sound_start(&m_pImpl->sound);
}

void CSoundInstanceStream::Pause() const
{
	if (!IsData() || !ma_sound_is_playing(&m_pImpl->sound))
		return;

	ma_sound_stop(&m_pImpl->sound);
	m_pImpl->bPaused = true;
}

void CSoundInstanceStream::Resume() const
{
	if (!IsData() || !m_pImpl->bPaused)
		return;

	m_pImpl->bPaused = false;
	ma_sound_start(&m_pImpl->sound);
}

void CSoundInstanceStream::Stop()
{
	Destroy();
}

void CSoundInstanceStream::GetVolume(float& rfVolume) const
{
	if (!IsData())
		return;

	rfVolume = ma_sound_get_volume(&m_pImpl->sound);
}

void CSoundInstanceStream::SetVolume(float volume) const
{
	if (!IsData())
		return;

	volume = max(0.0f, min(1.0f, volume));
	ma_sound_set_volume(&m_pImpl->sound, volume);
}

bool CSoundInstanceStream::SetSound(CSoundData* pSound)
{
	return true;
}

void CSoundInstanceStream::SetPosition(float x, float y, float z) const
{
}

void CSoundInstanceStream::SetOrientation(float x_face, float y_face, float z_face,
	float x_normal, float y_normal, float z_normal) const
{
}

void CSoundInstanceStream::SetVelocity(float fx, float fy, float fz, float fMagnitude) const
{
}
