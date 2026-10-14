import app, net, ime, ui, wndMgr, serverInfo, localeInfo, constInfo, ServerStateChecker, snd, systemSetting
import binascii, os
import time, grp

SERVER = 1
CHANNEL = 1

PATH_BASE = "lightwork/login/"

WEB_URL = "https://metin2.com/"
DISCORD_URL = "https://discord.com/invite/metin2"

class LoginWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self)
		
		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)
		self.connectingDialog = None
		self.stream = stream
		self.channelButton = None
		self.channelChTxt = None
		self.languageList = ["en","de","ro","pl","it","cz","hu","tr"]
		self.selected_language		= 0
		self.clickedLang = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)

	def Open(self):
		ServerStateChecker.Create(self)
		self.loginFailureMsgDict={
			"ALREADY"	: localeInfo.LOGIN_FAILURE_ALREAY,
			"NOLANG"	: "NOLANG Error",
			"ACCOUNT_BANNED"	: localeInfo.LOGIN_FAILURE_ACCOUNT_BAN,
			"NOID"		: localeInfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: localeInfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: localeInfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: localeInfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: localeInfo.LOGIN_FAILURE_BLOCK_ID,
			"BESAMEKEY"	: localeInfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: localeInfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: localeInfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: localeInfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: localeInfo.LOGIN_FAILURE_WEB_BLOCK,
			"BADSCLID"	: localeInfo.LOGIN_FAILURE_WRONG_SOCIALID,
			"AGELIMIT"	: localeInfo.LOGIN_FAILURE_SHUTDOWN_TIME,
			"NOCLIENT"	: localeInfo.LOGIN_FAILURE_CLIENT_VERSION,
			"NOPIN"		: localeInfo.LOGIN_FAILURE_PIN,
			"NOSERVER"		: localeInfo.LOGIN_FAILURE_SERVER,
			"HWIDERROR"		: localeInfo.LOGIN_FAILURE_HWIDERROR,
			"HWIDFULL"		: localeInfo.LOGIN_FAILURE_HWIDFULL,
			"HWIDBAN"		: localeInfo.LOGIN_FAILURE_HWIDBAN,
		}

		self.loginFailureFuncDict = {
			"WRONGPWD"	: self.__DisconnectAndInputPassword,
			"QUIT"		: app.Exit,
		}

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")

		self.__LoadScript("uiscript/LoginWindow.py")

		ime.AddExceptKey(91)
		ime.AddExceptKey(93)
		# self.SetServ(1)
		self.idEditLine.SetFocus()
		
		self.Show()
		app.ShowCursor()
		self.__RequestServerStateList()
		# self.__RefreshServerStateList()
		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			self.InitLanguageBoard()

			localeName = app.GetLoca()
			for i, k in constInfo.LOCALE_LANG_DICT.items():
				if localeName in constInfo.LOCALE_LANG_DICT[i]["locale"]:
					net.SetLanguage(i)
					break

		self.SetServ(1)
		self.LoadChosenServer()
		self.SetChannel(1)
		snd.SetMusicVolume(systemSetting.GetMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())
		snd.FadeInMusic("BGM/login_window.mp3")
		snd.PlaySound("sound/ui/window_open.wav")

	def LoadChosenServer(self):
		if not constInfo.GetReg("sv_chosen"):
			self.SetServ(1)
		else:
			selectedServer = "%s" % binascii.a2b_base64("%s" % constInfo.GetReg("sv_chosen"))
			if selectedServer:
				self.SetServ(int(selectedServer))

	def WriteChosenServer(self, serverChosen):
		constInfo.SetReg("sv_chosen", str(binascii.b2a_base64(str(serverChosen))))

	def Close(self):
		snd.FadeOutMusic("BGM/login_window.mp3")
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None
		ServerStateChecker.Initialize(self)

		if self.stream.popupWindow:
			self.stream.popupWindow.Close()
		self.connectingDialog = None
		self.Hide()
		app.HideCursor()
		ime.ClearExceptKey()

	def SetIDEditLineFocus(self):
		if self.idEditLine != None:
			self.idEditLine.SetFocus()

	def SetPasswordEditLineFocus(self):
		if self.pwdEditLine != None:
			self.pwdEditLine.SetFocus()

	def OnConnectFailure(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None
		snd.PlaySound("sound/ui/loginfail.wav")
		self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, self.EmptyFunc)

	def OnHandShake(self):
		snd.PlaySound("sound/ui/loginok.wav")
		if self.IsShow():
			self.PopupDisplayMessage(localeInfo.LOGIN_CONNECT_SUCCESS)

	def OnLoginStart(self):
		self.PopupDisplayMessage(localeInfo.LOGIN_PROCESSING)

	def OnLoginFailure(self, error):
		if self.connectingDialog:
			self.connectingDialog.Close()
			self.connectingDialog = None
		try:
			loginFailureMsg = self.loginFailureMsgDict[error]
		except KeyError:
			loginFailureMsg = localeInfo.LOGIN_FAILURE_UNKNOWN  + error

		loginFailureFunc=self.loginFailureFuncDict.get(error, self.SetPasswordEditLineFocus)
		snd.PlaySound("sound/ui/loginfail.wav")
		self.PopupNotifyMessage(loginFailureMsg, loginFailureFunc)

	def __DisconnectAndInputPassword(self):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		self.SetPasswordEditLineFocus()
		net.Disconnect()

	def __LoadScript(self, fileName):
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, fileName)

			self.idEditLine = self.GetChild("UserEditLine")
			self.pwdEditLine = self.GetChild("PwEditLine")
			self.loginButton = self.GetChild("LoginBtn")
			
			self.channelButton = {
				1 : self.GetChild("ChannelBtn1"),
				2 :	self.GetChild("ChannelBtn2"),
				3 : self.GetChild("ChannelBtn3"),
				4 : self.GetChild("ChannelBtn4"),
				5 : self.GetChild("ChannelBtn5"),
				6 : self.GetChild("ChannelBtn6")
			}

			self.servButton = {
				1 : self.GetChild("SvButton1"),
				2 :	self.GetChild("SvButton2")
			}
			
			self.GetChild("ExitBtn").SetEvent(ui.__mem_func__(self.MainBoard))
			self.GetChild("WebBtn").SetEvent(ui.__mem_func__(self.ClickHomePage))
			self.GetChild("DiscordBtn").SetEvent(ui.__mem_func__(self.ClickDiscord))
			self.GetChild("ForgotBtn").SetEvent(ui.__mem_func__(self.ClickForgotPWButton))
			self.GetChild("RegisterBtn").SetEvent(ui.__mem_func__(self.ClickRegisterButton))

		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.BindObject") 

		for (channelID, channelButtons) in self.channelButton.items():
			channelButtons.SetEvent(ui.__mem_func__(self.SetChannel), channelID)

		for (servID, servButtons) in self.servButton.items():
			servButtons.SetEvent(ui.__mem_func__(self.SetServ), servID)

		self.loginButton.SetEvent(ui.__mem_func__(self.__OnClickLoginButton))

		self.idEditLine.SetReturnEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))
		self.idEditLine.SetTabEvent(ui.__mem_func__(self.pwdEditLine.SetFocus))

		self.pwdEditLine.SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.pwdEditLine.SetTabEvent(ui.__mem_func__(self.idEditLine.SetFocus))

		self.AccButtons = []
		a = 42
		for i in xrange(7):
			btn = RegisterButton(i, self)
			btn.SetParent(self.GetChild("Save"))
			btn.SetPosition(35, 68 + (i * a))
			btn.Show()
			self.AccButtons.append(btn)

	def MainBoard(self):
		self.stream.SetPhaseWindow(0)
		
	def SetChannel(self, ch):
		global CHANNEL
		CHANNEL = int(ch)
		for (channelID, channelButtons) in self.channelButton.items():
			if ch != channelID:
				channelButtons.SetUp()
				channelButtons.Enable()
			else:
				channelButtons.Down()
				channelButtons.Disable()

		self.SetInfos()

	def SetServ(self, sv):
		global SERVER
		SERVER = int(sv)
		constInfo.SERVER_SELECTED = int(sv)
		for (servID, servButtons) in self.servButton.items():
			if sv != servID:
				servButtons.SetUp()
				servButtons.Enable()
			else:
				servButtons.Down()
				servButtons.Disable()
		self.SetInfos()
		self.__RequestServerStateList()
		# self.__RefreshServerStateList()
		self.WriteChosenServer(sv)

	def SetInfos(self):
		channelDict = serverInfo.REGION_DICT[0][SERVER]["channel"]
		authDict = serverInfo.REGION_AUTH_SERVER_DICT[0][SERVER]
		markDict = serverInfo.MARKADDR_DICT[SERVER * 10]
		port = authDict["port"]
		port2 = channelDict[CHANNEL]["tcp_port"]
		self.stream.SetConnectInfo(channelDict[CHANNEL]["ip"], port2, authDict["ip"], port)
		net.SetMarkServer(markDict["ip"], markDict["tcp_port"])
		app.SetGuildMarkPath(markDict["mark"])
		app.SetGuildSymbolPath(markDict["symbol_path"])
		net.SetServerInfo("%s, %s" % (serverInfo.REGION_DICT[0][SERVER]["name"], channelDict[CHANNEL]["name"]))

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def GetLangDialog(self, bLanguage):
			if bLanguage == "en":
				self.selected_language = 1
			elif bLanguage == "pt":
				self.selected_language = 2
			elif bLanguage == "es":
				self.selected_language = 3
			elif bLanguage == "fr":
				self.selected_language = 4
			elif bLanguage == "de":
				self.selected_language = 5
			elif bLanguage == "ro":
				self.selected_language = 6
			elif bLanguage == "pl":
				self.selected_language = 7
			elif bLanguage == "it":
				self.selected_language = 8
			elif bLanguage == "cz":
				self.selected_language = 9
			elif bLanguage == "hu":
				self.selected_language = 10
			elif bLanguage == "tr":
				self.selected_language = 11
			else:
				self.selected_language = 1

	def Connect(self, id, pwd):
		self.SetInfos()

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_CONNETING, self.EmptyFunc, localeInfo.UI_CANCEL)

		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			self.GetLangDialog(self.getLanguage())
			locale = constInfo.LOCALE_LANG_DICT[self.selected_language]["locale"]
			code_page = constInfo.LOCALE_LANG_DICT[self.selected_language]["code_page"]

			if self.__SaveLoca(code_page, locale):
				net.SetLanguage(self.selected_language)

		self.stream.SetLoginInfo(id, pwd, serverInfo.CLIENT_VERSION)
		self.stream.Connect()
		
	def PopupDisplayMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg)

	def PopupNotifyMessage(self, msg, func=0):
		if not func:
			func = self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def OnPressExitKey(self):
		if self.stream.popupWindow:
			self.stream.popupWindow.Close()
		self.stream.SetPhaseWindow(0)
		return True

	def OnKeyDown(self, key):#06.04.2019
		if app.DIK_ESC == key: #ESC
			self.OnPressExitKey()
		elif app.DIK_F1 == key: #F1
			self.LoginSelectedAccount(0)
		elif app.DIK_F2 == key: #F2
			self.LoginSelectedAccount(1)
		elif app.DIK_F3 == key: #F3
			self.LoginSelectedAccount(2)
		elif app.DIK_F4 == key: #F4
			self.LoginSelectedAccount(3)
		elif app.DIK_F5 == key: #F5
			self.LoginSelectedAccount(4)
		elif app.DIK_F6 == key: #F6
			self.LoginSelectedAccount(5)
		elif app.DIK_F7 == key: #F6
			self.LoginSelectedAccount(6)
		else:
			return True
		return True

	def OnUpdate(self):
		ServerStateChecker.Update()

	def EmptyFunc(self):
		pass

	def __OnClickLoginButton(self):
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()

		if len(id)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_ID, self.SetIDEditLineFocus)
			return

		if len(pwd)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_PASSWORD, self.SetPasswordEditLineFocus)
			return

		self.Connect(id, pwd)

	def WriteAndReadAccount(self, i):    
		if not constInfo.GetReg("id%d" % i) and not constInfo.GetReg("pwd%d" % i):
			if self.idEditLine.GetText() == "" or self.pwdEditLine.GetText() == "":
				return

			constInfo.SetReg("id%d" % i, str(binascii.b2a_base64(self.idEditLine.GetText())))
			constInfo.SetReg("pwd%d" % i, str(binascii.b2a_base64(self.pwdEditLine.GetText())))

			self.AccButtons[i].text.SetText(self.idEditLine.GetText())
			self.AccButtons[i].btn2.SetUpVisual(PATH_BASE + "buttons/delete_btn.png")
			self.AccButtons[i].btn2.SetOverVisual(PATH_BASE+ "buttons/delete_btn.png")
			self.AccButtons[i].btn2.SetDownVisual(PATH_BASE+ "buttons/delete_btn.png")
			self.AccButtons[i].btn2.SetEvent(ui.__mem_func__(self.DeleteAccount), i)

			self.PopupNotifyMessage(localeInfo.ACCOUNT_HAS_REGISTERED, self.EmptyFunc)

	def DeleteAccount(self, i):
		constInfo.SetReg("id%d" % i, "")
		constInfo.SetReg("pwd%d" % i, "")

		self.AccButtons[i].text.SetText(localeInfo.SAVE_ACCOUNT_BUTTON)
		self.AccButtons[i].btn2.SetUpVisual(PATH_BASE + "buttons/save_btn.png")
		self.AccButtons[i].btn2.SetOverVisual(PATH_BASE+ "buttons/save_btn.png")
		self.AccButtons[i].btn2.SetDownVisual(PATH_BASE+ "buttons/save_btn.png")
		self.AccButtons[i].btn2.SetEvent(ui.__mem_func__(self.WriteAndReadAccount), i)

	def LoginSelectedAccount(self, i):
		self.idEditLine.SetText("%s" % binascii.a2b_base64("%s" % constInfo.GetReg("id%d" % i)))
		self.pwdEditLine.SetText("%s" % binascii.a2b_base64("%s" % constInfo.GetReg("pwd%d" % i)))
		self.__OnClickLoginButton()

	def __RequestServerStateList(self):
		try:
			channelDict = serverInfo.REGION_DICT[0][SERVER]["channel"]
		except:
			return

		ServerStateChecker.Initialize()
		for id, channelDataDict in channelDict.items():
			key = channelDataDict["key"]
			ip = channelDataDict["ip"]
			udp_port = channelDataDict["udp_port"]
			ServerStateChecker.AddChannel(key, ip, udp_port)
			
		ServerStateChecker.Request()

	# def __RefreshServerStateList(self):
	# 	try:
	# 		channelDict = serverInfo.REGION_DICT[0][SERVER]["channel"]
	# 	except:
	# 		return

	# 	for channelID, channelDataDict in channelDict.items():
	# 		channelState = channelDataDict["state"]
	# 		if channelState == serverInfo.STATE_NONE:
	# 			self.channelChTxt[int(channelID) - 1].SetText(channelState)
	# 		else:
	# 			self.channelChTxt[int(channelID) - 1].SetText(channelState)

	def NotifyChannelState(self, addrKey, state):
		pass
	# 	try:
	# 		stateName = serverInfo.STATE_DICT[state]
	# 	except:
	# 		stateName = serverInfo.STATE_NONE

	# 	regionID = int(addrKey / 1000)
	# 	serverID = int(addrKey / 10) % 100
	# 	channelID = addrKey % 10

		# try:
		# 	serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["state"] = stateName		
		# 	self.__RefreshServerStateList()
		# except:
		# 	import exception
		# 	exception.Abort(localeInfo.CHANNEL_NOT_FIND_INFO)

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def InitLanguageBoard(self):
			self.WIDTH_FLAG = 37

			self.typeButtonList, groupButtonDict = [], {}
			for i in xrange(len(self.languageList)):
				bLanguage = self.languageList[i]

				groupButtonDict[i] = ui.RadioButton()
				groupButtonDict[i].SetParent(self.GetChild("Save"))
				groupButtonDict[i].SetPosition(374, 30 + self.WIDTH_FLAG*(i+1))
				groupButtonDict[i].SetUpVisual(PATH_BASE + "flags/%s.png" % bLanguage)
				groupButtonDict[i].SetOverVisual(PATH_BASE + "flags/%s_2.png" % bLanguage)
				groupButtonDict[i].SetDownVisual(PATH_BASE + "flags/%s_3.png" % bLanguage)
				groupButtonDict[i].SAFE_SetEvent(self.OnSelectLanguageButton, bLanguage)
				groupButtonDict[i].Show()

				self.langMem = bLanguage

				self.typeButtonList.append(groupButtonDict[i])

			self.ClickRadioButton(self.typeButtonList, self.getLanguageAsIndex(self.getLanguage()))
			
		def getLanguageAsIndex(self, bLanguage):
			for i in xrange(len(self.languageList)):
				if self.languageList[i] == bLanguage:
					return i
					
		def getLanguage(self):
			f = open("UserData/lang.cfg", "r")
			return f.read()
			
		def setLanguage(self, language):
			self.language = language
			
		def ClickRadioButton(self, buttonList, buttonIndex):
			try:
				selButton = buttonList[buttonIndex]
			except IndexError:
				return

			for eachButton in buttonList:
				eachButton.SetUp()

			selButton.Down()

		def __SaveLoca(self, code_page, locale):
			if app.SetLoca(code_page, locale):
				return True

			return False

		def OnSelectLanguageButton(self, bLanguage):

			if self.clickedLang:
				return

			file = open("UserData/lang.cfg", "w")
			file.write(bLanguage) 
			file.close()
	
			if bLanguage == "en":
				self.selected_language = 1
				file = open("UserData/loca.cfg", "w")
				file.write("1254 en") 
				file.close()
			# elif bLanguage == "pt":
			# 	self.selected_language = 2
			# 	file = open("UserData/loca.cfg", "w")
			# 	file.write("1254 pt") 
			# 	file.close()
			# elif bLanguage == "es":
			# 	self.selected_language = 3
			# 	file = open("UserData/loca.cfg", "w")
			# 	file.write("1254 es") 
			# 	file.close()
			# elif bLanguage == "fr":
			# 	self.selected_language = 4
			# 	file = open("UserData/loca.cfg", "w")
			# 	file.write("1254 fr") 
			# 	file.close()
			elif bLanguage == "de":
				self.selected_language = 5
				file = open("UserData/loca.cfg", "w")
				file.write("1254 de") 
				file.close()
			elif bLanguage == "ro":
				self.selected_language = 6
				file = open("UserData/loca.cfg", "w")
				file.write("1250 ro") 
				file.close()
			elif bLanguage == "pl":
				self.selected_language = 7
				file = open("UserData/loca.cfg", "w")
				file.write("1250 pl") 
				file.close()
			elif bLanguage == "it":
				self.selected_language = 8
				file = open("UserData/loca.cfg", "w")
				file.write("1254 it") 
				file.close()
			elif bLanguage == "cz":
				self.selected_language = 9
				file = open("UserData/loca.cfg", "w")
				file.write("1250 cz") 
				file.close()
			elif bLanguage == "hu":
				self.selected_language = 10
				file = open("UserData/loca.cfg", "w")
				file.write("1250 hu") 
				file.close()
			elif bLanguage == "tr":
				self.selected_language = 11
				file = open("UserData/loca.cfg", "w")
				file.write("1254 tr") 
				file.close()
			else:
				self.selected_language = 1
				file = open("UserData/loca.cfg", "w")
				file.write("1254 en") 
				file.close()

			locale = constInfo.LOCALE_LANG_DICT[self.selected_language]["locale"]
			code_page = constInfo.LOCALE_LANG_DICT[self.selected_language]["code_page"]

			if self.__SaveLoca(code_page, locale):
				net.SetLanguage(self.selected_language)

			# app.ShellExecute("m2.bin")

			self.clickedLang = True

			self.PopupDisplayMessage("Restart the client to see the changes.")
			# self.changeLanguageTime = app.GetTime() + 5.0

	def OnPressExitKey(self):
		# self.eventExit()
		return True

	def ClickRegisterButton(self):
		os.system("start {}Register".format(WEB_URL))

	def ClickForgotPWButton(self):
		os.system("start {}Forget/Password".format(WEB_URL))

	def ClickHomePage(self):
		os.system("start {}".format(WEB_URL))

	def ClickDiscord(self):
		os.system("start {}".format(DISCORD_URL))


class ConnectingDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/ConnectingDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.countdownMessage = self.GetChild("countdown_message")

		except:
			import exception
			exception.Abort("ConnectingDialog.LoadDialog.BindObject")

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime

		self.Lock()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Unlock()
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def SetText(self, text):
		self.message.SetText(text)

	def SetCountDownMessage(self, waitTime):
		self.countdownMessage.SetText("%.0f%s" % (waitTime, localeInfo.SECOND))

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)

	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.clock())
		if 0 == lastTime:
			self.Close()
			self.eventTimeOver()
		else:
			self.SetCountDownMessage(self.endTime - time.clock())

		# if self.changeLanguageTime:
			# if app.GetTime() > self.changeLanguageTime:
				# app.Exit()


class RegisterButton(ui.Window):
	def __init__(self, idx, parent):
		ui.Window.__init__(self)
		self.hasAccount = constInfo.GetReg("id%d" % idx) and constInfo.GetReg("pwd%d" % idx)

		self.SetSize(315, 35)

		self.backgroundImage = ui.MakeExpandedImageBox(self, PATH_BASE + "saved_button.png", 0, 0)
		self.backgroundImage.OnMouseLeftButtonDown =  lambda i = idx : parent.LoginSelectedAccount(i)
		self.event = parent.WriteAndReadAccount

		self.text = ui.TextLine()
		if self.hasAccount:
			self.text.SetText(binascii.a2b_base64("%s" % constInfo.GetReg("id%d" % idx)))
		else:
			self.text.SetText(localeInfo.SAVE_ACCOUNT_BUTTON)
		self.text.SetParent(self)
		self.text.SetVerticalAlignCenter()
		self.text.SetWindowVerticalAlignCenter()
		self.text.SetPackedFontColor(grp.GenerateColor(94, 94, 94, 1.0))
		self.text.SetPosition(15, 0)
		self.text.Show()

		self.btn2 = ui.Button()
		self.btn2.SetParent(self)
		self.btn2.SetWindowVerticalAlignCenter()
		self.btn2.SetPosition(240, 0)

		if self.hasAccount:
			self.btn2.SetUpVisual(PATH_BASE + "buttons/delete_btn.png")
			self.btn2.SetOverVisual(PATH_BASE+ "buttons/delete_btn.png")
			self.btn2.SetDownVisual(PATH_BASE+ "buttons/delete_btn.png")
			self.event = parent.DeleteAccount
		else:
			self.btn2.SetUpVisual(PATH_BASE + "buttons/save_btn.png")
			self.btn2.SetOverVisual(PATH_BASE+ "buttons/save_btn.png")
			self.btn2.SetDownVisual(PATH_BASE+ "buttons/save_btn.png")

		self.btn2.SetEvent(ui.__mem_func__(self.event), idx)
		self.btn2.Show()

		self.shortcutImage = ui.MakeExpandedImageBox(self, PATH_BASE + "buttons/key_f{}.png".format(idx+1), 280, 0)

	def __del__(self):
		ui.Window.__del__(self)