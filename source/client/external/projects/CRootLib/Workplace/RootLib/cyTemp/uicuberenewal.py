# -*- coding: cp949 -*-
#267038372
import ui
import item
import localeInfo
import uiToolTip
import player
import grp
import cube_renewal
import app
import mouseModule

def FReturnInfo(func,index):
	(vnum_reward, count_reward, item_reward_stackable, vnum_material_1, count_material_1, vnum_material_2, count_material_2, vnum_material_3, count_material_3, vnum_material_4, count_material_4, vnum_material_5, count_material_5, vnum_material_6, count_material_6, vnum_material_7, count_material_7, vnum_material_8, count_material_8, vnum_material_9, count_material_9, vnum_material_10, count_material_10, gold, percent, category) = cube_renewal.GetDates(index)
	info = {
			"vnum_reward" : vnum_reward,
			"count_reward" : count_reward,
			"item_reward_stackable" : item_reward_stackable,
			"vnum_material_1" : vnum_material_1,
			"count_material_1" : count_material_1,
			"vnum_material_2" : vnum_material_2,
			"count_material_2" : count_material_2,
			"vnum_material_3" : vnum_material_3,
			"count_material_3" : count_material_3,
			"vnum_material_4" : vnum_material_4,
			"count_material_4" : count_material_4,
			"vnum_material_5" : vnum_material_5,
			"count_material_5" : count_material_5,

			"vnum_material_6" : vnum_material_6,
			"count_material_6" : count_material_6,
			"vnum_material_7" : vnum_material_7,
			"count_material_7" : count_material_7,
			"vnum_material_8" : vnum_material_8,
			"count_material_8" : count_material_8,
			"vnum_material_9" : vnum_material_9,
			"count_material_9" : count_material_9,
			"vnum_material_10" : vnum_material_10,
			"count_material_10" : count_material_10,

			"gold" : gold,
			"percent" : percent,
			"category" : category
	}

	return info[func]

class CubeRenewalItem(ui.Window):

	def __init__(self, getParentEvent):
		ui.Window.__init__(self)
		self.SetParent(getParentEvent().GetBoard())
		
		self.index = -1
		self.type = -1

		self.count_all = -1

		self.date_cube = None

		self.index = -1

		self.button = ui.Button()
		self.button.SetParent(self)
		self.button.SetEvent(self.Select)
		self.button.Show()

		self.image = ui.ImageBox()
		self.image.SetParent(self)
		self.image.SetPosition(7,3)
		self.image.Show()

		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.SetPosition(40,2)
		self.text.Show()

		self.count_total = ui.TextLine()
		self.count_total.SetParent(self)
		self.count_total.SetPosition(16,2)
		self.count_total.Hide()

		self.getParentEvent = getParentEvent

		self.SetSize(280, 17)

	def SetName(self, name):
		self.name = name
		self.text.SetText(name)

	def SetCountTotal(self, count):

		self.count_all = count

		if count <= 0:
			self.count_total.Hide()
			self.text.SetPosition(17,2)
			return

		self.count_total.SetText("[%d]"%(count*self.GetCountReward()))
		self.count_total.SetPackedFontColor(grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0))
		self.count_total.Show()

		w, h = self.count_total.GetTextSize()
		self.text.SetPosition(w+20,2)

	def GetCount(self):
		return self.count_all

	def SetType(self,type):
		self.type = type

	def AppendIndex(self,index):
		self.index = index

	def GetIndex(self):
		return self.index

	def GetDates(self,func):
		return FReturnInfo(func,self.GetIndex())

	def GetVnumReward(self):
		return self.GetDates("vnum_reward")

	def GetCountReward(self):
		return self.GetDates("count_reward")

	def GetItemStackable(self):
		return self.GetDates("item_reward_stackable")

	def GetVnumMaterial(self,index):
		return self.GetDates("vnum_material_%d" % index)

	def GetCountMaterial(self,index):
		return self.GetDates("count_material_%d" % index)

	def GetGold(self):
		return self.GetDates("gold")

	def GetPercentage(self):
		return self.GetDates("percent")

	def GetName(self):
		return self.name

	def GetType(self):
		return self.type

	def GetStepWidth(self):
		return 0

	def Select(self):
		self.getParentEvent().OnSelectItem(self)

