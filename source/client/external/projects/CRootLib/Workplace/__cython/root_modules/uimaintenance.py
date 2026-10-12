import ui, app, localeInfo

class MaintenanceWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.maintime = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/maintenance.py")
		except:
			import exception
			exception.Abort("MaintenanceWindow.LoadWindow.LoadObject")
		try:
			self.board = self.GetChild("Thinboard")
			self.textLine1 = self.GetChild("message1")
			self.textLine2 = self.GetChild("message3")
			self.textLine3 = self.GetChild("message2")
			self.textLine1.SetFontName("Verdana:14")
			self.textLine2.SetFontName("Verdana:13")
			# self.textLine3.SetFontName("Verdana:12")

		except:
			import exception
			exception.Abort("MaintenanceWindow.LoadWindow.LoadObject")

	def Open(self, time, duration):
		self.SetTop()
		self.Show()
		self.textLine1.SetText(localeInfo.MAINTENANCE_TEXT_1 % (self.SecondToHMD(int(duration))))
		self.maintime = int(time)

	def Close(self):
		self.Hide()

	def SecondToHMD(self, time):
		second = int(time % 60)
		minute = int((time / 60) % 60)
		hour = int(((time / 60) / 60) % 24)
		day = int((((time / 60) / 60) / 24) % 30)

		if hour <= 0:
			if time % 60 == 0:
				return localeInfo.MAINTENANCE_TEXT_2 % (minute)
			else:
				return localeInfo.MAINTENANCE_TEXT_3 % (minute, second)
		else:
			if day <= 0:
				if time % 60*60 == 0:
					return localeInfo.MAINTENANCE_TEXT_4 % (hour)
				else:
					if time % 60 == 0:
						return localeInfo.MAINTENANCE_TEXT_5 % (hour, minute)
					else:
						return localeInfo.MAINTENANCE_TEXT_6 % (hour, minute, second)
			else:
				return localeInfo.MAINTENANCE_TEXT_7 % (day, hour, minute, second)

	def OnUpdate(self):
		remain_time = self.maintime - app.GetGlobalTimeStamp()
		if remain_time > 0:
			self.textLine2.SetText(localeInfo.MAINTENANCE_TEXT_8 % (self.SecondToHMD(remain_time)))
		else:
			self.Hide()