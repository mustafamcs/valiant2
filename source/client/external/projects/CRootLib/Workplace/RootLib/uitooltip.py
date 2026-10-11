import dbg, player, item, grp, wndMgr, skill, shop, exchange, grpText, safebox, localeInfo, app, background, nonplayer, chr \
	, ui ,colorInfo, constInfo, systemSetting, uiScriptLocale, textwrap
if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import acce
if app.ENABLE_AURA_SYSTEM:
	import aura
if app.ENABLE_EXTENDED_BLEND_AFFECT:
	import blend_table

WARP_SCROLLS = [22011, 22000, 22010]

DESC_DEFAULT_MAX_COLS = 26
DESC_WESTERN_MAX_COLS = 35
DESC_WESTERN_MAX_WIDTH = 220

if app.ENABLE_NEW_PET_SYSTEM:
	def pointop(n):
		t = int(n)

		if t / 10 < 1:
			return "0."+n
		else:		
			return n[0:len(n)-1]+"."+n[len(n)-1:]

def chop(n):
	return round(n - 0.5, 1)

def SplitDescription(desc, limit):
	total_tokens = desc.split()
	line_tokens = []
	line_len = 0
	lines = []
	for token in total_tokens:
		if "|" in token:
			sep_pos = token.find("|")
			line_tokens.append(token[:sep_pos])

			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 1)
			line_tokens = [token[sep_pos+1:]]
		elif app.WJ_MULTI_TEXTLINE and "\\n" in token:
			sep_pos = token.find("\\n")
			line_tokens.append(token[:sep_pos])
		else:
			line_len += len(token)
			if len(line_tokens) + line_len > limit:
				lines.append(" ".join(line_tokens))
				line_len = len(token)
				line_tokens = [token]
			else:
				line_tokens.append(token)

	if line_tokens:
		lines.append(" ".join(line_tokens))

	return lines

def GET_AFFECT_STRING(affType, affValue):
	if 0 == affType:
		return None
	
	try:
		affectString = ItemToolTip.AFFECT_DICT[affType]
		if type(affectString) != str:
			return affectString(affValue)

		if affectString.find("%d") != -1:
			return affectString % affValue
		else:
			return affectString
	except KeyError:
		return "UNKNOWN_TYPE[%s] %s" % (affType, affValue)

class ToolTip(ui.ThinBoard):

	TOOL_TIP_WIDTH = 190
	TOOL_TIP_HEIGHT = 10

	TEXT_LINE_HEIGHT = 17

	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	PRICE_COLOR = 0xffFFB96D

	HIGH_PRICE_COLOR = SPECIAL_TITLE_COLOR
	MIDDLE_PRICE_COLOR = grp.GenerateColor(0.85, 0.85, 0.85, 1.0)
	LOW_PRICE_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

	ENABLE_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	DISABLE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

	NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	SPECIAL_POSITIVE_COLOR = grp.GenerateColor(0.6911, 0.8754, 0.7068, 1.0) #bonus 1-4
	SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0) #bonus 6-7
	SPECIAL_POSITIVE_COLOR5 = grp.GenerateColor(0.7824, 0.9004, 0.8024, 1.0) #bonus 5
	PRICE_INFO_COLOR = grp.GenerateColor(1.0, 0.88, 0.0, 1.0)
	if app.ENABLE_DS_SET_BONUS:
		TEXTLINE_2ND_COLOR_DEFAULT = grp.GenerateColor(1.0, 1.0, 0.6078, 1.0)
	if app.ENABLE_6TH_7TH_ATTR:
		ATTR_6TH_7TH_COLOR = -102

	CONDITION_COLOR = 0xffBEB47D
	CAN_LEVEL_UP_COLOR = 0xff8EC292
	CANNOT_LEVEL_UP_COLOR = DISABLE_COLOR
	NEED_SKILL_POINT_COLOR = 0xff9A9CDB
	TOOLTIP_STUFF_COLOR = 0xffABFFF6
	if app.ENABLE_BUY_WITH_ITEMS:
		SHOP_ITEM_COLOR = 0xff15d131
	CHANGELOOK_ITEMNAME_COLOR = 0xffBCE55C
	SINIRSIZ_COLOR = 0xffFFFF00
	if app.ENABLE_COLORFUL_DESCRIPTIONS:
		RED_COLOR = grp.GenerateColor(0,255,255, 1.0)
		BLUE_COLOR = grp.GenerateColor(0,0.75,1, 1.0)
		GREEN_COLOR = grp.GenerateColor(0.23,0.83,0.24, 1.0)
		YELLOW_COLOR = 0xffFFFF00
		ORANGE_COLOR = grp.GenerateColor(24,116,205, 1.0)
		PINK_COLOR = grp.GenerateColor(1.0,0.0,1.0, 1.0)
		PURPLE_COLOR = grp.GenerateColor(0.63,0.13,0.94, 1.0)

	if app.ENABLE_NEW_PET_SYSTEM:
		ITEM_BUFF_LEVEL_COLOR = 0xffffd300
		ITEM_BUFF_TYPE_COLOR = 0xfffc9c3a
		ITEM_BUFF_RATE_COLOR = 0xff40e0d0
		ITEM_BUFF_DURATION_COLOR = 0xffadff00
		ITEM_BUFF_USAGE_COLOR = 0xffffffff

	itemShopPreviewItems = [0 for x in xrange(5)]
	iShopWeapon, iShopArmor, iShopHair, iShopAcce, iShopAura = xrange(5)

	def __init__(self, width = TOOL_TIP_WIDTH, isPickable=False):
		ui.ThinBoard.__init__(self, "TOP_MOST")

		# if app.ENABLE_WINDOW_ANIMATION:
		# 	self.SetWindowAnimation()

		if not isPickable:
			self.AddFlag("not_pick")

		self.AddFlag("float")

		self.followFlag = True
		self.toolTipWidth = width

		self.xPos = -1
		self.yPos = -1

		if app.ENABLE_DS_SET_BONUS:
			self.window_type = player.INVENTORY

		self.defFontName = (localeInfo.GetDefaultFont() if app.ENABLE_FONT_SELECT else localeInfo.UI_DEF_FONT)
		self.ClearToolTip()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def ClearToolTip(self):
		self.toolTipHeight = 12
		self.childrenList = []

	def SetFollow(self, flag):
		self.followFlag = flag

	def SetDefaultFontName(self, fontName):
		self.defFontName = fontName

	def AppendSpace(self, size):
		self.toolTipHeight += size
		self.ResizeToolTip()

	def AddTooltipWidth(self, size):
		self.toolTipWidth += size
		self.ResizeToolTip()

	def SetThinBoardSize(self, width, height = 12):
		self.toolTipWidth = width 
		self.toolTipHeight = height

	def AppendHorizontalLine(self):

		for i in xrange(2):
			horizontalLine = ui.Line()
			horizontalLine.SetParent(self)
			horizontalLine.SetPosition(0, self.toolTipHeight + 3 + i)
			horizontalLine.SetWindowHorizontalAlignCenter()
			horizontalLine.SetSize(150, 0)
			horizontalLine.Show()

			if 0 == i:
				horizontalLine.SetColor(0xff555555)
			else:
				horizontalLine.SetColor(0xff000000)

			self.childrenList.append(horizontalLine)

		self.toolTipHeight += 11
		self.ResizeToolTip()

	def AlignHorizonalCenter(self):
		for child in self.childrenList:
			(x, y)=child.GetLocalPosition()
			child.SetPosition(self.toolTipWidth/2, y)

		self.ResizeToolTip()

	def AlignTextLineHorizonalCenter(self):
		for child in self.childrenList:
			if type(child).__name__ == "TextLine":
				(x, y) = child.GetLocalPosition()
				child.SetPosition(self.toolTipWidth / 2, y)

		self.ResizeToolTip()

	def AutoAppendTextLine(self, text, color = FONT_COLOR, centerAlign = True, showState = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		if showState:
			textLine.Show()

		self.childrenList.append(textLine)

		(textWidth, textHeight)=textLine.GetTextSize()

		textWidth += 40
		textHeight += 5

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.toolTipHeight += textHeight

		return textLine

	def AutoAppendNewTextLineResize(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()
 
		(textWidth, textHeight) = textLine.GetTextSize()
		textWidth += 30
		textHeight += 10
		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth
 
		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)
 
		self.childrenList.append(textLine)
 
		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.AlignHorizonalCenter()
		return textLine

	if app.ENABLE_OFFICAL_CHARACTER_SCREEN:
		def SetThinBoardSize(self, width, height = 12) :#new select
			self.toolTipWidth = width
			self.toolTipHeight = height

		def ResizeToolTipText(self, x, y):
			self.SetSize(x, y)

	def AutoAppendTextLineNew(self, text, lineCount = 6, charLimit = 30, stepSize = 15):
		wrapper = textwrap.TextWrapper(width=charLimit) 

		self.textLines = []
		for i in xrange(lineCount):
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight+stepSize*i) 
			textLine.SetHorizontalAlignCenter()
			textLine.SetOutline()
			textLine.Show()
			self.textLines.append(textLine)

		for i in xrange(lineCount):
			self.textLines[i].SetText("")

		wrapper = textwrap.TextWrapper(width=charLimit)

		wordList = wrapper.wrap(text=text) 
		curTextLine = 0

		for word in wordList:
			if curTextLine < lineCount:
				self.textLines[curTextLine].SetText(word)
				self.childrenList.append(self.textLines[curTextLine])

				(textWidth, textHeight)=self.textLines[curTextLine].GetTextSize()

				textWidth += 30
				textHeight += 5

				if self.toolTipWidth < textWidth:
					self.toolTipWidth = textWidth

				self.toolTipHeight += textHeight
				self.ResizeToolTip()

				curTextLine += 1
			else:
				break

		return self.textLines

	def AutoAppendTextLineItem(self, vnum):

		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()
		itemImage.SetPosition(150, 15)

		item.SelectItem(vnum)
		itemImage.LoadImage(item.GetIconImageFileName())

		self.ResizeToolTip()

		self.toolTipHeight += itemImage.GetHeight()
		self.childrenList.append(itemImage)
		self.AppendTextLine(item.GetItemName(), self.TITLE_COLOR)


	def AutoAppendTextLineImage(self, image):

		imgBox = ui.ImageBox()
		imgBox.SetParent(self)
		imgBox.SetWindowName("image")
		imgBox.LoadImage(image)
		imgBox.Show()
		imgBox.SetPosition(0, self.toolTipHeight)
		self.childrenList.append(imgBox)
		self.AlignHorizonalCenter()
		return imgBox

	def AutoAppendNewTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.Show()
		textLine.SetPosition(15, self.toolTipHeight)
		
		self.childrenList.append(textLine)
		(textWidth, textHeight) = textLine.GetTextSize()
		textWidth += 30
		textHeight += 10
		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth
		
		self.toolTipHeight += textHeight
		self.ResizeToolTipText(textWidth, self.toolTipHeight)
		return textLine

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True, height = 0):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		if app.WJ_MULTI_TEXTLINE:
			textLine.SetLineHeight(self.TEXT_LINE_HEIGHT)
		textLine.Show()

		if centerAlign:
			if height != 0:
				textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight + (height / 2))
			else:
				textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)
		
		if height == 0:
			if app.WJ_MULTI_TEXTLINE:
				lineCount = textLine.GetTextLineCount()
				if lineCount > 1:
					height += self.TEXT_LINE_HEIGHT * lineCount + 13
				else:
					height += self.TEXT_LINE_HEIGHT * lineCount
			else:
				height += self.TEXT_LINE_HEIGHT

		self.toolTipHeight += height
		self.ResizeToolTip()
		return textLine

	if app.ENABLE_DS_SET_BONUS:
		def AppendTwoColorTextLine(self, text, color, text2, color2 = TEXTLINE_2ND_COLOR_DEFAULT, centerAlign = True):
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetFontName(self.defFontName)
			textLine.SetPackedFontColor(color)
			textLine.SetText(text)
			textLine.SetOutline()
			textLine.SetFeather(False)
			textLine.Show()

			textLine2 = ui.TextLine()
			textLine2.SetParent(textLine)
			textLine2.SetFontName(self.defFontName)
			textLine2.SetPackedFontColor(color2)
			textLine2.SetText(text2)
			textLine2.SetOutline()
			textLine2.SetFeather(False)
			textLine2.Show()

			w, h = textLine.GetTextSize()
			w2, h2 = textLine2.GetTextSize()

			if centerAlign:
				textLine.SetPosition(self.toolTipWidth / 2 - w2 / 2, self.toolTipHeight)
				textLine.SetHorizontalAlignCenter()
				textLine2.SetPosition(w / 2, 0)
			else:
				textLine.SetPosition(10, self.toolTipHeight)

			self.childrenList.append(textLine)
			self.childrenList.append(textLine2)

			self.toolTipHeight += self.TEXT_LINE_HEIGHT
			self.ResizeToolTip()

			return textLine

	def AppendDescription(self, desc, limit, color = FONT_COLOR):
		if localeInfo.IsEUROPE():
			self.__AppendDescription_WesternLanguage(desc, color)
		else:
			self.__AppendDescription_EasternLanguage(desc, limit, color)

	def __AppendDescription_EasternLanguage(self, description, characterLimitation, color=FONT_COLOR):
		length = len(description)
		if 0 == length:
			return

		lineCount = grpText.GetSplitingTextLineCount(description, characterLimitation)
		for i in xrange(lineCount):
			if 0 == i:
				self.AppendSpace(5)
			self.AppendTextLine(grpText.GetSplitingTextLine(description, characterLimitation, i), color)

	def __AppendDescription_WesternLanguage(self, desc, color=FONT_COLOR):
		if not desc:
			return

		lines = SplitDescription(desc, DESC_WESTERN_MAX_COLS)
		if not lines:
			return

		self.AppendSpace(5)
		for line in lines:
			self.AppendTextLine(line, color)

	def ResizeToolTip(self):
		self.SetSize(self.toolTipWidth, self.TOOL_TIP_HEIGHT + self.toolTipHeight)

	def SetTitle(self, name):
		self.AppendTextLine(name, self.TITLE_COLOR)

	def GetLimitTextLineColor(self, curValue, limitValue):
		if curValue < limitValue:
			return self.DISABLE_COLOR

		return self.ENABLE_COLOR

	def GetChangeTextLineColor(self, value, isSpecial=False):
		if value > 0:
			if isSpecial:
				return self.SPECIAL_POSITIVE_COLOR
			else:
				return self.POSITIVE_COLOR

		if 0 == value:
			return self.NORMAL_COLOR

		return self.NEGATIVE_COLOR

	def SetToolTipPosition(self, x = -1, y = -1):
		self.xPos = x
		self.yPos = y

	def ShowToolTip(self):
		self.SetTop()
		self.Show()

		self.OnUpdate()

	def HideToolTip(self):
		self.Hide()
		constInfo.SELECTED_ITEM_VNUM[3] = False

	def OnUpdate(self):

		if not self.followFlag:
			return

		x = 0
		y = 0
		width = self.GetWidth()
		height = self.toolTipHeight

		if -1 == self.xPos and -1 == self.yPos:

			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseY < wndMgr.GetScreenHeight() - 300:
				y = mouseY + 40
			else:
				y = mouseY - height - 30

			x = mouseX - width/2

		else:

			x = self.xPos - width/2
			y = self.yPos - height

		x = max(x, 0)
		y = max(y, 0)
		x = min(x + width/2, wndMgr.GetScreenWidth() - width/2) - width/2
		y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

		parentWindow = self.GetParentProxy()
		if parentWindow:
			(gx, gy) = parentWindow.GetGlobalPosition()
			x -= gx
			y -= gy

		self.SetPosition(x, y)

		if player.GetItemIndex(item.EQUIPMENT_WEAPON):
			pass

