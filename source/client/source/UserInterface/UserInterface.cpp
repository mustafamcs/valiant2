#include "StdAfx.h"
#include "PythonApplication.h"
#include "PythonExceptionSender.h"
#include "resource.h"
#include "../EterFSLib/FileSystemIncl.hpp"
#ifdef ENABLE_CEF_BROWSER
#include "CefWebBrowser.h"
#endif
#include "../eterBase/CPostIt.h"
#ifdef ENABLE_CLIENT_OPTIMISATION
#include "PythonOptimizationBoost.h"
#endif

#ifdef ENABLE_HWID
#include "HWIDManager.h"
#endif

#ifdef ENABLE_LMW_PROTECTION
#include "LMWProtection.hpp"
#endif

#include <tbb/parallel_for.h>
#include <rapidjson/document.h>
#include <rapidjson/error/en.h>
#include <shellapi.h>

extern "C" {
	extern int _fltused;// @Lightwork1
	FILE __iob_func[3] = { *stdin, *stdout, *stderr };
	volatile int _AVOID_FLOATING_POINT_LIBRARY_BUG = _fltused;
	__declspec(dllexport) DWORD NvOptimusEnablement = 0x00000001;
	__declspec(dllexport) int AmdPowerXpressRequestHighPerformance = 1;
};

#pragma comment(linker, "/NODEFAULTLIB:libci.lib")
#include <algorithm>
#include "../EterBase/Filename.h"
#pragma comment( lib, "version.lib" )
#pragma comment( lib, "python27.lib" )
#pragma comment( lib, "imagehlp.lib" )
#pragma comment( lib, "devil.lib" )

#pragma comment( lib, "granny2.11.8.0.lib" )
#pragma comment( lib, "mss32.lib" )
#pragma comment( lib, "winmm.lib" )
#pragma comment( lib, "imm32.lib" )
#pragma comment( lib, "oldnames.lib" )
#pragma comment( lib, "SpeedTreeRT.lib" )
#pragma comment( lib, "dinput8.lib" )
#pragma comment( lib, "dxguid.lib" )
#pragma comment( lib, "ws2_32.lib" )
#pragma comment( lib, "strmiids.lib" )
#pragma comment( lib, "ddraw.lib" )
#pragma comment( lib, "dmoguids.lib" )
#include <stdlib.h>
#include <cryptopp/cryptoppLibLink.h>

#ifdef ENABLE_OFFLINE_SHOP
#pragma comment( lib, "libconfig.lib" )
#pragma comment( lib, "shlwapi.lib" )
#endif

#pragma comment( lib, "xxhash.lib")
#pragma comment( lib, "lz4.lib")
#pragma comment( lib, "zlib.lib")

#define ENABLE_PYLIB_CHECK

#ifdef __USE_CYTHON__
#include "../../external/projects/CRootLib/Workplace/RootLib/PythonrootlibManager.cpp"
#endif

#ifdef __USE_EXTRA_CYTHON__
#include "../../external/projects/CUiScriptLib/Workplace/UiScriptLib/PythonuiscriptlibManager.cpp"
#endif

extern bool SetDefaultCodePage(DWORD codePage);

static const char* sc_apszPythonLibraryFilenames[] =
{
	"UserDict.pyc",
	"__future__.pyc",
	"copy_reg.pyc",
	"linecache.pyc",
	"ntpath.pyc",
	"os.pyc",
	"site.pyc",
	"stat.pyc",
	"string.pyc",
	"traceback.pyc",
	"types.pyc",
	"\n",
};

#ifdef ENABLE_PYLIB_CHECK
#define PRINT_LEVEL 0
#define PRINTME(level, ...) if(PRINT_LEVEL>=level) TraceError(__VA_ARGS__);
#define PYFOLD "./lib"

typedef struct PyLibFiles_s
{
	std::string sFileName;
	size_t stSize;
	DWORD dwCRC32;
} PyLibFiles_t;

