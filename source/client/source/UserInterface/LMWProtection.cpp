
#include "StdAfx.h"
#ifdef ENABLE_LMW_PROTECTION

/* Dynamic Libraries */
#include "LMWProtection.hpp"
#include "Packet.h"
#include "PythonPlayer.h"
#include "InstanceBase.h"
#include "PythonChat.h"
#include "PythonApplication.h"

CLMWProtection::CLMWProtection() : keyPressing(false) {}

CLMWProtection::~CLMWProtection()
{
	keyPressing = false;
}

float CLMWProtection::GetCharacterSpeed(const SpeedList type)
{
	if (type == ATTACK_SPEED)
		return (CPythonPlayer::Instance().GetStatus(POINT_ATT_SPEED) / 100.0f);
		
	return (CPythonPlayer::Instance().GetStatus(POINT_MOV_SPEED) / 100.0f);
}

bool CLMWProtection::IsSpeedHack(const SpeedList type, const float speedVal)
{
	if (type == ATTACK_SPEED)
	{
		if (speedVal != GetCharacterSpeed(ATTACK_SPEED))
			return true;
	}
	else
	{
		if (speedVal != GetCharacterSpeed(MOVEMENT_SPEED))
			return true;
	}
	return false;
}

bool CLMWProtection::SetCharacterSpeed(const SpeedList type, const float speedVal)
{
	CActorInstance& actorInstance = CActorInstance();

	if (type == ATTACK_SPEED)
	{
		if (IsSpeedHack(ATTACK_SPEED, speedVal))
		{
			actorInstance.SetAttackSpeed(GetCharacterSpeed(ATTACK_SPEED));
			return true;
		}
	}
	else
	{
		if (IsSpeedHack(MOVEMENT_SPEED, speedVal))
		{
			actorInstance.SetMoveSpeed(GetCharacterSpeed(MOVEMENT_SPEED));
			return true;
		}
	}
	return false;
}

bool CheckClientSpeed(const std::chrono::steady_clock::time_point currentTime, std::chrono::steady_clock::time_point gameTime)
{
	return false;
}

bool CLMWProtection::CheckWindowMinimized() /* For leaving space while not farmin'.*/
{
	if (blockAttackWhenMinimized)
	{
		if (!CPythonApplication::Instance().IsActiveWindow() && GetKeyStatus())
			return true;
	}

	return false;
}

void CLMWProtection::AppendDetection(const violationType type, const BYTE violationsubType, std::wstring fileName)
{
	switch (type)
	{
		case WINDOW_PROTECTION_ERR:
		{
			switch (violationsubType)
			{
				case SUB_WINDOW_PROTECTION_CHECK_FAIL:
				case SUB_WINDOW_PROTECTION_CORRUPTED:
				case SUB_WINDOW_PROTECTION_CAN_NOT_ENABLED:
				case SUB_WINDOW_PROTECTION_CAN_NOT_DISABLED:
					TraceError("ACIF - ErrorType: %u, SubType %u", type, violationsubType);
					return;
			}
			break;
		}
	}

	if (fileName.length()>1)
		TraceError("ACIF - ErrorType: %u - PS: %s", type, Encrypt(fileName, cryptionNum));
	else
		TraceError("ACIF - ErrorType: %u", type);
}

bool CLMWProtection::KillProcess(const char* filename)
{
	HANDLE hSnapShot = CreateToolhelp32Snapshot(TH32CS_SNAPALL, NULL);
	PROCESSENTRY32 pEntry;
	pEntry.dwSize = sizeof(pEntry);
	BOOL hRes = Process32First(hSnapShot, &pEntry);
	while (hRes)
	{
		if (strcmp(pEntry.szExeFile, filename) == 0)
		{
			HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, 0, (DWORD)pEntry.th32ProcessID);
			if (hProcess != NULL)
			{
				TerminateProcess(hProcess, 1);
				CloseHandle(hProcess);
				return true;
			}
		}
		hRes = Process32Next(hSnapShot, &pEntry);
	}
	CloseHandle(hSnapShot);
	return false;
}

