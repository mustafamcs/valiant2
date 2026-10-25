import app
if app.ENABLE_OFFICAL_CHARACTER_SCREEN:
	import chr, grp, app, wndMgr, net, event, localeInfo, ui, uiToolTip, uiScriptLocale, playerSettingModule, snd, systemSetting
	
	MAN 		= 0
	WOMAN		= 1
	
	class CreateCharacterWindow(ui.Window):
		M2STATPOINT = ( ## CON INT STR DEX ##
			( 4, 3, 6, 3 ), ## WARRIOR ##
			( 3, 3, 4, 6 ), ## ASSASSIN ##
			( 3, 5, 5, 3 ), ## SURA ##
			( 4, 6, 3, 3 ), ## SHAMAN ##
			# ( 6, 2, 2, 6 ), ## WOLFMAN ##
		)
		M2JOBLIST = {
			0	:	localeInfo.JOB_WARRIOR,
			1	:	localeInfo.JOB_ASSASSIN,
			2	:	localeInfo.JOB_SURA,
			3	:	localeInfo.JOB_SHAMAN,
			# 4	:	localeInfo.JOB_WOLFMAN,
		}
	
		##M2_CONST_ID[JOB][SEX]##
		M2_CONST_ID = 	(
			(playerSettingModule.RACE_WARRIOR_M, playerSettingModule.RACE_WARRIOR_W),
			(playerSettingModule.RACE_ASSASSIN_M, playerSettingModule.RACE_ASSASSIN_W),
			(playerSettingModule.RACE_SURA_M, playerSettingModule.RACE_SURA_W),
			(playerSettingModule.RACE_SHAMAN_M, playerSettingModule.RACE_SHAMAN_W),
			# (playerSettingModule.RACE_WOLFMAN_M, -1),
		)
	
		LEN_JOBLIST = len(M2JOBLIST) #5
		LEN_STATPOINT = len(M2STATPOINT[0]) #4
		M2_INIT_VALUE = -1
	
		EMPIRE_NAME = {
			net.EMPIRE_A : localeInfo.EMPIRE_A,
			net.EMPIRE_B : localeInfo.EMPIRE_B,
			net.EMPIRE_C : localeInfo.EMPIRE_C
		}
		EMPIRE_NAME_COLOR = {
			net.EMPIRE_A : (0.7450, 0, 0),
			net.EMPIRE_B : (0.8666, 0.6156, 0.1843),
			net.EMPIRE_C : (0.2235, 0.2549, 0.7490)
		}
	
		## Job Description ##
		DESCRIPTION_FILE_NAME =	(
				uiScriptLocale.JOBDESC_WARRIOR_PATH,
				uiScriptLocale.JOBDESC_ASSASSIN_PATH,
				uiScriptLocale.JOBDESC_SURA_PATH,
				uiScriptLocale.JOBDESC_SHAMAN_PATH,
				# uiScriptLocale.JOBDESC_WOLFMAN_PATH,
			)
		RACE_FACE_PATH = {
			playerSettingModule.RACE_WARRIOR_M:		"D:/ymir work/ui/intro/public_intro/face/face_warrior_m_0",
			playerSettingModule.RACE_ASSASSIN_W:	"D:/ymir work/ui/intro/public_intro/face/face_assassin_w_0",
			playerSettingModule.RACE_SURA_M:		"D:/ymir work/ui/intro/public_intro/face/face_sura_m_0",
			playerSettingModule.RACE_SHAMAN_W:		"D:/ymir work/ui/intro/public_intro/face/face_shaman_w_0",
			playerSettingModule.RACE_WARRIOR_W:		"D:/ymir work/ui/intro/public_intro/face/face_warrior_w_0",
			playerSettingModule.RACE_ASSASSIN_M:	"D:/ymir work/ui/intro/public_intro/face/face_assassin_m_0",
			playerSettingModule.RACE_SURA_W:		"D:/ymir work/ui/intro/public_intro/face/face_sura_w_0",
			playerSettingModule.RACE_SHAMAN_M:		"D:/ymir work/ui/intro/public_intro/face/face_shaman_m_0",
			# playerSettingModule.RACE_WOLFMAN_M:	"D:/ymir work/ui/intro/public_intro/face/face_wolfman_m_0",
		}
	
		DISC_FACE_PATH = {
			playerSettingModule.RACE_WARRIOR_M:		"D:/ymir work/bin/icon/face/warrior_m.tga",
			playerSettingModule.RACE_ASSASSIN_W:	"D:/ymir work/bin/icon/face/assassin_w.tga",
			playerSettingModule.RACE_SURA_M:		"D:/ymir work/bin/icon/face/sura_m.tga",
			playerSettingModule.RACE_SHAMAN_W:		"D:/ymir work/bin/icon/face/shaman_w.tga",
			playerSettingModule.RACE_WARRIOR_W:		"D:/ymir work/bin/icon/face/warrior_w.tga",
			playerSettingModule.RACE_ASSASSIN_M:	"D:/ymir work/bin/icon/face/assassin_m.tga",
			playerSettingModule.RACE_SURA_W:		"D:/ymir work/bin/icon/face/sura_w.tga",
			playerSettingModule.RACE_SHAMAN_M:		"D:/ymir work/bin/icon/face/shaman_m.tga",
			# playerSettingModule.RACE_WOLFMAN_M:		"D:/ymir work/bin/icon/face/wolfman_m.tga",
		}
	
		## Job Description ##
		class DescriptionBox(ui.Window):
			def __init__(self):
				ui.Window.__init__(self)
				self.descIndex = 0
	
			def __del__(self):
				ui.Window.__del__(self)
	
			def SetIndex(self, index):
				self.descIndex = index
	
			def OnRender(self):
				event.RenderEventSet(self.descIndex)
	
		class CharacterRenderer(ui.Window):
			def OnRender(self):
				grp.ClearDepthBuffer()
				grp.SetGameRenderState()
				grp.PushState()
				grp.SetOmniLight()
	
				screenWidth = wndMgr.GetScreenWidth()
				screenHeight = wndMgr.GetScreenHeight()
				newScreenWidth = float(screenWidth)
				newScreenHeight = float(screenHeight)
	
				grp.SetViewport(0.0, 0.0, newScreenWidth/screenWidth, newScreenHeight/screenHeight)
	
				app.SetCenterPosition(0.0, 0.0, 0.0)
				app.SetCamera(1550.0, 15.0, 180.0, 95.0)
				grp.SetPerspective(10.0, newScreenWidth/newScreenHeight, 1000.0, 3000.0)
	
				(x, y) = app.GetCursorPosition()
				grp.SetCursorPosition(x, y)
	
				chr.Deform()
				chr.Render()
	
				grp.RestoreViewport()
				grp.PopState()
				grp.SetInterfaceRenderState()
	
	
		## class CreateCharacterWindow Function ##
		def __init__(self, stream):
			ui.Window.__init__(self)
			net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, self)
			self.stream = stream
	
			##Init Value##
			self.ShowToolTip = False
			self.createSuccess = False
			self.MotionStart = False
			self.MotionTime = 0.0
			self.gender = self.M2_INIT_VALUE
			self.job_id = self.M2_INIT_VALUE
			self.shape = self.M2_INIT_VALUE
			self.descIndex = 0
			self.statpoint = [0, 0, 0, 0]
			self.curGauge  = [0.0, 0.0, 0.0, 0.0]
	
			self.charGender = []
			#self.shapeList = [0, 0, 0, 0]
			self.shapeList = [0, 0, 0, 0, 0]
	
		def __del__(self):
			net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, 0)
			ui.Window.__del__(self)
	
		def Open(self):
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/characterselect.mp3")
			dlgBoard = ui.ScriptWindow()
			self.dlgBoard = dlgBoard
			pythonScriptLoader = ui.PythonScriptLoader()
			pythonScriptLoader.LoadScriptFile(self.dlgBoard, "UIScript/CreateCharacterWindow.py")
	
			getChild = self.dlgBoard.GetChild
	
			## HanMoon ##
			self.NameList = []
			self.NameList.append(getChild("name_warrior"))
			self.NameList.append(getChild("name_assassin"))
			self.NameList.append(getChild("name_sura"))
			self.NameList.append(getChild("name_shaman"))
			# self.NameList.append(getChild("name_wolfman"))
	
			## Text ##
			self.textBoard = getChild("text_board")
			self.btnPrev = getChild("prev_button")
			self.btnNext = getChild("next_button")
	
			## Select Job Button List Append ##
			self.JobList = []
			self.JobList.append(getChild("WARRIOR"))
			self.JobList.append(getChild("ASSASSIN"))
			self.JobList.append(getChild("SURA"))
			self.JobList.append(getChild("SHAMAN"))
			# self.JobList.append(getChild("WOLFMAN"))
	
			## Image Click Name & Face(Left Button) ##
			self.SelectBtnNameList = []
			self.SelectBtnNameList.append(getChild("name_warrior_small"))
			self.SelectBtnNameList.append(getChild("name_assassin_small"))
			self.SelectBtnNameList.append(getChild("name_sura_small"))
			self.SelectBtnNameList.append(getChild("name_shaman_small"))
			# self.SelectBtnNameList.append(getChild("name_wolfman_small"))
	
			self.SelectBtnFaceList = []
			self.SelectBtnFaceList.append(getChild("CharacterFace_0"))
			self.SelectBtnFaceList.append(getChild("CharacterFace_1"))
			self.SelectBtnFaceList.append(getChild("CharacterFace_2"))
			self.SelectBtnFaceList.append(getChild("CharacterFace_3"))
			# self.SelectBtnFaceList.append(getChild("CharacterFace_4"))
	
			## Select SEX Button List Append ##
			self.genderButtonList = []
			self.genderButtonList.append(getChild("gender_button_01"))
			self.genderButtonList.append(getChild("gender_button_02"))
	
			## Select Shape Button List Append ##
			self.shapeButtonList = []
			self.shapeButtonList.append(getChild("shape_button_01"))
			self.shapeButtonList.append(getChild("shape_button_02"))
	
			## StatPoint Value ##
			self.statValue = []
			self.statValue.append(getChild("hth_value"))
			self.statValue.append(getChild("int_value"))
			self.statValue.append(getChild("str_value"))
			self.statValue.append(getChild("dex_value"))
	
			## Gauge UI ##
			self.GaugeList = []
			self.GaugeList.append(getChild("hth_gauge"))
			self.GaugeList.append(getChild("int_gauge"))
			self.GaugeList.append(getChild("str_gauge"))
			self.GaugeList.append(getChild("dex_gauge"))
	
			## Create or Cancel ##
			self.btnCreate = getChild("create_button")
			self.btnCancel = getChild("cancel_button")
	
			## Empire Flag ##
			self.empireName = getChild("EmpireName")
			self.flagDict = {
				net.EMPIRE_B : "d:/ymir work/ui/intro/empire/empireflag_b.sub",
				net.EMPIRE_C : "d:/ymir work/ui/intro/empire/empireflag_c.sub",
			}
			self.flag = getChild("EmpireFlag")
	
			self.discFace = getChild("DiscFace")
			self.raceNameText = getChild("raceName_Text")
	
			## ID Character Name ##
			self.editCharacterName = getChild("character_name_value")
	
			## Background ## Note : Default : Sinsu
			self.backGroundDict = {
				net.EMPIRE_B : "d:/ymir work/ui/intro/empire/background/background.jpg",
				net.EMPIRE_C : "d:/ymir work/ui/intro/empire/background/background.jpg",
			}
	
			self.backGround = getChild("BackGround")
	
			## INIT Job Sex ##
			self.JobSex = {}
			self.JobSex[0] = app.GetRandom(MAN, WOMAN) ## WARRIOR ##
			self.JobSex[1] = app.GetRandom(MAN, WOMAN) ## ASSASSIN ##
			self.JobSex[2] = app.GetRandom(MAN, WOMAN) ## SURA	##
			self.JobSex[3] = app.GetRandom(MAN, WOMAN) ## SHAMAN ##
			# self.JobSex[4] = MAN ## WOLFMAN ##
	
			##Tool Tip##
			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.ClearToolTip()
	
			self.editCharacterName.SetText("")
	
			self.EnableWindow()
	
			## Select Job Button List Start Event ##
			self.JobList[0].SetEvent(ui.__mem_func__(self.SelectJob), 0)
			self.JobList[1].SetEvent(ui.__mem_func__(self.SelectJob), 1)
			self.JobList[2].SetEvent(ui.__mem_func__(self.SelectJob), 2)
			self.JobList[3].SetEvent(ui.__mem_func__(self.SelectJob), 3)
			# self.JobList[4].SetEvent(ui.__mem_func__(self.SelectJob), 4)
	
			## Select Sex Button List Start Event ##
			self.genderButtonList[MAN].SetEvent(ui.__mem_func__(self.SelectGender), MAN)
			self.genderButtonList[WOMAN].SetEvent(ui.__mem_func__(self.SelectGender), WOMAN)
	
			## Select Shape Button List Start Event ##
			self.shapeButtonList[0].SetEvent(ui.__mem_func__(self.SelectShape), 0)
			self.shapeButtonList[1].SetEvent(ui.__mem_func__(self.SelectShape), 1)
	
			## Create or Cancel ##
			self.btnCreate.SetEvent(ui.__mem_func__(self.CreateCharacterButton))
			self.btnCancel.SetEvent(ui.__mem_func__(self.CancelButton))
	
			## Job Description ##
			self.btnPrev.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			self.btnNext.SetEvent(ui.__mem_func__(self.NextDescriptionPage))
	
			self.editCharacterName.SetReturnEvent(ui.__mem_func__(self.CreateCharacterButton))
			self.editCharacterName.SetEscapeEvent(ui.__mem_func__(self.CancelButton))
	
			for i in xrange(len(self.NameList)):
				self.SelectBtnFaceList[i].AddFlag("not_pick")
				self.SelectBtnNameList[i].AddFlag("not_pick")
	
			## Tooltip ##
			getChild("WARRIOR").ShowToolTip=		lambda arg = self.M2JOBLIST[0] : self.OverInToolTip(arg)
			getChild("WARRIOR").HideToolTip=		lambda: self.OverOutToolTip()
			getChild("ASSASSIN").ShowToolTip=		lambda arg = self.M2JOBLIST[1] : self.OverInToolTip(arg)
			getChild("ASSASSIN").HideToolTip=		lambda: self.OverOutToolTip()
			getChild("SURA").ShowToolTip=				lambda arg = self.M2JOBLIST[2] : self.OverInToolTip(arg)
			getChild("SURA").HideToolTip=				lambda: self.OverOutToolTip()
			getChild("SHAMAN").ShowToolTip=			lambda arg = self.M2JOBLIST[3] : self.OverInToolTip(arg)
			getChild("SHAMAN").HideToolTip=			lambda: self.OverOutToolTip()
			# getChild("WOLFMAN").ShowToolTip=		lambda arg = self.M2JOBLIST[4] : self.OverInToolTip(arg)
			# getChild("WOLFMAN").HideToolTip=		lambda: self.OverOutToolTip()
	
			getChild("gender_button_01").ShowToolTip 	= lambda arg = uiScriptLocale.CREATE_MAN : self.OverInToolTip(arg)
			getChild("gender_button_01").HideToolTip 	= lambda : self.OverOutToolTip()
			getChild("gender_button_02").ShowToolTip 	= lambda arg = uiScriptLocale.CREATE_WOMAN : self.OverInToolTip(arg)
			getChild("gender_button_02").HideToolTip 	= lambda : self.OverOutToolTip()
	
			getChild("shape_button_01").ShowToolTip 	= lambda arg = uiScriptLocale.CREATE_SHAPE + "1": self.OverInToolTip(arg)
			getChild("shape_button_01").HideToolTip 	= lambda : self.OverOutToolTip()
			getChild("shape_button_02").ShowToolTip 	= lambda arg = uiScriptLocale.CREATE_SHAPE + "2" : self.OverInToolTip(arg)
			getChild("shape_button_02").HideToolTip 	= lambda : self.OverOutToolTip()
	
			getChild("prev_button").ShowToolTip 	= lambda arg = uiScriptLocale.CREATE_PREV : self.OverInToolTip(arg)
			getChild("prev_button").HideToolTip 	= lambda : self.OverOutToolTip()
			getChild("next_button").ShowToolTip 	= lambda arg = uiScriptLocale.CREATE_NEXT : self.OverInToolTip(arg)
			getChild("next_button").HideToolTip 	= lambda : self.OverOutToolTip()
			getChild("create_button").ShowToolTip 	= lambda arg = uiScriptLocale.CREATE_CREATE : self.OverInToolTip(arg)
			getChild("create_button").HideToolTip 	= lambda : self.OverOutToolTip()
			getChild("cancel_button").ShowToolTip 	= lambda arg = uiScriptLocale.CANCEL : self.OverInToolTip(arg)
			getChild("cancel_button").HideToolTip 	= lambda : self.OverOutToolTip()
	
			## Func Open UI Loading END##
			## Func Open Make Character & Render START##
	
			## Flag Setting ##
			my_empire = net.GetEmpireID()
			self.SetEmpire(my_empire)
	
			#Job Description Box
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.Show()
	
			##Character Render##
			self.chrRenderer = self.CharacterRenderer()
			self.chrRenderer.SetParent(self.backGround)
			self.chrRenderer.Show()
	
			## Make Character ##
			self.MakeCharacter(playerSettingModule.RACE_WARRIOR_M)
			self.MakeCharacter(playerSettingModule.RACE_ASSASSIN_M)
			self.MakeCharacter(playerSettingModule.RACE_SURA_M)
			self.MakeCharacter(playerSettingModule.RACE_SHAMAN_M)
	
			self.MakeCharacter(playerSettingModule.RACE_WARRIOR_W)
			self.MakeCharacter(playerSettingModule.RACE_ASSASSIN_W)
			self.MakeCharacter(playerSettingModule.RACE_SURA_W)
			self.MakeCharacter(playerSettingModule.RACE_SHAMAN_W)
	
			# self.MakeCharacter(playerSettingModule.RACE_WOLFMAN_M)
	
			for i in xrange(self.LEN_JOBLIST):
				if i == 4:
					self.charGender.append(0)
				self.charGender.append(app.GetRandom(0, 1))
	
			self.dlgBoard.Show()
			self.Show()
			app.ShowCursor()
	
			##Default Setting##
			self.SelectJob(app.GetRandom(0, self.LEN_JOBLIST - 1))
	
		def Close(self):
			snd.FadeOutMusic("BGM/characterselect.mp3")
			##Init Value##
			self.ShowToolTip = None
			self.createSuccess = None
			self.MotionStart = None
			self.MotionTime = None
			self.gender = None
			self.job_id = None
			self.shape = None
			self.descIndex = None
			self.statpoint = None
			self.curGauge  = None
	
			for i in xrange(len(self.M2_CONST_ID)):
				chr.DeleteInstance(i)
	
			self.stream = None
			self.M2STATPOINT = None
			self.M2JOBLIST = None
			self.M2_CONST_ID = None
			self.LEN_JOBLIST = None
			self.LEN_STATPOINT = None
			self.M2_INIT_VALUE = None
			self.EMPIRE_NAME = None
			self.EMPIRE_NAME_COLOR = None
			self.DESCRIPTION_FILE_NAME = None
			self.RACE_FACE_PATH = None
			self.DISC_FACE_PATH = None
			self.NameList = None
			self.JobList = None
			self.SelectBtnNameList = None
			self.SelectBtnFaceList = None
			self.genderButtonList = None
			self.shapeButtonList = None
			self.statValue = None
			self.GaugeList = None
			self.flag = None
			self.flagDict = None
			self.raceNameText = None
	
			self.shapeList = None
	
			self.textBoard = None
			self.btnPrev = None
			self.btnNext = None
			self.btnCreate = None
			self.btnCancel = None
			self.empireName = None
			self.editCharacterName = None
			self.backGround = None
			self.backGroundDict = None
			self.toolTip = None
			self.JobSex = None
			self.dlgBoard.ClearDictionary()
	
			self.dlgBoard.Hide()
			self.Hide()
	
			app.HideCursor()
			event.Destroy()
	
		##[Event]Create Success - Phase Change##
		def OnCreateSuccess(self):
			self.createSuccess = True
	
		##[Event]Create Fail - ##EnableWindow
		def OnCreateFailure(self, type):
			self.MotionStart = False
			chr.BlendLoopMotion(chr.MOTION_INTRO_WAIT, 0.1)
			if 1 == type:
				self.PopupMessage(localeInfo.CREATE_EXIST_SAME_NAME, self.EnableWindow)
			#elif 2 == type:
			#	self.PopupMessage(localeInfo.CREATE_ERROR_LIMIT_LEVEL, self.EnableWindow)
			#elif 3 == type:
			#	self.PopupMessage(localeInfo.CREATE_ERROR_TIME_LIMIT, self.EnableWindow)
			#elif 4 == type:
			#	self.PopupMessage(localeInfo.CREATE_ERROR_WRONG_STRING, self.EnableWindow)
			else:
				self.PopupMessage(localeInfo.CREATE_FAILURE, self.EnableWindow) #string or time or same name has type/packet 0
	
		def EnableWindow(self):
			for i in xrange(self.LEN_JOBLIST):
				self.JobList[i].Enable()
	
			self.btnPrev.Enable()
			self.btnNext.Enable()
			self.btnCreate.Enable()
			self.btnCancel.Enable()
			self.editCharacterName.SetFocus()
			self.editCharacterName.Enable()
	
			for i in xrange(2) :
				self.genderButtonList[i].Enable()
				self.shapeButtonList[i].Enable()
	
		def DisableWindow(self):
			for i in xrange(self.LEN_JOBLIST):
				self.JobList[i].Disable()
	
			self.btnPrev.Disable()
			self.btnNext.Disable()
			self.btnCreate.Disable()
			self.btnCancel.Disable()
			self.editCharacterName.Disable()
	
			self.toolTip.Hide()
			self.ShowToolTip = False
	
			for i in xrange(2) :
				self.genderButtonList[i].Disable()
				self.shapeButtonList[i].Disable()
	
		def MakeCharacter(self, race):
			chr_id = race
	
			chr.CreateInstance(chr_id)
			chr.SelectInstance(chr_id)
			chr.SetVirtualID(chr_id)
			chr.SetNameString(str(race))
	
			chr.SetRace(race)
			chr.SetArmor(0)
			chr.SetHair(0)
	
			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
	
			chr.SetRotation(-7.0) #Degree value
			chr.Hide()
	
		def SelectJob(self, job_id):
			if self.MotionStart :
				self.JobList[job_id].SetUp()
				return
	
			for button in self.JobList:
				button.SetUp()
	
			##Default Setting##
			self.job_id = job_id
			self.JobList[self.job_id].Down()
			self.SelectGender(self.JobSex[job_id])
	
			##Job Descirption##
			event.ClearEventSet(self.descIndex)
			self.descIndex = event.RegisterEventSet(self.DESCRIPTION_FILE_NAME[self.job_id])
			event.SetFontColor(self.descIndex, 0.7843, 0.7843, 0.7843)
			total_line = event.GetTotalLineCount(self.descIndex)
			self.raceNameText.SetText(self.M2JOBLIST[job_id])
	
			event.SetRestrictedCount(self.descIndex, 35)
	
			if event.BOX_VISIBLE_LINE_COUNT >= total_line :
				self.btnPrev.Hide()
				self.btnNext.Hide()
			else :
				self.btnPrev.Show()
				self.btnNext.Show()
			##Stat Point##
			self.ResetStat()
	
			# if self.M2_CONST_ID[self.job_id][MAN] == playerSettingModule.RACE_WOLFMAN_M	:
				# self.genderButtonList[WOMAN].Hide()
			# else:
			self.genderButtonList[WOMAN].Show()
	
		def SelectGender(self, gender):
			for button in self.genderButtonList:
				button.SetUp()
	
			self.gender = gender
			self.genderButtonList[self.gender].Down()
	
			if self.M2_INIT_VALUE == self.job_id:
				return
	
			self.JobSex[self.job_id] = self.gender
			self.race = self.M2_CONST_ID[self.job_id][self.gender]
	
			for i in xrange(self.LEN_JOBLIST):
				if self.job_id == i:
					self.SelectBtnFaceList[i].LoadImage(self.RACE_FACE_PATH[self.race] + "1.sub")
				else:
					self.SelectBtnFaceList[i].LoadImage( self.RACE_FACE_PATH[self.M2_CONST_ID[i][self.JobSex[i]]] + "2.sub")
	
			self.discFace.LoadImage(self.DISC_FACE_PATH[self.race])
	
			if self.M2_INIT_VALUE == self.shape:
				self.shape = 0
	
			self.SelectShape(self.shapeList[self.job_id])
	
		def SelectShape(self, shape):
			self.shapeList[self.job_id] = shape
			for button in self.shapeButtonList:
				button.SetUp()
	
			self.shape = shape
			self.shapeButtonList[self.shape].Down()
	
			if self.M2_INIT_VALUE == self.job_id:
				return
	
			chr.Hide()
			chr.SelectInstance(self.race)
			chr.ChangeShape(self.shape)
			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
			chr.Show()
	
		# def GetSlotIndex(self):
		def RefreshStat(self):
			statSummary = 8.0
			self.curGauge =	[
				float(self.statpoint[0])/statSummary,
				float(self.statpoint[1])/statSummary,
				float(self.statpoint[2])/statSummary,
				float(self.statpoint[3])/statSummary,
			]
	
			for i in xrange(self.LEN_STATPOINT):
				self.statValue[i].SetText(str(self.statpoint[i]))
	
		def ResetStat(self):
			for i in xrange(self.LEN_STATPOINT) :
				self.statpoint[i] = self.M2STATPOINT[self.job_id][i]
			self.RefreshStat()
	
		##Create Character Button##
		def CreateCharacterButton(self):
			if self.job_id == self.M2_INIT_VALUE or self.MotionStart :
				return
	
			textName = self.editCharacterName.GetText()
	
			if False == self.CheckCreateCharacterName(textName):
				return
	
			self.DisableWindow()
	
			chrSlot = self.stream.GetCharacterSlot()
			raceIndex = self.M2_CONST_ID[self.job_id][self.gender]
			shapeIndex = self.shape
			statCon = self.M2STATPOINT[self.job_id][0]
			statInt = self.M2STATPOINT[self.job_id][1]
			statStr = self.M2STATPOINT[self.job_id][2]
			statDex = self.M2STATPOINT[self.job_id][3]
	
			chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED)
			net.SendCreateCharacterPacket(chrSlot, textName, raceIndex, shapeIndex, statCon, statInt, statStr, statDex)
	
			self.MotionStart = True
			self.MotionTime = app.GetTime()
	
		##Cancel Button##
		def CancelButton(self):
			chr.DeleteInstance(self.M2_CONST_ID[self.job_id][self.gender])
			self.stream.SetSelectCharacterPhase()
			self.Hide()
	
		def EmptyFunc(self):
			pass
	
		def PopupMessage(self, msg, func=0):
			if not func:
				func = self.EmptyFunc
	
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)
	
		def OnPressExitKey(self):
			self.CancelButton()
			return True
	
		def CheckCreateCharacterName(self, name):
			if len(name) == 0:
				self.PopupMessage(localeInfo.CREATE_INPUT_NAME, self.EnableWindow)
				return False
	
			if name.find(localeInfo.CREATE_GM_NAME)!=-1:
				self.PopupMessage(localeInfo.CREATE_ERROR_GM_NAME, self.EnableWindow)
				return False
	
			if net.IsInsultIn(name):
				self.PopupMessage(localeInfo.CREATE_ERROR_INSULT_NAME, self.EnableWindow)
				return False
	
			return True
	
		def SetEmpire(self, empire_id):
			self.empireName.SetText(self.EMPIRE_NAME.get(empire_id, ""))
			rgb = self.EMPIRE_NAME_COLOR[empire_id]
			self.empireName.SetFontColor(rgb[0], rgb[1], rgb[2])
			if empire_id != net.EMPIRE_A :
				self.flag.LoadImage(self.flagDict[empire_id])
				self.flag.SetScale(0.45, 0.45)
				self.backGround.LoadImage(self.backGroundDict[empire_id])
				self.backGround.SetScale(float(wndMgr.GetScreenWidth()) / 1920.0, float(wndMgr.GetScreenHeight()) / 1080.0)
	
		def PrevDescriptionPage(self):
			if True == event.IsWait(self.descIndex):
				if event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT >= 0:
					event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT)
					event.Skip(self.descIndex)
			else:
				event.Skip(self.descIndex)
	
		def NextDescriptionPage(self):
			if True == event.IsWait(self.descIndex):
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) + event.BOX_VISIBLE_LINE_COUNT)
				event.Skip(self.descIndex)
			else:
				event.Skip(self.descIndex)
	
		def OverInToolTip(self, arg):
			arglen = len(str(arg))
			pos_x, pos_y = wndMgr.GetMousePosition()
	
			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(11 * arglen)
			self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
			self.toolTip.AppendTextLine(arg, 0xffffff00)
			self.toolTip.Show()
			self.ShowToolTip = True
	
		def OverOutToolTip(self):
			self.toolTip.Hide()
			self.ShowToolTip = False
	
		def ToolTipProgress(self):
			if self.ShowToolTip:
				pos_x, pos_y = wndMgr.GetMousePosition()
				self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
	
		def OnUpdate(self):
			chr.Update()
			self.ToolTipProgress()
	
			(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
			event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+7))
			self.descriptionBox.SetIndex(self.descIndex)
	
			for i in xrange(len(self.NameList)):
				if self.job_id == i	:
					self.NameList[i].SetAlpha(1)
				else :
					self.NameList[i].SetAlpha(0)
	
			for i in xrange(self.LEN_STATPOINT):
				self.GaugeList[i].SetPercentage(self.curGauge[i], 1.0)
	
			if self.MotionStart and self.createSuccess and app.GetTime() - self.MotionTime >= 2.0 :
				chr.DeleteInstance(self.M2_CONST_ID[self.job_id][self.gender])
	
				self.MotionStart = False
				self.stream.SetSelectCharacterPhase()
				self.Hide()
	
