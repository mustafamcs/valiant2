import app
if app.ENABLE_INVENTORY_REWORK:
	import ui, player, mouseModule, net, app, item, player, chat, uiScriptLocale, uiAttachMetin, uiCommon, uiPrivateShopBuilder ,localeInfo \
		,constInfo ,ime ,wndMgr, uiPickItem, uiToolTip, blend_table, extraInfo, snd
	
	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		import acce
	if app.ENABLE_OFFLINE_SHOP:
		import offlineshop, uiOfflineShop
	if app.ENABLE_CHECKINOUT_UPDATE:
		import exchange
	
	if app.ENABLE_HIDE_HIGHLIGHT:
		import systemSetting
	if app.ENABLE_AURA_SYSTEM:
		import aura
	
	ITEM_FLAG_APPLICABLE = 1 << 14
	
	if extraInfo.ENABLE_INVENTORY_SIDEBAR:
		class SideBar(ui.Window):
			def __init__(self):
				ui.Window.__init__(self)
				self.__buttons = []
				self.SetSize(34, 0)
				if app.ENABLE_WINDOW_ANIMATION:
					self.SetWindowAnimation()
			def __del__(self):
				ui.Window.__del__(self)
				del self.__buttons[:]
		
			def AddButton(self, tooltip, defaultImage, hoverImage, activeImage, callback):
				btn = ui.Button()
				btn.SetParent(self)
				# btn.SetPosition(0, len(self.__buttons) * 36)
				btn.SetPosition(0, len(self.__buttons) * 36)
				btn.SetUpVisual(defaultImage)
				btn.SetOverVisual(hoverImage)
				btn.SetDownVisual(activeImage)
				btn.SetEvent(callback)
				btn.SetToolTipText(tooltip, -20, 7, 2)
				btn.Show()
			
				self.__buttons.append(btn)
			
				self.SetSize(self.GetWidth(), len(self.__buttons) * 36)
		
			def Reposition(self, x, y):
				self.SetPosition(x-10, y+155)#Baslangic konumu ayarlama
	
	class InventoryWindow(ui.ScriptWindow):
	
		USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_CHANGE_ATTRIBUTE2",  "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET")
		if app.ENABLE_USE_COSTUME_ATTR:
			USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR"])
	
		if app.ENABLE_ATTR_RARE_RENEWAL:
			USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_CHANGE_RARE_ATTRIBUTE", "USE_ADD_RARE_ATTRIBUTE"])
	
		questionDialog = None
		tooltipItem = None
		if app.ENABLE_SLOT_TOOLTIP:
			tooltipSlot = None
	
		dlgPickMoney = None
		interface = None
		sellingSlotNumber = -1
		isLoaded = 0
	
		wndEquip = None
		wndCostume = None
		wndBoosters = None
	
		if app.ENABLE_HIGHLIGHT_SYSTEM:
			liHighlightedItems = []
	
		if app.WJ_ENABLE_TRADABLE_ICON:
			bindWnds = []
	
		if extraInfo.ENABLE_INVENTORY_SIDEBAR:
			_inventorySidebar_ = None
	
		def __init__(self):
			ui.ScriptWindow.__init__(self)
	
			self.inventoryPageIndex = 0
	
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.wndAcceCombine = None
				self.wndAcceAbsorption = None
	
			if app.ENABLE_HIDE_COSTUME_SYSTEM:
				self.visibleButtonList = []
	
			self.__LoadWindow()
			if app.ENABLE_WINDOW_ANIMATION:
				self.SetWindowAnimation()
	
		def __del__(self):
			ui.ScriptWindow.__del__(self)
	
		def Show(self):
			self.__LoadWindow()
	
			ui.ScriptWindow.Show(self)
	
			if extraInfo.ENABLE_INVENTORY_SIDEBAR:
				if self._inventorySidebar_:
					self._inventorySidebar_.Show()
	
			if app.ENABLE_HIDE_COSTUME_SYSTEM:
				self.RefreshVisibleCostume() #Refresh hide costumes tooltip
	
		def BindInterfaceClass(self, interface):
			self.interface = interface
	
		if app.WJ_ENABLE_TRADABLE_ICON:
			def BindWindow(self, wnd):
				self.bindWnds.append(wnd)
	
		def __LoadWindow(self):
			if self.isLoaded == 1:
				return
	
			self.isLoaded = 1
	
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
			except:
				import exception
				exception.Abort("InventoryWindow.LoadWindow.LoadObject")
	
			try:
				wndItem = self.GetChild("ItemSlot")
				titleBar = self.GetChild("TitleBar")
				titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
	
				self.titleName = self.GetChild("TitleName")
	
				# Inventory Pages
				wndEquip 			= self.GetChild("Equipments_Slot")
				wndCostume 			= self.GetChild("Costumes_Slot")
				wndBoosters			= self.GetChild("Boosters_Slot")
	
				# Inventory Buttons
				self.DSSButton = self.GetChild2("DSSButton")
				self.mallButton = self.GetChild2("MallButton")
				self.sortInventoryButton = self.GetChild2("arrange_button")
				self.inventoryTab = []
				for i in xrange(player.INVENTORY_PAGE_COUNT):
					self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))
	
				self.equipmentTab = []
				for i in xrange(3):
					self.equipmentTab.append(self.GetChild("Equipment_Tab_%02d" % (i+1)))
	
				if app.WJ_ENABLE_TRADABLE_ICON:
					self.listCantMouseSlot = []
	
				if app.ENABLE_HIDE_COSTUME_SYSTEM:
					self.hideCostumeBtnList = [
					"hideHairCostumeBtn",
					"hideBodyCostumeBtn",
					"hideWeaponCostumeBtn",
					"hideAcceCostumeBtn",
					"hideAuraCostumeBtn",
					"hideCrownBtn"
					]
					for costumeBtns in self.hideCostumeBtnList:
						self.visibleButtonList.append(self.GetChild(costumeBtns))
	
			except:
				import exception
				exception.Abort("InventoryWindow.LoadWindow.BindObject")
	
			## Item
			wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
			wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
			wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
			wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
	
			## Equipment
			for invPages in [wndEquip, wndCostume, wndBoosters]:
				invPages.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
				invPages.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
				invPages.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
				invPages.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
				invPages.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				invPages.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
				if app.ENABLE_SLOT_TOOLTIP:
					invPages.SetOverInSlotEvent(ui.__mem_func__(self.OverInSlot))
					invPages.SetOverOutSlotEvent(ui.__mem_func__(self.OverOutSlot))
	
			self.windowNameList=[
				localeInfo.INVENTORY_TITLE_01,
				localeInfo.INVENTORY_TITLE_02,
				localeInfo.INVENTORY_TITLE_03
			]
	
			if app.ENABLE_SLOT_TOOLTIP:
				self.tooltipSlot = uiToolTip.ToolTip(140)
	
			## PickMoneyDialog
			dlgPickMoney = uiPickItem.PickItemDialog()
			dlgPickMoney.LoadDialog()
			dlgPickMoney.Hide()
	
			## AttachMetinDialog
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
			self.attachMetinDialog.Hide()
	
			for i in xrange(player.INVENTORY_PAGE_COUNT):
				self.inventoryTab[i].SetEvent(lambda arg=i: self.SetInventoryPage(arg))
				self.inventoryTab[0].Down()
	
			#@Init the new inventory category
			self.equipmentPageIndex = 0
			self.inventoryCategoryObjects = [self.GetChild("equipment_window"),
											self.GetChild("costume_window"),
											self.GetChild("booster_window")]
			index = 0
			for index, button in enumerate(self.equipmentTab):
				button.SetEvent(lambda arg=index: self.SetEquipmentPage(arg))
				button.ShowToolTip = lambda arg=index: self.OverInButton(arg, True)
				button.HideToolTip = lambda arg=index: self.OverOutButton()
				index += 1
	
			self.wndItem = wndItem
			self.wndEquip = wndEquip
			self.wndCostume = wndCostume
			self.wndBoosters = wndBoosters
	
			self.waitTime = 0
	
			self.dlgPickMoney = dlgPickMoney
	
			if self.DSSButton:
				self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))
	
			if self.sortInventoryButton:
				self.sortInventoryButton.SetEvent(ui.__mem_func__(self.click_sort_inventory))
				self.sortInventoryButton.ShowToolTip = lambda arg=0: self.OverInButton(arg)
				self.sortInventoryButton.HideToolTip = lambda arg=0: self.OverOutButton()
	
			# MallButton
			if self.mallButton:
				self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))
		
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.listAttachedAcces = []
	
			if app.ENABLE_AURA_SYSTEM:
				self.listAttachedAuras = []
	
			if app.ENABLE_HIDE_COSTUME_SYSTEM:
				for i in xrange(len(self.hideCostumeBtnList)):
					self.visibleButtonList[i].SetToggleUpEvent(ui.__mem_func__(self.VisibleCostume), i+1, 0)
					self.visibleButtonList[i].SetToggleDownEvent(ui.__mem_func__(self.VisibleCostume), i+1, 1)
	
			if extraInfo.ENABLE_INVENTORY_SIDEBAR:
				INV_IMG_PATH = "d:/ymir work/ui/game/side_inv/{}"
				imgDict = {
					"OfflineShop" : ["offlineshop.png", "offlineshop1.png", "offlineshop2.png"],
					"Switchbot" : ["switchbot.png", "switchbot1.png", "switchbot2.png"],
					"Wiki" : ["wikipedia.png", "wikipedia1.png", "wikipedia2.png"],
					"Buffi" : ["buffi.png", "buffi1.png", "buffi2.png"],
					# "SpecialInventory" : ["specialstorage.png", "specialstorage1.png", "specialstorage2.png"],
					# "DistanceNPC" : ["distancenpc.png", "distancenpc1.png", "distancenpc2.png"]
					}
				x, y = self.GetGlobalPosition()
				self._inventorySidebar_ = SideBar()
	
				self._inventorySidebar_.Reposition(x, y)
				# self._inventorySidebar_.AddButton(localeInfo.INVENTORY_SIDEBAR_BUTTON_1, INV_IMG_PATH.format(imgDict["SpecialInventory"][0]), INV_IMG_PATH.format(imgDict["SpecialInventory"][1]), INV_IMG_PATH.format(imgDict["SpecialInventory"][2]), self.clickSpecialInventory)
				self._inventorySidebar_.AddButton(localeInfo.INVENTORY_SIDEBAR_BUTTON_2, INV_IMG_PATH.format(imgDict["Wiki"][0]), INV_IMG_PATH.format(imgDict["Wiki"][1]), INV_IMG_PATH.format(imgDict["Wiki"][2]), self.clickWikipedia)
				self._inventorySidebar_.AddButton(localeInfo.INVENTORY_SIDEBAR_BUTTON_3, INV_IMG_PATH.format(imgDict["OfflineShop"][0]), INV_IMG_PATH.format(imgDict["OfflineShop"][1]), INV_IMG_PATH.format(imgDict["OfflineShop"][2]), self.clickOfflineShop)
				self._inventorySidebar_.AddButton(localeInfo.INVENTORY_SIDEBAR_BUTTON_4, INV_IMG_PATH.format(imgDict["Switchbot"][0]), INV_IMG_PATH.format(imgDict["Switchbot"][1]), INV_IMG_PATH.format(imgDict["Switchbot"][2]), self.clickSwitchbot)
				self._inventorySidebar_.AddButton(localeInfo.INVENTORY_SIDEBAR_BUTTON_5, INV_IMG_PATH.format(imgDict["Buffi"][0]), INV_IMG_PATH.format(imgDict["Buffi"][1]), INV_IMG_PATH.format(imgDict["Buffi"][2]), self.clickBuffiWindow)
				# self._inventorySidebar_.AddButton(localeInfo.INVENTORY_SIDEBAR_BUTTON_5, INV_IMG_PATH.format(imgDict["DistanceNPC"][0]), INV_IMG_PATH.format(imgDict["DistanceNPC"][1]), INV_IMG_PATH.format(imgDict["DistanceNPC"][2]), self.clickDistanceNPC)
	
			## Refresh
			self.SetInventoryPage(0)
			self.SetEquipmentPage(0)
			self.RefreshItemSlot()
	
		if extraInfo.ENABLE_INVENTORY_SIDEBAR:
			def clickOfflineShop(self):
				if self.interface:
					self.interface.wndGame.OpenPrivateShopBuilder()
	
			def clickSwitchbot(self):
				if self.interface:
					self.interface.ToggleSwitchbotWindow()
	
			def clickWikipedia(self):
				if self.interface:
					self.interface.OpenWikiWindow()
	
			def clickSpecialInventory(self):
				if self.interface:
					self.interface.ToggleSpecialStorageWindow()
	
			def clickDistanceNPC(self):
				if self.interface:
					self.interface.OpenDistanceNPCWindow()
	
			def clickBuffiWindow(self):
				if self.interface:
					self.interface.OpenBuffiWindow()
	
		def OverInButton(self, textType=-1, isCat = False):
			if not self.tooltipSlot:
				return
	
			if isCat:
				self.tooltipSlot.ClearToolTip()
				self.tooltipSlot.AlignHorizonalCenter()
				self.tooltipSlot.AutoAppendNewTextLine(self.windowNameList[textType])
				self.tooltipSlot.Show()
			else:
				if textType == 0:
					self.tooltipSlot.ClearToolTip()
					self.tooltipSlot.AlignHorizonalCenter()
					self.tooltipSlot.AutoAppendNewTextLine(uiScriptLocale.SPECIAL_STORAGE_ARRANGE)
					self.tooltipSlot.Show()
	
		def OverOutButton(self):
			if self.tooltipSlot:
				self.tooltipSlot.Hide()
	
		def Destroy(self):
			self.ClearDictionary()
			self.dlgPickMoney.Destroy()
			self.dlgPickMoney = 0
			self.attachMetinDialog.Destroy()
			self.attachMetinDialog = 0
			self.tooltipItem = None
			self.wndItem = 0
			self.wndEquip = 0
			self.wndCostume = 0
			self.wndBoosters = 0
			self.dlgPickMoney = 0
			self.questionDialog = None
			self.DSSButton = None
			self.mallButton = None
			self.interface = None
			self.waitTime = 0
			self.sortInventoryButton = None
			if constInfo.ENABLE_DSS_ACTIVE_EFFECT_BUTTON:
				self.DSSButtonEffect = None
			if app.ENABLE_OFFLINE_SHOP:	
				self.offlineShopNotificationEffect = None
	
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.bindWnds = []
	
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.wndAcceCombine = None
				self.wndAcceAbsorption = None
	
			self.inventoryTab = []
			self.equipmentTab = []
	
			if extraInfo.ENABLE_INVENTORY_SIDEBAR:
				if self._inventorySidebar_:
					del self._inventorySidebar_
	
			if app.ENABLE_SLOT_TOOLTIP:
				self.tooltipItem = None
	
		def Hide(self):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
				self.OnCloseQuestionDialog()
				return
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
	
			if self.dlgPickMoney:
				self.dlgPickMoney.Close()
	
			if extraInfo.ENABLE_INVENTORY_SIDEBAR:
				if self._inventorySidebar_:
					self._inventorySidebar_.Hide()
	
			if app.ENABLE_SLOT_TOOLTIP and self.tooltipSlot:
				self.tooltipSlot.HideToolTip()
	
			wndMgr.Hide(self.hWnd)
	
		def Close(self):
			self.Hide()
	
		def SetInventoryPage(self, page):
			self.inventoryPageIndex = page
			for index in xrange(len(self.inventoryTab)):
				self.inventoryTab[index].SetUp()
			self.inventoryTab[page].Down()
			self.RefreshBagSlotWindow()
	
		def SetEquipmentPage(self, page):
			self.equipmentPageIndex = page
	
			for button_key in xrange(len(self.equipmentTab)):
				invCatButtons = self.equipmentTab[button_key]
				invCatButtons.SetUp() if button_key != page else invCatButtons.Down()
			
			for key in xrange(len(self.inventoryCategoryObjects)):
				invCatObjects = self.inventoryCategoryObjects[key]
				invCatObjects.Hide() if key != page else invCatObjects.Show()
	
			self.equipmentPageIndex = page
			self.equipmentTab[1-page].SetUp()
			self.RefreshEquipSlotWindow()
	
			self.titleName.SetText(self.windowNameList[page])
	
		def ClickMallButton(self):
			if self.interface.wndSpecialStorage.GetSafeboxMallShowState():
				return
	
			if not self.interface.wndSpecialStorage.IsShow():
				self.interface.wndSpecialStorage.Show()
	
			self.interface.wndSpecialStorage.SetStorageMode(not self.interface.wndSpecialStorage.GetStorageMode())
	
		# DSSButton
		def ClickDSSButton(self):
			self.interface.ToggleDragonSoulWindow()
	
		def OnPickItem(self, count):
			itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.INVENTORY, itemSlotIndex):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
	
			selectedItemVNum = player.GetItemIndex(itemSlotIndex)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)
	
		if constInfo.ENABLE_DSS_ACTIVE_EFFECT_BUTTON:
			def UseDSSButtonEffect(self, enable):
				if self.DSSButton:
					DSS_BUTTON_1 = "d:/ymir work/ui/dragonsoul/dss_inventory_button_01.tga"
					DSS_BUTTON_2 = "d:/ymir work/ui/dragonsoul/dss_inventory_button_02.tga"
					DSS_BUTTON_3 = "d:/ymir work/ui/dragonsoul/dss_inventory_button_03.tga"
	
					DSSButtonEffect = ui.SlotWindow()
					DSSButtonEffect.AddFlag("attach")
					DSSButtonEffect.SetParent(self.DSSButton)
					DSSButtonEffect.SetPosition(3.2, 0)
	
					DSSButtonEffect.AppendSlot(0, 0, 0, 32, 32)
					DSSButtonEffect.SetRenderSlot(0)
					DSSButtonEffect.RefreshSlot()
	
					if enable == True:
						DSSButtonEffect.ActivateSlot(0, (51.00 / 255.0), (91.00 / 255.0), (220.00 / 255.0), 1.0)
						DSSButtonEffect.Show()
					else:
						DSSButtonEffect.DeactivateSlot(0)
						DSSButtonEffect.Hide()
					self.DSSButtonEffect = DSSButtonEffect
	
		def click_sort_inventory(self):
			self.__ClickStartButton()
	
		def __ClickStartButton(self):
			self.startQuestionDialog = uiCommon.QuestionDialog2()
			self.startQuestionDialog.SetText1(localeInfo.ARRANGE_INFO_1)
			self.startQuestionDialog.SetText2(localeInfo.ARRANGE_INFO_2)
			self.startQuestionDialog.SetAcceptEvent(ui.__mem_func__(self.__StartAccept))
			self.startQuestionDialog.SetCancelEvent(ui.__mem_func__(self.__StartCancel))
			self.startQuestionDialog.Open()
	
		def __StartAccept(self):
			net.SendChatPacket("/l05_sort_normal_items")
			self.__StartCancel()
		def __StartCancel(self):
			self.startQuestionDialog.Close()
	
		def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
			if player.IsEquipmentSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
				return local
	
			return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local
	
		def GetInventoryPageIndex(self):
			return self.inventoryPageIndex
	
		def RefreshBagSlotWindow(self):
			getItemVNum=player.GetItemIndex
			getItemCount=player.GetItemCount
			setItemVNum = self.wndItem.SetItemSlot
	
			if app.WJ_ENABLE_TRADABLE_ICON:
				if self.interface:
					onTopWindow = self.interface.GetOnTopWindow()
	
			for i in xrange(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
	
				itemCount = getItemCount(slotNumber)
	
				if 0 == itemCount:
					self.wndItem.ClearSlot(i)
					continue
	
				elif 1 == itemCount:
					itemCount = 0
	
				itemVnum = getItemVNum(slotNumber)
				setItemVNum(i, itemVnum, itemCount)
	
				if app.ENABLE_HIGHLIGHT_SYSTEM:
					if itemVnum == 0 and slotNumber in self.liHighlightedItems:
						self.liHighlightedItems.remove(slotNumber)
						
				if app.ENABLE_HIGHLIGHT_SYSTEM:
					if not slotNumber in self.liHighlightedItems:
						self.wndItem.DeactivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)
	
				# if app.ENABLE_AURA_SYSTEM:
				# 	slotNumberChecked = 0
				# 	for j in xrange(aura.WINDOW_MAX_MATERIALS):
				# 		(isHere, iCell) = aura.GetAttachedItem(j)
				# 		if isHere:
				# 			if iCell == slotNumber:
				# 				self.wndItem.ActivateSlot(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
				# 				if not slotNumber in self.listAttachedAuras:
				# 					self.listAttachedAuras.append(slotNumber)
						
				# 				slotNumberChecked = 1
				# 		else:
				# 			if slotNumber in self.listAttachedAuras and not slotNumberChecked:
				# 				self.wndItem.DeactivateSlot(i)
				# 				self.listAttachedAuras.remove(slotNumber)
	
				if app.WJ_ENABLE_TRADABLE_ICON:
					if itemVnum and self.interface and onTopWindow:
						if self.interface.MarkUnusableInvenSlotOnTopWnd(onTopWindow, slotNumber, player.INVENTORY):
							self.wndItem.SetUnusableSlotOnTopWnd(i)
						else:
							self.wndItem.SetUsableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
	
				elif (app.ENABLE_HIGHLIGHT_SYSTEM and not (constInfo.IS_BLEND_POTION(itemVnum) or constInfo.IS_EXTENDED_BLEND_POTION(itemVnum))) or (app.ENABLE_BUFFI_SYSTEM and constInfo.IS_BUFFI_ITEM(itemVnum)) :
					if not slotNumber in self.liHighlightedItems:
						self.wndItem.DeactivateSlot(i)
	
				if app.ENABLE_ITEM_TRANSACTIONS:
					self.wndItem.ActivateSlot(i, (255.00 / 255.0), (255.00 / 255.0), (0.00 / 255.0), 1.0) if self.interface.wndItemTransactions.IsThisItemAdded(player.INVENTORY, slotNumber) else self.wndItem.DeactivateSlot(i)
	
				if (app.ENABLE_EXTENDED_BLEND_AFFECT and (constInfo.IS_BLEND_POTION(itemVnum) or constInfo.IS_EXTENDED_BLEND_POTION(itemVnum))) or (app.ENABLE_BUFFI_SYSTEM and constInfo.IS_BUFFI_ITEM(itemVnum)):
					metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
					tempSlotNum = slotNumber
					if tempSlotNum >= player.INVENTORY_PAGE_SIZE:
						tempSlotNum -= (self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE)
	
					isActivated = 0 != metinSocket[3]
	
					if isActivated:
						self.wndItem.ActivateSlot(tempSlotNum)
					else:
						self.wndItem.DeactivateSlot(tempSlotNum)
	
				# if app.ENABLE_ACCE_COSTUME_SYSTEM:
				# 	slotNumberChecked = 0
				# 	if app.ENABLE_HIGHLIGHT_SYSTEM:
				# 		if not slotNumber in self.liHighlightedItems:
				# 			self.wndItem.DeactivateSlot(i)
				# 	else:
				# 		self.wndItem.DeactivateSlot(i)
	
				# 	for j in xrange(acce.WINDOW_MAX_MATERIALS):
				# 		(isHere, iCell) = acce.GetAttachedItem(j)
				# 		if isHere:
				# 			if iCell == slotNumber:
				# 				self.wndItem.ActivateSlot(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
				# 				if not slotNumber in self.listAttachedAcces:
				# 					self.listAttachedAcces.append(slotNumber)
	
				# 				slotNumberChecked = 1
				# 		else:
				# 			if slotNumber in self.listAttachedAcces and not slotNumberChecked:
				# 				self.wndItem.DeactivateSlot(i)
				# 				self.listAttachedAcces.remove(slotNumber)
	
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.MouseSlotEventRefresh()
				map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)
	
			self.wndItem.RefreshSlot()
			if app.ENABLE_HIGHLIGHT_SYSTEM:
				self.__RefreshHighlights()
	
		if app.ENABLE_HIGHLIGHT_SYSTEM:
			def HighlightSlot(self, slot):
				if not slot in self.liHighlightedItems:
					self.liHighlightedItems.append(slot)
	
			def __RefreshHighlights(self):
				if app.ENABLE_HIDE_HIGHLIGHT and systemSetting.IsHighlightShow() == False:
					return
				for i in xrange(player.INVENTORY_PAGE_SIZE):
					slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
					if slotNumber in self.liHighlightedItems:
						self.wndItem.NewItemActivateSlot(i) #blue
	
		def RefreshEquipSlotWindow(self):
			getItemVNum=player.GetItemIndex
			getItemCount=player.GetItemCount
			setItemVNum=self.wndEquip.SetItemSlot
			for i in xrange(player.EQUIPMENT_PAGE_COUNT):
				slotNumber = player.EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0
				setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
	
			self.wndEquip.RefreshSlot()
	
			if self.wndCostume:
				for slotNumber in self.wndCostume.GetSlotNumber():
					self.wndCostume.SetItemSlot(slotNumber, player.GetItemIndex(slotNumber), 0)
					self.wndCostume.EnableCoverButton(slotNumber)
				
				self.wndCostume.RefreshSlot()
	
			if self.wndBoosters:
				for slotNumber in self.wndBoosters.GetSlotNumber():
					self.wndBoosters.SetItemSlot(slotNumber, player.GetItemIndex(slotNumber), 0)
					self.wndBoosters.EnableCoverButton(slotNumber)
				self.wndBoosters.RefreshSlot()
	
		def RefreshItemSlot(self):
			self.RefreshBagSlotWindow()
			self.RefreshEquipSlotWindow()
	
		def SetItemToolTip(self, tooltipItem):
			self.tooltipItem = tooltipItem
	
		def SellItem(self):
			if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.INVENTORY, self.sellingSlotNumber):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return
			if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
				if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
					net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
					snd.PlaySound("sound/ui/money.wav")
			self.OnCloseQuestionDialog()
	
		def OnDetachMetinFromItem(self):
			if None == self.questionDialog:
				return
	
			self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
			self.OnCloseQuestionDialog()
	
		def OnCloseQuestionDialog(self):
			if not self.questionDialog:
				return
	
			self.questionDialog.Close()
			self.questionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
	
		## Slot Event
		def SelectEmptySlot(self, selectedSlotPos):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return
	
			selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)
	
			if mouseModule.mouseController.isAttached():
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
				attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
				if app.ENABLE_SPECIAL_STORAGE:
					attachedCount = mouseModule.mouseController.GetAttachedItemCount()
	
				if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.SlotTypeToInvenType(attachedSlotType), attachedSlotPos):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
	
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					#@fixme011 BEGIN (block ds equip)
					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
					if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
						mouseModule.mouseController.DeattachObject()
						return
					#@fixme011 END
	
					itemCount = player.GetItemCount(attachedSlotPos)
	
					if self.dlgPickMoney and self.dlgPickMoney.IsSplitAll():
						net.SendChatPacket("/split_normal_item %d %d %d" % (attachedSlotPos, attachedCount, selectedSlotPos))
						self.dlgPickMoney.SplitClear()
					else:
						self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)
	
					if item.IsRefineScroll(attachedItemIndex):
						self.wndItem.SetUseMode(False)
	
				elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
					mouseModule.mouseController.RunCallBack("INVENTORY")
	
				elif player.SLOT_TYPE_SHOP == attachedSlotType:
					net.SendShopBuyPacket(attachedSlotPos)
	
				elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)
	
				elif app.ENABLE_SWITCHBOT and player.SLOT_TYPE_SWITCHBOT == attachedSlotType:
					net.SendItemMovePacket(player.SWITCHBOT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)
	
				elif app.ENABLE_SPECIAL_STORAGE and attachedSlotType in [player.SLOT_TYPE_UPGRADE_INVENTORY, player.SLOT_TYPE_STONE_INVENTORY, player.SLOT_TYPE_BOOK_INVENTORY, player.SLOT_TYPE_CHEST_INVENTORY]:
					net.SendItemMovePacket(constInfo.getSpecialInventoryType(attachedSlotType), attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)
	
				elif player.SLOT_TYPE_MALL == attachedSlotType:
					net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)
	
				elif app.ENABLE_BUFFI_SYSTEM and player.SLOT_TYPE_BUFFI == attachedSlotType:
					net.SendItemMovePacket(player.BUFFI_WINDOW, attachedSlotPos, player.INVENTORY, selectedSlotPos, 1)
	
				mouseModule.mouseController.DeattachObject()
	
		def SelectItemSlot(self, itemSlotIndex):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return
			if self.attachMetinDialog.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return
	
			itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)
	
			if mouseModule.mouseController.isAttached():
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
	
				if app.ENABLE_SPECIAL_STORAGE:
					if attachedSlotType in [player.SLOT_TYPE_INVENTORY, player.SLOT_TYPE_UPGRADE_INVENTORY, player.SLOT_TYPE_STONE_INVENTORY, player.SLOT_TYPE_BOOK_INVENTORY, player.SLOT_TYPE_CHEST_INVENTORY]:
							#@fixme011 BEGIN (block ds equip)
						attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
						if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
							mouseModule.mouseController.DeattachObject()
							return
						#@fixme011 END
						self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedInvenType, attachedSlotPos, itemSlotIndex, attachedSlotType)
	
				else:
					if player.SLOT_TYPE_INVENTORY == attachedSlotType:
						#@fixme011 BEGIN (block ds equip)
						attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
						if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
							mouseModule.mouseController.DeattachObject()
							return
						#@fixme011 END
						self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedInvenType, attachedSlotPos, itemSlotIndex, attachedSlotType)
	
	
	
				mouseModule.mouseController.DeattachObject()
	
			else:
				ItemVNum = player.GetItemIndex(itemSlotIndex)
				item.SelectItem(ItemVNum)
				curCursorNum = app.GetCursor()
				if app.SELL == curCursorNum:
					self.__SellItem(itemSlotIndex)
	
				elif app.BUY == curCursorNum:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
	
				elif app.ENABLE_ITEM_TRANSACTIONS and app.IsPressed(app.DIK_X):
					if self.interface.wndItemTransactions.IsThisItemAdded(player.INVENTORY, itemSlotIndex):
						self.interface.RemoveItemTransactionsSlot(player.INVENTORY, itemSlotIndex)
					else:
						self.interface.AppendItemTransactionsSlot(player.INVENTORY, itemSlotIndex)
					return
	
				elif app.IsPressed(app.DIK_LALT):
					link = player.GetItemLink(itemSlotIndex)
					ime.PasteString(link)
	
				elif app.IsPressed(app.DIK_LSHIFT):
					itemCount = player.GetItemCount(itemSlotIndex)
					if itemCount > 1:
						self.dlgPickMoney.SetTitleName(uiScriptLocale.SPLIT_ITEMS_WINDOW_TITLE)
						self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
						self.dlgPickMoney.Open(itemCount, itemVnum=ItemVNum)
						self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
	
				# elif app.IsPressed(app.DIK_LCONTROL):
				# 	itemIndex = player.GetItemIndex(itemSlotIndex)
	
				# 	if True == item.CanAddToQuickSlotItem(itemIndex):
				# 		player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				# 	else:
				# 		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)
	
				else:
					selectedItemVNum = player.GetItemIndex(itemSlotIndex)
					itemCount = player.GetItemCount(itemSlotIndex)
					mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
					snd.PlaySound("sound/ui/pick.wav")
	
					if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
						self.wndItem.SetUseMode(True)
					else:
						self.wndItem.SetUseMode(False)
	
		def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemInv, srcItemSlotPos, dstItemSlotPos, attachedSlotType):
			if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and (uiOfflineShop.IsSaleSlot(player.INVENTORY, srcItemSlotPos) or uiOfflineShop.IsSaleSlot(player.INVENTORY , dstItemSlotPos)):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return
	
			if app.ENABLE_ITEM_TRANSACTIONS:
				if self.interface.wndItemTransactions.IsItemInList():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
					return
	
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			attachedCount = mouseModule.mouseController.GetAttachedItemCount()
	
			if app.ENABLE_SPECIAL_STORAGE:
				if srcItemSlotPos == dstItemSlotPos and attachedInvenType == player.INVENTORY:
					return
			else:
				if srcItemSlotPos == dstItemSlotPos:
					return
	
			if app.ENABLE_SPECIAL_STORAGE:
				if constInfo.IsAttr(srcItemVID):
					if srcItemInv != player.INVENTORY:
						self.__SendUseItemToItemPacketAttr(srcItemSlotPos, dstItemSlotPos)
						return
	
			if item.IsRefineScroll(srcItemVID):
				if player.GetItemIndex(srcItemSlotPos) == player.GetItemIndex(dstItemSlotPos):
					self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos,0)
				else:
					self.RefineItem(srcItemSlotPos, dstItemSlotPos)
					self.wndItem.SetUseMode(False)
	
			elif srcItemVID == player.GetItemIndex(dstItemSlotPos):
				self.__SendMoveItemPacketSpecial(attachedInvenType, attachedSlotPos, player.INVENTORY, dstItemSlotPos, attachedCount)
				return
	
			elif item.IsMetin(srcItemVID):
				self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)
	
			elif item.IsDetachScroll(srcItemVID):
				self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)
	
			elif item.IsKey(srcItemVID):
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
	
			elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
	
			elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
	
			else:
				if player.IsEquipmentSlot(dstItemSlotPos):
					if item.IsEquipmentVID(srcItemVID):
						self.__UseItem(srcItemSlotPos)
				else:
					self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
	
		def __SellItem(self, itemSlotPos):
			if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return
			if not player.IsEquipmentSlot(itemSlotPos):
				self.sellingSlotNumber = itemSlotPos
				itemIndex = player.GetItemIndex(itemSlotPos)
				itemCount = player.GetItemCount(itemSlotPos)
	
	
				self.sellingSlotitemIndex = itemIndex
				self.sellingSlotitemCount = itemCount
	
				item.SelectItem(itemIndex)
	
				if item.IsAntiFlag(item.ANTIFLAG_SELL):
					popup = uiCommon.PopupDialog()
					popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
					popup.SetAcceptEvent(self.__OnClosePopupDialog)
					popup.Open()
					popup.SetAutoClose(True)
					self.popup = popup
					return
				itemPrice = item.GetISellItemPrice(itemSlotPos)*itemCount#fixed
	
				item.GetItemName(itemIndex)
				itemName = item.GetItemName()
	
				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				self.questionDialog.Open()
				self.questionDialog.count = itemCount
	
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
	
		def __OnClosePopupDialog(self):
			self.pop = None
	
		def RefineItem(self, scrollSlotPos, targetSlotPos):
	
			scrollIndex = player.GetItemIndex(scrollSlotPos)
			targetIndex = player.GetItemIndex(targetSlotPos)
			if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return
			if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
				return
	
			if int(scrollIndex) == 71032:
				constInfo.usedUpgraddeItemType = 1
			elif int(scrollIndex) == 70039:
				constInfo.usedUpgraddeItemType = 2
			elif int(scrollIndex) == 25042:
				constInfo.usedUpgraddeItemType = 3
			else:
				constInfo.usedUpgraddeItemType = 0
	
			if app.ENABLE_REFINE_RENEWAL:
				constInfo.AUTO_REFINE_TYPE = 1
				constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
				constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos
	
			self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
			return
	
		def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
			scrollIndex = player.GetItemIndex(scrollSlotPos)
			targetIndex = player.GetItemIndex(targetSlotPos)
	
			if not player.CanDetach(scrollIndex, targetSlotPos):
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					item.SelectItem(scrollIndex)
					if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_FAILURE_CLEAN)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				return
	
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				item.SelectItem(targetIndex)
				if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
					item.SelectItem(scrollIndex)
					if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
						self.questionDialog.SetText(localeInfo.ACCE_DO_YOU_CLEAN)
	
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.sourcePos = scrollSlotPos
			self.questionDialog.targetPos = targetSlotPos
	
		def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
			if app.ENABLE_SPECIAL_STORAGE:
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				if player.INVENTORY == attachedSlotType:
					metinIndex = player.GetItemIndex(metinSlotPos)
				else:
					metinIndex = player.GetItemIndex(player.STONE_INVENTORY, metinSlotPos)
			else:
				metinIndex = player.GetItemIndex(metinSlotPos)
			targetIndex = player.GetItemIndex(targetSlotPos)
	
			item.SelectItem(metinIndex)
			itemName = item.GetItemName()
	
			result = player.CanAttachMetin(metinIndex, targetSlotPos)
	
			if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))
	
			if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))
	
			elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))
	
			elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)
	
			if player.ATTACH_METIN_OK != result:
				return
	
			self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)
	
		def OverOutItem(self):
			self.wndItem.SetUsableItem(False)
			if None != self.tooltipItem:
				self.tooltipItem.HideToolTip()
	
		if app.ENABLE_SLOT_TOOLTIP:
			def OverInSlot(self, slotIndex):
	
				m_slotTooltip = {
					item.EQUIPMENT_WEAPON : uiScriptLocale.LOOTING_SYSTEM_WEAPON,
					item.EQUIPMENT_HEAD : uiScriptLocale.LOOTING_SYSTEM_HEAD,
					item.EQUIPMENT_BODY : uiScriptLocale.LOOTING_SYSTEM_ARMOR,
					item.EQUIPMENT_SHOES : uiScriptLocale.LOOTING_SYSTEM_CATEGORY_COMMON_FOOTS,
					item.EQUIPMENT_WRIST : uiScriptLocale.LOOTING_SYSTEM_CATEGORY_COMMON_WRIST,
					item.EQUIPMENT_NECK : uiScriptLocale.LOOTING_SYSTEM_CATEGORY_COMMON_NECK,
					item.EQUIPMENT_EAR : uiScriptLocale.LOOTING_SYSTEM_CATEGORY_COMMON_EAR,
					item.EQUIPMENT_ARROW : localeInfo.INVENTORYSLOT_TOOLTIP_ARROW,
					item.EQUIPMENT_SHIELD : localeInfo.INVENTORYSLOT_TOOLTIP_SHIELD,
	
					item.EQUIPMENT_BELT : uiScriptLocale.LOOTING_SYSTEM_CATEGORY_COMMON_BELT,
					item.EQUIPMENT_PET : localeInfo.CUBE_CATEGORY_PET,
	
					item.EQUIPMENT_PENDANT : localeInfo.CATEGORY_JEWELRY_ARMOR_PENDANT,
					item.EQUIPMENT_GLOVE : localeInfo.INVENTORYSLOT_TOOLTIP_GLOVE,
					item.EQUIPMENT_CROWN : localeInfo.INVENTORYSLOT_TOOLTIP_CROWN,
	
					item.DREAMSOUL_SLOT_RED : localeInfo.INVENTORYSLOT_TOOLTIP_DREAMSOUL_RED,
					item.DREAMSOUL_SLOT_BLUE : localeInfo.INVENTORYSLOT_TOOLTIP_DREAMSOUL_BLUE,
	
					item.EQUIPMENT_UNIQUE1 : uiScriptLocale.LOOTING_SYSTEM_UNIQUE,
					item.EQUIPMENT_UNIQUE2 : uiScriptLocale.LOOTING_SYSTEM_UNIQUE,
	
					item.EQUIPMENT_COSTUME_WEAPON : localeInfo.INVENTORYSLOT_TOOLTIP_WEAPON_SKIN,
					item.EQUIPMENT_COSTUME_HAIR : localeInfo.INVENTORYSLOT_TOOLTIP_HAIR,
					item.EQUIPMENT_COSTUME_BODY : localeInfo.INVENTORYSLOT_TOOLTIP_BODY,
					item.EQUIPMENT_MOUNT : localeInfo.PRIVATESHOPSEARCH_COSTUME_MOUNT,
					item.EQUIPMENT_ACCE : localeInfo.CATEGORY_COSTUMES_SASH,
	
					item.COSTUME_SLOT_AURA : localeInfo.INVENTORYSLOT_TOOLTIP_AURA,
		
					item.MOUNT_SKIN_SLOT : localeInfo.INVENTORYSLOT_TOOLTIP_MOUNT_SKIN,
					item.PET_SKIN_SLOT : localeInfo.INVENTORYSLOT_TOOLTIP_PET_SKIN,
					item.COSTUME_SLOT_WING : localeInfo.INVENTORYSLOT_TOOLTIP_ACCE_SKIN,
	
					item.ITEM_AURA_SKIN_SLOT : localeInfo.INVENTORYSLOT_TOOLTIP_AURA_SKIN,
	
					item.BOOSTER_SLOT_WEAPON : localeInfo.INVENTORYSLOT_TOOLTIP_BOOSTER,
					item.BOOSTER_SLOT_BODY : localeInfo.INVENTORYSLOT_TOOLTIP_BOOSTER2,
					item.BOOSTER_SLOT_HEAD : localeInfo.INVENTORYSLOT_TOOLTIP_BOOSTER3,
	
					item.EQUIPMENT_NEW_PET : localeInfo.INVENTORYSLOT_TOOLTIP_PET_SYSTEM,
	
					# item.BOOSTER_SLOT_SASH : localeInfo.INVENTORYSLOT_TOOLTIP_BOOSTER4,
					# item.BOOSTER_SLOT_PET : localeInfo.INVENTORYSLOT_TOOLTIP_BOOSTER5,
					# item.BOOSTER_SLOT_MOUNT : localeInfo.INVENTORYSLOT_TOOLTIP_BOOSTER6,
	
					item.RING_SLOT_0 : localeInfo.INVENTORYSLOT_TOOLTIP_RING,
					item.RING_SLOT_1 : localeInfo.INVENTORYSLOT_TOOLTIP_RING2,
					item.RING_SLOT_2 : localeInfo.INVENTORYSLOT_TOOLTIP_RING3,
					item.RING_SLOT_3 : localeInfo.INVENTORYSLOT_TOOLTIP_RING4,
					# item.RING_SLOT_4 : uiScriptLocale.LOOTING_SYSTEM_UNIQUE,
					# item.RING_SLOT_5 : uiScriptLocale.LOOTING_SYSTEM_UNIQUE,
					# item.RING_SLOT_6 : uiScriptLocale.LOOTING_SYSTEM_UNIQUE,
					# item.RING_SLOT_7 : uiScriptLocale.LOOTING_SYSTEM_UNIQUE,
	
	
				}
				
				if slotIndex in m_slotTooltip and self.tooltipSlot and\
					(self.wndEquip.IsIn() or self.wndCostume.IsIn() or self.wndBoosters.IsIn()):
					self.tooltipSlot.ClearToolTip()
					self.tooltipSlot.AutoAppendTextLine(m_slotTooltip[slotIndex])
					self.tooltipSlot.AlignHorizonalCenter()
					self.tooltipSlot.ShowToolTip()
	
			def OverOutSlot(self):
				if self.tooltipSlot:
					self.tooltipSlot.HideToolTip()
	
	## Lightwork correction@343
		def InventorySlotTooltipCheck(self, overSlotPosGlobal):
			# if self.wndItem.IsIn() or self.wndBelt.wndBeltInventorySlot.IsIn () or\
	
			windows = (self.wndItem.IsIn(), self.wndEquip.IsIn(), self.wndCostume.IsIn(), self.wndBoosters.IsIn())
	
			if any(windows):
				self.ShowToolTip(overSlotPosGlobal)
	## Lightwork correction@343
	
		def OverInItem(self, overSlotPos):
			overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
			self.wndItem.SetUsableItem(False)
	
			if app.ENABLE_HIGHLIGHT_SYSTEM and overSlotPosGlobal in self.liHighlightedItems:
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					if not overSlotPosGlobal in (self.listAttachedAcces or self.listAttachedAuras):
						self.liHighlightedItems.remove(overSlotPosGlobal)
					elif not overSlotPosGlobal in self.listAttachedCl:
						self.liHighlightedItems.remove(overSlotPosGlobal)
				else:
					self.liHighlightedItems.remove(overSlotPosGlobal)
				self.wndItem.DeactivateSlot(overSlotPos)
	
			if mouseModule.mouseController.isAttached():
				attachedItemType = mouseModule.mouseController.GetAttachedType()
				if app.ENABLE_SPECIAL_STORAGE:
					if player.SLOT_TYPE_INVENTORY == attachedItemType or player.SLOT_TYPE_UPGRADE_INVENTORY == attachedItemType or player.SLOT_TYPE_STONE_INVENTORY == attachedItemType or player.SLOT_TYPE_BOOK_INVENTORY == attachedItemType or player.SLOT_TYPE_CHEST_INVENTORY == attachedItemType:
						attachedSlotPos = mouseModule.mouseController.GetRealAttachedSlotNumber()
						attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
	
						if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPosGlobal):
							self.wndItem.SetUsableItem(True)
							self.wndItem.SetUseMode(True)
							self.ShowToolTip(overSlotPosGlobal)
							return
				else:
					if player.SLOT_TYPE_INVENTORY == attachedItemType:
						attachedSlotPos = mouseModule.mouseController.GetRealAttachedSlotNumber()
						attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
						if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPosGlobal):
							self.wndItem.SetUsableItem(True)
							self.ShowToolTip(overSlotPosGlobal)
							return
	## Lightwork correction@343
			self.InventorySlotTooltipCheck(overSlotPosGlobal)
	## Lightwork correction@343
	
		def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
	
			if item.IsRefineScroll(srcItemVNum):
				return True
			elif item.IsMetin(srcItemVNum):
				return True
			elif item.IsDetachScroll(srcItemVNum):
				return True
			elif item.IsKey(srcItemVNum):
				return True
			elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
				return True
			else:
				if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
					return True
	
			return False
	
		if app.ENABLE_SPECIAL_STORAGE:
			def __SendUseItemToItemPacketAttr(self, srcSlotPos, dstSlotPos):
				if uiPrivateShopBuilder.IsBuildingPrivateShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
					return
						
				net.SendItemUseToItemPacket(player.CHEST_INVENTORY, srcSlotPos, player.INVENTORY, dstSlotPos)
	
	
		def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
	
			if app.ENABLE_SPECIAL_STORAGE:
				if srcSlotPos == dstSlotPos and not item.IsMetin(srcItemVNum):
					return False
			else:
				if srcSlotPos == dstSlotPos:
					return False
	
			if item.IsRefineScroll(srcItemVNum):
				if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
					return True
			if srcItemVNum == player.GetItemIndex(dstSlotPos):
				if player.GetItemCount(dstSlotPos) < 50000:##item max count
					return True
			elif item.IsMetin(srcItemVNum):
				if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
					return True
			elif item.IsDetachScroll(srcItemVNum):
				if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
					return True
			elif item.IsKey(srcItemVNum):
				if player.CanUnlock(srcItemVNum, dstSlotPos):
					return True
	
			elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
				return True
	
			else:
				useType=item.GetUseType(srcItemVNum)
	
				if "USE_CLEAN_SOCKET" == useType:
					if self.__CanCleanBrokenMetinStone(dstSlotPos):
						return True
				elif "USE_CHANGE_ATTRIBUTE" == useType:
					if self.__CanChangeItemAttrList(dstSlotPos):
						return True
				elif "USE_CHANGE_ATTRIBUTE2" == useType:
					if self.__CanChangeItemAttrListCostume(dstSlotPos):
						return True
				elif "USE_ADD_ATTRIBUTE" == useType:
					if self.__CanAddItemAttr(dstSlotPos):
						return True
				elif "USE_ADD_ATTRIBUTE2" == useType:
					if self.__CanAddItemAttr(dstSlotPos):
						return True
				elif "USE_ADD_ACCESSORY_SOCKET" == useType:
					if self.__CanAddAccessorySocket(dstSlotPos):
						return True
				elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
					if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
						return True
				elif "USE_PUT_INTO_BELT_SOCKET" == useType:
					dstItemVNum = player.GetItemIndex(dstSlotPos)
					item.SelectItem(dstItemVNum)
	
					if item.ITEM_TYPE_BELT == item.GetItemType():
						return True
				elif app.ENABLE_USE_COSTUME_ATTR and "USE_CHANGE_COSTUME_ATTR" == useType:
					if self.__CanChangeCostumeAttrList(dstSlotPos):
						return True
				elif app.ENABLE_USE_COSTUME_ATTR and "USE_RESET_COSTUME_ATTR" == useType:
					if self.__CanResetCostumeAttr(dstSlotPos):
						return True
	
				elif app.ENABLE_ATTR_RARE_RENEWAL and useType in ("USE_CHANGE_RARE_ATTRIBUTE","USE_ADD_RARE_ATTRIBUTE"):
					return self.canRareAttr(srcSlotPos, dstSlotPos)
	
			return False
	
		def __CanCleanBrokenMetinStone(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if item.ITEM_TYPE_WEAPON != item.GetItemType():
				return False
	
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
					return True
	
			return False
	
		def __CanChangeItemAttrList(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False
	
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					return True
	
			return False
	
		def __CanChangeItemAttrListCostume(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if item.GetItemType() != item.ITEM_TYPE_COSTUME:
				return False
	
			if not item.GetItemSubType() in (item.COSTUME_TYPE_BODY, item.COSTUME_TYPE_HAIR, item.COSTUME_TYPE_WEAPON):
				return True
	
			return False
	
		if app.ENABLE_USE_COSTUME_ATTR:
			def __CanChangeCostumeAttrList(self, dstSlotPos):
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				if dstItemVNum == 0:
					return False
	
				item.SelectItem(dstItemVNum)
	
				if item.GetItemType() != item.ITEM_TYPE_COSTUME:
					return False
	
				for i in xrange(player.METIN_SOCKET_MAX_NUM):
					if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
						return True
	
				return False
	
			def __CanResetCostumeAttr(self, dstSlotPos):
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				if dstItemVNum == 0:
					return False
	
				item.SelectItem(dstItemVNum)
	
				if item.GetItemType() != item.ITEM_TYPE_COSTUME:
					return False
	
				for i in xrange(player.METIN_SOCKET_MAX_NUM):
					if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
						return True
	
				return False
	
		def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if item.GetItemType() != item.ITEM_TYPE_ARMOR:
				return False
	
			if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				return False
	
			curCount = player.GetItemMetinSocket(dstSlotPos, 0)
			maxCount = player.GetItemMetinSocket(dstSlotPos, 1)
	
			if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
				return False
	
			if curCount>=maxCount:
				return False
	
			return True
	
		def __CanAddAccessorySocket(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if item.GetItemType() != item.ITEM_TYPE_ARMOR:
				return False
	
			if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				return False
	
			curCount = player.GetItemMetinSocket(dstSlotPos, 0)
			maxCount = player.GetItemMetinSocket(dstSlotPos, 1)
	
			ACCESSORY_SOCKET_MAX_SIZE = 3
			if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
				return False
	
			return True
	
		def __CanAddItemAttr(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False
	
			attrCount = 0
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					attrCount += 1
	
			if attrCount<4:
				return True
	
			return False
	
		def ShowToolTip(self, slotIndex):
			itemVnum = player.GetItemIndex(slotIndex)
			if None != self.tooltipItem:
				self.tooltipItem.SetInventoryItem(slotIndex)
	
				if app.ENABLE_RENDER_TARGET:
					self.tooltipItem.AppendRenderingTooltip(itemVnum)
	
				if app.ENABLE_OFFLINE_SHOP:
					if uiOfflineShop.IsBuildingShop():
						self.__AddTooltipSaleMode(slotIndex)
	
		if app.ENABLE_OFFLINE_SHOP:
			def __AddTooltipSaleMode(self, slot):
				if player.IsEquipmentSlot(slot):
					return
	
				itemIndex = player.GetItemIndex(slot)
				if itemIndex !=0:
					item.SelectItem(itemIndex)
					if item.IsAntiFlag(item.ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ANTIFLAG_GIVE):
						return
	
					self.tooltipItem.AddRightClickForSale()
	
		def OnTop(self):
			if None != self.tooltipItem:
				self.tooltipItem.SetTop()
	
			if app.WJ_ENABLE_TRADABLE_ICON:
				map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)
	
		def OnPressEscapeKey(self):
			self.Close()
			return True
	
		def UseItemSlot(self, slotIndex):
			curCursorNum = app.GetCursor()
	
			if self.interface.IsAnyWindowOpen():
				return
	
			globalSlot 	= self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					itemIndex 	= player.GetItemIndex(globalSlot)
					item.SelectItem(itemIndex)
	
					if app.IsPressed(app.DIK_LCONTROL):
						if not item.IsAntiFlag(item.ANTIFLAG_GIVE) and not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
							self.interface.wndShopOffline.SetFastAddItem(True)
							offlineshop.ShopBuilding_AddItem(player.INVENTORY, globalSlot, True) ## lightygrid
						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
						return
					else:
						if not item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
							offlineshop.ShopBuilding_AddItem(player.INVENTORY, globalSlot)
						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
						return
	
			if self.interface and app.IsPressed(app.DIK_LCONTROL) and self.interface.wndSpecialStorage.IsShow():
				if app.GetTime() < self.waitTime:
					chat.AppendChat(1, localeInfo.MINING_EVENT_RENEWAL_HIT_DELAY)
					return
				self.waitTime = app.GetTime() + 0.5
				net.SendChatPacket("/transfer_inv_to_specialinventory %d" % (globalSlot))
				return
	
			if self.attachMetinDialog.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return
	
			if app.SELL == curCursorNum:
				return
	
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
				return
	
			slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
	
			if app.ENABLE_FAST_SKILL_BOOK_SYSTEM:
				itemVNum = player.GetItemIndex(slotIndex)
				if constInfo.IsFastReadItem(itemVNum) and not self.interface.dlgExchange.IsShow():
					openPage = constInfo.GetFastReadItemPage(itemVNum)
					self.interface.OpenReadBookWindowPage(openPage)
					return
	
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
					return
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if self.isShowAcceWindow():
					acce.Add(player.INVENTORY, slotIndex, 255)
					return
			if app.ENABLE_AURA_SYSTEM:
				itemVNum = player.GetItemIndex(slotIndex)
				if self.isShowAuraWindow():
					aura.Add(player.INVENTORY, slotIndex, 255)
					return
	
			if app.ENABLE_CHECKINOUT_UPDATE:
				if exchange.isTrading() and slotIndex < player.EQUIPMENT_SLOT_START:
					net.SendExchangeItemAddPacket(player.INVENTORY, slotIndex, -1)
					return
	
			if app.ENABLE_NEW_PET_SYSTEM:
				getItemVnum = player.GetItemIndex(slotIndex)
				if constInfo.IS_NEW_PET_USABLE_ITEM(getItemVnum):
					net.SendChatPacket("/feedpetitem %d" % (slotIndex))
					return
	
			if app.ENABLE_NAMING_SCROLL:
				getItemVnum = player.GetItemIndex(slotIndex)
				if constInfo.IS_NAMING_SCROLL(getItemVnum):
					changeNameDialog = uiCommon.ChangeNameDialog(getItemVnum, slotIndex)
					changeNameDialog.Show()
	
			self.__UseItem(slotIndex)
			mouseModule.mouseController.DeattachObject()
			self.OverOutItem()
	
		if app.ENABLE_CHECKINOUT_UPDATE:
			def __GetCurrentItemGrid(self):
				itemGrid = [[False for slot in xrange(player.INVENTORY_PAGE_SIZE)] for page in xrange(player.INVENTORY_PAGE_COUNT)]
	
				for page in xrange(player.INVENTORY_PAGE_COUNT):
					for slot in xrange(player.INVENTORY_PAGE_SIZE):
						itemVnum = player.GetItemIndex(slot + page * player.INVENTORY_PAGE_SIZE)
						if itemVnum <> 0:
							(w, h) = item.GetItemSize(item.SelectItem(itemVnum))
							for i in xrange(h):
								itemGrid[page][slot + i * 5] = True
	
				return itemGrid
	
			def __FindEmptyCellForSize(self, itemGrid, size):
				for page in xrange(player.INVENTORY_PAGE_COUNT):
					for slot in xrange(player.INVENTORY_PAGE_SIZE):
						if itemGrid[page][slot] == False:
							possible = True
							for i in xrange(size):
								p = slot + (i * 5)
	
								try:
									if itemGrid[page][p] == True:
										possible = False
										break
								except IndexError:
									possible = False
									break
	
							if possible:
								return slot + page * player.INVENTORY_PAGE_SIZE
	
				return -1
	
			def AttachItemFromSafebox(self, slotIndex, itemIndex):
				itemGrid = self.__GetCurrentItemGrid()
	
				if item.GetItemType(item.SelectItem(itemIndex)) == item.ITEM_TYPE_DS:
					return
	
				emptySlotIndex = self.__FindEmptyCellForSize(itemGrid, item.GetItemSize()[1])
				if emptySlotIndex <> -1:
					net.SendSafeboxCheckoutPacket(slotIndex, player.INVENTORY, emptySlotIndex)
	
				return True
	
		def __UseItem(self, slotIndex):
			if app.ENABLE_OFFLINE_SHOP and uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.INVENTORY, slotIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
				return
		
			if app.ENABLE_CHECKINOUT_UPDATE:
				if self.interface and self.interface.AttachInvenItemToOtherWindowSlot(player.INVENTORY, slotIndex):#slotIndex is the argument of __UseItem
					return
		
			ItemVNum = player.GetItemIndex(slotIndex)
			item.SelectItem(ItemVNum)
	
			if constInfo.CONFIRM_BEFORE_USE_ITEMLIST(ItemVNum):
				self.questionDialog = uiCommon.QuestionDialog()
	
				if slotIndex == item.EQUIPMENT_UNIQUE1 or slotIndex == item.EQUIPMENT_UNIQUE2:
					self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM3)
				else:
					self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM2)
		
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
				self.questionDialog.Open()
				self.questionDialog.slotIndex = slotIndex
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
	
			elif app.IsPressed(app.DIK_LALT):
				# if str(background.GetCurrentMapName()) in constInfo.chestCheckMaps:
				# 	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.YOU_CANNOT_OPEN_CHEST_IN_CITY)
				# 	return
				net.SendItemUsePacket(player.INVENTORY, slotIndex, constInfo.CHEST_OPEN_COUNT)
				return
	
	
			else:
				self.__SendUseItemPacket(slotIndex)
	
		def __UseItemQuestionDialog_OnCancel(self):
			self.OnCloseQuestionDialog()
	
		def __UseItemQuestionDialog_OnAccept(self):
			self.__SendUseItemPacket(self.questionDialog.slotIndex)
			self.OnCloseQuestionDialog()
	
		def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
	
			net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)
	
		def __SendUseItemPacket(self, slotPos):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
	
			net.SendItemUsePacket(slotPos)
	
		def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
				return
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
	
			if app.ENABLE_ITEM_TRANSACTIONS:
				if self.interface.wndItemTransactions.IsItemInList():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
					return
	
			net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)
	
		def __SendMoveItemPacketSpecial(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
				return
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
	
			if app.ENABLE_ITEM_TRANSACTIONS:
				if self.interface.wndItemTransactions.IsItemInList():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
					return
	
			net.SendItemMovePacket(srcSlotWindow , srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)
	
		def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				self.wndDragonSoulRefine = wndDragonSoulRefine
	
		def OnMoveWindow(self, x, y):
			if extraInfo.ENABLE_INVENTORY_SIDEBAR:
				if self._inventorySidebar_:
					self._inventorySidebar_.Reposition(x, y)
			else:
				pass
	
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			def SetAcceWindow(self, wndAcceCombine, wndAcceAbsorption):
				self.wndAcceCombine = wndAcceCombine
				self.wndAcceAbsorption = wndAcceAbsorption
	
			def isShowAcceWindow(self):
				if self.wndAcceCombine:
					if self.wndAcceCombine.IsShow():
						return 1
				if self.wndAcceAbsorption:
					if self.wndAcceAbsorption.IsShow():
						return 1
				return 0
	
		if app.ENABLE_DROP_DIALOG_EXTENDED_SYSTEM:
			def DeleteItem(self, slotPos, invenType):
				if player.IsEquipmentSlot(slotPos):
					return
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
				itemQuestionDialog2.SetAcceptEvent(lambda arg=1: self.__AnswerDeleteItem(arg))
				itemQuestionDialog2.SetDestroyEvent(lambda arg=0: self.__AnswerDeleteItem(arg))
				itemQuestionDialog2.SetCancelEvent(lambda arg=2: self.__AnswerDeleteItem(arg))
				itemQuestionDialog2.slotPos = slotPos
				itemQuestionDialog2.invenType = invenType
				itemQuestionDialog2.Open(itemIndex, slotPos, "", invenType)
				self.itemQuestionDialog2 = itemQuestionDialog2
	
			def __AnswerDeleteItem(self, answer):
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
	
		if app.WJ_ENABLE_TRADABLE_ICON:
			def MouseSlotEventRefresh(self):
				for i in xrange(self.wndItem.GetSlotCount()):
					slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
					if slotNumber in self.listCantMouseSlot:
						itemInvenPage = slotNumber / player.INVENTORY_PAGE_SIZE
						localSlotPos = slotNumber - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
	
						self.wndItem.SetCantMouseEventSlot(localSlotPos)
						self.wndItem.RefreshSlot()
	
			def MouseSlotEventClear(self):
				for i in xrange(self.wndItem.GetSlotCount()):
					slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
					if slotNumber in self.listCantMouseSlot:
						self.wndItem.SetCanMouseEventSlot(i)
						self.listCantMouseSlot.remove(slotNumber)
	
			def SetCantMouseSlot(self, slot):
				if slot > player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT:
					return
	
				if not slot in self.listCantMouseSlot:
					self.listCantMouseSlot.append(slot)
	
			def SetCanMouseSlot(self, inventorylocalslot):
				if inventorylocalslot in self.listCantMouseSlot:
					if inventorylocalslot >= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
						self.wndItem.SetCanMouseEventSlot(inventorylocalslot-player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex)
					else:
						self.wndItem.SetCanMouseEventSlot(inventorylocalslot)
	
					self.listCantMouseSlot.remove(inventorylocalslot)
	
		def OnRunMouseWheel(self, nLen):
			if nLen > 0:
	
				if self.wndEquip.IsIn() or self.wndCostume.IsIn() or self.wndBoosters.IsIn():
					if self.equipmentPageIndex > 0:
						self.SetEquipmentPage(self.equipmentPageIndex - 1)
	
				elif self.wndItem.IsIn():
					if self.inventoryPageIndex > 0:
						self.SetInventoryPage(self.inventoryPageIndex - 1)
	
			else:
	
				if self.wndEquip.IsIn() or self.wndCostume.IsIn() or self.wndBoosters.IsIn():
					if self.equipmentPageIndex < 2:
						self.SetEquipmentPage(self.equipmentPageIndex + 1)
	
				elif self.wndItem.IsIn():
					if self.inventoryPageIndex < (player.INVENTORY_PAGE_COUNT - 1):
						self.SetInventoryPage(self.inventoryPageIndex + 1)
	
	
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			def RefreshVisibleCostume(self):
				hair, body, weapon, acce, aura, crown = player.GetHiddenCostumeState()
	
				if hair == 1:
					self.visibleButtonList[0].Down()
				else:
					self.visibleButtonList[0].SetUp()
	
				if body == 1:
					self.visibleButtonList[1].Down()
				else:
					self.visibleButtonList[1].SetUp()
	
				if weapon == 1:
					self.visibleButtonList[2].Down()
				else:
					self.visibleButtonList[2].SetUp()
	
				if acce == 1:
					self.visibleButtonList[3].Down()
				else:
					self.visibleButtonList[3].SetUp()
	
				if aura == 1:
					self.visibleButtonList[4].Down()
				else:
					self.visibleButtonList[4].SetUp()
	
				if crown == 1:
					self.visibleButtonList[5].Down()
				else:
					self.visibleButtonList[5].SetUp()
	
			def VisibleCostume(self, part, hidden):
				if not player.CanInteract():
					chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.TEXTTAIL_CANT_INTERACT)
					self.visibleButtonList[part-1].SetUp() if hidden == 1 else self.visibleButtonList[part-1].Down()
					return
	
				net.SendChatPacket("/set_char_settings %d %d" % (part, hidden))
	
		if app.ENABLE_AURA_SYSTEM:
			def SetAuraWindow(self, wndAuraAbsorption, wndAuraRefine):
				self.wndAuraRefine = wndAuraRefine
				self.wndAuraAbsorption = wndAuraAbsorption
	
			def isShowAuraWindow(self):
				if self.wndAuraRefine:
					if self.wndAuraRefine.IsShow():
						return 1
	
				if self.wndAuraAbsorption:
					if self.wndAuraAbsorption.IsShow():
						return 1
	
				return 0
	
		if app.ENABLE_ATTR_RARE_RENEWAL:
			def canRareAttr(self, srcSlotPos, dstSlotPos):
				srcItemVNum = player.GetItemIndex(dstSlotPos)
				item.SelectItem(srcItemVNum)
				rareAttrValue = item.GetValue(5)
	
				dstItemVNum = player.GetItemIndex(dstSlotPos)
	
				if rareAttrValue == 0:
					return self.IsSkinItem(dstItemVNum)
	
				return False
	
			def IsSkinItem(self, dstItemVNum):
				item.SelectItem(dstItemVNum)
	
				if item.GetItemType() in [item.ITEM_PET_SKIN, item.ITEM_MOUNT_SKIN]:
					return True
	
				return False
	
		def ActivateAllAffectItems(self):
	
			activeList = list()
			notActiveList = list()
	
			for slotNumber in xrange((player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT)):
	
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				isActivated = metinSocket[3]
	
				getItemVNum=player.GetItemIndex
	
				itemVnum = getItemVNum(slotNumber)
	
				if itemVnum in blend_table.BLEND_BASE_TIME:
					if isActivated:
						activeList.append(slotNumber)
					else:
						notActiveList.append(slotNumber)
	
			if len(activeList) >= len(notActiveList):
				for i in activeList:
					self.__UseItem(i)
			else:
				if not activeList:
					for i in notActiveList:
						self.__UseItem(i)
				else:
					if notActiveList:
						for i in notActiveList:
							self.__UseItem(i)
					else:
						for i in activeList:
							self.__UseItem(i)
