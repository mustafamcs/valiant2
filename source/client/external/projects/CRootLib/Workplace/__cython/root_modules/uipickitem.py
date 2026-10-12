import wndMgr, ui, ime, localeInfo, app, uitooltip

class PickItemDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.unitValue = 1
		self.maxValue = 0
		self.eventAccept = 0
		self.doAll = False
		self.tooltipItem = uitooltip.ItemToolTip()
		self.tooltipItem.Hide()
		self.itemVnum = 0

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PickItemDialog.py")
		except:
			import exception
			exception.Abort("MoneyDialog.LoadDialog.LoadScript")

		try:
			self.board = self.GetChild("board")
			self.maxValueTextLine = self.GetChild("max_value")
			self.pickValueEditLine = self.GetChild("money_value")
			self.acceptButton = self.GetChild("accept_button")
			self.cancelButton = self.GetChild("cancel_button")
		except:
			import exception
			exception.Abort("MoneyDialog.LoadDialog.BindObject")

		self.pickValueEditLine.SetReturnEvent(ui.__mem_func__(self.OnAccept))
		self.pickValueEditLine.SetEscapeEvent(ui.__mem_func__(self.Close))
		self.acceptButton.SetEvent(ui.__mem_func__(self.OnAccept))
		self.cancelButton.SetEvent(ui.__mem_func__(self.Close))
		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.checkBox = ui.CheckBoxRenewal()
		self.checkBox.SetParent(self)
		self.checkBox.SetPosition(58, 58)
		self.checkBox.SetWindowVerticalAlignBottom()
		self.checkBox.OnMouseLeftButtonDown = ui.__mem_func__(self.SetSplitFunction)
		self.checkBox.SetCheckStatus(self.doAll)
		self.checkBox.SetTextInfo(localeInfo.SPLIT_MULTIPLE_ITEMS)
		self.checkBox.Show()

		self.itemSlot = ui.GridSlotWindow()
		self.itemSlot.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
		self.itemSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
		self.itemSlot.SetParent(self)
		self.itemSlot.SetPosition(22, 34)
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		self.itemSlot.Show()

	def SplitClear(self):
		self.doAll = False
		self.checkBox.SetCheckStatus(self.doAll)
		
	def SetSplitFunction(self):
		self.doAll = not self.doAll

	def IsSplitAll(self):
		return self.doAll
		
	def Destroy(self):
		self.ClearDictionary()
		self.eventAccept = 0
		self.maxValue = 0
		self.pickValueEditLine = 0		
		self.acceptButton = 0
		self.cancelButton = 0
		self.board = None
		self.doAll = False

	def SetTitleName(self, text):
		self.board.SetTitleName(text)

	def SetAcceptEvent(self, event):
		self.eventAccept = event

	def SetMax(self, max):
		self.pickValueEditLine.SetMax(max)

	def Open(self, maxValue, itemVnum):

		unitValue=1
		self.itemVnum = itemVnum

		width = self.GetWidth()
		(mouseX, mouseY) = wndMgr.GetMousePosition()

		if mouseX + width/2 > wndMgr.GetScreenWidth():
			xPos = wndMgr.GetScreenWidth() - width
		elif mouseX - width/2 < 0:
			xPos = 0
		else:
			xPos = mouseX - width/2

		# xPos-=110

		self.SetPosition(xPos, mouseY-130)

		self.maxValueTextLine.SetText(" / " + str(maxValue))

		self.pickValueEditLine.SetText(str(unitValue))
		self.pickValueEditLine.SetFocus()

		ime.SetCursorPosition(1)

		self.itemSlot.SetItemSlot(0, itemVnum, maxValue)
		self.itemSlot.RefreshSlot()

		self.unitValue = unitValue
		self.maxValue = maxValue
		self.Show()
		self.SetTop()

	def Close(self):
		self.pickValueEditLine.KillFocus()
		self.Hide()
		self.OnOverOutItem()

	def OnAccept(self):

		text = self.pickValueEditLine.GetText()
		if len(text) > 0 and text.isdigit():
			money = int(text)
			money = min(money, self.maxValue)
			if money > 0:
				if self.eventAccept:
					self.eventAccept(money)

		self.Close()

	def OnOverInItem(self, slotNumber):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(self.itemVnum, 0)

	def OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()