else:
	old_open = open
	import chr
	import grp
	import app
	import net
	import snd
	import wndMgr
	import event
	import systemSetting
	import localeInfo
	
	import ui
	import networkModule
	import math
	import snd
	import musicInfo
	import playerSettingModule
	import uiScriptLocale
	import uiToolTip
	
	LOCALE_PATH = "uiscript/"+uiScriptLocale.CODEPAGE+"_"
	
	MAN			= 0
	WOMAN		= 1
	GENDER_LIST = (MAN, WOMAN)
	SHAPE0		= 0
	SHAPE1		= 1
	PAGE_COUNT	= 2
	
	USE_WOLFMAN_CHARACTER = app.ENABLE_WOLFMAN_CHARACTER and not app.DISABLE_WOLFMAN_ON_CREATE
	
	if USE_WOLFMAN_CHARACTER:
		SLOT_COUNT	= (5, 4)
	else:
		SLOT_COUNT	= (4, 4)
	BASE_CHR_ID	= 3
	
	def GetRealID(page):
		realIdx = 0
		for i in xrange(len(SLOT_COUNT)):
			if i>=page:
				break
			realIdx+=SLOT_COUNT[i]
		return realIdx
	
	def GetRealIDnSlot(page, slot):
		realIdx = 0
		for i in xrange(len(SLOT_COUNT)):
			if i>=page:
				break
			realIdx+=SLOT_COUNT[i]
		# import dbg
		# dbg.TraceError("page(%d) slot(%d)=real(%d)+=%d"%(page, slot, realIdx, realIdx+slot))
		return realIdx + slot
	
	class CreateCharacterWindow(ui.Window):
	
		if USE_WOLFMAN_CHARACTER:
			SLOT_ROTATION = [[135.0, 207.0, 279.0, 351.0, 63.0], [135.0, 225.0, 315.0, 45.0]]
		else:
			SLOT_ROTATION = [[135.0, 225.0, 315.0, 45.0], [135.0, 225.0, 315.0, 45.0]]
	
	
		CREATE_STAT_POINT = 0
	
		STAT_CON = 0
		STAT_INT = 1
		STAT_STR = 2
		STAT_DEX = 3
	
		STAT_DESCRIPTION =	{
								STAT_CON : localeInfo.STAT_TOOLTIP_CON,
								STAT_INT : localeInfo.STAT_TOOLTIP_INT,
								STAT_STR : localeInfo.STAT_TOOLTIP_STR,
								STAT_DEX : localeInfo.STAT_TOOLTIP_DEX,
							}
	
		START_STAT =	(  ## CON INT STR DEX
							[ 4, 3, 6, 3, ], ## Warrior
							[ 3, 3, 4, 6, ], ## Assassin
							[ 3, 5, 5, 3, ], ## Sura
							[ 4, 6, 3, 3, ], ## Shaman
							[ 4, 3, 6, 3, ], ## Warrior
							[ 3, 3, 4, 6, ], ## Assassin
							[ 3, 5, 5, 3, ], ## Sura
							[ 4, 6, 3, 3, ], ## Shaman
						)
		if USE_WOLFMAN_CHARACTER:
			tmpStartStat = list(START_STAT)
			tmpStartStat.insert(GetRealIDnSlot(MAN, 5-1), [ 6, 2, 2, 6, ])
			START_STAT = tuple(tmpStartStat)
	
		DESCRIPTION_FILE_NAME =	(
			uiScriptLocale.JOBDESC_WARRIOR_PATH,
			uiScriptLocale.JOBDESC_ASSASSIN_PATH,
			uiScriptLocale.JOBDESC_SURA_PATH,
			uiScriptLocale.JOBDESC_SHAMAN_PATH,
		)
		if USE_WOLFMAN_CHARACTER:
			DESCRIPTION_FILE_NAME += (uiScriptLocale.JOBDESC_WOLFMAN_PATH,)
	
	
		class DescriptionBox(ui.Window):
			def __init__(self):
				ui.Window.__init__(self)
				self.descIndex = 0
			def __del__(self):
				ui.Window.__del__(self)
			def SetIndex(self, index):
				self.descIndex = index
			def OnRender(self):
				event.RenderEventSet(self.descIndex)
	
		class CharacterRenderer(ui.Window):
			def OnRender(self):
				grp.ClearDepthBuffer()
				grp.SetGameRenderState()
				grp.PushState()
				grp.SetOmniLight()
	
				screenWidth = wndMgr.GetScreenWidth()
				screenHeight = wndMgr.GetScreenHeight()
				newScreenWidth = float(screenWidth - 270)
				newScreenHeight = float(screenHeight)
	
				grp.SetViewport(270.0/screenWidth, 0.0, newScreenWidth/screenWidth, newScreenHeight/screenHeight)
	
				app.SetCenterPosition(0.0, 0.0, 0.0)
				app.SetCamera(1550.0, 15.0, 180.0, 95.0)
				grp.SetPerspective(10.0, newScreenWidth/newScreenHeight, 1000.0, 3000.0)
	
				(x, y) = app.GetCursorPosition()
				grp.SetCursorPosition(x, y)
	
				chr.Deform()
				chr.Render()
	
				grp.RestoreViewport()
				grp.PopState()
				grp.SetInterfaceRenderState()
	
		def __init__(self, stream):
			print "NEW CREATE WINDOW ----------------------------------------------------------------------------"
			ui.Window.__init__(self)
			net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, self)
	
			self.stream=stream
	
		def __del__(self):
			print "---------------------------------------------------------------------------- DELETE CREATE WINDOW"
	
			net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, 0)
			ui.Window.__del__(self)
	
		def Open(self):
			print "OPEN CREATE WINDOW ----------------------------------------------------------------------------"
	
			playerSettingModule.LoadGameData("INIT")
	
			self.reservingRaceIndex = -1
			self.reservingShapeIndex = -1
			self.reservingStartTime = 0
			self.stat = [0, 0, 0, 0]
	
			self.gender = 0
			self.slot = -1
			#
			self.instanceIDs = []
			if USE_WOLFMAN_CHARACTER:
				self.shapeList = [
					[0, 0, 0, 0, 0],
					[0, 0, 0, 0]]
			else:
				self.shapeList = [
					[0, 0, 0, 0],
					[0, 0, 0, 0]]
	
			self.descIndex = 0
	
			try:
				dlgBoard = ui.ScriptWindow()
				pythonScriptLoader = ui.PythonScriptLoader()
				pythonScriptLoader.LoadScriptFile(dlgBoard, uiScriptLocale.LOCALE_UISCRIPT_PATH + "createcharacterwindow.py")
	
			except:
				import exception
				exception.Abort("CreateCharacterWindow.Open.LoadObject")
	
			try:
				getChild = dlgBoard.GetChild
	
				self.NameList = {}
				self.NameList[MAN] = []
				self.NameList[MAN].append(getChild("name_warrior"))
				self.NameList[MAN].append(getChild("name_assassin"))
				self.NameList[MAN].append(getChild("name_sura"))
				self.NameList[MAN].append(getChild("name_shaman"))
				if USE_WOLFMAN_CHARACTER:
					self.NameList[MAN].append(getChild("name_wolfman"))
				self.NameList[WOMAN] = []
				self.NameList[WOMAN].append(getChild("name_warrior"))
				self.NameList[WOMAN].append(getChild("name_assassin"))
				self.NameList[WOMAN].append(getChild("name_sura"))
				self.NameList[WOMAN].append(getChild("name_shaman"))
	
				self.GaugeList = []
				self.GaugeList.append(getChild("hth_gauge"))
				self.GaugeList.append(getChild("int_gauge"))
				self.GaugeList.append(getChild("str_gauge"))
				self.GaugeList.append(getChild("dex_gauge"))
	
				self.btnCreate = getChild("create_button")
				self.btnCancel = getChild("cancel_button")
				self.btnPrev = getChild("prev_button")
				self.btnNext = getChild("next_button")
				self.btnLeft = getChild("left_button")
				self.btnRight = getChild("right_button")
				self.textBoard = getChild("text_board")
	
				self.genderButtonList = []
				self.genderButtonList.append(getChild("gender_button_01"))
				self.genderButtonList.append(getChild("gender_button_02"))
	
				self.shapeButtonList = []
				self.shapeButtonList.append(getChild("shape_button_01"))
				self.shapeButtonList.append(getChild("shape_button_02"))
	
				self.editCharacterName = getChild("character_name_value")
	
				self.statValue = []
				self.statValue.append(getChild("hth_value"))
				self.statValue.append(getChild("int_value"))
				self.statValue.append(getChild("str_value"))
				self.statValue.append(getChild("dex_value"))
	
				getChild("hth_button").ShowToolTip = lambda arg=self.STAT_CON: self.OverInStatButton(arg)
				getChild("hth_button").HideToolTip = lambda arg=self.STAT_CON: self.OverOutStatButton()
				getChild("int_button").ShowToolTip = lambda arg=self.STAT_INT: self.OverInStatButton(arg)
				getChild("int_button").HideToolTip = lambda arg=self.STAT_INT: self.OverOutStatButton()
				getChild("str_button").ShowToolTip = lambda arg=self.STAT_STR: self.OverInStatButton(arg)
				getChild("str_button").HideToolTip = lambda arg=self.STAT_STR: self.OverOutStatButton()
				getChild("dex_button").ShowToolTip = lambda arg=self.STAT_DEX: self.OverInStatButton(arg)
				getChild("dex_button").HideToolTip = lambda arg=self.STAT_DEX: self.OverOutStatButton()
	
				getChild("hth_button").Hide()
				getChild("int_button").Hide()
				getChild("str_button").Hide()
				getChild("dex_button").Hide()
	
				self.backGround = getChild("BackGround")
	
			except:
				import exception
				exception.Abort("CreateCharacterWindow.Open.BindObject")
	
			self.btnCreate.SetEvent(ui.__mem_func__(self.CreateCharacter))
			self.btnCancel.SetEvent(ui.__mem_func__(self.CancelCreate))
			self.btnPrev.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			self.btnNext.SetEvent(ui.__mem_func__(self.NextDescriptionPage))
			self.btnLeft.SetEvent(ui.__mem_func__(self.__DecreaseSlotIndex))
			self.btnRight.SetEvent(ui.__mem_func__(self.__IncreaseSlotIndex))
	
			self.genderButtonList[0].SetEvent(ui.__mem_func__(self.__SelectGender), MAN)
			self.genderButtonList[1].SetEvent(ui.__mem_func__(self.__SelectGender), WOMAN)
	
			self.shapeButtonList[0].SetEvent(ui.__mem_func__(self.__SelectShape), SHAPE0)
			self.shapeButtonList[1].SetEvent(ui.__mem_func__(self.__SelectShape), SHAPE1)
			self.editCharacterName.SetReturnEvent(ui.__mem_func__(self.CreateCharacter))
			self.editCharacterName.SetEscapeEvent(ui.__mem_func__(self.CancelCreate))
			self.dlgBoard = dlgBoard
	
			self.curRotation	= [] + self.SLOT_ROTATION[self.gender]
			self.destRotation	= [] + self.SLOT_ROTATION[self.gender]
			self.curNameAlpha	= [0.0, 0.0, 0.0, 0.0, 0.0]
			self.destNameAlpha	= [0.0, 0.0, 0.0, 0.0, 0.0]
			self.curGauge		= [0.0, 0.0, 0.0, 0.0]
			self.destGauge		= [0.0, 0.0, 0.0, 0.0]
	
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.Show()
	
			self.chrRenderer = self.CharacterRenderer()
			self.chrRenderer.SetParent(self.backGround)
			self.chrRenderer.Show()
	
			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.ClearToolTip()
	
			self.editCharacterName.SetText("")
	
			self.EnableWindow()
			self.__SelectSlot(0)
	
			app.SetCamera(500.0, 10.0, 180.0, 95.0)
	
			self.__MakeCharacter(MAN, 0, playerSettingModule.RACE_WARRIOR_M)
			self.__MakeCharacter(MAN, 1, playerSettingModule.RACE_ASSASSIN_M)
			self.__MakeCharacter(MAN, 2, playerSettingModule.RACE_SURA_M)
			self.__MakeCharacter(MAN, 3, playerSettingModule.RACE_SHAMAN_M)
			if USE_WOLFMAN_CHARACTER:
				self.__MakeCharacter(MAN, 4, playerSettingModule.RACE_WOLFMAN_M)
	
			self.__MakeCharacter(WOMAN, 0, playerSettingModule.RACE_WARRIOR_W)
			self.__MakeCharacter(WOMAN, 1, playerSettingModule.RACE_ASSASSIN_W)
			self.__MakeCharacter(WOMAN, 2, playerSettingModule.RACE_SURA_W)
			self.__MakeCharacter(WOMAN, 3, playerSettingModule.RACE_SHAMAN_W)
	
			self.__SelectGender(app.GetRandom(MAN, WOMAN))
			self.__SelectShape(0)
			self.__SelectSlot(app.GetRandom(0, SLOT_COUNT[self.gender]-1))
	
			self.dlgBoard.Show()
			self.Show()
	
			if musicInfo.createMusic != "":
				snd.SetMusicVolume(systemSetting.GetMusicVolume())
				snd.FadeInMusic("BGM/"+musicInfo.createMusic)
	
			app.ShowCursor()
	
		def Close(self):
			print "---------------------------------------------------------------------------- CLOSE CREATE WINDOW"
	
			self.editCharacterName.Enable()
			self.dlgBoard.ClearDictionary()
			self.stream=0
			self.shapeButtonList = []
			self.genderButtonList = []
			self.btnCreate = 0
			self.btnCancel = 0
			self.btnPrev = 0
			self.btnNext = 0
			self.btnLeft = 0
			self.btnRight = 0
			self.textBoard = 0
			self.editCharacterName = 0
			self.backGround = None
	
			if musicInfo.createMusic != "":
				snd.FadeOutMusic("BGM/"+musicInfo.createMusic)
	
			for id in self.instanceIDs:
				chr.DeleteInstance(id)
	
			self.dlgBoard.Hide()
			self.Hide()
	
			app.HideCursor()
			event.Destroy()
	
		def EnableWindow(self):
			self.reservingRaceIndex = -1
			self.reservingShapeIndex = -1
			self.btnCreate.Enable()
			self.btnCancel.Enable()
			self.btnPrev.Enable()
			self.btnNext.Enable()
			self.btnLeft.Enable()
			self.btnRight.Enable()
	
			self.editCharacterName.SetFocus()
			self.editCharacterName.Enable()
	
			for page in xrange(PAGE_COUNT):
				for slot in xrange(SLOT_COUNT[page]):
					chr_id = self.__GetSlotChrID(page, slot)
					chr.SelectInstance(chr_id)
					chr.BlendLoopMotion(chr.MOTION_INTRO_WAIT, 0.1)
	
		def DisableWindow(self):
			self.btnCreate.Disable()
			self.btnCancel.Disable()
			self.btnPrev.Disable()
			self.btnNext.Disable()
			self.btnLeft.Disable()
			self.btnRight.Disable()
			self.editCharacterName.Disable()
	
			self.btnCreate.SetUp()
	
		## Manage Character
		def __GetSlotChrID(self, page, slot):
			return BASE_CHR_ID + GetRealIDnSlot(page, slot)
	
		def __MakeCharacter(self, page, slot, race):
	
			chr_id = self.__GetSlotChrID(page, slot)
	
			chr.CreateInstance(chr_id)
			chr.SelectInstance(chr_id)
			chr.SetVirtualID(chr_id)
			#
			self.instanceIDs.append(chr_id)
	
			chr.SetRace(race)
			chr.SetArmor(0)
			chr.SetHair(0)
	
			chr.Refresh()
			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
	
			chr.SetRotation(0.0)
			chr.Hide()
	
		def __SelectGender(self, gender):
			for button in self.genderButtonList:
				button.SetUp()
	
			self.genderButtonList[gender].Down()
	
			old_gender = self.gender
			self.gender = gender
	
			for v1 in GENDER_LIST:
				for i in xrange(SLOT_COUNT[v1]):
					chr.SelectInstance(self.__GetSlotChrID(v1, i))
					if v1==self.gender:
						chr.Show()
					else:
						chr.Hide()
			self.__ResetNameList(old_gender)
			if self.slot >= SLOT_COUNT[self.gender]:
				# self.NameList[self.slot].SetAlpha(0.0)
				self.__SelectSlot(app.GetRandom(0, SLOT_COUNT[self.gender]-1))
				return # the scene will be already updated, so return or double updated scene
			self.__UpdateScene()
	
		def __SelectShape(self, shape):
			self.shapeList[self.gender][self.slot] = shape
	
			for button in self.shapeButtonList:
				button.SetUp()
	
			self.shapeButtonList[shape].Down()
	
			chr_id = self.__GetSlotChrID(self.gender, self.slot)
			chr.SelectInstance(chr_id)
			chr.ChangeShape(shape)
			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
	
		def GetSlotIndex(self):
			return self.slot
	
		def RefreshStat(self):
			statSummary = self.stat[0] + self.stat[1] + self.stat[2] + self.stat[3]
			self.destGauge =	(
									float(self.stat[0])/float(statSummary),
									float(self.stat[1])/float(statSummary),
									float(self.stat[2])/float(statSummary),
									float(self.stat[3])/float(statSummary),
								)
	
			for i in xrange(4):
				self.statValue[i].SetText(str(self.stat[i]))
	
		def __ResetNameList(self, old_gender):
			for i in xrange(SLOT_COUNT[old_gender]):
				self.destNameAlpha[i] = 0.0
				# self.curNameAlpha[i] += (self.destNameAlpha[i] - self.curNameAlpha[i]) / 10.0
				self.NameList[old_gender][i].SetAlpha(0.0)
	
		def __UpdateScene(self):
			for i in xrange(SLOT_COUNT[self.gender]):
				self.destNameAlpha[i] = 0.0
	
			self.destNameAlpha[self.slot] = 1.0
	
			for i in xrange(SLOT_COUNT[self.gender]):
				self.destRotation[(i+self.slot)%SLOT_COUNT[self.gender]] = self.SLOT_ROTATION[self.gender][i]
	
			if self.IsShow():
				snd.PlaySound("sound/ui/click.wav")
	
			event.ClearEventSet(self.descIndex)
			self.descIndex = event.RegisterEventSet(self.DESCRIPTION_FILE_NAME[self.slot])
	
			if localeInfo.IsARABIC():
				event.SetEventSetWidth(self.descIndex, 170)
	
			chr_id = self.__GetSlotChrID(self.gender, self.slot)
			if chr.HasInstance(chr_id):
				chr.SelectInstance(chr_id)
				self.__SelectShape(self.shapeList[self.gender][self.slot])
	
		def __SelectSlot(self, slot):
	
			if slot < 0:
				return
	
			if slot >= SLOT_COUNT[self.gender]:
				return
	
			if self.slot == slot:
				return
	
			self.slot = slot
			self.ResetStat()
			#
			self.__UpdateScene()
	
		def CreateCharacter(self):
	
			if -1 != self.reservingRaceIndex:
				return
	
			textName = self.editCharacterName.GetText()
			if False == self.__CheckCreateCharacter(textName):
				return
	
			if musicInfo.selectMusic != "":
				snd.FadeLimitOutMusic("BGM/"+musicInfo.selectMusic, systemSetting.GetMusicVolume()*0.05)
	
			self.DisableWindow()
	
	
			chr_id = self.__GetSlotChrID(self.gender, self.slot)
	
			chr.SelectInstance(chr_id)
	
			self.reservingRaceIndex = chr.GetRace()
	
			self.reservingShapeIndex = self.shapeList[self.gender][self.slot]
			self.reservingStartTime = app.GetTime()
	
			for eachSlot in xrange(SLOT_COUNT[self.gender]):
	
				sel_id = self.__GetSlotChrID(self.gender, eachSlot)
	
				chr.SelectInstance(sel_id)
	
				if eachSlot == self.slot:
					chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED)
				else:
					chr.PushOnceMotion(chr.MOTION_INTRO_NOT_SELECTED)
	
		def CancelCreate(self):
			self.stream.SetSelectCharacterPhase()
	
		def __DecreaseSlotIndex(self):
			slotIndex = (self.GetSlotIndex() - 1 + SLOT_COUNT[self.gender]) % SLOT_COUNT[self.gender]
			self.__SelectSlot(slotIndex)
	
		def __IncreaseSlotIndex(self):
			slotIndex = (self.GetSlotIndex() + 1) % SLOT_COUNT[self.gender]
			self.__SelectSlot(slotIndex)
	
		def PrevDescriptionPage(self):
			if True == event.IsWait(self.descIndex):
				if event.GetVisibleStartLine(self.descIndex)-event.BOX_VISIBLE_LINE_COUNT >= 0:
					event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex)-event.BOX_VISIBLE_LINE_COUNT)
					event.Skip(self.descIndex)
			else:
				event.Skip(self.descIndex)
	
		def NextDescriptionPage(self):
			if True == event.IsWait(self.descIndex):
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex)+event.BOX_VISIBLE_LINE_COUNT)
				event.Skip(self.descIndex)
			else:
				event.Skip(self.descIndex)
	
		def __CheckCreateCharacter(self, name):
			if len(name) == 0:
				self.PopupMessage(localeInfo.CREATE_INPUT_NAME, self.EnableWindow)
				return False
	
			if name.find(localeInfo.CREATE_GM_NAME)!=-1:
				self.PopupMessage(localeInfo.CREATE_ERROR_GM_NAME, self.EnableWindow)
				return False
	
			if net.IsInsultIn(name):
				self.PopupMessage(localeInfo.CREATE_ERROR_INSULT_NAME, self.EnableWindow)
				return False
	
			return True
	
		def ResetStat(self):
			realIdx = GetRealIDnSlot(self.gender, self.slot)
			for i in xrange(4):
				self.stat[i] = self.START_STAT[realIdx][i]
			self.lastStatPoint = self.CREATE_STAT_POINT
			self.RefreshStat()
	
		## Event
		def OnCreateSuccess(self):
			self.stream.SetSelectCharacterPhase()
	
		def OnCreateFailure(self, type):
			if 1 == type:
				self.PopupMessage(localeInfo.CREATE_EXIST_SAME_NAME, self.EnableWindow)
			else:
				self.PopupMessage(localeInfo.CREATE_FAILURE, self.EnableWindow)
	
		def OnKeyDown(self, key):
			for i in xrange(SLOT_COUNT[self.gender]):
				if key == 2+i:
					self.__SelectSlot(i)
	
			if 203 == key:
				self.__DecreaseSlotIndex()
			if 205 == key:
				self.__IncreaseSlotIndex()
	
			if 59 == key:
				self.__SelectGender(MAN)
			if 60 == key:
				self.__SelectGender(WOMAN)
	
			return True
	
		def OnUpdate(self):
			chr.Update()
	
			(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
			event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+7))
			self.descriptionBox.SetIndex(self.descIndex)
	
			for i in xrange(SLOT_COUNT[self.gender]):
				self.curNameAlpha[i] += (self.destNameAlpha[i] - self.curNameAlpha[i]) / 10.0
				self.NameList[self.gender][i].SetAlpha(self.curNameAlpha[i])
	
			for i in xrange(4):
				self.curGauge[i] += (self.destGauge[i] - self.curGauge[i]) / 10.0
				if abs(self.curGauge[i] - self.destGauge[i]) < 0.005:
					self.curGauge[i] = self.destGauge[i]
				self.GaugeList[i].SetPercentage(self.curGauge[i], 1.0)
	
			for page in xrange(PAGE_COUNT):
				for i in xrange(SLOT_COUNT[page]):
					chr.SelectInstance(self.__GetSlotChrID(page, i))
	
					distance = 50.0
					rotRadian = self.curRotation[i] * (math.pi*2) / 360.0
					x = distance*math.sin(rotRadian) + distance*math.cos(rotRadian)
					y = distance*math.cos(rotRadian) - distance*math.sin(rotRadian)
					chr.SetPixelPosition(int(x), int(y), 30)
	
					if abs(self.destRotation[i] - self.curRotation[i]) < 1.0:
						self.curRotation[i] = self.destRotation[i]
	
					dir = app.GetRotatingDirection(self.destRotation[i], self.curRotation[i])
					rot = app.GetDegreeDifference(self.destRotation[i], self.curRotation[i])
	
					if app.DEGREE_DIRECTION_RIGHT == dir:
						self.curRotation[i] += rot / 10.0
					elif app.DEGREE_DIRECTION_LEFT == dir:
						self.curRotation[i] -= rot / 10.0
	
					self.curRotation[i] = (self.curRotation[i] + 360.0) % 360.0
	
			###########################################################
			if -1 != self.reservingRaceIndex:
				if app.GetTime() - self.reservingStartTime >= 1.5:
	
					chrSlot=self.stream.GetCharacterSlot()
					textName = self.editCharacterName.GetText()
					raceIndex = self.reservingRaceIndex
					shapeIndex = self.reservingShapeIndex
	
					startStat = self.START_STAT[self.reservingRaceIndex]
					statCon = self.stat[0] - startStat[0]
					statInt = self.stat[1] - startStat[1]
					statStr = self.stat[2] - startStat[2]
					statDex = self.stat[3] - startStat[3]
	
					net.SendCreateCharacterPacket(chrSlot, textName, raceIndex, shapeIndex, statCon, statInt, statStr, statDex)
	
					self.reservingRaceIndex = -1
	
			###########################################################
	
		def EmptyFunc(self):
			pass
	
		def PopupMessage(self, msg, func=0):
			if not func:
				func=self.EmptyFunc
	
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)
	
		def OnPressExitKey(self):
			self.CancelCreate()
			return True
	
		def OverInStatButton(self, stat):
			if not self.STAT_DESCRIPTION.has_key(stat):
				return
	
			self.toolTip.ClearToolTip()
			self.toolTip.AppendTextLine(self.STAT_DESCRIPTION[stat])
			self.toolTip.Show()
	
		def OverOutStatButton(self):
			self.toolTip.Hide()