PyLibFiles_t PyLibFilesTable[] =
{
#if PY_VERSION_HEX==0x020706f0
	{ PYFOLD"/abc.pyc", 6187, 3834771731},
	{ PYFOLD"/bisect.pyc", 3236, 3116899751},
	{ PYFOLD"/codecs.pyc", 36978, 2928014693},
	{ PYFOLD"/collections.pyc", 26172, 385366131},
	{ PYFOLD"/copy.pyc", 13208, 1091298715},
	{ PYFOLD"/copy_reg.pyc", 5157, 536292604},
	{ PYFOLD"/encodings/aliases.pyc", 8803, 3888310600},
	{ PYFOLD"/encodings/cp949.pyc", 2009, 1824094431},
	{ PYFOLD"/encodings/__init__.pyc", 4510, 2926961588},
	{ PYFOLD"/fnmatch.pyc", 3732, 4270526278},
	{ PYFOLD"/functools.pyc", 6193, 3257285433},
	{ PYFOLD"/genericpath.pyc", 3303, 1652596334},
	{ PYFOLD"/heapq.pyc", 13896, 2948659214},
	{ PYFOLD"/keyword.pyc", 2169, 2178546341},
	{ PYFOLD"/linecache.pyc", 3235, 4048207604},
	{ PYFOLD"/locale.pyc", 49841, 4114662314},
	{ PYFOLD"/ntpath.pyc", 11961, 2765879465},
	{ PYFOLD"/os.pyc", 25769, 911432770},
	{ PYFOLD"/pyexpat.pyd", 127488, 2778492911},
	{ PYFOLD"/pyexpat_d.pyd", 194560, 2589182738},
	{ PYFOLD"/re.pyc", 13178, 1671609387},
	{ PYFOLD"/shutil.pyc", 19273, 1873281015},
	{ PYFOLD"/site.pyc", 20019, 3897044925},
	{ PYFOLD"/sre_compile.pyc", 11107, 1620746411},
	{ PYFOLD"/sre_constants.pyc", 6108, 3900811275},
	{ PYFOLD"/sre_parse.pyc", 19244, 1459430047},
	{ PYFOLD"/stat.pyc", 2791, 1375966108},
	{ PYFOLD"/string.pyc", 19656, 1066063587},
	{ PYFOLD"/sysconfig.pyc", 17571, 1529083148},
	{ PYFOLD"/traceback.pyc", 11703, 3768933732},
	{ PYFOLD"/types.pyc", 2530, 920695307},
	{ PYFOLD"/UserDict.pyc", 9000, 1431875928},
	{ PYFOLD"/warnings.pyc", 13232, 3752454002},
	{ PYFOLD"/weakref.pyc", 16037, 2124701469},
	{ PYFOLD"/xml/dom/domreg.pyc", 3506, 2127674645},
	{ PYFOLD"/xml/dom/expatbuilder.pyc", 36698, 316034696},
	{ PYFOLD"/xml/dom/minicompat.pyc", 4144, 747596376},
	{ PYFOLD"/xml/dom/minidom.pyc", 74704, 1543233763},
	{ PYFOLD"/xml/dom/nodefilter.pyc", 1243, 3805409468},
	{ PYFOLD"/xml/dom/xmlbuilder.pyc", 18659, 4118801318},
	{ PYFOLD"/xml/dom/__init__.pyc", 7337, 343751384},
	{ PYFOLD"/xml/parsers/expat.pyc", 326, 2425747752},
	{ PYFOLD"/xml/parsers/__init__.pyc", 353, 1691127318},
	{ PYFOLD"/xml/__init__.pyc", 1117, 3531597556},
	{ PYFOLD"/_abcoll.pyc", 22339, 2365844594},
	{ PYFOLD"/_locale.pyc", 49841, 4114662314},
	{ PYFOLD"/_weakrefset.pyc", 10490, 1576811346},
	{ PYFOLD"/__future__.pyc", 4431, 2857792867},
#elif PY_VERSION_HEX==0x020203f0
#else
#error "unknown python version"
#endif
};

