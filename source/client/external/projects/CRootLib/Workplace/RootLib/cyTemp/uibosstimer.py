# -*- coding: cp949 -*-
#1574028506
import ui, localeInfo, item, app, uiCommon, constInfo, uiToolTip, dungeonInfo, renderTarget, player, binascii
import net

ErrorMessageList = {
	0 : localeInfo.DUNGEON_TIMER_ERROR_LEVEL,
	1 : localeInfo.DUNGEON_TIMER_ERROR_TICKET,
	2 : localeInfo.DUNGEON_TIMER_ERROR_QTIME,
	3 : localeInfo.DUNGEON_TIMER_ERROR_BUSY,
	4 : localeInfo.DUNGEON_TIMER_ERROR_UNKNOWN
}

ELEMENT_IMG_PATH = \
{
	1 : "d:/ymir work/ui/game/12zi/element/elect.sub", # RACE_FLAG_ATT_ELEC
	2 : "d:/ymir work/ui/game/12zi/element/fire.sub", # RACE_FLAG_ATT_FIRE
	3 : "d:/ymir work/ui/game/12zi/element/ice.sub", # RACE_FLAG_ATT_ICE
	4 : "d:/ymir work/ui/game/12zi/element/wind.sub", # RACE_FLAG_ATT_WIND
	5 : "d:/ymir work/ui/game/12zi/element/earth.sub", # RACE_FLAG_ATT_EARTH
	6 : "d:/ymir work/ui/game/12zi/element/dark.sub", # RACE_FLAG_ATT_DARK
}

DungeonInfoList = {
    0 : {
    "name": localeInfo.DUNGEON_NAME_1,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_03,
    "element" : ELEMENT_IMG_PATH[6]
    },
    1 : {
    "name": localeInfo.DUNGEON_NAME_2,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_05,
    "element" : ELEMENT_IMG_PATH[4]
    },
    2 : {
    "name": localeInfo.DUNGEON_NAME_3,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_02,
    "element" : ELEMENT_IMG_PATH[5]
    },
    3 : {
    "name": localeInfo.DUNGEON_NAME_4,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_03,
    "element" : ELEMENT_IMG_PATH[3]
    },
    4 : {
    "name": localeInfo.DUNGEON_NAME_5,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_04,
    "element" : ELEMENT_IMG_PATH[6]
    },
    5 : {
    "name": localeInfo.DUNGEON_NAME_6,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_02,
    "element" : ELEMENT_IMG_PATH[1]
    },
    6 : {
    "name": localeInfo.DUNGEON_NAME_7,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_01,
    "element" : ELEMENT_IMG_PATH[2]
    },
    7 : {
    "name": localeInfo.DUNGEON_NAME_8,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_04,
    "element" : ELEMENT_IMG_PATH[3]
    },
    8 : {
    "name": localeInfo.DUNGEON_NAME_9,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_05,
    "element" : ELEMENT_IMG_PATH[1]
    },
    9 : {
    "name": localeInfo.DUNGEON_NAME_10,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_01,
    "element" : ELEMENT_IMG_PATH[4]
    },
    10 : {
    "name": localeInfo.DUNGEON_NAME_11,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_01,
    "element" : ELEMENT_IMG_PATH[5]
    },
    11 : {
    "name": localeInfo.DUNGEON_NAME_12,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_01,
    "element" : ELEMENT_IMG_PATH[6]
    },
    12 : {
    "name": localeInfo.DUNGEON_NAME_13,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_04,
    "element" : ELEMENT_IMG_PATH[2]
    },
    13 : {
    "name": localeInfo.DUNGEON_NAME_14,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_03,
    "element" : ELEMENT_IMG_PATH[4]
    },
    14 : {
    "name": localeInfo.DUNGEON_NAME_15,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_05,
    "element" : ELEMENT_IMG_PATH[3]
    },
    15 : {
    "name": localeInfo.DUNGEON_NAME_16,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_02,
    "element" : ELEMENT_IMG_PATH[1]
    },
    16 : {
    "name": localeInfo.DUNGEON_NAME_17,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_05,
    "element" : ELEMENT_IMG_PATH[5]
    },
    17 : {
    "name": localeInfo.DUNGEON_NAME_18,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_04,
    "element" : ELEMENT_IMG_PATH[6]
    },
    18 : {
    "name": localeInfo.DUNGEON_NAME_19,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_02,
    "element" : ELEMENT_IMG_PATH[3]
    },
    19 : {
    "name": localeInfo.DUNGEON_NAME_20,
    "bonus" : localeInfo.DUNGEON_TIME_BONUS_NAME_03,
    "element" : ELEMENT_IMG_PATH[4]
    }
}

