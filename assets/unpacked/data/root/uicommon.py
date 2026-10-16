# -*- coding: cp1256 -*-
import ui
import localeInfo
import app
import ime, chat, net
import uiScriptLocale, uiToolTip, item, wndMgr, localeInfo, constInfo, player, chr

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None
		self.is_autoclose = FALSE
		self.autoclose_timer = 0
		# if app.ENABLE_WINDOW_ANIMATION:
		# 	self.SetWindowAnimation()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.acceptButton = self.GetChild("accept")
			self.acceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

		# if app.ENABLE_WINDOW_ANIMATION and not self.stateSlide:
		# 	self.SetWindowAnimation()

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.acceptEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)
		# self.SetSize(self.GetWidth() + len(text), self.GetHeight())
		# self.board.SetSize(self.board.GetWidth() + len(text), self.board.GetHeight())
		# self.SetCenterPosition()
		# self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetButtonName(self, name):
		self.acceptButton.SetText(name)

	def SetAutoClose(self, flag, time = 2.5):
		self.is_autoclose = flag
		self.autoclose_timer = app.GetTime() + time

	def SetAutoCloseLong(self, flag, time = 5.0):
		self.is_autoclose = flag
		self.autoclose_timer = app.GetTime() + time

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

	def OnUpdate(self):
		if self.IsShow() and self.is_autoclose:
			current_time = app.GetTime()

			self.acceptButton.SetText(
				"OK (%.1f sn)" % (self.autoclose_timer - current_time)
			)

			if self.autoclose_timer < current_time:
				self.Close()

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 9
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True

class QuestionDialog2(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()
	
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text):
		self.textLine1.SetText(text)

	def SetText2(self, text):
		self.textLine2.SetText(text)

class QuestionDialogWithTimeLimit(QuestionDialog2):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()
		self.SetMaxLength(15)
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		# self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		length = min(15, length)
		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))

	def GetText(self):
		return self.inputValue.GetText()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)

		text = self.inputValue.GetText()

		money = 0
		if text and text.isdigit():
			try:
				money = long(text)
			except ValueError:
				money = 199999999

		if text:
			money = min(constInfo.ConvertMoneyText(text), 999999999999999)

		self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))

