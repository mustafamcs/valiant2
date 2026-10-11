#include "StdAfx.h"
#include "PythonSystem.h"
#include "PythonApplication.h"
#include "InstanceBase.h"

#define DEFAULT_VALUE_ALWAYS_SHOW_NAME		true

void CPythonSystem::SetInterfaceHandler(PyObject* poHandler)
{
	m_poInterfaceHandler = poHandler;
}

void CPythonSystem::DestroyInterfaceHandler()
{
	m_poInterfaceHandler = NULL;
}

void CPythonSystem::SaveWindowStatus(int iIndex, int iVisible, int iMinimized, int ix, int iy, int iHeight)
{
	m_WindowStatus[iIndex].isVisible = iVisible;
	m_WindowStatus[iIndex].isMinimized = iMinimized;
	m_WindowStatus[iIndex].ixPosition = ix;
	m_WindowStatus[iIndex].iyPosition = iy;
	m_WindowStatus[iIndex].iHeight = iHeight;
}

void CPythonSystem::GetDisplaySettings()
{
	memset(m_ResolutionList, 0, sizeof(TResolution) * RESOLUTION_MAX_NUM);
	m_ResolutionCount = 0;

	LPDIRECT3D9 lpD3D = CPythonGraphic::Instance().GetD3D();

	D3DADAPTER_IDENTIFIER9 d3dAdapterIdentifier;
	D3DDISPLAYMODE d3ddmDesktop;

	lpD3D->GetAdapterIdentifier(0, 0, &d3dAdapterIdentifier);
	lpD3D->GetAdapterDisplayMode(0, &d3ddmDesktop);

	DWORD dwNumAdapterModes = lpD3D->GetAdapterModeCount(0, d3ddmDesktop.Format);

	for (UINT iMode = 0; iMode < dwNumAdapterModes; iMode++)
	{
		D3DDISPLAYMODE DisplayMode;
		lpD3D->EnumAdapterModes(0, d3ddmDesktop.Format, iMode, &DisplayMode);
		DWORD bpp = 0;

		if (DisplayMode.Width < 800 || DisplayMode.Height < 600)
			continue;

		if (DisplayMode.Format == D3DFMT_R5G6B5)
			bpp = 16;
		else if (DisplayMode.Format == D3DFMT_X8R8G8B8)
			bpp = 32;
		else
			continue;

		int check_res = false;

		for (int i = 0; !check_res && i < m_ResolutionCount; ++i)
		{
			if (m_ResolutionList[i].bpp != bpp ||
				m_ResolutionList[i].width != DisplayMode.Width ||
				m_ResolutionList[i].height != DisplayMode.Height)
				continue;

			int check_fre = false;

			for (int j = 0; j < m_ResolutionList[i].frequency_count; ++j)
			{
				if (m_ResolutionList[i].frequency[j] == DisplayMode.RefreshRate)
				{
					check_fre = true;
					break;
				}
			}

			if (!check_fre)
				if (m_ResolutionList[i].frequency_count < FREQUENCY_MAX_NUM)
					m_ResolutionList[i].frequency[m_ResolutionList[i].frequency_count++] = DisplayMode.RefreshRate;

			check_res = true;
		}

		if (!check_res)
		{
			if (m_ResolutionCount < RESOLUTION_MAX_NUM)
			{
				m_ResolutionList[m_ResolutionCount].width = DisplayMode.Width;
				m_ResolutionList[m_ResolutionCount].height = DisplayMode.Height;
				m_ResolutionList[m_ResolutionCount].bpp = bpp;
				m_ResolutionList[m_ResolutionCount].frequency[0] = DisplayMode.RefreshRate;
				m_ResolutionList[m_ResolutionCount].frequency_count = 1;

				++m_ResolutionCount;
			}
		}
	}
}

int	CPythonSystem::GetResolutionCount()
{
	return m_ResolutionCount;
}

int CPythonSystem::GetFrequencyCount(int index)
{
	if (index >= m_ResolutionCount)
		return 0;

	return m_ResolutionList[index].frequency_count;
}

bool CPythonSystem::GetResolution(int index, OUT DWORD* width, OUT DWORD* height, OUT DWORD* bpp)
{
	if (index >= m_ResolutionCount)
		return false;

	*width = m_ResolutionList[index].width;
	*height = m_ResolutionList[index].height;
	*bpp = m_ResolutionList[index].bpp;
	return true;
}

bool CPythonSystem::GetFrequency(int index, int freq_index, OUT DWORD* frequncy)
{
	if (index >= m_ResolutionCount)
		return false;

	if (freq_index >= m_ResolutionList[index].frequency_count)
		return false;

	*frequncy = m_ResolutionList[index].frequency[freq_index];
	return true;
}