class CubeRenewalCategoryItem(CubeRenewalItem):

	def __init__(self, getParentEvent):
		self.OpenFunc = FALSE
		self.SubCategorys = []
		self.index = -1

		CubeRenewalItem.__init__(self, getParentEvent)

		self.button.SetUpVisual("d:/ymir work/ui/game/cube/cube_menu_tab1.sub")
		self.button.SetOverVisual("d:/ymir work/ui/game/cube/cube_menu_tab1.sub")
		self.button.SetDownVisual("d:/ymir work/ui/game/cube/cube_menu_tab1.sub")

		self.SetType(1)

	def SetCategory(self,index,name):
		self.SetName(name)
		self.IndexCategory(index)

	def AppendSubCategorys(self, date_cube):
		subCategorys = CubeRenewalSubCategoryItem(self.getParentEvent)
		subCategorys.AppendIndex(date_cube)
		subCategorys.LoadInfo()
		subCategorys.Select()
		self.SubCategorys.append(subCategorys)

	def GetListSubCategorys(self):
		return self.SubCategorys

	def IndexCategory(self,index):
		self.index = index

	def GetIndexCategory(self):
		return self.index

	def FindVnumSubCategory(self, key):
		list = filter(lambda argMember, argKey=key: argMember.IsSameVnum(argKey), self.SubCategorys)
		if list:
			return list[0]

		return None

	def Open(self):
		self.image.LoadImage("d:/ymir work/ui/game/cube/cube_menu_tab1_minus.sub")
		self.OpenFunc = TRUE

	def Close(self):
		self.image.LoadImage("d:/ymir work/ui/game/cube/cube_menu_tab1_plus.sub")
		self.OpenFunc = FALSE
		map(ui.Window.Hide, self.SubCategorys)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def IsOpen(self):
		return self.OpenFunc

	def Select(self):
		if self.OpenFunc:
			self.Close()
		else:
			self.Open()

		for x in self.GetListSubCategorys():
			x.Select()

		self.getParentEvent().OnRefresh()
		
class CubeRenewalSubCategoryItem(CubeRenewalItem):

	def __init__(self, getParentEvent):

		self.OpenFunc = FALSE
		self.SubCategoryObjects = []

		CubeRenewalItem.__init__(self, getParentEvent)

		self.button.SetUpVisual("d:/ymir work/ui/game/cube/cube_menu_tab2.sub")
		self.button.SetOverVisual("d:/ymir work/ui/game/cube/cube_menu_tab2.sub")
		self.button.SetDownVisual("d:/ymir work/ui/game/cube/cube_menu_tab2.sub")

		self.image.SetPosition(7,4)
		self.text.SetPosition(25,2)
		self.text.SetPackedFontColor(0xffa28b5f)

		self.SetType(2)

	def LoadInfo(self):
		item.SelectItem(self.GetVnumReward())
		self.SetName(item.GetItemName())

	def AppendSubCategoryObjects(self, date_cube):
		subCategoryobj = CubeRenewalSubCategoryObjects(self.getParentEvent)
		subCategoryobj.AppendIndex(date_cube)
		subCategoryobj.LoadInfo()
		self.SubCategoryObjects.append(subCategoryobj)

	def IsSameVnum(self, vnum):
		return self.GetVnumReward() == vnum

	def Open(self):
		self.image.LoadImage("d:/ymir work/ui/game/cube/cube_menu_tab2_minus.sub")
		self.OpenFunc = TRUE

	def Close(self):
		self.image.LoadImage("d:/ymir work/ui/game/cube/cube_menu_tab2_plus.sub")
		self.OpenFunc = FALSE
		map(ui.Window.Hide, self.SubCategoryObjects)

	def OnPressEscapeKey(self):
		self.Close()
		return True	

	def IsOpen(self):
		return self.OpenFunc

	def GetListSubCategorysObjects(self):
		return self.SubCategoryObjects

	def Select(self):
		if self.OpenFunc:
			self.Close()
		else:
			self.Open()

		self.getParentEvent().OnRefresh()