if app.ENABLE_OFFLINE_SHOP:
	class ShopOfflinePopup(ui.BorderB):
		def __init__(self):
			ui.BorderB.__init__(self)
			
			self.isActiveSlide = False
			self.isActiveSlideOut = False
			self.endTime = 0
			self.wndWidth = 0

			self.wndIcon = ui.ExpandedImageBox()
			self.wndIcon.SetParent(self)
			self.wndIcon.LoadImage("icon/emoji/others/shopsearchyang.png")
			self.wndIcon.SetPosition(5, 10)
			self.wndIcon.Show()

			self.textInfo = ui.TextLine()
			self.textInfo.SetParent(self.wndIcon)
			self.textInfo.SetWindowHorizontalAlignCenter()
			self.textInfo.SetWindowVerticalAlignCenter()
			self.textInfo.SetHorizontalAlignCenter()
			self.textInfo.SetVerticalAlignCenter()

			self.listNotification = {}

		def AddNotification(self, dwItemID, itemName, itemPrice, dwItemCount):
			self.listNotification[dwItemID] = [itemName, itemPrice, dwItemCount]
			self.Close()

		def __del__(self):
			ui.BorderB.__del__(self)

		def SlideIn(self, dwItemID, itemName, itemPrice, dwItemCount):
			self.SetTop()
			self.Show()
			
			self.isActiveSlide = True
			self.endTime = app.GetGlobalTimeStamp() + 4
			
			self.textInfo.SetText("|cffFFD700" + str(itemName) + "|r " + localeInfo.SHOP_BUY_NOTIF_0 + "|cffFFD700"+str(itemPrice)+"|r " + localeInfo.SHOP_BUY_NOTIF_1)
			self.textInfo.SetPosition(160 + len(str(itemPrice)) + 5, 0)
			self.textInfo.Show()

			self.wndWidth = 323 + len(str(itemPrice)) * 2
			self.SetSize(self.wndWidth, 35)
			self.SetPosition(-self.wndWidth, wndMgr.GetScreenHeight() - 100 - 32*4)

		def Close(self):
			if self.isActiveSlide:
				return

			if len(self.listNotification) == 0:
				self.Hide()
			else:
				for itemf in self.listNotification:
					self.SlideIn(itemf, self.listNotification[itemf][0], self.listNotification[itemf][1], self.listNotification[itemf][2])
					del self.listNotification[itemf]
					break

		def Destroy(self):
			self.Hide()
			self.listNotification = {}

		def OnUpdate(self):
			if self.isActiveSlide and self.isActiveSlide == True:
				x, y = self.GetLocalPosition()
				if x < 0:
					self.SetPosition(x + 4, y)
					
			if self.endTime - app.GetGlobalTimeStamp() <= 0 and self.isActiveSlideOut == False and self.isActiveSlide == True:
				self.isActiveSlide = False
				self.isActiveSlideOut = True
					
			if self.isActiveSlideOut and self.isActiveSlideOut == True:
				x, y = self.GetLocalPosition()
				if x > -(self.wndWidth):
					self.SetPosition(x - 4, y)
					
				if x <= -(self.wndWidth):
					self.isActiveSlideOut = False
					self.Close()

	class OfflineShopInputDialog(ui.ScriptWindow):
		PATH_ROOT = "offlineshop/lightwork/shopseller/"
		
		def __init__(self, ItemVnum, ItemCount, editItem=False):
			ui.ScriptWindow.__init__(self)
			self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
			self.__CreateDialog(ItemVnum,ItemCount, editItem)
			self.SetMaxLength(15)
			self.SetCenterPosition()
			if app.ENABLE_WINDOW_ANIMATION:
				self.SetWindowAnimation()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		#Average Price
		def __CreateDialog(self, ItemVnum, ItemCount, editItem):

			if not ItemCount:
				ItemCount = 1

			self.avgPrice = 0

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

			getObject = self.GetChild
			self.board = self.GetChild("board")
			self.board.Hide()
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputValue = getObject("InputValue")
			# self.inputValue.SetNumberMode()
			self.inputValue.SetText("0")

			self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
			self.inputValue.OnPressEscapeKey = ui.__mem_func__(self.OnPressEscapeKey)
			self.moneyText = getObject("MoneyValue")

			self.board = ui.ExpandedImageBox()
			self.board.SetParent(self)
			self.board.AddFlag("not_pick")
			self.board.LoadImage(self.PATH_ROOT + "bg.tga")
			self.board.Show()

			self.acceptButton = ui.MakeButton(self, 21.5, 386, False, "offlineshop/lightwork/shopbuilder/", "btn_big_default.png", "btn_big_hover.png", "btn_big_down.png")
			self.acceptButton.SetText(uiScriptLocale.ACCEPT)

			self.cancelButton = ui.MakeButton(self, 121.5, 386, False, "offlineshop/lightwork/shopbuilder/", "btn_big_default.png", "btn_big_hover.png", "btn_big_down.png")
			self.cancelButton.SetText(uiScriptLocale.KEYCHANGE_CANCLE)
			
			self.boardItem = ui.ExpandedImageBox()
			self.boardItem.SetParent(self)
			self.boardItem.SetPosition(0, 246)
			self.boardItem.AddFlag("not_pick")
			self.boardItem.LoadImage(self.PATH_ROOT + "bg_item.png")
			self.boardItem.SetWindowHorizontalAlignCenter()
			self.boardItem.Show()

			self.itemVnum = ItemVnum

			import item
			item.SelectItem(ItemVnum)
			self.ItemIcon = ui.ExpandedImageBox()
			self.ItemIcon.SetParent(self.boardItem)
			self.ItemIcon.SetPosition(0, 0)
			self.ItemIcon.LoadImage(item.GetIconImageFileName())
			self.ItemIcon.SetWindowHorizontalAlignCenter()
			self.ItemIcon.SetWindowVerticalAlignCenter()
			self.ItemIcon.Show()

			self.boardYang = ui.ExpandedImageBox()
			self.boardYang.SetParent(self)
			self.boardYang.SetPosition(25, 111)
			self.boardYang.LoadImage(self.PATH_ROOT + "price.dds")
			self.boardYang.Show()
			
			self.inputValue.SetParent(self.boardYang)
			self.inputValue.SetPosition(29, 8)
		
			self.wndNameItem = ui.MakeTextLineNew(self, 0, 225, item.GetItemName())
			self.wndNameItem.SetWindowHorizontalAlignCenter()
			self.wndNameItem.SetHorizontalAlignCenter()
			
			self.wndNameLine1 = ui.MakeTextLineNew(self, 0, 23, localeInfo.OFFLINESHOP_INPUT_INFO)
			self.wndNameLine1.SetWindowHorizontalAlignCenter()
			self.wndNameLine1.SetHorizontalAlignCenter()

			self.wndNameLine2 = ui.MakeTextLineNew(self, 0, 35, localeInfo.OFFLINESHOP_INPUT_INFO2)
			self.wndNameLine2.SetWindowHorizontalAlignCenter()
			self.wndNameLine2.SetHorizontalAlignCenter()

			#Average Price
			self.averagePriceInfo = ui.MakeTextLineNew(self, 0, 58, localeInfo.OFFLINESHOP_AVERAGE_PRICE_INFO)
			self.averagePriceInfo.SetWindowHorizontalAlignCenter()
			self.averagePriceInfo.SetHorizontalAlignCenter()
			self.averagePrice = ui.MakeTextLineNew(self, 0, 73, localeInfo.OFFLINESHOP_AVERAGE_PRICE_NO_INFO)
			self.averagePrice.SetWindowHorizontalAlignCenter()
			self.averagePrice.SetHorizontalAlignCenter()

			self.averagePriceBulk = ui.MakeTextLineNew(self, 0, 88, localeInfo.OFFLINESHOP_AVERAGE_PRICE_NO_INFO)
			self.averagePriceBulk.SetWindowHorizontalAlignCenter()
			self.averagePriceBulk.SetHorizontalAlignCenter()

			self.ItemCount = int(ItemCount)
			#Average Price

			self.moneyText.SetParent(self)
			self.moneyText.SetPosition(0, 361)
			self.moneyText.SetWindowHorizontalAlignCenter()
			self.moneyText.SetHorizontalAlignCenter()

			self.sellWithAveragePrice = ui.ExpandedImageBox()
			self.sellWithAveragePrice.SetParent(self)
			self.sellWithAveragePrice.SetPosition(23, 141)
			self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.sellWithAveragePrice.IsChecked = False
			self.sellWithAveragePrice.OnMouseLeftButtonDown = ui.__mem_func__(self.SellWithAveragePrice)
			self.sellWithAveragePrice.Show()

			self.avgPriceSellText = ui.TextLine()
			self.avgPriceSellText.SetParent(self.sellWithAveragePrice)
			self.avgPriceSellText.SetPosition(25, 2)
			self.avgPriceSellText.SetText(localeInfo.OFFLINESHOP_SELL_WITH_AVG_PRICE)
			self.avgPriceSellText.Show()

			self.sellWithAveragePrice2 = ui.ExpandedImageBox()
			self.sellWithAveragePrice2.SetParent(self)
			self.sellWithAveragePrice2.SetPosition(23, 161)
			self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.sellWithAveragePrice2.IsChecked = False
			self.sellWithAveragePrice2.OnMouseLeftButtonDown = ui.__mem_func__(self.SellWithAveragePrice2)
			self.sellWithAveragePrice2.Show()

			self.avgPriceSellText2 = ui.TextLine()
			self.avgPriceSellText2.SetParent(self.sellWithAveragePrice2)
			self.avgPriceSellText2.SetPosition(25, 2)
			self.avgPriceSellText2.SetText(localeInfo.OFFLINESHOP_SELL_WITH_AVG_PRICE2)
			self.avgPriceSellText2.Show()

			self.sellWithAveragePrice3 = ui.ExpandedImageBox()
			self.sellWithAveragePrice3.SetParent(self)
			self.sellWithAveragePrice3.SetPosition(23, 181)
			self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.sellWithAveragePrice3.IsChecked = False
			self.sellWithAveragePrice3.OnMouseLeftButtonDown = ui.__mem_func__(self.SellWithAveragePrice3)
			self.sellWithAveragePrice3.Show()

			self.avgPriceSellText3 = ui.TextLine()
			self.avgPriceSellText3.SetParent(self.sellWithAveragePrice3)
			self.avgPriceSellText3.SetPosition(25, 2)
			self.avgPriceSellText3.SetText(localeInfo.OFFLINESHOP_SELL_WITH_AVG_PRICE3)
			self.avgPriceSellText3.Show()

			self.editItem = editItem
			if self.editItem:

				self.changeAllPrice = ui.ExpandedImageBox()
				self.changeAllPrice.SetParent(self)
				self.changeAllPrice.SetPosition(23, 201)
				self.changeAllPrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
				self.changeAllPrice.IsChecked = False
				self.changeAllPrice.OnMouseLeftButtonDown = ui.__mem_func__(self.ChangeAllPrice)
				self.changeAllPrice.Show()

				self.changeAllPriceText = ui.TextLine()
				self.changeAllPriceText.SetParent(self.changeAllPrice)
				self.changeAllPriceText.SetPosition(25, 2)
				self.changeAllPriceText.SetText(localeInfo.OFFLINESHOP_CHANGE_ALL_PRICE)
				self.changeAllPriceText.Show()

			self.interface = constInfo.GetInterfaceInstance()

			self.SetSize(self.board.GetWidth(), self.board.GetHeight())
		def SellWithAveragePrice(self):

			if self.sellWithAveragePrice2.IsChecked:
				self.sellWithAveragePrice2.IsChecked = False
				self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")

			elif self.sellWithAveragePrice3.IsChecked:
				self.sellWithAveragePrice3.IsChecked = False
				self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")


			if self.sellWithAveragePrice.IsChecked:
				self.sellWithAveragePrice.IsChecked = False
				self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.sellWithAveragePrice.IsChecked = True
				self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		def SellWithAveragePrice2(self):

			if self.sellWithAveragePrice.IsChecked:
				self.sellWithAveragePrice.IsChecked = False
				self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")

			elif self.sellWithAveragePrice3.IsChecked:
				self.sellWithAveragePrice3.IsChecked = False
				self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")


			if self.sellWithAveragePrice2.IsChecked:
				self.sellWithAveragePrice2.IsChecked = False
				self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.sellWithAveragePrice2.IsChecked = True
				self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		def SellWithAveragePrice3(self):

			if self.sellWithAveragePrice.IsChecked:
				self.sellWithAveragePrice.IsChecked = False
				self.sellWithAveragePrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")

			elif self.sellWithAveragePrice2.IsChecked:
				self.sellWithAveragePrice2.IsChecked = False
				self.sellWithAveragePrice2.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")


			if self.sellWithAveragePrice3.IsChecked:
				self.sellWithAveragePrice3.IsChecked = False
				self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.sellWithAveragePrice3.IsChecked = True
				self.sellWithAveragePrice3.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		def ChangeAllPrice(self):
			if self.changeAllPrice.IsChecked:
				self.changeAllPrice.IsChecked = False
				self.changeAllPrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.changeAllPrice.IsChecked = True
				self.changeAllPrice.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		def OnUpdate(self):
			avgPrice = self.avgPrice * self.ItemCount

			if self.sellWithAveragePrice.IsChecked:
				self.inputValue.SetText(str(avgPrice))
				self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(avgPrice))
				self.inputValue.OnKillFocus()
			elif self.sellWithAveragePrice2.IsChecked:
				self.inputValue.SetText(str(int((avgPrice)*110)/100))
				self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(str(int((avgPrice)*110)/100)))
				self.inputValue.OnKillFocus()
			elif self.sellWithAveragePrice3.IsChecked:
				self.inputValue.SetText(str(int((avgPrice)*90)/100))
				self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(str(int((avgPrice)*90)/100)))
				self.inputValue.OnKillFocus()
			else:
				self.inputValue.OnSetFocus()


		def OnPressEscapeKey(self):
			self.Close()
			return True

		def Open(self):
			self.inputValue.SetText("")
			self.inputValue.SetFocus()
			self.__OnValueUpdate()
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.ClearDictionary()
			self.board = None
			self.acceptButton = None
			self.cancelButton = None
			self.inputValue = None
			self.Hide()

		def SetTitle(self, name):
			pass

		def SetFocus(self):
			self.inputValue.SetFocus()

		def SetMaxLength(self, length):
			length = min(15, length)
			self.inputValue.SetMax(length)

		def SetMoneyHeaderText(self, text):
			self.moneyHeaderText = text

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)
			self.inputValue.OnIMEReturn = event

		def SetCancelEvent(self, event):
			# self.board.SetCloseEvent(event)
			self.cancelButton.SetEvent(event)
			self.inputValue.OnPressEscapeKey = event

		def SetValue(self, value):
			value=str(value)
			self.inputValue.SetText(value)
			self.__OnValueUpdate()
			ime.SetCursorPosition(len(value))

		def GetText(self):
			return self.inputValue.GetText()

		def __OnValueUpdate(self):
			ui.EditLine.OnIMEUpdate(self.inputValue)

			money = 0
			text = self.inputValue.GetText()
			if text and text.isdigit():
				try:
					money = long(text)
				except ValueError:
					money = 199999999

			if text:
				money = min(constInfo.ConvertMoneyText(text), 999999999999999)

			self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))
			self.inputValue.OnSetFocus()

		#Average Price
		def AveragePriceUpdate(self, amount):
			self.avgPrice = int(amount)
			self.averagePrice.SetText(localeInfo.OFFLINESHOP_AVERAGE_PRICE.format(localeInfo.NumberToMoneyString(amount)))
			self.averagePriceBulk.SetText(localeInfo.OFFLINESHOP_AVERAGE_PRICE2.format(localeInfo.NumberToMoneyString(amount * self.ItemCount)))

		def ArrangeItemPrices(self):
			money = 0
			text = self.inputValue.GetText()
			if text and text.isdigit():
				try:
					money = long(text)
				except ValueError:
					money = 199999999

			if text:
				money = min(constInfo.ConvertMoneyText(text), 999999999999999)

			if self.editItem:
				if self.changeAllPrice.IsChecked:
					self.interface.wndShopOffline.ReArrangeItemPrices(self.itemVnum, money/self.ItemCount)

		def GetEditAllState(self):
			self.interface.wndShopOffline.SetEditAllState(self.changeAllPrice.IsChecked if self.editItem else False)

