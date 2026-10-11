#ifndef __MILESLIB_CSOUNDDATA_H__
#define __MILESLIB_CSOUNDDATA_H__

#include "../Controls.h"
#include <vector>
#include "../eterBase/MappedFile.h"

class CSoundData
{
public:
	enum
	{
		FLAG_DATA_SIZE = 1,
		SOUND_FILE_MAX_NUM = 5,
	};

public:
	static void SetPackMode();

	CSoundData();
	virtual ~CSoundData();

	void Assign(const char *filename);
	LPVOID Get();
	ULONG GetSize();
	void Release();
	DWORD GetAccessTime();
	const char *GetFileName();

	void SetPlayTime(DWORD dwPlayTime);
	DWORD GetPlayTime();

	// Dosya bir kez 16 bit PCM'e cozulur; ornekler bu tamponu paylasir.
	const short *GetPcm() const;
	unsigned __int64 GetFrameCount() const;
	DWORD GetChannels() const;
	DWORD GetSampleRate() const;

	static bool LoadFileData(const char *filename, std::vector<BYTE> &rData);

protected:
	bool ReadFromDisk();
	void Destroy();

protected:
	char m_filename[128];
	int m_iRefCount;
	DWORD m_dwAccessTime;
	DWORD m_dwPlayTime;
	ULONG m_size;
	LPVOID m_data;
	long m_flag;
	bool m_assigned;

	std::vector<short> m_pcm;
	DWORD m_channels;
	DWORD m_sampleRate;
	bool m_bReadFailed;

	static bool ms_bPackMode;
};

#endif