else:
	old_open = open
	import ui
	import player
	import mouseModule
	import net
	import app
	import snd
	import item
	import player
	import chat
	import grp
	import uiScriptLocale
	import uiRefine
	import uiAttachMetin
	import uiPickMoney
	import uiCommon
	import uiPrivateShopBuilder
	import localeInfo
	import constInfo
	import ime
	import wndMgr
	import dbg
	
	if app.ENABLE_CHEQUE_SYSTEM:
		import uiToolTip
		import uiPickETC
	
	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		import acce
	from _weakref import proxy
	
	ITEM_MALL_BUTTON_ENABLE = True
	
	ITEM_FLAG_APPLICABLE = 1 << 14
	
	class CostumeWindow(ui.ScriptWindow):
	
		def __init__(self, wndInventory):
			import exception
	
			if not app.ENABLE_COSTUME_SYSTEM:
				exception.Abort("What do you do?")
				return
	
			if not wndInventory:
				exception.Abort("wndInventory parameter must be set to InventoryWindow")
				return
	
			ui.ScriptWindow.__init__(self)
	
			self.isLoaded = 0
			self.wndInventory = wndInventory;
	
			self.__LoadWindow()
	
		def __del__(self):
			ui.ScriptWindow.__del__(self)
	
		@ui.WindowDestroy
		def Destroy(self):
			self.ClearDictionary()
			self.wndInventory = None
	
		def Show(self):
			self.__LoadWindow()
			self.RefreshCostumeSlot()
	
			ui.ScriptWindow.Show(self)
	
		def Close(self):
			self.Hide()
	
		def __LoadWindow(self):
			if self.isLoaded == 1:
				return
	
			self.isLoaded = 1
	
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
			except:
				import exception
				exception.Abort("CostumeWindow.LoadWindow.LoadObject")
	
			try:
				wndEquip = self.GetChild("CostumeSlot")
				self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
	
			except:
				import exception
				exception.Abort("CostumeWindow.LoadWindow.BindObject")
	
			## Equipment
			wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
			wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
			wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
			wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
			wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
			wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))
	
			self.wndEquip = wndEquip
	
		def RefreshCostumeSlot(self):
			getItemVNum=player.GetItemIndex
	
			for i in xrange(item.COSTUME_SLOT_COUNT):
				slotNumber = item.COSTUME_SLOT_START + i
				self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)
	
			if app.ENABLE_WEAPON_COSTUME_SYSTEM:
				self.wndEquip.SetItemSlot(item.COSTUME_SLOT_WEAPON, getItemVNum(item.COSTUME_SLOT_WEAPON), 0)
	
			self.wndEquip.RefreshSlot()
	
	class BeltInventoryWindow(ui.ScriptWindow):
	
		def __init__(self, wndInventory):
			import exception
	
			if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:
				exception.Abort("What do you do?")
				return
	
			if not wndInventory:
				exception.Abort("wndInventory parameter must be set to InventoryWindow")
				return
	
			ui.ScriptWindow.__init__(self)
	
			self.isLoaded = 0
			self.wndInventory = wndInventory
	
			self.wndBeltInventoryLayer = None
			self.wndBeltInventorySlot = None
			self.expandBtn = None
			self.minBtn = None
	
			self.__LoadWindow()
	
		def __del__(self):
			ui.ScriptWindow.__del__(self)
	
		@ui.WindowDestroy
		def Destroy(self):
			self.wndInventory = None
	
		def Show(self, openBeltSlot = False):
			self.__LoadWindow()
			self.RefreshSlot()
	
			ui.ScriptWindow.Show(self)
	
			if openBeltSlot:
				self.OpenInventory()
			else:
				self.CloseInventory()
	
		def Close(self):
			self.Hide()
	
		def IsOpeningInventory(self):
			if self.wndBeltInventoryLayer:
				return self.wndBeltInventoryLayer.IsShow()
			return False
	
		def OpenInventory(self):
			self.wndBeltInventoryLayer.Show()
			self.expandBtn.Hide()
	
			if localeInfo.IsARABIC() == 0:
				self.AdjustPositionAndSize()
	
		def CloseInventory(self):
			self.wndBeltInventoryLayer.Hide()
			self.expandBtn.Show()
	
			if localeInfo.IsARABIC() == 0:
				self.AdjustPositionAndSize()
	
		def GetBasePosition(self):
			x, y = self.wndInventory.GetGlobalPosition()
			return x - 148, y + 241
	
		def AdjustPositionAndSize(self):
			bx, by = self.GetBasePosition()
	
			if self.IsOpeningInventory():
				self.SetPosition(bx, by)
				self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())
	
			else:
				self.SetPosition(bx + 138, by);
				self.SetSize(10, self.GetHeight())
	
		def __LoadWindow(self):
			if self.isLoaded == 1:
				return
	
			self.isLoaded = 1
	
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
			except:
				import exception
				exception.Abort("CostumeWindow.LoadWindow.LoadObject")
	
			try:
				self.ORIGINAL_WIDTH = self.GetWidth()
				wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
				self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
				self.expandBtn = self.GetChild("ExpandBtn")
				self.minBtn = self.GetChild("MinimizeBtn")
	
				self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
				self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))
	
				if localeInfo.IsARABIC() :
					self.expandBtn.SetPosition(self.expandBtn.GetWidth() - 2, 15)
					self.wndBeltInventoryLayer.SetPosition(self.wndBeltInventoryLayer.GetWidth() - 5, 0)
					self.minBtn.SetPosition(self.minBtn.GetWidth() + 3, 15)
	
				for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
					slotNumber = item.BELT_INVENTORY_SLOT_START + i
					wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
													"d:/ymir work/ui/game/quest/slot_button_01.sub",\
													"d:/ymir work/ui/game/quest/slot_button_01.sub",\
													"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)
	
			except:
				import exception
				exception.Abort("CostumeWindow.LoadWindow.BindObject")
	
			## Equipment
			wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
			wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
			wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
			wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
			wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
			wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))
	
			self.wndBeltInventorySlot = wndBeltInventorySlot
	
		def RefreshSlot(self):
			getItemVNum=player.GetItemIndex
	
			for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), player.GetItemCount(slotNumber))
				self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)
	
				avail = "0"
	
				if player.IsAvailableBeltInventoryCell(slotNumber):
					self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
				else:
					self.wndBeltInventorySlot.DisableCoverButton(slotNumber)
	
			self.wndBeltInventorySlot.RefreshSlot()
	
	
	class InventoryWindow(ui.ScriptWindow):
	
		USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET")
		if app.ENABLE_USE_COSTUME_ATTR:
			USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR"])
	
		questionDialog = None
		tooltipItem = None
		wndCostume = None
		wndBelt = None
		dlgPickMoney = None
		if app.ENABLE_CHEQUE_SYSTEM:
			dlgPickETC = None
	
		sellingSlotNumber = -1
		isLoaded = 0
		isOpenedCostumeWindowWhenClosingInventory = 0
		isOpenedBeltWindowWhenClosingInventory = 0
	
		if app.ENABLE_HIGHLIGHT_NEW_ITEM:
			liHighlightedItems = []
	
		def __init__(self):
			ui.ScriptWindow.__init__(self)
	
			self.isOpenedBeltWindowWhenClosingInventory = 0
	
			self.inventoryPageIndex = 0
	
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.wndAcceCombine = None
				self.wndAcceAbsorption = None
	
			self.__LoadWindow()
	
		def __del__(self):
			ui.ScriptWindow.__del__(self)
	
		def Show(self):
			self.__LoadWindow()
	
			ui.ScriptWindow.Show(self)
	
			if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
				self.wndCostume.Show()
	
			if self.wndBelt:
				self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)
	
		def BindInterfaceClass(self, interface):
			self.interface = interface
			if app.ENABLE_WON_EXCHANGE_WINDOW and self.interface and self.wndChequeSlot:
				self.wndChequeSlot.SetEvent(ui.__mem_func__(self.interface.ToggleWonExchangeWindow))
	
		def __LoadWindow(self):
			if self.isLoaded == 1:
				return
	
			self.isLoaded = 1
	
			try:
				pyScrLoader = ui.PythonScriptLoader()
	
				if app.ENABLE_EXTEND_INVEN_SYSTEM:
					if not localeInfo.IsARABIC():
						pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindowEx.py")
					else:
						pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "InventoryWindow.py")
				else:
					pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
			except:
				import exception
				exception.Abort("InventoryWindow.LoadWindow.LoadObject")
	
			try:
				wndItem = self.GetChild("ItemSlot")
				wndEquip = self.GetChild("EquipmentSlot")
				self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
				self.wndMoney = self.GetChild("Money")
				self.wndMoneySlot = self.GetChild("Money_Slot")
				self.mallButton = self.GetChild2("MallButton")
				self.DSSButton = self.GetChild2("DSSButton")
				self.costumeButton = self.GetChild2("CostumeButton")
	
				if app.ENABLE_CHEQUE_SYSTEM:
					self.wndCheque = self.GetChild("Cheque")
					self.wndChequeSlot = self.GetChild("Cheque_Slot")
	
					self.wndMoneyIcon = self.GetChild("Money_Icon")
					self.wndChequeIcon = self.GetChild("Cheque_Icon")
	
					self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
					self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 1)
	
					self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
					self.wndChequeIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 1)
	
					self.toolTip = uiToolTip.ToolTip()
					self.toolTip.ClearToolTip()
	
	
				self.inventoryTab = []
				for i in xrange(player.INVENTORY_PAGE_COUNT):
					self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))
	
				self.equipmentTab = []
				self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
				self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))
	
				if self.costumeButton and not app.ENABLE_COSTUME_SYSTEM:
					self.costumeButton.Hide()
					self.costumeButton.Destroy()
					self.costumeButton = 0
	
				# Belt Inventory Window
				self.wndBelt = None
	
				if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
					self.wndBelt = BeltInventoryWindow(self)
	
			except:
				import exception
				exception.Abort("InventoryWindow.LoadWindow.BindObject")
	
			## Item
			wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
			wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
			wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
			wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
	
			## Equipment
			wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
			wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
			wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
			wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
	
			## PickMoneyDialog
			dlgPickMoney = uiPickMoney.PickMoneyDialog()
			dlgPickMoney.LoadDialog()
			dlgPickMoney.Hide()
	
			## PickETCDialog
			if app.ENABLE_CHEQUE_SYSTEM:
				dlgPickETC = uiPickETC.PickETCDialog()
				dlgPickETC.LoadDialog()
				dlgPickETC.Hide()
	
			## RefineDialog
			self.refineDialog = uiRefine.RefineDialog()
			self.refineDialog.Hide()
	
			## AttachMetinDialog
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
			self.attachMetinDialog.Hide()
	
			## MoneySlot
			if app.ENABLE_CHEQUE_SYSTEM:
				self.wndChequeSlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 1)
				self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 0)
			else:
				self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))
	
			for i in xrange(player.INVENTORY_PAGE_COUNT):
				self.inventoryTab[i].SAFE_SetEvent(self.SetInventoryPage, i)
			self.inventoryTab[0].Down()
	
			self.equipmentTab[0].SAFE_SetEvent(self.SetEquipmentPage, 0)
			self.equipmentTab[1].SAFE_SetEvent(self.SetEquipmentPage, 1)
			self.equipmentTab[0].Down()
			self.equipmentTab[0].Hide()
			self.equipmentTab[1].Hide()
	
			self.wndItem = wndItem
			self.wndEquip = wndEquip
			self.dlgPickMoney = dlgPickMoney
	
			if app.ENABLE_CHEQUE_SYSTEM:
				self.dlgPickETC = dlgPickETC
	
			# MallButton
			if self.mallButton:
				self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))
	
			if self.DSSButton:
				self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))
	
			# Costume Button
			if self.costumeButton:
				self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))
	
			self.wndCostume = None
	
	 		#####
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.listAttachedAcces = []
	
			## Refresh
			self.SetInventoryPage(0)
			self.SetEquipmentPage(0)
			self.RefreshItemSlot()
			self.RefreshStatus()
	
		@ui.WindowDestroy
		def Destroy(self):
			self.ClearDictionary()
	
			if self.dlgPickMoney:
				self.dlgPickMoney.Destroy()
				self.dlgPickMoney = 0
	
			if self.refineDialog:
				self.refineDialog.Destroy()
				self.refineDialog = 0
	
			if app.ENABLE_CHEQUE_SYSTEM and self.dlgPickETC:
				self.dlgPickETC.Destroy()
				self.dlgPickETC = 0
	
			if self.attachMetinDialog:
				self.attachMetinDialog.Destroy()
				self.attachMetinDialog = 0
	
			self.tooltipItem = None
			self.wndItem = 0
			self.wndEquip = 0
			self.dlgPickMoney = 0
			self.wndMoney = 0
			self.wndMoneySlot = 0
			if app.ENABLE_CHEQUE_SYSTEM:
				self.wndCheque = 0
				self.wndChequeSlot = 0
				self.dlgPickETC = 0
			self.questionDialog = None
			self.mallButton = None
			self.DSSButton = None
			self.costumeButton = None
			self.wndDragonSoulRefine = None
			self.interface = None
	
			if self.wndCostume:
				self.wndCostume.Destroy()
				self.wndCostume = None
	
			if self.wndBelt:
				self.wndBelt.Destroy()
				self.wndBelt = None
	
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.wndAcceCombine = None
				self.wndAcceAbsorption = None
	
			self.inventoryTab = []
			self.equipmentTab = []
	
		def Hide(self):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
				self.OnCloseQuestionDialog()
				return
			if None != self.tooltipItem:
				self.tooltipItem.HideToolTip()
	
			if self.wndCostume:
				self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
				self.wndCostume.Close()
	
			if self.wndBelt:
				self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()
				print "Is Opening Belt Inven?? ", self.isOpenedBeltWindowWhenClosingInventory
				self.wndBelt.Close()
	
			if self.dlgPickMoney:
				self.dlgPickMoney.Close()
	
			if app.ENABLE_CHEQUE_SYSTEM:
				if self.dlgPickETC:
					self.dlgPickETC.Close()
	
			wndMgr.Hide(self.hWnd)
	
	
		def Close(self):
			self.Hide()
	
		def SetInventoryPage(self, page):
			self.inventoryPageIndex = page
			for i in xrange(player.INVENTORY_PAGE_COUNT):
				if i!=page:
					self.inventoryTab[i].SetUp()
			self.RefreshBagSlotWindow()
	
		def SetEquipmentPage(self, page):
			self.equipmentPageIndex = page
			self.equipmentTab[1-page].SetUp()
			self.RefreshEquipSlotWindow()
	
		def ClickMallButton(self):
			print "click_mall_button"
			net.SendChatPacket("/click_mall")
	
		# DSSButton
		def ClickDSSButton(self):
			print "click_dss_button"
			self.interface.ToggleDragonSoulWindow()
	
		def ClickCostumeButton(self):
			print "Click Costume Button"
			if self.wndCostume:
				if self.wndCostume.IsShow():
					self.wndCostume.Hide()
				else:
					self.wndCostume.Show()
			else:
				self.wndCostume = CostumeWindow(self)
				self.wndCostume.Show()
	
		def OpenPickMoneyDialog(self, focus_idx = 0):
			if mouseModule.mouseController.isAttached():
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():
					if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
						net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
						snd.PlaySound("sound/ui/money.wav")
	
				mouseModule.mouseController.DeattachObject()
	
			else:
				curMoney = player.GetElk()
				if app.ENABLE_CHEQUE_SYSTEM:
					curCheque = player.GetCheque()
					if curMoney <= 0 and curCheque <= 0:
						return
				else:
					curCheque = 1 # default money value
					if curMoney <= 0:
						return
	
				self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
				self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
				self.dlgPickMoney.Open(curMoney, curCheque)
				self.dlgPickMoney.SetMax(9)
				if app.ENABLE_CHEQUE_SYSTEM:
					self.dlgPickMoney.SetMaxCheque(3)
					self.dlgPickMoney.SetFocus(focus_idx)
	
		def OnPickMoney(self, money, cheque=0):
			mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money, cheque)
	
		def OnPickItem(self, count):
			if app.ENABLE_CHEQUE_SYSTEM:
				itemSlotIndex = self.dlgPickETC.itemGlobalSlotIndex
			else:
				itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
			selectedItemVNum = player.GetItemIndex(itemSlotIndex)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)
	
		def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
			if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
				return local
	
			return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local
	
		def RefreshBagSlotWindow(self):
			getItemVNum=player.GetItemIndex
			getItemCount=player.GetItemCount
			setItemVNum=self.wndItem.SetItemSlot
	
			for i in xrange(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
	
				itemCount = getItemCount(slotNumber)
				if 0 == itemCount:
					self.wndItem.ClearSlot(i)
					continue
				elif 1 == itemCount:
					itemCount = 0
	
				itemVnum = getItemVNum(slotNumber)
				setItemVNum(i, itemVnum, itemCount)
	
				if constInfo.IS_AUTO_POTION(itemVnum):
					metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
	
					isActivated = 0 != metinSocket[0]
	
					if isActivated:
						self.wndItem.ActivateSlot(i)
						potionType = 0
						if constInfo.IS_AUTO_POTION_HP(itemVnum):
							potionType = player.AUTO_POTION_TYPE_HP
						elif constInfo.IS_AUTO_POTION_SP(itemVnum):
							potionType = player.AUTO_POTION_TYPE_SP
	
						usedAmount = int(metinSocket[1])
						totalAmount = int(metinSocket[2])
						player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))
	
					else:
						self.wndItem.DeactivateSlot(i)
	
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					slotNumberChecked = 0
					if not constInfo.IS_AUTO_POTION(itemVnum):
						if app.ENABLE_HIGHLIGHT_NEW_ITEM:
							if not slotNumber in self.liHighlightedItems:
								self.wndItem.DeactivateSlot(i)
						else:
							self.wndItem.DeactivateSlot(i)
	
					for j in xrange(acce.WINDOW_MAX_MATERIALS):
						(isHere, iCell) = acce.GetAttachedItem(j)
						if isHere:
							if iCell == slotNumber:
								self.wndItem.ActivateSlot(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
								if not slotNumber in self.listAttachedAcces:
									self.listAttachedAcces.append(slotNumber)
	
								slotNumberChecked = 1
						else:
							if slotNumber in self.listAttachedAcces and not slotNumberChecked:
								self.wndItem.DeactivateSlot(i)
								self.listAttachedAcces.remove(slotNumber)
	
				elif app.ENABLE_HIGHLIGHT_NEW_ITEM and not constInfo.IS_AUTO_POTION(itemVnum):
					if not slotNumber in self.liHighlightedItems:
						self.wndItem.DeactivateSlot(i)
	
				if constInfo.ENABLE_ACTIVE_PET_SEAL_EFFECT and constInfo.IS_PET_SEAL(itemVnum):
					metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
					isActivated = 0 != metinSocket[2]
					if isActivated:
						self.wndItem.ActivateSlot(i)
					else:
						self.wndItem.DeactivateSlot(i)
	
			self.wndItem.RefreshSlot()
			if app.ENABLE_HIGHLIGHT_NEW_ITEM:
				self.__RefreshHighlights()
	
			if self.wndBelt:
				self.wndBelt.RefreshSlot()
	
	
	
	
		if app.ENABLE_HIGHLIGHT_NEW_ITEM:
			def HighlightSlot(self, slot):
				if not slot in self.liHighlightedItems:
					self.liHighlightedItems.append(slot)
	
			def __RefreshHighlights(self):
				for i in xrange(player.INVENTORY_PAGE_SIZE):
					slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
					if slotNumber in self.liHighlightedItems:
						self.wndItem.ActivateSlot(i)
	
	
		def SetItemSlotVnum(self, slotNumber):
			getItemVNum=player.GetItemIndex
			getItemCount=player.GetItemCount
			setItemVNum=self.wndEquip.SetItemSlot
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
			return
	
		def RefreshEquipSlotWindow(self):
			SetItemSlotVnum = self.SetItemSlotVnum
			for i in xrange(player.EQUIPMENT_PAGE_COUNT):
				SetItemSlotVnum(player.EQUIPMENT_SLOT_START + i)
	
			if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
				SetItemSlotVnum(item.EQUIPMENT_BELT)
			if app.ENABLE_PENDANT_SYSTEM:
				SetItemSlotVnum(item.EQUIPMENT_PENDANT)
			if app.ENABLE_GLOVE_SYSTEM:
				SetItemSlotVnum(item.EQUIPMENT_GLOVE)
	
			self.wndEquip.RefreshSlot()
	
			if self.wndCostume:
				self.wndCostume.RefreshCostumeSlot()
	
		def RefreshItemSlot(self):
			self.RefreshBagSlotWindow()
			self.RefreshEquipSlotWindow()
	
		def RefreshStatus(self):
			money = player.GetElk()
			self.wndMoney.SetText(localeInfo.NumberToString(money) if app.ENABLE_CHEQUE_SYSTEM else localeInfo.NumberToMoneyString(money))
			if app.ENABLE_CHEQUE_SYSTEM:
				cheque = player.GetCheque()
				self.wndCheque.SetText(localeInfo.NumberToGoldNotText(cheque))
	
		def SetItemToolTip(self, tooltipItem):
			self.tooltipItem = tooltipItem
	
		def SellItem(self):
			if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
				if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
					net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
					snd.PlaySound("sound/ui/money.wav")
			self.OnCloseQuestionDialog()
	
		def OnDetachMetinFromItem(self):
			if None == self.questionDialog:
				return
	
			#net.SendItemUseToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
			self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
			self.OnCloseQuestionDialog()
	
		def OnCloseQuestionDialog(self):
			if not self.questionDialog:
				return
	
			self.questionDialog.Close()
			self.questionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
	
		## Slot Event
		def SelectEmptySlot(self, selectedSlotPos):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return
	
			selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)
	
			if mouseModule.mouseController.isAttached():
	
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
				attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
	
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					#@fixme011 BEGIN (block ds equip)
					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
					if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
						mouseModule.mouseController.DeattachObject()
						return
					#@fixme011 END
	
					itemCount = player.GetItemCount(attachedSlotPos)
					attachedCount = mouseModule.mouseController.GetAttachedItemCount()
					self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)
	
					if item.IsRefineScroll(attachedItemIndex):
						self.wndItem.SetUseMode(False)
	
				elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
					mouseModule.mouseController.RunCallBack("INVENTORY")
	
				elif player.SLOT_TYPE_SHOP == attachedSlotType:
					net.SendShopBuyPacket(attachedSlotPos)
	
				elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
	
					if player.ITEM_MONEY == attachedItemIndex:
						net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
						snd.PlaySound("sound/ui/money.wav")
	
					else:
						net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)
	
				elif player.SLOT_TYPE_MALL == attachedSlotType:
					net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)
	
				mouseModule.mouseController.DeattachObject()
	
		def SelectItemSlot(self, itemSlotIndex):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return
	
			itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)
	
			if mouseModule.mouseController.isAttached():
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
	
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					#@fixme011 BEGIN (block ds equip)
					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
					if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
						mouseModule.mouseController.DeattachObject()
						return
					#@fixme011 END
					self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)
	
				mouseModule.mouseController.DeattachObject()
	
			else:
	
				curCursorNum = app.GetCursor()
				if app.SELL == curCursorNum:
					self.__SellItem(itemSlotIndex)
	
				elif app.BUY == curCursorNum:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
	
				elif app.IsPressed(app.DIK_LALT):
					link = player.GetItemLink(itemSlotIndex)
					ime.PasteString(link)
	
				elif app.IsPressed(app.DIK_LSHIFT):
					itemCount = player.GetItemCount(itemSlotIndex)
	
					if app.ENABLE_CHEQUE_SYSTEM:
						if itemCount > 1:
							self.dlgPickETC.SetTitleName(localeInfo.PICK_ITEM_TITLE)
							self.dlgPickETC.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
							self.dlgPickETC.Open(itemCount)
							self.dlgPickETC.itemGlobalSlotIndex = itemSlotIndex
					else:
						if itemCount > 1:
							self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
							self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
							self.dlgPickMoney.Open(itemCount)
							self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
					#else:
						#selectedItemVNum = player.GetItemIndex(itemSlotIndex)
						#mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum)
	
				elif app.IsPressed(app.DIK_LCONTROL):
					itemIndex = player.GetItemIndex(itemSlotIndex)
	
					if True == item.CanAddToQuickSlotItem(itemIndex):
						player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)
	
				else:
					selectedItemVNum = player.GetItemIndex(itemSlotIndex)
					itemCount = player.GetItemCount(itemSlotIndex)
					mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
	
					if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
						self.wndItem.SetUseMode(True)
					else:
						self.wndItem.SetUseMode(False)
	
					snd.PlaySound("sound/ui/pick.wav")
	
		if app.ENABLE_CHEQUE_SYSTEM:
			def OverInToolTip(self, arg):
				arglen = len(str(arg))
				pos_x, pos_y = wndMgr.GetMousePosition()
	
				self.toolTip.ClearToolTip()
				self.toolTip.SetThinBoardSize(11 * arglen)
				self.toolTip.SetToolTipPosition(pos_x + 5, pos_y - 5)
				self.toolTip.AppendTextLine(arg, 0xffffff00)
				self.toolTip.Show()
	
			def OverOutToolTip(self):
				self.toolTip.Hide()
	
			def EventProgress(self, event_type, idx):
				if "mouse_over_in" == str(event_type):
					if idx == 0 :
						self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_YANG)
					elif idx == 1 :
						self.OverInToolTip(localeInfo.CHEQUE_SYSTEM_UNIT_WON)
					else:
						return
				elif "mouse_over_out" == str(event_type) :
					self.OverOutToolTip()
				else:
					return
	
		def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
			if srcItemSlotPos == dstItemSlotPos:
				return
	
			# cyh itemseal 2013 11 08
			if app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVID):
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
	
			elif item.IsRefineScroll(srcItemVID):
				if constInfo.ENABLE_SELF_STACK_SCROLLS and player.GetItemIndex(srcItemSlotPos) == player.GetItemIndex(dstItemSlotPos):
					self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos,0)
				else:
					self.RefineItem(srcItemSlotPos, dstItemSlotPos)
					self.wndItem.SetUseMode(False)
	
			elif item.IsMetin(srcItemVID):
				self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)
	
			elif item.IsDetachScroll(srcItemVID):
				self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)
	
			elif item.IsKey(srcItemVID):
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
	
			elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
	
			elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
	
			elif constInfo.ENABLE_SELF_STACK_SCROLLS and srcItemVID in (71052,71051,71084,71085):
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
	
			else:
				#snd.PlaySound("sound/ui/drop.wav")
	
				if player.IsEquipmentSlot(dstItemSlotPos):
	
					if item.IsEquipmentVID(srcItemVID):
						self.__UseItem(srcItemSlotPos)
	
				else:
					self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
					#net.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)
	
		def __SellItem(self, itemSlotPos):
			if not player.IsEquipmentSlot(itemSlotPos):
				self.sellingSlotNumber = itemSlotPos
				itemIndex = player.GetItemIndex(itemSlotPos)
				itemCount = player.GetItemCount(itemSlotPos)
	
	
				self.sellingSlotitemIndex = itemIndex
				self.sellingSlotitemCount = itemCount
	
				item.SelectItem(itemIndex)
				## 20140220
				if item.IsAntiFlag(item.ANTIFLAG_SELL):
					popup = uiCommon.PopupDialog()
					popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
					popup.SetAcceptEvent(self.__OnClosePopupDialog)
					popup.Open()
					self.popup = popup
					return
	
				itemPrice = item.GetISellItemPrice()
	
				if item.Is1GoldItem():
					itemPrice = itemCount / itemPrice
				else:
					itemPrice = itemPrice * itemCount
	
				if not app.ENABLE_NO_SELL_PRICE_DIVIDED_BY_5:
					itemPrice /= 5
	
				item.GetItemName(itemIndex)
				itemName = item.GetItemName()
	
				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				self.questionDialog.Open()
				self.questionDialog.count = itemCount
	
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
	
		def __OnClosePopupDialog(self):
			self.pop = None
	
		def RefineItem(self, scrollSlotPos, targetSlotPos):
	
			scrollIndex = player.GetItemIndex(scrollSlotPos)
			targetIndex = player.GetItemIndex(targetSlotPos)
	
			if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
				return
	
			###########################################################
			self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
			#net.SendItemUseToItemPacket(scrollSlotPos, targetSlotPos)
			return
	
		def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
			scrollIndex = player.GetItemIndex(scrollSlotPos)
			targetIndex = player.GetItemIndex(targetSlotPos)
	
			if not player.CanDetach(scrollIndex, targetSlotPos):
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					item.SelectItem(scrollIndex)
					if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_FAILURE_CLEAN)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				return
	
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				item.SelectItem(targetIndex)
				if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
					item.SelectItem(scrollIndex)
					if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
						self.questionDialog.SetText(localeInfo.ACCE_DO_YOU_CLEAN)
	
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.sourcePos = scrollSlotPos
			self.questionDialog.targetPos = targetSlotPos
	
		def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
			metinIndex = player.GetItemIndex(metinSlotPos)
			targetIndex = player.GetItemIndex(targetSlotPos)
	
			item.SelectItem(metinIndex)
			itemName = item.GetItemName()
	
			result = player.CanAttachMetin(metinIndex, targetSlotPos)
	
			if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))
	
			if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))
	
			elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))
	
			elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)
	
			if player.ATTACH_METIN_OK != result:
				return
	
			self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)
	
	
	
		def OverOutItem(self):
			self.wndItem.SetUsableItem(False)
			if None != self.tooltipItem:
				self.tooltipItem.HideToolTip()
	
		def OverInItem(self, overSlotPos):
			overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
			self.wndItem.SetUsableItem(False)
	
	
			if app.ENABLE_HIGHLIGHT_NEW_ITEM and overSlotPosGlobal in self.liHighlightedItems:
				self.liHighlightedItems.remove(overSlotPosGlobal)
				self.wndItem.DeactivateSlot(overSlotPos)
	
	
			if mouseModule.mouseController.isAttached():
				attachedItemType = mouseModule.mouseController.GetAttachedType()
				if player.SLOT_TYPE_INVENTORY == attachedItemType:
	
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
	
					if attachedItemVNum==player.ITEM_MONEY: # @fixme005
						pass
					elif self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPosGlobal):
						self.wndItem.SetUsableItem(True)
						self.ShowToolTip(overSlotPosGlobal)
						return
	
			self.ShowToolTip(overSlotPosGlobal)
	
	
		def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
			if item.IsRefineScroll(srcItemVNum):
				return True
			elif item.IsMetin(srcItemVNum):
				return True
			elif item.IsDetachScroll(srcItemVNum):
				return True
			elif item.IsKey(srcItemVNum):
				return True
			elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
				return True
			elif constInfo.ENABLE_SELF_STACK_SCROLLS and srcItemVNum in (71052,71051,71084,71085):
				return True
			else:
				if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
					return True
	
			return False
	
		def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
			if srcSlotPos == dstSlotPos:
				return False
	
			if item.IsRefineScroll(srcItemVNum):
				if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
					return True
				elif constInfo.ENABLE_SELF_STACK_SCROLLS and player.GetItemIndex(dstSlotPos) == srcItemVNum:
					return True
			elif item.IsMetin(srcItemVNum):
				if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
					return True
			elif item.IsDetachScroll(srcItemVNum):
				if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
					return True
			elif item.IsKey(srcItemVNum):
				if player.CanUnlock(srcItemVNum, dstSlotPos):
					return True
	
			elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
				return True
	
			elif constInfo.ENABLE_SELF_STACK_SCROLLS and srcItemVNum in (71052,71051,71084,71085):
				return True
	
			else:
				useType=item.GetUseType(srcItemVNum)
	
				if "USE_CLEAN_SOCKET" == useType:
					if self.__CanCleanBrokenMetinStone(dstSlotPos):
						return True
				elif "USE_CHANGE_ATTRIBUTE" == useType:
					if self.__CanChangeItemAttrList(dstSlotPos):
						return True
				elif "USE_ADD_ATTRIBUTE" == useType:
					if self.__CanAddItemAttr(dstSlotPos):
						return True
				elif "USE_ADD_ATTRIBUTE2" == useType:
					if self.__CanAddItemAttr(dstSlotPos):
						return True
				elif "USE_ADD_ACCESSORY_SOCKET" == useType:
					if self.__CanAddAccessorySocket(dstSlotPos):
						return True
				elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
					if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
						return True;
				elif "USE_PUT_INTO_BELT_SOCKET" == useType:
					dstItemVNum = player.GetItemIndex(dstSlotPos)
					print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum
	
					item.SelectItem(dstItemVNum)
	
					if item.ITEM_TYPE_BELT == item.GetItemType():
						return True
				elif app.ENABLE_USE_COSTUME_ATTR and "USE_CHANGE_COSTUME_ATTR" == useType:
					if self.__CanChangeCostumeAttrList(dstSlotPos):
						return True
				elif app.ENABLE_USE_COSTUME_ATTR and "USE_RESET_COSTUME_ATTR" == useType:
					if self.__CanResetCostumeAttr(dstSlotPos):
						return True
	
			return False
	
		def __CanCleanBrokenMetinStone(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if item.ITEM_TYPE_WEAPON != item.GetItemType():
				return False
	
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
					return True
	
			return False
	
		def __CanChangeItemAttrList(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False
	
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					return True
	
			return False
	
		if app.ENABLE_USE_COSTUME_ATTR:
			def __CanChangeCostumeAttrList(self, dstSlotPos):
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				if dstItemVNum == 0:
					return False
	
				item.SelectItem(dstItemVNum)
	
				if item.GetItemType() != item.ITEM_TYPE_COSTUME:
					return False
	
				for i in xrange(player.METIN_SOCKET_MAX_NUM):
					if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
						return True
	
				return False
	
			def __CanResetCostumeAttr(self, dstSlotPos):
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				if dstItemVNum == 0:
					return False
	
				item.SelectItem(dstItemVNum)
	
				if item.GetItemType() != item.ITEM_TYPE_COSTUME:
					return False
	
				for i in xrange(player.METIN_SOCKET_MAX_NUM):
					if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
						return True
	
				return False
	
		def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if item.GetItemType() != item.ITEM_TYPE_ARMOR:
				return False
	
			if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				return False
	
			curCount = player.GetItemMetinSocket(dstSlotPos, 0)
			maxCount = player.GetItemMetinSocket(dstSlotPos, 1)
	
			if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
				return False
	
			if curCount>=maxCount:
				return False
	
			return True
	
		def __CanAddAccessorySocket(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if item.GetItemType() != item.ITEM_TYPE_ARMOR:
				return False
	
			if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				return False
	
			curCount = player.GetItemMetinSocket(dstSlotPos, 0)
			maxCount = player.GetItemMetinSocket(dstSlotPos, 1)
	
			ACCESSORY_SOCKET_MAX_SIZE = 3
			if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
				return False
	
			return True
	
		def __CanAddItemAttr(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False
	
			item.SelectItem(dstItemVNum)
	
			if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False
	
			attrCount = 0
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					attrCount += 1
	
			if attrCount<4:
				return True
	
			return False
	
		def ShowToolTip(self, slotIndex):
			if None != self.tooltipItem:
				self.tooltipItem.SetInventoryItem(slotIndex)
	
		def OnTop(self):
			if None != self.tooltipItem:
				self.tooltipItem.SetTop()
	
		def OnPressEscapeKey(self):
			self.Close()
			return True
	
		def UseItemSlot(self, slotIndex):
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				return
	
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
				return
	
			slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
	
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
					return
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if self.isShowAcceWindow():
					acce.Add(player.INVENTORY, slotIndex, 255)
					return
	
			self.__UseItem(slotIndex)
			mouseModule.mouseController.DeattachObject()
			self.OverOutItem()
	
		def __UseItem(self, slotIndex):
			ItemVNum = player.GetItemIndex(slotIndex)
			item.SelectItem(ItemVNum)
			if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
				self.questionDialog.Open()
				self.questionDialog.slotIndex = slotIndex
	
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
	
			else:
				self.__SendUseItemPacket(slotIndex)
				#net.SendItemUsePacket(slotIndex)
	
		def __UseItemQuestionDialog_OnCancel(self):
			self.OnCloseQuestionDialog()
	
		def __UseItemQuestionDialog_OnAccept(self):
			self.__SendUseItemPacket(self.questionDialog.slotIndex)
			self.OnCloseQuestionDialog()
	
		def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
	
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			srcItemVNum = player.GetItemIndex(srcSlotPos)
			if constInfo.ENABLE_SELF_STACK_SCROLLS and dstItemVNum == srcItemVNum:
				self.__SendMoveItemPacket(srcSlotPos, dstSlotPos, 0)
			else:
				net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)
	
		def __SendUseItemPacket(self, slotPos):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
	
			net.SendItemUsePacket(slotPos)
	
		def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
				return
	
			net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)
	
		def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				self.wndDragonSoulRefine = wndDragonSoulRefine
	
		def OnMoveWindow(self, x, y):
			# print "Inventory Global Pos : ", self.GetGlobalPosition()
			if self.wndBelt:
				# print "Belt Global Pos : ", self.wndBelt.GetGlobalPosition()
				self.wndBelt.AdjustPositionAndSize()
	
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			def SetAcceWindow(self, wndAcceCombine, wndAcceAbsorption):
				self.wndAcceCombine = wndAcceCombine
				self.wndAcceAbsorption = wndAcceAbsorption
	
			def isShowAcceWindow(self):
				if self.wndAcceCombine:
					if self.wndAcceCombine.IsShow():
						return 1
				if self.wndAcceAbsorption:
					if self.wndAcceAbsorption.IsShow():
						return 1
				return 0
	InventoryWindow.GetInventoryPageIndex = lambda self: self.inventoryPageIndex
	InventoryWindow.UseDSSButtonEffect = lambda self, enable: None
	InventoryWindow.DeleteItem = lambda self, slotPos, invenType: None
	InventoryWindow.AttachItemFromSafebox = lambda self, slotIndex, itemIndex: None
	InventoryWindow.BindWindow = lambda self, wnd: None
	InventoryWindow.MouseSlotEventClear = lambda self: None
	InventoryWindow.RefreshVisibleCostume = lambda self: None
	InventoryWindow.SetAuraWindow = lambda self, wnd1, wnd2: None
	InventoryWindow.SetCanMouseSlot = lambda self, idx: None
	InventoryWindow.SetCantMouseSlot = lambda self, idx: None
