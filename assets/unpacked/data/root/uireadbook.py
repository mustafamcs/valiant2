import ui, chat, net, player, localeInfo, app, wndMgr, chr, uiToolTip

from playersettingmodule import SKILL_INDEX_DICT

READ_BOOK, READ_SOULSTONE, READ_SAGE_SOULSTONE, \
	READ_PASSIVE, READ_BUFFI, READ_BUFFI_SOULSTONE, READ_BUFFI_SAGE_SOULSTONE  = xrange(7)

class ReadBookWindow(ui.Window):

	def __init__(self):
		ui.Window.__init__(self)
		self.Constructor()
	def __del__(self):
		ui.Window.__del__(self)

	def Constructor(self):
		self.wndPage = {}
		self.currentPage = 0

		self.toolTip = uiToolTip.ItemToolTip()
		self.toolTipGeneral = uiToolTip.ToolTip(100)
		self.toolTipGeneral.HideToolTip()

		self.LoadPages()


		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def LoadPages(self):
		self.AddFlag("movable")

		SIDEBAR_PATH_PATTERN = "d:/ymir work/ui/game/fastread/{}"
		imgDict = {
				0 : ["bk_0.png", "bk_1.png", "bk_2.png"],
				1 : ["soulstone_0.png", "soulstone_1.png", "soulstone_2.png"],
				2 : ["sage_soulstone_0.png", "sage_soulstone_1.png", "sage_soulstone_2.png"],
				3 : ["passive_0.png", "passive_1.png", "passive_2.png"],
				4 : ["shaman_book_0.png", "shaman_book_1.png", "shaman_book_2.png"],
				5 : ["shaman_soulstone_0.png", "shaman_soulstone_1.png", "shaman_soulstone_2.png"],
				6 : ["shaman_sage_soulstone_0.png", "shaman_sage_soulstone_1.png", "shaman_sage_soulstone_2.png"]
			}

		self.sidebar = SideBar()
		self.sidebar.AddButton(localeInfo.READ_FAST_BTN_01, SIDEBAR_PATH_PATTERN.format(imgDict[0][0]), SIDEBAR_PATH_PATTERN.format(imgDict[0][1]), SIDEBAR_PATH_PATTERN.format(imgDict[0][2]), self.SetPage, READ_BOOK)
		self.sidebar.AddButton(localeInfo.READ_FAST_BTN_02, SIDEBAR_PATH_PATTERN.format(imgDict[1][0]), SIDEBAR_PATH_PATTERN.format(imgDict[1][1]), SIDEBAR_PATH_PATTERN.format(imgDict[1][2]), self.SetPage, READ_SOULSTONE)
		self.sidebar.AddButton(localeInfo.READ_FAST_BTN_03, SIDEBAR_PATH_PATTERN.format(imgDict[2][0]), SIDEBAR_PATH_PATTERN.format(imgDict[2][1]), SIDEBAR_PATH_PATTERN.format(imgDict[2][2]), self.SetPage, READ_SAGE_SOULSTONE)
		self.sidebar.AddButton(localeInfo.READ_FAST_BTN_04, SIDEBAR_PATH_PATTERN.format(imgDict[3][0]), SIDEBAR_PATH_PATTERN.format(imgDict[3][1]), SIDEBAR_PATH_PATTERN.format(imgDict[3][2]), self.SetPage, READ_PASSIVE)
		self.sidebar.AddButton(localeInfo.READ_FAST_BTN_05, SIDEBAR_PATH_PATTERN.format(imgDict[4][0]), SIDEBAR_PATH_PATTERN.format(imgDict[4][1]), SIDEBAR_PATH_PATTERN.format(imgDict[4][2]), self.SetPage, READ_BUFFI)
		self.sidebar.AddButton(localeInfo.READ_FAST_BTN_06, SIDEBAR_PATH_PATTERN.format(imgDict[5][0]), SIDEBAR_PATH_PATTERN.format(imgDict[5][1]), SIDEBAR_PATH_PATTERN.format(imgDict[5][2]), self.SetPage, READ_BUFFI_SOULSTONE)
		self.sidebar.AddButton(localeInfo.READ_FAST_BTN_07, SIDEBAR_PATH_PATTERN.format(imgDict[6][0]), SIDEBAR_PATH_PATTERN.format(imgDict[6][1]), SIDEBAR_PATH_PATTERN.format(imgDict[6][2]), self.SetPage, READ_BUFFI_SAGE_SOULSTONE)

		self.InitPage(270, 260, READ_BOOK, localeInfo.READ_FAST_TITLE_01)
		self.InitPage(270, 260, READ_SOULSTONE, localeInfo.READ_FAST_TITLE_02)
		self.InitPage(270, 260, READ_SAGE_SOULSTONE, localeInfo.READ_FAST_TITLE_03)
		self.InitPage(270, 260, READ_PASSIVE, localeInfo.READ_FAST_TITLE_04)
		self.InitPage(270, 260, READ_BUFFI, localeInfo.READ_FAST_TITLE_05)
		self.InitPage(270, 260, READ_BUFFI_SOULSTONE, localeInfo.READ_FAST_TITLE_06)
		self.InitPage(270, 260, READ_BUFFI_SAGE_SOULSTONE, localeInfo.READ_FAST_TITLE_07)

		self.SetPage(READ_BOOK)

	def SetPage(self, page):

		self.OverOutItem()

		for i in xrange(len(self.sidebar.buttonList)):
			self.sidebar.buttonList[i].SetUp()

		for j in xrange(len(self.wndPage)):
			self.wndPage[j].Hide()
		if page == READ_BOOK:
			self.wndPage[READ_BOOK].Show()
			self.sidebar.buttonList[READ_BOOK].Down()
		elif page == READ_SOULSTONE:
			self.wndPage[READ_SOULSTONE].Show()
			self.sidebar.buttonList[READ_SOULSTONE].Down()
		elif page == READ_SAGE_SOULSTONE:
			self.wndPage[READ_SAGE_SOULSTONE].Show()
			self.sidebar.buttonList[READ_SAGE_SOULSTONE].Down()
		elif page == READ_PASSIVE:
			self.wndPage[READ_PASSIVE].Show()
			self.sidebar.buttonList[READ_PASSIVE].Down()
		elif page == READ_BUFFI:
			self.wndPage[READ_BUFFI].Show()
			self.sidebar.buttonList[READ_BUFFI].Down()
		elif page == READ_BUFFI_SOULSTONE:
			self.wndPage[READ_BUFFI_SOULSTONE].Show()
			self.sidebar.buttonList[READ_BUFFI_SOULSTONE].Down()
		elif page == READ_BUFFI_SAGE_SOULSTONE:
			self.wndPage[READ_BUFFI_SAGE_SOULSTONE].Show()
			self.sidebar.buttonList[READ_BUFFI_SAGE_SOULSTONE].Down()
		self.currentPage = page


	def InitPage(self, width, height, page, title):
		self.wndPage[page] = ui.MakeBoardWithTitleBar(self, "not_pick", title, ui.__mem_func__(self.Close), width, height)
		self.SetSize(self.wndPage[page].GetWidth(), self.wndPage[page].GetHeight())
		self.SetCenterPosition()

		for i in xrange(len(self.sidebar.buttonList)):
			self.sidebar.buttonList[i].SetUp()

		self.sidebar.buttonList[page].Down()

		if page == READ_BOOK:
			self.wndPage[page].Show()

			self.selectedSkill = None
			self.selectedSkillIndex = 0

			self.background = ui.BorderA()
			self.background.SetParent(self.wndPage[READ_BOOK])
			self.background.SetPosition(10, 30)
			self.background.SetSize(self.wndPage[page].GetWidth()-22, self.wndPage[page].GetHeight()-42)
			self.background.Show()

			self.needItemSlot = ui.GridSlotWindow()
			self.needItemSlot.ArrangeSlot(0, 2, 1, 32, 32, 16, 0)
			self.needItemSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemSlot.SetParent(self.background)
			self.needItemSlot.SetPosition(85, 18)
			self.needItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.needItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemSlot.Show()

			self.needItemSlotBook = ui.GridSlotWindow()
			self.needItemSlotBook.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
			self.needItemSlotBook.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemSlotBook.SetParent(self.background)
			self.needItemSlotBook.SetPosition(155, 18)
			self.needItemSlotBook.SetOverInItemEvent(ui.__mem_func__(self.OverInItemBook))
			self.needItemSlotBook.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemSlotBook.Hide()

			self.textReady = ui.MakeTextLineNew(self.background, -5, -35, "Select Skill To Read!")

			self.textReady.SetWindowHorizontalAlignCenter()
			self.textReady.SetHorizontalAlignCenter()
			self.textReady.SetWindowVerticalAlignCenter()
			self.textReady.SetVerticalAlignCenter()

			self.bookSkills = ui.GridSlotWindow()
			self.bookSkills.ArrangeSlot(0, 6, 1, 32, 32, 4, 0)
			self.bookSkills.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.bookSkills.SetParent(self.background)
			self.bookSkills.SetPosition(17, 95)
			self.bookSkills.Show()

			self.readBtn = ui.MakeButton(self.background, 50, 150, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readBtn.SetText(localeInfo.READ_FAST_BTN_TEXT_01)
			self.readBtn.SAFE_SetEvent(self.ReadBook, "NORMAL")

			self.readFastBtn = ui.MakeButton(self.background, 50, 150 + self.readBtn.GetHeight() + 5, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readFastBtn.SetText(localeInfo.READ_FAST_BTN_TEXT_02)
			self.readFastBtn.SAFE_SetEvent(self.ReadBook, "FAST")

		elif page == READ_SOULSTONE:
			self.wndPage[page].Show()

			self.selectedSkillSoul = None

			self.backgroundEx = ui.BorderA()
			self.backgroundEx.SetParent(self.wndPage[READ_SOULSTONE])
			self.backgroundEx.SetPosition(10, 30)
			self.backgroundEx.SetSize(self.wndPage[page].GetWidth()-22, self.wndPage[page].GetHeight()-42)
			self.backgroundEx.Show()

			self.needItemsSoul = ui.GridSlotWindow()
			self.needItemsSoul.ArrangeSlot(0, 2, 1, 32, 32, 8, 0)
			self.needItemsSoul.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemsSoul.SetParent(self.backgroundEx)
			self.needItemsSoul.SetPosition(45, 18)
			self.needItemsSoul.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.needItemsSoul.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemsSoul.Show()

			self.needItemsSoul2 = ui.GridSlotWindow()
			self.needItemsSoul2.ArrangeSlot(2, 2, 1, 32, 32, 8, 0)
			self.needItemsSoul2.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemsSoul2.SetParent(self.backgroundEx)
			self.needItemsSoul2.SetPosition(125, 18)
			self.needItemsSoul2.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.needItemsSoul2.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemsSoul2.Show()

			self.textReadySoul = ui.MakeTextLineNew(self.backgroundEx, -5, -35, "Select Skill To Read!")

			self.textReadySoul.SetWindowHorizontalAlignCenter()
			self.textReadySoul.SetHorizontalAlignCenter()
			self.textReadySoul.SetWindowVerticalAlignCenter()
			self.textReadySoul.SetVerticalAlignCenter()

			self.soulStoneSkills = ui.GridSlotWindow()
			self.soulStoneSkills.ArrangeSlot(0, 6, 1, 32, 32, 4, 0)
			self.soulStoneSkills.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.soulStoneSkills.SetParent(self.backgroundEx)
			self.soulStoneSkills.SetPosition(17, 95)
			self.soulStoneSkills.Show()

			self.readBtnSoul = ui.MakeButton(self.backgroundEx, 50, 150, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readBtnSoul.SetText(localeInfo.READ_FAST_BTN_TEXT_01)
			self.readBtnSoul.SAFE_SetEvent(self.ReadBook, "NORMAL")

			self.readFastBtnSoul = ui.MakeButton(self.backgroundEx, 50, 150 + self.readBtn.GetHeight() + 5, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readFastBtnSoul.SetText(localeInfo.READ_FAST_BTN_TEXT_02)
			self.readFastBtnSoul.SAFE_SetEvent(self.ReadBook, "FAST")

			self.CheckBoxSoul = ui.ExpandedImageBox()
			self.CheckBoxSoul.SetParent(self.backgroundEx)
			self.CheckBoxSoul.SetPosition(200, 25)
			self.CheckBoxSoul.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.CheckBoxSoul.IsChecked = 0
			self.CheckBoxSoul.OnMouseLeftButtonDown = lambda event = "SOULSTONE" : self.OnCheckBox(event)
			self.CheckBoxSoul.OnMouseOverIn = ui.__mem_func__(self.CheckBoxOverIn)
			self.CheckBoxSoul.OnMouseOverOut = ui.__mem_func__(self.OverOutItem)
			self.CheckBoxSoul.Show()

		elif page == READ_SAGE_SOULSTONE:
			self.wndPage[page].Show()

			self.selectedSkillSoulSage = None

			self.backgroundExSage = ui.BorderA()
			self.backgroundExSage.SetParent(self.wndPage[READ_SAGE_SOULSTONE])
			self.backgroundExSage.SetPosition(10, 30)
			self.backgroundExSage.SetSize(self.wndPage[page].GetWidth()-22, self.wndPage[page].GetHeight()-42)
			self.backgroundExSage.Show()

			self.needItemsSoulSage = ui.GridSlotWindow()
			self.needItemsSoulSage.ArrangeSlot(0, 2, 1, 32, 32, 8, 0)
			self.needItemsSoulSage.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemsSoulSage.SetParent(self.backgroundExSage)
			self.needItemsSoulSage.SetPosition(45, 18)
			self.needItemsSoulSage.SetOverInItemEvent(ui.__mem_func__(self.OverInItem2))
			self.needItemsSoulSage.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemsSoulSage.Show()

			self.needItemsSoul2Sage = ui.GridSlotWindow()
			self.needItemsSoul2Sage.ArrangeSlot(2, 2, 1, 32, 32, 8, 0)
			self.needItemsSoul2Sage.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemsSoul2Sage.SetParent(self.backgroundExSage)
			self.needItemsSoul2Sage.SetPosition(125, 18)
			self.needItemsSoul2Sage.SetOverInItemEvent(ui.__mem_func__(self.OverInItem2))
			self.needItemsSoul2Sage.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemsSoul2Sage.Show()

			self.textReadySoulSage = ui.MakeTextLineNew(self.backgroundExSage, -5, -35, "Select Skill To Read!")

			self.textReadySoulSage.SetWindowHorizontalAlignCenter()
			self.textReadySoulSage.SetHorizontalAlignCenter()
			self.textReadySoulSage.SetWindowVerticalAlignCenter()
			self.textReadySoulSage.SetVerticalAlignCenter()

			self.soulStoneSkillsSage = ui.GridSlotWindow()
			self.soulStoneSkillsSage.ArrangeSlot(0, 6, 1, 32, 32, 4, 0)
			self.soulStoneSkillsSage.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.soulStoneSkillsSage.SetParent(self.backgroundExSage)
			self.soulStoneSkillsSage.SetPosition(17, 95)
			self.soulStoneSkillsSage.Show()

			self.readBtnSoulSage = ui.MakeButton(self.backgroundExSage, 50, 150, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readBtnSoulSage.SetText(localeInfo.READ_FAST_BTN_TEXT_01)
			self.readBtnSoulSage.SAFE_SetEvent(self.ReadBook, "NORMAL")

			self.readFastBtnSoulSage = ui.MakeButton(self.backgroundExSage, 50, 150 + self.readBtn.GetHeight() + 5, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readFastBtnSoulSage.SetText(localeInfo.READ_FAST_BTN_TEXT_02)
			self.readFastBtnSoulSage.SAFE_SetEvent(self.ReadBook, "FAST")

			self.CheckBoxSoulSage = ui.ExpandedImageBox()
			self.CheckBoxSoulSage.SetParent(self.backgroundExSage)
			self.CheckBoxSoulSage.SetPosition(200, 25)
			self.CheckBoxSoulSage.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.CheckBoxSoulSage.IsChecked = 0
			self.CheckBoxSoulSage.OnMouseLeftButtonDown = lambda event = "SAGE" : self.OnCheckBox(event)
			self.CheckBoxSoulSage.OnMouseOverIn = ui.__mem_func__(self.CheckBoxOverIn)
			self.CheckBoxSoulSage.OnMouseOverOut = ui.__mem_func__(self.OverOutItem)
			self.CheckBoxSoulSage.Show()

		elif page == READ_PASSIVE:
			self.selectedSkillPassive = None
			self.selectedSkillIndexPassive = 0

			self.backgroundPassive = ui.BorderA()
			self.backgroundPassive.SetParent(self.wndPage[READ_PASSIVE])
			self.backgroundPassive.SetPosition(10, 30)
			self.backgroundPassive.SetSize(self.wndPage[page].GetWidth()-22, self.wndPage[page].GetHeight()-42)
			self.backgroundPassive.Show()

			self.needItemSlotPassive = ui.GridSlotWindow()
			self.needItemSlotPassive.ArrangeSlot(0, 2, 1, 32, 32, 16, 0)
			self.needItemSlotPassive.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemSlotPassive.SetParent(self.backgroundPassive)
			self.needItemSlotPassive.SetPosition(85, 18)
			self.needItemSlotPassive.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.needItemSlotPassive.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemSlotPassive.Show()

			self.needItemSlotPassiveBook = ui.GridSlotWindow()
			self.needItemSlotPassiveBook.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
			self.needItemSlotPassiveBook.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemSlotPassiveBook.SetParent(self.backgroundPassive)
			self.needItemSlotPassiveBook.SetPosition(155, 18)
			self.needItemSlotPassiveBook.SetOverInItemEvent(ui.__mem_func__(self.OverInItemPassiveBook))
			self.needItemSlotPassiveBook.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemSlotPassiveBook.Hide()

			self.textReadyPassive = ui.MakeTextLineNew(self.backgroundPassive, -5, 29, "Select Skill To Read!")

			self.textReadyPassive.SetWindowHorizontalAlignCenter()
			self.textReadyPassive.SetHorizontalAlignCenter()
			self.textReadyPassive.SetWindowVerticalAlignCenter()
			self.textReadyPassive.SetVerticalAlignCenter()

			self.bookSkillsPassive = ui.GridSlotWindow()
			self.bookSkillsPassive.ArrangeSlot(0, 6, 1, 32, 32, 4, 0)
			self.bookSkillsPassive.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.bookSkillsPassive.SetParent(self.backgroundPassive)
			self.bookSkillsPassive.SetPosition(17, 60)
			self.bookSkillsPassive.Show()

			self.bookSkillsPassive2 = ui.GridSlotWindow()
			self.bookSkillsPassive2.ArrangeSlot(0, 5, 1, 32, 32, 4, 0)
			self.bookSkillsPassive2.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.bookSkillsPassive2.SetParent(self.backgroundPassive)
			self.bookSkillsPassive2.SetPosition(35, 60+35)
			self.bookSkillsPassive2.Show()

			self.readBtnPassive = ui.MakeButton(self.backgroundPassive, 50, 150, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readBtnPassive.SetText(localeInfo.READ_FAST_BTN_TEXT_01)
			self.readBtnPassive.SAFE_SetEvent(self.ReadBook, "NORMAL")

			self.readFastBtnPassive = ui.MakeButton(self.backgroundPassive, 50, 150 + self.readBtnPassive.GetHeight() + 5, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readFastBtnPassive.SetText(localeInfo.READ_FAST_BTN_TEXT_02)
			self.readFastBtnPassive.SAFE_SetEvent(self.ReadBook, "FAST")

			self.passiveSelectedSkillIndex = None

			self.bookVnumsPassive = {
				121 : 24010,
				124 : 24011,
				200 : 24002,
				201 : 24003,
				202 : 24004,
				203 : 24005,
				204 : 24006,
				205 : 24007,
				206 : 24008,
				207 : 24009,
				208 : 24012,
			}

		elif page == READ_BUFFI:
			self.selectedSkillBuffi = None
			self.selectedSkillIndexBuffi = 0

			self.backgroundBuffi = ui.BorderA()
			self.backgroundBuffi.SetParent(self.wndPage[READ_BUFFI])
			self.backgroundBuffi.SetPosition(10, 30)
			self.backgroundBuffi.SetSize(self.wndPage[page].GetWidth()-22, self.wndPage[page].GetHeight()-42)
			self.backgroundBuffi.Show()

			self.needItemSlotBuffi = ui.GridSlotWindow()
			self.needItemSlotBuffi.ArrangeSlot(0, 2, 1, 32, 32, 16, 0)
			self.needItemSlotBuffi.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemSlotBuffi.SetParent(self.backgroundBuffi)
			self.needItemSlotBuffi.SetPosition(85, 18)
			self.needItemSlotBuffi.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.needItemSlotBuffi.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemSlotBuffi.Show()

			self.needItemSlotBuffiBook = ui.GridSlotWindow()
			self.needItemSlotBuffiBook.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
			self.needItemSlotBuffiBook.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemSlotBuffiBook.SetParent(self.backgroundBuffi)
			self.needItemSlotBuffiBook.SetPosition(155, 18)
			self.needItemSlotBuffiBook.SetOverInItemEvent(ui.__mem_func__(self.OverInItemBuffiBook))
			self.needItemSlotBuffiBook.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemSlotBuffiBook.Hide()

			self.textReadyBuffi = ui.MakeTextLineNew(self.backgroundBuffi, -5, -35, "Select Skill To Read!")

			self.textReadyBuffi.SetWindowHorizontalAlignCenter()
			self.textReadyBuffi.SetHorizontalAlignCenter()
			self.textReadyBuffi.SetWindowVerticalAlignCenter()
			self.textReadyBuffi.SetVerticalAlignCenter()

			self.bookSkillsBuffi = ui.GridSlotWindow()
			self.bookSkillsBuffi.ArrangeSlot(0, 5, 1, 32, 32, 4, 0)
			self.bookSkillsBuffi.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.bookSkillsBuffi.SetParent(self.backgroundBuffi)
			self.bookSkillsBuffi.SetPosition(35, 95)
			self.bookSkillsBuffi.Show()

			self.readBtnBuffi = ui.MakeButton(self.backgroundBuffi, 50, 150, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readBtnBuffi.SetText(localeInfo.READ_FAST_BTN_TEXT_01)
			self.readBtnBuffi.SAFE_SetEvent(self.ReadBook, "NORMAL")

			self.readFastBtnBuffi = ui.MakeButton(self.backgroundBuffi, 50, 150 + self.readBtnBuffi.GetHeight() + 5, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readFastBtnBuffi.SetText(localeInfo.READ_FAST_BTN_TEXT_02)
			self.readFastBtnBuffi.SAFE_SetEvent(self.ReadBook, "FAST")

			self.buffiSkillBooks = \
			{
				180 : 50494,
				181 : 50495,
				182 : 50496,
				183 : 50510,
				184 : 50511
			}
			self.buffiSelectedSkillIndex = None

		elif page == READ_BUFFI_SOULSTONE:
			self.wndPage[page].Show()

			self.selectedSkillBuffiSoul = None

			self.backgroundExBuffi = ui.BorderA()
			self.backgroundExBuffi.SetParent(self.wndPage[READ_BUFFI_SOULSTONE])
			self.backgroundExBuffi.SetPosition(10, 30)
			self.backgroundExBuffi.SetSize(self.wndPage[page].GetWidth()-22, self.wndPage[page].GetHeight()-42)
			self.backgroundExBuffi.Show()

			self.needItemsSoulBuffi = ui.GridSlotWindow()
			self.needItemsSoulBuffi.ArrangeSlot(0, 2, 1, 32, 32, 8, 0)
			self.needItemsSoulBuffi.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemsSoulBuffi.SetParent(self.backgroundExBuffi)
			self.needItemsSoulBuffi.SetPosition(45, 18)
			self.needItemsSoulBuffi.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.needItemsSoulBuffi.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemsSoulBuffi.Show()

			self.needItemsSoul2Buffi = ui.GridSlotWindow()
			self.needItemsSoul2Buffi.ArrangeSlot(2, 2, 1, 32, 32, 8, 0)
			self.needItemsSoul2Buffi.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemsSoul2Buffi.SetParent(self.backgroundExBuffi)
			self.needItemsSoul2Buffi.SetPosition(125, 18)
			self.needItemsSoul2Buffi.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.needItemsSoul2Buffi.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemsSoul2Buffi.Show()

			self.textReadySoulBuffi = ui.MakeTextLineNew(self.backgroundExBuffi, -5, -35, "Select Skill To Read!")

			self.textReadySoulBuffi.SetWindowHorizontalAlignCenter()
			self.textReadySoulBuffi.SetHorizontalAlignCenter()
			self.textReadySoulBuffi.SetWindowVerticalAlignCenter()
			self.textReadySoulBuffi.SetVerticalAlignCenter()

			self.soulStoneSkillsBuffi = ui.GridSlotWindow()
			self.soulStoneSkillsBuffi.ArrangeSlot(0, 5, 1, 32, 32, 4, 0)
			self.soulStoneSkillsBuffi.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.soulStoneSkillsBuffi.SetParent(self.backgroundExBuffi)
			self.soulStoneSkillsBuffi.SetPosition(35, 95)
			self.soulStoneSkillsBuffi.Show()

			self.readBtnSoulBuffi = ui.MakeButton(self.backgroundExBuffi, 50, 150, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readBtnSoulBuffi.SetText(localeInfo.READ_FAST_BTN_TEXT_01)
			self.readBtnSoulBuffi.SAFE_SetEvent(self.ReadBook, "NORMAL")

			self.readFastBtnSoulBuffi = ui.MakeButton(self.backgroundExBuffi, 50, 150 + self.readBtn.GetHeight() + 5, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readFastBtnSoulBuffi.SetText(localeInfo.READ_FAST_BTN_TEXT_02)
			self.readFastBtnSoulBuffi.SAFE_SetEvent(self.ReadBook, "FAST")
			self.buffiSelectedSkillIndexSoul = None

			self.CheckBoxSoulBuffi = ui.ExpandedImageBox()
			self.CheckBoxSoulBuffi.SetParent(self.backgroundExBuffi)
			self.CheckBoxSoulBuffi.SetPosition(200, 25)
			self.CheckBoxSoulBuffi.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.CheckBoxSoulBuffi.IsChecked = 0
			self.CheckBoxSoulBuffi.OnMouseLeftButtonDown = lambda event = "BUFFI" : self.OnCheckBox(event)
			self.CheckBoxSoulBuffi.OnMouseOverIn = ui.__mem_func__(self.CheckBoxOverIn)
			self.CheckBoxSoulBuffi.OnMouseOverOut = ui.__mem_func__(self.OverOutItem)
			self.CheckBoxSoulBuffi.Show()

		elif page == READ_BUFFI_SAGE_SOULSTONE:
			self.wndPage[page].Show()
			self.selectedSkillBuffiSoulSage = None

			self.backgroundExBuffiSage = ui.BorderA()
			self.backgroundExBuffiSage.SetParent(self.wndPage[READ_BUFFI_SAGE_SOULSTONE])
			self.backgroundExBuffiSage.SetPosition(10, 30)
			self.backgroundExBuffiSage.SetSize(self.wndPage[page].GetWidth()-22, self.wndPage[page].GetHeight()-42)
			self.backgroundExBuffiSage.Show()

			self.needItemsSoulBuffiSage = ui.GridSlotWindow()
			self.needItemsSoulBuffiSage.ArrangeSlot(0, 2, 1, 32, 32, 8, 0)
			self.needItemsSoulBuffiSage.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemsSoulBuffiSage.SetParent(self.backgroundExBuffiSage)
			self.needItemsSoulBuffiSage.SetPosition(45, 18)
			self.needItemsSoulBuffiSage.SetOverInItemEvent(ui.__mem_func__(self.OverInItem2))
			self.needItemsSoulBuffiSage.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemsSoulBuffiSage.Show()

			self.needItemsSoul2BuffiSage = ui.GridSlotWindow()
			self.needItemsSoul2BuffiSage.ArrangeSlot(2, 2, 1, 32, 32, 8, 0)
			self.needItemsSoul2BuffiSage.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.needItemsSoul2BuffiSage.SetParent(self.backgroundExBuffiSage)
			self.needItemsSoul2BuffiSage.SetPosition(125, 18)
			self.needItemsSoul2BuffiSage.SetOverInItemEvent(ui.__mem_func__(self.OverInItem2))
			self.needItemsSoul2BuffiSage.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.needItemsSoul2BuffiSage.Show()

			self.textReadySoulBuffiSage = ui.MakeTextLineNew(self.backgroundExBuffiSage, -5, -35, "Select Skill To Read!")

			self.textReadySoulBuffiSage.SetWindowHorizontalAlignCenter()
			self.textReadySoulBuffiSage.SetHorizontalAlignCenter()
			self.textReadySoulBuffiSage.SetWindowVerticalAlignCenter()
			self.textReadySoulBuffiSage.SetVerticalAlignCenter()

			self.soulStoneSkillsBuffiSage = ui.GridSlotWindow()
			self.soulStoneSkillsBuffiSage.ArrangeSlot(0, 5, 1, 32, 32, 4, 0)
			self.soulStoneSkillsBuffiSage.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)
			self.soulStoneSkillsBuffiSage.SetParent(self.backgroundExBuffiSage)
			self.soulStoneSkillsBuffiSage.SetPosition(35, 95)
			self.soulStoneSkillsBuffiSage.Show()

			self.readBtnSoulBuffiSage = ui.MakeButton(self.backgroundExBuffiSage, 50, 150, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readBtnSoulBuffiSage.SetText(localeInfo.READ_FAST_BTN_TEXT_01)
			self.readBtnSoulBuffiSage.SAFE_SetEvent(self.ReadBook, "NORMAL")

			self.readFastBtnSoulBuffiSage = ui.MakeButton(self.backgroundExBuffiSage, 50, 150 + self.readBtn.GetHeight() + 5, "", "offlineshop/lightwork/searchshop/", "btn_filter_norm.png", "btn_filter_hover.png", "btn_filter_down.png")
			self.readFastBtnSoulBuffiSage.SetText(localeInfo.READ_FAST_BTN_TEXT_02)
			self.readFastBtnSoulBuffiSage.SAFE_SetEvent(self.ReadBook, "FAST")
			self.buffiSelectedSkillIndexSoulSage = None

			self.CheckBoxSoulBuffiSage = ui.ExpandedImageBox()
			self.CheckBoxSoulBuffiSage.SetParent(self.backgroundExBuffiSage)
			self.CheckBoxSoulBuffiSage.SetPosition(200, 25)
			self.CheckBoxSoulBuffiSage.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			self.CheckBoxSoulBuffiSage.IsChecked = 0
			self.CheckBoxSoulBuffiSage.OnMouseLeftButtonDown = lambda event = "BUFFI_SAGE" : self.OnCheckBox(event)
			self.CheckBoxSoulBuffiSage.OnMouseOverIn = ui.__mem_func__(self.CheckBoxOverIn)
			self.CheckBoxSoulBuffiSage.OnMouseOverOut = ui.__mem_func__(self.OverOutItem)
			self.CheckBoxSoulBuffiSage.Show()

	def OnCheckBox(self, pageType):

		if pageType == "SOULSTONE":
			if self.CheckBoxSoul.IsChecked:
				self.CheckBoxSoul.IsChecked = 0
				self.CheckBoxSoul.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.CheckBoxSoul.IsChecked = 1
				self.CheckBoxSoul.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		elif pageType == "SAGE":
			if self.CheckBoxSoulSage.IsChecked:
				self.CheckBoxSoulSage.IsChecked = 0
				self.CheckBoxSoulSage.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.CheckBoxSoulSage.IsChecked = 1
				self.CheckBoxSoulSage.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		elif pageType == "BUFFI":
			if self.CheckBoxSoulBuffi.IsChecked:
				self.CheckBoxSoulBuffi.IsChecked = 0
				self.CheckBoxSoulBuffi.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.CheckBoxSoulBuffi.IsChecked = 1
				self.CheckBoxSoulBuffi.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")

		elif pageType == "BUFFI_SAGE":
			if self.CheckBoxSoulBuffiSage.IsChecked:
				self.CheckBoxSoulBuffiSage.IsChecked = 0
				self.CheckBoxSoulBuffiSage.LoadImage("d:/ymir work/ui/game/biolog_system/select_button01.png")
			else:
				self.CheckBoxSoulBuffiSage.IsChecked = 1
				self.CheckBoxSoulBuffiSage.LoadImage("d:/ymir work/ui/game/biolog_system/select_button02.png")


	def CheckBoxOverIn(self):
		if self.toolTipGeneral:
			self.toolTipGeneral.AutoAppendTextLine(localeInfo.READ_FAST_ZEN_BEAN_TOOLTIP)
			self.toolTipGeneral.AppendSpace(20)
			# self.toolTipGeneral.ResizeToolTip()
			self.toolTipGeneral.ShowToolTip()

	def OnUpdate(self):
		if self.currentPage == READ_BOOK:
			self.needItemSlot.SetItemSlot(0, 71001, player.GetItemCountByVnum(71001))
			self.needItemSlot.RefreshSlot()
			self.needItemSlot.SetItemSlot(1, 71094, player.GetItemCountByVnum(71094))
			self.needItemSlot.RefreshSlot()
			self.needItemSlotBook.RefreshSlot()

			race = net.GetMainActorRace()
			group = net.GetMainActorSkillGroup()
			job = chr.RaceToJob(race)

			if SKILL_INDEX_DICT.has_key(job):
				if SKILL_INDEX_DICT[job].has_key(group):
					activeSkillList = SKILL_INDEX_DICT[job][group]

					for i in xrange(len(activeSkillList)):
						skillIndexx = activeSkillList[i]
						if i != 6 and i != 7:
							if i >= 0 and i <= 5:
								skillLevel = player.GetSkillLevel(i+1)
								skillGrade = player.GetSkillGrade(i+1)
								self.bookSkills.SetSkillSlotNew(i, skillIndexx, skillGrade, skillLevel)
								self.bookSkills.SetSlotCountNew(i, skillGrade, skillLevel)
								self.bookSkills.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
								self.bookSkills.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))

			self.bookSkills.RefreshSlot()

			if self.selectedSkill == None:
				self.textReady.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				self.textReady.SetOutLineColor(0.6, 0, 0, 1)
			else:
				self.textReady.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_READY)
				self.textReady.SetOutLineColor(0, 0.45, 0, 1)

			if self.selectedSkillIndex != 0:
				self.needItemSlotBook.SetItemSlot(0, 50400 + self.selectedSkillIndex, player.GetItemCountByVnum(50400 + self.selectedSkillIndex))
				self.needItemSlotBook.RefreshSlot()

		elif self.currentPage == READ_SOULSTONE:
			self.needItemsSoul.SetItemSlot(0, 71001, player.GetItemCountByVnum(71001))
			self.needItemsSoul.RefreshSlot()
			self.needItemsSoul.SetItemSlot(1, 71094, player.GetItemCountByVnum(71094))
			self.needItemsSoul.RefreshSlot()

			self.needItemsSoul2.SetItemSlot(2, 50513, player.GetItemCountByVnum(50513))
			self.needItemsSoul2.RefreshSlot()
			self.needItemsSoul2.SetItemSlot(3, 70102, player.GetItemCountByVnum(70102))
			self.needItemsSoul2.RefreshSlot()

			race = net.GetMainActorRace()
			group = net.GetMainActorSkillGroup()
			job = chr.RaceToJob(race)

			if SKILL_INDEX_DICT.has_key(job):
				if SKILL_INDEX_DICT[job].has_key(group):
					activeSkillList = SKILL_INDEX_DICT[job][group]

					for i in xrange(len(activeSkillList)):
						skillIndexx = activeSkillList[i]
						if i != 6 and i != 7:
							if i >= 0 and i <= 5:
								skillLevel = player.GetSkillLevel(i+1)
								skillGrade = player.GetSkillGrade(i+1)
								self.soulStoneSkills.SetSkillSlotNew(i, skillIndexx, skillGrade, skillLevel)
								self.soulStoneSkills.SetSlotCountNew(i, skillGrade, skillLevel)
								self.soulStoneSkills.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
								self.soulStoneSkills.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))

			self.soulStoneSkills.RefreshSlot()

			if self.selectedSkillSoul == None:
				self.textReadySoul.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				self.textReadySoul.SetOutLineColor(0.6, 0, 0, 1)
			else:
				self.textReadySoul.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_READY)
				self.textReadySoul.SetOutLineColor(0, 0.45, 0, 1)

		elif self.currentPage == READ_SAGE_SOULSTONE:
			self.needItemsSoulSage.SetItemSlot(0, 24013, player.GetItemCountByVnum(24013))
			self.needItemsSoulSage.RefreshSlot()
			self.needItemsSoulSage.SetItemSlot(1, 24014, player.GetItemCountByVnum(24014))
			self.needItemsSoulSage.RefreshSlot()

			self.needItemsSoul2Sage.SetItemSlot(2, 24000, player.GetItemCountByVnum(24000))
			self.needItemsSoul2Sage.RefreshSlot()
			self.needItemsSoul2Sage.SetItemSlot(3, 70102, player.GetItemCountByVnum(70102))
			self.needItemsSoul2Sage.RefreshSlot()

			race = net.GetMainActorRace()
			group = net.GetMainActorSkillGroup()
			job = chr.RaceToJob(race)

			if SKILL_INDEX_DICT.has_key(job):
				if SKILL_INDEX_DICT[job].has_key(group):
					activeSkillList = SKILL_INDEX_DICT[job][group]

					for i in xrange(len(activeSkillList)):
						skillIndexx = activeSkillList[i]
						if i != 6 and i != 7:
							if i >= 0 and i <= 5:
								skillLevel = player.GetSkillLevel(i+1)
								skillGrade = player.GetSkillGrade(i+1)
								self.soulStoneSkillsSage.SetSkillSlotNew(i, skillIndexx, skillGrade, skillLevel)
								self.soulStoneSkillsSage.SetSlotCountNew(i, skillGrade, skillLevel)
								self.soulStoneSkillsSage.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
								self.soulStoneSkillsSage.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))

			self.soulStoneSkillsSage.RefreshSlot()

			if self.selectedSkillSoulSage == None:
				self.textReadySoulSage.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				self.textReadySoulSage.SetOutLineColor(0.6, 0, 0, 1)
			else:
				self.textReadySoulSage.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_READY)
				self.textReadySoulSage.SetOutLineColor(0, 0.45, 0, 1)

		elif self.currentPage == READ_PASSIVE:
			self.needItemSlotPassive.SetItemSlot(0, 71001, player.GetItemCountByVnum(71001))
			self.needItemSlotPassive.RefreshSlot()
			self.needItemSlotPassive.SetItemSlot(1, 71094, player.GetItemCountByVnum(71094))
			self.needItemSlotPassive.RefreshSlot()
			self.needItemSlotPassiveBook.RefreshSlot()

			self.passiveSkillList = [121, 124, 200, 201, 202, 203]
			self.passiveSkillList2 = [204, 205, 206, 207, 208]
			
			for n, skillIdx in enumerate(self.passiveSkillList):

				addValue = SKILL_INDEX_DICT[2]["SUPPORT"].index(skillIdx)

				skillLevel = player.GetSkillLevel(addValue+101)
				skillGrade = player.GetSkillGrade(addValue+101)
				self.bookSkillsPassive.SetSkillSlotNew(n, skillIdx, skillGrade, skillLevel)
				self.bookSkillsPassive.SetSlotCountNew(n, skillGrade, skillLevel)
				self.bookSkillsPassive.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				self.bookSkillsPassive.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))

			for k, skillIdx in enumerate(self.passiveSkillList2):

				addValue = SKILL_INDEX_DICT[2]["SUPPORT"].index(skillIdx)

				skillLevel = player.GetSkillLevel(101 + addValue)
				skillGrade = player.GetSkillGrade(101 + addValue)
				self.bookSkillsPassive2.SetSkillSlotNew(k, skillIdx, skillGrade, skillLevel)
				self.bookSkillsPassive2.SetSlotCountNew(k, skillGrade, skillLevel)
				self.bookSkillsPassive2.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				self.bookSkillsPassive2.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))

			self.bookSkillsPassive.RefreshSlot()
			self.bookSkillsPassive2.RefreshSlot()

			if self.passiveSelectedSkillIndex == None:
				self.textReadyPassive.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				self.textReadyPassive.SetOutLineColor(0.6, 0, 0, 1)
			else:
				self.textReadyPassive.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_READY)
				self.textReadyPassive.SetOutLineColor(0, 0.45, 0, 1)
				self.needItemSlotPassiveBook.SetItemSlot(0, self.bookVnumsPassive.get(self.passiveSelectedSkillIndex), player.GetItemCountByVnum(self.bookVnumsPassive.get(self.passiveSelectedSkillIndex)))
				self.needItemSlotPassiveBook.RefreshSlot()

		elif self.currentPage == READ_BUFFI:
			self.needItemSlotBuffi.SetItemSlot(0, 71001, player.GetItemCountByVnum(71001))
			self.needItemSlotBuffi.RefreshSlot()
			self.needItemSlotBuffi.SetItemSlot(1, 71094, player.GetItemCountByVnum(71094))
			self.needItemSlotBuffi.RefreshSlot()
			self.needItemSlotBuffiBook.RefreshSlot()

			self.buffiSkills = xrange(180, 185)
			
			for n, skillIdx in enumerate(self.buffiSkills):
				skillLevel = player.GetSkillLevel(n+161)
				skillGrade = player.GetSkillGrade(n+161)
				self.bookSkillsBuffi.SetSkillSlotNew(n, skillIdx, skillGrade, skillLevel)
				self.bookSkillsBuffi.SetSlotCountNew(n, skillGrade, skillLevel)
				self.bookSkillsBuffi.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				self.bookSkillsBuffi.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))

			self.bookSkillsBuffi.RefreshSlot()

			if self.buffiSelectedSkillIndex == None:
				self.textReadyBuffi.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				self.textReadyBuffi.SetOutLineColor(0.6, 0, 0, 1)
			else:
				self.textReadyBuffi.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_READY)
				self.textReadyBuffi.SetOutLineColor(0, 0.45, 0, 1)
				self.needItemSlotBuffiBook.SetItemSlot(0, self.buffiSkillBooks.get(self.buffiSelectedSkillIndex, 0), player.GetItemCountByVnum(self.buffiSkillBooks.get(self.buffiSelectedSkillIndex, 0)))
				self.needItemSlotBuffiBook.RefreshSlot()

		elif self.currentPage == READ_BUFFI_SOULSTONE:
			self.needItemsSoulBuffi.SetItemSlot(0, 71001, player.GetItemCountByVnum(71001))
			self.needItemsSoulBuffi.RefreshSlot()
			self.needItemsSoulBuffi.SetItemSlot(1, 71094, player.GetItemCountByVnum(71094))
			self.needItemsSoulBuffi.RefreshSlot()

			self.needItemsSoul2Buffi.SetItemSlot(2, 50513, player.GetItemCountByVnum(50513))
			self.needItemsSoul2Buffi.RefreshSlot()
			self.needItemsSoul2Buffi.SetItemSlot(3, 70102, player.GetItemCountByVnum(70102))
			self.needItemsSoul2Buffi.RefreshSlot()

			self.buffiSkills = xrange(180, 185)
			
			for n, skillIdx in enumerate(self.buffiSkills):
				skillLevel = player.GetSkillLevel(n+161)
				skillGrade = player.GetSkillGrade(n+161)
				self.soulStoneSkillsBuffi.SetSkillSlotNew(n, skillIdx, skillGrade, skillLevel)
				self.soulStoneSkillsBuffi.SetSlotCountNew(n, skillGrade, skillLevel)
				self.soulStoneSkillsBuffi.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				self.soulStoneSkillsBuffi.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))
	
			self.soulStoneSkillsBuffi.RefreshSlot()

			if self.selectedSkillBuffiSoul == None:
				self.textReadySoulBuffi.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				self.textReadySoulBuffi.SetOutLineColor(0.6, 0, 0, 1)
			else:
				self.textReadySoulBuffi.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_READY)
				self.textReadySoulBuffi.SetOutLineColor(0, 0.45, 0, 1)

		elif self.currentPage == READ_BUFFI_SAGE_SOULSTONE:
			self.needItemsSoulBuffiSage.SetItemSlot(0, 24013, player.GetItemCountByVnum(24013))
			self.needItemsSoulBuffiSage.RefreshSlot()
			self.needItemsSoulBuffiSage.SetItemSlot(1, 24014, player.GetItemCountByVnum(24014))
			self.needItemsSoulBuffiSage.RefreshSlot()

			self.needItemsSoul2BuffiSage.SetItemSlot(2, 24000, player.GetItemCountByVnum(24000))
			self.needItemsSoul2BuffiSage.RefreshSlot()
			self.needItemsSoul2BuffiSage.SetItemSlot(3, 70102, player.GetItemCountByVnum(70102))
			self.needItemsSoul2BuffiSage.RefreshSlot()

			self.buffiSkills = xrange(180, 185)
			
			for n, skillIdx in enumerate(self.buffiSkills):
				skillLevel = player.GetSkillLevel(n+161)
				skillGrade = player.GetSkillGrade(n+161)
				self.soulStoneSkillsBuffiSage.SetSkillSlotNew(n, skillIdx, skillGrade, skillLevel)
				self.soulStoneSkillsBuffiSage.SetSlotCountNew(n, skillGrade, skillLevel)
				self.soulStoneSkillsBuffiSage.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
				self.soulStoneSkillsBuffiSage.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))
	
			self.soulStoneSkillsBuffiSage.RefreshSlot()

			if self.selectedSkillBuffiSoulSage == None:
				self.textReadySoulBuffiSage.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				self.textReadySoulBuffiSage.SetOutLineColor(0.6, 0, 0, 1)
			else:
				self.textReadySoulBuffiSage.SetText(localeInfo.READ_FAST_SKILL_READ_STATE_READY)
				self.textReadySoulBuffiSage.SetOutLineColor(0, 0.45, 0, 1)

	def SelectSkill(self, value):
		skillGrade = player.GetSkillGrade(value+1)


		if self.currentPage == READ_BOOK:

			if skillGrade == 1: # Current page 1 == book, Soulstone == 2
				self.selectedSkill = value
			
				for i in xrange(6):
					if i == value:
						self.bookSkills.ActivateSlot(i)
					else:
						self.bookSkills.DeactivateSlot(i)

				skillIdx = player.GetSkillIndex(int(self.selectedSkill+1))
				self.selectedSkillIndex = skillIdx
				self.needItemSlot.SetPosition(60, 18)
				self.needItemSlotBook.Show()

			else:
				chat.AppendChat(1, localeInfo.READ_FAST_CANT_IMPROVE_THIS_SKILL)

		elif self.currentPage == READ_SOULSTONE:

			if skillGrade == 2: # Current page 1 == book, Soulstone == 2
				self.selectedSkillSoul = value
				for i in xrange(6):
					if i == value:
						self.soulStoneSkills.ActivateSlot(i)
					else:
						self.soulStoneSkills.DeactivateSlot(i)
			else:
				chat.AppendChat(1, localeInfo.READ_FAST_CANT_IMPROVE_THIS_SKILL)

		elif self.currentPage == READ_SAGE_SOULSTONE:

			if skillGrade == 3: # Current page 1 == book, Soulstone == 2
				self.selectedSkillSoulSage = value

				for i in xrange(6):
					if i == value:
						self.soulStoneSkillsSage.ActivateSlot(i)
					else:
						self.soulStoneSkillsSage.DeactivateSlot(i)
			else:
				chat.AppendChat(1, localeInfo.READ_FAST_CANT_IMPROVE_THIS_SKILL)


		elif self.currentPage == READ_PASSIVE:
			self.selectedSkillPassive = value

			addVal = SKILL_INDEX_DICT[2]["SUPPORT"].index(self.passiveSkillList[value])

			if self.bookSkillsPassive2.IsIn():
				addVal = SKILL_INDEX_DICT[2]["SUPPORT"].index(self.passiveSkillList2[value])

			skillGrade = player.GetSkillGrade(addVal+101)
			self.passiveSelectedSkillIndex = player.GetSkillIndex(addVal+101)

			if skillGrade <= 3: # Current page 1 == book, Soulstone == 2
				for i in xrange(6):
					self.bookSkillsPassive.DeactivateSlot(i)
					self.bookSkillsPassive2.DeactivateSlot(i)

					usedList = None

					if self.bookSkillsPassive.IsIn():
						usedList = self.bookSkillsPassive
					else:
						usedList = self.bookSkillsPassive2

					if i == value:
						usedList.ActivateSlot(i)
					else:
						usedList.DeactivateSlot(i)
					
				self.needItemSlotPassive.SetPosition(60, 18)
				self.needItemSlotPassiveBook.Show()

			else:
				chat.AppendChat(1, localeInfo.READ_FAST_CANT_IMPROVE_THIS_SKILL)

		elif self.currentPage == READ_BUFFI:
			self.selectedSkillBuffi = value

			skillGrade = player.GetSkillGrade(value+161)
			self.buffiSelectedSkillIndex = player.GetSkillIndex(value+161)

			if skillGrade <= 1: # Current page 1 == book, Soulstone == 2
				for i in xrange(6):
					self.bookSkillsBuffi.DeactivateSlot(i)
				
					if i == value:
						self.bookSkillsBuffi.ActivateSlot(i)
					else:
						self.bookSkillsBuffi.DeactivateSlot(i)
					
				self.needItemSlotBuffi.SetPosition(60, 18)
				self.needItemSlotBuffiBook.Show()

			else:
				chat.AppendChat(1, localeInfo.READ_FAST_CANT_IMPROVE_THIS_SKILL)

		elif self.currentPage == READ_BUFFI_SOULSTONE:
			skillGrade = player.GetSkillGrade(value+161)

			if skillGrade == 2: # Current page 1 == book, Soulstone == 2

				self.selectedSkillBuffiSoul = value
				self.buffiSelectedSkillIndexSoul = player.GetSkillIndex(value+161)

				for i in xrange(6):
					if i == value:
						self.soulStoneSkillsBuffi.ActivateSlot(i)
					else:
						self.soulStoneSkillsBuffi.DeactivateSlot(i)

			else:
				chat.AppendChat(1, localeInfo.READ_FAST_CANT_IMPROVE_THIS_SKILL)

		elif self.currentPage == READ_BUFFI_SAGE_SOULSTONE:

			skillGrade = player.GetSkillGrade(value+161)
			if skillGrade == 3: # Current page 1 == book, Soulstone == 2

				self.selectedSkillBuffiSoulSage = value
				self.buffiSelectedSkillIndexSoulSage = player.GetSkillIndex(value+161)

				for i in xrange(6):
					if i == value:
						self.soulStoneSkillsBuffiSage.ActivateSlot(i)
					else:
						self.soulStoneSkillsBuffiSage.DeactivateSlot(i)
			else:
				chat.AppendChat(1, localeInfo.READ_FAST_CANT_IMPROVE_THIS_SKILL)
		else:
			chat.AppendChat(1, "Invalid selection made!")

	def Open(self):
		self.Show()

		if self.sidebar:
			x, y = self.GetGlobalPosition()
			self.sidebar.Reposition(x, y)
			self.sidebar.Show()

	def Close(self):
		self.Hide()
		if self.sidebar:
			self.sidebar.Hide()

		self.OverOutItem()

	def OnMoveWindow(self, x, y):
		if self.sidebar:
			self.sidebar.Reposition(x, y)

	def ReadBook(self, state):
		if self.currentPage == READ_BOOK:

			if self.selectedSkill == None:
				chat.AppendChat(1, localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				return
			skillIdx = player.GetSkillIndex(int(self.selectedSkill+1))

			if state == "NORMAL":
				net.SendChatPacket("/read_book_command 1 " + str(skillIdx))
			elif state == "FAST":
				net.SendChatPacket("/read_book_command 0 " + str(skillIdx))

		elif self.currentPage == READ_SOULSTONE:

			if self.selectedSkillSoul == None:
				chat.AppendChat(1, localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				return

			skillIdx = player.GetSkillIndex(int(self.selectedSkillSoul)+1)

			if state == "NORMAL":
				net.SendChatPacket("/soulstone_read_event 1 0 {} {} ".format(str(skillIdx), str(self.CheckBoxSoul.IsChecked)))
			elif state == "FAST":
				net.SendChatPacket("/soulstone_read_event 0 0 {} {} ".format(str(skillIdx), str(self.CheckBoxSoul.IsChecked)))

		elif self.currentPage == READ_SAGE_SOULSTONE:

			if self.selectedSkillSoulSage == None:
				chat.AppendChat(1, localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				return

			skillIdx = player.GetSkillIndex(int(self.selectedSkillSoulSage+1))
			if state == "NORMAL":
				net.SendChatPacket("/soulstone_read_event 1 1 {} {} ".format(str(skillIdx), str(self.CheckBoxSoulSage.IsChecked)))
			elif state == "FAST":
				net.SendChatPacket("/soulstone_read_event 0 1 {} {} ".format(str(skillIdx), str(self.CheckBoxSoulSage.IsChecked)))

		elif self.currentPage == READ_PASSIVE:

			if self.passiveSelectedSkillIndex == None:
				chat.AppendChat(1, localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				return

			if state == "NORMAL":
				net.SendChatPacket("/passive_read 0 " + str(self.passiveSelectedSkillIndex))
			elif state == "FAST":
				net.SendChatPacket("/passive_read 1 " + str(self.passiveSelectedSkillIndex))

		elif self.currentPage == READ_BUFFI:

			if self.buffiSelectedSkillIndex == None:
				chat.AppendChat(1, localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				return

			if state == "NORMAL":
				net.SendChatPacket("/read_book_command 1 " + str(self.buffiSelectedSkillIndex))
			elif state == "FAST":
				net.SendChatPacket("/read_book_command 0 " + str(self.buffiSelectedSkillIndex))

		elif self.currentPage == READ_BUFFI_SOULSTONE:

			if self.buffiSelectedSkillIndexSoul == None:
				chat.AppendChat(1, localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				return

			if state == "NORMAL":
				net.SendChatPacket("/soulstone_read_event 1 0 {} {} ".format(str(self.buffiSelectedSkillIndexSoul), str(self.CheckBoxSoulBuffi.IsChecked)))
			elif state == "FAST":
				net.SendChatPacket("/soulstone_read_event 0 0 {} {} ".format(str(self.buffiSelectedSkillIndexSoul), str(self.CheckBoxSoulBuffi.IsChecked)))

		elif self.currentPage == READ_BUFFI_SAGE_SOULSTONE:

			if self.buffiSelectedSkillIndexSoulSage == None:
				chat.AppendChat(1, localeInfo.READ_FAST_SKILL_READ_STATE_NOT_READY)
				return

			if state == "NORMAL":
				net.SendChatPacket("/soulstone_read_event 1 1 {} {} ".format(str(self.buffiSelectedSkillIndexSoulSage), str(self.CheckBoxSoulBuffiSage.IsChecked)))
			elif state == "FAST":
				net.SendChatPacket("/soulstone_read_event 0 1 {} {} ".format(str(self.buffiSelectedSkillIndexSoulSage), str(self.CheckBoxSoulBuffiSage.IsChecked)))

	def OverInItem(self, slot):

		vnumDict = {
			0 : 71001,
			1 : 71094,
			2 : 50513,
			3 : 70102,
		}

		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.AddItemData(vnumDict.get(slot), 0)

	def OverInItem2(self, slot):

		vnumDict = {
			0 : 24013,
			1 : 24014,
			2 : 24000,
			3 : 70102,
		}

		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.AddItemData(vnumDict.get(slot), 0)

	def OverInItemBook(self, slot):
		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.AddItemData(50400 + self.selectedSkillIndex, 0)

	def OverInItemPassiveBook(self, slot):
		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.AddItemData(self.bookVnumsPassive.get(self.passiveSelectedSkillIndex), 0)

	def OverInItemBuffiBook(self, slot):
		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.AddItemData(self.buffiSkillBooks.get(self.buffiSelectedSkillIndex, 0), 0)

	def OverOutItem(self):
		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.Hide()
			
		if self.toolTipGeneral:
			self.toolTipGeneral.ClearToolTip()
			self.toolTipGeneral.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True

class SideBar(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.buttonList = []
		self.SetSize(75, 0)
		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.Window.__del__(self)
		del self.buttonList[:]

	def AddButton(self, tooltip, normalIMG, hoverIMG, overIMG, callFunc, param = None):
		btn = ui.RadioButton()
		btn.SetParent(self)
		btn.SetPosition(0, len(self.buttonList) * 31)
		btn.SetUpVisual(normalIMG)
		btn.SetOverVisual(hoverIMG)
		btn.SetDownVisual(overIMG)
		btn.SetEvent(lambda arg = param : callFunc(param))
		btn.SetToolTipText(tooltip, -30, 7, 2)
		btn.Show()
	
		self.buttonList.append(btn)
	
		self.SetSize(self.GetWidth(), len(self.buttonList) * 31)

	def RefreshChangedPageImage(self, page):
		for index in xrange(len(self.buttonList)):
			self.buttonList[index].SetUp()

		self.buttonList[page].Down()


	def Reposition(self, x, y):
		self.SetPosition(x-30, y+20)

