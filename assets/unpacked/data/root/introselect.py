import app
if app.ENABLE_OFFICAL_CHARACTER_SCREEN:
	import ui, chr, grp, event, wndMgr, uiToolTip, localeInfo, uiScriptLocale, playerSettingModule, app, net, player, chat, snd, systemSetting
	
	ENABLE_ENGNUM_DELETE_CODE = True
	
	M2_INIT_VALUE = -1
	CHARACTER_SLOT_COUNT_MAX = 5
	
	if app.ENABLE_WOLFMAN_CHARACTER:
		JOB_WARRIOR, JOB_ASSASSIN, JOB_SURA, JOB_SHAMAN, JOB_WOLFMAN = xrange(5)
	else:
		JOB_WARRIOR, JOB_ASSASSIN, JOB_SURA, JOB_SHAMAN	= xrange(4)
		
	class MyCharacters :
		class MyUnit :
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				def __init__(self, const_id, name, level, race, playtime, guildname, form, hair, acce, stat_str, stat_dex, stat_hth, stat_int, change_name):
					self.UnitDataDic = {
						"ID" 	: 	const_id,
						"NAME"	:	name,
						"LEVEL"	:	level,
						"RACE"	:	race,
						"PLAYTIME"	:	playtime,
						"GUILDNAME"	:	guildname,
						"FORM"	:	form,
						"HAIR"	:	hair,
						"ACCE"	:	acce,
						"STR"	:	stat_str,
						"DEX"	:	stat_dex,
						"HTH"	:	stat_hth,
						"INT"	:	stat_int,
						"CHANGENAME"	:	change_name,
					}
	
			else:
				def __init__(self, const_id, name, level, race, playtime, guildname, form, hair, stat_str, stat_dex, stat_hth, stat_int, change_name):
					self.UnitDataDic = {
						"ID" 	: 	const_id,
						"NAME"	:	name,
						"LEVEL"	:	level,
						"RACE"	:	race,
						"PLAYTIME"	:	playtime,
						"GUILDNAME"	:	guildname,
						"FORM"	:	form,
						"HAIR"	:	hair,
						"STR"	:	stat_str,
						"DEX"	:	stat_dex,
						"HTH"	:	stat_hth,
						"INT"	:	stat_int,
						"CHANGENAME"	:	change_name,
					}
	
			def __del__(self) :
				self.UnitDataDic = None
			
			def GetUnitData(self) :
				return self.UnitDataDic
	
		def __init__(self, stream) :
			self.MainStream = stream
			self.PriorityData = []
			self.myUnitDic = {}
			self.HowManyChar = 0
			self.EmptySlot	=  []
			self.Race 		= [None, None, None, None, None]
			self.Job		= [None, None, None, None, None]
			self.Guild_Name = [None, None, None, None, None]
			self.Play_Time 	= [None, None, None, None, None]
			self.Change_Name= [None, None, None, None, None]
			self.Stat_Point = { 0 : None, 1 : None, 2 : None, 3 : None, 4 : None }
	
		def __del__(self) :
			self.MainStream = None 
			
			for i in xrange(self.HowManyChar) :
				chr.DeleteInstance(i)
				
			self.PriorityData = None
			self.myUnitDic = None
			self.HowManyChar = None
			self.EmptySlot	= None
			self.Race = None
			self.Job = None
			self.Guild_Name = None
			self.Play_Time = None
			self.Change_Name = None
			self.Stat_Point = None
				
		def LoadCharacterData(self) :
			self.RefreshData()
			self.MainStream.All_ButtonInfoHide()
	
			for i in xrange(CHARACTER_SLOT_COUNT_MAX):
				pid = net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_ID)
	
				if not pid:
					self.EmptySlot.append(i)
					continue
					
				name 			= net.GetAccountCharacterSlotDataString(i, net.ACCOUNT_CHARACTER_SLOT_NAME)
				level 			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
				race 			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_RACE)
				playtime 		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
				guildname 		= net.GetAccountCharacterSlotDataString(i, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME)
				form 			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_FORM)
				hair 			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_HAIR)
				stat_str 		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_STR)
				stat_dex		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_DEX)
				stat_hth		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_HTH)
				stat_int		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_INT)
				# last_playtime	= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_LAST_PLAYTIME)
				last_playtime	= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
				change_name		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_CHANGE_NAME_FLAG)
				
				self.SetPriorityData(last_playtime, i)
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					acce = net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_ACCE)
					self.myUnitDic[i] = self.MyUnit(i, name, level, race, playtime, guildname, form, hair, acce, stat_str, stat_dex, stat_hth, stat_int, change_name)
				else:
					self.myUnitDic[i] = self.MyUnit(i, name, level, race, playtime, guildname, form, hair, stat_str, stat_dex, stat_hth, stat_int, change_name)
				
			self.PriorityData.sort(reverse = True)
	
			for i in xrange(len(self.PriorityData)) :
				time, index = self.PriorityData[i]
				DestDataDic = self.myUnitDic[index].GetUnitData()
				
				self.SetSortingData(i, DestDataDic["RACE"], DestDataDic["GUILDNAME"], DestDataDic["PLAYTIME"], DestDataDic["STR"], DestDataDic["DEX"], DestDataDic["HTH"], DestDataDic["INT"], DestDataDic["CHANGENAME"])
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					self.MakeCharacter(i, DestDataDic["NAME"], DestDataDic["RACE"], DestDataDic["FORM"], DestDataDic["HAIR"], DestDataDic["ACCE"])
				else:
					self.MakeCharacter(i, DestDataDic["NAME"], DestDataDic["RACE"], DestDataDic["FORM"], DestDataDic["HAIR"])
	
				self.MainStream.InitDataSet(i, DestDataDic["NAME"], DestDataDic["LEVEL"], DestDataDic["ID"])
	
			if self.HowManyChar :
				self.MainStream.SelectButton(0)
	
			net.SelectCharacterCacheDestroy()
			return self.HowManyChar
			
		def SetPriorityData(self, last_playtime, index) :
			self.PriorityData.append([last_playtime, index])
		
		def MakeCharacter(self, slot, name, race, form, hair, acce = 0):
			chr.CreateInstance(slot)
			chr.SelectInstance(slot)
			chr.SetVirtualID(slot)
			chr.SetNameString(name)
	
			chr.SetRace(race)
			chr.SetArmor(form)
			chr.SetHair(hair)
			
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				chr.SetAcce(acce)
		
			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
			
			if app.ENABLE_WOLFMAN_CHARACTER and chr.RaceToJob(race) == JOB_WOLFMAN:
				chr.SetScale(0.95, 0.95, 0.95)
				
			chr.SetRotation(0.0)
			chr.Hide()
			
		def SetSortingData(self, slot, race, guildname, playtime, pStr, pDex, pHth, pInt, changename) :	
			self.HowManyChar += 1
			self.Race[slot] = race
			self.Job[slot] = chr.RaceToJob(race)
			self.Guild_Name[slot] = guildname
			self.Play_Time[slot] = playtime
			self.Change_Name[slot] = changename
			self.Stat_Point[slot] = [pHth, pInt, pStr, pDex]
		
		def GetRace(self, slot) :
			return self.Race[slot]
		
		def GetJob(self, slot) :
			return self.Job[slot]
			
		def GetMyCharacterCount(self) :
			return self.HowManyChar
			
		def GetEmptySlot(self) :
			if not len(self.EmptySlot) :
				return M2_INIT_VALUE
			
			return self.EmptySlot[0]
			
		def GetStatPoint(self, slot) :			
			return self.Stat_Point[slot]
		
		def GetGuildNamePlayTime(self, slot) :
			return self.Guild_Name[slot], self.Play_Time[slot]
			
		def GetChangeName(self, slot) :
			return self.Change_Name[slot]
			
		def SetChangeNameSuccess(self, slot) :
			self.Change_Name[slot] = 0
			
		def RefreshData(self) :
			self.HowManyChar = 0
			self.EmptySlot	=  []
			self.PriorityData = []
			self.Race 		= [None, None, None, None, None]
			self.Guild_Name = [None, None, None, None, None]
			self.Play_Time 	= [None, None, None, None, None]
			self.Change_Name= [None, None, None, None, None]
			self.Stat_Point = { 0 : None, 1 : None, 2 : None, 3 : None, 4 : None }
			
	class SelectCharacterWindow(ui.Window) :	
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
		RACE_FACE_PATH = {
			playerSettingModule.RACE_WARRIOR_M		:	"D:/ymir work/ui/intro/public_intro/face/face_warrior_m_0",
			playerSettingModule.RACE_ASSASSIN_W		:	"D:/ymir work/ui/intro/public_intro/face/face_assassin_w_0",
			playerSettingModule.RACE_SURA_M			:	"D:/ymir work/ui/intro/public_intro/face/face_sura_m_0",
			playerSettingModule.RACE_SHAMAN_W		:	"D:/ymir work/ui/intro/public_intro/face/face_shaman_w_0",
			playerSettingModule.RACE_WARRIOR_W		:	"D:/ymir work/ui/intro/public_intro/face/face_warrior_w_0",
			playerSettingModule.RACE_ASSASSIN_M		:	"D:/ymir work/ui/intro/public_intro/face/face_assassin_m_0",
			playerSettingModule.RACE_SURA_W			:	"D:/ymir work/ui/intro/public_intro/face/face_sura_w_0",
			playerSettingModule.RACE_SHAMAN_M		:	"D:/ymir work/ui/intro/public_intro/face/face_shaman_m_0",
			playerSettingModule.RACE_WOLFMAN_M		:	"D:/ymir work/ui/intro/public_intro/face/face_wolfman_m_0",
		}
		DISC_FACE_PATH = {
			playerSettingModule.RACE_WARRIOR_M		:"d:/ymir work/bin/icon/face/warrior_m.tga",
			playerSettingModule.RACE_ASSASSIN_W		:"d:/ymir work/bin/icon/face/assassin_w.tga",
			playerSettingModule.RACE_SURA_M			:"d:/ymir work/bin/icon/face/sura_m.tga",
			playerSettingModule.RACE_SHAMAN_W		:"d:/ymir work/bin/icon/face/shaman_w.tga",
			playerSettingModule.RACE_WARRIOR_W		:"d:/ymir work/bin/icon/face/warrior_w.tga",
			playerSettingModule.RACE_ASSASSIN_M		:"d:/ymir work/bin/icon/face/assassin_m.tga",
			playerSettingModule.RACE_SURA_W			:"d:/ymir work/bin/icon/face/sura_w.tga",
			playerSettingModule.RACE_SHAMAN_M		:"d:/ymir work/bin/icon/face/shaman_m.tga",
			playerSettingModule.RACE_WOLFMAN_M		:"d:/ymir work/bin/icon/face/wolfman_m.tga",
		}
	
		##Job Description## 
		DESCRIPTION_FILE_NAME =	[
			uiScriptLocale.JOBDESC_WARRIOR_PATH,
			uiScriptLocale.JOBDESC_ASSASSIN_PATH,
			uiScriptLocale.JOBDESC_SURA_PATH,
			uiScriptLocale.JOBDESC_SHAMAN_PATH,
			uiScriptLocale.JOBDESC_WOLFMAN_PATH,
		]
	
		##Job List##
		JOB_LIST = { 	
			0	:	localeInfo.JOB_WARRIOR,	
			1	:	localeInfo.JOB_ASSASSIN,	
			2	:	localeInfo.JOB_SURA,
			3	:	localeInfo.JOB_SHAMAN,		 
			4:	localeInfo.JOB_WOLFMAN,
		}
		if app.ENABLE_WOLFMAN_CHARACTER:
			RACE_FACE_PATH[playerSettingModule.RACE_WOLFMAN_M] = "D:/ymir work/ui/intro/public_intro/face/face_wolfman_m_0"
			DISC_FACE_PATH[playerSettingModule.RACE_WOLFMAN_M] = "icon/face/wolfman_m.tga"
			DESCRIPTION_FILE_NAME += [uiScriptLocale.JOBDESC_WOLFMAN_PATH]
			JOB_LIST[4] = localeInfo.JOB_WOLFMAN
	
		Rotation = 0
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
	
				app.SetCenterPosition(0.0, 0.0, 0.0) #X, Z, Y ( X+ RIGHT, Z+ ??, Y+ DOWN ) ? ? ??? ? ? 
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
			ui.Window.__init__(self)
			net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)
			self.stream = stream
			
			##Init Value##
			self.SelectSlot = M2_INIT_VALUE
			self.SelectEmpire = False
			self.ShowToolTip = False
			self.select_job = M2_INIT_VALUE
			self.select_race = M2_INIT_VALUE
			self.LEN_STATPOINT = 4
			self.descIndex = 0
			self.statpoint = [0, 0, 0, 0]
			self.curGauge  = [0.0, 0.0, 0.0, 0.0]
			self.Name_FontColor_Def	 = grp.GenerateColor(0.7215, 0.7215, 0.7215, 1.0)
			self.Name_FontColor		 = grp.GenerateColor(197.0/255.0, 134.0/255.0, 101.0/255.0, 1.0)
			self.Level_FontColor 	 = grp.GenerateColor(250.0/255.0, 211.0/255.0, 136.0/255.0, 1.0)
			self.Not_SelectMotion = False
			self.MotionStart = False
			self.MotionTime = 0.0
			self.RealSlot = []
			self.Disable = False
			self.Rotation = 0
		def __del__(self):
			ui.Window.__del__(self)
			net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, 0)
			
		def Open(self):
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/characterselect.mp3")
			dlgBoard = ui.ScriptWindow()
			self.dlgBoard = dlgBoard
			pythonScriptLoader = ui.PythonScriptLoader()
			pythonScriptLoader.LoadScriptFile( self.dlgBoard, "UIScript/selectcharacterwindow.py" )
	
			getChild = self.dlgBoard.GetChild
			
			##Background##
			self.backGroundDict = {
				net.EMPIRE_A : "d:/ymir work/ui/intro/empire/background/background.jpg",
				net.EMPIRE_B : "d:/ymir work/ui/intro/empire/background/background.jpg",
				net.EMPIRE_C : "d:/ymir work/ui/intro/empire/background/background.jpg",
			}
			self.backGround = getChild("BackGround")
		
			##??##
			self.NameList = []
			self.NameList.append(getChild("name_warrior"))
			self.NameList.append(getChild("name_assassin"))
			self.NameList.append(getChild("name_sura"))
			self.NameList.append(getChild("name_shaman"))
			# if app.ENABLE_WOLFMAN_CHARACTER:
				# self.NameList.append(getChild("name_wolfman"))
			
			##Empire Flag##
			self.empireName = getChild("EmpireName")
			self.flagDict = {
				net.EMPIRE_A : "d:/ymir work/ui/intro/empire/empireflag_a.sub",
				net.EMPIRE_B : "d:/ymir work/ui/intro/empire/empireflag_b.sub",
				net.EMPIRE_C : "d:/ymir work/ui/intro/empire/empireflag_c.sub",
			}
			self.flag = getChild("EmpireFlag")
	
			##Button List##
			self.btnStart		= getChild("start_button")
			self.btnCreate		= getChild("create_button")
			self.btnDelete		= getChild("delete_button")
			self.btnExit		= getChild("exit_button")
			
			##Face Image##
			self.FaceImage = []
			self.FaceImage.append(getChild("CharacterFace_0"))
			self.FaceImage.append(getChild("CharacterFace_1"))
			self.FaceImage.append(getChild("CharacterFace_2"))
			self.FaceImage.append(getChild("CharacterFace_3"))
			self.FaceImage.append(getChild("CharacterFace_4"))
			
			##Select Character List##
			self.CharacterButtonList = []
			self.CharacterButtonList.append(getChild("CharacterSlot_0"))
			self.CharacterButtonList.append(getChild("CharacterSlot_1"))
			self.CharacterButtonList.append(getChild("CharacterSlot_2"))
			self.CharacterButtonList.append(getChild("CharacterSlot_3"))
			self.CharacterButtonList.append(getChild("CharacterSlot_4"))
			
			##ToolTip : GuildName, PlayTime##
			getChild("CharacterSlot_0").ShowToolTip = lambda arg = 0 : self.OverInToolTip(arg)
			getChild("CharacterSlot_0").HideToolTip = lambda : self.OverOutToolTip()
			getChild("CharacterSlot_1").ShowToolTip = lambda arg = 1 : self.OverInToolTip(arg)
			getChild("CharacterSlot_1").HideToolTip = lambda : self.OverOutToolTip()
			getChild("CharacterSlot_2").ShowToolTip = lambda arg = 2 : self.OverInToolTip(arg)
			getChild("CharacterSlot_2").HideToolTip = lambda : self.OverOutToolTip()
			getChild("CharacterSlot_3").ShowToolTip = lambda arg = 3 : self.OverInToolTip(arg)
			getChild("CharacterSlot_3").HideToolTip = lambda : self.OverOutToolTip()
			if app.ENABLE_WOLFMAN_CHARACTER:
				getChild("CharacterSlot_4").ShowToolTip = lambda arg = 4 : self.OverInToolTip(arg)
				getChild("CharacterSlot_4").HideToolTip = lambda : self.OverOutToolTip()
			
			## ToolTip etc : Create, Delete, Start, Exit, Prev, Next ##
			getChild("create_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_CREATE : self.OverInToolTipETC(arg)
			getChild("create_button").HideToolTip = lambda : self.OverOutToolTip()
			getChild("delete_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_DELETE : self.OverInToolTipETC(arg)
			getChild("delete_button").HideToolTip = lambda : self.OverOutToolTip()
			getChild("start_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_SELECT : self.OverInToolTipETC(arg)
			getChild("start_button").HideToolTip = lambda : self.OverOutToolTip()
			getChild("exit_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_EXIT : self.OverInToolTipETC(arg)
			getChild("exit_button").HideToolTip = lambda : self.OverOutToolTip()
			getChild("prev_button").ShowToolTip = lambda arg = uiScriptLocale.CREATE_PREV : self.OverInToolTipETC(arg)
			getChild("prev_button").HideToolTip = lambda : self.OverOutToolTip()
			getChild("next_button").ShowToolTip = lambda arg = uiScriptLocale.CREATE_NEXT : self.OverInToolTipETC(arg)
			getChild("next_button").HideToolTip = lambda : self.OverOutToolTip()
			
			
			##StatPoint Value##
			self.statValue = []
			self.statValue.append(getChild("hth_value"))
			self.statValue.append(getChild("int_value"))
			self.statValue.append(getChild("str_value"))
			self.statValue.append(getChild("dex_value"))
			
			##Gauge UI##
			self.GaugeList = []
			self.GaugeList.append(getChild("hth_gauge"))
			self.GaugeList.append(getChild("int_gauge"))
			self.GaugeList.append(getChild("str_gauge"))
			self.GaugeList.append(getChild("dex_gauge"))
			
			##Text##
			self.textBoard = getChild("text_board")
			self.btnPrev = getChild("prev_button")
			self.btnNext = getChild("next_button")
			
			##DescFace##
			self.discFace = getChild("DiscFace")
			self.raceNameText = getChild("raceName_Text")
			
			##MyID##
			# self.descPhaseText = getChild("desc_phase_text")
			self.myID = getChild("my_id")
			self.myID.SetText(net.GetLoginID())
			
			##Button Event##
			self.btnStart.SetEvent(ui.__mem_func__(self.StartGameButton))
			self.btnCreate.SetEvent(ui.__mem_func__(self.CreateCharacterButton))
			self.btnExit.SetEvent(ui.__mem_func__(self.ExitButton))
			self.btnDelete.SetEvent(ui.__mem_func__(self.InputPrivateCode))		
			
			##Select MyCharacter##
			self.CharacterButtonList[0].SetEvent(ui.__mem_func__(self.SelectButton), 0)
			self.CharacterButtonList[1].SetEvent(ui.__mem_func__(self.SelectButton), 1)
			self.CharacterButtonList[2].SetEvent(ui.__mem_func__(self.SelectButton), 2)
			self.CharacterButtonList[3].SetEvent(ui.__mem_func__(self.SelectButton), 3)
			self.CharacterButtonList[4].SetEvent(ui.__mem_func__(self.SelectButton), 4)
	
			self.FaceImage[0].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_click", 0)
			self.FaceImage[1].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_click", 1)
			self.FaceImage[2].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_click", 2)
			self.FaceImage[3].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_click", 3)
			self.FaceImage[4].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_click", 4)
	
			self.FaceImage[0].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
			self.FaceImage[1].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 1)
			self.FaceImage[2].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 2)
			self.FaceImage[3].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 3)
			self.FaceImage[4].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 4)
	
			self.FaceImage[0].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
			self.FaceImage[1].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 1)
			self.FaceImage[2].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 2)
			self.FaceImage[3].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 3)
			self.FaceImage[4].SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 4)
	
			##Job Description##
			self.btnPrev.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			self.btnNext.SetEvent(ui.__mem_func__(self.NextDescriptionPage))
			
			##MyCharacter CLASS##
			self.mycharacters = MyCharacters(self)
			self.mycharacters.LoadCharacterData()
					
			if not self.mycharacters.GetMyCharacterCount() :
				self.stream.SetCharacterSlot(self.mycharacters.GetEmptySlot())
				self.SelectEmpire = False
			
			##Job Description Box##
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.Show()
			
			##Tool Tip(Guild Name, PlayTime)##
			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.ClearToolTip()
			
			self.dlgBoard.Show()
			self.Show()
			
			##Empire Flag & Background Setting##
			my_empire = net.GetEmpireID()
			self.SetEmpire(my_empire)
		
			app.ShowCursor()
			
			##Character Render##
			self.chrRenderer = self.CharacterRenderer()
			self.chrRenderer.SetParent(self.backGround)
			self.chrRenderer.Show()
			
			##Default Setting##
		def EventProgress(self, event_type, slot) :
			if self.Disable :
				return
	
			if "mouse_click" == event_type :
				if slot == self.SelectSlot :
					return 
				self.SelectButton(slot)
	
			elif "mouse_over_in" == event_type :
				for button in self.CharacterButtonList :
					button.SetUp()
			
				self.CharacterButtonList[slot].Over()
				self.CharacterButtonList[self.SelectSlot].Down()
				self.OverInToolTip(slot)
	
			elif "mouse_over_out" == event_type :
				for button in self.CharacterButtonList :
					button.SetUp()
				
				self.CharacterButtonList[self.SelectSlot].Down()
				self.OverOutToolTip()
			else :
				pass
			
		def SelectButton(self, slot):		
			if slot >= self.mycharacters.GetMyCharacterCount() or slot == self.SelectSlot :
				return
				
			if self.Not_SelectMotion or self.MotionTime != 0.0 :
				self.CharacterButtonList[slot].SetUp()
				self.CharacterButtonList[slot].Over()
				return
			
			for button in self.CharacterButtonList:
				button.SetUp()
						
			self.SelectSlot = slot
			self.CharacterButtonList[self.SelectSlot].Down()
			self.stream.SetCharacterSlot(self.RealSlot[self.SelectSlot])
			
			self.select_job = self.mycharacters.GetJob(self.SelectSlot)
			
			##Job Descirption##
			event.ClearEventSet(self.descIndex)
			self.descIndex = event.RegisterEventSet(self.DESCRIPTION_FILE_NAME[self.select_job])
			event.SetFontColor(self.descIndex, 0.7843, 0.7843, 0.7843)
			
			event.SetRestrictedCount(self.descIndex, 35)
	
			if event.BOX_VISIBLE_LINE_COUNT >= event.GetTotalLineCount(self.descIndex):
				self.btnPrev.Hide()
				self.btnNext.Hide()
			else :
				self.btnPrev.Show()
				self.btnNext.Show()
			
			self.ResetStat()
			
			## ?? Setting ##
			for i in xrange(len(self.NameList)):
				if self.select_job == i	: 
					self.NameList[i].SetAlpha(1)
				else :
					self.NameList[i].SetAlpha(0)
			
			## Face Setting & Font Color Setting ##
			self.select_race = self.mycharacters.GetRace(self.SelectSlot)
			for i in xrange(self.mycharacters.GetMyCharacterCount()) :
				if slot == i :
					self.FaceImage[slot].LoadImage(self.RACE_FACE_PATH[self.select_race] + "1.sub")
					self.CharacterButtonList[slot].SetAppendTextColor(0, self.Name_FontColor)
				else :
					self.FaceImage[i].LoadImage(self.RACE_FACE_PATH[self.mycharacters.GetRace(i)] + "2.sub")
					self.CharacterButtonList[i].SetAppendTextColor(0, self.Name_FontColor_Def)
			
			## Desc Face & raceText Setting ##
			self.discFace.LoadImage(self.DISC_FACE_PATH[self.select_race])
			self.raceNameText.SetText(self.JOB_LIST[self.select_job])
			
			chr.Hide()
			chr.SelectInstance(self.SelectSlot)
			chr.Show()
			
		def Close(self):
			snd.FadeOutMusic("BGM/characterselect.mp3")
			del self.mycharacters
			self.EMPIRE_NAME = None
			self.EMPIRE_NAME_COLOR = None
			self.RACE_FACE_PATH = None
			self.DISC_FACE_PATH = None
			self.DESCRIPTION_FILE_NAME = None
			self.JOB_LIST = None
			
			##Default Value##
			self.SelectSlot = None
			self.SelectEmpire = None
			self.ShowToolTip = None
			self.LEN_STATPOINT = None
			self.descIndex = None
			self.statpoint = None#[]
			self.curGauge  = None#[]
			self.Name_FontColor_Def	 = None
			self.Name_FontColor		 = None
			self.Level_FontColor 	 = None
			self.Not_SelectMotion = None
			self.MotionStart = None
			self.MotionTime = None
			self.RealSlot = None
		
			self.select_job = None
			self.select_race = None
			
			##Open Func##
			self.dlgBoard = None
			self.backGround = None
			self.backGroundDict = None
			self.NameList = None#[]
			self.empireName = None
			self.flag = None
			self.flagDict = None#{}
			self.btnStart = None	
			self.btnCreate = None	
			self.btnDelete = None	
			self.btnExit = None	
			self.FaceImage = None#[]
			self.CharacterButtonList = None#[]
			self.statValue = None#[]
			self.GaugeList = None#[]
			self.textBoard = None
			self.btnPrev = None
			self.btnNext = None
			self.raceNameText = None
			#self.descPhaseText = None
			self.myID = None
			
			self.descriptionBox = None
			self.toolTip = None
			self.Disable = None
	
			self.Hide()
			self.KillFocus()
			app.HideCursor()
			event.Destroy()
			
		def SetEmpire(self, empire_id):
			self.empireName.SetText(self.EMPIRE_NAME.get(empire_id, ""))
			rgb = self.EMPIRE_NAME_COLOR[empire_id]
			self.empireName.SetFontColor(rgb[0], rgb[1], rgb[2])
			if empire_id != net.EMPIRE_A :
				self.flag.LoadImage(self.flagDict[empire_id])
				self.flag.SetScale(0.45, 0.45)
				self.backGround.LoadImage(self.backGroundDict[empire_id])
				self.backGround.SetScale(float(wndMgr.GetScreenWidth()) / 1920.0, float(wndMgr.GetScreenHeight()) / 1080.0)
							
		def CreateCharacterButton(self):
			slotNumber = self.mycharacters.GetEmptySlot()
				
			if slotNumber == M2_INIT_VALUE:
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.CREATE_FULL, 0, localeInfo.UI_OK)
				return 
			
			pid = self.GetCharacterSlotPID(slotNumber)
			
			if not pid:
				self.stream.SetCharacterSlot(slotNumber)
	
				if not self.mycharacters.GetMyCharacterCount() :
					self.SelectEmpire = True
				else :
					self.stream.SetCreateCharacterPhase()
					self.Hide()
			
		def ExitButton(self):
			self.stream.SetLoginPhase()		
			self.Hide()
			
		def StartGameButton(self):
	
			if self.mycharacters.GetChangeName(self.SelectSlot):
				self.OpenChangeNameDialog()
				return
	
			if not self.mycharacters.GetMyCharacterCount():
				return
	
			self.MotionStart = True
			self.DisableWindow()
		
			chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED)
	
			self.MotionTime = app.GetTime()
	
		def OnUpdate(self):
			chr.Update()
			# self.Rotation = self.Rotation - 1
			# chr.SetRotation(self.Rotation)
			self.ToolTipProgress()
			
			if self.SelectEmpire :
				self.SelectEmpire = False
				self.stream.SetReselectEmpirePhase()
				self.Hide()
				
			# if self.MotionStart and app.GetTiime() - self.MotionTime >= 0.1:
			if self.MotionStart:
				self.MotionStart = False
				chrSlot = self.stream.GetCharacterSlot()
			
				net.DirectEnter(chrSlot)
				playTime = net.GetAccountCharacterSlotDataInteger(chrSlot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
	
				player.SetPlayTime(playTime)
				chat.Clear()
			
			(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
			event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+7))
			self.descriptionBox.SetIndex(self.descIndex)
			
			for i in xrange(self.LEN_STATPOINT):
				self.GaugeList[i].SetPercentage(self.curGauge[i], 1.0)
	
		# def Refresh(self):
		def GetCharacterSlotPID(self, slotIndex):
			return net.GetAccountCharacterSlotDataInteger(slotIndex, net.ACCOUNT_CHARACTER_SLOT_ID)
		
		def All_ButtonInfoHide(self) :
	
			for i in xrange(CHARACTER_SLOT_COUNT_MAX):
				self.CharacterButtonList[i].Hide()
				self.FaceImage[i].Hide()
				
		def InitDataSet(self, slot, name, level, real_slot):	
			width = self.CharacterButtonList[slot].GetWidth()
			height = self.CharacterButtonList[slot].GetHeight()
			self.CharacterButtonList[slot].AppendTextLine(name				, (localeInfo.GetDefaultFont() if app.ENABLE_FONT_SELECT else localeInfo.UI_DEF_FONT), self.Name_FontColor_Def	, "right", width - 12, height/4 + 2)
			self.CharacterButtonList[slot].AppendTextLine("Lv." + str(level), (localeInfo.GetDefaultFont() if app.ENABLE_FONT_SELECT else localeInfo.UI_DEF_FONT), self.Level_FontColor		, "left", width - 42, height*3/4)
	
			self.CharacterButtonList[slot].Show()
			self.FaceImage[slot].LoadImage(self.RACE_FACE_PATH[self.mycharacters.GetRace(slot)] + "2.sub")
			self.FaceImage[slot].Show()
			self.RealSlot.append(real_slot)
					
		def InputPrivateCode(self) :
			if not self.mycharacters.GetMyCharacterCount() :
				return
				
			import uiCommon
			privateInputBoard = uiCommon.InputDialogWithDescription()
			privateInputBoard.SetTitle(localeInfo.INPUT_PRIVATE_CODE_DIALOG_TITLE)
			privateInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrivateCode))
			privateInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrivateCode))
			
			if ENABLE_ENGNUM_DELETE_CODE:
				pass
			else:
				privateInputBoard.SetNumberMode()
				
			privateInputBoard.SetSecretMode()
			privateInputBoard.SetMaxLength(7)
				
			privateInputBoard.SetBoardWidth(250)
			privateInputBoard.SetDescription(localeInfo.INPUT_PRIVATE_CODE_DIALOG_DESCRIPTION)
			privateInputBoard.Open()
			self.privateInputBoard = privateInputBoard
			
			self.DisableWindow()
			
			if not self.Not_SelectMotion:
				self.Not_SelectMotion = True
				chr.PushOnceMotion(chr.MOTION_INTRO_NOT_SELECTED, 0.1)
			
		def AcceptInputPrivateCode(self) :
			privateCode = self.privateInputBoard.GetText()
			if not privateCode:
				return
			
			pid = net.GetAccountCharacterSlotDataInteger(self.RealSlot[self.SelectSlot], net.ACCOUNT_CHARACTER_SLOT_ID)
			
			if not pid :
				self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
				return
	
			net.SendDestroyCharacterPacket(self.RealSlot[self.SelectSlot], privateCode)
			self.PopupMessage(localeInfo.SELECT_DELEING)
	
			self.CancelInputPrivateCode()
			return True
		
		def CancelInputPrivateCode(self) :
			self.privateInputBoard = None
			self.Not_SelectMotion = False
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
			self.EnableWindow()
			return True
			
		def OnDeleteSuccess(self, slot):
			self.PopupMessage(localeInfo.SELECT_DELETED)
			for i in xrange(len(self.RealSlot)):
				chr.DeleteInstance(i)
				
			self.RealSlot = []
			self.SelectSlot = M2_INIT_VALUE
			
			for button in self.CharacterButtonList :
				button.AppendTextLineAllClear()
						
			if not self.mycharacters.LoadCharacterData() :
				self.stream.popupWindow.Close()
				self.stream.SetCharacterSlot(self.mycharacters.GetEmptySlot())
				self.SelectEmpire = True
		
		def OnDeleteFailure(self):
			self.PopupMessage(localeInfo.SELECT_CAN_NOT_DELETE)
				
		def EmptyFunc(self):
			pass
	
		def PopupMessage(self, msg, func=0):
			if not func:
				func=self.EmptyFunc
	
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)
		
		def RefreshStat(self):
			statSummary = 90.0 
			self.curGauge =	[
				float(self.statpoint[0])/statSummary,
				float(self.statpoint[1])/statSummary,
				float(self.statpoint[2])/statSummary,
				float(self.statpoint[3])/statSummary,
			]
								
			for i in xrange(self.LEN_STATPOINT) :
				self.statValue[i].SetText(str(self.statpoint[i]))
	
		def ResetStat(self):
			myStatPoint = self.mycharacters.GetStatPoint(self.SelectSlot)
			
			if not myStatPoint :
				return
			
			for i in xrange(self.LEN_STATPOINT) :
				self.statpoint[i] = myStatPoint[i]
			
			self.RefreshStat()
		
		##Job Description Prev & Next Button##
		def PrevDescriptionPage(self):
			if True == event.IsWait(self.descIndex) :
				if event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT >= 0:
					event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT)
					event.Skip(self.descIndex)
			else :
				event.Skip(self.descIndex)
		
		def NextDescriptionPage(self):
			if True == event.IsWait(self.descIndex):
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) + event.BOX_VISIBLE_LINE_COUNT)
				event.Skip(self.descIndex)
			else :
				event.Skip(self.descIndex)
		
		##ToolTip : GuildName, PlayTime##
		def OverInToolTip(self, slot):
			GuildName = localeInfo.GUILD_NAME
			myGuildName, myPlayTime = self.mycharacters.GetGuildNamePlayTime(slot)
			pos_x, pos_y = self.CharacterButtonList[slot].GetGlobalPosition()
			
			if not myGuildName :
				myGuildName = localeInfo.SELECT_NOT_JOIN_GUILD
	
			guild_name = GuildName + " : " + myGuildName
			play_time = uiScriptLocale.SELECT_PLAYTIME + " :"
			day = myPlayTime / (60 * 24)
			if day : 
				play_time = play_time + " " + str(day) + localeInfo.DAY
			hour = (myPlayTime - (day * 60 * 24))/60
			if hour :
				play_time = play_time + " " + str(hour) + localeInfo.HOUR
			min = myPlayTime - (hour * 60) - (day * 60 * 24)
		
			play_time = play_time + " " + str(min) + localeInfo.MINUTE
			
			textlen = max(len(guild_name), len(play_time))
			tooltip_width = 6 * textlen + 22
	
			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(tooltip_width)
	
			self.toolTip.SetToolTipPosition(pos_x + 173 + tooltip_width/2, pos_y + 34)
			self.toolTip.AppendTextLine(guild_name, 0xffe4cb1b, False)
			self.toolTip.AppendTextLine(play_time, 0xffffff00, False)
	
			self.toolTip.Show()
		
		def OverInToolTipETC(self, arg):
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
		
		def SameLoginDisconnect(self):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.LOGIN_FAILURE_SAMELOGIN, self.ExitButton, localeInfo.UI_OK)
			
		def OnIMEReturn(self):
			self.StartGameButton()
			return True
		
		def OnPressEscapeKey(self):
			self.ExitButton()
			return True
		
		def OnKeyDown(self, key):
			if self.MotionTime != 0.0:
				return
				
			if 2 == key: #1
				self.SelectButton(0)
			elif 3 == key:
				self.SelectButton(1)
			elif 4 == key:
				self.SelectButton(2)
			elif 5 == key:
				self.SelectButton(3)
			elif 6 == key:
				self.SelectButton(4)
			elif 28 == key: #and not self.stream.popupWindow.IsShow():
				self.StartGameButton()
			elif 200 == key or 208 == key:
				self.KeyInputUpDown(key)
			else:
				return True
	
			return True
			
		def KeyInputUpDown(self, key) :
			idx = self.SelectSlot
			maxValue = self.mycharacters.GetMyCharacterCount()
			if 200 == key : #UP
				idx = idx - 1
				if idx < 0 :
					idx = maxValue - 1
	
			elif 208 == key : #DOWN
				idx = idx + 1 
				if idx >= maxValue :
					idx = 0
			else: # ?? ?? ????, ?? ?? ?? ??
				self.SelectButton(0)
	
			self.SelectButton(idx)
	
		def OnPressExitKey(self):
			self.ExitButton()
			return True
		
		def DisableWindow(self):
			self.btnStart.Disable()
			self.btnStart.Down()
			self.btnCreate.Disable()
			self.btnCreate.Down()
			self.btnExit.Disable()
			self.btnExit.Down()
			self.btnDelete.Disable()
			self.btnDelete.Down()
			self.btnPrev.Disable()
			self.btnPrev.Down()
			self.btnNext.Disable()
			self.btnNext.Down()
			self.toolTip.Hide()
			self.ShowToolTip = False
			self.Disable = True
			for button in self.CharacterButtonList:
				button.Disable()
				# button.Down()
	
		def EnableWindow(self):
			self.btnStart.Enable()
			self.btnCreate.Enable()
			self.btnExit.Enable()
			self.btnDelete.Enable()
			self.btnPrev.Enable()
			self.btnNext.Enable()
			self.Disable = False
			for button in self.CharacterButtonList:
				button.Enable()
	
		def OpenChangeNameDialog(self):
			import uiCommon
			nameInputBoard = uiCommon.InputDialogWithDescription()
			nameInputBoard.SetTitle(localeInfo.SELECT_CHANGE_NAME_TITLE)
			nameInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputName))
			nameInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputName))
			nameInputBoard.SetMaxLength(chr.PLAYER_NAME_MAX_LEN)
			nameInputBoard.SetBoardWidth(200)
			nameInputBoard.SetDescription(localeInfo.SELECT_INPUT_CHANGING_NAME)
			nameInputBoard.Open()
			nameInputBoard.slot = self.RealSlot[self.SelectSlot]
			self.nameInputBoard = nameInputBoard
			
		def AcceptInputName(self):
			changeName = self.nameInputBoard.GetText()
			if not changeName:
				return
	
			net.SendChangeNamePacket(self.nameInputBoard.slot, changeName)
			return self.CancelInputName()
	
		def CancelInputName(self):
			self.nameInputBoard.Close()
			self.nameInputBoard = None
			self.EnableWindow()
			return True
	
		def OnCreateFailure(self, type):
			if 0 == type:
				self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_NAME)
			elif 1 == type:
				self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_ALREADY_EXIST_NAME)
			elif 100 == type:
				self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_INDEX)
				
		def OnChangeName(self, slot, name):
			for i in xrange(len(self.RealSlot)) :
				if self.RealSlot[i] == slot :
					self.ChangeNameButton(i, name)
					self.SelectButton(i)
					self.PopupMessage(localeInfo.SELECT_CHANGED_NAME)
					break
					
		def ChangeNameButton(self, slot, name) :
			self.CharacterButtonList[slot].SetAppendTextChangeText(0, name)
			self.mycharacters.SetChangeNameSuccess(slot)