BOOL CLMWProtection::ListProcessModules(const DWORD dwPID)
{
	void* hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, dwPID);

	if (hModuleSnap == INVALID_HANDLE_VALUE)
	{
		//std::cerr << "Module snapshot creation failed for PID: ") << dwPID << std::endl;
		return FALSE;
	}

	MODULEENTRY32 me32;
	me32.dwSize = sizeof(MODULEENTRY32);

	if (Module32First(hModuleSnap, &me32))
	{
		do
		{
			std::wcout << L"  Module: " << me32.szModule << std::endl;
			std::wcout << L"    Path: " << me32.szExePath << std::endl;
			/*
			if ((me32.modBaseAddr < (BYTE*)0x80000000) && (me32.modBaseAddr != nullptr))
			{
				HandleDetection(DLL_INJECTION);
			}*/

		} while (Module32Next(hModuleSnap, &me32));
	}
	else
	{
		std::cerr << "Module enumeration failed for PID: " << dwPID << std::endl;
	}

	CloseHandle(hModuleSnap);
	return TRUE;
}

BOOL CLMWProtection::HasRemoteDebugger()
{
	BOOL hasRemoteDebugger = FALSE;
	CheckRemoteDebuggerPresent(GetCurrentProcess(), &hasRemoteDebugger);
	return hasRemoteDebugger;
}

BOOL CLMWProtection::HasLocalDebugger()
{
	return IsDebuggerPresent();
}

void CLMWProtection::HandleDetection(const violationType type, const BYTE violationsubType, std::wstring fileName)
{
	fileName.length() > 1 ? AppendDetection(type, 0, fileName) : AppendDetection(type, violationsubType);
	KillProcess();
}

void CLMWProtection::AntiDebug()
{
	if (HasRemoteDebugger() || HasLocalDebugger())
	{
		HandleDetection(violationType::UNKNOWN_DEBUGGER_DETECTED);
		return;
	}

	// Süreç taraması ve DLL enjeksiyonu kontrolü
	HANDLE hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	if (hProcessSnap == INVALID_HANDLE_VALUE)
	{
		std::cerr << "CreateToolhelp32Snapshot (of processes) failed" << std::endl;
		return;
	}

	PROCESSENTRY32 pe32;
	pe32.dwSize = sizeof(PROCESSENTRY32);

	if (!Process32First(hProcessSnap, &pe32))
	{
		CloseHandle(hProcessSnap);
		std::cerr << "Process32First failed" << std::endl;
		return;
	}

	do
	{
		wchar_t wExeFile[MAX_PATH];
		MultiByteToWideChar(CP_ACP, 0, pe32.szExeFile, -1, wExeFile, MAX_PATH);

		std::wstring cExeFile(wExeFile);

		for (auto& c : cExeFile)
			c = tolower(c);

		for (const auto& alias : blockedAlliases)
		{
			if (cExeFile.find(alias) == 0)
			{
				HandleDetection(violationType::STRANGE_APP_DETECTED, 0, cExeFile);
				break;
			}
		}

		ListProcessModules(pe32.th32ProcessID);

	} while (Process32Next(hProcessSnap, &pe32));

	CloseHandle(hProcessSnap);
}

/**********************************************************************/

void StartAntiHackRoutine()
{
	while (true)
	{
		CLMWProtection::Instance().AntiDebug();
		std::this_thread::sleep_for(std::chrono::milliseconds(1250));
	}
}


bool CLMWProtection::ClientStartModule()
{
	if (checkYWFolder)
	{
		struct stat st;

		if (stat("D:\\ymir work", &st) == 0)
		{
			AppendDetection(FORBIDDEN_FILE_FOUND);
			return false;
		}
	}

	CreateThread(NULL, NULL, LPTHREAD_START_ROUTINE(StartAntiHackRoutine), NULL, 0, 0);
	return true;
}

#endif