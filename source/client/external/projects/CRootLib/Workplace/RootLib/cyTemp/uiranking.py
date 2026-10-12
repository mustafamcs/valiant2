# -*- coding: cp949 -*-
#-1651219444
import ui, constInfo, localeInfo, app, uiScriptLocale

from uicharacter import FACE_IMAGE_DICT

rankList = [
        {
            "ranktype" : "STATS_POWER",
            "title" : uiScriptLocale.STATICS_15,
        },
        {
            "ranktype" : "STATS_MONSTER_KILLED",
            "title" : uiScriptLocale.STATICS_05,
        },
        {
            "ranktype" : "STATS_STONE_KILLED",
            "title" : uiScriptLocale.STATICS_06,
        },
        {
            "ranktype" : "STATS_BOSS_KILLED",
            "title" : uiScriptLocale.STATICS_07,
        },
        {
            "ranktype" : "STATS_PLAYER_KILLED",
            "title" : uiScriptLocale.STATICS_08,
        },
        {
            "ranktype" : "STATS_MONSTER_DAMAGE",
            "title" : uiScriptLocale.STATICS_02,
        },
        {
            "ranktype" : "STATS_STONE_DAMAGE",
            "title" : uiScriptLocale.STATICS_03,
        },
        {
            "ranktype" : "STATS_BOSS_DAMAGE",
            "title" : uiScriptLocale.STATICS_04,
        },
        {
            "ranktype" : "STATS_PLAYER_DAMAGE",
            "title" : uiScriptLocale.STATICS_01,
        },
        {
            "ranktype" : "STATS_OPENED_CHEST",
            "title" : uiScriptLocale.STATICS_13,
        },
        {
            "ranktype" : "STATS_FISHING",
            "title" : uiScriptLocale.STATICS_11,
        },
        {
            "ranktype" : "STATS_MINING",
            "title" : uiScriptLocale.STATICS_12,
        },
        {
            "ranktype" : "STATS_COMPLATE_DUNGEON",
            "title" : uiScriptLocale.STATICS_10,
        },
        {
            "ranktype" : "STATS_UPGRADE_ITEM",
            "title" : uiScriptLocale.STATICS_09,
        },
        {
            "ranktype" : "STATS_USE_ENCHANTED_ITEM",
            "title" : uiScriptLocale.STATICS_14,
        },
        {
            "ranktype" : "RANKING_ALIGN",
            "title" : uiScriptLocale.STATICS_16,
        },
        {
            "ranktype" : "RANKING_PLAY_TIME",
            "title" : uiScriptLocale.STATICS_17,
        }
	]

countryList = {
	0: "en",
	1: "en",
	2: "pt",
	3: "es",
	4: "fr",
	5: "de",
	6: "ro",
	7: "pl",
	8: "it",
	9: "cz",
	10: "hu",
	11: "tr",
}


