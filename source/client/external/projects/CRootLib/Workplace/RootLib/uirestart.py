import dbg, app, net, ui

class RestartDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Constructor()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/restartdialog.py")

		except Exception, msg:
			import sys
			(type, msg, tb)=sys.exc_info()
			dbg.TraceError("RestartDialog.LoadDialog - %s:%s" % (type, msg))
			app.Abort()
			return 0

		try:
			self.restartHereButton=self.GetChild("restart_here_button")
			self.restartTownButton=self.GetChild("restart_town_button")
		except:
			import sys
			(type, msg, tb)=sys.exc_info()
			dbg.TraceError("RestartDialog.LoadDialog - %s:%s" % (type, msg))
			app.Abort()
			return 0

		self.restartHereButton.SetEvent(ui.__mem_func__(self.RestartHere))
		self.restartTownButton.SetEvent(ui.__mem_func__(self.RestartTown))

		self.respawnHereCurTime = ui.MakeTextLineNew(self.restartHereButton, 137, 5, "(%d)")
		self.respawnTownCurTime = ui.MakeTextLineNew(self.restartTownButton, 137, 5, "(%d)")
		return 1

	def Constructor(self):
		self.restartHereButton=None
		self.restartTownButton=None
		self.isClickedRespawnButton = False
		self.isClickedRespawnTownButton = False
		self.startHereTimer = 0
		self.startTownTimer = 0

	def Destroy(self):
		self.Constructor()
		self.ClearDictionary()

	def OpenDialog(self):
		self.Show()
		self.startHereTimer = app.GetTime() + 10
		self.startTownTimer = app.GetTime() + 10

	def Close(self):
		self.Hide()
		return True

	def RestartHere(self):
		self.startHereRemainingTime = self.startHereTimer-app.GetTime()

		if self.isClickedRespawnTownButton:
			return

		if self.startHereRemainingTime > 0:
			self.isClickedRespawnButton = True if self.isClickedRespawnButton == False else True
			return

		net.SendChatPacket("/restart_here")
		self.isClickedRespawnButton = False

	def RestartTown(self):
		self.startTownRemainingTime = self.startTownTimer-app.GetTime()

		if self.isClickedRespawnButton:
			return

		if self.startTownRemainingTime > 0:
			self.isClickedRespawnTownButton = True if self.isClickedRespawnTownButton == False else True
			return

		net.SendChatPacket("/restart_town")
		self.isClickedRespawnTownButton = False

	def OnPressExitKey(self):
		return True

	def OnPressEscapeKey(self):
		return True

	def ButtonImageSet(self, typeB, btnType = "RESTART"):

		if btnType == "RESTART":
			self.restartHereButton.SetUpVisual("d:/ymir work/ui/public/XLarge_Button_0{}.sub".format(typeB))
		else:
			self.restartTownButton.SetUpVisual("d:/ymir work/ui/public/XLarge_Button_0{}.sub".format(typeB))

	def OnUpdate(self):

		self.startHereRemainingTime = self.startHereTimer-app.GetTime()
		self.startTownRemainingTime = self.startTownTimer-app.GetTime()

		if self.startHereRemainingTime < 0:
			self.startHereRemainingTime = 0
		if self.startTownRemainingTime < 0:
			self.startTownRemainingTime = 0

		self.respawnHereCurTime.SetText("{:.02f}".format(self.startHereRemainingTime))
		self.respawnTownCurTime.SetText("{:.02f}".format((self.startTownRemainingTime)))

		if self.isClickedRespawnButton:
			if self.startHereRemainingTime <= 0:
				self.ButtonImageSet(1)
				self.RestartHere()
			else:
				self.ButtonImageSet(2)
		else:
			if self.startHereRemainingTime <= 0:
				self.ButtonImageSet(1)
			else:
				self.ButtonImageSet(3)

		if self.isClickedRespawnTownButton:
			if self.startTownRemainingTime <= 0:
				self.ButtonImageSet(1, "TOWN")
				self.RestartTown()
			else:
				self.ButtonImageSet(2, "TOWN")
		else:
			if self.startTownRemainingTime <= 0:
				self.ButtonImageSet(1, "TOWN")
			else:
				self.ButtonImageSet(3, "TOWN")