int	CPythonSystem::GetResolutionIndex(DWORD width, DWORD height, DWORD bit)
{
	DWORD re_width, re_height, re_bit;
	int i = 0;

	while (GetResolution(i, &re_width, &re_height, &re_bit))
	{
		if (re_width == width)
			if (re_height == height)
				if (re_bit == bit)
					return i;
		i++;
	}

	return 0;
}

int	CPythonSystem::GetFrequencyIndex(int res_index, DWORD frequency)
{
	DWORD re_frequency;
	int i = 0;

	while (GetFrequency(res_index, i, &re_frequency))
	{
		if (re_frequency == frequency)
			return i;

		i++;
	}

	return 0;
}

DWORD CPythonSystem::GetWidth()
{
	return m_Config.width;
}

DWORD CPythonSystem::GetHeight()
{
	return m_Config.height;
}
DWORD CPythonSystem::GetBPP()
{
	return m_Config.bpp;
}
DWORD CPythonSystem::GetFrequency()
{
	return m_Config.frequency;
}

bool CPythonSystem::IsSoftwareCursor()
{
	return m_Config.is_software_cursor;
}

#ifdef ENABLE_OUTLINED_NAMES
bool CPythonSystem::GetNamesType()
{
	return m_Config.bNamesOutline;
}

void CPythonSystem::SetNamesType(int value)
{
	m_Config.bNamesOutline = value;
}
#endif

#ifdef ENABLE_HIDE_AFFECT_ICONS
bool CPythonSystem::IsAffectIconShow()
{
	return m_Config.bShowAffectIcons;
}

void CPythonSystem::SetEffectIconShow(int value)
{
	m_Config.bShowAffectIcons = value;
}
#endif

#ifdef ENABLE_PERSPECTIVE_VIEW
float CPythonSystem::GetFieldPerspective()
{
	return m_Config.fField;
}

void CPythonSystem::SetFieldPerspective(float fValue)
{
	m_Config.fField = fValue;
}
#endif

#ifdef ENABLE_METIN_SCALE
float CPythonSystem::GetMetinstoneScale()
{
	if (m_Config.fStoneScale > 1.0f)
		m_Config.fStoneScale = 0.0f;

	return m_Config.fStoneScale;
}

void CPythonSystem::SetMetinstoneScale(float fValue)
{
	m_Config.fStoneScale = fMIN(fValue, 1.0f);
	CPythonTextTail::Instance().TextTailHeightRefresh();
}
#endif

#ifdef ENABLE_DAMAGE_SIZE_SCALE
float CPythonSystem::GetDamageTextureScale()
{
	return m_Config.fDamageTextureScale;
}

void CPythonSystem::SetDamageTextureScale(float fValue)
{
	m_Config.fDamageTextureScale = fMIN(fValue, 1.0f);
}
#endif

#ifdef ENABLE_HIDE_HIGHLIGHT
bool CPythonSystem::IsHighlightShow()
{
	return m_Config.bShowHighlightEffect;
}

void CPythonSystem::SetHighlightShow(int value)
{
	m_Config.bShowHighlightEffect = value;
}
#endif

#ifdef ENABLE_HIDE_TOOLTIP_EMOJI
bool CPythonSystem::GetEmojiStatus()
{
	return m_Config.bEmoji;
}

void CPythonSystem::SetEmojiStatus(int value)
{
	m_Config.bEmoji = value;
}
#endif

#ifdef ENABLE_HIDE_EFFECTS
bool CPythonSystem::IsEffectActive()
{
	return m_Config.bEffects;
}

void CPythonSystem::SetEffectActive(int value)
{
	m_Config.bEffects = value;
}
#endif

float CPythonSystem::GetMusicVolume()
{
	return m_Config.music_volume;
}

int CPythonSystem::GetSoundVolume()
{
	return m_Config.voice_volume;
}

void CPythonSystem::SetMusicVolume(float fVolume)
{
	m_Config.music_volume = fMAX(0.0f, fMIN(fVolume, 1.0f));
	SaveConfig();
}

void CPythonSystem::SetSoundVolumef(float fVolume)
{
	m_Config.voice_volume = (BYTE)(5.0f * fMAX(0.0f, fMIN(fVolume, 1.0f)));
	SaveConfig();
}

int CPythonSystem::GetDistance()
{
	return m_Config.iDistance;
}

int CPythonSystem::GetShadowLevel()
{
	return m_Config.iShadowLevel;
}

void CPythonSystem::SetShadowLevel(unsigned int level)
{
	m_Config.iShadowLevel = MIN(level, 5);
	CPythonBackground::instance().RefreshShadowLevel();
}

