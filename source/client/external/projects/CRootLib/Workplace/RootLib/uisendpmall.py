import ui, app, net, ime, chr, uiScriptLocale

class AdminWhisperManager(ui.Window):

	height = 500
	width = 175

	def __init__(self):
		ui.Window.__init__(self)

		self.maxCharacter = 512
		self.UI_Elements = { }
		self.__CreateUI()

		self.__BuildKeyDict()

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.Window.__del__(self)

	def __CreateUI(self):
		self.UI_Elements["MainBoard"] = ui.BoardWithTitleBar()
		self.UI_Elements["MainBoard"].SetSize(500, self.width)
		self.UI_Elements["MainBoard"].SetCenterPosition()
		self.UI_Elements["MainBoard"].AddFlag('movable')
		self.UI_Elements["MainBoard"].AddFlag('float')
		self.UI_Elements["MainBoard"].SetTitleName(uiScriptLocale.SEND_WHISPER_ADMIN_TITLE)
		self.UI_Elements["MainBoard"].SetCloseEvent(self.Close)
		self.UI_Elements["MainBoard"].Show()

		self.UI_Elements["Char_Counter_Text"] = ui.TextLine()
		self.UI_Elements["Char_Counter_Text"].SetParent(self.UI_Elements["MainBoard"])
		self.UI_Elements["Char_Counter_Text"].SetPosition(458, self.width-25)
		self.UI_Elements["Char_Counter_Text"].SetText("0/%d" % (self.maxCharacter))
		self.UI_Elements["Char_Counter_Text"].Show()

		self.UI_Elements["Message_Slotbar"] = ui.SlotBar()
		self.UI_Elements["Message_Slotbar"].SetParent(self.UI_Elements["MainBoard"])
		self.UI_Elements["Message_Slotbar"].SetSize(478, 90)
		self.UI_Elements["Message_Slotbar"].SetPosition(10, 35)
		self.UI_Elements["Message_Slotbar"].Show()
		
		self.UI_Elements["Message_Editline"] = ui.EditLine()
		self.UI_Elements["Message_Editline"].SetParent(self.UI_Elements["Message_Slotbar"])
		self.UI_Elements["Message_Editline"].SetSize(478, 90)
		self.UI_Elements["Message_Editline"].SetPosition(7, 3)
		self.UI_Elements["Message_Editline"].SetMax(self.maxCharacter)
		self.UI_Elements["Message_Editline"].SetLimitWidth(469)
		self.UI_Elements["Message_Editline"].SetMultiLine()
		self.UI_Elements["Message_Editline"].SetText("")
		self.UI_Elements["Message_Editline"].SetOverlayText(uiScriptLocale.SEND_WHISPER_ADMIN_INFO)
	
		self.UI_Elements["Message_Editline"].Show()
		self.UI_Elements["Message_Editline"].OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)

		self.UI_Elements["Send_Button"] = ui.Button()
		self.UI_Elements["Send_Button"].SetParent(self.UI_Elements["MainBoard"])
		self.UI_Elements["Send_Button"].SetPosition(180, self.width-35)
		self.UI_Elements["Send_Button"].SetUpVisual('offlineshop/lightwork/searchshop/btn_filter_norm.png')
		self.UI_Elements["Send_Button"].SetOverVisual('offlineshop/lightwork/searchshop/btn_filter_hover.png')
		self.UI_Elements["Send_Button"].SetDownVisual('offlineshop/lightwork/searchshop/btn_filter_down.png')
		self.UI_Elements["Send_Button"].SetText(uiScriptLocale.WHISPER_SEND)
		self.UI_Elements["Send_Button"].SetEvent(self.__SendFunc)
		self.UI_Elements["Send_Button"].Show()

		self.UI_Elements["Clear_Button"] = ui.Button()
		self.UI_Elements["Clear_Button"].SetParent(self.UI_Elements["MainBoard"])
		self.UI_Elements["Clear_Button"].SetPosition(self.UI_Elements["MainBoard"].GetWidth() - 50, 8)
		self.UI_Elements["Clear_Button"].SetUpVisual("d:/ymir work/ui/game/guild/Refresh_Button_01.sub")
		self.UI_Elements["Clear_Button"].SetOverVisual("d:/ymir work/ui/game/guild/Refresh_Button_02.sub")
		self.UI_Elements["Clear_Button"].SetDownVisual("d:/ymir work/ui/game/guild/Refresh_Button_03.sub")
		self.UI_Elements["Clear_Button"].SetToolTipText(uiScriptLocale.CHATTING_SETTING_CLEAR)
		self.UI_Elements["Clear_Button"].SetEvent(self.__RefreshFunc)
		self.UI_Elements["Clear_Button"].Show()

	def __SetColor(self, newColor):
		self.SelectedColor = newColor
		self.UI_Elements["Message_Editline"].SetText("%s" % (self.ColorCodes[self.Colors.index(self.SelectedColor)]))

	def __RefreshFunc(self):
		self.UI_Elements["Message_Editline"].SetText("")
		self.UI_Elements["Char_Counter_Text"].SetText("0/%d" % (self.maxCharacter))

	def __SendFunc(self):
		text = self.UI_Elements["Message_Editline"].GetText()
		text = text.replace(" ", "$")

		net.SendBulkWhisperPacket(str(text))

	def __PasteFunc(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			from ui import EnablePaste
			EnablePaste(True)

			ime.PasteTextFromClipBoard()

			EnablePaste(False)

	def __BuildKeyDict(self):
		onPressKeyDict = {}
		onPressKeyDict[app.DIK_V] = lambda : self.__PasteFunc()
		self.onPressKeyDict = onPressKeyDict
	
	def OnKeyDown(self, key):
		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise
		return True

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.UI_Elements["Message_Editline"])
	
		text = self.UI_Elements["Message_Editline"].GetText()
		self.UI_Elements["Char_Counter_Text"].SetText("%d/%d" % (len(text), self.maxCharacter))

	def OpenWindow(self):
		if not chr.IsGameMaster(0):
			return

		if self.UI_Elements["MainBoard"].IsShow():
			self.UI_Elements["MainBoard"].Hide()
		else:
			self.UI_Elements["MainBoard"].Show()
	
	def Close(self):
		self.UI_Elements["MainBoard"].Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True