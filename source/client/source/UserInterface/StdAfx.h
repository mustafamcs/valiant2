#pragma once

#pragma warning(disable:4702)
#pragma warning(disable:4100)
#pragma warning(disable:4201)
#pragma warning(disable:4511)
#pragma warning(disable:4663)
#pragma warning(disable:4018)
#pragma warning(disable:4245)

#if _MSC_VER >= 1400
//if don't use below, time_t is 64bit
#define _USE_32BIT_TIME_T
#endif
#include <iterator>
#include "../eterLib/StdAfx.h"
#include "../eterPythonLib/StdAfx.h"
#include "../gameLib/StdAfx.h"
#include "../scriptLib/StdAfx.h"
#include "../EffectLib/StdAfx.h"
#include "../PRTerrainLib/StdAfx.h"
#include "../SpeedTreeLib/StdAfx.h"

#ifndef __D3DRM_H__
#define __D3DRM_H__
#endif

#include <dshow.h>
#include <qedit.h>

#include "Locale.h"

#include "GameType.h"
extern DWORD __DEFAULT_CODE_PAGE__;

#define APP_NAME	"Metin 2"

enum eSettings
{
	POINT_MAX_NUM = 255,
	CHARACTER_NAME_MAX_LEN = 64, //@Lightwork131
#if defined(LOCALE_SERVICE_JAPAN)
	PLAYER_NAME_MAX_LEN = 16,
#else
	PLAYER_NAME_MAX_LEN = 12,
#endif
#ifdef ENABLE_OFFLINE_SHOP
	OFFLINE_SHOP_NAME_MAX_LEN = 40 + CHARACTER_NAME_MAX_LEN + 1,
	OFFLINE_SHOP_ITEM_MAX_LEN = 24,
#endif
};

void initudp();
void initapp();
void initime();
void initsystemSetting();
void initchr();
void initchrmgr();
void initChat();
void initTextTail();
void initime();
void initItem();
void initNonPlayer();
void initnet();
void initPlayer();
void initSectionDisplayer();
void initServerStateChecker();
void initTrade();
void initMiniMap();
void initProfiler();
void initEvent();
void initeffect();
void initsnd();
void initeventmgr();
void initBackground();
void initwndMgr();
void initshop();
void initpack();
void initskill();
void initfly();
void initquest();
void initsafebox();
void initguild();
void initMessenger();
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
void initAcce();
#endif
#ifdef ENABLE_CUBE_RENEWAL_WORLDARD
void intcuberenewal();
#endif
#ifdef ENABLE_OFFLINE_SHOP
void initofflineshop();
#endif
#ifdef ENABLE_SWITCHBOT
void initSwitchbot();
#endif
#ifdef ENABLE_RENDER_TARGET
void initRenderTarget();
#endif
#ifdef ENABLE_GLOBAL_RANKING
void initStaticsRank();
#endif
#ifdef ENABLE_NEW_PET_SYSTEM
void initskillpet();
void initnewpet();
#endif
#ifdef ENABLE_BIOLOG_SYSTEM
void initBiolog();
#endif
#ifdef ENABLE_IN_GAME_LOG_SYSTEM
void initInGameLog();
#endif

#ifdef ENABLE_DUNGEON_INFO
void initDungeonInfo();
#endif

#ifdef ENABLE_NEW_MODULE_CONFIG
void initcfg();
#endif
#ifdef ENABLE_AURA_SYSTEM
void initAura();
#endif
#ifdef ENABLE_WIKI
void initWiki();
#endif

