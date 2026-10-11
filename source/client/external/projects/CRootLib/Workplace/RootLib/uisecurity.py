import ui, localeInfo, player, app, chat, uiCommon, wndMgr


class WritingCaptcha(ui.Board):
	PATH_IMAGE = "lightwork/securityvalues/"
	PATH_BUTTON = "offlineshop/lightwork/searchshop/"

	REMAINING_TIME = 20

	def __init__(self):
		ui.Board.__init__(self)
		self.Constructor()
		self.LoadWindow()

	def __del__(self):
		ui.Board.__del__(self)

	def Constructor(self):
		self.textList = []
		self.answerList = [0, 0, 0, 0, 0]
		self.buttonList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.endTime = 0
		self.missAnswerCount = 0
		self.correctAnswer = None

		self.BackgroundShadow = uiCommon.BackgroundShadow(1)
		self.BackgroundShadow.Hide()

		self.SetParent(self.BackgroundShadow)

	def Open(self):
		self.BackgroundShadow.Show()
		self.Show()

		for newAnswer in xrange(5):
			self.answerList[newAnswer] = self.GetRandomNum(True)
			self.textList[newAnswer].LoadImage(self.PATH_IMAGE + "{}/".format(self.answerList[newAnswer]) + "{}.dds".format(self.GetRandomNum()))

		self.endTime = app.GetTime() + self.REMAINING_TIME

	def Close(self):
		self.Hide()
		self.BackgroundShadow.Hide()

	def LoadWindow(self):
		self.SetSize(240, 290)
		self.SetCenterPosition()

		# self.boardList = [ui.ThinBoardCircle(), ui.BorderA(), ui.BorderB(), ui.BorderC(), ui.ThinBoard(), ui.ThinBoardGold()]

		self.editLingBG = ui.ExpandedImageBox()
		self.editLingBG.SetParent(self)
		self.editLingBG.SetPosition(55, 105)
		self.editLingBG.SetSize(200, 30)
		self.editLingBG.LoadImage("d:/ymir work/ui/public/Parameter_Slot_04.sub")
		self.editLingBG.Show()

		self.answerText = ui.TextLine()
		self.answerText.SetParent(self.editLingBG)
		self.answerText.SetPosition(45, 2)
		self.answerText.SetText("")
		self.answerText.Show()

		self.correctAnswer = ui.TextLine()
		self.correctAnswer.SetText("")

		self.boardBackground = ui.ThinBoard()
		self.boardBackground.SetParent(self)
		self.boardBackground.SetPosition(10, 10)
		self.boardBackground.SetSize(220, 270)
		self.boardBackground.Show()

		self.textBG = ui.ThinBoard()
		self.textBG.SetParent(self.boardBackground)
		self.textBG.SetPosition(5, 5)
		self.textBG.SetSize(210, 64)
		self.textBG.Show()

		for num in xrange(6):
			self.textList.append(num)
			self.textList[num] = ui.ExpandedImageBox()
			self.textList[num].SetParent(self.textBG)
			self.textList[num].SetPosition(16+(num * 36), 0)
			self.textList[num].Show()

		self.questionText = ui.MakeTextLineNew(self.textBG, 40, 70, localeInfo.SECURITY_SELECT_ANSWER)

		for btn in xrange(1, 10):
			if btn >= 1 and btn <= 3:
				self.buttonList[btn] = ui.MakeButton(self, -45+btn*67, 185, False, self.PATH_IMAGE, "small_button_0.png", "small_button_1.png", "small_button_2.png")
				self.buttonList[btn].SetText("{}".format(btn))
			elif btn >= 4 and btn <= 6:
				self.buttonList[btn] = ui.MakeButton(self, -45+(btn-3)*67, 161, False, self.PATH_IMAGE, "small_button_0.png", "small_button_1.png", "small_button_2.png")
				self.buttonList[btn].SetText("{}".format(btn))
			elif btn >= 7:
				self.buttonList[btn] = ui.MakeButton(self, -45+(btn-6)*67, 137, False, self.PATH_IMAGE, "small_button_0.png", "small_button_1.png", "small_button_2.png")
				self.buttonList[btn].SetText("{}".format(btn))
			self.buttonList[btn].SetEvent(ui.__mem_func__(self.PressNumber), btn)

		self.clearButton = ui.MakeButton(self, -45+67, 209, False, self.PATH_IMAGE, "small_button_0.png", "small_button_1.png", "small_button_2.png")
		self.clearButton.SetText(localeInfo.SECURITY_CLEAR)
		self.clearButton.SetEvent(ui.__mem_func__(self.ClearAnswerText))

		self.buttonList[0] = ui.MakeButton(self, -45+2*67, 209, False, self.PATH_IMAGE, "small_button_0.png", "small_button_1.png", "small_button_2.png")
		self.buttonList[0].SetText("0")
		self.buttonList[0].SetEvent(ui.__mem_func__(self.PressNumber), 0)

		self.confirmButton = ui.MakeButton(self, -45+3*67, 209, False, self.PATH_IMAGE, "small_button_0.png", "small_button_1.png", "small_button_2.png")
		self.confirmButton.SetText(localeInfo.SECURITY_CONFIRM)
		self.confirmButton.SetEvent(ui.__mem_func__(self.ConfirmAnswer))

		self.remainingTimeGauge = ui.Gauge()
		self.remainingTimeGauge.SetParent(self)
		self.remainingTimeGauge.MakeGauge(190, "white")
		self.remainingTimeGauge.SetPosition(22, 240)
		self.remainingTimeGauge.Show()

		self.remainingTimeText = ui.TextLine()
		self.remainingTimeText.SetParent(self)
		self.remainingTimeText.SetPosition(75, 250)
		self.remainingTimeText.Show()

	def GetRandomNum(self, folderList = False):
		if folderList:
			return app.GetRandom(0, 9)
		return app.GetRandom(0, 7)

	# def OnPressEscapeKey(self):
	#     self.Close()
	#     return True

	def PressNumber(self, num):
		if len(self.answerText.GetText()) >= 5:
			return

		self.answerText.SetText(self.answerText.GetText() + str(num))

	def ClearAnswerText(self):
		self.answerText.SetText("")

	def ConfirmAnswer(self):
		self.correctAnswer.SetText("")
		for ansLetter in self.answerList:
			self.correctAnswer.SetText(self.correctAnswer.GetText() + str(ansLetter))

		if self.correctAnswer.GetText() == self.answerText.GetText():
			self.CorrectAnswer()
			return
		else:
			self.WrongAnswer()

	def CorrectAnswer(self): # cevap dogru
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_ANSWER_SUCCESS)
		player.SetBotControlState(False)
		player.SetBotControlWindow()
		self.Close()

	def WrongAnswer(self): # Cevap yanlıssa bunu cagir,
		if self.missAnswerCount >= 2:
			player.BotControlFail()
			# chat.AppendChat(chat.CHAT_TYPE_INFO, "Close the client") # iki kez yanlis oldu
			self.Close()
		else:
			self.missAnswerCount += 1
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_YOU_HAVE_ONE_MORE_CHANGE)
			for newAnswer in xrange(5):
				self.answerList[newAnswer] = self.GetRandomNum(True)
				self.textList[newAnswer].LoadImage(self.PATH_IMAGE + "{}/".format(self.answerList[newAnswer]) + "{}.dds".format(self.GetRandomNum()))
			self.endTime-=5
			self.answerText.SetText("")

	def TimeIsUp(self): #Sure bitti oyunu kapat.
		player.BotControlFail()
		# chat.AppendChat(chat.CHAT_TYPE_INFO, "Close the client")
		self.Close()

	def OnUpdate(self):
		if app.GetTime() >= self.endTime:
			self.TimeIsUp()

		self.remainingTimeText.SetText(localeInfo.SECURITY_REMAINING_TIME.format(self.endTime - app.GetTime()))
		self.remainingTimeGauge.SetPercentage(max(0, self.endTime - app.GetTime()), self.REMAINING_TIME)