int CPythonSystem::IsSaveID()
{
	return m_Config.isSaveID;
}

const char* CPythonSystem::GetSaveID()
{
	return m_Config.SaveID;
}

bool CPythonSystem::isViewCulling()
{
	return m_Config.is_object_culling;
}

void CPythonSystem::SetSaveID(int iValue, const char* c_szSaveID)
{
	if (iValue != 1)
		return;

	m_Config.isSaveID = iValue;
	strncpy(m_Config.SaveID, c_szSaveID, sizeof(m_Config.SaveID) - 1);
}

CPythonSystem::TConfig* CPythonSystem::GetConfig()
{
	return &m_Config;
}

void CPythonSystem::SetConfig(TConfig* pNewConfig)
{
	m_Config = *pNewConfig;
}

void CPythonSystem::SetDefaultConfig()
{
	memset(&m_Config, 0, sizeof(m_Config));

	m_Config.width = 1280;
	m_Config.height = 720;
	m_Config.bpp = 32;
	m_Config.frequency = 60;
#ifdef ENABLE_FPS_SYSTEM_LIMIT_REWORK
	m_Config.frequency = g_fGameFPS < 60 ? 60 : g_fGameFPS;
#else
	m_Config.frequency = 60;
#endif
	m_Config.bWindowed = false;

	m_Config.is_software_cursor = false;
	m_Config.is_object_culling = true;
	m_Config.iDistance = 3;

	m_Config.gamma = 5;
	m_Config.music_volume = 1.0f;
	m_Config.voice_volume = 5;

	m_Config.bDecompressDDS = 0;
	m_Config.bSoftwareTiling = 0;
	m_Config.iShadowLevel = 5;
	m_Config.bViewChat = true;

	m_Config.bAlwaysShowName = DEFAULT_VALUE_ALWAYS_SHOW_NAME;

	m_Config.bShowDamage = true;
	m_Config.bShowSalesText = true;
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
	m_Config.bShowMobAIFlag = true;
#endif
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBLEVEL)
	m_Config.bShowMobLevel = true;
#endif
#ifdef ENABLE_OUTLINED_NAMES
	m_Config.bNamesOutline = true;
#endif
#ifdef ENABLE_HIDE_AFFECT_ICONS
	m_Config.bShowAffectIcons = true;
#endif
#ifdef ENABLE_PERSPECTIVE_VIEW
	m_Config.fField = 0.0f;
#endif
#ifdef ENABLE_HIDE_HIGHLIGHT
	m_Config.bShowHighlightEffect = true;
#endif
#ifdef ENABLE_HIDE_MOB_SYSTEM
	memset(&m_Config.bHideMobs, false, sizeof(m_Config.bHideMobs));
#endif
#ifdef ENABLE_ANIMATION_SELECT
	m_Config.iAnimation = 5;
#endif
#ifdef ENABLE_FONT_SELECT
	m_Config.iFontSelected = 0;
#endif
#ifdef ENABLE_HIDE_EFFECTS
	m_Config.bEffects = false;
#endif
#ifdef ENABLE_HIDE_TOOLTIP_EMOJI
	m_Config.bEmoji = true;
#endif
#ifdef ENABLE_METIN_SCALE
	m_Config.fStoneScale = 0.0f;
#endif
#ifdef ENABLE_DAMAGE_SIZE_SCALE
	m_Config.fDamageTextureScale = 0.0f;
#endif
#ifdef ENABLE_SKYBOX_SELECT
	m_Config.iSkyBoxSelected = 0;
#endif
#ifdef ENABLE_RANGE_ENTITY_OPTIMISATION
	m_Config.bEntityRange = ENTITY_FAR;
#endif
#ifdef ENABLE_AREA_OPTIMISATION
	m_Config.fLoadingDistance = 0.0f;
#endif
#ifdef ENABLE_SELECT_DAMAGE_TYPE
	m_Config.iDamageType = 0;
	m_Config.bDamageRenewal = false;
#endif
#ifdef ENABLE_EVENT_MANAGER
	m_Config.bHideEventImage = true;
#endif
#ifdef ENABLE_LOADING_WINDOW_RENEWAL
	m_Config.bAnimatedLoading = true;
#endif
}

bool CPythonSystem::IsWindowed()
{
	return m_Config.bWindowed;
}

bool CPythonSystem::IsViewChat()
{
	return m_Config.bViewChat;
}

void CPythonSystem::SetViewChatFlag(int iFlag)
{
	m_Config.bViewChat = iFlag == 1 ? true : false;
}

bool CPythonSystem::IsAlwaysShowName()
{
	return m_Config.bAlwaysShowName;
}

