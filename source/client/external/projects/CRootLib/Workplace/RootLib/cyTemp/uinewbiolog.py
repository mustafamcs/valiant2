# -*- coding: cp949 -*-
#1775447965
import ui, item, uiToolTip, chat, player, localeInfo, app, biolog, net

class BiologWindow(ui.BoardWithTitleBar):

    PATH_BASE = "d:/ymir work/ui/game/biolog_system/"

    MAX_WIDTH = 310
    MAX_HEIGHT = 235

    SHOP_INDEX = 6

    soulStoneMobVnumList = {    30220 : 192,
                                30221 : 193,
                                30222 : 8061, 
                                }

    def __init__(self):
        ui.BoardWithTitleBar.__init__(self)
        self.resetInfo()
        self.LoadInformationsData()
        self.CreateWindow()

        if app.ENABLE_WINDOW_ANIMATION:
            self.SetWindowAnimation()

    def __del__(self):
        ui.BoardWithTitleBar.__del__(self)

    def resetInfo(self):
        self.itemTooltip = uiToolTip.ItemToolTip()
        self.InformationList = {}
        self.interface = None

    def CreateWindow(self):
        self.SetSize(self.MAX_WIDTH, self.MAX_HEIGHT)
        self.SetCenterPosition()
        self.AddFlag("movable")
        self.SetTitleName("Biolog")

        self.topBG = ui.ThinBoard()
        self.topBG.SetParent(self)
        self.topBG.SetSize(self.MAX_WIDTH-23, 50)
        self.topBG.SetPosition(12, 32)
        self.topBG.Show()

        self.biologTextBG = ui.ThinBoardCircle()
        self.biologTextBG.SetParent(self.topBG)
        self.biologTextBG.SetSize(230, 20)
        self.biologTextBG.SetPosition(45, 13)
        self.biologTextBG.Show()

        self.biologHead = ui.ExpandedImageBox()
        self.biologHead.SetParent(self.topBG)
        self.biologHead.LoadImage(self.PATH_BASE + "biolog_icon.png")
        self.biologHead.SetPosition(9, 5)
        self.biologHead.Show()

        self.biologText = ui.TextLine()
        self.biologText.SetParent(self.biologTextBG)
        self.biologText.SetPosition(5, 0)
        self.biologText.SetHorizontalAlignCenter()
        self.biologText.SetVerticalAlignCenter()
        self.biologText.SetWindowHorizontalAlignCenter()
        self.biologText.SetWindowVerticalAlignCenter()
        self.biologText.SetText("Current Mission: Orc Tooth")
        self.biologText.Show()

        self.progressBackground = ui.ExpandedImageBox()
        self.progressBackground.SetParent(self.topBG)
        self.progressBackground.LoadImage(self.PATH_BASE + "progress_background.png")
        self.progressBackground.SetPosition(-4, 52)
        self.progressBackground.SetScale(0.95, 0.95)
        self.progressBackground.Show()

        self.progessText = ui.TextLine()
        self.progessText.SetParent(self.progressBackground)
        self.progessText.SetPosition(8, 8)
        self.progessText.SetText(localeInfo.BIOLOG_PROGRESS_STATE)
        self.progessText.Show()

        # self.progressBG = ui.ExpandedImageBox()
        # self.progressBG.SetParent(self.progressBackground)
        # self.progressBG.LoadImage(self.PATH_BASE + "progressbar_full.png")
        # self.progressBG.SetClipRect(50)
        # self.progressBG.Show()

        self.progressGauge = ui.Gauge()
        self.progressGauge.SetParent(self.progressBackground)
        self.progressGauge.MakeGauge(155, "white")
        self.progressGauge.SetPosition(100, 12)
        self.progressGauge.Show()

        self.countText = ui.TextLine()
        self.countText.SetParent(self.progressBackground)
        self.countText.SetPosition(260, 8)
        self.countText.SetText("[0/10]")
        self.countText.Show()

        self.itemInfoBG = ui.ExpandedImageBox()
        self.itemInfoBG.SetParent(self.topBG)
        self.itemInfoBG.LoadImage(self.PATH_BASE + "item_info_background.png")
        self.itemInfoBG.SetPosition(-4, 87)
        self.itemInfoBG.SetScale(0.95, 0.95)
        self.itemInfoBG.Show()

        self.btnShop = ui.MakeButton(self, 260, 128, False, self.PATH_BASE, "shop_button01.png", "shop_button02.png", "shop_button03.png")
        self.btnSubmit = ui.MakeButton(self, 5, 165, False, self.PATH_BASE, "submit_button01.png", "submit_button02.png", "submit_button03.png")
        self.btnSubmit.SetEvent(ui.__mem_func__(self.DeliveryItem))
        self.btnShop.SetEvent(ui.__mem_func__(self.OpenShop))
        self.btnSubmit.SetText(localeInfo.BIOLOG_DELIVER_ITEM)

        self.missionState = ui.ExpandedImageBox()
        self.missionState.SetParent(self)
        self.missionState.LoadImage(self.PATH_BASE + "available.png")
        self.missionState.SetPosition(7, 197)
        self.missionState.Show()

        self.missionStateText = ui.TextLine()
        self.missionStateText.SetParent(self.missionState)
        self.missionStateText.SetPosition(0, 0)
        self.missionStateText.SetText(localeInfo.BIOLOG_CAN_DELIVER_NEXT_ITEM)
        self.missionStateText.SetHorizontalAlignCenter()
        self.missionStateText.SetVerticalAlignCenter()
        self.missionStateText.SetWindowHorizontalAlignCenter()
        self.missionStateText.SetWindowVerticalAlignCenter()
        self.missionStateText.Show()

        self.essenceItem = ui.ExpandedImageBox()
        self.essenceItem.SetParent(self)
        self.essenceItem.SetWindowHorizontalAlignRight()
        self.essenceItem.SetPosition(154, 125)
        self.essenceItem.SAFE_SetStringEvent("MOUSE_LEFT_DOWN", self.OnClickCooldownCheckbox)
        self.essenceItem.SAFE_SetStringEvent("MOUSE_OVER_IN", self.OverInSupport)
        self.essenceItem.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.OnOverOutItem)
        item.SelectItem(30629)
        image = item.GetIconImageFileName()
        self.essenceItem.LoadImage(image)
        self.essenceItem.Show()

        self.essenceItemCheckbox = ui.ExpandedImageBox()
        self.essenceItemCheckbox.SetParent(self)
        self.essenceItemCheckbox.SetPosition(120, 134)
        self.essenceItemCheckbox.LoadImage(self.PATH_BASE + "select_button01.png")
        self.essenceItemCheckbox.IsChecked = False
        self.essenceItemCheckbox.Show()
        self.essenceItemCheckbox.OnMouseLeftButtonDown = ui.__mem_func__(self.OnClickEssenceCheckbox)

        self.resetCooldownItem = ui.ExpandedImageBox()
        self.resetCooldownItem.SetParent(self)
        self.resetCooldownItem.SetWindowHorizontalAlignRight()
        self.resetCooldownItem.SetPosition(220, 125)
        self.resetCooldownItem.SAFE_SetStringEvent("MOUSE_LEFT_DOWN", self.OnClickEssenceCheckbox)
        self.resetCooldownItem.SAFE_SetStringEvent("MOUSE_OVER_IN", self.OverInSupport2)
        self.resetCooldownItem.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.OnOverOutItem)
        item.SelectItem(71035)
        image = item.GetIconImageFileName()
        self.resetCooldownItem.LoadImage(image)
        self.resetCooldownItem.Show()

        self.resetCooldownCheckbox = ui.ExpandedImageBox()
        self.resetCooldownCheckbox.SetParent(self)
        self.resetCooldownCheckbox.SetPosition(190, 134)
        self.resetCooldownCheckbox.LoadImage(self.PATH_BASE + "select_button01.png")
        self.resetCooldownCheckbox.IsChecked = False
        self.resetCooldownCheckbox.Show()
        self.resetCooldownCheckbox.OnMouseLeftButtonDown = ui.__mem_func__(self.OnClickCooldownCheckbox)

        self.currentItemSlot = ui.ImageBox()
        self.currentItemSlot.SetParent(self)
        self.currentItemSlot.SetPosition(13.2, 126)
        self.currentItemSlot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
        self.currentItemSlot.Show()

        self.currentItem = ui.SlotWindow()
        self.currentItem.SetParent(self.currentItemSlot)
        self.currentItem.SetSize(32, 32)
        self.currentItem.AppendSlot(0,1,1,32,32)
        self.currentItem.SetPosition(-1, -1)
        self.currentItem.Show()
        self.currentItem.SetItemSlot(0, self.InformationList["biologItem"])
        self.currentItem.SetOverInItemEvent(lambda slotNumber, iVnum = self.InformationList["biologItem"]: self.OnOverInItem(slotNumber, self.InformationList["biologItem"]))
        self.currentItem.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

        bonussesBGSize = (290, 34)

        self.bonussesBG = ui.BorderA()
        self.bonussesBG.SetParent(self.topBG)
        self.bonussesBG.SetSize(*bonussesBGSize)
        self.bonussesBG.SetPosition(-4, 200)
        self.bonussesBG.Show()

        self.bonusTitle = ui.TextLine()
        self.bonusTitle.SetParent(self.bonussesBG)
        self.bonusTitle.SetPosition(0, 0)
        self.bonusTitle.SetText("BonusName")
        self.bonusTitle.SetHorizontalAlignCenter()
        self.bonusTitle.SetVerticalAlignCenter()
        self.bonusTitle.SetWindowHorizontalAlignCenter()
        self.bonusTitle.SetWindowVerticalAlignCenter()
        self.bonusTitle.Show()

        self.bonusses2BG = ui.BorderA()
        self.bonusses2BG.SetParent(self.topBG)
        self.bonusses2BG.SetPosition(-4, 234)
        self.bonusses2BG.SetSize(*bonussesBGSize)
        self.bonusses2BG.Show()

        self.bonus2Title = ui.TextLine()
        self.bonus2Title.SetParent(self.bonusses2BG)
        self.bonus2Title.SetPosition(0, 0)
        self.bonus2Title.SetText("BonusName")
        self.bonus2Title.SetHorizontalAlignCenter()
        self.bonus2Title.SetVerticalAlignCenter()
        self.bonus2Title.SetWindowHorizontalAlignCenter()
        self.bonus2Title.SetWindowVerticalAlignCenter()
        self.bonus2Title.Show()

        self.soulStoneBG = ui.ExpandedImageBox()
        self.soulStoneBG.SetParent(self.topBG)
        self.soulStoneBG.LoadImage(self.PATH_BASE + "unavailable.png")
        self.soulStoneBG.SetPosition(0, 235)
        self.soulStoneBG.SetScale(0.95, 0.95)
        self.soulStoneBG.Hide()

        self.soulStoneTitle = ui.TextLine()
        self.soulStoneTitle.SetParent(self.soulStoneBG)
        self.soulStoneTitle.SetPosition(0, 0)
        self.soulStoneTitle.SetText("SoulStone Info")
        self.soulStoneTitle.SetHorizontalAlignCenter()
        self.soulStoneTitle.SetVerticalAlignCenter()
        self.soulStoneTitle.SetWindowHorizontalAlignCenter()
        self.soulStoneTitle.SetWindowVerticalAlignCenter()
        self.soulStoneTitle.Hide()

    def Open(self):

        if player.GetStatus(player.LEVEL)<30:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.YOU_NEED_LEVEL.format(30))
            return

        self.Show()

    def Close(self):
        self.Hide()
        self.OnOverOutItem()

    def OnPressEscapeKey(self):
        self.Close()
        return True

    def OnClickCooldownCheckbox(self):
        if self.resetCooldownCheckbox.IsChecked:
            self.resetCooldownCheckbox.IsChecked = False
            self.resetCooldownCheckbox.LoadImage(self.PATH_BASE + "select_button01.png")
        else:
            self.resetCooldownCheckbox.IsChecked = True
            self.resetCooldownCheckbox.LoadImage(self.PATH_BASE + "select_button02.png")

    def OnClickEssenceCheckbox(self):
        if self.essenceItemCheckbox.IsChecked:
            self.essenceItemCheckbox.IsChecked = False
            self.essenceItemCheckbox.LoadImage(self.PATH_BASE + "select_button01.png")
        else:
            self.essenceItemCheckbox.IsChecked = True
            self.essenceItemCheckbox.LoadImage(self.PATH_BASE + "select_button02.png")

    def LoadInformationsData(self):
        biologbonus = []
        for y in xrange(4):
            biologbonus.append({})

        vnum,count,biologbonus[0][0], biologbonus[0][1], biologbonus[1][0], biologbonus[1][1],\
            biologbonus[2][0], biologbonus[2][1],biologbonus[3][0], biologbonus[3][1] = biolog.SendInformations()
        
        given_count, time = biolog.SendState()

        self.InformationList = {
                "biologItem" : vnum,
                "biologCooldown" : time + app.GetTime(),
                "biologCountInformations" : [given_count, count],
                "biologBonusList": [["","","",""]],
            }

        #constInfo.BIOLOG_SECOND
        for i in xrange (4):
            BonusText = " "
            if biologbonus[i][0] != 0:
                BonusText = uiToolTip.GET_AFFECT_STRING(biologbonus[i][0],biologbonus[i][1])
            self.InformationList["biologBonusList"][0][i] = BonusText

    def OverInSupport(self):
        if self.itemTooltip:
            self.itemTooltip.ClearToolTip()
            self.itemTooltip.AddItemData(30629, 0)

    def OverInSupport2(self):
        if self.itemTooltip:
            self.itemTooltip.ClearToolTip()
            self.itemTooltip.AddItemData(71035, 0)

    def OnOverInItem(self, slotNumber, iVnum):
        if self.itemTooltip:
            self.itemTooltip.ClearToolTip()
            self.itemTooltip.AddItemData(iVnum, 0)

    def OnOverOutItem(self):
        if self.itemTooltip:
            self.itemTooltip.HideToolTip()

    def LevelUpdate(self):
        self.LoadInformationsData()

        self.bonusTitle.SetText("{}".format(self.InformationList["biologBonusList"][0][0])) # bir tane bonus olacak diye boyle
        self.bonus2Title.SetText("{}".format(self.InformationList["biologBonusList"][0][1])) # bir tane bonus olacak diye boyle

        self.currentItem.SetItemSlot(0, self.InformationList["biologItem"])

        item.SelectItem(self.InformationList["biologItem"])
        self.biologText.SetText(localeInfo.BIOLOG_CURRENT_MISSION.format(item.GetItemName()))
        self.countText.SetText("[{}/{}]".format(self.InformationList["biologCountInformations"][0], self.InformationList["biologCountInformations"][1]))
        self.progressGauge.SetPercentage(max(0, self.InformationList["biologCountInformations"][0]), self.InformationList["biologCountInformations"][1])

        if len(self.InformationList["biologBonusList"][0][0]) > 1:
            self.bonusTitle.Show()
            self.bonussesBG.Show()

            if len(self.InformationList["biologBonusList"][0][1]) > 1:
                self.bonus2Title.Show()
                self.bonusses2BG.Show()

                # if self.InformationList["biologCountInformations"][1] == 1:
                #     self.SetSize(self.MAX_WIDTH, self.MAX_HEIGHT + 105)
                #     # self.soulStoneBG.Show()
                #     # self.soulStoneTitle.Show()
                #     # self.soulStoneTitle.SetText(localeInfo.BIOLOG_SOULSTONE_INFO.format(nonplayer.GetMonsterName(self.soulStoneMobVnumList[self.InformationList["biologItem"]])))
                #     # self.soulStoneBG.SetPosition(0, 268)
                #     self.soulStoneTitle.SetPosition(20, 278)
                # else:
                self.SetSize(self.MAX_WIDTH, self.MAX_HEIGHT + 75)
                self.soulStoneBG.Hide()
                self.soulStoneTitle.Hide()
            else:
                self.bonus2Title.Hide()
                self.bonusses2BG.Hide()

                # if self.InformationList["biologCountInformations"][1] == 1:
                #     self.SetSize(self.MAX_WIDTH, self.MAX_HEIGHT + 75)
                #     self.soulStoneBG.SetPosition(0, 235)
                #     # self.soulStoneTitle.SetPosition(20, 245)
                #     self.soulStoneBG.Show()
                    # self.soulStoneTitle.Show()
                    # self.soulStoneTitle.SetText(localeInfo.BIOLOG_SOULSTONE_INFO.format(nonplayer.GetMonsterName(self.soulStoneMobVnumList[self.InformationList["biologItem"]])))
                # else:
                self.SetSize(self.MAX_WIDTH, self.MAX_HEIGHT + 40)
                self.soulStoneBG.Hide()
                self.soulStoneTitle.Hide()
        else:
            self.bonusTitle.Hide()
            self.bonussesBG.Hide()
            self.bonus2Title.Hide()
            self.bonusses2BG.Hide()
            self.SetSize(self.MAX_WIDTH, self.MAX_HEIGHT)
            self.soulStoneBG.SetPosition(0, 235)
            self.soulStoneTitle.SetPosition(20, 245)

        if biolog.IsMaxLevel():
            self.Close()

    def OnUpdate(self):
        if self.InformationList["biologCooldown"] >= app.GetTime():
            self.missionStateText.SetText(localeInfo.BIOLOG_REMAINING_TIME + localeInfo.SecondToHMS(self.InformationList["biologCooldown"] - app.GetTime()))
            self.missionState.LoadImage(self.PATH_BASE + "unavailable.png")
        else:
            self.missionStateText.SetText(localeInfo.BIOLOG_CAN_DELIVER_NEXT_ITEM)
            self.missionState.LoadImage(self.PATH_BASE + "available.png")

    def CountUpdate(self):
        given_count, time = biolog.SendState()
        self.InformationList["biologCooldown"] = time + app.GetTime()
        self.InformationList["biologCountInformations"][0] = given_count
        item.SelectItem(self.InformationList["biologItem"])
        self.biologText.SetText(localeInfo.BIOLOG_CURRENT_MISSION.format(item.GetItemName()))
        self.countText.SetText("[{}/{}]".format(self.InformationList["biologCountInformations"][0], self.InformationList["biologCountInformations"][1]))
        self.progressGauge.SetPercentage(max(0, self.InformationList["biologCountInformations"][0]), self.InformationList["biologCountInformations"][1])

    def DeliveryItem(self):
        if player.GetItemCountByVnum(self.InformationList["biologItem"]) == 0:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.BIOLOG_NOT_ENOUGH_MATERIAL)
            return

        remainingTime = self.InformationList["biologCooldown"] >= app.GetTime()

        if remainingTime:
            if not self.resetCooldownCheckbox.IsChecked or (not self.resetCooldownCheckbox.IsChecked and self.essenceItemCheckbox.IsChecked):
                chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.BIOLOG_COOLDOWN_NOT_FINISHED)
                return
        else:
            if self.resetCooldownCheckbox.IsChecked:
                chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.BIOLOG_COOLDOWN_CANT_RESET_CUZ_NO_COOLDOWN)
                return

        randomPosX = app.GetRandom(-75, 75)
        randomPosY = app.GetRandom(-50, 50)

        x, y = self.GetGlobalPosition()

        self.SetPosition(x+randomPosX, y+randomPosY)

        biolog.DeliveryItem(0, self.essenceItemCheckbox.IsChecked, self.resetCooldownCheckbox.IsChecked)

    def OpenShop(self):
        net.SendChatPacket("/open_this_distance_npc %d" % self.SHOP_INDEX)

    def BindInterface(self, interface):
        self.interface = interface
