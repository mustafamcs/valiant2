__author__ = "Light05"
__system__ = "Client Optimisation - IntroLoading Renewal"
__date__ = "30.08.2022"
__ver__ = "0.15"

import ui, net, wndMgr, app

class LoadingWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, self)

		self.stream=stream
		self.loadingImage = None

	def __del__(self):
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, 0)
		ui.Window.__del__(self)

	def Open(self):

		self.loadingImage = ui.ExpandedImageBox()
		self.loadingImage.SetParent(self)
		self.loadingImage.SetPosition(0, 0)
		self.loadingImage.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.loadingImage.Show()

		self.loadingImage.LoadImage("d:/ymir work/uiloading/loading.jpg")

		width = float(wndMgr.GetScreenWidth()) / float(self.loadingImage.GetWidth())
		height = float(wndMgr.GetScreenHeight()) / float(self.loadingImage.GetHeight())

		self.loadingImage.SetScale(width, height)
		self.Show()

		net.SendSelectCharacterPacket(self.stream.GetCharacterSlot())

		app.SetFrameSkip(0)

	def Close(self):
		app.SetFrameSkip(1)
		self.loadingImage = None
		self.ClearDictionary()
		self.Hide()

	def OnPressEscapeKey(self):
		app.SetFrameSkip(1)
		self.stream.SetLoginPhase()
		return True