void CPythonSystem::SetAlwaysShowNameFlag(int iFlag)
{
	m_Config.bAlwaysShowName = iFlag == 1 ? true : false;
}

bool CPythonSystem::IsShowDamage()
{
	return m_Config.bShowDamage;
}

void CPythonSystem::SetShowDamageFlag(int iFlag)
{
	m_Config.bShowDamage = iFlag == 1 ? true : false;
}

bool CPythonSystem::IsShowSalesText()
{
	return m_Config.bShowSalesText;
}

void CPythonSystem::SetShowSalesTextFlag(int iFlag)
{
	m_Config.bShowSalesText = iFlag == 1 ? true : false;
}

#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
bool CPythonSystem::IsShowMobAIFlag()
{
	return m_Config.bShowMobAIFlag;
}

void CPythonSystem::SetShowMobAIFlagFlag(int iFlag)
{
	m_Config.bShowMobAIFlag = iFlag == 1 ? true : false;
}
#endif
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBLEVEL)
bool CPythonSystem::IsShowMobLevel()
{
	return m_Config.bShowMobLevel;
}

void CPythonSystem::SetShowMobLevelFlag(int iFlag)
{
	m_Config.bShowMobLevel = iFlag == 1 ? true : false;
}
#endif

bool CPythonSystem::IsAutoTiling()
{
	if (m_Config.bSoftwareTiling == 0)
		return true;

	return false;
}

void CPythonSystem::SetSoftwareTiling(bool isEnable)
{
	if (isEnable)
		m_Config.bSoftwareTiling = 1;
	else
		m_Config.bSoftwareTiling = 2;
}

bool CPythonSystem::IsSoftwareTiling()
{
	if (m_Config.bSoftwareTiling == 1)
		return true;

	return false;
}

bool CPythonSystem::IsUseDefaultIME()
{
	return m_Config.bUseDefaultIME;
}

