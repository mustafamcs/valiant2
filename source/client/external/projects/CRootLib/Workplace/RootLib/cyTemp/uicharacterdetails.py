# -*- coding: cp949 -*-
#-522043353
import ui, player, item, app, localeInfo, uiScriptLocale
from uiToolTip import ItemToolTip

import constInfo

IMG_DIR = "d:/ymir work/ui/game/characterdetails/"
bonus_list = [
	[localeInfo.BONUS_TABLE_TITLE_1,
		[
			[item.APPLY_ATTBONUS_MONSTER, item.GetApplyPoint(item.APPLY_ATTBONUS_MONSTER)],
			[item.APPLY_ATTBONUS_STONE, item.GetApplyPoint( item.APPLY_ATTBONUS_STONE )],
			[item.APPLY_ATTBONUS_BOSS, item.GetApplyPoint( item.APPLY_ATTBONUS_BOSS )],
			[item.APPLY_ATTBONUS_PVM_STR, item.GetApplyPoint( item.APPLY_ATTBONUS_PVM_STR )],
			[item.APPLY_ATTBONUS_PVM_AVG, item.GetApplyPoint( item.APPLY_ATTBONUS_PVM_AVG )],
			[item.APPLY_ATTBONUS_PVM_BERSERKER, item.GetApplyPoint( item.APPLY_ATTBONUS_PVM_BERSERKER )],
			[item.APPLY_ATT_GRADE_BONUS, item.GetApplyPoint( item.APPLY_ATT_GRADE_BONUS )],
			[item.APPLY_DEF_GRADE_BONUS, item.GetApplyPoint( item.APPLY_DEF_GRADE_BONUS )],
			[item.APPLY_ATTBONUS_HUMAN, item.GetApplyPoint( item.APPLY_ATTBONUS_HUMAN )],
			[item.APPLY_ATTBONUS_ORC, item.GetApplyPoint( item.APPLY_ATTBONUS_ORC )],
			[item.APPLY_ATTBONUS_UNDEAD, item.GetApplyPoint( item.APPLY_ATTBONUS_UNDEAD )],
			[item.APPLY_ATTBONUS_ANIMAL, item.GetApplyPoint( item.APPLY_ATTBONUS_ANIMAL )],
			[item.APPLY_ATTBONUS_MILGYO, item.GetApplyPoint( item.APPLY_ATTBONUS_MILGYO )],
			[item.APPLY_ATTBONUS_DEVIL, item.GetApplyPoint( item.APPLY_ATTBONUS_DEVIL )],
			[item.APPLY_NORMAL_HIT_DAMAGE_BONUS, item.GetApplyPoint( item.APPLY_NORMAL_HIT_DAMAGE_BONUS )],
			[item.APPLY_NORMAL_HIT_DEFEND_BONUS, item.GetApplyPoint( item.APPLY_NORMAL_HIT_DEFEND_BONUS )],
			[item.APPLY_SKILL_DAMAGE_BONUS, item.GetApplyPoint( item.APPLY_SKILL_DAMAGE_BONUS )],
			[item.APPLY_SKILL_DEFEND_BONUS, item.GetApplyPoint( item.APPLY_SKILL_DEFEND_BONUS )],
			[item.APPLY_MELEE_MAGIC_ATTBONUS_PER, item.GetApplyPoint( item.APPLY_MELEE_MAGIC_ATTBONUS_PER )],
			[item.APPLY_MAGIC_ATTBONUS_PER, item.GetApplyPoint( item.APPLY_MAGIC_ATTBONUS_PER )],
			[item.APPLY_CRITICAL_PCT, item.GetApplyPoint( item.APPLY_CRITICAL_PCT )],
			[item.APPLY_PENETRATE_PCT, item.GetApplyPoint( item.APPLY_PENETRATE_PCT )],
			[item.APPLY_ANTI_CRITICAL_PCT, item.GetApplyPoint( item.APPLY_ANTI_CRITICAL_PCT )],
			[item.APPLY_ANTI_PENETRATE_PCT, item.GetApplyPoint( item.APPLY_ANTI_PENETRATE_PCT )],
		]
	],
	[localeInfo.BONUS_TABLE_TITLE_2,
		[

			[item.APPLY_ATTBONUS_ELEMENT, item.GetApplyPoint( item.APPLY_ATTBONUS_ELEMENT )],
			[item.APPLY_DEFBONUS_ELEMENT, item.GetApplyPoint( item.APPLY_DEFBONUS_ELEMENT )],

			[item.APPLY_ATTBONUS_FIRE, item.GetApplyPoint( item.APPLY_ATTBONUS_FIRE )],
			[item.APPLY_ATTBONUS_ICE, item.GetApplyPoint( item.APPLY_ATTBONUS_ICE )],
			[item.APPLY_ATTBONUS_WIND, item.GetApplyPoint( item.APPLY_ATTBONUS_WIND )],
			[item.APPLY_ATTBONUS_EARTH, item.GetApplyPoint( item.APPLY_ATTBONUS_EARTH )],
			[item.APPLY_ATTBONUS_DARK, item.GetApplyPoint( item.APPLY_ATTBONUS_DARK )],
			[item.APPLY_ATTBONUS_ELEC, item.GetApplyPoint( item.APPLY_ATTBONUS_ELEC )],

			[item.APPLY_RESIST_FIRE, item.GetApplyPoint( item.APPLY_RESIST_FIRE )],
			[item.APPLY_RESIST_ICE, item.GetApplyPoint( item.APPLY_RESIST_ICE )],
			[item.APPLY_RESIST_EARTH, item.GetApplyPoint( item.APPLY_RESIST_EARTH )],
			[item.APPLY_RESIST_WIND, item.GetApplyPoint( item.APPLY_RESIST_WIND )],
			[item.APPLY_RESIST_DARK, item.GetApplyPoint( item.APPLY_RESIST_DARK )],
			[item.APPLY_RESIST_ELEC, item.GetApplyPoint( item.APPLY_RESIST_ELEC )],
		]
	],
	[localeInfo.BONUS_TABLE_TITLE_4,
		[

			[item.APPLY_DEFBONUS_PVM, item.GetApplyPoint( item.APPLY_DEFBONUS_PVM )],

			[item.APPLY_ATTBONUS_PVP, item.GetApplyPoint( item.APPLY_ATTBONUS_PVP )],
			[item.APPLY_DEFBONUS_PVP, item.GetApplyPoint( item.APPLY_DEFBONUS_PVP )],

			[item.APPLY_RESIST_SWORD, item.GetApplyPoint( item.APPLY_RESIST_SWORD )],
			[item.APPLY_RESIST_TWOHAND, item.GetApplyPoint( item.APPLY_RESIST_TWOHAND )],
			[item.APPLY_RESIST_DAGGER, item.GetApplyPoint( item.APPLY_RESIST_DAGGER )],
			[item.APPLY_RESIST_BELL, item.GetApplyPoint( item.APPLY_RESIST_BELL )],
			[item.APPLY_RESIST_FAN, item.GetApplyPoint( item.APPLY_RESIST_FAN )],
			[item.APPLY_RESIST_BOW, item.GetApplyPoint( item.APPLY_RESIST_BOW )],

			[item.APPLY_ATTBONUS_WARRIOR, item.GetApplyPoint(item.APPLY_ATTBONUS_WARRIOR)],
			[item.APPLY_ATTBONUS_ASSASSIN, item.GetApplyPoint(item.APPLY_ATTBONUS_ASSASSIN )],
			[item.APPLY_ATTBONUS_SURA, item.GetApplyPoint(item.APPLY_ATTBONUS_SURA )],
			[item.APPLY_ATTBONUS_SHAMAN, item.GetApplyPoint( item.APPLY_ATTBONUS_SHAMAN )],
			# [item.APPLY_ATTBONUS_WOLFMAN, item.GetApplyPoint( item.APPLY_ATTBONUS_WOLFMAN )],

			[item.APPLY_RESIST_WARRIOR, item.GetApplyPoint(item.APPLY_RESIST_WARRIOR)],
			[item.APPLY_RESIST_ASSASSIN, item.GetApplyPoint(item.APPLY_RESIST_ASSASSIN)],
			[item.APPLY_RESIST_SURA, item.GetApplyPoint(item.APPLY_ATTBONUS_SURA)],
			[item.APPLY_RESIST_SHAMAN, item.GetApplyPoint( item.APPLY_RESIST_SHAMAN )],
			# [item.APPLY_ATTBONUS_WOLFMAN, item.GetApplyPoint( item.APPLY_ATTBONUS_WOLFMAN )],

		]
	],
	[localeInfo.BONUS_TABLE_TITLE_5,
		[
			[item.APPLY_STUN_PCT, item.GetApplyPoint( item.APPLY_STUN_PCT )],
			[item.APPLY_SLOW_PCT, item.GetApplyPoint( item.APPLY_SLOW_PCT )],
			[item.APPLY_POISON_PCT, item.GetApplyPoint( item.APPLY_POISON_PCT )],
			[item.APPLY_POISON_REDUCE, item.GetApplyPoint( item.APPLY_POISON_REDUCE )],
			[item.APPLY_STEAL_HP, item.GetApplyPoint( item.APPLY_STEAL_HP )],
			[item.APPLY_STEAL_SP, item.GetApplyPoint( item.APPLY_STEAL_SP )],
			[item.APPLY_HP_REGEN, item.GetApplyPoint( item.APPLY_HP_REGEN )],
			[item.APPLY_SP_REGEN, item.GetApplyPoint( item.APPLY_SP_REGEN )],
			[item.APPLY_BLOCK, item.GetApplyPoint( item.APPLY_BLOCK )],
			[item.APPLY_DODGE, item.GetApplyPoint( item.APPLY_DODGE )],
			[item.APPLY_REFLECT_MELEE, item.GetApplyPoint( item.APPLY_REFLECT_MELEE )],
			[item.APPLY_KILL_HP_RECOVER, item.GetApplyPoint( item.APPLY_KILL_HP_RECOVER )],
			[item.APPLY_KILL_SP_RECOVER, item.GetApplyPoint( item.APPLY_KILL_SP_RECOVER )],
			[item.APPLY_EXP_DOUBLE_BONUS, item.GetApplyPoint( item.APPLY_EXP_DOUBLE_BONUS )],
			[item.APPLY_GOLD_DOUBLE_BONUS, item.GetApplyPoint( item.APPLY_GOLD_DOUBLE_BONUS )],
			[item.APPLY_ITEM_DROP_BONUS, item.GetApplyPoint( item.APPLY_ITEM_DROP_BONUS )],
		]
	],
]

