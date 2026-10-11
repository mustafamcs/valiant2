#include "StdAfx.h"
#include "Timer.h"
#ifdef ENABLE_FPS_SYSTEM_LIMIT_REWORK
#include "../GameLib/GameType.h"
#endif

static LARGE_INTEGER gs_liTickCountPerSec;
static DWORD gs_dwBaseTime = 0;
static DWORD gs_dwServerTime = 0;
static DWORD gs_dwClientTime = 0;
static DWORD gs_dwFrameTime = 0;

#pragma comment(lib, "winmm.lib")

BOOL ELTimer_Init()
{
	gs_dwBaseTime = timeGetTime();
	return 1;
}

DWORD ELTimer_GetMSec()
{
	return timeGetTime() - gs_dwBaseTime;
}

VOID	ELTimer_SetServerMSec(DWORD dwServerTime)
{
	NANOBEGIN
		if (0 != dwServerTime)
		{
			gs_dwServerTime = dwServerTime;
			gs_dwClientTime = CTimer::instance().GetCurrentMillisecond();
		}
	NANOEND
}

DWORD	ELTimer_GetServerMSec()
{
	return CTimer::instance().GetCurrentMillisecond() - gs_dwClientTime + gs_dwServerTime;
}

DWORD	ELTimer_GetFrameMSec()
{
	return gs_dwFrameTime;
}

DWORD	ELTimer_GetServerFrameMSec()
{
	return ELTimer_GetFrameMSec() - gs_dwClientTime + gs_dwServerTime;
}

VOID	ELTimer_SetFrameMSec()
{
	gs_dwFrameTime = ELTimer_GetMSec();
}

CTimer::CTimer()
{
	ELTimer_Init();

	NANOBEGIN
		if (this)
		{
			m_dwCurrentTime = 0;
			m_bUseRealTime = true;
			m_index = 0;

			m_dwElapsedTime = 0;

			m_fCurrentTime = 0.0f;
		}
	NANOEND
}

CTimer::~CTimer() = default;

void CTimer::SetBaseTime()
{
	m_dwCurrentTime = 0;
}

void CTimer::Advance()
{
	if (!m_bUseRealTime)
	{
		++m_index;

		if (m_index == 1)
			m_index = -1;

#ifdef ENABLE_FPS_SYSTEM_LIMIT_REWORK
		m_dwCurrentTime += (16 - ((g_fGameFPS - 60) / 10)) + (m_index & 1); // 6 for 160fps
#else
		m_dwCurrentTime += 16 + (m_index & 1);
#endif
		m_fCurrentTime = m_dwCurrentTime / 1000.0f;
	}
	else
	{
		DWORD currentTime = ELTimer_GetMSec();

		if (m_dwCurrentTime == 0)
			m_dwCurrentTime = currentTime;

		m_dwElapsedTime = currentTime - m_dwCurrentTime;
		m_dwCurrentTime = currentTime;
	}
}

void CTimer::Adjust(int iTimeGap)
{
	m_dwCurrentTime += iTimeGap;
}

float CTimer::GetCurrentSecond()
{
	if (m_bUseRealTime)
		return ELTimer_GetMSec() / 1000.0f;

	return m_fCurrentTime;
}

DWORD CTimer::GetCurrentMillisecond()
{
	if (m_bUseRealTime)
		return ELTimer_GetMSec();

	return m_dwCurrentTime;
}

float CTimer::GetElapsedSecond()
{
	return GetElapsedMillisecond() / 1000.0f;
}

DWORD CTimer::GetElapsedMillisecond()
{
	if (!m_bUseRealTime)
#ifdef ENABLE_FPS_SYSTEM_LIMIT_REWORK
		return (16 - ((g_fGameFPS - 60) / 10)) + (m_index & 1); // 160fp
#else
		return 16 + (m_index & 1);
#endif

	return m_dwElapsedTime;
}

void CTimer::UseCustomTime()
{
	m_bUseRealTime = false;
}