bool checkPyLibDir(const string szDirName)
{
	bool HasHack = false;

	char szDirNamePath[MAX_PATH];
	sprintf(szDirNamePath, "%s\\*", szDirName.c_str());

	WIN32_FIND_DATA f;
	HANDLE h = FindFirstFile(szDirNamePath, &f);

	if (h == INVALID_HANDLE_VALUE) { return HasHack; }

	do
	{
		if (HasHack)
			break;
		const char* name = f.cFileName;

		if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0) { continue; }

		if (f.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
		{
			char filePath[MAX_PATH];
			sprintf(filePath, "%s%s%s", szDirName.c_str(), "\\", name);
			PRINTME(1, "sub %s", filePath);
			checkPyLibDir(filePath);
		}
		else
		{
			// start processing file
			PRINTME(1, "starting %s", name);
			std::string sName(name);
			std::string sPathName(szDirName + "/" + name);
			// change \\ to /
			std::replace(sPathName.begin(), sPathName.end(), '\\', '/');
			PRINTME(1, "path %s", sPathName.c_str());
			// lower file name
			std::transform(sName.begin(), sName.end(), sName.begin(), ::tolower);
			{
				PRINTME(1, "verify %s", sName.c_str());
				bool isPyLibFound = false;
				for (PyLibFiles_t* i1 = std::begin(PyLibFilesTable), *e1 = std::end(PyLibFilesTable); i1 < e1; i1++)
				{
					if (!i1->sFileName.compare(sPathName))
					{
						PRINTME(1, "found %s==%s", i1->sFileName.c_str(), sName.c_str());
						DWORD dwCrc32 = GetFileCRC32(sPathName.c_str());
						// assert(dwCrc32);
						DWORD dwFileSize = f.nFileSizeLow;
						if (i1->stSize != dwFileSize)
						{
							PRINTME(1, "wrong size %u==%u", i1->stSize, dwFileSize);
							HasHack = true;
							PRINTME(0, "wrong size %u for %s", dwFileSize, sPathName.c_str());
							return HasHack;
						}
						else if (i1->dwCRC32 != dwCrc32)
						{
							PRINTME(1, "wrong crc32 %u==%u", i1->dwCRC32, dwCrc32);
							HasHack = true;
							PRINTME(0, "wrong crc32 %u for %s", dwCrc32, sPathName.c_str());
							return HasHack;
						}
						PRINTME(1, "right size %u==%u", i1->stSize, dwFileSize);
						PRINTME(1, "right crc32 %u==%u", i1->dwCRC32, dwCrc32);
						PRINTME(2, "{ \"%s\", %u, %u},", sPathName.c_str(), dwFileSize, dwCrc32);
						isPyLibFound = true;
						break;
					}
				}
				// block ambiguous pyc/d files
				if (!isPyLibFound)
				{
					PRINTME(1, "not found %s", sName.c_str());
				}
				PRINTME(1, "skipping file(%s) hack(%u) found(%u)", sName.c_str(), HasHack, isPyLibFound);
			}
		}
	} while (FindNextFile(h, &f));
	FindClose(h);
	return HasHack;
}

bool __CheckPyLibFiles()
{
	if (checkPyLibDir(PYFOLD))
		return false;
	return true;
}
#endif



bool CheckPythonLibraryFilenames()
{
	for (int i = 0; *sc_apszPythonLibraryFilenames[i] != '\n'; ++i)
	{
		std::string stFilename = "lib\\";
		stFilename += sc_apszPythonLibraryFilenames[i];

		if (_access(stFilename.c_str(), 0) != 0)
		{
			return false;
		}

		MoveFile(stFilename.c_str(), stFilename.c_str());
	}

	return true;
}

int Setup(LPSTR lpCmdLine); // Internal function forward

static bool PackInitialize(CFile& file, FileSystemManager* file_system)
{
	rapidjson::Document document;
	document.Parse(reinterpret_cast<const char*>(file.GetData()));

	if (document.HasParseError())
	{
		TraceError("%ls parse failed! Error: %s offset: %u", file.GetFileName().c_str(), GetParseError_En(document.GetParseError()), document.GetErrorOffset());
		return false;
	}

	if (!document.HasMember("pack_dir"))
	{
		TraceError("%ls has no member `pack_dir`", file.GetFileName().c_str());
		return false;
	}

	if (!document.HasMember("files"))
	{
		TraceError("%ls has no member `files`", file.GetFileName().c_str());
		return false;
	}

	if (!document["pack_dir"].IsString())
	{
		TraceError("%ls type member `pack_dir` is not string", file.GetFileName().c_str());
		return false;
	}

	if (!document["files"].IsArray())
	{
		TraceError("%ls type member `files` is not array", file.GetFileName().c_str());
		return false;
	}

	const std::string pack_dir = document["pack_dir"].GetString();
	const auto& files = document["files"];

	parallel_for(tbb::blocked_range<int32_t>(0, files.Size()),
		[&](const tbb::blocked_range<int32_t> r)
		{
			for (auto i = r.begin(); i < r.end(); ++i)
			{
				if (!files[i].IsString())
					continue;

				const auto& name = pack_dir + files[i].GetString() + ".pak";
				const auto& key = file_system->GetArchiveKey(name);
				if (!file_system->AddArchive(name, key)) {
					abort();
				}
			}
			return true;
		}
	);
	return true;
}

