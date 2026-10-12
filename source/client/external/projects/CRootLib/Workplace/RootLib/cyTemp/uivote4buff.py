# -*- coding: cp949 -*-
#490846838
import ui, constInfo, app, net

WEBSITE_LINK = "https://www.youtube.com/watch?v=KW4msApcqhQ"

IMAGE_PATH = "d:/ymir work/ui/vote4buff/"

class VoteWindow(ui.BoardWithTitleBar):

	class Vote(ui.Button):
		def __init__(self, text):
			ui.Button.__init__(self)

			self.window = ui.Window()
			self.window.SetParent(self)
			self.window.SetSize(102, 21)
			self.window.SetPosition(1, 89)
			self.window.Show()

			self.bonusText = ui.MakeTextLineNew(self.window, 0, 0, text)
			self.bonusText.SetHorizontalAlignCenter()
			self.bonusText.SetVerticalAlignCenter()
			self.bonusText.SetWindowHorizontalAlignCenter()
			self.bonusText.SetWindowVerticalAlignCenter()

		def __del__(self):
			ui.Button.__del__(self)

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.SetTitleName("Vote4Buff")
		self.SetSize(390, 279)
		self.SetCenterPosition()
		self.AddFlag("movable")

		self.bonusButtons = list()
		self.voteClickedTime = app.GetTime() + 10000

		self.interface = constInfo.GetInterfaceInstance()

		self.LoadGeneralImages()
		self.dalga = 0

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def LoadGeneralImages(self):
		self.backgroundTop = ui.BorderA()
		self.backgroundTop.SetParent(self)
		self.backgroundTop.SetSize(370, 43)
		self.backgroundTop.SetPosition(10, 32)
		self.backgroundTop.Show()

		self.backgroundCenter = ui.BorderA()
		self.backgroundCenter.SetParent(self)
		self.backgroundCenter.SetSize(370, 146)
		self.backgroundCenter.SetPosition(10, 76)
		self.backgroundCenter.Show()

		self.backgroundBottom = ui.BorderA()
		self.backgroundBottom.SetParent(self)
		self.backgroundBottom.SetSize(370, 46)
		self.backgroundBottom.SetPosition(10, 223)
		self.backgroundBottom.Show()

		self.voteButton = ui.MakeButton(self.backgroundTop, 0, 0, "", IMAGE_PATH, "choose_background.png", "choose_background_2.png", "choose_background_3.png")
		self.voteButton.SetText("You can not vote now.")
		self.voteButton.SetEvent(self.OpenVotePage)
		self.voteButton.SetWindowHorizontalAlignCenter()
		self.voteButton.SetWindowVerticalAlignCenter()

		voteName = {
			0 : {
				"voteName" : "Max HP +1000",
				"voteImage" : "hp",
			},
			1 : {
				"voteName" : "Monster +10%",
				"voteImage" : "monster",
			},
			2 : {
				"voteName" : "EXP +20%",
				"voteImage" : "exp",
			},
		}

		for i in xrange(3):
			self.bonusButtons.append(i)
			self.bonusButtons[i] = self.Vote(voteName[i]["voteName"])
			self.bonusButtons[i].SetParent(self.backgroundCenter)
			self.bonusButtons[i].SetPosition(18 + 115*i, 20)
			self.bonusButtons[i].SetUpVisual(IMAGE_PATH + voteName[i]["voteImage"] + ".png")
			self.bonusButtons[i].SetOverVisual(IMAGE_PATH + voteName[i]["voteImage"] + "_2.png")
			self.bonusButtons[i].SetDownVisual(IMAGE_PATH + voteName[i]["voteImage"] + "_3.png")
			self.bonusButtons[i].SetDisableVisual(IMAGE_PATH + voteName[i]["voteImage"] + "_3.png")
			self.bonusButtons[i].SAFE_SetEvent(self.ConfirmVote, i)
			self.bonusButtons[i].Show()
			self.bonusButtons[i].Down()
			self.bonusButtons[i].Disable()

		self.stateImage = ui.MakeExpandedImageBox(self.backgroundBottom, IMAGE_PATH + "available.png", 3, 4)
		self.stateText = ui.MakeTextLineNew(self.stateImage, 0, 0, "Available")
		self.stateText.SetHorizontalAlignCenter()
		self.stateText.SetVerticalAlignCenter()
		self.stateText.SetWindowHorizontalAlignCenter()
		self.stateText.SetWindowVerticalAlignCenter()

	def OpenVotePage(self):
		self.interface.wndWeb.Open("https://www.metin2pserver.info/vote-ELYSIUM2.htm")
		self.voteClickedTime = app.GetTime() + 22

	def ConfirmVote(self, index):
		net.SendChatPacket("/vote_bonus {}".format(index+1))
		self.Close()

	def Open(self):
		self.Show()

	def Close(self):
		self.Hide()

	def DalgaMotoru(self):
		self.dalga = 1
		for i in xrange(3):
			self.bonusButtons[i].Enable()
			self.bonusButtons[i].SetUp()

	def OnUpdate(self):
		if self.voteClickedTime < app.GetTime() and self.dalga == 0:
			self.DalgaMotoru()

class VoteImage(ui.ExpandedImageBox):

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)
		self.SetPosition(20, 500)
		self.eventType = 0
		self.VoteWindow = VoteWindow()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)
	def SetEventType(self, event):
		self.eventType = event
	def Open(self):
		self.LoadImage("d:/ymir work/ui/game/biolog_system/icon01.png")
		self.Show()

	def OnMouseLeftButtonDown(self):
		self.VoteWindow.Open()

	def OnMouseOverIn(self):
		self.LoadImage("d:/ymir work/ui/game/biolog_system/icon02.png")

	def OnMouseOverOut(self):
		self.LoadImage("d:/ymir work/ui/game/biolog_system/icon01.png")
