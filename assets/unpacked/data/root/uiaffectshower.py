import ui, localeInfo, chr, app, skill, player, uiToolTip, uiCommon, net, math, uiScriptLocale, constInfo
from _weakref import proxy

if app.ENABLE_AFFECT_BUFF_REMOVE:
	overInImage = None
	affectDict={}
	def TypeToAffect(affect):
		_dict = {
			chr.AFFECT_JEONGWI : 3,
			chr.AFFECT_GEOMGYEONG : 4,
			chr.AFFECT_CHEONGEUN : 19,
			chr.AFFECT_GYEONGGONG : 49,
			chr.AFFECT_EUNHYEONG : 34,
			chr.AFFECT_GWIGEOM : 63,
			chr.AFFECT_GONGPO : 64,
			chr.AFFECT_JUMAGAP : 65,
			chr.AFFECT_HOSIN : 94,
			chr.AFFECT_BOHO : 95,
			chr.AFFECT_KWAESOK : 110,
			chr.AFFECT_HEUKSIN : 79,
			chr.AFFECT_MUYEONG : 78,
			chr.AFFECT_GICHEON : 96,
			chr.AFFECT_JEUNGRYEOK : 111,
			chr.AFFECT_PABEOP : 66,

		}
		return _dict[affect] if _dict.has_key(affect) else affect


class LovePointImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/LovePoint/"
	FILE_DICT = {
		0 : FILE_PATH + "01.dds",
		1 : FILE_PATH + "02.dds",
		2 : FILE_PATH + "02.dds",
		3 : FILE_PATH + "03.dds",
		4 : FILE_PATH + "04.dds",
		5 : FILE_PATH + "05.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetLoverInfo(self, name, lovePoint):
		self.loverName = name
		self.lovePoint = lovePoint
		self.__Refresh()

	def OnUpdateLovePoint(self, lovePoint):
		self.lovePoint = lovePoint
		self.__Refresh()

	def __Refresh(self):
		self.lovePoint = max(0, self.lovePoint)
		self.lovePoint = min(100, self.lovePoint)

		if 0 == self.lovePoint:
			loveGrade = 0
		else:
			loveGrade = self.lovePoint / 25 + 1

		fileName = self.FILE_DICT.get(loveGrade, self.FILE_PATH+"00.dds")

		try:
			self.LoadImage(fileName)
			self.SetScale(1.0, 1.0)
		
		except:
			import dbg
			dbg.TraceError("LovePointImage.SetLoverInfo(lovePoint=%d) - LoadError %s" % (self.lovePoint, fileName))


		self.toolTip.ClearToolTip()
		self.toolTip.SetTitle(self.loverName)
		self.toolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
# END_OF_WEDDING


class HorseImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/HorseState/"

	FILE_DICT = {
		00 : FILE_PATH+"00.dds",
		01 : FILE_PATH+"00.dds",
		02 : FILE_PATH+"00.dds",
		03 : FILE_PATH+"00.dds",
		10 : FILE_PATH+"10.dds",
		11 : FILE_PATH+"11.dds",
		12 : FILE_PATH+"12.dds",
		13 : FILE_PATH+"13.dds",
		20 : FILE_PATH+"20.dds",
		21 : FILE_PATH+"21.dds",
		22 : FILE_PATH+"22.dds",
		23 : FILE_PATH+"23.dds",
		30 : FILE_PATH+"30.dds",
		31 : FILE_PATH+"31.dds",
		32 : FILE_PATH+"32.dds",
		33 : FILE_PATH+"33.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		#self.textLineList = []
		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __GetHorseGrade(self, level):
		if 0 == level:
			return 0

		return (level-1)/10 + 1

	def SetState(self, level, health, battery):
		if self.toolTip:
			self.toolTip.ClearToolTip()

		if level>0:
			try:
				grade = self.__GetHorseGrade(level)
				self.__AppendText(localeInfo.LEVEL_LIST[grade])
			except IndexError:
				return

			try:
				healthName=localeInfo.HEALTH_LIST[health]
				if len(healthName)>0:
					self.__AppendText(healthName)
			except IndexError:
				return

			if health>0:
				if battery==0:
					self.__AppendText(localeInfo.NEEFD_REST)

			try:
				fileName=self.FILE_DICT[health*10+battery]
			except KeyError:
				pass
			try:
				self.LoadImage(fileName)
			except:
					pass
		self.SetScale(1.0, 1.0)

	def __AppendText(self, text):
		if self.toolTip:
			self.toolTip.AppendTextLine(text)
			self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		if self.toolTip:
			self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		if self.toolTip:
			self.toolTip.HideToolTip()

# AUTO_POTION
class AutoPotionImage(ui.ExpandedImageBox):

	FILE_PATH_HP = "d:/ymir work/ui/pattern/auto_hpgauge/"
	FILE_PATH_SP = "d:/ymir work/ui/pattern/auto_spgauge/"

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0
		self.potionType = player.AUTO_POTION_TYPE_HP
		self.filePath = ""

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetPotionType(self, type):
		self.potionType = type

		if player.AUTO_POTION_TYPE_HP == type:
			self.filePath = self.FILE_PATH_HP
		elif player.AUTO_POTION_TYPE_SP == type:
			self.filePath = self.FILE_PATH_SP


	def OnUpdateAutoPotionImage(self):
		self.__Refresh()

	def __Refresh(self):

		isActivated, currentAmount, totalAmount, slotIndex = player.GetAutoPotionInfo(self.potionType)

		amountPercent = (float(currentAmount) / totalAmount) * 100.0
		grade = math.ceil(amountPercent / 20)

		if 5.0 > amountPercent:
			grade = 0

		if 80.0 < amountPercent:
			grade = 4
			if 90.0 < amountPercent:
				grade = 5

		fmt = self.filePath + "%.2d.dds"
		fileName = fmt % grade

		try:
			self.LoadImage(fileName)
		except:
			import dbg
			dbg.TraceError("AutoPotionImage.__Refresh(potionType=%d) - LoadError %s" % (self.potionType, fileName))

		self.SetScale(1.0, 1.0)

		self.toolTip.ClearToolTip()

		if player.AUTO_POTION_TYPE_HP == type:
			self.toolTip.SetTitle(localeInfo.TOOLTIP_AUTO_POTION_HP)
		else:
			self.toolTip.SetTitle(localeInfo.TOOLTIP_AUTO_POTION_SP)

		self.toolTip.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST	% (amountPercent))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
# END_OF_AUTO_POTION


class AffectImage(ui.ExpandedImageBox):

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.HideToolTip()
		self.isSkillAffect = True
		self.description = None
		self.endTime = 0
		self.affect = None
		self.isClocked = True
		if app.ENABLE_AFFECT_BUFF_REMOVE:
			self.buffQuestionDialog = None
			self.skillIndex = None
			self.SetEvent(ui.__mem_func__(self.OnBuffQuestionDialog), "mouse_click")

		self.interface = constInfo.GetInterfaceInstance()

	def SetAffect(self, affect):
		self.affect = affect

	def GetAffect(self):
		return self.affect

	def GetSkillIndex(self):
		return self.skillIndex

	def FormatTime(self, time):
		text = ""

		d = time // (24 * 3600)
		time = time % (24 * 3600)
		h = time // 3600
		time %= 3600
		m = time // 60
		time %= 60
		s = time

		if d:
			text += "%dd " % d
		if text or h:
			text += "%dh " % h
		if text or m:
			text += "%dm " % m
		if text or s:
			text += "%ds " % s

		return text[:-1]

	def SetToolTipText(self, text, x = 0, y = -19):
		self.toolTip.ClearToolTip()
		self.toolTip.AppendSpace(-5)
		self.toolTip.AppendDescription(text, 26)

	def SetDescription(self, description):
		self.description = description
		self.__UpdateDescription2()

	def SetDuration(self, duration):
		self.endTime = 0
		if duration > 0:
			self.endTime = app.GetGlobalTimeStamp() + duration
			leftTime = self.FormatTime(self.endTime - app.GetGlobalTimeStamp())
			self.toolTip.AppendTextLine("(%s : %s)" % (localeInfo.LEFT_TIME, leftTime))
			self.toolTip.ResizeToolTip()
	
	def UpdateAutoPotionDescription(self):
		potionType = player.AUTO_POTION_TYPE_HP if self.affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY\
			else player.AUTO_POTION_TYPE_SP
		isActivated, currentAmount, totalAmount, slotIndex = player.GetAutoPotionInfo(potionType)

		try:
			amountPercent = (float(currentAmount) / totalAmount) * 100.0
		except:
			amountPercent = 100.0

		self.toolTip.childrenList[-1].SetText(self.description % amountPercent)

	def SetClock(self, isClocked):
		self.isClocked = isClocked
		self.SetDescription(self.description)
		
	def UpdateDescription(self):
		if not self.isClocked:
			return
	
		if not self.description:
			return
			
		if self.endTime > 0:
			leftTime = self.FormatTime(self.endTime - app.GetGlobalTimeStamp())

			self.toolTip.childrenList[-1].SetText("(%s : %s)" % (localeInfo.LEFT_TIME, leftTime))

	def __UpdateDescription2(self):
		if not self.description:
			return

		toolTip = self.description
		self.SetToolTipText(toolTip, 0, 40)

	def SetSkillAffectFlag(self, flag):
		self.isSkillAffect = flag

	if app.ENABLE_AFFECT_BUFF_REMOVE:
		def SetSkillIndex(self, skillIndex):
			self.skillIndex = skillIndex

	def IsSkillAffect(self):
		return self.isSkillAffect

	if app.ENABLE_AFFECT_BUFF_REMOVE:
		def OnBuffQuestionDialog(self):

			skillIndex = self.skillIndex
			affectIndex = self.affect

			if skillIndex == -1:
				skillIndex = 0

			potionList = { 534 : localeInfo.TOOLTIP_AUTO_POTION_HP, 535 : localeInfo.TOOLTIP_AUTO_POTION_SP, 551 :localeInfo.TOOLTIP_AUTO_PICK_UP}
			self.buffQuestionDialog = uiCommon.QuestionDialog()

			if affectIndex and not skillIndex and affectIndex in potionList.keys():
				self.buffQuestionDialog.SetText(localeInfo.BUFF_AFFECT_REMOVE_QUESTION2 % (potionList[affectIndex]))
				self.buffQuestionDialog.SetAcceptEvent(lambda arg = affectIndex: self.OnCloseBuffQuestionDialog(arg))
			else:
				if skillIndex:
					self.buffQuestionDialog.SetText(localeInfo.BUFF_AFFECT_REMOVE_QUESTION % (skill.GetSkillName(skillIndex)))
					self.buffQuestionDialog.SetAcceptEvent(lambda arg = skillIndex: self.OnCloseBuffQuestionDialog(arg))
				elif (affectIndex == chr.NEW_AFFECT_POLYMORPH and app.ENABLE_AFFECT_POLYMORPH_REMOVE):
					self.buffQuestionDialog.SetText(localeInfo.BUFF_AFFECT_REMOVE_QUESTION3)
					self.buffQuestionDialog.SetAcceptEvent(lambda arg = chr.NEW_AFFECT_POLYMORPH: self.OnCloseBuffQuestionDialog(arg))
				else:
					return

			self.buffQuestionDialog.SetWidth(350)
			self.buffQuestionDialog.SetCancelEvent(lambda arg = 0: self.OnCloseBuffQuestionDialog(arg))
			self.buffQuestionDialog.Open()
			
		def OnCloseBuffQuestionDialog(self, answer):
			if not self.buffQuestionDialog:
				return

			self.buffQuestionDialog.Close()
			self.buffQuestionDialog = None

			if not answer:
				return

			net.SendChatPacket("/remove_this_buff %d" % answer)
			return True

	def OnMouseOverIn(self):
		if app.ENABLE_AFFECT_BUFF_REMOVE and self.interface:
			tooltip = self.interface.tooltipSkill if self.IsSkillAffect() else self.interface.tooltipItem

			if tooltip:
				tooltip.ClearToolTip()
				global overInImage, affectDict
				overInImage = proxy(self)
				affect = TypeToAffect(self.GetAffect()) if self.IsSkillAffect() else self.GetAffect()

				if affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == 551:
					if affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
						tooltip.AutoAppendNewTextLineResize(localeInfo.TOOLTIP_AUTO_POTION_HP)
					elif affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
						tooltip.AutoAppendNewTextLineResize(localeInfo.TOOLTIP_AUTO_POTION_SP)
					else:
						tooltip.AutoAppendNewTextLineResize(localeInfo.TOOLTIP_AUTO_PICK_UP)
						if self.endTime > 0:
							if self.endTime - app.GetGlobalTimeStamp() < 86400*365:
								tooltip.AutoAppendNewTextLineResize("%s: %s" % (localeInfo.LEFT_TIME, self.FormatTime(self.endTime - app.GetGlobalTimeStamp())), 0xffC5C7C4)
							else:
								tooltip.AutoAppendNewTextLineResize(localeInfo.AFFECT_UNLIMITED_DURATION, 0xffC5C7C4)
    
						# elif maxDuration > 0:
							# if maxDuration - app.GetGlobalTimeStamp() < 86400*365:
								# tooltip.AutoAppendNewTextLineResize("%s: %s" % (localeInfo.LEFT_TIME, self.FormatTime(maxDuration - app.GetGlobalTimeStamp())), 0xffC5C7C4)
							# else:
							# tooltip.AutoAppendNewTextLineResize(localeInfo.AFFECT_UNLIMITED_DURATION, 0xffC5C7C4)

					tooltip.AutoAppendNewTextLineResize(localeInfo.DELETE_AFFECT_TOOLTIP2)

				else:
					affectData = affectDict[affect] if affectDict.has_key(affect) else {}
					affectList = affectData["affect"] if affectData.has_key("affect") else []
					maxDuration = affectData["duration"] if affectData.has_key("duration") else 0

					if self.description:
						tooltip.AutoAppendNewTextLineResize(self.description, 0xffE9E7D2)
						tooltip.AppendSpace(5)

					if self.IsSkillAffect():
						# tooltip.AutoAppendNewTextLineResize(skill.GetSkillName(self.GetSkillIndex()))
						for data in affectList:
							if data[0] != 0 and uiToolTip.ItemToolTip.POINT_DICT.has_key(data[0]):
								tooltip.AutoAppendNewTextLineResize(uiToolTip.ItemToolTip.POINT_DICT[data[0]](data[1]), 0xff95A693)
					else:
						for data in affectList:
							if data[0] != 0 and uiToolTip.ItemToolTip.POINT_DICT.has_key(data[0]):
								tooltip.AutoAppendNewTextLineResize(uiToolTip.ItemToolTip.POINT_DICT[data[0]](data[1]), 0xff95A693)

					if app.ENABLE_NAMING_SCROLL:
						if affect == chr.NEW_AFFECT_NAMING_SCROLL_MOUNT:
							tooltip.AutoAppendNewTextLineResize(localeInfo.NAMING_SCROLL_PERCANTAGE_INCREASE_IN_BONUS_MOUNT.format(affectList[0][1]))

						elif affect == chr.NEW_AFFECT_NAMING_SCROLL_PET:
							tooltip.AutoAppendNewTextLineResize(localeInfo.NAMING_SCROLL_PERCANTAGE_INCREASE_IN_BONUS_PET.format(affectList[0][1]))
						elif affect == chr.NEW_AFFECT_NAMING_SCROLL_BUFFI:
							tooltip.AutoAppendNewTextLineResize(localeInfo.NAMING_SCROLL_PERCANTAGE_INCREASE_IN_BONUS_BUFFI)

					if self.endTime > 0:
						if self.endTime - app.GetGlobalTimeStamp() < 86400*365:
							tooltip.AutoAppendNewTextLineResize("%s: %s" % (localeInfo.LEFT_TIME, self.FormatTime(self.endTime - app.GetGlobalTimeStamp())), 0xffC5C7C4)
						else:
							tooltip.AutoAppendNewTextLineResize(localeInfo.AFFECT_UNLIMITED_DURATION, 0xffC5C7C4)
    
					elif maxDuration > 0:

						if maxDuration - app.GetGlobalTimeStamp() < 86400*365:
							tooltip.AutoAppendNewTextLineResize("%s: %s" % (localeInfo.LEFT_TIME, self.FormatTime(maxDuration - app.GetGlobalTimeStamp())), 0xffC5C7C4)
						else:
							tooltip.AutoAppendNewTextLineResize(localeInfo.AFFECT_UNLIMITED_DURATION, 0xffC5C7C4)

					if self.IsSkillAffect() and self.GetSkillIndex() or affect == chr.NEW_AFFECT_POLYMORPH and not (affect == chr.AFFECT_PARTY_BONUS and app.ENABLE_LEADERSHIP_EXTENSION):
						tooltip.AppendSpace(3)
						tooltip.AutoAppendNewTextLineResize(localeInfo.DELETE_AFFECT_TOOLTIP)

				tooltip.ShowToolTip()

	def OnMouseOverOut(self):
		if app.ENABLE_AFFECT_BUFF_REMOVE:
			global overInImage
			overInImage = None
			
			if self.interface:
				if self.interface.tooltipItem:
					self.interface.tooltipItem.HideToolTip()
    
				if self.interface.tooltipSkill:
					self.interface.tooltipSkill.HideToolTip()
		else:
			if self.toolTipText:
				self.toolTipText.Hide()

class AffectShower(ui.Window):

	MALL_DESC_IDX_START = 1000
	IMAGE_STEP = 24
	IMAGE_STEP_Y = 24
	AFFECT_MAX_NUM = 32
	INFINITE_AFFECT_DURATION = 0x1FFFFFFF 
	END_STRING = "_03"

	AFFECT_DATA_DICT =	{				
			# chr.AFFECT_POISON 									: (localeInfo.SKILL_TOXICDIE, 					"d:/ymir work/ui/skill/common/affect/poison.sub"),
			# chr.AFFECT_SLOW 									: (localeInfo.SKILL_SLOW, 						"d:/ymir work/ui/skill/common/affect/slow.sub"),
			# chr.AFFECT_STUN 									: (localeInfo.SKILL_STUN, 						"d:/ymir work/ui/skill/common/affect/stun.sub"),
			chr.AFFECT_ATT_SPEED_POTION 						: (localeInfo.SKILL_INC_ATKSPD, 				"d:/ymir work/ui/game/new_affects/greenpot.png"),
			chr.AFFECT_MOV_SPEED_POTION 						: (localeInfo.SKILL_INC_MOVSPD, 				"d:/ymir work/ui/game/new_affects/purplepot.png"),
			# chr.AFFECT_FISH_MIND 								: (localeInfo.SKILL_FISHMIND, 					"d:/ymir work/ui/game/new_affects/fishing.png"),
			chr.AFFECT_JEONGWI 									: (localeInfo.SKILL_JEONGWI, 					"d:/ymir work/ui/game/new_affects/skill/skill_3.png",),
			chr.AFFECT_GEOMGYEONG 								: (localeInfo.SKILL_GEOMGYEONG, 				"d:/ymir work/ui/game/new_affects/skill/skill_1.png",),
			chr.AFFECT_CHEONGEUN 								: (localeInfo.SKILL_CHEONGEUN, 					"d:/ymir work/ui/game/new_affects/skill/skill_2.png",),
			chr.AFFECT_GYEONGGONG 								: (localeInfo.SKILL_GYEONGGONG, 				"d:/ymir work/ui/game/new_affects/skill/skill_5.png",),
			chr.AFFECT_EUNHYEONG 								: (localeInfo.SKILL_EUNHYEONG, 					"d:/ymir work/ui/game/new_affects/skill/skill_4.png",),
			chr.AFFECT_GWIGEOM 									: (localeInfo.SKILL_GWIGEOM, 					"d:/ymir work/ui/game/new_affects/skill/skill_11.png",),
			chr.AFFECT_GONGPO 									: (localeInfo.SKILL_GONGPO, 					"d:/ymir work/ui/game/new_affects/skill/skill_12.png",),
			chr.AFFECT_JUMAGAP 									: (localeInfo.SKILL_JUMAGAP, 					"d:/ymir work/ui/game/new_affects/skill/skill_13.png",),
			chr.AFFECT_HOSIN 									: (localeInfo.SKILL_HOSIN, 						"d:/ymir work/ui/game/new_affects/skill/skill_7.png",),
			chr.AFFECT_BOHO 									: (localeInfo.SKILL_BOHO, 						"d:/ymir work/ui/game/new_affects/skill/skill_6.png",),
			chr.AFFECT_KWAESOK 									: (localeInfo.SKILL_KWAESOK, 					"d:/ymir work/ui/game/new_affects/skill/skill_9.png",),
			chr.AFFECT_HEUKSIN 									: (localeInfo.SKILL_HEUKSIN, 					"d:/ymir work/ui/game/new_affects/skill/skill_15.png",),
			chr.AFFECT_MUYEONG 									: (localeInfo.SKILL_MUYEONG, 					"d:/ymir work/ui/game/new_affects/skill/skill_14.png",),
			chr.AFFECT_GICHEON 									: (localeInfo.SKILL_GICHEON, 					"d:/ymir work/ui/game/new_affects/skill/skill_8.png",),
			chr.AFFECT_JEUNGRYEOK 								: (localeInfo.SKILL_JEUNGRYEOK, 				"d:/ymir work/ui/game/new_affects/skill/skill_10.png",),
			chr.AFFECT_PABEOP 									: (localeInfo.SKILL_PABEOP, 					"d:/ymir work/ui/game/new_affects/skill/skill_16.png",),
			chr.AFFECT_FALLEN_CHEONGEUN 						: (localeInfo.SKILL_CHEONGEUN, 					"d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
			chr.AFFECT_FIRE 									: (localeInfo.SKILL_FIRE, 						"d:/ymir work/ui/skill/sura/hwayeom_03.sub",),
			chr.AFFECT_CHINA_FIREWORK 							: (localeInfo.SKILL_POWERFUL_STRIKE,			"d:/ymir work/ui/skill/common/affect/powerfulstrike.sub",),
			chr.NEW_AFFECT_EXP_BONUS 							: (localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC, 	"d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),
			chr.NEW_AFFECT_ITEM_BONUS 							: (localeInfo.TOOLTIP_MALL_ITEMBONUS_STATIC, 	"d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
			chr.NEW_AFFECT_SAFEBOX 								: (localeInfo.TOOLTIP_MALL_SAFEBOX, 			"d:/ymir work/ui/skill/common/affect/safebox.sub",),
			chr.NEW_AFFECT_AUTOLOOT 							: (localeInfo.TOOLTIP_MALL_AUTOLOOT, 			"d:/ymir work/ui/skill/common/affect/autoloot.sub",),
			chr.NEW_AFFECT_FISH_MIND 							: (localeInfo.TOOLTIP_MALL_FISH_MIND, 			"d:/ymir work/ui/game/new_affects/fishing.png",),
			chr.NEW_AFFECT_MARRIAGE_FAST 						: (localeInfo.TOOLTIP_MALL_MARRIAGE_FAST, 		"d:/ymir work/ui/skill/common/affect/marriage_fast.sub",),
			chr.NEW_AFFECT_GOLD_BONUS 							: (localeInfo.TOOLTIP_MALL_GOLDBONUS_STATIC, 	"d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),
			chr.NEW_AFFECT_NO_DEATH_PENALTY 					: (localeInfo.TOOLTIP_APPLY_NO_DEATH_PENALTY, 	"d:/ymir work/ui/skill/common/affect/gold_premium.sub",),
			chr.NEW_AFFECT_SKILL_BOOK_BONUS 					: (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_BONUS, 	"d:/ymir work/ui/skill/common/affect/gold_premium.sub",),
			chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY					: (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_NO_DELAY,"d:/ymir work/ui/skill/common/affect/gold_premium.sub",),
			chr.NEW_AFFECT_AUTO_HP_RECOVERY 					: (localeInfo.TOOLTIP_AUTO_POTION_REST, 		"d:/ymir work/ui/game/new_affects/redpot.png",),
			chr.NEW_AFFECT_AUTO_SP_RECOVERY 					: (localeInfo.TOOLTIP_AUTO_POTION_REST, 		"d:/ymir work/ui/game/new_affects/bluepot.png",),

			MALL_DESC_IDX_START+player.POINT_MALL_ATTBONUS 		: (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, 	"d:/ymir work/ui/skill/common/affect/att_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_DEFBONUS 		: (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, 	"d:/ymir work/ui/skill/common/affect/def_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_EXPBONUS 		: (localeInfo.TOOLTIP_MALL_EXPBONUS2, 			"d:/ymir work/ui/game/new_affects/bilgelik.png",),
			MALL_DESC_IDX_START+player.POINT_MALL_ITEMBONUS 	: (localeInfo.TOOLTIP_MALL_ITEMBONUS, 			"d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_GOLDBONUS 	: (localeInfo.TOOLTIP_MALL_GOLDBONUS, 			"d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_CRITICAL_PCT 		: (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,		"d:/ymir work/ui/skill/common/affect/critical.sub"),
			MALL_DESC_IDX_START+player.POINT_PENETRATE_PCT 		: (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,		"d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			MALL_DESC_IDX_START+player.POINT_MAX_HP_PCT 		: (localeInfo.TOOLTIP_MAX_HP_PCT, 				"d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			MALL_DESC_IDX_START+player.POINT_MAX_SP_PCT 		: (localeInfo.TOOLTIP_MAX_SP_PCT, 				"d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
	}
	if app.ENABLE_DRAGON_SOUL_SYSTEM:
	# 	AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK1] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK1, "d:/ymir work/ui/game/new_affects/buff_ds_sky.png",),
	# 	AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK2] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK2, "d:/ymir work/ui/game/new_affects/buff_ds_land.png"),

		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK1] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK1, "d:/ymir work/ui/game/new_affects/buff_ds_sky.png")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK2] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK2, "d:/ymir work/ui/game/new_affects/buff_ds_land.png")

	if app.ENABLE_DS_SET_BONUS:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DS_SET] = (localeInfo.TOOLTIP_DS_SET, "d:/ymir work/ui/game/new_affects/setbonus.png")

	if app.ENABLE_NAMING_SCROLL:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_NAMING_SCROLL_MOUNT] = (localeInfo.TOOLTIP_NAMING_SCROLL_MOUNT, "d:/ymir work/ui/game/new_affects/mountname.png")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_NAMING_SCROLL_PET] = (localeInfo.TOOLTIP_NAMING_SCROLL_PET, "d:/ymir work/ui/game/new_affects/petname.png")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_NAMING_SCROLL_BUFFI] = (localeInfo.TOOLTIP_NAMING_SCROLL_BUFFI, "d:/ymir work/ui/game/new_affects/shamanname.png")

	if app.ENABLE_PREMIUM_MEMBER_SYSTEM:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_PREMIUM] = (localeInfo.TOOLTIP_SYSTEM_PREMIUM, "d:/ymir work/ui/game/new_affects/premium.png")
		AFFECT_DATA_DICT[551] = (localeInfo.TOOLTIP_SYSTEM_AUTO_PICKUP, "d:/ymir work/ui/game/new_affects/pick.png")

	if app.ENABLE_METIN_QUEUE:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_METIN_QUEUE] = (localeInfo.TOOLTIP_SYSTEM_METIN_QUEUE, "d:/ymir work/ui/game/new_affects/metin.png")

	if app.ENABLE_VOTE4BUFF:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_VOTE4BUFF] = (localeInfo.TOOLTIP_SYSTEM_V4B, "d:/ymir work/ui/game/new_affects/vote.png")

	if app.ENABLE_EXTENDED_BATTLE_PASS:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_BATTLEPASS] = (localeInfo.BATTLEPASS_DESC, "d:/ymir work/ui/game/new_affects/battlepass.png")
	if app.ENABLE_ADDSTONE_NOT_FAIL_ITEM:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_SUCCESS_ADDSTONE] = (localeInfo.ADDSTONE_PREMIUM_DESC, "d:/ymir work/ui/game/new_affects/stone_chance.png")

	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DATA_DICT[chr.AFFECT_BLEEDING] = (localeInfo.SKILL_BLEEDING, "d:/ymir work/ui/skill/common/affect/poison.sub")
		AFFECT_DATA_DICT[chr.AFFECT_RED_POSSESSION] = (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/wolfman/red_possession" + END_STRING + ".sub",)
		AFFECT_DATA_DICT[chr.AFFECT_BLUE_POSSESSION] = (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/wolfman/blue_possession" + END_STRING + ".sub",)

	if app.ENABLE_NEW_BLEND_AFFECT:
		AFFECT_DATA_DICT[chr.AFFECT_BLEND_POTION_1] = (localeInfo.TOOLTIP_AFFECT_BLEND_POTION_1, "d:/ymir work/ui/game/new_affects/" + "reddew" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_BLEND_POTION_2] = (localeInfo.TOOLTIP_AFFECT_BLEND_POTION_2, "d:/ymir work/ui/game/new_affects/" + "orangedew" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_BLEND_POTION_3] = (localeInfo.TOOLTIP_AFFECT_BLEND_POTION_3, "d:/ymir work/ui/game/new_affects/" + "yellowdew" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_BLEND_POTION_4] = (localeInfo.TOOLTIP_AFFECT_BLEND_POTION_4, "d:/ymir work/ui/game/new_affects/" + "greendew" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_BLEND_POTION_5] = (localeInfo.TOOLTIP_AFFECT_BLEND_POTION_5, "d:/ymir work/ui/game/new_affects/" + "bluedew" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_BLEND_POTION_6] = (localeInfo.TOOLTIP_AFFECT_BLEND_POTION_6, "d:/ymir work/ui/game/new_affects/" + "whitedew" + ".png")

		AFFECT_DATA_DICT[chr.AFFECT_BLEND_POTION_7] = (localeInfo.TOOLTIP_AFFECT_BLEND_POTION_7, "d:/ymir work/ui/game/new_affects/" + "pinkdew" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_BLEND_POTION_8] = (localeInfo.TOOLTIP_AFFECT_BLEND_POTION_8, "d:/ymir work/ui/game/new_affects/" + "turqoisedew" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_BLEND_POTION_9] = (localeInfo.TOOLTIP_AFFECT_BLEND_POTION_9, "d:/ymir work/ui/game/new_affects/" + "blackdew" + ".png")

		AFFECT_DATA_DICT[chr.AFFECT_ENERGY] = (localeInfo.TOOLTIP_AFFECT_ENERGY, "d:/ymir work/ui/game/new_affects/" + "energy" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_DRAGON_GOD_1] = (localeInfo.TOOLTIP_AFFECT_DRAGON_GOD_1, "d:/ymir work/ui/game/new_affects/" + "mark_1" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_DRAGON_GOD_2] = (localeInfo.TOOLTIP_AFFECT_DRAGON_GOD_2, "d:/ymir work/ui/game/new_affects/" + "mark_2" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_DRAGON_GOD_3] = (localeInfo.TOOLTIP_AFFECT_DRAGON_GOD_3, "d:/ymir work/ui/game/new_affects/" + "mark_3" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_DRAGON_GOD_4] = (localeInfo.TOOLTIP_AFFECT_DRAGON_GOD_4, "d:/ymir work/ui/game/new_affects/" + "mark_4" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_CRITICAL] = (localeInfo.TOOLTIP_AFFECT_CRITICAL, "d:/ymir work/ui/game/new_affects/" + "critic" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_PENETRATE] = (localeInfo.TOOLTIP_AFFECT_PENETRATE, "d:/ymir work/ui/game/new_affects/" + "penetration" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_ATTACK_SPEED] = (localeInfo.TOOLTIP_AFFECT_ATTACK_SPEED, "d:/ymir work/ui/game/new_affects/" + "greenpot" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_MOVE_SPEED] = (localeInfo.TOOLTIP_AFFECT_MOVE_SPEED, "d:/ymir work/ui/game/new_affects/" + "purplepot" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_WATER_POTION_1] = (localeInfo.TOOLTIP_AFFECT_WATER_POTION_1, "d:/ymir work/ui/game/new_affects/" + "w1" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_WATER_POTION_2] = (localeInfo.TOOLTIP_AFFECT_WATER_POTION_2, "d:/ymir work/ui/game/new_affects/" + "w2"+ ".png")

		AFFECT_DATA_DICT[chr.AFFECT_POTION_ELEMENT_ICE] = (localeInfo.TOOLTIP_AFFECT_ELEMENT_ICE, "d:/ymir work/ui/game/new_affects/" + "super_ice" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_POTION_ELEMENT_FIRE] = (localeInfo.TOOLTIP_AFFECT_ELEMENT_FIRE, "d:/ymir work/ui/game/new_affects/" + "super_fire" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_POTION_ELEMENT_WIND] = (localeInfo.TOOLTIP_AFFECT_ELEMENT_WIND, "d:/ymir work/ui/game/new_affects/" + "super_wind" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_POTION_ELEMENT_DARK] = (localeInfo.TOOLTIP_AFFECT_ELEMENT_DARK, "d:/ymir work/ui/game/new_affects/" + "super_dark" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_POTION_ELEMENT_ELEC] = (localeInfo.TOOLTIP_AFFECT_ELEMENT_ELEC, "d:/ymir work/ui/game/new_affects/" + "super_elec" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_POTION_ELEMENT_EARTH] = (localeInfo.TOOLTIP_AFFECT_ELEMENT_EARTH, "d:/ymir work/ui/game/new_affects/" + "super_earth" + ".png")

		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_01] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_01, "d:/ymir work/ui/game/new_affects/" + "balik1" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_02] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_02, "d:/ymir work/ui/game/new_affects/" + "balik2" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_03] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_03, "d:/ymir work/ui/game/new_affects/" + "balik3" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_04] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_04, "d:/ymir work/ui/game/new_affects/" + "balik4" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_05] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_05, "d:/ymir work/ui/game/new_affects/" + "balik5" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_06] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_06, "d:/ymir work/ui/game/new_affects/" + "balik6" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_07] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_07, "d:/ymir work/ui/game/new_affects/" + "balik7" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_08] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_08, "d:/ymir work/ui/game/new_affects/" + "balik8" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_09] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_09, "d:/ymir work/ui/game/new_affects/" + "balik9" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_10] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_10, "d:/ymir work/ui/game/new_affects/" + "balik10" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_11] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_11, "d:/ymir work/ui/game/new_affects/" + "balik11" + ".png")
		AFFECT_DATA_DICT[chr.AFFECT_FISH_ITEM_12] = (localeInfo.TOOLTIP_AFFECT_FISH_ITEM_12, "d:/ymir work/ui/game/new_affects/" + "balik12" + ".png")


	if app.ENABLE_AFFECT_POLYMORPH_REMOVE:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_POLYMORPH] =  (localeInfo.POLYMORPH_AFFECT_TOOLTIP, "d:/ymir work/ui/game/new_affects/polyicon.png")

	if app.ENABLE_LEADERSHIP_EXTENSION:
		AFFECT_DATA_DICT[chr.AFFECT_PARTY_BONUS] = (uiScriptLocale.GUILD_INFO_MASTER, "d:/ymir work/ui/game/new_affects/leader.png")

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.ClearAllAffects()
		self.serverPlayTime=0
		self.clientPlayTime=0
		self.lastUpdateTime=0
		if app.ENABLE_AFFECT_BUFF_REMOVE:
			global affectDict, overInImage
			affectDict={}
			overInImage=None
		self.horseImage=None
		self.lovePointImage=None

	def __init__(self):
		ui.Window.__init__(self)
		self.interface = None
		self.serverPlayTime=0
		self.clientPlayTime=0

		self.lastUpdateTime=0
		self.affectImageDict={}
		self.horseImage=None
		self.lovePointImage=None
		self.autoPotionImageHP = AutoPotionImage()
		self.autoPotionImageSP = AutoPotionImage()
		self.SetPosition(10, 10)
		self.Show()

	def BindInterface(self, interface):
		self.interface = proxy(interface)

	def ClearAllAffects(self):
		self.horseImage=None
		self.lovePointImage=None
		self.affectImageDict={}
		self.__ArrangeImageList()

	def ClearAffects(self):
		self.living_affectImageDict={}
		for key, image in self.affectImageDict.items():
			if not image.IsSkillAffect():
				self.living_affectImageDict[key] = image
		self.affectImageDict = self.living_affectImageDict
		self.__ArrangeImageList()

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		
		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		else:
			affect = type

		if self.affectImageDict.has_key(affect):
			return

		if app.ENABLE_AFFECT_BUFF_REMOVE:
			global affectDict
			affectNew = self.AffectToRealIndex(affect)
			affectData = affectDict[affectNew] if affectDict.has_key(affectNew) else {}
			affectList = affectData["affect"] if affectData.has_key("affect") else []
			maxDuration = affectData["duration"] if affectData.has_key("duration") else 0
			if not [pointIdx, value] in affectList:
				affectList.append([pointIdx, value])
			if duration+app.GetGlobalTimeStamp() > maxDuration:
				affectData["duration"] = duration+app.GetGlobalTimeStamp()
			affectData["affect"] = affectList
			affectDict[affectNew] = affectData

		if app.ENABLE_NEW_BLEND_AFFECT:
			if type < 500 and\
				not type == chr.NEW_AFFECT_POLYMORPH and\
				not type == chr.AFFECT_BLEND_POTION_1 and\
				not type == chr.AFFECT_BLEND_POTION_2 and\
				not type == chr.AFFECT_BLEND_POTION_3 and\
				not type == chr.AFFECT_BLEND_POTION_4 and\
				not type == chr.AFFECT_BLEND_POTION_5 and\
				not type == chr.AFFECT_BLEND_POTION_6 and\
				not type == chr.AFFECT_BLEND_POTION_7 and\
				not type == chr.AFFECT_BLEND_POTION_8 and\
				not type == chr.AFFECT_BLEND_POTION_9 and\
				not type == chr.AFFECT_ENERGY and\
				not type == chr.AFFECT_DRAGON_GOD_1 and\
				not type == chr.AFFECT_DRAGON_GOD_2 and\
				not type == chr.AFFECT_DRAGON_GOD_3 and\
				not type == chr.AFFECT_DRAGON_GOD_4 and\
				not type == chr.AFFECT_CRITICAL and\
				not type == chr.AFFECT_PENETRATE and\
				not type == chr.AFFECT_ATTACK_SPEED and\
				not type == chr.AFFECT_MOVE_SPEED and\
				not type == chr.AFFECT_WATER_POTION_1 and\
				not type == chr.AFFECT_WATER_POTION_2 and\
				not type == chr.AFFECT_POTION_ELEMENT_ICE and\
				not type == chr.AFFECT_POTION_ELEMENT_FIRE and\
				not type == chr.AFFECT_POTION_ELEMENT_WIND and\
				not type == chr.AFFECT_POTION_ELEMENT_DARK and\
				not type == chr.AFFECT_POTION_ELEMENT_ELEC and\
				not type == chr.AFFECT_POTION_ELEMENT_EARTH and\
				not type == chr.AFFECT_FISH_ITEM_01 and\
				not type == chr.AFFECT_FISH_ITEM_02 and\
				not type == chr.AFFECT_FISH_ITEM_03 and\
				not type == chr.AFFECT_FISH_ITEM_04 and\
				not type == chr.AFFECT_FISH_ITEM_05 and\
				not type == chr.AFFECT_FISH_ITEM_06 and\
				not type == chr.AFFECT_FISH_ITEM_07 and\
				not type == chr.AFFECT_FISH_ITEM_08 and\
				not type == chr.AFFECT_FISH_ITEM_09 and\
				not type == chr.AFFECT_FISH_ITEM_10 and\
				not type == chr.AFFECT_FISH_ITEM_11 and\
				not type == chr.AFFECT_FISH_ITEM_12:
				return
		else:
			if type < 500:
				return

		if self.affectImageDict.has_key(affect):
			return

		if not self.AFFECT_DATA_DICT.has_key(affect):
			return

		try:
			value = float(value)
		except Exception:
			if isinstance(value, str):
				return

		if affect == chr.NEW_AFFECT_NO_DEATH_PENALTY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_BONUS or\
		   affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or\
		   affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY:
			duration = 0

		affectData = self.AFFECT_DATA_DICT[affect]

		description = affectData[0]
		filename = affectData[1]

		if app.ENABLE_NAMING_SCROLL:
			if affect == chr.NEW_AFFECT_NAMING_SCROLL_MOUNT:
				constInfo.NAMING_BONUS_RATES[0] = float(value)
			if affect == chr.NEW_AFFECT_NAMING_SCROLL_PET:
				constInfo.NAMING_BONUS_RATES[1] = float(value)

		if pointIdx == player.POINT_MALL_ITEMBONUS or\
		   pointIdx == player.POINT_MALL_GOLDBONUS:
			value = 1 + float(value) / 100.0

		else:

			if affect != chr.NEW_AFFECT_AUTO_SP_RECOVERY and affect != chr.NEW_AFFECT_AUTO_HP_RECOVERY:
				# TODO: Get rid of these wrappers...
				if callable(affectData[0]):
					description = affectData[0](float(value))
				else:
					try:
						description = affectData[0] % value
					except TypeError:
						description = affectData[0]
					except ValueError:
						description = affectData[0]

		try:
			image = AffectImage()
			image.SetParent(self)
			image.LoadImage(filename)
			image.SetDescription(description)
			image.SetDuration(duration)
			image.SetAffect(affect)
			if affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE or\
				affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE_UNDER_15 or\
				self.INFINITE_AFFECT_DURATION < duration:
				image.SetClock(False)
				image.UpdateDescription()
			elif affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
				image.UpdateAutoPotionDescription()
			else:
				image.UpdateDescription()

			image.SetScale(1.0, 1.0)
			image.SetSkillAffectFlag(False)
			image.Show()
			self.affectImageDict[affect] = image
			self.__ArrangeImageList()
		except Exception, e:
			pass

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		else:
			affect = type

		if app.ENABLE_AFFECT_BUFF_REMOVE:
			global affectDict
			affectNew = self.AffectToRealIndex(affect)
			affectData = affectDict[affectNew] if affectDict.has_key(affectNew) else {}
			affectList = affectData["affect"] if affectData.has_key("affect") else []
			removeIndex = -1
			for data in affectList:
				if data[0] == pointIdx:
					removeIndex = affectList.index(data)
					break
			if removeIndex != -1:
				del affectList[removeIndex]
				affectData["affect"] = affectList
				affectDict[affectNew] = affectData

		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetAffect(self, affect):
		self.__AppendAffect(affect)
		self.__ArrangeImageList()

	def ResetAffect(self, affect):
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetLoverInfo(self, name, lovePoint):
		image = LovePointImage()
		image.SetParent(self)
		image.SetLoverInfo(name, lovePoint)
		self.lovePointImage = image
		self.__ArrangeImageList()

	def ShowLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Show()
			self.__ArrangeImageList()

	def HideLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Hide()
			self.__ArrangeImageList()

	def ClearLoverState(self):
		self.lovePointImage = None
		self.__ArrangeImageList()

	def OnUpdateLovePoint(self, lovePoint):
		if self.lovePointImage:
			self.lovePointImage.OnUpdateLovePoint(lovePoint)

	def SetHorseState(self, level, health, battery):
		if level==0:
			self.horseImage=None
		else:
			image = HorseImage()
			image.SetParent(self)
			image.SetState(level, health, battery)
			image.Show()

			self.horseImage=image
		self.__ArrangeImageList()

	def SetPlayTime(self, playTime):
		self.serverPlayTime = playTime
		self.clientPlayTime = app.GetTime()

	def __AppendAffect(self, affect):
		if self.affectImageDict.has_key(affect):
			return

		try:
			affectData=self.AFFECT_DATA_DICT[affect]
		except KeyError:
			return

		name=affectData[0]
		filename=affectData[1]

		skillIndex=player.AffectIndexToSkillIndex(affect)

		if 0 !=skillIndex:
			name=skill.GetSkillName(skillIndex)

		image=AffectImage()
		image.SetParent(self)
		image.SetSkillAffectFlag(True)
		image.SetAffect(affect)
		image.SetDescription(name)
		if app.ENABLE_AFFECT_BUFF_REMOVE:
			image.SetSkillIndex(skillIndex)
			
		try:
			image.LoadImage(filename)
		except:
			pass

		image.SetToolTipText(name, 0, 40)
		image.SetScale(1.0, 1.0)
		image.Show()

		self.affectImageDict[affect]=image

	def __RemoveAffect(self, affect):

		if not self.affectImageDict.has_key(affect):
			return

		del self.affectImageDict[affect]

		self.__ArrangeImageList()

	def __ArrangeImageList(self):
		width = len(self.affectImageDict) * self.IMAGE_STEP
		countSkillImage = 0
		
		if self.lovePointImage and self.lovePointImage.IsShow():
			width += self.IMAGE_STEP
			countSkillImage += 1

		if self.horseImage and self.horseImage.IsShow():
			width += self.IMAGE_STEP
			countSkillImage += 1

		self.SetSize(width, self.IMAGE_STEP_Y)


		for image in self.affectImageDict.values():
			if image.IsSkillAffect():
				countSkillImage += 1
		yPos = 0 if countSkillImage == 0 else self.IMAGE_STEP
		xSkillPos = 0
		xPos = 0
		AffectCount = 0
		
		if self.lovePointImage and self.lovePointImage.IsShow():
			self.lovePointImage.SetPosition(xSkillPos, 0)
			xSkillPos += self.IMAGE_STEP

		if self.horseImage and self.horseImage.IsShow():
			self.horseImage.SetPosition(xSkillPos, 0)
			xSkillPos += self.IMAGE_STEP

		for image in self.affectImageDict.values():
			if image.IsSkillAffect():
				image.SetPosition(xSkillPos, 0)
				xSkillPos += self.IMAGE_STEP
			else:
				image.SetPosition(xPos, yPos)
				AffectCount += 1
				xPos += self.IMAGE_STEP
				
				if AffectCount % 8 == 0:
					yPos += self.IMAGE_STEP
					xPos = 0
			
			self.SetSize(8 * self.IMAGE_STEP, yPos + self.IMAGE_STEP)
		
		if self.interface and self.interface.wndParty:
			totalSkillAffects = countSkillImage
			totalOthersAffects = AffectCount
			totalAffects = totalSkillAffects + totalOthersAffects
			
			row_count = (self.GetLastEffectPosition()/self.IMAGE_STEP)
			
			canResize = (totalSkillAffects > 0 and totalOthersAffects > 0) or (totalOthersAffects > 10)
			self.interface.wndParty.UpdateAffectPosition(canResize, (row_count * self.IMAGE_STEP))

	def GetLastEffectPosition(self):
		new_y = 0
		for image in self.affectImageDict.values():
			image_pos_Y = image.GetLocalPosition()[1]
			if image_pos_Y > new_y:
				new_y = image_pos_Y
		
		return new_y
	
	def OnUpdate(self):
		try:
			if app.GetGlobalTime() - self.lastUpdateTime > 500:
				self.lastUpdateTime = app.GetGlobalTime()
				if app.ENABLE_AFFECT_BUFF_REMOVE:
					global overInImage
					if overInImage:
						overInImage.OnMouseOverIn()
				else:
					for image in self.affectImageDict.values():
						if image.GetAffect() == chr.NEW_AFFECT_AUTO_HP_RECOVERY or image.GetAffect() == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
							image.UpdateAutoPotionDescription()
							continue
						if not image.IsSkillAffect():
							image.UpdateDescription()
		except Exception, e:
			pass


	if app.ENABLE_AFFECT_BUFF_REMOVE:
		def AffectToRealIndex(self, affect):
			_dict = {
				209:chr.AFFECT_POISON,
				211:chr.AFFECT_SLOW,
				210:chr.AFFECT_STUN,
				201:chr.AFFECT_ATT_SPEED_POTION,
				200:chr.AFFECT_MOV_SPEED_POTION,
				208:chr.AFFECT_FISH_MIND,
			}
			return _dict[affect] if _dict.has_key(affect) else affect