class DungeonInformationsWindow(ui.BoardWithTitleBar):
	PATH_BASE 			= "d:/ymir work/ui/game/boss_timer/"
	PATH_ICONS 			= PATH_BASE + "icons/"
	PATH_SCROLLBAR 		= PATH_BASE + "scrollbar/"

	QUESTS = list()

	RENDER_TARGET_INDEX = 101

	def __init__(self):	
		ui.BoardWithTitleBar.__init__(self)

		self.itemToolTip = uiToolTip.ItemToolTip()
		self.itemVnum = None
		self.lastUpdateTime = 0
		self.selectedIndex = 0

		self.LoadHiddenBoss()

		self.interface = constInfo.GetInterfaceInstance()
		self.LoadDungeonInfoData()
		self.LoadWindowAndGUI()
		self.LoadRenderTarget()

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def LoadRenderTarget(self):
		self.ModelPreview = ui.RenderTarget()
		self.ModelPreview.SetParent(self.borderBGLeft)
		self.ModelPreview.SetWindowHorizontalAlignCenter()
		self.ModelPreview.SetSize(251, 162)
		self.ModelPreview.SetPosition(300, 4)
		self.ModelPreview.SetRenderTarget(self.RENDER_TARGET_INDEX)
		self.ModelPreview.Show()

		renderTarget.SetBackground(self.RENDER_TARGET_INDEX, "d:/ymir work/ui/game/render/preview_back.tga")
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
		renderTarget.ResetModel(self.RENDER_TARGET_INDEX)

		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, self.QUESTS[0][5])
		
		renderTarget.Zoom(self.RENDER_TARGET_INDEX, -5)

	def LoadWindowAndGUI(self):

		if not len(self.hiddenList):
			self.SetSize(607, 375 + 55)
		else:
			self.SetSize(607, 375 + 55, 564, 36)

		self.SetCenterPosition()
		self.SetTitleName(localeInfo.DUNGEON_TIMER_TITLE)
		self.SetCloseEvent(self.Close)

		self.AddFlag("float")
		self.AddFlag("movable")

		self.borderBGLeft = ui.BorderA()
		self.borderBGLeft.SetParent(self)
		self.borderBGLeft.SetPosition(10, 35)
		self.borderBGLeft.SetSize(310, 332+48)
		self.borderBGLeft.Show()

		self.borderBGRight = ui.BorderA()
		self.borderBGRight.SetParent(self.borderBGLeft)
		self.borderBGRight.SetPosition(324, 0)
		self.borderBGRight.SetSize(260, 332+48)
		self.borderBGRight.Show()

		# self.backgroundInfo2 = ui.ImageBox()
		# self.backgroundInfo2.SetParent(self.borderBGLeft)
		# self.backgroundInfo2.SetPosition(355, 10)
		# self.backgroundInfo2.LoadImage(self.PATH_BASE + "bgTop.png")
		# self.backgroundInfo2.Show()

		self.backgroundInfo = ui.ImageBox()
		self.backgroundInfo.SetParent(self.borderBGLeft)
		self.backgroundInfo.SetPosition(332, 128+40)
		self.backgroundInfo.LoadImage(self.PATH_BASE + "bgInfo.png")
		self.backgroundInfo.Show()

		self.dungeonNameBox = ui.Window()
		self.dungeonNameBox.SetParent(self)
		self.dungeonNameBox.SetPosition(341, 102+40)
		self.dungeonNameBox.SetSize(251, 28)
		self.dungeonNameBox.Show()

		self.dungeonName = ui.TextLine()
		self.dungeonName.SetParent(self.dungeonNameBox)
		self.dungeonName.SetPosition(0, 7)
		self.dungeonName.SetWindowHorizontalAlignCenter()
		self.dungeonName.SetHorizontalAlignCenter()
		self.dungeonName.Show()

		self.dungeonInfo = list()

		baseX = 347
		baseY = 203

		for i in xrange(4):
			infoBox = ui.Window()
			infoBox.SetParent(self) 
			infoBox.SetPosition(baseX, baseY + ( i * 25 ))
			infoBox.SetSize(237, 18)
			infoBox.Show()

			infoTitle = ui.TextLine()
			infoTitle.SetParent(infoBox)
			infoTitle.SetPosition(8, 2)
			infoTitle.SetWindowHorizontalAlignLeft()
			infoTitle.SetHorizontalAlignLeft()
			infoTitle.Show()

			infoValue = ui.TextLine()
			infoValue.SetParent(infoBox)
			infoValue.SetPosition(8, 2)
			infoValue.SetWindowHorizontalAlignRight()
			infoValue.SetHorizontalAlignRight()
			infoValue.Show()

			bonusInfo = ui.TextLine()
			bonusInfo.SetParent(infoBox)
			bonusInfo.SetPosition(8, 2)
			bonusInfo.SetWindowHorizontalAlignRight()
			bonusInfo.SetHorizontalAlignRight()
			bonusInfo.Show()

			self.dungeonInfo.append( [infoBox, infoTitle, infoValue, bonusInfo] )

		self.dungeonInfo[0][1].SetText(localeInfo.DUNGEON_TIMER_MINLVL)
		self.dungeonInfo[1][1].SetText(localeInfo.DUNGEON_TIMER_GROUPREQ)
		self.dungeonInfo[2][1].SetText(localeInfo.DUNGEON_TIMER_COOLDOWN)
		self.dungeonInfo[3][1].SetText(localeInfo.DUNGEON_TIME_BONUS_TITLE)

		self.passageTicketBox = ui.Window()
		self.passageTicketBox.SetParent(self)
		self.passageTicketBox.SetPosition(347, 193+32+75)
		self.passageTicketBox.SetSize(239, 43)
		self.passageTicketBox.Show()

		self.passageTicketText = ui.TextLine()
		self.passageTicketText.SetParent(self.passageTicketBox)
		self.passageTicketText.SetPosition(10, 15)
		self.passageTicketText.SetHorizontalAlignLeft()
		self.passageTicketText.SetText(localeInfo.DUNGEON_TIMER_TICKET)
		self.passageTicketText.Show()

		self.elementImageBox = ui.Window()
		self.elementImageBox.SetParent(self)
		self.elementImageBox.SetPosition(347, 193+32+75+40)
		self.elementImageBox.SetSize(239, 43)
		self.elementImageBox.Show()

		self.elementInfo = ui.TextLine()
		self.elementInfo.SetParent(self.elementImageBox)
		self.elementInfo.SetPosition(10, 15)
		self.elementInfo.SetHorizontalAlignLeft()
		self.elementInfo.SetText("Element")
		self.elementInfo.Show()

		self.elementImage = ui.ExpandedImageBox()
		self.elementImage.SetParent(self.elementImageBox)
		self.elementImage.SetScale(0.8, 0.8)
		self.elementImage.SetPosition(200, 6)
		self.elementImage.LoadImage(ELEMENT_IMG_PATH[1])
		# self.elementImage.SetWindowHorizontalAlignRight()
		# self.elementImage.SetWindowVerticalAlignCenter()
		self.elementImage.Show()

		item.SelectItem(30179)

		image = item.GetIconImageFileName()

		self.passageTicketItem = ui.ExpandedImageBox()
		self.passageTicketItem.SetParent(self.passageTicketBox)
		self.passageTicketItem.SetWindowHorizontalAlignRight()
		self.passageTicketItem.SetPosition(42, 7)
		self.passageTicketItem.SAFE_SetStringEvent("MOUSE_OVER_IN", self.OnPassageTicketHover)
		self.passageTicketItem.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.OnPassageTicketMouseOut)
		self.passageTicketItem.LoadImage(image)
		self.passageTicketItem.Show()

		self.passageTicketItemNone = ui.TextLine()
		self.passageTicketItemNone.SetParent(self.passageTicketBox)
		self.passageTicketItemNone.SetWindowHorizontalAlignRight()
		self.passageTicketItemNone.SetHorizontalAlignCenter()
		self.passageTicketItemNone.SetPosition(30, 15)
		self.passageTicketItemNone.SetText(localeInfo.DUNGEON_TIME_NO_ITEM)
		self.passageTicketItemNone.Show()

		self.btnTeleport = ui.Button()
		self.btnTeleport.SetParent(self)
		self.btnTeleport.SetUpVisual(self.PATH_BASE + "btn_1_normal.png")
		self.btnTeleport.SetOverVisual(self.PATH_BASE + "btn_1_hover.png")
		self.btnTeleport.SetDownVisual(self.PATH_BASE + "btn_1_down.png")
		self.btnTeleport.SetPosition(356+40, 384)
		self.btnTeleport.SetToolTipText(localeInfo.DUNGEON_TIMER_TP)
		self.btnTeleport.SetEvent(self.OnTeleportButton)
		self.btnTeleport.Show()

		self.btnBossDrop = ui.Button()
		self.btnBossDrop.SetParent(self)
		self.btnBossDrop.SetUpVisual(self.PATH_BASE + "btn_3_normal.png")
		self.btnBossDrop.SetOverVisual(self.PATH_BASE + "btn_3_hover.png")
		self.btnBossDrop.SetDownVisual(self.PATH_BASE + "btn_3_down.png")
		self.btnBossDrop.SetPosition(432+40, 384)
		self.btnBossDrop.SetToolTipText(localeInfo.DUNGEON_TIMER_BOSS_DROP)
		self.btnBossDrop.SetEvent(self.ShowBossDrop)
		self.btnBossDrop.Show()

		self.btnShop = ui.Button()
		self.btnShop.SetParent(self.passageTicketBox)
		self.btnShop.SetUpVisual("d:/ymir work/ui/game/biolog_system/" + "shop_button01.png")
		self.btnShop.SetOverVisual("d:/ymir work/ui/game/biolog_system/" + "shop_button02.png")
		self.btnShop.SetDownVisual("d:/ymir work/ui/game/biolog_system/" + "shop_button03.png")
		self.btnShop.SetPosition(160, 7)
		# self.btnShop.SetToolTipText(localeInfo.DUNGEON_TIMER_RESET_COOLDOWN)
		self.btnShop.SetEvent(self.ShopButton)
		self.btnShop.Show()

		# self.btnWiki = ui.Button()
		# self.btnWiki.SetParent(self)
		# self.btnWiki.SetUpVisual(self.PATH_BASE + "btn_4_normal.png")
		# self.btnWiki.SetOverVisual(self.PATH_BASE + "btn_4_hover.png")
		# self.btnWiki.SetDownVisual(self.PATH_BASE + "btn_4_down.png")
		# self.btnWiki.SetPosition(432, 316)
		# self.btnWiki.SetToolTipText(localeInfo.DUNGEON_TIMER_WIKI_BUTTON)
		# self.btnWiki.SetEvent(self.SearchBossVnumOnWikipedia)
		# self.btnWiki.Show()

		questX = 18 if len(self.QUESTS) > 7 else 23
		questY = 37

		self.questListBox = ui.ListBoxEx()
		self.questListBox.SetParent(self.borderBGLeft)
		self.questListBox.SetPosition(questX, questY)
		self.questListBox.SetSize(300, 320)
		self.questListBox.SetPosition(5, 8)
		self.questListBox.SetItemSize(300, 53)
		self.questListBox.SetItemStep(53)
		self.questListBox.SetViewItemCount(7)
		self.questListBox.Show()

		self.scrollBarQLB = ui.ModernScrollBar()
		self.scrollBarQLB.SetParent(self)
		self.scrollBarQLB.SetPosition(306 + questX + 1-3, questY - 1)
		self.scrollBarQLB.SetScrollBarSize(318+61) 
		self.scrollBarQLB.SetContentHeight(53*dungeonInfo.maxDungeon())
		self.scrollBarQLB.SetScrollStep(0.1) 
		self.scrollBarQLB.Show()

		self.questListBox.SetScrollBar(self.scrollBarQLB)

		self.CreateDungeons()

		self.resetHiddenBossBG = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga", 8, 7)
		self.resetHiddenBossBG.Hide()

		self.resetHiddenBoss = ui.MakeButton(self.resetHiddenBossBG, 11, 3, "", "", "d:/ymir work/ui/game/ref0.png", "d:/ymir work/ui/game/ref1.png", "d:/ymir work/ui/game/ref2.png")
		self.resetHiddenBoss.SetEvent(ui.__mem_func__(self.ResetDungeonHiddenList))
		# self.resetHiddenBoss.Hide()

		if len(self.hiddenList):
			self.resetHiddenBossBG.Show()

		if len(self.QUESTS) < 7:
			self.scrollBarQLB.Hide()
		else:
			self.scrollBarQLB.Show()

		self.SelectFirstDungeon(True)

	def OnPassageTicketHover(self):
		if self.itemVnum:
			self.itemToolTip.SetItemToolTip(self.itemVnum)
			self.itemToolTip.ShowToolTip()

	def OnPassageTicketMouseOut(self):
		self.itemToolTip.HideToolTip()

	def OnClickDungeonButton(self, idx, firstTime=False):

		if idx == self.selectedIndex and not firstTime:
			return

		self.selectedIndex = idx

		self.ChangePassageTicket(self.selectedIndex)
		self.ChangeBossRenderTarget(self.selectedIndex)
		self.ChangeDungeonInfo(self.selectedIndex)

		self.dungeonInfo[0][1].SetText(localeInfo.DUNGEON_TIMER_MINLVL)
		self.passageTicketText.SetText(localeInfo.DUNGEON_TIMER_TICKET)
		self.dungeonInfo[1][1].SetText(localeInfo.DUNGEON_TIMER_GROUPREQ)
		self.dungeonInfo[3][1].SetText(localeInfo.DUNGEON_TIME_BONUS_TITLE)

		self.elementImage.LoadImage(DungeonInfoList[idx]["element"])
		self.elementImage.SetScale(0.8, 0.8)

	def HideSelectedDungeon(self, index):
		if index in self.hiddenList:
			return

		if len(self.hiddenList) >= (dungeonInfo.maxDungeon()-1):
			return

		self.hiddenList.append(index)

		self.CreateDungeons()

		self.SelectFirstDungeon()

		if self.resetHiddenBossBG:
			self.resetHiddenBossBG.Show()
		self.SetSize(607, 375+55, 564, 36)

		self.SaveHiddenBossList()

	def ResetDungeonHiddenList(self):
		self.hiddenList = list()
		self.CreateDungeons()

		if self.resetHiddenBossBG:
			self.resetHiddenBossBG.Hide()
		self.SetSize(607, 375+55)

		self.SaveHiddenBossList()

	def OnTeleportButton(self):
		self.dialog = uiCommon.QuestionDialog()
		self.dialog.index = self.selectedIndex
		self.dialog.SetText(localeInfo.TIMER_WARP_QUESTION % str(self.QUESTS[self.selectedIndex][0]))
		self.dialog.SetAcceptText(localeInfo.DUNGEON_TIMER_CONFIRM)
		self.dialog.SetCancelText(localeInfo.DUNGEON_TIMER_DECLINE)
		self.dialog.SetAcceptEvent(lambda arg = True: self.SendWarpCommand(arg))
		self.dialog.SetCancelEvent(lambda arg = False: self.SendWarpCommand(arg))
		self.dialog.Open()

	def ShopButton(self):
		net.SendChatPacket("/open_this_distance_npc 5")

	def SearchBossVnumOnWikipedia(self):
		getCurrentBossVnum = self.QUESTS[self.selectedIndex][5]
		if self.interface.wndWiki:
			self.interface.wndWiki.searchBossWithVnum(getCurrentBossVnum)
		self.Close()
		return

	def SendWarpCommand(self, answer):
		minLev, maxLev = self.QUESTS[self.selectedIndex][6]
		playerLevel = player.GetStatus(player.LEVEL)

		if playerLevel < minLev or playerLevel > maxLev:
			constInfo.GetGameInstance().DungeonInfoErrorMessage(0)
			self.dialog.Hide()
			self.dialog.Close()
			return

		if answer:
			dungeonInfo.loginRequest(self.dialog.index)

		self.dialog.Hide()
		self.dialog.Close()

	def ShowBossDrop(self):
		currentBossChest = self.QUESTS[self.selectedIndex][4]
		if self.interface.wndWiki:
			self.interface.wndWiki.searchItemWithName(currentBossChest)

	def ChangeDungeonInfo(self, id):
		minLevel = self.QUESTS[id][1]
		self.dungeonInfo[0][2].SetText(minLevel)
		self.dungeonInfo[1][2].SetText(localeInfo.DUNGEON_TIMER_GROUP_REQ_NO)
		self.dungeonInfo[2][2].SetText(localeInfo.SecondToHMS(self.QUESTS[id][2]))
		self.dungeonInfo[3][2].SetText(DungeonInfoList[id]["bonus"])

	def ChangePassageTicket(self, id):
		itemVnum = self.QUESTS[id][3]

		if not itemVnum or itemVnum == 0:
			self.passageTicketItem.Hide()
			self.passageTicketItemNone.Show()
			return

		item.SelectItem(itemVnum)
		image = item.GetIconImageFileName()
		self.passageTicketItem.LoadImage(image)
		self.itemVnum = itemVnum
		self.passageTicketItem.Show()
		self.passageTicketItemNone.Hide()

	def ChangeBossRenderTarget(self, id):
		bossRender = self.QUESTS[id][5]
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)

		if not bossRender or bossRender == 0:
			bossRender=101

		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, bossRender)
		renderTarget.Zoom(self.RENDER_TARGET_INDEX, -5)

	def ChangeDungeonName(self, id):
		dungeonName = self.QUESTS[id][0]
		self.dungeonName.SetText(dungeonName)

	def Close(self):

		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)
		self.Hide()

	def Open(self):
		self.SetCenterPosition()
		self.Show()
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)

	def ChangeQuestBackground(self, index, newBackground, selected=False):
		dungButtonList = self.questListBox.GetItems()

		if selected:
			for item in dungButtonList:
				if item.GetButtonIndex() == self.selectedIndex:
					index = item.GetOrderIndex()
					break

		currentBackground = dungButtonList[index].backgroundImage.GetImageName()

		if currentBackground == newBackground:
			return

		dungButtonList[index].backgroundImage.LoadImage(newBackground)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self):
		self.RefreshDungeonButtons()

	def OnRunMouseWheel(self, nLen):
		if nLen > 0: 
			self.scrollBarQLB.OnUp() 
		else: 
			self.scrollBarQLB.OnDown()

	def LoadDungeonInfoData(self):
		for i in xrange(dungeonInfo.maxDungeon()):
			self.QUESTS.append([])
			args = tuple(dungeonInfo.getTable(i))
			if not args:
				continue

			bossVnum = args[0]
			bossName = DungeonInfoList[i]["name"]
			levelLimit = localeInfo.DUNGEON_TIMER_MIN_MAX_LEVEL.format(args[2],args[3])
			coolDown = args[1]
			ticketVnum = args[4]
			chestVnum = args[5]

			if len(bossName) > 24:
				bossName = bossName[:24] + "..."

			self.QUESTS[i] = (bossName, levelLimit, coolDown, ticketVnum, chestVnum, bossVnum, (args[2], args[3]))

	def CreateDungeons(self):
		self.questListBox.RemoveAllItems()

		dungeonCount = 0

		for dungeonIndex in xrange(dungeonInfo.maxDungeon()):

			if dungeonIndex in self.hiddenList:
				continue

			createdDungeon = Dungeon(dungeonIndex, parent=self, order=dungeonCount)
			self.questListBox.AppendItem(createdDungeon)
			dungeonCount+=1

		self.scrollBarQLB.SetContentHeight(53*dungeonCount)

	def RefreshDungeonButtons(self):
		dungButtonList = self.questListBox.GetItems()

		for index, btn in enumerate(dungButtonList):
			buttonIndex = btn.GetButtonIndex()

			cooldownTextLine = btn.cooldownText
			bossLevelMin, bossLevelMax = self.QUESTS[index][6]

			cooldown = self.TimeToString(dungeonInfo.getTime(buttonIndex))
			cooldownTextLine.SetText(cooldown)
			isAvailable = (cooldown == "00:00:00") and (bossLevelMin <=  player.GetStatus(player.LEVEL) <= bossLevelMax)

			if isAvailable:
				self.ChangeQuestBackground(index, self.PATH_BASE + "available.png")

				textAvailable = localeInfo.DUNGEON_TIMER_AVAILABLE

				if textAvailable.endswith( '!' ):
					textAvailable = textAvailable[:-1]

				dungButtonList[index].stateInfo.SetText(textAvailable)
			else:
				self.ChangeQuestBackground(index, self.PATH_BASE + "not_available.png")

				dungButtonList[index].stateInfo.SetText(localeInfo.DUNGEON_TIMER_NOT_AVAILABLE)

			self.ChangeQuestBackground(self.selectedIndex, self.PATH_BASE + "selected.png", True)

	def SelectFirstDungeon(self, firstTime = False):
		dungeonList = self.questListBox.GetItems()
		firstElement = dungeonList[0].GetButtonIndex()

		self.OnClickDungeonButton(firstElement, firstTime)

	def TimeToString(self, timeLeft):
		if timeLeft > 0:
			hours = int(timeLeft / 3600)
			minutes = int((timeLeft - hours * 3600) / 60)
			seconds = int(timeLeft - hours * 3600 - minutes * 60)

			timeLeftString = ""

			if hours < 10:
				timeLeftString += "0"

			timeLeftString += str(hours) + ":"

			if minutes < 10:
				timeLeftString += "0"

			timeLeftString += str(minutes) + ":"

			if seconds < 10:
				timeLeftString += "0"

			return timeLeftString + str(seconds)

		return "00:00:00"

	def LoadHiddenBoss(self):
		try:
			hidden_data = constInfo.GetReg("hiddenBossList_{}".format(player.GetName()))
			if hidden_data is not None:
				hiddenList = eval(binascii.a2b_base64(hidden_data))
				if hiddenList:
					self.hiddenList = hiddenList
				else:
					self.hiddenList = []
			else:
				self.hiddenList = []
		except IOError:
			self.hiddenList = []

	def SaveHiddenBossList(self):
		encoded_data = binascii.b2a_base64(str(self.hiddenList))
		constInfo.SetReg("hiddenBossList_{}".format(player.GetName()), encoded_data)

