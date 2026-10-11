#static
import ui, constInfo, localeInfo, uiScriptLocale

# dynamic
import dbg, player, chat, net, systemSetting, pack, app, background, snd

from _weakref import proxy
blockMode = 0
IMG_DIR = "d:/ymir work/ui/game/gameoption/"

class GameOptionWindow(ui.BoardWithTitleBar):

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
	def Destroy(self):
		self.pvpModeButtonDict={}
		self.blockButtonList=[]
		self.questLetterButtonList=[]
		self.viewChatButtonList = []
		self.nameColorModeButtonList = []
		self.viewTargetBoardButtonList=[]
		self.alwaysShowNameButtonList=[]
		self.showDamageButtonList=[]
		self.showsalesTextButtonList=[]
		self.cameraModeButtonList=[]
		self.fogModeButtonList = []
		if app.WJ_SHOW_MOB_INFO:
			self.showMobInfoButtonList = []
		if app.ENABLE_OUTLINED_NAMES:
			self.showOutlinedNamesList = []
		if app.ENABLE_HIDE_AFFECT_ICONS:
			self.showAffectIconsList = []
		if app.ENABLE_HIDE_HIGHLIGHT:
			self.showHighlightIconList = []
		if app.ENABLE_HIDE_MOB_SYSTEM:
			self.HiddenItemsList=[]
		if app.ENABLE_FONT_SELECT:
			self.FontList=[]
		if app.ENABLE_HIDE_EFFECTS:
			self.showHideEffectList = []
		if app.ENABLE_HIDE_TOOLTIP_EMOJI:
			self.showHideTooltipEmojis = []
		if app.ENABLE_SKYBOX_SELECT:
			self.skyBoxObjects=[]
			self.skyBoxes = [
			"d:/ymir work/environment/sunset_kf.msenv",
			"d:/ymir work/environment/hazysun_kf.msenv", 
			"d:/ymir work/environment/cloudysun_kf.msenv",
			"d:/ymir work/environment/eveningsun_kf.msenv",
			"d:/ymir work/environment/rainyday_kf.msenv",
			"d:/ymir work/environment/overcastday_kf.msenv",
			"d:/ymir work/environment/foggysunset_kf.msenv",
			"d:/ymir work/environment/cloudymonth_kf.msenv"
			]
		if app.ENABLE_SHADER_OPTIONS:
			self.showHideShadows = []
		if app.ENABLE_RANGE_ENTITY_OPTIMISATION:
			self.entitySelectButtons=[]
		if app.ENABLE_SELECT_DAMAGE_TYPE:
			self.damageTypeButtons=[]
			self.damageTypeRenewalButtons=[]

		if app.ENABLE_EVENT_MANAGER:
			self.showEventIconList = []

		if app.ENABLE_LOADING_WINDOW_RENEWAL:
			self.showLoadingTypeList = []

		if app.ENABLE_PERSPECTIVE_VIEW:
			self.cameraPerspective = None
		if app.ENABLE_METIN_SCALE:
			self.stoneScaling = None
		if app.ENABLE_DAMAGE_SIZE_SCALE:
			self.damageScaling = None

		if app.ENABLE_ANIMATION_SELECT:
			self.animatedWindow = None
			self.animatedWindowInfo = None
			self.currentSelectedAnimation = 0
			self.lastSelectedAnimation = 0

		for j in xrange(10):
			for x in xrange(10):
				if self.children.has_key("optionWindow%d%d"%(j,x)):
					window = self.children["optionWindow%d%d"%(j,x)]
					if window:
						window.Hide()
						window.scrollBar = None
						window.ClearDictionary()
						window.Destroy()
		self.children = {}
		self.Hide()

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.children = {}
		self.Destroy()
		self.__LoadWindow()
		self.SetTitleName(uiScriptLocale.GAMEOPTION_TITLE)
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __LoadWindow(self):
		self.AddFlag("movable")
		self.AddFlag("attach")
		option_data = {
			uiScriptLocale.GAMEOPTION_TITLE:{
				"index": 0,
				uiScriptLocale.CHATTING_SETTING_DEFAULT_TITLE : {"index": 0,},
				localeInfo.OFFLINESHOP_TITLE_OTHER : {"index": 1,},
				"Ses" : {"index": 2,},
			},
			uiScriptLocale.GAMEOPTION_CAT_02:{
			"index": 1,
				uiScriptLocale.CHATTING_SETTING_DEFAULT_TITLE		:	{"index": 0,},
				uiScriptLocale.GAMEOPTION_CAT_02_SUBCAT_1		:	{"index": 1,},
				uiScriptLocale.GAMEOPTION_CAT_02_SUBCAT_2	:	{"index": 2,},
			},
			# uiScriptLocale.GAMEOPTION_CAT_03:{
			# 	"index": 2,
			# 	uiScriptLocale.CHATTING_SETTING_DEFAULT_TITLE:{"index": 0,},
			# },
		}

		for key, optionTitles in option_data.items():
			if self.IsCanContinue(key):
				continue

			if not optionTitles.has_key("index"):
				continue
			optionIndex = optionTitles["index"]

			bg = BackgroundImage()
			bg.SetParent(self)
			bg.AddFlag("attach")
			bg.SetSize(476, 326)
			bg.SetPosition(10, 65)
			bg.Show()
			self.children["bg%d"%optionIndex] = bg

			titleButton = ui.RadioButton()
			titleButton.SetParent(self)

			if optionIndex == 0:
				titleButton.SetUpVisual(IMG_DIR+"cat_title_0.png")
				titleButton.SetOverVisual(IMG_DIR+"cat_title_1.png")
				titleButton.SetDownVisual(IMG_DIR+"cat_title_2.png")
				titleButton.SetPosition(105+(optionIndex*(titleButton.GetWidth()+10)), 39)
			elif optionIndex == len(option_data)-1:
				titleButton.SetUpVisual(IMG_DIR+"cat_title_0.png")
				titleButton.SetOverVisual(IMG_DIR+"cat_title_1.png")
				titleButton.SetDownVisual(IMG_DIR+"cat_title_2.png")
				titleButton.SetPosition(105+(optionIndex*(titleButton.GetWidth()+10)), 39)
			else:
				titleButton.SetUpVisual(IMG_DIR+"cat_title_0.png")
				titleButton.SetOverVisual(IMG_DIR+"cat_title_1.png")
				titleButton.SetDownVisual(IMG_DIR+"cat_title_2.png")
				titleButton.SetPosition(105+(optionIndex*(titleButton.GetWidth()+10)), 39)

			titleButton.SetText(key)
			titleButton.SAFE_SetEvent(self.SetOptionType, optionIndex)
			titleButton.Show()
			self.children["titleBtn%d"%optionIndex] = titleButton

			for keyEx, optionTypes in optionTitles.items():
				if self.IsCanContinue(keyEx):
					continue
				if not optionTypes.has_key("index"):
					continue

				categoryIndex = optionTypes["index"]
				optionCategory = ui.RadioButton()
				optionCategory.SetParent(bg)
				optionCategory.SetUpVisual(IMG_DIR+"category_0.png")
				optionCategory.SetOverVisual(IMG_DIR+"category_1.png")
				optionCategory.SetDownVisual(IMG_DIR+"category_2.png")
				optionCategory.SetPosition(7, 10 + (categoryIndex*(optionCategory.GetHeight() + 5)))
				optionCategory.SAFE_SetEvent(self.SetCategoryType, categoryIndex)
				optionCategory.SetText(keyEx)
				optionCategory.Show()
				self.children["optionCategory%d%d"%(optionIndex,categoryIndex)] = optionCategory
				optionWindow = self.CreateOptionWindow(bg, optionIndex,categoryIndex)
				self.children["optionWindow%d%d"%(optionIndex,categoryIndex)] = optionWindow

		self.SetOptionType(0)
		self.SetSize(8+bg.GetWidth()+10,65+bg.GetHeight()+10)
		self.SetCenterPosition()
		self.UpdateScrollBar()

	def Open(self):
		self.RefreshBlock()
		self.Show()
	def OnPressEscapeKey(self):
		self.Hide()
		return True
	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			btn=buttonList[buttonIndex]
		except IndexError:
			return
		for eachButton in buttonList:
			eachButton.SetUp()
		btn.Down()

	def IsCanContinue(self, dictKey):
		if dictKey == "index":
			return True
		return False

	def SetOptionType(self, optionType):
		self.children["optionType"] = optionType
		for j in xrange(10):
			if self.children.has_key("titleBtn%d"%j):
				titleBtn = self.children["titleBtn%d"%j]
				if j == optionType:
					titleBtn.Down()
				else:
					titleBtn.SetUp()
			if self.children.has_key("bg%d"%j):
				bg = self.children["bg%d"%j]
				if j == optionType:
					bg.Show()
				else:
					bg.Hide()
		self.SetCategoryType(0)

	def SetCategoryType(self, categoryType):
		for j in xrange(3):
			for x in xrange(5):
				if self.children.has_key("optionWindow%d%d" % (j,x)):
					self.children["optionWindow%d%d"%(j,x)].Hide()

		self.children["categoryType"] = categoryType
		currentCategoryType = self.children["optionType"]
		for j in xrange(10):
			if self.children.has_key("optionCategory%d%d"%(currentCategoryType,j)):
				categoryBtn = self.children["optionCategory%d%d"%(currentCategoryType,j)]
				if j == categoryType:
					categoryBtn.Down()
				else:
					categoryBtn.SetUp()

		if self.children.has_key("optionWindow%d%d" % (currentCategoryType,categoryType)):
			self.children["optionWindow%d%d"%(currentCategoryType,categoryType)].Show()

		self.UpdateScrollBar()

	def CreateOptionWindow(self, windowBG, optionIndex, categoryIndex):
		scriptWindow = ui.ScriptWindow()
		scriptWindow.SetParent(windowBG)
		#try:
		fileName = "UIScript/game_option_%d_%d.py"%(optionIndex, categoryIndex)
		pyScrLoader = ui.PythonScriptLoader()
		if pack.Exist(fileName):
			pyScrLoader.LoadScriptFile(scriptWindow, fileName)
			self.LoadCatetoryOptions(scriptWindow, optionIndex, categoryIndex)
		else:
			dbg.TraceError("[GameOption]Can't find script window for optionIndex: %d categoryIndex: %d"%(optionIndex, categoryIndex))

		if scriptWindow.GetWidth() > 0:
		#Auto add scrollbar
			scrollBar = ui.SlimScrollBar()
			scrollBar.SetParent(scriptWindow)
			scrollBar.SetPosition(scriptWindow.GetWidth()-scrollBar.GetWidth()+ 9, 0)
			scrollBar.SetScrollBarSize(scriptWindow.GetHeight()-3)
			scrollBar.Hide()
			scrollBar.SetScrollEvent(ui.__mem_func__(self.UpdateScrollBar))
			scriptWindow.scrollBar = scrollBar
			scriptWindow.OnRunMouseWheel = ui.__mem_func__(self.OnRunMouseWheel)

			scriptChildrens = scriptWindow.Children
			for child in scriptChildrens:
				(_x,_y) = child.GetLocalPosition()
				child.SetPosition(_x,_y, True)

			scriptWindow.Show()
		else:
			scriptWindow.scrollBar = None
		
		return scriptWindow

	def LoadCatetoryOptions(self, scriptWindow, optionIndex, categoryIndex):
		#try:
		GetObject = scriptWindow.GetChild

		if optionIndex == 0:#Game-Options

			if categoryIndex == 0:#General
				self.pvpModeButtonDict[player.PK_MODE_PEACE] = GetObject("pvp_peace")
				self.pvpModeButtonDict[player.PK_MODE_PEACE].SAFE_SetEvent(self.__OnClickPvPModePeaceButton)
				self.pvpModeButtonDict[player.PK_MODE_REVENGE] = GetObject("pvp_revenge")
				self.pvpModeButtonDict[player.PK_MODE_REVENGE].SAFE_SetEvent(self.__OnClickPvPModeRevengeButton)
				self.pvpModeButtonDict[player.PK_MODE_GUILD] = GetObject("pvp_guild")
				self.pvpModeButtonDict[player.PK_MODE_GUILD].SAFE_SetEvent(self.__OnClickPvPModeGuildButton)
				self.pvpModeButtonDict[player.PK_MODE_FREE] = GetObject("pvp_free")
				self.pvpModeButtonDict[player.PK_MODE_FREE].SAFE_SetEvent(self.__OnClickPvPModeFreeButton)
				self.__SetPeacePKMode()
				self.__SetPKMode(player.PK_MODE_PEACE)

				block_exchange_button = GetObject("block_exchange_button")
				block_exchange_button.SetToggleUpEvent(self.__OnClickBlockExchangeButton)
				block_exchange_button.SetToggleDownEvent(self.__OnClickBlockExchangeButton)
				self.blockButtonList.append(block_exchange_button)

				block_party_button = GetObject("block_party_button")
				block_party_button.SetToggleUpEvent(self.__OnClickBlockPartyButton)
				block_party_button.SetToggleDownEvent(self.__OnClickBlockPartyButton)
				self.blockButtonList.append(block_party_button)

				block_guild_button = GetObject("block_guild_button")
				block_guild_button.SetToggleUpEvent(self.__OnClickBlockGuildButton)
				block_guild_button.SetToggleDownEvent(self.__OnClickBlockGuildButton)
				self.blockButtonList.append(block_guild_button)

				block_whisper_button = GetObject("block_whisper_button")
				block_whisper_button.SetToggleUpEvent(self.__OnClickBlockWhisperButton)
				block_whisper_button.SetToggleDownEvent(self.__OnClickBlockWhisperButton)
				self.blockButtonList.append(block_whisper_button)

				block_friend_button = GetObject("block_friend_button")
				block_friend_button.SetToggleUpEvent(self.__OnClickBlockFriendButton)
				block_friend_button.SetToggleDownEvent(self.__OnClickBlockFriendButton)
				self.blockButtonList.append(block_friend_button)

				block_party_request_button = GetObject("block_party_request_button")
				block_party_request_button.SetToggleUpEvent(self.__OnClickBlockPartyRequest)
				block_party_request_button.SetToggleDownEvent(self.__OnClickBlockPartyRequest)
				self.blockButtonList.append(block_party_request_button)

				# if app.ENABLE_TELEPORT_TO_A_FRIEND:
				# 	block_warp_request_button = GetObject("block_warp_request_button")
				# 	block_warp_request_button.SetToggleUpEvent(self.__OnClickBlockWarpRequest)
				# 	block_warp_request_button.SetToggleDownEvent(self.__OnClickBlockWarpRequest)
				# 	self.blockButtonList.append(block_warp_request_button)

				self.viewChatButtonList.append(GetObject("view_chat_on_button"))
				self.viewChatButtonList[0].SAFE_SetEvent(self.__OnClickViewChat)
				self.viewChatButtonList.append(GetObject("view_chat_off_button"))
				self.viewChatButtonList[1].SAFE_SetEvent(self.__OnClickViewChat)
				self.RefreshViewChat()

				self.nameColorModeButtonList.append(GetObject("name_color_normal"))
				self.nameColorModeButtonList[0].SAFE_SetEvent(self.__OnClickNameColorMode)
				self.nameColorModeButtonList.append(GetObject("name_color_empire"))
				self.nameColorModeButtonList[1].SAFE_SetEvent(self.__OnClickNameColorMode)
				self.RefreshNameColor()

				if app.WJ_SHOW_MOB_INFO:
					self.showMobInfoButtonList.append(GetObject("show_mob_level_button"))
					self.showMobInfoButtonList.append(GetObject("show_mob_AI_flag_button"))
					self.showMobInfoButtonList[0].SetToggleUpEvent(self.__OnClickShowMobLevelButton)
					self.showMobInfoButtonList[0].SetToggleDownEvent(self.__OnClickShowMobLevelButton)
					self.showMobInfoButtonList[1].SetToggleUpEvent(self.__OnClickShowMobAIFlagButton)
					self.showMobInfoButtonList[1].SetToggleDownEvent(self.__OnClickShowMobAIFlagButton)
					self.RefreshShowMobInfo()

			elif categoryIndex == 1:#Pickup

				if app.ENABLE_METIN_SCALE:
					stoneScaling = GetObject("stone_scale")
					stoneScaling.SetSliderPos(float(systemSetting.GetMetinstoneScale()))
					stoneScaling.SetEvent(ui.__mem_func__(self.OnStoneScaling))
					self.stoneScaling = stoneScaling

				if app.ENABLE_DAMAGE_SIZE_SCALE:
					damageScaling = GetObject("damage_scale")
					damageScaling.SetSliderPos(float(systemSetting.GetDamageTextureScale()))
					damageScaling.SetEvent(ui.__mem_func__(self.OnDamageScaling))
					self.damageScaling = damageScaling

			elif categoryIndex == 2:#Sound
				self.ctrlSoundVolume = GetObject("sound_volume_controller")
				self.ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()) / 5.0)
				self.ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))
				self.ctrlMusicVolume = GetObject("music_volume_controller")
				self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
				self.ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))

		elif optionIndex == 1:#Graphic-Options
			if categoryIndex == 0:#General
				self.showDamageButtonList.append(GetObject("show_damage_on_button"))
				self.showDamageButtonList[0].SAFE_SetEvent(self.__OnClickShowDamage)
				self.showDamageButtonList.append(GetObject("show_damage_off_button"))
				self.showDamageButtonList[1].SAFE_SetEvent(self.__OnClickShowDamage)
				self.RefreshShowDamage()

				self.cameraModeButtonList.append(GetObject("camera_short"))
				self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraMode)
				self.cameraModeButtonList.append(GetObject("camera_long"))
				self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraMode)
				self.RefreshCameraMode()

				self.fogModeButtonList.append(GetObject("fog_level0"))
				self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFog, 0)
				self.fogModeButtonList.append(GetObject("fog_level1"))
				self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFog, 1)
				self.fogModeButtonList.append(GetObject("fog_level2"))
				self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFog, 2)
				self.RefreshFog()

				if app.ENABLE_PERSPECTIVE_VIEW:
					cameraPerspective = GetObject("fov_controller")
					cameraPerspective.SetSliderPos(float(systemSetting.GetFieldPerspective() / 100))
					cameraPerspective.SetEvent(ui.__mem_func__(self.OnChangeFOV))
					self.cameraPerspective = cameraPerspective

				if app.ENABLE_SELECT_DAMAGE_TYPE:
					self.damageTypeButtons.append(GetObject("damage_type_normal"))
					self.damageTypeButtons[0].SAFE_SetEvent(self.__OnClickChangeDamageType, 0)
					self.damageTypeButtons.append(GetObject("damage_type_dotted"))
					self.damageTypeButtons[1].SAFE_SetEvent(self.__OnClickChangeDamageType, 1)
					self.damageTypeButtons.append(GetObject("damage_type_with_letter"))
					self.damageTypeButtons[2].SAFE_SetEvent(self.__OnClickChangeDamageType, 2)
					self.GetDamageType()
    
					self.damageTypeRenewalButtons.append(GetObject("damage_type_renewal_normal"))
					self.damageTypeRenewalButtons[0].SAFE_SetEvent(self.__OnClickChangeDamageTypeRenewal, 0)
					self.damageTypeRenewalButtons.append(GetObject("damage_type_renewal_new"))
					self.damageTypeRenewalButtons[1].SAFE_SetEvent(self.__OnClickChangeDamageTypeRenewal, 1)
					self.GetDamageTypeRenewal()

				if app.ENABLE_LOADING_WINDOW_RENEWAL:
					self.showLoadingTypeList.append(GetObject("loading_type_animated"))
					self.showLoadingTypeList[0].SAFE_SetEvent(self.__OnClickLoadingTypeButton)
					self.showLoadingTypeList.append(GetObject("loading_type_normal"))
					self.showLoadingTypeList[1].SAFE_SetEvent(self.__OnClickLoadingTypeButton)
					self.RefresLoadingTypeButtons()


				if app.ENABLE_SKYBOX_SELECT:
					self.skyBoxList = ["skybox_type_default", "skybox_type_1",
					"skybox_type_2",  "skybox_type_3",  "skybox_type_4",
					"skybox_type_5", "skybox_type_6", "skybox_type_7"]
					for i in xrange(len(self.skyBoxList)):
						self.skyBoxObjects.append(i)
						self.skyBoxObjects[i] = GetObject(self.skyBoxList[i])
						self.skyBoxObjects[i].SAFE_SetEvent(self.OnSelectSkyBox, i)
						self.skyBoxObjects[i].SAFE_SetEvent(self.OnSelectSkyBox, i)
					self.RefreshSkyBoxButtons()


			elif categoryIndex == 1:#Interface
				self.showsalesTextButtonList.append(GetObject("salestext_off_button"))
				self.showsalesTextButtonList[0].SAFE_SetEvent(self.__OnClickSalesText)
				self.showsalesTextButtonList.append(GetObject("salestext_on_button"))
				self.showsalesTextButtonList[1].SAFE_SetEvent(self.__OnClickSalesText)
				self.RefreshShowSalesText()

				if app.ENABLE_HIDE_TOOLTIP_EMOJI:
					self.showHideTooltipEmojis.append(GetObject("show_emoji"))
					self.showHideTooltipEmojis[0].SAFE_SetEvent(self.__OnClickEmoji)
					self.showHideTooltipEmojis.append(GetObject("hide_emoji"))
					self.showHideTooltipEmojis[1].SAFE_SetEvent(self.__OnClickEmoji)
					self.RefreshEmojis()

				if app.ENABLE_ANIMATION_SELECT:
					self.currentSelectedAnimation = systemSetting.GetCurrentAnimation()
					self.lastSelectedAnimation = self.currentSelectedAnimation
					systemSetting.SetAnimation(self.currentSelectedAnimation)
					self.animatedWindowInfo = {
						0: uiScriptLocale.GAMEOPTION_ANIMATIONS_OFF,
						1: uiScriptLocale.GAMEOPTION_ANIMATIONS1,
						2: uiScriptLocale.GAMEOPTION_ANIMATIONS2,
						3: uiScriptLocale.GAMEOPTION_ANIMATIONS3,
						4: uiScriptLocale.GAMEOPTION_ANIMATIONS4,
						5: uiScriptLocale.GAMEOPTION_ANIMATIONS5,
						6: uiScriptLocale.GAMEOPTION_ANIMATIONS6,
						7: uiScriptLocale.GAMEOPTION_ANIMATIONS7,
					}
					self.animatedWindow = ui.ComboBoxImage(GetObject("animation_window"),"d:/ymir work/ui/pattern/select_image.tga",30, 35)
					self.animatedWindow.SetCurrentItem(self.animatedWindowInfo[self.currentSelectedAnimation])
					self.animatedWindow.SetParent(GetObject("animation_window"))
					for index, data in self.animatedWindowInfo.iteritems():
						self.animatedWindow.InsertItem(index, data)
					self.animatedWindow.SetEvent(lambda x, point=proxy(self): point.__ClickAnimation(x))
					self.animatedWindow.Show()

				if app.ENABLE_FONT_SELECT:
					self.FontList.append(GetObject("font_tahoma"))
					self.FontList[0].SAFE_SetEvent(self.__OnClickChangeFont, 0)
					self.FontList.append(GetObject("font_arial"))
					self.FontList[1].SAFE_SetEvent(self.__OnClickChangeFont, 1)
					self.FontList.append(GetObject("font_tahoma_big"))
					self.FontList[2].SAFE_SetEvent(self.__OnClickChangeFont, 2)
					self.FontList.append(GetObject("font_verdana"))
					self.FontList[3].SAFE_SetEvent(self.__OnClickChangeFont, 3)
					self.GetFontType()

				if app.ENABLE_EVENT_MANAGER:
					self.showEventIconList.append(GetObject("show_event_icon"))
					self.showEventIconList[0].SAFE_SetEvent(self.__OnClickEventIconButton)
					self.showEventIconList.append(GetObject("hide_event_icon"))
					self.showEventIconList[1].SAFE_SetEvent(self.__OnClickEventIconButton)
					self.RefreshEventIconButtons()

			elif categoryIndex == 2:#Performance
				self.alwaysShowNameButtonList.append(GetObject("always_show_name_on_button"))
				self.alwaysShowNameButtonList[0].SAFE_SetEvent(self.__OnClickAlwaysShowName)
				self.alwaysShowNameButtonList.append(GetObject("always_show_name_off_button"))
				self.alwaysShowNameButtonList[1].SAFE_SetEvent(self.__OnClickAlwaysShowName)
				self.RefreshAlwaysShowName()

				if app.ENABLE_SHADER_OPTIONS:
					self.showHideShadows.append(GetObject("shadow_off"))
					self.showHideShadows.append(GetObject("shadow_normal"))
					self.showHideShadows.append(GetObject("shadow_high"))
					self.showHideShadows[0].SAFE_SetEvent(self.__OnClickSetShadowLevel, 0)
					self.showHideShadows[1].SAFE_SetEvent(self.__OnClickSetShadowLevel, 1)
					self.showHideShadows[2].SAFE_SetEvent(self.__OnClickSetShadowLevel, 2)
					self.RefreshShadowLevel()

				if app.ENABLE_OUTLINED_NAMES:
					self.showOutlinedNamesList.append(GetObject("outline_on_button"))
					self.showOutlinedNamesList[0].SAFE_SetEvent(self.__OnClickOulineName)
					self.showOutlinedNamesList.append(GetObject("outline_off_button"))
					self.showOutlinedNamesList[1].SAFE_SetEvent(self.__OnClickOulineName)
					self.RefreshOulineName()

				if app.ENABLE_RANGE_ENTITY_OPTIMISATION:
					self.entitySelectButtons.append(GetObject("entity_range_short_button"))
					self.entitySelectButtons[0].SAFE_SetEvent(self.__OnClickChangeEntityRange, 0)
					self.entitySelectButtons.append(GetObject("entity_range_normal_button"))
					self.entitySelectButtons[1].SAFE_SetEvent(self.__OnClickChangeEntityRange, 1)
					self.entitySelectButtons.append(GetObject("entity_range_far_button"))
					self.entitySelectButtons[2].SAFE_SetEvent(self.__OnClickChangeEntityRange, 2)
					self.RefreshEntityRangeButtons()

				if app.ENABLE_HIDE_AFFECT_ICONS:
					self.showAffectIconsList.append(GetObject("show_affect_icons"))
					self.showAffectIconsList[0].SAFE_SetEvent(self.__OnClickAffectIcons)
					self.showAffectIconsList.append(GetObject("hide_affect_icons"))
					self.showAffectIconsList[1].SAFE_SetEvent(self.__OnClickAffectIcons)
					self.RefreshAffectIcons()

				if app.ENABLE_HIDE_HIGHLIGHT:
					self.showHighlightIconList.append(GetObject("show_highlight_new_items"))
					self.showHighlightIconList[0].SAFE_SetEvent(self.__OnClickHighlightItems)
					self.showHighlightIconList.append(GetObject("hide_highlight_new_items"))
					self.showHighlightIconList[1].SAFE_SetEvent(self.__OnClickHighlightItems)
					self.RefreshHighlightItems()

				if app.ENABLE_HIDE_EFFECTS:
					self.showHideEffectList.append(GetObject("hide_effects"))
					self.showHideEffectList.append(GetObject("show_effects"))
					self.showHideEffectList[0].SAFE_SetEvent(self.__OnClickEffectsButtons)
					self.showHideEffectList[1].SAFE_SetEvent(self.__OnClickEffectsButtons)
					self.RefreshHideEffects()

				# if app.ENABLE_AREA_OPTIMISATION:
				# 	self.objectScaling = GetObject("object_distance_scale")
				# 	self.objectScaling.SetSliderPos(float(systemSetting.GetLoadingDistance()))
				# 	self.objectScaling.SetEvent(ui.__mem_func__(self.OnObjectScaling))

				if app.ENABLE_HIDE_MOB_SYSTEM:
					hideNPC = GetObject("hide_npc")
					hideNPC.SetToggleUpEvent(self.__OnHideState, 0)
					hideNPC.SetToggleDownEvent(self.__OnHideState, 0)
					self.HiddenItemsList.append(hideNPC)
					hideMount = GetObject("hide_mount")
					hideMount.SetToggleUpEvent(self.__OnHideState, 1)
					hideMount.SetToggleDownEvent(self.__OnHideState, 1)
					self.HiddenItemsList.append(hideMount)
					hidePet = GetObject("hide_pet")
					hidePet.SetToggleUpEvent(self.__OnHideState, 2)
					hidePet.SetToggleDownEvent(self.__OnHideState, 2)
					self.HiddenItemsList.append(hidePet)
					hideShops = GetObject("hide_shops")
					hideShops.SetToggleUpEvent(self.__OnHideState, 3)
					hideShops.SetToggleDownEvent(self.__OnHideState, 3)
					self.HiddenItemsList.append(hideShops)
					self.RefreshAllHideButtons()

	# Dont Touch #
	def GetCurrentWindow(self):
		if self.children.has_key("optionType") and self.children.has_key("categoryType"):
			(optionType,categoryType) = (self.children["optionType"],self.children["categoryType"])
			if self.children.has_key("optionWindow%d%d"%(optionType,categoryType)):
				return self.children["optionWindow%d%d"%(optionType,categoryType)]
		return None
	def GetCurrentScrollBar(self):
		window = self.GetCurrentWindow()
		if window != None:
			return window.scrollBar
		return None
	def OnRunMouseWheel(self, nLen):
		scrollBar = self.GetCurrentScrollBar()
		if scrollBar:
			if scrollBar.IsShow():
				if nLen > 0:
					scrollBar.OnUp()
				else:
					scrollBar.OnDown()
				return True
		return False

	def UpdateScrollBar(self):
		window = self.GetCurrentWindow()
		if window == None:
			return
		scrollBar = window.scrollBar
		if scrollBar == None:
			return
		scriptChildrens = window.Children
		if len(scriptChildrens) == 0:
			return

		windowHeight = window.GetHeight()

		# OLD SHIT
		#lastChildren = scriptChildrens[len(scriptChildrens)-1]
		#screenSize = lastChildren.exPos[1]+lastChildren.GetHeight()

		screenSize = 0
		for child in scriptChildrens:
			childHeight = child.exPos[1] + child.GetHeight()
			if childHeight > screenSize:
				screenSize=childHeight

		if screenSize > windowHeight:
			scrollLen = screenSize-windowHeight
			basePos = int(scrollBar.GetPos()*scrollLen)
			for child in scriptChildrens:
				(_x,_y) = child.exPos
				child.SetPosition(_x,_y-basePos)

			scrollBar.SetMiddleBarSize(float(windowHeight-5)/float(screenSize))
			scrollBar.Show()
		else:
			scrollBar.Hide()

		_wy = window.GetGlobalPosition()[1]
		elementDictionary = window.ElementDictionary
		for childName, child in elementDictionary.items():
			(_x,_y) = child.GetGlobalPosition()
			childHeight = child.GetHeight()
			textLines = []
			images = []
			if isinstance(child, ui.ExpandedImageBox):
				images.append(child)
			elif isinstance(child, ui.TextLine):
				textLines.append(child)
			elif isinstance(child, ui.ToggleButton) or isinstance(child, ui.RadioButton):
				if child.ButtonText != None:
					textLines.append(child.ButtonText)
				images.append(child)
			elif isinstance(child, ui.SliderBar):
				if child.backGroundImage != None:
					images.append(child.backGroundImage)
				if child.cursor != None:
					images.append(child.cursor)

			for childItem in textLines:
				if _y < _wy:
					if childItem.IsShow():
						childItem.Hide()
				elif _y > (_wy+windowHeight-20):
					if childItem.IsShow():
						childItem.Hide()
				else:
					if not childItem.IsShow():
						childItem.Show()

			for childItem in images:
				if _y < _wy:
					if childItem.IsShow():
						childItem.Hide()
				elif _y > (_wy + windowHeight -25):
					if childItem.IsShow():
						childItem.Hide()
				else:
					if not childItem.IsShow():
						childItem.Show()
	# Dont Touch #

	# PvP - Mode
	def __SetPeacePKMode(self):
		self.__SetPKMode(player.PK_MODE_PEACE)

	def __SetPKMode(self, mode):
		if self.pvpModeButtonDict.has_key(mode):
			self.pvpModeButtonDict[mode].Down()
			for key in self.pvpModeButtonDict.keys():
				if key != mode:
					self.pvpModeButtonDict[key].SetUp()

	def __CheckPvPProtectedLevelPlayer(self):
		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__SetPeacePKMode()
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return True
		return False

	def __RefreshPVPButtonList(self):
		self.__SetPKMode(player.GetPKMode())

	def __OnClickPvPModePeaceButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return
		self.__RefreshPVPButtonList()
		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 0", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeRevengeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return
		self.__RefreshPVPButtonList()
		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 1", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeFreeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return
		self.__RefreshPVPButtonList()
		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 2", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeGuildButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return
		self.__RefreshPVPButtonList()
		if 0 == player.GetGuildID():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
			return
		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 4", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

	def OnChangePKMode(self):
		self.__RefreshPVPButtonList()
	# PvP - Mode

	# Block - Mode
	def RefreshBlock(self):
		global blockMode
		for i in xrange(len(self.blockButtonList)):
			if 0 != (blockMode & (1 << i)):
				self.blockButtonList[i].Down()
			else:
				self.blockButtonList[i].SetUp()
	def OnBlockMode(self, mode):
		global blockMode
		blockMode = mode
		self.RefreshBlock()
	def __OnClickBlockExchangeButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_EXCHANGE))
	def __OnClickBlockPartyButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY))
	def __OnClickBlockGuildButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_GUILD))
	def __OnClickBlockWhisperButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_WHISPER))
	def __OnClickBlockFriendButton(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_FRIEND))
	def __OnClickBlockPartyRequest(self):
		self.RefreshBlock()
		global blockMode
		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_PARTY_REQUEST))

	# if app.ENABLE_TELEPORT_TO_A_FRIEND:
	# 	def __OnClickBlockWarpRequest(self):
	# 		self.RefreshBlock()
	# 		global blockMode
	# 		net.SendChatPacket("/setblockmode " + str(blockMode ^ player.BLOCK_WARP_REQUEST))

	# Block - Mode

	# Chat - Mode
	def RefreshViewChat(self):
		if systemSetting.IsViewChat():
			self.viewChatButtonList[0].Down()
			self.viewChatButtonList[1].SetUp()
		else:
			self.viewChatButtonList[0].SetUp()
			self.viewChatButtonList[1].Down()
	def __OnClickViewChat(self):
		systemSetting.SetViewChatFlag(not systemSetting.IsViewChat())
		self.RefreshViewChat()
	# Chat - Mode

	# Name Color - Mode
	def __OnClickNameColorMode(self):
		constInfo.SET_CHRNAME_COLOR_INDEX(not constInfo.GET_CHRNAME_COLOR_INDEX())
		self.RefreshNameColor()
	def RefreshNameColor(self):
		index = constInfo.GET_CHRNAME_COLOR_INDEX()
		self.nameColorModeButtonList[index].Down()
		self.nameColorModeButtonList[not index].SetUp()
	# Name Color - Mode

	# Target Board - Mode
	def RefreshTargetBoard(self):
		index = constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD()
		self.viewTargetBoardButtonList[index].Down()
		self.viewTargetBoardButtonList[not index].SetUp()
	def __SetTargetBoardViewMode(self):
		constInfo.SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(not constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD())
		self.RefreshTargetBoard()
	# Target Board - Mode

	# Show Always Name - Mode
	def RefreshAlwaysShowName(self):
		index = systemSetting.IsAlwaysShowName()
		self.alwaysShowNameButtonList[index].SetUp()
		self.alwaysShowNameButtonList[not index].Down()
	def __OnClickAlwaysShowName(self):
		systemSetting.SetAlwaysShowNameFlag(not systemSetting.IsAlwaysShowName())
		self.RefreshAlwaysShowName()

	# Show Always Name - Mode

	if app.ENABLE_OUTLINED_NAMES:
		def RefreshOulineName(self):
			index = systemSetting.GetNamesType()
			self.showOutlinedNamesList[index].SetUp()
			self.showOutlinedNamesList[not index].Down()
		def __OnClickOulineName(self):
			systemSetting.SetNamesType(not systemSetting.GetNamesType())
			self.RefreshOulineName()

	if app.ENABLE_HIDE_AFFECT_ICONS:
		def RefreshAffectIcons(self):
			index = systemSetting.IsAffectIconShow()
			self.showAffectIconsList[index].SetUp()
			self.showAffectIconsList[not index].Down()
		def __OnClickAffectIcons(self):
			constInfo.AffectIconState = 1
			systemSetting.SetEffectIconShow(not systemSetting.IsAffectIconShow())
			self.RefreshAffectIcons()

	if app.ENABLE_HIDE_HIGHLIGHT:
		def RefreshHighlightItems(self):
			index = systemSetting.IsHighlightShow()
			self.showHighlightIconList[index].SetUp()
			self.showHighlightIconList[not index].Down()
		def __OnClickHighlightItems(self):
			systemSetting.SetHighlightShow(not systemSetting.IsHighlightShow())
			self.RefreshHighlightItems()

	if app.ENABLE_EVENT_MANAGER:
		def RefreshEventIconButtons(self):
			index = systemSetting.IsEventIconShow()
			self.showEventIconList[index].SetUp()
			self.showEventIconList[not index].Down()

		def __OnClickEventIconButton(self):
			interface = constInfo.GetInterfaceInstance()
			systemSetting.SetEventIconShow(not systemSetting.IsEventIconShow())
			self.RefreshEventIconButtons()
			interface.SetEventManagerIconState()

	if app.ENABLE_LOADING_WINDOW_RENEWAL:
		def RefresLoadingTypeButtons(self):
			index = systemSetting.IsLoadingAnimated()
			self.showLoadingTypeList[index].SetUp()
			self.showLoadingTypeList[not index].Down()

		def __OnClickLoadingTypeButton(self):
			systemSetting.SetLoadingWindowType(not systemSetting.IsLoadingAnimated())
			self.RefresLoadingTypeButtons()

	# Show Damage - Mode
	def RefreshShowDamage(self):
		index = systemSetting.IsShowDamage()
		self.showDamageButtonList[index].SetUp()
		self.showDamageButtonList[not index].Down()
  
	def __OnClickShowDamage(self):
		systemSetting.SetShowDamageFlag(not systemSetting.IsShowDamage())
		self.RefreshShowDamage()
	# Show Damage - Mode

	# Sales Text - Mode
	def __OnClickSalesText(self):
		systemSetting.SetShowSalesTextFlag(not systemSetting.IsShowSalesText())
		self.RefreshShowSalesText()
	def RefreshShowSalesText(self):
		index = systemSetting.IsShowSalesText()
		self.showsalesTextButtonList[index].Down()
		self.showsalesTextButtonList[not index].SetUp()
	# Sales Text - Mode

	# Camera - Mode
	def RefreshCameraMode(self):
		index = constInfo.GET_CAMERA_MAX_DISTANCE_INDEX()
		self.cameraModeButtonList[index].Down()
		self.cameraModeButtonList[not index].SetUp()
	def __OnClickCameraMode(self):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(not constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())
		self.RefreshCameraMode()
	# Camera - Mode

	# Fog - Mode
	def RefreshFog(self):
		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
	def __OnClickFog(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.RefreshFog()
	# Fog - Mode
	# Mob Info - Mode
	if app.WJ_SHOW_MOB_INFO:
		def RefreshShowMobInfo(self):
			if systemSetting.IsShowMobLevel():
				self.showMobInfoButtonList[0].Down()
			else:
				self.showMobInfoButtonList[0].SetUp()
			if systemSetting.IsShowMobAIFlag():
				self.showMobInfoButtonList[1].Down()
			else:
				self.showMobInfoButtonList[1].SetUp()

		def __OnClickShowMobLevelButton(self):
			systemSetting.SetShowMobLevel(not systemSetting.IsShowMobLevel())
			self.RefreshShowMobInfo()
		def __OnClickShowMobAIFlagButton(self):
			systemSetting.SetShowMobAIFlag(not systemSetting.IsShowMobAIFlag())
			self.RefreshShowMobInfo()
	# Mob Info - Mode

	if app.ENABLE_PERSPECTIVE_VIEW:
		def OnChangeFOV(self):
			if not self.cameraPerspective:
				return
			
			pos = float(self.cameraPerspective.GetSliderPos())
			systemSetting.SetFieldPerspective(pos * 100)

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos)
		systemSetting.SetMusicVolume(pos)

	if app.ENABLE_METIN_SCALE:
		def OnStoneScaling(self):
			if not self.stoneScaling:
				return
			pos = float(self.stoneScaling.GetSliderPos())
			systemSetting.SetMetinstoneScale(pos)

	# if app.ENABLE_AREA_OPTIMISATION:
	# 	def OnObjectScaling(self):
	# 		if not self.objectScaling:
	# 			return
	# 		pos = float(self.objectScaling.GetSliderPos())
	# 		systemSetting.SetLoadingDistance(pos)
			
	if app.ENABLE_DAMAGE_SIZE_SCALE:
		def OnDamageScaling(self):
			if not self.damageScaling:
				return
			pos = float(self.damageScaling.GetSliderPos())
			systemSetting.SetDamageTextureScale(pos)

	if app.ENABLE_HIDE_MOB_SYSTEM:
		def __OnHideState(self, type):
			systemSetting.SetMobTypeHiddenState(type, not systemSetting.IsMobTypeHidden(type))
			self.RefreshHideButtons(type)

		def RefreshHideButtons(self, type):
			if systemSetting.IsMobTypeHidden(type):
				self.HiddenItemsList[type].SetUp()
			else:
				self.HiddenItemsList[type].Down()

		def RefreshAllHideButtons(self):
			for type in xrange(4):
				self.RefreshHideButtons(type)

	if app.ENABLE_ANIMATION_SELECT:
		def __ClickAnimation(self, flag):
			self.currentSelectedAnimation = flag
			self.animatedWindow.SetCurrentItem(self.animatedWindowInfo[flag])
			self.animatedWindow.CloseListBox()
			systemSetting.SetAnimation(self.currentSelectedAnimation)
			if flag == 0 or self.lastSelectedAnimation == 0:
				import introLogin
				self.popUpTimer = introLogin.ConnectingDialog()
				self.popUpTimer.Open(10.0)
				net.ExitGame()
				self.popUpTimer.SetText(localeInfo.LEFT_TIME)
				# self.popUpTimer.SAFE_SetTimeOverEvent(self.OnEndCountDown)
				# self.popUpTimer.SAFE_SetExitEvent(self.OnPressExitKey)

	if app.ENABLE_FONT_SELECT:
		def __OnClickChangeFont(self, flag):
			systemSetting.SetFontType(flag)
			import introLogin
			self.popUpTimer = introLogin.ConnectingDialog()
			self.popUpTimer.Open(10.0)
			net.ExitApplication()
			self.popUpTimer.SetText(localeInfo.LEFT_TIME)
			# self.popUpTimer.SAFE_SetTimeOverEvent(self.OnEndCountDown)
			# self.popUpTimer.SAFE_SetExitEvent(self.OnPressExitKey)
			self.GetFontType()

		def GetFontType(self):
			index = systemSetting.GetFontType()
			self.FontList[index].Down()
			self.FontList[not index].SetUp()

	if app.ENABLE_HIDE_EFFECTS:
		def RefreshHideEffects(self):
			index = systemSetting.IsEffectActive()
			self.showHideEffectList[index].SetUp()
			self.showHideEffectList[not index].Down()

		def __OnClickEffectsButtons(self):
			systemSetting.SetEffectActive(not systemSetting.IsEffectActive())
			self.RefreshHideEffects()

	if app.ENABLE_HIDE_TOOLTIP_EMOJI:
		def __OnClickEmoji(self):
			systemSetting.SetEmojiStatus(not systemSetting.GetEmojiStatus())
			self.RefreshEmojis()

		def RefreshEmojis(self):
			index = systemSetting.GetEmojiStatus()
			self.showHideTooltipEmojis[index].Down()
			self.showHideTooltipEmojis[not index].SetUp()

	def SetScrollPositionForTarget(self):
		self.SetOptionType(0)
		self.SetCategoryType(1)
		# window = self.GetCurrentWindow()
		# scrollBar = window.scrollBar
		# scrollBar.SetPos(50)

	if app.ENABLE_SKYBOX_SELECT:
		def OnSelectSkyBox(self, index):
			systemSetting.SetSkyBox(index)
			self.RefreshSkyBoxButtons()

		def RefreshSkyBoxButtons(self):
			index = systemSetting.GetSkyBox()

			if index == 0:
				background.SetDefaultSkybox()
			else:
				background.RegisterEnvironmentData(index, self.skyBoxes[index])
				background.SetEnvironmentData(index)

			self.skyBoxObjects[index].Down()
			for j in xrange(len(self.skyBoxObjects)):
				if j != index:
					self.skyBoxObjects[j].SetUp()

	if app.ENABLE_SHADER_OPTIONS:
		def __OnClickSetShadowLevel(self, flag):
			if flag is 1:
				flag = 3
			elif flag is 2:
				flag = 5

			if flag == 0:
				background.SetNoShader()
			else:
				systemSetting.SetShadowLevel(flag)

			self.RefreshShadowLevel()

		def GetShaderIdx(self):
			index = systemSetting.GetShadowLevel()
			if index == 3:
				return 1
			elif index == 5:
				return 2
			else:
				return index

		def RefreshShadowLevel(self):
			idx = self.GetShaderIdx()
			self.showHideShadows[idx].Down()
			for j in xrange(len(self.showHideShadows)):
				if j != idx:
					self.showHideShadows[j].SetUp()

	if app.ENABLE_RANGE_ENTITY_OPTIMISATION:
		def __OnClickChangeEntityRange(self, flag):
			systemSetting.SetEntityRange(flag)
			self.RefreshEntityRangeButtons()

		def RefreshEntityRangeButtons(self):
			index = systemSetting.GetEntityRange()
			self.entitySelectButtons[index].Down()
			for j in xrange(len(self.entitySelectButtons)):
				if j != index:
					self.entitySelectButtons[j].SetUp()

	if app.ENABLE_SELECT_DAMAGE_TYPE:
		def __OnClickChangeDamageType(self, flag):
			systemSetting.SetDamageType(flag)
			self.GetDamageType()

		def GetDamageType(self):
			index = systemSetting.GetDamageType()
			self.damageTypeButtons[index].Down()
			for j in xrange(len(self.damageTypeButtons)):
				if j != index:
					self.damageTypeButtons[j].SetUp()

		def __OnClickChangeDamageTypeRenewal(self, flag):
			systemSetting.SetDamageTypeRenewal(flag)
			self.GetDamageTypeRenewal()

		def GetDamageTypeRenewal(self):
			index = systemSetting.GetDamageTypeRenewal()
			self.damageTypeRenewalButtons[index].Down()
			for j in xrange(len(self.damageTypeRenewalButtons)):
				if j != index:
					self.damageTypeRenewalButtons[j].SetUp()


class BackgroundImage(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.leftSide = ui.BorderA()
		self.leftSide.SetParent(self)
		self.leftSide.SetPosition(0, 0)
		self.leftSide.SetSize(169, 326)
		self.leftSide.Show()

		self.rightSide = ui.BorderA()
		self.rightSide.SetParent(self)
		self.rightSide.SetPosition(169, 0)
		self.rightSide.SetSize(305, 326)
		self.rightSide.Show()

	def __del__(self):
		ui.Window.__del__(self)

