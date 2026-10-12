# -*- coding: cp949 -*-
#1344515789
import ui
import net
import app
import localeInfo

SHOP_CONFIG = {
	0 : {
		'shop_name'			:	localeInfo.DISTANCE_NPC_SHOP_TITLE_0,
		"shop_id"			:	1,
	},
	1 : {
		'shop_name'			:	localeInfo.DISTANCE_NPC_SHOP_TITLE_1,
		"shop_id"			:	4,
	},
	2 : {
		'shop_name'			:	localeInfo.DISTANCE_NPC_SHOP_TITLE_2,
		"shop_id"			:	6,
	},
	3 : {
		'shop_name'			:	localeInfo.DISTANCE_NPC_SHOP_TITLE_3,
		"shop_id"			:	3,
	},
	4 : {
		'shop_name'			:	localeInfo.DISTANCE_NPC_SHOP_TITLE_4,
		"shop_id"			:	2,
	},
	5 : {
		'shop_name'			:	localeInfo.DISTANCE_NPC_SHOP_TITLE_5,
		"shop_id"			:	8,
	},
}

buttonCountPerScroll = 5 if len(SHOP_CONFIG) > 5 else len(SHOP_CONFIG)
maxShopCount = len(SHOP_CONFIG)

class DistanceShoppingWindow(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.ResetInformations()
		self.__Load()
		self.SetCenterPosition()

		if app.ENABLE_WINDOW_ANIMATION:
			self.SetWindowAnimation()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def ResetInformations(self):
		self.board = None
		self.scrollbar = None
		self.btns = None

	def Destroy(self):
		self.ClearDictionary()
		self.ResetInformations()

	def __Load(self):

		self.AddFlag("movable")
		self.board = ui.MakeBoardWithTitleBar(self, "not_pick", localeInfo.DISTANCE_NPC_TITLE, ui.__mem_func__(self.Close), 221, 284)
		self.SetSize(self.board.GetWidth(), self.board.GetHeight())

		self.scrollbar = ui.ScrollBarNew()
		self.scrollbar.SetParent(self.board)
		self.scrollbar.SetScrollBarSize(234)
		self.scrollbar.SetPosition(197, 37)
		self.scrollbar.Show()
		
		self.btns = []
		
		for i in xrange(min(buttonCountPerScroll, maxShopCount)):
			x = 11
			if i % 1 != 0:
				x = 10 + 356
			
			self.btns.append(Buttons(self.board, x, 30 + 48 * i, i))
			self.btns[i].SetupBoard(i)
			self.btns[i].SetShopInfo(i)
			
		if maxShopCount <= buttonCountPerScroll:
			self.scrollbar.Hide()
		else:
			self.scrollbar.SetMiddleBarSize(float(buttonCountPerScroll) / float(maxShopCount))
			self.scrollbar.Show()
			
		self.scrollbar.SetScrollEvent(self.__OnScroll)
		
	def __OnScroll(self):
		buttonCountPerScroll = int(len(self.btns))
		pos = int(self.scrollbar.GetPos() * (maxShopCount - buttonCountPerScroll))
		if pos % 1 == 0:
			i = 0
			while i < buttonCountPerScroll - 1:
				realPos = i + pos
				self.btns[i].SetupBoard(realPos)
				self.btns[i+1].SetupBoard(realPos+1)
				self.btns[i].SetShopInfo(realPos)
				self.btns[i+1].SetShopInfo(realPos+1)
				i = i + 1

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def OnRunMouseWheel(self, nLen):
		scroll = self.scrollbar
		if nLen > 0:
			scroll.OnUp()
		else:
			scroll.OnDown()
			
		return True

class Buttons(ui.ScriptWindow):
	def __init__(self, parent, x, y, index):
		ui.ScriptWindow.__init__(self)
		self.board = self.CreateBoard(parent, 181,46, x, y+4)
		self.index = index	
			
		self.gui = {
				'buttons' : {
					'openshop' :	self.CreateButton(self.board, 0, 0, lambda: self.OpenDistanceShop()),
					'shop_name' :		self.CreateTextline(self.board, 12-2, 14, 1),
					},
				}
		
	def OpenDistanceShop(self):
		net.SendChatPacket("/open_this_distance_npc %d" % SHOP_CONFIG[self.index]['shop_id'])
		
	def SetupBoard(self, index):
		self.index = index
		self.gui['buttons']['openshop'].SetUpVisual("d:/ymir work/ui/transparent_board.tga")
		self.gui['buttons']['openshop'].SetOverVisual("d:/ymir work/ui/transparent_board_overin.tga")
		self.gui['buttons']['openshop'].SetDownVisual("d:/ymir work/ui/transparent_board.tga")

	def SetShopInfo(self, index):
		self.index = index
		self.gui['buttons']['shop_name'].SetText(SHOP_CONFIG[index]['shop_name'])
		
	def HideBoard(self):
		self.board.Hide()
		
	def ShowBoard(self):
		self.board.Show()
	
	def CreateTextline(self, parent, x, y, val):
		textline = ui.TextLine()
		textline.SetParent(parent)
		textline.SetPosition(x,y)
		if val == 1:
			textline.SetHorizontalAlignLeft()
		elif val == 2:
			textline.SetHorizontalAlignRight()
		textline.Show()
		return textline
		
	def CreateBoard(self, parent, width, height, x, y):
		board = ui.ThinBoard()
		board.SetParent(parent)
		board.SetSize(width, height)
		board.SetPosition(x, y)
		board.SetTop()
		board.Show()
		return board
		
	def CreateButton(self, parent, x, y, event):
		button = ui.Button()
		button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual("d:/ymir work/ui/transparent_board.tga")
		button.SetOverVisual("d:/ymir work/ui/transparent_board_overin.tga")
		button.SetDownVisual("d:/ymir work/ui/transparent_board.tga")
		button.SetEvent(event)
		button.Show()
		return button
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.Hide()
