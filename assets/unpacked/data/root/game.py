import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgr
import player
import chat
import textTail
import net
import wndMgr
import systemSetting
import snd
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import exchange
import ime
import ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiTarget, math

import uiPrivateShopBuilder

import mouseModule
import localeInfo

import interfaceModule

import stringCommander

import uiToolTip

if app.ENABLE_OFFLINE_SHOP:
    import uiOfflineShop, offlineshop

if app.ENABLE_GLOBAL_RANKING:
    import uiranking
    import ranking

if app.ENABLE_ITEMSHOP:
    import uiItemShopNew

if app.ENABLE_DUNGEON_INFO:
    import uiBossTimer
    import dungeonInfo
    import nonplayer

if app.ENABLE_MINING_RENEWAL:
    import uiminingrenewal

# import lightwork

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = True
SCREENSHOT_DIR = None

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0

if app.ENABLE_IN_GAME_LOG_SYSTEM:
    import uiingamelog

if app.ENABLE_PM_ALL_SEND_SYSTEM:
    import uisendpmall

# if app.ENABLE_BOT_CONTROL:
import uisecurity
import uivalianttools

class GameWindow(ui.ScriptWindow):
    def __init__(self, stream):
        ui.ScriptWindow.__init__(self, "GAME")
        self.SetWindowName("game")
        net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
        player.SetGameWindow(self)

        self.quickSlotPageIndex = 0
        self.lastPKModeSendedTime = 0
        self.pressNumber = None

        if app.ENABLE_BOT_CONTROL:
            self.botControlWnd = None

        self.guildWarQuestionDialog = None
        self.interface = None
        self.targetBoard = None
        self.mapNameShower = None
        self.affectShower = None
        self.playerGauge = None
        if app.ENABLE_FISHING_RENEWAL:
            self.FishGame = None
        if app.ENABLE_MINING_RENEWAL:
            self.wndMiningGame = None
        self.stream=stream
        self.interface = interfaceModule.Interface(self)
        constInfo.SetGameInstance(self)
        self.interface.MakeInterface()
        self.interface.ShowDefaultWindows()

        self.curtain = uiPhaseCurtain.PhaseCurtain()
        # self.curtain.speed = 0.03
        self.curtain.Hide()

        self.targetBoard = uiTarget.TargetBoard()
        self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
        self.targetBoard.Hide()

        if app.ENABLE_OFFLINE_SHOP:
            offlineshop.HideShopNames()

        self.mapNameShower = uiMapNameShower.MapNameShower()
        self.affectShower = uiAffectShower.AffectShower()

        self.playerGauge = uiPlayerGauge.PlayerGauge(self)
        self.playerGauge.Hide()

        self.itemDropQuestionDialog = None

        self.__SetQuickSlotMode()

        if app.ENABLE_GLOBAL_RANKING:
            self.rankingWindow = None

        if app.ENABLE_IN_GAME_LOG_SYSTEM:
            self.wndInGameLog = None

        if app.ENABLE_PM_ALL_SEND_SYSTEM:
            self.whisperAdmin = uisendpmall.AdminWhisperManager()
            self.whisperAdmin.Close()

        if app.ENABLE_AUTO_SHOUT:
            self.lastShoutTime = 0

        if app.ENABLE_SKYBOX_SELECT:
            self.interface.wndgameOption.RefreshSkyBoxButtons()

        if app.ENABLE_DUNGEON_INFO:
            self.wndBossTimer = None

        if app.ENABLE_MOVIEMODE_CAMERA:
            self.isFreeCamera = False
            self.ResetFreeCam()

        self.wndDropInfoTracker = None
        if getattr(app, "ENABLE_DROP_INFO_WINDOW", 0):
            self.wndDropInfoTracker = uivalianttools.DropInfoTrackerWindow()

        self.wndBuyBack = None
        self.wndGmItemRestore = None
        if getattr(app, "ENABLE_BUY_BACK_ITEM", 0):
            self.wndBuyBack = uivalianttools.BuyBackWindow()
            self.wndBuyBack.Hide()
            self.wndGmItemRestore = uivalianttools.GmItemRestoreWindow()
            self.wndGmItemRestore.Hide()

        self.__ServerCommand_Build()
        self.__ProcessPreservedServerCommand()

    def __del__(self):
        player.SetGameWindow(0)
        net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
        ui.ScriptWindow.__del__(self)

    def Open(self):
        app.SetFrameSkip(1)

        self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

        self.quickSlotPageIndex = 0
        self.PickingCharacterIndex = -1
        self.PickingItemIndex = -1
        self.ShowNameFlag = False

        self.enableXMasBoom = False
        self.startTimeXMasBoom = 0.0
        self.indexXMasBoom = 0

        global cameraDistance, cameraPitch, cameraRotation, cameraHeight

        app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

        constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
        constInfo.SET_DEFAULT_CHRNAME_COLOR()
        constInfo.SET_DEFAULT_FOG_LEVEL()
        constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
        constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
        constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

        # TWO_HANDED_WEAPON_ATTACK_SPEED_UP
        constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
        # END_OF_TWO_HANDED_WEAPON_ATTACK_SPEED_UP

        import event
        event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

        textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

        self.__BuildKeyDict()

        # PRIVATE_SHOP_PRICE_LIST
        uiPrivateShopBuilder.Clear()
        # END_OF_PRIVATE_SHOP_PRICE_LIST

        # UNKNOWN_UPDATE
        exchange.InitTrading()
        # END_OF_UNKNOWN_UPDATE

        # if app.ENABLE_ULTIMATE_REGEN:
        if hasattr(player, "LoadBossNPC"): player.LoadBossNPC()

        self.__SetQuickSlotMode()
        self.__SelectQuickPage(self.quickSlotPageIndex)

        self.SetFocus()
        self.Show()
        app.ShowCursor()

        snd.SetMusicVolume(systemSetting.GetMusicVolume())
        snd.SetSoundVolume(systemSetting.GetSoundVolume())
        snd.FadeInMusic("BGM/enter_the_east.mp3")

        net.SendEnterGamePacket()

        self.autoChangeTime = 0
        if os.path.exists("autochange.cfg"):
            os.remove("autochange.cfg")
            self.autoChangeTime = app.GetTime() + 8

        # START_GAME_ERROR_EXIT
        try:
            self.StartGame()
        except:
            import exception
            exception.Abort("GameWindow.Open")
        # END_OF_START_GAME_ERROR_EXIT

        if app.ENABLE_AUTO_SHOUT:
            self.lastShoutTime = app.GetTime() + constInfo.SHOUT_PER_SECOND

        if app.ENABLE_MOVIEMODE_CAMERA:
            self.isFreeCamera = False
            self.ResetFreeCam()

    def Close(self):
        snd.FadeOutMusic("BGM/enter_the_east.mp3")
        snd.StopAllSound()
        constInfo.CloseWindows()
        self.Hide()

        global cameraDistance, cameraPitch, cameraRotation, cameraHeight
        (cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

        self.onPressKeyDict = None
        self.onClickKeyDict = None

        chat.Close()
        grp.InitScreenEffect()
        chr.Destroy()
        textTail.Clear()
        quest.Clear()
        background.Destroy()
        guild.Destroy()
        messenger.Destroy()
        skill.ClearSkillData()
        wndMgr.Unlock()
        mouseModule.mouseController.DeattachObject()

        if self.guildWarQuestionDialog:
            self.guildWarQuestionDialog.Close()

        self.guildNameBoard = None
        self.partyRequestQuestionDialog = None
        self.partyInviteQuestionDialog = None
        self.guildInviteQuestionDialog = None
        self.guildWarQuestionDialog = None
        self.messengerAddFriendQuestion = None

        if app.ENABLE_IN_GAME_LOG_SYSTEM:
            if self.wndInGameLog:
                self.wndInGameLog.Destroy()
                self.wndInGameLog = None

        if app.ENABLE_BOT_CONTROL:
            if self.botControlWnd:
                self.botControlWnd.Constructor()
                self.botControlWnd = None

        # UNKNOWN_UPDATE
        self.itemDropQuestionDialog = None
        # END_OF_UNKNOWN_UPDATE

        # QUEST_CONFIRM
        self.confirmDialog = None
        # END_OF_QUEST_CONFIRM

        self.PrintCoord = None
        self.FrameRate = None
        self.Pitch = None
        self.Splat = None
        self.TextureNum = None
        self.ObjectNum = None
        self.ViewDistance = None
        self.PrintMousePos = None

        self.ClearDictionary()

        self.playerGauge = None
        self.mapNameShower = None
        self.affectShower = None

        if self.targetBoard:
            self.targetBoard.Destroy()
            del self.targetBoard

        if self.interface:
            self.interface.HideAllWindows()
            self.interface.Close()
            self.interface = None

        if app.ENABLE_GLOBAL_RANKING:
            if self.rankingWindow:
                self.rankingWindow.Hide()
                del self.rankingWindow

        if app.ENABLE_PM_ALL_SEND_SYSTEM:
            if self.whisperAdmin:
                self.whisperAdmin.Close()
                self.whisperAdmin.Destroy()
                del self.whisperAdmin

        if app.ENABLE_DUNGEON_INFO:
            if self.wndBossTimer:
                self.wndBossTimer.Hide()
                self.wndBossTimer.Destroy()
                del self.wndBossTimer

        if app.ENABLE_MOVIEMODE_CAMERA:
            if self.isFreeCamera:
                app.SetDefaultCamera()
                self.isFreeCamera = False
                self.freeCam = list()

        if self.wndDropInfoTracker:
            self.wndDropInfoTracker.Hide()
            self.wndDropInfoTracker = None

        if self.wndBuyBack:
            self.wndBuyBack.Hide()
            self.wndBuyBack = None

        if self.wndGmItemRestore:
            self.wndGmItemRestore.Hide()
            self.wndGmItemRestore = None

        try:
                if self.wndMiningGame:
                    self.wndMiningGame.Close(True)
                    self.wndMiningGame.Hide()
        except:
                    pass
    
        player.ClearSkillDict()
        player.ResetCameraRotation()

        self.KillFocus()
        app.HideCursor()
        constInfo.SetGameInstance(None)

    def __BuildKeyDict(self):
        onPressKeyDict = {}

        onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
        onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
        onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
        onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
        onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
        onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
        onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
        onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
        onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
        onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
        onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
        onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
        onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)

        onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
        onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
        onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
        onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

        onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
        onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
        onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
        onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
        onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
        onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
        onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
        onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

        onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
        onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
        onPressKeyDict[app.DIK_G]			= self.__PressGKey
        onPressKeyDict[app.DIK_Q]			= self.__PressQKey

        onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
        onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
        onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
        onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
        onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
        onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
        onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
        onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
        onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
        onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
        onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
        onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
        onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
        onPressKeyDict[app.DIK_O]			= self.__PressOKey
        onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
        onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
        onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
        onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
        onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

        onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
        onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
        onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
        onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()

        if app.ENABLE_NEW_PET_SYSTEM:
            onPressKeyDict[app.DIK_P] = lambda: self.OpenPetInterface()

        onPressKeyDict[app.DIK_E] = lambda: self.__PressEKey()

        if app.ENABLE_SPECIAL_STORAGE:
            onPressKeyDict[app.DIK_U]	= lambda: self.interface.ToggleSpecialStorageWindow()
        if app.ENABLE_OFFLINE_SHOP:
            onPressKeyDict[app.DIK_J]		= lambda : self.OpenShopSearch()
            onPressKeyDict[app.DIK_K]		= lambda : self.OpenPrivateShopBuilder()

        # onPressKeyDict[app.DIK_X]	= lambda : self.interface.dlgSystem.ClickMoveChannelButton()

        if app.ENABLE_EVENT_MANAGER:
            onPressKeyDict[app.DIK_F8]	= lambda : self.interface.OpenEventCalendar()

        if app.ENABLE_DUNGEON_INFO:
            onPressKeyDict[app.DIK_TAB]	= lambda : self.ToggleBossTimerWindow()

        if app.ENABLE_IN_GAME_LOG_SYSTEM:
            onPressKeyDict[app.DIK_F6]		= lambda : self.OpenInGameLog()

        if app.ENABLE_SWITCHBOT:
            onPressKeyDict[app.DIK_F5]	= lambda : self.interface.ToggleSwitchbotWindow()

        if app.ENABLE_GLOBAL_RANKING:
            onPressKeyDict[app.DIK_F7]		= lambda : self.SendOpenRanking()

        if app.ENABLE_MOVIEMODE_CAMERA:
            onPressKeyDict[app.DIK_F11]	= lambda : self.__ToggleFreeCamera()

        self.onPressKeyDict = onPressKeyDict

        onClickKeyDict = {}
        onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
        onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
        onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
        onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
        onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

        onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
        onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
        onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
        onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
        onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
        onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
        onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
        onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
        onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

        self.onClickKeyDict=onClickKeyDict

    def __PressNumKey(self,num):
        if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
            if num >= 1 and num <= 9:
                if(chrmgr.IsPossibleEmoticon(-1)):
                    chrmgr.SetEmoticon(-1,int(num)-1)
                    net.SendEmoticon(int(num)-1)
        else:
            if num >= 1 and num <= 4:
                self.pressNumber(num-1)

    if app.ENABLE_OFFLINE_SHOP:
        def OpenPrivateShopBuilder(self):
            if self.interface.wndShopOffline:
                if self.interface.wndShopOffline.IsShow() == False or self.interface.wndShopOffline.wBoard[3].IsShow():
                    self.interface.wndShopOffline.Open()
                else:
                    self.interface.wndShopOffline.Close()

        def OpenShopSearch(self):
            if self.interface.wndShopSearch:
                if not self.interface.wndShopSearch.IsShow():
                    self.interface.wndShopSearch.Show()
                else:
                    self.interface.wndShopSearch.Close()

    def	__PressJKey(self):
        if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
            if player.IsMountingHorse():
                net.SendChatPacket("/unmount")
            else:
                #net.SendChatPacket("/user_horse_ride")
                if not uiPrivateShopBuilder.IsBuildingPrivateShop():
                    for i in xrange(player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT):
                        if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
                            net.SendItemUsePacket(i)
                            break

    def	__PressHKey(self):
        if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
            net.SendChatPacket("/user_horse_ride")
        else:
            if app.ENABLE_WIKI:
                self.interface.OpenWikiWindow()

    def	__PressBKey(self):
        if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
            net.SendChatPacket("/user_horse_back")
        else:
            state = "EMOTICON"
            self.interface.ToggleCharacterWindow(state)

    def	__PressFKey(self):
        if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
            net.SendChatPacket("/user_horse_feed")
        else:
            app.ZoomCamera(app.CAMERA_TO_POSITIVE)

    def __PressGKey(self):
        if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
            net.SendChatPacket("/ride")
        else:
            if self.ShowNameFlag:
                self.interface.ToggleGuildWindow()
            else:
                app.PitchCamera(app.CAMERA_TO_POSITIVE)

    def __PressOKey(self):
        if app.IsPressed(app.DIK_LCONTROL):
            self.interface.wndDragonSoul.ActivateSelectedDeck(0)
            return
        self.interface.ToggleDragonSoulWindowWithNoInfo()

    def __PressPKey(self):
        if app.IsPressed(app.DIK_LCONTROL):
            self.interface.wndDragonSoul.ActivateSelectedDeck(1)
            return True
        return False

    def __PressEKey(self):
        if app.IsPressed(app.DIK_LCONTROL):
            self.interface.wndInventory.ActivateAllAffectItems()
            return

        app.RotateCamera(app.CAMERA_TO_POSITIVE)

    def	__ReleaseGKey(self):
        app.PitchCamera(app.CAMERA_STOP)

    def __PressQKey(self):
        if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
            if 0==interfaceModule.IsQBHide:
                interfaceModule.IsQBHide = 1
                self.interface.HideAllQuestButton()
            else:
                interfaceModule.IsQBHide = 0
                self.interface.ShowAllQuestButton()
        else:
            app.RotateCamera(app.CAMERA_TO_NEGATIVE)

    def __SetQuickSlotMode(self):
        self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

    def __SetQuickPageMode(self):
        self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

    def __PressQuickSlot(self, localSlotIndex):
        player.RequestUseLocalQuickSlot(localSlotIndex)

    def __SelectQuickPage(self, pageIndex):
        self.quickSlotPageIndex = pageIndex
        player.SetQuickPage(pageIndex)

    def __NotifyError(self, msg):
        chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

    def ChangePKMode(self):

        if not app.IsPressed(app.DIK_LCONTROL):
            return

        if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
            self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
            return

        curTime = app.GetTime()
        if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
            return

        self.lastPKModeSendedTime = curTime

        curPKMode = player.GetPKMode()
        nextPKMode = curPKMode + 1
        if nextPKMode == player.PK_MODE_PROTECT:
            if 0 == player.GetGuildID():
                chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
                nextPKMode = 0
            else:
                nextPKMode = player.PK_MODE_GUILD

        elif nextPKMode == player.PK_MODE_MAX_NUM:
            nextPKMode = 0

        net.SendChatPacket("/PKMode " + str(nextPKMode))

    def OnChangePKMode(self):

        self.interface.OnChangePKMode()

        try:
            self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
        except KeyError:
            pass

    ###############################################################################################
    ###############################################################################################
    ## Game Callback Functions

    # Start
    def StartGame(self):
        self.RefreshInventory()
        self.RefreshEquipment()
        self.RefreshCharacter()
        self.RefreshSkill()

        if app.ENABLE_LOADING_WINDOW_RENEWAL and systemSetting.IsLoadingAnimated():
            if constInfo.CURTAIN_ACTIVE == 1:
                constInfo.CURTAIN_ACTIVE = 0

    # Refresh
    def CheckGameButton(self):
        if self.interface:
            self.interface.CheckGameButton()

    def RefreshAlignment(self):
        self.interface.RefreshAlignment()

    def RefreshStatus(self):
        self.CheckGameButton()

        if self.interface:
            self.interface.RefreshStatus()

        if self.playerGauge:
            self.playerGauge.RefreshGauge()

    def RefreshStamina(self):
        self.interface.RefreshStamina()

    def RefreshSkill(self):
        self.CheckGameButton()
        if self.interface:
            self.interface.RefreshSkill()

    def RefreshQuest(self):
        self.interface.RefreshQuest()

    def RefreshMessenger(self):
        self.interface.RefreshMessenger()

    def RefreshGuildInfoPage(self):
        self.interface.RefreshGuildInfoPage()

    def RefreshGuildBoardPage(self):
        self.interface.RefreshGuildBoardPage()

    def RefreshGuildMemberPage(self):
        self.interface.RefreshGuildMemberPage()

    def RefreshGuildMemberPageGradeComboBox(self):
        self.interface.RefreshGuildMemberPageGradeComboBox()

    def RefreshGuildSkillPage(self):
        self.interface.RefreshGuildSkillPage()

    def RefreshGuildGradePage(self):
        self.interface.RefreshGuildGradePage()

    def OnBlockMode(self, mode):
        self.interface.OnBlockMode(mode)

    def OpenQuestWindow(self, skin, idx):
        self.interface.OpenQuestWindow(skin, idx)

    def AskGuildName(self):

        guildNameBoard = uiCommon.InputDialog()
        guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
        guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
        guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
        guildNameBoard.Open()

        self.guildNameBoard = guildNameBoard

    def ConfirmGuildName(self):
        guildName = self.guildNameBoard.GetText()
        if not guildName:
            return

        if net.IsInsultIn(guildName):
            self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
            return

        net.SendAnswerMakeGuildPacket(guildName)
        self.guildNameBoard.Close()
        self.guildNameBoard = None
        return True

    def CancelGuildName(self):
        self.guildNameBoard.Close()
        self.guildNameBoard = None
        return True

    ## Refine
    def PopupMessage(self, msg):
        if self.stream:
            self.stream.popupWindow.Close()
            self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

    def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
        self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)

    def AppendMaterialToRefineDialog(self, vnum, count):
        self.interface.AppendMaterialToRefineDialog(vnum, count)

    def RunUseSkillEvent(self, slotIndex, coolTime):
        self.interface.OnUseSkill(slotIndex, coolTime)

    def ClearAffects(self):
        self.affectShower.ClearAffects()

    def SetAffect(self, affect):
        self.affectShower.SetAffect(affect)

    def ResetAffect(self, affect):
        self.affectShower.ResetAffect(affect)

    # UNKNOWN_UPDATE
    def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
        self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
        if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
            self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
        elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
            self.BINARY_DragonSoulGiveQuilification()
        elif app.ENABLE_DS_SET_BONUS and chr.NEW_AFFECT_DS_SET == type:
            self.interface.DragonSoulSetGrade(value)

    def BINARY_NEW_RemoveAffect(self, type, pointIdx):
        self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
        if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
            self.interface.DragonSoulDeactivate()
        elif app.ENABLE_DS_SET_BONUS and chr.NEW_AFFECT_DS_SET == type:
            self.interface.DragonSoulSetGrade(0)

    if app.WJ_ENABLE_TRADABLE_ICON:
        def BINARY_AddItemToExchange(self, inven_type, inven_pos, display_pos):
            if inven_type == player.INVENTORY:
                self.interface.CantTradableItemExchangeFromInventory(display_pos, inven_pos)
            
            if inven_type == player.DRAGON_SOUL_INVENTORY:
                self.interface.CantTradableItemExchangeFromDragonSoul(display_pos, inven_pos)
            
            if app.ENABLE_SPECIAL_STORAGE:
                if inven_type in (player.UPGRADE_INVENTORY, player.BOOK_INVENTORY, player.STONE_INVENTORY, player.CHEST_INVENTORY):
                    self.interface.CantTradableItemExchangeFromStorage(display_pos, inven_pos, inven_type)

    # END_OF_UNKNOWN_UPDATE

    def ActivateSkillSlot(self, slotIndex):
        if self.interface:
            self.interface.OnActivateSkill(slotIndex)

    def DeactivateSkillSlot(self, slotIndex):
        if self.interface:
            self.interface.OnDeactivateSkill(slotIndex)

    def RefreshEquipment(self):
        if self.interface:
            self.interface.RefreshInventory()

    def RefreshInventory(self):
        if self.interface:
            self.interface.RefreshInventory()

    def RefreshCharacter(self):
        if self.interface:
            self.interface.RefreshCharacter()

    def OnGameOver(self):
        self.CloseTargetBoard()
        self.OpenRestartDialog()

    def OpenRestartDialog(self):
        self.interface.OpenRestartDialog()

    def ChangeCurrentSkill(self, skillSlotNumber):
        self.interface.OnChangeCurrentSkill(skillSlotNumber)

    ## TargetBoard
    def SetPCTargetBoard(self, vid, name):
        self.targetBoard.Open(vid, name)

        if app.IsPressed(app.DIK_LCONTROL):

            if not player.IsSameEmpire(vid):
                return

            if player.IsMainCharacterIndex(vid):
                return
            elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
                return

            self.interface.OpenWhisperDialog(name)


    def RefreshTargetBoardByVID(self, vid):
        self.targetBoard.RefreshByVID(vid)

    def RefreshTargetBoardByName(self, name):
        self.targetBoard.RefreshByName(name)

    def __RefreshTargetBoard(self):
        self.targetBoard.Refresh()

    if app.ENABLE_SHOW_TARGET_HP:
        def SetHPTargetBoard(self, vid, hpPercentage, hpTarget, bElement):
            if vid != self.targetBoard.GetTargetVID():
                self.targetBoard.ResetTargetBoard()
                self.targetBoard.SetEnemyVID(vid)
            
            self.targetBoard.SetHP(hpPercentage, hpTarget)

            self.targetBoard.SetElementImage(bElement, self, *self.targetBoard.GetGlobalPosition())
            self.targetBoard.Show()
    else:
        def SetHPTargetBoard(self, vid, hpPercentage):
            if vid != self.targetBoard.GetTargetVID():
                self.targetBoard.ResetTargetBoard()
                self.targetBoard.SetEnemyVID(vid)

            self.targetBoard.SetHP(hpPercentage)
            self.targetBoard.Show()

    def CloseTargetBoardIfDifferent(self, vid):
        if vid != self.targetBoard.GetTargetVID():
            self.targetBoard.Close()

    def CloseTargetBoard(self):
        self.targetBoard.Close()

    ## View Equipment
    def OpenEquipmentDialog(self, vid):
        self.interface.OpenEquipmentDialog(vid)

    def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
        self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

    def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
        self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

    def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
        self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

    # SHOW_LOCAL_MAP_NAME
    def ShowMapName(self, mapName, x, y):
        try:
            if self.mapNameShower:
                self.mapNameShower.ShowMapName(mapName, x, y)
            
            if self.interface:
                self.interface.SetMapName(mapName)
        except Exception:
            pass

    def BINARY_OpenAtlasWindow(self):
        self.interface.BINARY_OpenAtlasWindow()

    ## Chat
    def OnRecvWhisper(self, mode, name, line):
        if mode == chat.WHISPER_TYPE_GM:
            self.interface.RegisterGameMasterName(name)
        chat.AppendWhisper(mode, name, line)
        self.interface.RecvWhisper(name)

    def OnRecvWhisperSystemMessage(self, mode, name, line):
        chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
        self.interface.RecvWhisper(name)

    def OnRecvWhisperError(self, mode, name, line):
        if localeInfo.WHISPER_ERROR.has_key(mode):
            chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
        else:
            chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
        self.interface.RecvWhisper(name)

    def RecvWhisper(self, name):
        self.interface.RecvWhisper(name)

    def OnPickMoney(self, money):
        moneyVal = int(money)
        if getattr(app, "ENABLE_DROP_INFO_WINDOW", 0) and hasattr(chat, "CHAT_TYPE_MONEY_INFO"):
            chat.AppendChat(chat.CHAT_TYPE_MONEY_INFO, localeInfo.GAME_PICK_MONEY % (moneyVal))
            if self.wndDropInfoTracker and constInfo.GET_DROP_INFO_TRACKER_MODE() != 0:
                self.wndDropInfoTracker.AddMoneyPickup(moneyVal)
        else:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (moneyVal))

    def BINARY_OnPickItem(self, vnum, count):
        if getattr(app, "ENABLE_DROP_INFO_WINDOW", 0) and self.wndDropInfoTracker:
            if constInfo.GET_DROP_INFO_TRACKER_MODE() != 0:
                self.wndDropInfoTracker.AddItemPickup(int(vnum), int(count))

    def RefreshDropInfoTrackerOption(self):
        if self.wndDropInfoTracker:
            self.wndDropInfoTracker.RefreshModeAndPosition()
        if self.interface and self.interface.wndChat and hasattr(chat, "CHAT_TYPE_ITEM_INFO"):
            chatID = self.interface.wndChat.chatID
            if constInfo.GET_DROP_INFO_TRACKER_MODE() != 0:
                chat.DisableChatMode(chatID, chat.CHAT_TYPE_ITEM_INFO)
                chat.DisableChatMode(chatID, chat.CHAT_TYPE_MONEY_INFO)
            else:
                chat.EnableChatMode(chatID, chat.CHAT_TYPE_ITEM_INFO)
                chat.EnableChatMode(chatID, chat.CHAT_TYPE_MONEY_INFO)

    def OnShopError(self, type):
        try:
            self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
        except KeyError:
            self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

    def OnSafeBoxError(self):
        self.PopupMessage(localeInfo.SAFEBOX_ERROR)

    def OnFishingSuccess(self, isFish, fishName):
        chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

    # ADD_FISHING_MESSAGE
    def OnFishingNotifyUnknown(self):
        chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

    def OnFishingWrongPlace(self):
        chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
    # END_OF_ADD_FISHING_MESSAGE

    def OnFishingNotify(self, isFish, fishName):
        chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

    def OnFishingFailure(self):
        chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

    def OnCannotPickItem(self):
        chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

    # MINING
    def OnCannotMining(self):
        chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
    # END_OF_MINING

    def OnCannotUseSkill(self, vid, type):
        if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
            textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

        if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

    def	OnCannotShotError(self, vid, type):
        textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

    ## PointReset
    def StartPointReset(self):
        self.interface.OpenPointResetDialog()

    ## Shop
    def StartShop(self, vid):
        self.interface.OpenShopDialog(vid)

    def EndShop(self):
        self.interface.CloseShopDialog()

    def RefreshShop(self):
        self.interface.RefreshShopDialog()

    ## Exchange
    def StartExchange(self):
        self.interface.StartExchange()

    def EndExchange(self):
        self.interface.EndExchange()

    def RefreshExchange(self):
        self.interface.RefreshExchange()

    ## Party
    def RecvPartyInviteQuestion(self, leaderVID, leaderName):
        partyInviteQuestionDialog = uiCommon.QuestionDialog()
        partyInviteQuestionDialog.SetText(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
        partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
        partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
        partyInviteQuestionDialog.Open()
        partyInviteQuestionDialog.partyLeaderVID = leaderVID
        self.partyInviteQuestionDialog = partyInviteQuestionDialog

    def AnswerPartyInvite(self, answer):

        if not self.partyInviteQuestionDialog:
            return

        partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

        distance = player.GetCharacterDistance(partyLeaderVID)
        if distance < 0.0 or distance > 5000:
            answer = False

        net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

        self.partyInviteQuestionDialog.Close()
        self.partyInviteQuestionDialog = None

    def AddPartyMember(self, pid, name):
        self.interface.AddPartyMember(pid, name)

    def UpdatePartyMemberInfo(self, pid):
        self.interface.UpdatePartyMemberInfo(pid)

    def RemovePartyMember(self, pid):
        self.interface.RemovePartyMember(pid)
        self.__RefreshTargetBoard()

    def LinkPartyMember(self, pid, vid):
        self.interface.LinkPartyMember(pid, vid)

    def UnlinkPartyMember(self, pid):
        self.interface.UnlinkPartyMember(pid)

    def UnlinkAllPartyMember(self):
        self.interface.UnlinkAllPartyMember()

    def ExitParty(self):
        self.interface.ExitParty()
        self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

    def ChangePartyParameter(self, distributionMode):
        self.interface.ChangePartyParameter(distributionMode)

    ## Messenger
    def OnMessengerAddFriendQuestion(self, name):
        messengerAddFriendQuestion = uiCommon.QuestionDialog2()
        messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
        messengerAddFriendQuestion.SetText2(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2)
        messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
        messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
        messengerAddFriendQuestion.Open()
        messengerAddFriendQuestion.name = name
        self.messengerAddFriendQuestion = messengerAddFriendQuestion

    def OnAcceptAddFriend(self):
        name = self.messengerAddFriendQuestion.name
        net.SendChatPacket("/messenger_auth y " + name)
        self.OnCloseAddFriendQuestionDialog()
        return True

    def OnDenyAddFriend(self):
        name = self.messengerAddFriendQuestion.name
        net.SendChatPacket("/messenger_auth n " + name)
        self.OnCloseAddFriendQuestionDialog()
        return True

    def OnCloseAddFriendQuestionDialog(self):
        self.messengerAddFriendQuestion.Close()
        self.messengerAddFriendQuestion = None
        return True

    ## SafeBox
    def OpenSafeboxWindow(self, size):
        self.interface.OpenSafeboxWindow(size)

    def RefreshSafebox(self):
        self.interface.RefreshSafebox()

    def RefreshSafeboxMoney(self):
        self.interface.RefreshSafeboxMoney()

    # ITEM_MALL
    def OpenMallWindow(self, size):
        self.interface.OpenMallWindow(size)

    def RefreshMall(self):
        self.interface.RefreshMall()
    # END_OF_ITEM_MALL

    ## Guild
    def RecvGuildInviteQuestion(self, guildID, guildName):
        guildInviteQuestionDialog = uiCommon.QuestionDialog()
        guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
        guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
        guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
        guildInviteQuestionDialog.Open()
        guildInviteQuestionDialog.guildID = guildID
        self.guildInviteQuestionDialog = guildInviteQuestionDialog

    def AnswerGuildInvite(self, answer):

        if not self.guildInviteQuestionDialog:
            return

        guildLeaderVID = self.guildInviteQuestionDialog.guildID
        net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

        self.guildInviteQuestionDialog.Close()
        self.guildInviteQuestionDialog = None

    def DeleteGuild(self):
        self.interface.DeleteGuild()

    ## Clock
    def ShowClock(self, second):
        self.interface.ShowClock(second)

    def HideClock(self):
        self.interface.HideClock()

    ## Emotion
    def BINARY_ActEmotion(self, emotionIndex):
        if self.interface.wndCharacter:
            self.interface.wndCharacter.ActEmotion(emotionIndex)

    ###############################################################################################
    ###############################################################################################
    ## Keyboard Functions

    def CheckFocus(self):
        if False == self.IsFocus():
            if True == self.interface.IsOpenChat():
                self.interface.ToggleChat()

            self.SetFocus()

    def SaveScreen(self):

        # SCREENSHOT_CWDSAVE
        if SCREENSHOT_CWDSAVE:
            if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
                os.mkdir(os.getcwd()+os.sep+"screenshot")

            (succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
        elif SCREENSHOT_DIR:
            (succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
        else:
            (succeeded, name) = grp.SaveScreenShot()
        # END_OF_SCREENSHOT_CWDSAVE

        if succeeded:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "%s %s %s" % (name, localeInfo.SCREENSHOT_SAVE1, localeInfo.SCREENSHOT_SAVE2))
        else:
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

    def ShowName(self):
        if app.ENABLE_OFFLINE_SHOP:
            offlineshop.ShowShopNames()
        self.ShowNameFlag = True
        self.playerGauge.EnableShowAlways()
        player.SetQuickPage(self.quickSlotPageIndex+1)

    # ADD_ALWAYS_SHOW_NAME
    def __IsShowName(self):

        if systemSetting.IsAlwaysShowName():
            return True

        if self.ShowNameFlag:
            return True

        return False
    # END_OF_ADD_ALWAYS_SHOW_NAME

    def HideName(self):
        if app.ENABLE_OFFLINE_SHOP:
            offlineshop.HideShopNames()
        self.ShowNameFlag = False
        self.playerGauge.DisableShowAlways()
        player.SetQuickPage(self.quickSlotPageIndex)

    def ShowMouseImage(self):
        self.interface.ShowMouseImage()

    def HideMouseImage(self):
        self.interface.HideMouseImage()

    def StartAttack(self):
        player.SetAttackKeyState(True)

    def EndAttack(self):
        player.SetAttackKeyState(False)

    def MoveUp(self):
        player.SetSingleDIKKeyState(app.DIK_UP, True)

    def MoveDown(self):
        player.SetSingleDIKKeyState(app.DIK_DOWN, True)

    def MoveLeft(self):
        player.SetSingleDIKKeyState(app.DIK_LEFT, True)

    def MoveRight(self):
        player.SetSingleDIKKeyState(app.DIK_RIGHT, True)

    def StopUp(self):
        player.SetSingleDIKKeyState(app.DIK_UP, False)

    def StopDown(self):
        player.SetSingleDIKKeyState(app.DIK_DOWN, False)

    def StopLeft(self):
        player.SetSingleDIKKeyState(app.DIK_LEFT, False)

    def StopRight(self):
        player.SetSingleDIKKeyState(app.DIK_RIGHT, False)

    def PickUpItem(self):
        if app.ENABLE_QUICK_PICKUP:
            player.PickAllItems()
        else:
            player.PickCloseItem()

    ###############################################################################################
    ###############################################################################################
    ## Event Handler

    def OnKeyDown(self, key):
        if self.interface.wndWeb and self.interface.wndWeb.IsShow():
            return

        if app.ENABLE_BOT_CONTROL:
            if self.isBotControlActive():
                return

        if self.ShortcutHotkeys(key):
            return

        if key == app.DIK_ESC:
            self.RequestDropItem(False)
            constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

        if app.ENABLE_MOVIEMODE_CAMERA:
            if self.isFreeCamera:
                if key == app.DIK_LSHIFT:
                    self.__PressShiftKey()
                elif key == app.DIK_LCONTROL:
                    self.__PressCtrlKey()

        try:
            self.onPressKeyDict[key]()
        except KeyError:
            pass
        except:
            raise

        return True

    def OnKeyUp(self, key):
        try:
            if self.onClickKeyDict:
                if self.onClickKeyDict.items():
                    self.onClickKeyDict[key]()

                if app.ENABLE_MOVIEMODE_CAMERA:
                    if self.isFreeCamera:
                        if key == app.DIK_LSHIFT:
                            self.__ReleaseShiftKey()
                        elif key == app.DIK_LCONTROL:
                            self.__ReleaseCtrlKey()


        except KeyError:
            pass
        except:
            raise

        return True

    def ShortcutHotkeys(self, key):
        itemVnum, inventoryType, slotIndex, showTooltip = constInfo.SELECTED_ITEM_VNUM

        if showTooltip:

            if app.IsPressed(app.DIK_LSHIFT) and key == app.DIK_H:
                if self.interface.wndWiki:
                    self.interface.wndWiki.searchItemWithName(itemVnum)
                    return True

            elif app.IsPressed(app.DIK_LSHIFT) and key == app.DIK_J:
                if not self.interface.wndShopSearch.IsShow():
                    self.interface.wndShopSearch.Show(True)
                item.SelectItem(itemVnum)
                self.interface.wndShopSearch.sItemName.SetText(item.GetItemName())
                self.interface.wndShopSearch.OnSearch()
                return True

            elif app.ENABLE_RENDER_TARGET and app.IsPressed(app.DIK_LSHIFT) and key == app.DIK_P:
                uiToolTip.ItemToolTip().ModelPreviewFull(itemVnum)
                return True

        return False

    def OnMouseLeftButtonDown(self):
        if self.interface.BUILD_OnMouseLeftButtonDown():
            return

        if mouseModule.mouseController.isAttached():
            self.CheckFocus()
        else:
            hyperlink = ui.GetHyperlink()
            if hyperlink:
                return
            else:
                self.CheckFocus()
                player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS)

        return True

    def OnMouseLeftButtonUp(self):

        if self.interface.BUILD_OnMouseLeftButtonUp():
            return

        if mouseModule.mouseController.isAttached():
            attachedType = mouseModule.mouseController.GetAttachedType()
            attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
            attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
            attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
            if app.ENABLE_OFFLINE_SHOP:
                if uiOfflineShop.IsBuildingShop() and uiOfflineShop.IsSaleSlot(player.SlotTypeToInvenType(attachedType), attachedItemSlotPos):
                    chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
                    return
            ## QuickSlot
            if player.SLOT_TYPE_QUICK_SLOT == attachedType:
                player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

            ## Inventory
            elif player.SLOT_TYPE_INVENTORY == attachedType:

                if player.ITEM_MONEY == attachedItemIndex:
                    self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
                else:
                    self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

            ## DragonSoul
            elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
                self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

            if app.ENABLE_SPECIAL_STORAGE:
                if player.SLOT_TYPE_UPGRADE_INVENTORY == attachedType or\
                    player.SLOT_TYPE_BOOK_INVENTORY == attachedType or\
                    player.SLOT_TYPE_STONE_INVENTORY == attachedType or\
                    player.SLOT_TYPE_CHEST_INVENTORY == attachedType:
                    self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

            mouseModule.mouseController.DeattachObject()

        else:
            hyperlink = ui.GetHyperlink()
            if hyperlink:
                if app.IsPressed(app.DIK_LALT):
                    link = chat.GetLinkFromHyperlink(hyperlink)
                    ime.PasteString(link)
                else:
                    self.interface.MakeHyperlinkTooltip(hyperlink)
                return
            else:
                player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)

        return True

    def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
        if app.ENABLE_SPECIAL_STORAGE:
            if player.SLOT_TYPE_INVENTORY == attachedType or\
                player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType or\
                player.SLOT_TYPE_UPGRADE_INVENTORY == attachedType or\
                player.SLOT_TYPE_BOOK_INVENTORY == attachedType or\
                player.SLOT_TYPE_STONE_INVENTORY == attachedType or\
                player.SLOT_TYPE_CHEST_INVENTORY == attachedType:
                attachedInvenType = player.SlotTypeToInvenType(attachedType)
                if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
                    if player.IsEquipmentSlot(attachedItemSlotPos) and\
                        player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType and\
                        player.SLOT_TYPE_UPGRADE_INVENTORY != attachedType and\
                        player.SLOT_TYPE_BOOK_INVENTORY != attachedType and\
                        player.SLOT_TYPE_STONE_INVENTORY != attachedType and \
                        player.SLOT_TYPE_CHEST_INVENTORY != attachedType:
                        self.stream.popupWindow.Close()
                        self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
                    else:
                        if chr.IsNPC(dstChrID):
                            if app.ENABLE_REFINE_RENEWAL:
                                constInfo.AUTO_REFINE_TYPE = 2
                                constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
                                constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
                                constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
                                constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount

                            net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
                        else:
                            net.SendExchangeStartPacket(dstChrID)
                            net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
                else:
                    if app.ENABLE_DROP_DIALOG_EXTENDED_SYSTEM:
                        self.interface.DeleteItem(attachedItemSlotPos, attachedInvenType)
                    else:
                        self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)
                    # self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)
        else:
            if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
                attachedInvenType = player.SlotTypeToInvenType(attachedType)
                if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
                    if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
                        self.stream.popupWindow.Close()
                        self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
                    else:
                        if chr.IsNPC(dstChrID):
                            if app.ENABLE_REFINE_RENEWAL:
                                constInfo.AUTO_REFINE_TYPE = 2
                                constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
                                constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
                                constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
                                constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount

                            net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
                        else:
                            net.SendExchangeStartPacket(dstChrID)
                            net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
                else:
                    if app.ENABLE_DROP_DIALOG_EXTENDED_SYSTEM:
                        self.interface.DeleteItem(attachedItemSlotPos, attachedInvenType)
                    else:
                        self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

    def __PutMoney(self, attachedType, attachedMoney, dstChrID):
        if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
            net.SendExchangeStartPacket(dstChrID)
            net.SendExchangeElkAddPacket(attachedMoney)
        else:
            if not app.ENABLE_DROP_DIALOG_EXTENDED_SYSTEM:
                self.__DropMoney(attachedType, attachedMoney)

    def __DropMoney(self, attachedType, attachedMoney):
        if uiPrivateShopBuilder.IsBuildingPrivateShop():
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
            return
        # END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

        if attachedMoney>=1000:
            self.stream.popupWindow.Close()
            self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
            return

        itemDropQuestionDialog = uiCommon.QuestionDialog()
        itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
        itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
        itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
        itemDropQuestionDialog.Open()
        itemDropQuestionDialog.dropType = attachedType
        itemDropQuestionDialog.dropCount = attachedMoney
        itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
        self.itemDropQuestionDialog = itemDropQuestionDialog

    def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
        if uiPrivateShopBuilder.IsBuildingPrivateShop():
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
            return
        # END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

        if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
            self.stream.popupWindow.Close()
            self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

        else:
            if player.SLOT_TYPE_INVENTORY == attachedType:
                dropItemIndex = player.GetItemIndex(attachedItemSlotPos)

                item.SelectItem(dropItemIndex)
                dropItemName = item.GetItemName()

                ## Question Text
                questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

                ## Dialog
                itemDropQuestionDialog = uiCommon.QuestionDialog()
                itemDropQuestionDialog.SetText(questionText)
                itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
                itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
                itemDropQuestionDialog.Open()
                itemDropQuestionDialog.dropType = attachedType
                itemDropQuestionDialog.dropNumber = attachedItemSlotPos
                itemDropQuestionDialog.dropCount = attachedItemCount
                self.itemDropQuestionDialog = itemDropQuestionDialog

                constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

            elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
                dropItemIndex = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

                item.SelectItem(dropItemIndex)
                dropItemName = item.GetItemName()

                ## Question Text
                questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

                ## Dialog
                itemDropQuestionDialog = uiCommon.QuestionDialog()
                itemDropQuestionDialog.SetText(questionText)
                itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
                itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
                itemDropQuestionDialog.Open()
                itemDropQuestionDialog.dropType = attachedType
                itemDropQuestionDialog.dropNumber = attachedItemSlotPos
                itemDropQuestionDialog.dropCount = attachedItemCount
                self.itemDropQuestionDialog = itemDropQuestionDialog

                constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

            elif app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_UPGRADE_INVENTORY == attachedType or player.SLOT_TYPE_BOOK_INVENTORY == attachedType or player.SLOT_TYPE_STONE_INVENTORY == attachedType or player.SLOT_TYPE_STONE_INVENTORY == attachedType or player.SLOT_TYPE_CHEST_INVENTORY == attachedType:
                dropItemIndex = player.GetItemIndex(player.SlotTypeToInvenType(attachedType), attachedItemSlotPos)
                item.SelectItem(dropItemIndex)
                dropItemName = item.GetItemName()
                questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)
                itemQuestionDialog = uiCommon.QuestionDialog()
                itemQuestionDialog.SetText(questionText)
                itemQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
                itemQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
                itemQuestionDialog.Open()
                itemQuestionDialog.dropType = attachedType
                itemQuestionDialog.dropNumber = attachedItemSlotPos
                itemQuestionDialog.dropCount = attachedItemCount
                self.itemQuestionDialog = itemQuestionDialog
                constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

    def RequestDropItem(self, answer):
        if not self.itemDropQuestionDialog:
            return

        if answer:
            dropType = self.itemDropQuestionDialog.dropType
            dropCount = self.itemDropQuestionDialog.dropCount
            dropNumber = self.itemDropQuestionDialog.dropNumber

            if player.SLOT_TYPE_INVENTORY == dropType:
                if dropNumber == player.ITEM_MONEY:
                    net.SendGoldDropPacketNew(dropCount)
                else:
                    # PRIVATESHOP_DISABLE_ITEM_DROP
                    self.__SendDropItemPacket(dropNumber, dropCount)
                    # END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
            elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
                    # PRIVATESHOP_DISABLE_ITEM_DROP
                    self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY)
                    # END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

            elif app.ENABLE_SPECIAL_STORAGE and player.SLOT_TYPE_UPGRADE_INVENTORY == dropType or player.SLOT_TYPE_BOOK_INVENTORY == dropType or player.SLOT_TYPE_STONE_INVENTORY == dropType or player.SLOT_TYPE_CHEST_INVENTORY == dropType:
                self.__SendDropItemPacket(dropNumber, dropCount, player.SlotTypeToInvenType(dropType))

        self.itemDropQuestionDialog.Close()
        self.itemDropQuestionDialog = None

        constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

    # PRIVATESHOP_DISABLE_ITEM_DROP
    def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
        if uiPrivateShopBuilder.IsBuildingPrivateShop():
            chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
            return

        net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)
    # END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

    def OnMouseRightButtonDown(self):

        self.CheckFocus()

        if True == mouseModule.mouseController.isAttached():
            mouseModule.mouseController.DeattachObject()

        else:
            player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

        return True

    def OnMouseRightButtonUp(self):
        if True == mouseModule.mouseController.isAttached():
            return True

        player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
        return True

    def OnMouseMiddleButtonDown(self):
        player.SetMouseMiddleButtonState(player.MBS_PRESS)

    def OnMouseMiddleButtonUp(self):
        player.SetMouseMiddleButtonState(player.MBS_CLICK)

    def OnUpdate(self):
        app.UpdateGame()

        if self.autoChangeTime and app.GetTime() >= self.autoChangeTime:
            self.autoChangeTime = 0
            net.ExitGame()

        if self.mapNameShower.IsShow():
            self.mapNameShower.Update()

        if app.ENABLE_HIDE_AFFECT_ICONS and constInfo.AffectIconState == 1:
            self.AffectIconState()
            constInfo.AffectIconState = 0

        if app.ENABLE_AUTO_SHOUT:
            if constInfo.AUTO_SHOUT_ACTIVATED and len(constInfo.LAST_SHOUT_MESSAGE) != 0 and hasattr(chr, "IsPremium") and chr.IsPremium():
                if self.lastShoutTime <= app.GetTime():
                    self.lastShoutTime = app.GetTime() + constInfo.SHOUT_PER_SECOND
                    net.SendChatPacket(str(constInfo.LAST_SHOUT_MESSAGE), chat.CHAT_TYPE_SHOUT)

        if app.ENABLE_BOT_CONTROL:
            if app.GetTime() > constInfo.DALGA_BOYU:
                if constInfo.DALGA_BOYU != 0:
                    player.SetBotControlState(True)
                self.BINARY_BotControlTimeUpdate()

        self.interface.BUILD_OnUpdate()

    def OnRender(self):
        app.RenderGame()
        (x, y) = app.GetCursorPosition()
        textTail.UpdateAllTextTail()

        if True == wndMgr.IsPickedWindow(self.hWnd):

            self.PickingCharacterIndex = chr.Pick()

            if -1 != self.PickingCharacterIndex:
                textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
            if 0 != self.targetBoard.GetTargetVID():
                textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

            # ADD_ALWAYS_SHOW_NAME
            if not self.__IsShowName():
                self.PickingItemIndex = item.Pick()
                if -1 != self.PickingItemIndex:
                    textTail.ShowItemTextTail(self.PickingItemIndex)
            # END_OF_ADD_ALWAYS_SHOW_NAME

        ## Show all name in the range

        # ADD_ALWAYS_SHOW_NAME
        if self.__IsShowName():
            textTail.ShowAllTextTail()
            self.PickingItemIndex = textTail.Pick(x, y)
        # END_OF_ADD_ALWAYS_SHOW_NAME

        textTail.UpdateShowingTextTail()
        textTail.ArrangeTextTail()
        if -1 != self.PickingItemIndex:
            textTail.SelectItemName(self.PickingItemIndex)

        grp.PopState()
        grp.SetInterfaceRenderState()

        textTail.Render()
        textTail.HideAllTextTail()

        if app.ENABLE_MOVIEMODE_CAMERA:
            if self.isFreeCamera and self.freeCam['accelerate'] != 0 and app.GetTime() > self.freeCam['nextSpeedup']:
                inMult = 1
                inValue = self.freeCam['inertia']

                if self.freeCam['inertia'] < 0:
                    inMult = -1
                    inValue = self.freeCam['inertia']*-1

                self.freeCam['speed'] += self.freeCam['spVariation'] + inMult*math.log(math.fabs(100 - inValue)+1)

                if self.freeCam['speed'] <= 0:
                    self.freeCam['speed'] = 1
                elif self.freeCam['speed'] > 750:
                    self.freeCam['speed'] = 750

                self.freeCam['inertia'] += self.freeCam['spVariation']*5

                self.freeCam['speed']
                app.SetFreeCameraSpeed(self.freeCam['speed'])
                self.freeCam['nextSpeedup'] = app.GetTime() + 0.1


    def OnPressEscapeKey(self):

        if app.ENABLE_BOT_CONTROL:
            if self.isBotControlActive():
                return

        if app.TARGET == app.GetCursor():
            app.SetCursor(app.NORMAL)

        elif True == mouseModule.mouseController.isAttached():
            mouseModule.mouseController.DeattachObject()

        else:
            self.interface.OpenSystemDialog()

        return True

    def OnIMEReturn(self):
        if app.IsPressed(app.DIK_LSHIFT):
            self.interface.OpenWhisperDialogWithoutTarget()
        else:
            self.interface.ToggleChat()
        return True

    def OnPressExitKey(self):
        self.interface.ToggleSystemDialog()
        return True

    ## BINARY CALLBACK
    ######################################################################################

    if app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
        def BINARY_AddItemToExchangeMsg(self, link, player, count):
            self.interface.AddItemToExchangeMsg(link, player, count)
        
        def BINARY_AddYangToExchangeMsg(self, yang, player):
            self.interface.AddYangToExchangeMsg(yang, player)

    # WEDDING
    def BINARY_LoverInfo(self, name, lovePoint):
        if self.interface.wndMessenger:
            self.interface.wndMessenger.OnAddLover(name, lovePoint)
        if self.affectShower:
            self.affectShower.SetLoverInfo(name, lovePoint)

    def BINARY_UpdateLovePoint(self, lovePoint):
        if self.interface.wndMessenger:
            self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
        if self.affectShower:
            self.affectShower.OnUpdateLovePoint(lovePoint)
    # END_OF_WEDDING

    # QUEST_CONFIRM
    def BINARY_OnQuestConfirm(self, msg, timeout, pid):
        confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
        confirmDialog.Open(msg, timeout)
        confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
        confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
        self.confirmDialog = confirmDialog
    # END_OF_QUEST_CONFIRM

    def BINARY_Highlight_Item(self, inven_type, inven_pos):
        # @fixme003 (+if self.interface:)
        if self.interface:
            self.interface.Highligt_Item(inven_type, inven_pos)

    def BINARY_DragonSoulGiveQuilification(self):
        self.interface.DragonSoulGiveQuilification()

    def BINARY_DragonSoulRefineWindow_Open(self):
        self.interface.OpenDragonSoulRefineWindow()

    def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
        self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

    def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
        self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)

    # END of DRAGON SOUL REFINE WINDOW

    def BINARY_SetBigMessage(self, message):
        self.interface.bigBoard.SetTip(message)

    def BINARY_SetTipMessage(self, message):
        self.interface.tipBoard.SetTip(message)

    def BINARY_AppendNotifyMessage(self, type):
        if not type in localeInfo.NOTIFY_MESSAGE:
            return
        chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

    if app.ENABLE_ZODIAC_TEMPLE_CHAT:
        def BINARY_SetMissionMessage(self, message):
            self.interface.missionBoard.SetMission(message)
            
        def BINARY_SetSubMissionMessage(self, message):
            self.interface.missionBoard.SetSubMission(message)
            
        def BINARY_CleanMissionMessage(self):
            self.interface.missionBoard.CleanMission()

    if app.ENABLE_EXTENDED_WHISPER_DETAILS and app.ENABLE_MULTI_LANGUAGE_SYSTEM:
        def BINARY_RecieveWhisperDetails(self, name, country):
            if self.interface:
                self.interface.RecieveWhisperDetails(name, country)

    def BINARY_Guild_EnterGuildArea(self, areaID):
        self.interface.BULID_EnterGuildArea(areaID)

    def BINARY_Guild_ExitGuildArea(self, areaID):
        self.interface.BULID_ExitGuildArea(areaID)

    def BINARY_GuildWar_OnSendDeclare(self, guildID):
        pass

    def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
        mainCharacterName = player.GetMainCharacterName()
        masterName = guild.GetGuildMasterName()
        if mainCharacterName == masterName:
            self.__GuildWar_OpenAskDialog(guildID, warType)

    def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
        self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

    def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
        self.interface.OnStartGuildWar(guildSelf, guildOpp)

    def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
        self.interface.OnEndGuildWar(guildSelf, guildOpp)

    def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
        self.interface.BINARY_SetObserverMode(isEnable)

    def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
        self.interface.wndMiniMap.UpdateObserverCount(observerCount)

    def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
        guildID1 = int(guildID1)
        guildID2 = int(guildID2)
        memberCount1 = int(memberCount1)
        memberCount2 = int(memberCount2)
        observerCount = int(observerCount)

        self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
        self.interface.wndMiniMap.UpdateObserverCount(observerCount)

    def __GuildWar_OpenAskDialog(self, guildID, warType):

        guildName = guild.GetGuildName(guildID)

        # REMOVED_GUILD_BUG_FIX
        if "Noname" == guildName:
            return
        # END_OF_REMOVED_GUILD_BUG_FIX

        import uiGuild
        questionDialog = uiGuild.AcceptGuildWarDialog()
        questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
        questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
        questionDialog.Open(guildName, warType)

        self.guildWarQuestionDialog = questionDialog

    def __GuildWar_CloseAskDialog(self):
        self.guildWarQuestionDialog.Close()
        self.guildWarQuestionDialog = None

    def __GuildWar_OnAccept(self):

        guildName = self.guildWarQuestionDialog.GetGuildName()

        net.SendChatPacket("/war " + guildName)
        self.__GuildWar_CloseAskDialog()

        return 1

    def __GuildWar_OnDecline(self):

        guildName = self.guildWarQuestionDialog.GetGuildName()

        net.SendChatPacket("/nowar " + guildName)
        self.__GuildWar_CloseAskDialog()

        return 1
    ## BINARY CALLBACK
    ######################################################################################

    def __ServerCommand_Build(self):
        serverCommandList={
            "ConsoleEnable"			: self.__Console_Enable,
            "DayMode"				: self.__DayMode_Update,
            "PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update,
            "CloseRestartWindow"	: self.__RestartDialog_Close,
            "OpenPrivateShop"		: self.__PrivateShop_Open,
            "PartyHealReady"		: self.PartyHealReady,
            "ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
            "CloseSafebox"			: self.CommandCloseSafebox,

            # ITEM_MALL
            "CloseMall"				: self.CommandCloseMall,
            "ShowMeMallPassword"	: self.AskMallPassword,
            "item_mall"				: self.__ItemMall_Open,
            # END_OF_ITEM_MALL

            "RefineSuceeded"		: self.RefineSuceededMessage,
            "RefineFailed"			: self.RefineFailedMessage,
            "xmas_snow"				: self.__XMasSnow_Enable,
            "xmas_boom"				: self.__XMasBoom_Enable,
            "xmas_song"				: self.__XMasSong_Enable,
            "xmas_tree"				: self.__XMasTree_Enable,
            "newyear_boom"			: self.__XMasBoom_Enable,
            "PartyRequest"			: self.__PartyRequestQuestion,
            "PartyRequestDenied"	: self.__PartyRequestDenied,
            "horse_state"			: self.__Horse_UpdateState,
            "hide_horse_state"		: self.__Horse_HideState,
            "WarUC"					: self.__GuildWar_UpdateMemberCount,
            "test_server"			: self.__EnableTestServerFlag,
            "mall"					: self.__InGameShop_Show,

            # WEDDING
            "lover_login"			: self.__LoginLover,
            "lover_logout"			: self.__LogoutLover,
            "lover_near"			: self.__LoverNear,
            "lover_far"				: self.__LoverFar,
            "lover_divorce"			: self.__LoverDivorce,
            "PlayMusic"				: self.__PlayMusic,
            # END_OF_WEDDING

            # PRIVATE_SHOP_PRICE_LIST
            "MyShopPriceList"		: self.__PrivateShop_PriceList,
            # END_OF_PRIVATE_SHOP_PRICE_LIST
            "SetFarmBlock"			: self.SetFarmBlock,
            "CloseAllWindows"			: self.CloseAllWindowsByCommand,
        }

        if app.ENABLE_FISHING_RENEWAL:
            serverCommandList["OpenFish"] = self.OpenFish

        if app.ENABLE_MINING_RENEWAL:
            serverCommandList.update({
                "MiningRenewalWindow" : self.MiningRenewalWindow,
                "SendPickaxePoint" : self.SendPickaxePoint
            })

        if app.ENABLE_ITEMSHOP:
            serverCommandList.update({
                "SetWheelItemData" : self.interface.SetWheelItemData,
                "OnSetWhell" : self.interface.OnSetWhell,
                "GetWheelGiftData" : self.interface.GetWheelGiftData,
                "SetDragonCoin" : self.ItemShopSetDragonCoin,
                "ItemShopAppendLog" :  self.ItemShopAppendLog
            })

        if app.ENABLE_TELEPORT_TO_A_FRIEND:
            serverCommandList["RequestWarpToCharacter"] = self.RequestWarpToCharacter

        if app.ENABLE_DISTANCE_SKILL_SELECT:
            serverCommandList.update({
                "SELECT_JOB" : self.SelectJob,
            })

        serverCommandList["SetVoteQuestIndex"] = self.SetVoteQuestIdx
        if app.ENABLE_VOTE4BUFF:
            serverCommandList.update({
                "Vote4Buff" : self.Vote4Buff,
            })

        if app.ENABLE_MAINTENANCE_SYSTEM:
            serverCommandList.update({
                "Maintenancegui"				:self.interface.ShowMaintenanceInfo,
            })

        if app.ENABLE_DUNGEON_MODULES:
            serverCommandList.update({
                "RefreshDungeonFloor"				:self.RefreshDungeonFloor,
                "RefreshDungeonTimer"				:self.RefreshDungeonTimer,
            })

        if getattr(app, "ENABLE_BUY_BACK_ITEM", 0):
            serverCommandList.update({
                "BuyBackClear"					: self.BINARY_BuyBackClear,
                "BuyBackItem"					: self.BINARY_BuyBackAppend,
                "GmRestoreClear"				: self.BINARY_GmRestoreClear,
                "GmRestoreItem"					: self.BINARY_GmRestoreAppend,
            })

        self.serverCommander=stringCommander.Analyzer()
        for serverCommandItem in serverCommandList.items():
            self.serverCommander.SAFE_RegisterCallBack(
                serverCommandItem[0], serverCommandItem[1]
            )

    if app.ENABLE_CUBE_RENEWAL_WORLDARD:
        def BINARY_CUBE_RENEWAL_OPEN(self):
            if self.interface:
                self.interface.BINARY_CUBE_RENEWAL_OPEN()

    def BINARY_ServerCommand_Run(self, line):
        try:
            return self.serverCommander.Run(line)
        except RuntimeError as msg:
            dbg.TraceError(msg)
            return 0

    def __ProcessPreservedServerCommand(self):
        try:
            command = net.GetPreservedServerCommand()
            while command:
                self.serverCommander.Run(command)
                command = net.GetPreservedServerCommand()
        except RuntimeError as msg:
            dbg.TraceError(msg)
            return 0

    def PartyHealReady(self):
        self.interface.PartyHealReady()

    def AskSafeboxPassword(self):
        self.interface.AskSafeboxPassword()

    # ITEM_MALL
    def AskMallPassword(self):
        self.interface.AskMallPassword()

    def __ItemMall_Open(self):
        self.interface.OpenItemMall()

    def CommandCloseMall(self):
        self.interface.CommandCloseMall()
    # END_OF_ITEM_MALL

    def RefineSuceededMessage(self):
        snd.PlaySound("sound/ui/make_soket.wav")
        self.PopupMessage(localeInfo.REFINE_SUCCESS)
        if app.ENABLE_REFINE_RENEWAL:
            self.interface.CheckRefineDialog(False)

    def RefineFailedMessage(self):
        snd.PlaySound("sound/ui/jaeryun_fail.wav")
        self.PopupMessage(localeInfo.REFINE_FAILURE)
        if app.ENABLE_REFINE_RENEWAL:
            self.interface.CheckRefineDialog(True)

    def CommandCloseSafebox(self):
        self.interface.CommandCloseSafebox()

    # PRIVATE_SHOP_PRICE_LIST
    def __PrivateShop_PriceList(self, itemVNum, itemPrice):
        uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)
    # END_OF_PRIVATE_SHOP_PRICE_LIST

    def __Horse_HideState(self):
        self.affectShower.SetHorseState(0, 0, 0)

    def __Horse_UpdateState(self, level, health, battery):
        self.affectShower.SetHorseState(int(level), int(health), int(battery))

    def __IsXMasMap(self):
        mapDict = ( "metin2_map_n_flame_01",
                    "metin2_map_n_desert_01",
                    "metin2_map_spiderdungeon",
                    "metin2_map_deviltower1", )

        if background.GetCurrentMapName() in mapDict:
            return False

        return True

    def __XMasSnow_Enable(self, mode):

        self.__XMasSong_Enable(mode)

        if "1"==mode:

            if not self.__IsXMasMap():
                return

            background.EnableSnow(1)

        else:
            background.EnableSnow(0)

    def __XMasBoom_Enable(self, mode):
        if "1"==mode:

            if not self.__IsXMasMap():
                return

            self.__DayMode_Update("dark")
            self.enableXMasBoom = True
            self.startTimeXMasBoom = app.GetTime()
        else:
            self.__DayMode_Update("light")
            self.enableXMasBoom = False

    def __XMasTree_Enable(self, grade):
        background.SetXMasTree(int(grade))

    def __XMasSong_Enable(self, mode):
        pass

    def __RestartDialog_Close(self):
        self.interface.CloseRestartDialog()

    def __Console_Enable(self):
        pass

    ## PrivateShop
    def __PrivateShop_Open(self):
        self.interface.OpenPrivateShopInputNameDialog()

    def BINARY_PrivateShop_Appear(self, vid, text):
        self.interface.AppearPrivateShop(vid, text)

    def BINARY_PrivateShop_Disappear(self, vid):
        self.interface.DisappearPrivateShop(vid)

    ## DayMode
    def __PRESERVE_DayMode_Update(self, mode):
        if "light"==mode:
            background.SetEnvironmentData(0)
        elif "dark"==mode:

            if not self.__IsXMasMap():
                return

            background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
            background.SetEnvironmentData(1)

    def __DayMode_Update(self, mode):
        if "light"==mode:
            self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
        elif "dark"==mode:
            if not self.__IsXMasMap():
                return
            self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

    def __DayMode_OnCompleteChangeToLight(self):
        background.SetEnvironmentData(0)
        self.curtain.FadeIn()

    def __DayMode_OnCompleteChangeToDark(self):
        background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
        background.SetEnvironmentData(1)
        self.curtain.FadeIn()

    ## XMasBoom
    def __XMasBoom_Update(self):

        self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
        if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
            return

        boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
        boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

        if app.GetTime() - self.startTimeXMasBoom > boomTime:

            self.indexXMasBoom += 1

            for i in xrange(boomCount):
                self.__XMasBoom_Boom()

    def __XMasBoom_Boom(self):
        pass

    def __PartyRequestQuestion(self, vid):
        vid = int(vid)
        partyRequestQuestionDialog = uiCommon.QuestionDialog()
        partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
        partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
        partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
        partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
        partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
        partyRequestQuestionDialog.Open()
        partyRequestQuestionDialog.vid = vid
        self.partyRequestQuestionDialog = partyRequestQuestionDialog

    def __AnswerPartyRequest(self, answer):
        if not self.partyRequestQuestionDialog:
            return

        vid = self.partyRequestQuestionDialog.vid

        if answer:
            net.SendChatPacket("/party_request_accept " + str(vid))
        else:
            net.SendChatPacket("/party_request_deny " + str(vid))

        self.partyRequestQuestionDialog.Close()
        self.partyRequestQuestionDialog = None

    def __PartyRequestDenied(self):
        self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

    def __EnableTestServerFlag(self):
        app.EnableTestServerFlag()

    def __InGameShop_Show(self, url):
        if constInfo.IN_GAME_SHOP_ENABLE:
            self.interface.OpenWebWindow(url)

    # WEDDING
    def __LoginLover(self):
        if self.interface.wndMessenger:
            self.interface.wndMessenger.OnLoginLover()

    def __LogoutLover(self):
        if self.interface.wndMessenger:
            self.interface.wndMessenger.OnLogoutLover()
        if self.affectShower:
            self.affectShower.HideLoverState()

    def __LoverNear(self):
        if self.affectShower:
            self.affectShower.ShowLoverState()

    def __LoverFar(self):
        if self.affectShower:
            self.affectShower.HideLoverState()

    def __LoverDivorce(self):
        if self.interface.wndMessenger:
            self.interface.wndMessenger.ClearLoverInfo()
        if self.affectShower:
            self.affectShower.ClearLoverState()

    def __PlayMusic(self, flag, filename):
        pass

    if app.ENABLE_ACCE_COSTUME_SYSTEM:
        def ActAcce(self, iAct, bWindow):
            if self.interface:
                self.interface.ActAcce(iAct, bWindow)

        def AlertAcce(self, bWindow):
            if not bWindow:
            # 	self.PopupMessage(localeInfo.ACCE_DEL_SERVEITEM)
            # else:
                self.PopupMessage(localeInfo.ACCE_DEL_ABSORDITEM)

    if app.ENABLE_TARGET_INFORMATION_SYSTEM:
        def BINARY_AddTargetMonsterDropInfo(self, raceNum, itemVnum, itemCount):
            if not raceNum in constInfo.MONSTER_INFO_DATA:
                constInfo.MONSTER_INFO_DATA.update({raceNum : {}})
                constInfo.MONSTER_INFO_DATA[raceNum].update({"items" : []})
            curList = constInfo.MONSTER_INFO_DATA[raceNum]["items"]

            isUpgradeable = False
            isMetin = False
            item.SelectItem(itemVnum)
            if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
                isUpgradeable = True
            elif item.GetItemType() == item.ITEM_TYPE_METIN:
                isMetin = True

            for curItem in curList:
                if isUpgradeable:
                    if curItem.has_key("vnum_list") and curItem["vnum_list"][0] / 10 * 10 == itemVnum / 10 * 10:
                        if not (itemVnum in curItem["vnum_list"]):
                            curItem["vnum_list"].append(itemVnum)
                        return
                elif isMetin:
                    if curItem.has_key("vnum_list"):
                        baseVnum = curItem["vnum_list"][0]
                    if curItem.has_key("vnum_list") and (baseVnum - baseVnum%1000) == (itemVnum - itemVnum%1000):
                        if not (itemVnum in curItem["vnum_list"]):
                            curItem["vnum_list"].append(itemVnum)
                        return
                else:
                    if curItem.has_key("vnum") and curItem["vnum"] == itemVnum and curItem["count"] == itemCount:
                        return

            if isUpgradeable or isMetin:
                curList.append({"vnum_list":[itemVnum], "count":itemCount})
            else:
                curList.append({"vnum":itemVnum, "count":itemCount})

        def BINARY_RefreshTargetMonsterDropInfo(self, raceNum):
            self.targetBoard.RefreshMonsterInfoBoard()

    if app.ENABLE_CHANNEL_INFO_UPDATE:
        def BINARY_ReceiveChannel(self, channel):
            import serverInfo
            if constInfo.SERVER_SELECTED == 1:
                srvName = serverInfo.SERVER_NAME
            else:
                srvName = serverInfo.SERVER_NAME_2
            net.SetServerInfo(srvName)
            if self.interface:
                if self.interface.wndMiniMap:
                    self.interface.wndMiniMap.UpdateChannelInfo(channel)
            constInfo.channel_idx = channel

    def OpenPrivateMessage(self, name):
        self.interface.OpenWhisperDialog(name)

    if app.ENABLE_SWITCHBOT:
        def RefreshSwitchbotWindow(self):
            if self.interface:
                self.interface.RefreshSwitchbotWindow()
            
        def RefreshSwitchbotItem(self, slot):
            if self.interface:
                self.interface.RefreshSwitchbotItem(slot)

    if app.ENABLE_GLOBAL_RANKING:
        def SendOpenRanking(self):
            if ranking.updatetime() < 1:
                net.SendChatPacket("/request_best_player_list")
                return

            if self.rankingWindow == None:
                self.rankingWindow = uiranking.RankingWindow()
                self.rankingWindow.Open()
            else:
                self.rankingWindow.Close()
                self.rankingWindow = None

        def BINARY_OpenRanking(self):
            if self.rankingWindow == None:
                self.rankingWindow = uiranking.RankingWindow()
                self.rankingWindow.Open()
            else:
                self.rankingWindow.Close()
                self.rankingWindow = None

        def BINARY_RankingData(self, ranktype, rank, name, value, race):
            if (rank > 10):
                constInfo.SetFlag("ranking_%s_my_player_order" % (uiranking.rankList[int(ranktype)]["ranktype"]), str((int(rank) - 10)))
                constInfo.SetFlag("ranking_%s_player_name_%d" % (uiranking.rankList[int(ranktype)]["ranktype"], 11), str(name))
                constInfo.SetFlag("ranking_%s_value_%d" % (uiranking.rankList[int(ranktype)]["ranktype"], 11), str(value))
                constInfo.SetFlag("ranking_%s_race_%d" % (uiranking.rankList[int(ranktype)]["ranktype"], 11), str(race))
            else:
                constInfo.SetFlag("ranking_%s_player_name_%d" % (uiranking.rankList[int(ranktype)]["ranktype"], (int(rank))), str(name))
                constInfo.SetFlag("ranking_%s_value_%d" % (uiranking.rankList[int(ranktype)]["ranktype"], (int(rank))), str(value))
                constInfo.SetFlag("ranking_%s_race_%d" % (uiranking.rankList[int(ranktype)]["ranktype"], (int(rank))), str(race))

        def BINARY_RankingDataCountry(self, ranktype, rank, country):
            constInfo.SetFlag("ranking_%s_other_data_%d" % (uiranking.rankList[int(ranktype)]["ranktype"], (int(rank))), str(country))

    if app.ENABLE_HIDE_AFFECT_ICONS:
        def AffectIconState(self):
            index = systemSetting.IsAffectIconShow()
            if index:
                self.affectShower.Show()
            else:
                self.affectShower.Hide()

    if app.ENABLE_BIOLOG_SYSTEM:
        def BIOLOG_OpenWindow(self):
            self.interface.OpenBiologWindow()

        def BIOLOG_UpdateLevel(self):
            if self.interface.wndBiolog:
                self.interface.wndBiolog.LevelUpdate()

        def BIOLOG_UpdateCount(self):
            if self.interface.wndBiolog:
                self.interface.wndBiolog.CountUpdate()

        def BIOLOG_MAX_LEVEL(self):
            if self.interface.wndBiolog == None:
                chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.BIOLOG_FINISHED)
            else:
                if self.interface.wndBiolog.IsShow():
                    self.interface.wndBiolog.Close()
                self.interface.wndBiolog == None
                chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.BIOLOG_FINISHED)


    if app.ENABLE_CHAR_SETTINGS:
        def RefreshCharSettings(self, settingstype):
            if settingstype == player.SETTINGS_ANTI_EXP:
                self.SetAntiExp()
            # if app.ENABLE_HIDE_COSTUME_SYSTEM:
            # 	self.GetCostumeHideState()

        def SetCharSettings(self):
            self.SetAntiExp()
            if app.ENABLE_HIDE_COSTUME_SYSTEM:
                self.GetCostumeHideState()

        def SetAntiExp(self):
            if self.interface:
                antiExp = self.interface.wndTaskBar.GetChild("AntiExp")
                if player.GetAntiExpState():
                    antiExp.SetUpVisual("d:/ymir work/ui/game/anti_exp/no_exp_0.png")
                    antiExp.SetOverVisual("d:/ymir work/ui/game/anti_exp/no_exp_1.png")
                    antiExp.SetDownVisual("d:/ymir work/ui/game/anti_exp/no_exp_2.png")

                    if self.interface.wndTaskBar.IsChild("RestExp_Value"):
                        self.interface.wndTaskBar.GetChild("Exp_Value").Hide()
                    if self.interface.wndTaskBar.IsChild("Exp_Value"):
                        self.interface.wndTaskBar.GetChild("RestExp_Value").Hide()

                    if self.interface.wndCharacter.IsChild("RestExp_Value"):
                        self.interface.wndCharacter.GetChild("Exp_Value").SetPackedFontColor(0xFFe80202)

                    for j in xrange(1, 5):
                        if self.interface.wndTaskBar.IsChild("EXPGauge_0%d"%j):
                            self.interface.wndTaskBar.GetChild("EXPGauge_0%d"%j).SetDiffuseColor(104.0 / 255.0, 104.0 / 255.0, 104.0 / 255.0, 1)
                else:
                    antiExp.SetUpVisual("d:/ymir work/ui/game/anti_exp/exp_0.png")
                    antiExp.SetOverVisual("d:/ymir work/ui/game/anti_exp/exp_1.png")
                    antiExp.SetDownVisual("d:/ymir work/ui/game/anti_exp/exp_2.png")

                    if self.interface.wndTaskBar.IsChild("RestExp_Value"):
                        self.interface.wndTaskBar.GetChild("Exp_Value").Show()
                    if self.interface.wndTaskBar.IsChild("Exp_Value"):
                        self.interface.wndTaskBar.GetChild("RestExp_Value").Show()

                    if self.interface.wndCharacter.IsChild("RestExp_Value"):
                        self.interface.wndCharacter.GetChild("Exp_Value").SetPackedFontColor(0xFFffffff)

                    for j in xrange(1, 5):
                        if self.interface.wndTaskBar.IsChild("EXPGauge_0%d"%j):
                            self.interface.wndTaskBar.GetChild("EXPGauge_0%d"%j).SetDiffuseColor(201, 160, 51, 1)

    if app.ENABLE_IN_GAME_LOG_SYSTEM:
        def BINARY_IN_GAME_LOG_OPEN(self,page):
            self.wndInGameLog.ChangePage(page)

        def OpenInGameLog(self):
            if not self.wndInGameLog:
                self.wndInGameLog = uiingamelog.IngameLogWindow()

            if self.wndInGameLog.IsShow():
                self.wndInGameLog.Close()
            else:
                self.wndInGameLog.Open()

        def BINARY_IN_GAME_LOG_TRADE_DETAILS(self,logID):
            self.wndInGameLog.UpdateLog(logID)

    if app.ENABLE_FISHING_RENEWAL:
        def OpenFish(self, p):
            n = int(p)
            if n == 1:
                import uiFishGame
                self.FishGame = uiFishGame.FishGame()
                # self.FishGame.ClearFishing()
                self.FishGame.StartFishing()
            else:
                if self.FishGame:
                    # self.FishGame.ClearFishing()
                    self.FishGame.Close()
                    del self.FishGame

    if app.ENABLE_MINING_RENEWAL:
        def MiningRenewalWindow(self, state, miningPoint):

            if miningPoint == -1:
                return

            state = int(state)

            if state == 1 and miningPoint:
                self.wndMiningGame = uiminingrenewal.MiningWindow()
                self.wndMiningGame.StartMining(miningPoint)
            else:
                try:
                    if self.wndMiningGame:
                        self.wndMiningGame.Close(True)
                        del self.wndMiningGame
                except:
                    pass

        def SendPickaxePoint(self, points):
            constInfo.MINING_POINT = int(points)

    if app.ENABLE_HIDE_COSTUME_SYSTEM:
        def GetCostumeHideState(self):
            self.interface.RefreshVisibleCostume()

    def SetFarmBlock(self, state):
        if self.interface:
            farmBlock = self.interface.wndTaskBar.GetChild("FarmBlock")
            if int(state):
                farmBlock.SetUpVisual("d:/ymir work/ui/game/anti_exp/no_farm_block_0.png")
                farmBlock.SetOverVisual("d:/ymir work/ui/game/anti_exp/no_farm_block_1.png")
                farmBlock.SetDownVisual("d:/ymir work/ui/game/anti_exp/no_farm_block_2.png")
            else:
                farmBlock.SetUpVisual("d:/ymir work/ui/game/anti_exp/farm_block_0.png")
                farmBlock.SetOverVisual("d:/ymir work/ui/game/anti_exp/farm_block_1.png")
                farmBlock.SetDownVisual("d:/ymir work/ui/game/anti_exp/farm_block_2.png")
                
        if app.ENABLE_DUNGEON_INFO:
            dungeonInfo.timeRequest()#Zindan surelerini sadece ilk giriste cekmesini saglar

    if app.ENABLE_PM_ALL_SEND_SYSTEM:
        def BINARY_OnRecvBulkWhisper(self, content):
            content = content.replace("$", " ")
            self.interface.RegisterGameMasterName(localeInfo.SYSTEM_MESSAGE)
            chat.AppendWhisper(chat.WHISPER_TYPE_CHAT, localeInfo.SYSTEM_MESSAGE, content)
            self.interface.RecvWhisper(localeInfo.SYSTEM_MESSAGE)

    def TestGui(self):
        # botcontrolType = app.GetRandom(0, 2)
        # if botcontrolType == 0:
        # 	self.botcontrolwindow = uisecurity.WritingCaptcha()
        # elif botcontrolType == 1:
        # 	self.botcontrolwindow = uisecurity.FindTheDifferentCaptcha()
        # elif botcontrolType == 2:
        # self.botcontrolwindow = uisecurity.SortTheNumbers()

        # if self.botcontrolwindow:
        # 	self.botcontrolwindow.Open()

        # import uibuffisystem
        import lightwork
        xd = lightwork.ModelTester()
        xd.Open()
        pass

    if app.ENABLE_DUNGEON_INFO:
        def ToggleBossTimerWindow(self):
            if self.wndBossTimer:
                if self.wndBossTimer.IsShow():
                    self.wndBossTimer.Close()
                else:
                    self.wndBossTimer.Open()
            else:
                self.wndBossTimer = uiBossTimer.DungeonInformationsWindow()
                # self.wndBossTimer.ReadHiddenBossList()
                self.wndBossTimer.Open()

        def DungeonInfoErrorMessage(self, messageID):
            self.PopupMessage(uiBossTimer.ErrorMessageList[int(messageID)])

        def DungeonNotificationMessage(self, bossVnum):
            bossName = nonplayer.GetMonsterName(int(bossVnum))
            message = localeInfo.DUNGEON_NOTIFICATION_MESSAGE.format(bossName)
            self.OnRecvWhisperSystemMessage(255, localeInfo.DUNGEON_NOTIFICATION_TITLE, message)

    if app.ENABLE_EVENT_MANAGER:
        def ClearEventManager(self):
            self.interface.ClearEventManager()
    
        def RefreshEventManager(self):
            self.interface.RefreshEventManager()
    
        def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
            self.interface.RefreshEventStatus(int(eventID), int(eventStatus), int(eventendTime), str(eventEndTimeText))

        def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
            self.interface.AppendEvent(int(dayIndex),int(eventID), int(eventIndex), str(startTime), str(endTime), int(empireFlag), int(channelFlag), int(value0), int(value1), int(value2), int(value3), int(startRealTime), int(endRealTime), int(isAlreadyStart))

    if app.ENABLE_ITEMSHOP:
        def ItemShopClear(self, updateTime):
            uiItemShopNew.ItemShopClear(int(updateTime))

        def ItemShopUpdateItem(self, itemID, itemVnum, itemPrice, itemDiscount, itemOffertime, itemTopSelling, itemAddedTime, itemSellingCount, itemMaxSellingCount, itemUntradeablePrice):
            uiItemShopNew.ItemShopUpdateItem(int(itemID), int(itemVnum), long(itemPrice), int(itemDiscount), int(itemOffertime), int(itemTopSelling), int(itemAddedTime), long(itemSellingCount), int(itemMaxSellingCount), long(itemUntradeablePrice))
            self.interface.ItemShopUpdateItem(int(itemID), int(itemMaxSellingCount))

        def ItemShopAppendItem(self, categoryIndex, categorySubIndex, itemID, itemVnum, itemPrice, itemDiscount, itemOffertime, itemTopSelling, itemAddedTime, itemSellingCount, itemMaxSellingCount, itemUntradeablePrice):
            uiItemShopNew.ItemShopAppendItem(int(categoryIndex), int(categorySubIndex), int(itemID), int(itemVnum), long(itemPrice), int(itemDiscount), int(itemOffertime), int(itemTopSelling), int(itemAddedTime), long(itemSellingCount), int(itemMaxSellingCount), long(itemUntradeablePrice))

        def ItemShopHideLoading(self):
            self.interface.ItemShopHideLoading()

        def ItemShopOpenMainPage(self):
            self.interface.OpenItemShopMainWindow()

        def ItemShopLogClear(self):
            uiItemShopNew.ItemShopLogClear()

        def ItemShopAppendLog(self, dateText, dateTime, playerName, ipAdress, itemVnum, itemCount, itemPrice):
            uiItemShopNew.ItemShopAppendLog(str(dateText), dateTime, str(playerName), str(ipAdress), int(itemVnum), int(itemCount), long(itemPrice))

        def ItemShopPurchasesWindow(self):
            self.interface.ItemShopPurchasesWindow()

        def ItemShopSetDragonCoin(self, dragonCoin):
            self.interface.ItemShopSetDragonCoin(long(dragonCoin))

        def ItemShopAppendLogEx(self, dateText, dateText2,dateTime, playerName, ipAdress, itemVnum, itemCount, itemPrice):
            uiItemShopNew.ItemShopAppendLog(str(dateText)+" "+str(dateText2), int(dateTime), str(playerName), str(ipAdress), int(itemVnum), int(itemCount), long(itemPrice))

    if app.ENABLE_SHOW_STROKE_INFO:
        def RegisterStroke(self, targetVID):
            self.targetBoard.RegisterStroke(targetVID)

    if app.ENABLE_TELEPORT_TO_A_FRIEND:
        def RequestWarpToCharacter(self, name):
            questionDialogWarp = uiCommon.QuestionDialog()
            questionDialogWarp.SetText(localeInfo.ACCEPT_WARP_FROM_YOUR_FRIEND_REQUEST % (name))
            questionDialogWarp.SetAcceptEvent(lambda: self.WarpAcceptEvent(name))
            questionDialogWarp.SetCancelEvent(lambda: self.WarpCancelEvent())
            questionDialogWarp.Open()
            self.questionDialogWarp = questionDialogWarp
            return

        def WarpAcceptEvent(self, name):
            net.SendMessengerSummonByNamePacket(name)
            self.questionDialogWarp.Close()

        def WarpCancelEvent(self):
            self.questionDialogWarp.Close()

    if app.ENABLE_NEW_PET_SYSTEM:
        def SetPetInformations(self, level, evolution, ptype, star):
            self.interface.wndPetWindow.SetInformations(level, evolution, ptype, star)

        def SetPetSkin(self, skinCount, skinVnum):
            self.interface.wndPetWindow.SetSkin(skinCount, skinVnum)

        def SetPetExp(self, petExperience, petNextExp):
            self.interface.wndPetWindow.SetExperience(petExperience, petNextExp)

        def SetPetskill(self, slot, idx, lv):
            self.interface.wndPetWindow.SetSkill(slot, idx, lv)

        def SetPetBonus(self, b1, b2, b3):
            self.interface.wndPetWindow.SetBonus(b1,b2,b3)

        def OpenPetInterface(self):
            if self.__PressPKey():
                return

            if self.interface.wndPetWindow.IsShow():
                self.interface.wndPetWindow.Close()
            else:
                self.interface.wndPetWindow.Open()
                self.interface.wndPetWindow.SetTop()

        def PetUnsummon(self):
            self.interface.wndPetWindow.PetUnsummon()

    if app.ENABLE_DISTANCE_SKILL_SELECT:
        def SelectJob(self):
            # if state == 1:#open
            self.interface.ToggleCharacterWindow("SKILL")
            self.interface.wndCharacter.ShowSelectSkillPage()
            constInfo.CHOOSE_SKILL = 1

    if app.ENABLE_AURA_SYSTEM:
        def ActAura(self, iAct, bWindow):
            if self.interface:
                self.interface.ActAura(iAct, bWindow)

        def AlertAura(self, bWindow):
            pass

    if app.ENABLE_BOT_CONTROL:
        def BINARY_BotControlOpen(self):
            botcontrolType = app.GetRandom(0, 2)
            if botcontrolType == 0:
                self.botControlWnd = uisecurity.WritingCaptcha()
            elif botcontrolType == 1:
                self.botControlWnd = uisecurity.FindTheDifferentCaptcha()
            elif botcontrolType == 2:
                self.botControlWnd = uisecurity.SortTheNumbers()

            if self.botControlWnd:
                self.botControlWnd.Open()

        def BINARY_BotControlTimeUpdate(self):
            botcontroltime = app.GetRandom(1200, 1800)
            constInfo.DALGA_BOYU = app.GetTime() + botcontroltime

        def BINARY_BotControlFail(self):
            self.EndExchange()
            self.interface.CommandCloseSafebox()
            net.SendChatPacket("/bot31_control_fail")

        def isBotControlActive(self):
            if self.botControlWnd:
                return self.botControlWnd.IsShow()

            return False

    def SetVoteQuestIdx(self, qidx):
        constInfo.VOTE_QUEST_IDX = int(qidx)

    if app.ENABLE_VOTE4BUFF:
        def Vote4Buff(self, cmd):
            cmd = int(cmd)

            if cmd == 0:
                if self.interface:
                    if self.interface.wndVoteIcon:
                        self.interface.wndVoteIcon.Hide()
                    if self.interface.wndTaskBar and getattr(self.interface.wndTaskBar, "Vote4BuffButton", None):
                        self.interface.wndTaskBar.Vote4BuffButton.Hide()
                return

            if self.interface:
                self.interface.MakeVote4BuffIcon()
                self.interface.wndVoteIcon.Open()
                self.interface.wndVoteIcon.SetEventType(cmd)


    if app.ENABLE_EXTENDED_BATTLE_PASS:
        def BINARY_ExtOpenBattlePass(self):
            if self.interface:
                self.interface.ReciveOpenExtBattlePass()
            
        def BINARY_ExtBattlePassAddGeneralInfo(self, BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime):
            if self.interface:

                if BattlePassName == "normal_november_2021_week_1":
                    BattlePassName = "Normal Mission Pass"
                elif BattlePassName == "premium_november_2021_week_1":
                    BattlePassName = "Premium Mission Pass"
                elif BattlePassName == "event_2021_advent_event":
                    BattlePassName = "Event Mission Pass"

                self.interface.AddExtendedBattleGeneralInfo(BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime)
                
        def BINARY_ExtBattlePassAddMission(self, battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3):
            if self.interface:
                self.interface.AddExtendedBattlePassMission(battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3)

        def BINARY_ExtBattlePassAddMissionReward(self, battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount):
            if self.interface:
                self.interface.AddExtendedBattlePassMissionReward(battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount)

        def BINARY_ExtBattlePassUpdate(self, battlepassType, missionIndex, missionType, newProgress):
            if self.interface:
                self.interface.UpdateExtendedBattlePassMission(battlepassType, missionIndex, missionType, newProgress)

        def BINARY_ExtBattlePassAddReward(self, battlepassType, battlepassID, itemVnum, itemCount):
            if self.interface:
                self.interface.AddExtendedBattlePassReward(battlepassType, battlepassID, itemVnum, itemCount)
        
        def BINARY_ExtBattlePassAddRanklistEntry(self, playername, battlepassType, battlepassID, startTime, endTime):
            if self.interface:
                self.interface.AddExtBattlePassRanklistEntry(playername, battlepassType, battlepassID, startTime, endTime)

    if app.ENABLE_DUNGEON_MODULES:
        def RefreshDungeonTimer(self, Floor,Time):
            if self.interface:
                if self.interface.wndMiniMap:
                    self.interface.wndMiniMap.Hide()
                self.interface.MakeDungeonTimerWindow()
                if self.interface.wndDungeonTimer:
                    self.interface.wndDungeonTimer.RefreshDungeonTimer(Time, Floor)

        def RefreshDungeonFloor(self, Floor2):
            if self.interface:
                if self.interface.wndMiniMap:
                    self.interface.wndMiniMap.Hide()
                self.interface.MakeDungeonTimerWindow()
                if self.interface.wndDungeonTimer:
                    self.interface.wndDungeonTimer.RefreshDungeonFloor(Floor2)

        def BINARY_SetMissionMessage(self, message):
            self.interface.missionBoardNew.SetMission(message)

    if app.ENABLE_6TH_7TH_ATTR:
        def OpenAttr67AddDlg(self):
            if self.interface:
                self.interface.OpenAttr67AddDlg()

    def CloseShownWindows(self):
        if app.ENABLE_GLOBAL_RANKING:
            if self.rankingWindow:
                if self.rankingWindow.IsShow():
                    self.rankingWindow.Hide()
        if app.ENABLE_PM_ALL_SEND_SYSTEM:
            if self.whisperAdmin:
                if self.whisperAdmin.IsShow():
                    self.whisperAdmin.Hide()
        if app.ENABLE_DUNGEON_INFO:
            if self.wndBossTimer:
                if self.wndBossTimer.IsShow():
                    self.wndBossTimer.Hide()
        if app.ENABLE_BOT_CONTROL:
            if self.botControlWnd:
                if self.botControlWnd.IsShow():
                    self.botControlWnd.Constructor()
                    self.botControlWnd.Hide()
        if app.ENABLE_IN_GAME_LOG_SYSTEM:
            if self.wndInGameLog:
                if self.wndInGameLog.IsShow():
                    self.wndInGameLog.Hide()

        if self.targetBoard:
            if self.targetBoard.IsShow():
                self.targetBoard.Hide()

    if app.ENABLE_MINI_GAME_OKEY_NORMAL:
        ## MiniGame Rumi
        def BINARY_Cards_UpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
            self.interface.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)

        def BINARY_Cards_FieldUpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
            self.interface.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

        def BINARY_Cards_PutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
            self.interface.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

        def MiniGameStart(self, safemode):
            self.interface.OpenCardsWindow(safemode)

    if app.ENABLE_MINI_GAME_BNW:
        def BINARY_MinigameBnwStart(self):
            self.interface.MinigameBnwStart()

        def BINARY_MinigameBnwDrawResult(self, result, playerPoints, enemyPoints):
            self.interface.MinigameBnwSetResult(result, playerPoints, enemyPoints)

    if app.ENABLE_MINI_GAME_CATCH_KING:
        def MiniGameCatchKingEvent(self, isEnable):
            pass

        def MiniGameCatchKingEventStart(self, bigScore):
            self.interface.MiniGameCatchKingEventStart(bigScore)

        def MiniGameCatchKingSetHandCard(self, cardNumber):
            self.interface.MiniGameCatchKingSetHandCard(cardNumber)

        def MiniGameCatchKingResultField(self, score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear):
            self.interface.MiniGameCatchKingResultField(score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear)

        def MiniGameCatchKingSetEndCard(self, cardPos, cardNumber):
            self.interface.MiniGameCatchKingSetEndCard(cardPos, cardNumber)

        def MiniGameCatchKingReward(self, rewardCode):
            self.interface.MiniGameCatchKingReward(rewardCode)

    if app.ENABLE_MOVIEMODE_CAMERA:
        def __PressShiftKey(self):
            if not self.isFreeCamera:
                self.__SetQuickPageMode()
            else:
                self.AccelerateFreeCam(True)
                
        def __ReleaseShiftKey(self):
            if not self.isFreeCamera:
                self.__SetQuickSlotMode()
            else:
                self.freeCam['accelerate'] = 0

        def __PressCtrlKey(self):
            if not self.isFreeCamera:
                self.ShowMouseImage()
            else:
                self.AccelerateFreeCam(False)

        def __ReleaseCtrlKey(self):
            if not self.isFreeCamera:
                self.HideMouseImage()
            else:
                self.freeCam['accelerate'] = 0

        def __ToggleFreeCamera(self):
            if not chr.IsGameMaster(0):
                return

            if not self.isFreeCamera:
                app.SetFreeCamera()
                app.SetCameraSpeed(75)
                self.isFreeCamera = True
            else:
                app.SetCameraSpeed(100)
                self.isFreeCamera = False
                self.ResetFreeCam()
                app.SetDefaultCamera()

        def ResetFreeCam(self):
            self.freeCam = {'speed': 100, 'accelerate': 0, 'spVariation': 0, 'nextSpeedup': 0, 'inertia': 0}

        def AccelerateFreeCam(self, positive):
            if positive:
                var = 1
            else:
                var = -1

            if self.freeCam['spVariation'] != var:
                self.freeCam['inertia'] = self.freeCam['inertia'] * -1

            self.freeCam['accelerate'] = 1
            self.freeCam['spVariation'] = var

    def CloseAllWindowsByCommand(self):
        interface = self.interface

        if interface:
            if interface.wndCubeRenewal:
                interface.wndCubeRenewal.Close()
            if interface.dlgRefineNew:
                interface.dlgRefineNew.CancelRefine()

    def BINARY_BuyBackClear(self):
        if self.wndBuyBack:
            self.wndBuyBack.ClearItems()

    def BINARY_BuyBackAppend(self, logId, vnum, count, price, logType, sellDate, socketsStr, a0, a1, a2, a3, a4, a5, a6):
        if self.wndBuyBack:
            self.wndBuyBack.AppendItem(logId, vnum, count, price, logType, sellDate, socketsStr, a0, a1, a2, a3, a4, a5, a6)

    def BINARY_GmRestoreClear(self):
        if self.wndGmItemRestore:
            self.wndGmItemRestore.ClearItems()

    def BINARY_GmRestoreAppend(self, logId, pid, playerName, logType, vnum, count, price, sellDate, socketsStr, a0, a1, a2, a3, a4, a5, a6):
        if self.wndGmItemRestore:
            self.wndGmItemRestore.AppendItem(logId, pid, playerName, logType, vnum, count, price, sellDate, socketsStr, a0, a1, a2, a3, a4, a5, a6)

    def OpenBuyBackWindow(self):
        if self.wndBuyBack:
            if self.wndBuyBack.IsShow():
                self.wndBuyBack.Close()
            else:
                self.wndBuyBack.Open()

    def OpenGmItemRestoreWindow(self):
        if self.wndGmItemRestore:
            if self.wndGmItemRestore.IsShow():
                self.wndGmItemRestore.Close()
            else:
                self.wndGmItemRestore.Open()