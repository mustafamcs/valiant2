import ui
import uiScriptLocale
import app
import net
import dbg
import player
import mouseModule
import wndMgr
import skill
import playerSettingModule
import quest
import localeInfo
import uiToolTip
import constInfo
import emotion
import chr
if app.ENABLE_QUEST_CATEGORY:
	import math
# if app.ENABLE_DETAILS_INTERFACE:
import uiCharacterDetails
import extraInfo
import chat, uiCommon, event
if app.ENABLE_SKILL_COLOR_SYSTEM:
	import uiSkillColor

SHOW_ONLY_ACTIVE_SKILL = False
SHOW_LIMIT_SUPPORT_SKILL_LIST = []
HIDE_SUPPORT_SKILL_POINT = True 
BLOCK_SUPPORT_SKILL_LIST = [130, 131]

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M : "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W : "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M : "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W : "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M : "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W : "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M : "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W : "icon/face/shaman_w.tga",
}


JOB_NAME_DICT = {
	0	:	[localeInfo.SKILL_GROUP_WARRIOR_1,localeInfo.SKILL_GROUP_WARRIOR_2],
	1	:	[localeInfo.SKILL_GROUP_ASSASSIN_1,localeInfo.SKILL_GROUP_ASSASSIN_2],
	2	:	[localeInfo.SKILL_GROUP_SURA_1,localeInfo.SKILL_GROUP_SURA_2],
	3	:	[localeInfo.SKILL_GROUP_SHAMAN_1,localeInfo.SKILL_GROUP_SHAMAN_2],
	4	:	["Skill Lycan", "None"]
}

if app.ENABLE_WOLFMAN_CHARACTER:
	FACE_IMAGE_DICT.update({playerSettingModule.RACE_WOLFMAN_M  : "icon/face/wolfman_m.tga",})

def unsigned32(n):
	return n & 0xFFFFFFFFL

if app.ENABLE_QUEST_CATEGORY:
	quest_slot_listbar = {
		"name" : "Quest_Slot",
		"type" : "listbar",

		"x" : 0,
		"y" : 0,

		"width" : 210,
		"height" : 20,

		"text" : "Quest title",
		"align" : "left",

		"horizontal_align" : "left",
		"vertical_align" : "left",
		"text_horizontal_align" : "left",
		"all_align" : "left",

		"text_height": 40
	}

	quest_lable_expend_img_path_dict = {
		0: "d:/ymir work/ui/quest_re/tabcolor_1_main.tga",
		1: "d:/ymir work/ui/quest_re/tabcolor_2_sub.tga",
		2: "d:/ymir work/ui/quest_re/tabcolor_3_levelup.tga",
		3: "d:/ymir work/ui/quest_re/tabcolor_4_event.tga",
		4: "d:/ymir work/ui/quest_re/tabcolor_5_collection.tga",
		5: "d:/ymir work/ui/quest_re/tabcolor_6_system.tga",
		6: "d:/ymir work/ui/quest_re/tabcolor_7_scroll.tga",
		7: "d:/ymir work/ui/quest_re/tabcolor_8_daily.tga"
	}

	quest_label_dict = {
		0 : localeInfo.QUEST_CATEGORY_00,
		1 : localeInfo.QUEST_CATEGORY_01,
		2 : localeInfo.QUEST_CATEGORY_02,
		3 : localeInfo.QUEST_CATEGORY_03,
		4 : localeInfo.QUEST_CATEGORY_04,
		5 : localeInfo.QUEST_CATEGORY_05,
		6 : localeInfo.QUEST_CATEGORY_06,
		7 : localeInfo.QUEST_CATEGORY_07,
	}