stat_list = [
    [uiScriptLocale.STATICS_01, "stats/max_player_damage.png"],
    [uiScriptLocale.STATICS_02, "stats/max_monster_damage.png"],
    [uiScriptLocale.STATICS_03, "stats/max_stone_damage.png"],
    [uiScriptLocale.STATICS_04, "stats/max_boss_damage.png"],
    [uiScriptLocale.STATICS_05, "stats/max_monster_damage.png"],
    [uiScriptLocale.STATICS_06, "stats/max_stone_damage.png"],
    [uiScriptLocale.STATICS_07, "stats/max_boss_damage.png"],
    [uiScriptLocale.STATICS_08, "stats/max_player_damage.png"],
    [uiScriptLocale.STATICS_09, "stats/upgrade_count.png"],
    [uiScriptLocale.STATICS_10, "stats/dungeon_count.png"],
    [uiScriptLocale.STATICS_11, "stats/catched_fish.png"],
    [uiScriptLocale.STATICS_12, "stats/mine_count.png"],
    [uiScriptLocale.STATICS_13, "stats/opened_chests.png"],
    [uiScriptLocale.STATICS_14, "stats/max_player_damage.png"]
]

def GetStatisticElement(index):
	statList = dict()

	statList = [ \
		player.GetStatus(player.POINT_PLAYER_DAMAGE),
		player.GetStatus(player.POINT_MONSTER_DAMAGE),
		player.GetStatus(player.POINT_STONE_DAMAGE),
		player.GetStatus(player.POINT_BOSS_DAMAGE),
		player.GetStatus(player.POINT_MONSTER_KILLED),
		player.GetStatus(player.POINT_STONE_KILLED),
		player.GetStatus(player.POINT_BOSS_KILLED),
		player.GetStatus(player.POINT_PLAYER_KILLED),
		player.GetStatus(player.POINT_UPGRADE_ITEM),
		player.GetStatus(player.POINT_COMPLATE_DUNGEON),
		player.GetStatus(player.POINT_FISHING),
		player.GetStatus(player.POINT_MINING),
		player.GetStatus(player.POINT_OPENED_CHEST),
		player.GetStatus(player.POINT_USE_ENCHANTED_ITEM)
	]

	return statList[index]


