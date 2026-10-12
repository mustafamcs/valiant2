import ui, mouseModule, item, localeInfo, uiToolTip, uiScriptLocale, wndMgr, \
	app, renderTarget, player, net, skill, chr

class BuffiWindow(ui.BoardWithTitleBar):

	RENDER_TARGET_INDEX = 66

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.Constructor()
		self.LoadImage()
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.BoardWithTitleBar.__init__(self)

	def Constructor(self):
		self.SetSize(537, 300)
		self.SetCenterPosition()
		self.AddFlag('movable')
		self.SetTitleName(localeInfo.BUFFI_WINDOW_TITLE)
		self.SetCloseEvent(self.Close)
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)

		self.tooltipSlot = uiToolTip.ToolTip(250)
		self.toolTipSkill = uiToolTip.SkillToolTip()
		self.itemTooltip = uiToolTip.ItemToolTip()

	def LoadImage(self):
		self.wndRender = ui.BorderA()
		self.wndRender.SetParent(self)
		self.wndRender.SetSize(250, 250)
		self.wndRender.SetPosition(15, 35)
		self.wndRender.Show()

		self.ModelPreview = ui.RenderTarget()
		self.ModelPreview.SetParent(self.wndRender)
		self.ModelPreview.SetWindowHorizontalAlignCenter()
		self.ModelPreview.SetSize(244, 294-60)
		self.ModelPreview.SetPosition(1, 2)
		self.ModelPreview.SetRenderTarget(self.RENDER_TARGET_INDEX)
		self.ModelPreview.Show()

		self.wndItems = ui.BorderA()
		self.wndItems.SetParent(self)
		self.wndItems.SetSize(250, 250)
		self.wndItems.SetPosition(270, 35)
		self.wndItems.Show()

		self.buffiSkills = ui.GridSlotWindow()
		self.buffiSkills.ArrangeSlot(0, 5, 1, 32, 32, 4, 0)
		self.buffiSkills.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
		self.buffiSkills.SetParent(self)
		self.buffiSkills.SetPosition(289+16, 230)
		self.buffiSkills.Show()

		self.lockedSkill = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/game/buffi/locked_slot_tr.png", 414, 230)
		self.lockedSkill.OnMouseOverIn = ui.__mem_func__(self.LockedOverIn)
		self.lockedSkill.OnMouseOverOut = ui.__mem_func__(self.LockedOverOut)

		self.lockedSkill2 = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/game/buffi/locked_slot_tr.png", 448, 230)
		self.lockedSkill2.OnMouseOverIn = ui.__mem_func__(self.LockedOverIn)
		self.lockedSkill2.OnMouseOverOut = ui.__mem_func__(self.LockedOverOut)

		# self.buffiSkillList = [91, 92, 93, 94, 95]
		
		self.buffiSkillList = [180, 181, 182, 183, 184]

		self.buffiItems = [36009, 36002, 36003, 0, 0]
		self.buffiItems2 = [36009, 36002, 36003, 0, 0]

		self.itemSlots = \
		{
			"grid" : [0, 0, 0, 0, 0],
			"slotsize" : [1, 2, 1, 1, 1],
			"positions" : [[320, 155], [379, 117], [379, 81], [437, 71], [437, 71+35]]
		}
		self.shamanSkeleton = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/game/buffi/shamanimage.png", 322, 80)

		for i in xrange(player.BUFFI_SLOT_COUNT):
			self.itemSlots["grid"][i] = ui.GridSlotWindow()
			self.itemSlots["grid"][i].SetParent(self)
			self.itemSlots["grid"][i].SetPosition(*self.itemSlots["positions"][i])
			self.itemSlots["grid"][i].ArrangeSlot(0, 1, self.itemSlots["slotsize"][i], 32, 32, 0, 0)
			self.itemSlots["grid"][i].SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			# self.itemSlots["grid"][i].SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			# self.itemSlots["grid"][i].SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			# self.itemSlots["grid"][i].SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
			self.itemSlots["grid"][i].SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			# self.itemSlots["grid"][i].SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
			# self.itemSlots["grid"][i].SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
			if app.ENABLE_SLOT_TOOLTIP:
				self.itemSlots["grid"][i].SetOverInSlotEvent(ui.__mem_func__(self.OverInSlot))
				self.itemSlots["grid"][i].SetOverOutSlotEvent(ui.__mem_func__(self.OverOutSlot))
			self.itemSlots["grid"][i].Show()


		self.shamanItemsTitle = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/game/characterdetails/category_item.png", 287, 45)
		self.shamanItemsText = ui.MakeTextLineNew(self.shamanItemsTitle, 0, 0, uiScriptLocale.INVENTORY_TITLE)

		self.shamanItemsText.SetHorizontalAlignCenter()
		self.shamanItemsText.SetVerticalAlignCenter()
		self.shamanItemsText.SetWindowHorizontalAlignCenter()
		self.shamanItemsText.SetWindowVerticalAlignCenter()

		self.shamanItemsSkills = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/game/characterdetails/category_item.png", 287, 195)
		self.shamanSkillsText = ui.MakeTextLineNew(self.shamanItemsSkills, 0, 0, localeInfo.CATEGORY_SKILL)
		self.shamanSkillsText.SetHorizontalAlignCenter()
		self.shamanSkillsText.SetVerticalAlignCenter()
		self.shamanSkillsText.SetWindowHorizontalAlignCenter()
		self.shamanSkillsText.SetWindowVerticalAlignCenter()

		# self.shamanSkeletonBG = ui.MakeExpandedImageBox(self, "d:/ymir work/ui/game/buffi/itembg.png", 287, 65)

		renderTarget.ResetModel(self.RENDER_TARGET_INDEX)
		self.CreateShamanRender()

	def Open(self):
		self.Show()
		self.CreateShamanRender()
		self.RefreshRenderTarget()

	def CreateShamanRender(self):
		renderTarget.SetBackground(self.RENDER_TARGET_INDEX, "d:/ymir work/ui/game/render/preview_back.tga")
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, 3)

	def Close(self):
		self.Hide()

		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)
		renderTarget.ResetModel(self.RENDER_TARGET_INDEX)
	
		if self.tooltipSlot:
			self.tooltipSlot.Hide()

		if self.toolTipSkill:
			self.toolTipSkill.Hide()

		if self.itemTooltip:
			self.itemTooltip.Hide()

	def OnPressEscapeKey(self):
		self.Close()

	def LockedOverIn(self):
		if self.tooltipSlot:
			self.tooltipSlot.ClearToolTip()
			self.tooltipSlot.AutoAppendTextLine(localeInfo.BUFFI_SKILL_LOCKED_TOOLTIP)
			self.tooltipSlot.AlignHorizonalCenter()
			self.tooltipSlot.AppendSpace(5)
			self.tooltipSlot.ShowToolTip()

	def LockedOverOut(self):
		self.OverOutSlot()

	def OnUpdate(self):
		if self.buffiSkills:
			for i, idx in enumerate(self.buffiSkillList, start=0):
				skillLevel = player.GetSkillLevel(i+161)
				skillGrade = player.GetSkillGrade(i+161)
			
				self.buffiSkills.SetSkillSlotNew(i, idx, skillGrade, skillLevel)
				self.buffiSkills.SetSlotCountNew(i, skillGrade, skillLevel)
				self.buffiSkills.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				self.buffiSkills.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				self.buffiSkills.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

			self.buffiSkills.RefreshSlot()

		for i in xrange(player.BUFFI_SLOT_COUNT):
			itemVnum = player.GetItemIndex(player.BUFFI_WINDOW, i)
			if itemVnum != 0:
				self.itemSlots["grid"][i].SetItemSlot(0, itemVnum)
				self.itemSlots["grid"][i].SetOverInItemEvent(lambda vnum = itemVnum, slot = i : self.OverInBuffiItem(i, itemVnum))
				self.itemSlots["grid"][i].SetUseSlotEvent(lambda vnum = itemVnum, slot = i: self.UseItemSlot(slot))
				self.itemSlots["grid"][i].SetUnselectItemSlotEvent(lambda vnum = itemVnum, slot = i: self.UseItemSlot(slot))

				self.itemSlots["grid"][i].SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutBuffiItem))
				self.buffiItems[i] = itemVnum
			else:
				self.itemSlots["grid"][i].ClearSlot(0)
				self.buffiItems[i] = self.buffiItems2[i]

			self.itemSlots["grid"][i].RefreshSlot()

		self.RefreshRenderTarget()

		# if player.CheckAffect(chr.NEW_AFFECT_NAMING_SCROLL_SHAMAN, 0):
		if self.IsNamingScrollActive():
			self.lockedSkill.Hide()
			self.lockedSkill2.Hide()
		else:
			self.lockedSkill.Show()
			self.lockedSkill2.Show()

	def IsNamingScrollActive(self):
		return player.CheckAffect(chr.NEW_AFFECT_NAMING_SCROLL_BUFFI, 0)

	def RefreshRenderTarget(self):

		renderTarget.SetHair(self.RENDER_TARGET_INDEX, self.buffiItems[2])
		renderTarget.SetArmor(self.RENDER_TARGET_INDEX, self.buffiItems[1])
		renderTarget.SetWeapon(self.RENDER_TARGET_INDEX, self.buffiItems[0])
		renderTarget.SetAcce(self.RENDER_TARGET_INDEX, self.buffiItems[3])

	def SelectEmptySlot(self, selectedSlotPos):

		if mouseModule.mouseController.isAttached():
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			net.SendItemMovePacket(player.INVENTORY, attachedSlotPos, player.BUFFI_WINDOW, selectedSlotPos, 1)
			mouseModule.mouseController.DeattachObject()

	def __GetSkillGradeFromSlot(self, skillSlot):
		return int(skillSlot / skill.SKILL_GRADE_STEP_COUNT)

	## ToolTip
	def OverInItem(self, slotNumber):
		if mouseModule.mouseController.isAttached():
			return

		if not self.IsNamingScrollActive() and slotNumber > 2:
			return

		slotNumber += 161
		if 0 == self.toolTipSkill:
			return

		skillIndex = player.GetSkillIndex(slotNumber)
		skillLevel = player.GetSkillLevel(slotNumber)

		if self.toolTipSkill:
			overInSkillGrade = self.__GetSkillGradeFromSlot(slotNumber)

			# if overInSkillGrade == skillGrade:
			self.toolTipSkill.SetSkillNew(slotNumber, skillIndex, overInSkillGrade, skillLevel)
			# else:
			# 	self.toolTipSkill.SetSkillOnlyName(slotNumber, skillIndex, overInSkillGrade)

	def OverOutItem(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.HideToolTip()

	def OverInSlot(self, slotIndex):

		m_slotTooltip = {
			0 : localeInfo.INVENTORYSLOT_TOOLTIP_WEAPON_SKIN,
			1 : localeInfo.INVENTORYSLOT_TOOLTIP_BODY,
			2 : localeInfo.INVENTORYSLOT_TOOLTIP_HAIR,
			3 : localeInfo.INVENTORYSLOT_TOOLTIP_ACCE_SKIN,
			4 : localeInfo.INVENTORYSLOT_TOOLTIP_AURA,
		}

		for i in xrange(5):
			if m_slotTooltip.has_key(slotIndex) and self.tooltipSlot and\
				(self.itemSlots["grid"][i].IsIn()):
				self.tooltipSlot.ClearToolTip()
				self.tooltipSlot.AutoAppendTextLine(m_slotTooltip[i])
				self.tooltipSlot.AlignHorizonalCenter()
				self.tooltipSlot.ShowToolTip()

	def OverOutSlot(self):
		if self.tooltipSlot:
			self.tooltipSlot.HideToolTip()

	def OverInBuffiItem(self, slot, iVnum):
		if self.itemTooltip:
			self.itemTooltip.ClearToolTip()

			metinSlot = [player.GetItemMetinSocket(player.BUFFI_WINDOW, slot, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(player.BUFFI_WINDOW, slot, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

			self.itemTooltip.AddItemData(iVnum, metinSlot, attrSlot, 0, 0, player.BUFFI_WINDOW, slot)

	def OnOverOutBuffiItem(self):
		if self.itemTooltip:
			self.itemTooltip.HideToolTip()

	def UseItemSlot(self, vnum):
		curCursorNum = app.GetCursor()

		if app.SELL == curCursorNum:
			return

		net.SendItemUsePacket(player.BUFFI_WINDOW, vnum)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def GetSlotIndex(self, vnum):
		item.SelectItem(vnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()

		if itemType == item.ITEM_TYPE_WEAPON or (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_WEAPON):
			return 0
		elif (itemType == item.ITEM_TYPE_ARMOR) or (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_BODY):
			return 1
		elif itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_HAIR:
			return 2
		#elif itemType == item.ITEM_TYPE_COSTUME and itemSubType in (item.COSTUME_TYPE_ACCE, item.COSTUME_TYPE_WING):
		#	return 3
		elif itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_AURA:
			return 4

		return -1
