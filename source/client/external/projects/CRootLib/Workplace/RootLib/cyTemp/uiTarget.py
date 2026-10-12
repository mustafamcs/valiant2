# -*- coding: cp949 -*-
#-932016769
import app
import ui
import player
import net
import wndMgr
import messenger
import guild
import chr
import nonplayer
import localeInfo
import constInfo

SAVED_POS = [0, 0]

if app.ENABLE_TARGET_INFORMATION_SYSTEM:
	import item, uiToolTip
	def HAS_FLAG(value, flag):
		return (value & flag) == flag

if app.ENABLE_SHOW_STROKE_INFO:
	DICT_MOB_STROKE_INFO = {}

class TargetBoard(ui.ThinBoardNew):

	if app.ENABLE_TARGET_INFORMATION_SYSTEM:
		class InfoBoard(ui.ThinBoardNew):
			class ItemListBoxItem(ui.ListBoxExNew.Item):
				def __init__(self, width):
					ui.ListBoxExNew.Item.__init__(self)

					image = ui.ExpandedImageBox()
					image.SetParent(self)
					image.Show()
					self.image = image

					nameLine = ui.TextLine()
					nameLine.SetParent(self)
					nameLine.SetPosition(32 + 5, 0)
					nameLine.Show()
					self.nameLine = nameLine

					self.SetSize(width, 32 + 5)

				def LoadImage(self, image, name = None):
					self.image.LoadImage(image)
					self.SetSize(self.GetWidth(), self.image.GetHeight() + 5 * (self.image.GetHeight() / 32))
					if name != None:
						self.SetText(name)

				def SetText(self, text):
					self.nameLine.SetText(text)

				def RefreshHeight(self):
					ui.ListBoxExNew.Item.RefreshHeight(self)
					self.image.SetRenderingRect(0.0, 0.0 - float(self.removeTop) / float(self.GetHeight()), 0.0, 0.0 - float(self.removeBottom) / float(self.GetHeight()))
					self.image.SetPosition(0, - self.removeTop)

			MAX_ITEM_COUNT = 5

			EXP_BASE_LVDELTA = [
				1,		# -15 0
				5,		# -14 1
				10,		# -13 2
				20,		# -12 3
				30,		# -11 4
				50,		# -10 5
				70,		# -9 6
				80,		# -8 7
				85,		# -7 8
				90,		# -6 9
				92,		# -5 10
				94,		# -4 11
				96,		# -3 12
				98,		# -2 13
				100,	# -1 14
				100,	# 0 15
				105,	# 1 16
				110,	# 2 17
				115,	# 3 18
				120,	# 4 19
				125,	# 5 20
				130,	# 6 21
				135,	# 7 22
				140,	# 8 23
				145,	# 9 24
				150,	# 10 25
				155,	# 11 26
				160,	# 12 27
				165,	# 13 28
				170,	# 14 29
				180,	# 15 30
			]

			RACE_FLAG_TO_NAME = {
				1 << 0 : localeInfo. TARGET_INFO_RACE_ANIMAL,
				1 << 1 : localeInfo. TARGET_INFO_RACE_UNDEAD,
				1 << 2 : localeInfo. TARGET_INFO_RACE_DEVIL,
				1 << 3 : localeInfo. TARGET_INFO_RACE_HUMAN,
				1 << 4 : localeInfo. TARGET_INFO_RACE_ORC,
				1 << 5 : localeInfo. TARGET_INFO_RACE_MILGYO,
				1 << 6 : localeInfo. TARGET_INFO_RACE_INSECT,
				1 << 7 : localeInfo. TARGET_INFO_RACE_FIRE,
				1 << 8 : localeInfo. TARGET_INFO_RACE_ICE,
				1 << 9 : localeInfo. TARGET_INFO_RACE_DESERT,
				1 << 10 : localeInfo.TARGET_INFO_RACE_TREE,
			}

			SUB_RACE_FLAG_TO_NAME = {
				1 << 11 : localeInfo.TARGET_INFO_RACE_ELEC,
				1 << 12 : localeInfo.TARGET_INFO_RACE_FIRE,
				1 << 13 : localeInfo.TARGET_INFO_RACE_ICE,
				1 << 14 : localeInfo.TARGET_INFO_RACE_WIND,
				1 << 15 : localeInfo.TARGET_INFO_RACE_EARTH,
				1 << 16 : localeInfo.TARGET_INFO_RACE_DARK,
			}

			STONE_START_VNUM = 28030
			STONE_LAST_VNUM = 28042

			BOARD_WIDTH = 300

			def __init__(self):
				ui.ThinBoardNew.__init__(self)

				self.HideCorners(self.LT)
				self.HideCorners(self.RT)
				self.HideLine(self.T)

				self.race = 0
				self.hasItems = False

				self.itemTooltip = uiToolTip.ItemToolTip()
				self.itemTooltip.HideToolTip()

				self.onlyDrops = None
				self.stoneImg = None
				self.stoneVnum = None
				self.stoneRace = None
				self.lastStoneVnum = 0
				self.nextStoneIconChange = 0
				self.interface = None
				self.itemScrollBar = None

				self.SetSize(self.BOARD_WIDTH, 0)

			def __del__(self):
				ui.ThinBoardNew.__del__(self)

			def __UpdatePosition(self, targetBoard):
				self.SetPosition(targetBoard.GetLeft() + (targetBoard.GetWidth() - self.GetWidth()) / 2, targetBoard.GetBottom() - 17)

			def Open(self, targetBoard, race, onlyDrops):
				self.onlyDrops = onlyDrops
				self.__LoadInformation(race)

				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)

				self.__UpdatePosition(targetBoard)

				self.Show()

			def Refresh(self):
				self.__LoadInformation(self.race)
				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)

			def Close(self):
				self.itemTooltip.HideToolTip()
				self.Hide()
				self.interface = None
			def __LoadInformation(self, race):
				self.yPos = 7
				self.children = []
				self.race = race
				self.stoneImg = None
				self.stoneVnum = None
				self.stoneRace = None
				self.nextStoneIconChange = 0

				self.itemScrollBar = None
				
				if self.onlyDrops:
					self.__LoadInformation_Drop(race)
					self.__LoadInformation_Drops(race)
				else:
					self.__LoadInformation_Default(race)
					self.__LoadInformation_Race(race)
					self.__LoadInformation_Resists(race)

			def __LoadInformation_Default_GetHitRate(self, race):
				attacker_dx = nonplayer.GetMonsterDX(race)
				attacker_level = nonplayer.GetMonsterLevel(race)

				self_dx = player.GetStatus(player.DX)
				self_level = player.GetStatus(player.LEVEL)

				iARSrc = min(90, (attacker_dx * 4 + attacker_level * 2) / 6)
				iERSrc = min(90, (self_dx * 4 + self_level * 2) / 6)

				fAR = (float(iARSrc) + 210.0) / 300.0
				fER = (float(iERSrc) * 2 + 5) / (float(iERSrc) + 95) * 3.0 / 10.0

				return fAR - fER

			def __LoadInformation_Resists(self, race):
				poison = nonplayer.GetMonsterResisPoison(race)
				app_poison = localeInfo.POISONED_NO
				if poison != 0:
					app_poison = localeInfo.POISONED_YES
				
				self.AppendSeperator()
				self.AppendTextLine(localeInfo.TARGET_INFO_RESISTS)
				self.AppendTextLine(localeInfo.TARGET_INFO_RESISTS_LINE0 % (nonplayer.GetResist(race, nonplayer.MOB_RESIST_SWORD), nonplayer.GetResist(race, nonplayer.MOB_RESIST_TWOHAND), nonplayer.GetResist(race, nonplayer.MOB_RESIST_BELL)))
				self.AppendTextLine(localeInfo.TARGET_INFO_RESISTS_LINE1 % (nonplayer.GetResist(race, nonplayer.MOB_RESIST_DAGGER), nonplayer.GetResist(race, nonplayer.MOB_RESIST_FAN), nonplayer.GetResist(race, nonplayer.MOB_RESIST_BOW)))

				self.AppendSeperator()
				self.AppendTextLine(localeInfo.TARGET_INFO_RESIS_5 % app_poison)
				
			def __LoadInformation_Drop(self, race):
				monsterLevel = nonplayer.GetMonsterLevel(race)
				player_level = player.GetStatus(player.LEVEL)
				is_stone = bool(nonplayer.IsMonsterStone(race))
				self.AppendSeperator()
				if ((player_level > monsterLevel) and abs(player_level-monsterLevel) > 15):
					self.AppendTextLine("|cffD14646{}.".format(localeInfo.CANT_GET_FROM_STONE_TARGET if is_stone else localeInfo.CANT_GET_FROM_MONSTER_TARGET))
					self.AppendTextLine(localeInfo.CANT_GET_FROM_SMT_CUZ)
					self.AppendTextLine("")
			
			def __LoadInformation_Default(self, race):
				self.AppendSeperator()
				self.AppendTextLine(localeInfo.INFORMATIONS_TARGET)
				self.AppendTextLine("")
				self.AppendTextLine(localeInfo.TARGET_INFO_MAX_HP % localeInfo.NumberToDecimal(nonplayer.GetMonsterMaxHP(race)))

				# calc att damage
				monsterLevel = nonplayer.GetMonsterLevel(race)
				fHitRate = self.__LoadInformation_Default_GetHitRate(race)
				iDamMin, iDamMax = nonplayer.GetMonsterDamage(race)
				iDamMin = long((iDamMin + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDamMax = long((iDamMax + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDef = player.GetStatus(player.DEF_GRADE) * (100 + player.GetStatus(player.DEF_BONUS)) / 100
				fDamMulti = nonplayer.GetMonsterDamageMultiply(race)
				iDamMin = long(max(0, iDamMin - iDef) * fDamMulti)
				iDamMax = long(max(0, iDamMax - iDef) * fDamMulti)
				if iDamMin < 1:
					iDamMin = 1
				if iDamMax < 5:
					iDamMax = 5
				self.AppendTextLine(localeInfo.TARGET_INFO_DAMAGE % (str(iDamMin), str(iDamMax)))

				idx = min(len(self.EXP_BASE_LVDELTA) - 1, max(0, (monsterLevel + 15) - player.GetStatus(player.LEVEL)))
				iExp = nonplayer.GetMonsterExp(race) * self.EXP_BASE_LVDELTA[idx] / 100
				self.AppendTextLine(localeInfo.TARGET_INFO_EXP % localeInfo.NumberToDecimal(iExp))
				self.AppendTextLine(localeInfo.TARGET_INFO_REGEN_INFO % (nonplayer.GetMobRegenPercent(race), nonplayer.GetMobRegenCycle(race)))

			def __LoadInformation_Race(self, race):
				dwRaceFlag = nonplayer.GetMonsterRaceFlag(race)
				self.AppendSeperator()

				mainrace = ""
				subrace = ""
				for i in xrange(17):
					curFlag = 1 << i
					if HAS_FLAG(dwRaceFlag, curFlag):
						if self.RACE_FLAG_TO_NAME.has_key(curFlag):
							mainrace += self.RACE_FLAG_TO_NAME[curFlag] + ", "
						elif self.SUB_RACE_FLAG_TO_NAME.has_key(curFlag):
							subrace += self.SUB_RACE_FLAG_TO_NAME[curFlag] + ", "
				if nonplayer.IsMonsterStone(race):
					mainrace += localeInfo.TARGET_INFO_RACE_METIN + ", "
				if mainrace == "":
					mainrace = localeInfo.TARGET_INFO_NO_RACE
				else:
					mainrace = mainrace[:-2]
				if subrace == "":
					subrace = localeInfo.TARGET_INFO_NO_RACE
				else:
					subrace = subrace[:-2]

				self.AppendTextLine(localeInfo.TARGET_INFO_MAINRACE % mainrace)
				self.AppendTextLine(localeInfo.TARGET_INFO_SUBRACE % subrace)

			def __LoadInformation_Drops(self, race):
				self.AppendTextLine(localeInfo.POSSIBLE_DROPS_FROM_TARGET)
				self.AppendSeperator(True)

				if race in constInfo.MONSTER_INFO_DATA:
					if len(constInfo.MONSTER_INFO_DATA[race]["items"]) == 0:
						self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)
					else:
						itemListBox = ui.ListBoxExNew(32 + 5, self.MAX_ITEM_COUNT)
						itemListBox.SetSize(self.GetWidth() - 15 * 2 - ui.ScrollBar.SCROLLBAR_WIDTH, (32 + 5) * self.MAX_ITEM_COUNT)
						height = 0
						for curItem in constInfo.MONSTER_INFO_DATA[race]["items"]:
							if curItem.has_key("vnum_list"):
								height += self.AppendItem(itemListBox, curItem["vnum_list"], curItem["count"], race)
							else:
								height += self.AppendItem(itemListBox, curItem["vnum"], curItem["count"], race)
						if height < itemListBox.GetHeight():
							itemListBox.SetSize(itemListBox.GetWidth(), height)
						self.AppendWindow(itemListBox, 15)
						itemListBox.SetBasePos(0)

						if len(constInfo.MONSTER_INFO_DATA[race]["items"]) > itemListBox.GetViewItemCount():
							itemScrollBar = ui.ScrollBarAe()
							itemScrollBar.SetParent(self)
							itemScrollBar.SetPosition(itemListBox.GetRight(), itemListBox.GetTop())
							itemScrollBar.SetScrollBarSize(32 * self.MAX_ITEM_COUNT + 5 * (self.MAX_ITEM_COUNT - 1))
							itemScrollBar.SetScrollStep(0.15)
							# itemScrollBar.UpdateScrollWidth(40)
							itemScrollBar.SetMiddleBarSize(float(self.MAX_ITEM_COUNT) / float(height / (32 + 5)))
							itemScrollBar.Show()
							itemListBox.SetScrollBar(itemScrollBar)
							self.itemScrollBar = itemScrollBar
				else:
					self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)

			def AppendTextLine(self, text):
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetWindowHorizontalAlignCenter()
				textLine.SetHorizontalAlignCenter()
				textLine.SetText(text)
				textLine.SetPosition(0, self.yPos)
				textLine.Show()

				self.children.append(textLine)
				self.yPos += 17

			def AppendSeperator(self, hide_image = False):
				img = ui.ImageBox()
				img.LoadImage("d:/ymir work/ui/pattern/seperator.tga")
				self.AppendWindow(img)
				img.SetPosition(img.GetLeft(), img.GetTop() - 15)
				if hide_image is True:
					img.Hide()
				self.yPos -= 15

			def AppendItem(self, listBox, vnums, count, race):
				if type(vnums) == int:
					vnum = vnums
				else:
					vnum = vnums[0]

				item.SelectItem(vnum)
				itemName = item.GetItemName()
				if type(vnums) != int and len(vnums) > 1:
					vnums = sorted(vnums)
					realName = itemName[:itemName.find("+")]
					if item.GetItemType() == item.ITEM_TYPE_METIN:
						realName = localeInfo.TARGET_INFO_STONE_NAME
						itemName = realName + ["+0 - +3", "+0 - +4"][bool(nonplayer.GetMonsterLevel(race) > 35)]
					else:
						itemName = realName + "+" + str(vnums[0] % 10) + " - +" + str(vnums[len(vnums) - 1] % 10)
					vnum = vnums[len(vnums) - 1]

				myItem = self.ItemListBoxItem(listBox.GetWidth())
				myItem.LoadImage(item.GetIconImageFileName())
				if count <= 1:
					myItem.SetText(itemName)
				else:
					myItem.SetText("%s - %dx" % (itemName, count))
				myItem.SAFE_SetOverInEvent(self.OnShowItemTooltip, vnum, race)
				myItem.SAFE_SetOverOutEvent(self.OnHideItemTooltip)
				listBox.AppendItem(myItem)

				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.stoneImg = myItem
					self.stoneVnum = vnums
					self.stoneRace = race
					self.lastStoneVnum = self.STONE_LAST_VNUM + vnums[len(vnums) - 1] % 1000 / 100 * 100

				return myItem.GetHeight()

			def OnShowItemTooltip(self, vnum, race):
				item.SelectItem(vnum)
				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.itemTooltip.isStone = True
					self.itemTooltip.stoneRace = race
					self.itemTooltip.isBook = False
					self.itemTooltip.isBook2 = False
					self.itemTooltip.SetItemToolTip(self.lastStoneVnum)
				else:
					self.itemTooltip.isStone = False
					self.itemTooltip.stoneRace = None
					self.itemTooltip.isBook = True
					self.itemTooltip.isBook2 = True
					self.itemTooltip.SetItemToolTip(vnum)
				if app.ENABLE_RENDER_TARGET:
					self.itemTooltip.AppendRenderingTooltip(vnum)
					self.itemTooltip.AppendWikiTooltip()

			def OnHideItemTooltip(self):
				self.itemTooltip.HideToolTip()

			def OnRunMouseWheel(self, nLen):
				if nLen > 0:
					self.itemScrollBar.OnUp()
				else:
					self.itemScrollBar.OnDown()

			def AppendWindow(self, wnd, x = 0, width = 0, height = 0):
				if width == 0:
					width = wnd.GetWidth()
				if height == 0:
					height = wnd.GetHeight()

				wnd.SetParent(self)
				if x == 0:
					wnd.SetPosition((self.GetWidth() - width) / 2, self.yPos)
				else:
					wnd.SetPosition(x, self.yPos)
				wnd.Show()

				self.children.append(wnd)
				self.yPos += height + 5

			def OnUpdate(self):
				if self.stoneImg != None and self.stoneVnum != None and self.stoneRace != None and app.GetTime() >= self.nextStoneIconChange:
					nextImg = self.lastStoneVnum + 1
					if nextImg % 100 > self.STONE_LAST_VNUM % 100:
						nextImg -= (self.STONE_LAST_VNUM - self.STONE_START_VNUM) + 1
					self.lastStoneVnum = nextImg
					self.nextStoneIconChange = app.GetTime() + 1.0

					item.SelectItem(nextImg)
					itemName = item.GetItemName()
					realName = itemName[:itemName.find("+")]
					stoneLevel = ["+0 - +3", "+0 - +4"][bool(nonplayer.GetMonsterLevel(self.stoneRace) > 35)]
					realName = realName + str(stoneLevel)
					self.stoneImg.LoadImage(item.GetIconImageFileName(), realName)

					if self.itemTooltip.IsShow() and self.itemTooltip.isStone:
						self.itemTooltip.SetItemToolTip(nextImg)

	BUTTON_NAME_LIST = (
		localeInfo.TARGET_BUTTON_WHISPER,
		localeInfo.TARGET_BUTTON_EXCHANGE,
		localeInfo.TARGET_BUTTON_FIGHT,
		localeInfo.TARGET_BUTTON_ACCEPT_FIGHT,
		localeInfo.TARGET_BUTTON_AVENGE,
		localeInfo.TARGET_BUTTON_FRIEND,
		localeInfo.TARGET_BUTTON_INVITE_PARTY,
		localeInfo.TARGET_BUTTON_LEAVE_PARTY,
		localeInfo.TARGET_BUTTON_EXCLUDE,
		localeInfo.TARGET_BUTTON_INVITE_GUILD,
		localeInfo.TARGET_BUTTON_DISMOUNT,
		localeInfo.TARGET_BUTTON_EXIT_OBSERVER,
		localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT,
		localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY,
		localeInfo.TARGET_BUTTON_BUILDING_DESTROY,
		localeInfo.TARGET_BUTTON_EMOTION_ALLOW,
		"VOTE_BLOCK_CHAT",
	)

	GRADE_NAME =	{
						nonplayer.PAWN : localeInfo.TARGET_LEVEL_PAWN,
						nonplayer.S_PAWN : localeInfo.TARGET_LEVEL_S_PAWN,
						nonplayer.KNIGHT : localeInfo.TARGET_LEVEL_KNIGHT,
						nonplayer.S_KNIGHT : localeInfo.TARGET_LEVEL_S_KNIGHT,
						nonplayer.BOSS : localeInfo.TARGET_LEVEL_BOSS,
						nonplayer.KING : localeInfo.TARGET_LEVEL_KING,
					}
	EXCHANGE_LIMIT_RANGE = 3000

	if app.ENABLE_ELEMENT_ADD:
		ELEMENT_IMG_PATH = \
		{
			1 : "d:/ymir work/ui/game/12zi/element/elect.sub", # RACE_FLAG_ATT_ELEC
			2 : "d:/ymir work/ui/game/12zi/element/fire.sub", # RACE_FLAG_ATT_FIRE
			3 : "d:/ymir work/ui/game/12zi/element/ice.sub", # RACE_FLAG_ATT_ICE
			4 : "d:/ymir work/ui/game/12zi/element/wind.sub", # RACE_FLAG_ATT_WIND
			5 : "d:/ymir work/ui/game/12zi/element/earth.sub", # RACE_FLAG_ATT_EARTH
			6 : "d:/ymir work/ui/game/12zi/element/dark.sub", # RACE_FLAG_ATT_DARK
		}

	def __init__(self):
		ui.ThinBoardNew.__init__(self)
		if app.ENABLE_SHOW_STROKE_INFO:
			strokeInfo = ui.TextLine()
			strokeInfo.SetDefaultFontName()
			strokeInfo.SetParent(self)
			strokeInfo.SetOutline()
			strokeInfo.SetPosition(10, 45)
			strokeInfo.Hide()

		name = ui.TextLine()
		name.SetParent(self)
		name.SetDefaultFontName()
		name.SetOutline()
		name.Show()

		hpGauge = ui.DynamicGauge()
		hpGauge.SetParent(self)
		hpGauge.MakeGauge ( 130 , "red" , "purple" )
		hpGauge.Hide()

		closeButton = ui.Button()
		closeButton.SetParent(self)
		closeButton.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		closeButton.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		closeButton.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		closeButton.SetPosition(30, 13)

		hpGauge.SetPosition(175, 17)
		hpGauge.SetWindowHorizontalAlignRight()
		closeButton.SetWindowHorizontalAlignRight()

		if app.ENABLE_TARGET_INFORMATION_SYSTEM:
			infoButton = ui.Button()
			infoButton.SetParent(self)
			infoButton.SetUpVisual("d:/ymir work/ui/pattern/dinfo1.png")
			infoButton.SetOverVisual("d:/ymir work/ui/pattern/dinfo2.png")
			infoButton.SetDownVisual("d:/ymir work/ui/pattern/dinfo3.png")
			infoButton.SetEvent(ui.__mem_func__(self.OnPressedInfoButton))
			infoButton.Hide()

			infoBoard = self.InfoBoard()
			infoBoard.Hide()
			infoButton.showWnd = infoBoard
			
			dropButton = ui.Button()
			dropButton.SetParent(self)
			dropButton.SetUpVisual("d:/ymir work/ui/pattern/minfo1.png")
			dropButton.SetOverVisual("d:/ymir work/ui/pattern/minfo2.png")
			dropButton.SetDownVisual("d:/ymir work/ui/pattern/minfo3.png")
			dropButton.SetEvent(ui.__mem_func__(self.OnPressedDropInfoButton))
			dropButton.Hide()

			settingsButton = ui.Button()
			settingsButton.SetParent(self)
			settingsButton.SetUpVisual("d:/ymir work/ui/pattern/settings_01.png")
			settingsButton.SetOverVisual("d:/ymir work/ui/pattern/settings_02.png")
			settingsButton.SetDownVisual("d:/ymir work/ui/pattern/settings_03.png")
			settingsButton.SetEvent(ui.__mem_func__(self.OpenGameOptionWindow))
			settingsButton.Hide()

			wikiButton = ui.Button()
			wikiButton.SetParent(self)
			wikiButton.SetUpVisual("d:/ymir work/ui/pattern/winfo1.png")
			wikiButton.SetOverVisual("d:/ymir work/ui/pattern/winfo2.png")
			wikiButton.SetDownVisual("d:/ymir work/ui/pattern/winfo3.png")
			wikiButton.SetEvent(ui.__mem_func__(self.OpenWiki))
			wikiButton.Hide()

		closeButton.SetEvent(ui.__mem_func__(self.OnPressedCloseButton))
		closeButton.Show()

		if app.ENABLE_SHOW_TARGET_HP:
			hpInformation = ui.TextLine()
			hpInformation.SetParent(hpGauge)
			hpInformation.SetDefaultFontName()
			hpInformation.SetPosition(5, 5)
			hpInformation.SetOutline()
			hpInformation.Hide()

		self.addQueueText = ui.MakeTextLineNew(self, 130, 8, localeInfo.ADD_METIN_QUEUE.format("|Eothers/key_shift|e + |Eothers/key_rc|e"))
		self.addQueueText.SetHorizontalAlignCenter()
		self.addQueueText.SetVerticalAlignCenter()
		self.addQueueText.SetWindowHorizontalAlignCenter()
		self.addQueueText.SetWindowVerticalAlignCenter()

		self.buttonDict = {}
		self.showingButtonList = []
		for buttonName in self.BUTTON_NAME_LIST:
			button = ui.Button()
			button.SetParent(self)

			button.SetUpVisual("lightwork/target/button_normal.tga")
			button.SetOverVisual("lightwork/target/button_hover.tga")
			button.SetDownVisual("lightwork/target/button_down.tga")

			button.SetWindowHorizontalAlignCenter()
			button.SetText(buttonName)
			button.Hide()
			self.buttonDict[buttonName] = button
			self.showingButtonList.append(button)

		self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER].SetEvent(ui.__mem_func__(self.OnWhisper))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE].SetEvent(ui.__mem_func__(self.OnExchange))
		self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_ACCEPT_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_AVENGE].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyInvite))
		self.buttonDict[localeInfo.TARGET_BUTTON_LEAVE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyExit))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCLUDE].SetEvent(ui.__mem_func__(self.OnPartyRemove))

		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_GUILD].SAFE_SetEvent(self.__OnGuildAddMember)
		self.buttonDict[localeInfo.TARGET_BUTTON_DISMOUNT].SAFE_SetEvent(self.__OnDismount)
		self.buttonDict[localeInfo.TARGET_BUTTON_EXIT_OBSERVER].SAFE_SetEvent(self.__OnExitObserver)
		self.buttonDict[localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT].SAFE_SetEvent(self.__OnViewEquipment)
		self.buttonDict[localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY].SAFE_SetEvent(self.__OnRequestParty)
		self.buttonDict[localeInfo.TARGET_BUTTON_BUILDING_DESTROY].SAFE_SetEvent(self.__OnDestroyBuilding)
		self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW].SAFE_SetEvent(self.__OnEmotionAllow)

		self.buttonDict["VOTE_BLOCK_CHAT"].SetEvent(ui.__mem_func__(self.__OnVoteBlockChat))

		self.name = name
		self.hpGauge = hpGauge
		if app.ENABLE_TARGET_INFORMATION_SYSTEM:
			self.infoButton = infoButton
			self.dropButton = dropButton
			self.settingsButton = settingsButton
			self.wikiButton = wikiButton
			self.vnum = 0
		if app.ENABLE_SHOW_TARGET_HP:
			self.hpInformation = hpInformation
		self.closeButton = closeButton
		self.nameString = 0
		self.nameLength = 0
		self.vid = 0
		self.eventWhisper = None
		self.isShowButton = False
		if app.ENABLE_ELEMENT_ADD:
			self.elementImage = None

		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.ClearToolTip()

		if app.ENABLE_SHOW_STROKE_INFO:
			self.strokeInfo = strokeInfo

		self.__Initialize()
		self.ResetTargetBoard()

		self.AddFlag("movable")


	def __del__(self):
		ui.ThinBoardNew.__del__(self)

	def BindInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def __Initialize(self):
		self.nameString = ""
		self.nameLength = 0
		self.vid = 0
		if app.ENABLE_TARGET_INFORMATION_SYSTEM:
			self.vnum = 0
		self.isShowButton = False

	def Destroy(self):
		self.eventWhisper = None
		self.closeButton = None
		if app.ENABLE_SHOW_STROKE_INFO:
			self.strokeInfo = None
		self.showingButtonList = None
		self.buttonDict = None
		self.name = None
		self.hpGauge = None

		if app.ENABLE_TARGET_INFORMATION_SYSTEM:
			if self.infoButton:
				self.infoButton.Hide()
				if self.infoButton.showWnd:
					self.infoButton.showWnd.Close()
				self.infoButton = None
			
			if self.dropButton:
				self.dropButton.Hide()
				self.dropButton = None

			if self.settingsButton:
				self.settingsButton.Hide()
				self.settingsButton = None

			if self.wikiButton:
				self.wikiButton.Hide()
				self.wikiButton = None

			if self.addQueueText:
				self.addQueueText.Hide()
				del self.addQueueText

			if app.ENABLE_SHOW_TARGET_HP:
				self.hpInformation = None

		if app.ENABLE_ELEMENT_ADD:
			self.elementImage = None
		self.__Initialize()

	if app.ENABLE_TARGET_INFORMATION_SYSTEM:
		def RefreshMonsterInfoBoard(self):
			if not self.infoButton.showWnd.IsShow():
				return

			self.infoButton.showWnd.Refresh()

		def OnPressedInfoButton(self):
			raceNum = player.GetRaceByVID(player.GetTargetVID())
			if constInfo.MONSTER_INFO_DATA.has_key(raceNum):
				del constInfo.MONSTER_INFO_DATA[raceNum]
			
			net.SendTargetInfoLoad(player.GetTargetVID())
			if self.infoButton.showWnd.IsShow():
				self.infoButton.showWnd.Close()
				if not self.infoButton.showWnd.onlyDrops:
					self.infoButton.showWnd.Open(self, self.vnum, True)
			elif self.vnum != 0:
				self.infoButton.showWnd.Open(self, self.vnum, True)
		
		def OnPressedDropInfoButton(self):
			raceNum = player.GetRaceByVID(player.GetTargetVID())
			if constInfo.MONSTER_INFO_DATA.has_key(raceNum):
				del constInfo.MONSTER_INFO_DATA[raceNum]
			
			if self.infoButton.showWnd.IsShow():
				self.infoButton.showWnd.Close()
				if self.infoButton.showWnd.onlyDrops:
					self.infoButton.showWnd.Open(self, self.vnum, False)
			elif self.vnum != 0:
				self.infoButton.showWnd.Open(self, self.vnum, False)

		def OpenGameOptionWindow(self):
			if self.infoButton.showWnd.IsShow():
				self.infoButton.showWnd.Close()
			interface = constInfo.GetInterfaceInstance()
			if interface:
				interface.ToggleGameOptionWindow(True)

		def OpenWiki(self):
			raceNum = player.GetRaceByVID(player.GetTargetVID())
			if constInfo.GetInterfaceInstance().wndWiki:
				constInfo.GetInterfaceInstance().wndWiki.searchBossWithVnum(raceNum)

	def OnPressedCloseButton(self):
		player.ClearTarget()
		self.Close()

	def Close(self):
		self.__Initialize()
		if app.ENABLE_TARGET_INFORMATION_SYSTEM:
			self.infoButton.Hide()
			self.infoButton.showWnd.Close()
			
			self.dropButton.Hide()
			self.settingsButton.Hide()
			self.wikiButton.Hide()
			self.addQueueText.Hide()

		if self.toolTip:
			self.toolTip.Hide()

		if self.elementImage:
			self.elementImage.Hide()

		self.Hide()

	def Open(self, vid, name):
		if vid:
			if not constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
				if not player.IsSameEmpire(vid):
					self.Hide()
					return

			if vid != self.GetTargetVID():
				self.ResetTargetBoard()
				self.SetTargetVID(vid)
				self.SetTargetName(name)

			if player.IsMainCharacterIndex(vid):
				self.__ShowMainCharacterMenu()
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
				self.Hide()
			else:
				self.RefreshButton()
				self.Show()
		else:
			self.HideAllButton()
			self.__ShowButton(localeInfo.TARGET_BUTTON_WHISPER)
			self.__ShowButton("VOTE_BLOCK_CHAT")
			self.__ArrangeButtonPosition()
			self.SetTargetName(name)
			self.Show()

	def Refresh(self):
		if self.IsShow():
			if self.IsShowButton():
				self.RefreshButton()

	def RefreshByVID(self, vid):
		if vid == self.GetTargetVID():
			self.Refresh()

	def RefreshByName(self, name):
		if name == self.GetTargetName():
			self.Refresh()

	def __ShowMainCharacterMenu(self):
		canShow=0

		self.HideAllButton()

		if player.IsMountingHorse():
			self.__ShowButton(localeInfo.TARGET_BUTTON_DISMOUNT)
			canShow=1

		if player.IsObserverMode():
			self.__ShowButton(localeInfo.TARGET_BUTTON_EXIT_OBSERVER)
			canShow=1

		if canShow:
			self.__ArrangeButtonPosition()
			self.Show()
		else:
			self.Hide()

	def __ShowNameOnlyMenu(self):
		self.HideAllButton()

	def SetWhisperEvent(self, event):
		self.eventWhisper = event

	def UpdatePosition(self):
		self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2, 10)

	def ResetTargetBoard(self):

		for btn in self.buttonDict.values():
			btn.Hide()

		self.__Initialize()

		self.name.SetPosition(0, 13)
		self.name.SetHorizontalAlignCenter()
		self.name.SetWindowHorizontalAlignCenter()
		self.hpGauge.Hide()
		if app.ENABLE_TARGET_INFORMATION_SYSTEM:
			self.infoButton.Hide()
			self.infoButton.showWnd.Close()
			
			self.dropButton.Hide()
			self.settingsButton.Hide()
			self.wikiButton.Hide()
		if app.ENABLE_ELEMENT_ADD and self.elementImage:
			self.elementImage.Hide()
			self.elementImage = None

		if app.ENABLE_SHOW_TARGET_HP:
			self.hpInformation.Hide()

			self.addQueueText.Hide()

		if app.ENABLE_SHOW_STROKE_INFO:
			self.strokeInfo.Hide()

		self.SetSize(300, 40)

	def SetTargetVID(self, vid):
		self.vid = vid
		if app.ENABLE_TARGET_INFORMATION_SYSTEM:
			self.vnum = 0

	def SetEnemyVID(self, vid):
		self.SetTargetVID(vid)

		if app.ENABLE_TARGET_INFORMATION_SYSTEM:
			vnum = nonplayer.GetRaceNumByVID(vid)
		name = chr.GetNameByVID(vid)
		level = nonplayer.GetLevelByVID(vid)
		grade = nonplayer.GetGradeByVID(vid)

		nameFront = ""
		if -1 != level:
			nameFront += "Lv." + str(level) + " "
		if self.GRADE_NAME.has_key(grade):
			nameFront += "(" + self.GRADE_NAME[grade] + ") "

		if (chr.IsGameMaster(0)):
			self.SetTargetName(nameFront + name + " ({})".format(vnum))
		else:
			self.SetTargetName(nameFront + name)

		if app.ENABLE_TARGET_INFORMATION_SYSTEM:
			if vnum >= 101:
				(textWidth, textHeight) = self.name.GetTextSize()

				self.infoButton.SetPosition(textWidth + 28, 12)
				self.infoButton.SetWindowHorizontalAlignLeft()
				self.infoButton.Show()

				self.dropButton.SetPosition(textWidth + 48, 12)
				self.dropButton.SetWindowHorizontalAlignLeft()
				self.dropButton.Show()

				self.settingsButton.SetPosition(textWidth + 68, 12)
				self.settingsButton.SetWindowHorizontalAlignLeft()

				if nonplayer.IsMonsterStone(vnum):
					self.settingsButton.Show()
					self.wikiButton.SetPosition(textWidth + 88, 12)
					self.wikiButton.SetWindowHorizontalAlignLeft()
					self.addQueueText.Show()
					self.SetSize(300, 60)
					self.strokeInfo.SetPosition(10, 65)
				else:
					self.settingsButton.Hide()
					self.wikiButton.SetPosition(textWidth + 68, 12)
					self.wikiButton.SetWindowHorizontalAlignLeft()
					self.addQueueText.Hide()
					self.SetSize(300, 40)
					self.strokeInfo.SetPosition(10, 45)

				self.wikiButton.Show()

				self.vnum = vnum

		

	def GetTargetVID(self):
		return self.vid

	def GetTargetName(self):
		return self.nameString

	def SetTargetName(self, name):
		self.nameString = name
		self.nameLength = len(name)
		self.name.SetText(name)

	def SetHP(self, hpPercentage, hpTarget):
		if not self.hpGauge.IsShow():
			self.SetSize(250 + 7 * self.nameLength, self.GetHeight())
			self.name.SetPosition(23, 13)

			self.name.SetWindowHorizontalAlignLeft()
			self.name.SetHorizontalAlignLeft()
			self.hpGauge.Show()
			self.UpdatePosition()
			self.name.Show()

		if SAVED_POS[0] != 0 or SAVED_POS[1] != 0:
			self.SetPosition(*SAVED_POS)

		if app.ENABLE_SHOW_STROKE_INFO:
			self.GetStrokeByVid(self.GetTargetVID())

		if chr.GetInstanceType(self.GetTargetVID()) != chr.INSTANCE_TYPE_PLAYER:
			iMinHP = hpTarget
			iMaxHP = nonplayer.GetMonsterMaxHP(nonplayer.GetRaceNumByVID(self.GetTargetVID()))
			if iMaxHP == 0:
				return
			true_perc = long(iMinHP * 100) / long(iMaxHP) 
			
			self.hpInformation.SetText("{} / {} ({}%)".format(localeInfo.NumberToDecimal(iMinHP),\
													localeInfo.NumberToDecimal(iMaxHP),\
													true_perc)) # to do
			
			(textWidth, textHeight)=self.hpInformation.GetTextSize()
			self.hpInformation.SetPosition(130 / 2 - textWidth / 2, -15)
			
			self.hpInformation.Show()
			
			self.hpGauge.SetPercentage(true_perc, 100)

	def ShowDefaultButton(self):

		self.isShowButton = True
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW])
		for button in self.showingButtonList:
			button.Show()

	def HideAllButton(self):
		self.isShowButton = False
		for button in self.showingButtonList:
			button.Hide()
		self.showingButtonList = []

	def __ShowButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		self.buttonDict[name].Show()
		self.showingButtonList.append(self.buttonDict[name])

	def __HideButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		button = self.buttonDict[name]
		button.Hide()

		for btnInList in self.showingButtonList:
			if btnInList == button:
				self.showingButtonList.remove(button)
				break

	def OnWhisper(self):
		if None != self.eventWhisper:
			self.eventWhisper(self.nameString)

	def OnExchange(self):
		net.SendExchangeStartPacket(self.vid)

	def OnPVP(self):
		net.SendChatPacket("/pvp %d" % (self.vid))

	def OnAppendToMessenger(self):
		net.SendMessengerAddByVIDPacket(self.vid)

	def OnPartyInvite(self):
		net.SendPartyInvitePacket(self.vid)

	def OnPartyExit(self):
		net.SendPartyExitPacket()

	def OnPartyRemove(self):
		net.SendPartyRemovePacketVID(self.vid)

	def __OnGuildAddMember(self):
		net.SendGuildAddMemberPacket(self.vid)

	def __OnDismount(self):
		net.SendChatPacket("/unmount")

	def __OnExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __OnViewEquipment(self):
		net.SendChatPacket("/view_equip " + str(self.vid))

	def __OnRequestParty(self):
		net.SendChatPacket("/party_request " + str(self.vid))

	def __OnDestroyBuilding(self):
		net.SendChatPacket("/build d %d" % (self.vid))

	def __OnEmotionAllow(self):
		net.SendChatPacket("/emotion_allow %d" % (self.vid))

	def __OnVoteBlockChat(self):
		cmd = "/vote_block_chat %s" % (self.nameString)
		net.SendChatPacket(cmd)

	def OnPressEscapeKey(self):
		self.OnPressedCloseButton()
		return True

	def IsShowButton(self):
		return self.isShowButton

	def RefreshButton(self):

		self.HideAllButton()

		if chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
			#self.__ShowButton(localeInfo.TARGET_BUTTON_BUILDING_DESTROY)
			#self.__ArrangeButtonPosition()
			return

		if player.IsPVPInstance(self.vid) or player.IsObserverMode():
			# PVP_INFO_SIZE_BUG_FIX
			self.SetSize(200 + 7*self.nameLength, 40)
			self.UpdatePosition()
			# END_OF_PVP_INFO_SIZE_BUG_FIX
			return

		self.ShowDefaultButton()

		if guild.MainPlayerHasAuthority(guild.AUTH_ADD_MEMBER):
			if not guild.IsMemberByName(self.nameString):
				if 0 == chr.GetGuildID(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_GUILD)

		if not messenger.IsFriendByName(self.nameString):
			self.__ShowButton(localeInfo.TARGET_BUTTON_FRIEND)

		if player.IsPartyMember(self.vid):

			self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if player.IsPartyLeader(self.vid):
				self.__ShowButton(localeInfo.TARGET_BUTTON_LEAVE_PARTY)
			elif player.IsPartyLeader(player.GetMainCharacterIndex()):
				self.__ShowButton(localeInfo.TARGET_BUTTON_EXCLUDE)

		else:
			if player.IsPartyMember(player.GetMainCharacterIndex()):
				if player.IsPartyLeader(player.GetMainCharacterIndex()):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
			else:
				if chr.IsPartyMember(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY)
				else:
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)

			if player.IsRevengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_AVENGE)
			elif player.IsChallengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_ACCEPT_FIGHT)
			elif player.IsCantFightInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if not player.IsSameEmpire(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
				self.__HideButton(localeInfo.TARGET_BUTTON_FRIEND)
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

		distance = player.GetCharacterDistance(self.vid)
		if distance > self.EXCHANGE_LIMIT_RANGE:
			self.__HideButton(localeInfo.TARGET_BUTTON_EXCHANGE)
			self.__ArrangeButtonPosition()

		self.__ArrangeButtonPosition()

	def __ArrangeButtonPosition(self):
		showingButtonCount = len(self.showingButtonList)

		pos = (-(showingButtonCount / 2) * 96) + 5
		if 0 == showingButtonCount % 2:
			pos += 44

		for button in self.showingButtonList:
			button.SetPosition(pos, 33)
			pos += 96

		self.SetSize(showingButtonCount * 103 + 10, 65)
		self.UpdatePosition()

	def OnUpdate(self):
		global SAVED_POS
		if self.isShowButton:

			exchangeButton = self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE]
			distance = player.GetCharacterDistance(self.vid)

			if distance < 0:
				return

			if exchangeButton.IsShow():
				if distance > self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

			else:
				if distance < self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

		else:
			SAVED_POS = self.GetGlobalPosition()

	def OnMoveWindow(self, x, y):
		if self.infoButton:
			if self.infoButton.showWnd.IsShow():
				self.infoButton.showWnd.Close()

		if self.elementImage:
			self.elementImage.SetPosition(self.GetLocalPosition()[0] - 40, self.GetLocalPosition()[1])

	if app.ENABLE_ELEMENT_ADD:
		def SetElementImage(self, element, parent, xPos, yPos):
			if element in self.ELEMENT_IMG_PATH.keys():
				self.elementImage = ElementImage(element, path=self.ELEMENT_IMG_PATH, tooltip=self.toolTip)
				self.elementImage.SetParent(parent)
				self.elementImage.SetPosition(xPos - 40, yPos)
				self.elementImage.Show()

	if app.ENABLE_SHOW_STROKE_INFO:
		def RegisterStroke(self, targetVID):
			if targetVID in DICT_MOB_STROKE_INFO:
				DICT_MOB_STROKE_INFO[targetVID] += 1
			else:
				DICT_MOB_STROKE_INFO.update({targetVID : 1})

		def GetStrokeByVid(self, targetVID):
			if targetVID in DICT_MOB_STROKE_INFO:
				self.strokeInfo.SetText(localeInfo.TOTAL_ATTACK_COUNT.format(DICT_MOB_STROKE_INFO[targetVID]))
				self.strokeInfo.Show()