class MultipleBuyDialog(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)

		self.SetSize(170, 90)
		self.SetPosition(0, 0)
		self.SetCenterPosition()
		self.SetCloseEvent(ui.__mem_func__(self.Close))

		self.maxValue = 0
		self.eventAccept = 0
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()
		self.itemVnum = 0
		self.priceList = []
		self.priceItemImgList = [None for x in xrange(5)]
		self.priceItemTextList = [None for x in xrange(5)]

		self.SetTitleName(localeInfo.MULTIPLE_BUYS_TITLE)

		self.CreateUI()

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

		self.AddFlag("movable")

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def CreateUI(self):

		self.btnWidth = 78
		self.acceptButton = ui.Button()
		self.acceptButton.SetParent(self)
		self.acceptButton.SetPosition(170/2 - 61 - 5, self.btnWidth)
		self.acceptButton.SetUpVisual("d:/ymir work/ui/public/acceptbutton00.sub")
		self.acceptButton.SetOverVisual("d:/ymir work/ui/public/acceptbutton01.sub")
		self.acceptButton.SetDownVisual("d:/ymir work/ui/public/acceptbutton02.sub")
		self.acceptButton.SetEvent(ui.__mem_func__(self.OnAccept))
		self.acceptButton.Show()

		self.cancelButton = ui.Button()
		self.cancelButton.SetParent(self)
		self.cancelButton.SetPosition(170/2 + 5, self.btnWidth)
		self.cancelButton.SetUpVisual("d:/ymir work/ui/public/canclebutton00.sub")
		self.cancelButton.SetOverVisual("d:/ymir work/ui/public/canclebutton01.sub")
		self.cancelButton.SetDownVisual("d:/ymir work/ui/public/canclebutton02.sub")
		self.cancelButton.SetEvent(ui.__mem_func__(self.Close))
		self.cancelButton.Show()

		self.editlinePos = 38
		self.editLineBG = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/public/Parameter_Slot_03.sub", 39, self.editlinePos)
		self.pickValueEditLine = ui.MakeEditline(self.editLineBG, 31, 2, self.editLineBG.GetWidth(), self.editLineBG.GetHeight(), 3, self.editLineBG.GetWidth())
		self.pickValueEditLine.SetNumberMode()

		self.pickValueEditLine.SetReturnEvent(ui.__mem_func__(self.OnAccept))
		self.pickValueEditLine.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.pickValueEditLine.SetEscapeEvent(ui.__mem_func__(self.Close))

		# self.itemSlot = ui.GridSlotWindow()
		# self.itemSlot.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		# self.itemSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
		# self.itemSlot.SetParent(self)
		# self.itemSlot.SetPosition(22, 34)
		# self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		# self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		# self.itemSlot.Show()

		self.totalItemPrice = ui.TextLine()
		self.totalItemPrice.SetParent(self)
		self.totalItemPrice.SetPosition(35, 32)
		self.totalItemPrice.Hide()

	def Destroy(self):
		self.eventAccept = 0
		self.maxValue = 0
		self.pickValueEditLine = 0
		self.acceptButton = 0
		self.cancelButton = 0
		self.board = None
		self.priceList= []
		self.priceItemImgList = []
		self.priceItemTextList = []

	def SetAcceptEvent(self, event):
		self.eventAccept = event

	def SetMax(self, max):
		self.pickValueEditLine.SetMax(app.MULTIPLE_BUY_MAX_COUNT)

	def Open(self, maxValue, unitValue=0, itemVnum = 0, priceList =[]):

		if len(priceList):
			self.priceList = priceList

		self.pickValueEditLine.SetText("")
		self.pickValueEditLine.SetFocus()

		ime.SetCursorPosition(1)
		self.itemVnum = itemVnum
		self.maxValue = maxValue
		self.Show()
		self.SetTop()
		self.__OnValueUpdate()


	def OnOverInItem(self, slotNumber):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(self.itemVnum, 0)

	def OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def Close(self):
		self.pickValueEditLine.KillFocus()
		self.Hide()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.pickValueEditLine)
		text = self.pickValueEditLine.GetText()

		if len(text) == 0:
			self.pickValueEditLine.SetText("")
			self.pickValueEditLine.SetOverlayText("count")
			self.SetDefaultPos()
		else:
			if int(text) > app.MULTIPLE_BUY_MAX_COUNT:
				self.pickValueEditLine.SetText(str(app.MULTIPLE_BUY_MAX_COUNT))
				text = str(app.MULTIPLE_BUY_MAX_COUNT)

			if len(self.priceList):
				# if self.priceList[0] != 0: # Gold
				self.SetSize(170, 100)
				self.totalItemPrice.SetText(localeInfo.ITEMSHOP_ADD_ITEM_PRICE_TITLE + " " + localeInfo.NumberToDecimalString("{}".format(int(text) * self.priceList[0])))
				self.totalItemPrice.Show() if self.priceList[0] != 0 else self.totalItemPrice.Hide()
				self.SetButtonWidth(68)
				self.EditLineWidth(self.editlinePos+10)

				if len(self.priceList[1]):
					if len(self.priceList[2]):

						if len(self.priceList[3]):
							if len(self.priceList[4]):
								if len(self.priceList[5]):

									(vnum, count) = self.priceList[1]
									item.SelectItem(vnum)
									self.priceItemImgList[0] = ui.ExpandedImageBox()
									self.priceItemImgList[0].SetParent(self)
									self.priceItemImgList[0].SetPosition(33, 48)
									self.priceItemImgList[0].LoadImage(item.GetIconImageFileName())
									self.priceItemImgList[0].Show()

									self.priceItemTextList[0] = ui.TextLine()
									self.priceItemTextList[0].SetParent(self.priceItemImgList[0])
									self.priceItemTextList[0].SetPosition(40, 10)
									haveCount = player.GetItemCountByVnum(vnum)
									if haveCount >= (int(text) * count):
										self.priceItemTextList[0].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
									else:
										self.priceItemTextList[0].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))

									self.priceItemTextList[0].Show()
			
									(vnum, count) = self.priceList[2]
									item.SelectItem(vnum)
									self.priceItemImgList[1] = ui.ExpandedImageBox()
									self.priceItemImgList[1].SetParent(self)
									self.priceItemImgList[1].SetPosition(33, 48+40)
									self.priceItemImgList[1].LoadImage(item.GetIconImageFileName())
									self.priceItemImgList[1].Show()

									self.priceItemTextList[1] = ui.TextLine()
									self.priceItemTextList[1].SetParent(self.priceItemImgList[1])
									self.priceItemTextList[1].SetPosition(40, 10)
									haveCount = player.GetItemCountByVnum(vnum)
									if haveCount >= (int(text) * count):
										self.priceItemTextList[1].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
									else:
										self.priceItemTextList[1].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
									self.priceItemTextList[1].Show()

									(vnum, count) = self.priceList[3]
									item.SelectItem(vnum)
									self.priceItemImgList[2] = ui.ExpandedImageBox()
									self.priceItemImgList[2].SetParent(self)
									self.priceItemImgList[2].SetPosition(33, 48+40*2)
									self.priceItemImgList[2].LoadImage(item.GetIconImageFileName())
									self.priceItemImgList[2].Show()

									self.priceItemTextList[2] = ui.TextLine()
									self.priceItemTextList[2].SetParent(self.priceItemImgList[2])
									self.priceItemTextList[2].SetPosition(40, 10)
									haveCount = player.GetItemCountByVnum(vnum)
									if haveCount >= (int(text) * count):
										self.priceItemTextList[2].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
									else:
										self.priceItemTextList[2].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
									self.priceItemTextList[2].Show()

									(vnum, count) = self.priceList[4]
									item.SelectItem(vnum)
									self.priceItemImgList[3] = ui.ExpandedImageBox()
									self.priceItemImgList[3].SetParent(self)
									self.priceItemImgList[3].SetPosition(33, 48+40*3)
									self.priceItemImgList[3].LoadImage(item.GetIconImageFileName())
									self.priceItemImgList[3].Show()

									self.priceItemTextList[3] = ui.TextLine()
									self.priceItemTextList[3].SetParent(self.priceItemImgList[3])
									self.priceItemTextList[3].SetPosition(40, 10)
									haveCount = player.GetItemCountByVnum(vnum)
									if haveCount >= (int(text) * count):
										self.priceItemTextList[3].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
									else:
										self.priceItemTextList[3].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
									self.priceItemTextList[3].Show()

									(vnum, count) = self.priceList[5]
									item.SelectItem(vnum)
									self.priceItemImgList[4] = ui.ExpandedImageBox()
									self.priceItemImgList[4].SetParent(self)
									self.priceItemImgList[4].SetPosition(33, 48+40*4)
									self.priceItemImgList[4].LoadImage(item.GetIconImageFileName())
									self.priceItemImgList[4].Show()

									self.priceItemTextList[4] = ui.TextLine()
									self.priceItemTextList[4].SetParent(self.priceItemImgList[4])
									self.priceItemTextList[4].SetPosition(40, 10)
									haveCount = player.GetItemCountByVnum(vnum)
									if haveCount >= (int(text) * count):
										self.priceItemTextList[4].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
									else:
										self.priceItemTextList[4].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
									self.priceItemTextList[4].Show()

									self.SetSize(170, 150+40*4)
									self.SetButtonWidth(108+40*4)
									self.EditLineWidth(self.editlinePos+50+40*4)

								else:
									(vnum, count) = self.priceList[1]
									item.SelectItem(vnum)
									self.priceItemImgList[0] = ui.ExpandedImageBox()
									self.priceItemImgList[0].SetParent(self)
									self.priceItemImgList[0].SetPosition(33, 48)
									self.priceItemImgList[0].LoadImage(item.GetIconImageFileName())
									self.priceItemImgList[0].Show()

									self.priceItemTextList[0] = ui.TextLine()
									self.priceItemTextList[0].SetParent(self.priceItemImgList[0])
									self.priceItemTextList[0].SetPosition(40, 10)
									haveCount = player.GetItemCountByVnum(vnum)
									if haveCount >= (int(text) * count):
										self.priceItemTextList[0].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
									else:
										self.priceItemTextList[0].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
									self.priceItemTextList[0].Show()
			
									(vnum, count) = self.priceList[2]
									item.SelectItem(vnum)
									self.priceItemImgList[1] = ui.ExpandedImageBox()
									self.priceItemImgList[1].SetParent(self)
									self.priceItemImgList[1].SetPosition(33, 48+40)
									self.priceItemImgList[1].LoadImage(item.GetIconImageFileName())
									self.priceItemImgList[1].Show()

									self.priceItemTextList[1] = ui.TextLine()
									self.priceItemTextList[1].SetParent(self.priceItemImgList[1])
									self.priceItemTextList[1].SetPosition(40, 10)
									haveCount = player.GetItemCountByVnum(vnum)
									if haveCount >= (int(text) * count):
										self.priceItemTextList[1].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
									else:
										self.priceItemTextList[1].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
									self.priceItemTextList[1].Show()

									(vnum, count) = self.priceList[3]
									item.SelectItem(vnum)
									self.priceItemImgList[2] = ui.ExpandedImageBox()
									self.priceItemImgList[2].SetParent(self)
									self.priceItemImgList[2].SetPosition(33, 48+40*2)
									self.priceItemImgList[2].LoadImage(item.GetIconImageFileName())
									self.priceItemImgList[2].Show()

									self.priceItemTextList[2] = ui.TextLine()
									self.priceItemTextList[2].SetParent(self.priceItemImgList[2])
									self.priceItemTextList[2].SetPosition(40, 10)
									haveCount = player.GetItemCountByVnum(vnum)
									if haveCount >= (int(text) * count):
										self.priceItemTextList[2].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
									else:
										self.priceItemTextList[2].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
									self.priceItemTextList[2].Show()

									(vnum, count) = self.priceList[4]
									item.SelectItem(vnum)
									self.priceItemImgList[3] = ui.ExpandedImageBox()
									self.priceItemImgList[3].SetParent(self)
									self.priceItemImgList[3].SetPosition(33, 48+40*3)
									self.priceItemImgList[3].LoadImage(item.GetIconImageFileName())
									self.priceItemImgList[3].Show()

									self.priceItemTextList[3] = ui.TextLine()
									self.priceItemTextList[3].SetParent(self.priceItemImgList[3])
									self.priceItemTextList[3].SetPosition(40, 10)
									haveCount = player.GetItemCountByVnum(vnum)
									if haveCount >= (int(text) * count):
										self.priceItemTextList[3].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
									else:
										self.priceItemTextList[3].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
									self.priceItemTextList[3].Show()

									self.SetSize(170, 150+40*3)
									self.SetButtonWidth(108+40*3)
									self.EditLineWidth(self.editlinePos+50+40*3)
							else:
								
								(vnum, count) = self.priceList[1]
								item.SelectItem(vnum)
								self.priceItemImgList[0] = ui.ExpandedImageBox()
								self.priceItemImgList[0].SetParent(self)
								self.priceItemImgList[0].SetPosition(33, 48)
								self.priceItemImgList[0].LoadImage(item.GetIconImageFileName())
								self.priceItemImgList[0].Show()

								self.priceItemTextList[0] = ui.TextLine()
								self.priceItemTextList[0].SetParent(self.priceItemImgList[0])
								self.priceItemTextList[0].SetPosition(40, 10)
								haveCount = player.GetItemCountByVnum(vnum)
								if haveCount >= (int(text) * count):
									self.priceItemTextList[0].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
								else:
									self.priceItemTextList[0].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
								self.priceItemTextList[0].Show()
		
								(vnum, count) = self.priceList[2]
								item.SelectItem(vnum)
								self.priceItemImgList[1] = ui.ExpandedImageBox()
								self.priceItemImgList[1].SetParent(self)
								self.priceItemImgList[1].SetPosition(33, 48+40)
								self.priceItemImgList[1].LoadImage(item.GetIconImageFileName())
								self.priceItemImgList[1].Show()

								self.priceItemTextList[1] = ui.TextLine()
								self.priceItemTextList[1].SetParent(self.priceItemImgList[1])
								self.priceItemTextList[1].SetPosition(40, 10)
								haveCount = player.GetItemCountByVnum(vnum)
								if haveCount >= (int(text) * count):
									self.priceItemTextList[1].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
								else:
									self.priceItemTextList[1].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
								self.priceItemTextList[1].Show()

								(vnum, count) = self.priceList[3]
								item.SelectItem(vnum)
								self.priceItemImgList[2] = ui.ExpandedImageBox()
								self.priceItemImgList[2].SetParent(self)
								self.priceItemImgList[2].SetPosition(33, 48+40*2)
								self.priceItemImgList[2].LoadImage(item.GetIconImageFileName())
								self.priceItemImgList[2].Show()

								self.priceItemTextList[2] = ui.TextLine()
								self.priceItemTextList[2].SetParent(self.priceItemImgList[2])
								self.priceItemTextList[2].SetPosition(40, 10)
								haveCount = player.GetItemCountByVnum(vnum)
								if haveCount >= (int(text) * count):
									self.priceItemTextList[2].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
								else:
									self.priceItemTextList[2].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
								self.priceItemTextList[2].Show()

								self.SetSize(170, 150+40*2)
								self.SetButtonWidth(108+40*2)
								self.EditLineWidth(self.editlinePos+50+40*2)
						else:

							(vnum, count) = self.priceList[1]
							item.SelectItem(vnum)
							self.priceItemImgList[0] = ui.ExpandedImageBox()
							self.priceItemImgList[0].SetParent(self)
							self.priceItemImgList[0].SetPosition(33, 48)
							self.priceItemImgList[0].LoadImage(item.GetIconImageFileName())
							self.priceItemImgList[0].Show()

							self.priceItemTextList[0] = ui.TextLine()
							self.priceItemTextList[0].SetParent(self.priceItemImgList[0])
							self.priceItemTextList[0].SetPosition(40, 10)
							haveCount = player.GetItemCountByVnum(vnum)
							if haveCount >= (int(text) * count):
								self.priceItemTextList[0].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
							else:
								self.priceItemTextList[0].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
							self.priceItemTextList[0].Show()
	
							(vnum, count) = self.priceList[2]
							item.SelectItem(vnum)
							self.priceItemImgList[1] = ui.ExpandedImageBox()
							self.priceItemImgList[1].SetParent(self)
							self.priceItemImgList[1].SetPosition(33, 48+40)
							self.priceItemImgList[1].LoadImage(item.GetIconImageFileName())
							self.priceItemImgList[1].Show()

							self.priceItemTextList[1] = ui.TextLine()
							self.priceItemTextList[1].SetParent(self.priceItemImgList[1])
							self.priceItemTextList[1].SetPosition(40, 10)
							haveCount = player.GetItemCountByVnum(vnum)
							if haveCount >= (int(text) * count):
								self.priceItemTextList[1].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
							else:
								self.priceItemTextList[1].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
							self.priceItemTextList[1].Show()

							self.SetSize(170, 150+40)
							self.SetButtonWidth(108+40)
							self.EditLineWidth(self.editlinePos+50+40)

					else:
						(vnum, count) = self.priceList[1]
						item.SelectItem(vnum)
						self.priceItemImgList[0] = ui.ExpandedImageBox()
						self.priceItemImgList[0].SetParent(self)
						self.priceItemImgList[0].SetPosition(33, 48)
						self.priceItemImgList[0].LoadImage(item.GetIconImageFileName())
						self.priceItemImgList[0].Show()

						self.priceItemTextList[0] = ui.TextLine()
						self.priceItemTextList[0].SetParent(self.priceItemImgList[0])
						self.priceItemTextList[0].SetPosition(40, 10)
						haveCount = player.GetItemCountByVnum(vnum)
						if haveCount >= (int(text) * count):
							self.priceItemTextList[0].SetText("x{} | |cff59b35f({})|r ".format((int(text) * count), haveCount))
						else:
							self.priceItemTextList[0].SetText("x{} | |cffc97b7f({})|r ".format((int(text) * count), haveCount))
						self.priceItemTextList[0].Show()

						self.SetSize(170, 150)
						self.SetButtonWidth(108)
						self.EditLineWidth(self.editlinePos+50)

					# else:
					# 	self.SetSize(170, 100)
					# 	self.totalItemPrice.SetText("Total Gold: {}".format(int(text) * self.priceList[0]))
					# 	self.totalItemPrice.Show()
					# 	self.SetButtonWidth(68)
					# 	self.EditLineWidth(self.editlinePos+10)

				else:
					self.totalItemPrice.SetText(localeInfo.ITEMSHOP_ADD_ITEM_PRICE_TITLE + " " + localeInfo.NumberToDecimalString("{}".format(int(text) * self.priceList[0])))
					if self.priceList[0] != 0:
						self.totalItemPrice.Show()
						self.SetButtonWidth(68)
						self.EditLineWidth(self.editlinePos+10)
						self.SetSize(170, 100)
					else:
						self.totalItemPrice.Hide()
						self.SetButtonWidth(58)
						self.EditLineWidth(self.editlinePos)
						self.SetSize(170, 90)
			else:
				self.SetDefaultPos()

		# self.itemSlot.SetItemSlot(0, self.itemVnum, int(text))
		# self.itemSlot.RefreshSlot()

	def SetDefaultPos(self):
		self.SetSize(170, 90)
		self.SetButtonWidth(58)
		self.EditLineWidth(self.editlinePos)
		self.totalItemPrice.Hide()

		for element in (self.priceItemImgList + self.priceItemTextList):
			if element:
				element.Hide()

	def SetButtonWidth(self, pos):
		self.acceptButton.SetPosition(170/2 - 61 - 5, pos)
		self.cancelButton.SetPosition(170/2 + 5, pos)

	def EditLineWidth(self, pos):
		self.editLineBG.SetPosition(39, pos)

	def OnAccept(self):
		text = self.pickValueEditLine.GetText()
		count = int(text)

		if text == "":
			return True

		if text:
			moneyValue = min(constInfo.ConvertMoneyText(text), self.maxValue)

			if self.eventAccept:
				self.eventAccept(moneyValue)

		self.Close()

		return True