bool RunMainScript(CPythonLauncher& pyLauncher, const char* lpCmdLine)
{
	initpack();
	initdbg();
	initime();
	initgrp();
	initgrpImage();
	initgrpText();
	initwndMgr();
	initudp();
	initapp();
	initsystemSetting();
	initchr();
	initchrmgr();
	initPlayer();
	initItem();
	initNonPlayer();
	initTrade();
	initChat();
	initTextTail();
	initnet();
	initMiniMap();
	initProfiler();
	initEvent();
	initeffect();
	initfly();
	initsnd();
	initeventmgr();
	initshop();
	initskill();
	initquest();
	initBackground();
	initMessenger();
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	initAcce();
#endif
	initsafebox();
	initguild();
	initServerStateChecker();
#ifdef ENABLE_CUBE_RENEWAL_WORLDARD
	intcuberenewal();
#endif
#ifdef ENABLE_OFFLINE_SHOP
	initofflineshop();
#endif
#ifdef ENABLE_SWITCHBOT
	initSwitchbot();
#endif
#ifdef ENABLE_RENDER_TARGET
	initRenderTarget();
#endif
#ifdef ENABLE_GLOBAL_RANKING
	initStaticsRank();
#endif
#ifdef ENABLE_BIOLOG_SYSTEM
	initBiolog();
#endif
#ifdef ENABLE_IN_GAME_LOG_SYSTEM
	initInGameLog();
#endif
#ifdef ENABLE_DUNGEON_INFO
	initDungeonInfo();
#endif
#ifdef __USE_CYTHON__
	initrootlibManager();
#endif
#ifdef __USE_EXTRA_CYTHON__
	inituiscriptlibManager();
#endif
#ifdef ENABLE_NEW_PET_SYSTEM
	initskillpet();
	initnewpet();
#endif
#ifdef ENABLE_NEW_MODULE_CONFIG
	initcfg();
#endif
#ifdef ENABLE_AURA_SYSTEM
	initAura();
#endif
#ifdef ENABLE_WIKI
	initWiki();
#endif
	PyObject* builtins = PyImport_ImportModule("__builtin__");

#ifdef NDEBUG // @warme601 _DISTRIBUTE -> NDEBUG
	PyModule_AddIntConstant(builtins, "__DEBUG__", 0);
#else
	PyModule_AddIntConstant(builtins, "__DEBUG__", 1);
#endif

#ifdef __USE_CYTHON__
	PyModule_AddIntConstant(builtins, "__USE_CYTHON__", 1);
#else
	PyModule_AddIntConstant(builtins, "__USE_CYTHON__", 0);
#endif
#ifdef __USE_EXTRA_CYTHON__
	PyModule_AddIntConstant(builtins, "__USE_EXTRA_CYTHON__", 1);
#else
	PyModule_AddIntConstant(builtins, "__USE_EXTRA_CYTHON__", 0);
#endif

	{
		std::vector<std::string> stVec;
		SplitLine(lpCmdLine, " ", &stVec);

		if (stVec.size() != 0 && "--pause-before-create-window" == stVec[0])
		{
			system("pause");
		}

#ifdef __USE_CYTHON__
		if (!pyLauncher.RunLine("import rootlib\nrootlib.moduleImport('system')"))
#else
		if (!pyLauncher.RunFile("system.py"))
#endif
		{
			TraceError("RunMain Error");
			return false;
		}
	}

	return true;
}

