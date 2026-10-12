# -*- coding: cp949 -*-
#964664470
import ui, uiCommon, item, uiToolTip, player, net, app, uiScriptLocale, localeInfo, constInfo

class RefineWindow(ui.BoardWithTitleBar):

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.defaultInformations()
		self.CreateRefineWindow()

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.BoardWithTitleBar().__del__(self)

	def CreateRefineWindow(self):
		self.AddFlag('movable')
		self.SetSize(367, 313)
		self.SetTitleName(localeInfo.REFINE_WINDOW)
		self.SetCenterPosition()
		self.SetCloseEvent(self.Close)

		self.borderBG = ui.BorderA()
		self.borderBG.SetParent(self)
		self.borderBG.SetPosition(10, 32)
		self.borderBG.SetSize(345, 271)
		self.borderBG.Show()

		self.informationBG = ui.BorderA()
		self.informationBG.SetParent(self.borderBG)
		self.informationBG.SetPosition(15, 5)
		self.informationBG.SetSize(315, 20)
		self.informationBG.Show()

		self.currentItem = ui.TextLine()
		self.currentItem.SetParent(self.informationBG)
		self.currentItem.SetPosition(5, 7)
		self.currentItem.SetWindowHorizontalAlignCenter()
		self.currentItem.SetHorizontalAlignCenter()
		self.currentItem.SetFontName("Tahoma:14")
		self.currentItem.Show()

		self.backgroundImage = ui.MakeImageBox(self.informationBG, "d:/ymir work/ui/game/refinerenewal/refinebg.png", 0, 31)
		self.backgroundImage.SetSize(self.backgroundImage.GetWidth(), self.backgroundImage.GetHeight())
		self.backgroundImage.Show()

		self.fastUpgadeText = ui.TextLine()
		self.fastUpgadeText.SetParent(self.informationBG)
		self.fastUpgadeText.SetPosition(70, 188)
		self.fastUpgadeText.SetText(localeInfo.REFINE_FAST_UPGRADE_CHECKBOX_TEXT)
		self.fastUpgadeText.Show()

		self.fastUpgradeCheckBox = ui.ExpandedImageBox()
		self.fastUpgradeCheckBox.SetParent(self.borderBG)
		self.fastUpgradeCheckBox.SetPosition(66, 195)
		self.fastUpgradeCheckBox.LoadImage("d:/ymir work/ui/game/checkboxrenewal/checkbox_new_unselected.tga")
		self.fastUpgradeCheckBox.SAFE_SetStringEvent("MOUSE_LEFT_DOWN", self.OnCheckBox, True)
		self.fastUpgradeCheckBox.Show()

		self.upgradingNeedText = ui.TextLine()
		self.upgradingNeedText.SetParent(self.informationBG)
		self.upgradingNeedText.SetPosition(70, 170)
		self.upgradingNeedText.Show()

		self.continueText = ui.TextLine()
		self.continueText.SetParent(self.borderBG)
		self.continueText.SetPosition(85, 213)
		self.continueText.SetText(localeInfo.REFINE_KEEP_WINDOW_OPEN)
		self.continueText.Show()

		self.continueCheckBox = ui.ExpandedImageBox()
		self.continueCheckBox.SetParent(self.borderBG)
		self.continueCheckBox.SetPosition(66, 215)
		self.continueCheckBox.LoadImage("d:/ymir work/ui/game/checkboxrenewal/checkbox_new_unselected.tga")
		self.continueCheckBox.OnMouseLeftButtonDown = ui.__mem_func__(self.OnCheckBox)
		self.continueCheckBox.Show()

		self.UpgradeButton = ui.MakeButton(self.borderBG, 20, 240, "", "d:/ymir work/ui/switchbot/", "btn_big_01.sub", "btn_big_02.sub", "btn_big_03.sub")
		self.UpgradeButton.SetText(localeInfo.OFFLINESHOP_TYPE_COMBOBOX_REFINE)
		self.UpgradeButton.SetEvent(ui.__mem_func__(self.OpenQuestionDialog))
		self.UpgradeButton.Show()
	
		self.CancelButton = ui.MakeButton(self.borderBG, 180, 240, "", "d:/ymir work/ui/switchbot/", "btn_big_01.sub", "btn_big_02.sub", "btn_big_03.sub")
		self.CancelButton.SetText(uiScriptLocale.KEYCHANGE_CANCLE)
		self.CancelButton.SetEvent(ui.__mem_func__(self.Close))
		self.CancelButton.Show()

		self.InformationButton = ui.MakeButton(self.borderBG, 162, 194, False, "d:/ymir work/ui/pattern/", "q_mark_01.tga", "q_mark_02.tga", "q_mark_01.tga")
		self.InformationButton.ShowToolTip = lambda arg=1: self.OverInButton()
		self.InformationButton.HideToolTip = lambda arg=1: self.OverOutButton()

		self.imagePositionList = [41, 100, 147, 194, 240, 287]

		for image in xrange(6):
			self.guiItemBGAndSlots[0].append(image)
			self.guiItemBGAndSlots[0][image] = ui.ExpandedImageBox()
			self.guiItemBGAndSlots[0][image].SetParent(self.borderBG)
			self.guiItemBGAndSlots[0][image].SetPosition(self.imagePositionList[image], 45)
			self.guiItemBGAndSlots[0][image].Show()

		self.itemIcons = ui.SlotWindow()
		self.itemIcons.SetParent(self.borderBG)
		self.itemIcons.SetPosition(39, 47)
		self.itemIcons.SetSize((32*9), 32*3)
		self.itemIcons.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemIcons.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.itemIcons.AppendSlot(0, 0, 0, 32, 32*3)

		for i in xrange(0, 6):
			self.itemIcons.AppendSlot(i+1, 46*i+62, 0, 32, 32*3)
		self.itemIcons.Show()

	def SetItemToolTip(self, itemTooltip):
		self.itemTooltip = itemTooltip

	def defaultInformations(self):
		self.IsSelected = False
		self.interface = None
		self.imagePositionList = []
		self.guiItemBGAndSlots = [ [], [], [], [] ]
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1, -1)
			self.wndInventory = None
		self.ResetRefineItems()
		self.fastUpgrade = False
		self.toolTipInfo = uiToolTip.ToolTip()

	def ResetRefineItems(self):
		self.refineItems = {}
		self.targetItemPos = 0
		self.itemVnum = 0
		self.cost = 0
		self.success = 0
		self.type = 0

	def CreateUpgradeInformations(self):
		item.SelectItem(self.itemVnum)
		self.currentItem.SetText(localeInfo.REFINE_TO.format(item.GetItemName()))
		self.upgradingNeedText.SetText(localeInfo.REFINE_SUCCES_AND_COST.format(self.cost, self.success))
		self.itemIcons.ClearSlot(0)
		self.itemIcons.SetItemSlot(0, self.itemVnum)

	def CreateMaterialInformations(self):
		for j in xrange(len(list(self.refineItems.keys()))):
			itemvnum = list(self.refineItems.keys())[j]
			self.itemIcons.ClearSlot(j+1)
			self.itemIcons.SetItemSlot(j+1, itemvnum)

		for countInfo in xrange(len(list(self.refineItems.keys()))):
			self.guiItemBGAndSlots[2].append(countInfo)
			self.guiItemBGAndSlots[2][countInfo] = ui.TextLine()
			self.guiItemBGAndSlots[2][countInfo].SetParent(self.borderBG)
			self.guiItemBGAndSlots[2][countInfo].SetPosition(self.imagePositionList[countInfo+1]-2, 147)
			self.guiItemBGAndSlots[2][countInfo].SetText("{}".format(list(self.refineItems.values())[countInfo]))
			self.guiItemBGAndSlots[2][countInfo].Show()

		for yourHaveCount in xrange(len(list(self.refineItems.keys()))):
			self.guiItemBGAndSlots[3].append(yourHaveCount)
			self.guiItemBGAndSlots[3][yourHaveCount] = ui.TextLine()
			self.guiItemBGAndSlots[3][yourHaveCount].SetParent(self.borderBG)
			self.guiItemBGAndSlots[3][yourHaveCount].SetPosition(self.imagePositionList[yourHaveCount+1]-2, 158)
			self.guiItemBGAndSlots[3][yourHaveCount].SetText("{}".format(0))
			self.guiItemBGAndSlots[3][yourHaveCount].Show()

	def OnCheckBox(self, fastType = False):

		if fastType:
			if self.fastUpgrade:
				self.fastUpgradeCheckBox.LoadImage("d:/ymir work/ui/game/checkboxrenewal/checkbox_new_unselected.tga")
				self.fastUpgrade = False
			else:
				self.fastUpgrade = True
				self.fastUpgradeCheckBox.LoadImage("d:/ymir work/ui/game/checkboxrenewal/checkbox_new_selected.tga")
				if not self.IsSelected:
					self.OnCheckBox()
		else:
			if self.IsSelected:
				self.continueCheckBox.LoadImage("d:/ymir work/ui/game/checkboxrenewal/checkbox_new_unselected.tga")
				self.IsSelected = False
				constInfo.IS_AUTO_REFINE = False
			else:
				self.IsSelected = True
				self.continueCheckBox.LoadImage("d:/ymir work/ui/game/checkboxrenewal/checkbox_new_selected.tga")
				constInfo.IS_AUTO_REFINE = True

	def OverInMyItem(self):
		if self.itemTooltip:
			self.itemTooltip.ClearToolTip()
			self.itemTooltip.AddItemData(self.itemVnum, self.metinSlot, self.attrSlot)

	def OverInItem(self, slotIndex):

		if slotIndex == 0:
			self.OverInMyItem()
		else:
			item = list(self.refineItems.keys())[slotIndex-1]
			if self.itemTooltip:
				self.itemTooltip.ClearToolTip()
				self.itemTooltip.AddItemData(item, 0, 0)

	def OverOutItem(self):
		if self.itemTooltip:
			self.itemTooltip.HideToolTip()

	def OverInButton(self):
		if self.InformationButton.IsIn() and self.toolTipInfo:
			self.toolTipInfo.ClearToolTip()
			self.toolTipInfo.AlignHorizonalCenter()
			self.toolTipInfo.AutoAppendNewTextLine(localeInfo.REFINE_FAST_UPGRADE_INFO)
			self.toolTipInfo.Show()

	def OverOutButton(self):
		if self.toolTipInfo:
			self.toolTipInfo.Hide()

	def Open(self, targetItemPos, nextGradeItemVnum, cost, prob, type):

		for i in xrange(6):
			self.itemIcons.ClearSlot(i)

		for j in xrange(len(list(self.refineItems.keys()))):
			self.guiItemBGAndSlots[2][j].SetText("")
			self.guiItemBGAndSlots[3][j].SetText("")

		self.ResetRefineItems()

		self.targetItemPos = targetItemPos
		self.itemVnum = nextGradeItemVnum
		self.cost = cost
		self.success = prob
		self.type = type

		self.metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			self.metinSlot.append(player.GetItemMetinSocket(self.targetItemPos, i))

		self.attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			self.attrSlot.append(player.GetItemAttribute(self.targetItemPos, i))

		self.CreateUpgradeInformations()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1, -1)
			self.SetCantMouseEventSlot(targetItemPos)

		self.SetTop()
		self.Show()

	def AppendMaterial(self, vnum, count):
		if not vnum in self.refineItems.keys():
			self.refineItems.update({vnum: count})
			self.CreateMaterialInformations()

	def OnUpdate(self):
		for x in xrange(len(self.refineItems.values())):
			self.guiItemBGAndSlots[3][x].SetText("{}".format(player.GetItemCountByVnum(list(self.refineItems.keys())[x])))
			if player.GetItemCountByVnum(list(self.refineItems.keys())[x]) >= list(self.refineItems.values())[x]:
				self.guiItemBGAndSlots[3][x].SetPackedFontColor(0xff48b52f)
			else:
				self.guiItemBGAndSlots[3][x].SetPackedFontColor(0xff8a2222)

	def Close(self, isDestroy = False):
		if not isDestroy:
			net.SendRefinePacket(255, 255)

		constInfo.AUTO_REFINE_TYPE = 0
		constInfo.AUTO_REFINE_DATA = {
			"ITEM" : [-1, -1],
			"NPC" : [0, -1, -1, 0]
		}

		if self.itemTooltip:
			self.itemTooltip.HideToolTip()
		if self.toolTipInfo:
			self.toolTipInfo.Hide()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1, -1)
			self.SetCanMouseEventSlot(self.targetItemPos)

		self.Hide()

	def CloseDestroy(self):
		for items in xrange(6):
			self.itemIcons.ClearSlot(items)

		self.ResetRefineItems()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1,-1)

	def Destroy(self):
		self.defaultInformations()
		self.Close(True)

	def BindInterface(self, interface):
		self.interface = interface

	def SetRefineInformations(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
		self.RefineInfo = [targetItemPos, nextGradeItemVnum, cost, prob, type]

	def OpenQuestionDialog(self):
		if 100 == self.success:
			self.Accept()
			return

		if self.fastUpgrade:
			self.Accept()
			return

		if 5 == self.type:
			self.Accept()
			return

		dlgQuestion = uiCommon.QuestionDialog2()
		dlgQuestion.SetText2(localeInfo.REFINE_WARNING2)
		dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.Accept))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))
		dlgQuestion.SetWidth(350)

		if 3 == self.type:
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_1)
			dlgQuestion.SetText2(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_2)
		elif 2 == self.type:
			dlgQuestion.SetText1(localeInfo.REFINE_DOWN_GRADE_WARNING)
		else:
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING)

		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion

	def Accept(self):
		net.SendRefinePacket(self.targetItemPos, self.type)
		self.CloseDialog()

	def CloseDialog(self, noItem=False):
		if self.dlgQuestion:
			self.dlgQuestion.Close()
			self.dlgQuestion = None

		if noItem:
			self.Close()

	def CheckRefine(self, isFail):
		if constInfo.IS_AUTO_REFINE == True:
			if constInfo.AUTO_REFINE_TYPE == 1:
				if constInfo.AUTO_REFINE_DATA["ITEM"][0] != -1 and constInfo.AUTO_REFINE_DATA["ITEM"][1] != -1:
					scrollIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][0])
					itemIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][1])
					
					if scrollIndex == 0 or (itemIndex % 10 == 8 and not isFail):
						self.CloseDialog(True)
					else:
						net.SendItemUseToItemPacket(constInfo.AUTO_REFINE_DATA["ITEM"][0], constInfo.AUTO_REFINE_DATA["ITEM"][1])

			elif constInfo.AUTO_REFINE_TYPE == 2:
				npcData = constInfo.AUTO_REFINE_DATA["NPC"]
				if npcData[0] != 0 and npcData[1] != -1 and npcData[2] != -1 and npcData[3] != 0:
					itemIndex = player.GetItemIndex(npcData[1], npcData[2])
					if (itemIndex % 10 == 8 and not isFail) or isFail:
						self.CloseDialog(True)
					else:
						net.SendGiveItemPacket(npcData[0], npcData[1], npcData[2], npcData[3])
			else:
				self.CloseDialog(True)
		else:
			self.CloseDialog(True)

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetCanMouseEventSlot(self, slotIndex):
			itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItem = (-1, -1)
			if self.wndInventory:
				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCanMouseEventSlot(localSlotPos)

		def SetCantMouseEventSlot(self, slotIndex):
			itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItem = (itemInvenPage, localSlotPos)
			if self.wndInventory:
				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				itemInvenPage, itemSlotPos = self.lockedItem
				if self.wndInventory:
					if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)
					self.wndInventory.wndItem.RefreshSlot()



