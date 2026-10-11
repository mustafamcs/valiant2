#pragma once

#ifdef ENABLE_HIDE_MOB_SYSTEM
enum EHiddenTypes
{
	HIDE_NPC,
	HIDE_MOUNT,
	HIDE_PET,
	HIDE_SHOP,
	HIDE_MAX
};
#endif

#ifdef ENABLE_RANGE_ENTITY_OPTIMISATION
enum EntityRange
{
	ENTITY_CLOSE = 2500,
	ENTITY_MIDDLE = 4500,
	ENTITY_FAR = 6500,
};
#endif

class CPythonSystem : public CSingleton<CPythonSystem>
{
public:
	enum EWindow
	{
		WINDOW_STATUS,
		WINDOW_INVENTORY,
		WINDOW_ABILITY,
		WINDOW_SOCIETY,
		WINDOW_JOURNAL,
		WINDOW_COMMAND,

		WINDOW_QUICK,
		WINDOW_GAUGE,
		WINDOW_MINIMAP,
		WINDOW_CHAT,

		WINDOW_MAX_NUM,
	};
	enum
	{
		FREQUENCY_MAX_NUM = 30,
		RESOLUTION_MAX_NUM = 100
	};

	typedef struct SResolution
	{
		DWORD	width;
		DWORD	height;
		DWORD	bpp;		// bits per pixel (high-color = 16bpp, true-color = 32bpp)

		DWORD	frequency[20];
		BYTE	frequency_count;
	} TResolution;

	typedef struct SWindowStatus
	{
		int		isVisible;
		int		isMinimized;

		int		ixPosition;
		int		iyPosition;
		int		iHeight;
	} TWindowStatus;

	typedef struct SConfig
	{
		DWORD			width;
		DWORD			height;
		DWORD			bpp;
		DWORD			frequency;

		bool			is_software_cursor;
		bool			is_object_culling;
		int				iDistance;
		int				iShadowLevel;
		float			music_volume;
		BYTE			voice_volume;
		int				gamma;

		int				isSaveID;
		char			SaveID[20];

		bool			bWindowed;
		bool			bDecompressDDS;
		bool			bUseDefaultIME;
		BYTE			bSoftwareTiling;
		bool			bViewChat;
		bool			bAlwaysShowName;
		bool			bShowDamage;
		bool			bShowSalesText;
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
		bool			bShowMobAIFlag;
#endif
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBLEVEL)
		bool			bShowMobLevel;
#endif
#ifdef ENABLE_OUTLINED_NAMES
		bool			bNamesOutline;
#endif
#ifdef ENABLE_HIDE_AFFECT_ICONS
		bool			bShowAffectIcons;
#endif
#ifdef ENABLE_PERSPECTIVE_VIEW
		float			fField;
#endif
#ifdef ENABLE_HIDE_HIGHLIGHT
		bool			bShowHighlightEffect;
#endif
#ifdef ENABLE_HIDE_MOB_SYSTEM
		bool			bHideMobs[HIDE_MAX];
#endif
#ifdef ENABLE_ANIMATION_SELECT
		BYTE			iAnimation;
#endif
#ifdef ENABLE_FONT_SELECT
		BYTE			iFontSelected;
#endif
#ifdef ENABLE_HIDE_EFFECTS
		bool			bEffects;
#endif
#ifdef ENABLE_HIDE_TOOLTIP_EMOJI
		bool			bEmoji;
#endif
#ifdef ENABLE_METIN_SCALE
		float			fStoneScale;
#endif
#ifdef ENABLE_DAMAGE_SIZE_SCALE
		float			fDamageTextureScale;
#endif
#ifdef ENABLE_SKYBOX_SELECT
		BYTE			iSkyBoxSelected;
#endif
#ifdef ENABLE_RANGE_ENTITY_OPTIMISATION
		DWORD			bEntityRange;
#endif
#ifdef ENABLE_AREA_OPTIMISATION
		float			fLoadingDistance;
#endif
#ifdef ENABLE_SELECT_DAMAGE_TYPE
		BYTE			iDamageType;
		bool			bDamageRenewal;
#endif
#ifdef ENABLE_EVENT_MANAGER
		bool			bHideEventImage;
#endif
#ifdef ENABLE_LOADING_WINDOW_RENEWAL
		bool			bAnimatedLoading;
#endif
	} TConfig;

public:
	CPythonSystem();
	virtual ~CPythonSystem();

	void Clear();
	void SetInterfaceHandler(PyObject* poHandler);
	void DestroyInterfaceHandler();

	// Config
	void							SetDefaultConfig();
	bool							LoadConfig();
	bool							SaveConfig();
	void							ApplyConfig();
	void							SetConfig(TConfig* set_config);
	TConfig* GetConfig();
	// Interface
	bool							LoadInterfaceStatus();
	void							SaveInterfaceStatus();
	bool							isInterfaceConfig();
	const TWindowStatus& GetWindowStatusReference(int iIndex);

	DWORD							GetWidth();
	DWORD							GetHeight();
	DWORD							GetBPP();
	DWORD							GetFrequency();
	bool							IsSoftwareCursor();
	bool							IsWindowed();
	bool							IsViewChat();
	bool							IsAlwaysShowName();
	float							GetMusicVolume();
	int								GetSoundVolume();
	void							SetMusicVolume(float fVolume);
	void							SetSoundVolumef(float fVolume);
	bool							IsShowDamage();
	bool							IsShowSalesText();
	bool							IsUseDefaultIME();
	bool							IsAutoTiling();
	bool							IsSoftwareTiling();
	void							SetSoftwareTiling(bool isEnable);
	void							SetViewChatFlag(int iFlag);
	void							SetAlwaysShowNameFlag(int iFlag);
	void							SetShowDamageFlag(int iFlag);
	void							SetShowSalesTextFlag(int iFlag);
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
	bool							IsShowMobAIFlag();
	void							SetShowMobAIFlagFlag(int iFlag);
