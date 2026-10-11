#ifndef __MILESLIB_CSOUNDBASE_H__
#define __MILESLIB_CSOUNDBASE_H__

#include <map>
#include <vector>
#include "SoundData.h"

struct ma_engine;

typedef std::map<DWORD, CSoundData*> TSoundDataMap;

class CSoundBase
{
public:
	CSoundBase();
	virtual ~CSoundBase();

	void Initialize();
	void Destroy();

	CSoundData* AddFile(DWORD dwFileCRC, const char* filename);
	DWORD GetFileCRC(const char* filename);

protected:
	static int ms_iRefCount;
	static ma_engine* ms_pEngine;
	static TSoundDataMap ms_dataMap;
	static bool ms_bInitialized;
};

#endif