else:
	old_open = open
	import chr
	import grp
	import app
	import math
	import wndMgr
	import snd
	import net
	import systemSetting
	import localeInfo
	import chr
	
	import ui
	import uiScriptLocale
	import networkModule
	import musicInfo
	import playerSettingModule
	
	####################################
	####################################
	import uiCommon
	import uiMapNameShower
	import uiAffectShower
	import uiPlayerGauge
	import uiCharacter
	import uiTarget
	import consoleModule
	
	import interfaceModule
	import uiTaskBar
	import uiInventory
	import constInfo
	###################################
	
	LEAVE_BUTTON_FOR_POTAL = False
	NOT_NEED_DELETE_CODE = False
	ENABLE_ENGNUM_DELETE_CODE = True
	
	###################################
	
	class SelectCharacterWindow(ui.Window):
	
		# SLOT4
		#SLOT_ROTATION = ( 140.0, 260.0, 20.0 )
		#SLOT_COUNT = 3
		if app.ENABLE_PLAYER_PER_ACCOUNT5:
			SLOT_ROTATION = [135.0, 207.0, 279.0, 351.0, 63.0]
			SLOT_COUNT = 5
			# SLOT_ROTATION = [135.0, 180.0, 225.0, 270.0, 315.0, 360.0, 45.0, 90.0]
			# SLOT_COUNT = 8
			# SLOT_ROTATION = [135.0, 157.5, 180.0, 202.5, 225.0, 247.5, 270.0, 292.5, 315.0, 337.5, 360.0, 382.5, 45.0, 67.5, 90.0, 112.5]
			# SLOT_COUNT = 16
		else:
			SLOT_ROTATION = [135.0, 225.0, 315.0, 45.0]
			SLOT_COUNT = 4
		if app.ENABLE_WOLFMAN_CHARACTER:
			CHARACTER_TYPE_COUNT = 5
		else:
			CHARACTER_TYPE_COUNT = 4
	
		EMPIRE_NAME = {
			net.EMPIRE_A : localeInfo.EMPIRE_A,
			net.EMPIRE_B : localeInfo.EMPIRE_B,
			net.EMPIRE_C : localeInfo.EMPIRE_C
		}
	
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
			ui.Window.__init__(self)
			net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)
	
			self.stream=stream
			self.slot = self.stream.GetCharacterSlot()
	
			self.openLoadingFlag = False
			self.startIndex = -1
			self.startReservingTime = 0
	
			self.flagDict = {}
			self.curRotation = []
			self.destRotation = []
			for rot in self.SLOT_ROTATION:
				self.curRotation.append(rot)
				self.destRotation.append(rot)
	
			self.curNameAlpha = []
			self.destNameAlpha = []
			for i in xrange(self.CHARACTER_TYPE_COUNT):
				self.curNameAlpha.append(0.0)
				self.destNameAlpha.append(0.0)
	
			self.curGauge = [0.0, 0.0, 0.0, 0.0]
			self.destGauge = [0.0, 0.0, 0.0, 0.0]
	
			self.dlgBoard = 0
			self.changeNameFlag = False
			self.nameInputBoard = None
			self.sendedChangeNamePacket = False
	
			self.startIndex = -1
			self.isLoad = 0
	
		def __del__(self):
			ui.Window.__del__(self)
			net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, 0)
	
		def Open(self):
			if not self.__LoadBoardDialog(uiScriptLocale.LOCALE_UISCRIPT_PATH + "selectcharacterwindow.py"):
				import dbg
				dbg.TraceError("SelectCharacterWindow.Open - __LoadScript Error")
				return
	
			if not self.__LoadQuestionDialog("uiscript/questiondialog.py"):
				return
	
			playerSettingModule.LoadGameData("INIT")
	
			self.InitCharacterBoard()
	
			self.btnStart.Enable()
			self.btnCreate.Enable()
			self.btnDelete.Enable()
			self.btnExit.Enable()
			self.btnLeft.Enable()
			self.btnRight.Enable()
	
			self.dlgBoard.Show()
			self.SetWindowName("SelectCharacterWindow")
			self.Show()
	
			if self.slot>=0:
				self.SelectSlot(self.slot)
	
			if musicInfo.selectMusic != "":
				snd.SetMusicVolume(systemSetting.GetMusicVolume())
				snd.FadeInMusic("BGM/"+musicInfo.selectMusic)
	
			app.SetCenterPosition(0.0, 0.0, 0.0)
			app.SetCamera(1550.0, 15.0, 180.0, 95.0)
	
			self.isLoad=1
			self.Refresh()
	
			if self.stream.isAutoSelect:
				chrSlot=self.stream.GetCharacterSlot()
				self.SelectSlot(chrSlot)
				self.StartGame()
	
			self.HideAllFlag()
			self.SetEmpire(net.GetEmpireID())
	
			app.ShowCursor()
	
		def Close(self):
			if musicInfo.selectMusic != "":
				snd.FadeOutMusic("BGM/"+musicInfo.selectMusic)
	
			self.stream.popupWindow.Close()
	
			if self.dlgBoard:
				self.dlgBoard.ClearDictionary()
	
			self.empireName = None
			self.flagDict = {}
			self.dlgBoard = None
			self.btnStart = None
			self.btnCreate = None
			self.btnDelete = None
			self.btnExit = None
			self.btnLeft = None
			self.btnRight = None
			self.backGround = None
	
			self.dlgQuestion.ClearDictionary()
			self.dlgQuestion = None
			self.dlgQuestionText = None
			self.dlgQuestionAcceptButton = None
			self.dlgQuestionCancelButton = None
			self.privateInputBoard = None
			self.nameInputBoard = None
	
			for i in xrange(self.SLOT_COUNT):
				chr.DeleteInstance(i)
	
			self.Hide()
			self.KillFocus()
	
			app.HideCursor()
	
		def SetEmpire(self, id):
			self.empireName.SetText(self.EMPIRE_NAME.get(id, ""))
			if self.flagDict.has_key(id):
				self.flagDict[id].Show()
	
		def HideAllFlag(self):
			for flag in self.flagDict.values():
				flag.Hide()
	
		def Refresh(self):
			if not self.isLoad:
				return
	
			# SLOT4
			indexArray = range(self.SLOT_COUNT-1, -1, -1)
			for index in indexArray:
				id=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ID)
				race=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_RACE)
				form=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_FORM)
				name=net.GetAccountCharacterSlotDataString(index, net.ACCOUNT_CHARACTER_SLOT_NAME)
				hair=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_HAIR)
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					acce = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ACCE)
	
				if id:
					if app.ENABLE_ACCE_COSTUME_SYSTEM:
						self.MakeCharacter(index, id, name, race, form, hair, acce)
					else:
						self.MakeCharacter(index, id, name, race, form, hair)
					self.SelectSlot(index)
	
			self.SelectSlot(self.slot)
	
		def GetCharacterSlotID(self, slotIndex):
			return net.GetAccountCharacterSlotDataInteger(slotIndex, net.ACCOUNT_CHARACTER_SLOT_ID)
	
		def __LoadQuestionDialog(self, fileName):
			self.dlgQuestion = ui.ScriptWindow()
	
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self.dlgQuestion, fileName)
			except:
				import exception
				exception.Abort("SelectCharacterWindow.LoadQuestionDialog.LoadScript")
	
			try:
				GetObject=self.dlgQuestion.GetChild
				self.dlgQuestionText=GetObject("message")
				self.dlgQuestionAcceptButton=GetObject("accept")
				self.dlgQuestionCancelButton=GetObject("cancel")
			except:
				import exception
				exception.Abort("SelectCharacterWindow.LoadQuestionDialog.BindObject")
	
			self.dlgQuestionText.SetText(localeInfo.SELECT_DO_YOU_DELETE_REALLY)
			self.dlgQuestionAcceptButton.SetEvent(ui.__mem_func__(self.RequestDeleteCharacter))
			self.dlgQuestionCancelButton.SetEvent(ui.__mem_func__(self.dlgQuestion.Hide))
			return 1
	
		def __LoadBoardDialog(self, fileName):
			self.dlgBoard = ui.ScriptWindow()
	
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self.dlgBoard, fileName)
			except:
				import exception
				exception.Abort("SelectCharacterWindow.LoadBoardDialog.LoadScript")
	
			try:
				GetObject=self.dlgBoard.GetChild
	
				self.btnStart		= GetObject("start_button")
				self.btnCreate		= GetObject("create_button")
				self.btnDelete		= GetObject("delete_button")
				self.btnExit		= GetObject("exit_button")
	
				self.CharacterName	= GetObject("character_name_value")
				self.CharacterLevel = GetObject("character_level_value")
				self.PlayTime		= GetObject("character_play_time_value")
				self.CharacterHTH	= GetObject("character_hth_value")
				self.CharacterINT	= GetObject("character_int_value")
				self.CharacterSTR	= GetObject("character_str_value")
				self.CharacterDEX	= GetObject("character_dex_value")
				self.GuildName		= GetObject("GuildName")
	
				self.NameList = []
				self.NameList.append(GetObject("name_warrior"))
				self.NameList.append(GetObject("name_assassin"))
				self.NameList.append(GetObject("name_sura"))
				self.NameList.append(GetObject("name_shaman"))
				if app.ENABLE_WOLFMAN_CHARACTER:
					self.NameList.append(GetObject("name_wolfman"))
	
				self.GaugeList = []
				self.GaugeList.append(GetObject("gauge_hth"))
				self.GaugeList.append(GetObject("gauge_int"))
				self.GaugeList.append(GetObject("gauge_str"))
				self.GaugeList.append(GetObject("gauge_dex"))
	
				self.btnLeft = GetObject("left_button")
				self.btnRight = GetObject("right_button")
	
				self.empireName = GetObject("EmpireName")
				self.flagDict[net.EMPIRE_A] = GetObject("EmpireFlag_A")
				self.flagDict[net.EMPIRE_B] = GetObject("EmpireFlag_B")
				self.flagDict[net.EMPIRE_C] = GetObject("EmpireFlag_C")
	
				self.backGround = GetObject("BackGround")
	
			except:
				import exception
				exception.Abort("SelectCharacterWindow.LoadBoardDialog.BindObject")
	
			for name in self.NameList:
				name.SetAlpha(0.0)
	
			self.btnStart.SetEvent(ui.__mem_func__(self.StartGame))
			self.btnCreate.SetEvent(ui.__mem_func__(self.CreateCharacter))
			self.btnExit.SetEvent(ui.__mem_func__(self.ExitSelect))
	
	
	
			if NOT_NEED_DELETE_CODE:
				self.btnDelete.SetEvent(ui.__mem_func__(self.PopupDeleteQuestion))
			else:
				self.btnDelete.SetEvent(ui.__mem_func__(self.InputPrivateCode))
	
			self.btnLeft.SetEvent(ui.__mem_func__(self.DecreaseSlotIndex))
			self.btnRight.SetEvent(ui.__mem_func__(self.IncreaseSlotIndex))
	
			self.chrRenderer = self.CharacterRenderer()
			self.chrRenderer.SetParent(self.backGround)
			self.chrRenderer.Show()
	
			return 1
	
		def MakeCharacter(self, index, id, name, race, form, hair, acce =0):
			if 0 == id:
				return
	
			chr.CreateInstance(index)
			chr.SelectInstance(index)
			chr.SetVirtualID(index)
			chr.SetNameString(name)
	
			chr.SetRace(race)
			chr.SetArmor(form)
			chr.SetHair(hair)
	
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				chr.SetAcce(acce)
	
			chr.Refresh()
			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
	
			chr.SetRotation(0.0)
	
		## Manage Character
		def StartGame(self):
	
			if self.sendedChangeNamePacket:
				return
	
			if self.changeNameFlag:
				self.OpenChangeNameDialog()
				return
	
			if -1 != self.startIndex:
				return
	
			if musicInfo.selectMusic != "":
				snd.FadeLimitOutMusic("BGM/"+musicInfo.selectMusic, systemSetting.GetMusicVolume()*0.05)
	
			self.btnStart.SetUp()
			self.btnCreate.SetUp()
			self.btnDelete.SetUp()
			self.btnExit.SetUp()
			self.btnLeft.SetUp()
			self.btnRight.SetUp()
	
			self.btnStart.Disable()
			self.btnCreate.Disable()
			self.btnDelete.Disable()
			self.btnExit.Disable()
			self.btnLeft.Disable()
			self.btnRight.Disable()
			self.dlgQuestion.Hide()
	
			self.stream.SetCharacterSlot(self.slot)
	
			self.startIndex = self.slot
			self.startReservingTime = app.GetTime()
	
			for i in xrange(self.SLOT_COUNT):
	
				if False == chr.HasInstance(i):
					continue
	
				chr.SelectInstance(i)
	
				if i == self.slot:
					self.slot=self.slot
					chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED, 0.1)
					continue
	
				chr.PushOnceMotion(chr.MOTION_INTRO_NOT_SELECTED, 0.1)
	
		def OpenChangeNameDialog(self):
			import uiCommon
			nameInputBoard = uiCommon.InputDialogWithDescription()
			nameInputBoard.SetTitle(localeInfo.SELECT_CHANGE_NAME_TITLE)
			nameInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputName))
			nameInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputName))
			nameInputBoard.SetMaxLength(chr.PLAYER_NAME_MAX_LEN)
			nameInputBoard.SetBoardWidth(200)
			nameInputBoard.SetDescription(localeInfo.SELECT_INPUT_CHANGING_NAME)
			nameInputBoard.Open()
			nameInputBoard.slot = self.slot
			self.nameInputBoard = nameInputBoard
	
		def OnChangeName(self, id, name):
			self.SelectSlot(id)
			self.sendedChangeNamePacket = False
			self.PopupMessage(localeInfo.SELECT_CHANGED_NAME)
	
		def AcceptInputName(self):
			changeName = self.nameInputBoard.GetText()
			if not changeName:
				return
	
			self.sendedChangeNamePacket = True
			net.SendChangeNamePacket(self.nameInputBoard.slot, changeName)
			return self.CancelInputName()
	
		def CancelInputName(self):
			self.nameInputBoard.Close()
			self.nameInputBoard = None
			return True
	
		def OnCreateFailure(self, type):
			self.sendedChangeNamePacket = False
			if 0 == type:
				self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_NAME)
			elif 1 == type:
				self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_ALREADY_EXIST_NAME)
			elif 100 == type:
				self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_INDEX)
	
		def CreateCharacter(self):
			id = self.GetCharacterSlotID(self.slot)
			if 0==id:
				self.stream.SetCharacterSlot(self.slot)
	
				EMPIRE_MODE = 1
	
				if EMPIRE_MODE:
					if self.__AreAllSlotEmpty():
						self.stream.SetReselectEmpirePhase()
					else:
						self.stream.SetCreateCharacterPhase()
	
				else:
					self.stream.SetCreateCharacterPhase()
	
		def __AreAllSlotEmpty(self):
			for iSlot in xrange(self.SLOT_COUNT):
				if 0!=net.GetAccountCharacterSlotDataInteger(iSlot, net.ACCOUNT_CHARACTER_SLOT_ID):
					return 0
			return 1
	
		def PopupDeleteQuestion(self):
			id = self.GetCharacterSlotID(self.slot)
			if 0 == id:
				return
	
			self.dlgQuestion.Show()
			self.dlgQuestion.SetTop()
	
		def RequestDeleteCharacter(self):
			self.dlgQuestion.Hide()
	
			id = self.GetCharacterSlotID(self.slot)
			if 0 == id:
				self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
				return
	
			net.SendDestroyCharacterPacket(self.slot, "1234567")
			self.PopupMessage(localeInfo.SELECT_DELEING)
	
		def InputPrivateCode(self):
	
			import uiCommon
			privateInputBoard = uiCommon.InputDialogWithDescription()
			privateInputBoard.SetTitle(localeInfo.INPUT_PRIVATE_CODE_DIALOG_TITLE)
			privateInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrivateCode))
			privateInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrivateCode))
	
			if ENABLE_ENGNUM_DELETE_CODE:
				pass
			else:
				privateInputBoard.SetNumberMode()
	
			privateInputBoard.SetSecretMode()
			privateInputBoard.SetMaxLength(7)
	
			privateInputBoard.SetBoardWidth(250)
			privateInputBoard.SetDescription(localeInfo.INPUT_PRIVATE_CODE_DIALOG_DESCRIPTION)
			privateInputBoard.Open()
			self.privateInputBoard = privateInputBoard
	
		def AcceptInputPrivateCode(self):
			privateCode = self.privateInputBoard.GetText()
			if not privateCode:
				return
	
			id = self.GetCharacterSlotID(self.slot)
			if 0 == id:
				self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
				return
	
			net.SendDestroyCharacterPacket(self.slot, privateCode)
			self.PopupMessage(localeInfo.SELECT_DELEING)
	
			self.CancelInputPrivateCode()
			return True
	
		def CancelInputPrivateCode(self):
			self.privateInputBoard = None
			return True
	
		def OnDeleteSuccess(self, slot):
			self.PopupMessage(localeInfo.SELECT_DELETED)
			self.DeleteCharacter(slot)
	
		def OnDeleteFailure(self):
			self.PopupMessage(localeInfo.SELECT_CAN_NOT_DELETE)
	
		def DeleteCharacter(self, index):
			chr.DeleteInstance(index)
			self.SelectSlot(self.slot)
	
		def ExitSelect(self):
			self.dlgQuestion.Hide()
	
			if LEAVE_BUTTON_FOR_POTAL:
				if app.loggined:
					self.stream.SetPhaseWindow(0)
				else:
					self.stream.setloginphase()
			else:
				self.stream.SetLoginPhase()
	
			self.Hide()
	
		def GetSlotIndex(self):
			return self.slot
	
		def DecreaseSlotIndex(self):
			slotIndex = (self.GetSlotIndex() - 1 + self.SLOT_COUNT) % self.SLOT_COUNT
			self.SelectSlot(slotIndex)
	
		def IncreaseSlotIndex(self):
			slotIndex = (self.GetSlotIndex() + 1) % self.SLOT_COUNT
			self.SelectSlot(slotIndex)
	
		def SelectSlot(self, index):
	
			if index < 0:
				return
			if index >= self.SLOT_COUNT:
				return
	
			self.slot = index
	
			chr.SelectInstance(self.slot)
	
			for i in xrange(self.CHARACTER_TYPE_COUNT):
				self.destNameAlpha[i] = 0.0
	
			for i in xrange(self.SLOT_COUNT):
				self.destRotation[(i+self.slot)%self.SLOT_COUNT] = self.SLOT_ROTATION[i]
	
			self.destGauge = [0.0, 0.0, 0.0, 0.0]
	
			id=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
			if 0 != id:
	
				self.btnStart.Show()
				self.btnDelete.Show()
				self.btnCreate.Hide()
	
				playTime=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
				level=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
				race=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)
				valueHTH=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HTH)
				valueINT=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_INT)
				valueSTR=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_STR)
				valueDEX=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_DEX)
				name=net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_NAME)
				guildID=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_ID)
				guildName=net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME)
				self.changeNameFlag=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_CHANGE_NAME_FLAG)
	
				job = chr.RaceToJob(race)
				if job >= 0 and job < self.CHARACTER_TYPE_COUNT:
					self.destNameAlpha[job] = 1.0
	
				self.CharacterName.SetText(name)
				self.CharacterLevel.SetText(str(level))
	
				self.PlayTime.SetText(str(playTime))
				self.CharacterHTH.SetText(str(valueHTH))
				self.CharacterINT.SetText(str(valueINT))
				self.CharacterSTR.SetText(str(valueSTR))
				self.CharacterDEX.SetText(str(valueDEX))
	
				if guildName:
					self.GuildName.SetText(guildName)
				else:
					self.GuildName.SetText(localeInfo.SELECT_NOT_JOIN_GUILD)
	
				statesSummary = float(valueHTH + valueINT + valueSTR + valueDEX)
				if statesSummary > 0.0:
					self.destGauge =	[
											float(valueHTH) / statesSummary,
											float(valueINT) / statesSummary,
											float(valueSTR) / statesSummary,
											float(valueDEX) / statesSummary
										]
	
			else:
	
				self.InitCharacterBoard()
	
		def InitCharacterBoard(self):
	
			self.btnStart.Hide()
			self.btnDelete.Hide()
			self.btnCreate.Show()
	
			self.CharacterName.SetText("")
			self.CharacterLevel.SetText("")
			self.PlayTime.SetText("")
			self.CharacterHTH.SetText("")
			self.CharacterINT.SetText("")
			self.CharacterSTR.SetText("")
			self.CharacterDEX.SetText("")
			self.GuildName.SetText(localeInfo.SELECT_NOT_JOIN_GUILD)
	
		## Event
		def OnIMEReturn(self):
			id = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
			if 0 == id:
				self.CreateCharacter()
			else:
				self.StartGame()
			return True
	
		def OnPressEscapeKey(self):
			self.ExitSelect()
			return True
	
		def OnKeyDown(self, key):
	
			for i in xrange(self.SLOT_COUNT):
				if 2+i == key:
					self.SelectSlot(i)
	
			if 203 == key:
				self.slot = (self.GetSlotIndex() - 1 + self.SLOT_COUNT) % self.SLOT_COUNT
				self.SelectSlot(self.slot)
			if 205 == key:
				self.slot = (self.GetSlotIndex() + 1) % self.SLOT_COUNT
				self.SelectSlot(self.slot)
	
			return True
	
		def OnUpdate(self):
			chr.Update()
	
			for i in xrange(4):
				self.curGauge[i] += (self.destGauge[i] - self.curGauge[i]) / 10.0
				if abs(self.curGauge[i] - self.destGauge[i]) < 0.005:
					self.curGauge[i] = self.destGauge[i]
				self.GaugeList[i].SetPercentage(self.curGauge[i], 1.0)
	
			for i in xrange(self.CHARACTER_TYPE_COUNT):
				self.curNameAlpha[i] += (self.destNameAlpha[i] - self.curNameAlpha[i]) / 10.0
				self.NameList[i].SetAlpha(self.curNameAlpha[i])
	
			for i in xrange(self.SLOT_COUNT):
	
				if False == chr.HasInstance(i):
					continue
	
				chr.SelectInstance(i)
	
				distance = 50.0
				rotRadian = self.curRotation[i] * (math.pi*2) / 360.0
				x = distance*math.sin(rotRadian) + distance*math.cos(rotRadian)
				y = distance*math.cos(rotRadian) - distance*math.sin(rotRadian)
				chr.SetPixelPosition(int(x), int(y), 30)
	
				#####
	
				dir = app.GetRotatingDirection(self.destRotation[i], self.curRotation[i])
				rot = app.GetDegreeDifference(self.destRotation[i], self.curRotation[i])
	
				if app.DEGREE_DIRECTION_RIGHT == dir:
					self.curRotation[i] += rot / 10.0
				elif app.DEGREE_DIRECTION_LEFT == dir:
					self.curRotation[i] -= rot / 10.0
	
				self.curRotation[i] = (self.curRotation[i] + 360.0) % 360.0
	
			#######################################################
			if -1 != self.startIndex:
	
				## Temporary
				if app.GetTime() - self.startReservingTime > constInfo.SELECT_CHAR_NO_DELAY:
					if False == self.openLoadingFlag:
						chrSlot=self.stream.GetCharacterSlot()
						net.DirectEnter(chrSlot)
						self.openLoadingFlag = True
	
						playTime=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
	
						import player
						player.SetPlayTime(playTime)
						import chat
						chat.Clear()
				## Temporary
			#######################################################
	
		def EmptyFunc(self):
			pass
	
		def PopupMessage(self, msg, func=0):
			if not func:
				func=self.EmptyFunc
	
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)
	
		def OnPressExitKey(self):
			self.ExitSelect()
			return True