class FindTheDifferentCaptcha(ui.Board):
	PATH_IMAGE = "lightwork/pickthewrongone/"
	PATH_BUTTON = "offlineshop/lightwork/searchshop/"

	REMAINING_TIME = 20

	def __init__(self):
		ui.Board.__init__(self)
		self.Constructor()
		self.LoadWindow()

	def __del__(self):
		ui.Board.__del__(self)

	def Constructor(self):
		self.imageList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.selectedIcon = None
		self.endTime = 0
		self.missAnswerCount = 0

		self.BackgroundShadow = uiCommon.BackgroundShadow(1)
		self.BackgroundShadow.Hide()

		self.SetParent(self.BackgroundShadow)

	def Open(self):
		self.BackgroundShadow.Show()
		self.Show()
		self.missAnswerCount = 0
		self.selectedIcon = self.GetRandomNum(True)
		self.contractImage = self.GetRandomNum()
		self.randomPosX = []
		self.randomPosY = [50, 108, 166]

		for image in xrange(12):
			if image < 4:
				self.imageList[image] = ui.MakeButton(self, 30 + 58 * image,  50, False, self.PATH_IMAGE, "{}/{}.png".format(self.selectedIcon, self.contractImage), "", "", True)
				self.randomPosX.append(30 + 58 * image)
			elif image < 8:
				self.imageList[image] = ui.MakeButton(self, 30 + 58 * (image - 4),  108, False, self.PATH_IMAGE, "{}/{}.png".format(self.selectedIcon, self.contractImage), "", "", True)
				self.randomPosX.append(30 + 58 * (image - 4))
			else:
				self.imageList[image] = ui.MakeButton(self, 30 + 58 * (image - 8),  166, False, self.PATH_IMAGE, "{}/{}.png".format(self.selectedIcon, self.contractImage), "", "", True)
				self.randomPosX.append(30 + 58 * (image - 8))
			self.imageList[image].SetEvent(ui.__mem_func__(self.WrongImage))

		self.randomImage = ui.MakeButton(self, self.randomPosX[app.GetRandom(0, 11)],  self.randomPosY[app.GetRandom(0, 2)], False, self.PATH_IMAGE, "{}/{}.png".format(self.selectedIcon, 0 if self.contractImage == 1 else 1), "", "", True)
		self.randomImage.SetEvent(ui.__mem_func__(self.CorrectImage))

		self.endTime = app.GetTime() + self.REMAINING_TIME

	def Close(self):
		self.Hide()
		self.BackgroundShadow.Hide()

	def LoadWindow(self):
		self.SetSize(280, 275)
		self.SetCenterPosition()

		self.bgImage = ui.ThinBoard()
		self.bgImage.SetParent(self)
		self.bgImage.SetSize(260, 255)
		self.bgImage.SetPosition(10, 10)
		self.bgImage.Show()

		self.questionText = ui.TextLine()
		self.questionText.SetParent(self)
		self.questionText.SetPosition(40, 20)
		self.questionText.SetText(localeInfo.SECURITY_FIND_THE_DIFFERENT)
		self.questionText.Show()

		self.remainingTimeGauge = ui.Gauge()
		self.remainingTimeGauge.SetParent(self)
		self.remainingTimeGauge.MakeGauge(190, "white")
		self.remainingTimeGauge.SetPosition(42, 235)
		self.remainingTimeGauge.Show()

		self.remainingTimeText = ui.TextLine()
		self.remainingTimeText.SetParent(self)
		self.remainingTimeText.SetPosition(95, 245)
		self.remainingTimeText.Show()

	def CorrectImage(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_ANSWER_SUCCESS)
		player.SetBotControlState(False)
		player.SetBotControlWindow()
		self.Close()

	def WrongImage(self): # Cevap yanlıssa bunu cagir,
		if self.missAnswerCount >= 2:
			player.BotControlFail()
			# chat.AppendChat(chat.CHAT_TYPE_INFO, "Close the client") # iki kez yanlis oldu
			self.Close()
		else:
			self.missAnswerCount += 1
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_YOU_HAVE_ONE_MORE_CHANGE)

			self.selectedIcon = self.GetRandomNum(True)
			self.contractImage = self.GetRandomNum()

			for image in xrange(12):
				if image < 4:
					self.imageList[image] = ui.MakeButton(self, 30 + 58 * image,  50, False, self.PATH_IMAGE, "{}/{}.png".format(self.selectedIcon, self.contractImage), "", "", True)
				elif image < 8:
					self.imageList[image] = ui.MakeButton(self, 30 + 58 * (image - 4),  108, False, self.PATH_IMAGE, "{}/{}.png".format(self.selectedIcon, self.contractImage), "", "", True)
				else:
					self.imageList[image] = ui.MakeButton(self, 30 + 58 * (image - 8),  166, False, self.PATH_IMAGE, "{}/{}.png".format(self.selectedIcon, self.contractImage), "", "", True)
				self.imageList[image].SetEvent(ui.__mem_func__(self.WrongImage))

			self.randomImage = ui.MakeButton(self, self.randomPosX[app.GetRandom(0, 11)],  self.randomPosY[app.GetRandom(0, 2)], False, self.PATH_IMAGE, "{}/{}.png".format(self.selectedIcon, 0 if self.contractImage == 1 else 1), "", "", True)
			self.randomImage.SetEvent(ui.__mem_func__(self.CorrectImage))

			self.endTime-=5

	def GetRandomNum(self, folderList = False):
		if folderList:
			return app.GetRandom(0, 13)
		return app.GetRandom(0, 1)

	# def OnPressEscapeKey(self):
	#     self.Close()
	#     return True

	def TimeIsUp(self): #Sure bitti oyunu kapat.
		player.BotControlFail()
		# chat.AppendChat(chat.CHAT_TYPE_INFO, "Close the client")
		self.Close()

	def OnUpdate(self):
		if app.GetTime() >= self.endTime:
			self.TimeIsUp()

		self.remainingTimeText.SetText(localeInfo.SECURITY_REMAINING_TIME.format(self.endTime - app.GetTime()))
		self.remainingTimeGauge.SetPercentage(max(0, self.endTime - app.GetTime()), self.REMAINING_TIME)