bool Main(HINSTANCE hInstance, LPSTR lpCmdLine)
{
	SetLogLevel(1);
	ilInit();

	if (!Setup(lpCmdLine))
		return false;

	OpenLogFile(false);

	static CLZO				lzo;
	FileSystemManager file_system;
#ifdef ENABLE_CLIENT_OPTIMISATION
	static CPythonOptimizationBoost PlayerSettings;
#endif
#ifdef ENABLE_LMW_PROTECTION
	static CLMWProtection LMWProtection;
#endif
#ifdef ENABLE_HWID
	static HWIDMANAGER hwidManager;
#endif

	CTextFileLoader::SetCacheMode();
	if (!file_system.InitializeFSManager(
#ifdef ENABLE_LAYER2_FILE_ENCRYPTION
		FILE_FLAG_XTEA
#endif
	))
	{
		LogBox("FileSystem Initialization failed");
		return false;
	}

	file_system.AddToDiskBlacklist("py");
	file_system.AddToDiskBlacklist("pyc");


	CFile file;
	const std::string pack_file = "lib/json/p_names.json";
	if (!file_system.OpenFile(pack_file, file))
	{
		TraceError("Failed to open %s", pack_file.c_str());
		file.Close();
		return false;
	}

	if (!PackInitialize(file, &file_system))
	{
		LogBox("Pack Initialization failed.");
		file.Close();
		return false;
	}


#ifdef ENABLE_NEW_MODULE_CONFIG
	static CPythonConfig m_pyConfig;
	m_pyConfig.Initialize("lib/data/config.cfg");
#endif

	if (LocaleService_LoadGlobal(hInstance))
		SetDefaultCodePage(LocaleService_GetCodePage());

#ifdef ENABLE_PYLIB_CHECK
	if (!__CheckPyLibFiles())
		return false;
#endif

#ifdef ENABLE_LMW_PROTECTION
	if (!CLMWProtection::Instance().ClientStartModule())
		return false;

#ifdef AUTO_PATCH_PROTECTION
	if (strstr(lpCmdLine, AUTO_PATCH_COMMAND) == 0)
	{
		ShellExecute(NULL, NULL, AUTO_PATCH_EXE_NAME, NULL, NULL, SW_SHOW);
		return false;
	}
#endif

#endif

	CPythonApplication* app = new CPythonApplication;

	app->Initialize(hInstance);

	bool appStart { false };
	{
		CPythonLauncher pyLauncher{};
		CPythonExceptionSender pyExceptionSender{};
		SetExceptionSender(&pyExceptionSender);

		if (pyLauncher.Create())
			appStart = RunMainScript(pyLauncher, lpCmdLine);

		app->Clear();

		timeEndPeriod(1);
		pyLauncher.Clear();
	}

	app->Destroy();
	delete app;

	return appStart;
}

int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	LocaleService_LoadConfig("UserData/loca.cfg");
	SetDefaultCodePage(LocaleService_GetCodePage());

#ifdef ENABLE_CEF_BROWSER
	CefWebBrowser_Startup(hInstance);
#endif

#ifndef ENABLE_PYLIB_CHECK
	if (!CheckPythonLibraryFilenames())
	{
		__ErrorPythonLibraryIsNotExist();
		goto Clean;
	}
#endif

	Main(hInstance, lpCmdLine);

#ifdef ENABLE_CEF_BROWSER
	CefWebBrowser_Cleanup();
#endif

	::CoUninitialize();

	return 0;
}


static void GrannyError(granny_log_message_type Type,
	granny_log_message_origin Origin,
	char const* File,
	granny_int32x Line,
	char const* Error,
	void* UserData)
{
}

int Setup(LPSTR lpCmdLine)
{
	TIMECAPS tc{};
	unsigned wTimerRes{};

	if (timeGetDevCaps(&tc, sizeof(TIMECAPS)) != TIMERR_NOERROR)
		return 0;

	wTimerRes = MINMAX(tc.wPeriodMin, 1, tc.wPeriodMax);
	timeBeginPeriod(wTimerRes);

	granny_log_callback Callback;
	Callback.Function = GrannyError;
	Callback.UserData = 0;
	GrannySetLogCallback(&Callback);
	return 1;
}