#endif
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBLEVEL)
	bool							IsShowMobLevel();
	void							SetShowMobLevelFlag(int iFlag);
#endif

	// Window
	void							SaveWindowStatus(int iIndex, int iVisible, int iMinimized, int ix, int iy, int iHeight);

	// SaveID
	int								IsSaveID();
	const char* GetSaveID();
	void							SetSaveID(int iValue, const char* c_szSaveID);

	/// Display
	void							GetDisplaySettings();

	int								GetResolutionCount();
	int								GetFrequencyCount(int index);
	bool							GetResolution(int index, OUT DWORD* width, OUT DWORD* height, OUT DWORD* bpp);
	bool							GetFrequency(int index, int freq_index, OUT DWORD* frequncy);
	int								GetResolutionIndex(DWORD width, DWORD height, DWORD bpp);
	int								GetFrequencyIndex(int res_index, DWORD frequency);
	bool							isViewCulling();


	int								GetDistance();
	int								GetShadowLevel();
	void							SetShadowLevel(unsigned int level);

#ifdef ENABLE_OUTLINED_NAMES
	bool							GetNamesType();
	void							SetNamesType(int value);
#endif

#ifdef ENABLE_HIDE_AFFECT_ICONS
	bool							IsAffectIconShow();
	void							SetEffectIconShow(int value);
#endif

#ifdef ENABLE_PERSPECTIVE_VIEW
	float							GetFieldPerspective();
	void							SetFieldPerspective(float fValue);
#endif

#ifdef ENABLE_HIDE_HIGHLIGHT
	bool							IsHighlightShow();
	void							SetHighlightShow(int value);
#endif

#ifdef ENABLE_HIDE_MOB_SYSTEM
	void							SetHiddenState(int type, bool state);
	bool							GetHiddenState(int type);
#endif
#ifdef ENABLE_FONT_SELECT
	void							SetFontType(BYTE iFlag);
	BYTE							GetFontType();
#endif

#ifdef ENABLE_RANGE_ENTITY_OPTIMISATION
	DWORD							GetEntityRange() { return m_Config.bEntityRange; }
	void							SetShowOnlyEntityInRange(DWORD value) { m_Config.bEntityRange = value; }
#endif

#ifdef ENABLE_SELECT_DAMAGE_TYPE
	void							SetDamageType(BYTE iFlag) { m_Config.iDamageType = iFlag; }
	BYTE							GetDamageType() { return m_Config.iDamageType; }

	void							SetDamageTypeRenewal(BYTE iFlag) { m_Config.bDamageRenewal = iFlag; }
	BYTE							GetDamageTypeRenewal() { return m_Config.bDamageRenewal; }
#endif

#ifdef ENABLE_HIDE_TOOLTIP_EMOJI
	bool							GetEmojiStatus();
	void							SetEmojiStatus(int value);
#endif

#ifdef ENABLE_METIN_SCALE
	float							GetMetinstoneScale();
	void							SetMetinstoneScale(float fValue);
#endif

#ifdef ENABLE_DAMAGE_SIZE_SCALE
	float							GetDamageTextureScale();
	void							SetDamageTextureScale(float fValue);
#endif

#ifdef ENABLE_FONT_SELECT
	void							SetSkyBoxType(BYTE iFlag);
	BYTE							GetSkyBox();
#endif

#ifdef ENABLE_HIDE_EFFECTS
	bool							IsEffectActive();
	void							SetEffectActive(int value);
#endif

#ifdef ENABLE_AREA_OPTIMISATION
	float							GetLoadingDistance() { return m_Config.fLoadingDistance; }
	void							SetLoadingDistance(float fValue) { m_Config.fLoadingDistance = fValue; }
#endif

#ifdef ENABLE_EVENT_MANAGER
	bool							IsEventIconShow() { return m_Config.bHideEventImage; }
	void							SetEventIconShow(int value) { m_Config.bHideEventImage = value; }
#endif

#ifdef ENABLE_LOADING_WINDOW_RENEWAL
	bool							IsLoadingAnimated() { return m_Config.bAnimatedLoading; }
	void							SetLoadingWindowType(int value) { m_Config.bAnimatedLoading = value; }
#endif

protected:
	TResolution						m_ResolutionList[RESOLUTION_MAX_NUM];
	int								m_ResolutionCount;

	TConfig							m_Config;
	TConfig							m_OldConfig;

	bool							m_isInterfaceConfig;
	PyObject* m_poInterfaceHandler;
	TWindowStatus					m_WindowStatus[WINDOW_MAX_NUM];
#ifdef ENABLE_ANIMATION_SELECT
public:
	void							SetAnimation(BYTE iFlag);
	BYTE							GetAnimation();
	void							AnimationDataWrite();
	std::pair<std::string, float>	GetCurrentAnimation(bool show);
protected:
	std::pair<std::string, float>	m_strAnimations[2];
#endif

};