class QuestionDialogItem(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.SetWindowName("uiCommon.QuestionDialogItem")
		self.__CreateDialog()
		
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.count = 0
		self.height = 0

		self.titleBar = ui.TitleBar()
		self.titleBar.SetParent(self.board)
		self.titleBar.MakeTitleBar(244, "yellow")
		self.titleBar.SetPosition(8, 7)
		self.titleBar.Show()

		self.titleName = ui.TextLine()
		self.titleName.SetParent(self.titleBar)
		self.titleName.SetPosition(0, 4)
		self.titleName.SetWindowHorizontalAlignCenter()
		self.titleName.SetHorizontalAlignCenter()
		self.titleName.Show()
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogitem.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.textLine2 = self.GetChild("message2")
		self.sellButton = self.GetChild("sell")
		self.cancelButton = self.GetChild("cancel")
		self.destroyButton = self.GetChild("destroy")

		self.slotList = []
		for i in xrange(3):
			slot = ui.ImageBox()
			slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
			slot.SetParent(self)
			slot.SetWindowHorizontalAlignCenter()
			self.slotList.append(slot)

	def Open(self, vnum, slot, text="", invenType = 0):
		item.SelectItem(vnum)
		xSlotCount, ySlotCount = item.GetItemSize()
		metinSlot = [player.GetItemMetinSocket(player.INVENTORY, slot, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		self.titleName.SetText(item.GetItemName())

		if text:
			textLine = ui.TextLine()
			textLine.SetPosition(0, 80 + 32*ySlotCount)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.SetVerticalAlignCenter()
			textLine.SetParent(self.board)
			textLine.SetText(text)
			textLine.Show()
			self.textLine = textLine

		slotGrid = ui.SlotWindow()
		slotGrid.SetParent(self)
		slotGrid.SetPosition(-16, 64)
		slotGrid.SetWindowHorizontalAlignCenter()
		slotGrid.AppendSlot(0, 0, 0, 32*xSlotCount, 32*ySlotCount)
		slotGrid.AddFlag("not_pick")
		slotGrid.Show()
		self.slotGrid = slotGrid

		if self.count > 1:
			self.slotGrid.SetItemSlot(0, vnum, self.count)
		else:
			self.slotGrid.SetItemSlot(0, vnum)

		if text:
			self.height -= 10
				
		self.SetSize(260, 100 + 32*ySlotCount + self.height)
		self.board.SetSize(260, 80 + 32*ySlotCount + self.height)
		self.textLine.SetPosition(0, 44)

		for i in xrange(min(3, ySlotCount)):
			self.slotList[i].SetPosition(0, 32 + ySlotCount*32 - i*32)
			self.slotList[i].OnMouseOverIn = lambda arg = slot : self.OverInItem(arg, invenType)
			self.slotList[i].OnMouseOverOut = lambda arg = self.tooltipItem: self.OverOutItem(arg)
			self.slotList[i].Show()

		self.GetChild("sell").SetPosition(-75, 74 + 32*ySlotCount + self.height)
		self.GetChild("cancel").SetPosition(75, 74 + 32*ySlotCount + self.height)
		self.GetChild("destroy").SetPosition(0, 74 + 32*ySlotCount + self.height)

		extraBuyBackHeight = 0
		if getattr(app, "ENABLE_BUY_BACK_ITEM", 0):
			extraBuyBackHeight = 28
			btnBuyBack = ui.Button()
			btnBuyBack.SetParent(self.board)
			btnBuyBack.SetWindowHorizontalAlignCenter()
			btnBuyBack.SetPosition(0, 100 + 32*ySlotCount + self.height)
			btnBuyBack.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			btnBuyBack.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			btnBuyBack.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			btnBuyBack.SetText(localeInfo.BUY_BACK_BUTTON)
			btnBuyBack.SetEvent(ui.__mem_func__(self.__OnClickBuyBack))
			btnBuyBack.Show()
			self.btnBuyBack = btnBuyBack

		self.SetSize(260, 100 + 32*ySlotCount + self.height + extraBuyBackHeight)
		self.board.SetSize(self.board.GetWidth(), self.board.GetHeight() + 30 + extraBuyBackHeight)

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def __OnClickBuyBack(self):
		self.Close()
		gameInst = constInfo.GetGameInstance()
		if gameInst and hasattr(gameInst, "OpenBuyBackWindow"):
			gameInst.OpenBuyBackWindow()

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)

	def SetMessage(self, text):
		self.textLine.SetText(text)
	def SetMessage2(self, text):
		self.textLine2.SetText(text)

	def OverInItem(self, slot, invenType):
		self.tooltipItem.SetInventoryItem(slot, invenType)

	def OverOutItem(self, tooltipItem):
		if 0 != tooltipItem:
			self.tooltipItem.HideToolTip()
			self.tooltipItem.ClearToolTip()

	def Close(self):
		self.ClearDictionary()
		self.slotList = []
		self.titleBar = None
		self.titleName = None
		self.textLine = None
		self.slotGrid = None
		self.btnBuyBack = None
		
		self.tooltipItem = 0
		self.Hide()
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	# def SetWidth(self, width):
		# height = self.GetHeight()
		# self.SetSize(width, height)
		# self.board.SetSize(width, height)
		# self.SetCenterPosition()
		# self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.sellButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.sellButton.SetEvent(event)

	def SetDestroyEvent(self, event):
		self.destroyButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.sellButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True

if app.ENABLE_NEW_PET_SYSTEM:
	class PopupDialog2(ui.ScriptWindow):

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.__LoadDialog()
			self.acceptEvent = lambda *arg: None

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __LoadDialog(self):
			try:
				PythonScriptLoader = ui.PythonScriptLoader()
				PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog2.py")

				self.board = self.GetChild("board")
				self.message1 = self.GetChild("message1")
				self.message2 = self.GetChild("message2")
				self.accceptButton = self.GetChild("accept")
				self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

			except:
				import exception
				exception.Abort("PopupDialog.LoadDialog.BindObject")

		def Open(self):
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.Hide()
			self.acceptEvent()

		def Destroy(self):
			self.Close()
			self.ClearDictionary()

		def SetWidth(self, width):
			height = self.GetHeight()
			self.SetSize(width, height)
			self.board.SetSize(width, height)
			self.SetCenterPosition()
			self.UpdateRect()

		def SetText1(self, text):
			self.message1.SetText(text)
			
		def SetText2(self, text):
			self.message2.SetText(text)		

		def SetAcceptEvent(self, event):
			self.acceptEvent = event

		def SetButtonName(self, name):
			self.accceptButton.SetText(name)

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def OnIMEReturn(self):
			self.Close()
			return True

class BackgroundShadow(ui.ExpandedImageBox):
	def __init__(self, alpha = 0.15):
		ui.ExpandedImageBox.__init__(self)
		self.FadeOut()
		self.LoadImage("d:/ymir work/ui/game/backgroundshadow/shadow.png")
		self.SetAlpha(alpha)
		self.Hide()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def FadeIn(self):
		self.SetTop()
		self.Show()

	def FadeOut(self):
		self.Hide()

if app.ENABLE_NAMING_SCROLL:
	class ChangeNameDialog(ui.BoardWithTitleBar):

		def __init__(self, itemVnum, itemPos):
			ui.BoardWithTitleBar.__init__(self)
			self.SetSize(170, 176)
			self.itemVnum = itemVnum
			self.itemPos = itemPos
			self.newName = None

			self.isLoaded = False

			self.SetCenterPosition()
			self.AddFlag('movable')
			self.SetTitleName(localeInfo.NAMING_SCROLL_TITLE)
			self.SetCloseEvent(self.Close)

			self.LoadMainDialog()

		def LoadMainDialog(self):
			if self.isLoaded:
				return

			self.ItemSlotBase = ui.ExpandedImageBox()
			self.ItemSlotBase.SetParent(self)
			self.ItemSlotBase.SetPosition(67, 35)
			self.ItemSlotBase.LoadImage("d:/ymir work/ui/public/slot_base.sub")
			# self.ItemSlotBase.SetStringEvent("MOUSE_OVER_IN", ui.__mem_func__(self.IconOnMouseOverIn))
			# self.ItemSlotBase.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.IconOnMouseOverOut))
			self.ItemSlotBase.Show()

			item.SelectItem(self.itemVnum)

			self.ItemIcon = ui.ExpandedImageBox()
			self.ItemIcon.SetParent(self.ItemSlotBase)
			self.ItemIcon.AddFlag("not_pick")
			self.ItemIcon.LoadImage(item.GetIconImageFileName())
			self.ItemIcon.SetWindowVerticalAlignCenter()
			self.ItemIcon.SetWindowHorizontalAlignCenter()
			self.ItemIcon.Show()

			self.textLine = ui.TextLine()
			self.textLine.SetParent(self)
			self.textLine.SetPosition(20, 85)
			self.textLine.SetSize(150, 20)
			self.textLine.SetText(localeInfo.NAMING_SCROLL_TEXT)
			self.textLine.Show()

			self.editlineBG = ui.ExpandedImageBox()
			self.editlineBG.SetParent(self)
			self.editlineBG.LoadImage("offlineshop/lightwork/searchshop/searchbg.png")
			self.editlineBG.SetPosition(15, 105)
			self.editlineBG.SetSize(150, 20)
			self.editlineBG.Show()

			self.editline = ui.EditLine()
			self.editline.SetParent(self.editlineBG)
			self.editline.SetPosition(4, 3)
			self.editline.SetSize(self.editlineBG.GetWidth(), self.editlineBG.GetHeight())
			self.editline.SetMax(16)
			self.editline.SetEscapeEvent(ui.__mem_func__(self.ClearEditline))
			self.editline.Show()

			self.btnConfirmName = ui.MakeButton(self, 40, 135, False, "offlineshop/lightwork/shopbuilder/", "btn_big_default.png", "btn_big_hover.png", "btn_big_down.png")
			self.btnConfirmName.SetText(localeInfo.UI_OK)
			self.btnConfirmName.SetEvent(ui.__mem_func__(self.ConfirmName))

			self.isLoaded = True

		def __del__(self):
			ui.BoardWithTitleBar.__del__(self)

		def ConfirmName(self):
			special_characters = "'.'{[]}^&()*|é\!@#$%^&*()-+?_=,<>/'€£¥•¶§•ªº«»~`:;´¨_ğüşöçİĞÜŞÖÇıæßðþÞÐŒœŠšŸ¥µÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'"
			self.newName = self.editline.GetText()
			if not len(self.newName):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NAMING_SCROLL_ERROR)
				self.Close()
				return

			if any(chs in special_characters for chs in self.newName):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NAMING_SCROLL_ERROR)
				self.Close()
				return

			scrollTypeList = {
				24050 : 1,
				24051 : 1,
				24052 : 1,
				24053 : 1,
				64000 : 1,

				24054 : 2,
				24055 : 2,
				24056 : 2,
				24057 : 2,
				64001 : 2,

				24058 : 3,
				24059 : 3,
				24060 : 3,
				24061 : 3,
				64002 : 3,
			}

			scrollType = scrollTypeList.get(self.itemVnum, -1)

			if scrollType == -1:
				return

			net.SendChatPacket("/naming_scroll_set_name %d %d %s" % (self.itemPos, scrollType, self.newName))

			self.Close()

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def ClearEditline(self):
			self.editline.SetText("")
			if self.editline:
				self.editline.KillFocus()
			return True

		def Open(self):
			self.Show()

		def Close(self):
			self.newName = None
			self.editline.SetText("")
			if self.editline:
				self.editline.KillFocus()
			self.Hide()


