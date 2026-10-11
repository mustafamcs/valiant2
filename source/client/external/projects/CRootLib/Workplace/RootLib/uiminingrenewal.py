# builtins
import app
import wndMgr
# root modules
import ui
import math
import net, chat
import ime, constInfo, localeInfo

class MiningWindow(ui.ScriptWindow):
	MINING_PATH = "d:/ymir work/ui/game/miningrenewal/"
	EFFECT_SIZE = 42 # Don't change this.

	# duration of "Miss", "Hit", and the wave
	EFFECT_DURATION = 0.3 # seconds

	HIT_WAIT = 1 # seconds
	MISS_PENALTY = 0.5 # seconds 

	# Fishing game duration
	FISHING_TIME_LIMIT = 30 # seconds
	# Number of hits required for a successful game
	HIT_TARGET_NUM = 100

	IS_MINING = 0

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__FullReset()

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		self.__FullReset()
		ui.ScriptWindow.__del__(self)

	def __FullReset(self):
		self.isLoaded = 0

		self.shiningImage = None
		self.effectContainer = None
		self.missEffect = None
		self.hitEffect = None
		self.backgroundCave = None
		self.goalCircle = None
		self.totalPointsText = None
		self.timerGauge = None
		# self.navigationArea = None
		self.board = None
		self.waveEffect = None

		self.__Reset()

	def __Reset(self):
		self.endTime = 0
		self.clickTime = 0
		self.nextHit = 0
		self.nextCourse = 0
		self.courseX = 0
		self.courseY = 0
		self.hits = 0
		self.canHit = False

		self.OnMouseOverOut()

	def Destroy(self):
		self.ClearDictionary()
		self.__FullReset()
		self.Hide()

	def Close(self, bForce = False):
		if self.IS_MINING or bForce:
			net.SendChatPacket("/mining_event_renewal 2")
			self.IS_MINING = 0
		self.__FullReset()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()

	def StartMining(self, miningPoint):

		self.HIT_TARGET_NUM = miningPoint
		self.__Reset()

		self.GetPickaxePoint()
		self.__Load()
		self.totalPointsText.SetText("{}/{}".format(self.hits, self.HIT_TARGET_NUM))

		# Give the fish a random initial position
		self.shiningImage.SetPosition(self.courseX, self.courseY)

		self.Show()

		self.endTime = app.GetTime() + self.FISHING_TIME_LIMIT

		self.IS_MINING = 1

		deg = app.GetRandom(0, 360)
		xPos, yPos = app.GetRandom(-35, 35), app.GetRandom(-100, -15)

		self.shiningImage.SetRotation(deg)
		self.shiningImage.SetPosition(xPos, yPos)

	def Show(self):
		self.__Load()
		ui.ScriptWindow.Show(self)

	def Open(self):
		self.Show()

	def __Load(self):
		if self.isLoaded:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/miningrenewal.py")
		except:
			import exception
			exception.Abort("MiningGame.__Load.UIScript/miningrenewal.py")

		try:
			self.board = self.GetChild('board')
			self.backgroundCave = self.GetChild('background_cave')
			self.goalCircle = self.GetChild('fishing_goal_circle')
			self.totalPointsText = self.GetChild('totalPoints')
			self.timerGauge = self.GetChild('fishing_timer_gauge')
			# self.navigationArea = self.GetChild('fishing_water_navArea')
		except:
			import exception
			exception.Abort("MiningGame.__Load.BindObject")

		try:
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.backgroundCave.SAFE_SetStringEvent("MOUSE_OVER_IN",self.OnMouseOverIn)
			self.backgroundCave.SAFE_SetStringEvent("MOUSE_OVER_OUT",self.OnMouseOverOut)
			self.backgroundCave.OnMouseLeftButtonDown = ui.__mem_func__(self.OnMouseLeftButtonDownEvent)
		except:
			import exception
			exception.Abort("MiningGame.__Load.BindEvent")

		self.effectContainer = ui.ScriptWindow()
		self.effectContainer.SetParent(self.backgroundCave)
		self.effectContainer.SetSize(0, 0)

		(cx, cy) = self.goalCircle.GetLocalPosition()
		(cw, ch) = (self.goalCircle.GetWidth(), self.goalCircle.GetHeight())

		# Set the effect container in the center of the circle(Origin point)
		self.effectContainer.SetPosition(cx + cw/2  - 10, cy + ch/2)
		self.effectContainer.Show()

		self.shiningImage = ui.AniImageBox()
		self.shiningImage.SetParent(self.effectContainer)
		self.shiningImage.AppendImage(self.MINING_PATH + "shining.png")
		self.shiningImage.AppendImage(self.MINING_PATH + "shining2.png")
		self.shiningImage.AppendImage(self.MINING_PATH + "shining3.png")
		self.shiningImage.AppendImage(self.MINING_PATH + "shining4.png")
		self.shiningImage.AppendImage(self.MINING_PATH + "shining5.png")
		self.shiningImage.AppendImage(self.MINING_PATH + "shining6.png")
		self.shiningImage.AppendImage(self.MINING_PATH + "shining7.png")
		self.shiningImage.AppendImage(self.MINING_PATH + "shining8.png")
		self.shiningImage.AppendImage(self.MINING_PATH + "shining9.png")
		self.shiningImage.AppendImage(self.MINING_PATH + "shining10.png")
		self.shiningImage.SetDelay(6)
		self.shiningImage.SetSize(20, 32)
		self.shiningImage.Show()

		self.missEffect = ui.AniImageBox()
		self.missEffect.SetParent(self.effectContainer)
		self.missEffect.AppendImage(self.MINING_PATH + "fishing_effect_miss.sub")

		self.hitEffect = ui.AniImageBox()
		self.hitEffect.SetParent(self.effectContainer)
		self.hitEffect.AppendImage(self.MINING_PATH + "fishing_effect_hit.sub")

		self.waveEffect = ui.AniImageBox()
		self.waveEffect.SetParent(self.effectContainer)
		self.waveEffect.AppendImage(self.MINING_PATH + "wave/mining_particle.sub")
		self.waveEffect.AppendImage(self.MINING_PATH + "wave/mining_particle2.sub")
		self.waveEffect.AppendImage(self.MINING_PATH + "wave/mining_particle3.sub")
		self.waveEffect.AppendImage(self.MINING_PATH + "wave/mining_particle4.sub")

	def OnMouseLeftButtonDownEvent(self):
		self.clickTime = app.GetTime()

		if (self.clickTime < self.nextHit):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MINING_EVENT_RENEWAL_HIT_DELAY)
			return

		if self.shiningImage:
			gw, gh = self.shiningImage.GetLocalPosition()
			fw, fh = self.shiningImage.GetWidth(), self.shiningImage.GetHeight()
			mx, my = wndMgr.GetMouseLocalPosition(self.effectContainer.hWnd)

			deg = app.GetRandom(0, 360)
			self.xPos, self.yPos = app.GetRandom(-35, 35), app.GetRandom(-100, -15)

		if ((mx >= gw) and (mx <= (gw + fw)) and ((my) >= gh) and (my <= (gh + fh-10))):

			self.CreateHitEffect(mx, my - self.EFFECT_SIZE) # - size to raise it a little higher

			self.hits += constInfo.MINING_POINT
			self.totalPointsText.SetText("{}/{}".format(self.hits, self.HIT_TARGET_NUM))

			net.SendChatPacket("/mining_event_renewal 0")

			self.nextHit = self.clickTime + self.HIT_WAIT #app.GetTime() + self.HIT_WAIT
		else:
			self.endTime -= self.MISS_PENALTY
			self.timerGauge.SetDiffuseColor(1, 0, 0, 1)
			self.CreateMissEffect(mx, my - self.EFFECT_SIZE) # - size to raise it a little higher

		self.shiningImage.SetRotation(deg)
		self.shiningImage.SetPosition(self.xPos, self.yPos)

		self.CreateWaveEffect(mx-15, my-10, 10)

	def OnUpdate(self):
		appTime = app.GetTime()

		if appTime >= self.endTime and self.IS_MINING:
			self.Close()
		else:
			if self.hits >= self.HIT_TARGET_NUM and self.IS_MINING:
				self.IS_MINING = 0
				self.Close()

	def OnRender(self):
		if self.timerGauge:
			self.timerGauge.SetPercentage(max(0, self.endTime - app.GetTime()), self.FISHING_TIME_LIMIT)

			if app.GetTime() > (self.clickTime + self.EFFECT_DURATION):
				self.timerGauge.SetDiffuseColor(1, 1, 1, 1)
				self.hitEffect.Hide()
				self.missEffect.Hide()
				self.waveEffect.Hide()

	def CreateMissEffect(self, x, y):
		self.missEffect.SetPosition(x, y)
		self.missEffect.Show()

	def CreateHitEffect(self, x, y):
		self.hitEffect.SetPosition(x, y)
		self.hitEffect.AppendImage(self.MINING_PATH + "fishing_effect_hit.sub")
		self.hitEffect.Show()

	def CreateWaveEffect(self, x, y, delay = 0):
		self.waveEffect.SetDelay(delay)
		self.waveEffect.SetPosition(x, y)
		self.waveEffect.Show()

	def OnMouseOverOut(self):
		if app.GetCursor() == app.FISH:
			app.SetCursor(app.NORMAL)

	def OnMouseOverIn(self):
		if app.GetCursor() == app.NORMAL:
			app.SetCursor(app.FISH)

	def GetPickaxePoint(self):
		net.SendChatPacket("/mining_event_renewal 1")