class CubeRenewalSubCategoryObjects(CubeRenewalItem):
	def __init__(self, getParentEvent):
		CubeRenewalItem.__init__(self, getParentEvent)

		self.button.SetUpVisual("d:/ymir work/ui/game/cube/cube_menu_tab3_default.sub")
		self.button.SetOverVisual("d:/ymir work/ui/game/cube/cube_menu_tab3_select.sub")
		self.button.SetDownVisual("d:/ymir work/ui/game/cube/cube_menu_tab3_select.sub")
		self.SetType(3)
		self.text.SetPosition(17,2)

	def LoadInfo(self):
		item.SelectItem(self.GetVnumReward())
		self.SetName(item.GetItemName()+' (%d%%)'%(self.GetPercentage()))
		self.CountTotal()

	def CountTotal(self):
		count_items = []
		count_all_items = 0

		for i in xrange(1, 11):
			if self.GetVnumMaterial(i) != 0:
				if player.GetItemCountByVnum(self.GetVnumMaterial(i)) >= self.GetCountMaterial(i):
					number = player.GetItemCountByVnum(self.GetVnumMaterial(i)) / (self.GetCountMaterial(i))
					count_items.append(number)

				count_all_items += 1

		if len(count_items) >= count_all_items:
			self.SetCountTotal(min(count_items))
		else:
			self.SetCountTotal(0)

	def UpdatePercentage(self):
		item.SelectItem(self.GetVnumReward())
		Percentage_Actual = self.GetPercentage()
		self.SetName(item.GetItemName()+' (%d%%)'%(Percentage_Actual))

	def UnSelect(self):
		self.button.SetUp()
		self.button.Enable()

	def SetSelect(self):
		self.button.Down()
		self.button.Disable()

	def Select(self):
		self.getParentEvent().SelectObject(self)