class ElementImage(ui.Window):

	ELEMENT_INFO_TOOLTIP = \
	{
		"element_tooltip" : {
			1 : localeInfo.TARGET_ELEMENT_ELEC, # RACE_FLAG_ATT_ELEC
			2 : localeInfo.TARGET_ELEMENT_FIRE, # RACE_FLAG_ATT_FIRE
			3 : localeInfo.TARGET_ELEMENT_ICE, # RACE_FLAG_ATT_ICE
			4 : localeInfo.TARGET_ELEMENT_WIND, # RACE_FLAG_ATT_WIND
			5 : localeInfo.TARGET_ELEMENT_EARTH, # RACE_FLAG_ATT_EARTH
			6 : localeInfo.TARGET_ELEMENT_DARK # RACE_FLAG_ATT_DARK
		},

		"element_attbonus" : {
			1 : localeInfo.TARGET_ATTBONUS_ELEC, # RACE_FLAG_ATT_ELEC
			2 : localeInfo.TARGET_ATTBONUS_FIRE, # RACE_FLAG_ATT_FIRE
			3 : localeInfo.TARGET_ATTBONUS_ICE, # RACE_FLAG_ATT_ICE
			4 : localeInfo.TARGET_ATTBONUS_WIND, # RACE_FLAG_ATT_WIND
			5 : localeInfo.TARGET_ATTBONUS_EARTH, # RACE_FLAG_ATT_EARTH
			6 : localeInfo.TARGET_ATTBONUS_DARK # RACE_FLAG_ATT_DARK
		},	
		"element_def" : {
			1 : localeInfo.TARGET_DEF_ELEC, # RACE_FLAG_ATT_ELEC
			2 : localeInfo.TARGET_DEF_FIRE, # RACE_FLAG_ATT_FIRE
			3 : localeInfo.TARGET_DEF_ICE, # RACE_FLAG_ATT_ICE
			4 : localeInfo.TARGET_DEF_WIND, # RACE_FLAG_ATT_WIND
			5 : localeInfo.TARGET_DEF_EARTH, # RACE_FLAG_ATT_EARTH
			6 : localeInfo.TARGET_DEF_DARK # RACE_FLAG_ATT_DARK
		}
	}

	def __init__(self, element, path, tooltip):
		ui.Window.__init__(self)
		self.element = element
		self.tooltip = tooltip

		self.SetPosition(-40, 0)
		self.SetWindowHorizontalAlignLeft()

		self.elementImg = ui.ExpandedImageBox()
		self.elementImg.SetParent(self)
		self.elementImg.LoadImage(path[element])
		self.elementImg.OnMouseOverIn = ui.__mem_func__(self.OnMouseOverIn)
		self.elementImg.OnMouseOverOut = ui.__mem_func__(self.OnMouseOverOut)
		self.elementImg.Show()
		self.SetSize(self.elementImg.GetWidth(), self.elementImg.GetHeight())

	def __del__(self):
		ui.Window.__del__(self)

	def OnMouseOverIn(self):
		if self.tooltip:
			self.tooltip.ClearToolTip()
			self.tooltip.AlignHorizonalCenter()
			self.tooltip.AutoAppendTextLine(localeInfo.TARGET_ELEMENT_INFO.format(self.ELEMENT_INFO_TOOLTIP["element_tooltip"].get(self.element, "Element not found!")))
			self.tooltip.AutoAppendTextLine(localeInfo.TARGET_ELEMENT_INFO2.format(self.ELEMENT_INFO_TOOLTIP["element_attbonus"].get(self.element, "Bonus not found!")))
			self.tooltip.AutoAppendTextLine(localeInfo.TARGET_ELEMENT_INFO3.format(self.ELEMENT_INFO_TOOLTIP["element_def"].get(self.element, "Bonus not found!")))
			self.tooltip.ResizeToolTip()
			self.tooltip.Show()

	def OnMouseOverOut(self):
		if self.tooltip:
			self.tooltip.Hide()
