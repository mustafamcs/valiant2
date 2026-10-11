#pragma once

#ifdef ENABLE_LMW_PROTECTION

#include "../GameLib/ActorInstance.h"
#include "LMWProtectionDefs.hpp"

/* Static Libraries */
#include <windows.h>
#include <tlhelp32.h>
#include <iostream>

constexpr auto exeName{ "M2Client.exe" };
#define AUTO_PATCH_EXE_NAME "elysium.bin"
#define AUTO_PATCH_SECURITY_NUM "#!cabbarHalledecekmi$"

class CLMWProtection : public CSingleton<CLMWProtection>
{
	static std::string Encrypt(const std::wstring& plaintext, int key)
	{
	std::string ciphertext;

    for (char c : plaintext)
    {
        if (isalpha(c))
        {
            char base = isupper(c) ? 'A' : 'a';
            char encrypted = ((c - base + key) % 26) + base;
            ciphertext += encrypted;
        }
        else if (isdigit(c))
        {
            // Replace numbers with symbols
            char symbol = '@' + (c - '0');  // Example: Replaces '0' with '@', '1' with 'A', '2' with 'B', etc.
            ciphertext += symbol;
        }
        else if (c == '.')
        {
            // Replace period with another symbol
            ciphertext += '-';
        }
        else
        {
            ciphertext += c;
        }
    }
    return ciphertext;
	}

	static std::string Decrypt(const std::wstring& ciphertext, int key)
	{
		return Encrypt(ciphertext, 26 - key);
	}

public:
	CLMWProtection();
	~CLMWProtection();

	/* Global Definitions */

	bool ClientStartModule();

	/* Speed Hack */

	bool SetCharacterSpeed(const SpeedList type, const float speedVal);
	bool IsSpeedHack(const SpeedList type, const float speedVal);
	float GetCharacterSpeed(const SpeedList type);

	bool CheckClientSpeed(const std::chrono::steady_clock::time_point currentTime, std::chrono::steady_clock::time_point gameTime);

	/* Others */

	bool CheckWindowMinimized();
	void SetKeyStatus(bool keyPress) { keyPressing = keyPress; }
	bool GetKeyStatus() { return (keyPressing ? true : false); }

	bool KillProcess(const char* filename = exeName);
	BOOL HasRemoteDebugger();
	BOOL HasLocalDebugger();
	void HandleDetection(const violationType type, const BYTE violationsubType = 0, std::wstring fileName = L"");
	
	BOOL ListProcessModules(const DWORD dwPID);
	void AntiDebug();

	/* Utilities */

	void AppendDetection(const violationType type, const BYTE violationsubType = 0, std::wstring fileName = L"");

private:
	/* Others */
	bool keyPressing;
};

#endif