bool CPythonSystem::LoadConfig()
{
	FILE* fp = NULL;

	if (NULL == (fp = fopen("metin2.cfg", "rt")))
		return false;

	char buf[256];
	char command[256];
	char value[256];

	while (fgets(buf, 256, fp))
	{
		if (sscanf(buf, " %s %s\n", command, value) == EOF)
			break;

		//@lightwork correction 445 start
		if (!stricmp(command, "WIDTH"))
		{
			if (atoi(value) < 800)
				m_Config.width = 800;
			else
				m_Config.width = atoi(value);
		}
		else if (!stricmp(command, "HEIGHT"))
		{
			if (atoi(value) < 600)
				m_Config.height = 600;
			else
				m_Config.height = atoi(value);
		}
		//@lightwork correction 445 end
		else if (!stricmp(command, "BPP"))
			m_Config.bpp = atoi(value);
		else if (!stricmp(command, "FREQUENCY"))
			m_Config.frequency = atoi(value);
		else if (!stricmp(command, "SOFTWARE_CURSOR"))
			m_Config.is_software_cursor = atoi(value) ? true : false;
		else if (!stricmp(command, "OBJECT_CULLING"))
			m_Config.is_object_culling = atoi(value) ? true : false;
		else if (!stricmp(command, "VISIBILITY"))
			m_Config.iDistance = atoi(value);
		else if (!stricmp(command, "MUSIC_VOLUME"))
			m_Config.music_volume = atof(value);
		else if (!stricmp(command, "VOICE_VOLUME"))
			m_Config.voice_volume = (BYTE)atoi(value);

		else if (!stricmp(command, "GAMMA"))
			m_Config.gamma = atoi(value);
		else if (!stricmp(command, "IS_SAVE_ID"))
			m_Config.isSaveID = atoi(value);
		else if (!stricmp(command, "SAVE_ID"))
			strncpy(m_Config.SaveID, value, 20);
		else if (!stricmp(command, "WINDOWED"))
		{
			m_Config.bWindowed = atoi(value) == 1 ? true : false;
		}
		else if (!stricmp(command, "USE_DEFAULT_IME"))
			m_Config.bUseDefaultIME = atoi(value) == 1 ? true : false;
		else if (!stricmp(command, "SOFTWARE_TILING"))
			m_Config.bSoftwareTiling = atoi(value);
		else if (!stricmp(command, "SHADOW_LEVEL"))
			m_Config.iShadowLevel = atoi(value);
		else if (!stricmp(command, "DECOMPRESSED_TEXTURE"))
			m_Config.bDecompressDDS = atoi(value) == 1 ? true : false;
		else if (!stricmp(command, "VIEW_CHAT"))
			m_Config.bViewChat = atoi(value) == 1 ? true : false;

		else if (!stricmp(command, "ALWAYS_VIEW_NAME"))
		{
			m_Config.bAlwaysShowName = atoi(value) == 1 ? true : false;
		}

		else if (!stricmp(command, "SHOW_DAMAGE"))
			m_Config.bShowDamage = atoi(value) == 1 ? true : false;
		else if (!stricmp(command, "SHOW_SALESTEXT"))
			m_Config.bShowSalesText = atoi(value) == 1 ? true : false;
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
		else if (!stricmp(command, "SHOW_MOBAIFLAG"))
			m_Config.bShowMobAIFlag = atoi(value) == 1 ? true : false;
#endif
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBLEVEL)
		else if (!stricmp(command, "SHOW_MOBLEVEL"))
			m_Config.bShowMobLevel = atoi(value) == 1 ? true : false;
#endif
#ifdef ENABLE_OUTLINED_NAMES
		else if (!stricmp(command, "TEXT_OUTLINE"))
		{
			m_Config.bNamesOutline = atoi(value) == 1 ? true : false;
		}
#endif
#ifdef ENABLE_HIDE_AFFECT_ICONS
		else if (!stricmp(command, "AFFECT_ICONS"))
		{
			m_Config.bShowAffectIcons = atoi(value) == 1 ? true : false;
		}
#endif
#ifdef ENABLE_PERSPECTIVE_VIEW
		else if (!stricmp(command, "FIELD_OF_VIEW_RATE"))
		{
			m_Config.fField = atof(value);
		}
#endif
#ifdef ENABLE_HIDE_HIGHLIGHT
		else if (!stricmp(command, "HIGHLIGHT_ANIMATION"))
		{
			m_Config.bShowHighlightEffect = atoi(value) == 1 ? true : false;
		}
#endif
#ifdef ENABLE_HIDE_MOB_SYSTEM
		else if (!stricmp(command, "HIDE_PETS"))
		{
			m_Config.bHideMobs[HIDE_PET] = atoi(value) == 1 ? true : false;
		}
		else if (!stricmp(command, "HIDE_MOUNTS"))
		{
			m_Config.bHideMobs[HIDE_MOUNT] = atoi(value) == 1 ? true : false;
		}
		else if (!stricmp(command, "HIDE_SHOPS"))
		{
			m_Config.bHideMobs[HIDE_SHOP] = atoi(value) == 1 ? true : false;
		}
		else if (!stricmp(command, "HIDE_NPC"))
		{
			m_Config.bHideMobs[HIDE_NPC] = atoi(value) == 1 ? true : false;
		}
#endif
#ifdef ENABLE_ANIMATION_SELECT
		else if (!stricmp(command, "ANIMATION_TYPE"))
		{
			m_Config.iAnimation = atoi(value);
		}
#endif
#ifdef ENABLE_FONT_SELECT
		else if (!stricmp(command, "FONT_TYPE"))
		{
			m_Config.iFontSelected = atoi(value);
		}
#endif
#ifdef ENABLE_HIDE_EFFECTS
		else if (!stricmp(command, "HIDE_EFFECTS"))
		{
			m_Config.bEffects = atoi(value) == 1 ? true : false;
		}
#endif
#ifdef ENABLE_HIDE_TOOLTIP_EMOJI
		else if (!stricmp(command, "HIDE_TOOLTIP_EMOJIS"))
		{
			m_Config.bEmoji = atoi(value) == 1 ? true : false;
		}
#endif
#ifdef ENABLE_METIN_SCALE
		else if (!stricmp(command, "METINSTONE_SCALE_RATE"))
		{
			m_Config.fStoneScale = atof(value);
		}
#endif
#ifdef ENABLE_DAMAGE_SIZE_SCALE
		else if (!stricmp(command, "DAMAGE_TEXTURE_SCALE_RATE"))
		{
			m_Config.fDamageTextureScale = atof(value);
		}
#endif
#ifdef ENABLE_SKYBOX_SELECT
		else if (!stricmp(command, "SELECTED_SKYBOX_TYPE"))
		{
			m_Config.iSkyBoxSelected = atoi(value);
		}
#endif
#ifdef ENABLE_RANGE_ENTITY_OPTIMISATION
		else if (!stricmp(command, "ENTITY_SHOW_DISTANCE"))
		{
			m_Config.bEntityRange = atoi(value);
		}
#endif
#ifdef ENABLE_AREA_OPTIMISATION
		else if (!stricmp(command, "MAP_LOADING_DISTANCE"))
		{
			m_Config.fLoadingDistance = atof(value);
		}
#endif
#ifdef ENABLE_SELECT_DAMAGE_TYPE
		else if (!stricmp(command, "DAMAGE_TYPE"))
		{
			m_Config.iDamageType = atoi(value);
		}
		else if (!stricmp(command, "DAMAGE_TYPE_RENEWED"))
		{
			m_Config.bDamageRenewal = atoi(value) == 1 ? true : false;
		}
#endif
#ifdef ENABLE_EVENT_MANAGER
		else if (!stricmp(command, "HIDE_EVENT_IMAGE"))
		{
			m_Config.bHideEventImage = atoi(value) == 1 ? true : false;
		}
#endif
#ifdef ENABLE_LOADING_WINDOW_RENEWAL
		else if (!stricmp(command, "ANIMATED_LOADING"))
		{
			m_Config.bAnimatedLoading = atoi(value) == 1 ? true : false;
		}
#endif
	}

	if (m_Config.bWindowed)
	{
		unsigned screen_width = GetSystemMetrics(SM_CXFULLSCREEN);
		unsigned screen_height = GetSystemMetrics(SM_CYFULLSCREEN);

		if (m_Config.width >= screen_width)
		{
			m_Config.width = screen_width;
		}
#ifdef ENABLE_FIX_HEIGHT_TASKBAR_COLLISION
		if (m_Config.height >= screen_height)
		{
			int config_height = m_Config.height;
			int difference = (config_height - screen_height) + 7;
			m_Config.height = config_height - difference;
		}
#else
		if (m_Config.height >= screen_height)
		{
			m_Config.height = screen_height;
		}
#endif
	}

	m_OldConfig = m_Config;

	fclose(fp);

	return true;
}