class CubeRenewalWindows(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		cube_renewal.SetCubeRenewalHandler(self)

		self.Category = [
			[1,"ARMOR", localeInfo.CUBE_CAT_01],
			[2,"WEAPON",localeInfo.CUBE_CAT_02],
			[3,"BRACELET",localeInfo.CUBE_CAT_03],
			[4,"PENDANT",localeInfo.CUBE_CAT_04],
			[5,"HELMET",localeInfo.CUBE_CAT_05],
			[6,"SASH",localeInfo.CUBE_CAT_06],
			[7,"AURA",localeInfo.CUBE_CAT_07],
			[8,"SPECIAL",localeInfo.CUBE_CAT_08],
			[9,"RING",localeInfo.CUBE_CAT_09],
			[10,"MOUNT",localeInfo.CUBE_CAT_10],
			[11,"PET",localeInfo.CUBE_CAT_11],
			[12,"MOUNT_SKIN",localeInfo.CUBE_CAT_12],
			[13,"PET_SKIN",localeInfo.CUBE_CAT_13],
			[14,"STONE",localeInfo.CUBE_CAT_14],
			[15,"NECKLACE",localeInfo.CUBE_CAT_15],
			[16,"EARRINGS",localeInfo.CUBE_CAT_16],
			[17,"SHIELD",localeInfo.CUBE_CAT_17],
			[18,"SHOE",localeInfo.CUBE_CAT_18],
			[19,"GLOVE",localeInfo.CUBE_CAT_19],
			[20,"BELT",localeInfo.CUBE_CAT_20],
			[21,"UNIQUE",localeInfo.CUBE_CAT_21],
			[22,"UPGRADE",localeInfo.CUBE_CAT_22],
			[23,"SASH_SKIN",localeInfo.CUBE_CAT_23],
			[24,"AURA_SKIN",localeInfo.CUBE_CAT_24],
			[25,"BOOKS",localeInfo.CUBE_CAT_25],
			[26,"ALCHEMY",localeInfo.CUBE_CAT_26],
			[27,"ALCHEMYUPGRADE",localeInfo.CUBE_CAT_27],
			[28,"ENCHANT",localeInfo.CUBE_CAT_28],
			[999,"OTHER", localeInfo.CUBE_CAT_999]
		]

		self.showingItemList = []
		self.Category_list = []
		self.startLine = 0
		self.MaxElements = 12
		self.cube_elements = {}
		self.selectedItem = None
		self.count_item_reward = 0

		self.currentPage = 1

		self.toolTip = uiToolTip.ItemToolTip()

		self.LoadWindow()
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()
	def __del__(self):
		cube_renewal.SetCubeRenewalHandler(None)
		ui.ScriptWindow.__init__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/cuberenewalwindow.py")
		except:
			import exception
			exception.Abort("CubeRenewalWindows.LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("item_list_board")
			self.item_slot = self.GetChild("item_slot")
			self.cube_list_scroll_bar = self.GetChild("cube_list_scroll_bar")
			self.yang_text = self.GetChild("yang_text")
			self.result_qty = self.GetChild("result_qty")
			self.button_ok = self.GetChild("button_ok")
			self.button_cancel = self.GetChild("button_cancel")

			self.qty_sub_button = self.GetChild("qty_sub_button")
			self.qty_add_button = self.GetChild("qty_add_button")

			self.prevPageButton = self.GetChild("prev_page")
			self.prevPageButton.SetEvent(self.ChangePage)
			self.prevPageButton.Hide()
			self.nextPageButton = self.GetChild("next_page")
			self.nextPageButton.SetEvent(self.ChangePage)
			self.nextPageButton.Hide()

			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			self.wndMoneySlotIcon = self.GetChild("yang_icon")
			self.wndMoneySlotIcon.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowMoneyTitleToolTip)
			self.wndMoneySlotIcon.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideMoneyTitleToolTip)
			self.__SetMoneyToolTip()

			if self.currentPage == 1:
				for i in xrange(1, 6):
					self.cube_elements["count_elements_%d"%i] = self.GetChild("material_qty_text_%d"%i)

			elif self.currentPage == 2:
				for i in xrange(6, 11):
					self.cube_elements["count_elements_%d"%i] = self.GetChild("material_qty_text_%d"%i)

		except:
			import exception
			exception.Abort("CubeRenewalWindows.LoadWindow.LoadElements")

		self.button_cancel.SetEvent(self.Close)
		self.button_ok.SetEvent(self.AcceptCube)

		self.result_qty.SetReturnEvent(self.AceptInputItem)
		self.result_qty.CanEdit(False)

		self.qty_sub_button.SetEvent(self.QtySubButton)
		self.qty_add_button.SetEvent(self.QtyAddButton)

		self.cube_list_scroll_bar.SetScrollEvent(ui.__mem_func__(self.OnScroll))

		self.icons_items = ui.SlotWindow()
		self.icons_items.SetParent(self.item_slot)
		self.icons_items.SetPosition(25,13)
		self.icons_items.SetSize((32*9),32*3)
		self.icons_items.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.icons_items.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		# if app.ENABLE_RENDER_TARGET:
			# self.icons_items.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
			# self.icons_items.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))

		self.icons_items.AppendSlot(0,0,0,32,32*3)

		for i in xrange(0, 6):
			self.icons_items.AppendSlot(i+1, 46*i+62, 0, 32, 32*3)

		self.icons_items.Show()

	def ChangePage(self):
		if self.currentPage == 1:
			self.currentPage = 2
			self.prevPageButton.Show()
			self.nextPageButton.Hide()

		elif self.currentPage == 2:
			self.currentPage = 1
			self.prevPageButton.Hide()
			self.nextPageButton.Show()
		self.UpdateInfoSelect()

	def SetItemToolTip(self, tooltipItem):
		self.toolTip = tooltipItem
		
	def BindInterface(self, interface):
		self.interface = interface

	def Open(self):
		(self.xShopStart, self.yShopStart, z) = player.GetMainCharacterPosition()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def BINARY_CUBE_RENEWAL_LOADING(self):
		self.ClearElements()
		self.LoadCategory()
		self.LoadSubCategory()
		self.LoadSubObjects()
		self.OnRefresh()

	def BINARY_CUBE_RENEWAL_UPDATE(self):
		if self.selectedItem:
			self.UpdateCountSubCategory()
			self.UpdateMaterialCount()

	def ClearElements(self):
		if len(self.showingItemList) > 0:
			map(ui.Window.Hide, self.showingItemList)

		for group in self.Category_list:
			group.Close()

			for Categorys in group.GetListSubCategorys():
				Categorys.Close()

		page2Index = [0, 6, 7, 8, 9, 10]

		for i in xrange(0, 6):
			self.icons_items.ClearSlot(i)
			if i > 0:
				self.cube_elements["count_elements_%d"%i].Hide()

		self.yang_text.Hide()
		self.result_qty.Hide()

		self.Category_list = []
		self.startLine = 0

		self.cube_list_scroll_bar.SetPos(0)

	def CheckListCategorysTotal(self):
		list1 = []
		list2 = []

		for i2 in xrange(cube_renewal.CountDates()):
			list1.append(self.CheckCategoryIndex(FReturnInfo("category",i2)))

		for ia in list1:
			if ia not in list2:
				list2.append(ia)

		return list2

	def LoadCategory(self):
		world = self.CheckListCategorysTotal()
		for i in world:
			for i1 in xrange(len(self.Category)):
				if self.Category[i1][0] == i:
					member = CubeRenewalCategoryItem(ui.__mem_func__(self.GetSelf))
					member.SetCategory(self.Category[i1][0],self.Category[i1][2])
					member.Close()
					member.Show()
					self.Category_list.append(member)

	def CheckCategoryIndex(self,name):
		vnum_default = 0
		for i in xrange(len(self.Category)):
			if name == self.Category[i][1]:
				return self.Category[i][0]
		for i in xrange(len(self.Category)):		
			if "WORLDARD" == self.Category[i][1]:
				return self.Category[i][0]

	def LoadSubCategory(self):
		for group in self.Category_list:
			for i in xrange(cube_renewal.CountDates()):
				if self.CheckCategoryIndex(FReturnInfo("category",i)) == group.GetIndexCategory():
					if not group.FindVnumSubCategory(FReturnInfo("vnum_reward",i)):
						group.AppendSubCategorys(i)

	def LoadSubObjects(self):
		for group in self.Category_list:
			for i in xrange(cube_renewal.CountDates()):
				if self.CheckCategoryIndex(FReturnInfo("category",i)) == group.GetIndexCategory():
					for Categorys in group.GetListSubCategorys():
						if FReturnInfo("vnum_reward",i) == Categorys.GetVnumReward():
							Categorys.AppendSubCategoryObjects(i)

	def OnScroll(self):
		scrollLineCount = len(self.showingItemList) - (self.MaxElements)
		startLine = int(scrollLineCount * self.cube_list_scroll_bar.GetPos())


		if startLine != self.startLine:
			self.startLine = startLine
			self.SetExtraInfo()

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.cube_list_scroll_bar.OnUp()
		else:
			self.cube_list_scroll_bar.OnDown()

	def __OnSelectEmptySlot(self,selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()

		if not self.selectedItem:
			return

		if self.selectedItem.GetPercentage() >= 100:
			return

		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()
			itemVNum = player.GetItemIndex(attachedSlotPos)
			itemCount = player.GetItemCount(attachedSlotPos)

	def __OnSelectItemSlot(self,selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if not self.selectedItem:
			return
		if self.selectedItem.GetPercentage() >= 100:
			return

	def OnRefresh(self):
		self.showingItemList = []

		for group in self.Category_list:
			self.showingItemList.append(group)

			if group.IsOpen():
				for Categorys in group.GetListSubCategorys():
					self.showingItemList.append(Categorys)

					if Categorys.IsOpen():
						for a in Categorys.GetListSubCategorysObjects():
							self.showingItemList.append(a)

		self.SetExtraInfo()

	def SetExtraInfo(self):
		if self.MaxElements >= len(self.showingItemList):
			self.cube_list_scroll_bar.Hide()
			self.startLine = 0
		else:
			if self.showingItemList:
				self.cube_list_scroll_bar.SetMiddleBarSize(float(self.MaxElements) / float(len(self.showingItemList)))
			self.cube_list_scroll_bar.Show()

		map(ui.Window.Hide, self.showingItemList)

		yPos = 11
		heightLimit = 240

		for item in self.showingItemList[self.startLine:]:
			XPos = 0
			if item.GetType() == 2:
				XPos += 15
			if item.GetType() == 3:
				XPos += 35
			item.SetPosition(6 + XPos, yPos)
			item.SetTop()
			item.Show()

			yPos += 20

			if yPos > heightLimit:
				break

	def SelectObject(self,item):
		if self.currentPage == 2:
			self.ChangePage()

		self.selectedItem = item
		if self.selectedItem:	
			if self.selectedItem.GetVnumMaterial(6) != 0:
				self.nextPageButton.Show()
			else:
				self.nextPageButton.Hide()

			self.UpdateInfoSelect()
			self.UpdateSelectSubCategory()

	def UpdateInfoSelect(self):
		if self.selectedItem:
			self.icons_items.ClearSlot(0)
			self.icons_items.SetItemSlot(0, self.selectedItem.GetVnumReward(), self.selectedItem.GetCountReward())

			page2Index = (0, 6, 7, 8, 9, 10)
			if self.currentPage == 1:
				for i in xrange(1, 6):
					self.icons_items.ClearSlot(i)
					self.icons_items.SetItemSlot(i, self.selectedItem.GetVnumMaterial(i), self.selectedItem.GetCountMaterial(i))

			elif self.currentPage == 2:
				for i in xrange(1, 6):
					self.icons_items.ClearSlot(i)
					self.icons_items.SetItemSlot(i, self.selectedItem.GetVnumMaterial(page2Index[i]), self.selectedItem.GetCountMaterial(page2Index[i]))

			self.result_qty.KillFocus()
			self.result_qty.CanEdit(self.selectedItem.GetItemStackable())
			self.result_qty.SetText("%s"%(self.selectedItem.GetCountReward()))
			self.result_qty.Show()

			self.count_item_reward = self.selectedItem.GetCountReward()
			self.UpdateMaterialCount()

	def UpdateMaterialCount(self):
		count = (self.count_item_reward/(self.selectedItem.GetCountReward()))

		page2Index = [0, 6, 7, 8, 9, 10]
		if self.currentPage == 1:
			for i in xrange(1, 6):
				if self.selectedItem.GetVnumMaterial(i) != 0:
					if player.GetItemCountByVnum(self.selectedItem.GetVnumMaterial(i)) >= (self.selectedItem.GetCountMaterial(i)*count):
						self.cube_elements["count_elements_%d"%i].SetPackedFontColor(grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0))
					else:
						self.cube_elements["count_elements_%d"%i].SetPackedFontColor(grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0))

					self.cube_elements["count_elements_%d"%i].SetText("%d/%d"%(player.GetItemCountByVnum(self.selectedItem.GetVnumMaterial(i)),self.selectedItem.GetCountMaterial(i)*count))
					self.cube_elements["count_elements_%d"%i].Show()
				else:
					self.cube_elements["count_elements_%d"%i].Hide()

		elif self.currentPage == 2:
			for i in xrange(1, 6):
				if self.selectedItem.GetVnumMaterial(page2Index[i]) != 0:
					if player.GetItemCountByVnum(self.selectedItem.GetVnumMaterial(page2Index[i])) >= (self.selectedItem.GetCountMaterial(page2Index[i]) * count):
						self.cube_elements["count_elements_%d" % i].SetPackedFontColor(grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0))
					else:
						self.cube_elements["count_elements_%d" % i].SetPackedFontColor(grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0))

					self.cube_elements["count_elements_%d" % i].SetText("%d/%d"%(player.GetItemCountByVnum(self.selectedItem.GetVnumMaterial(page2Index[i])),self.selectedItem.GetCountMaterial(page2Index[i])*count))
					self.cube_elements["count_elements_%d" % i].Show()

				else:
					self.cube_elements["count_elements_%d" % i].Hide()

		self.yang_text.SetText(localeInfo.NumberToMoneyString(self.selectedItem.GetGold()*count))
		self.yang_text.Show()

		if int(self.selectedItem.GetGold()*count) < player.GetElk():
			self.yang_text.SetPackedFontColor(grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0))
		else:
			self.yang_text.SetPackedFontColor(grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0))

	def ConvertInputResult(self):
		edit = int(self.result_qty.GetText())
		total = self.selectedItem.GetCountReward()
		convert = edit % total
		return convert

	def AceptInputItem(self):
		self.result_qty.KillFocus()

		result_total = int(self.result_qty.GetText())

		if int(self.result_qty.GetText()) < self.selectedItem.GetCountReward():
			result_total = self.selectedItem.GetCountReward()
		elif result_total > 200:
			result_total = 200
		else:
			result = self.ConvertInputResult()
			if result != 0:
				result_total = result_total-result

		self.count_item_reward = result_total
		self.result_qty.SetText("%d"%(result_total))

		count = (self.count_item_reward/(self.selectedItem.GetCountReward()))

		page2Index = (0, 6, 7, 8, 9, 10)

		for i in xrange(0, 6):
			self.icons_items.ClearSlot(i)
			if i == 0:
				self.icons_items.SetItemSlot(i,self.selectedItem.GetVnumReward(),self.count_item_reward)
			else:
				if self.currentPage == 1:
					self.icons_items.SetItemSlot(i, self.selectedItem.GetVnumMaterial(i), self.selectedItem.GetCountMaterial(i)*count)
				else:
					self.icons_items.SetItemSlot(i, self.selectedItem.GetVnumMaterial(page2Index[i]), self.selectedItem.GetCountMaterial(page2Index[i]))

	def AcceptCube(self):

		# if any({self.interface.dlgShop.IsShow(), self.interface.dlgRefineNew.IsShow()}) :
			# return

		if self.selectedItem:
			index = self.selectedItem.GetIndex()
			self.CheckInputFocus()
			count = (self.count_item_reward/(self.selectedItem.GetCountReward()))
			cube_renewal.CubeRenewalMakeItem(index, count)

	def QtyAddButton(self):
		if self.selectedItem and self.selectedItem.GetItemStackable():
			self.result_qty.SetText("%d"%(self.selectedItem.GetCountReward()*self.selectedItem.GetCount()))
			self.AceptInputItem()
		if self.currentPage == 2:
			self.ChangePage()

	def QtySubButton(self):
		if self.selectedItem and self.selectedItem.GetItemStackable():
			self.result_qty.SetText("%d"%(self.selectedItem.GetCountReward()))
			self.AceptInputItem()
		if self.currentPage == 2:
			self.ChangePage()

	def CheckInputFocus(self):
		if self.result_qty.IsFocus():
			self.result_qty.SetText("%d"%(self.selectedItem.GetCountReward()))
			self.AceptInputItem()

	def OnSelectItem(self, item):
		self.selectedItem = item

		if self.selectedItem:
			self.selectedItem.Select()

	def OnUpdate(self):
		if self.showingItemList:
			self.UpdateCountSubCategory()
		if self.selectedItem:
			self.UpdateMaterialCount()

	def UpdateCountSubCategory(self):
		for group in self.Category_list:
			if group.IsOpen():
				for Categorys in group.GetListSubCategorys():
					if Categorys.IsOpen():
						for a in Categorys.GetListSubCategorysObjects():
							a.CountTotal()
							a.UpdatePercentage()

	def UpdateSelectSubCategory(self):
		for group in self.Category_list:
			for Categorys in group.GetListSubCategorys():
				for a in Categorys.GetListSubCategorysObjects():
					a.UnSelect()
		self.selectedItem.SetSelect()

	def GetBoard(self):
		return self.board

	def GetSelf(self):
		return self

	def OverInItem(self, index):
		self.toolTip.ClearToolTip()
		page2Index = [0, 6, 7, 8, 9, 10]

		vnum = 0

		if self.selectedItem:
			if index == 0:
				vnum = self.selectedItem.GetVnumReward()
			else:
				vnum = self.selectedItem.GetVnumMaterial(index) if self.currentPage == 1 else self.selectedItem.GetVnumMaterial(page2Index[index])

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)

		self.toolTip.AddItemData(vnum, metinSlot)

		if app.ENABLE_RENDER_TARGET:
			self.toolTip.AppendRenderingTooltip(vnum)
			self.toolTip.AppendWikiTooltip()
			self.toolTip.AppendSpace(5)
			self.toolTip.AppendTextLine(localeInfo.SHOP_SEARCH_SHORTCUT_SEARCH, centerAlign = False)

	def BindInterface(self, interface):
		self.interface = interface

	# if app.ENABLE_RENDER_TARGET:
	# 	def UseItemSlot(self, slotIndex):
	# 		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
	# 			return

	# 		page2Index = [0, 6, 7, 8, 9, 10]

	# 		if self.selectedItem:
	# 			if slotIndex == 0:
	# 				vnum = self.selectedItem.GetVnumReward()
	# 			else:
	# 				vnum = self.selectedItem.GetVnumMaterial(slotIndex) if self.currentPage == 1 else self.selectedItem.GetVnumMaterial(page2Index[slotIndex])
    
				# if app.IsPressed(app.DIK_LCONTROL) and app.ENABLE_RENDER_TARGET:
				# 	item.SelectItem(vnum)
				# 	self.toolTip.ModelPreviewFull(vnum, slotIndex)

	# def OnSelectItemSlot(self, slotIndex):
		# page2Index = [0, 6, 7, 8, 9, 10]
		# if slotIndex == 0:
		# 	vnum = self.selectedItem.GetVnumReward()
		# else:
		# 	vnum = self.selectedItem.GetVnumMaterial(slotIndex) if self.currentPage == 1 else self.selectedItem.GetVnumMaterial(page2Index[slotIndex])

		# item.SelectItem(vnum)
		# constInfo.SEND_ITEM_VNUM = vnum
		# interfaceClass = constInfo.GetInterfaceInstance()


	def OverOutItem(self):
		if self.toolTip != None:
			self.toolTip.HideToolTip()
			self.toolTip.ClearToolTip()

	def __SetMoneyToolTip(self):
		self.toolTipMoneyTitle = uiToolTip.ToolTip(20)
		self.toolTipMoneyTitle.AutoAppendTextLine(localeInfo.MONETARY_UNIT0)
		self.toolTipMoneyTitle.AlignHorizonalCenter()

	def __ShowMoneyTitleToolTip(self):
		self.toolTipMoneyTitle.ShowToolTip()
	def __HideMoneyTitleToolTip(self):
		self.toolTipMoneyTitle.HideToolTip()

	def Close(self):
		cube_renewal.CubeRenewalClose()
		self.selectedItem = None
		self.prevPageButton.Hide()
		self.nextPageButton.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

