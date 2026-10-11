import ui, item, localeInfo, uiToolTip, chat, \
    app, renderTarget, player, petskill, grp, newpet
    
PATH_ROOT = "offlineshop/lightwork/searchshop/"

PET_SYSTEM_DIR = "d:/ymir work/ui/game/petsystem/"

PET_EVOLUTION_TABLE = (
	(40,1, 55120, 10 ),
	(60,2, 55121, 20),
	(80,3, 55122, 30 )
)

PET_SKIN_ITEM_VNUM_LIST = (55130, 55131, 55132, 55133, 55134)

class PetWindow(ui.BoardWithTitleBar):

	RENDER_TARGET_INDEX = 69

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.Constructor()
		self.LoadGui()
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
		self.toolTipInfo = None

	def Open(self):
		self.Show()
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, self.petSkinLevel)

	def LoadGui(self):
		self.SetSize(610, 400)
		self.SetCenterPosition()
		self.AddFlag('movable')
		self.SetTitleName(localeInfo.PET_INFORMATIONS_TITLE)
		self.SetCloseEvent(self.Close)

		self.loadRenderTarget()

		self.titleBorder = ui.BorderA()
		self.titleBorder.SetParent(self.wndRender)
		self.titleBorder.SetPosition(280, 0)
		self.titleBorder.SetSize(300, 15)
		self.titleBorder.Show()

		self.petInformationsTitle = ui.TextLine()
		self.petInformationsTitle.SetParent(self.titleBorder)
		self.petInformationsTitle.SetPosition(90, 9)
		self.petInformationsTitle.SetText(localeInfo.PET_INFORMATIONS_TITLE2)
		self.petInformationsTitle.SetFontName(localeInfo.GetDefaultFont() if app.ENABLE_FONT_SELECT else localeInfo.UI_DEF_FONT)
		self.petInformationsTitle.Show()

		self.InformationButton = ui.MakeButton(self, 492, 44, False, "d:/ymir work/ui/pattern/", "q_mark_01.tga", "q_mark_01.tga", "q_mark_01.tga")
		self.InformationButton.ShowToolTip = ui.__mem_func__(self.OverInInformations)
		self.InformationButton.HideToolTip = ui.__mem_func__(self.OverInOutTooltip)

		self.experienceBorder = ui.BorderA()
		self.experienceBorder.SetParent(self.titleBorder)
		self.experienceBorder.SetPosition(0, 35)
		self.experienceBorder.SetSize(300, 50)
		self.experienceBorder.Show()

		self.experienceTitle = ui.TextLine()
		self.experienceTitle.SetParent(self.experienceBorder)
		self.experienceTitle.SetPosition(95, 9)
		self.experienceTitle.SetText(localeInfo.PET_INFORMATION_EXPERIENCE.format(1))
		self.experienceTitle.SetFontName(localeInfo.GetDefaultFont() if app.ENABLE_FONT_SELECT else localeInfo.UI_DEF_FONT)
		self.experienceTitle.Show()

		self.remainingTimeGauge = ui.Gauge()
		self.remainingTimeGauge.SetParent(self.experienceBorder)
		self.remainingTimeGauge.MakeGauge(220, "yellow")
		self.remainingTimeGauge.SetPosition(37, 32)
		self.remainingTimeGauge.Show()

		self.starBorder = ui.BorderA()
		self.starBorder.SetParent(self.experienceBorder)
		self.starBorder.SetPosition(0, 55)
		self.starBorder.SetSize(300, 50)
		self.starBorder.Show()

		for star in xrange(10):
			self.starList.append(star)
			self.starList[star] = ui.ExpandedImageBox()
			self.starList[star].SetParent(self)
			self.starList[star].SetPosition(304.5 + (star * 28), 135)
			self.starList[star].LoadImage(PET_SYSTEM_DIR + "star_empty.png")
			self.starList[star].OnMouseOverIn = ui.__mem_func__(self.OverInStar)
			self.starList[star].OnMouseOverIn = lambda arg = star : self.OverInStar(arg)
			self.starList[star].OnMouseOverOut = ui.__mem_func__(self.OverInOutTooltip)
			self.starList[star].Show()

		self.infoBorder = ui.BorderA()
		self.infoBorder.SetParent(self.starBorder)
		self.infoBorder.SetPosition(0, 55)
		self.infoBorder.SetSize(300, 70)
		self.infoBorder.Show()

		for attrImage in xrange(len(self.petAttrList)):

			self.petAttrImageTitleList.append(attrImage)
			self.petAttrImageTitleList[attrImage] = ui.ExpandedImageBox()
			self.petAttrImageTitleList[attrImage].SetParent(self.infoBorder)
			self.petAttrImageTitleList[attrImage].SetPosition(11 + attrImage * 94, 10)
			self.petAttrImageTitleList[attrImage].LoadImage(PET_SYSTEM_DIR + "image.png")
			self.petAttrImageTitleList[attrImage].Show()

			self.petAttrImageList.append(attrImage)
			self.petAttrImageList[attrImage] = ui.ExpandedImageBox()
			self.petAttrImageList[attrImage].SetParent(self.petAttrImageTitleList[attrImage])
			self.petAttrImageList[attrImage].SetPosition(0, 25)
			self.petAttrImageList[attrImage].LoadImage(PET_SYSTEM_DIR + "image_black.png")
			self.petAttrImageList[attrImage].Show()

			self.petAttrTextList.append(attrImage)
			self.petAttrTextList[attrImage] = ui.TextLine()
			self.petAttrTextList[attrImage].SetParent(self.petAttrImageTitleList[attrImage])

			if attrImage is 0:
				self.petAttrTextList[attrImage].SetPosition(21, 3)
			elif attrImage is 1:
				self.petAttrTextList[attrImage].SetPosition(13, 3)
			else:
				self.petAttrTextList[attrImage].SetPosition(7, 3)

			self.petAttrTextList[attrImage].SetText(self.petAttrList[attrImage])	
			self.petAttrTextList[attrImage].SetFontName(localeInfo.GetDefaultFont() if app.ENABLE_FONT_SELECT else localeInfo.UI_DEF_FONT)
			self.petAttrTextList[attrImage].SetPosition(0, 0)
			self.petAttrTextList[attrImage].SetHorizontalAlignCenter()
			self.petAttrTextList[attrImage].SetVerticalAlignCenter()
			self.petAttrTextList[attrImage].SetWindowHorizontalAlignCenter()
			self.petAttrTextList[attrImage].SetWindowVerticalAlignCenter()
			self.petAttrTextList[attrImage].Show()

			self.petAttRateList.append(attrImage)
			self.petAttRateList[attrImage] = ui.TextLine()
			self.petAttRateList[attrImage].SetParent(self.petAttrImageList[attrImage])
			self.petAttRateList[attrImage].SetPosition(0, 0)
			self.petAttRateList[attrImage].SetText("+%{}".format(self.petAttrValueList[attrImage]))	
			self.petAttRateList[attrImage].SetFontName(localeInfo.GetDefaultFont() if app.ENABLE_FONT_SELECT else localeInfo.UI_DEF_FONT)
			self.petAttRateList[attrImage].SetHorizontalAlignCenter()
			self.petAttRateList[attrImage].SetVerticalAlignCenter()
			self.petAttRateList[attrImage].SetWindowHorizontalAlignCenter()
			self.petAttRateList[attrImage].SetWindowVerticalAlignCenter()
			self.petAttRateList[attrImage].Show()

		self.skillBorder = ui.BorderA()
		self.skillBorder.SetParent(self.infoBorder)
		self.skillBorder.SetPosition(0, 75)
		self.skillBorder.SetSize(300, 45)
		self.skillBorder.Show()

		self.slotIcons = []
		for i in xrange(8):
			self.slotIcons.append(i)
			self.slotIcons[i] = ui.ImageBox()
			self.slotIcons[i].SetParent(self.skillBorder)
			self.slotIcons[i].SetPosition(9 + i * 35, 6)
			self.slotIcons[i].LoadImage("d:/ymir work/ui/public/slot_base.sub")
			self.slotIcons[i].Show()

		self.skillList = ui.SlotWindow()
		self.skillList.SetParent(self)
		self.skillList.SetPosition(306, 263)
		self.skillList.SetSize(32*9, 32)

		self.SetDefaultInformations()

		self.skillList.SetOverInItemEvent(ui.__mem_func__(self.PetSkillTooltipShow))
		self.skillList.SetOverOutItemEvent(ui.__mem_func__(self.OverInOutTooltip))
		# self.skillList.SetSelectEmptySlotEvent(ui.__mem_func__(self.IncreaseSkill))
		# self.skillList.SetSelectItemSlotEvent(ui.__mem_func__(self.IncreaseSkill))
		self.skillList.Show()

		for i in xrange(8):
			self.skillList.ClearSlot(i)
			self.skillList.SetSlot(i, 7, 32, 32, petskill.GetEmptySkill())

		PET_FILE_NAME = "%s/pet_skill.txt" % app.GetLocalePath()
		PET_FILE_SKILL = "locale/common/pet_skill_bonus.txt"
		self.petFile = open(PET_FILE_NAME, "r").readlines()
		self.petFileSkill = open(PET_FILE_SKILL, "r").readlines()

		self.buttonBorder = ui.BorderA()
		self.buttonBorder.SetParent(self.skillBorder)
		self.buttonBorder.SetPosition(0, 45)
		self.buttonBorder.SetSize(300, 85)
		self.buttonBorder.Show()

		## Creating Buttons
		self.buttonList = [0, 0, 0, 0, 0, 0]

		self.buttonTitle = [
			localeInfo.PET_INFORMATION_BUTTON_TEXT_0,
			localeInfo.PET_INFORMATION_BUTTON_TEXT_1,
			localeInfo.PET_INFORMATION_BUTTON_TEXT_2,
			localeInfo.PET_INFORMATION_BUTTON_TEXT_3,
			localeInfo.PET_INFORMATION_BUTTON_TEXT_4,
			localeInfo.PET_INFORMATION_BUTTON_TEXT_5
		]

		self.buttonList[0] = ui.MakeButton(self, 300, 305, False, PATH_ROOT, "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
		self.buttonList[0].SetEvent(ui.__mem_func__(self.PetTypeIncrease))
		self.buttonList[1] = ui.MakeButton(self, 300+145, 305, False, PATH_ROOT, "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
		self.buttonList[1].SetEvent(ui.__mem_func__(self.PetBonusChange))
		self.buttonList[2] = ui.MakeButton(self, 300, 330, False, PATH_ROOT, "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
		self.buttonList[2].SetEvent(ui.__mem_func__(self.PetStarIncrease))
		self.buttonList[3] = ui.MakeButton(self, 300+145, 330, False, PATH_ROOT, "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
		self.buttonList[3].SetEvent(ui.__mem_func__(self.PetEvolutioIncrease))
		self.buttonList[4] = ui.MakeButton(self, 300, 355, False, PATH_ROOT, "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
		self.buttonList[4].SetEvent(ui.__mem_func__(self.PetActivateSkin))
		self.buttonList[5] = ui.MakeButton(self, 300+145, 355, False, PATH_ROOT, "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")


		for index in xrange(len(self.buttonTitle)):
			self.buttonList[index].SetText(self.buttonTitle[index])

		self.buttonList[0].Down()

		for i in xrange(8):
			self.skillList.ClearSlot(i)
			self.skillList.SetSlot(i, 7, 32, 32, petskill.GetEmptySkill())

	def loadRenderTarget(self):

		self.wndRender = ui.BorderA()
		self.wndRender.SetParent(self)
		self.wndRender.SetSize(280, 350)
		self.wndRender.SetPosition(15, 35)
		self.wndRender.Show()

		self.ModelPreview = ui.RenderTarget()
		self.ModelPreview.SetParent(self.wndRender)
		self.ModelPreview.SetWindowHorizontalAlignCenter()
		self.ModelPreview.SetSize(274, 344)
		self.ModelPreview.SetPosition(1, 2)
		self.ModelPreview.SetRenderTarget(self.RENDER_TARGET_INDEX)
		self.ModelPreview.Show()

		renderTarget.SetBackground(self.RENDER_TARGET_INDEX, "d:/ymir work/ui/game/render/preview_back.tga")
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
		renderTarget.ResetModel(self.RENDER_TARGET_INDEX)

		self.buttonBackgroundShadow = ui.MakeImageBox(self, PET_SYSTEM_DIR + "blackbg.png", 19, 350)

		self.editSkinButton = ui.MakeButton(self, 233, 40, False, PET_SYSTEM_DIR, "editbutton.png", "editbutton_1.png", "editbutton_2.png")
		
		self.prevSkinButton = ui.MakeButton(self, 37, 355, False, PET_SYSTEM_DIR, "prevbutton.png", "prevbutton_1.png", "prevbutton_2.png")
		self.nextSkinButton = ui.MakeButton(self, 219, 355, False, PET_SYSTEM_DIR, "nextbutton.png", "nextbutton_1.png", "nextbutton_1.png")
		self.saveSkinButton = ui.MakeButton(self, 105, 355, False, PET_SYSTEM_DIR, "savebutton.png", "savebutton_1.png", "savebutton_2.png")
		self.editSkinButton.Hide()
		self.prevSkinButton.Hide()
		self.nextSkinButton.Hide()
		self.saveSkinButton.Hide()
		self.buttonBackgroundShadow.Hide()

		self.editSkinButton.SetEvent(ui.__mem_func__(self.ChangePetSkinButton))
		self.prevSkinButton.SetEvent(ui.__mem_func__(self.PreviousSkin))
		self.nextSkinButton.SetEvent(ui.__mem_func__(self.NextSkin))
		self.saveSkinButton.SetEvent(ui.__mem_func__(self.SaveSkin))

		# self.itemTooltip = uiToolTip.ItemToolTip()

	def Constructor(self):

		self.toolTipInfo = uiToolTip.ToolTip()
		self.IsSummon = False
		self.petLevel = 1
		self.petType = 0
		self.petEvolution = 1

		self.petCurrentExperience = 0
		self.petTotalExperience = 0

		self.starList = []
		self.ownedStars = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.totalStarCount = 0

		self.petLevelIncreaseRate = [0, 0]
		self.petSkinLevel = 0
		self.userSelectedSkin = 0

		self.buttonList = []

		self.skinList = (34045, 34073, 34080, 34064, 34082, 34047)
		self.selectedSkin = self.skinList[0]
		self.buttonTitle = []
		self.temporarySkin = self.skinList[0]
		self.unlockedSkinCount = 0

		self.petAttrList = [localeInfo.PET_INFORMATION_ATTR_0,
							localeInfo.PET_INFORMATION_ATTR_1,
							localeInfo.PET_INFORMATION_ATTR_2]

		self.petAttrImageTitleList = []
		self.petAttrImageList = []
		self.petAttrTextList = []
		self.petAttRateList = []
		self.petAttrValueList = [0.0, 0.0, 0.0]

		self.tooltipArray = [ [-1,-1], [-1,-1], [-1,-1] , [-1,-1],[-1,-1], [-1,-1], [-1,-1] , [-1,-1]]

		self.isEditMode = False

		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)

	def Destroy(self):
		self.Constructor()

	def ClearPetInformations(self):
		self.ownedStars = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.totalStarCount = 0
		self.petSkinLevel = 0
		self.userSelectedSkin = 0
		self.unlockedSkinCount = 0
		self.skinList = (34045, 34073, 34080, 34064, 34082, 34047)
		self.selectedSkin = self.skinList[0]
		self.temporarySkin = self.skinList[0]
		self.petLevel = 1
		self.petType = 0
		self.petEvolution = 1
		self.petCurrentExperience = 0

		for i in xrange(0, 3):
			self.petAttrValueList[i] = 0.0
			self.petAttRateList[i].SetText("+%{:.1f}".format(float(0.0)))

		for i in xrange(8):
			self.skillList.ClearSlot(i)
			self.skillList.SetSlot(i, 7, 32, 32, petskill.GetEmptySkill())

		for star in xrange(10):
			self.starList[star].LoadImage(PET_SYSTEM_DIR + "star_empty.png")

		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)
		renderTarget.ResetModel(self.RENDER_TARGET_INDEX)

	def SetDefaultInformations(self):
		for i in xrange(8):
			self.skillList.AppendSlot(i, 35*i, 0, 32, 32)
			self.skillList.ClearSlot(i)
			self.skillList.SetSlot(i, 7, 32, 32, petskill.GetEmptySkill())

	def CheckLockedSkinButtons(self):
		if self.isEditMode:
			if self.skinList.index(self.temporarySkin) >= (self.petSkinLevel+1):
				self.saveSkinButton.Hide()
				# self.saveSkinButton.Disable()
			else:
				self.saveSkinButton.Show()
				# self.saveSkinButton.Enable()

	def PreviousSkin(self):
		getPreviousSkin = self.skinList.index(self.selectedSkin)

		self.selectedSkin = self.skinList[getPreviousSkin - 1]
		self.temporarySkin = self.selectedSkin
		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, self.selectedSkin)

	def NextSkin(self):

		getNextSkin = self.skinList.index(self.selectedSkin)
		nextSkin = getNextSkin+1

		self.selectedSkin = self.skinList[0 if self.selectedSkin == self.skinList[-1] else nextSkin]
		self.temporarySkin = self.selectedSkin
		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, self.selectedSkin)

	def SaveSkin(self):
		
		if self.skinList.index(self.temporarySkin) >= (self.petSkinLevel+1):
			chat.AppendChat(1, localeInfo.YOU_CANNOT_SELECT_UNLOCKED_SKIN)
			return

		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, self.temporarySkin)
		self.CancelEditMode()

		if self.unlockedSkinCount >= 1:
			self.editSkinButton.Show()

		newpet.SkinChange(self.skinList.index(self.selectedSkin))

	def SelectSkin(self, index):
		self.selectedSkin = self.skinList[index]
		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, self.selectedSkin)

	def SetExperience(self, petExperience, totalExperience):
		self.petCurrentExperience = int(petExperience)
		if totalExperience > 0:
			self.petTotalExperience = int(totalExperience)

		percentage = 0

		if self.petTotalExperience:
			if petExperience:
				percentage = min(100.0, float(petExperience)/float(self.petTotalExperience)*100)

		self.experienceTitle.SetText(localeInfo.PET_INFORMATION_EXPERIENCE.format(percentage))
		self.remainingTimeGauge.SetPercentage(self.petCurrentExperience, self.petTotalExperience)

	def PetSkillTooltipShow(self, slot):
		if self.tooltipArray[slot][0] > 0:
			tokens = self.petFile[self.tooltipArray[slot][0]-1][:-1].split("\t")
			tokens2 = self.petFileSkill[self.tooltipArray[slot][0]-1][:-1].split("\t")
			self.toolTipInfo.ClearToolTip()
			self.toolTipInfo.AutoAppendTextLine(tokens[1], grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0))
			self.toolTipInfo.AppendDescription(tokens[4], 26)
			self.toolTipInfo.AppendSpace(5)
			self.toolTipInfo.AutoAppendTextLine(uiToolTip.GET_AFFECT_STRING(int(tokens2[1]), int(tokens2[self.tooltipArray[slot][1]+1])))		
			self.toolTipInfo.AutoAppendTextLine(localeInfo.PET_SYSTEM_SKILL_COOLDOWN+tokens[5]+"s", grp.GenerateColor(1.0, 0.7843, 0.0, 1.0))
			self.toolTipInfo.AlignHorizonalCenter()
			self.toolTipInfo.ShowToolTip()

	def OverInInformations(self):
		if self.toolTipInfo:
			self.toolTipInfo.ClearToolTip()
			self.toolTipInfo.AlignHorizonalCenter()
			self.toolTipInfo.AutoAppendNewTextLine(localeInfo.PET_INFORMATION_SUMMARY_INFO.format(self.petLevel))
			self.toolTipInfo.AppendSpace(1)
			self.toolTipInfo.AutoAppendNewTextLine(localeInfo.PET_INFORMATION_SUMMARY_INFO2.format(self.petType + 1))
			self.toolTipInfo.AppendSpace(1)
			self.toolTipInfo.AutoAppendNewTextLine(localeInfo.PET_INFORMATION_SUMMARY_INFO3.format(self.petEvolution))
			self.toolTipInfo.AppendSpace(1)
			self.toolTipInfo.AutoAppendNewTextLine(localeInfo.PET_INFORMATION_SUMMARY_INFO4.format(self.totalStarCount))
			self.toolTipInfo.AppendSpace(1)
			self.toolTipInfo.AutoAppendNewTextLine(localeInfo.PET_INFORMATION_SUMMARY_INFO5.format(*self.GetPetRatesByType()))
			self.toolTipInfo.AppendSpace(1)
			self.toolTipInfo.AutoAppendNewTextLine(localeInfo.PET_INFORMATION_SUMMARY_INFO6.format(self.petSkinLevel))
			self.toolTipInfo.Show()

	def Close(self):
		self.Hide()
		if self.toolTipInfo:
			self.toolTipInfo.Hide()

		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)
		renderTarget.ResetModel(self.RENDER_TARGET_INDEX)
		self.CancelEditMode()
		try: 
			self.SelectSkin(self.skinList.index(self.userSelectedSkin))
		except:
			pass

	def CancelEditMode(self):
		self.isEditMode = False

		self.editSkinButton.Show()
		self.prevSkinButton.Hide()
		self.nextSkinButton.Hide()
		self.saveSkinButton.Hide()
		self.buttonBackgroundShadow.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def SetSkill(self, slot = -1, idx = -1, lv = -1):
		if int(idx) != -1:
			self.skillList.ClearSlot(int(slot))
			self.skillList.SetPetSkillSlot(int(slot), int(idx), int(lv))
			self.skillList.SetCoverButton(int(slot))
			self.skillList.SetAlwaysRenderCoverButton(int(slot), True)
			self.tooltipArray[int(slot)][0] = int(idx)
			self.tooltipArray[int(slot)][1] = int(lv)
		else:
			for i in xrange(8):
				self.skillList.AppendSlot(i, 35*i, 0, 32, 32)
				self.skillList.ClearSlot(i)
			self.skillList.SetSlot(int(slot), 7, 32, 32, petskill.GetEmptySkill())

	def OverInStar(self, currentStar):
		if self.toolTipInfo:
			self.toolTipInfo.ClearToolTip()
			self.toolTipInfo.AlignHorizonalCenter()
			self.toolTipInfo.AutoAppendNewTextLine(localeInfo.PET_STAR_BONUS_TOOLTIP.format(self.totalStarCount*5) if self.ownedStars[currentStar] else localeInfo.PET_STAR_BONUS_TOOLTIP2)
			self.toolTipInfo.Show()

	def OverInOutTooltip(self):
		if self.toolTipInfo:
			self.toolTipInfo.Hide()

	def ChangePetSkinButton(self):
		if not self.isEditMode:
			self.editSkinButton.Hide()

			self.prevSkinButton.Show()
			self.nextSkinButton.Show()
			self.saveSkinButton.Show()
			self.buttonBackgroundShadow.Show()
			self.isEditMode = True

	def SetSkin(self, skinCount, skinVnum):
		self.unlockedSkinCount = skinCount
		self.petSkinLevel = skinCount
		self.userSelectedSkin = skinVnum

		if self.unlockedSkinCount >= 1:
			self.editSkinButton.Show()

		if self.petLevel >= 80:
			skinVnum += 1

		self.SelectSkin(self.skinList.index(skinVnum))

	def SetBonus(self, b1, b2, b3):
		self.bonusList = [b1, b2, b3]
		for i in xrange(3):
			self.petAttRateList[i].SetText("+%{:.1f}".format(float(self.bonusList[i])/10))

	def GetPetRatesByType(self):
    
		PetRates = {
			0: (1, 3),
			1: (1, 4),
			2: (1, 5),
			3: (1, 6),
			4: (1, 7),
			5: (2, 7),
			6: (3, 7),
			7: (3, 8)
		}

		return PetRates[self.petType]

	def SetInformations(self, level, evolution, ptype, star):
		self.petLevel = level
		self.petEvolution = evolution
		self.petType = ptype
		self.totalStarCount = star
		self.IsSummon = True

		for st in xrange(self.totalStarCount):
			self.starList[st].LoadImage(PET_SYSTEM_DIR + "star_full.png")
			self.ownedStars[st] = 1
			
		if (level >= 80):
			self.skinList = (34046, 34074, 34081, 34065, 34083, 34048)
			self.selectedSkin = self.skinList[0]
			self.temporarySkin = self.skinList[0]

	def PetUnsummon(self):
		self.IsSummon = False
		self.ClearPetInformations()

	def PetTypeIncrease(self):
		if not self.IsSummon:
			return

		if self.petType == 7:
			chat.AppendChat(1, localeInfo.PET_TYPE_EVENT_ERROR_0)
			return

		if player.GetItemCountByVnum(55125) == 0:
			chat.AppendChat(1, localeInfo.PET_TYPE_EVENT_ERROR_3)
			return

		newpet.TypeIncrease()

	def PetBonusChange(self):
		if not self.IsSummon:
			return

		if player.GetItemCountByVnum(55127) == 0:
			chat.AppendChat(1, localeInfo.PET_CHANGE_EVENT_ERROR_0)
			return		

		if self.petLevel != 1 and self.petLevel < 40:
			chat.AppendChat(1, localeInfo.PET_CHANGE_EVENT_ERROR_1)
			return

		newpet.BonusChange()

	def PetStarIncrease(self):
		if not self.IsSummon:
			return

		if self.totalStarCount == 10:
			chat.AppendChat(1, localeInfo.PET_STAR_EVENT_ERROR_0)
			return

		if self.petLevel < 80:
			chat.AppendChat(1, localeInfo.PET_STAR_EVENT_ERROR_1)
			return

		if player.GetItemCountByVnum(55128) == 0:
			chat.AppendChat(1, localeInfo.PET_STAR_EVENT_ERROR_2)
			return

		newpet.StarIncrease()

	def PetEvolutioIncrease(self):
		if not self.IsSummon:
			return
	
		if self.petEvolution == 3:
			chat.AppendChat(1, localeInfo.PET_EVOLUTION_EVENT_ERROR_0)
			return

		evoTabIdx = -1

		for i in xrange(3):
			if PET_EVOLUTION_TABLE[i][0] == self.petLevel:
				evoTabIdx = i 
				break

		if evoTabIdx == -1:
			chat.AppendChat(1, localeInfo.PET_EVOLUTION_EVENT_ERROR_1)
			return

		if player.GetItemCountByVnum(PET_EVOLUTION_TABLE[evoTabIdx][2]) < PET_EVOLUTION_TABLE[evoTabIdx][3]:
			item.SelectItem(PET_EVOLUTION_TABLE[evoTabIdx][2])
			chat.AppendChat(1, localeInfo.PET_EVOLUTION_EVENT_ERROR_2.format(PET_EVOLUTION_TABLE[evoTabIdx][3], item.GetItemName()))
			return

		newpet.EvolutionIncrease()

	def PetActivateSkin(self): 
		if not self.IsSummon:
			return

		if self.unlockedSkinCount == 5:
			chat.AppendChat(1, localeInfo.PET_SKIN_ACTIVATE_EVENT_ERROR_0)
			return

		if player.GetItemCountByVnum(PET_SKIN_ITEM_VNUM_LIST[self.unlockedSkinCount]) < 1:
			item.SelectItem(PET_SKIN_ITEM_VNUM_LIST[self.unlockedSkinCount])
			chat.AppendChat(1, localeInfo.PET_SKIN_ACTIVATE_EVENT_ERROR_1.format((item.GetItemName())))
			return	

		newpet.ActivateSkin()

	def OnUpdate(self):
		if self.IsSummon:
			renderTarget.SelectModel(self.RENDER_TARGET_INDEX, self.selectedSkin)
			renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
		else:
			renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)
			self.editSkinButton.Hide()

		self.CheckLockedSkinButtons()

	# def OnUpdate(self):
	# 	if self.unlockedSkinCount >= 1:
	# 		self.editSkinButton.Show()
	# 	else:
	# 		self.editSkinButton.Hide()
	# 		self.prevSkinButton.Hide()
	# 		self.nextSkinButton.Hide()
	# 		self.saveSkinButton.Hide()
	# 		self.buttonBackgroundShadow.Show()