class SortTheNumbers(ui.Board):
	PATH_IMAGE = "lightwork/securityvalues/"
	PATH_BUTTON = "offlineshop/lightwork/searchshop/"

	REMAINING_TIME = 20

	def __init__(self):
		ui.Board.__init__(self)
		self.Constructor()
		self.LoadWindow()

	def __del__(self):
		ui.Board.__del__(self)

	def Constructor(self):
		self.endTime = 0
		self.missAnswerCount = 0
		self.numberParentList = [0, 0, 0, 0, 0]
		self.numberList = [0, 0, 0, 0, 0]
		self.answerNumberList = [0, 0, 0, 0, 0]
		self.numberGetLocalPositionList = [0, 0, 0, 0, 0]
		self.newList = []
		self.isSorted = False

		self.selectedNumber = -1
		self.checkTime = 0

		self.BackgroundShadow = uiCommon.BackgroundShadow(1)
		self.BackgroundShadow.Hide()

		self.SetParent(self.BackgroundShadow)

	def Open(self):
		self.BackgroundShadow.Show()
		self.Show()
		self.missAnswerCount = 0
		self.isSorted = False

		for gen in xrange(5):
			self.answerNumberList[gen] = app.GetRandom(0, 9)

		self.answerNumberList = set(self.answerNumberList)

		while len(self.answerNumberList) < 5:
			self.answerNumberList.add(app.GetRandom(0, 9))

		self.answerNumberList = list(self.answerNumberList)

		for number in xrange(5):
			self.numberList[number] = ui.ExpandedImageBox()
			self.numberList[number].SetParent(self)
			self.numberList[number].SetPosition(75+number*36, 155)
			self.numberList[number].LoadImage(self.PATH_IMAGE+"{}/{}.dds".format(self.answerNumberList[number], app.GetRandom(0, 7)))
			self.numberList[number].OnMouseOverIn = lambda index = number : self.OverInNumber(index)
			self.numberList[number].Show()
			self.numberList[number].AddFlag("movable")

		self.endTime = app.GetTime() + self.REMAINING_TIME

	def OverInNumber(self, idx):
		self.selectedNumber = idx

	def Close(self):
		self.Hide()
		self.isSorted = False
		self.BackgroundShadow.Hide()

	def LoadWindow(self):
		self.SetSize(350, 275)
		self.SetCenterPosition()

		self.bgImage = ui.ThinBoard()
		self.bgImage.SetParent(self)
		self.bgImage.SetSize(330, 255)
		self.bgImage.SetPosition(10, 10)
		self.bgImage.Show()

		self.questionText = ui.TextLine()
		self.questionText.SetParent(self)
		self.questionText.SetPosition(38, 20)
	
		self.questionRandom = app.GetRandom(0, 10)
		self.questionText.SetText(localeInfo.SECURITY_SORT_IMAGES.format(localeInfo.SECURITY_SORT_IMAGES2 if  self.questionRandom < 5 else localeInfo.SECURITY_SORT_IMAGES3))
		self.questionText.Show()

		for parent in xrange(5):
			self.numberParentList[parent] = ui.ThinBoardCircle()
			self.numberParentList[parent].SetParent(self)
			self.numberParentList[parent].SetSize(50, 70)
			self.numberParentList[parent].SetPosition(30 + 60 * parent, 50)
			self.numberParentList[parent].Show()

		self.remainingTimeGauge = ui.Gauge()
		self.remainingTimeGauge.SetParent(self)
		self.remainingTimeGauge.MakeGauge(190, "white")
		self.remainingTimeGauge.SetPosition(42+35, 235)
		self.remainingTimeGauge.Show()

		self.remainingTimeText = ui.TextLine()
		self.remainingTimeText.SetParent(self)
		self.remainingTimeText.SetPosition(95+35, 245)
		self.remainingTimeText.Show()

		self.confirmButton = ui.MakeButton(self, 92, 130, False, "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
		self.confirmButton.SetText(localeInfo.SECURITY_CONFIRM)
		self.confirmButton.SetEvent(ui.__mem_func__(self.ConfirmSelected))

		# self.resetPositions = ui.MakeButton(self, 240, 130, localeInfo.SECURITY_NUMBERS_RESET_POS, "offlineshop/lightwork/searchshop/", "refresh_normal.png", "refresh_hover.png", "refresh_down.png")
		# self.resetPositions.SetEvent(ui.__mem_func__(self.ResetNumberPositions))

	def ConfirmSelected(self): # Onayladi sonuc burada verielcek
		if (30 <= self.numberList[self.GetNumberImagePosition(0)].GetLocalPosition()[0] <= 48) and (39 <= self.numberList[self.GetNumberImagePosition(0)].GetLocalPosition()[1] <= 60):
			# Check if the second box is correct
			if (90 <= self.numberList[self.GetNumberImagePosition(1)].GetLocalPosition()[0] <= 108) and (39 <= self.numberList[self.GetNumberImagePosition(1)].GetLocalPosition()[1] <= 60):
				# Check if the third box is correct
				if (150 <= self.numberList[self.GetNumberImagePosition(2)].GetLocalPosition()[0] <= 168) and (39 <= self.numberList[self.GetNumberImagePosition(2)].GetLocalPosition()[1] <= 60):
					# Check if the fourth box is correct
					if (210 <= self.numberList[self.GetNumberImagePosition(3)].GetLocalPosition()[0] <= 228) and (39 <= self.numberList[self.GetNumberImagePosition(3)].GetLocalPosition()[1] <= 60):
						# Check if the fifth box is correct
						if (270 <= self.numberList[self.GetNumberImagePosition(4)].GetLocalPosition()[0] <= 288) and (39 <= self.numberList[self.GetNumberImagePosition(4)].GetLocalPosition()[1] <= 60):
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_ANSWER_SUCCESS) # Tumunu gectim burada yapilacak basarili diye diger turlu 5 sn azalacak
							player.SetBotControlState(False)
							player.SetBotControlWindow()
							self.Close()
						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_ANSWER_IS_WRONG)
							self.endTime-=5
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_ANSWER_IS_WRONG)
						self.endTime-=5
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_ANSWER_IS_WRONG)
					self.endTime-=5
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_ANSWER_IS_WRONG)
				self.endTime-=5
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SECURITY_ANSWER_IS_WRONG)
			self.endTime-=5
		

	def PlaceNearest(self):

		if (self.checkTime > app.GetTime()):
			return

		if self.numberList[self.selectedNumber].IsIn():
			x, y = wndMgr.GetMousePosition()
			_x, _y = self.GetLocalPosition()
			# chat.AppendChat(1, "{}".format(self.GetLocalPosition()))

			inWidthRange = 360 <= y <= 430

			inFirstBox = 656 <= x <= 703
			inSecondBox = 713 <= x <= 760
			inThirdBox = 776 <= x <= 823
			inFourthBox = 835 <= x <= 882
			inFifthBox = 895 <= x <= 942

			if inWidthRange:
				if inFirstBox:
					self.numberList[self.selectedNumber].SetPosition(39, 51)

				elif inSecondBox:
					self.numberList[self.selectedNumber].SetPosition(97, 51)

				elif inThirdBox:
					self.numberList[self.selectedNumber].SetPosition(157, 51)

				elif inFourthBox:
					self.numberList[self.selectedNumber].SetPosition(218, 51)

				elif inFifthBox:
					self.numberList[self.selectedNumber].SetPosition(279, 51)

			self.checkTime = app.GetTime() + 0.2

	def ResetNumberPositions(self):
		for number in xrange(5):
			self.numberList[number].SetPosition(75+number*36, 155)

	def GetRandomNum(self, folderList = False):
		if folderList:
			return app.GetRandom(0, 13)
		return app.GetRandom(0, 1)

	# def OnPressEscapeKey(self):
	#     self.Close()
	#     return True

	def TimeIsUp(self): #Sure bitti oyunu kapat.
		player.BotControlFail()
		# chat.AppendChat(chat.CHAT_TYPE_INFO, "Close the client")
		self.Close()

	def SortTheList(self):
		if self.isSorted:
			return

		for elem in self.answerNumberList:
			self.newList.append(elem)

		for i in xrange(len(self.newList)):
			for j in xrange(i + 1, len(self.newList)):
				if (self.newList[i] > self.newList[j]) if self.questionRandom < 5 else (self.newList[i] < self.newList[j]):
					self.newList[i], self.newList[j] = self.newList[j], self.newList[i]

		self.isSorted = True

	def GetNumberImagePosition(self, idx):
		self.SortTheList()
		return self.answerNumberList.index(self.newList[idx])

	def OnUpdate(self):
		if app.GetTime() >= self.endTime:
			self.TimeIsUp()

		self.remainingTimeText.SetText(localeInfo.SECURITY_REMAINING_TIME.format(self.endTime - app.GetTime()))
		self.remainingTimeGauge.SetPercentage(max(0, self.endTime - app.GetTime()), self.REMAINING_TIME)

		for nm in xrange(5):
			self.numberGetLocalPositionList[nm] = [self.numberList[nm].GetLocalPosition()]

		# self.PlaceNearest()