bool CPythonSystem::SaveConfig()
{
	FILE* fp;

	if (NULL == (fp = fopen("metin2.cfg", "wt")))
		return false;

	fprintf(fp, "WIDTH						%d\n"
		"HEIGHT						%d\n"
		"BPP						%d\n"
		"FREQUENCY					%d\n"
		"SOFTWARE_CURSOR			%d\n"
		"OBJECT_CULLING				%d\n"
		"VISIBILITY					%d\n"
		"MUSIC_VOLUME				%.3f\n"
		"VOICE_VOLUME				%d\n"
		"GAMMA						%d\n"
		"IS_SAVE_ID					%d\n"
		"SAVE_ID					%s\n"
		"DECOMPRESSED_TEXTURE		%d\n",
		m_Config.width,
		m_Config.height,
		m_Config.bpp,
		m_Config.frequency,
		m_Config.is_software_cursor,
		m_Config.is_object_culling,
		m_Config.iDistance,
		m_Config.music_volume,
		m_Config.voice_volume,
		m_Config.gamma,
		m_Config.isSaveID,
		m_Config.SaveID,
		m_Config.bDecompressDDS);

	if (m_Config.bWindowed == 1)
		fprintf(fp, "WINDOWED				%d\n", m_Config.bWindowed);
	if (m_Config.bViewChat == 0)
		fprintf(fp, "VIEW_CHAT				%d\n", m_Config.bViewChat);
	if (m_Config.bAlwaysShowName != DEFAULT_VALUE_ALWAYS_SHOW_NAME)
		fprintf(fp, "ALWAYS_VIEW_NAME		%d\n", m_Config.bAlwaysShowName);

	if (m_Config.bShowDamage == 0)
		fprintf(fp, "SHOW_DAMAGE		%d\n", m_Config.bShowDamage);
	if (m_Config.bShowSalesText == 0)
		fprintf(fp, "SHOW_SALESTEXT		%d\n", m_Config.bShowSalesText);
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
	if (m_Config.bShowMobAIFlag == 0)
		fprintf(fp, "SHOW_MOBAIFLAG		%d\n", m_Config.bShowMobAIFlag);
#endif
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBLEVEL)
	if (m_Config.bShowMobLevel == 0)
		fprintf(fp, "SHOW_MOBLEVEL		%d\n", m_Config.bShowMobLevel);
#endif
	fprintf(fp, "USE_DEFAULT_IME		%d\n", m_Config.bUseDefaultIME);
	fprintf(fp, "SOFTWARE_TILING		%d\n", m_Config.bSoftwareTiling);
	fprintf(fp, "SHADOW_LEVEL			%d\n", m_Config.iShadowLevel);
#ifdef ENABLE_OUTLINED_NAMES
	fprintf(fp, "TEXT_OUTLINE			%d\n", m_Config.bNamesOutline);
#endif
#ifdef ENABLE_HIDE_AFFECT_ICONS
	fprintf(fp, "AFFECT_ICONS			%d\n", m_Config.bShowAffectIcons);
#endif
#ifdef ENABLE_PERSPECTIVE_VIEW
	fprintf(fp, "FIELD_OF_VIEW_RATE		%.2f\n", m_Config.fField);
