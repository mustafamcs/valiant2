import app
if app.ENABLE_MESSENGER_TEAM:
	import app, ui, grp, net, guild, messenger, localeInfo, constInfo, uiToolTip, uiCommon

	FRIEND = 0
	GUILD = 1
	IMG_DIR = "new_messenger/"

	class MessengerItem(ui.Window):

		def __init__(self, getParentEvent):
			ui.Window.__init__(self)

			self.SetParent(getParentEvent())
			self.AddFlag("float")

			self.name = ""
			self.image = ui.ImageBox()
			self.image.AddFlag("not_pick")
			self.image.SetParent(self)
			self.image.Show()
			self.text = ui.TextLine()
			self.text.SetParent(self)
			if app.WJ_MULTI_TEXTLINE:
				self.text.DisableEnterToken()
			self.text.SetPosition(20, 2)
			self.text.Show()

			self.lovePoint = -1
			self.lovePointToolTip = None

			self.isSelected = False

			self.flag = ui.ImageBox()
			self.flag.AddFlag("not_pick")
			self.flag.SetParent(self)
			self.flag.SetPosition(0, 2)
			self.flag.Hide()

			# self.flag.Hide()

			self.getParentEvent = getParentEvent

		def SetName(self, name):
			self.name = name
			if name:
				self.text.SetText(name)
				self.SetSize(20 + 6*len(name) + 4, 16)

		def SetLangFlag(self, lang):
			self.flag.LoadImage("d:/ymir work/ui/game/flag/{}.tga".format(lang))
			self.text.SetPosition(40, 2)
			self.image.SetPosition(20, 2)
			self.flag.Show()

		def SetLovePoint(self, lovePoint):
			self.lovePoint = lovePoint

		def Select(self):
			self.isSelected = True

		def UnSelect(self):
			self.isSelected = False

		def GetName(self):
			return self.name

		def GetStepWidth(self):
			return 0

		# Whisper
		def CanWhisper(self):
			return False

		def IsOnline(self):
			return False

		def OnWhisper(self):
			pass

		# Remove
		def CanRemove(self):
			return False

		def OnRemove(self):
			return False

		# Warp
		def CanWarp(self):
			return False

		def OnWarp(self):
			pass

		def OnMouseOverIn(self):
			if -1 != self.lovePoint:
				if not self.lovePointToolTip:
					self.lovePointToolTip = uiToolTip.ToolTip(100)
					self.lovePointToolTip.SetTitle(self.name)
					self.lovePointToolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))
					self.lovePointToolTip.ResizeToolTip()
				self.lovePointToolTip.ShowToolTip()

		def OnMouseOverOut(self):
			if self.lovePointToolTip:
				self.lovePointToolTip.HideToolTip()

		def OnMouseLeftButtonDown(self):
			self.getParentEvent().OnSelectItem(self)

		def OnMouseLeftButtonDoubleClick(self):
			self.getParentEvent().OnDoubleClickItem(self)

		def OnRender(self):
			if self.isSelected:
				x, y = self.GetGlobalPosition()
				grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
				grp.RenderBar(x+16, y, self.GetWidth()-16, self.GetHeight())

	class MessengerMemberItem(MessengerItem):

		STATE_OFFLINE = 0
		STATE_ONLINE = 1
		IMAGE_FILE_NAME = {	"ONLINE" : "d:/ymir work/ui/game/windows/messenger_list_online.sub",
							"OFFLINE" : "d:/ymir work/ui/game/windows/messenger_list_offline.sub", }

		def __init__(self, getParentEvent):
			MessengerItem.__init__(self, getParentEvent)
			self.key = None
			self.state = self.STATE_OFFLINE
			self.Offline()

		def GetStepWidth(self):
			return 15

		def SetKey(self, key):
			self.key = key

		def IsSameKey(self, key):
			return self.key == key

		def IsOnline(self):
			if self.STATE_ONLINE == self.state:
				return True

			return False

		def Online(self):
			self.image.LoadImage(self.IMAGE_FILE_NAME["ONLINE"])
			self.state = self.STATE_ONLINE

		def Offline(self):
			self.image.LoadImage(self.IMAGE_FILE_NAME["OFFLINE"])
			self.state = self.STATE_OFFLINE

		def CanWhisper(self):
			if self.IsOnline():
				return True

			return False

		def OnWhisper(self):
			if self.IsOnline():
				self.getParentEvent().whisperButtonEvent(self.GetName())

		def Select(self):
			MessengerItem.Select(self)

	class MessengerGroupItem(MessengerItem):

		IMAGE_FILE_NAME = {	"OPEN" : "d:/ymir work/ui/game/windows/messenger_list_open.sub",
							"CLOSE" : "d:/ymir work/ui/game/windows/messenger_list_close.sub", }

		def __init__(self, getParentEvent):
			self.isOpen = False
			self.memberList = []

			MessengerItem.__init__(self, getParentEvent)

		def AppendMember(self, member, key, name, flag=None):
			member.SetKey(key)
			member.SetName(name)
			if flag != None:
				member.SetLangFlag(flag)

			self.memberList.append(member)
			return member

		def RemoveMember(self, item):
			for i in xrange(len(self.memberList)):
				if item == self.memberList[i]:
					del self.memberList[i]
					return

		def ClearMember(self):
			self.memberList = []

		def FindMember(self, key):
			list = filter(lambda argMember, argKey=key: argMember.IsSameKey(argKey), self.memberList)
			if list:
				return list[0]

			return None

		def GetLoginMemberList(self):
			return filter(MessengerMemberItem.IsOnline, self.memberList)

		def GetLogoutMemberList(self):
			return filter(lambda arg: not arg.IsOnline(), self.memberList)

		def IsOpen(self):
			return self.isOpen

		def Open(self):
			self.image.LoadImage(self.IMAGE_FILE_NAME["OPEN"])
			self.isOpen = True

		def Close(self):
			self.image.LoadImage(self.IMAGE_FILE_NAME["CLOSE"])
			self.isOpen = False

			map(ui.Window.Hide, self.memberList)

		def Select(self):

			if self.IsOpen():
				self.Close()
			else:
				self.Open()

			MessengerItem.Select(self)
			self.getParentEvent().OnRefreshList()

	class MessengerFriendItem(MessengerMemberItem):

		def __init__(self, getParentEvent):
			MessengerMemberItem.__init__(self, getParentEvent)

		def CanRemove(self):
			return True

		def OnRemove(self):
			messenger.RemoveFriend(self.key)
			net.SendMessengerRemovePacket(self.key, self.name)
			return True

		if app.ENABLE_TELEPORT_TO_A_FRIEND:
			def CanWarp(self):
				if not self.IsOnline():
					return False
				return True
				
			def OnWarp(self):
				net.SendMessengerRequestWarpByNamePacket(self.name)

	if app.ENABLE_MESSENGER_TEAM:
		class MessengerTeamItem(MessengerMemberItem):

			def __init__(self, getParentEvent):
				MessengerMemberItem.__init__(self, getParentEvent)

			def CanRemove(self):
				return FALSE
			
			def OnRemove(self):
				return FALSE

	class MessengerGuildItem(MessengerMemberItem):

		def __init__(self, getParentEvent):
			MessengerMemberItem.__init__(self, getParentEvent)

		def CanWarp(self):
			if not self.IsOnline():
				return False
			return True

		def OnWarp(self):
			net.SendGuildUseSkillPacket(155, self.key)

		def CanRemove(self):
			for i in xrange(guild.ENEMY_GUILD_SLOT_MAX_COUNT):
				if guild.GetEnemyGuildName(i) != "":
					return False

			if guild.MainPlayerHasAuthority(guild.AUTH_REMOVE_MEMBER):
				if guild.IsMemberByName(self.name):
					return True

			return False

		def OnRemove(self):
			net.SendGuildRemoveMemberPacket(self.key)
			return True

	class MessengerFriendGroup(MessengerGroupItem):

		def __init__(self, getParentEvent):
			MessengerGroupItem.__init__(self, getParentEvent)
			self.SetName(localeInfo.MESSENGER_FRIEND)

		def AppendMember(self, key, name):
			item = MessengerFriendItem(self.getParentEvent)
			return MessengerGroupItem.AppendMember(self, item, key, name)

	class MessengerBlockGroup(MessengerGroupItem):

		def __init__(self, getParentEvent):
			MessengerGroupItem.__init__(self, getParentEvent)
			self.SetName(localeInfo.MESSENGER_FRIEND)

		def AppendMember(self, key, name):
			item = MessengerFriendItem(self.getParentEvent)
			return MessengerGroupItem.AppendMember(self, item, key, name)
				

	if app.ENABLE_MESSENGER_TEAM:
		class MessengerTeamGroup(MessengerGroupItem):

			def __init__(self, getParentEvent):
				MessengerGroupItem.__init__(self, getParentEvent)
				self.SetName(localeInfo.MESSENGER_SUPPORT)

			def AppendMember(self, key, name):
				item = MessengerTeamItem(self.getParentEvent)
				getFlag = constInfo.MESSENGER_GM_FLAGLIST.get(key, None)

				return MessengerGroupItem.AppendMember(self, item, key, name, getFlag)
					

	class MessengerGuildGroup(MessengerGroupItem):

		def __init__(self, getParentEvent):
			MessengerGroupItem.__init__(self, getParentEvent)
			self.SetName(localeInfo.MESSENGER_GUILD)
			self.AddFlag("float")

		def AppendMember(self, key, name):
			item = MessengerGuildItem(self.getParentEvent)
			return MessengerGroupItem.AppendMember(self, item, key, name)

	class MessengerFamilyGroup(MessengerGroupItem):

		def __init__(self, getParentEvent):
			MessengerGroupItem.__init__(self, getParentEvent)
			self.SetName(localeInfo.MESSENGER_FAMILY)
			self.AddFlag("float")

			self.lover = None

		def AppendMember(self, key, name):
			item = MessengerGuildItem(self.getParentEvent)
			self.lover = item
			return MessengerGroupItem.AppendMember(self, item, key, name)

		def GetLover(self):
			return self.lover

	###################################################################################################
	###################################################################################################
	###################################################################################################

	class MessengerWindow(ui.ScriptWindow):

		START_POSITION = 95

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			messenger.SetMessengerHandler(self)

			self.board = None
			self.groupList = []
			self.showingItemList = []
			self.selectedItem = None
			self.whisperButtonEvent = lambda *arg: None
			self.familyGroup = None
			self.scrollBar = None

			self.guildButtonEvent = None

			self.showingPageSize = 0
			self.startLine = 0

			self.isLoaded = 0

			self.pageIdx = 0

			self.__AddGroup()
			messenger.RefreshGuildMember()

		def Show(self):
			if self.isLoaded==0:
				self.isLoaded=1

				self.__LoadWindow()
				self.OnRefreshList()
				if app.ENABLE_WINDOW_ANIMATION:
					self.SetWindowAnimation()
			ui.ScriptWindow.Show(self)

		def __LoadWindow(self):

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/MessengerWindow.py")

			try:
				self.board = self.GetChild("board")
				self.whisperButton = self.GetChild("WhisperButton")
				self.removeButton = self.GetChild("RemoveButton")
				self.addFriendButton = self.GetChild("AddFriendButton")
				self.guildButton = self.GetChild("GuildButton")
			except:
				import exception
				exception.Abort("MessengerWindow.__LoadWindow.__Bind")

			self.board.SetCloseEvent(ui.__mem_func__(self.Close))

			self.whisperButton.SetEvent(ui.__mem_func__(self.OnPressWhisperButton))
			self.removeButton.SetEvent(ui.__mem_func__(self.OnPressRemoveButton))
			self.addFriendButton.SetEvent(ui.__mem_func__(self.OnPressAddFriendButton))
			self.guildButton.SetEvent(ui.__mem_func__(self.OnPressGuildButton))

			self.blockButton = self.GetChild("BlockButton")
			self.blockButton.SetEvent(ui.__mem_func__(self.OnPressBlockButton))
			self.blockButton.Disable()
			self.scrollBar = ScrollBarSpecial()
			self.scrollBar.SetParent(self.GetChild("page_bg"))
			self.scrollBar.SetPosition(149 - 10, 32)
			self.scrollBar.SetSize(7, 175)
			self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
			self.scrollBar.Show()

			for j in xrange(4):
				self.GetChild("page_{}_btn".format(j)).SAFE_SetEvent(self.__ClickPage, j)

			self.GetChild("search_btn").SetEvent(ui.__mem_func__(self.OnRefreshList))
			self.GetChild("clear_btn").SetEvent(ui.__mem_func__(self.__ClearSearch))
			self.GetChild("editline").OnPressEscapeKey = ui.__mem_func__(self.Close)
			self.GetChild("editline").OnIMEUpdate = ui.__mem_func__(self.OnIMEUpdate)

			self.whisperButton.Disable()
			self.removeButton.Disable()

			self.__ClickPage(0)

		def OnPressBlockButton(self):
			pass

		def __ClearSearch(self):
			self.GetChild("editline").SetText("")
			self.OnRefreshList()
		def OnIMEUpdate(self):
			editline = self.GetChild("editline")
			while True:
				if editline.GetTextSize()[0] >= 100:
					text = editline.GetText()
					editline.SetText(text[:len(text)-2])
				else:
					break
			ui.EditLine.OnIMEUpdate(editline)
			self.OnRefreshList()

		def __ClickRadioButton(self, buttonList, buttonIndex):
			try:
				selButton = buttonList[buttonIndex]
			except IndexError:
				return
			for eachButton in buttonList:
				eachButton.SetUp()
			selButton.Down()

		def __ClickPage(self, pageIdx):
			if self.pageIdx == pageIdx:
				return
			self.__ClickRadioButton([self.GetChild("page_{}_btn".format(j)) for j in xrange(4)], pageIdx)
			self.GetChild("page_bg").LoadImage("{}page_{}.png".format(IMG_DIR, pageIdx))
			self.pageIdx = pageIdx
			self.OnRefreshList()

		def __del__(self):
			messenger.SetMessengerHandler(None)
			ui.ScriptWindow.__del__(self)

		def Destroy(self):
			self.board = None
			self.scrollBar = None
			self.resizeButton = None
			self.friendNameBoard = None
			self.questionDialog = None
			self.popupDialog = None
			self.inputDialog = None
			self.familyGroup = None

			self.whisperButton = None
			self.removeButton = None

		def OnCloseQuestionDialog(self):
			if self.questionDialog:
				self.questionDialog.Close()
			self.questionDialog = None
			return True

		def Close(self):
			self.questionDialog = None
			self.Hide()

		def SetSize(self, width, height):
			ui.ScriptWindow.SetSize(self, width, height)
			if self.board:
				self.board.SetSize(width, height)

		def __LocateMember(self):

			if self.isLoaded==0:
				return

			yPos = self.START_POSITION
			heightLimit = 175

			map(ui.Window.Hide, self.showingItemList)

			for item in self.showingItemList[self.startLine:]:
				item.SetPosition(8 + item.GetStepWidth(), yPos)
				item.SetTop()
				item.Show()
				yPos+=20
				if yPos >= self.START_POSITION + heightLimit:
					break

			totalY = len(self.showingItemList) * 20

			if totalY > heightLimit:
				self.scrollBar.SetScale(heightLimit, totalY)
			else:
				self.scrollBar.SetPos(0)
				self.scrollBar.SetScale(175, 175)

		def __AddGroup(self):
			member = MessengerFriendGroup(ui.__mem_func__(self.GetSelf))
			member.Open()
			member.Show()
			self.groupList.append(member)

			member = MessengerGuildGroup(ui.__mem_func__(self.GetSelf))
			member.Open()
			member.Show()
			self.groupList.append(member)

			member = MessengerBlockGroup(ui.__mem_func__(self.GetSelf))
			member.Open()
			member.Show()
			self.groupList.append(member)

			if app.ENABLE_MESSENGER_TEAM:
				member = MessengerTeamGroup(ui.__mem_func__(self.GetSelf))
				member.Open()
				member.Show()
				self.groupList.append(member)

		def __AddFamilyGroup(self):
			member = MessengerFamilyGroup(ui.__mem_func__(self.GetSelf))
			member.Open()
			member.Show()

			self.familyGroup = member

		def ClearGuildMember(self):
			self.groupList[GUILD].ClearMember()

		def SetWhisperButtonEvent(self, event):
			self.whisperButtonEvent=event

		def SetGuildButtonEvent(self, event):
			self.guildButtonEvent=event

		def OnCloseInputDialog(self):
			self.inputDialog.Close()
			self.inputDialog = None
			return True

		def OnPressGuildButton(self):
			self.guildButtonEvent()

		def OnPressAddFriendButton(self):
			friendNameBoard = uiCommon.InputDialog()
			friendNameBoard.SetTitle(localeInfo.MESSENGER_ADD_FRIEND)
			friendNameBoard.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend))
			friendNameBoard.SetCancelEvent(ui.__mem_func__(self.OnCancelAddFriend))
			friendNameBoard.Open()
			self.friendNameBoard = friendNameBoard

		def OnAddFriend(self):
			text = self.friendNameBoard.GetText()
			if text:
				net.SendMessengerAddByNamePacket(text)
			if self.friendNameBoard:
				self.friendNameBoard.Close()
			self.friendNameBoard = None
			return True

		def OnCancelAddFriend(self):
			self.friendNameBoard.Close()
			self.friendNameBoard = None
			return True

		def OnPressWhisperButton(self):
			if self.selectedItem:
				self.selectedItem.OnWhisper()

		def OnPressRemoveButton(self):
			if self.selectedItem:
				if self.selectedItem.CanRemove():
					self.questionDialog = uiCommon.QuestionDialog()
					self.questionDialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE)
					self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnRemove))
					self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
					self.questionDialog.Open()

		def OnRemove(self):
			if self.selectedItem:
				if self.selectedItem.CanRemove():
					map(lambda arg, argDeletingItem=self.selectedItem: arg.RemoveMember(argDeletingItem), self.groupList)
					self.selectedItem.OnRemove()
					self.selectedItem.UnSelect()
					self.selectedItem = None
					self.OnRefreshList()

			self.OnCloseQuestionDialog()

		def OnScroll(self):
			scrollLineCount = len(self.showingItemList)

			startLine = int(scrollLineCount * self.scrollBar.GetPos())

			if startLine != self.startLine:
				if startLine+9 > scrollLineCount:
					startLine = scrollLineCount - 9
				if startLine < 0:
					startLine = 0

				self.startLine = startLine
				self.__LocateMember()

		def OnPressEscapeKey(self):
			self.Close()
			return True

		## CallBack
		def OnSelectItem(self, item):

			if self.selectedItem:
				if item != self.selectedItem:
					self.selectedItem.UnSelect()

			self.selectedItem = item

			if self.selectedItem:
				self.selectedItem.Select()

				if self.selectedItem.CanWhisper():
					self.whisperButton.Enable()
				else:
					self.whisperButton.Disable()

				if self.selectedItem.CanRemove():
					self.removeButton.Enable()
				else:
					self.removeButton.Disable()

		def OnDoubleClickItem(self, item):

			if not self.selectedItem:
				return

			if self.selectedItem.IsOnline():
				self.OnPressWhisperButton()

		def GetSelf(self):
			return self

		def OnRefreshList(self):
			map(ui.Window.Hide, self.groupList)
			map(ui.Window.Hide, self.showingItemList)
			self.showingItemList = []

			if self.familyGroup:
				if self.familyGroup.GetLover() and self.pageIdx == 0:
					self.showingItemList.append(self.familyGroup.GetLover())

			searchText = self.GetChild("editline").GetText().lower() if self.IsChild("editline") else ""

			group = self.groupList[self.pageIdx]
			loginMemberList = group.GetLoginMemberList()
			logoutMemberList = group.GetLogoutMemberList()

			if loginMemberList or logoutMemberList:
				for member in loginMemberList:
					if searchText != "":
						if member.name.lower().find(searchText) == -1:
							continue
				
					self.showingItemList.append(member)
				for member in logoutMemberList:
					if searchText != "":
						if member.name.lower().find(searchText) == -1:
							continue
					self.showingItemList.append(member)

			self.startLine = 0
			if self.scrollBar:
				self.scrollBar.SetPos(0)
			self.__LocateMember()

		def RefreshMessenger(self):
			self.OnRefreshList()

		## EventHandler
		def __AddList(self, groupIndex, key, name):
			group = self.groupList[groupIndex]
			member = group.FindMember(key)
			if not member:
				member = group.AppendMember(key, name)
				self.OnSelectItem(None)
			return member

		def OnRemoveList(self, groupIndex, key):
			group = self.groupList[groupIndex]
			group.RemoveMember(group.FindMember(key))
			self.OnRefreshList()

		def OnRemoveAllList(self, groupIndex):
			group = self.groupList[groupIndex]
			group.ClearMember()
			self.OnRefreshList()

		def OnLogin(self, groupIndex, key, name=None):
			if not name:
				name = key

			member = self.__AddList(groupIndex, key, name)
			member.SetName(name)
			member.Online()
			self.OnRefreshList()

			if not name in constInfo.ALREADY_NOTIFY_LIST:
				self.onlinePopup = uiCommon.OnlinePopup()
				self.onlinePopup.SetUserName(name)
				self.onlinePopup.SetEvent(ui.__mem_func__(self.OpenWhisper), "MOUSE_LEFT_BUTTON_UP", name)
				self.onlinePopup.SlideIn()
			
				constInfo.ALREADY_NOTIFY_LIST.append(name)

		def OpenWhisper(self, eventType, userName):
			self.whisperButtonEvent(userName)

		def OnLogout(self, groupIndex, key, name=None):
			member = self.__AddList(groupIndex, key, name)
			if not name:
				name = key
			member.SetName(name)
			member.Offline()
			self.OnRefreshList()

		def OnAddLover(self, name, lovePoint):
			if not self.familyGroup:
				self.__AddFamilyGroup()

			member = self.familyGroup.AppendMember(0, name)

			member.SetName(name)
			member.SetLovePoint(lovePoint)
			member.Offline()
			self.OnRefreshList()

		def OnUpdateLovePoint(self, lovePoint):
			if not self.familyGroup:
				return

			lover = self.familyGroup.GetLover()
			if not lover:
				return

			lover.SetLovePoint(lovePoint)

		def OnLoginLover(self):
			if not self.familyGroup:
				return

			lover = self.familyGroup.GetLover()
			if not lover:
				return

			lover.Online()

		def OnLogoutLover(self):
			if not self.familyGroup:
				return

			lover = self.familyGroup.GetLover()
			if not lover:
				return

			lover.Offline()

		def ClearLoverInfo(self):
			if not self.familyGroup:
				return

			self.familyGroup.ClearMember()
			self.familyGroup = None
			self.OnRefreshList()

	from operator import truediv
	class ScrollBarSpecial(ui.Window):
		BASE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
		CORNERS_AND_LINES_COLOR = grp.GenerateColor(0.3411, 0.3411, 0.3411, 1.0)
		BAR_NUMB = 9 #This is static value! Please dont touch in him.
		SCROLL_WIDTH= 8
		class MiddleBar(ui.DragButton):
			MIDDLE_BAR_COLOR = grp.GenerateColor(78.0 / 255.0, 65.0 / 255.0, 51.0 / 255.0, 1.0)
			def __init__(self, horizontal_scroll):
				ui.DragButton.__init__(self)
				self.AddFlag("movable")
				self.horizontal_scroll = horizontal_scroll
				self.middle = ui.Bar()
				self.middle.SetParent(self)
				self.middle.AddFlag("attach")
				self.middle.AddFlag("not_pick")
				self.middle.SetColor(self.MIDDLE_BAR_COLOR)
				self.middle.SetSize(1, 1)
				self.middle.Show()
			def SetStaticScale(self, size):
				(base_width, base_height) = (self.middle.GetWidth(), self.middle.GetHeight())
				if not self.horizontal_scroll:
					ui.DragButton.SetSize(self, base_width, size)
					self.middle.SetSize(base_width, size)
				else:
					ui.DragButton.SetSize(self, size, base_height)
					self.middle.SetSize(size, base_height)
			def SetSize(self, selfSize, fullSize):
				(base_width, base_height) = (self.middle.GetWidth(), self.middle.GetHeight())
				
				if not self.horizontal_scroll:
					ui.DragButton.SetSize(self, base_width, truediv(int(selfSize), int(fullSize)) * selfSize)
					self.middle.SetSize(base_width, truediv(int(selfSize), int(fullSize)) * selfSize)
				else:
					ui.DragButton.SetSize(self, truediv(int(selfSize), int(fullSize)) * selfSize, base_height)
					self.middle.SetSize(truediv(int(selfSize), int(fullSize)) * selfSize, base_height)
			def SetStaticSize(self, size):
				size = max(2, size)
				
				if not self.horizontal_scroll:
					ui.DragButton.SetSize(self, size, self.middle.GetHeight())
					self.middle.SetSize(size, self.middle.GetHeight())
				else:
					ui.DragButton.SetSize(self, self.middle.GetWidth(), size)
					self.middle.SetSize(self.middle.GetWidth(), size)
		def __init__(self, horizontal_scroll = False):
			ui.Window.__init__(self)
			self.horizontal_scroll = horizontal_scroll
			self.scrollEvent = None
			self.scrollSpeed = 50
			self.sizeScale = 1.0
			self.bars = []
			for i in xrange(self.BAR_NUMB):
				br = ui.Bar()
				br.SetParent(self)
				br.AddFlag("attach")
				br.AddFlag("not_pick")
				br.SetColor([self.CORNERS_AND_LINES_COLOR, self.BASE_COLOR][i == (self.BAR_NUMB-1)])
				if not (i % 2 == 0): br.SetSize(1, 1)
				br.Show()
				self.bars.append(br)
			self.middleBar = self.MiddleBar(self.horizontal_scroll)
			self.middleBar.SetParent(self)
			self.middleBar.SetMoveEvent(ui.__mem_func__(self.OnScrollMove))
			self.middleBar.Show()
		def OnScrollMove(self):
			if not self.scrollEvent:
				return
			arg = float(self.middleBar.GetLocalPosition()[1] - 1) / float(self.GetHeight() - 2 - self.middleBar.GetHeight()) if not self.horizontal_scroll else\
					float(self.middleBar.GetLocalPosition()[0] - 1) / float(self.GetWidth() - 2 - self.middleBar.GetWidth())
			self.scrollEvent(arg)
		def SetScrollEvent(self, func):
			self.scrollEvent = func
		def SetScrollSpeed(self, speed):
			self.scrollSpeed = speed
		def OnMouseWheel(self, length):
			if not self.IsShow():
				return False
			length = int((length * 0.01) * self.scrollSpeed)
			if not self.horizontal_scroll:
				val = min(max(1, self.middleBar.GetLocalPosition()[1] - (length * 0.01) * self.scrollSpeed * self.sizeScale), self.GetHeight() - self.middleBar.GetHeight() - 1)
				self.middleBar.SetPosition(1, val)
			else:
				val = min(max(1, self.middleBar.GetLocalPosition()[0] - (length * 0.01) *  self.scrollSpeed * self.sizeScale), self.GetWidth() - self.middleBar.GetWidth() - 1)
				self.middleBar.SetPosition(val, 1)
			self.OnScrollMove()
			return True
		def GetPos(self):
			return float(self.middleBar.GetLocalPosition()[1] - 1) / float(self.GetHeight() - 2 - self.middleBar.GetHeight()) if not self.horizontal_scroll else float(self.middleBar.GetLocalPosition()[0] - 1) / float(self.GetWidth() - 2 - self.middleBar.GetWidth())
		def OnMouseLeftButtonDown(self):
			(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
			if not self.horizontal_scroll:
				if xMouseLocalPosition == 0 or xMouseLocalPosition == self.GetWidth():
					return
				y_pos = (yMouseLocalPosition - self.middleBar.GetHeight() / 2)
				self.middleBar.SetPosition(1, y_pos)
			else:
				if yMouseLocalPosition == 0 or yMouseLocalPosition == self.GetHeight():
					return
				x_pos = (xMouseLocalPosition - self.middleBar.GetWidth() / 2)
				self.middleBar.SetPosition(x_pos, 1)
			self.OnScrollMove()
		def SetSize(self, w, h):
			(width, height) = (max(3, w), max(3, h))
			ui.Window.SetSize(self, width, height)
			self.bars[0].SetSize(1, (height - 2))
			self.bars[0].SetPosition(0, 1)
			self.bars[2].SetSize((width - 2), 1)
			self.bars[2].SetPosition(1, 0)
			self.bars[4].SetSize(1, (height - 2))
			self.bars[4].SetPosition((width - 1), 1)
			self.bars[6].SetSize((width - 2), 1)
			self.bars[6].SetPosition(1, (height - 1))
			self.bars[8].SetSize((width - 2), (height - 2))
			self.bars[8].SetPosition(1, 1)
			self.bars[1].SetPosition(0, 0)
			self.bars[3].SetPosition((width - 1), 0)
			self.bars[5].SetPosition((width - 1), (height - 1))
			self.bars[7].SetPosition(0, (height - 1))
			if not self.horizontal_scroll:
				self.middleBar.SetStaticSize(width - 2)
				self.middleBar.SetSize(12, self.GetHeight())
			else:
				self.middleBar.SetStaticSize(height - 2)
				self.middleBar.SetSize(12, self.GetWidth())
			self.middleBar.SetRestrictMovementArea(1, 1, width - 2, height - 2)
		def SetScale(self, selfSize, fullSize):
			self.sizeScale = float(selfSize)/float(fullSize)
			if self.sizeScale <= 0.0305:
				self.sizeScale = 0.05
			self.middleBar.SetSize(selfSize, fullSize)
		def SetStaticScale(self, r_size):
			self.middleBar.SetStaticScale(r_size)
		def SetPosScale(self, fScale):
			pos = (math.ceil((self.GetHeight() - 2 - self.middleBar.GetHeight()) * fScale) + 1) if not self.horizontal_scroll else (math.ceil((self.GetWidth() - 2 - self.middleBar.GetWidth()) * fScale) + 1)
			self.SetPos(pos)
		def SetPos(self, pos):
			wPos = (1, pos) if not self.horizontal_scroll else (pos, 1)
			self.middleBar.SetPosition(*wPos)

else:
	import app
	import ui
	import grp
	import net
	import guild
	import messenger
	import localeInfo
	import constInfo
	import uiToolTip
	import uiGameOption

	import uiCommon
	from _weakref import proxy

	FRIEND = 0
	GUILD = 1

	class MessengerItem(ui.Window):

		def __init__(self, getParentEvent):
			ui.Window.__init__(self)

			self.SetParent(getParentEvent())
			self.AddFlag("float")

			self.name = ""
			self.image = ui.ImageBox()
			self.image.AddFlag("not_pick")
			self.image.SetParent(self)
			self.image.Show()
			self.text = ui.TextLine()
			self.text.SetParent(self)
			self.text.SetPosition(20, 2)
			self.text.Show()

			self.lovePoint = -1
			self.lovePointToolTip = None

			self.isSelected = False

			self.getParentEvent = getParentEvent

		def SetName(self, name):
			self.name = name
			if name:
				self.text.SetText(name)
				self.SetSize(20 + 6*len(name) + 4, 16)

				if localeInfo.IsARABIC():
					self.text.SetPosition(20 + 6*len(name) + 4, 2)

		def SetLovePoint(self, lovePoint):
			self.lovePoint = lovePoint

		def Select(self):
			self.isSelected = True

		def UnSelect(self):
			self.isSelected = False

		def GetName(self):
			return self.name

		def GetStepWidth(self):
			return 0

		# Whisper
		def CanWhisper(self):
			return False

		def IsOnline(self):
			return False

		def OnWhisper(self):
			pass

		# Remove
		def CanRemove(self):
			return False

		def OnRemove(self):
			return False

		# Warp
		def CanWarp(self):
			return False

		def OnWarp(self):
			pass

		def OnMouseOverIn(self):
			if -1 != self.lovePoint:
				if not self.lovePointToolTip:
					self.lovePointToolTip = uiToolTip.ToolTip(100)
					self.lovePointToolTip.SetTitle(self.name)
					self.lovePointToolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))
					self.lovePointToolTip.ResizeToolTip()
				self.lovePointToolTip.ShowToolTip()

		def OnMouseOverOut(self):
			if self.lovePointToolTip:
				self.lovePointToolTip.HideToolTip()

		def OnMouseLeftButtonDown(self):
			self.getParentEvent().OnSelectItem(self)

		def OnMouseLeftButtonDoubleClick(self):
			self.getParentEvent().OnDoubleClickItem(self)

		def OnRender(self):
			if self.isSelected:
				x, y = self.GetGlobalPosition()
				grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
				grp.RenderBar(x+16, y, self.GetWidth()-16, self.GetHeight())

	class MessengerMemberItem(MessengerItem):

		STATE_OFFLINE = 0
		STATE_ONLINE = 1

		IMAGE_FILE_NAME = {	"ONLINE" : "d:/ymir work/ui/game/windows/messenger_list_online.sub",
							"OFFLINE" : "d:/ymir work/ui/game/windows/messenger_list_offline.sub", }

		def __init__(self, getParentEvent):
			MessengerItem.__init__(self, getParentEvent)
			self.key = None
			self.state = self.STATE_OFFLINE
			self.Offline()

		def GetStepWidth(self):
			return 15

		def SetKey(self, key):
			self.key = key

		def IsSameKey(self, key):
			return self.key == key

		def IsOnline(self):
			if self.STATE_ONLINE == self.state:
				return True

			return False

		def Online(self):
			self.image.LoadImage(self.IMAGE_FILE_NAME["ONLINE"])
			self.state = self.STATE_ONLINE

		def Offline(self):
			self.image.LoadImage(self.IMAGE_FILE_NAME["OFFLINE"])
			self.state = self.STATE_OFFLINE

		def CanWhisper(self):
			if self.IsOnline():
				return True

			return False

		def OnWhisper(self):
			if self.IsOnline():
				self.getParentEvent().whisperButtonEvent(self.GetName())

		def Select(self):
			MessengerItem.Select(self)

	class MessengerGroupItem(MessengerItem):

		IMAGE_FILE_NAME = {	"OPEN" : "d:/ymir work/ui/game/windows/messenger_list_open.sub",
							"CLOSE" : "d:/ymir work/ui/game/windows/messenger_list_close.sub", }

		def __init__(self, getParentEvent):
			self.isOpen = False
			self.memberList = []

			MessengerItem.__init__(self, getParentEvent)

		def AppendMember(self, member, key, name):
			member.SetKey(key)
			member.SetName(name)
			self.memberList.append(member)
			return member

		def RemoveMember(self, item):
			for i in xrange(len(self.memberList)):
				if item == self.memberList[i]:
					del self.memberList[i]
					return

		def ClearMember(self):
			self.memberList = []

		def FindMember(self, key):
			list = filter(lambda argMember, argKey=key: argMember.IsSameKey(argKey), self.memberList)
			if list:
				return list[0]

			return None

		def GetLoginMemberList(self):
			return filter(MessengerMemberItem.IsOnline, self.memberList)

		def GetLogoutMemberList(self):
			return filter(lambda arg: not arg.IsOnline(), self.memberList)

		def IsOpen(self):
			return self.isOpen

		def Open(self):
			self.image.LoadImage(self.IMAGE_FILE_NAME["OPEN"])
			self.isOpen = True

		def Close(self):
			self.image.LoadImage(self.IMAGE_FILE_NAME["CLOSE"])
			self.isOpen = False

			map(ui.Window.Hide, self.memberList)

		def Select(self):

			if self.IsOpen():
				self.Close()
			else:
				self.Open()

			MessengerItem.Select(self)
			self.getParentEvent().OnRefreshList()

	class MessengerFriendItem(MessengerMemberItem):

		def __init__(self, getParentEvent):
			MessengerMemberItem.__init__(self, getParentEvent)

		def CanRemove(self):
			return True

		def OnRemove(self):
			messenger.RemoveFriend(self.key)
			net.SendMessengerRemovePacket(self.key, self.name)
			return True

	class MessengerGuildItem(MessengerMemberItem):

		def __init__(self, getParentEvent):
			MessengerMemberItem.__init__(self, getParentEvent)

		def CanWarp(self):
			if not self.IsOnline():
				return False
			return True

		def OnWarp(self):
			net.SendGuildUseSkillPacket(155, self.key)

		def CanRemove(self):
			for i in xrange(guild.ENEMY_GUILD_SLOT_MAX_COUNT):
				if guild.GetEnemyGuildName(i) != "":
					return False

			if guild.MainPlayerHasAuthority(guild.AUTH_REMOVE_MEMBER):
				if guild.IsMemberByName(self.name):
					return True

			return False

		def OnRemove(self):
			net.SendGuildRemoveMemberPacket(self.key)
			return True

	class MessengerFriendGroup(MessengerGroupItem):

		def __init__(self, getParentEvent):
			MessengerGroupItem.__init__(self, getParentEvent)
			self.SetName(localeInfo.MESSENGER_FRIEND)

		def AppendMember(self, key, name):
			item = MessengerFriendItem(self.getParentEvent)
			return MessengerGroupItem.AppendMember(self, item, key, name)

	class MessengerGuildGroup(MessengerGroupItem):

		def __init__(self, getParentEvent):
			MessengerGroupItem.__init__(self, getParentEvent)
			self.SetName(localeInfo.MESSENGER_GUILD)
			self.AddFlag("float")

		def AppendMember(self, key, name):
			item = MessengerGuildItem(self.getParentEvent)
			return MessengerGroupItem.AppendMember(self, item, key, name)

	class MessengerFamilyGroup(MessengerGroupItem):

		def __init__(self, getParentEvent):
			MessengerGroupItem.__init__(self, getParentEvent)
			self.SetName(localeInfo.MESSENGER_FAMILY)
			self.AddFlag("float")

			self.lover = None

		def AppendMember(self, key, name):
			item = MessengerGuildItem(self.getParentEvent)
			self.lover = item
			return MessengerGroupItem.AppendMember(self, item, key, name)

		def GetLover(self):
			return self.lover

	###################################################################################################
	###################################################################################################
	###################################################################################################

	class MessengerWindow(ui.ScriptWindow):

		START_POSITION = 40

		class ResizeButton(ui.DragButton):

			def OnMouseOverIn(self):
				app.SetCursor(app.VSIZE)

			def OnMouseOverOut(self):
				app.SetCursor(app.NORMAL)

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			messenger.SetMessengerHandler(self)

			self.board = None
			self.groupList = []
			self.showingItemList = []
			self.selectedItem = None
			self.whisperButtonEvent = lambda *arg: None
			self.familyGroup = None

			self.guildButtonEvent = None

			self.showingPageSize = 0
			self.startLine = 0

			self.isLoaded = 0

			self.__AddGroup()
			messenger.RefreshGuildMember()

		def Show(self):
			if self.isLoaded==0:
				self.isLoaded=1

				self.__LoadWindow()
				self.OnRefreshList()
				self.OnResizeDialog()

			ui.ScriptWindow.Show(self)

		def __LoadWindow(self):

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/MessengerWindow.py")

			try:
				self.board = self.GetChild("board")
				self.scrollBar = self.GetChild("ScrollBar")
				self.whisperButton = self.GetChild("WhisperButton")
				self.removeButton = self.GetChild("RemoveButton")
				self.addFriendButton = self.GetChild("AddFriendButton")
				self.guildButton = self.GetChild("GuildButton")
			except:
				import exception
				exception.Abort("MessengerWindow.__LoadWindow.__Bind")

			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
			self.whisperButton.SetEvent(ui.__mem_func__(self.OnPressWhisperButton))
			self.removeButton.SetEvent(ui.__mem_func__(self.OnPressRemoveButton))
			self.addFriendButton.SetEvent(ui.__mem_func__(self.OnPressAddFriendButton))
			self.guildButton.SetEvent(ui.__mem_func__(self.OnPressGuildButton))

			width = self.GetWidth()
			height = self.GetHeight()
			self.addFriendButton.SetPosition(-60, 30)
			self.whisperButton.SetPosition(-20, 30)
			self.removeButton.SetPosition(20, 30)
			self.guildButton.SetPosition(60, 30)

			self.whisperButton.Disable()
			self.removeButton.Disable()

			resizeButton = self.ResizeButton()
			resizeButton.AddFlag("restrict_x")
			resizeButton.SetParent(self)
			resizeButton.SetSize(self.GetWidth(), 10)
			resizeButton.SetWindowVerticalAlignBottom()
			resizeButton.SetPosition(0, 0)
			resizeButton.Show()
			self.resizeButton = resizeButton
			self.resizeButton.SetMoveEvent(ui.__mem_func__(self.OnResizeDialog))
			self.resizeButton.SetPosition(0, 300)

			for list in self.groupList:
				list.SetTop()

		def __del__(self):
			messenger.SetMessengerHandler(None)
			ui.ScriptWindow.__del__(self)

		@ui.WindowDestroy
		def Destroy(self):
			self.board = None
			self.scrollBar = None
			self.resizeButton = None
			self.friendNameBoard = None
			self.questionDialog = None
			self.popupDialog = None
			self.inputDialog = None
			self.familyGroup = None

			self.whisperButton = None
			self.removeButton = None

		def OnCloseQuestionDialog(self):
			self.questionDialog.Close()
			self.questionDialog = None
			return True

		def Close(self):
			self.questionDialog = None
			self.Hide()

		def SetSize(self, width, height):
			ui.ScriptWindow.SetSize(self, width, height)
			if self.board:
				self.board.SetSize(width, height)

		def OnResizeDialog(self):
			x, y = self.resizeButton.GetLocalPosition()
			if y < 140:
				self.resizeButton.SetPosition(x, 140)
				return
			self.SetSize(self.GetWidth(), y + self.resizeButton.GetHeight())

			self.showingPageSize = y - (self.START_POSITION + 26)
			self.scrollBar.SetScrollBarSize(self.showingPageSize)

			self.__LocateMember()

			self.resizeButton.TurnOffCallBack()
			self.UpdateRect()
			self.resizeButton.TurnOnCallBack()

		def __LocateMember(self):

			if self.isLoaded==0:
				return

			if self.showingPageSize/20 >= len(self.showingItemList):
				self.scrollBar.Hide()
				self.startLine = 0
			else:
				if self.showingItemList:
					self.scrollBar.SetMiddleBarSize(float(self.showingPageSize/20) / float(len(self.showingItemList)))
				self.scrollBar.Show()

			#####

			yPos = self.START_POSITION
			heightLimit = self.GetHeight() - (self.START_POSITION + 13)

			map(ui.Window.Hide, self.showingItemList)

			for item in self.showingItemList[self.startLine:]:
				item.SetPosition(20 + item.GetStepWidth(), yPos)
				item.SetTop()
				item.Show()

				yPos += 20
				if yPos > heightLimit:
					break

		def __AddGroup(self):
			member = MessengerFriendGroup(ui.__mem_func__(self.GetSelf))
			member.Open()
			member.Show()
			self.groupList.append(member)

			member = MessengerGuildGroup(ui.__mem_func__(self.GetSelf))
			member.Open()
			member.Show()
			self.groupList.append(member)

		def __AddFamilyGroup(self):
			member = MessengerFamilyGroup(ui.__mem_func__(self.GetSelf))
			member.Open()
			member.Show()

			self.familyGroup = member

		def ClearGuildMember(self):
			self.groupList[GUILD].ClearMember()

		def SetWhisperButtonEvent(self, event):
			self.whisperButtonEvent=event

		def SetGuildButtonEvent(self, event):
			self.guildButtonEvent=event

		def OnCloseInputDialog(self):
			self.inputDialog.Close()
			self.inputDialog = None
			return True

		def OnPressGuildButton(self):
			self.guildButtonEvent()

		def OnPressAddFriendButton(self):
			friendNameBoard = uiCommon.InputDialog()
			friendNameBoard.SetTitle(localeInfo.MESSENGER_ADD_FRIEND)
			friendNameBoard.SetAcceptEvent(ui.__mem_func__(self.OnAddFriend))
			friendNameBoard.SetCancelEvent(ui.__mem_func__(self.OnCancelAddFriend))
			friendNameBoard.Open()
			self.friendNameBoard = friendNameBoard

		def OnAddFriend(self):
			text = self.friendNameBoard.GetText()
			if text:
				net.SendMessengerAddByNamePacket(text)
			self.friendNameBoard.Close()
			self.friendNameBoard = None
			return True

		def OnCancelAddFriend(self):
			self.friendNameBoard.Close()
			self.friendNameBoard = None
			return True

		def OnPressWhisperButton(self):
			if self.selectedItem:
				self.selectedItem.OnWhisper()

		def OnPressRemoveButton(self):
			if self.selectedItem:
				if self.selectedItem.CanRemove():
					self.questionDialog = uiCommon.QuestionDialog()
					self.questionDialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE)
					self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnRemove))
					self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
					self.questionDialog.Open()

		def OnRemove(self):
			if self.selectedItem:
				if self.selectedItem.CanRemove():
					map(lambda arg, argDeletingItem=self.selectedItem: arg.RemoveMember(argDeletingItem), self.groupList)
					self.selectedItem.OnRemove()
					self.selectedItem.UnSelect()
					self.selectedItem = None
					self.OnRefreshList()

			self.OnCloseQuestionDialog()

		def OnScroll(self):
			scrollLineCount = len(self.showingItemList) - (self.showingPageSize/20)
			startLine = int(scrollLineCount * self.scrollBar.GetPos())

			if startLine != self.startLine:
				self.startLine = startLine
				self.__LocateMember()

		def OnPressEscapeKey(self):
			self.Close()
			return True

		## CallBack
		def OnSelectItem(self, item):

			if self.selectedItem:
				if item != self.selectedItem:
					self.selectedItem.UnSelect()

			self.selectedItem = item

			if self.selectedItem:
				self.selectedItem.Select()

				if self.selectedItem.CanWhisper():
					self.whisperButton.Enable()
				else:
					self.whisperButton.Disable()

				if self.selectedItem.CanRemove():
					self.removeButton.Enable()
				else:
					self.removeButton.Disable()

		def OnDoubleClickItem(self, item):

			if not self.selectedItem:
				return

			if self.selectedItem.IsOnline():
				self.OnPressWhisperButton()

		def GetSelf(self):
			return self

		def OnRefreshList(self):
			self.showingItemList = []

			if self.familyGroup:
				self.showingItemList.append(self.familyGroup)
				if self.familyGroup.GetLover():
					self.showingItemList.append(self.familyGroup.GetLover())

			for group in self.groupList:

				self.showingItemList.append(group)

				if group.IsOpen():

					loginMemberList = group.GetLoginMemberList()
					logoutMemberList = group.GetLogoutMemberList()

					if loginMemberList or logoutMemberList:
						for member in loginMemberList:
							self.showingItemList.append(member)
						for member in logoutMemberList:
							self.showingItemList.append(member)

					else:
						item = MessengerItem(ui.__mem_func__(self.GetSelf))
						item.SetName(localeInfo.MESSENGER_EMPTY_LIST)
						self.showingItemList.append(item)

			self.__LocateMember()

		def RefreshMessenger(self):
			self.OnRefreshList()

		## EventHandler
		def __AddList(self, groupIndex, key, name):
			group = self.groupList[groupIndex]
			member = group.FindMember(key)
			if not member:
				member = group.AppendMember(key, name)
				self.OnSelectItem(None)
			return member

		def OnRemoveList(self, groupIndex, key):
			group = self.groupList[groupIndex]
			group.RemoveMember(group.FindMember(key))
			self.OnRefreshList()

		def OnRemoveAllList(self, groupIndex):
			group = self.groupList[groupIndex]
			group.ClearMember()
			self.OnRefreshList()

		def OnLogin(self, groupIndex, key, name=None):
			if not name:
				name = key
			group = self.groupList[groupIndex]
			member = self.__AddList(groupIndex, key, name)
			member.SetName(name)
			member.Online()
			self.OnRefreshList()

		def OnLogout(self, groupIndex, key, name=None):
			group = self.groupList[groupIndex]
			member = self.__AddList(groupIndex, key, name)
			if not name:
				name = key
			member.SetName(name)
			member.Offline()
			self.OnRefreshList()

		def OnAddLover(self, name, lovePoint):
			if not self.familyGroup:
				self.__AddFamilyGroup()

			member = self.familyGroup.AppendMember(0, name)

			member.SetName(name)
			member.SetLovePoint(lovePoint)
			member.Offline()
			self.OnRefreshList()

		def OnUpdateLovePoint(self, lovePoint):
			if not self.familyGroup:
				return

			lover = self.familyGroup.GetLover()
			if not lover:
				return

			lover.SetLovePoint(lovePoint)

		def OnLoginLover(self):
			if not self.familyGroup:
				return

			lover = self.familyGroup.GetLover()
			if not lover:
				return

			lover.Online()

		def OnLogoutLover(self):
			if not self.familyGroup:
				return

			lover = self.familyGroup.GetLover()
			if not lover:
				return

			lover.Offline()

		def ClearLoverInfo(self):
			if not self.familyGroup:
				return

			self.familyGroup.ClearMember()
			self.familyGroup = None
			self.OnRefreshList()