class RankingWindow(ui.BoardWithTitleBar):
    def __init__(self):
        ui.BoardWithTitleBar.__init__(self)
        self.Index= 0
        self.LoadGeneralData()

    def __del__(self):
        ui.BoardWithTitleBar.__init__(self)

    def LoadGeneralData(self):
        self.SetSize(650, 467)
        self.SetCenterPosition()
        self.AddFlag("movable")

        self.SetTitleName(uiScriptLocale.GLOBAL_RANKING_TITLE)

        self.categoryMask = ui.Window()
        self.categoryMask.SetParent(self)
        self.categoryMask.SetPosition(10, 38)
        self.categoryMask.SetSize(200, 412)
        self.categoryMask.Show()

        self.categoryBackground = ui.BorderA()
        self.categoryBackground.SetParent(self)
        self.categoryBackground.SetPosition(10, 33)
        self.categoryBackground.SetSize(200, 391+31)
        self.categoryBackground.Show()

        self.informationsBackground = ui.BorderA()
        self.informationsBackground.SetParent(self)
        self.informationsBackground.SetPosition(215, 33)
        self.informationsBackground.SetSize(420, 391+31)
        self.informationsBackground.Show()

        self.bestplayerListBG = ui.MakeExpandedImageBox(self.informationsBackground, "d:/ymir work/ui/game/ranking/topranking_playerlistbg.png", 5, 6)

        self.playerRank = ui.MakeTextLineNew(self.bestplayerListBG, 9, 10, localeInfo.RANKING_PLAYER_RANK)
        self.playerName = ui.MakeTextLineNew(self.bestplayerListBG, 120, 10, localeInfo.RANKING_PLAYER_NAME)
        self.playerCountry = ui.MakeTextLineNew(self.bestplayerListBG, 233, 10, localeInfo.RANKING_PLAYER_COUNTRY)
        self.playerScore = ui.MakeTextLineNew(self.bestplayerListBG, 335, 10, localeInfo.RANKING_PLAYER_SCORE)

        self.LoadCategories()

        self.playerList = ui.ListBoxEx()
        self.playerList.SetParent(self.informationsBackground)
        self.playerList.SetPosition(15, 34)
        self.playerList.SetViewItemCount(11)
        self.playerList.SetItemStep(34)
        self.playerList.SetItemSize(200, 33)
        self.playerList.Show()

    def LoadCategories(self):
        self.categoryList = []

        for key in xrange(len(rankList)):
            category = RankingCategory(self, key)
            category.Show()
            self.categoryList.append(category)

        self.categoryScrollbar = ui.NewSlimScrollBar()
        self.categoryScrollbar.SetParent(self)
        self.categoryScrollbar.SetScrollBarSize(390+25)
        self.categoryScrollbar.SetPosition(210, 34)
        self.categoryScrollbar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
        self.categoryScrollbar.SetScrollStep(0.2)
        self.categoryScrollbar.Show()

        self.ResetScrollBarPos()
        self.ResizeScrollBar()	
        self.AdjustItemPositions()

        if app.ENABLE_WINDOW_ANIMATION:
            self.SetWindowAnimation()

    def LoadPlayerData(self, index = 0):
        self.playerList.RemoveAllItems()
        self.Index = index
        global rankList

        for j in xrange(10):
            if constInfo.GetFlag("ranking_%s_value_%d"%(rankList[index]["ranktype"], j)) == 0:
                continue

            playerRank = (j+1)
            resultItem = Player(self, playerRank, constInfo.GetFlag("ranking_%s_player_name_%d"%(rankList[index]["ranktype"], j)),
                                constInfo.GetFlag("ranking_%s_other_data_%d"%(rankList[index]["ranktype"], j)),
                                constInfo.GetFlag("ranking_%s_value_%d"%(rankList[index]["ranktype"], j)), 
                                constInfo.GetFlag("ranking_%s_race_%d"%(rankList[index]["ranktype"], j)))
            resultItem.Show()

            self.playerList.AppendItem(resultItem)

        resultItem = Player(self, constInfo.GetFlag("ranking_%s_my_player_order"%(rankList[index]["ranktype"])),
                            constInfo.GetFlag("ranking_%s_player_name_%d"%(rankList[index]["ranktype"], 11)),
                            constInfo.GetFlag("ranking_%s_other_data_%d"%(rankList[index]["ranktype"], 11)),
                            constInfo.GetFlag("ranking_%s_value_%d"%(rankList[index]["ranktype"], 11)), 
                            constInfo.GetFlag("ranking_%s_race_%d"%(rankList[index]["ranktype"], 11)), True)
        resultItem.Show()

        self.playerList.AppendItem(resultItem)

        for idx, button in enumerate(self.categoryList):
            if idx == self.Index:
                button.categoryButton.LoadImage("d:/ymir work/ui/game/ranking/btn_down.png")
            else:
                button.categoryButton.LoadImage("d:/ymir work/ui/game/ranking/btn_normal.png")

        if len(rankList) > 7:
            self.categoryScrollbar.Show()
        else:
            self.categoryScrollbar.Hide()

    def __OnScroll(self):
        self.AdjustItemPositions(True)

    def Open(self):
        self.Show()
        self.LoadPlayerData(self.Index)

    def Close(self):
        self.Hide()

    def OnPressEscapeKey(self):
        self.Close()

    def ResetScrollBarPos(self):
        self.categoryScrollbar.SetPos(0)

    def GetTotalItemHeight(self):
        totalHeight = 0
        
        if self.categoryList:
            for itemH in self.categoryList:
                totalHeight += itemH.GetHeight()
            
        return totalHeight + 7

    def ResizeScrollBar(self):

        totalHeight = float(self.GetTotalItemHeight())

        if totalHeight:
            scrollBarHeight = min(float(self.categoryBackground.GetHeight() - 10) / totalHeight, 1.0)
        else:
            scrollBarHeight = 1.0
            
        self.categoryScrollbar.SetMiddleBarSize(scrollBarHeight)

    def AdjustItemPositions(self, scrolling=False):
        scrollPos = self.categoryScrollbar.GetPos()
        totalHeight = self.GetTotalItemHeight() - self.categoryBackground.GetHeight()

        idx = 0

        CurIdx, yAccumulate = 0, 5
        for item in self.categoryList[idx:]:
            if scrolling:
                setPos = yAccumulate - int(scrollPos * totalHeight)
                item.categoryButton.SetPosition(6, setPos)
            else:
                item.categoryButton.SetPosition(6, yAccumulate)
                
            # item.categoryButton.SetBasePosition(0, yAccumulate)

            CurIdx += 1
            #Mesafe
            yAccumulate += item.categoryButton.GetHeight()

    def OnRender(self):
        xList, yList = self.categoryBackground.GetGlobalPosition()
        widthList, heightList = self.categoryBackground.GetWidth(), self.categoryBackground.GetHeight()
    
        for itemH in self.categoryList:
            itemH.categoryButton.SetClipRect(xList, yList + 3, xList + widthList, yList + heightList -5)
            itemH.categoryImage.SetClipRect(xList, yList + 3, xList + widthList, yList + heightList -5)
            itemH.categoryButton.SetClippingMaskWindow(self.categoryMask)

    def OnRunMouseWheel(self, nLen):
        if self.categoryScrollbar:
            if nLen > 0:
                self.categoryScrollbar.OnUp()
            else:
                self.categoryScrollbar.OnDown()