class CharacterDetailsUI(ui.ScriptWindow):
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.btnIndex = 0

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetTop()
		self.Refresh()

	def Close(self):
		self.Hide()

	def AdjustPosition(self, x, y):
		self.SetPosition(x + self.GetWidth(), y)

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			radioBtn = buttonList[buttonIndex]
		except IndexError:
			return
		for eachButton in buttonList:
			eachButton.SetUp()
		radioBtn.Down()

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Destroy()
		self.__LoadScript()
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CharacterDetailsWindow.py")

			self.GetChild("bonus_button").SAFE_SetEvent(self.SetCategory, 0)
			self.GetChild("stat_button").SAFE_SetEvent(self.SetCategory, 1)
			
		except:
			import exception
			exception.Abort("CharacterDetailsUI.__LoadScript")

		elementList = self.ElementDictionary
		self.statisticContainer = list()

		statWindow = self.GetChild("stat_window")

		clipParentStats = ui.Window()
		clipParentStats.SetParent(statWindow)
		clipParentStats.SetPosition(0, 8)
		clipParentStats.SetSize(227, 352)
		clipParentStats.Hide()
		elementList["clipParentStats"] = clipParentStats

		for index, item in enumerate(stat_list):
			desc = item[0]
			image = item[1]
			stat = StatisticElement(statWindow, desc, image, index)
			stat.Hide()
			self.statisticContainer.append(stat)

		statisticsScrollbar = ui.ScrollBarAe()
		statisticsScrollbar.SetParent(statWindow)
		statisticsScrollbar.SetPosition(220, 0)
		statisticsScrollbar.SetScrollBarSize(362)
		statisticsScrollbar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		statisticsScrollbar.SetScrollStep(0.05)
		statisticsScrollbar.Show()
		self.statisticsScrollbar = statisticsScrollbar

		self.ResetScrollBarPos()
		self.ResizeScrollBar()	
		self.AdjustItemPositions()

		search_winodw = self.GetChild("search_winodw")
		bonusWindow = self.GetChild("bonus_window")

		searchBoard = SearchSlotBoard()
		searchBoard.SetParent(search_winodw)
		searchBoard.SetPosition((search_winodw.GetWidth()/2)-(129/2),11)
		searchBoard.SetSize(129, 23)
		searchBoard.Show()
		elementList["searchBoard"] = searchBoard

		itemSearch = ui.EditLine()
		itemSearch.SetParent(searchBoard)
		itemSearch.SetMax(24)
		itemSearch.SetPosition(5,5)
		itemSearch.SetSize(searchBoard.GetWidth(), searchBoard.GetHeight())
		itemSearch.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		itemSearch.Show()
		elementList["itemSearch"] = itemSearch

		scrollBar = ui.SlimScrollBar()
		scrollBar.SetParent(bonusWindow)
		scrollBar.SetPosition((bonusWindow.GetWidth()-scrollBar.GetWidth())+5, 2)
		scrollBar.SetScrollBarSize((bonusWindow.GetHeight()-2))
		scrollBar.SetScrollEvent(ui.__mem_func__(self.Refresh))
		scrollBar.Show()
		elementList["scrollBar"] = scrollBar

		clipParent = ui.Window()
		clipParent.SetParent(bonusWindow)
		clipParent.SetPosition(0, 4)
		clipParent.SetSize(227, 300)
		clipParent.Hide()

		elementList["clipParent"] = clipParent

		for i in xrange(len(bonus_list)):
			bonus_data = bonus_list[i][1]

			category = ui.ExpandedImageBox()
			category.SetParent(bonusWindow)
			category.LoadImage(IMG_DIR+"category_item.png")
			category.buttonStatus = 0
			category.SetEvent(ui.__mem_func__(self.SetBonusCategory), "mouse_click", i)
			# category.OnMouseOverIn = lambda arg=i, event="OVERIN":self.OverCategory(event, arg)
			# category.OnMouseOverOut = lambda arg=i, event="OVEROUT":self.OverCategory(event, arg)

			category.Show()
			elementList["%d_category"%i] = category

			categoryExpandedImage = ui.ExpandedImageBox()
			categoryExpandedImage.SetParent(category)
			categoryExpandedImage.SetPosition(192, 6)
			categoryExpandedImage.LoadImage("icon/emoji/others/expand.png")
			categoryExpandedImage.OnMouseLeftButtonDown = lambda category=i : self.SetBonusCategory(None, categoryIndex=category)
			categoryExpandedImage.Show()

			elementList["%d_categoryExpandedImage"%i] = categoryExpandedImage

			categoryText = ui.TextLine()
			categoryText.SetParent(category)
			categoryText.SetHorizontalAlignCenter()
			categoryText.SetVerticalAlignCenter()
			categoryText.SetWindowHorizontalAlignCenter()
			categoryText.SetWindowVerticalAlignCenter()
			categoryText.SetPosition(0, 0)
			categoryText.SetText(bonus_list[i][0])
			categoryText.Show()
			elementList["%d_categoryText"%i] = categoryText

			for j in xrange(len(bonus_data)):
				bonusImage = ui.ExpandedImageBox()
				bonusImage.SetParent(bonusWindow)
				bonusImage.LoadImage(IMG_DIR+"bonus_item.tga")
				bonusImage.Show()
				elementList["%d_%d_image"%(i,j)] = bonusImage

				bonusText = ItemToolTip.AFFECT_DICT[bonus_data[j][0]](0)

				disabledStr = ["%","+"]
				newText = ""
				for x in bonusText:
					if x in disabledStr:
						continue
					if x.isdigit():
						continue
					newText+=x
				bonusText=newText

				bonusName = ui.TextLine()
				bonusName.AddFlag("not_pick")
				bonusName.SetParent(bonusImage)
				bonusName.SetHorizontalAlignCenter()
				bonusName.SetPosition(72,3)
				bonusName.SetText(bonusText)

				newText = ""
				if bonusName.GetTextSize()[0] > 134:
					for o in xrange(100):
						if bonusName.GetTextSize()[0] > 134:
							newText = bonusName.GetText()[:len(bonusName.GetText())-2]+"..."
							bonusName.SetText(bonusName.GetText()[:len(bonusName.GetText())-2])
						else:
							break

				if newText != "":
					bonusName.SetText(newText)

				bonusName.Show()
				elementList["%d_%d_name"%(i,j)] = bonusName

				bonusValue = ui.TextLine()
				bonusValue.AddFlag("not_pick")
				bonusValue.SetParent(bonusImage)
				bonusValue.SetHorizontalAlignCenter()
				bonusValue.SetPosition(170,3)
				# bonusValue.SetFontName("Tahoma:13")
				bonusValue.SetText("0")
				bonusValue.Show()
				elementList["%d_%d_value"%(i,j)] = bonusValue

		self.SetCategory(0)

	def __OnValueUpdate(self):
		elementList = self.ElementDictionary
		itemSearch = elementList["itemSearch"]
		ui.EditLine.OnIMEUpdate(itemSearch)
		bonusWindow = self.GetChild("bonus_window")
		searchText = itemSearch.GetText()
		board = elementList["searchBoard"]
		totalWidth = 129
		if len(searchText) > 0:
			self.ElementDictionary["scrollBar"].SetPos(0, True)
			totalWidth-=25
			windowHeight = bonusWindow.GetWidth()-15
			textSize = itemSearch.GetTextSize()[0]
			if textSize >= totalWidth:
				if textSize >= windowHeight:
					totalWidth = windowHeight
				else:
					totalWidth = textSize
			totalWidth+=25
			if totalWidth >= windowHeight:
				totalWidth = windowHeight
		board.SetSize(totalWidth,23)
		itemSearch.SetSize(totalWidth,23)
		board.SetPosition((bonusWindow.GetWidth()/2)-(board.GetWidth()/2),11)
		self.Refresh()

	def OverCategory(self, event, element):
		button = self.ElementDictionary["%d_category"%element]
		isActive = False
		for category in xrange(len(bonus_list)):
			btn = self.ElementDictionary["%d_category"%category]
			if btn.buttonStatus:
				isActive = True

		if event=="OVERIN":
			if isActive:
				button.LoadImage(IMG_DIR+"hover.png")
			else:
				button.LoadImage(IMG_DIR+"no_hover.png")
		else:
			if isActive:
				button.LoadImage(IMG_DIR+"category_item.png")
			else:
				button.LoadImage(IMG_DIR+"no_category_item.png")

	def SetBonusCategory(self, emptyArg, categoryIndex):
		category = self.ElementDictionary["%d_category"%categoryIndex]
		category.buttonStatus = not category.buttonStatus

		if category.buttonStatus == 0:
			self.ElementDictionary["%d_categoryExpandedImage"%categoryIndex].LoadImage("icon/emoji/others/expand.png")
		else:
			self.ElementDictionary["%d_categoryExpandedImage"%categoryIndex].LoadImage("icon/emoji/others/collapse.png")

		self.Refresh()

	def Refresh(self):
		elementList = self.ElementDictionary

		(X_POS,Y_POS) = (3, 3)
		CATEGORY_Y_RANGE = 30
		CATEGORY_Y_FIRST_BONUS_RANGE = 29
		BONUS_X = 13

		if self.btnIndex == 0:
			bonusWindow = self.GetChild("bonus_window")
			scrollBar = self.GetChild("scrollBar")
			(basePos,windowHeight) = (0,bonusWindow.GetHeight()-46)

			searchText = elementList["itemSearch"].GetText().lower()

			maxHeight = 0
			if len(searchText) > 0:
				for i in xrange(len(bonus_list)):
					bonus_data = bonus_list[i][1]
					for j in xrange(len(bonus_data)):
						text = elementList["%d_%d_name"%(i,j)].GetText().lower()
						if text.find(searchText) != -1:
							maxHeight += CATEGORY_Y_FIRST_BONUS_RANGE
			else:
				for i in xrange(len(bonus_list)):
					bonus_data = bonus_list[i][1]
					if elementList.has_key("%d_category"%i):
						categoryBtn = elementList["%d_category"%i]
						if categoryBtn.buttonStatus == 0:
							maxHeight += CATEGORY_Y_RANGE
						else:
							maxHeight += CATEGORY_Y_FIRST_BONUS_RANGE
							for j in xrange(len(bonus_data)):
								maxHeight += CATEGORY_Y_FIRST_BONUS_RANGE

			if maxHeight > windowHeight:
				scrollLen = maxHeight-windowHeight
				basePos = int(scrollBar.GetPos()*scrollLen)
				stepSize = 1.0 / (scrollLen/100.0)
				scrollBar.SetScrollStep(stepSize/2)
				scrollBar.SetMiddleBarSize(float(windowHeight-5)/float(maxHeight))
				scrollBar.Show()
				for i in xrange(len(bonus_list)):
					elementList["%d_category"%i].LoadImage(IMG_DIR+"category_item.png")
			else:
				scrollBar.Hide()
				for i in xrange(len(bonus_list)):
					elementList["%d_category"%i].LoadImage(IMG_DIR+"no_category_item.png")

			textLines = []
			images = []
			_wy = bonusWindow.GetGlobalPosition()[1]+43

			if len(searchText) > 0:
				for i in xrange(len(bonus_list)):
					bonus_data = bonus_list[i][1]
					if elementList.has_key("%d_category"%i):
						elementList["%d_category"%i].Hide()
						for j in xrange(len(bonus_data)):
							text = elementList["%d_%d_name"%(i,j)].GetText().lower()
							if text.find(searchText) != -1:
								elementList["%d_%d_image"%(i,j)].Show()
								elementList["%d_%d_image"%(i,j)].SetPosition(BONUS_X, Y_POS - basePos, True)
								elementList["%d_%d_value"%(i,j)].SetText(str(player.GetStatus(bonus_data[j][1])))
								Y_POS += CATEGORY_Y_FIRST_BONUS_RANGE
								images.append(elementList["%d_%d_image"%(i,j)])
								textLines.append(elementList["%d_%d_name"%(i,j)])
								textLines.append(elementList["%d_%d_value"%(i,j)])
							else:
								elementList["%d_%d_image"%(i,j)].Hide()
			else:
				for i in xrange(len(bonus_list)):
					bonus_data = bonus_list[i][1]
					if elementList.has_key("%d_category"%i):
						categoryBtn = elementList["%d_category"%i]
						categoryBtn.SetPosition(X_POS, Y_POS - basePos, True)
						categoryBtn.Show()

						images.append(categoryBtn)
						textLines.append(elementList["%d_categoryText"%i])

						if categoryBtn.buttonStatus == 0:
							Y_POS += CATEGORY_Y_RANGE
							for j in xrange(len(bonus_data)):
								elementList["%d_%d_image"%(i,j)].Hide()
						else:
							Y_POS += CATEGORY_Y_FIRST_BONUS_RANGE
							for j in xrange(len(bonus_data)):
								elementList["%d_%d_image"%(i,j)].Show()
								elementList["%d_%d_image"%(i,j)].SetPosition(BONUS_X, Y_POS - basePos, True)
								elementList["%d_%d_value"%(i,j)].SetText(str(player.GetStatus(bonus_data[j][1])))
								Y_POS += CATEGORY_Y_FIRST_BONUS_RANGE

								images.append(elementList["%d_%d_image"%(i,j)])
								textLines.append(elementList["%d_%d_name"%(i,j)])
								textLines.append(elementList["%d_%d_value"%(i,j)])

			generalParent = elementList["clipParent"]
			xList, yList = generalParent.GetGlobalPosition()
			widthList, heightList = generalParent.GetWidth(), generalParent.GetHeight()	


			for x in xrange(len(bonus_list)):
				images.append(elementList["%d_categoryExpandedImage"%x])

			for childItem in textLines:
				if childItem:
					childItem.SetClippingMaskWindow(generalParent)

			for childItem in images:
					if childItem:
						childItem.SetClipRect(xList, yList, xList + widthList, yList + heightList)

		elif self.btnIndex == 1:
			self.statisticsScrollbar.Show()

	def OnUpdate(self):
		if len(self.ElementDictionary["itemSearch"].GetText()) > 0:
			self.ElementDictionary["itemSearch"].SetOverlayText("")
		else:
			self.ElementDictionary["itemSearch"].SetOverlayText(localeInfo.BONUS_TABLE_ENTER_BONUSNAME)

		for index, statElement in enumerate(self.statisticContainer):
			statElement.statisticValue.SetText(localeInfo.NumberToDecimal("%d"% GetStatisticElement(index)))


	def SetCategory(self, categoryIndex):
		self.btnIndex = categoryIndex
		self.__ClickRadioButton([self.GetChild("bonus_button"),self.GetChild("stat_button")],categoryIndex)
		self.ElementDictionary["itemSearch"].KillFocus()

		if self.btnIndex == 0:
			self.GetChild("bonus_window").Show()
			self.GetChild("stat_window").Hide()

		elif self.btnIndex == 1:
			self.GetChild("bonus_window").Hide()
			self.GetChild("stat_window").Show()
			self.ResetScrollBarPos()

		self.Refresh()

	def ResetScrollBarPos(self):
		self.statisticsScrollbar.SetPos(0)

	def GetTotalItemHeight(self):
		totalHeight = 0
		
		if self.statisticContainer:
			for itemH in self.statisticContainer:
				totalHeight += itemH.GetHeight()
			
		return totalHeight

	def __OnScroll(self):
		self.AdjustItemPositions(True)

	def ResizeScrollBar(self):

		totalHeight = float(self.GetTotalItemHeight())

		if totalHeight:
			scrollBarHeight = min(float(self.GetChild("stat_window").GetHeight() - 10) / totalHeight, 1.0)
		else:
			scrollBarHeight = 1.0
			
		self.statisticsScrollbar.SetMiddleBarSize(scrollBarHeight)

	def AdjustItemPositions(self, scrolling=False):
		scrollPos = self.statisticsScrollbar.GetPos()
		totalHeight = self.GetTotalItemHeight() - self.GetChild("stat_window").GetHeight()

		idx = 0

		CurIdx, yAccumulate = 0, 0
		for item in self.statisticContainer[idx:]:
			if scrolling:
				setPos = yAccumulate - int(scrollPos * totalHeight)
				item.backgroundImage.SetPosition(0, setPos)
			else:
				item.backgroundImage.SetPosition(0, yAccumulate)
				
			CurIdx += 1
			#Mesafe
			yAccumulate += item.backgroundImage.GetHeight()

	def OnRender(self):
		parent = self.ElementDictionary["clipParentStats"]

		xList, yList = parent.GetGlobalPosition()
		widthList, heightList = parent.GetWidth(), parent.GetHeight()
	
		for itemH in self.statisticContainer:
			itemH.backgroundImage.SetClipRect(xList, yList - 5, xList + widthList + 20, yList + heightList)
			itemH.valueContainer.SetClipRect(xList, yList, xList + widthList, yList + heightList)

			itemH.statisticDesc.SetClippingMaskWindow(parent)
			itemH.statisticValue.SetClippingMaskWindow(parent)

	def OnRunMouseWheel(self, nLen):
		if self.btnIndex == 0:
			if self.ElementDictionary.has_key("scrollBar"):
				scrollBar = self.ElementDictionary["scrollBar"]
		else:
			if self.statisticsScrollbar:
				scrollBar = self.statisticsScrollbar


		if scrollBar.IsShow():
			if nLen > 0:
				scrollBar.OnUp()
			else:
				scrollBar.OnDown()

			return True
		return False