class CharacterWindow(ui.ScriptWindow):

	ACTIVE_PAGE_SLOT_COUNT = 8
	SUPPORT_PAGE_SLOT_COUNT = 12
	HORSE_SLOT_COUNT = 6
	PAGE_SLOT_COUNT = 12
	PAGE_HORSE = 2
	if app.ENABLE_SKILLS_LEVEL_OVER_P:
		SKILL_GRADE_SLOT_COUNT = 3

	SKILL_GROUP_NAME_DICT = {
		playerSettingModule.JOB_WARRIOR : { 1 : localeInfo.SKILL_GROUP_WARRIOR_1, 2 : localeInfo.SKILL_GROUP_WARRIOR_2, },
		playerSettingModule.JOB_ASSASSIN : { 1 : localeInfo.SKILL_GROUP_ASSASSIN_1, 2 : localeInfo.SKILL_GROUP_ASSASSIN_2, },
		playerSettingModule.JOB_SURA : { 1 : localeInfo.SKILL_GROUP_SURA_1, 2 : localeInfo.SKILL_GROUP_SURA_2, },
		playerSettingModule.JOB_SHAMAN : { 1 : localeInfo.SKILL_GROUP_SHAMAN_1, 2 : localeInfo.SKILL_GROUP_SHAMAN_2, },
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		SKILL_GROUP_NAME_DICT.update({playerSettingModule.JOB_WOLFMAN		: { 1 : localeInfo.JOB_WOLFMAN1,	2 : localeInfo.JOB_WOLFMAN2, },})

	STAT_DESCRIPTION = {
		"HTH" : localeInfo.STAT_TOOLTIP_IMG_CON,
		"INT" : localeInfo.STAT_TOOLTIP_IMG_INT,
		"STR" : localeInfo.STAT_TOOLTIP_IMG_STR,
		"DEX" : localeInfo.STAT_TOOLTIP_IMG_DEX,
	}

	STAT_MINUS_DESCRIPTION = localeInfo.STAT_MINUS_DESCRIPTION

	if app.ENABLE_QUEST_CATEGORY:
		MAX_QUEST_PAGE_HEIGHT = 293.5

	def __init__(self):

		if app.ENABLE_QUEST_CATEGORY:
			self.isQuestCategoryLoad = False
		# if app.ENABLE_DETAILS_INTERFACE:
		self.chWndPos = (24, (wndMgr.GetScreenHeight() / 2) - 200)
		self.chDetailsWnd = None
		self.isOpenedDetailsWnd = False

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			self.skillColorWnd = None
			self.skillColorWndIsShow = False
			self.skillColorWndSetPosition = False
			self.skillColorButton = []
		self.interface = constInfo.GetInterfaceInstance()

		ui.ScriptWindow.__init__(self)
		self.state = "STATUS"
		self.isLoaded = 0

		self.toolTipSkill = 0

		self.__Initialize()
		self.__LoadWindow()

		self.statusPlusCommandDict = {
			"HTH" : "/stat ht",
			"INT" : "/stat iq",
			"STR" : "/stat st",
			"DEX" : "/stat dx",
		}

		self.statusMinusCommandDict = {
			"HTH-" : "/stat- ht",
			"INT-" : "/stat- iq",
			"STR-" : "/stat- st",
			"DEX-" : "/stat- dx",
		}
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.refreshToolTip = 0
		self.curSelectedSkillGroup = 0
		self.canUseHorseSkill = -1

		self.toolTip = None
		self.toolTipJob = None
		self.toolTipAlignment = None
		self.toolTipSkill = None

		self.faceImage = None
		self.statusPlusLabel = None
		self.statusPlusValue = None
		self.activeSlot = None
		self.tabDict = None
		self.tabButtonDict = None
		self.pageDict = None
		self.titleBarDict = None
		self.statusPlusButtonDict = None
		self.statusMinusButtonDict = None

		self.skillPageDict = None
		if app.ENABLE_QUEST_CATEGORY:
			self.questScrollBar = None
			self.questLastScrollPosition = 0
			self.questPage = None
			self.questTitleBar = None
			self.quest_page_board_window = None
			self.quest_object_board_window = None
			self.questSlotList = []
			self.questCategory = {}
			self.questCategoryList = []

			self.questColorList = {
				"green" : 0xFF83C055,
				"blue": 0xFF45678D,
				"golden": 0xFFCAB62F,
				"default_title": 0xFFCEC6B5
			}

			self.questOpenedCategories = []
			self.questMaxOpenedCategories = 1

			self.questClicked = []
			self.questIndexMap = {}
			self.questCounterList = []
			self.questClockList = []
			self.questSeparatorList = []

			self.displayY = 0
			self.baseCutY = 0
			self.questCategoryRenderPos = []
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = None
			self.questSlot = None
			self.questNameList = None
			self.questLastTimeList = None
			self.questLastCountList = None
		self.skillGroupButton = ()

		self.activeSlot = None
		self.activeSkillPointValue = None
		self.supportSkillPointValue = None
		self.horseSkillPointValue = None
		self.skillGroupButton1 = None
		self.skillGroupButton2 = None
		self.activeSkillGroupName = None

		self.guildNameSlot = None
		self.guildNameValue = None
		self.characterNameSlot = None
		self.characterNameValue = None

		self.emotionToolTip = None
		self.soloEmotionSlot = None
		self.dualEmotionSlot = None
		self.specialEmotionSlot = None

		# if app.ENABLE_DETAILS_UI:
		self.ExpandBtn = None
		self.MinimizeBtn = None
		self.chDetailsWnd = None
		self.isOpenedDetailsWnd = False

	def Show(self):
		self.__LoadWindow()
		# if app.ENABLE_DETAILS_INTERFACE:
		self.__InitCharacterDetailsUIButton()
		if self.chDetailsWnd and self.isOpenedDetailsWnd:
			self.chDetailsWnd.Show()
		ui.ScriptWindow.Show(self)


	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __BindObject(self):
		self.toolTip = uiToolTip.ToolTip()
		self.toolTipJob = uiToolTip.ToolTip()
		self.toolTipAlignment = uiToolTip.ToolTip(130)

		self.faceImage = self.GetChild("Face_Image")

		faceSlot=self.GetChild("Face_Slot")
		if 949 == app.GetDefaultCodePage():
			faceSlot.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowJobToolTip)
			faceSlot.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideJobToolTip)

		self.statusPlusLabel = self.GetChild("Status_Plus_Label")
		self.statusPlusValue = self.GetChild("Status_Plus_Value")

		self.characterNameSlot = self.GetChild("Character_Name_Slot")
		self.characterNameValue = self.GetChild("Character_Name")
		self.guildNameSlot = self.GetChild("Guild_Name_Slot")
		self.guildNameValue = self.GetChild("Guild_Name")
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowAlignmentToolTip)
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideAlignmentToolTip)

		self.activeSlot = self.GetChild("Skill_Active_Slot")
		self.activeSkillPointValue = self.GetChild("Active_Skill_Point_Value")
		self.supportSkillPointValue = self.GetChild("Support_Skill_Point_Value")
		self.horseSkillPointValue = self.GetChild("horse_Skill_Point_Value")
		self.skillGroupButton1 = self.GetChild("Skill_Group_Button_1")
		self.skillGroupButton2 = self.GetChild("Skill_Group_Button_2")
		self.activeSkillGroupName = self.GetChild("Active_Skill_Group_Name")

		if app.ENABLE_QUEST_CATEGORY:
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questPage = self.GetChild("Quest_Page")
			self.questTitleBar = self.GetChild("Quest_TitleBar")
			self.quest_page_board_window = self.GetChild("quest_page_board_window")
			self.quest_object_board_window = self.GetChild("quest_object_board_window")

		self.tabDict = {
			"STATUS" : self.GetChild("Tab_01"),
			"SKILL" : self.GetChild("Tab_02"),
			"EMOTICON" : self.GetChild("Tab_03"),
			"QUEST" : self.GetChild("Tab_04"),
		}

		self.tabButtonDict = {
			"STATUS" : self.GetChild("Tab_Button_01"),
			"SKILL" : self.GetChild("Tab_Button_02"),
			"EMOTICON" : self.GetChild("Tab_Button_03"),
			"QUEST" : self.GetChild("Tab_Button_04")
		}

		self.pageDict = {
			"STATUS" : self.GetChild("Character_Page"),
			"SKILL" : self.GetChild("Skill_Page"),
			"EMOTICON" : self.GetChild("Emoticon_Page"),
			"QUEST" : self.GetChild("Quest_Page")
		}

		self.titleBarDict = {
			"STATUS" : self.GetChild("Character_TitleBar"),
			"SKILL" : self.GetChild("Skill_TitleBar"),
			"EMOTICON" : self.GetChild("Emoticon_TitleBar"),
			"QUEST" : self.GetChild("Quest_TitleBar")
		}

		self.statusPlusButtonDict = {
			"HTH" : self.GetChild("HTH_Plus"),
			"INT" : self.GetChild("INT_Plus"),
			"STR" : self.GetChild("STR_Plus"),
			"DEX" : self.GetChild("DEX_Plus"),
		}

		self.statusMinusButtonDict = {
			"HTH-" : self.GetChild("HTH_Minus"),
			"INT-" : self.GetChild("INT_Minus"),
			"STR-" : self.GetChild("STR_Minus"),
			"DEX-" : self.GetChild("DEX_Minus"),
		}

		self.skillPageDict = {
			"ACTIVE" : self.GetChild("Skill_Active_Slot"),
			"SUPPORT" : self.GetChild("Skill_ETC_Slot"),
			"HORSE" : self.GetChild("Skill_HORSE_Slot"),
		}

		self.skillPageStatDict = {
			"SUPPORT" : player.SKILL_SUPPORT,
			"ACTIVE" : player.SKILL_ACTIVE,
			"HORSE" : player.SKILL_HORSE,
		}

		self.labelPageStatDict = {
			"SUPPORT"	: self.GetChild("Support_Skill_Point_Label"),
			"ACTIVE"	: self.GetChild("Active_Skill_Point_Label"),
			"SETBONUS"	: self.GetChild("Set_Skill_Point_Label"),
			"HORSE"		: self.GetChild("horse_Skill_Point_Label"),
		}

		self.skillGroupButton = (
			self.GetChild("Skill_Group_Button_1"),
			self.GetChild("Skill_Group_Button_2"),
		)

		self.tabSungmaButtonDict = {
			"BASE" : self.GetChild("change_base_button"),
			"SUNGMA" : self.GetChild("change_conqueror_button")
		}

		self.SungmaPageDict = {
			"BASE" : self.GetChild("base_info"),
			"SUNGMA" : self.GetChild("sungma_info"),
		}

		self.skillChooseBG = self.GetChild("skillChooseBG")

		self.titleBGSelectJob = ui.MakeExpandedImageBox(self.skillChooseBG, "d:/ymir work/ui/game/ekstra/skillselect/title.png", 36, 25)

		self.textSelectJob = ui.MakeTextLineNew(self.titleBGSelectJob, 0, 0, localeInfo.SELECT_JOB_INFO)
		self.textSelectJob.SetHorizontalAlignCenter()
		self.textSelectJob.SetVerticalAlignCenter()
		self.textSelectJob.SetWindowHorizontalAlignCenter()
		self.textSelectJob.SetWindowVerticalAlignCenter()

		self.btnSelect = ui.MakeButton(self, 50, 120, False, "offlineshop/lightwork/shopbuilder/", "btn_norm.png", "btn_hover.png", "btn_down.png")
		self.btnSelect.SetText(JOB_NAME_DICT[self.GetRealRace()][0])
		self.btnSelect.SetEvent(ui.__mem_func__(self.SelectJobFirstQuestion))
		self.btnSelect2 = ui.MakeButton(self, 125, 120, False, "offlineshop/lightwork/shopbuilder/", "btn_norm.png", "btn_hover.png", "btn_down.png")
		self.btnSelect2.SetText(JOB_NAME_DICT[self.GetRealRace()][1])
		self.btnSelect2.SetEvent(ui.__mem_func__(self.SelectJobSecondQuestion))
		self.HideSelectSkillPage()

		## TabButton1 (Character)
		self.GetChild("Tab_Button_01").ShowToolTip = lambda arg=uiScriptLocale.CHARACTER_MAIN: self.__ShowToolTipButton(arg)
		self.GetChild("Tab_Button_01").HideToolTip = lambda arg=uiScriptLocale.CHARACTER_MAIN: self.__HideToolTip()
		## TabButton2 (Skill)
		self.GetChild("Tab_Button_02").ShowToolTip = lambda arg=uiScriptLocale.CHARACTER_SKILL: self.__ShowToolTipButton(arg)
		self.GetChild("Tab_Button_02").HideToolTip = lambda arg=uiScriptLocale.CHARACTER_SKILL: self.__HideToolTip()
		## TabButton3 (Emoticon)
		self.GetChild("Tab_Button_03").ShowToolTip = lambda arg=uiScriptLocale.CHARACTER_ACTION: self.__ShowToolTipButton(arg)
		self.GetChild("Tab_Button_03").HideToolTip = lambda arg=uiScriptLocale.CHARACTER_ACTION: self.__HideToolTip()
		## TabButton4 (Quest)
		self.GetChild("Tab_Button_04").ShowToolTip = lambda arg=uiScriptLocale.CHARACTER_QUEST: self.__ShowToolTipButton(arg)
		self.GetChild("Tab_Button_04").HideToolTip = lambda arg=uiScriptLocale.CHARACTER_QUEST: self.__HideToolTip()

		## Level
		self.GetChild("Lv_ToolTip").ShowToolTip = lambda arg=localeInfo.STAT_TOOLTIP_LEVEL: self.__ShowToolTipButton(arg)
		self.GetChild("Lv_ToolTip").HideToolTip = lambda arg=localeInfo.STAT_TOOLTIP_LEVEL: self.__HideToolTip()

		## EXP
		self.GetChild("Exp_ToolTip").ShowToolTip = lambda arg=localeInfo.STAT_TOOLTIP_EXP: self.__ShowToolTipButton(arg)
		self.GetChild("Exp_ToolTip").HideToolTip = lambda arg=localeInfo.STAT_TOOLTIP_EXP: self.__HideToolTip()


		## Base Level
		self.GetChild("change_base_button").ShowToolTip = lambda arg=localeInfo.STAT_TOOLTIP_LEVEL: self.__ShowToolTipButton(arg)
		self.GetChild("change_base_button").HideToolTip = lambda arg=localeInfo.STAT_TOOLTIP_LEVEL: self.__HideToolTip()

		# self.GetChild("change_base_button").Hide()

		## Conqueror Level
		self.GetChild("change_conqueror_button").ShowToolTip = lambda arg=localeInfo.STAT_TOOLTIP_CONQUEROR_LEVEL: self.__ShowToolTipButton(arg)
		self.GetChild("change_conqueror_button").HideToolTip = lambda arg=localeInfo.STAT_TOOLTIP_CONQUEROR_LEVEL: self.__HideToolTip()
		self.GetChild("change_conqueror_button").Hide()

		## Passive Relic
		self.passive_expanded_btn = self.GetChild("passive_expanded_btn")
		self.passive_expanded_btn.ShowToolTip = lambda arg=localeInfo.STAT_TOOLTIP_PASSIVE: self.__ShowToolTipButton(arg)
		self.passive_expanded_btn.HideToolTip = lambda arg=localeInfo.STAT_TOOLTIP_PASSIVE: self.__HideToolTip()
		self.passive_expanded_btn.Hide()

		## Char Status Info
		self.GetChild("Char_Info_Status_img").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_STAT : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("Char_Info_Status_img").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## Status Plus Points
		self.GetChild("Status_Plus_Label").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_POINT : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("Status_Plus_Label").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		## CON (Constitution)
		self.GetChild("HTH_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_IMG_CON : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("HTH_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## INT (Intelligence)
		self.GetChild("INT_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_IMG_INT : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("INT_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## STR (Strength)
		self.GetChild("STR_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_IMG_STR : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("STR_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## DEX (Dexterity)
		self.GetChild("DEX_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_IMG_DEX : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("DEX_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		## HP (Health)
		self.GetChild("HEL_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_HP : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("HEL_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## SP (Stamina)
		self.GetChild("SP_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SP : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("SP_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## ATT (Attack)
		self.GetChild("ATT_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_ATT : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("ATT_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## DEF (Defense)
		self.GetChild("DEF_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_DEF : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("DEF_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		## MSPD (Move Speed)
		self.GetChild("MSPD_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_MOVE_SPEED : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("MSPD_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## ASPD (Attack Speed)
		self.GetChild("ASPD_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_ATT_SPEED : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("ASPD_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## CSPD (Cast Speed)
		self.GetChild("CSPD_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_CAST_SPEED : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("CSPD_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## MATT (Magic Attack)
		self.GetChild("MATT_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_MAG_ATT : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("MATT_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## MDEF (Magic Defense)
		self.GetChild("MDEF_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_MAG_DEF : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("MDEF_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		## EF (Evasion Resistance)
		self.GetChild("ER_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_DODGE_PER : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("ER_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		## Active Skill Point Label
		self.GetChild("Active_Skill_Point_Label").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_POINT : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("Active_Skill_Point_Label").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		self.GetChild("Set_Skill_Point_Label").OnMouseOverIn = lambda arg = localeInfo.SKILL_SET_BONUS_TOOLTIP_AVAIL_FOR_SAGE, arg2 = 50 : ui.__mem_func__(self.__ShowToolTipButton)(arg, arg2)
		self.GetChild("Set_Skill_Point_Label").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		## Support Skill Point Label
		self.GetChild("Support_Skill_ToolTip").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SUPPORT_SKILL + " (2)" : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("Support_Skill_ToolTip").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		self.GetChild("passive_skill_tooltip").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SUPPORT_SKILL : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("passive_skill_tooltip").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		self.GetChild("horse_skill_tooltip").OnMouseOverIn = lambda arg = localeInfo.SKILL_GROUP_HORSE : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("horse_skill_tooltip").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		self.GetChild("horse_Skill_Point_Label").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_POINT : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("horse_Skill_Point_Label").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		self.GetChild("Action_Bar_Img").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_ACTION : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("Action_Bar_Img").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		self.GetChild("Reaction_Bar_Img").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_REACTION : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("Reaction_Bar_Img").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
		self.GetChild("Special_Action_Bar_Img").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SPECIAL_ACTION : ui.__mem_func__(self.__ShowToolTip)(arg)
		self.GetChild("Special_Action_Bar_Img").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

		global SHOW_ONLY_ACTIVE_SKILL
		global HIDE_SUPPORT_SKILL_POINT
		if SHOW_ONLY_ACTIVE_SKILL or HIDE_SUPPORT_SKILL_POINT:
			self.GetChild("Support_Skill_Point_Label").Hide()

		self.soloEmotionSlot = self.GetChild("SoloEmotionSlot")
		self.dualEmotionSlot = self.GetChild("DualEmotionSlot")
		self.specialEmotionSlot = self.GetChild("SpecialEmotionSlot")
		self.__SetEmotionSlot()

		if app.ENABLE_QUEST_CATEGORY:
			self.questScrollBar.SetParent(self.quest_page_board_window)
			for i in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				self.questCategory = ui.SubTitleBar()
				self.questCategory.SetParent(self.questPage)
				self.questCategory.MakeSubTitleBar(210, "red")
				self.questCategory.SetText(quest_label_dict[i])
				self.questCategory.SetSize(210, 16)
				self.questCategory.SetTextColor(0xffCEC6B5)
				self.questCategory.SetPosition(13, 0)
				self.questCategoryList.append(self.questCategory)

				# self.questCategoryList.append(self.questCategory[i])
				# self.questCategoryList.append(self.GetChild("Quest_Category_0" + str(i)))
				self.questCategoryRenderPos.append(0)

			self.questScrollBar.SetParent(self.questPage)
			self.RearrangeQuestCategories(xrange(quest.QUEST_CATEGORY_MAX_NUM))
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.OnQuestScroll))
			self.questSlot = self.GetChild("Quest_Slot")
			for i in xrange(quest.QUEST_MAX_NUM):
				self.questSlot.HideSlotBaseImage(i)
				self.questSlot.SetCoverButton(i,\
					"d:/ymir work/ui/game/quest/slot_button_01.sub",\
					"d:/ymir work/ui/game/quest/slot_button_02.sub",\
					"d:/ymir work/ui/game/quest/slot_button_03.sub",\
					"d:/ymir work/ui/game/quest/slot_button_03.sub", True)

			self.questNameList = []
			self.questLastTimeList = []
			self.questLastCountList = []
			for i in xrange(quest.QUEST_MAX_NUM):
				self.questNameList.append(self.GetChild("Quest_Name_0" + str(i)))
				self.questLastTimeList.append(self.GetChild("Quest_LastTime_0" + str(i)))
				self.questLastCountList.append(self.GetChild("Quest_LastCount_0" + str(i)))

		# if app.ENABLE_DETAILS_INTERFACE:
		self.MainBoard = self.GetChild("board")
		self.ExpandBtn = ui.MakeButton(self.MainBoard, 240, 150, "", "d:/ymir work/ui/game/belt_inventory/", "btn_minimize_normal.tga", "btn_minimize_over.tga", "btn_minimize_down.tga")
		self.ExpandBtn.SetEvent(ui.__mem_func__(self.__ClickExpandButton))
		self.MinimizeBtn = ui.MakeButton(self.MainBoard, 240, 150, "", "d:/ymir work/ui/game/belt_inventory/", "btn_expand_normal.tga", "btn_expand_over.tga", "btn_expand_down.tga")
		self.MinimizeBtn.SetEvent(ui.__mem_func__(self.__ClickMinimizeButton))
		self.ExpandBtn.ShowToolTip = lambda arg=localeInfo.DETAILS_TITLE: self.__ShowToolTipButton(arg)
		self.ExpandBtn.HideToolTip = lambda arg=localeInfo.DETAILS_TITLE: self.__HideToolTip()
		self.MinimizeBtn.ShowToolTip = lambda arg=localeInfo.DETAILS_TITLE: self.__ShowToolTipButton(arg)
		self.MinimizeBtn.HideToolTip = lambda arg=localeInfo.DETAILS_TITLE: self.__HideToolTip()

	def GetRealRace(self):
		race = net.GetMainActorRace()
		if race >= 4:
			return race-4
		else:
			return race

	def SelectJobFirstQuestion(self):
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.SELECT_JOB_ACCEPT_SKILL % JOB_NAME_DICT[self.GetRealRace()][0])
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SelectJobFirst))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__OnCloseQuestionDialog))
		self.questionDialog.Open()

	def SelectJobFirst(self):
		net.SendChatPacket("/31cekenkaplumbaga 1")
		self.__OnCloseQuestionDialog()
		self.HideSelectSkillPage()
		constInfo.CHOOSE_SKILL = 0

	def SelectJobSecondQuestion(self):
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.SELECT_JOB_ACCEPT_SKILL % JOB_NAME_DICT[self.GetRealRace()][1])
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SelectJobSecond))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__OnCloseQuestionDialog))
		self.questionDialog.Open()

	def SelectJobSecond(self):
		net.SendChatPacket("/31cekenkaplumbaga 2")
		self.__OnCloseQuestionDialog()
		self.HideSelectSkillPage()
		constInfo.CHOOSE_SKILL = 0

	def __OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()
		self.questionDialog = None

	def ShowSelectSkillPage(self):
		self.skillChooseBG.Show()
		self.titleBGSelectJob.Show()
		self.textSelectJob.Show()
		self.btnSelect.Show()
		self.btnSelect2.Show()

	def HideSelectSkillPage(self):
		self.skillChooseBG.Hide()
		self.titleBGSelectJob.Hide()
		self.textSelectJob.Hide()
		self.btnSelect.Hide()
		self.btnSelect2.Hide()

	# if app.ENABLE_DETAILS_INTERFACE:
	def OnTop(self):
		if self.chDetailsWnd:
			self.chDetailsWnd.SetTop()
	def Hide(self):
		if self.chDetailsWnd:
			self.isOpenedDetailsWnd = self.chDetailsWnd.IsShow()
			self.chDetailsWnd.Close()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if self.skillColorWnd and self.skillColorWnd.IsShow():
				self.skillColorWnd.Close()
		wndMgr.Hide(self.hWnd)

	def __InitCharacterDetailsUIButton(self):
		self.ExpandBtn.Show()
		self.MinimizeBtn.Hide()

	def __ClickExpandButton(self):
		if not self.chDetailsWnd:
			self.chDetailsWnd = uiCharacterDetails.CharacterDetailsUI()
			self.chDetailsWnd.Show()
		else:
			self.chDetailsWnd.Show()

		self.ExpandBtn.Hide()
		self.MinimizeBtn.Show()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			self.skillColorWndSetPosition = True

	def __ClickMinimizeButton(self):			
		self.chDetailsWnd.Hide()
		self.MinimizeBtn.Hide()
		self.ExpandBtn.Show()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			self.skillColorWndSetPosition = False

	def __SetSkillSlotEvent(self):
		for skillPageValue in self.skillPageDict.itervalues():
			skillPageValue.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			skillPageValue.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))
			skillPageValue.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			skillPageValue.SetUnselectItemSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetUseSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			skillPageValue.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			skillPageValue.SetPressedSlotButtonEvent(ui.__mem_func__(self.OnPressedSlotButton))
			skillPageValue.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
				"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
				"d:/ymir work/ui/game/windows/btn_plus_down.sub")

	def __SetEmotionSlot(self):
		self.emotionToolTip = uiToolTip.ToolTip()

		for slot in (self.soloEmotionSlot, self.dualEmotionSlot, self.specialEmotionSlot):
			slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectEmotion))
			slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetUseSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInEmotion))
			slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutEmotion))
			slot.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
				"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
				"d:/ymir work/ui/game/windows/btn_plus_down.sub")

		for slotIdx, datadict in emotion.EMOTION_DICT.items():
			emotionIdx = slotIdx

			slot = self.soloEmotionSlot
			
			if slotIdx > 50 and slotIdx <= 60:
					slot = self.dualEmotionSlot
			elif slotIdx > 60:
				slot = self.specialEmotionSlot

			slot.SetEmotionSlot(slotIdx, emotionIdx)
			slot.SetCoverButton(slotIdx)

	def __SelectEmotion(self, slotIndex):
		if not slotIndex in emotion.EMOTION_DICT:
			return

		if app.IsPressed(app.DIK_LCONTROL):
			player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_EMOTION, slotIndex)
			return

		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_EMOTION, slotIndex, slotIndex)

	def __ClickEmotionSlot(self, slotIndex):
		if not slotIndex in emotion.EMOTION_DICT:
			return

		if player.IsActingEmotion():
			return

		command = emotion.EMOTION_DICT[slotIndex]["command"]

		if slotIndex > 50 and slotIndex <= 60:
				vid = player.GetTargetVID()

				if 0 == vid or vid == player.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EMOTION_CHOOSE_ONE)
					return

				command += " " + chr.GetNameByVID(vid)

		net.SendChatPacket(command)

	def ActEmotion(self, emotionIndex):
		self.__ClickEmotionSlot(emotionIndex)

	def __OverInEmotion(self, slotIndex):
		if self.emotionToolTip:

			if not slotIndex in emotion.EMOTION_DICT:
				return

			self.emotionToolTip.ClearToolTip()
			self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])
			self.emotionToolTip.AlignHorizonalCenter()
			self.emotionToolTip.ShowToolTip()

	def __OverOutEmotion(self):
		if self.emotionToolTip:
			self.emotionToolTip.HideToolTip()

	def __BindEvent(self):
		for i in xrange(len(self.skillGroupButton)):
			self.skillGroupButton[i].SetEvent(ui.__mem_func__(self.__SelectSkillGroup),i)

		self.RefreshQuest()
		self.__HideJobToolTip()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)

		for (tabKey, tabButton) in self.tabSungmaButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabSungmaButton), tabKey)
			self.tabSungmaButtonDict["SUNGMA"].Hide()

		for (statusPlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.SAFE_SetEvent(self.__OnClickStatusPlusButton, statusPlusKey)
			statusPlusButton.ShowToolTip = lambda arg=statusPlusKey: self.__OverInStatButton(arg)
			statusPlusButton.HideToolTip = lambda arg=statusPlusKey: self.__OverOutStatButton()

		for (statusMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.SAFE_SetEvent(self.__OnClickStatusMinusButton, statusMinusKey)
			statusMinusButton.ShowToolTip = lambda arg=statusMinusKey: self.__OverInStatMinusButton(arg)
			statusMinusButton.HideToolTip = lambda arg=statusMinusKey: self.__OverOutStatMinusButton()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.SetCloseEvent(ui.__mem_func__(self.Hide))

		if app.ENABLE_QUEST_CATEGORY:
			self.questTitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScrollQuest))

			for i in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				self.questCategoryList[i].SetEvent(ui.__mem_func__(self.__OnClickQuestCategoryButton), i)
		else:
			self.questSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectQuest))

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			self.__LoadScript("UIScript/CharacterWindow.py")

			self.__BindObject()
			self.__BindEvent()
		except:
			import exception
			exception.Abort("CharacterWindow.__LoadWindow")

		self.SetState("STATUS")
		self.SetSubState("BASE")

	def Destroy(self):
		self.ClearDictionary()

		# if app.ENABLE_DETAILS_INTERFACE:
		if self.chDetailsWnd:
			self.chDetailsWnd.Destroy()
			self.chDetailsWnd=None

		if app.ENABLE_LEADERSHIP_EXTENSION:
			if self.interface.wndPartyBonusWindow:
				self.interface.wndPartyBonusWindow.Close()

		self.__Initialize()

	def Close(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.Hide()

		# if app.ENABLE_DETAILS_INTERFACE:
		if self.chDetailsWnd and self.chDetailsWnd.IsShow():
			self.isOpenedDetailsWnd = False
			self.chDetailsWnd.Hide()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if self.skillColorWnd and self.skillColorWnd.IsShow():
				self.skillColorWnd.Hide()

		if app.ENABLE_LEADERSHIP_EXTENSION:
			if self.interface.wndPartyBonusWindow:
				if self.interface.wndPartyBonusWindow.IsShow():
					self.interface.wndPartyBonusWindow.Hide()

		self.Hide()

	def SetSkillToolTip(self, toolTipSkill):
		self.toolTipSkill = toolTipSkill

	def __OnClickStatusPlusButton(self, statusKey):
		try:
			status_inc = constInfo.INCREASE_POINTS_CTRL\
						if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL) else 1
			
			statusPlusCommand=self.statusPlusCommandDict[statusKey]
			net.SendChatPacket("%s %d" % (statusPlusCommand, status_inc))
		except KeyError, msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusPlusButton KeyError: %s", msg)

	def __OnClickStatusMinusButton(self, statusKey):
		try:
			statusMinusCommand=self.statusMinusCommandDict[statusKey]
			net.SendChatPacket(statusMinusCommand)
		except KeyError, msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusMinusButton KeyError: %s", msg)

	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)

	def __OnClickTabSungmaButton(self, stateKey):
		self.SetSubState(stateKey)

	def SetState(self, stateKey):
		self.state = stateKey

		if app.ENABLE_QUEST_CATEGORY:
			if stateKey != "QUEST":
				self.questPage.Hide()
			else:
				self.__LoadQuestCategory()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if stateKey!=tabKey:
				tabButton.SetUp()

		for tabValue in self.tabDict.itervalues():
			tabValue.Hide()

		for pageValue in self.pageDict.itervalues():
			pageValue.Hide()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.Hide()

		self.titleBarDict[stateKey].Show()
		self.tabDict[stateKey].Show()
		self.pageDict[stateKey].Show()

		if app.ENABLE_LEADERSHIP_EXTENSION:
			if self.interface.wndPartyBonusWindow:
				self.interface.wndPartyBonusWindow.Hide()

		if constInfo.CHOOSE_SKILL == 1:
			if stateKey != "SKILL":
				self.HideSelectSkillPage()
			else:
				self.ShowSelectSkillPage()
		else:
			self.HideSelectSkillPage()

	def GetState(self):
		return self.state

	def SetSubState(self, stateSubKey):
		self.substate = stateSubKey

		for (tabKey, tabButton) in self.tabSungmaButtonDict.items():
			if stateSubKey != tabKey:
				tabButton.SetUp()

		self.tabSungmaButtonDict[stateSubKey].Down()

		for pageValue in self.SungmaPageDict.itervalues():
			pageValue.Hide()

		self.SungmaPageDict[stateSubKey].Show()

	def __GetTotalAtkText(self):
		minAtk=player.GetStatus(player.ATT_MIN)
		maxAtk=player.GetStatus(player.ATT_MAX)
		atkBonus=player.GetStatus(player.ATT_BONUS)
		attackerBonus=player.GetStatus(player.ATTACKER_BONUS)
		min = int(minAtk+atkBonus)
		max = int(maxAtk+atkBonus)
		attack = int(attackerBonus)
		groupbonusattack = self.GetChild("ATT_Slot")

		if minAtk == maxAtk:
			if attack == 0:
				return "%s" % (localeInfo.NumberToDecimalString((min)))
			else:
				return "%s |cff00ff00|h+ (%s)" % (localeInfo.NumberToDecimalString(min), localeInfo.NumberToDecimalString(attack))
		else:
			if attack == 0:
				return "%s - %s" % (localeInfo.NumberToDecimalString(min), localeInfo.NumberToDecimalString(max))
			else:
				return "%s - %s |cff00ff00|h+ (%s)" % (localeInfo.NumberToDecimalString(min), localeInfo.NumberToDecimalString(max), localeInfo.NumberToDecimalString(attack))

	def __GetTotalMagAtkText(self):
		minMagAtk=player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MIN_MAGIC_WEP)
		maxMagAtk=player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MAX_MAGIC_WEP)

		if minMagAtk==maxMagAtk:
			return "%s" % (localeInfo.NumberToDecimalString(minMagAtk))
		else:
			return "%s - %s" % (localeInfo.NumberToDecimalString(minMagAtk), localeInfo.NumberToDecimalString(maxMagAtk))

	def __GetTotalDefText(self):
		defValue=player.GetStatus(player.DEF_GRADE)
		if constInfo.ADD_DEF_BONUS_ENABLE:
			defValue+=player.GetStatus(player.DEF_BONUS)
		return "%s" % (localeInfo.NumberToDecimalString(defValue))

	def RefreshStatus(self):
		if self.isLoaded == 0:
			return

		try:
			self.GetChild("Level_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.LEVEL)))
			self.GetChild("Exp_Value").SetText(localeInfo.NumberToDecimalString(unsigned32(player.GetEXP())))
			self.GetChild("RestExp_Value").SetText(localeInfo.NumberToDecimalString(unsigned32(player.GetStatus(player.NEXT_EXP))))
			self.GetChild("HP_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.HP)) + ' / ' + localeInfo.NumberToDecimalString(player.GetStatus(player.MAX_HP)))
			self.GetChild("SP_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.SP)) + ' / ' + localeInfo.NumberToDecimalString(player.GetStatus(player.MAX_SP)))

			self.GetChild("STR_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.ST)))
			self.GetChild("DEX_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.DX)))
			self.GetChild("HTH_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.HT)))
			self.GetChild("INT_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.IQ)))

			self.GetChild("ATT_Value").SetText(self.__GetTotalAtkText())
			self.GetChild("DEF_Value").SetText(self.__GetTotalDefText())

			self.GetChild("MATT_Value").SetText(self.__GetTotalMagAtkText())
			# self.GetChild("MATT_Value").SetText(str(player.GetStatus(player.MAG_ATT)))

			self.GetChild("MDEF_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.MAG_DEF)))
			self.GetChild("ASPD_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.ATT_SPEED)))
			self.GetChild("MSPD_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.MOVING_SPEED)))
			self.GetChild("CSPD_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.CASTING_SPEED)))
			self.GetChild("ER_Value").SetText(localeInfo.NumberToDecimalString(player.GetStatus(player.EVADE_RATE)))

			self.GetChild("BattlePoint").SetText(localeInfo.BATTLEPONT_TEXT + localeInfo.NumberToDecimal("%d" % (player.GetStatus(player.POINT_POWER_RANK))))

		except:
			pass

		self.__RefreshStatusPlusButtonList()
		self.__RefreshStatusMinusButtonList()
		self.RefreshAlignment()

		if self.refreshToolTip:
			self.refreshToolTip()

		# if app.ENABLE_DETAILS_INTERFACE:
		if self.chDetailsWnd:
			if self.chDetailsWnd.IsShow():
				self.chDetailsWnd.Refresh()

	def __RefreshStatusPlusButtonList(self):
		if self.isLoaded==0:
			return

		statusPlusPoint=player.GetStatus(player.STAT)

		if statusPlusPoint>0:
			self.statusPlusValue.SetText(str(statusPlusPoint))
			self.statusPlusLabel.Show()
			self.ShowStatusPlusButtonList()
		else:
			self.statusPlusValue.SetText(str(0))
			self.statusPlusLabel.Hide()
			self.HideStatusPlusButtonList()

	def __RefreshStatusMinusButtonList(self):
		if self.isLoaded==0:
			return

		statusMinusPoint=self.__GetStatMinusPoint()

		if statusMinusPoint>0:
			self.__ShowStatusMinusButtonList()
		else:
			self.__HideStatusMinusButtonList()


	alignmentList = {
		8: 1000,
		7: 4000,
		6: 8000,
		5: 12000,
		4: 20000,
		3: 30000,
		2: 50000,
		1: 75000,
		0: 100000,
	}

	def RefreshAlignment(self):
		point, grade = player.GetAlignmentData()
		colorList = extraInfo.TITLE_COLOR_DICT[grade]
		gradeColor = ui.GenerateColor(colorList[0], colorList[1], colorList[2])

		self.toolTipAlignment.ClearToolTip()
		self.toolTipAlignment.AutoAppendTextLine(extraInfo.TITLE_NAME_LIST[grade], gradeColor)
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.ALIGNMENT_NAME + str(point))
		self.toolTipAlignment.AlignHorizonalCenter()
		self.toolTipAlignment.AppendSpace(4)

		bonusCount = player.GetAlignmentBonusCount(grade)
		BONUS_COLOR = 0xff7CCD7C
		if grade < 9:
			self.toolTipAlignment.AutoAppendTextLine(localeInfo.TOOLTIP_ALIGNMENT_INFO)
			self.toolTipAlignment.AppendSpace(2)

		for i in xrange(bonusCount):
			bonusType, bonusValue = player.GetAlignmentBonusInfo(grade,i)
			bonusText = uiToolTip.GET_AFFECT_STRING(bonusType, bonusValue)
			self.toolTipAlignment.AutoAppendTextLine("{}".format(bonusText), BONUS_COLOR)
			self.toolTipAlignment.AppendSpace(2)

		bonusCount = player.GetAlignmentBonusCount(grade-1)
		if bonusCount:
			self.toolTipAlignment.AppendHorizontalLine()
			self.toolTipAlignment.AppendSpace(4)
			self.toolTipAlignment.AutoAppendTextLine(localeInfo.TOOLTIP_ALIGNMENT_INFO2)
			self.toolTipAlignment.AppendSpace(4)
			colorList = extraInfo.TITLE_COLOR_DICT[grade-1]
			gradeColor = ui.GenerateColor(colorList[0], colorList[1], colorList[2])
			self.toolTipAlignment.AutoAppendTextLine(extraInfo.TITLE_NAME_LIST[grade-1], gradeColor)
			self.toolTipAlignment.AutoAppendTextLine(localeInfo.ALIGNMENT_NAME + str(self.alignmentList.get(grade-1, 0)))

		for i in xrange(bonusCount):
			bonusType, bonusValue = player.GetAlignmentBonusInfo(grade-1, i)
			bonusText = uiToolTip.GET_AFFECT_STRING(bonusType, bonusValue)
			self.toolTipAlignment.AutoAppendTextLine("{}".format(bonusText), 0xffFFB96D)
			self.toolTipAlignment.AppendSpace(2)

	def __ShowStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Show()

	def __HideStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Hide()

	def ShowStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Show()

	def HideStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Hide()

	def SelectSkill(self, skillSlotIndex):
		mouseController = mouseModule.mouseController

		if not mouseController.isAttached():
			srcSlotIndex = self.__RealSkillSlotToSourceSlot(skillSlotIndex)
			selectedSkillIndex = player.GetSkillIndex(srcSlotIndex)

			if app.ENABLE_LEADERSHIP_EXTENSION:
				if selectedSkillIndex == 121:
					x, y = self.GetGlobalPosition()
					if self.interface:
						if self.interface.wndPartyBonusWindow.IsShow():
							self.interface.wndPartyBonusWindow.Close()
						else:
							self.interface.TogglePartyBonusWindow()
							self.interface.wndPartyBonusWindow.AdjustPosition(x, y + 406)
					return

			if skill.CanUseSkill(selectedSkillIndex):
				if app.IsPressed(app.DIK_LCONTROL):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_SKILL, srcSlotIndex)
					return

				mouseController.AttachObject(self, player.SLOT_TYPE_SKILL, srcSlotIndex, selectedSkillIndex)
		else:
			mouseController.DeattachObject()

	def SelectEmptySlot(self, SlotIndex):
		mouseModule.mouseController.DeattachObject()

	def __ShowToolTip(self, desc, extend = 1):
		if not self.toolTip:
			return

		descLen = len(desc)
		self.toolTip.ClearToolTip()
		# self.toolTip.SetThinBoardSize(11 * descLen)
		self.toolTip.AutoAppendTextLine(desc)
		self.toolTip.AlignHorizonalCenter()
		self.toolTip.AppendSpace(extend)
		self.toolTip.Show()

	def __HideToolTip(self):
		self.__HideStatToolTip()

	def __ShowToolTipButton(self, desc, extend=1):
		self.__ShowToolTip(desc, extend)

	# def __ShowToolTipImg(self, event_type, text):
	# 	if "mouse_over_in" == event_type :
	# 		textLen = len(text)

	# 		self.toolTip.ClearToolTip()
	# 		self.toolTip.SetThinBoardSize(11 * arglen)
	# 		# self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
	# 		self.toolTip.AppendTextLine(text, 0xffffffff)
	# 		self.toolTip.Show()
	# 	elif "mouse_over_out" == event_type:
	# 		self.__HideToolTip()

	def __TogglePassiveAttrWindow(self, event_type):
		pass

	def __ToolTipProgress(self):
		pass

	## ToolTip
	def OverInItem(self, slotNumber):
		if mouseModule.mouseController.isAttached():
			return

		if 0 == self.toolTipSkill:
			return

		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillLevel = player.GetSkillLevel(srcSlotIndex)
		skillGrade = player.GetSkillGrade(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		if self.toolTipSkill:
			if skill.SKILL_TYPE_ACTIVE == skillType:
				overInSkillGrade = self.__GetSkillGradeFromSlot(slotNumber)
				
				if (overInSkillGrade == self.SKILL_GRADE_SLOT_COUNT-1 and skillGrade >= self.SKILL_GRADE_SLOT_COUNT) if app.ENABLE_SKILLS_LEVEL_OVER_P else (overInSkillGrade == skill.SKILL_GRADE_COUNT-1 and skillGrade == skill.SKILL_GRADE_COUNT):
					self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)
				elif overInSkillGrade == skillGrade:
					self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, overInSkillGrade, skillLevel)
				else:
					self.toolTipSkill.SetSkillOnlyName(srcSlotIndex, skillIndex, overInSkillGrade)
			else:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)

	def OverOutItem(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.HideToolTip()

	## Quest
	def __SelectQuest(self, slotIndex):
		if app.ENABLE_QUEST_CATEGORY:
			questIndex = self.questIndexMap[slotIndex]

			if not questIndex in self.questClicked:
				self.questClicked.append(questIndex)
		else:
			questIndex = quest.GetQuestIndex(self.questShowingStartIndex + slotIndex)

		import event
		event.QuestButtonClick(-2147483648 + questIndex)

	def RefreshQuest(self):
		if app.ENABLE_QUEST_CATEGORY:
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			for cat in self.questOpenedCategories:
				self.RefreshQuestCategory(cat)

			self.RefreshQuestCategoriesCount()
		else:
			if self.isLoaded == 0:
				return

			self.OnQuestScroll()

			questCount = quest.GetQuestCount()
			questRange = xrange(quest.QUEST_MAX_NUM)

			if questCount > quest.QUEST_MAX_NUM:
				self.questScrollBar.Show()
			else:
				self.questScrollBar.Hide()

			for i in questRange[:questCount]:
				(questName, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(self.questShowingStartIndex + i)

				self.questNameList[i].SetText(questName)
				self.questNameList[i].Show()
				self.questLastCountList[i].Show()
				self.questLastTimeList[i].Show()

				if len(questCounterName) > 0:
					self.questLastCountList[i].SetText("%s : %d" % (questCounterName, questCounterValue))
				else:
					self.questLastCountList[i].SetText("")

				## Icon
				self.questSlot.SetSlot(i, i, 1, 1, questIcon)

			for i in questRange[questCount:]:
				self.questNameList[i].Hide()
				self.questLastTimeList[i].Hide()
				self.questLastCountList[i].Hide()
				self.questSlot.ClearSlot(i)
				self.questSlot.HideSlotBaseImage(i)

			self.__UpdateQuestClock()

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.questScrollBar.OnUp()
		else:
			self.questScrollBar.OnDown()

	def __UpdateQuestClock(self):
		if "QUEST" == self.state:
			if app.ENABLE_QUEST_CATEGORY:
				for clock in self.questClockList:
					clockText = localeInfo.QUEST_UNLIMITED_TIME

					if clock.GetProperty("idx"):
						(lastName, lastTime) = quest.GetQuestLastTime(clock.GetProperty("idx"))

						if len(lastName) > 0:
							if lastTime <= 0:
								clockText = localeInfo.QUEST_TIMEOVER
							else:
								questLastMinute = lastTime / 60
								questLastSecond = lastTime % 60

								clockText = lastName + " : "

								if questLastMinute > 0:
									clockText += str(questLastMinute) + localeInfo.QUEST_MIN
									if questLastSecond > 0:
										clockText += " "

								if questLastSecond > 0:
									clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					clock.SetText(clockText)
			else:
				# QUEST_LIMIT_COUNT_BUG_FIX
				for i in xrange(min(quest.GetQuestCount(), quest.QUEST_MAX_NUM)):
				# END_OF_QUEST_LIMIT_COUNT_BUG_FIX
					(lastName, lastTime) = quest.GetQuestLastTime(i + self.questShowingStartIndex)

					clockText = localeInfo.QUEST_UNLIMITED_TIME
					if len(lastName) > 0:

						if lastTime <= 0:
							clockText = localeInfo.QUEST_TIMEOVER
						else:
							questLastMinute = lastTime / 60
							questLastSecond = lastTime % 60

							clockText = lastName + " : "

							if questLastMinute > 0:
								clockText += str(questLastMinute) + localeInfo.QUEST_MIN
								if questLastSecond > 0:
									clockText += " "

							if questLastSecond > 0:
								clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					self.questLastTimeList[i].SetText(clockText)

	def __GetStatMinusPoint(self):
		POINT_STAT_RESET_COUNT = 112
		return player.GetStatus(POINT_STAT_RESET_COUNT)

	def __OverInStatMinusButton(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_MINUS_DESCRIPTION[stat] % self.__GetStatMinusPoint())
		except KeyError:
			pass

		self.refreshToolTip = lambda arg = stat : ui.__mem_func__(self.__OverInStatMinusButton)(arg)

	def __OverOutStatMinusButton(self):
		self.__HideStatToolTip()
		self.refreshToolTip = 0

	def __OverInStatButton(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_DESCRIPTION[stat])
		except KeyError:
			pass

	def __OverOutStatButton(self):
		self.__HideStatToolTip()

	def __ShowStatToolTip(self, statDesc):
		if not self.toolTip:
			return

		statDescLen = len(statDesc)
		self.toolTip.SetThinBoardSize(11 * statDescLen)
		self.toolTip.AlignHorizonalCenter()

		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(statDesc)
		self.toolTip.AppendSpace(5)
		self.toolTip.AppendTextLine("|Eothers/key_ctrl|e + |Eothers/key_lc|e - " +\
								"10x " + uiScriptLocale.GAME_STAT_UP.format(constInfo.INCREASE_POINTS_CTRL))
		self.toolTip.Show()

	def __HideStatToolTip(self):
		if self.toolTip:
			self.toolTip.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self):
		self.__UpdateQuestClock()
		if app.ENABLE_SKILL_COLOR_SYSTEM:
			self.__SetOnMoveWindowPos(self.skillColorWndSetPosition)

		# if self.GetChild("Character_Page"):
		# 	if self.GetChild("BattlePoint"):
				# self.GetChild("BattlePoint").SetText(localeInfo.BATTLEPONT_TEXT + localeInfo.NumberToDecimal("%d" % (player.GetStatus(player.POINT_POWER_RANK))))

	def RefreshNormalSkillCoolTime(self, skillPage, slotCount):

		startSlotIndex = skillPage.GetStartIndex()
		getSkillType=skill.GetSkillType
		getSkillIndex=player.GetSkillIndex
		getSkillGrade=player.GetSkillGrade
		getSkillLevel=player.GetSkillLevel
		
		for i in xrange(slotCount+1):
			slotIndex = i + startSlotIndex
			skillIndex = getSkillIndex(slotIndex)

			if 0 == skillIndex:
				continue

			skillGrade = getSkillGrade(slotIndex)
			skillLevel = getSkillLevel(slotIndex)
			skillType = getSkillType(skillIndex)
			
			slot_index_old = None
			for j in xrange(skill.SKILL_GRADE_COUNT):
				realSlotIndex = self.__GetRealSkillSlot(j, slotIndex)
				if(skillGrade != j):
					slot_index_old = realSlotIndex
				else:
					if slot_index_old:
						skillPage.UpdateSlotCoolTime(skillType, realSlotIndex, slot_index_old)
					break
		self.__RestoreSlotCoolTime(skillPage)

	## Skill Process
	if app.ENABLE_SKILLS_LEVEL_OVER_P:
		def __RefreshSkillPage(self, name, slotCount):
			global SHOW_LIMIT_SUPPORT_SKILL_LIST
			global BLOCK_SUPPORT_SKILL_LIST

			skillPage = self.skillPageDict[name]
			startSlotIndex = skillPage.GetStartIndex()

			if "ACTIVE" == name:
				if self.PAGE_HORSE==self.curSelectedSkillGroup:
					startSlotIndex+=slotCount

			self.RefreshNormalSkillCoolTime(skillPage, slotCount)

			getSkillType=skill.GetSkillType

			getSkillIndex=player.GetSkillIndex
			getSkillGrade=player.GetSkillGrade
			getSkillLevel=player.GetSkillLevel

			for i in xrange(slotCount+1):
				slotIndex= i + startSlotIndex
				skillIndex= getSkillIndex(slotIndex)

				for j in xrange(skill.SKILL_GRADE_COUNT):
					realSlotIndex = self.__GetRealSkillSlot(j, i)
					skillPage.ClearSlot(realSlotIndex)

				if 0 == skillIndex:
					continue

				if skillIndex in BLOCK_SUPPORT_SKILL_LIST:
					continue

				skillGrade=getSkillGrade(slotIndex)
				skillLevel=getSkillLevel(slotIndex)
				skillType=getSkillType(skillIndex)

				if player.SKILL_INDEX_RIDING == skillIndex:
					if 1==skillGrade:
						skillLevel+=19
					elif 2==skillGrade:
						skillLevel+=29
					elif 3==skillGrade:
						skillLevel+=39
					elif 4==skillGrade:
						skillLevel=50

					skillPage.SetSkillSlotNew(slotIndex, skillIndex, max(skillLevel-1, 0), skillLevel)
					skillPage.SetSlotCount(slotIndex, skillLevel)

				elif skill.SKILL_TYPE_ACTIVE==skillType:
					for j in xrange(self.SKILL_GRADE_SLOT_COUNT):
						realSlotIndex = self.__GetRealSkillSlot(j, slotIndex)

						if (skillGrade >= self.SKILL_GRADE_SLOT_COUNT) and j == (self.SKILL_GRADE_SLOT_COUNT-1):
							skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, skillGrade, skillLevel)
							skillPage.SetCoverButton(realSlotIndex)
							skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
						else:
							skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, j, skillLevel)
							skillPage.SetCoverButton(realSlotIndex)
    
							if (not self.__CanUseSkillNow()) or (skillGrade != j):
								skillPage.SetSlotCount(realSlotIndex, 0)
								skillPage.DisableCoverButton(realSlotIndex)
								skillPage.DeactivateSlot(realSlotIndex) # hotfix
							else:
								skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

						if player.IsSkillActive(slotIndex) and (skillGrade == j): # fix lwork
							skillPage.ActivateSlot(realSlotIndex)
						else:
							skillPage.DeactivateSlot(realSlotIndex)

				else:
					if app.ENABLE_PASSIVE_SKILLS:
						if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
							realSlotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)
							if skillIndex in xrange(player.SKILL_INDEX_PASSIVE_MONSTER, player.SKILL_INDEX_PASSIVE_MAX_NUM):
								skillPage.SetSkillSlotPassive(realSlotIndex, skillIndex, skillGrade, skillLevel)
							else:
								skillPage.SetSkillSlot(realSlotIndex, skillIndex, skillLevel)

							skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
							if skill.CanUseSkill(skillIndex):
								skillPage.SetCoverButton(realSlotIndex)

					else:
						if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
							realSlotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)
							skillPage.SetSkillSlot(realSlotIndex, skillIndex, skillLevel)
							skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
							if skill.CanUseSkill(skillIndex):
								skillPage.SetCoverButton(realSlotIndex)

				skillPage.RefreshSlot()

			self.__RestoreSlotCoolTime(skillPage)

			if app.ENABLE_SKILL_COLOR_SYSTEM:
				if "ACTIVE" == name:
					if self.PAGE_HORSE != self.curSelectedSkillGroup and not self.curSelectedSkillGroup == 4:
						self.__CreateSkillColorButton(skillPage)
					else:
						self.skillColorButton = []

	else:
		def __RefreshSkillPage(self, name, slotCount):
			global SHOW_LIMIT_SUPPORT_SKILL_LIST
			global BLOCK_SUPPORT_SKILL_LIST

			skillPage = self.skillPageDict[name]

			startSlotIndex = skillPage.GetStartIndex()
			if "ACTIVE" == name:
				if self.PAGE_HORSE == self.curSelectedSkillGroup:
					startSlotIndex += slotCount

			getSkillType = skill.GetSkillType
			getSkillIndex = player.GetSkillIndex
			getSkillGrade = player.GetSkillGrade
			getSkillLevel = player.GetSkillLevel
			getSkillLevelUpPoint = skill.GetSkillLevelUpPoint
			getSkillMaxLevel = skill.GetSkillMaxLevel

			for i in xrange(slotCount + 1):
				slotIndex = i + startSlotIndex
				skillIndex = getSkillIndex(slotIndex)

				for j in xrange(skill.SKILL_GRADE_COUNT):
					skillPage.ClearSlot(self.__GetRealSkillSlot(j, i))

				if 0 == skillIndex:
					continue

				if skillIndex in BLOCK_SUPPORT_SKILL_LIST:
					continue

				skillGrade = getSkillGrade(slotIndex)
				skillLevel = getSkillLevel(slotIndex)
				skillType = getSkillType(skillIndex)

				if player.SKILL_INDEX_RIDING == skillIndex:
					if skillGrade == 1:
						skillLevel += 19
					elif skillGrade == 2:
						skillLevel += 29
					elif skillGrade == 3:
						skillLevel = 40

					skillPage.SetSkillSlotNew(slotIndex, skillIndex, max(skillLevel - 1, 0), skillLevel)
					skillPage.SetSlotCount(slotIndex, skillLevel)

				elif skill.SKILL_TYPE_ACTIVE == skillType:
					for j in xrange(skill.SKILL_GRADE_COUNT):
						realSlotIndex = self.__GetRealSkillSlot(j, slotIndex)
						skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, j, skillLevel)
						skillPage.SetCoverButton(realSlotIndex)

						if (skillGrade == skill.SKILL_GRADE_COUNT) and j == (skill.SKILL_GRADE_COUNT-1):
							skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
						elif (not self.__CanUseSkillNow()) or (skillGrade != j):
							skillPage.SetSlotCount(realSlotIndex, 0)
							skillPage.DisableCoverButton(realSlotIndex)
							skillPage.DeactivateSlot(realSlotIndex) # fix
						else:
							skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
						if player.IsSkillActive(slotIndex):
							skillPage.ActivateSlot(self.__GetRealSkillSlot(skillGrade, slotIndex))
				else:
					if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
						realSlotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)
						skillPage.SetSkillSlot(realSlotIndex, skillIndex, skillLevel)
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

						if skill.CanUseSkill(skillIndex):
							skillPage.SetCoverButton(realSlotIndex)

						if player.IsSkillActive(slotIndex) and (skillGrade == j): # fix
							skillPage.ActivateSlot(realSlotIndex)

				skillPage.RefreshSlot()

			self.__RestoreSlotCoolTime(skillPage)

			if app.ENABLE_SKILL_COLOR_SYSTEM:
				if "ACTIVE" == name:
					if self.PAGE_HORSE != self.curSelectedSkillGroup and not self.curSelectedSkillGroup == 4:
						self.__CreateSkillColorButton(skillPage)
					else:
						self.skillColorButton = []

	def __RestoreSlotCoolTime(self, skillPage):
		restoreType = skill.SKILL_TYPE_NONE
		skillPage.RestoreSlotCoolTime(skill.SKILL_TYPE_ACTIVE)
		skillPage.RestoreSlotCoolTime(skill.SKILL_TYPE_HORSE)
		skillPage.RestoreSlotCoolTime(restoreType)

	def RefreshSkill(self):
		if self.isLoaded==0:
			return

		if self.__IsChangedHorseRidingSkillLevel():
			self.RefreshCharacter()
			return

		global SHOW_ONLY_ACTIVE_SKILL
		if SHOW_ONLY_ACTIVE_SKILL:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
		else:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
			self.__RefreshSkillPage("HORSE", self.HORSE_SLOT_COUNT)
			self.__RefreshSkillPage("SUPPORT", self.SUPPORT_PAGE_SLOT_COUNT)

		self.RefreshSkillPlusButtonList()

	if app.ENABLE_SKILL_COLOR_SYSTEM:
		def __CreateSkillColorButton(self, parent):
			self.skillColorButton = []

			xPos, yPos = 0, 0
			for idx in xrange(self.PAGE_SLOT_COUNT):
				skillSlot = idx
				if skillSlot < 6:
					if (skillSlot % 2) == 0:
						xPos = 75
						yPos = 4 + (skillSlot / 2 * 36)
					else:
						xPos = 187
						yPos = 4 + (skillSlot / 2 * 36)

					skillIndex = player.GetSkillIndex(skillSlot + 1)
					skillMaxGrade = 3

					if len(self.skillColorButton) == skillSlot:
						self.skillColorButton.append([])
						self.skillColorButton[skillSlot] = ui.Button()
						self.skillColorButton[skillSlot].SetParent(parent)
						self.skillColorButton[skillSlot].SetUpVisual("d:/ymir work/ui/game/skill_color/skill_color_button_default.tga")
						self.skillColorButton[skillSlot].SetOverVisual("d:/ymir work/ui/game/skill_color/skill_color_button_over.tga")
						self.skillColorButton[skillSlot].SetDownVisual("d:/ymir work/ui/game/skill_color/skill_color_button_down.tga")
						self.skillColorButton[skillSlot].SetPosition(xPos, yPos)
						self.skillColorButton[skillSlot].SetEvent(lambda arg = skillSlot, arg2 = skillIndex: self.__OnPressSkillColorButton(arg, arg2))
						if player.GetSkillGrade(skillSlot + 1) >= skillMaxGrade:
							self.skillColorButton[skillSlot].Show()
						else:
							self.skillColorButton[skillSlot].Hide()
					else:
						self.skillColorButton[skillSlot].SetPosition(xPos, yPos)

		def __SetOnMoveWindowPos(self, extended):
			x, y = self.GetGlobalPosition()
			if self.skillColorWndIsShow:
				if extended:
					self.skillColorWnd.SetPosition(x+491,y)
				else:
					self.skillColorWnd.SetPosition(x+250,y)

			if self.chDetailsWnd:
				self.chDetailsWnd.AdjustPosition(x, y)

			if app.ENABLE_LEADERSHIP_EXTENSION:
				try:
					if self.interface:
						if self.interface.wndPartyBonusWindow:
							x, y = self.GetGlobalPosition()
							self.interface.wndPartyBonusWindow.AdjustPosition(x, y + 406)
				except Exception or KeyError:
					pass

		def __OnPressSkillColorButton(self, skillSlot, skillIndex):
			try:
				self.skillColorWnd = uiSkillColor.SkillColorWindow(skillSlot, skillIndex)

				if self.skillColorWnd:
					if self.skillColorWndIsShow:
						self.skillColorWnd.Close()
						self.skillColorWndIsShow = False
					else:
						self.skillColorWnd.Show()
						self.skillColorWndIsShow = True
			except Exception:
					pass

	def CanShowPlusButton(self, skillIndex, skillLevel, curStatPoint):
		if 0 == skillIndex:
			return False

		if not skill.CanLevelUpSkill(skillIndex, skillLevel):
			return False

		return True

	def __RefreshSkillPlusButton(self, name):
		global HIDE_SUPPORT_SKILL_POINT
		if HIDE_SUPPORT_SKILL_POINT and "SUPPORT" == name:
			return

		slotWindow = self.skillPageDict[name]
		slotWindow.HideAllSlotButton()

		labelWindow = self.labelPageStatDict[name]
		slotStatType = self.skillPageStatDict[name]
		if 0 == slotStatType:
			return

		statPoint = player.GetStatus(slotStatType)
		startSlotIndex = slotWindow.GetStartIndex()
		if "HORSE" == name:
			startSlotIndex += self.ACTIVE_PAGE_SLOT_COUNT

		if statPoint > 0:
			labelWindow.Show()
			for i in xrange(self.PAGE_SLOT_COUNT):
				slotIndex = i + startSlotIndex
				skillIndex = player.GetSkillIndex(slotIndex)
				skillGrade = player.GetSkillGrade(slotIndex)
				skillLevel = player.GetSkillLevel(slotIndex)

				if skillIndex == 0:
					continue
				if skillGrade != 0:
					continue

				if name == "HORSE":
					if player.GetStatus(player.LEVEL) >= skill.GetSkillLevelLimit(skillIndex):
						if skillLevel < 20:
							slotWindow.ShowSlotButton(self.__GetETCSkillRealSlotIndex(slotIndex))
				else:
					if "SUPPORT" == name:
						if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
							if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
								slotWindow.ShowSlotButton(slotIndex)
					else:
						if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
							slotWindow.ShowSlotButton(slotIndex)
		else:
			labelWindow.Hide()


	def RefreshSkillPlusButtonList(self):
		if self.isLoaded==0:
			return

		self.RefreshSkillPlusPointLabel()

		if not self.__CanUseSkillNow():
			return

		try:
			self.__RefreshSkillPlusButton("HORSE")
			self.__RefreshSkillPlusButton("ACTIVE")
			self.__RefreshSkillPlusButton("SUPPORT")

		except:
			import exception
			exception.Abort("CharacterWindow.RefreshSkillPlusButtonList.BindObject")

	def RefreshSkillPlusPointLabel(self):
		if self.isLoaded==0:
			return

		activeStatPoint = player.GetStatus(player.SKILL_ACTIVE)
		self.activeSkillPointValue.SetText(str(activeStatPoint))
		horseStatPoint = player.GetStatus(player.SKILL_HORSE)
		self.horseSkillPointValue.SetText(str(horseStatPoint))
		supportStatPoint = max(0, player.GetStatus(player.SKILL_SUPPORT))
		self.supportSkillPointValue.SetText(str(supportStatPoint))

	## Skill Level Up Button
	def OnPressedSlotButton(self, slotNumber):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)

		skillIndex = player.GetSkillIndex(srcSlotIndex)
		curLevel = player.GetSkillLevel(srcSlotIndex)
		maxLevel = skill.GetSkillMaxLevel(skillIndex)

		net.SendChatPacket("/skillup " + str(skillIndex))

	## Use Skill
	def ClickSkillSlot(self, slotIndex):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotIndex)
		skillIndex = player.GetSkillIndex(srcSlotIndex)

		if 0 == skillIndex:
			return
		
		skillType = skill.GetSkillType(skillIndex)

		if not self.__CanUseSkillNow():
			if skill.SKILL_TYPE_ACTIVE == skillType:
				return

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if skill.CanUseSkill(skillIndex):
					player.ClickSkillSlot(srcSlotIndex)
					return

		mouseModule.mouseController.DeattachObject()

	def OnUseSkill(self, slotIndex, coolTime):
		skillIndex = player.GetSkillIndex(slotIndex)

		if 0 == skillIndex:
			return
		
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			skillGrade = player.GetSkillGrade(slotIndex)
			slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		## ETC
		else:
			slotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.StoreSlotCoolTime(skillType, slotIndex, coolTime)
				self.__RestoreSlotCoolTime(slotWindow)
				#slotWindow.SetSlotCoolTime(slotIndex, coolTime)
				return

	def OnActivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.ActivateSlot(slotIndex)
				return

		self.RefreshSkill()

	def OnDeactivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.DeactivateSlot(slotIndex)
				return

		self.RefreshSkill()

	def __ShowJobToolTip(self):
		self.toolTipJob.ShowToolTip()

	def __HideJobToolTip(self):
		self.toolTipJob.HideToolTip()

	def __SetJobText(self, mainJob, subJob):
		if player.GetStatus(player.LEVEL)<5:
			subJob=0

		if 949 == app.GetDefaultCodePage():
			self.toolTipJob.ClearToolTip()

			try:
				jobInfoTitle=localeInfo.JOBINFO_TITLE[mainJob][subJob]
				jobInfoData=localeInfo.JOBINFO_DATA_LIST[mainJob][subJob]
			except IndexError:
				return

			self.toolTipJob.AutoAppendTextLine(jobInfoTitle)
			self.toolTipJob.AppendSpace(5)

			for jobInfoDataLine in jobInfoData:
				self.toolTipJob.AutoAppendTextLine(jobInfoDataLine)

			self.toolTipJob.AlignHorizonalCenter()

	def __ShowAlignmentToolTip(self):
		self.toolTipAlignment.ShowToolTip()

	def __HideAlignmentToolTip(self):
		self.toolTipAlignment.HideToolTip()

	def RefreshCharacter(self):
		if self.isLoaded == 0:
			return

		## Name
		try:
			characterName = player.GetName()
			guildName = player.GetGuildName()
			self.characterNameValue.SetText(characterName)
			self.guildNameValue.SetText(guildName)
			if not guildName:
				self.characterNameSlot.SetPosition(109, 34)
				self.guildNameSlot.Hide()
			else:
				self.characterNameSlot.SetPosition(153, 34)
				self.guildNameSlot.Show()

		except:
			import exception
			exception.Abort("CharacterWindow.RefreshCharacter.BindObject")

		race = net.GetMainActorRace()
		group = net.GetMainActorSkillGroup()
		empire = net.GetMainActorEmpire()

		## Job Text
		job = chr.RaceToJob(race)
		self.__SetJobText(job, group)

		## FaceImage
		try:
			faceImageName = FACE_IMAGE_DICT[race]

			try:
				self.faceImage.LoadImage(faceImageName)
			except:
				self.faceImage.Hide()

		except KeyError:
			self.faceImage.Hide()

		## GroupName
		self.__SetSkillGroupName(race, group)

		## Skill
		if 0 == group:
			self.__SelectSkillGroup(0)

		else:
			self.__SetSkillSlotData(race, group, empire)

	def __SetSkillGroupName(self, race, group):
		job = chr.RaceToJob(race)

		if not self.SKILL_GROUP_NAME_DICT.has_key(job):
			return

		nameList = self.SKILL_GROUP_NAME_DICT[job]

		if 0 == group:
			self.skillGroupButton1.SetText(nameList[1])
			self.skillGroupButton2.SetText(nameList[2])
			self.skillGroupButton1.Show()

			if app.ENABLE_WOLFMAN_CHARACTER and playerSettingModule.RACE_WOLFMAN_M != race:
				self.skillGroupButton2.Show()

			self.activeSkillGroupName.Hide()
		else:
				self.activeSkillGroupName.SetText(nameList.get(group, "Noname"))
				self.activeSkillGroupName.Show()
				self.skillGroupButton1.Hide()
				self.skillGroupButton2.Hide()

	def __SetSkillSlotData(self, race, group, empire=0):
		## SkillIndex
		playerSettingModule.RegisterSkill(race, group, empire)

		## Event
		self.__SetSkillSlotEvent()

		## Refresh
		self.RefreshSkill()

	def __SelectSkillGroup(self, index):
		for btn in self.skillGroupButton:
			btn.SetUp()
		self.skillGroupButton[index].Down()

		self.curSelectedSkillGroup = index
		self.__SetSkillSlotData(net.GetMainActorRace(), index+1, net.GetMainActorEmpire())

	def __CanUseSkillNow(self):
		if 0 == net.GetMainActorSkillGroup():
			return False

		return True

	def __CanUseHorseSkill(self):
		slotIndex = player.GetSkillSlotIndex(player.SKILL_INDEX_RIDING)

		if not slotIndex:
			return False

		grade = player.GetSkillGrade(slotIndex) # hotfix
		level = player.GetSkillLevel(slotIndex)

		if level < 0:
			level *= -1
		# if level >= 20 :
			# return True
		if grade >= 1 and level >= 1: # hotfix
			return True

		return False

	def __IsChangedHorseRidingSkillLevel(self):
		ret = False

		if -1 == self.canUseHorseSkill:
			self.canUseHorseSkill = self.__CanUseHorseSkill()

		if self.canUseHorseSkill != self.__CanUseHorseSkill():
			ret = True

		self.canUseHorseSkill = self.__CanUseHorseSkill()
		return ret

	def __GetRealSkillSlot(self, skillGrade, skillSlot):
		if app.ENABLE_SKILLS_LEVEL_OVER_P:
			return skillSlot + min(self.SKILL_GRADE_SLOT_COUNT-1, skillGrade)*skill.SKILL_GRADE_STEP_COUNT
		else:
			return skillSlot + min(skill.SKILL_GRADE_COUNT-1, skillGrade) * skill.SKILL_GRADE_STEP_COUNT

	def __GetETCSkillRealSlotIndex(self, skillSlot):
		if skillSlot > 100:
			return skillSlot
		return skillSlot % self.ACTIVE_PAGE_SLOT_COUNT

	def __RealSkillSlotToSourceSlot(self, realSkillSlot):
		if realSkillSlot > 100:
			return realSkillSlot
		return realSkillSlot % skill.SKILL_GRADE_STEP_COUNT

	def __GetSkillGradeFromSlot(self, skillSlot):
		return int(skillSlot / skill.SKILL_GRADE_STEP_COUNT)

	def SelectSkillGroup(self, index):
		self.__SelectSkillGroup(index)

	def OnQuestScroll(self):
		questCount = quest.GetQuestCount()
		scrollLineCount = max(0, questCount - quest.QUEST_MAX_NUM)
		startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

		if startIndex != self.questShowingStartIndex:
			self.questShowingStartIndex = startIndex
			self.RefreshQuest()

	if app.ENABLE_QUEST_CATEGORY:
		def __OnScrollQuest(self):
			if self.state != "QUEST":
				return

			curPos = self.questScrollBar.GetPos()
			if math.fabs(curPos - self.questLastScrollPosition) >= 0.001:
				self.RerenderQuestPage()
				self.questLastScrollPosition = curPos

		def ResetQuestScroll(self):
			self.questScrollBar.Hide()

			if self.questScrollBar.GetPos() != 0:
				self.questScrollBar.SetPos(0)

		def RerenderQuestPage(self):
			overflowingY = self.displayY - self.MAX_QUEST_PAGE_HEIGHT
			if overflowingY < 0:
				overflowingY = 0

			self.baseCutY = math.ceil(overflowingY * self.questScrollBar.GetPos())
			self.displayY = 0
			self.RearrangeQuestCategories(range(quest.QUEST_CATEGORY_MAX_NUM))
			self.RefreshQuestCategory()

			if overflowingY > 0:
				if (len(self.questOpenedCategories)) == 0:
					self.ResetQuestScroll()
				else:
					self.questScrollBar.Show()
			else:
				self.ResetQuestScroll()

		def __LoadQuestCategory(self):
			self.questPage.Show()

			if self.isLoaded == 0:
				return

			for i in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				category = self.questCategoryList[i]

				categoryName = category.GetProperty("name")
				if not categoryName:
					category.SetProperty("name", category.GetText())
					categoryName = category.GetText()

				questCount = self.GetQuestCountInCategory(i)
				self.questCategoryList[i].SetTextAlignLeft(categoryName + " (" + str(questCount) + ")")
				self.questCategoryList[i].SetTextColor(self.GetQuestCategoryColor(i))
				self.questCategoryList[i].SetQuestLabel(quest_lable_expend_img_path_dict[i], self.GetQuestCountInCategory(i))
				self.questCategoryList[i].Show()

			self.RefreshQuestCategory()
			if self.isQuestCategoryLoad == False:
				self.questScrollBar.Hide()
			else:
				self.RerenderQuestPage()

			self.isQuestCategoryLoad = True

		def GetQuestCategoryColor(self, category):
			return self.questColorList["default_title"]

		def GetQuestProperties(self, questName):
			findString = {
				"*" : "blue",
				"&" : "green",
				"~" : "golden"
			}

			if questName[0] in findString:
				return (questName[1:], findString[questName[0]])

			return (questName, None)

		def IsQuestCategoryOpen(self, category):
			return (category in self.questOpenedCategories)

		def ToggleCategory(self, category):
			if self.IsQuestCategoryOpen(category):
				self.CloseQuestCategory(category)
			else:
				self.OpenQuestCategory(category)

		def RearrangeQuestCategories(self, categoryRange):
			i = 0
			for i in categoryRange:
				if (self.displayY - self.baseCutY) >= 0 and (self.displayY - self.baseCutY) < self.MAX_QUEST_PAGE_HEIGHT - 20:
					self.questCategoryList[i].SetPosition(13, (self.displayY - self.baseCutY) + 10)
					self.questCategoryList[i].Show()
				else:
					self.questCategoryList[i].Hide()

				self.displayY += 20
				self.questCategoryRenderPos[i] = self.displayY

		def CloseQuestCategory(self, category):
			self.questCategoryList[category].CloseCategory(self.GetQuestCountInCategory(category))

			if category in self.questOpenedCategories:
				self.questOpenedCategories.remove(category)

			for currentSlot in self.questSlotList:
				if currentSlot.GetProperty("category") == category:
					currentSlot.Hide()
					self.displayY -= currentSlot.GetHeight()

			self.RerenderQuestPage()

		def OpenQuestCategory(self, category):
			if self.GetQuestCountInCategory(category) == 0:
				return

			while len(self.questOpenedCategories) >= self.questMaxOpenedCategories:
				openedCategories = self.questOpenedCategories.pop()
				self.CloseQuestCategory(openedCategories)

			self.questCategoryList[category].OpenCategory(self.GetQuestCountInCategory(category))
			self.questOpenedCategories.append(category)
			self.RefreshQuestCategory(category)
			self.RerenderQuestPage()

		def RefreshQuestCategory(self, category = -1):
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			categories = []
			if category == -1:
				categories = self.questOpenedCategories
			elif not category in self.questOpenedCategories:
				self.OpenQuestCategory(category)
				return
			else:
				categories.append(category)

			for currentCategory in categories:
				self.displayY = self.questCategoryRenderPos[currentCategory]

				self.LoadCategory(currentCategory)
				self.RearrangeQuestCategories(xrange(currentCategory + 1, quest.QUEST_CATEGORY_MAX_NUM))

		def RefreshQuestCategoriesCount(self):
			for category in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				categoryName = self.questCategoryList[category].GetProperty("name")
				questCount = self.GetQuestCountInCategory(category)
				self.questCategoryList[category].SetTextAlignLeft(categoryName + " (" + str(questCount) + ")")
				self.questCategoryList[category].SetQuestLabel(quest_lable_expend_img_path_dict[category], questCount)
				if questCount <= 0:
					self.CloseQuestCategory(category)

		def RefreshQuest(self):
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			for category in self.questOpenedCategories:
				self.RefreshQuestCategory(category)

			self.RefreshQuestCategoriesCount()

		def CreateQuestSlot(self, name):
			for questSlot in self.questSlotList:
				if questSlot.GetWindowName() == name:
					return questSlot

			pyScrLoader = ui.PythonScriptLoader()
			slot = ui.ListBar()
			pyScrLoader.LoadElementListBar(slot, quest_slot_listbar, self.questPage)

			slot.SetParent(self.quest_page_board_window)
			slot.SetWindowName(name)
			slot.Hide()
			self.questSlotList.append(slot)
			return slot

		def SetQuest(self, slot, questID, questName, questCounterName, questCounterValue):
			(name, color) = self.GetQuestProperties(questName)
			slot.SetTextAlignLeft(name, 20)
			if color:
				slot.SetTextColor(self.questColorList[color])
			slot.SetEvent(ui.__mem_func__(self.__SelectQuest), questID)
			slot.SetWindowHorizontalAlignLeft()
			slot.Show()

		def LoadCategory(self, category):
			self.questIndexMap = {}
			self.questCounterList = []
			self.questClockList = []
			self.questSeparatorList = []

			for questSlot in self.questSlotList:
				questSlot.Hide()

			questCount = 0
			for questIdx in self.GetQuestsInCategory(category):
				questCount += 1
				(questID, questIndex, questName, questCategory, _, questCounterName, questCounterValue) = questIdx
				(lastName, lastTime) = quest.GetQuestLastTime(questID)

				slot = self.CreateQuestSlot("QuestSlotList_" + str(questCategory) + "_" + str(questID))

				slot.SetPosition(0, (self.displayY - self.baseCutY))
				slot.SetParent(self.quest_page_board_window)
				baseDisplayY = self.displayY

				## -- Quest Counter
				hasCounter = False
				if questCounterName != "":
					self.displayY += 15

					counter = ui.TextLine()
					counter.SetParent(slot)
					counter.SetPosition(20, 20 - 2.5)
					counter.SetText(questCounterName + ": " + str(questCounterValue))
					counter.Show()

					self.questCounterList.append(counter)
					hasCounter = True
				## -- Quest Counter

				## -- Quest Clock
				self.displayY += 15

				clockText = localeInfo.QUEST_UNLIMITED_TIME
				if len(lastName) > 0:
					if lastTime <= 0:
						clockText = localeInfo.QUEST_TIMEOVER
					else:
						questLastMinute = lastTime / 60
						questLastSecond = lastTime % 60

						clockText = lastName + " : "

						if questLastMinute > 0:
							clockText += str(questLastMinute) + localeInfo.QUEST_MIN
							if questLastSecond > 0:
								clockText += " "

						if questLastSecond > 0:
							clockText += str(questLastSecond) + localeInfo.QUEST_SEC

				clock = ui.TextLine()
				clock.SetParent(slot)
				clock.SetPosition(0, 20 + (int(hasCounter) * 14) - 2.5)
				clock.SetText(clockText)
				clock.SetHorizontalAlignCenter()
				clock.SetVerticalAlignCenter()
				clock.SetWindowHorizontalAlignCenter()
				clock.SetWindowVerticalAlignCenter()
				clock.SetProperty("idx", questID)
				self.questClockList.append(clock)
				clock.Show()
				## -- Quest Clock

				## -- Quest Separator
				self.displayY += 5
				if questCount < self.GetQuestCountInCategory(category):
					seperator = ui.ImageBox()
					seperator.SetParent(slot)
					seperator.SetPosition(4, 20 + (int(hasCounter) * 14 - 2.5) + 15)
					seperator.LoadImage("d:/ymir work/ui/quest_re/quest_list_line_01.tga")
					seperator.Show()
					self.questSeparatorList.append(seperator)
				## -- Quest Separator

				slot.SetProperty("category", questCategory)

				if questIndex in self.questClicked:
					slot.OnClickEvent()

				if (baseDisplayY - self.baseCutY) + 2 >= 0 and (baseDisplayY - self.baseCutY) + 2 < self.MAX_QUEST_PAGE_HEIGHT - 30:
					self.questIndexMap[questID] = questIndex
					self.SetQuest(slot, questID, questName, questCounterName, questCounterValue)

				self.displayY += 15

			newList = []
			for questSlot in self.questSlotList:
				if questSlot.IsShow():
					newList.append(questSlot)

			self.questSlotList = newList

		def __OnClickQuestCategoryButton(self, category):
			self.ToggleCategory(category)

		def GetQuestsInCategory(self, category, retCount = False):
			questList = []
			count = 0
			for i in xrange(quest.GetQuestCount()):
				(questIndex, questName, questCategory, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(i)
				if questCategory == category:
					count += 1
					questList.append((i, questIndex, questName, questCategory, questIcon, questCounterName, questCounterValue))

			if retCount:
				return count

			return questList

		def GetQuestCountInCategory(self, category):
			return self.GetQuestsInCategory(category, True)