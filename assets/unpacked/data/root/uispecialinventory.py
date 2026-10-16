import ui, player, mouseModule, ime, net, app, item, chat, uiScriptLocale, uiCommon, uiPrivateShopBuilder \
,uiPickItem, localeInfo, constInfo, exchange, background, shop, safebox, uiToolTip, wndMgr, grp
from _weakref import proxy

if app.ENABLE_OFFLINE_SHOP:
	import uiOfflineShop
	import offlineshop

if app.ENABLE_HIDE_HIGHLIGHT:
	import systemSetting

ITEM_FLAG_APPLICABLE = 1 << 14

class SpecialInventory(ui.BoardWithTitleBar):

	BOOK_TYPE, STONE_TYPE, UPGRADE_TYPE, CHEST_TYPE, SAFEBOX_TYPE, MALL_TYPE, WINDOW_TYPE_MAX_NUM = xrange(7)
	SORT_UPGRADE, SORT_BOOK, SORT_STONE, SORT_CHEST = xrange(4)

	SLOT_WINDOW_TYPE = {
		BOOK_TYPE	:	{"window" : player.BOOK_INVENTORY, 		"slot" : player.SLOT_TYPE_BOOK_INVENTORY,       "title": localeInfo.TOOLTIP_SKILLBOOK_NAME,     "sort_inventory" : "/l05_sort_special_inv_items %d" % (player.BOOK_INVENTORY)},
		STONE_TYPE	:	{"window" : player.STONE_INVENTORY, 	"slot" : player.SLOT_TYPE_STONE_INVENTORY,      "title": uiScriptLocale.GUILD_METIN_STONE,      "sort_inventory" : "/l05_sort_special_inv_items %d" % (player.STONE_INVENTORY)},
		UPGRADE_TYPE:	{"window" : player.UPGRADE_INVENTORY, 	"slot" : player.SLOT_TYPE_UPGRADE_INVENTORY,    "title": uiScriptLocale.REFINE_TTILE,           "sort_inventory" : "/l05_sort_special_inv_items %d" % (player.UPGRADE_INVENTORY)},
		CHEST_TYPE	:	{"window" : player.CHEST_INVENTORY, 	"slot" : player.SLOT_TYPE_CHEST_INVENTORY,      "title": localeInfo.INVENTORY_GENERAL_ITEMS,    "sort_inventory" : "/l05_sort_special_inv_items %d" % (player.CHEST_INVENTORY)},
		SAFEBOX_TYPE:	{"window" : player.SAFEBOX, 			"slot" : player.SLOT_TYPE_SAFEBOX,              "title": uiScriptLocale.SAFE_TITLE,             "sort_inventory" : ""},
		MALL_TYPE	:	{"window" : player.MALL, 				"slot" : player.SLOT_TYPE_MALL,                 "title": uiScriptLocale.MALL_TITLE,             "sort_inventory" : ""},
	}

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.Constructor()
		self.LoadWindow()

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
		self.Constructor()

	def Constructor(self):
		self.questionDialog = None
		self.tooltipItem = None
		self.dlgSplitItems = None
		self.sellingSlotNumber = -1
		self.interface = None

		# Outside Parameters
		self.safeboxWindow = None
		self.mallWindow = None

		self.currentInventoryPage = 0
		self.currentCategory = 0

		self.cooldownTime = 0
		self.storageMode = False
		self.searchMode = False
		self.isShowSafeboxMall = False

		self.searchList = []

		if app.ENABLE_HIGHLIGHT_SYSTEM:
			self.bindWnds = []
			self.listHighlightedSlot = {
				self.BOOK_TYPE : [],
				self.STONE_TYPE : [],
				self.UPGRADE_TYPE : [],
				self.CHEST_TYPE : [],
			}

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.listCantMouseSlot = {
				self.BOOK_TYPE : [],
				self.STONE_TYPE : [],
				self.UPGRADE_TYPE : [],
				self.CHEST_TYPE : [],
				}

		self.inventoryButtons = []
		self.categoryButtons = []

	def LoadWindow(self):
		self.SetPosition(wndMgr.GetScreenWidth() - 176 - 287 - 10, (wndMgr.GetScreenHeight() - 37 - 525))
		self.AddFlag("movable")
		self.SetTitleName(uiScriptLocale.SPECIAL_INVENTORY_TITLE)
		self.SetCloseEvent(self.Close)

		self.wndItem = ui.GridSlotWindow()
		self.wndItem.SetParent(self)
		self.wndItem.SetPosition(7.5, 31)
		self.wndItem.ArrangeSlot(0, 5, 9, 32, 32, 0, 0)
		self.wndItem.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
		self.wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		self.wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndItem.Show()

		self.pageButtonTextList = ["I", "II", "III", "IV", "V"]
		for i in xrange(player.SPECIAL_PAGE_COUNT):
			button = ui.RadioButton()
			button.SetParent(self)
			button.SetUpVisual("d:/ymir work/ui/game/windows/tab_button_small_01.sub")
			button.SetOverVisual("d:/ymir work/ui/game/windows/tab_button_small_02.sub")
			button.SetDownVisual("d:/ymir work/ui/game/windows/tab_button_small_03.sub")
			button.SetPosition(7 + 32 * i, 325)
			button.SetText(self.pageButtonTextList[i])
			button.SetEvent(ui.__mem_func__(self.SetInventoryPage), i)    
			button.Show()
			self.inventoryButtons.append(button)

		buttonFolder = "d:/ymir work/ui/game/ekstra/special_inventory/"
		categoryIconList = [
			["book_1.png", "book_2.png", "book_3.png"], #Book
			["stone_1.png", "stone_2.png", "stone_3.png"], #Stone
			["upgrade_1.png", "upgrade_2.png", "upgrade_3.png"], #Upgrade
			["chest_1.png", "chest_2.png", "chest_3.png"], #General Items
			["safebox_1.png", "safebox_2.png", "safebox_3.png"], #Safebox
			["mall_1.png", "mall_2.png", "mall_3.png"],  #Mall
			
		]

		self.bgImageForButtons = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/game/ekstra/special_inventory/catbg.png", 8, 320)

		categoryPosList = [[7, 6], [7+36,6], [7+36*2, 6], [7+36*3,6], [7, 6+36], [7+36, 6+36]]
		for i in xrange(self.WINDOW_TYPE_MAX_NUM):
			button = ui.RadioButton()
			button.SetParent(self.bgImageForButtons)
			button.SetUpVisual(buttonFolder + categoryIconList[i][0])
			button.SetOverVisual(buttonFolder + categoryIconList[i][1])
			button.SetDownVisual(buttonFolder + categoryIconList[i][2])
			button.SetPosition(categoryPosList[i][0], categoryPosList[i][1])
			button.SetEvent(ui.__mem_func__(self.SetCategoryPage), i)
			button.ShowToolTip = lambda arg=i, arg2 = True: self.OverInButton(arg, arg2)
			button.HideToolTip = lambda arg=i: self.OverOutButton()
			button.Show()
			self.categoryButtons.append(button)

		self.sortInventoryBG = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/game/sbgs.png", 8, 7)
		self.sortInventoryButton = ui.MakeButton(self.sortInventoryBG, 11, 3, "", "", "d:/ymir work/ui/game/ref0.png", "d:/ymir work/ui/game/ref1.png", "d:/ymir work/ui/game/ref2.png")
		self.sortInventoryButton.SetEvent(ui.__mem_func__(self.SortInventoryFunction))
		self.sortInventoryButton.ShowToolTip = lambda arg=0: self.OverInButton(arg)
		self.sortInventoryButton.HideToolTip = lambda arg=0: self.OverOutButton()

		self.searchInventoryButton = ui.MakeButton(self.sortInventoryBG, 31, 3, "", "", "d:/ymir work/ui/game/sear0.png", "d:/ymir work/ui/game/sear1.png", "d:/ymir work/ui/game/sear2.png")
		self.searchInventoryButton.SetEvent(ui.__mem_func__(self.ToggleSearchMode))
		self.searchInventoryButton.ShowToolTip = lambda arg=1: self.OverInButton(arg)
		self.searchInventoryButton.HideToolTip = lambda arg=0: self.OverOutButton()

		loadAnimDir = "offlineshop/lightwork/searchshop/ani/new/"
		self.loadingAnimation = ui.AniImageBox()
		self.loadingAnimation.SetParent(self)
		self.loadingAnimation.SetPosition(55, 200)
		self.loadingAnimation.SetDelay(2)
		for animation in xrange(1, 33):
			self.loadingAnimation.AppendImage(loadAnimDir+"{}.png".format(animation))
		self.loadingAnimation.Hide()
		self.loadingText = ui.MakeTextLineNew(self.loadingAnimation, 0, 50, localeInfo.SPECIAL_STORAGE_PAGE_PLEASE_WAIT)

		self.searchEditLineImage = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/game/ekstra/special_inventory/hint5.png", 19, 67)
		self.searchEditLineImage.Hide()
		self.searchEditline = ui.MakeEditline(self.searchEditLineImage, 25, 4, 137, 22, 26, 137)
		self.searchEditline.SetUpdateEvent(ui.__mem_func__(self.OnIMEUpdateSearchItem))
		self.searchEditline.SetTabEvent(ui.__mem_func__(self.SearchItemCompleteTextSearch))
		self.searchEditline.SetReturnEvent(ui.__mem_func__(self.SearchItemCompleteTextSearch))
		self.searchEditline.SetEscapeEvent(ui.__mem_func__(self.ClearSearchItem))
		self.searchEditline.SetOverlayText(localeInfo.SHOP_SEARCH_ENTER_ITEMNAME)
		self.searchEditlineItemIcon = ui.MakeExpandedImageBox(self.searchEditLineImage, "d:/ymir work/ui/game/ekstra/special_inventory/asbg2.png", 2, 0)

		self.searchEditItemHint = ui.TextLine()
		self.searchEditItemHint.SetParent(self.searchEditline)
		# self.searchEditItemHint.SetPosition(0, 0)
		self.searchEditItemHint.SetPackedFontColor(grp.GenerateColor(1.0, 1.0, 1.0, 0.5))
		self.searchEditItemHint.Show()

		self.searchClearButton = ui.Button()
		self.searchClearButton.SetParent(self.searchEditline)
		self.searchClearButton.SetPosition(113.5, -3.5)
		self.searchClearButton.SetUpVisual("d:/ymir work/ui/game/inventory/search_btn_x_0.png")
		self.searchClearButton.SetOverVisual("d:/ymir work/ui/game/inventory/search_btn_x_1.png")
		self.searchClearButton.SetDownVisual("d:/ymir work/ui/game/inventory/search_btn_x_2.png")
		self.searchClearButton.SAFE_SetEvent(self.ClearSearchItem)
		self.searchClearButton.Hide()

		self.toolTipButtons = uiToolTip.ToolTip()
		self.toolTipButtons.ClearToolTip()

		self.dlgSplitItems = uiPickItem.PickItemDialog()
		self.dlgSplitItems.LoadDialog()
		self.dlgSplitItems.Hide()

		self.SetInventoryPage(0)
		self.SetCategoryPage(0)
		self.SetStorageMode(False)
		self.SetSearchMode(False)

	def Destroy(self):
		self.Constructor()

	def BindInterfaceClass(self, interfaceClass, safeboxClass, mallClass):
		self.interface = proxy(interfaceClass)
		self.safeboxWindow = proxy(safeboxClass)
		self.mallWindow = proxy(mallClass)

	if app.WJ_ENABLE_TRADABLE_ICON:
		def BindWindow(self, wnd):
			self.bindWnds.append(wnd)


	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SetInventoryPage(self, page):
		self.inventoryButtons[self.currentInventoryPage].SetUp()
		self.currentInventoryPage = page
		self.inventoryButtons[self.currentInventoryPage].Down()
		self.RefreshBagSlotWindow()

	def GetCategoryIndex(self):
		return self.currentCategory

	def GetInventoryPageIndex(self):
		return self.currentInventoryPage

	def SetCategoryPage(self, category):

		if self.currentCategory == self.SAFEBOX_TYPE:
			self.CloseSafebox()

		elif self.currentCategory == self.MALL_TYPE:
			self.CloseMall()

		self.currentCategory = category
		for index in xrange(len(self.categoryButtons)):
			self.categoryButtons[index].SetUp()
		self.categoryButtons[category].Down()
		self.SetTitleName(self.GetInventoryTitle())
		self.RefreshBagSlotWindow()

		if category == self.SAFEBOX_TYPE:
			if not self.storageMode:
				return
			self.sortInventoryButton.Hide()
			self.searchInventoryButton.Hide()
			self.sortInventoryButton.Disable()
			self.searchInventoryButton.Disable()
			self.OpenSafebox()
			self.interface.wndItemTransactions.Close() if app.ENABLE_ITEM_TRANSACTIONS else None
		elif category == self.MALL_TYPE:
			if not self.storageMode:
				return
			self.sortInventoryButton.Hide()
			self.searchInventoryButton.Hide()
			self.sortInventoryButton.Disable()
			self.searchInventoryButton.Disable()
			self.OpenMall()
			self.interface.wndItemTransactions.Close() if app.ENABLE_ITEM_TRANSACTIONS else None
		else:
			self.sortInventoryButton.Show()
			self.searchInventoryButton.Show()
			self.sortInventoryButton.Enable()
			self.searchInventoryButton.Enable()

		self.ClearSearchItem(True)

	def OverInItem(self, overSlotPos):
		overSlotPos = self.GetInventoryLocalSlotPosToGlobalSlotPos(overSlotPos)

		if app.ENABLE_HIGHLIGHT_SYSTEM:
			self.DelHighlightSlot(overSlotPos)

		self.wndItem.SetUsableItem(False)