class StatisticElement(ui.Window):

	def __init__(self, parent, desc, image, index):
		ui.Window.__init__(self)
		self.index = index
		self.parent = parent

		self.backgroundImage = ui.MakeExpandedImageBox(parent, IMG_DIR + image, 6, 5)
		self.statisticDesc = ui.MakeTextLineNew(self.backgroundImage, 0, -15, desc)

		self.statisticDesc.SetHorizontalAlignCenter()
		self.statisticDesc.SetVerticalAlignCenter()
		self.statisticDesc.SetWindowHorizontalAlignCenter()
		self.statisticDesc.SetWindowVerticalAlignCenter()

		self.valueContainer = ui.MakeExpandedImageBox(self.backgroundImage, IMG_DIR+"statsinfobg.png", 70, 25)
		self.statisticValue = ui.MakeTextLineNew(self.valueContainer, 0, 0, "0")

		self.statisticValue.SetHorizontalAlignCenter()
		self.statisticValue.SetVerticalAlignCenter()
		self.statisticValue.SetWindowHorizontalAlignCenter()
		self.statisticValue.SetWindowVerticalAlignCenter()

		self.SetSize(self.backgroundImage.GetWidth(), self.backgroundImage.GetHeight())

	def __del__(self):
		ui.Window.__del__(self)

	def SetBasePosition(self, x, y):
		self.xBase = x
		self.yBase = y

	def GetBasePosition(self):
		return (self.xBase, self.yBase)

