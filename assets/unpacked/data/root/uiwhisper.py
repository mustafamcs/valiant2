import ui, net, chat, player, app, localeInfo, ime, chr, messenger, constInfo

class WhisperButton(ui.Button):
	def __init__(self):
		ui.Button.__init__(self, "TOP_MOST")

	def __del__(self):
		ui.Button.__del__(self)

	def SetToolTipText(self, text, x=0, y = 32):
		ui.Button.SetToolTipText(self, text, x, y)
		self.ToolTipText.Show()

	def SetToolTipTextWithColor(self, text, color, x=0, y = 32):
		ui.Button.SetToolTipText(self, text, x, y)
		self.ToolTipText.SetPackedFontColor(color)
		self.ToolTipText.Show()

	def ShowToolTip(self):
		if 0 != self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if 0 != self.ToolTipText:
			self.ToolTipText.Hide()

class WhisperDialog(ui.ScriptWindow):

	class TextRenderer(ui.Window):
		def SetTargetName(self, targetName):
			self.targetName = targetName

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			chat.RenderWhisper(self.targetName, x, y)

	class ResizeButton(ui.DragButton):

		def __init__(self):
			ui.DragButton.__init__(self)

		def __del__(self):
			ui.DragButton.__del__(self)

		def OnMouseOverIn(self):
			app.SetCursor(app.HVSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

	def __init__(self, eventMinimize, eventClose):
		ui.ScriptWindow.__init__(self)
		self.targetName = ""
		self.eventMinimize = eventMinimize
		self.eventClose = eventClose
		self.eventAcceptTarget = None
		if app.ENABLE_MULTI_LANGUAGE_SYSTEM and app.ENABLE_EXTENDED_WHISPER_DETAILS:
			self.countryID = 0

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/WhisperDialog.py")
		except:
			import exception
			exception.Abort("WhisperDialog.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.titleName = GetObject("titlename")
			self.titleNameEdit = GetObject("titlename_edit")

			if app.WJ_MULTI_TEXTLINE:
				self.titleName.DisableEnterToken()
				self.titleNameEdit.DisableEnterToken()

			self.closeButton = GetObject("closebutton")
			self.scrollBar = GetObject("scrollbar")
			self.chatLine = GetObject("chatline")
			self.minimizeButton = GetObject("minimizebutton")
			self.ignoreButton = GetObject("ignorebutton")
			self.acceptButton = GetObject("acceptbutton")
			self.sendButton = GetObject("sendbutton")
			self.board = GetObject("board")
			self.editBar = GetObject("editbar")
			self.gamemasterMark = GetObject("gamemastermark")
		except:
			import exception
			exception.Abort("DialogWindow.LoadDialog.BindObject")

		self.gamemasterMark.Hide()
		self.titleName.SetText("")
		self.titleNameEdit.SetText("")
		self.minimizeButton.SetEvent(ui.__mem_func__(self.Minimize))
		self.closeButton.SetEvent(ui.__mem_func__(self.Close))
		self.scrollBar.SetPos(1.0)
		self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.chatLine.SetReturnEvent(ui.__mem_func__(self.SendWhisper))
		self.chatLine.SetEscapeEvent(ui.__mem_func__(self.Minimize))
		self.chatLine.SetMultiLine()
		self.sendButton.SetEvent(ui.__mem_func__(self.SendWhisper))
		self.titleNameEdit.SetReturnEvent(ui.__mem_func__(self.AcceptTarget))
		self.titleNameEdit.SetEscapeEvent(ui.__mem_func__(self.Close))
		self.ignoreButton.SetToggleDownEvent(ui.__mem_func__(self.IgnoreTarget))
		self.ignoreButton.SetToggleUpEvent(ui.__mem_func__(self.IgnoreTarget))
		self.acceptButton.SetEvent(ui.__mem_func__(self.AcceptTarget))

		self.textRenderer = self.TextRenderer()
		self.textRenderer.SetParent(self)
		self.textRenderer.SetPosition(20, 28)
		self.textRenderer.SetTargetName("")
		self.textRenderer.Show()

		self.resizeButton = self.ResizeButton()
		self.resizeButton.SetParent(self)
		self.resizeButton.SetSize(20, 20)
		self.resizeButton.SetPosition(280, 180)
		self.resizeButton.SetMoveEvent(ui.__mem_func__(self.ResizeWhisperDialog))
		self.resizeButton.Show()

		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			self.countryFlag = ui.ExpandedImageBox()
			self.countryFlag.SetParent(self.board)
			self.countryFlag.SetPosition(115, 28)
			self.countryFlag.Show()

		self.ResizeWhisperDialog()

	def Destroy(self):

		self.eventMinimize = None
		self.eventClose = None
		self.eventAcceptTarget = None

		self.ClearDictionary()
		self.scrollBar.Destroy()
		self.titleName = None
		self.titleNameEdit = None
		self.closeButton = None
		self.scrollBar = None
		self.chatLine = None
		self.sendButton = None
		self.ignoreButton = None
		self.acceptButton = None
		self.minimizeButton = None
		self.textRenderer = None
		self.board = None
		self.editBar = None
		self.resizeButton = None
		
		if app.ENABLE_MULTI_LANGUAGE_SYSTEM and app.ENABLE_EXTENDED_WHISPER_DETAILS:
			self.countryFlag = None
			self.countryID = 0

	def ResizeWhisperDialog(self):
		(xPos, yPos) = self.resizeButton.GetLocalPosition()
		if xPos < 280:
			self.resizeButton.SetPosition(280, yPos)
			return
		if yPos < 150:
			self.resizeButton.SetPosition(xPos, 150)
			return
		self.SetWhisperDialogSize(xPos + 20, yPos + 20)


	def OnRunMouseWheel(self, nLen):
		if self.scrollBar:
			if nLen > 0:
				self.scrollBar.OnUp()
			else:
				self.scrollBar.OnDown()

	def SetWhisperDialogSize(self, width, height):
		try:

			max = int((width-90)/6) * 3 - 6
			self.board.SetSize(width, height)
			self.scrollBar.SetPosition(width-25, 35)
			self.scrollBar.SetScrollBarSize(height-100)
			self.scrollBar.SetPos(1.0)
			self.editBar.SetSize(width-18, 50)
			self.chatLine.SetSize(width-90, 40)
			self.chatLine.SetLimitWidth(width-90)
			self.SetSize(width, height)

			if 0 != self.targetName:
				chat.SetWhisperBoxSize(self.targetName, width - 50, height - 90)

			self.textRenderer.SetPosition(20, 28)
			self.scrollBar.SetPosition(width-25, 35)
			self.editBar.SetPosition(10, height-60)
			self.sendButton.SetPosition(width-80, 10)
			self.minimizeButton.SetPosition(width-42, 12)
			self.closeButton.SetPosition(width-24, 12)

			self.SetChatLineMax(max)

		except:
			import exception
			exception.Abort("WhisperDialog.SetWhisperDialogSize.BindObject")

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM and app.ENABLE_EXTENDED_WHISPER_DETAILS:
		def RequestCountryFlag(self, targetName):
			if targetName:
				net.SendWhisperDetails(targetName)

			if self.countryFlag:
				fixedWidth = 145
				self.countryFlag.SetPosition(fixedWidth, 11)

		def SetCountryFlag(self, countryID):
			self.countryID = countryID

			if countryID != 0:
				self.countryFlag.LoadImage("d:/ymir work/ui/login_new/flags/flag_%s_down.tga" % constInfo.LOCALE_LANG_DICT[countryID]["locale"])
				self.countryFlag.Show()
			else:
				self.countryFlag.Hide()


	def SetChatLineMax(self, max):
		self.chatLine.SetMax(max)

		from grpText import GetSplitingTextLine

		text = self.chatLine.GetText()
		if text:
			self.chatLine.SetText(GetSplitingTextLine(text, max, 0))

	def OpenWithTarget(self, targetName):
		chat.CreateWhisper(targetName)
		chat.SetWhisperBoxSize(targetName, self.GetWidth() - 60, self.GetHeight() - 90)
		self.chatLine.SetFocus()
		self.titleName.SetText(targetName)
		self.targetName = targetName
		self.textRenderer.SetTargetName(targetName)
		self.titleNameEdit.Hide()
		self.ignoreButton.Hide()

		self.acceptButton.Hide()
		self.gamemasterMark.Hide()
		self.minimizeButton.Show()

		if app.ENABLE_TELEPORT_TO_A_FRIEND:
			self.playerTeleport = ui.Button()
			self.playerTeleport.SetParent(self.board)
			self.playerTeleport.SetPosition(195+37, 10)
			self.playerTeleport.SetUpVisual("d:/ymir work/ui/game/ekstra/whisper/teleport_friend_0.png")
			self.playerTeleport.SetOverVisual("d:/ymir work/ui/game/ekstra/whisper/teleport_friend_1.png")
			self.playerTeleport.SetDownVisual("d:/ymir work/ui/game/ekstra/whisper/teleport_friend_2.png")
			self.playerTeleport.SetEvent(ui.__mem_func__(self.TeleportEvent))
			# self.playerTeleport.Show()

		if not messenger.IsFriendByName(self.targetName):
			self.friendButton = ui.Button()
			self.friendButton.SetParent(self.board)
			self.friendButton.SetPosition(145+37, 10)
			self.friendButton.SetUpVisual("d:/ymir work/ui/game/ekstra/whisper/add_friend_01.png")
			self.friendButton.SetOverVisual("d:/ymir work/ui/game/ekstra/whisper/add_friend_02.png")
			self.friendButton.SetDownVisual("d:/ymir work/ui/game/ekstra/whisper/add_friend_03.png")
			self.friendButton.SetText("")
			self.friendButton.SetEvent(ui.__mem_func__(self.AddFriend))
			if app.ENABLE_EXTENDED_WHISPER_DETAILS:
				self.friendButton.Show()
			else:
				self.friendButton.Hide()

			self.playerShopButton = ui.Button()
			self.playerShopButton.SetParent(self.board)
			self.playerShopButton.SetPosition(170+37, 10)
			self.playerShopButton.SetUpVisual("d:/ymir work/ui/game/ekstra/whisper/playershop_01.png")
			self.playerShopButton.SetOverVisual("d:/ymir work/ui/game/ekstra/whisper/playershop_02.png")
			self.playerShopButton.SetDownVisual("d:/ymir work/ui/game/ekstra/whisper/playershop_03.png")
			self.playerShopButton.SetEvent(lambda arg = targetName : self.SearchPlayerNameOnShops(arg))
			if app.ENABLE_SHOP_SEARCH:
				self.playerShopButton.Show()
			else:
				self.playerShopButton.Hide()
		else:

			self.playerShopButton = ui.Button()
			self.playerShopButton.SetParent(self.board)
			self.playerShopButton.SetPosition(145+37, 10)
			self.playerShopButton.SetUpVisual("d:/ymir work/ui/game/ekstra/whisper/playershop_01.png")
			self.playerShopButton.SetOverVisual("d:/ymir work/ui/game/ekstra/whisper/playershop_02.png")
			self.playerShopButton.SetDownVisual("d:/ymir work/ui/game/ekstra/whisper/playershop_03.png")
			self.playerShopButton.SetEvent(lambda arg = targetName : self.SearchPlayerNameOnShops(arg))
			if app.ENABLE_SHOP_SEARCH:
				self.playerShopButton.Show()
			else:
				self.playerShopButton.Hide()


		if app.ENABLE_PM_ALL_SEND_SYSTEM:
			if self.targetName in [localeInfo.SYSTEM_MESSAGE, localeInfo.DUNGEON_NOTIFICATION_TITLE, "[BIOLOG]"]:
				self.playerShopButton.Hide()
				self.playerTeleport.Hide()
				self.friendButton.Hide()
				self.chatLine.Disable()
				self.sendButton.Hide()
				self.countryFlag.Hide()
				return

		if app.ENABLE_MULTI_LANGUAGE_SYSTEM and app.ENABLE_EXTENDED_WHISPER_DETAILS:
			self.RequestCountryFlag(targetName)
			self.countryFlag.Hide()

	def AddFriend(self):
		net.SendMessengerAddByNamePacket(self.targetName)
		self.friendButton.Hide()
		self.playerShopButton.SetPosition(145+34, 10)
		self.playerTeleport.SetPosition(170+34, 10)

	def OpenWithoutTarget(self, event):
		self.eventAcceptTarget = event
		self.titleName.SetText("")
		self.titleNameEdit.SetText("")
		self.titleNameEdit.SetFocus()
		self.targetName = 0
		self.titleNameEdit.Show()
		self.ignoreButton.Hide()
		self.acceptButton.Show()
		self.minimizeButton.Hide()
		self.gamemasterMark.Hide()
		if app.ENABLE_MULTI_LANGUAGE_SYSTEM and app.ENABLE_EXTENDED_WHISPER_DETAILS:
			self.countryFlag.Hide()

	def SearchPlayerNameOnShops(self, targetName):
		if not self.interface.wndShopSearch.IsShow():
			self.interface.wndShopSearch.Show(True)
		self.interface.wndShopSearch.OnClearSearchData()
		self.interface.wndShopSearch.sItemName.SetText(targetName)
		self.interface.wndShopSearch.OnCheckBox()
		self.interface.wndShopSearch.OnSearch()

	def SetGameMasterLook(self):
		self.gamemasterMark.Show()

	def Minimize(self):
		self.titleNameEdit.KillFocus()
		self.chatLine.KillFocus()
		self.Hide()

		if None != self.eventMinimize:
			self.eventMinimize(self.targetName)

	def Close(self):
		chat.ClearWhisper(self.targetName)
		self.titleNameEdit.KillFocus()
		self.chatLine.KillFocus()
		self.Hide()

		if self.eventClose:
			self.eventClose(self.targetName)

	def IgnoreTarget(self):
		net.SendChatPacket("/ignore " + self.targetName)

	if app.ENABLE_TELEPORT_TO_A_FRIEND:
		def TeleportEvent(self):
			net.SendMessengerRequestWarpByNamePacket(self.targetName)
			self.playerTeleport.Hide()

	def AcceptTarget(self):
		name = self.titleNameEdit.GetText()
		if len(name) <= 0:
			self.Close()
			return

		if None != self.eventAcceptTarget:
			self.titleNameEdit.KillFocus()
			self.eventAcceptTarget(name)
			if app.ENABLE_MULTI_LANGUAGE_SYSTEM and app.ENABLE_EXTENDED_WHISPER_DETAILS:
				self.RequestCountryFlag(name)

	def OnScroll(self):
		chat.SetWhisperPosition(self.targetName, self.scrollBar.GetPos())

	def SendWhisper(self):

		text = self.chatLine.GetText()
		textLength = len(text)

		if app.ENABLE_PM_ALL_SEND_SYSTEM:
			if self.targetName in [localeInfo.SYSTEM_MESSAGE, localeInfo.DUNGEON_NOTIFICATION_TITLE, "[BIOLOG]"]:
				return

		if textLength > 0:
			if net.IsInsultIn(text):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHAT_INSULT_STRING)
				return

			if app.ENABLE_LINK_IN_CHAT:
				link = self.GetLink(text)
				if link != "":
					if not chr.IsGameMaster():
						text = text.replace(link, "|cFF00C0FC|h|Hweb:" + link.replace("://", "XxX") + "|h" + link + "|h|r")
					else:
						text = text.replace(link, "|cFF00C0FC|h|Hsysweb:" + link.replace("://", "XxX") + "|h" + link + "|h|r")

			net.SendWhisperPacket(self.targetName, text)
			self.chatLine.SetText("")

			chat.AppendWhisper(chat.WHISPER_TYPE_CHAT, self.targetName, player.GetName() + " : " + text)

	def OnTop(self):
		if self.chatLine:
			self.chatLine.SetFocus()

	def BindInterface(self, interface):
		self.interface = interface

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)

	if app.ENABLE_LINK_IN_CHAT:
		def GetLink(self, text):
			start = text.find("http://")
			if start == -1:
				start = text.find("https://")
			if start == -1:
				return ""

			return text[start:len(text)].split(" ")[0]
