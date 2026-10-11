#include "StdAfx.h"
#include "SoundData.h"

#include "../EterFSLib/FileSystemManager.hpp"
#include "../eterBase/Timer.h"

#include <miniaudio.h>

bool CSoundData::ms_bPackMode = false;

const char *CSoundData::GetFileName()
{
	return m_filename;
}

void CSoundData::Assign(const char *filename)
{
	assert(m_assigned == false);

	strncpy(m_filename, filename, sizeof(m_filename) - 1);
	m_assigned = true;
}

LPVOID CSoundData::Get()
{
	++m_iRefCount;
	m_dwAccessTime = ELTimer_GetMSec();

	if (m_pcm.empty() && !m_bReadFailed)
		ReadFromDisk();

	return m_pcm.empty() ? NULL : &m_pcm[0];
}

ULONG CSoundData::GetSize()
{
	return (ULONG)(m_pcm.size() * sizeof(short));
}

void CSoundData::Release()
{
	--m_iRefCount;
}

DWORD CSoundData::GetPlayTime()
{
	return m_dwPlayTime;
}

void CSoundData::SetPlayTime(DWORD dwPlayTime)
{
	m_dwPlayTime = dwPlayTime;
}

DWORD CSoundData::GetAccessTime()
{
	return m_dwAccessTime;
}

const short *CSoundData::GetPcm() const
{
	return m_pcm.empty() ? NULL : &m_pcm[0];
}

unsigned __int64 CSoundData::GetFrameCount() const
{
	return m_channels ? m_pcm.size() / m_channels : 0;
}

DWORD CSoundData::GetChannels() const
{
	return m_channels;
}

DWORD CSoundData::GetSampleRate() const
{
	return m_sampleRate;
}

bool CSoundData::LoadFileData(const char *filename, std::vector<BYTE> &rData)
{
	rData.clear();

	std::unique_ptr<DataBuffer> packedData = FileSystem::FileSystemManager::Instance().Get(filename);
	if (packedData && !packedData->is_null())
	{
		const BYTE* pBytes = packedData->get_data<BYTE>();
		rData.assign(pBytes, pBytes + packedData->get_size());
		return !rData.empty();
	}

	FILE *fp = fopen(filename, "rb");
	if (!fp)
		return false;

	fseek(fp, 0, SEEK_END);
	long lSize = ftell(fp);
	fseek(fp, 0, SEEK_SET);

	if (lSize > 0)
	{
		rData.resize(lSize);
		if (fread(&rData[0], 1, lSize, fp) != (size_t)lSize)
			rData.clear();
	}

	fclose(fp);
	return !rData.empty();
}

bool CSoundData::ReadFromDisk()
{
	assert(m_assigned == true);

	std::vector<BYTE> file;
	if (!LoadFileData(m_filename, file))
	{
		TraceError("CSoundData::ReadFromDisk - file not found: %s", m_filename);
		m_bReadFailed = true;
		return false;
	}

	ma_decoder_config config = ma_decoder_config_init(ma_format_s16, 0, 0);
	ma_decoder decoder;

	if (ma_decoder_init_memory(&file[0], file.size(), &config, &decoder) != MA_SUCCESS)
	{
		TraceError("CSoundData::ReadFromDisk - decoder failed: %s", m_filename);
		m_bReadFailed = true;
		return false;
	}

	m_channels = decoder.outputChannels;
	m_sampleRate = decoder.outputSampleRate;

	ma_uint64 ullTotal = 0;
	if (ma_decoder_get_length_in_pcm_frames(&decoder, &ullTotal) == MA_SUCCESS && ullTotal > 0)
		m_pcm.reserve((size_t)(ullTotal * m_channels));

	const ma_uint64 CHUNK_FRAMES = 4096;
	std::vector<short> chunk((size_t)(CHUNK_FRAMES * m_channels));

	for (;;)
	{
		ma_uint64 ullRead = 0;
		ma_result result = ma_decoder_read_pcm_frames(&decoder, &chunk[0], CHUNK_FRAMES, &ullRead);

		if (ullRead > 0)
			m_pcm.insert(m_pcm.end(), chunk.begin(), chunk.begin() + (size_t)(ullRead * m_channels));

		if (result != MA_SUCCESS || ullRead < CHUNK_FRAMES)
			break;
	}

	ma_decoder_uninit(&decoder);

	if (m_pcm.empty())
	{
		m_bReadFailed = true;
		return false;
	}

	return true;
}

void CSoundData::Destroy()
{
	std::vector<short>().swap(m_pcm);
	m_channels = 0;
	m_sampleRate = 0;
}

CSoundData::CSoundData()
	: m_iRefCount(0),
	  m_dwPlayTime(0),
	  m_size(0),
	  m_data(NULL),
	  m_flag(0),
	  m_assigned(false),
	  m_channels(0),
	  m_sampleRate(0),
	  m_bReadFailed(false)
{
	m_filename[0] = '\0';
	m_dwAccessTime = ELTimer_GetMSec();
}

CSoundData::~CSoundData()
{
	Destroy();
}

void CSoundData::SetPackMode()
{
	ms_bPackMode = true;
}
