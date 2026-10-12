# -*- coding: cp949 -*-
#1431897210
import ui, uiScriptLocale, wndMgr, player, miniMap, localeInfo, net, app, chr, constInfo, serverInfo
if app.ENABLE_BIOLOG_SYSTEM:
	import biolog

import time

#ifdef ENABLE_ULTIMATE_REGEN
def FormatTime(seconds):
	if seconds <= 0:
		return "0s"
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	text = ""
	if d > 0:
		text+= str(d)+"d "
	if h > 0:
		text+= str(h)+"h "
	if m > 0:
		text+= str(m)+"m "
	if s > 0:
		text+= str(s)+"s "
	return text

class MapTextToolTip(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetHorizontalAlignCenter()
		textLine.SetOutline()
		textLine.SetHorizontalAlignRight()
		textLine.Show()
		self.textLine = textLine

	def __del__(self):
		ui.Window.__del__(self)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetTooltipPosition(self, PosX, PosY):
		self.textLine.SetPosition(PosX - 5, PosY)

	def SetTextColor(self, TextColor):
		self.textLine.SetPackedFontColor(TextColor)

	def GetTextSize(self):
		return self.textLine.GetTextSize()

	def SetHorizontalAlignLeft(self):
		if self.textLine:
			self.textLine.SetHorizontalAlignLeft()

class AtlasWindow(ui.ScriptWindow):

	class AtlasRenderer(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")

		def __del__(self):
			ui.Window.__del__(self)

		def OnUpdate(self):
			miniMap.UpdateAtlas()

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			fx = float(x)
			fy = float(y)
			miniMap.RenderAtlas(fx, fy)

		def HideAtlas(self):
			miniMap.HideAtlas()

		def ShowAtlas(self):
			miniMap.ShowAtlas()

	def __init__(self):
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Hide()
		self.infoGuildMark = ui.MarkBox()
		self.infoGuildMark.Hide()
		self.AtlasMainWindow = None
		self.mapName = ""
		self.board = 0
		self.IsShowWindowValue = False

		self.tooltipInfoEx = MapTextToolTip()
		self.tooltipInfoEx.Hide()

		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetMapName(self, mapName):
		if 949==app.GetDefaultCodePage():
			try:
				self.board.SetTitleName(localeInfo.MINIMAP_ZONE_NAME_DICT[mapName])
			except:
				pass

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AtlasWindow.py")
		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.LoadScript")

		try:
			self.board = self.GetChild("board")

		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.BindObject")

		self.AtlasMainWindow = self.AtlasRenderer()
		self.board.SetCloseEvent(self.Close)
		self.AtlasMainWindow.SetParent(self.board)
		self.AtlasMainWindow.SetPosition(7, 30)
		self.tooltipInfo.SetParent(self.board)
		self.tooltipInfoEx.SetParent(self.board)
		self.infoGuildMark.SetParent(self.board)
		if app.ENABLE_ATLAS_SCALE:
			self.SetPosition(wndMgr.GetScreenWidth() - 136 - 256 - 10 - 165, 78)
		else:
			self.SetPosition(wndMgr.GetScreenWidth() - 136 - 256 - 10, 0)
		if app.ENABLE_MINIMAP_TELEPORT:
			self.board.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.OnMouseLeftButtonUpEvent))
		self.Hide()

		miniMap.RegisterAtlasWindow(self)
		if app.ENABLE_ATLAS_SCALE:
			miniMap.SetAtlasScale(1.0, 1.0)

	def Destroy(self):
		miniMap.UnregisterAtlasWindow()
		self.ClearDictionary()
		self.AtlasMainWindow = None
		self.tooltipAtlasClose = 0
		self.tooltipInfo = None
		self.tooltipInfoEx = None
		self.infoGuildMark = None
		self.board = None

	def OnUpdate(self):

		if not self.tooltipInfo:
			return

		if not self.infoGuildMark:
			return

		self.infoGuildMark.Hide()
		self.tooltipInfo.Hide()
		self.tooltipInfoEx.Hide()

		if False == self.board.IsIn():
			return

		(mouseX, mouseY) = wndMgr.GetMousePosition()
		(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID, diRegenTime) = miniMap.GetAtlasInfo(mouseX, mouseY)

		if False == bFind:
			return

		if "empty_guild_area" == sName:
			sName = localeInfo.GUILD_EMPTY_AREA

		(x, y) = self.GetGlobalPosition()

		if diRegenTime != 0:# it is boss!
			self.tooltipInfoEx.SetText("%s - (%d, %d)" % (sName, iPosX, iPosY))
			self.tooltipInfo.SetText(localeInfo.MINIMAP_BOSS_TOOLTIP % FormatTime(diRegenTime))
			self.tooltipInfoEx.SetTooltipPosition(mouseX - x, mouseY - y + 12)
			self.tooltipInfoEx.SetTextColor(dwTextColor)
			self.tooltipInfoEx.Show()
			self.tooltipInfoEx.SetTop()

		else:
			self.tooltipInfo.SetText("%s (%d, %d)" % (sName, iPosX, iPosY))
			self.tooltipInfo.SetTextColor(dwTextColor)

		self.tooltipInfo.SetTooltipPosition(mouseX - x, mouseY - y)
		self.tooltipInfo.SetTextColor(dwTextColor)
		self.tooltipInfo.Show()
		self.tooltipInfo.SetTop()

		if 0 != dwGuildID:
			textWidth, textHeight = self.tooltipInfo.GetTextSize()
			self.infoGuildMark.SetIndex(dwGuildID)
			self.infoGuildMark.SetPosition(mouseX - x - textWidth - 18 - 5, mouseY - y)
			self.infoGuildMark.Show()

	def Hide(self):
		if self.AtlasMainWindow:
			self.AtlasMainWindow.HideAtlas()
			self.AtlasMainWindow.Hide()
		ui.ScriptWindow.Hide(self)

	def Show(self):
		if self.AtlasMainWindow:
			(bGet, iSizeX, iSizeY) = miniMap.GetAtlasSize()
			if bGet:
				self.SetSize(iSizeX + 15, iSizeY + 38)

				self.board.SetSize(iSizeX + 15, iSizeY + 38)
				#self.AtlasMainWindow.SetSize(iSizeX, iSizeY)
				self.AtlasMainWindow.ShowAtlas()
				self.AtlasMainWindow.Show()
		ui.ScriptWindow.Show(self)
		self.IsShowWindowValue = True

	def Close(self):
		self.IsShowWindowValue = False
		self.Hide()

	def IsShowWindow(self):
		return self.IsShowWindowValue

	def SetCenterPositionAdjust(self, x, y):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)

	if app.ENABLE_MINIMAP_TELEPORT:
		def OnMouseLeftButtonUpEvent(self):
			(mouseX, mouseY) = wndMgr.GetMousePosition()
			(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID, diRegenTime) = miniMap.GetAtlasInfo(mouseX, mouseY)
			if chr.IsGameMaster(0):
				net.SendChatPacket("/go %s %s" % (str(iPosX), str(iPosY)))

	def OnPressEscapeKey(self):
		self.Close()
		return True

