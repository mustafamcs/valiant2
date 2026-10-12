# -*- coding: cp949 -*-
#-699808798
import app, player, net, chat, exchange, item, localeInfo, ui, mouseModule, uiPickMoney, wndMgr, uiCommon, playerSettingModule
if app.ENABLE_OFFLINE_SHOP:
	import uiOfflineShop

class ExchangeDialog(ui.ScriptWindow):
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
	
	if app.ENABLE_WOLFMAN_CHARACTER:
		FACE_IMAGE_DICT.update({playerSettingModule.RACE_WOLFMAN_M : "icon/face/wolfman_m.tga",})

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.TitleName = 0
		self.tooltipItem = 0
		self.xStart = 0
		self.yStart = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.wndInventory = None
			self.wndDragonSoul = None
			self.lockedItems = {i:(-1,-1) for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}
			self.lockedItemsDS = {i:(-1,-1,-1) for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}
			
			if app.ENABLE_SPECIAL_STORAGE:
				self.wndSpecialStorage = None
				self.lockedItemsStorage = {i:(-1,-1,-1) for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}

		self.tradeWrongEnterCount = 0

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	class Item(ui.ListBoxEx.Item):
		def __init__(self,parent, text, value=0):
			ui.ListBoxEx.Item.__init__(self)
			self.textBox=ui.TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			self.textBox.Show()
			self.value = value

		def GetValue(self):
			return self.value

		def __del__(self):
			ui.ListBoxEx.Item.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		if app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			PythonScriptLoader.LoadScriptFile(self, "UIScript/exchangedialog_new.py")
		else:
			PythonScriptLoader.LoadScriptFile(self, "UIScript/exchangedialog.py")

		## Owner
		self.OwnerSlot = self.GetChild("Owner_Slot")
		self.OwnerSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectOwnerEmptySlot))
		self.OwnerSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectOwnerItemSlot))
		self.OwnerSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInOwnerItem))
		self.OwnerSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.OwnerMoney = self.GetChild("Owner_Money_Value")
		if not app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			self.OwnerAcceptLight = self.GetChild("Owner_Accept_Light")
			self.OwnerAcceptLight.Disable()
		self.OwnerMoneyButton = self.GetChild("Owner_Money")
		self.OwnerMoneyButton.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))
		
		self.TargetSlot = self.GetChild("Target_Slot")
		self.TargetSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInTargetItem))
		self.TargetSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.TargetMoney = self.GetChild("Target_Money_Value")
		if not app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			self.TargetAcceptLight = self.GetChild("Target_Accept_Light")
			self.TargetAcceptLight.Disable()
		
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
		dlgPickMoney.SetTitleName(localeInfo.EXCHANGE_MONEY)
		dlgPickMoney.SetMax(15)
		dlgPickMoney.Hide()
		self.dlgPickMoney = dlgPickMoney

		## Button
		self.AcceptButton = self.GetChild("Owner_Accept_Button")
		self.AcceptButton.SetToggleDownEvent(ui.__mem_func__(self.AcceptExchange))
		
		if app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			self.TargetAcceptButton = self.GetChild("Target_Accept_Button")

		self.TitleName = self.GetChild("TitleName")
		self.GetChild("TitleBar").SetCloseEvent(net.SendExchangeExitPacket)
		if app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			self.FaceOwnerImage = self.GetChild("FaceOwner_Image")
			self.FaceTargetImage = self.GetChild("FaceTarget_Image")
			self.TargetName = self.GetChild("target_NameText")
			self.TargetLevel = self.GetChild("target_LvText")
			self.listOwnerSlot = []
			self.listTargetSlot = []

	def Destroy(self):
		self.ClearDictionary()
		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0
		self.OwnerSlot = 0
		self.OwnerMoney = 0
		if not app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			self.OwnerAcceptLight = 0
		self.OwnerMoneyButton = 0
		self.TargetSlot = 0
		self.TargetMoney = 0
		if not app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			self.TargetAcceptLight = 0
		self.TitleName = 0
		self.AcceptButton = 0
		if app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			self.TargetAcceptButton = 0
			self.FaceOwnerImage = None
			self.FaceTargetImage = None
			self.TargetName = None
			self.TargetLevel = None
		self.tooltipItem = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.wndInventory = None
			self.wndDragonSoul = None
			self.lockedItems = {i:(-1,-1) for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}
			self.lockedItemsDS = {i:(-1,-1,-1) for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}
			
			if app.ENABLE_SPECIAL_STORAGE:
				self.wndSpecialStorage = None
				self.lockedItemsStorage = {i:(-1,-1,-1) for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}

	def OpenDialog(self):
		if app.ENABLE_LEVEL_IN_TRADE:
			self.TitleName.SetText(localeInfo.EXCHANGE_TITLE_LEVEL % (exchange.GetNameFromTarget(), exchange.GetLevelFromTarget()))
		else:
			self.TitleName.SetText(localeInfo.EXCHANGE_TITLE % (exchange.GetNameFromTarget()))
		
		self.AcceptButton.Enable()
		self.AcceptButton.SetUp()
		if app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			self.TargetAcceptButton.Disable()
			self.TargetAcceptButton.SetUp()
			self.FaceOwnerImage.LoadImage(self.FACE_IMAGE_DICT[exchange.GetRaceFromSelf()])
			self.FaceTargetImage.LoadImage(self.FACE_IMAGE_DICT[exchange.GetRaceFromTarget()])
			self.TargetName.SetText(exchange.GetNameFromTarget())
			self.TargetLevel.SetText(localeInfo.NEW_EXCHANGE_LEVEL % (exchange.GetLevelFromTarget()))

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface.SetOnTopWindow(player.ON_TOP_WND_EXCHANGE)
			self.interface.RefreshMarkInventoryBag()

		self.SetTop()
		self.Show()

		self.tradeWrongEnterCount = 2

		(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()

	def CloseDialog(self):
		wndMgr.OnceIgnoreMouseLeftButtonUpEvent()

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.dlgPickMoney.Close()
		self.Hide()

		if app.WJ_ENABLE_TRADABLE_ICON:
			for exchangePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItems = {i:(-1,-1) for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}
			
			for exchangePos, (itemInvenPage, itemSlotPos, srcSlotIndex) in self.lockedItemsDS.items():
				category = 0
				if srcSlotIndex >= 0 and srcSlotIndex < 192:
					category = 0
				elif srcSlotIndex >= 192 and srcSlotIndex < 384:
					category = 1
				elif srcSlotIndex >= 384 and srcSlotIndex < 576:
					category = 2
				elif srcSlotIndex >= 576 and srcSlotIndex < 768:
					category = 3
				elif srcSlotIndex >= 768 and srcSlotIndex < 960:
					category = 4
				elif srcSlotIndex >= 960 and srcSlotIndex < 1152:
					category = 5

				catCount = 6

				if self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage:
					self.wndDragonSoul.wndItem.SetCanMouseEventSlot(itemSlotPos)
				elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount:
					self.wndDragonSoul.wndItem.SetCanMouseEventSlot(itemSlotPos)
				elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*2:
					self.wndDragonSoul.wndItem.SetCanMouseEventSlot(itemSlotPos)
				elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*3:
					self.wndDragonSoul.wndItem.SetCanMouseEventSlot(itemSlotPos)
				elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*4:
					self.wndDragonSoul.wndItem.SetCanMouseEventSlot(itemSlotPos)
				elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*5:
					self.wndDragonSoul.wndItem.SetCanMouseEventSlot(itemSlotPos)	


			self.lockedItemsDS = {i:(-1,-1,-1) for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}
			
			if app.ENABLE_SPECIAL_STORAGE:
				for exchangePos, (itemInvenPage, itemSlotPos, invenType) in self.lockedItemsStorage.items():
				
					category = 0
					if invenType == player.UPGRADE_INVENTORY:
						category = 0
					elif invenType == player.BOOK_INVENTORY:
						category = 1
					elif invenType == player.STONE_INVENTORY:
						category = 2
					elif invenType == player.CHEST_INVENTORY:
						category = 3
					
					if itemInvenPage == self.wndSpecialStorage.GetInventoryPageIndex() and self.wndSpecialStorage.GetCategoryIndex() == category:
						self.wndSpecialStorage.wndItem.SetCanMouseEventSlot(itemSlotPos)
					
				self.lockedItemsStorage = {i:(-1,-1,-1) for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM)}
			
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
				self.interface.RefreshMarkInventoryBag()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OpenPickMoneyDialog(self):
		if exchange.GetElkFromSelf() > 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANT_EDIT_MONEY)
			return
		
		self.dlgPickMoney.Open(player.GetElk())

	def OnPickMoney(self, money):
		net.SendExchangeElkAddPacket(long(money))

	def AcceptExchange(self):
		if app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
			itemCountInTrade = 0
			yangAmountInTrade = 0

			for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
				itemCount = exchange.GetItemCountFromSelf(i)
				if itemCount >= 1:
					itemCountInTrade+=1
			
			if exchange.GetElkFromSelf() >= 1:
				yangAmountInTrade = int(exchange.GetElkFromSelf())

			if itemCountInTrade >= 3 or \
				yangAmountInTrade >= 1000000000:
				self.AskConfirmTrade()
			else:

				if exchange.GetElkFromSelf() >= 1 or itemCountInTrade:
					self.questionDialog = uiCommon.QuestionDialog2()
					self.questionDialog.SetText1(localeInfo.NEW_EXCHANGE_ALERT1)
					self.questionDialog.SetText2(localeInfo.NEW_EXCHANGE_ALERT2)
					self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.AcceptQuestion))
					self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
					self.questionDialog.Open()
				else:
					net.SendExchangeAcceptPacket()
					self.AcceptButton.Disable()
		else:
			net.SendExchangeAcceptPacket()
			self.AcceptButton.Disable()

	def AskConfirmTrade(self):
		self.userNameInput	= uiCommon.InputDialogWithDescription()
		self.userNameInput.SetMaxLength(24)
		self.userNameInput.SetDescription(localeInfo.TRADE_CONFIRMATION_DESC)
		self.userNameInput.SetAcceptEvent(self.AcceptEnteringName)
		self.userNameInput.SetCancelEvent(self.CancelEnteringName)
		self.userNameInput.SetTitle(localeInfo.TRADE_CONFIRMATION_TITLE)

		self.userNameInput.inputValue.SetText("")
		self.userNameInput.Open()
		self.AcceptButton.Disable()

	def AcceptEnteringName(self):
		targetName = self.userNameInput.GetText()

		self.popupMessage = uiCommon.PopupDialog()
		self.popupMessage.SetWidth(250)

		if targetName == exchange.GetNameFromTarget():
			net.SendExchangeAcceptPacket()
			self.AcceptButton.Disable()
			self.AcceptButton.Down()
			self.userNameInput.Hide()
			self.userNameInput = None
		else:
			if self.tradeWrongEnterCount > 0:
				self.popupMessage.SetText(localeInfo.TRADE_CONFIRMATION_ERROR.format(self.tradeWrongEnterCount))
				self.popupMessage.Open()
			else:
				self.CloseDialog()
				self.popupMessage.SetText(localeInfo.TRADE_CONFIRMATION_ERROR2)
				self.popupMessage.Open()
				net.SendExchangeExitPacket()
	
		self.tradeWrongEnterCount -= 1

	def CancelEnteringName(self):
		self.userNameInput.Hide()
		self.userNameInput = None
		self.AcceptButton.Enable()
		self.AcceptButton.SetUp()

	if app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
		def AcceptQuestion(self):
			net.SendExchangeAcceptPacket()
			self.AcceptButton.Disable()

			if self.questionDialog:
				self.questionDialog.Close()
			
			self.questionDialog = None

		def OnCloseQuestionDialog(self):
			if self.questionDialog:
				self.questionDialog.Close()
				self.questionDialog = None

			self.AcceptButton.Enable()
			self.AcceptButton.SetUp()

	def SelectOwnerEmptySlot(self, SlotIndex):
		if False == mouseModule.mouseController.isAttached():
			return

		if mouseModule.mouseController.IsAttachedMoney():
			net.SendExchangeElkAddPacket(mouseModule.mouseController.GetAttachedMoneyAmount())
		else:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			if (player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType):
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				SrcSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
				DstSlotNumber = SlotIndex
				if app.ENABLE_OFFLINE_SHOP:
					if uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(attachedInvenType, mouseModule.mouseController.GetAttachedSlotNumber()):
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
						return
				itemID = player.GetItemIndex(attachedInvenType, SrcSlotNumber)
				item.SelectItem(itemID)
				if item.IsAntiFlag(item.ANTIFLAG_GIVE):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANNOT_GIVE)
					mouseModule.mouseController.DeattachObject()
					return

				net.SendExchangeItemAddPacket(attachedInvenType, SrcSlotNumber, DstSlotNumber)
			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_UPGRADE_INVENTORY == attachedSlotType or\
					player.SLOT_TYPE_BOOK_INVENTORY == attachedSlotType or\
					player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType or\
					player.SLOT_TYPE_CHEST_INVENTORY == attachedSlotType:
					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
					if app.ENABLE_OFFLINE_SHOP:
						if uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(attachedInvenType, mouseModule.mouseController.GetAttachedSlotNumber()):
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
							return
					SrcSlotNumber = mouseModule.mouseController.GetRealAttachedSlotNumber()
					DstSlotNumber = SlotIndex
	
					itemID = player.GetItemIndex(attachedSlotType, SrcSlotNumber)
					item.SelectItem(itemID)
					
					if item.IsAntiFlag(item.ANTIFLAG_GIVE):
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANNOT_GIVE)
						mouseModule.mouseController.DeattachObject()
						return
						
					net.SendExchangeItemAddPacket(attachedInvenType, SrcSlotNumber, DstSlotNumber)
					
		mouseModule.mouseController.DeattachObject()

	def SelectOwnerItemSlot(self, SlotIndex):
		if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
			money = mouseModule.mouseController.GetAttachedItemCount()
			net.SendExchangeElkAddPacket(money)

	def RefreshOwnerSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromSelf(i)
			itemCount = exchange.GetItemCountFromSelf(i)
			if 1 == itemCount:
				itemCount = 0
			self.OwnerSlot.SetItemSlot(i, itemIndex, itemCount)

		self.OwnerSlot.RefreshSlot()

	def RefreshTargetSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromTarget(i)
			itemCount = exchange.GetItemCountFromTarget(i)
			if 1 == itemCount:
				itemCount = 0
			self.TargetSlot.SetItemSlot(i, itemIndex, itemCount)

		self.TargetSlot.RefreshSlot()

	def Refresh(self):
		self.RefreshOwnerSlot()
		self.RefreshTargetSlot()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.RefreshLockedSlot()

		self.OwnerMoney.SetText(localeInfo.NumberToMoneyString(exchange.GetElkFromSelf()))
		self.TargetMoney.SetText(localeInfo.NumberToMoneyString(exchange.GetElkFromTarget()))
		if exchange.GetAcceptFromSelf() == True:
			if not app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
				self.OwnerAcceptLight.Down()
			else:
				self.OwnerSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 0.3500, 0.8500, 0.3500, 1.0)
		else:

			self.AcceptButton.Enable()
			self.AcceptButton.SetUp()
			if not app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
				self.OwnerAcceptLight.SetUp()
			else:
				self.OwnerSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
		
		if exchange.GetAcceptFromTarget() == True:
			if not app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
				self.TargetAcceptLight.Down()
			else:
				self.TargetAcceptButton.Down()
				self.TargetSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 0.3500, 0.8500, 0.3500, 1.0)
		else:
			if not app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
				self.TargetAcceptLight.SetUp()
			else:
				self.TargetAcceptButton.SetUp()
				self.TargetSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)

	def OverInOwnerItem(self, slotIndex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeOwnerItem(slotIndex)

			if app.ENABLE_RENDER_TARGET:
				itemVnum = exchange.GetItemVnumFromSelf(slotIndex)
				self.tooltipItem.AppendRenderingTooltip(itemVnum)
	def OverInTargetItem(self, slotIndex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeTargetItem(slotIndex)
			
			if app.ENABLE_RENDER_TARGET:
				itemVnum = exchange.GetItemVnumFromTarget(slotIndex)
				self.tooltipItem.AppendRenderingTooltip(itemVnum)
	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnTop(self):
		self.tooltipItem.SetTop()

		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_EXCHANGE)
				self.interface.RefreshMarkInventoryBag()

	def OnUpdate(self):
		USE_EXCHANGE_LIMIT_RANGE = 1000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xStart) > USE_EXCHANGE_LIMIT_RANGE or abs(y - self.yStart) > USE_EXCHANGE_LIMIT_RANGE:
			(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()
			net.SendExchangeExitPacket()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItem(self, slotIndex, invenType):
			itemIndex = player.GetItemIndex(invenType, slotIndex)
		
			if itemIndex:
				# if player.GetItemBind(invenType, slotIndex) >= 1:
					# return True
					
				return player.IsAntiFlagBySlot(invenType, slotIndex, item.ANTIFLAG_GIVE)
				
			return False

		def CantTradableItemFromInventory(self, destSlotIndex, srcSlotIndex):
			if True == exchange.GetAcceptFromTarget():
				return

			itemInvenPage = srcSlotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = srcSlotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItems[destSlotIndex] = (itemInvenPage, localSlotPos)

			if self.wndInventory.GetInventoryPageIndex() == itemInvenPage and self.IsShow():
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def CantTradableItemFromDragonSoul(self, destSlotIndex, srcSlotIndex):
			if True == exchange.GetAcceptFromTarget():
				return

			if self.wndInventory:
				for exchangePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
					if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)
				self.wndInventory.wndItem.RefreshSlot()

			itemInvenPage = srcSlotIndex / player.DRAGON_SOUL_PAGE_SIZE
			localSlotPos = srcSlotIndex - (itemInvenPage * player.DRAGON_SOUL_PAGE_SIZE)
			self.lockedItemsDS[destSlotIndex] = (itemInvenPage, localSlotPos, srcSlotIndex)

			category = 0
			if srcSlotIndex >= 0 and srcSlotIndex < 192:
				category = 0
			elif srcSlotIndex >= 192 and srcSlotIndex < 384:
				category = 1
			elif srcSlotIndex >= 384 and srcSlotIndex < 576:
				category = 2
			elif srcSlotIndex >= 576 and srcSlotIndex < 768:
				category = 3
			elif srcSlotIndex >= 768 and srcSlotIndex < 960:
				category = 4
			elif srcSlotIndex >= 960 and srcSlotIndex < 1152:
				category = 5

			catCount = 6

			if self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage and self.IsShow():
				self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
			elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount and self.IsShow():
				self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
			elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*2 and self.IsShow():
				self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
			elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*3 and self.IsShow():
				self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
			elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*4 and self.IsShow():
				self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
			elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*5 and self.IsShow():
				self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)

		if app.ENABLE_SPECIAL_STORAGE:
			def CantTradableItemFromStorage(self, destSlotIndex, srcSlotIndex, invenType):
				if True == exchange.GetAcceptFromTarget():
					return

				itemInvenPage = srcSlotIndex / player.SPECIAL_PAGE_SIZE
				localSlotPos = srcSlotIndex - (itemInvenPage * player.SPECIAL_PAGE_SIZE)
				self.lockedItemsStorage[destSlotIndex] = (itemInvenPage, localSlotPos, invenType)
				
				category = 0
				if invenType == player.BOOK_INVENTORY:
					category = 0
				if invenType == player.STONE_INVENTORY:
					category = 1
				elif invenType == player.UPGRADE_INVENTORY:
					category = 2
				elif invenType == player.CHEST_INVENTORY:
					category = 3

				if self.wndSpecialStorage:
					if self.wndSpecialStorage.GetInventoryPageIndex() == itemInvenPage and self.wndSpecialStorage.GetCategoryIndex() == category and self.IsShow():
						self.wndSpecialStorage.wndItem.SetCantMouseEventSlot(localSlotPos)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				for exchangePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
					if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()
			
			if self.wndDragonSoul:
				for exchangePos, (itemInvenPage, itemSlotPos, srcSlotIndex) in self.lockedItemsDS.items():
					
					category = 0
					if srcSlotIndex >= 0 and srcSlotIndex < 192:
						category = 0
					elif srcSlotIndex >= 192 and srcSlotIndex < 384:
						category = 1
					elif srcSlotIndex >= 384 and srcSlotIndex < 576:
						category = 2
					elif srcSlotIndex >= 576 and srcSlotIndex < 768:
						category = 3
					elif srcSlotIndex >= 768 and srcSlotIndex < 960:
						category = 4
					elif srcSlotIndex >= 960 and srcSlotIndex < 1152:
						category = 5

					catCount = 6

					if self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage:
						self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
					elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount:
						self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
					elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*2:
						self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
					elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*3:
						self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
					elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*4:
						self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)
					elif self.wndDragonSoul.GetCategoryIndex() == category and self.wndDragonSoul.GetInventoryPageIndex() == itemInvenPage-catCount*5:
						self.wndDragonSoul.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndDragonSoul.wndItem.RefreshSlot()

			if app.ENABLE_SPECIAL_STORAGE:
				if self.wndSpecialStorage:
					for exchangePos, (itemInvenPage, itemSlotPos, invenType) in self.lockedItemsStorage.items():
					
						category = 0
						if invenType == player.BOOK_INVENTORY:
							category = 0
						elif invenType == player.STONE_INVENTORY:
							category = 1
						elif invenType == player.UPGRADE_INVENTORY:
							category = 2
						elif invenType == player.CHEST_INVENTORY:
							category = 3
							
						if self.wndSpecialStorage.GetInventoryPageIndex() == itemInvenPage and self.wndSpecialStorage.GetCategoryIndex() == category:
							self.wndSpecialStorage.wndItem.SetCantMouseEventSlot(itemSlotPos)

					self.wndSpecialStorage.wndItem.RefreshSlot()

		def BindInterface(self, interface):
			self.interface = interface
			
		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)

		def SetDSInven(self, wndDragonSoul):
			from _weakref import proxy
			self.wndDragonSoul = proxy(wndDragonSoul)
			
		if app.ENABLE_SPECIAL_STORAGE:
			def SetSpecialInven(self, wndSpecialStorage):
				from _weakref import proxy
				self.wndSpecialStorage = proxy(wndSpecialStorage)