class SearchSlotBoard(ui.Window):
	CORNER_WIDTH = 7
	CORNER_HEIGHT = 7
	LINE_WIDTH = 7
	LINE_HEIGHT = 7
	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3
	def __init__(self):
		ui.Window.__init__(self)
		self.MakeBoard()
		self.MakeBase()
	def MakeBoard(self):
		cornerPath = IMG_DIR+"board/corner_"
		linePath = IMG_DIR+"board/"
		CornerFileNames = [ cornerPath+dir+".tga" for dir in ("left_top", "left_bottom", "right_top", "right_bottom") ]
		LineFileNames = [ linePath+dir+".tga" for dir in ("left", "right", "top", "bottom") ]
		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ui.ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)
		self.Lines = []
		for fileName in LineFileNames:
			Line = ui.ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)
		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)
	def MakeBase(self):
		self.Base = ui.ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage(IMG_DIR+"board/base.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()
	def __del__(self):
		ui.Window.__del__(self)
	def Destroy(self):
		self.Base=0
		self.Corners=0
		self.Lines=0
		self.CORNER_WIDTH = 0
		self.CORNER_HEIGHT = 0
		self.LINE_WIDTH = 0
		self.LINE_HEIGHT = 0
		self.LT = 0
		self.LB = 0
		self.RT = 0
		self.RB = 0
		self.L = 0
		self.R = 0
		self.T = 0
		self.B = 0
	def SetSize(self, width, height):
		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		ui.Window.SetSize(self, width, height)
		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)
		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