class ItemToolTip(ToolTip):
	if app.ENABLE_TARGET_INFORMATION_SYSTEM:
		isStone = False
		isBook = False
		isBook2 = False

	CHARACTER_NAMES = (
		localeInfo.JOB_WARRIOR,
		localeInfo.JOB_ASSASSIN,
		localeInfo.JOB_SURA,
		localeInfo.JOB_SHAMAN,
	)
	# if app.ENABLE_WOLFMAN_CHARACTER:
		# CHARACTER_NAMES += (
			# localeInfo.JOB_WOLFMAN,
		# )

	if app.ENABLE_HIDE_TOOLTIP_EMOJI:
		CHARACTER_NAMES_IMAGE = (
			"|Eemoji/warrior_m|e",
			"|Eemoji/assassin_w|e",
			"|Eemoji/sura_m|e",
			"|Eemoji/shaman_w|e",
		)
		# if app.ENABLE_WOLFMAN_CHARACTER:
			# CHARACTER_NAMES_IMAGE += (
				# "|Eemoji/wolfman|e",
			# )

	CHARACTER_COUNT = len(CHARACTER_NAMES)
	WEAR_NAMES = (
		localeInfo.TOOLTIP_ARMOR,
		localeInfo.TOOLTIP_HELMET,
		localeInfo.TOOLTIP_SHOES,
		localeInfo.TOOLTIP_WRISTLET,
		localeInfo.TOOLTIP_WEAPON,
		localeInfo.TOOLTIP_NECK,
		localeInfo.TOOLTIP_EAR,
		localeInfo.TOOLTIP_UNIQUE,
		localeInfo.TOOLTIP_SHIELD,
		localeInfo.TOOLTIP_ARROW,
	)
	WEAR_COUNT = len(WEAR_NAMES)

	AFFECT_DICT = {
		item.APPLY_MAX_HP : localeInfo.TOOLTIP_MAX_HP,
		item.APPLY_MAX_SP : localeInfo.TOOLTIP_MAX_SP,
		item.APPLY_CON : localeInfo.TOOLTIP_CON,
		item.APPLY_INT : localeInfo.TOOLTIP_INT,
		item.APPLY_STR : localeInfo.TOOLTIP_STR,
		item.APPLY_DEX : localeInfo.TOOLTIP_DEX,
		item.APPLY_ATT_SPEED : localeInfo.TOOLTIP_ATT_SPEED,
		item.APPLY_MOV_SPEED : localeInfo.TOOLTIP_MOV_SPEED,
		item.APPLY_CAST_SPEED : localeInfo.TOOLTIP_CAST_SPEED,
		item.APPLY_HP_REGEN : localeInfo.TOOLTIP_HP_REGEN,
		item.APPLY_SP_REGEN : localeInfo.TOOLTIP_SP_REGEN,
		item.APPLY_POISON_PCT : localeInfo.TOOLTIP_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT : localeInfo.TOOLTIP_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT : localeInfo.TOOLTIP_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT : localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,

		item.APPLY_ATTBONUS_WARRIOR : localeInfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN : localeInfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA : localeInfo.TOOLTIP_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,

		item.APPLY_ATTBONUS_HUMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL : localeInfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO : localeInfo.TOOLTIP_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD : localeInfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL : localeInfo.TOOLTIP_APPLY_ATTBONUS_DEVIL,
		item.APPLY_STEAL_HP : localeInfo.TOOLTIP_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP : localeInfo.TOOLTIP_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT : localeInfo.TOOLTIP_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER : localeInfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK : localeInfo.TOOLTIP_APPLY_BLOCK,
		item.APPLY_DODGE : localeInfo.TOOLTIP_APPLY_DODGE,
		item.APPLY_RESIST_SWORD : localeInfo.TOOLTIP_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND : localeInfo.TOOLTIP_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER : localeInfo.TOOLTIP_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL : localeInfo.TOOLTIP_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN : localeInfo.TOOLTIP_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW : localeInfo.TOOLTIP_RESIST_BOW,
		item.APPLY_RESIST_FIRE : localeInfo.TOOLTIP_RESIST_FIRE,
		item.APPLY_RESIST_ELEC : localeInfo.TOOLTIP_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC : localeInfo.TOOLTIP_RESIST_MAGIC,
		item.APPLY_RESIST_WIND : localeInfo.TOOLTIP_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE : localeInfo.TOOLTIP_APPLY_REFLECT_MELEE,
		item.APPLY_REFLECT_CURSE : localeInfo.TOOLTIP_APPLY_REFLECT_CURSE,
		item.APPLY_POISON_REDUCE : localeInfo.TOOLTIP_APPLY_POISON_REDUCE,
		item.APPLY_KILL_SP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_SP_RECOVER,
		item.APPLY_EXP_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS : localeInfo.TOOLTIP_APPLY_ITEM_DROP_BONUS,
		item.APPLY_POTION_BONUS : localeInfo.TOOLTIP_APPLY_POTION_BONUS,
		item.APPLY_KILL_HP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_HP_RECOVER,
		item.APPLY_IMMUNE_STUN : localeInfo.TOOLTIP_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW : localeInfo.TOOLTIP_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL : localeInfo.TOOLTIP_APPLY_IMMUNE_FALL,
		item.APPLY_BOW_DISTANCE : localeInfo.TOOLTIP_BOW_DISTANCE,
		item.APPLY_DEF_GRADE_BONUS : localeInfo.TOOLTIP_DEF_GRADE,
		item.APPLY_ATT_GRADE_BONUS : localeInfo.TOOLTIP_ATT_GRADE,
		item.APPLY_MAGIC_ATT_GRADE : localeInfo.TOOLTIP_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE : localeInfo.TOOLTIP_MAGIC_DEF_GRADE,
		item.APPLY_MAX_STAMINA : localeInfo.TOOLTIP_MAX_STAMINA,
		item.APPLY_MALL_ATTBONUS : localeInfo.TOOLTIP_MALL_ATTBONUS,
		item.APPLY_MALL_DEFBONUS : localeInfo.TOOLTIP_MALL_DEFBONUS,
		item.APPLY_MALL_EXPBONUS : localeInfo.TOOLTIP_MALL_EXPBONUS,
		item.APPLY_MALL_ITEMBONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS,
		item.APPLY_MALL_GOLDBONUS : localeInfo.TOOLTIP_MALL_GOLDBONUS,
		item.APPLY_SKILL_DAMAGE_BONUS : localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS : localeInfo.TOOLTIP_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
		item.APPLY_RESIST_WARRIOR : localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR,
		item.APPLY_RESIST_ASSASSIN : localeInfo.TOOLTIP_APPLY_RESIST_ASSASSIN,
		item.APPLY_RESIST_SURA : localeInfo.TOOLTIP_APPLY_RESIST_SURA,
		item.APPLY_RESIST_SHAMAN : localeInfo.TOOLTIP_APPLY_RESIST_SHAMAN,
		item.APPLY_MAX_HP_PCT : localeInfo.TOOLTIP_APPLY_MAX_HP_PCT,
		item.APPLY_MAX_SP_PCT : localeInfo.TOOLTIP_APPLY_MAX_SP_PCT,
		item.APPLY_ENERGY : localeInfo.TOOLTIP_ENERGY,
		item.APPLY_COSTUME_ATTR_BONUS : localeInfo.TOOLTIP_COSTUME_ATTR_BONUS,

		item.APPLY_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE : localeInfo.TOOLTIP_RESIST_ICE,
		item.APPLY_RESIST_EARTH : localeInfo.TOOLTIP_RESIST_EARTH,
		item.APPLY_RESIST_DARK : localeInfo.TOOLTIP_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT : localeInfo.TOOLTIP_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT : localeInfo.TOOLTIP_ANTI_PENETRATE_PCT,
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DICT.update({
			item.APPLY_BLEEDING_PCT : localeInfo.TOOLTIP_APPLY_BLEEDING_PCT,
			item.APPLY_BLEEDING_REDUCE : localeInfo.TOOLTIP_APPLY_BLEEDING_REDUCE,
			item.APPLY_ATTBONUS_WOLFMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_WOLFMAN,
			item.APPLY_RESIST_CLAW : localeInfo.TOOLTIP_APPLY_RESIST_CLAW,
			item.APPLY_RESIST_WOLFMAN : localeInfo.TOOLTIP_APPLY_RESIST_WOLFMAN,
		})

	if app.ENABLE_MAGIC_REDUCTION_SYSTEM:
		AFFECT_DICT.update({
			item.APPLY_RESIST_MAGIC_REDUCTION : localeInfo.TOOLTIP_RESIST_MAGIC_REDUCTION,
		})

	if app.ENABLE_EXTRA_APPLY_BONUS:
		AFFECT_DICT.update({
			item.APPLY_ATTBONUS_STONE : localeInfo.TOOLTIP_ATTBONUS_STONE,
			item.APPLY_ATTBONUS_BOSS : localeInfo.TOOLTIP_ATTBONUS_BOSS,

			item.APPLY_ATTBONUS_PVM_STR : localeInfo.TOOLTIP_ATTBONUS_PVM_STR,
			item.APPLY_ATTBONUS_PVM_AVG : localeInfo.TOOLTIP_ATTBONUS_PVM_AVG,
			item.APPLY_ATTBONUS_PVM_BERSERKER : localeInfo.TOOLTIP_ATTBONUS_PVM_BERSERKER,

			item.APPLY_DEFBONUS_PVM : localeInfo.TOOLTIP_DEFBONUS_PVM,
			item.APPLY_ATTBONUS_PVP : localeInfo.TOOLTIP_ATTBONUS_PVP,
			item.APPLY_DEFBONUS_PVP : localeInfo.TOOLTIP_DEFBONUS_PVP,

			item.APPLY_ATTBONUS_FIRE : localeInfo.TOOLTIP_ATTBONUS_FIRE,
			item.APPLY_ATTBONUS_ICE : localeInfo.TOOLTIP_ATTBONUS_ICE,
			item.APPLY_ATTBONUS_WIND : localeInfo.TOOLTIP_ATTBONUS_WIND,
			item.APPLY_ATTBONUS_EARTH : localeInfo.TOOLTIP_ATTBONUS_EARTH,
			item.APPLY_ATTBONUS_DARK : localeInfo.TOOLTIP_ATTBONUS_DARK,
			item.APPLY_ATTBONUS_ELEC : localeInfo.TOOLTIP_ATTBONUS_ELEC,
			item.APPLY_ATTBONUS_ELEMENT : localeInfo.TOOLTIP_ATTBONUS_ELEMENT,
			item.APPLY_DEFBONUS_ELEMENT : localeInfo.TOOLTIP_DEFBONUS_ELEMENT,

		})

	ATTRIBUTE_NEED_WIDTH = {
		23 : 230,
		24 : 230,
		25 : 230,
		26 : 220,
		27 : 210,

		35 : 210,
		36 : 210,
		37 : 210,
		38 : 210,
		39 : 210,
		40 : 210,
		41 : 210,

		42 : 220,
		43 : 230,
		45 : 230,
	}

	ANTI_FLAG_DICT = {
		0 : item.ITEM_ANTIFLAG_WARRIOR,
		1 : item.ITEM_ANTIFLAG_ASSASSIN,
		2 : item.ITEM_ANTIFLAG_SURA,
		3 : item.ITEM_ANTIFLAG_SHAMAN,
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		ANTI_FLAG_DICT.update({
			4 : item.ITEM_ANTIFLAG_WOLFMAN,
		})

	POINT_DICT = {item.GetApplyPoint(affect): name for affect, name in AFFECT_DICT.items()}

	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

	def __init__(self, *args, **kwargs):
		ToolTip.__init__(self, *args, **kwargs)
		self.itemVnum = 0
		self.isShopItem = False
		self.isNamingScrollActive = False
		self.metinSlot = []

		if app.ENABLE_DS_SET_BONUS:
			self.interface = None

		self.bCannotUseItemForceSetDisableColor = True

	def __del__(self):
		ToolTip.__del__(self)
		self.metinSlot = None

	if app.ENABLE_DS_SET_BONUS:
		def BindInterface(self, interface):
			from _weakref import proxy
			self.interface = proxy(interface)

	def SetCannotUseItemForceSetDisableColor(self, enable):
		self.bCannotUseItemForceSetDisableColor = enable

	def CanEquip(self):
		if not item.IsEquipmentVID(self.itemVnum):
			return True

		race = player.GetRace()
		job = chr.RaceToJob(race)
		if not self.ANTI_FLAG_DICT.has_key(job):
			return False

		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return False

		sex = chr.RaceToSex(race)

		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return False

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			return False

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_LEVEL == limitType:
				if player.GetStatus(player.LEVEL) < limitValue:
					return False

		return True

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True, height = 0):
		# if not self.CanEquip() and self.bCannotUseItemForceSetDisableColor:
			# color = self.DISABLE_COLOR
		
		# if len(text) > 32:
			# newWidth = (len(text) - 48)

		self.ResizeToolTip()
		return ToolTip.AppendTextLine(self, text, color, centerAlign, height)

	def ClearToolTip(self):
		self.isShopItem = False
		self.toolTipWidth = self.TOOL_TIP_WIDTH
		ToolTip.ClearToolTip(self)

	if app.ENABLE_TARGET_INFORMATION_SYSTEM:
		def SetItemToolTipStone(self, itemVnum):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)

			itemDesc = item.GetItemDescription()
			attrSlot = 0
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			itemName = item.GetItemName()
			realName = itemName[:itemName.find("+")]
			self.SetTitle(realName + " +0 - +4")

	def SetInventoryItem(self, slotIndex, window_type = player.INVENTORY):
		if app.ENABLE_DS_SET_BONUS:
			self.window_type = window_type

		itemVnum = player.GetItemIndex(window_type, slotIndex)
		itemType = item.GetItemType()

		if 0 == itemVnum:
			return

		self.ClearToolTip()
		if shop.IsOpen():
			if not shop.IsPrivateShop():
				item.SelectItem(itemVnum)
				self.AppendSellingPrice(player.GetISellItemPrice(window_type, slotIndex))

		metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

		self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, window_type, slotIndex)

		self.yang_tickets = { # vnum - yang karsılıgı
			80003: 2500,
			80004: 5000,
			80005: 7500,
			80006: 10000,
			80008: 150000
		}

		getCurrentItemCount = player.GetItemCount(window_type, slotIndex)
		if itemVnum in self.yang_tickets.keys():
			self.AppendSpace(5)
			self.AppendTextLine("|Eothers/shopsearchyang|e - " + "{} Yang".format(localeInfo.NumberToDecimal(self.yang_tickets[itemVnum]*getCurrentItemCount)), colorInfo.BLEND_ATTRIBUTE)
			self.AppendSpace(3)

		if app.ENABLE_HIDE_TOOLTIP_EMOJI and systemSetting.GetEmojiStatus():
			# self.AppendHorizontalLine()
			self.AppendSpace(2)
			self.AppendTextLine(localeInfo.ITEM_TRANSACTIONS_FAST_ITEMS_TOOLTIP, centerAlign = False)
			self.AppendSpace(5)

			self.AppendTextLine(localeInfo.SHOP_SEARCH_SHORTCUT_SEARCH, centerAlign = False)
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.WIKI_SEARCH_SHORTCUT_SEARCH, centerAlign = False)
			self.AppendSpace(5)

			if self.interface:
				if self.interface.dlgExchange.IsShow():
					self.AppendTextLine(localeInfo.MOVE_ITEM_TO_EXCHANGE, centerAlign = False)
					self.AppendSpace(5)
				if app.ENABLE_CHECK_IF_SAFEBOX_OPEN and safebox.isOpen():
					self.AppendTextLine(localeInfo.MOVE_ITEM_TO_SAFEBOX, centerAlign = False)
					self.AppendSpace(5)

				if self.interface.wndInventory and self.interface.wndSpecialStorage:
					if self.interface.wndInventory.IsShow() and self.interface.wndSpecialStorage.IsShow():
						self.AppendTextLine(localeInfo.FAST_MOVE_ITEM_BETWEEN_INV, centerAlign = False)
						self.AppendSpace(5)

			if app.ENABLE_FAST_SKILL_BOOK_SYSTEM:
				if itemVnum in xrange(50400, 50500):
					self.AppendTextLine(localeInfo.FAST_SKILL_BOOK_SYSTEM_TOOLTIP, centerAlign = False)
					self.AppendSpace(5)

			if itemVnum in blend_table.BLEND_BASE_TIME and app.ENABLE_EXTENDED_BLEND_AFFECT:
				self.AppendTextLine(localeInfo.USE_CONSUMABLE_TOOLTIP, centerAlign = False)
				self.AppendSpace(5)

			item.SelectItem(itemVnum)
			if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
				if (getCurrentItemCount) > 1:
					self.AppendTextLine(localeInfo.FAST_OPEN_CHEST_TOOLTIP.format(min(getCurrentItemCount, constInfo.CHEST_OPEN_COUNT)), centerAlign= False)
					self.AppendSpace(5)

			self.ResizeToolTip()

	def SetShopItem(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		if app.ENABLE_ITEMSHOP:
			item.SelectItem(itemVnum)
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					metinSlot[2] = limitValue
				elif item.LIMIT_REAL_TIME == limitType or item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					#metinSlot[2] = app.GetGlobalTimeStamp()+limitValue
					metinSlot[2] = limitValue

		self.AddItemData(itemVnum, metinSlot, attrSlot)

		self.AppendHorizontalLine()

		if app.ENABLE_BUY_WITH_ITEMS:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.ITEM_PRICE_TITLE, self.GetPriceColor(price))
			priced = False
			if price > 0:
				self.AppendPrice(price)
				priced = True
			
			for i in xrange(shop.MAX_SHOP_PRICES):
				(vnum, count) = shop.GetBuyWithItem(slotIndex, i)
				if vnum > 0 and count > 0:
					if not priced:
						priced = True
					
					self.AppendPrice_WithItem(vnum, count)
			
			if not priced:
				self.AppendTextLine(localeInfo.FREE_ITEM, self.CHANGELOOK_ITEMNAME_COLOR)
		else:
			self.AppendPrice(price)

		self.AppendSpace(12)
		self.AppendTextLine(localeInfo.MULTIPLE_BUY_TOOLTIP, centerAlign = False)
		self.AppendSpace(5)

		self.ResizeToolTip()

	if app.ENABLE_BUY_WITH_ITEMS:
		def AppendPrice_WithItem(self, vnum, price):
			item.SelectItem(vnum)
			icon = item.GetIconImageFileName()
			iconImage = ui.ImageBox()
			iconImage.SetParent(self)
			iconImage.LoadImage(icon)
			height = iconImage.GetHeight()
			del iconImage
			haveCount = player.GetItemCountByVnum(vnum)

			#self.AppendSpace(height)

			if haveCount >= price:
				text = localeInfo.ITEM_IS_WORTH % (price, icon, item.GetItemName()) + " |cff59b35f({})".format(haveCount)
			else:
				text = localeInfo.ITEM_IS_WORTH % (price, icon, item.GetItemName()) + " |cffc97b7f({})".format(haveCount)

			color = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
			self.AppendTextLine(text, color, True, height)

	if app.ENABLE_AURA_SYSTEM:
		def SetAuraResultItem(self, slotIndex, window_type = player.INVENTORY):
			(itemVnum, MinAbs, MaxAbs) = aura.GetResultItem()
			if not itemVnum:
				return

			self.ClearToolTip()

			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_AURA:
				return

			absChance = float(MinAbs) / 10.0
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnum, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendLimitInformation()

			## ABSORPTION RATE
			self.AppendTextLine(localeInfo.AURA_LEVEL_STEP % (int(metinSlot[aura.LEVEL_SOCKET]), int(metinSlot[aura.LEVEL_SOCKET])), self.CONDITION_COLOR)
			self.AppendTextLine(localeInfo.AURA_DRAIN_PER % (absChance), self.CONDITION_COLOR)
			## END ABSOPRTION RATE

			itemAbsorbedVnum = int(metinSlot[aura.ABSORBED_SOCKET])
			if itemAbsorbedVnum:
				## ATTACK / DEFENCE
				item.SelectItem(itemAbsorbedVnum)
				if item.GetItemType() == item.ITEM_TYPE_WEAPON:
					if item.GetItemSubType() == item.WEAPON_FAN:
						self.__AppendMagicAttackInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendAttackPowerInfo(absChance)
					else:
						self.__AppendAttackPowerInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendMagicAttackInfo(absChance)
	
				elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
					defGrade = item.GetValue(1)
					defBonus = item.GetValue(5) * 2
					defGrade = self.CalcAcceValue(defGrade, absChance)
					defBonus = self.CalcAcceValue(defBonus, absChance)
			
					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
			
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicDefenceInfo(absChance)
				## END ATTACK / DEFENCE
		
				## EFFECT
				item.SelectItem(itemAbsorbedVnum)
				for i in xrange(item.ITEM_APPLY_MAX_NUM):
					(affectType, affectValue) = item.GetAffect(i)
					affectValue = self.CalcAcceValue(affectValue, absChance)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString and affectValue > 0:
						self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
			
					item.SelectItem(itemAbsorbedVnum)
				# END EFFECT
		
			item.SelectItem(itemVnum)
			## ATTR
			self.__AppendAttributeInformation(attrSlot, MaxAbs)
			# END ATTR

			self.AppendWearableInformation()
			self.ShowToolTip()

		def SetAuraResultAbsItem(self, slotIndex1, slotIndex2, window_type = player.INVENTORY):
			itemVnumAura = player.GetItemIndex(window_type, slotIndex1)
			itemVnumTarget = player.GetItemIndex(window_type, slotIndex2)
			if not itemVnumAura or not itemVnumTarget:
				return

			self.ClearToolTip()

			item.SelectItem(itemVnumAura)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_AURA:
				return

			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex1, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex2, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnumAura, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			item.SelectItem(itemVnumAura)
			self.__AppendLimitInformation()

			absChance = float(metinSlot[aura.ABSORPTION_SOCKET]) / 10.0

			## ABSORPTION RATE
			self.AppendTextLine(localeInfo.AURA_LEVEL_STEP % (int(metinSlot[aura.LEVEL_SOCKET]), int(metinSlot[aura.LEVEL_SOCKET])), self.CONDITION_COLOR)
			self.AppendTextLine(localeInfo.AURA_DRAIN_PER % (absChance), self.CONDITION_COLOR)
			## END ABSOPRTION RATE

			## ATTACK / DEFENCE
			itemAbsorbedVnum = itemVnumTarget
			item.SelectItem(itemAbsorbedVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON:
				if item.GetItemSubType() == item.WEAPON_FAN:
					self.__AppendMagicAttackInfo(absChance)
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendAttackPowerInfo(absChance)
				else:
					self.__AppendAttackPowerInfo(absChance)
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicAttackInfo(absChance)
			elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
				defGrade = item.GetValue(1)
				defBonus = item.GetValue(5) * 2
				defGrade = self.CalcAcceValue(defGrade, absChance)
				defBonus = self.CalcAcceValue(defBonus, absChance)
		
				if defGrade > 0:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
		
				item.SelectItem(itemAbsorbedVnum)
				self.__AppendMagicDefenceInfo(absChance)
			## END ATTACK / DEFENCE

			## EFFECT
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectValue = self.CalcAcceValue(affectValue, absChance)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString and affectValue > 0:
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
		
				item.SelectItem(itemAbsorbedVnum)
			## END EFFECT

			## ATTR
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if not value:
					continue
		
				value = self.CalcAcceValue(value, absChance)
				affectString = self.__GetAffectString(type, value)
				if affectString and value > 0:
					affectColor = self.__GetAttributeColor(i, value)
					self.AppendTextLine(affectString, affectColor)
		
				item.SelectItem(itemAbsorbedVnum)
			## END ATTR

			## WEARABLE
			item.SelectItem(itemVnumAura)
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

			item.SelectItem(itemVnumAura)
			flagList = (
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN)
			)
			# flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)

			characterNames = ""
			for i in xrange(self.CHARACTER_COUNT):
				name = self.CHARACTER_NAMES[i]
				flag = flagList[i]
				if flag:
					characterNames += " "
					characterNames += name

			textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
			textLine.SetFeather()

			item.SelectItem(itemVnumAura)
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			## END WEARABLE

			self.ShowToolTip()
		

	def SetShopItemBySecondaryCoin(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot)
		self.AppendPriceBySecondaryCoin(price)

	def SetExchangeOwnerItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromSelf(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromSelf(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromSelf(slotIndex, i))
		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetExchangeTargetItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromTarget(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromTarget(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromTarget(slotIndex, i))
		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetPrivateShopBuilderItem(self, invenType, invenPos, privateShopSlotIndex):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()
		self.AppendSellingPrice(shop.GetPrivateShopItemPrice(invenType, invenPos))

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetSafeBoxItem(self, slotIndex):
		itemVnum = safebox.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetItemAttribute(slotIndex, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex))

	def SetMallItem(self, slotIndex):
		itemVnum = safebox.GetMallItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetMallItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetMallItemAttribute(slotIndex, i))

		if app.ENABLE_ITEMSHOP:
			item.SelectItem(itemVnum)
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					metinSlot[0] = limitValue
				elif item.LIMIT_REAL_TIME == limitType or item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					metinSlot[0] = app.GetGlobalTimeStamp()+limitValue

		self.AddItemData(itemVnum, metinSlot, attrSlot)

	if app.ENABLE_WIKI:
		def SetItemToolTipWiki(self, itemVnum):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)
			metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [(0,0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					metinSlot[0] = limitValue
				elif item.LIMIT_REAL_TIME == limitType or item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					metinSlot[0] = app.GetGlobalTimeStamp()+limitValue
			self.SetTitle(item.GetItemName())
			self.AppendDescription(item.GetItemDescription(), 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.AppendWearableInformation()
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					if metinSlot[0] > 0:
						self.AppendMallItemLastTime(metinSlot[0])
					break
			self.ShowToolTip()

	def SetItemToolTip(self, itemVnum):
		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))

		if app.ENABLE_ITEMSHOP:
			item.SelectItem(itemVnum)
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					metinSlot[0] = limitValue
				elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					metinSlot[0] = limitValue
				elif item.LIMIT_REAL_TIME == limitType:
					metinSlot[0] = app.GetGlobalTimeStamp()+limitValue

		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def __AppendAttackSpeedInfo(self, item):
		atkSpd = item.GetValue(0)

		if atkSpd < 80:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_FAST
		elif atkSpd <= 95:
			stSpd = localeInfo.TOOLTIP_ITEM_FAST
		elif atkSpd <= 105:
			stSpd = localeInfo.TOOLTIP_ITEM_NORMAL
		elif atkSpd <= 120:
			stSpd = localeInfo.TOOLTIP_ITEM_SLOW
		else:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_SLOW

		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_SPEED % stSpd, self.NORMAL_COLOR)

	def __AppendAttackGradeInfo(self):
		atkGrade = item.GetValue(1)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_GRADE % atkGrade, self.GetChangeTextLineColor(atkGrade))

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def CalcAcceValue(self, value, abs):
			if not value:
				return 0

			valueCalc 	= round(value * abs) / 100
			valueCalc 	-= 0.5
			valueCalc 	= int(valueCalc) +1 if valueCalc > 0 else int(valueCalc)
			value 		= 1 if (valueCalc <= 0 and value > 0) else valueCalc
			return value

	def __AppendAttackPowerInfo(self, itemAbsChance = 0):
		minPower = item.GetValue(3)
		maxPower = item.GetValue(4)
		addPower = item.GetValue(5)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if itemAbsChance != 0:
				minPower = self.CalcAcceValue(minPower, itemAbsChance)
				maxPower = self.CalcAcceValue(maxPower, itemAbsChance)
				addPower = self.CalcAcceValue(addPower, itemAbsChance)

		if maxPower > minPower:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower), self.POSITIVE_COLOR)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % (minPower+addPower), self.POSITIVE_COLOR)

	def __AppendMagicAttackInfo(self, itemAbsChance = 0):
		minMagicAttackPower = item.GetValue(1)
		maxMagicAttackPower = item.GetValue(2)
		addPower 			= item.GetValue(5)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if itemAbsChance != 0:
				minMagicAttackPower = self.CalcAcceValue(minMagicAttackPower, itemAbsChance)
				maxMagicAttackPower = self.CalcAcceValue(maxMagicAttackPower, itemAbsChance)
				addPower 			= self.CalcAcceValue(addPower, itemAbsChance)

		if minMagicAttackPower > 0 or maxMagicAttackPower > 0:
			if maxMagicAttackPower > minMagicAttackPower:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (minMagicAttackPower+addPower, maxMagicAttackPower+addPower), self.POSITIVE_COLOR)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % (minMagicAttackPower+addPower), self.POSITIVE_COLOR)

	def __AppendMagicDefenceInfo(self, itemAbsChance = 0):
		magicDefencePower = item.GetValue(0)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if itemAbsChance != 0:
				magicDefencePower = self.CalcAcceValue(magicDefencePower, itemAbsChance)

		if magicDefencePower > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_DEF_POWER % magicDefencePower, self.GetChangeTextLineColor(magicDefencePower))


	def __AppendAttributeInformation(self, attrSlot, itemAbsChance = 0):
		if 0 != attrSlot:
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]

				if 0 == value:
					continue

				affectString = self.__GetAffectString(type, value)
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					if item.GetItemType() == item.ITEM_TYPE_COSTUME:
						if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
							if itemAbsChance != 0:
								value = self.CalcAcceValue(value, itemAbsChance)
								affectString = self.__GetAffectString(type, value)

				if app.ENABLE_AURA_SYSTEM:
					if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_AURA and itemAbsChance:
						value = self.CalcAcceValue(value, itemAbsChance)
						affectString = self.__GetAffectString(type, value)

				if affectString:
					affectColor = self.__GetAttributeColor(i, value)
					self.AppendTextLine(affectString, affectColor)

	if app.ENABLE_DS_SET_BONUS:
		def __AppendDragonSoulAttributeInformation(self, attrSlot, dsType = 0, grade = 0):
			if 0 != attrSlot:
				if grade != 0:
					setWeightValue = item.GetDSSetWeight(dsType, grade)
					basicApplyCount = item.GetDSBasicApplyCount(dsType, grade)
					
					for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
						type = attrSlot[i][0]
						value = attrSlot[i][1]
						if 0 == value:
							continue
						
						affectString = self.__GetAffectString(type, value)
						if affectString:
							affectColor = self.__GetAttributeColor(i, value)
							
							setValue = 0
							if i < basicApplyCount:
								setValue = item.GetDSBasicApplyValue(dsType, type)
							else:
								setValue = item.GetDSAdditionalApplyValue(dsType, type)
							
							if setValue != 0:
								setValue = (setValue * setWeightValue - 1)/100 + 1
								if affectString.find('%') == -1:
									self.AppendTwoColorTextLine(affectString, affectColor, " (+%d)" % (setValue))
								else:
									self.AppendTwoColorTextLine(affectString, affectColor, " (+%d%%)" % (setValue))
							else:
								self.AppendTextLine(affectString, affectColor)
				else:
					for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
						type = attrSlot[i][0]
						value = attrSlot[i][1]
						if 0 == value:
							continue
						
						affectString = self.__GetAffectString(type, value)
						if affectString:
							affectColor = self.__GetAttributeColor(i, value)
							self.AppendTextLine(affectString, affectColor)

	def __GetAttributeColor(self, index, value):
		if value > 0:
			if index >= player.ATTRIBUTE_SLOT_RARE_START and index < player.ATTRIBUTE_SLOT_RARE_END:
				if app.ENABLE_6TH_7TH_ATTR:
					return self.ATTR_6TH_7TH_COLOR
				else:
					return self.SPECIAL_POSITIVE_COLOR2
			else:
				if index == player.ATTRIBUTE_SLOT_NORM_END:
					return self.SPECIAL_POSITIVE_COLOR5
				else:
					return self.SPECIAL_POSITIVE_COLOR

		elif value == 0:
			return self.NORMAL_COLOR
		else:
			return self.NEGATIVE_COLOR

	def __IsPolymorphItem(self, itemVnum):
		if itemVnum >= 70103 and itemVnum <= 70107:
			return 1
		return 0

	if app.ENABLE_6TH_7TH_ATTR:
		def AppendAttribute6th7thPossibility(self, attrSlot):
			if attrSlot == 0:
				return

			count = 0
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]

				if 0 == type or 0 == value:
					continue

				count += 1

			if (5 <= count <= 6):
				self.AppendTextLine(localeInfo.ATTR_6TH_7TH_POSSIBILITY, self.ATTR_6TH_7TH_COLOR)


	def __SetPolymorphItemTitle(self, monsterVnum):
		itemName =nonplayer.GetMonsterName(monsterVnum)
		itemName+=" "
		itemName+=item.GetItemName()
		self.SetTitle(itemName)

	def __CheckAntiFlag(self):
		race = player.GetRace()
		job = chr.RaceToJob(race)
		
		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return True
		else:
			return False

	def __CheckSex(self):
		sex = chr.RaceToSex(player.GetRace())
		MALE = 1
		FEMALE = 0
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return True
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == MALE:
			return False

	def __SetNormalItemTitle(self, itemVnum):
		if self.__CheckAntiFlag() == True:
			self.AppendTextLine(item.GetItemName(), self.DISABLE_COLOR)
		else:
			if self.__CheckSex() == True:
				self.AppendTextLine(item.GetItemName(), self.DISABLE_COLOR)
			else:
				if constInfo.SHOW_COUNT_TYPE_LIST(itemVnum):
					self.AppendTextLine(item.GetItemName() + " (%d)" % player.GetItemCountByVnum(itemVnum), self.TITLE_COLOR)
				else:
					self.AppendTextLine(item.GetItemName(), self.TITLE_COLOR)

	def __SetSpecialItemTitle(self, itemVnum):
		if self.__CheckAntiFlag() == True:
			self.AppendTextLine(item.GetItemName(), self.DISABLE_COLOR)
		else:
			if self.__CheckSex() == True:
				self.AppendTextLine(item.GetItemName(), self.DISABLE_COLOR)
			else:
				if constInfo.SHOW_COUNT_TYPE_LIST(itemVnum):
					self.AppendTextLine(item.GetItemName() + " (%d)" % player.GetItemCountByVnum(itemVnum), self.SPECIAL_TITLE_COLOR)
				else:
					self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)


	def __SetItemTitle(self, itemVnum, metinSlot, attrSlot):

		if self.__IsPolymorphItem(itemVnum):
			self.__SetPolymorphItemTitle(metinSlot[0])
		else:
			if self.__IsAttr(attrSlot):
				self.__SetSpecialItemTitle(itemVnum)
				return

			self.__SetNormalItemTitle(itemVnum)

	def __IsAttr(self, attrSlot):
		if not attrSlot:
			return False

		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			if 0 != type:
				return True

		return False

	if app.ENABLE_OFFLINE_SHOP:
		def AddRightClickForSale(self):
			self.AppendSpace(3)
			self.AppendTextLine(localeInfo.OFFLINESHOP_TOOLTIP_RIGHT_CLICK_FOR_SALE, centerAlign = False)
			self.AppendSpace(3)
			self.AppendTextLine(localeInfo.OFFLINESHOP_TOOLTIP_RIGHT_CLICK_FOR_SALE2, centerAlign = False)

	def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0):
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
				metinSlot[i]=player.METIN_SOCKET_TYPE_SILVER

		self.AddItemData(itemVnum, metinSlot, attrSlot, isRefine=True)

	def AddItemData_Offline(self, itemVnum, itemDesc, itemSummary, metinSlot, attrSlot):
		self.__AdjustMaxWidth(attrSlot, itemDesc)
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

	def AddItemData(self, itemVnum, metinSlot, attrSlot = 0, flags = 0, unbindTime = 0, window_type = player.INVENTORY, slotIndex = -1, isRefine = False):
		self.itemVnum = itemVnum
		self.metinSlot = metinSlot
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()

		if not item.GetItemDescription():
			self.__CalculateToolTipWidth(isRefine)

		if 50026 == itemVnum:
			if 0 != metinSlot:
				name = item.GetItemName()
				if metinSlot[0] > 0:
					name += " "
					name += localeInfo.NumberToMoneyString(metinSlot[0])
			self.SetTitle(name)
			self.ShowToolTip()
			return

		### Skill Book ###
		elif 50300 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
			self.ShowToolTip()
			return
		elif 70037 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
			self.AppendDescription(item.GetItemDescription(), 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.ShowToolTip()
			return
		elif 70055 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
			self.AppendDescription(item.GetItemDescription(), 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)

		if player.GetItemIndex(window_type, slotIndex) != 0:
			constInfo.SELECTED_ITEM_VNUM = [player.GetItemIndex(window_type, slotIndex), window_type, slotIndex, True]
		else:
			constInfo.SELECTED_ITEM_VNUM = [itemVnum, -1, -1, True]

		self.ShowToolTip()
		###########################################################################################

		itemDesc = item.GetItemDescription()
		itemSummary = item.GetItemSummary()
		if app.ENABLE_COLORFUL_DESCRIPTIONS:
			itemRed = item.GetItemRed()
			itemBlue = item.GetItemBlue()
			itemGreen = item.GetItemGreen()
			itemYellow = item.GetItemYellow()
			itePurpleange = item.GetItePurpleange()
			itemPink = item.GetItemPink()
			itemPurple = item.GetItemPurple()

		isCostumeItem = 0
		isCostumeHair = 0
		isCostumeBody = 0
		if app.ENABLE_MOUNT_COSTUME_SYSTEM:
			isCostumeMount = 0
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			isCostumeAcce = 0
		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			isCostumeWeapon = 0
		if app.ENABLE_AURA_SYSTEM:
			isCostumeAura = 0
		# if app.ENABLE_ACCE_COSTUME_SKIN:
		isAcceCostume = 0

		if app.ENABLE_COSTUME_SYSTEM:
			if item.ITEM_TYPE_COSTUME == itemType:
				isCostumeItem = 1
				isCostumeHair = item.COSTUME_TYPE_HAIR == itemSubType
				isCostumeBody = item.COSTUME_TYPE_BODY == itemSubType
				if app.ENABLE_MOUNT_COSTUME_SYSTEM:
					isCostumeMount = item.COSTUME_TYPE_MOUNT == itemSubType
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					isCostumeAcce = item.COSTUME_TYPE_ACCE == itemSubType
				if app.ENABLE_WEAPON_COSTUME_SYSTEM:
					isCostumeWeapon = item.COSTUME_TYPE_WEAPON == itemSubType
				if app.ENABLE_AURA_SYSTEM:
					isCostumeAura = item.COSTUME_TYPE_AURA == itemSubType
				# if app.ENABLE_ACCE_COSTUME_SKIN:
					isAcceCostume = item.COSTUME_TYPE_WING == itemSubType


				#dbg.TraceError("IS_COSTUME_ITEM! body(%d) hair(%d)" % (isCostumeBody, isCostumeHair))

		self.__AdjustMaxWidth(attrSlot, itemDesc)

		if chr.IsGameMaster(0):
			self.AppendTextLine("Vnum: (%d), Type: (%d), SubType: (%d)" % (itemVnum, itemType, itemSubType), self.TOOLTIP_STUFF_COLOR)
			self.AppendSpace(5)

		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		### Hair Preview Image ###
		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)
		if app.ENABLE_COLORFUL_DESCRIPTIONS:
			self.AppendDescription(itemRed, 26, self.RED_COLOR)
			self.AppendDescription(itemBlue, 26, self.BLUE_COLOR)
			self.AppendDescription(itemGreen, 26, self.GREEN_COLOR)
			self.AppendDescription(itemYellow, 26, self.YELLOW_COLOR)
			self.AppendDescription(itePurpleange, 26, self.ORANGE_COLOR)
			self.AppendDescription(itemPink, 26, self.PINK_COLOR)
			self.AppendDescription(itemPurple, 26, self.PURPLE_COLOR)

		if app.ENABLE_NEW_PET_SYSTEM:
			self.AppendNewPetInformations(itemVnum, metinSlot, attrSlot)

		### Weapon ###
		if item.ITEM_TYPE_WEAPON == itemType:

			self.__AppendLimitInformation()

			self.AppendSpace(5)

			if item.WEAPON_FAN == itemSubType:
				self.__AppendMagicAttackInfo()
				self.__AppendAttackPowerInfo()

			else:
				self.__AppendAttackPowerInfo()
				self.__AppendMagicAttackInfo()

			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			if app.ENABLE_6TH_7TH_ATTR:
				self.AppendAttribute6th7thPossibility(attrSlot)

			self.AppendWearableInformation()
			self.__AppendMetinSlotInfo(metinSlot)

		### Armor ###
		elif item.ITEM_TYPE_ARMOR == itemType:
			self.__AppendLimitInformation()

			defGrade = item.GetValue(1)
			defBonus = item.GetValue(5)*2
			if defGrade > 0:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade+defBonus), self.GetChangeTextLineColor(defGrade))

			self.__AppendMagicDefenceInfo()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			if app.ENABLE_6TH_7TH_ATTR:
				self.AppendAttribute6th7thPossibility(attrSlot)

			self.AppendWearableInformation()

			if itemSubType in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemSubType))
			elif itemSubType == item.ARMOR_HEAD:
				self.__AppendAccessoryMetinSlotInfo(metinSlot, 24701)
			elif itemSubType == item.ARMOR_FOOTS:
				self.__AppendAccessoryMetinSlotInfo(metinSlot, 24707)
			elif itemSubType == item.ARMOR_SHIELD:
				self.__AppendAccessoryMetinSlotInfo(metinSlot, 24704)
			else:
				self.__AppendMetinSlotInfo(metinSlot)

		### Ring Slot Item (Not UNIQUE) ###
		elif item.ITEM_TYPE_RING == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			#self.__AppendAccessoryMetinSlotInfo(metinSlot, 99001)


		### Belt Item ###
		elif item.ITEM_TYPE_BELT == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_BELT_MATERIAL_VNUM(itemVnum))

		elif 0 != isCostumeItem and not isCostumeMount:

			bHasRealtimeFlag = 0

			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			if app.ENABLE_ACCE_COSTUME_SYSTEM and isCostumeAcce and not isAcceCostume:
				## ABSORPTION RATE
				absChance = int(metinSlot[acce.ABSORPTION_SOCKET])
				self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE % (absChance), self.CONDITION_COLOR)
				## END ABSORPTION RATE

				itemAbsorbedVnum = int(metinSlot[acce.ABSORBED_SOCKET])
				if itemAbsorbedVnum:
					## ATTACK / DEFENSE
					item.SelectItem(itemAbsorbedVnum)
					if item.GetItemType() == item.ITEM_TYPE_WEAPON:
						if item.GetItemSubType() == item.WEAPON_FAN:
							self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])
							item.SelectItem(itemAbsorbedVnum)
							self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
						else:
							self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
							item.SelectItem(itemAbsorbedVnum)
							self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])

					elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
						defGrade = item.GetValue(1)
						defBonus = item.GetValue(5) * 2
						defGrade = self.CalcAcceValue(defGrade, metinSlot[acce.ABSORPTION_SOCKET])
						defBonus = self.CalcAcceValue(defBonus, metinSlot[acce.ABSORPTION_SOCKET])

						if defGrade > 0:
							self.AppendSpace(5)
							self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))

						item.SelectItem(itemAbsorbedVnum)
						self.__AppendMagicDefenceInfo(metinSlot[acce.ABSORPTION_SOCKET])
					## END ATTACK / DEFENSE

					## EFFECT
					item.SelectItem(itemAbsorbedVnum)
					for i in xrange(item.ITEM_APPLY_MAX_NUM):
						(affectType, affectValue) = item.GetAffect(i)
						affectValue = self.CalcAcceValue(affectValue, metinSlot[acce.ABSORPTION_SOCKET])
						affectString = self.__GetAffectString(affectType, affectValue)
						if (not app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue != 0)\
								or (app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue > 0):
							self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

						item.SelectItem(itemAbsorbedVnum)
					# END EFFECT

					item.SelectItem(itemVnum)
					## ATTR
					self.__AppendAttributeInformation(attrSlot, metinSlot[acce.ABSORPTION_SOCKET])
					# END ATTR
				else:
					# ATTR
					self.__AppendAttributeInformation(attrSlot)
					# END ATTR

			elif app.ENABLE_AURA_SYSTEM and (itemVnum >= 49001 and itemVnum <= 49006):
				## ABSORPTION RATE
				absChance = (float(metinSlot[aura.ABSORPTION_SOCKET]) / 10.0)
				self.AppendTextLine(localeInfo.AURA_LEVEL_STEP % (int(metinSlot[aura.LEVEL_SOCKET]), int(metinSlot[aura.LEVEL_SOCKET])), self.CONDITION_COLOR)
				self.AppendTextLine(localeInfo.AURA_DRAIN_PER % (absChance), self.CONDITION_COLOR)
				## END ABSOPRTION RATE
				itemAbsorbedVnum = int(metinSlot[aura.ABSORBED_SOCKET])
				if itemAbsorbedVnum:
					## ATTACK / DEFENCE
					item.SelectItem(itemAbsorbedVnum)
					if item.GetItemType() == item.ITEM_TYPE_WEAPON:
						if item.GetItemSubType() == item.WEAPON_FAN:
							self.__AppendMagicAttackInfo(absChance)
							item.SelectItem(itemAbsorbedVnum)
							self.__AppendAttackPowerInfo(absChance)
						else:
							self.__AppendAttackPowerInfo(absChance)
							item.SelectItem(itemAbsorbedVnum)
							self.__AppendMagicAttackInfo(absChance)
					elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
						defGrade = item.GetValue(1)
						defBonus = item.GetValue(5) * 2
						defGrade = self.CalcAcceValue(defGrade, absChance)
						defBonus = self.CalcAcceValue(defBonus, absChance)
						if defGrade > 0:
							self.AppendSpace(5)
							self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
				
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendMagicDefenceInfo(absChance)
					## END ATTACK / DEFENCE
			
					## EFFECT
					item.SelectItem(itemAbsorbedVnum)
					for i in xrange(item.ITEM_APPLY_MAX_NUM):
						(affectType, affectValue) = item.GetAffect(i)
						affectValue = self.CalcAcceValue(affectValue, absChance)
						affectString = self.__GetAffectString(affectType, affectValue)
						if affectString and affectValue > 0:
							self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
				
						item.SelectItem(itemAbsorbedVnum)
					# END EFFECT
			
					item.SelectItem(itemVnum)
					## ATTR
					self.__AppendAttributeInformation(attrSlot, absChance)
					# END ATTR
				else:
					# ATTR
					self.__AppendAttributeInformation(attrSlot)
					# END ATTR

			else:


				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if any((isCostumeHair, isCostumeBody, isCostumeWeapon)) and not bHasRealtimeFlag:
					self.AppendSpace(3)
					self.AppendTextLine(localeInfo.ITEM_BONUSSES, colorInfo.BLEND_ATTRIBUTE_DESC)
					self.AppendSpace(1)

					for i in xrange(5):
						attrType = attrSlot[i][0]
						attrvalue = attrSlot[i][1]
						affectString = self.__GetAffectString(attrType, attrvalue)
						if affectString:
							self.AppendTextLine(affectString, self.GetChangeTextLineColor(attrvalue, True))
						else:
							self.AppendTextLine(localeInfo.ITEM_HAS_NO_BONUS, self.DISABLE_COLOR)

				else:
					self.__AppendAttributeInformation(attrSlot)

			self.AppendWearableInformation()

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				self.AppendAbsorbedItemInfo(itemVnum, int(metinSlot[aura.ABSORBED_SOCKET]), attrSlot)

			if bHasRealtimeFlag:
				self.AppendMallItemLastTime(metinSlot[0])

		## Rod ##
		elif item.ITEM_TYPE_ROD == itemType:

			if itemVnum >= 27401 and itemVnum <= 27404:
				rodLevel = itemVnum % 27400 
				self.AppendTextLine(localeInfo.FISHING_BETTER_CHANCE + (" +{}%".format(int(rodLevel*5))), self.POSITIVE_COLOR)

			if 0 != metinSlot:
				# curLevel = item.GetValue(0) / 10
				# curEXP = metinSlot[0]
				# maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				# self.__AppendRodInformation(curLevel, curEXP, maxEXP)

		## Pick ##
		elif item.ITEM_TYPE_PICK == itemType:

			if app.ENABLE_MINING_RENEWAL:
				if itemVnum == 29101:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%10",self.POSITIVE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP+ " +%1", self.POSITIVE_COLOR)
					self.AppendTextLine(localeInfo.MINING_FRACTION_COUNT+ " 10-25", self.POSITIVE_COLOR)
				elif itemVnum == 29102:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%12",self.POSITIVE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP+ " +%5", self.POSITIVE_COLOR)
					self.AppendTextLine(localeInfo.MINING_FRACTION_COUNT+ " 25-40", self.POSITIVE_COLOR)
				elif itemVnum == 29103:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%14", self.POSITIVE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP+ " +%10", self.POSITIVE_COLOR)
					self.AppendTextLine(localeInfo.MINING_FRACTION_COUNT+ " 40-55", self.POSITIVE_COLOR)
				elif itemVnum == 29104:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%20", self.POSITIVE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP+ " +%20", self.POSITIVE_COLOR)
					self.AppendTextLine(localeInfo.MINING_FRACTION_COUNT+ " 55-75", self.POSITIVE_COLOR)

			# if 0 != metinSlot:
				# curLevel = item.GetValue(0) / 10
				# curEXP = metinSlot[0]
				# maxEXP = item.GetValue(2)
				# self.__AppendLimitInformation()
				# self.__AppendPickInformation(curLevel, curEXP, maxEXP)

		### Metin ###
		elif item.ITEM_TYPE_METIN == itemType:
			self.AppendMetinInformation()
			self.AppendMetinWearInformation()

		### Fish ###
		elif item.ITEM_TYPE_FISH == itemType:
			if 0 != metinSlot:
				self.__AppendFishInfo(metinSlot[0])

		elif item.ITEM_TYPE_GIFTBOX == itemType:
				self.__AppendLimitInformation()
			# if window_type in [player.INVENTORY, player.CHEST_INVENTORY] and app.ENABLE_HIDE_TOOLTIP_EMOJI and systemSetting.GetEmojiStatus():
			# 	self.AppendTextLine(localeInfo.GIFTBOX_VIEW_CHEST_DROP_TOOLTIP, centerAlign= False)
			# 	self.AppendSpace(5)
			# 	self.__AdjustMaxWidth(attrSlot, itemDesc)
			# 	if (player.GetItemCount(window_type, slotIndex)) > 1:
			# 		self.AppendSpace(5)
			# 		self.AppendTextLine(localeInfo.FAST_OPEN_CHEST_TOOLTIP.format(min(player.GetItemCount(window_type, slotIndex), constInfo.CHEST_OPEN_COUNT)), centerAlign= False)

		### UNIQUE) ###
		elif item.ITEM_TYPE_UNIQUE == itemType:
			# self.__AppendAffectInformation()
			# self.__AppendAttributeInformation(attrSlot)
			# self.AppendMallItemLastTime(metinSlot[0])


			self.__AppendLimitInformation()

			bHasRealtimeFlag = 0

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1

			if 1 == bHasRealtimeFlag:
				self.AppendMallItemLastTime(metinSlot[0])
			else:
				time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

				if 1 == item.GetValue(2):
					self.AppendMallItemLastTime(time)
				else:
					self.AppendUniqueItemLastTime(time)

		## item.ITEM_TYPE_BLEND
		elif item.ITEM_TYPE_BLEND == itemType:
			self.__AppendLimitInformation()

			if metinSlot:
				affectType = metinSlot[0]
				affectValue = metinSlot[1]
				time = metinSlot[2]
				status = metinSlot[3]

				if app.ENABLE_EXTENDED_BLEND_AFFECT:
					if blend_table.BLEND_BASE_TIME.has_key(itemVnum):
						isPerma = blend_table.BLEND_BASE_TIME[itemVnum]["perma"]
						if not isPerma:
							self.AutoAppendNewTextLineResize(localeInfo.DECS_DEW_TEST, colorInfo.BLEND_ATTRIBUTE_DESC)
							self.AutoAppendNewTextLineResize(localeInfo.DECS_DEW_TEST2, colorInfo.BLEND_ATTRIBUTE_DESC)
							self.AutoAppendNewTextLineResize(localeInfo.DECS_DEW_TEST3, colorInfo.BLEND_ATTRIBUTE_DESC)
	
				if app.ENABLE_EXTENDED_BLEND_AFFECT:
					affectText = self.AutoAppendNewTextLineResize(self.__GetAffectString(affectType, affectValue), colorInfo.BLEND_ATTRIBUTE)
				else:
					affectText = self.__GetAffectString(affectType, affectValue)

				self.AppendTextLine(affectText, self.NORMAL_COLOR)
				self.AppendSpace(-15)
				if app.ENABLE_EXTENDED_BLEND_AFFECT:

					if time > item.MIN_INFINITE_DURATION:
						self.AppendTextLine(localeInfo.INFINITE_USE, self.YELLOW_COLOR)
					else:
						if self.isShopItem:
							isPerma = blend_table.BLEND_BASE_TIME[itemVnum]["perma"]
							bonusID = blend_table.BLEND_BASE_TIME[itemVnum]["bonus_id"]
							bonusValue = blend_table.BLEND_BASE_TIME[itemVnum]["bonus_value"]
							self.AppendSpace(-10)
							self.AppendTextLine(self.__GetAffectString(bonusID, bonusValue[0]), self.POSITIVE_COLOR)
							if not isPerma:
								self.AppendTextLine(localeInfo.LEFT_TIME + ": " + localeInfo.SecondToDHM(1800), self.GREEN_COLOR)
							else:
								self.AppendTextLine(localeInfo.INFINITE_USE, self.GREEN_COLOR)
						else:
							if time > 0:
								endTime = app.GetGlobalTimeStamp() + time
								leftSec = max(0, endTime - app.GetGlobalTimeStamp())
								self.AppendTextLine(localeInfo.LEFT_TIME + ": " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)
							if status:
								self.AppendTextLine(localeInfo.BLEND_STATE, self.GREEN_COLOR)
							else:
								self.AppendTextLine(localeInfo.BLEND_STATE2, self.DISABLE_COLOR)

				else:
					if time > 0:
						minute = (time / 60)
						second = (time % 60)
						timeString = localeInfo.TOOLTIP_POTION_TIME

						if minute > 0:
							timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
						if second > 0:
							timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

						self.AppendTextLine(timeString)
					else:
						self.AppendTextLine(localeInfo.BLEND_POTION_NO_TIME)

			else:
				self.AppendTextLine("BLEND_POTION_NO_INFO")

		elif item.ITEM_TYPE_COSTUME == itemType and isCostumeMount:
			if player.CheckAffect(chr.NEW_AFFECT_NAMING_SCROLL_MOUNT, 0):
				self.__AppendAffectInformation(0)
			else:
				self.__AppendAffectInformation()

			self.__AppendAttributeInformation(attrSlot)

			bHasRealtimeFlag = 0

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1

			if 1 == bHasRealtimeFlag:
				self.AppendMallItemLastTime(metinSlot[0])
			else:
				time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

				if 1 == item.GetValue(2):
					self.AppendMallItemLastTime(time)
				else:
					self.AppendUniqueItemLastTime(time)

		# if app.ENABLE_PET_COSTUME_SYSTEM:
		elif item.ITEM_TYPE_PET == itemType: 
			if player.CheckAffect(chr.NEW_AFFECT_NAMING_SCROLL_PET, 0):
				self.__AppendAffectInformation(1)
			else:
				self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			bHasRealtimeFlag = 0

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1

			if 1 == bHasRealtimeFlag:
				self.AppendMallItemLastTime(metinSlot[0])
			else:
				time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

				if 1 == item.GetValue(2):
					self.AppendMallItemLastTime(time)
				else:
					self.AppendUniqueItemLastTime(time)

		# elif itemType in [item.ITEM_MOUNT_SKIN, item.ITEM_PET_SKIN, item.ITEM_BOOSTER, item.ITEM_RINGS, item.ITEM_PENDANT, item.ITEM_GLOVE, item.ENABLE_DREAMSOUL, item.ITEM_RINGS]:
		# elif itemType in [item.ITEM_MOUNT_SKIN, item.ITEM_PET_SKIN, item.ITEM_BOOSTER, item.ITEM_RINGS, item.ITEM_PENDANT, item.ITEM_GLOVE, item.ITEM_DREAMSOUL, item.ITEM_AURA_SKIN]:
		elif itemType in [item.ITEM_MOUNT_SKIN, item.ITEM_PET_SKIN, item.ITEM_RINGS, item.ITEM_PENDANT, item.ITEM_GLOVE, item.ITEM_DREAMSOUL, item.ITEM_AURA_SKIN]:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.AppendWearableInformation()
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])
			if itemType == item.ITEM_PENDANT:
				self.__AppendAccessoryMetinSlotInfo(metinSlot, 24713)
			elif itemType == item.ITEM_GLOVE:
				self.__AppendAccessoryMetinSlotInfo(metinSlot, 24716)

		elif itemType == item.ITEM_BOOSTER:

			boosterRate = constInfo.BOOSTER_ITEM_RATES[itemVnum][0]

			if boosterRate > 1:
				self.AppendSpace(3)
				# canGetSetBonus = hasWeapon and hasArmor and hasHelmet
				self.AppendTextLine(localeInfo.ITEM_BOOSTER_TOOLTIP3.format(boosterRate), self.HIGH_PRICE_COLOR)
				self.AppendSpace(2)
				self.AppendTextLine(localeInfo.ITEM_BOOSTER_TOOLTIP4.format(boosterRate), self.HIGH_PRICE_COLOR)
				hasWeapon = player.GetItemIndex(item.EQUIPMENT_WEAPON)
				hasArmor = player.GetItemIndex(item.EQUIPMENT_BODY)
				hasHelmet = player.GetItemIndex(item.EQUIPMENT_HEAD)

				hasBoosterWeapon = player.GetItemIndex(item.BOOSTER_SLOT_WEAPON)
				hasBoosterArmor = player.GetItemIndex(item.BOOSTER_SLOT_BODY)
				hasBoosterHair = player.GetItemIndex(item.BOOSTER_SLOT_HEAD)

				wearAllBooster = (hasBoosterWeapon and hasBoosterArmor and hasBoosterHair) 
				giveSetBonus = False

				if wearAllBooster:
					if constInfo.BOOSTER_ITEM_RATES[hasBoosterWeapon] == constInfo.BOOSTER_ITEM_RATES[hasBoosterArmor] and \
						constInfo.BOOSTER_ITEM_RATES[hasBoosterWeapon] == constInfo.BOOSTER_ITEM_RATES[hasBoosterHair]:
						giveSetBonus = True

				if giveSetBonus:
					self.AppendSpace(3)
					self.AppendTextLine(localeInfo.ITEM_BOOSTER_TOOLTIP6, self.GREEN_COLOR)
					# self.AppendSpace(-5)
					self.AppendTextLine(localeInfo.ITEM_BOOSTER_TOOLTIP7, self.GREEN_COLOR)
					boosterRate+= 5
				else:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.ITEM_BOOSTER_TOOLTIP5, self.DISABLE_COLOR)

				self.AppendSpace(3)
				self.AppendTextLine(localeInfo.ITEM_BOOSTER_TOOLTIP, self.BLUE_COLOR)
				self.AppendSpace(3)
				self.AppendTextLine(localeInfo.ITEM_BOOSTER_TOOLTIP2, self.BLUE_COLOR)

				if itemSubType == 0: # WEAPON
					if hasWeapon:
						item.SelectItem(hasWeapon)
						attrSlot = [player.GetItemAttribute(player.INVENTORY, item.EQUIPMENT_WEAPON, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

				elif itemSubType == 1: # ARMOR
					if hasArmor:
						item.SelectItem(hasArmor)
						attrSlot = [player.GetItemAttribute(player.INVENTORY, item.EQUIPMENT_BODY, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
				else:
					if hasHelmet:
						item.SelectItem(hasHelmet)
						attrSlot = [player.GetItemAttribute(player.INVENTORY, item.EQUIPMENT_HEAD, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

				self.AppendHorizontalLine()
				if item.GetItemType() == item.ITEM_TYPE_WEAPON:
					if item.GetItemSubType() == item.WEAPON_FAN:
						self.__AppendMagicAttackInfo(boosterRate)
						self.__AppendAttackPowerInfo(boosterRate)
					else:
						self.__AppendAttackPowerInfo(boosterRate)
						self.__AppendMagicAttackInfo(boosterRate)

				elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
					defGrade = item.GetValue(1)
					defBonus = item.GetValue(5) * 2

					if defGrade > 0:
						# self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (((defGrade + defBonus) * boosterRate)/100)), self.GetChangeTextLineColor(defGrade)
			
					self.__AppendMagicDefenceInfo(boosterRate)
				self.__AppendAffectInformation(divideRate=boosterRate)

				self.AppendSpace(5)

				for i in xrange(item.ITEM_APPLY_MAX_NUM):
					affectType = attrSlot[i][0]
					affectValue = (attrSlot[i][1] * boosterRate) / 100

					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue, True))

				item.SelectItem(itemVnum)
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if item.LIMIT_REAL_TIME == limitType:
						self.AppendMallItemLastTime(metinSlot[0])


			self.AppendSpace(5)

		# if app.ENABLE_CROWN_SYSTEM:
		elif item.ITEM_TYPE_CROWN == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.AppendWearableInformation()

			bHasRealtimeFlag = 0
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1
			if bHasRealtimeFlag == 1:
				self.AppendMallItemLastTime(metinSlot[0])
			self.__AppendAccessoryMetinSlotInfo(metinSlot, 24710)

		elif item.ITEM_TYPE_SHINING == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			bHasRealtimeFlag = 0
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1

			if bHasRealtimeFlag == 1:
				self.AppendMallItemLastTime(metinSlot[0])
			else:
				self.__AppendMetinSlotInfo(metinSlot)

		### Use ###
		elif item.ITEM_TYPE_USE == itemType:
			self.__AppendLimitInformation()

			if item.USE_POTION == itemSubType or item.USE_POTION_NODELAY == itemSubType:
				self.__AppendPotionInformation()

			elif item.USE_ABILITY_UP == itemSubType:
				self.__AppendAbilityPotionInformation()

			if 27989 == itemVnum or 76006 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (6 - useCount), self.NORMAL_COLOR)

			elif 50004 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (10 - useCount), self.NORMAL_COLOR)

			elif itemVnum in WARP_SCROLLS:
				if 0 != metinSlot:
					xPos = int(metinSlot[0])
					yPos = int(metinSlot[1])

					if xPos != 0 and yPos != 0:
						(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(xPos, yPos)

						localeMapName=localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")

						self.AppendSpace(5)

						if localeMapName!="":
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION % (localeMapName, int(xPos-xBase)/100, int(yPos-yBase)/100), self.NORMAL_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION_ERROR % (int(xPos)/100, int(yPos)/100), self.NORMAL_COLOR)
							dbg.TraceError("NOT_EXIST_IN_MINIMAP_ZONE_NAME_DICT: %s" % mapName)

			#####
			if item.USE_SPECIAL == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					if 0 != metinSlot:
						time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

						if 1 == item.GetValue(2):
							self.AppendMallItemLastTime(time)

				if itemVnum in xrange(57000, 57012):
					self.__AppendAffectInformation()
					self.__AppendAttributeInformation(attrSlot)

				if itemVnum in (79505, 79512, 79507, 79603, 50096):
					neededItemCount = 0
					if itemVnum == 79505:
						neededItemCount = 24
					elif itemVnum == 79512:
						neededItemCount = 18
					elif itemVnum == 79507:
						neededItemCount = 28
					elif itemVnum == 79603:
						neededItemCount = 25
					elif itemVnum == 50096:
						neededItemCount = 50

					self.AppendTextLine(localeInfo.CONVER_TO_CARD_SET.format(neededItemCount))

				if itemVnum == 70038:
					capeGoldInfo = {
						0 : 5000,
						1 : 10000,
						2 : 15000,
						3 : 25000,
						4 : 40000
					}
					self.AppendHorizontalLine()
					self.AppendSpace(2)
					self.AppendTextLine("Level >= 30 -" + "{} |Eothers/shopsearchyang|e ".format(localeInfo.NumberToDecimal(capeGoldInfo[0])), colorInfo.BLEND_ATTRIBUTE)
					self.AppendTextLine("Level >= 50 -" + "{} |Eothers/shopsearchyang|e ".format(localeInfo.NumberToDecimal(capeGoldInfo[1])), colorInfo.BLEND_ATTRIBUTE)
					self.AppendTextLine("Level >= 75 -" + "{} |Eothers/shopsearchyang|e ".format(localeInfo.NumberToDecimal(capeGoldInfo[2])), colorInfo.BLEND_ATTRIBUTE)
					self.AppendTextLine("Level >= 90 -" + "{} |Eothers/shopsearchyang|e ".format(localeInfo.NumberToDecimal(capeGoldInfo[3])), colorInfo.BLEND_ATTRIBUTE)
					self.AppendTextLine("Level >= 105 -" + "{} |Eothers/shopsearchyang|e ".format(localeInfo.NumberToDecimal(capeGoldInfo[4])), colorInfo.BLEND_ATTRIBUTE)

			elif item.USE_TIME_CHARGE_PER == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(item.GetValue(0)))

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_TIME_CHARGE_FIX == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(item.GetValue(0)))

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			elif "USE_CHANGE_ATTRIBUTE2" == item.GetUseType(itemVnum):
				self.__AppendAffectInformation()
				self.__AppendAttributeInformation(attrSlot)

				helmetVnums = range(24155, 24165)
				bodyVnums = range(24175, 24185)
				weaponVnums = range(24195, 24200)
				weaponVnums2 = range(24225, 24230)

				if itemVnum in (helmetVnums + bodyVnums + weaponVnums + weaponVnums2):
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TO_ADD_THIS_YOU_NEED_TO_ADD_FIRST_ONE, self.GREEN_COLOR)
					self.AppendTextLine(localeInfo.TO_ADD_THIS_YOU_NEED_TO_ADD_FIRST_ONE2, self.GREEN_COLOR)

		elif item.ITEM_TYPE_QUEST == itemType:
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])
		elif item.ITEM_TYPE_DS == itemType:
			self.AppendTextLine(self.__DragonSoulInfoString(itemVnum))

			if app.ENABLE_DS_SET_BONUS:
				if window_type == player.INVENTORY and self.interface and self.interface.wndDragonSoul:
					self.__AppendDragonSoulAttributeInformation(attrSlot, itemVnum/10000, self.interface.wndDragonSoul.GetDSSetGrade())
				else:
					self.__AppendDragonSoulAttributeInformation(attrSlot)
			else:
				self.__AppendAttributeInformation(attrSlot)

		elif item.ITEM_TYPE_SPECIAL == itemType: # ENABLE_MINI_GAME_CATCH_KING / ENABLE_MINI_GAME_BNW / ENABLE_MINI_GAME_OKEY_NORMAL
			item.SelectItem(itemVnum)
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)
			#dbg.TraceError("LimitType : %d, limitValue : %d" % (limitType, limitValue))

			if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
				self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)
				#dbg.TraceError("2) REAL_TIME_START_FIRST_USE flag On ")

			elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
				self.AppendTimerBasedOnWearLastTime(metinSlot)
				#dbg.TraceError("1) REAL_TIME flag On ")


		AFDict = {
			uiScriptLocale.SAFE_TITLE: item.IsAntiFlag(item.ITEM_ANTIFLAG_DROP),
			uiScriptLocale.SHOP_SELL: item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL),
			localeInfo.TARGET_BUTTON_EXCHANGE: item.IsAntiFlag(item.ITEM_ANTIFLAG_GIVE),
			localeInfo.TOOLTIP_ANTIFLAG_STACK: item.IsAntiFlag(item.ITEM_ANTIFLAG_STACK),
			uiScriptLocale.SHOP_TITLE: item.IsAntiFlag(item.ITEM_ANTIFLAG_MYSHOP),
			uiScriptLocale.SAFE_TITLE: item.IsAntiFlag(item.ITEM_ANTIFLAG_SAFEBOX),
		}
		
		AFNames = [name for name, flag in AFDict.iteritems() if flag]
		if AFNames:

			AFTitle = self.AppendTextLine(localeInfo.NOT_POSSIBLE, self.DISABLE_COLOR)
			AFLine = self.AppendTextLine('{}'.format(', '.join(AFNames)), self.DISABLE_COLOR)

			AFTitle.SetFeather()
			AFLine.SetFeather()

		self.ShowToolTip()

	def __DragonSoulInfoString (self, dwVnum):
		step = (dwVnum / 100) % 10
		refine = (dwVnum / 10) % 10
		if 0 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL1 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 1 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL2 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 2 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL3 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 3 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL4 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 4 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL5 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		else:
			return ""

	def __IsHair(self, itemVnum):
		return (self.__IsOldHair(itemVnum) or
			self.__IsNewHair(itemVnum) or
			self.__IsNewHair2(itemVnum) or
			self.__IsNewHair3(itemVnum)
		)

	def __IsOldHair(self, itemVnum):
		return itemVnum > 73000 and itemVnum < 74000

	def __IsNewHair(self, itemVnum):
		return itemVnum > 74000 and itemVnum < 75000

	def __IsNewHair2(self, itemVnum):
		return itemVnum > 75000 and itemVnum < 76000

	def __IsNewHair3(self, itemVnum):
		return ((74012 < itemVnum and itemVnum < 74022) or
			(74262 < itemVnum and itemVnum < 74272) or
			(74512 < itemVnum and itemVnum < 74599) or
			(74762 < itemVnum and itemVnum < 74799) or
			(45000 < itemVnum and itemVnum < 47000))

	if app.ENABLE_RENDER_TARGET:
		def ModelPreviewFull(self, itemVnum, slotIndex = -1, itemShop = False):
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()

			IsPets = (itemType == item.ITEM_TYPE_PET or itemType == item.ITEM_PET_SKIN) 
			IsMounts = ((itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_MOUNT) or itemType == item.ITEM_MOUNT_SKIN)

			IsArmor = (itemType == item.ITEM_TYPE_ARMOR and itemSubType == item.ARMOR_BODY)
			IsWeapon = (itemType == item.ITEM_TYPE_WEAPON)

			IsCostumeBody = (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_BODY)
			IsCostumeHair = (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_HAIR)
			IsCostumeWeapon = (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_WEAPON)
			IsCostumeAcce = (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_ACCE)
			IsCostumeAcceSkin = (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_WING)
			isAura = (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_AURA) or (itemType == item.ITEM_AURA_SKIN)

			import uiRenderTarget, chat
			self.wndTargetRender = uiRenderTarget.RenderTarget.Get()

			if itemShop:
				if IsWeapon or IsCostumeWeapon:
					self.itemShopPreviewItems[self.iShopWeapon] = itemVnum
				elif IsArmor or IsCostumeBody:
					self.itemShopPreviewItems[self.iShopArmor] = itemVnum
				elif IsCostumeHair:
					self.itemShopPreviewItems[self.iShopHair] = itemVnum
				elif IsCostumeAcce or IsCostumeAcceSkin:
					self.itemShopPreviewItems[self.iShopAcce] = itemVnum
				elif isAura:
					self.itemShopPreviewItems[self.iShopAura] = itemVnum

				self.wndTargetRender.DisplayUser(self.ItemGetRace(itemVnum), self.itemShopPreviewItems[self.iShopWeapon], \
				self.itemShopPreviewItems[self.iShopArmor],
				self.itemShopPreviewItems[self.iShopHair],
				self.itemShopPreviewItems[self.iShopAcce],
				self.itemShopPreviewItems[self.iShopAura]
				)
				self.wndTargetRender.Open()

			else:
				if IsWeapon or IsCostumeWeapon:
					self.wndTargetRender.DisplayUser(self.ItemGetRace(itemVnum), vItemWeapon=itemVnum)
					self.wndTargetRender.Open()
				elif IsArmor or IsCostumeBody:
					self.wndTargetRender.DisplayUser(self.ItemGetRace(itemVnum), vItemArmor=itemVnum)
					self.wndTargetRender.Open()
		
				elif IsCostumeHair:
					self.wndTargetRender.DisplayUser(self.ItemGetRace(itemVnum), vItemHair=itemVnum)
					self.wndTargetRender.Open()
				elif IsCostumeAcce or IsCostumeAcceSkin:
					self.wndTargetRender.DisplayUser(self.ItemGetRace(itemVnum), vItemAcce=itemVnum)
					self.wndTargetRender.Open()
				elif isAura:
					self.wndTargetRender.DisplayUser(self.ItemGetRace(itemVnum), vItemAura=itemVnum)
					self.wndTargetRender.Open()

				elif IsPets or IsMounts:
					mobVnum = item.GetValue(1)
					if mobVnum != 0:
						self.wndTargetRender.DisplayUser(vRace=mobVnum)
						self.wndTargetRender.Open()

		def AppendRenderingTooltip(self, itemVnum):
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()

			IsPets = (itemType == item.ITEM_TYPE_PET or itemType == item.ITEM_PET_SKIN) 
			IsMounts = ((itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_MOUNT) or itemType == item.ITEM_MOUNT_SKIN)

			if itemType == item.ITEM_TYPE_WEAPON or\
				(itemType == item.ITEM_TYPE_ARMOR and itemSubType == item.ARMOR_BODY) or\
				(itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_BODY) or\
				(itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_HAIR) or\
				(itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_ACCE) or\
				(itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_WING) or\
				(itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_WEAPON) or IsPets or IsMounts or \
				(itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_AURA) or (itemType == item.ITEM_AURA_SKIN):
				
				if app.ENABLE_HIDE_TOOLTIP_EMOJI and systemSetting.GetEmojiStatus():
					self.AppendSpace(2)
					self.AppendTextLine(localeInfo.MODEL_ITEM_PREVIEW, centerAlign = False)

		def ItemGetRace(self, itemVnum = 0):
			races_m = []
			races_f = []
			MALES = [0, 5, 2, 7, 8]
			FEMALES = [4, 1, 6, 3]
			
			item.SelectItem(itemVnum)
			
			if not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR):
				races_m.append(MALES[0])
				races_f.append(FEMALES[0])
			if not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN):
				races_m.append(MALES[1])
				races_f.append(FEMALES[1])
			if not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA):
				races_m.append(MALES[2])
				races_f.append(FEMALES[2])
			if not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
				races_m.append(MALES[3])
				races_f.append(FEMALES[3])
			# if not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN):
				# races_m.append(MALES[4])

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				races_f = []
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				races_m = []
			
			race = player.GetRace()
			
			if race in races_m or race in races_f:
				return race
			
			if len(races_f) == 0:
				if race in races_m:
					return race
				if len(races_m) > 2:
					return app.GetRandom(0, len(races_m) - 1)
				return races_m[0]
			
			elif len(races_m) == 0:
				if race in races_f:
					return race
				if len(races_f) > 2:
					return app.GetRandom(0, len(races_f) - 1)
				return races_f[0]
			
			else:
				table = []
				for i in races_f:
					table.append(i)
				for i in races_m:
					table.append(i)
					
				return table[app.GetRandom(0, len(table) - 1)]

			return race


	def AppendWikiTooltip(self):
		self.AppendSpace(5)
		if app.ENABLE_HIDE_TOOLTIP_EMOJI and systemSetting.GetEmojiStatus():
			self.AppendTextLine(localeInfo.WIKI_SEARCH_SHORTCUT_SEARCH, centerAlign = False)

	def __AppendHairIcon(self, itemVnum):
		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()

		if self.__IsOldHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum)+".tga")
		elif self.__IsNewHair3(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif self.__IsNewHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum-1000)+".tga")
		elif self.__IsNewHair2(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))

		itemImage.SetPosition(itemImage.GetWidth()/2, self.toolTipHeight)
		self.toolTipHeight += itemImage.GetHeight()
		#self.toolTipWidth += itemImage.GetWidth()/2
		self.childrenList.append(itemImage)
		self.ResizeToolTip()

	def __AdjustMaxWidth(self, attrSlot, desc):
		newToolTipWidth = self.toolTipWidth
		newToolTipWidth = max(self.__AdjustAttrMaxWidth(attrSlot), newToolTipWidth)
		newToolTipWidth = max(self.__AdjustDescMaxWidth(desc), newToolTipWidth)
		if newToolTipWidth > self.toolTipWidth:
			self.toolTipWidth = newToolTipWidth
			self.ResizeToolTip()

	def __AdjustAttrMaxWidth(self, attrSlot):
		if 0 == attrSlot:
			return self.toolTipWidth

		maxWidth = self.toolTipWidth
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			value = attrSlot[i][1]
			if self.ATTRIBUTE_NEED_WIDTH.has_key(type):
				if value > 0:
					maxWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], maxWidth)

			attrText = self.AppendTextLine(self.__GetAffectString(type, value))
			(tW, _) = attrText.GetTextSize()
			self.childrenList.remove(attrText)
			self.toolTipHeight -= self.TEXT_LINE_HEIGHT

			maxWidth = max(tW + 12, maxWidth)

		return maxWidth

	def __AdjustDescMaxWidth(self, desc):
		if len(desc) < DESC_DEFAULT_MAX_COLS:
			return self.toolTipWidth

		return DESC_WESTERN_MAX_WIDTH

	def SafeboxItemMoveToInventory(self):
		self.AppendTextLine(localeInfo.MOVE_ITEM_TO_SAFEBOX_TO_INVEN)

	def AppendIcon(self, itemVnum, itemCount):
		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()
		
		item.SelectItem(itemVnum)
		itemImage.LoadImage(item.GetIconImageFileName())

		if itemCount > 1:
			countNumberLine = ui.NumberLine()
			countNumberLine.SetParent(itemImage)
			countNumberLine.SetWindowHorizontalAlignRight()
			countNumberLine.SetHorizontalAlignRight()
			countNumberLine.SetNumber(str(itemCount))
			countNumberLine.SetPosition(3, itemImage.GetHeight() - 8)
			countNumberLine.Show()

		itemImage.SetPosition((self.GetWidth() - itemImage.GetWidth()) / 2, self.toolTipHeight)
		self.toolTipHeight += itemImage.GetHeight()

		self.childrenList.append(itemImage)
		if itemCount > 1:
			self.childrenList.append(countNumberLine)
		self.ResizeToolTip()

	def ResizeToolTipWidth(self, width):
		self.toolTipWidth = width

	def __CalculateToolTipWidth(self, isRefine=False):
		affectTextLineLenList = []

		metinSocket = self.metinSlot
		if metinSocket:
			for socketIndex in metinSocket:
				if socketIndex:
					item.SelectItem(socketIndex)

					affectType, affectValue = item.GetAffect(0)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						affectTextLineLenList.append(len(affectString))

			if self.itemVnum:
				item.SelectItem(self.itemVnum)
			self.metinSlot = None

		if self.toolTipWidth == self.TOOL_TIP_WIDTH:
			if affectTextLineLenList:
				self.toolTipWidth += max(affectTextLineLenList) + 25

		if app.ENABLE_HIDE_TOOLTIP_EMOJI and systemSetting.GetEmojiStatus() and not isRefine:
			self.toolTipWidth +=75

			if self.isNamingScrollActive:
				self.toolTipWidth += 55

		self.AlignTextLineHorizonalCenter()

	def __SetSkillBookToolTip(self, skillIndex, bookName, skillGrade):
		skillName = skill.GetSkillName(skillIndex)

		if not skillName:
			return

		itemName = skillName + " " + bookName
		self.SetTitle(itemName)

	def __AppendPickInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE3, self.NORMAL_COLOR)


	def __AppendRodInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE3, self.NORMAL_COLOR)

	def __AppendLimitInformation(self):

		appendSpace = False

		for i in xrange(item.LIMIT_MAX_NUM):

			(limitType, limitValue) = item.GetLimit(i)

			if limitValue > 0:
				if False == appendSpace:
					self.AppendSpace(5)
					appendSpace = True

			else:
				continue

			if item.LIMIT_LEVEL == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.LEVEL), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (limitValue), color)

	def __GetAffectString(self, affectType, affectValue):
		if 0 == affectType:
			return None

		if 0 == affectValue:
			return None

		try:
			return self.AFFECT_DICT[affectType](affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def __AppendAffectInformation(self, type = -1, divideRate=0):
		if type in (0, 1):
			self.AppendTextLine(localeInfo.NAMING_SCROLL_AFFECT_TITLE.format(int(constInfo.NAMING_SCROLL_GET_BONUS_RATE(type))), self.GREEN_COLOR)
			self.isNamingScrollActive = True

		for i in xrange(item.ITEM_APPLY_MAX_NUM):
			(affectType, affectValue) = item.GetAffect(i)
			if app.ENABLE_ACCE_COSTUME_SYSTEM and affectType==item.APPLY_ACCEDRAIN_RATE:
				continue

			mountRate = constInfo.NAMING_SCROLL_GET_BONUS_RATE(0)
			petRate = constInfo.NAMING_SCROLL_GET_BONUS_RATE(1)

			additionalValue = -1

			if type == 0 and mountRate:
				additionalValue = (affectValue*mountRate)/100
			elif type == 1 and petRate:
				additionalValue = (affectValue*petRate)/100

			affectString = self.__GetAffectString(affectType, (affectValue*divideRate)/100 if divideRate else affectValue)
			if affectString:
				if type in (0, 1) and additionalValue:
					self.AppendTextLine(affectString + " |cff00C78C(+{})".format(int(additionalValue)), self.GetChangeTextLineColor(affectValue))
				else:
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendWearableInformation(self):
		self.AppendSpace(5)
		if self.__CheckAntiFlag() == True:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.DISABLE_COLOR)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)
		flagList = (
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN))
		# if app.ENABLE_WOLFMAN_CHARACTER:
			# flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)

		characterNames = ""
		for i in xrange(self.CHARACTER_COUNT):
			name = self.CHARACTER_NAMES[i]
			flag = flagList[i]
			if flag:
				characterNames += " "
				characterNames += name
		if self.__CheckAntiFlag() == True:
			textLine = self.AppendTextLine(characterNames, self.DISABLE_COLOR, True)
		else:
			textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
		textLine.SetFeather()
		race = player.GetRace()
		sex = chr.RaceToSex(race)
		MALE = 1
		FEMALE = 0
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
			if sex == MALE:
				textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.DISABLE_COLOR, True)
				textLine.SetFeather()
			else:
				textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
			if sex == FEMALE:
				textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.DISABLE_COLOR, True)
				textLine.SetFeather()
			else:
				textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def AppendAbsorbedItemInfo(self, itemVnum, socketItem, attrSlot):
			if socketItem:
				item.SelectItem(itemVnum)
				self.AppendHorizontalLine()
				if (item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_ACCE) or \
						(itemVnum >= 49001 and itemVnum <= 49006):
					item.SelectItem(socketItem)
					self.AppendTextLine(localeInfo.ACCE_ABSORBED_ITEM_NAME, 0xff8BBDFF)
					self.AppendTextLine("{}".format(item.GetItemName()), 0xffBCE55C)
					self.AppendSpace(2)
					# self.AppendTextLine(localeInfo.ACCE_ABSORBED_BONUSSES, self.ITEM_BUFF_LEVEL_COLOR) 
					# self.AppendSpace(2)

					if item.GetItemType() == item.ITEM_TYPE_WEAPON:
						if item.GetItemSubType() == item.WEAPON_FAN:
							self.__AppendMagicAttackInfo()
							self.__AppendAttackPowerInfo()
						else:
							self.__AppendAttackPowerInfo()
							self.__AppendMagicAttackInfo()

					elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
						defGrade = item.GetValue(1)
						defBonus = item.GetValue(5) * 2

						if defGrade > 0:
							self.AppendSpace(5)
							self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))

						self.__AppendMagicDefenceInfo()

					for i in xrange(item.ITEM_APPLY_MAX_NUM):
						(affectType, affectValue) = item.GetAffect(i)
						affectString = self.__GetAffectString(affectType, affectValue)
						if (not app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue != 0)\
								or (app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue > 0):
							self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

					self.__AppendAttributeInformation(attrSlot)

	def __AppendPotionInformation(self):
		self.AppendSpace(5)

		healHP = item.GetValue(0)
		healSP = item.GetValue(1)
		healStatus = item.GetValue(2)
		healPercentageHP = item.GetValue(3)
		healPercentageSP = item.GetValue(4)

		if healHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_POINT % healHP, self.GetChangeTextLineColor(healHP))
		if healSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_POINT % healSP, self.GetChangeTextLineColor(healSP))
		if healStatus != 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_CURE)
		if healPercentageHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_PERCENT % healPercentageHP, self.GetChangeTextLineColor(healPercentageHP))
		if healPercentageSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_PERCENT % healPercentageSP, self.GetChangeTextLineColor(healPercentageSP))

	def __AppendAbilityPotionInformation(self):

		self.AppendSpace(5)

		abilityType = item.GetValue(0)
		time = item.GetValue(1)
		point = item.GetValue(2)

		if abilityType == item.APPLY_ATT_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_ATTACK_SPEED % point, self.GetChangeTextLineColor(point))
		elif abilityType == item.APPLY_MOV_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_MOVING_SPEED % point, self.GetChangeTextLineColor(point))

		if time > 0:
			minute = (time / 60)
			second = (time % 60)
			timeString = localeInfo.TOOLTIP_POTION_TIME

			if minute > 0:
				timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
			if second > 0:
				timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

			self.AppendTextLine(timeString)

	def GetPriceColor(self, price):
		if price>=constInfo.HIGH_PRICE:
			return self.HIGH_PRICE_COLOR
		if price>=constInfo.MIDDLE_PRICE:
			return self.MIDDLE_PRICE_COLOR
		else:
			return self.LOW_PRICE_COLOR

	def AppendPrice(self, price):
		self.AppendSpace(5)
		if price == 0:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_FREE, self.SPECIAL_POSITIVE_COLOR2)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))

	def AppendPriceBySecondaryCoin(self, price):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToSecondaryCoinString(price)), self.GetPriceColor(price))

	def AppendSellingPrice(self, price):
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL):
			self.AppendTextLine(localeInfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
			self.AppendSpace(5)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_SELLPRICE % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
			self.AppendSpace(5)

	def AppendMetinInformation(self):
		if constInfo.ENABLE_FULLSTONE_DETAILS:
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					self.AppendSpace(5)
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendMetinWearInformation(self):

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SOCKET_REFINABLE_ITEM, self.NORMAL_COLOR)

		flagList = (item.IsWearableFlag(item.WEARABLE_BODY),
					item.IsWearableFlag(item.WEARABLE_HEAD),
					item.IsWearableFlag(item.WEARABLE_FOOTS),
					item.IsWearableFlag(item.WEARABLE_WRIST),
					item.IsWearableFlag(item.WEARABLE_WEAPON),
					item.IsWearableFlag(item.WEARABLE_NECK),
					item.IsWearableFlag(item.WEARABLE_EAR),
					item.IsWearableFlag(item.WEARABLE_UNIQUE),
					item.IsWearableFlag(item.WEARABLE_SHIELD),
					item.IsWearableFlag(item.WEARABLE_ARROW))

		wearNames = ""
		for i in xrange(self.WEAR_COUNT):

			name = self.WEAR_NAMES[i]
			flag = flagList[i]

			if flag:
				wearNames += "  "
				wearNames += name

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
		textLine.SetHorizontalAlignCenter()
		textLine.SetPackedFontColor(self.NORMAL_COLOR)
		textLine.SetText(wearNames)
		textLine.Show()
		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

	def GetMetinSocketType(self, number):
		if player.METIN_SOCKET_TYPE_NONE == number:
			return player.METIN_SOCKET_TYPE_NONE
		elif player.METIN_SOCKET_TYPE_SILVER == number:
			return player.METIN_SOCKET_TYPE_SILVER
		elif player.METIN_SOCKET_TYPE_GOLD == number:
			return player.METIN_SOCKET_TYPE_GOLD
		else:
			item.SelectItem(number)
			if item.METIN_NORMAL == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_SILVER
			elif item.METIN_GOLD == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_GOLD
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_RING_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_BELT_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER

		return player.METIN_SOCKET_TYPE_NONE

	def GetMetinItemIndex(self, number):
		if player.METIN_SOCKET_TYPE_SILVER == number:
			return 0
		if player.METIN_SOCKET_TYPE_GOLD == number:
			return 0

		return number

	def __AppendAccessoryMetinSlotInfo(self, metinSlot, mtrlVnum):

		ACCESSORY_SOCKET_MAX_SIZE = 3
		cur = min(metinSlot[0], ACCESSORY_SOCKET_MAX_SIZE)
		end = min(metinSlot[1], ACCESSORY_SOCKET_MAX_SIZE)

		permanent = 0
		if metinSlot[2] == 62:
			mtrlVnum = constInfo.JewelAccessoryInfosDict[mtrlVnum]
			permanent = 1

		bonusDict = [10, 20, 40, 50]
		permanentBonusDict = [15, 25, 55, 65]

		affectType1, affectValue1 = item.GetAffect(0)
		affectList1=[0, max(1, affectValue1*bonusDict[0]/100), max(2, affectValue1*bonusDict[1]/100), max(3, affectValue1*bonusDict[2]/100), max(4, affectValue1*bonusDict[3]/100)]
		affectType2, affectValue2 = item.GetAffect(1)
		affectList2=[0, max(1, affectValue2*bonusDict[0]/100), max(2, affectValue2*bonusDict[1]/100), max(3, affectValue2*bonusDict[2]/100), max(4, affectValue2*bonusDict[3]/100)]
		affectType3, affectValue3 = item.GetAffect(2)
		affectList3=[0, max(1, affectValue3*bonusDict[0]/100), max(2, affectValue3*bonusDict[1]/100), max(3, affectValue3*bonusDict[2]/100), max(4, affectValue3*bonusDict[3]/100)]
		affectType4, affectValue4 = item.GetAffect(3)
		affectList4=[0, max(1, affectValue4*bonusDict[0]/100), max(2, affectValue4*bonusDict[1]/100), max(3, affectValue4*bonusDict[2]/100), max(4, affectValue4*bonusDict[3]/100)]
		affectType5, affectValue5 = item.GetAffect(4)
		affectList5=[0, max(1, affectValue5*bonusDict[0]/100), max(2, affectValue5*bonusDict[1]/100), max(3, affectValue5*bonusDict[2]/100), max(4, affectValue5*bonusDict[3]/100)]

		permaAffectList1=[0, max(1, affectValue1*permanentBonusDict[0]/100), max(2, affectValue1*permanentBonusDict[1]/100), max(3, affectValue1*permanentBonusDict[2]/100), max(4, affectValue1*permanentBonusDict[3]/100)]
		permaAffectList2=[0, max(1, affectValue2*permanentBonusDict[0]/100), max(2, affectValue2*permanentBonusDict[1]/100), max(3, affectValue2*permanentBonusDict[2]/100), max(4, affectValue2*permanentBonusDict[3]/100)]
		permaAffectList3=[0, max(1, affectValue3*permanentBonusDict[0]/100), max(2, affectValue3*permanentBonusDict[1]/100), max(3, affectValue3*permanentBonusDict[2]/100), max(4, affectValue3*permanentBonusDict[3]/100)]
		permaAffectList4=[0, max(1, affectValue4*permanentBonusDict[0]/100), max(2, affectValue4*permanentBonusDict[1]/100), max(3, affectValue4*permanentBonusDict[2]/100), max(4, affectValue4*permanentBonusDict[3]/100)]
		permaAffectList5=[0, max(1, affectValue5*permanentBonusDict[0]/100), max(2, affectValue5*permanentBonusDict[1]/100), max(3, affectValue5*permanentBonusDict[2]/100), max(4, affectValue5*permanentBonusDict[3]/100)]

		mtrlPos = 0
		mtrlList = [mtrlVnum]*cur+[player.METIN_SOCKET_TYPE_SILVER] * (end-cur)
		attr_total = [0, 0, 0, 0, 0]
		attr_total_permanent = [0, 0, 0, 0, 0]
		left_time = 0

		self.AppendSpace(5)

		if mtrlVnum > 0 and end > 0:
			item.SelectItem(mtrlVnum)
			self.AppendTextLine(localeInfo.JEWEL_TYPE_TEXT.format(str(item.GetItemName())), self.TOOLTIP_STUFF_COLOR)
			self.AppendSpace(5)
		
		height = self.toolTipHeight

		for mtrl in mtrlList:
			affectString1 = self.__GetAffectString(affectType1, affectList1[mtrlPos+1]-affectList1[mtrlPos])
			affectString2 = self.__GetAffectString(affectType2, affectList2[mtrlPos+1]-affectList2[mtrlPos])
			affectString3 = self.__GetAffectString(affectType3, affectList3[mtrlPos+1]-affectList3[mtrlPos])
			affectString4 = self.__GetAffectString(affectType4, affectList4[mtrlPos+1]-affectList4[mtrlPos])
			affectString5 = self.__GetAffectString(affectType5, affectList5[mtrlPos+1]-affectList5[mtrlPos])

			leftTime = 0
			if mtrl > 1:
				if affectString1:
					attr_total[0] += affectList1[mtrlPos+1]-affectList1[mtrlPos]
					attr_total_permanent[0] += permaAffectList1[mtrlPos+1]-permaAffectList1[mtrlPos]
				if affectString2:
					attr_total[1] += affectList2[mtrlPos+1]-affectList2[mtrlPos]
					attr_total_permanent[1] += permaAffectList2[mtrlPos+1]-permaAffectList2[mtrlPos]
				if affectString3:
					attr_total[2] += affectList3[mtrlPos+1]-affectList3[mtrlPos]
					attr_total_permanent[2] += permaAffectList3[mtrlPos+1]-permaAffectList3[mtrlPos]
				if affectString4:
					attr_total[3] += affectList4[mtrlPos+1]-affectList4[mtrlPos]
					attr_total_permanent[3] += permaAffectList4[mtrlPos+1]-permaAffectList4[mtrlPos]
				if affectString5:
					attr_total[4] += affectList5[mtrlPos+1]-affectList5[mtrlPos]
					attr_total_permanent[4] += permaAffectList5[mtrlPos+1]-permaAffectList5[mtrlPos]

			left_time = metinSlot[2]

			self.__AppendMetinSlotInfo_AppendMetinSocketData_New(mtrlPos, mtrl, leftTime, permanent, height, end)
			mtrlPos+=1

		if end > 0:
			self.toolTipHeight += 35
			self.AppendSpace(5)

			affectString11 = self.__GetAffectString(affectType1, attr_total[0])
			affectString22 = self.__GetAffectString(affectType2, attr_total[1])
			affectString33 = self.__GetAffectString(affectType3, attr_total[2])
			affectString44 = self.__GetAffectString(affectType4, attr_total[3])
			affectString55 = self.__GetAffectString(affectType5, attr_total[4])

			permaAttrRate = attr_total_permanent[0] - attr_total[0]
			permaAttrRate2 = attr_total_permanent[1] - attr_total[1]
			permaAttrRate3 = attr_total_permanent[2] - attr_total[2]
			permaAttrRate4 = attr_total_permanent[3] - attr_total[3]
			permaAttrRate5 = attr_total_permanent[4] - attr_total[4]

			if permanent:
				affectString11 = self.__GetAffectString(affectType1, attr_total_permanent[0] - permaAttrRate)
				affectString22 = self.__GetAffectString(affectType2, attr_total_permanent[1] - permaAttrRate2)
				affectString33 = self.__GetAffectString(affectType3, attr_total_permanent[2] - permaAttrRate3)
				affectString44 = self.__GetAffectString(affectType4, attr_total_permanent[3] - permaAttrRate4)
				affectString55 = self.__GetAffectString(affectType5, attr_total_permanent[4] - permaAttrRate5)

			if affectString11:
				self.AppendTextLine(localeInfo.JEWEL_BONUSSES, self.TOOLTIP_STUFF_COLOR)

			if permanent:
				if permaAttrRate <= 0:
					if affectString11:
						self.AppendTextLine(affectString11, self.POSITIVE_COLOR)
					if affectString22:
						self.AppendTextLine(affectString22, self.POSITIVE_COLOR)
					if affectString33:
						self.AppendTextLine(affectString33, self.POSITIVE_COLOR)
					if affectString44:
						self.AppendTextLine(affectString44, self.POSITIVE_COLOR)
					if affectString55:
						self.AppendTextLine(affectString55, self.POSITIVE_COLOR)
				else:
					if affectString11:
						self.AppendTextLine(affectString11 + (" |cffFFD700(+{})".format(permaAttrRate)), self.POSITIVE_COLOR)
					if affectString22:
						self.AppendTextLine(affectString22 + (" |cffFFD700(+{})".format(permaAttrRate2)), self.POSITIVE_COLOR)
					if affectString33:
						self.AppendTextLine(affectString33 + (" |cffFFD700(+{})".format(permaAttrRate3)), self.POSITIVE_COLOR)
					if affectString44:
						self.AppendTextLine(affectString44 + (" |cffFFD700(+{})".format(permaAttrRate4)), self.POSITIVE_COLOR)
					if affectString55:
						self.AppendTextLine(affectString55 + (" |cffFFD700(+{})".format(permaAttrRate5)), self.POSITIVE_COLOR)

			else:
				if affectString11:
					self.AppendTextLine(affectString11, self.POSITIVE_COLOR)
				if affectString22:
					self.AppendTextLine(affectString22, self.POSITIVE_COLOR)
				if affectString33:
					self.AppendTextLine(affectString33, self.POSITIVE_COLOR)
				if affectString44:
					self.AppendTextLine(affectString44, self.POSITIVE_COLOR)
				if affectString55:
					self.AppendTextLine(affectString55, self.POSITIVE_COLOR)

			self.ResizeToolTip()

			if 0 != left_time and permanent != 1:
				timeText = (localeInfo.LEFT_TIME + ": " + localeInfo.SecondToDHM(left_time))
				self.AppendSpace(5)
				self.AppendTextLine(timeText, self.PRICE_INFO_COLOR)

			# if permanent:
			# 	timeText = localeInfo.PERMANENT_ACCESSORY_SOCKET
			# 	self.AppendSpace(5)
			# 	self.AppendTextLine(timeText, self.PRICE_INFO_COLOR)

		self.ResizeToolTip()

	def __AppendMetinSlotInfo_AppendMetinSocketData_New(self, index, metinSlotData, leftTime=0, permanent=0, height=0, end=0):

		slotType = self.GetMetinSocketType(metinSlotData)
		itemIndex = self.GetMetinItemIndex(metinSlotData)

		if 0 == slotType:
			return

		slotImage = ui.ImageBox()
		slotImage.SetParent(self)
		slotImage.Show()

		if player.METIN_SOCKET_TYPE_SILVER == slotType and permanent == 0:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
		elif player.METIN_SOCKET_TYPE_GOLD == slotType and permanent == 0:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")
		elif permanent > 0:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

		self.childrenList.append(slotImage)
	
			
		calc_x = (self.toolTipWidth/2) - (17.5*end)
		
		slotImage.SetPosition(calc_x+index*38, height)

		metinImage = ui.ImageBox()
		metinImage.SetParent(slotImage)
		metinImage.Show()
		self.childrenList.append(metinImage)

		if itemIndex:
			item.SelectItem(itemIndex)

			## Image
			try:
				metinImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" % 
					(itemIndex, item.GetIconImageFileName())
				)

			metinImage.SetPosition(1, 1)


	def __AppendMetinSlotInfo(self, metinSlot):
		if self.__AppendMetinSlotInfo_IsEmptySlotList(metinSlot):
			return

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])

	def __AppendMetinSlotInfo_IsEmptySlotList(self, metinSlot):
		if 0 == metinSlot:
			return 1

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if 0 != self.GetMetinSocketType(metinSlotData):
				if 0 != self.GetMetinItemIndex(metinSlotData):
					return 0

		return 1

	def __AppendMetinSlotInfo_AppendMetinSocketData(self, index, metinSlotData, custumAffectString="", custumAffectString2="", custumAffectString3="", leftTime=0):

		slotType = self.GetMetinSocketType(metinSlotData)
		itemIndex = self.GetMetinItemIndex(metinSlotData)

		if 0 == slotType:
			return

		self.AppendSpace(5)

		slotImage = ui.ImageBox()
		slotImage.SetParent(self)
		slotImage.Show()

		## Name
		nameTextLine = ui.TextLine()
		nameTextLine.SetParent(self)
		nameTextLine.SetFontName(self.defFontName)
		nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
		nameTextLine.SetOutline()
		nameTextLine.SetFeather()
		nameTextLine.Show()

		self.childrenList.append(nameTextLine)

		if player.METIN_SOCKET_TYPE_SILVER == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
		elif player.METIN_SOCKET_TYPE_GOLD == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

		self.childrenList.append(slotImage)

		slotImage.SetPosition(9, self.toolTipHeight-1)
		nameTextLine.SetPosition(50, self.toolTipHeight + 2)

		metinImage = ui.ImageBox()
		metinImage.SetParent(self)
		metinImage.Show()
		self.childrenList.append(metinImage)

		if itemIndex:

			item.SelectItem(itemIndex)

			## Image
			try:
				metinImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" %
					(itemIndex, item.GetIconImageFileName())
				)

			nameTextLine.SetText(item.GetItemName())

			## Affect
			affectTextLine = ui.TextLine()
			affectTextLine.SetParent(self)
			affectTextLine.SetFontName(self.defFontName)
			affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
			affectTextLine.SetOutline()
			affectTextLine.SetFeather()
			affectTextLine.Show()

			metinImage.SetPosition(10, self.toolTipHeight)
			affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

			if custumAffectString:
				affectTextLine.SetText(custumAffectString)
			elif itemIndex!=constInfo.ERROR_METIN_STONE:
				affectType, affectValue = item.GetAffect(0)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectTextLine.SetText(affectString)
			else:
				affectTextLine.SetText(localeInfo.TOOLTIP_APPLY_NOAFFECT)

			self.childrenList.append(affectTextLine)

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString2) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString2 = self.__GetAffectString(*item.GetAffect(1))

			if custumAffectString2:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString2)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString3) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString3 = self.__GetAffectString(*item.GetAffect(2))

			if custumAffectString3:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString3)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if 0 != leftTime:
				timeText = (localeInfo.LEFT_TIME + ": " + localeInfo.SecondToDHM(leftTime))

				timeTextLine = ui.TextLine()
				timeTextLine.SetParent(self)
				timeTextLine.SetFontName(self.defFontName)
				timeTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				timeTextLine.SetOutline()
				timeTextLine.SetFeather()
				timeTextLine.Show()
				timeTextLine.SetText(timeText)
				self.childrenList.append(timeTextLine)
				self.toolTipHeight += 16 + 2

		else:
			nameTextLine.SetText(localeInfo.TOOLTIP_SOCKET_EMPTY)

		self.toolTipHeight += 35
		self.ResizeToolTip()

	def __AppendFishInfo(self, size):
		if size > 0:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISH_LEN % (float(size) / 100.0), self.NORMAL_COLOR)

	def AppendUniqueItemLastTime(self, restMin):
		if restMin > 0: # @fixme012
			restSecond = restMin*60
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.LEFT_TIME + ": " + localeInfo.SecondToDHM(restSecond), self.NORMAL_COLOR)

	def AppendMallItemLastTime(self, endTime):
		if endTime > 0: # @fixme012
			leftSec = max(0, endTime - app.GetGlobalTimeStamp())
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.LEFT_TIME + ": " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

	def AppendTimerBasedOnWearLastTime(self, metinSlot):
		if 0 == metinSlot[0]:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.CANNOT_USE, self.DISABLE_COLOR)
		else:
			endTime = app.GetGlobalTimeStamp() + metinSlot[0]
			self.AppendMallItemLastTime(endTime)

	def AppendRealTimeStartFirstUseLastTime(self, item, metinSlot, limitIndex):
		useCount = metinSlot[1]
		endTime = metinSlot[0]

		if 0 == useCount:
			if 0 == endTime:
				(limitType, limitValue) = item.GetLimit(limitIndex)
				endTime = limitValue

			endTime += app.GetGlobalTimeStamp()

		self.AppendMallItemLastTime(endTime)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def SetAcceResultItem(self, slotIndex, window_type = player.INVENTORY):
			(itemVnum, MinAbs, MaxAbs) = acce.GetResultItem()
			if not itemVnum:
				return

			self.ClearToolTip()

			metinSlot 	= [player.GetItemMetinSocket(window_type, slotIndex, i) 	for i in xrange(player.METIN_SOCKET_MAX_NUM)	]
			attrSlot 	= [player.GetItemAttribute(window_type, slotIndex, i) 		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)	]

			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_ACCE:
				return

			absChance = MaxAbs
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnum, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendLimitInformation()

			## ABSORPTION RATE
			if MinAbs == MaxAbs:
				self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE % (MinAbs), self.CONDITION_COLOR)
			else:
				self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE2 % (MinAbs, MaxAbs), self.CONDITION_COLOR)
			## END ABSOPRTION RATE

			itemAbsorbedVnum = int(metinSlot[acce.ABSORBED_SOCKET])
			if itemAbsorbedVnum:
				## ATTACK / DEFENCE
				item.SelectItem(itemAbsorbedVnum)
				if item.GetItemType() == item.ITEM_TYPE_WEAPON:
					if item.GetItemSubType() == item.WEAPON_FAN:
						self.__AppendMagicAttackInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendAttackPowerInfo(absChance)
					else:
						self.__AppendAttackPowerInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendMagicAttackInfo(absChance)
				elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
					defGrade = item.GetValue(1)
					defBonus = item.GetValue(5) * 2
					defGrade = self.CalcAcceValue(defGrade, absChance)
					defBonus = self.CalcAcceValue(defBonus, absChance)

					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))

					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicDefenceInfo(absChance)
				## END ATTACK / DEFENCE

				## EFFECT
				item.SelectItem(itemAbsorbedVnum)
				for i in xrange(item.ITEM_APPLY_MAX_NUM):
					(affectType, affectValue) = item.GetAffect(i)
					affectValue = self.CalcAcceValue(affectValue, absChance)
					affectString = self.__GetAffectString(affectType, affectValue)
					if (not app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue != 0)\
							or (app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue > 0):
						self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

					item.SelectItem(itemAbsorbedVnum)
				# END EFFECT

			item.SelectItem(itemVnum)
			## ATTR
			self.__AppendAttributeInformation(attrSlot, MaxAbs)
			# END ATTR

			self.AppendWearableInformation()
			self.ShowToolTip()

		def SetAcceResultAbsItem(self, slotIndex1, slotIndex2, window_type = player.INVENTORY):
			itemVnumAcce = player.GetItemIndex(window_type, slotIndex1)
			itemVnumTarget = player.GetItemIndex(window_type, slotIndex2)
			if not itemVnumAcce or not itemVnumTarget:
				return

			self.ClearToolTip()

			item.SelectItem(itemVnumAcce)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_ACCE:
				return

			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex1, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex2, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnumAcce, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			item.SelectItem(itemVnumAcce)
			self.__AppendLimitInformation()

			## ABSORPTION RATE
			self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE % (metinSlot[acce.ABSORPTION_SOCKET]), self.CONDITION_COLOR)
			## END ABSOPRTION RATE

			## ATTACK / DEFENCE
			itemAbsorbedVnum = itemVnumTarget
			item.SelectItem(itemAbsorbedVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON:
				if item.GetItemSubType() == item.WEAPON_FAN:
					self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
				else:
					self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])
			elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
				defGrade = item.GetValue(1)
				defBonus = item.GetValue(5) * 2
				defGrade = self.CalcAcceValue(defGrade, metinSlot[acce.ABSORPTION_SOCKET])
				defBonus = self.CalcAcceValue(defBonus, metinSlot[acce.ABSORPTION_SOCKET])

				if defGrade > 0:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))

				item.SelectItem(itemAbsorbedVnum)
				self.__AppendMagicDefenceInfo(metinSlot[acce.ABSORPTION_SOCKET])
			## END ATTACK / DEFENCE

			## EFFECT
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectValue = self.CalcAcceValue(affectValue, metinSlot[acce.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(affectType, affectValue)
				if (not app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue != 0)\
						or (app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue > 0):
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

				item.SelectItem(itemAbsorbedVnum)
			## END EFFECT

			## ATTR
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if not value:
					continue

				affectValue = self.CalcAcceValue(value, metinSlot[acce.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(type, affectValue)
				if (not app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue != 0)\
						or (app.USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS and affectString and affectValue > 0):
					affectColor = self.__GetAttributeColor(i, affectValue)
					self.AppendTextLine(affectString, affectColor)

				item.SelectItem(itemAbsorbedVnum)
			## END ATTR

			## WEARABLE
			item.SelectItem(itemVnumAcce)
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

			item.SelectItem(itemVnumAcce)
			flagList = (
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN)
			)

			# if app.ENABLE_WOLFMAN_CHARACTER:
				# flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)

			characterNames = ""
			for i in xrange(self.CHARACTER_COUNT):
				name = self.CHARACTER_NAMES[i]
				flag = flagList[i]
				if flag:
					characterNames += " "
					characterNames += name

			textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
			textLine.SetFeather()

			item.SelectItem(itemVnumAcce)
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			## END WEARABLE

			self.ShowToolTip()

	if app.ENABLE_NEW_PET_SYSTEM:
		def AppendNewPetInformations(self, itemVnum, metinSlot, attrSlot):
			if constInfo.IS_NEW_PET_ITEM(itemVnum):

				getPetLevel = int(attrSlot[0][1])
				getPetType = int(attrSlot[1][1])
				getPetEvolution = int(attrSlot[0][0])
				getPetStar = int(attrSlot[1][0])
				
				getPetSkillList = [
					attrSlot[2][0],
					# attrSlot[7][1],
					# attrSlot[9][1],
					# attrSlot[11][1],
					# attrSlot[13][1],
					# attrSlot[15][1],
					# attrSlot[17][1]
				]

				getPetSkillValueList = [
					attrSlot[2][1],
					attrSlot[6][1],
					# attrSlot[8][1],
					# attrSlot[10][1],
					# attrSlot[12][1],
					# attrSlot[14][1],
					# attrSlot[16][1],
					# attrSlot[18][1]
				]

				if attrSlot[0][1] != 0:
					self.AppendSpace(2)

				self.AppendTextLine(localeInfo.WIKI_LEVEL_MOB_TEXT % getPetLevel, self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.PET_EVO_NAME_TOOLTIP.format(self.GetPetEvolutionFunc(getPetEvolution)), self.SPECIAL_POSITIVE_COLOR)

				self.AppendTextLine(localeInfo.PET_INFORMATION_ATTR_0+ localeInfo.NEW_PET_SYSTEM_PERCANTAGE_RATE + " " + pointop(str(metinSlot[0])) + "%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.PET_INFORMATION_ATTR_1 + localeInfo.NEW_PET_SYSTEM_PERCANTAGE_RATE + " "+ pointop(str(metinSlot[1])) + "%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine(localeInfo.PET_INFORMATION_ATTR_2 + localeInfo.NEW_PET_SYSTEM_PERCANTAGE_RATE + " "+ pointop(str(metinSlot[2])) + "%", self.SPECIAL_POSITIVE_COLOR)

				self.AppendTextLine(localeInfo.PET_TOOLTIP4 + self.GetPetTypeFunc(getPetType), self.SPECIAL_POSITIVE_COLOR)

				if getPetLevel == 250:
					self.AppendTextLine(localeInfo.PET_INFORMATION_PETSTAR_INFO % (getPetStar), self.SPECIAL_POSITIVE_COLOR)
					self.AppendSpace(2)

				if getPetEvolution >= 3 and getPetLevel >= 80:
					for elem in xrange(2, 10):
						(attr, value) = attrSlot[elem]
						if attr != 0:
							self.AppendTextLine(localeInfo.PET_INFORMATION_SKILL_AND_SKILLLEVEL % (str(self.GetPetSkill(attr)), value), self.SINIRSIZ_COLOR)
						else:
							self.AppendTextLine(localeInfo.PET_SYSTEM_CAN_OPEN_SKILL % (elem-1), self.NEGATIVE_COLOR)

		def GetPetSkill(self, index):
			PetSkills = {
					1 : localeInfo.PET_SKILL_EFFECT_1,
					2 : localeInfo.PET_SKILL_EFFECT_2,
					3 : localeInfo.PET_SKILL_EFFECT_3,
					4 : localeInfo.PET_SKILL_EFFECT_4,
					5 : localeInfo.PET_SKILL_EFFECT_5,
					6 : localeInfo.PET_SKILL_EFFECT_6,
					7 : localeInfo.PET_SKILL_EFFECT_7,
					8 : localeInfo.PET_SKILL_EFFECT_8,
					9 : localeInfo.PET_SKILL_EFFECT_9,
					10 : localeInfo.PET_SKILL_EFFECT_10,
					11 : localeInfo.PET_SKILL_EFFECT_11,
					12 : localeInfo.PET_SKILL_EFFECT_12,
					13 : localeInfo.PET_SKILL_EFFECT_13,
					14 : localeInfo.PET_SKILL_EFFECT_14,
					15 : localeInfo.PET_SKILL_EFFECT_15,
				}
			return PetSkills[index]

		def GetPetEvolutionFunc(self, index):
			petEvolutionList = (localeInfo.PET_EVO_NAME_1, localeInfo.PET_EVO_NAME_2, localeInfo.PET_EVO_NAME_3,
				localeInfo.PET_EVO_NAME_4, localeInfo.PET_EVO_NAME_5, localeInfo.PET_EVO_NAME_6, localeInfo.PET_EVO_NAME_7
			)
			return petEvolutionList[index]

		def GetPetTypeFunc(self, index):
			petTypeList = (localeInfo.PET_TYPE1, localeInfo.PET_TYPE2, localeInfo.PET_TYPE3, localeInfo.PET_TYPE4, localeInfo.PET_TYPE5, localeInfo.PET_TYPE6, localeInfo.PET_TYPE7, localeInfo.PET_TYPE8,
				localeInfo.PET_TYPE9,localeInfo.PET_TYPE10,localeInfo.PET_TYPE11,localeInfo.PET_TYPE12,localeInfo.PET_TYPE13,localeInfo.PET_TYPE14,localeInfo.PET_TYPE15,localeInfo.PET_TYPE16
			)
			return petTypeList[index]

class HyperlinkItemToolTip(ItemToolTip):
	def __init__(self):
		ItemToolTip.__init__(self, isPickable=True)

	def SetHyperlinkItem(self, tokens):
		minTokenCount = 3 + player.METIN_SOCKET_MAX_NUM
		maxTokenCount = minTokenCount + 2 * player.ATTRIBUTE_SLOT_MAX_NUM
		if tokens and minTokenCount <= len(tokens) <= maxTokenCount:
			head, vnum, flag = tokens[:3]
			itemVnum = int(vnum, 16)
			metinSlot = [int(metin, 16) for metin in tokens[3:3 + player.METIN_SOCKET_MAX_NUM]]

			rests = tokens[3 + player.METIN_SOCKET_MAX_NUM:]
			if rests:
				attrSlot = []

				rests.reverse()
				while rests:
					key=int(rests.pop(), 16)
					if rests:
						val=int(rests.pop())
						attrSlot.append((key, val))

				attrSlot+=[(0, 0)] * (player.ATTRIBUTE_SLOT_MAX_NUM - len(attrSlot))
			else:
				attrSlot=[(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM

			self.ClearToolTip()
			self.AddItemData(itemVnum, metinSlot, attrSlot)

			ItemToolTip.OnUpdate(self)

	def OnUpdate(self):
		pass

	def OnMouseLeftButtonDown(self):
		self.Hide()

class SkillToolTip(ToolTip):

	POINT_NAME_DICT = {
		player.LEVEL : localeInfo.SKILL_TOOLTIP_LEVEL,
		player.IQ : localeInfo.SKILL_TOOLTIP_INT,
	}

	SKILL_TOOL_TIP_WIDTH = 200
	PARTY_SKILL_TOOL_TIP_WIDTH = 340

	PARTY_SKILL_EXPERIENCE_AFFECT_LIST = (	( 2, 2,  10,),
											( 8, 3,  20,),
											(14, 4,  30,),
											(22, 5,  45,),
											(28, 6,  60,),
											(34, 7,  80,),
											(38, 8, 100,), )

	PARTY_SKILL_PLUS_GRADE_AFFECT_LIST = (	( 4, 2, 1, 0,),
											(10, 3, 2, 0,),
											(16, 4, 2, 1,),
											(24, 5, 2, 2,), )

	PARTY_SKILL_ATTACKER_AFFECT_LIST = (	( 36, 3, ),
											( 26, 1, ),
											( 32, 2, ), )

	SKILL_GRADE_NAME = {	player.SKILL_GRADE_MASTER : localeInfo.SKILL_GRADE_NAME_MASTER,
							player.SKILL_GRADE_GRAND_MASTER : localeInfo.SKILL_GRADE_NAME_GRAND_MASTER,
							player.SKILL_GRADE_PERFECT_MASTER : localeInfo.SKILL_GRADE_NAME_PERFECT_MASTER, }

	if app.ENABLE_SKILLS_LEVEL_OVER_P:
		SKILL_GRADE_NAME.update({player.SKILL_GRADE_SAGE_MASTER : "%s Sage Master",})
		SKILL_GRADE_NAME.update({player.SKILL_GRADE_LEGENDARY_MASTER : "%s Legendary Master",})


	AFFECT_NAME_DICT =	{
							"HP" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_POWER,
							"ATT_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_GRADE,
							"DEF_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_DEF_GRADE,
							"ATT_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_SPEED,
							"MOV_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_MOV_SPEED,
							"DODGE" : localeInfo.TOOLTIP_SKILL_AFFECT_DODGE,
							"RESIST_NORMAL" : localeInfo.TOOLTIP_SKILL_AFFECT_RESIST_NORMAL,
							"REFLECT_MELEE" : localeInfo.TOOLTIP_SKILL_AFFECT_REFLECT_MELEE,
						}
	AFFECT_APPEND_TEXT_DICT =	{
									"DODGE" : "%",
									"RESIST_NORMAL" : "%",
									"REFLECT_MELEE" : "%",
								}

	if app.ENABLE_PASSIVE_SKILLS:
		PASSIVE_SKILL_DICT = {
			player.SKILL_INDEX_PASSIVE_MONSTER : localeInfo.SKILL_MONSTER_DESCRIPTION,
			player.SKILL_INDEX_PASSIVE_METIN : localeInfo.SKILL_METIN_DESCRIPTION,
			player.SKILL_INDEX_PASSIVE_BERSERKER : localeInfo.SKILL_BERSERKER_DESCRIPTION,
			player.SKILL_INDEX_PASSIVE_HUMAN : localeInfo.SKILL_HUMAN_DESCRIPTION,
			player.SKILL_INDEX_PASSIVE_SKILL_COOLDOWN : localeInfo.SKILL_COOLDOWN_DESCRIPTION,
			player.SKILL_INDEX_PASSIVE_DRAGON_HEARTH : localeInfo.SKILL_DRAGON_HEARTH_DESCRIPTION,
			player.SKILL_INDEX_PASSIVE_HERBOLOGY : localeInfo.SKILL_RESIST_HERBOLOGY_DESCRIPTION,
			player.SKILL_INDEX_PASSIVE_UPGRADING : localeInfo.SKILL_RESIST_UPGRADING_DESCRIPTION,
			player.SKILL_INDEX_PASSIVE_FISHING : localeInfo.SKILL_RESIST_FISHING_DESCRIPTION,
		}

	def __init__(self, *args, **kwargs):
		ToolTip.__init__(self, *args, **kwargs)
	
	def __del__(self):
		ToolTip.__del__(self)

	if app.ENABLE_AFFECT_BUFF_REMOVE:
		def SetSkillEx(self, skillIndex, skillLevel = -1):
			if 0 == skillIndex:
				return
			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillCurrentPercentage), self.ENABLE_COLOR)
			self.ResizeToolTip()

	def SetSkill(self, skillIndex, skillLevel = -1):

		if 0 == skillIndex:
			return

		if skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillGrade = player.GetSkillGrade(slotIndex)
			skillLevel = player.GetSkillLevel(slotIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def SetSkillNew(self, slotIndex, skillIndex, skillGrade, skillLevel):

		if 0 == skillIndex:
			return

		if player.SKILL_INDEX_TONGSOL == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillLevel = player.GetSkillLevel(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendPartySkillData(skillGrade, skillLevel)

		elif player.SKILL_INDEX_RIDING == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			self.AppendSupportSkillDefaultData(skillIndex, skillGrade, skillLevel, 30)

		elif player.SKILL_INDEX_SUMMON == skillIndex:

			maxLevel = 10

			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)

			## Description
			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			if skillLevel == 10:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel*10), self.NORMAL_COLOR)

			else:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.__AppendSummonDescription(skillLevel, self.NORMAL_COLOR)

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel+1), self.NEGATIVE_COLOR)
				self.__AppendSummonDescription(skillLevel+1, self.NEGATIVE_COLOR)

		elif skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		elif skillIndex in self.PASSIVE_SKILL_DICT and app.ENABLE_PASSIVE_SKILLS:
			level_limit = 60
			# self.skillMaxLevelEndDict = { 0: 20, 1 : 10, 2 : 10, 3 : 10, 4 : 10, 5 : 10}
			self.skillMaxLevelEndDict = { 0: 20, 1 : 10, 2 : 10, 3 : 10, 4 : 10}
			# self.dic_string_skill = { 1:" ", 20: "Master", 30: "Grand Master", 40: "Perfect Master", 50:"Sage Master", 60:"Legendary Master" }
			self.dic_string_skill = { 1:" ", 20: "Master", 30: "Grand Master", 40: "Perfect Master", 50:"Sage Master" }

			skillMaxLevelEnd = self.skillMaxLevelEndDict[skillGrade]
			
			if not skillGrade:
				new_skillLevel = skillLevel
			else:
				new_skillLevel = skillLevel+((skillGrade * 10) + 10) - 1
			
			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)

			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
			self.__AppendPassiveSkillDescription(new_skillLevel, skillIndex, self.NORMAL_COLOR)
			if new_skillLevel < 50:
				self.AppendSpace(5)
				if new_skillLevel+1 in self.dic_string_skill:
					self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL.format((self.dic_string_skill[new_skillLevel+1]), self.NEGATIVE_COLOR))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.NEGATIVE_COLOR)
				self.__AppendPassiveSkillDescription(new_skillLevel+1, skillIndex, self.NEGATIVE_COLOR)

			self.AlignHorizonalCenter()

		elif skillIndex == 124 and app.ENABLE_MINING_RENEWAL:
			if not skillGrade:
				new_skillLevel = skillLevel
			else:
				new_skillLevel = skillLevel+((skillGrade * 10) + 10) - 1

			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)
			self.AppendSpace(5)
			# self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL)
			self.AppendMiningSkillDescription(new_skillLevel, skillIndex, self.POSITIVE_COLOR,)
			# self.AlignHorizonalCenter()
			# self.AddTooltipWidth(40)

		else:
			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)

			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex, skillGrade)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def __SetSkillTitle(self, skillIndex, skillGrade):
		if chr.IsGameMaster(0):
			self.AppendTextLine("Skill Vnum: (%d)" % skillIndex, self.TOOLTIP_STUFF_COLOR)
			self.AppendSpace(5)
		self.SetTitle(skill.GetSkillName(skillIndex, skillGrade))
		self.__AppendSkillGradeName(skillIndex, skillGrade)

	def __AppendSkillGradeName(self, skillIndex, skillGrade):
		if self.SKILL_GRADE_NAME.has_key(skillGrade):
			self.AppendSpace(5)
			self.AppendTextLine(self.SKILL_GRADE_NAME[skillGrade] % (skill.GetSkillName(skillIndex, 0)), self.CAN_LEVEL_UP_COLOR)

	def SetSkillOnlyName(self, slotIndex, skillIndex, skillGrade):
		if 0 == skillIndex:
			return

		slotIndex = player.GetSkillSlotIndex(skillIndex)

		self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
		self.ResizeToolTip()

		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)
		self.AppendDefaultData(skillIndex, skillGrade)
		self.AppendSkillConditionData(skillIndex)
		self.ShowToolTip()

	def AppendDefaultData(self, skillIndex, skillGrade = 0):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Level Limit
		levelLimit = skill.GetSkillLevelLimit(skillIndex)
		if levelLimit > 0:

			color = self.NORMAL_COLOR
			if player.GetStatus(player.LEVEL) < levelLimit:
				color = self.NEGATIVE_COLOR

			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (levelLimit), color)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

	def AppendSupportSkillDefaultData(self, skillIndex, skillGrade, skillLevel, maxLevel):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel = 40

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_WITH_MAX % (skillLevel, maxLevel), self.NORMAL_COLOR)

	def AppendSkillConditionData(self, skillIndex):
		conditionDataCount = skill.GetSkillConditionDescriptionCount(skillIndex)
		if conditionDataCount > 0:
			self.AppendSpace(5)
			for i in xrange(conditionDataCount):
				self.AppendTextLine(skill.GetSkillConditionDescription(skillIndex, i), self.CONDITION_COLOR)

	def AppendGuildSkillData(self, skillIndex, skillLevel):
		skillMaxLevel = 7
		skillCurrentPercentage = float(skillLevel) / float(skillMaxLevel)
		skillNextPercentage = float(skillLevel+1) / float(skillMaxLevel)
		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillLevel == skillMaxLevel:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillCurrentPercentage), self.ENABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillCurrentPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.ENABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillCurrentPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.ENABLE_COLOR)

		## Next Level
		if skillLevel < skillMaxLevel:
			if self.HasSkillLevelDescription(skillIndex, skillLevel+1):
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevel), self.DISABLE_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillNextPercentage), self.DISABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillNextPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.DISABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillNextPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.DISABLE_COLOR)

	def AppendSkillDataNew(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage):

		self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
		self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

		if app.ENABLE_SKILLS_LEVEL_OVER_P:
			self.skillMaxLevelStartDict.update({3 : 10,})
			self.skillMaxLevelEndDict.update({3 : 10,})
			# self.skillMaxLevelStartDict.update({3 : 10, 4:10,})
			# self.skillMaxLevelEndDict.update({3 : 10, 4:10,})

		skillLevelUpPoint = 1
		realSkillGrade = player.GetSkillGrade(slotIndex)
		skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
		skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillGrade == skill.SKILL_GRADE_COUNT - 2:
					pass
				elif skillLevel == skillMaxLevelEnd:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.AppendSkillLevelDescriptionNew(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR)

		## Next Level
		if realSkillGrade != skill.SKILL_GRADE_COUNT - 2:
			if skillLevel < skillMaxLevelEnd:
				if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
					self.AppendSpace(5)
					if skillIndex == 141 or skillIndex == 142:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_INT % (skillLevel+1), self.DISABLE_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
					self.AppendSkillLevelDescriptionNew(skillIndex, skillNextPercentage, self.DISABLE_COLOR)

		# if not skillIndex in (121, 122, 123, 124, 125, 126, 137, 138, 139, 140):
		# 	if skillGrade <= 3:
		# 		self.AppendTextLine(localeInfo.SKILL_SET_BONUS_TOOLTIP_AVAIL_FOR_SAGE, self.PURPLE_COLOR)
		# 		self.AppendTextLine(localeInfo.SKILL_SET_BONUS_TOOLTIP_AVAIL_FOR_SAGE2, self.PURPLE_COLOR)
		# 	elif skillGrade == 4:
		# 		self.AppendTextLine(localeInfo.SKILL_SET_BONUS_TOOLTIP, self.ITEM_BUFF_LEVEL_COLOR)
		# 		self.AppendTextLine(localeInfo.SKILL_SET_BONUS_AFFECT_TOOLTIP, self.POSITIVE_COLOR)
		# 		self.AppendTextLine(localeInfo.SKILL_SET_BONUS_AFFECT2_TOOLTIP, self.POSITIVE_COLOR)
				# self.AppendTextLine(localeInfo.SKILL_SET_BONUS_TOOLTIP_AVAIL_FOR_LEGENDARY, self.PURPLE_COLOR)
				# self.AppendTextLine(localeInfo.SKILL_SET_BONUS_TOOLTIP_AVAIL_FOR_LEGENDARY2, self.PURPLE_COLOR)
			# elif skillGrade == 5:
				# self.AppendTextLine(localeInfo.SKILL_SET_BONUS_TOOLTIP2, self.BLUE_COLOR)
				# self.AppendTextLine(localeInfo.SKILL_SET_BONUS_AFFECT3_TOOLTIP,self.POSITIVE_COLOR)
				# self.AppendTextLine(localeInfo.SKILL_SET_BONUS_AFFECT4_TOOLTIP,self.POSITIVE_COLOR)
				# self.AppendTextLine(localeInfo.SKILL_SET_BONUS_AFFECT5_TOOLTIP,self.POSITIVE_COLOR)

	def AppendSkillLevelDescriptionNew(self, skillIndex, skillPercentage, color):

		affectDataCount = skill.GetNewAffectDataCount(skillIndex)
		if affectDataCount > 0:
			for i in xrange(affectDataCount):
				type, minValue, maxValue = skill.GetNewAffectData(skillIndex, i, skillPercentage)

				if not self.AFFECT_NAME_DICT.has_key(type):
					continue

				minValue = int(minValue)
				maxValue = int(maxValue)
				affectText = self.AFFECT_NAME_DICT[type]

				if "HP" == type:
					if minValue < 0 and maxValue < 0:
						minValue *= -1
						maxValue *= -1

					else:
						affectText = localeInfo.TOOLTIP_SKILL_AFFECT_HEAL

				affectText += str(minValue)
				if minValue != maxValue:
					affectText += " - " + str(maxValue)
				affectText += self.AFFECT_APPEND_TEXT_DICT.get(type, "")

				self.AppendTextLine(affectText, color)

		else:
			for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillPercentage), color)


		## Duration
		duration = skill.GetDuration(skillIndex, skillPercentage)
		if duration > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

		## Cooltime
		coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
		if coolTime > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

		## SP
		needSP = skill.GetSkillNeedSP(skillIndex, skillPercentage)
		if needSP != 0:
			continuationSP = skill.GetSkillContinuationSP(skillIndex, skillPercentage)

			if skill.IsUseHPSkill(skillIndex):
				self.AppendNeedHP(needSP, continuationSP, color)
			else:
				self.AppendNeedSP(needSP, continuationSP, color)

	def AppendSkillRequirement(self, skillIndex, skillLevel):

		skillMaxLevel = skill.GetSkillMaxLevel(skillIndex)

		if skillLevel >= skillMaxLevel:
			return

		isAppendHorizontalLine = False

		## Requirement
		if skill.IsSkillRequirement(skillIndex):

			if not isAppendHorizontalLine:
				isAppendHorizontalLine = True
				self.AppendHorizontalLine()

			requireSkillName, requireSkillLevel = skill.GetSkillRequirementData(skillIndex)

			color = self.CANNOT_LEVEL_UP_COLOR
			if skill.CheckRequirementSueccess(skillIndex):
				color = self.CAN_LEVEL_UP_COLOR
			self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_SKILL_LEVEL % (requireSkillName, requireSkillLevel), color)

		## Require Stat
		requireStatCount = skill.GetSkillRequireStatCount(skillIndex)
		if requireStatCount > 0:

			for i in xrange(requireStatCount):
				type, level = skill.GetSkillRequireStatData(skillIndex, i)
				if self.POINT_NAME_DICT.has_key(type):

					if not isAppendHorizontalLine:
						isAppendHorizontalLine = True
						self.AppendHorizontalLine()

					name = self.POINT_NAME_DICT[type]
					color = self.CANNOT_LEVEL_UP_COLOR
					if player.GetStatus(type) >= level:
						color = self.CAN_LEVEL_UP_COLOR
					self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_STAT_LEVEL % (name, level), color)

	def HasSkillLevelDescription(self, skillIndex, skillLevel):
		if skill.GetSkillAffectDescriptionCount(skillIndex) > 0:
			return True
		if skill.GetSkillCoolTime(skillIndex, skillLevel) > 0:
			return True
		if skill.GetSkillNeedSP(skillIndex, skillLevel) > 0:
			return True

		return False

	def AppendMasterAffectDescription(self, index, desc, color):
		self.AppendTextLine(desc, color)

	def AppendNextAffectDescription(self, index, desc):
		self.AppendTextLine(desc, self.DISABLE_COLOR)

	def AppendNeedHP(self, needSP, continuationSP, color):

		self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP_PER_SEC % (continuationSP), color)

	def AppendNeedSP(self, needSP, continuationSP, color):

		if -1 == needSP:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_ALL_SP, color)

		else:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP_PER_SEC % (continuationSP), color)

	def AppendPartySkillData(self, skillGrade, skillLevel):
		# @fixme008 BEGIN
		def comma_fix(vl):
			return vl.replace("%,0f", "%.0f")
		# @fixme008 END

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel =  40
		elif 4 == skillGrade:
			skillLevel =  50

		if skillLevel <= 0:
			return

		skillIndex = player.SKILL_INDEX_TONGSOL
		slotIndex = player.GetSkillSlotIndex(skillIndex)
		skillPower = player.GetSkillCurrentEfficientPercentage(slotIndex)
		k = skillPower # @fixme008
		self.AppendSpace(5)
		self.AutoAppendTextLine(localeInfo.TOOLTIP_PARTY_SKILL_LEVEL % skillLevel, self.NORMAL_COLOR)

		# @fixme008 BEGIN

		if skillLevel>=20:
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_BERSERKER) 	% chop(1 + 5 * k))
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_TANKER) 	% chop(50 + 1450 * k))
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_ATTACKER) % chop( 10 + 60 * k ))

		if skillLevel>=25:
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_BUFFER) % chop(5 + 45 * k ))

		if skillLevel>=35:
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_SKILL_MASTER) % chop(25 + 600 * k ))

		if skillLevel>=40:
			self.AutoAppendTextLine(comma_fix(localeInfo.PARTY_SKILL_DEFENDER) % chop( 5 + 30 * k ))
		# @fixme008 END

		self.AppendSpace(6)
		if skillLevel >=20:
			self.AutoAppendTextLine(localeInfo.CLICK_TO_GET_BONUS, self.ENABLE_COLOR)
		else:
			self.AutoAppendTextLine(localeInfo.NEED_AT_LEAST_M1, self.CONDITION_COLOR)
			self.AutoAppendTextLine(localeInfo.NEED_AT_LEAST_M1_2, self.CONDITION_COLOR)

		self.AlignHorizonalCenter()

	def __AppendSummonDescription(self, skillLevel, color):
		if skillLevel > 1:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel * 10), color)
		elif 1 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (15), color)
		elif 0 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (10), color)

	if app.ENABLE_PASSIVE_SKILLS:
		def __AppendPassiveSkillDescription(self, new_skillLevel, skillIndex, color):
			if skillIndex in xrange(player.SKILL_INDEX_PASSIVE_MONSTER, player.SKILL_INDEX_PASSIVE_METIN+1):
				if new_skillLevel > 1:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (new_skillLevel * 0.24), color)
				elif 1 == new_skillLevel:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (0.24), color)
				elif 0 == new_skillLevel:
					self.AppendTextLine(localeInfo.SKILL_PASSIVE_NOT_LEVEL, color)

			elif skillIndex  == player.SKILL_INDEX_PASSIVE_BERSERKER:
				if new_skillLevel > 1:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (new_skillLevel * 0.24), color)
				elif 1 == new_skillLevel:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (0.24), color)
				elif 0 == new_skillLevel:
					self.AppendTextLine(localeInfo.SKILL_PASSIVE_NOT_LEVEL, color)

			elif skillIndex  == player.SKILL_INDEX_PASSIVE_HUMAN:
				if new_skillLevel > 1:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (new_skillLevel * 0.12), color)
				elif 1 == new_skillLevel:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (0.12), color)
				elif 0 == new_skillLevel:
					self.AppendTextLine(localeInfo.SKILL_PASSIVE_NOT_LEVEL, color)

			elif skillIndex  == player.SKILL_INDEX_PASSIVE_SKILL_COOLDOWN:
				if new_skillLevel > 1:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (new_skillLevel * 72), color)
				elif 1 == new_skillLevel:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (72), color)
				elif 0 == new_skillLevel:
					self.AppendTextLine(localeInfo.SKILL_PASSIVE_NOT_LEVEL, color)

			elif skillIndex  == player.SKILL_INDEX_PASSIVE_DRAGON_HEARTH:
				if new_skillLevel > 1:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (new_skillLevel * 50), color)
				elif 1 == new_skillLevel:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (50), color)
				elif 0 == new_skillLevel:
					self.AppendTextLine(localeInfo.SKILL_PASSIVE_NOT_LEVEL, color)

			elif skillIndex  == player.SKILL_INDEX_PASSIVE_HERBOLOGY:
				if new_skillLevel > 1:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (new_skillLevel * 0.5), color)
				elif 1 == new_skillLevel:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (0.5), color)
				elif 0 == new_skillLevel:
					self.AppendTextLine(localeInfo.SKILL_PASSIVE_NOT_LEVEL, color)

			elif skillIndex  == player.SKILL_INDEX_PASSIVE_UPGRADING:
				if new_skillLevel > 1:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (new_skillLevel * 0.2), color)
				elif 1 == new_skillLevel:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (0.2), color)
				elif 0 == new_skillLevel:
					self.AppendTextLine(localeInfo.SKILL_PASSIVE_NOT_LEVEL, color)

			elif skillIndex  == player.SKILL_INDEX_PASSIVE_FISHING:
				if new_skillLevel > 1:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (new_skillLevel * 0.5), color)
				elif 1 == new_skillLevel:
					self.AppendTextLine(str(self.PASSIVE_SKILL_DICT[skillIndex]) % (0.5), color)
				elif 0 == new_skillLevel:
					self.AppendTextLine(localeInfo.SKILL_PASSIVE_NOT_LEVEL, color)

	if app.ENABLE_MINING_RENEWAL:
		def AppendMiningSkillDescription(self, skillLevel, skillIndex, color):
			if skillIndex is player.SKILL_INDEX_MINING:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				if skillLevel < 10:
					self.AppendHorizontalLine()
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS2)
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + " |cff00C78CLevel 10",)
					return


				if skillLevel >= 10 and skillLevel < 20:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%1", color)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%2", color)

					self.AppendHorizontalLine()
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + " |cff00C78CMaster",)
					#Next bonus
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS,)
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%2", self.DISABLE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%4", self.DISABLE_COLOR)


				elif skillLevel >= 20 and skillLevel < 25:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%2", color)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%4", color)

					self.AppendHorizontalLine()
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + "|cff00C78CMaster Level 5",)
					#Next bonus
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS,)
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%3", self.DISABLE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%6", self.DISABLE_COLOR)

				elif skillLevel >= 25 and skillLevel < 30:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%3", color)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%6", color)

					self.AppendHorizontalLine()
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + "|cff00C78CGrand Master",)
					#Next bonus
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS,)
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%4", self.DISABLE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%8", self.DISABLE_COLOR)

				elif skillLevel >= 30 and skillLevel < 35:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%4", color)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%8", color)

					self.AppendHorizontalLine()
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + " |cff00C78CGrand Master Level 5",)
					#Next bonus
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS,)
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%5", self.DISABLE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%10", self.DISABLE_COLOR)

				elif skillLevel >= 35 and skillLevel < 40:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%5", color)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%10", color)

					self.AppendHorizontalLine()
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + " |cff00C78CPerfect Master",)
					#Next bonus
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS,)
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%6", self.DISABLE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%12", self.DISABLE_COLOR)

				elif skillLevel >= 40 and skillLevel < 45:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%6", color)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%12", color)

					self.AppendHorizontalLine()
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + " |cff00C78CPerfect Master Level 5",)
					#Next bonus
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS,)
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%7", self.DISABLE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%14", self.DISABLE_COLOR)

				elif skillLevel >= 45 and skillLevel < 50:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%7", color)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%14", color)

					self.AppendHorizontalLine()
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + " |cff00C78CSage Master",)
					#Next bonus
					self.AppendTextLine(localeInfo.MINING_NEXT_BONUS,)
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%8", self.DISABLE_COLOR)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%16", self.DISABLE_COLOR)

				elif skillLevel >= 50 and skillLevel < 55:
					self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%8", color)
					self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%16", color)

					# self.AppendHorizontalLine()
					# self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + " |cff00C78CSage Master Level 5",)
					# # #Next bonus
					# self.AppendTextLine(localeInfo.MINING_NEXT_BONUS,)
					# self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%9", self.DISABLE_COLOR)
					# self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%18", self.DISABLE_COLOR)

				# elif skillLevel >= 55 and skillLevel < 60:
				# 	self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%9", color)
				# 	self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%18", color)

				# 	self.AppendHorizontalLine()
				# 	self.AppendTextLine(localeInfo.MINING_NEXT_BONUS_SKILL_LEVEL + " |cff00C78CLegendary Master",)
				# 	#Next bonus
				# 	self.AppendTextLine(localeInfo.MINING_NEXT_BONUS,)
				# 	self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%10", self.DISABLE_COLOR)
				# 	self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%20", self.DISABLE_COLOR)

				# elif skillLevel >= 60:
				# 	self.AppendTextLine(localeInfo.MINING_POINT_TOOLTIP + " +%10", color)
				# 	self.AppendTextLine(localeInfo.MINING_DOUBLE_TOOLTIP + " +%20", color)
