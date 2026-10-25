import app, net, ui, uiPhaseCurtain, constInfo, localeInfo, systemSetting, uiQuest, uiCommon, wndMgr

import introEmpire, introSelect, introCreate, intrologin, game, introLoading, exception

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.CloseEvent = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

	def Open(self, Message, event = 0, ButtonName = localeInfo.UI_CANCEL):
		if self.IsShow():
			self.Close()

		self.Lock()
		self.SetTop()
		self.CloseEvent = event

		AcceptButton = self.GetChild("accept")
		AcceptButton.SetText(ButtonName)
		AcceptButton.SetEvent(ui.__mem_func__(self.Close))

		self.GetChild("message").SetText(Message)
		self.Show()

	def Close(self):
		if not self.IsShow():
			self.CloseEvent = 0
			return

		self.Unlock()
		self.Hide()

		if self.CloseEvent:
			self.CloseEvent()
			self.CloseEvent = 0

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class MainStream(object):
	def __init__(self):
		net.SetHandler(self)
		net.SetTCPRecvBufferSize(128*1024)
		net.SetTCPSendBufferSize(4096)
		net.SetUDPRecvBufferSize(4096)

		self.id=""
		self.pwd=""
		self.clientVersion =""
		self.addr=""
		self.port=0
		self.account_addr=0
		self.account_port=0
		self.slot=0
		self.isAutoSelect=0
		self.isAutoLogin=0

		self.curtain = 0
		self.curPhaseWindow = 0
		self.newPhaseWindow = 0

	def __del__(self):
		if uiQuest.QuestDialog:
			if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
				uiQuest.QuestDialog.QuestCurtain.Hide() # Ghost gui fixed? lightwork correction
				uiQuest.QuestDialog.QuestCurtain.Close()
				del uiQuest.QuestDssialog.QuestCurtain

	def Destroy(self):

		if self.curPhaseWindow:
			self.curPhaseWindow.Close()
			del self.curPhaseWindow

		if self.newPhaseWindow:
			self.newPhaseWindow.Close()
			del self.newPhaseWindow

		if self.popupWindow:
			self.popupWindow.Destroy()
			del self.popupWindow

		if self.curtain:
			del self.curtain

	def Create(self):
		self.CreatePopupDialog()
		self.curtain = uiPhaseCurtain.PhaseCurtain()

	def SetPhaseWindow(self, newPhaseWindow):
		if self.newPhaseWindow:
			self.__ChangePhaseWindow()

		self.newPhaseWindow = newPhaseWindow

		if app.ENABLE_DISTANCE_SKILL_SELECT and constInfo.CHOOSE_SKILL:
			constInfo.CHOOSE_SKILL = 0

		if self.curPhaseWindow:
			self.curtain.FadeOut(self.__ChangePhaseWindow)
		else:
			self.__ChangePhaseWindow()

	def __ChangePhaseWindow(self):
		oldPhaseWindow=self.curPhaseWindow
		newPhaseWindow=self.newPhaseWindow
		self.curPhaseWindow=0
		self.newPhaseWindow=0

		if oldPhaseWindow:
			oldPhaseWindow.Close()

		if newPhaseWindow:
			newPhaseWindow.SetFocus()
			newPhaseWindow.Open()

		self.curPhaseWindow=newPhaseWindow

		if self.curPhaseWindow:
			self.curtain.FadeIn()
			#self.curPhaseWindow.SetFocus()
		else:
			app.Exit()

	def CreatePopupDialog(self):
		self.popupWindow = PopupDialog()
		self.popupWindow.LoadDialog()
		self.popupWindow.SetCenterPosition()
		self.popupWindow.Hide()

	def SetLoginPhase(self):
		net.Disconnect()
		self.SetPhaseWindow(intrologin.LoginWindow(self))

		if app.ENABLE_LOADING_WINDOW_RENEWAL:
			if constInfo.CURTAIN_ACTIVE == 0:
				constInfo.CURTAIN_ACTIVE = 1

	def SetSelectEmpirePhase(self):
		try:
			self.SetPhaseWindow(introEmpire.SelectEmpireWindow(self))
		except:
			exception.Abort("networkModule.SetSelectEmpirePhase")

	def SetReselectEmpirePhase(self):
		try:
			self.SetPhaseWindow(introEmpire.ReselectEmpireWindow(self))
		except:
			exception.Abort("networkModule.SetReselectEmpirePhase")

	def SetSelectCharacterPhase(self):
		try:
			localeInfo.LoadLocaleData()

			if self.popupWindow:
				self.popupWindow.Close()

			self.SetPhaseWindow(introSelect.SelectCharacterWindow(self))

			if app.ENABLE_LOADING_WINDOW_RENEWAL:
				if constInfo.CURTAIN_ACTIVE == 0:
					constInfo.CURTAIN_ACTIVE = 1
		except:
			exception.Abort("networkModule.SetSelectCharacterPhase")

	def SetCreateCharacterPhase(self):
		try:
			self.SetPhaseWindow(introCreate.CreateCharacterWindow(self))
		except:
			exception.Abort("networkModule.SetCreateCharacterPhase")

	def SetLoadingPhase(self):
		try:
			if app.ENABLE_LOADING_WINDOW_RENEWAL and systemSetting.IsLoadingAnimated() and not constInfo.CURTAIN_ACTIVE:
				class LoadingWindow(ui.ScriptWindow):
					def __init__(self, stream):
						ui.Window.__init__(self)
						net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, self)
						self.stream=stream

						self.loadingShadow = uiCommon.BackgroundShadow()
						self.loadingShadow.SetParent(self)
						self.loadingShadow.SetPosition(0, 0)
						self.loadingShadow.Hide()

					def __del__(self):
						net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, 0)
						ui.Window.__del__(self)

					def Open(self):
						net.SendSelectCharacterPacket(self.stream.GetCharacterSlot())
						app.SetFrameSkip(0)
						self.Show()
    
						self.loadingAnim = ui.AniImageBox()
						self.loadingAnim.SetParent(self.loadingShadow)
						self.loadingAnim.SetOnEndFrame(ui.__mem_func__(self.HideAnimation))

						for image in xrange(37, 0, -1):
							self.loadingAnim.AppendImage("d:/ymir work/ui/game/loading_logo/anim_{}-min.png".format(image))

						self.loadingAnim.SetDelay(1.5)
						self.loadingAnim.SetPosition((wndMgr.GetScreenWidth() - 750) / 2, (wndMgr.GetScreenHeight() - 433) / 2)
						self.loadingShadow.Show()
						self.loadingAnim.Show()
						
					def Close(self):
						app.SetFrameSkip(1)
						self.loadingAnim = None

					def OnPressEscapeKey(self):
						return True

					def HideAnimation(self):
						self.loadingAnim.Hide()
						self.loadingShadow.Hide()

				self.SetPhaseWindow(LoadingWindow(self))
			else:
				self.SetPhaseWindow(introLoading.LoadingWindow(self))

		except:
			exception.Abort("networkModule.SetLoadingPhase")

	def SetGamePhase(self):
		try:
			if self.popupWindow:
				self.popupWindow.Close()

			self.SetPhaseWindow(game.GameWindow(self))
		except:
			raise exception.Abort("networkModule.SetGamePhase")

	def Connect(self):
		if constInfo.KEEP_ACCOUNT_CONNETION_ENABLE:
			net.ConnectToAccountServer(self.addr, self.port, self.account_addr, self.account_port)
		else:
			net.ConnectTCP(self.addr, self.port)

	def SetConnectInfo(self, addr, port, account_addr=0, account_port=0):
		self.addr = addr
		self.port = port
		self.account_addr = account_addr
		self.account_port = account_port

	def GetConnectAddr(self):
		return self.addr

	def SetLoginInfo(self, id, pwd, clientVersion = ""):
		self.id = id
		self.pwd = pwd
		self.clientVersion = clientVersion
		net.SetLoginInfo(id, pwd, clientVersion)

	def CancelEnterGame(self):
		pass

	def SetCharacterSlot(self, slot):
		self.slot=slot

	def GetCharacterSlot(self):
		return self.slot