class Dungeon(ui.Window):
	def __init__(self, idx, parent, order):
		ui.Window.__init__(self)

		photoIndex = idx+1
		self.btnIndex = idx
		self.orderInList = order

		backgroundImage = ui.ImageBoxTimer()
		backgroundImage.SetParent(self)
		backgroundImage.SetPosition(0, 0)
		backgroundImage.LoadImage(parent.PATH_BASE + "available.png")
		backgroundImage.SAFE_SetStringEvent("MOUSE_LEFT_DOWN", parent.OnClickDungeonButton, idx)
		backgroundImage.Show()
		self.backgroundImage = backgroundImage

		bossMiniicon = ui.ImageBoxTimer()
		bossMiniicon.SetParent(backgroundImage)
		bossMiniicon.SetPosition(0, 0)
		bossMiniicon.LoadImage(parent.PATH_ICONS + "%d.png" % photoIndex)
		bossMiniicon.SAFE_SetStringEvent("MOUSE_LEFT_DOWN", parent.OnClickDungeonButton, idx)
		bossMiniicon.Show()
		self.bossMiniicon = bossMiniicon

		dungName = ui.TextLine()
		dungName.SetParent(backgroundImage)
		dungName.SetPosition(0, -9)
		dungName.SetWindowHorizontalAlignCenter()
		dungName.SetHorizontalAlignCenter()
		dungName.SetWindowVerticalAlignCenter()
		dungName.SetVerticalAlignCenter()
		dungName.SetText(parent.QUESTS[idx][0])
		dungName.Show()
		self.dungName = dungName

		watchImage = ui.ImageBoxTimer()
		watchImage.SetParent(backgroundImage)
		watchImage.SetPosition(250, 10)
		watchImage.LoadImage(parent.PATH_BASE + "timer.tga")
		watchImage.SAFE_SetStringEvent("MOUSE_LEFT_DOWN", parent.OnClickDungeonButton, idx)
		watchImage.Show()
		self.watchImage = watchImage

		cooldownText = ui.TextLine()
		cooldownText.SetParent(backgroundImage)
		cooldownText.SetPosition(110, 10)
		cooldownText.SetWindowHorizontalAlignCenter()
		cooldownText.SetHorizontalAlignCenter()
		cooldownText.SetWindowVerticalAlignCenter()
		cooldownText.SetVerticalAlignCenter()
		cooldownText.SetText(localeInfo.DUNGEON_TIMER_COOLDOWN)
		cooldownText.Show()
		self.cooldownText = cooldownText

		stateInfo = ui.TextLine()
		stateInfo.SetParent(backgroundImage)
		stateInfo.SetPosition(0, 10)
		stateInfo.SetWindowHorizontalAlignCenter()
		stateInfo.SetHorizontalAlignCenter()
		stateInfo.SetWindowVerticalAlignCenter()
		stateInfo.SetVerticalAlignCenter()
		stateInfo.SetText(localeInfo.DUNGEON_TIMER_AVAILABLE)
		stateInfo.Show()
		self.stateInfo = stateInfo

		hideButton = ui.Button()
		hideButton.SetParent(backgroundImage)
		hideButton.SetPosition(60, 17)
		hideButton.SetUpVisual(parent.PATH_BASE + "btn_hide_1.png")
		hideButton.SetOverVisual(parent.PATH_BASE + "btn_hide_2.png")
		hideButton.SetDownVisual(parent.PATH_BASE + "btn_hide_3.png")
		hideButton.SetEvent(lambda dungIndex = idx : parent.HideSelectedDungeon(dungIndex))	
		hideButton.Show()
		self.hideButton = hideButton

		self.SetSize(backgroundImage.GetWidth(), backgroundImage.GetHeight())

	def __del__(self):
		ui.Window.__del__(self)

	def GetButtonIndex(self):
		return self.btnIndex

	def GetOrderIndex(self):
		return self.orderInList