class ChatColorMenu(ui.ImageBox):
	COLOR_LIST = { 
        "colors": [
			ui.GenerateColor(255, 255, 255),	# WHITE / DEFAULT
			ui.GenerateColor(0, 128, 255),		# BLUE
			ui.GenerateColor(255, 0, 0),		# RED
			ui.GenerateColor(255, 255, 0),		# YELLOW
			ui.GenerateColor(0, 255, 0),		# GREEN
			ui.GenerateColor(255, 165, 0),		# ORANGE
			ui.GenerateColor(64, 224, 208),		# TURQUOISE
			ui.GenerateColor(0, 0, 0),			# BLACK
			ui.GenerateColor(160, 32, 240),		# PURPLE
			ui.GenerateColor(255, 105, 180),	# PINK
		],
		"hex" : [
			"|cffe3e6e4",		# WHITE / DEFAULT
			"|cff284feb",		# BLUE
			"|cffd6151f",		# RED
			"|cffd6bf15",		# YELLOW
			"|cff15d618",		# GREEN
			"|cffd69f15",		# ORANGE
			"|cff15d6c9",		# TURQUOISE
			"|cff020303",		# BLACK
			"|cff9204de",		# PURPLE
			"|cfff26beb",		# PINK
		]
	}

	def __init__(self):
		ui.ImageBox.__init__(self)
		self.AddFlag("float")
		self.is_loaded = False
		self.selectedColor = self.COLOR_LIST["hex"][0]

	def __del__(self):
		ui.ImageBox.__del__(self)

	def Destroy(self):
		pass

	def __LoadWindow(self):
		self.LoadImage("d:/ymir work/ui/game/chat/color_bg.tga")

		self.bars = []
		y_start = 8
		for i in xrange(len(self.COLOR_LIST["colors"])):
			bar = ui.Bar()
			bar.SetParent(self)
			bar.SetSize(30, 16)
			bar.SetColor(self.COLOR_LIST["colors"][i])
			bar.SetPosition(6, y_start)
			bar.Hide()
			bar.OnMouseLeftButtonDown = lambda arg=i: self.OnMouseLeftButtonDown(arg)

			self.bars.append(bar)
			y_start += 21

		self.is_loaded = True

	def Open(self):
		if not self.is_loaded:
			self.__LoadWindow()

		self.Show()
		self.SetTop()

		for bar in self.bars:
			bar.Show()

	def Close(self):
		self.Hide()

	def OnMouseLeftButtonDown(self, key=-1):
		if key not in xrange(len(self.COLOR_LIST["colors"])):
			return

		if not chr.IsPremium():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_SEARCH_PREMIUM_NEEDED_FOR_THIS_ACTION)
			return

		self.selectedColor = self.COLOR_LIST["hex"][key]

		self.Close()

	def GetColor(self):
		return self.selectedColor