class MiniMap(ui.ScriptWindow):

	CANNOT_SEE_INFO_MAP_DICT = {
		"metin2_map_monkeydungeon" : False,
		"metin2_map_monkeydungeon_02" : False,
		"metin2_map_monkeydungeon_03" : False,
		"metin2_map_devilsCatacomb" : False,
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__Initialize()

		miniMap.Create()
		miniMap.SetScale(2.0)

		self.AtlasWindow = AtlasWindow()
		self.AtlasWindow.LoadWindow()
		self.AtlasWindow.Hide()

		self.tooltipMiniMapOpen = MapTextToolTip()
		self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)
		self.tooltipMiniMapOpen.Show()
		self.tooltipMiniMapClose = MapTextToolTip()
		self.tooltipMiniMapClose.SetText(localeInfo.UI_CLOSE)
		self.tooltipMiniMapClose.Show()
		self.tooltipScaleUp = MapTextToolTip()
		self.tooltipScaleUp.SetText(localeInfo.MINIMAP_INC_SCALE)
		self.tooltipScaleUp.Show()
		self.tooltipScaleDown = MapTextToolTip()
		self.tooltipScaleDown.SetText(localeInfo.MINIMAP_DEC_SCALE)
		self.tooltipScaleDown.Show()
		self.tooltipAtlasOpen = MapTextToolTip()
		self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		self.tooltipAtlasOpen.Show()
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		if app.ENABLE_OFFLINE_SHOP:
			self.tooltipShopSearch = MapTextToolTip()
			self.tooltipShopSearch.SetText(uiScriptLocale.PRIVATESHOPSEARCH_SEARCH)
			self.tooltipShopSearch.Show()
			self.tooltipShopSearch.SetHorizontalAlignLeft()

		if app.ENABLE_GLOBAL_RANKING:
			self.tooltipRanking = MapTextToolTip()
			self.tooltipRanking.SetText(uiScriptLocale.TOTAL_RANKING)
			self.tooltipRanking.Show()
			self.tooltipRanking.SetHorizontalAlignLeft()

		if app.ENABLE_BIOLOG_SYSTEM:
			self.tooltipBiolog = MapTextToolTip()
			self.tooltipBiolog.SetText(uiScriptLocale.QUEST_UI_TEXT_COLLECTION)
			self.tooltipBiolog.Show()
			self.tooltipBiolog.SetHorizontalAlignLeft()

		if app.ENABLE_EXTENDED_BATTLE_PASS:
			self.tooltipBattlePass = MapTextToolTip()
			self.tooltipBattlePass.SetText("Battle-Pass")
			self.tooltipBattlePass.Show()

		if app.ENABLE_DUNGEON_INFO:
			self.tooltipDungeonInfo = MapTextToolTip()
			self.tooltipDungeonInfo.SetText(localeInfo.DUNGEON_TIMER_TITLE)
			self.tooltipDungeonInfo.Show()

		if miniMap.IsAtlas():
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		else:
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_CAN_NOT_SHOW_AREAMAP)

		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		self.mapName = ""

		self.isLoaded = 0
		self.canSeeInfo = True

	def __del__(self):
		miniMap.Destroy()
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.positionInfo = 0
		self.observerCount = 0

		self.OpenWindow = 0
		self.CloseWindow = 0
		self.ScaleUpButton = 0
		self.ScaleDownButton = 0
		self.MiniMapHideButton = 0
		self.MiniMapShowButton = 0
		self.AtlasShowButton = 0

		self.tooltipMiniMapOpen = 0
		self.tooltipMiniMapClose = 0
		self.tooltipScaleUp = 0
		self.tooltipScaleDown = 0
		self.tooltipAtlasOpen = 0
		self.tooltipInfo = None
		self.serverInfo = None
		self.channelInfo = None
		self.FPSInfo = 0

		self.currentDate = 0
		self.currentHour = 0

		self.interface = None

		if app.ENABLE_GLOBAL_RANKING:
			self.globalRankingButton = None
			self.tooltipglobalRanking = None

		if app.ENABLE_OFFLINE_SHOP:
			self.shopSearchButton = None
			self.tooltipShopSearch = None

		if app.ENABLE_BIOLOG_SYSTEM:
			self.biologButton = None
			self.tooltipBiolog = None

		if app.ENABLE_EXTENDED_BATTLE_PASS:
			self.battlePassButton = None
			self.tooltipBattlePass = None

		if app.ENABLE_DUNGEON_INFO:
			self.DungeonInfoButton = None
			self.tooltipDungeonInfo = None

	def SetMapName(self, mapName):
		self.mapName=mapName
		self.AtlasWindow.SetMapName(mapName)

		if self.CANNOT_SEE_INFO_MAP_DICT.has_key(mapName):
			self.canSeeInfo = False
			self.HideMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP_CANNOT_SEE)
		else:
			self.canSeeInfo = True
			self.ShowMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/MiniMap.py")

		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.LoadScript")

		try:
			self.OpenWindow = self.GetChild("OpenWindow")
			self.MiniMapWindow = self.GetChild("MiniMapWindow")
			self.ScaleUpButton = self.GetChild("ScaleUpButton")
			self.ScaleDownButton = self.GetChild("ScaleDownButton")
			self.MiniMapHideButton = self.GetChild("MiniMapHideButton")
			self.AtlasShowButton = self.GetChild("AtlasShowButton")
			self.CloseWindow = self.GetChild("CloseWindow")
			self.MiniMapShowButton = self.GetChild("MiniMapShowButton")
			self.positionInfo = self.GetChild("PositionInfo")
			self.observerCount = self.GetChild("ObserverCount")
			self.serverInfo = self.GetChild("ServerInfo")
			self.channelInfo = self.GetChild("ChannelInfo")
			self.FPSInfo = self.GetChild("FPSInfo")
			self.currentDate = self.GetChild("CurrentDate")
			self.currentHour = self.GetChild("CurrentTime")

			if app.ENABLE_GLOBAL_RANKING:
				self.globalRankingButton = self.GetChild("GlobalRankingButton")
			if app.ENABLE_OFFLINE_SHOP:
				self.shopSearchButton = self.GetChild("ShopSearchButton")
			if app.ENABLE_BIOLOG_SYSTEM:
				self.biologButton = self.GetChild("BiologButton")
			if app.ENABLE_EXTENDED_BATTLE_PASS:
				self.battlePassButton = self.GetChild("BattlePassButton")
			if app.ENABLE_DUNGEON_INFO:
				self.DungeonInfoButton = self.GetChild("DungeonInfoButton")

		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.Bind")

		if constInfo.MINIMAP_POSITIONINFO_ENABLE==0:
			self.positionInfo.Hide()

		self.serverInfo.SetText(net.GetServerInfo())
		self.channelInfo.SetText("CH Unknown")
		self.ScaleUpButton.SetEvent(ui.__mem_func__(self.ScaleUp))
		self.ScaleDownButton.SetEvent(ui.__mem_func__(self.ScaleDown))
		self.MiniMapHideButton.SetEvent(ui.__mem_func__(self.HideMiniMap))
		self.MiniMapShowButton.SetEvent(ui.__mem_func__(self.ShowMiniMap))

		if app.ENABLE_GLOBAL_RANKING:
			self.globalRankingButton.SetEvent(ui.__mem_func__(self.__OnClickGlobalRankingButton))

		if app.ENABLE_OFFLINE_SHOP:
			self.shopSearchButton.SetEvent(ui.__mem_func__(self.__OnClickOfflineShopButton))
		
		if app.ENABLE_BIOLOG_SYSTEM:
			self.biologButton.SetEvent(ui.__mem_func__(self.__OnClickBiologButton))

		if miniMap.IsAtlas():
			self.AtlasShowButton.SetEvent(ui.__mem_func__(self.ShowAtlas))

		(ButtonPosX, ButtonPosY) = self.MiniMapShowButton.GetGlobalPosition()
		self.tooltipMiniMapOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.MiniMapHideButton.GetGlobalPosition()
		self.tooltipMiniMapClose.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleUpButton.GetGlobalPosition()
		self.tooltipScaleUp.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleDownButton.GetGlobalPosition()
		self.tooltipScaleDown.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.AtlasShowButton.GetGlobalPosition()
		self.tooltipAtlasOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		if app.ENABLE_OFFLINE_SHOP:
			(ButtonPosX, ButtonPosY) = self.shopSearchButton.GetGlobalPosition()
			ShopSearchTooltipTextWidth = self.tooltipShopSearch.GetTextSize()[0]
			self.tooltipShopSearch.SetTooltipPosition(ButtonPosX-ShopSearchTooltipTextWidth, ButtonPosY + 10)

		if app.ENABLE_GLOBAL_RANKING:
			(ButtonPosX, ButtonPosY) = self.globalRankingButton.GetGlobalPosition()
			GlobalRankingTooltipTextWidth = self.tooltipRanking.GetTextSize()[0]
			self.tooltipRanking.SetTooltipPosition(ButtonPosX-GlobalRankingTooltipTextWidth, ButtonPosY + 10)

		if app.ENABLE_BIOLOG_SYSTEM:
			(ButtonPosX, ButtonPosY) = self.biologButton.GetGlobalPosition()
			BiologTooltipTextWidth = self.tooltipBiolog.GetTextSize()[0]
			self.tooltipBiolog.SetTooltipPosition(ButtonPosX-BiologTooltipTextWidth, ButtonPosY + 10)

		if app.ENABLE_EXTENDED_BATTLE_PASS:
			self.battlePassButton.SetEvent(ui.__mem_func__(self.OnClickBattlePass))
			(ButtonPosX, ButtonPosY) = self.battlePassButton.GetGlobalPosition()
			self.tooltipBattlePass.SetTooltipPosition(ButtonPosX, ButtonPosY)

		if app.ENABLE_DUNGEON_INFO:
			self.DungeonInfoButton.SetEvent(ui.__mem_func__(self.OnClickDungeonInfo))
			(ButtonPosX, ButtonPosY) = self.DungeonInfoButton.GetGlobalPosition()
			self.tooltipDungeonInfo.SetTooltipPosition(ButtonPosX, ButtonPosY)

		self.ShowMiniMap()

	def Destroy(self):
		self.HideMiniMap()

		self.AtlasWindow.Destroy()
		self.AtlasWindow = None

		self.ClearDictionary()

		self.__Initialize()

	def UpdateObserverCount(self, observerCount):
		if observerCount>0:
			self.observerCount.Show()
		elif observerCount<=0:
			self.observerCount.Hide()

		self.observerCount.SetText(localeInfo.MINIMAP_OBSERVER_COUNT % observerCount)

	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		miniMap.Update(x, y)

		self.positionInfo.SetText("(%.0f, %.0f)" % (x/100, y/100))
		self.currentDate.SetText(time.strftime("%d/%m/%Y"))
		self.currentHour.SetText(time.strftime("%H:%M:%S"))

		rtt = app.GetRTT()
		if rtt > 999:
			rtt = "+999".format(rtt)

		pktLossPct = app.GetPacketLossPct()

		if chr.IsGameMaster(0):
			self.FPSInfo.SetText("Rps: {}, UFPS: {}".format(app.GetRenderFPS(), app.GetUpdateFPS()))
			self.FPSInfo.SetPosition(-20, 0)
		else:
			self.FPSInfo.SetText("{} fps {} ping".format(app.GetRenderFPS(), rtt))
			self.FPSInfo.SetPosition(-8, 0)

		if self.tooltipInfo:
			if True == self.MiniMapWindow.IsIn():
				(mouseX, mouseY) = wndMgr.GetMousePosition()
				(bFind, sName, iPosX, iPosY, dwTextColor) = miniMap.GetInfo(mouseX, mouseY)
				if bFind == 0:
					self.tooltipInfo.Hide()
				elif not self.canSeeInfo:
					self.tooltipInfo.SetText("%s(%s)" % (sName, localeInfo.UI_POS_UNKNOWN))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
				else:
					self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
			else:
				self.tooltipInfo.Hide()

		if True == self.MiniMapShowButton.IsIn():
			self.tooltipMiniMapOpen.Show()
		else:
			self.tooltipMiniMapOpen.Hide()

		if True == self.MiniMapHideButton.IsIn():
			self.tooltipMiniMapClose.Show()
		else:
			self.tooltipMiniMapClose.Hide()

		if True == self.ScaleUpButton.IsIn():
			self.tooltipScaleUp.Show()
		else:
			self.tooltipScaleUp.Hide()

		if True == self.ScaleDownButton.IsIn():
			self.tooltipScaleDown.Show()
		else:
			self.tooltipScaleDown.Hide()

		if True == self.AtlasShowButton.IsIn():
			self.tooltipAtlasOpen.Show()
		else:
			self.tooltipAtlasOpen.Hide()

		if True == self.globalRankingButton.IsIn() and app.ENABLE_GLOBAL_RANKING:
			self.tooltipRanking.Show()
		else:
			self.tooltipRanking.Hide()

		if True == self.shopSearchButton.IsIn() and app.ENABLE_OFFLINE_SHOP:
			self.tooltipShopSearch.Show()
		else:
			self.tooltipShopSearch.Hide()

		if True == self.biologButton.IsIn() and app.ENABLE_BIOLOG_SYSTEM:
			self.tooltipBiolog.Show()
		else:
			self.tooltipBiolog.Hide()

		if app.ENABLE_EXTENDED_BATTLE_PASS and self.battlePassButton.IsIn():
			self.tooltipBattlePass.Show()
		else:
			self.tooltipBattlePass.Hide()

		if app.ENABLE_DUNGEON_INFO and self.DungeonInfoButton.IsIn():
			self.tooltipDungeonInfo.Show()
		else:
			self.tooltipDungeonInfo.Hide()

	def OnRender(self):
		(x, y) = self.GetGlobalPosition()
		fx = float(x)
		fy = float(y)
		miniMap.Render(fx + 4.0, fy + 5.0)

	def BindInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def Close(self):
		self.HideMiniMap()

	def HideMiniMap(self):
		miniMap.Hide()
		self.OpenWindow.Hide()
		self.CloseWindow.Show()

	def ShowMiniMap(self):
		if not self.canSeeInfo:
			return

		miniMap.Show()
		self.OpenWindow.Show()
		self.CloseWindow.Hide()

	def isShowMiniMap(self):
		return miniMap.isShow()

	def ScaleUp(self):
		miniMap.ScaleUp()

	def ScaleDown(self):
		miniMap.ScaleDown()

	def ShowAtlas(self):
		if not miniMap.IsAtlas():
			return
		if self.AtlasWindow.IsShow():
			self.AtlasWindow.Hide()
		else:
			self.AtlasWindow.Show()

	def ToggleAtlasWindow(self):
		if not miniMap.IsAtlas():
			return
		if self.AtlasWindow.IsShow():
			self.AtlasWindow.Hide()
		else:
			self.AtlasWindow.Show()

	if app.ENABLE_CHANNEL_INFO_UPDATE:
		def UpdateChannelInfo(self, channel):
			if constInfo.SERVER_SELECTED == 1:
				srvName = serverInfo.SERVER_NAME
			else:
				srvName = serverInfo.SERVER_NAME_2

			if channel == 99:
				serverInfoStr = 'Social Channel'
			else:
				serverInfoStr = 'Channel {}'.format(str(channel))

			self.channelInfo.SetText(serverInfoStr)
			self.serverInfo.SetText(srvName)
			net.SetServerInfo(srvName)

	if app.ENABLE_GLOBAL_RANKING:
		def __OnClickGlobalRankingButton(self):
			self.interface.wndGame.SendOpenRanking()

	if app.ENABLE_OFFLINE_SHOP:
		def __OnClickOfflineShopButton(self):
			if self.interface.wndShopSearch.IsShow():
				self.interface.wndShopSearch.Hide()
			else:
				self.interface.wndShopSearch.Show()

	if app.ENABLE_BIOLOG_SYSTEM:
		def __OnClickBiologButton(self):
			biolog.OpenWindow()

	if app.ENABLE_EXTENDED_BATTLE_PASS:
		def OnClickBattlePass(self):
			if self.interface:
				self.interface.ToggleBattlePassExtended()

	if app.ENABLE_DUNGEON_INFO:
		def OnClickDungeonInfo(self):
			game = constInfo.GetGameInstance()
			if game:
				game.ToggleBossTimerWindow()