#endif
#ifdef ENABLE_HIDE_HIGHLIGHT
	fprintf(fp, "HIGHLIGHT_ANIMATION	%d\n", m_Config.bShowHighlightEffect);
#endif
#ifdef ENABLE_HIDE_MOB_SYSTEM
	fprintf(fp, "HIDE_PETS				%d\n", m_Config.bHideMobs[HIDE_PET]);
	fprintf(fp, "HIDE_MOUNTS			%d\n", m_Config.bHideMobs[HIDE_MOUNT]);
	fprintf(fp, "HIDE_SHOPS				%d\n", m_Config.bHideMobs[HIDE_SHOP]);
	fprintf(fp, "HIDE_NPC				%d\n", m_Config.bHideMobs[HIDE_NPC]);
#endif
#ifdef ENABLE_ANIMATION_SELECT
	fprintf(fp, "ANIMATION_TYPE			%d\n", m_Config.iAnimation);
#endif
#ifdef ENABLE_FONT_SELECT
	fprintf(fp, "FONT_TYPE				%d\n", m_Config.iFontSelected);
#endif
#ifdef ENABLE_HIDE_EFFECTS
	fprintf(fp, "HIDE_EFFECTS			%d\n", m_Config.bEffects);
#endif
#ifdef ENABLE_HIDE_TOOLTIP_EMOJI
	fprintf(fp, "HIDE_TOOLTIP_EMOJIS	%d\n", m_Config.bEmoji);
#endif
#ifdef ENABLE_METIN_SCALE
	fprintf(fp, "METINSTONE_SCALE_RATE	%.1f\n", m_Config.fStoneScale);
#endif
#ifdef ENABLE_DAMAGE_SIZE_SCALE
	fprintf(fp, "DAMAGE_TEXTURE_SCALE_RATE	%.1f\n", m_Config.fDamageTextureScale);
#endif
#ifdef ENABLE_SKYBOX_SELECT
	fprintf(fp, "SELECTED_SKYBOX_TYPE	%d\n", m_Config.iSkyBoxSelected);
#endif
#ifdef ENABLE_RANGE_ENTITY_OPTIMISATION
	fprintf(fp, "ENTITY_SHOW_DISTANCE	%d\n", m_Config.bEntityRange);
#endif
#ifdef ENABLE_AREA_OPTIMISATION
	fprintf(fp, "MAP_LOADING_DISTANCE	%.1f\n", m_Config.fLoadingDistance);
#endif
#ifdef ENABLE_SELECT_DAMAGE_TYPE
	fprintf(fp, "DAMAGE_TYPE				%d\n", m_Config.iDamageType);
	fprintf(fp, "DAMAGE_TYPE_RENEWED				%d\n", m_Config.bDamageRenewal);
#endif
#ifdef ENABLE_EVENT_MANAGER
	fprintf(fp, "HIDE_EVENT_IMAGE			%d\n", m_Config.bHideEventImage);
#endif
#ifdef ENABLE_LOADING_WINDOW_RENEWAL
	fprintf(fp, "ANIMATED_LOADING			%d\n", m_Config.bAnimatedLoading);
#endif
	fprintf(fp, "\n");

	fclose(fp);
	return true;
}

bool CPythonSystem::LoadInterfaceStatus()
{
	FILE* File;
	File = fopen("interface.cfg", "rb");

	if (!File)
		return false;

	fread(m_WindowStatus, 1, sizeof(TWindowStatus) * WINDOW_MAX_NUM, File);
	fclose(File);
	return true;
}

void CPythonSystem::SaveInterfaceStatus()
{
	if (!m_poInterfaceHandler)
		return;

	PyCallClassMemberFunc(m_poInterfaceHandler, "OnSaveInterfaceStatus", Py_BuildValue("()"));

	FILE* File;

	File = fopen("interface.cfg", "wb");

	if (!File)
	{
		TraceError("Cannot open interface.cfg");
		return;
	}

	fwrite(m_WindowStatus, 1, sizeof(TWindowStatus) * WINDOW_MAX_NUM, File);
	fclose(File);
}

bool CPythonSystem::isInterfaceConfig()
{
	return m_isInterfaceConfig;
}

const CPythonSystem::TWindowStatus& CPythonSystem::GetWindowStatusReference(int iIndex)
{
	return m_WindowStatus[iIndex];
}

