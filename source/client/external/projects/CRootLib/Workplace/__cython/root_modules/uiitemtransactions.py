import ui, localeInfo, player, item, chat, constInfo, uiCommon, app, shop

class ItemTransactions(ui.BoardWithTitleBar):
	WINDOW_WIDTH = 210
	WINDOW_HEIGHT = 140

	ITEM_TRANSACTIONS_LIST = []

	def __init__(self): 
		ui.BoardWithTitleBar.__init__(self)
		self.SetSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
		self.SetCenterPosition()
		self.AddFlag("movable")
		self.AddFlag("float")
		self.Hide()
		self.SetTitleName(localeInfo.ITEM_TRANSACTIONS_TITLE)
		self.SetCloseEvent(self.Close)

		self.interface = constInfo.GetInterfaceInstance()

		self.CreateSellButton()
		self.CreateDeleteButton()
		self.CreateSellPrice()
		self.CreateSellItemSelectedCount()
		self.CreateSellInfo()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def Destroy(self):
		self.Hide()
		self.ResetWindow()

	def Close(self):
		self.Hide()
		self.ResetWindow()
		item.RefreshInventory()
		if self.interface:
			self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
			# self.interface.RefreshMarkInventoryBag()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantSellInvenItem(self, slotIndex, invenType):
			itemIndex = player.GetItemIndex(invenType, slotIndex)
		
			if itemIndex:
				# if player.GetItemBind(invenType, slotIndex) >= 1:
					# return True
					
				return player.IsAntiFlagBySlot(invenType, slotIndex, item.ANTIFLAG_SELL)
				
			return False

		def OnTop(self):
			if not self.interface:
				return
				
			if shop.IsPrivateShop():
				self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
				self.interface.RefreshMarkInventoryBag()
			else:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_SHOP)
				self.interface.RefreshMarkInventoryBag()


	def Open(self):
		self.SetTop()
		self.Show()

	def ResetWindow(self):
		self.ITEM_TRANSACTIONS_LIST = []
		self.UpdatePrice()

	def AppendSellSlot(self, inventoryType, slotIndex):

		if self.IsThisItemAdded(inventoryType, slotIndex):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ITEM_TRANSACTIONS_ALREADY_IN_LIST)
			return

		if player.IsEquipmentSlot(slotIndex):
			return
		
		itemVnum = player.GetItemIndex(inventoryType, slotIndex)
		if itemVnum == 0:
			return
		item.SelectItem(itemVnum)
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL):
			return

		if not self.IsShow():
			self.Open()
			self.ResetWindow()

		self.ITEM_TRANSACTIONS_LIST.append({inventoryType: slotIndex})

	def RemoveSellSlot(self, inventoryType, slotIndex):
		self.ITEM_TRANSACTIONS_LIST.remove({inventoryType : slotIndex})
		if len(self.ITEM_TRANSACTIONS_LIST) == 0:
			self.Close()

	def CreateSellButton(self):
		sellButton = ui.Button()
		sellButton.SetParent(self)
		sellButton.SetPosition(self.WINDOW_WIDTH / 2 - 95, self.WINDOW_HEIGHT - 35)
		sellButton.SetUpVisual("d:/ymir work/ui/itemtransactions/mobil_sell_accept_01.png")
		sellButton.SetOverVisual("d:/ymir work/ui/itemtransactions/mobil_sell_accept_02.png")
		sellButton.SetDownVisual("d:/ymir work/ui/itemtransactions/mobil_sell_accept_03.png")
		sellButton.SetEvent(lambda arg = "Sell" : self.QuestionDialog(arg))
		sellButton.Show()

		self.sellButton = sellButton

	def CreateDeleteButton(self):
		self.deleteButton = ui.Button()
		self.deleteButton.SetParent(self)
		self.deleteButton.SetPosition(self.WINDOW_WIDTH / 2 + 1, self.WINDOW_HEIGHT - 35)
		self.deleteButton.SetUpVisual("d:/ymir work/ui/itemtransactions/mobil_sell_cancel_01.png")
		self.deleteButton.SetOverVisual("d:/ymir work/ui/itemtransactions/mobil_sell_cancel_02.png")
		self.deleteButton.SetDownVisual("d:/ymir work/ui/itemtransactions/mobil_sell_cancel_03.png")
		self.deleteButton.SetEvent(lambda arg = "Destroy" : self.QuestionDialog(arg))
		self.deleteButton.Show()

	def CreateSellItemSelectedCount(self):
		sellItemSelectedCountBG = ui.ImageBox()
		sellItemSelectedCountBG.SetParent(self)
		sellItemSelectedCountBG.SetPosition(self.WINDOW_WIDTH / 2 - 133 / 2, 7+30)
		sellItemSelectedCountBG.LoadImage("d:/ymir work/ui/itemtransactions/mobile_sell_value_bg.png")
		sellItemSelectedCountBG.Show()

		self.sellItemSelectedCountBG = sellItemSelectedCountBG

		sellItemSelectedCount = ui.TextLine()
		sellItemSelectedCount.SetParent(self)
		sellItemSelectedCount.SetPosition(self.WINDOW_WIDTH / 2, 10+30)
		sellItemSelectedCount.SetText("0")
		sellItemSelectedCount.SetHorizontalAlignCenter()
		sellItemSelectedCount.Show()

		self.sellItemSelectedCount = sellItemSelectedCount

	def CreateSellInfo(self):
		sellInfo = ui.TextLine()
		sellInfo.SetParent(self)
		sellInfo.SetPosition(self.WINDOW_WIDTH / 2, 49+30)
		sellInfo.SetText(localeInfo.ITEM_TRANSACTIONS_ADD_ITEMS)
		sellInfo.SetHorizontalAlignCenter()
		sellInfo.Show()
		self.sellInfo = sellInfo

	def CreateSellPrice(self):
		sellPriceBG = ui.ImageBox()
		sellPriceBG.SetParent(self)
		sellPriceBG.SetPosition(self.WINDOW_WIDTH / 2 - 133 / 2, 27+30)
		sellPriceBG.LoadImage("d:/ymir work/ui/itemtransactions/mobile_sell_value_bg.png")
		sellPriceBG.Show()

		self.sellPriceBG = sellPriceBG

		sellPrice = ui.TextLine()
		sellPrice.SetParent(self)
		sellPrice.SetPosition(self.WINDOW_WIDTH / 2, 29+30)
		sellPrice.SetText("0")
		sellPrice.SetHorizontalAlignCenter()
		sellPrice.Show()

		self.sellPrice = sellPrice

	def AdjustPosition(self, x, y):
		self.SetPosition(x, y)

	def UpdatePrice(self):
		price = 0
		selected_count = 0

		for totalItems in xrange(len(self.ITEM_TRANSACTIONS_LIST)):
			for invenType, itemSlotIndex in self.ITEM_TRANSACTIONS_LIST[totalItems].items():
				itemIndex = player.GetItemIndex(invenType, itemSlotIndex)
				if itemIndex == 0:
					continue
				item.SelectItem(itemIndex)
				itemPrice = item.GetISellItemPrice()
				itemCount = player.GetItemCount(invenType, itemSlotIndex)
		
				itemPrice = itemPrice * itemCount

				price += itemPrice
				selected_count += 1

		self.sellPrice.SetText(localeInfo.NumberToDecimalString(price))
		self.sellPrice.SetHorizontalAlignCenter()
		self.sellItemSelectedCount.SetText(localeInfo.ITEM_TRANSACTIONS_SELECTED_COUNT % selected_count)
		self.sellItemSelectedCount.SetHorizontalAlignCenter()

	def __OnClickTransactionsButton(self, transactions):
		itemLst = []
		for i in xrange(len(self.ITEM_TRANSACTIONS_LIST)):
			for invenType, itemSlotIndex in self.ITEM_TRANSACTIONS_LIST[i].items():
				tupleinfo = (itemSlotIndex,invenType)
				itemLst.append(tupleinfo)

		itemTuple = tuple(itemLst)
		item.SendTransactions(transactions, itemTuple)
		self.ResetWindow()
		self.Close()

	def IsThisItemAdded(self, inventoryType, slotIndex):
		for itemList in self.ITEM_TRANSACTIONS_LIST:
			if inventoryType in itemList and slotIndex in itemList.values():
				return True
		return False

	def IsItemInList(self):
		if len(self.ITEM_TRANSACTIONS_LIST) >= 1:
			return True
		return False

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def QuestionDialog(self, questionType):
		self.startQuestionDialog = uiCommon.QuestionDialog()
		if questionType is "Sell":
			self.startQuestionDialog.SetText(localeInfo.ITEM_TRANSACTIONS_QUESTION_DIALOG_1)
			self.startQuestionDialog.SetAcceptEvent(lambda arg=0: self.AcceptRequest(arg))
		elif questionType is "Destroy":
			self.startQuestionDialog.SetText(localeInfo.ITEM_TRANSACTIONS_QUESTION_DIALOG_2)
			self.startQuestionDialog.SetAcceptEvent(lambda arg=1: self.AcceptRequest(arg))
		self.startQuestionDialog.SetCancelEvent(ui.__mem_func__(self.CancelRequest))
		self.startQuestionDialog.Open()

	def AcceptRequest(self, type):
		if type is 0:
			self.__OnClickTransactionsButton(0)
		elif type is 1:
			self.__OnClickTransactionsButton(1)
		self.CancelRequest()

	def CancelRequest(self):
		self.startQuestionDialog.Close()