class OnlinePopup(ui.BorderB):
	def __init__(self):
		ui.BorderB.__init__(self)
		
		self.isActiveSlide = False
		self.isActiveSlideOut = False
		self.endTime = 0
		self.wndWidth = 0

		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetFontName("Verdana:14")
		self.textLine.SetWindowHorizontalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.SetPosition(3, 0)
		self.textLine.Show()
		
		# self.onlineImage = ui.ImageBox()
		# self.onlineImage.SetParent(self)
		# self.onlineImage.SetPosition(8, 8)
		# self.onlineImage.LoadImage("d:/ymir work/ui/game/windows/messenger_list_online.sub")
		# self.onlineImage.Show()
		
	def __del__(self):
		ui.BorderB.__del__(self)

	def SlideIn(self):
		self.SetTop()
		self.Show()
		
		self.isActiveSlide = True
		self.endTime = app.GetGlobalTimeStamp() + 5

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Close()

	def SetUserName(self, name):
		self.textLine.SetText(uiScriptLocale.PLAYER_IS_ONLINE_NOW % ("|cffFFCA33%s|r" % str(name)))
		
		self.wndWidth = self.textLine.GetTextSize()[0] + 40
		self.SetSize(self.wndWidth, 40)
		self.SetPosition(-self.wndWidth, wndMgr.GetScreenHeight() - 200)
		
	def OnUpdate(self):
		if self.isActiveSlide:
			x, y = self.GetLocalPosition()
			if x < 0:
				self.SetPosition(x + 2, y)
				
		if self.endTime - app.GetGlobalTimeStamp() <= 0 and not self.isActiveSlideOut and self.isActiveSlide:
			self.isActiveSlide = False
			self.isActiveSlideOut = True
				
		if self.isActiveSlideOut and self.isActiveSlideOut:
			x, y = self.GetLocalPosition()
			if x > -(self.wndWidth):
				self.SetPosition(x - 2, y)
				
			if x <= -(self.wndWidth):
				self.isActiveSlideOut = False
				self.Close()