void CPythonSystem::ApplyConfig()
{
	if (m_OldConfig.gamma != m_Config.gamma)
	{
		float val = 1.0f;

		switch (m_Config.gamma)
		{
		case 0: val = 0.4f;	break;
		case 1: val = 0.7f; break;
		case 2: val = 1.0f; break;
		case 3: val = 1.2f; break;
		case 4: val = 1.4f; break;
		}

		CPythonGraphic::Instance().SetGamma(val);
	}

	if (m_OldConfig.is_software_cursor != m_Config.is_software_cursor)
	{
		if (m_Config.is_software_cursor)
			CPythonApplication::Instance().SetCursorMode(CPythonApplication::CURSOR_MODE_SOFTWARE);
		else
			CPythonApplication::Instance().SetCursorMode(CPythonApplication::CURSOR_MODE_HARDWARE);
	}

	m_OldConfig = m_Config;
}

void CPythonSystem::Clear()
{
	SetInterfaceHandler(NULL);
}

CPythonSystem::CPythonSystem()
{
	memset(&m_Config, 0, sizeof(TConfig));

	m_poInterfaceHandler = NULL;

	SetDefaultConfig();

	LoadConfig();

	if (LoadInterfaceStatus())
		m_isInterfaceConfig = true;
	else
		m_isInterfaceConfig = false;
}

CPythonSystem::~CPythonSystem()
{
	assert(m_poInterfaceHandler == NULL && "CPythonSystem MUST CLEAR!");
}

#ifdef ENABLE_HIDE_MOB_SYSTEM
void CPythonSystem::SetHiddenState(int type, bool state)
{
	m_Config.bHideMobs[type] = state;
	CPythonCharacterManager::Instance().UpdateTextTail(type, state);

}

bool CPythonSystem::GetHiddenState(int type)
{
	return m_Config.bHideMobs[type];
}
#endif

#ifdef ENABLE_ANIMATION_SELECT
void CPythonSystem::SetAnimation(BYTE iFlag)
{
	m_Config.iAnimation = iFlag;
	AnimationDataWrite();
}

BYTE CPythonSystem::GetAnimation()
{
	return m_Config.iAnimation;
}

void CPythonSystem::AnimationDataWrite()
{
	switch (m_Config.iAnimation)
	{
	case 1: {m_strAnimations[0] = std::make_pair("cubicOut", 200 * (g_fGameFPS / 90)); m_strAnimations[1] = std::make_pair("quadraticOut", 100 * (g_fGameFPS / 90)); break; }
	case 2: {m_strAnimations[0] = std::make_pair("cubicOut", 180 * (g_fGameFPS / 90)); m_strAnimations[1] = std::make_pair("circularOut", 115 * (g_fGameFPS / 90)); break; }
	case 3: {m_strAnimations[0] = std::make_pair("exponentialIn", 50 * (g_fGameFPS / 90)); m_strAnimations[1] = std::make_pair("exponentialOut", 120 * (g_fGameFPS / 90)); break; }
	case 4: {m_strAnimations[0] = std::make_pair("elasticIn", 60 * (g_fGameFPS / 90)); m_strAnimations[1] = std::make_pair("elasticOut", 120 * (g_fGameFPS / 90)); break; }
	case 5: {m_strAnimations[0] = std::make_pair("backIn", 70 * (g_fGameFPS / 90)); m_strAnimations[1] = std::make_pair("backOut", 120 * (g_fGameFPS / 90)); break; }
	case 6: {m_strAnimations[0] = std::make_pair("cubicOut", 175 * (g_fGameFPS / 90)); m_strAnimations[1] = std::make_pair("cubicOut", 120 * (g_fGameFPS / 90)); break; }
	default: {m_strAnimations[0] = std::make_pair("cubicOut", 160 * (g_fGameFPS / 90)); m_strAnimations[1] = std::make_pair("exponentialOut", 70 * (g_fGameFPS / 90)); break; }
	}
}

std::pair<std::string, float> CPythonSystem::GetCurrentAnimation(bool show)
{
	if (m_strAnimations[0].first.length() < 1 || m_strAnimations[1].first.length() < 1)
	{
		AnimationDataWrite();
	}
	return show ? m_strAnimations[1] : m_strAnimations[0];
}
#endif

#ifdef ENABLE_FONT_SELECT
void CPythonSystem::SetFontType(BYTE iFlag)
{
	m_Config.iFontSelected = iFlag;
}

BYTE CPythonSystem::GetFontType()
{
	if (m_Config.iFontSelected > 3) {
		m_Config.iFontSelected = 0;
	}
	return m_Config.iFontSelected;
}
#endif

#ifdef ENABLE_SKYBOX_SELECT
void CPythonSystem::SetSkyBoxType(BYTE iFlag)
{
	m_Config.iSkyBoxSelected = iFlag;
}

BYTE CPythonSystem::GetSkyBox()
{
	return m_Config.iSkyBoxSelected;
}
#endif