class RankingCategory(ui.Window):
    def __init__(self, parent, index):
        ui.Window.__init__(self)

        self.categoryButton = ui.MakeExpandedImageBox(parent.categoryBackground, "d:/ymir work/ui/game/ranking/btn_normal.png", 0, 0)
        self.categoryButton.SetPosition(6, 5 if index == 0 else index*self.categoryButton.GetHeight()+5)
        self.categoryButton.OnMouseLeftButtonDown = lambda arg = index : parent.LoadPlayerData(arg)

        self.categoryImage = ui.MakeExpandedImageBox(self.categoryButton, "d:/ymir work/ui/game/ranking/category_icons/rank_{}.png".format(index), 7, 2)

        self.categoryTitle = ui.MakeTextLineNew(self.categoryButton, 79, 19, rankList[index]["title"])
        if len(self.categoryTitle.GetText()) > 20:
            self.categoryTitle.SetText(self.categoryTitle.GetText()[:18] + "...")

        self.SetSize(self.categoryButton.GetWidth(), self.categoryButton.GetHeight())

    def __del__(self):
        ui.Window.__init__(self)

    def SetBasePosition(self, x, y):
        self.xBase = x
        self.yBase = y

    def GetBasePosition(self):
        return (self.xBase, self.yBase)

class Player(ui.Window):
    def __init__(self, parent, index, name, flag, value, race = 0, myStats = False):
        ui.Window.__init__(self)
        self.parent = parent
        self.SetParent(parent)
        self.Index = int(index)
        self.race = int(race if race != None else 0)
        self.name = str(name)
        self.flag = int(flag) if flag != None else 0
        self.value = str(value)
        self.myStats = myStats
        self.SetSize(403, 28)
        self.loadInformations()

    def loadInformations(self):
        if str(self.name) == "None":
            return

        color = "|cffffffff"
        if not self.myStats:
            if self.Index == 1:
                color = "|cffFFC500" #1
            elif self.Index == 2:
                color = "|cFFC0C0C0" #2
            elif self.Index == 3:
                color = "|cFF8B4513" #3

        if self.Index > 3 or self.myStats:
            if not self.myStats or (self.myStats and int(self.value) != 0):
                self.orderList = ui.TextLine()
                self.orderList.SetParent(self)
                self.orderList.SetText("{}".format(self.Index))
                self.orderList.SetHorizontalAlignLeft()
                self.orderList.SetWindowVerticalAlignCenter()
                self.orderList.SetWindowHorizontalAlignCenter()
                self.orderList.SetPosition(-77, 0)
                self.orderList.Show()

        self.raceImage = ui.ExpandedImageBox()
        self.raceImage.SetParent(self)
        self.raceImage.LoadImage(FACE_IMAGE_DICT[self.race])
        self.raceImage.SetPosition(75, 13)
        self.raceImage.SetScale(0.50, 0.50)
        self.raceImage.Show()

        self.NameText = ui.TextLine()
        self.NameText.SetParent(self)
        self.NameText.SetText("%s%s" % (color, self.name))
        self.NameText.SetHorizontalAlignLeft()
        self.NameText.SetWindowVerticalAlignCenter()
        self.NameText.SetWindowHorizontalAlignCenter()
        self.NameText.SetPosition(0, 0)
        self.NameText.Show()

        self.flagImage = ui.ExpandedImageBox()
        self.flagImage.SetParent(self)
        self.flagImage.LoadImage("d:/ymir work/ui/login_new/flags/flag_%s_down.tga" % countryList[self.flag])
        # self.flagImage.SetHorizontalAlignRight()
        self.flagImage.SetWindowVerticalAlignCenter()
        self.flagImage.SetWindowHorizontalAlignCenter()
        self.flagImage.SetPosition(135, 8)
        self.flagImage.Show()

        self.valueText = ui.TextLine()
        self.valueText.SetParent(self)
        self.valueText.SetText("%s%s" % (color,localeInfo.NumberToDecimal(self.value)))
        self.valueText.SetHorizontalAlignRight()
        self.valueText.SetWindowVerticalAlignCenter()
        self.valueText.SetWindowHorizontalAlignCenter()
        self.valueText.Show()

        self.valueText.SetPosition(215 + len(self.valueText.GetText())*2, 0)
