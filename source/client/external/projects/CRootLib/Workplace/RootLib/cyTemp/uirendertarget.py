# -*- coding: cp949 -*-
#-443794341
import ui, wndMgr, renderTarget, player, item, app, localeInfo

class RenderTarget(ui.ScriptWindow):
	RENDER_TARGET_INDEX = 1
	children={}
	Window = None

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.max_pos_x = wndMgr.GetScreenWidth()
		self.max_pos_y = wndMgr.GetScreenHeight()
		self.Initialize()
		self.Init()
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def Initialize(self):
		self.interface = None
		self.isDrag = False
		self.totalPos = list()
		self.lastPos = None

	@staticmethod
	def Get():
		if RenderTarget.Window == None:
			RenderTarget.Window = RenderTarget()
		return RenderTarget.Window

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Initialize()

	def DisplayUser(self, vRace=0, vItemWeapon=0, vItemArmor=0, vItemHair=0, vItemAcce=0, vItemAura=0, slotIndex = -1):
		renderTarget.SetBackground(self.RENDER_TARGET_INDEX, "d:/ymir work/ui/game/render/preview_back.tga")
		renderTarget.SetRotation(self.RENDER_TARGET_INDEX, False)
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
		renderTarget.ResetModel(self.RENDER_TARGET_INDEX)
		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, vRace)
		# renderTarget.SetEffect(self.RENDER_TARGET_INDEX)
		renderTarget.RotateEyeAroundTarget(1, 0, 0)

		if vRace > 8:
			return
	
		renderTarget.SetHair(self.RENDER_TARGET_INDEX, 1)
		renderTarget.SetArmor(self.RENDER_TARGET_INDEX, player.GetItemIndex(player.EQUIPMENT_SLOT_START))

		playerRace = player.GetRace()

		if vItemArmor != 0:
			renderTarget.SetArmor(self.RENDER_TARGET_INDEX, vItemArmor)
		else:
			if playerRace == vRace:
				if player.GetItemIndex(item.EQUIPMENT_COSTUME_BODY) == 0:
					renderTarget.SetArmor(self.RENDER_TARGET_INDEX, player.GetItemIndex(player.EQUIPMENT_SLOT_START))
				else:
					renderTarget.SetArmor(self.RENDER_TARGET_INDEX, 0)

		if vItemWeapon != 0:
			renderTarget.SetWeapon(self.RENDER_TARGET_INDEX, vItemWeapon)
		else:
			if playerRace == vRace:
				if player.GetItemIndex(item.EQUIPMENT_COSTUME_WEAPON) == 0:
					renderTarget.SetWeapon(self.RENDER_TARGET_INDEX, player.GetItemIndex(item.EQUIPMENT_COSTUME_WEAPON))
				else:
					renderTarget.SetWeapon(self.RENDER_TARGET_INDEX, 0)

		if vItemHair != 0:
			renderTarget.SetHair(self.RENDER_TARGET_INDEX, vItemHair)
		else:
			if playerRace == vRace:
				renderTarget.SetHair(self.RENDER_TARGET_INDEX, 1)

		if vItemAcce != 0:
			renderTarget.SetAcce(self.RENDER_TARGET_INDEX, vItemAcce)
		else:
			if playerRace == vRace:
				renderTarget.SetAcce(self.RENDER_TARGET_INDEX, 0)

		if vItemAura != 0:
			renderTarget.SetAura(self.RENDER_TARGET_INDEX, vItemAura)
		else:
			if playerRace == vRace:
				renderTarget.SetAura(self.RENDER_TARGET_INDEX, 0)

		self.totalPos = [0, 0] #fixed auto position lightwork

	def Init(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/RenderTargetWindow.py")
		except:
			import exception
			exception.Abort("RenderTargetWindow.LoadDialog.LoadScript")

		try:
			self.titleBar = self.GetChild("TitleBar")
			self.titleBar.CloseButton("show")
			self.titleBar.SetCloseEvent(self.Close)
			self.board = self.GetChild("board")
			self.RenderTarget = self.GetChild("RenderTarget")
			self.SetMouseRightButtonDownEvent(ui.__mem_func__(self.RenderMouseRightDown))
			self.SetMouseRightButtonUpEvent(ui.__mem_func__(self.RenderMouseRightUp))
			self.SetCenterPosition()

			moveText = ui.TextLine()
			moveText.SetParent(self)
			moveText.SetHorizontalAlignRight()
			moveText.SetPosition(self.GetWidth()-10, self.GetHeight()-75)
			moveText.SetText(localeInfo.MODEL_ITEM_PREVIEW_MOVE)
			moveText.Show()
			self.children["moveText"]=moveText
			
			zoomText = ui.TextLine()
			zoomText.SetParent(self)
			zoomText.SetHorizontalAlignRight()
			zoomText.SetPosition(self.GetWidth()-10, self.GetHeight()-50)
			zoomText.SetText(localeInfo.MODEL_ITEM_PREVIEW_ZOOM)
			zoomText.Show()
			self.children["zoomText"]=zoomText

		except:
			import exception
			exception.Abort("RenderTargetWindow.LoadDialog.BindObject")

	def BindInterface(self, interface):
		self.interface = interface

	def Destroy(self):
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)
		self.Close()
		self.Initialize()

	def Close(self):
		self.Hide()

	def Open(self):
		self.Show()
		self.SetTop()

	def IsShow(self):
		return self.Show()

	def OnPressEscapeKey(self):
		self.Close()

	def CanCheckMouse(self):
		return self.isDrag

	def OnUpdate(self):
		if self.CanCheckMouse():
			[currentMousePos, lastPos] = [app.GetCursorPosition(), self.lastPos]
			totalPos = self.totalPos if self.totalPos else [0, 0]
			_x = (currentMousePos[0] - lastPos[0]) + totalPos[0]
			_y = (currentMousePos[1] - lastPos[1]) + totalPos[1]

			fNewPitchVelocity = _y * 0.3
			fNewRotationVelocity = _x * 0.3
			renderTarget.RotateEyeAroundTarget(1, fNewPitchVelocity, fNewRotationVelocity)

			self.totalPos = [_x, _y]
			self.lastPos = currentMousePos

	def OnRunMouseWheel(self, nLen):
		if not renderTarget.IsShow(1):
			return False

		renderTarget.Zoom(1, app.CAMERA_TO_NEGATIVE if nLen > 0 else app.CAMERA_TO_POSITIVE)
		return True

	def RenderMouseRightUp(self):
		app.SetCursor(app.NORMAL)
		self.isDrag = False
		return True

	def RenderMouseRightDown(self):
		app.SetCursor(app.CAMERA_ROTATE)
		self.lastPos = app.GetCursorPosition()
		self.isDrag = True
		return True


