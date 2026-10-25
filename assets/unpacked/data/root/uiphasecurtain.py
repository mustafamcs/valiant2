import grp, ui, wndMgr, systemSetting, constInfo

class PhaseCurtain(ui.Bar):

	def __init__(self):
		ui.Bar.__init__(self, "CURTAIN")
		self.speed = 0.1
		self.curAlpha = 0.0
		self.event = 0
		self.args = -1
		self.FadeInFlag = False
		self.SetWindowName("PhaseCurtain")
		self.AddFlag("float")

	def __del__(self):
		ui.Bar.__del__(self)

	def SAFE_FadeOut(self, event, args = -1):
		self.FadeOut(ui.__mem_func__(event), args)

	def FadeOut(self, event, args = -1):
		self.curAlpha = 0.0
		self.SetAlpha(self.curAlpha)
		self.Show()
		self.event = event
		self.args = args

	def FadeIn(self):
		self.event = 0
		self.FadeInFlag = True

	def SetAlpha(self, alpha):
		if getattr(systemSetting, "IsLoadingAnimated", lambda: 0)():
			if constInfo.CURTAIN_ACTIVE == 0:
				alpha = 0

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		color = grp.GenerateColor(0.0, 0.0, 0.0, alpha)
		self.SetColor(color)

	def OnUpdate(self):
		if 0 != self.event:
			self.curAlpha += self.speed
			if self.curAlpha >= 1.0:
				self.curAlpha = 1.0
				self.event()

		elif self.FadeInFlag:
			self.curAlpha -= self.speed
			if self.curAlpha <= 0.0:
				self.curAlpha = 0.0
				self.eventFadeIn = 0
				self.FadeInFlag = False
				self.Hide()

		self.SetAlpha(self.curAlpha)
