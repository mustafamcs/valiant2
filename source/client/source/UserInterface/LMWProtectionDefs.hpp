#pragma once

constexpr bool blockAttackWhenMinimized{ false };
constexpr bool checkYWFolder{ false };
constexpr unsigned cryptionNum{ 51 };
constexpr bool speedHackControl{ 0 };

const std::vector<std::wstring> blockedAlliases = 
{
	L"cheat", L"process", L"h3x",
	L"hxd", L"ida", L"fiddle",
};

enum violationType : int
{
	ATTACK_SPEED_HACK = 552,
	MOVEMENT_SPEED_HACK,
	DAMAGE_HACK,
	TELEPORT_HACK,
	DLL_INJECTION,
	CLIENT_INIT_FAILED,
	STRANGE_APP_DETECTED,
	VIRTUAL_MACHINE_DETECTED,
	FORBIDDEN_FILE_FOUND, // Possible ymir work folder on disk d
	WINDOW_PROTECTION_ERR,
	UNKNOWN_DEBUGGER_DETECTED,
	UNKNOWN_ERROR
};

enum winProtectionViolations : int
{
	SUB_WINDOW_PROTECTION_CHECK_FAIL,
	SUB_WINDOW_PROTECTION_CORRUPTED,
	SUB_WINDOW_PROTECTION_CAN_NOT_ENABLED,
	SUB_WINDOW_PROTECTION_CAN_NOT_DISABLED
};

enum SpeedList : int
{
	ATTACK_SPEED,
	MOVEMENT_SPEED
};