## Lightwork correction@343
		if self.wndItem.IsIn():
			self.ShowToolTip(overSlotPos)
## Lightwork correction@343

	def ShowToolTip(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex, self.GetInventoryWindow())

			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					self.AddTooltipSaleMode(self.GetInventoryWindow(), slotIndex)

	if app.ENABLE_OFFLINE_SHOP:
		def AddTooltipSaleMode(self, window, slot):
			itemIndex = player.GetItemIndex(window,slot)
			if itemIndex !=0:
				item.SelectItem(itemIndex)
				if item.IsAntiFlag(item.ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ANTIFLAG_GIVE):
					return
				
				self.tooltipItem.AddRightClickForSale()

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInButton(self, textType=-1, isCat = False):
		if not self.toolTipButtons:
			return

		if isCat:
			self.toolTipButtons.ClearToolTip()
			self.toolTipButtons.AlignHorizonalCenter()
			self.toolTipButtons.AutoAppendNewTextLine(self.SLOT_WINDOW_TYPE[textType]["title"])
			self.toolTipButtons.Show()
		else:
			if textType == 0:
				self.toolTipButtons.ClearToolTip()
				self.toolTipButtons.AlignHorizonalCenter()
				self.toolTipButtons.AutoAppendNewTextLine(uiScriptLocale.SPECIAL_STORAGE_ARRANGE)
				self.toolTipButtons.Show()
			elif textType == 1:
				self.toolTipButtons.ClearToolTip()
				self.toolTipButtons.AlignHorizonalCenter()
				self.toolTipButtons.AutoAppendNewTextLine(uiScriptLocale.PARTY_MATCH_TEXT_REQUEST_MATCH)
				self.toolTipButtons.Show()


	def OverOutButton(self):
		if self.toolTipButtons:
			self.toolTipButtons.Hide()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.GetInventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)
		selectedItemVNum = player.GetItemIndex(self.GetInventoryWindow(), itemSlotIndex)
		itemCount = player.GetItemCount(self.GetInventoryWindow(), itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if self.GetInventoryType() != attachedSlotType:
				self.DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)
			else:
				if attachedItemVID == selectedItemVNum:
					net.SendItemMovePacket(self.GetInventoryWindow(), attachedSlotPos, self.GetInventoryWindow(), itemSlotIndex, 0) #This modifi: last value: attachedItemCount
				else:
					net.SendItemUseToItemPacket(self.GetInventoryWindow(), attachedSlotPos, self.GetInventoryWindow(), itemSlotIndex)

			mouseModule.mouseController.DeattachObject()
		else:
			item.SelectItem(selectedItemVNum)
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(self.GetInventoryWindow(), itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				if itemCount > 1:
					self.dlgSplitItems.SetTitleName(uiScriptLocale.SPLIT_ITEMS_WINDOW_TITLE)
					self.dlgSplitItems.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgSplitItems.Open(itemCount, itemVnum=player.GetItemIndex(self.GetInventoryWindow(), itemSlotIndex))
					self.dlgSplitItems.itemGlobalSlotIndex = itemSlotIndex

			elif self.interface and app.ENABLE_CHECK_IF_SAFEBOX_OPEN and safebox.isOpen() and (app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)) and not self.interface.dlgExchange.IsShow():
				self.interface.AttachItemFromSafebox(itemSlotIndex, safebox.GetItemID(itemSlotIndex))

			elif app.ENABLE_ITEM_TRANSACTIONS and app.IsPressed(app.DIK_X):
				if self.interface.wndItemTransactions.IsThisItemAdded(self.GetInventoryWindow(), itemSlotIndex):
					self.interface.RemoveItemTransactionsSlot(self.GetInventoryWindow(), itemSlotIndex)
				else:
					self.interface.AppendItemTransactionsSlot(self.GetInventoryWindow(), itemSlotIndex)

			else:
				mouseModule.mouseController.AttachObject(self, self.GetInventoryType(), itemSlotIndex, selectedItemVNum, itemCount)
				self.wndItem.SetUseMode(False)

	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if safebox.isOpen():
			return

		selectedSlotPos = self.GetInventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)
		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.SlotTypeToInvenType(attachedSlotType),attachedSlotPos):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return

			if self.IsSearchActive():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_CANNOT_DO_THIS_WHILE_SEARCHING)
				return

			if player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
				net.SendSafeboxCheckoutPacket(attachedSlotPos, self.GetInventoryWindow(), selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, self.GetInventoryWindow(), selectedSlotPos)

			elif player.RESERVED_WINDOW != attachedInvenType:
				itemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()

				if self.dlgSplitItems and self.dlgSplitItems.IsSplitAll():
					if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop():
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
						return
					if self.IsSearchActive():
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_CANNOT_DO_THIS_WHILE_SEARCHING)
						return
					net.SendChatPacket("/split_special_inv_item %d %d %d %d" % (attachedSlotPos, attachedCount, selectedSlotPos,self.GetInventoryWindow()))
					self.dlgSplitItems.SplitClear()
				else:
					self.SendMoveItemPacket(attachedInvenType, attachedSlotPos, self.GetInventoryWindow(), selectedSlotPos, attachedCount)

			elif player.SLOT_TYPE_INVENTORY == attachedSlotType:
				net.SendItemMovePacket(player.INVENTORY, attachedSlotPos, constInfo.getSpecialInventoryType(attachedSlotType), selectedSlotPos, long(attachedItemCount))

			elif attachedSlotType == player.SLOT_TYPE_UPGRADE_INVENTORY:
				net.SendItemMovePacket(constInfo.getSpecialInventoryType(attachedSlotType), attachedSlotPos, player.INVENTORY, selectedSlotPos, long(attachedItemCount))

			mouseModule.mouseController.DeattachObject()

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		if self.interface.IsAnyWindowOpen():
			return

		# ItemVNum = player.GetItemIndex(self.GetInventoryWindow(), slotIndex)
		windowIndex = self.GetInventoryWindow()
		slotIndex = self.GetInventoryLocalSlotPosToGlobalSlotPos(slotIndex)
		itemIndex = player.GetItemIndex(self.GetInventoryWindow(), slotIndex)
		item.SelectItem(itemIndex)

		if app.ENABLE_OFFLINE_SHOP:
			if uiOfflineShop.IsBuildingShop():
				if app.IsPressed(app.DIK_LCONTROL):
					if not item.IsAntiFlag(item.ANTIFLAG_GIVE) and not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
						self.interface.wndShopOffline.SetFastAddItem(True)
						offlineshop.ShopBuilding_AddItem(windowIndex, slotIndex, True) ## lightygrid
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
				else:
					if not item.IsAntiFlag(item.ANTIFLAG_GIVE) and not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
						offlineshop.ShopBuilding_AddItem(windowIndex, slotIndex)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return

		if app.ENABLE_CHECKINOUT_UPDATE:
			if exchange.isTrading() and (windowIndex, slotIndex):
				if windowIndex == player.UPGRADE_INVENTORY:
					net.SendExchangeItemAddPacket(player.UPGRADE_INVENTORY, slotIndex, -1)
					return
				elif windowIndex == player.BOOK_INVENTORY:
					net.SendExchangeItemAddPacket(player.BOOK_INVENTORY, slotIndex, -1)
					return
				elif windowIndex == player.STONE_INVENTORY:
					net.SendExchangeItemAddPacket(player.STONE_INVENTORY, slotIndex, -1)
					return
				elif windowIndex == player.CHEST_INVENTORY:
					net.SendExchangeItemAddPacket(player.CHEST_INVENTORY, slotIndex, -1)
					return

		if self.interface and self.interface.wndInventory.IsShow() and app.IsPressed(app.DIK_LCONTROL) and not self.interface.dlgExchange.IsShow() and not safebox.isOpen():
			if app.GetTime() < self.cooldownTime:
				chat.AppendChat(1, localeInfo.MINING_EVENT_RENEWAL_HIT_DELAY)
				return
			self.cooldownTime = app.GetTime() + 0.5
			net.SendChatPacket("/transfer_specialinv_to_inventory %d %d" % (slotIndex, self.GetInventoryWindow()))
			return

		if app.ENABLE_FAST_SKILL_BOOK_SYSTEM:
			if windowIndex == player.BOOK_INVENTORY:
				itemVnum = player.GetItemIndex(player.BOOK_INVENTORY, slotIndex)
				if constInfo.IsFastReadItem(itemVnum) and not self.interface.dlgExchange.IsShow():
					openPage = constInfo.GetFastReadItemPage(itemVnum)
					self.interface.OpenReadBookWindowPage(openPage)
					return

		# if app.ENABLE_CHEST_OPEN_RENEWAL:
		if app.IsPressed(app.DIK_LALT):
			# if str(background.GetCurrentMapName()) in constInfo.chestCheckMaps:
			# 	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.YOU_CANNOT_OPEN_CHEST_IN_CITY)
			# 	return
			net.SendItemUsePacket(windowIndex, slotIndex, constInfo.CHEST_OPEN_COUNT)
			return

		else:
			net.SendItemUsePacket(windowIndex, slotIndex)

		self.OverOutItem()

	def SendMoveItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if app.ENABLE_OFFLINE_SHOP:
			if uiOfflineShop.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return

		if self.IsSearchActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_CANNOT_DO_THIS_WHILE_SEARCHING)
			return

		if app.ENABLE_ITEM_TRANSACTIONS:
			if self.interface.wndItemTransactions.IsItemInList():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return

		net.SendItemMovePacket(srcSlotWindow , srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)

	def DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
		attachedCount = mouseModule.mouseController.GetAttachedItemCount()

		if srcItemSlotPos == dstItemSlotPos and attachedInvenType == self.GetInventoryWindow():
			return

		if app.ENABLE_ITEM_TRANSACTIONS:
			if self.interface.wndItemTransactions.IsItemInList():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return

		if (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
		else:
			self.SendMoveItemPacket(attachedInvenType, attachedSlotPos, self.GetInventoryWindow(), dstItemSlotPos, attachedCount)

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if self.interface.IsShowDlgQuestionWindow():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DONT_USE_ITEM_WHEN_SHOW_CONFIRM)
			return

		if app.ENABLE_ITEM_TRANSACTIONS:
			if self.interface.wndItemTransactions.IsItemInList():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return

		net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SellItem(self, itemSlotPos, soruSorma=False):
		if app.ENABLE_OFFLINE_SHOP:
			if uiOfflineShop.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return

		if self.IsSearchActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_CANNOT_DO_THIS_WHILE_SEARCHING)
			return

		self.sellingSlotNumber = itemSlotPos
		itemIndex = player.GetItemIndex(self.GetInventoryWindow(), itemSlotPos)
		itemCount = player.GetItemCount(self.GetInventoryWindow(), itemSlotPos)

		item.SelectItem(itemIndex)

		if item.IsAntiFlag(item.ANTIFLAG_SELL):
			popup = uiCommon.PopupDialog()
			popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
			popup.SetAcceptEvent(self.__OnClosePopupDialog)
			popup.SetAutoClose(True)
			popup.Open()
			self.popup = popup
			return

		if soruSorma:
			net.SendItemSellPacket(self.GetInventoryWindow(), itemSlotPos, itemCount)
			return
	
		item.GetItemName(itemIndex)
		itemName = item.GetItemName()
		itemPrice = item.GetISellItemPrice(itemSlotPos)*itemCount#fixed

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.count = itemCount

	def SellItem(self):
		if app.ENABLE_OFFLINE_SHOP:
			if uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(self.GetInventoryWindow(), self.sellingSlotNumber):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return
		if self.IsSearchActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_CANNOT_DO_THIS_WHILE_SEARCHING)
			return

		if app.ENABLE_ITEM_TRANSACTIONS:
			if self.interface.wndItemTransactions.IsItemInList():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return

		net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, self.GetInventoryWindow())
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None

	def __OnClosePopupDialog(self):
		if self.pop:
			self.pop.Close()
		self.pop = None

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()

	def RefreshBagSlotWindow(self):
		if not self.CanRefreshSpecialStoragePage():
			return
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVnum=self.wndItem.SetItemSlot

		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				onTopWindow = self.interface.GetOnTopWindow()

		if app.ENABLE_HIGHLIGHT_SYSTEM:
			for i in xrange(self.wndItem.GetSlotCount()):
				self.wndItem.DeactivateSlot(i)

		for i in xrange(player.SPECIAL_PAGE_SIZE*player.SPECIAL_PAGE_COUNT):
			self.wndItem.EnableSlot(i)

			slotNumber = self.GetInventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(self.GetInventoryWindow(), slotNumber)
			itemVnum = getItemVNum(self.GetInventoryWindow(), slotNumber)

			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			setItemVnum(i, itemVnum, itemCount)

			if app.ENABLE_ITEM_TRANSACTIONS:
				self.wndItem.ActivateSlot(i, (255.00 / 255.0), (255.00 / 255.0), (0.00 / 255.0), 1.0) if self.interface.wndItemTransactions.IsThisItemAdded(self.GetInventoryWindow(), slotNumber) else self.wndItem.DeactivateSlot(i)

			if len(self.searchList):
				if slotNumber not in self.searchList:
					self.wndItem.DisableSlot(i)
				else:
					self.wndItem.EnableSlot(i)

			if app.WJ_ENABLE_TRADABLE_ICON:
				if itemVnum and self.interface and onTopWindow:
					if self.interface.MarkUnusableInvenSlotOnTopWnd(onTopWindow, slotNumber, self.GetInventoryWindow()):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.MouseSlotEventRefresh()
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)

		self.wndItem.RefreshSlot()
		if app.ENABLE_HIGHLIGHT_SYSTEM:
			self.HighlightSlot_Refresh()

	if app.ENABLE_HIGHLIGHT_SYSTEM:
		def HighlightSlot_Refresh(self):
			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.GetInventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listHighlightedSlot[self.currentCategory] and self.currentCategory < 4 and app.ENABLE_HIDE_HIGHLIGHT and systemSetting.IsHighlightShow():
					self.wndItem.NewItemActivateSlot(i) #blue

		def HighlightSlot(self, slot, slotType):
			if slot > player.SPECIAL_PAGE_SIZE * player.SPECIAL_PAGE_COUNT:
				return

			self.listHighlightedSlot[self.currentCategory].append(slot)

		def DelHighlightSlot(self, inventorylocalslot):
			if inventorylocalslot in self.listHighlightedSlot[self.currentCategory] and self.currentCategory < 4:
				if inventorylocalslot >= player.INVENTORY_PAGE_SIZE*self.currentInventoryPage:
					self.wndItem.DeactivateSlot(inventorylocalslot-player.INVENTORY_PAGE_SIZE*self.currentInventoryPage)
				else:
					self.wndItem.DeactivateSlot(inventorylocalslot)

				self.listHighlightedSlot[self.currentCategory].remove(inventorylocalslot)

	# Get Part
	def GetInventoryPageIndex(self):
		return self.currentInventoryPage

	def GetInventoryWindow(self):
		return self.SLOT_WINDOW_TYPE[self.currentCategory]["window"]

	def GetInventoryType(self):
		return self.SLOT_WINDOW_TYPE[self.currentCategory]["slot"]

	def GetInventoryTitle(self):
		return self.SLOT_WINDOW_TYPE[self.currentCategory]["title"]

	def GetInventorySortCommand(self):
		return self.SLOT_WINDOW_TYPE[self.currentCategory]["sort_inventory"]

	def GetInventoryLocalSlotPosToGlobalSlotPos(self, localSlotPos):
		return self.currentInventoryPage * player.SPECIAL_PAGE_SIZE + localSlotPos
	# Get Part

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnTop(self):
		if self.tooltipItem:
			self.tooltipItem.SetTop()

		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgSplitItems.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(self.GetInventoryWindow(), itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, self.GetInventoryType(), itemSlotIndex, selectedItemVNum, count)

	def Close(self):
		if self.GetStorageMode():
			self.SetStorageMode(False)

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.dlgSplitItems:
			self.dlgSplitItems.Close()

		if self.currentCategory == self.SAFEBOX_TYPE:
			self.CloseSafebox()

		elif self.currentCategory == self.MALL_TYPE:
			self.CloseMall()

		self.SetCategoryPage(0)
		self.Hide()

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			if self.currentInventoryPage > 0:
				self.SetInventoryPage(self.currentInventoryPage - 1)

		else:
			if self.currentInventoryPage < (player.SPECIAL_PAGE_COUNT - 1):
				self.SetInventoryPage(self.currentInventoryPage + 1)

	def CanRefreshSpecialStoragePage(self):
		if self.currentCategory == self.SAFEBOX_TYPE or self.currentCategory == self.MALL_TYPE:
			return False
		return True

	def OpenSafebox(self):
		net.SendChatPacket("/safebox_password 000000")
		self.wndItem.Hide()

		for i in xrange(player.SPECIAL_PAGE_COUNT):
			self.inventoryButtons[i].Hide()

		self.loadingAnimation.Show()
		self.isShowSafeboxMall = True

	def CloseSafebox(self):
		net.SendChatPacket("/safebox_close")
		self.wndItem.Show()

		for i in xrange(player.SPECIAL_PAGE_COUNT):
			self.inventoryButtons[i].Show()

		if self.safeboxWindow:
			self.safeboxWindow.Hide()

		self.loadingAnimation.Hide()
		self.isShowSafeboxMall = False

	def ShowSafeboxWindow(self, size):
		if self.currentCategory != self.SAFEBOX_TYPE or not self.IsShow():
			net.SendChatPacket("/safebox_close")
			return
		
		if self.safeboxWindow:
			self.safeboxWindow.ShowWindow(size)
			self.loadingAnimation.Hide()
		self.isShowSafeboxMall = True

	def ShowMallWindow(self, size):
		if self.currentCategory != self.MALL_TYPE or not self.IsShow():
			net.SendChatPacket("/safebox_close")
			return
		
		if self.mallWindow:
			self.mallWindow.ShowWindow(size)
			self.loadingAnimation.Hide()
		self.isShowSafeboxMall = True

	def CommandCloseSafebox(self):
		if self.safeboxWindow:
			self.safeboxWindow.CommandCloseSafebox()
		self.isShowSafeboxMall = False

	def CommandCloseMall(self):
		if self.mallWindow:
			self.mallWindow.CommandCloseMall()
		self.isShowSafeboxMall = False

	def OpenMall(self):
		net.SendChatPacket("/mall_password 000000")
		self.wndItem.Hide()

		for i in xrange(player.SPECIAL_PAGE_COUNT):
			self.inventoryButtons[i].Hide()

		self.loadingAnimation.Show()
		self.isShowSafeboxMall = True

	def CloseMall(self):
		net.SendChatPacket("/mall_close")
		self.wndItem.Show()

		for i in xrange(player.SPECIAL_PAGE_COUNT):
			self.inventoryButtons[i].Show()

		if self.mallWindow:
			self.mallWindow.Hide()

		self.loadingAnimation.Hide()
		self.isShowSafeboxMall = False

	def CommandCloseMall(self):
		if self.mallWindow:
			self.mallWindow.CommandCloseMall()
		self.isShowSafeboxMall = False

	if app.ENABLE_DROP_DIALOG_EXTENDED_SYSTEM:
		def DeleteItem(self, slotPos, invenType):
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
			itemIndex = player.GetItemIndex(invenType, slotPos)
			item.SelectItem(itemIndex)
			itemQuestionDialog2 = uiCommon.QuestionDialogItem()
			ItemName = item.GetItemName()
			if len(ItemName) > 11:
				ItemName = ItemName[:11] + "..."
			if (player.GetItemCount(invenType, slotPos)) > 1:
				itemQuestionDialog2.SetMessage(localeInfo.ITEM_QUESTION_DIAGLOG_1.format((ItemName), player.GetItemCount(invenType, slotPos)))
			else:
				itemQuestionDialog2.SetMessage(localeInfo.ITEM_QUESTION_DIAGLOG_2.format(ItemName))
			itemQuestionDialog2.SetMessage2(localeInfo.ITEM_QUESTION_DIAGLOG_3.format(localeInfo.NumberToMoneyString(item.GetISellItemPrice() * player.GetItemCount(invenType, slotPos) * 100 / 100)))
			itemQuestionDialog2.SetAcceptEvent(lambda arg = 1: self.__AnswerDeleteItem(arg))
			itemQuestionDialog2.SetDestroyEvent(lambda arg = 0: self.__AnswerDeleteItem(arg))
			itemQuestionDialog2.SetCancelEvent(lambda arg = 2: self.__AnswerDeleteItem(arg))
			itemQuestionDialog2.slotPos = slotPos
			itemQuestionDialog2.invenType = invenType
			itemQuestionDialog2.Open(itemIndex, slotPos, "", invenType)
			self.itemQuestionDialog2 = itemQuestionDialog2

		def __AnswerDeleteItem(self, answer):
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
			if not self.itemQuestionDialog2:
				return
			else:
				if answer == 0:
					net.SendItemDeletePacket(self.itemQuestionDialog2.slotPos, self.itemQuestionDialog2.invenType)
				elif answer == 1:
					net.SendItemSellPacket(self.itemQuestionDialog2.slotPos, self.itemQuestionDialog2.invenType)
				self.itemQuestionDialog2.Close()
				self.itemQuestionDialog2 = None
				return

	def OnIMEUpdateSearchItem(self):
		EDIT_TEXT_BASE_COLOR = grp.GenerateColor(0.8549, 0.8549, 0.8549, 1.0)
		EDIT_TEXT_NOT_FOUND_COLOR = grp.GenerateColor(1.0, 0.2, 0.2, 1.0)
		self.searchEditItemHint.SetText("")
		self.searchEditline.SetPackedFontColor(EDIT_TEXT_BASE_COLOR)
		search_text = self.searchEditline.GetText()
		(itemHint, itemVnum) = item.GetItemDataByNamePart(search_text)
		item.SelectItem(itemVnum)

		if len(search_text):
			self.searchClearButton.Show()
			if itemVnum == -1:
				self.searchEditItemHint.SetText("")
				self.searchEditline.SetPackedFontColor(EDIT_TEXT_NOT_FOUND_COLOR)
				self.searchEditlineItemIcon.LoadImage("d:/ymir work/ui/game/ekstra/special_inventory/asbg2.png")

			else:
				self.searchEditItemHint.SetText(search_text + " " + itemHint[len(search_text):])
				if item.GetItemType() in [item.ITEM_TYPE_COSTUME, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_WEAPON]:
					self.searchEditlineItemIcon.LoadImage("d:/ymir work/ui/game/ekstra/special_inventory/asbg2.png")
				else:
					self.searchEditlineItemIcon.LoadImage(item.GetIconImageFileName())
					self.searchEditlineItemIcon.SetScale(0.65, 0.65)
		else:
			self.searchEditline.SetText("")
			self.searchEditItemHint.SetText("")
			self.searchClearButton.Hide()
			self.searchEditlineItemIcon.LoadImage("d:/ymir work/ui/game/ekstra/special_inventory/asbg2.png")

		if self.searchEditline.GetText():
			self.SetInventoryPage(0)
			for i in xrange(player.SPECIAL_PAGE_SIZE*player.SPECIAL_PAGE_COUNT):
				slotNumber = self.GetInventoryLocalSlotPosToGlobalSlotPos(i)
				itemIndex = player.GetItemIndex(self.GetInventoryWindow(), slotNumber)
				if itemIndex != 0:
					item.SelectItem(itemIndex)
					if item.GetItemName().lower().replace(" ", "") in self.searchEditline.GetText().lower().replace(" ", ""):
						if not i in self.searchList:
							self.searchList.append(slotNumber)
							self.RefreshBagSlotWindow()
		else:
			self.searchList = []
			self.RefreshBagSlotWindow()

	def SearchItemCompleteTextSearch(self):
		if self.searchEditline.GetText():
			oldTextItem = self.searchEditline.GetText()
			self.searchEditline.SetText(oldTextItem + self.searchEditItemHint.GetText()[len(oldTextItem)+1:])
			self.searchEditline.SetEndPosition()
			self.OnIMEUpdateSearchItem()

	def ClearSearchItem(self, changePage = False):
		if not self.searchEditline:
			return

		if len(self.searchEditline.GetText()) < 1:
			return

		if not changePage:
			if self.searchEditline.IsShowCursor():
				# self.OnPressEscapeKey()
			# else:
				self.searchEditline.SetText("")
				self.searchEditItemHint.SetText("")
		else:
			self.searchEditline.SetText("")
			self.searchEditItemHint.SetText("")

		self.searchList = []
		self.RefreshBagSlotWindow()
		
		if self.searchEditline:
			self.searchEditline.KillFocus()

		self.searchClearButton.Hide()
		self.searchEditlineItemIcon.LoadImage("d:/ymir work/ui/game/ekstra/special_inventory/asbg2.png")

	def IsSearchActive(self):
		if self.searchEditline.GetText():
			return True
		return False

	def SortInventoryFunction(self):
		if self.currentCategory == self.SAFEBOX_TYPE or self.currentCategory == self.MALL_TYPE:
			return

		if app.ENABLE_OFFLINE_SHOP:
			if uiOfflineShop.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return
	
		if self.IsSearchActive():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_CANNOT_DO_THIS_WHILE_SEARCHING)
			return

		self.startQuestionDialog = uiCommon.QuestionDialog2()
		self.startQuestionDialog.SetText1(localeInfo.ARRANGE_INFO_1)
		self.startQuestionDialog.SetText2(localeInfo.ARRANGE_INFO_2)
		self.startQuestionDialog.SetAcceptEvent(ui.__mem_func__(self.AcceptEvent))
		self.startQuestionDialog.SetCancelEvent(ui.__mem_func__(self.CancelEvent))
		self.startQuestionDialog.Open()

	def AcceptEvent(self):
		net.SendChatPacket(self.GetInventorySortCommand())
		self.CancelEvent()

	def CancelEvent(self):
		self.startQuestionDialog.Close()

	def SetStorageMode(self, mode):
		self.storageMode = mode
		self.SetSearchMode(False)

		if mode == True:
			self.SetSize(176, 438, 104, 65)
			self.bgImageForButtons.LoadImage("d:/ymir work/ui/game/ekstra/special_inventory/category_background.png")
			self.bgImageForButtons.SetPosition(8, 350)

			self.categoryButtons[self.SAFEBOX_TYPE].Show()
			self.categoryButtons[self.MALL_TYPE].Show()

		else:
			self.bgImageForButtons.LoadImage("d:/ymir work/ui/game/ekstra/special_inventory/catbg.png")
			self.bgImageForButtons.SetPosition(8, 350)
			self.SetSize(176, 403, 104, 65)
			self.categoryButtons[self.SAFEBOX_TYPE].Hide()
			self.categoryButtons[self.MALL_TYPE].Hide()

	def ToggleSearchMode(self):
		self.SetSearchMode(not self.searchMode)

	def SetSearchMode(self, mode):
		if self.GetSafeboxMallShowState():
			return

		self.ClearSearchItem()

		self.searchMode = mode

		if mode == True:
			self.SetSize(176, 430, 104, 65)
			self.searchEditLineImage.SetPosition(8, 35)
			self.searchEditLineImage.Show()
			self.wndItem.SetPosition(7.5, 61)
			for i in xrange(player.SPECIAL_PAGE_COUNT):
				self.inventoryButtons[i].SetPosition(7 + 32 * i, 325+26)
			self.bgImageForButtons.SetPosition(8, 376)

			if self.storageMode:
				self.SetStorageMode(False)

		else:
			self.searchEditLineImage.Hide()
			self.SetSize(176, 403, 104, 65)
			self.wndItem.SetPosition(7.5, 31)
			for i in xrange(player.SPECIAL_PAGE_COUNT):
				self.inventoryButtons[i].SetPosition(7 + 32 * i, 325)
			self.bgImageForButtons.SetPosition(8, 350)

	def GetStorageMode(self):
		return self.storageMode

	def GetSafeboxMallShowState(self):
		return self.isShowSafeboxMall

	if app.WJ_ENABLE_TRADABLE_ICON:
		def MouseSlotEventRefresh(self):
			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.GetInventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listCantMouseSlot[self.currentCategory]:
					itemInvenPage = slotNumber / player.INVENTORY_PAGE_SIZE
					localSlotPos = slotNumber - (itemInvenPage * player.INVENTORY_PAGE_SIZE)

					self.wndItem.SetCantMouseEventSlot(localSlotPos)
					self.wndItem.RefreshSlot()

		def MouseSlotEventClear(self):

			for i in xrange(self.wndItem.GetSlotCount()):
				slotNumber = self.GetInventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.listCantMouseSlot[self.currentCategory]:
					self.wndItem.SetCanMouseEventSlot(i)
					self.listCantMouseSlot[self.currentCategory].remove(slotNumber)

		def SetCantMouseSlot(self, slot):
			if slot > player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT:
				return

			if not slot in self.listCantMouseSlot[self.currentCategory]:
				self.listCantMouseSlot[self.currentCategory].append(slot)

		def SetCanMouseSlot(self, inventorylocalslot):

			if inventorylocalslot in self.listCantMouseSlot[self.currentCategory]:
				if inventorylocalslot >= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
					self.wndItem.SetCanMouseEventSlot(inventorylocalslot-player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex)
				else:
					self.wndItem.SetCanMouseEventSlot(inventorylocalslot)

				self.listCantMouseSlot[self.currentCategory].remove(inventorylocalslot)
