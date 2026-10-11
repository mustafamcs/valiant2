#ifndef __MILESLIB_MAINSTANCE_H__
#define __MILESLIB_MAINSTANCE_H__

// Only for MilesLib .cpp files: pulls in miniaudio.h.
#include <miniaudio.h>
#include "SoundData.h"

struct SMaInstance
{
	ma_audio_buffer_ref ref;
	ma_sound sound;
	bool bInit;
	bool bPaused;

	SMaInstance()
		: bInit(false),
		  bPaused(false)
	{
	}
};

inline void MaInstance_Release(SMaInstance &r)
{
	if (r.bInit)
	{
		ma_sound_uninit(&r.sound);
		ma_audio_buffer_ref_uninit(&r.ref);
		r.bInit = false;
	}

	r.bPaused = false;
}

inline bool MaInstance_Set(ma_engine *pEngine, SMaInstance &r, CSoundData *pData, bool bSpatial)
{
	MaInstance_Release(r);

	if (!pEngine || !pData || !pData->GetPcm())
		return false;

	if (ma_audio_buffer_ref_init(ma_format_s16, pData->GetChannels(), pData->GetPcm(), pData->GetFrameCount(), &r.ref) != MA_SUCCESS)
		return false;

	r.ref.sampleRate = pData->GetSampleRate();

	if (ma_sound_init_from_data_source(pEngine, &r.ref, bSpatial ? 0 : MA_SOUND_FLAG_NO_SPATIALIZATION, NULL, &r.sound) != MA_SUCCESS)
	{
		ma_audio_buffer_ref_uninit(&r.ref);
		return false;
	}

	r.bInit = true;
	return true;
}

// Miles loop count: 0 = forever, n = play n times.
inline void MaInstance_Play(ma_engine *pEngine, SMaInstance &r, int iLoopCount)
{
	if (!r.bInit)
		return;

	ma_sound_stop(&r.sound);
	ma_sound_seek_to_pcm_frame(&r.sound, 0);
	ma_sound_set_stop_time_in_pcm_frames(&r.sound, ~(ma_uint64)0);
	ma_sound_set_looping(&r.sound, iLoopCount != 1 ? MA_TRUE : MA_FALSE);

	if (iLoopCount > 1)
	{
		ma_uint64 ullFrames = 0;
		ma_sound_get_length_in_pcm_frames(&r.sound, &ullFrames);

		const ma_uint32 uSourceRate = r.ref.sampleRate ? r.ref.sampleRate : ma_engine_get_sample_rate(pEngine);
		const ma_uint64 ullEngineFrames = ullFrames * ma_engine_get_sample_rate(pEngine) / uSourceRate;
		ma_sound_set_stop_time_in_pcm_frames(&r.sound, ma_engine_get_time_in_pcm_frames(pEngine) + ullEngineFrames * iLoopCount);
	}

	r.bPaused = false;
	ma_sound_start(&r.sound);
}

inline void MaInstance_Pause(SMaInstance &r)
{
	if (!r.bInit || !ma_sound_is_playing(&r.sound))
		return;

	ma_sound_stop(&r.sound);
	r.bPaused = true;
}

inline void MaInstance_Resume(SMaInstance &r)
{
	if (!r.bInit || !r.bPaused)
		return;

	r.bPaused = false;
	ma_sound_start(&r.sound);
}

inline void MaInstance_Stop(SMaInstance &r)
{
	if (!r.bInit)
		return;

	ma_sound_stop(&r.sound);
	r.bPaused = false;
}

inline bool MaInstance_IsDone(const SMaInstance &r)
{
	if (!r.bInit)
		return true;

	return !r.bPaused && !ma_sound_is_playing(&r.sound);
}

#endif
