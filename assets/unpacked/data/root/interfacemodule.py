import constInfo
import systemSetting
import wndMgr
import chat
import app
import player
import uiTaskBar
import uiCharacter
import uiInventory
import uiDragonSoul
import uiChat
import uiMessenger
import guild
import ui
import uiHelp
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uirefine
import uiEquipmentDialog
import uiGameButton
import uiTip
import net
# ACCESSORY_REFINE_ADD_METIN_STONE
import uiSelectItem
# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
import uiScriptLocale

import event
import localeInfo

if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import uiacce

if app.ENABLE_SPECIAL_STORAGE:
	import chr, uiSpecialInventory

if app.ENABLE_OFFLINE_SHOP:
	import  uiOfflineShop, uiShopSearch

if app.ENABLE_SWITCHBOT:
	import uiSwitchbot
if app.ENABLE_ITEM_TRANSACTIONS:
	import uiitemtransactions

if app.ENABLE_BIOLOG_SYSTEM:
	import uinewbiolog

import uiGameOptionNew

if app.ENABLE_DISTANCE_NPC:
	import uiDistanceNPC

if app.ENABLE_EVENT_MANAGER:
	import uiEventCalendarNew

if app.ENABLE_ITEMSHOP:
	import uiItemShopNew

if app.ENABLE_NEW_PET_SYSTEM:
	import uipetsystem

if app.ENABLE_AURA_SYSTEM:
	import uiaura

if app.ENABLE_WIKI:
	import uiWiki

if app.ENABLE_RENDER_TARGET:
	import uiRenderTarget

if app.ENABLE_VOTE4BUFF:
	import uiVote4Buff

if app.ENABLE_MAINTENANCE_SYSTEM:
	import uimaintenance

if app.ENABLE_EXTENDED_BATTLE_PASS:
	import uiBattlePassExtended

if app.ENABLE_FAST_SKILL_BOOK_SYSTEM:
	import uireadbook

if app.ENABLE_LEADERSHIP_EXTENSION:
	import uiPartyBonusDistribute

if app.ENABLE_DUNGEON_MODULES:
	import uiDungeonTimer

if app.ENABLE_6TH_7TH_ATTR:
	import uiAttr67Add

if app.ENABLE_LINK_IN_CHAT:
	import os

if app.ENABLE_BUFFI_SYSTEM:
	import uibuffisystem

if app.ENABLE_MINI_GAME_OKEY_NORMAL:
	import uiMiniGameRumi

if app.ENABLE_MINI_GAME_BNW:
	import uiminigameblacknwhite

if app.ENABLE_MINI_GAME_CATCH_KING:
	import uiMiniGameCatchKing

import item

IsQBHide = 0
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2
	wndGame = 0
	def __init__(self, gameWindow):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None
		self.wndGame = gameWindow

		# ITEM_MALL
		self.mallPageDlg = None
		# END_OF_ITEM_MALL

		self.wndWeb = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndExpandedTaskBar = None
		self.wndExpandedMoney = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.wndChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		self.wndGuildBuilding = None
		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			self.wndCubeRenewal = None
		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage = None

		if app.ENABLE_OFFLINE_SHOP:
			self.wndShopOffline = None
			self.wndShopSearch = None
			self.wndShopNotification = None

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.OnTopWindow = None
			self.dlgShop = None
			self.dlgExchange = None
			self.privateShopBuilder = None
			self.wndSafebox = None
			self.wndAcceCombine = None
			self.wndAcceAbsorption = None

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = None

		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		event.SetInterfaceWindow(self)

		if app.ENABLE_ITEM_TRANSACTIONS:
			self.wndItemTransactions = None

		if app.ENABLE_BIOLOG_SYSTEM:
			self.wndBiolog = None
		self.wndgameOption = None

		if app.ENABLE_ZODIAC_TEMPLE_CHAT:
			self.missionBoard = None

		if app.ENABLE_DUNGEON_MODULES:
			self.missionBoardNew = None
	
		if app.ENABLE_EVENT_MANAGER:
			self.wndEventManager = None
			self.wndEventIcon = None

		if app.ENABLE_FAST_SKILL_BOOK_SYSTEM:
			self.readBookWnd = None

		if app.ENABLE_BUFFI_SYSTEM:
			self.buffiWnd = None

		if app.ENABLE_ITEMSHOP:
			self.wndItemShop=None

		if app.ENABLE_WIKI:
			self.wndWiki = None

		if app.ENABLE_RENDER_TARGET:
			self.wndRenderTarget = None

		if app.ENABLE_VOTE4BUFF:
			self.wndVoteIcon = None

		if app.ENABLE_MAINTENANCE_SYSTEM:
			self.wndMaintenanceWindow = None

		if app.ENABLE_EXTENDED_BATTLE_PASS:
			self.wndBattlePassExtended = None
			self.isFirstOpeningExtBattlePass = False

		if app.ENABLE_LEADERSHIP_EXTENSION:
			self.wndPartyBonusWindow = None

		if app.ENABLE_DUNGEON_MODULES:
			self.wndDungeonTimer=None

		if app.ENABLE_LINK_IN_CHAT:
			self.OpenLinkQuestionDialog = None

		if app.ENABLE_MINI_GAME_CATCH_KING:
			self.wndCatchKingGame = None

		if app.ENABLE_CHANNEL_SWITCH_SYSTEM:
			self.moveChannelDlg = None

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeExpandMoney(self):
		self.wndExpandedMoney = uiTaskBar.ExpandedMoneyTaskBar()

	if app.ENABLE_ITEM_TRANSACTIONS:
		def __MakeItemTransactions(self):
			if self.wndItemTransactions:
				return
			self.wndItemTransactions = uiitemtransactions.ItemTransactions()
			self.wndItemTransactions.Hide()

	def __MakeChatWindow(self):

		wndChat = uiChat.ChatWindow()

		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))
		if app.ENABLE_STOP_CHAT:
			self.wndChat.SetStopChatEvent(ui.__mem_func__(self.StopChatButton))

		if app.ENABLE_AUTO_SHOUT:
			self.wndChat.SetAutoShoutEvent(ui.__mem_func__(self.AutoShoutButton))

	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND_MONEY, ui.__mem_func__(self.ToggleExpandedMoneyButton))

		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))
		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		self.wndEnergyBar = None
		import app
		if app.ENABLE_ENERGY_SYSTEM:
			wndEnergyBar = uiTaskBar.EnergyBar()
			wndEnergyBar.LoadWindow()
			self.wndEnergyBar = wndEnergyBar

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("HELP", ui.__mem_func__(self.__OnClickHelpButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))
		self.wndGameButton = wndGameButton

	def __MakeWindows(self):
		wndCharacter = uiCharacter.CharacterWindow()
		wndInventory = uiInventory.InventoryWindow()
		wndInventory.BindInterfaceClass(self)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			wndDragonSoul = uiDragonSoul.DragonSoulWindow()
			wndDragonSoul.BindInterfaceClass(self)
			wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()
		else:
			wndDragonSoul = None
			wndDragonSoulRefine = None

		wndMiniMap = uiMiniMap.MiniMap()
		wndMiniMap.BindInterface(self)
		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage = uiSpecialInventory.SpecialInventory()
			wndSafebox = uiSafebox.SafeboxWindow(self.wndSpecialStorage)
		else:
			wndSafebox = uiSafebox.SafeboxWindow()

		if app.ENABLE_LEADERSHIP_EXTENSION:
			self.wndPartyBonusWindow = uiPartyBonusDistribute.PartyBonusDistributeWindow()
			self.wndPartyBonusWindow = uiPartyBonusDistribute.PartyBonusDistributeWindow()

		wndSafebox.BindInterface(self)

		# ITEM_MALL
		if app.ENABLE_SPECIAL_STORAGE:
			wndMall = uiSafebox.MallWindow(self.wndSpecialStorage)
			self.wndSpecialStorage.BindInterfaceClass(self, wndSafebox, wndMall)
		else:
			wndMall = uiSafebox.MallWindow()
		self.wndMall = wndMall
		# END_OF_ITEM_MALL

		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)
		wndMall.BindInterface(self)
		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		self.wndDragonSoul = wndDragonSoul
		self.wndDragonSoulRefine = wndDragonSoulRefine
		self.wndMiniMap = wndMiniMap
		self.wndSafebox = wndSafebox
		self.wndMall = wndMall
		self.wndChatLog = wndChatLog

		if app.ENABLE_OFFLINE_SHOP:
			self.wndShopOffline = uiOfflineShop.OfflineShopWindow()
			self.wndShopOffline.Hide()

			self.wndShopSearch = uiShopSearch.ShopSearch()
			self.wndShopSearch.Hide()

			self.wndShopNotification = uiOfflineShop.SoldNotification()
			self.wndShopNotification.Hide()

		if app.ENABLE_BIOLOG_SYSTEM:
			self.wndBiolog = uinewbiolog.BiologWindow()
			self.wndBiolog.Hide()

		if app.ENABLE_FAST_SKILL_BOOK_SYSTEM:
			self.readBookWnd = uireadbook.ReadBookWindow()
			self.readBookWnd.Hide()

		if app.ENABLE_BUFFI_SYSTEM:
			self.buffiWnd = uibuffisystem.BuffiWindow()
			self.buffiWnd.Hide()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
			self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
			self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()

		if app.ENABLE_MINI_GAME_CATCH_KING:
			self.wndCatchKingGame = uiMiniGameCatchKing.MiniGameCatchKing()

		if app.ENABLE_FONT_SELECT:
			self.wndgameOption = uiGameOptionNew.GameOptionWindow()
		else:
			self.wndgameOption = None

		if app.ENABLE_DISTANCE_NPC:
			self.wndDistanceNPC = uiDistanceNPC.DistanceShoppingWindow()

		if app.ENABLE_WIKI:
			self.MakeWiki()

		if app.ENABLE_MAINTENANCE_SYSTEM:
			self.MakeMaintenanceWindows()

		if app.ENABLE_6TH_7TH_ATTR:
			self.wndAttr67Add = uiAttr67Add.Attr67AddWindow()
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.wndAttr67Add.BindInterface(self)
				self.wndAttr67Add.SetInven(self.wndInventory)
				self.wndInventory.BindWindow(self.wndAttr67Add)

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgExchange.BindInterface(self)
			self.dlgExchange.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgExchange)
			self.dlgExchange.SetDSInven(self.wndDragonSoul)
			self.wndDragonSoul.BindWindow(self.dlgExchange)
			
			if app.ENABLE_SPECIAL_STORAGE:
				self.dlgExchange.SetSpecialInven(self.wndSpecialStorage)
				self.wndSpecialStorage.BindWindow(self.dlgExchange)
		self.dlgExchange.Hide()

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		self.dlgShop.LoadDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgShop.BindInterface(self)
		self.dlgShop.Hide()

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.LoadDialog()
		self.dlgSystem.SetOpenHelpWindowEvent(ui.__mem_func__(self.OpenHelpWindow))
		self.dlgSystem.BindInterface(self)
		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		if app.ENABLE_DS_SET_BONUS:
			self.tooltipItem.BindInterface(self)
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.toolTipWhisper = uiToolTip.ToolTip()
		self.toolTipWhisper.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.privateShopBuilder.BindInterface(self)
		self.privateShopBuilder.Hide()

		self.dlgRefineNew = uirefine.RefineDialogNew()
		# self.dlgRefineNew.SetItemToolTip(self.tooltipItem)
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgRefineNew.BindInterface(self)
			self.dlgRefineNew.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgRefineNew)
		self.dlgRefineNew.Hide()

		if app.ENABLE_MINI_GAME_BNW:
			self.dlgMinigameBnw = uiminigameblacknwhite.BlackNWhiteGamePage()
			self.dlgMinigameBnw.Hide()

		if app.ENABLE_EXTENDED_BATTLE_PASS:
			self.wndBattlePassExtended = uiBattlePassExtended.BattlePassWindow()

		if app.ENABLE_NEW_PET_SYSTEM:
			self.wndPetWindow = uipetsystem.PetWindow()
			# self.wndPetWindow.SetItemToolTip(self.tooltipItem)
			self.wndPetWindow.Hide()

	def __MakeHelpWindow(self):
		self.wndHelp = uiHelp.HelpWindow()
		self.wndHelp.LoadDialog()
		self.wndHelp.SetCloseEvent(ui.__mem_func__(self.CloseHelpWindow))
		self.wndHelp.Hide()

	def __MakeTipBoard(self):
		# if app.__RENEWAL_NOTICE__:
		self.tipBoard = uiTip.TipBoardNew() if app.ENABLE_DUNGEON_MODULES else uiTip.TipBoard()
	# else:
		# self.tipBoard = uiTip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()

		if app.ENABLE_ZODIAC_TEMPLE_CHAT:
			self.missionBoard = uiTip.MissionBoard()
			self.missionBoard.Hide()

		if app.ENABLE_DUNGEON_MODULES:
			self.missionBoardNew = uiTip.MissionBoardNew()
			self.missionBoardNew.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __MakeAcceWindow(self):
			self.wndAcceCombine = uiacce.CombineWindow()
			self.wndAcceCombine.LoadWindow()
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.wndAcceCombine.BindInterface(self)
			self.wndAcceCombine.Hide()

			self.wndAcceAbsorption = uiacce.AbsorbWindow()
			self.wndAcceAbsorption.LoadWindow()
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.wndAcceAbsorption.BindInterface(self)
			self.wndAcceAbsorption.Hide()

			if self.wndInventory:
				self.wndInventory.SetAcceWindow(self.wndAcceCombine, self.wndAcceAbsorption)

	if app.ENABLE_AURA_SYSTEM:
		def __MakeAuraWindow(self):

			self.wndAuraRefine = uiaura.RefineWindow(self.wndInventory, self)
			self.wndAuraRefine.LoadWindow()
			self.wndAuraRefine.Hide()

			self.wndAuraAbsorption = uiaura.AbsorbWindow(self.wndInventory, self)
			self.wndAuraAbsorption.LoadWindow()
			self.wndAuraAbsorption.Hide()

			if self.wndInventory:
				self.wndInventory.SetAuraWindow(self.wndAuraAbsorption, self.wndAuraRefine)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiSelectItem.SelectItemWindow()
		self.wndItemSelect.Hide()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def __MakeCubeRenewal(self):
			import uicuberenewal
			self.wndCubeRenewal = uicuberenewal.CubeRenewalWindows()
			self.wndCubeRenewal.Hide()

	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
		def __MakeCardsInfoWindow(self):
			self.wndCardsInfo = uiMiniGameRumi.CardsInfoWindow()
			self.wndCardsInfo.LoadWindow()
			self.wndCardsInfo.Hide()

		def __MakeCardsWindow(self):
			self.wndCards = uiMiniGameRumi.CardsWindow()
			self.wndCards.LoadWindow()
			self.wndCards.Hide()

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeHelpWindow()
		self.__MakeTipBoard()
		self.__MakeWebWindow()
		self.__MakeExpandMoney()
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.__MakeAcceWindow()
		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			self.__MakeCubeRenewal()
		if app.ENABLE_ITEM_TRANSACTIONS:
			self.__MakeItemTransactions()
		if app.ENABLE_AURA_SYSTEM:
			self.__MakeAuraWindow()

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.__MakeItemSelectWindow()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			self.__MakeCardsInfoWindow()
			self.__MakeCardsWindow()

		if app.ENABLE_OFFLINE_SHOP:
			self.wndShopOffline.SetItemToolTip(self.tooltipItem)
			self.wndShopOffline.BindInterface(self)
			self.wndShopSearch.SetItemToolTip(self.tooltipItem)
			self.wndShopSearch.BindInterface(self)

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
			self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine.SetItemToolTip(self.tooltipItem)
			self.wndAcceAbsorption.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)

		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL


		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_BIOLOG_SYSTEM:
			self.wndBiolog.BindInterface(self)

		if app.ENABLE_AURA_SYSTEM:
			self.wndAuraAbsorption.SetItemToolTip(self.tooltipItem)
			self.wndAuraRefine.SetItemToolTip(self.tooltipItem)

		self.__InitWhisper()
		self.DRAGON_SOUL_IS_QUALIFIED = True

	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				if self.hyperlinkItemTooltip:
					self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
			elif "whisper" == type and app.ENABLE_CHAT_FLAG_AND_PM:
				if player.GetName() != str(tokens[1]):
					self.OpenWhisperDialog(str(tokens[1]))

			elif app.ENABLE_LINK_IN_CHAT and "web" == type and tokens[1].startswith("httpXxX") or "web" == type and tokens[1].startswith("httpsXxX"):
					OpenLinkQuestionDialog = uiCommon.QuestionDialog2()
					OpenLinkQuestionDialog.SetText1(localeInfo.CHAT_OPEN_LINK_DANGER)
					OpenLinkQuestionDialog.SetText2(localeInfo.CHAT_OPEN_LINK)
					OpenLinkQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerOpenLink(arg))
					OpenLinkQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerOpenLink(arg))
					constInfo.link = "start " + tokens[1].replace("XxX", "://").replace("&","^&")
					OpenLinkQuestionDialog.Open()
					self.OpenLinkQuestionDialog = OpenLinkQuestionDialog
			elif app.ENABLE_LINK_IN_CHAT and "sysweb" == type:
				os.system("start " + tokens[1].replace("XxX", "://"))

			elif app.ENABLE_WIKI and type == "wiki":
				self.MakeWiki()
				self.wndWiki.RunHistoryArgument(str(tokens[1]))
				self.wndWiki.Open()


	if app.ENABLE_LINK_IN_CHAT:
		def AnswerOpenLink(self, answer):
			if not self.OpenLinkQuestionDialog:
				return

			self.OpenLinkQuestionDialog.Close()
			self.OpenLinkQuestionDialog = None

			if not answer:
				return

			link = constInfo.link
			os.system(link)

	## Make Windows & Dialogs
	################################

	def Close(self):
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()
			# if uiQuest.QuestDialog.QuestCurtain.IsShow():
			# 	uiQuest.QuestDialog.QuestCurtain.Hide() # Ghost gui fixed? lightwork correction

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if self.wndChat:
			self.wndChat.Hide()
			self.wndChat.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Hide()
			self.wndTaskBar.Destroy()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()
			self.wndExpandedTaskBar.Destroy()

		if self.wndExpandedMoney:
			self.wndExpandedMoney.Hide()
			self.wndExpandedMoney.Destroy()

		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()
			self.wndEnergyBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Close()
			self.wndCharacter.Hide()
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Hide()
			self.wndInventory.Destroy()

		if self.wndDragonSoul:
			self.wndDragonSoul.Close()
			self.wndDragonSoul.Hide()
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Close()
			self.wndDragonSoulRefine.Hide()
			self.wndDragonSoulRefine.Destroy()

		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			if self.wndCardsInfo:
				self.wndCardsInfo.Hide()
				self.wndCardsInfo.Destroy()

			if self.wndCards:
				self.wndCards.Hide()
				self.wndCards.Destroy()

		if self.dlgExchange:
			# self.dlgExchange.CloseDialog()
			self.dlgExchange.Hide()
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Hide()
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			# self.dlgShop.Close()
			self.dlgShop.Hide()
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Hide()
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Hide()
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Hide()
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Hide()
			self.wndSafebox.Destroy()

		if self.wndWeb:
			self.wndWeb.Hide()
			self.wndWeb.Destroy()
			del self.wndWeb

		if self.wndMall:
			self.wndMall.Hide()
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Hide()
			self.wndParty.Destroy()

		if self.wndHelp:
			self.wndHelp.Close()
			self.wndHelp.Hide()
			self.wndHelp.Destroy()

		if app.ENABLE_ACCE_COSTUME_SYSTEM and self.wndAcceCombine:
			# self.wndAcceCombine.Close()
			self.wndAcceCombine.Hide()
			self.wndAcceCombine.Destroy()

		if app.ENABLE_ACCE_COSTUME_SYSTEM and self.wndAcceAbsorption:
			# self.wndAcceAbsorption.Close()
			self.wndAcceAbsorption.Hide()
			self.wndAcceAbsorption.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Hide()
			self.wndMessenger.Destroy()

		if self.wndGuild:
			# self.wndGuild.Close()
			self.wndGuild.Hide()
			self.wndGuild.Destroy()

		if self.privateShopBuilder:
			# self.privateShopBuilder.Close()
			self.privateShopBuilder.Hide()
			self.privateShopBuilder.Destroy()

		if self.dlgRefineNew:
			# self.dlgRefineNew.Close()
			self.dlgRefineNew.Hide()
			self.dlgRefineNew.Destroy()

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Hide()
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Hide()
			self.wndGameButton.Destroy()

		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Hide()
			self.mallPageDlg.Destroy()
		# END_OF_ITEM_MALL

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Close()
			self.wndItemSelect.Hide()
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			if self.wndCubeRenewal:
				self.wndCubeRenewal.Close()
				self.wndCubeRenewal.Hide()
				self.wndCubeRenewal.Destroy()

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.Hide()
				self.wndSpecialStorage.Destroy()

		if app.ENABLE_OFFLINE_SHOP:
			if self.wndShopOffline:
				# self.wndShopOffline.Close()
				self.wndShopOffline.Hide()
				self.wndShopOffline.Destroy()
				del self.wndShopOffline	

			if self.wndShopSearch:
				# self.wndShopSearch.Close()
				self.wndShopSearch.Hide()
				self.wndShopSearch.Destroy()
				del self.wndShopSearch

			if self.wndShopNotification:
				# self.wndShopNotification.Close()
				self.wndShopNotification.Hide()
				self.wndShopNotification.Destroy()
				del self.wndShopNotification

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Close()
				self.wndSwitchbot.Hide()
				self.wndSwitchbot.Destroy()
				del self.wndSwitchbot

		if app.ENABLE_ITEM_TRANSACTIONS:
			if self.wndItemTransactions:
				self.wndItemTransactions.Close()
				self.wndItemTransactions.Hide()
				self.wndItemTransactions.Destroy()
				del self.wndItemTransactions

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndBiolog:
				self.wndBiolog.Close()
				self.wndBiolog.Hide()
				self.wndBiolog.Destroy()
				del self.wndBiolog

		if app.ENABLE_MINI_GAME_BNW:
			if self.dlgMinigameBnw:
				self.dlgMinigameBnw.Hide()
				self.dlgMinigameBnw.Destroy()
				del self.dlgMinigameBnw

		if self.wndgameOption:
			self.wndgameOption.Hide() ## Lightwork correction@222
			self.wndgameOption.Destroy()
			del self.wndgameOption

		if app.ENABLE_DISTANCE_NPC and self.wndDistanceNPC:
			self.wndDistanceNPC.Hide()
			self.wndDistanceNPC.Destroy()
			del self.wndDistanceNPC

		if app.ENABLE_EVENT_MANAGER:
			if self.wndEventManager:
				self.wndEventManager.Hide()
				self.wndEventManager.Destroy()
				del self.wndEventManager

			if self.wndEventIcon:
				self.wndEventIcon.Hide()
				self.wndEventIcon.Destroy()
				del self.wndEventIcon

		if app.ENABLE_ITEMSHOP:
			if self.wndItemShop:
				self.wndItemShop.Hide()
				self.wndItemShop.Destroy()
				del self.wndItemShop

		if app.ENABLE_NEW_PET_SYSTEM:
			if self.wndPetWindow:
				self.wndPetWindow.Close()
				self.wndPetWindow.Hide()
				self.wndPetWindow.Destroy()
				del self.wndPetWindow

		if app.ENABLE_AURA_SYSTEM:
			if self.wndAuraAbsorption:
				self.wndAuraAbsorption.Close()
				self.wndAuraAbsorption.Hide()
				self.wndAuraAbsorption.Destroy()
				del self.wndAuraAbsorption

			if self.wndAuraRefine:
				self.wndAuraRefine.Close()
				self.wndAuraRefine.Hide()
				self.wndAuraRefine.Destroy()
				del self.wndAuraRefine

		if app.ENABLE_WIKI:
			if self.wndWiki:
				self.wndWiki.Close()
				self.wndWiki.Hide()
				self.wndWiki.Destroy()
				del self.wndWiki

		if app.ENABLE_RENDER_TARGET:
			if self.wndRenderTarget:
				self.wndRenderTarget.Close()
				self.wndRenderTarget.Hide()
				self.wndRenderTarget.Destroy()
				del self.wndRenderTarget

		if app.ENABLE_VOTE4BUFF:
			if self.wndVoteIcon:
				self.wndVoteIcon.Hide()
				self.wndVoteIcon.Destroy()
				del self.wndVoteIcon

		if app.ENABLE_MAINTENANCE_SYSTEM:
			if self.wndMaintenanceWindow:
				self.wndMaintenanceWindow.Hide()
				self.wndMaintenanceWindow.Destroy()
				del self.wndMaintenanceWindow

		if app.ENABLE_EXTENDED_BATTLE_PASS:
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.Close()
				self.wndBattlePassExtended.Hide()
				self.wndBattlePassExtended.sidebar.Hide()

				self.wndBattlePassExtended.Destroy()
				del self.wndBattlePassExtended

		if app.ENABLE_FAST_SKILL_BOOK_SYSTEM and self.readBookWnd:
			self.readBookWnd.Close()
			self.readBookWnd.Hide()
			self.readBookWnd.Destroy()
			del self.readBookWnd

		if app.ENABLE_BUFFI_SYSTEM and self.buffiWnd:
			self.buffiWnd.Close()
			self.buffiWnd.Hide()
			self.buffiWnd.Destroy()
			del self.buffiWnd

		if app.ENABLE_MINI_GAME_CATCH_KING:
			if self.wndCatchKingGame:
				self.wndCatchKingGame.Close()
				self.wndCatchKingGame.Hide()
				self.wndCatchKingGame.Destroy()
				del self.wndCatchKingGame

		if app.ENABLE_LEADERSHIP_EXTENSION:
			if self.wndPartyBonusWindow:
				self.wndPartyBonusWindow.Hide()
				self.wndPartyBonusWindow.Destroy()
				del self.wndPartyBonusWindow

		if app.ENABLE_DUNGEON_MODULES:
			if self.wndDungeonTimer:
				self.wndDungeonTimer.Close()
				self.wndDungeonTimer.Hide()
				del self.wndDungeonTimer

		if app.ENABLE_6TH_7TH_ATTR:
			if self.wndAttr67Add:
				# self.wndAttr67Add.Close()
				self.wndAttr67Add.Hide()
				del self.wndAttr67Add

		if app.ENABLE_CHANNEL_SWITCH_SYSTEM:
			if self.moveChannelDlg:
				self.moveChannelDlg.Hide()
				self.moveChannelDlg.Destroy()
				del self.moveChannelDlg

		self.wndChatLog.Destroy()

		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()

		del self.mallPageDlg
		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.wndTaskBar
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar
		del self.wndEnergyBar
		del self.wndCharacter
		del self.wndInventory
		del self.wndExpandedMoney
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.toolTipWhisper
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndHelp
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		del self.wndItemSelect
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			del self.wndAcceCombine
			del self.wndAcceAbsorption
		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			del self.wndCubeRenewal
		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndSpecialStorage:
				del self.wndSpecialStorage
		if app.ENABLE_ZODIAC_TEMPLE_CHAT:
			del self.missionBoard
		if app.ENABLE_DUNGEON_MODULES:
			del self.missionBoardNew
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			del self.wndCardsInfo
			del self.wndCards

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()

	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshStatus()
		self.wndExpandedMoney.RefreshStatus()

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshItemSlot()
		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage.RefreshItemSlot()

	def RefreshCharacter(self):
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()
		if app.ENABLE_INVENTORY_REWORK and self.wndExpandedMoney:
			self.wndExpandedMoney.Show()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):
		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()

		if skin:
			q.Lock()
			wnds = self.HideWindowsBeforeWarp()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda obj, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

			q.AddOnCloseEvent(q.Unlock)

		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))

		self.wndQuestWindow[self.wndQuestWindowNewKey] = q
		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE

	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	if app.ENABLE_EXCHANGE_WINDOW_RENEWAL:
		def AddItemToExchangeMsg(self, link, player, count):
			self.dlgExchange.AddItemToExchangeMsg(link, player, count)
		
		def AddYangToExchangeMsg(self, yang, player):
			self.dlgExchange.AddYangToExchangeMsg(yang, player)

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	## Party
	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)

		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()

		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	## Safebox
	def AskSafeboxPassword(self):
		if app.ENABLE_SPECIAL_STORAGE:
			return

		if self.wndSafebox.IsShow():
			return

		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage.ShowSafeboxWindow(size)
			return

		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()

	def CommandCloseSafebox(self):
		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage.CommandCloseSafebox()
		else:
			self.wndSafebox.CommandCloseSafebox()

	def AskMallPassword(self):
		if app.ENABLE_SPECIAL_STORAGE:
			return

		if self.wndMall.IsShow():
			return

		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage.ShowMallWindow(size)
			return

		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage.CommandCloseMall()
		else:
			self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
		if not self.guildScoreBoardDict.has_key(key):
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):

		if self.IsAnyWindowOpen():
			self.dlgRefineNew.CancelRefine()
			return

		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	if app.ENABLE_REFINE_RENEWAL:
		def CheckRefineDialog(self, isFail):
			self.dlgRefineNew.CheckRefine(isFail)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	if app.ENABLE_SPECIAL_STORAGE:
		def ToggleSpecialStorageWindow(self):
			if not player.IsObserverMode():
				if not self.wndSpecialStorage.IsShow():
					self.wndSpecialStorage.Show()
				else:
					self.wndSpecialStorage.Close()

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Show()
			self.wndDragonSoulRefine.Show()
		self.wndChat.Show()
		self.wndMiniMap.Show()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()
		if app.ENABLE_INVENTORY_REWORK and self.wndExpandedMoney:
			self.wndExpandedMoney.Show()

	def HideAllWindows(self):
		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()

		if self.wndCharacter:
			self.wndCharacter.Close()

		if self.wndInventory:
			self.wndInventory.Hide()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Hide()
			self.wndDragonSoulRefine.Hide()

		if self.wndChat:
			self.wndChat.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.Close()

		if self.wndExpandedMoney:
			self.wndExpandedMoney.Hide()

		if app.ENABLE_EXTENDED_BATTLE_PASS:
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.Hide()
				self.wndBattlePassExtended.sidebar.Hide()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleExpandedMoneyButton(self):
		if self.wndExpandedMoney.IsShow():
			self.wndExpandedMoney.Close()
		else:
			self.wndExpandedMoney.Open()

	def ToggleChat(self):
		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			if self.wndWeb:
				if not self.wndWeb.IsShow():
					self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	def OpenRestartDialog(self):
		self.dlgRestart.OpenDialog()
		self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if not self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == player.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					self.wndCharacter.Close()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def ToggleInventoryWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
				if app.ENABLE_INVENTORY_REWORK and self.wndExpandedMoney:
					self.wndExpandedMoney.Show()
				if app.ENABLE_SPECIAL_STORAGE:
					if constInfo.SpecialInventoryMode == 1:
						constInfo.IsSpecialInventoryOpen=1
						self.wndSpecialStorage.Show()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()
				if app.ENABLE_SPECIAL_STORAGE:
					if constInfo.SpecialInventoryMode == 1:
						constInfo.IsSpecialInventoryOpen=0
						self.wndSpecialStorage.Close()

	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()

	def DragonSoulActivate(self, deck):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	if app.ENABLE_DS_SET_BONUS:
		def DragonSoulSetGrade(self, grade):
			self.wndDragonSoul.SetDSSetGrade(grade)

	def DragonSoulDeactivate(self):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.DeactivateDragonSoul()

	def Highligt_Item(self, inven_type, inven_pos):
		if player.DRAGON_SOUL_INVENTORY == inven_type:
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				self.wndDragonSoul.HighlightSlot(inven_pos)

		elif app.ENABLE_HIGHLIGHT_SYSTEM and player.SLOT_TYPE_INVENTORY == inven_type:
			self.wndInventory.HighlightSlot(inven_pos)
		elif app.ENABLE_HIGHLIGHT_SYSTEM and inven_type in [ player.UPGRADE_INVENTORY, player.BOOK_INVENTORY, player.STONE_INVENTORY, player.CHEST_INVENTORY ]:
			self.wndSpecialStorage.HighlightSlot(inven_pos, inven_type)

	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True
		if (self.wndExpandedTaskBar): # none fixed
			self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, uiScriptLocale.TASKBAR_DRAGON_SOUL)

	def ToggleDragonSoulWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
					else:
						try:
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.Open()
						except:
							self.wndPopupDialog = uiCommon.PopupDialog()
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.Open()
				else:
					self.wndDragonSoul.Close()

	def ToggleDragonSoulWindowWithNoInfo(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
				else:
					self.wndDragonSoul.Close()

	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	def OpenDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Show()
					if None != self.wndDragonSoul:
						if False == self.wndDragonSoul.IsShow():
							self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Close()

	def ToggleGuildWindow(self):
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	if app.ENABLE_STOP_CHAT:
		def StopChatButton(self):
			import net
			net.SendChatPacket("/set_char_settings {}".format(player.SETTINGS_STOP_CHAT))

	if app.ENABLE_STOP_CHAT:
		def AutoShoutButton(self):
			if not chr.IsPremium():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_SEARCH_PREMIUM_NEEDED_FOR_THIS_ACTION)
				return

			if constInfo.AUTO_SHOUT_ACTIVATED:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_SHOUT_INFO2)
				constInfo.AUTO_SHOUT_ACTIVATED = 0
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_SHOUT_INFO)
				constInfo.AUTO_SHOUT_ACTIVATED = 1
				if constInfo.LAST_SHOUT_MESSAGE == "":
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AUTO_SHOUT_INFO3)

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __OnClickHelpButton(self):
		player.SetPlayTime(1)
		self.CheckGameButton()
		self.OpenHelpWindow()

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	def OpenHelpWindow(self):
		self.wndUICurtain.Show()
		self.wndHelp.Open()

	def CloseHelpWindow(self):
		self.wndUICurtain.Hide()
		self.wndHelp.Close()

	def OpenWebWindow(self, url):
		self.wndWeb.Open(url)
		self.wndChat.CloseChat()

	def CloseWbWindow(self):
		self.wndWeb.Close()

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			self.wndCubeRenewal.Show()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			board = (self.wndAcceAbsorption,self.wndAcceCombine)[int(bWindow)]
			if iAct == 1:
				self.ActAcceOpen(board)
			elif iAct == 2:
				self.ActAcceClose(board)
			elif iAct == 3 or iAct == 4:
				self.ActAcceRefresh(board, iAct)

		def ActAcceOpen(self,board):
			if not board.IsOpened():
				board.Open()
			if not self.wndInventory.IsShow():
				self.wndInventory.Show()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceClose(self,board):
			if board.IsOpened():
				board.Close()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceRefresh(self,board,iAct):
			if board.IsOpened():
				board.Refresh(iAct)
			self.wndInventory.RefreshBagSlotWindow()

	def HideWindowsBeforeWarp(self):

		hideWindows = self.wndTaskBar,\
						self.wndInventory,\
						self.wndExpandedMoney,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			hideWindows += self.wndDragonSoul,\
						self.wndDragonSoulRefine,

		showWndList = filter(lambda x:x.IsShow(), hideWindows)

		hideWindows +=self.wndCharacter,

		hideWindows +=self.wndMiniMap.AtlasWindow,

		if app.ENABLE_SWITCHBOT and self.wndSwitchbot:
			hideWindows += self.wndSwitchbot,

		if app.ENABLE_ITEM_TRANSACTIONS and self.wndItemTransactions:
			hideWindows += self.wndItemTransactions,

		if app.ENABLE_EXTENDED_BATTLE_PASS:
			if self.wndBattlePassExtended:
				hideWindows += self.wndBattlePassExtended,
				hideWindows += self.wndBattlePassExtended.sidebar,

		if app.ENABLE_LEADERSHIP_EXTENSION:
			if self.wndPartyBonusWindow:
				hideWindows += self.wndPartyBonusWindow,

		if app.ENABLE_DISTANCE_NPC:
			if self.wndDistanceNPC:
				hideWindows += self.wndDistanceNPC,

		# if app.ENABLE_DISTANCE_NPC:
		if self.wndgameOption:
			hideWindows += self.wndgameOption,

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndBiolog:
				hideWindows += self.wndBiolog,

		if app.ENABLE_ITEM_TRANSACTIONS:
			if self.wndItemTransactions:
				hideWindows += self.wndItemTransactions,

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndDistanceNPC:
				hideWindows += self.wndSpecialStorage,

		if app.ENABLE_OFFLINE_SHOP:
			if self.wndShopOffline:
				hideWindows += self.wndShopOffline,
			if self.wndShopSearch:
				hideWindows += self.wndShopSearch,
			if self.wndShopNotification:
				hideWindows += self.wndShopNotification,

		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.dlgShop:
				hideWindows += self.dlgShop,
			if self.dlgExchange:
				hideWindows += self.dlgExchange,
			if self.privateShopBuilder:
				hideWindows += self.privateShopBuilder,
			if self.wndSafebox:
				hideWindows += self.wndSafebox,
			if self.wndAcceCombine:
				hideWindows += self.wndAcceCombine,
			if self.wndAcceAbsorption:
				hideWindows += self.wndAcceAbsorption,

		if app.ENABLE_EVENT_MANAGER:
			if self.wndEventManager:
				hideWindows += self.wndEventManager,

		if app.ENABLE_FAST_SKILL_BOOK_SYSTEM:
			if self.readBookWnd:
				hideWindows += self.readBookWnd,
				hideWindows += self.readBookWnd.sidebar,

		if app.ENABLE_BUFFI_SYSTEM:
			if self.buffiWnd:
				hideWindows += self.buffiWnd,

		if app.ENABLE_WIKI:
			if self.wndWiki:
				hideWindows += self.wndWiki,

		if app.ENABLE_RENDER_TARGET:
			if self.wndRenderTarget:
				hideWindows += self.wndRenderTarget,

		if app.ENABLE_EXTENDED_BATTLE_PASS:
			if self.wndBattlePassExtended:
				hideWindows += self.wndBattlePassExtended,
				hideWindows += self.wndBattlePassExtended.sidebar,

		if app.ENABLE_LEADERSHIP_EXTENSION:
			if self.wndPartyBonusWindow:
				hideWindows += self.wndPartyBonusWindow,

		if app.ENABLE_NEW_PET_SYSTEM:
			if self.wndPetWindow:
				hideWindows += self.wndPetWindow,

		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			if self.wndCardsInfo:
				hideWindows += self.wndCardsInfo,			
			if self.wndCards:
				hideWindows += self.wndCards,

		if app.ENABLE_MINI_GAME_CATCH_KING:
			if self.wndCatchKingGame:
				hideWindows += self.wndCatchKingGame,

		if app.ENABLE_MINI_GAME_BNW:
			if self.dlgMinigameBnw:
				hideWindows += self.dlgMinigameBnw,

		if app.ENABLE_CHANNEL_SWITCH_SYSTEM:
			if self.moveChannelDlg:
				hideWindows += self.moveChannelDlg,

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)

		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			if self.wndCubeRenewal:
				if self.wndCubeRenewal.IsShow():
					self.wndCubeRenewal.Close()

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		constInfo.GetGameInstance().CloseShownWindows()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return showWndList

	def __ShowWindows(self, wnds):
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	#####################################################################################
	### Private Shop ###

	def OpenPrivateShopInputNameDialog(self):
		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenPrivateShopBuilder(self):

		if not self.inputDialog:
			return True

		if not len(self.inputDialog.GetText()):
			return True

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return True

	def AppearPrivateShop(self, vid, text):

		board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)
		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):

		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	#####################################################################################
	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	#####################################################################################

	#####################################################################################
	### Quest ###
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		if "item"==iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName

		if iconName and (iconType not in ("item", "file")): # type "ex" implied
			btn.SetUpVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName.replace("open", "close")))
			btn.SetOverVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
			btn.SetDownVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
		else:
			if localeInfo.IsEUROPE():
				btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
				btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
				btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
		# END_OF_QUEST_LETTER_IMAGE

		if not app.ENABLE_QUEST_CATEGORY:
			btn.SetToolTipText(name, -20, 35)
			btn.ToolTipText.SetHorizontalAlignLeft()

			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			btn.Show()
		else:
			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

	def __ArrangeQuestButton(self):
		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()
		
		if self.wndParty and player.IsPartyMember(player.GetMainCharacterIndex()) != 0:
			xPos = 100 + 30
		else:
			xPos = 20

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:
			if app.ENABLE_QUEST_CATEGORY:
				btn.SetToolTipText(str(len(self.questButtonList)))
				btn.ToolTipText.SetHorizontalAlignCenter()

			btn.SetPosition(xPos, yPos + (count%yCount * 63))

			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				if app.ENABLE_QUEST_CATEGORY and count > 0:
					btn.Hide()
				else:
					btn.Show()
			
			count += 1

	def __StartQuest(self, btn):
		if app.ENABLE_QUEST_CATEGORY:
			self.__OnClickQuestButton()
			self.HideAllQuestButton()
		else:
			event.QuestButtonClick(btn.index)
			self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
			if app.ENABLE_QUEST_CATEGORY:
				break
	#####################################################################################

	#####################################################################################
	### Whisper ###

	def __InitWhisper(self):
		chat.InitWhisper(self)

	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	if app.ENABLE_EXTENDED_WHISPER_DETAILS and app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def RecieveWhisperDetails(self, name, country):
			if self.whisperDialogDict.has_key(name):
				self.whisperDialogDict[name].SetCountryFlag(country)
			else:
				btn = self.__FindWhisperButton(name)
				if btn != 0:
					btn.countryID = country

	def OpenWhisperDialog(self, name):
		if not self.whisperDialogDict.has_key(name):
			dlg = self.__MakeWhisperDialog(name)
			dlg.OpenWithTarget(name)
			dlg.chatLine.SetFocus()
			dlg.Show()

			self.__CheckGameMaster(name)
			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

	def RecvWhisper(self, name):
		if not self.whisperDialogDict.has_key(name):
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()
				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))
			else:
				btn.Flash()

		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	def ShowWhisperDialog(self, btn):
		try:
			if app.IsPressed(app.DIK_LCONTROL):
				self.__DestroyWhisperButton(btn)
				self.__HideToolTipButton()
				return
			else:
				self.__MakeWhisperDialog(btn.name)
				dlgWhisper = self.whisperDialogDict[btn.name]
				dlgWhisper.OpenWithTarget(btn.name)
				dlgWhisper.Show()
				self.__CheckGameMaster(btn.name)
				self.__HideToolTipButton()
		except:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

		self.__DestroyWhisperButton(btn)

	def MinimizeWhisperDialog(self, name):

		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None
			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()
		whisperButton.SetUpVisual("d:/ymir work/ui/design_new/buttons/message.tga")
		whisperButton.SetOverVisual("d:/ymir work/ui/design_new/buttons/message.tga")
		whisperButton.SetDownVisual("d:/ymir work/ui/design_new/buttons/message.tga")

		whisperButton.ShowToolTip = lambda arg=localeInfo.BUTTON_TOOLTIP_WHISPER_CLOSE: self.__ShowToolTipButton(arg)
		whisperButton.HideToolTip = lambda arg=localeInfo.BUTTON_TOOLTIP_WHISPER_CLOSE: self.__HideToolTipButton()

		if self.IsGameMasterName(name):
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		else:
			whisperButton.SetToolTipText(name)

		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SAFE_SetEvent(self.ShowWhisperDialog, whisperButton)
		whisperButton.Show()
		whisperButton.name = name
	
		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()
		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()
		self.__HideToolTipButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return True
		else:
			return False

	#####################################################################################

	#####################################################################################
	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.HideWindowsBeforeWarp()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return True
		# END_OF_GUILD_BUILDING
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()

	#####################################################################################

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def GetInventoryPageIndex(self):
		if self.wndInventory:
			return self.wndInventory.GetInventoryPageIndex()
		else:
			return -1

	def EmptyFunction(self):
		pass

	if constInfo.ENABLE_DSS_ACTIVE_EFFECT_BUTTON:
		def UseDSSButtonEffect(self, enable):
			if self.wndInventory:
				self.wndInventory.UseDSSButtonEffect(enable)

	if app.ENABLE_DROP_DIALOG_EXTENDED_SYSTEM:
		def DeleteItem(self, slotPos, invenType):
			if app.ENABLE_OFFLINE_SHOP:
				if uiOfflineShop.IsBuildingShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_DOING_PRIVATE_SHOP_OPEN)
					return
			if self.wndInventory:
				self.wndInventory.DeleteItem(slotPos, invenType)

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetCantMouseSlot(self, slot, invenType):
			if invenType == player.INVENTORY:
				if self.wndInventory:
					self.wndInventory.SetCantMouseSlot(slot)
					self.RefreshMarkInventoryBag()
			
			if invenType == player.DRAGON_SOUL_INVENTORY:
				if self.wndDragonSoul:
					self.wndDragonSoul.SetCantMouseSlot(slot)
					self.RefreshMarkInventoryBag()
			
			if app.ENABLE_SPECIAL_STORAGE:
				if invenType in (player.UPGRADE_INVENTORY, player.BOOK_INVENTORY, player.STONE_INVENTORY, player.CHEST_INVENTORY):
					if self.wndSpecialStorage:
						self.wndSpecialStorage.SetCantMouseSlot(slot, invenType)
						self.RefreshMarkInventoryBag()
				
		def SetCanMouseSlot(self, slot, invenType):
			if invenType == player.INVENTORY:
				if self.wndInventory:		
					self.wndInventory.SetCanMouseSlot(slot)
					self.RefreshMarkInventoryBag()
			
			if invenType == player.DRAGON_SOUL_INVENTORY:
				if self.wndDragonSoul:
					self.wndDragonSoul.SetCanMouseSlot(slot)
					self.RefreshMarkInventoryBag()
			
			if app.ENABLE_SPECIAL_STORAGE:
				if invenType == player.UPGRADE_INVENTORY or invenType == player.BOOK_INVENTORY or invenType == player.STONE_INVENTORY or invenType == player.CHEST_INVENTORY:
					if self.wndSpecialStorage:
						self.wndSpecialStorage.SetCanMouseSlot(slot, invenType)
						self.RefreshMarkInventoryBag()
				
		def MouseSlotEventClear(self):
			if self.wndInventory:
				self.wndInventory.MouseSlotEventClear()
				self.RefreshMarkInventoryBag()
			
			if self.wndDragonSoul:
				self.wndDragonSoul.MouseSlotEventClear()
				self.RefreshMarkInventoryBag()
			
			if app.ENABLE_SPECIAL_STORAGE:
				if self.wndSpecialStorage:
					self.wndSpecialStorage.MouseSlotEventClear()
					self.RefreshMarkInventoryBag()
		
		def MarkUnusableInvenSlotOnTopWnd(self, onTopWnd, InvenSlot, InvenType):
			if onTopWnd == player.ON_TOP_WND_SHOP and self.dlgShop and self.dlgShop.CantSellInvenItem(InvenSlot, InvenType):
				return True
			if onTopWnd == player.ON_TOP_WND_SHOP and self.wndItemTransactions and self.wndItemTransactions.CantSellInvenItem(InvenSlot, InvenType):
				return True
			elif onTopWnd == player.ON_TOP_WND_EXCHANGE and self.dlgExchange and self.dlgExchange.CantTradableItem(InvenSlot, InvenType):
				return True
			elif onTopWnd == player.ON_TOP_WND_SAFEBOX and self.wndSafebox and self.wndSafebox.CantCheckInItem(InvenSlot, InvenType):
				return True
			elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP and self.privateShopBuilder and self.privateShopBuilder.CantTradableItem(InvenSlot, InvenType):
				return True
			elif onTopWnd == player.ON_TOP_WND_ACCE_COMBINE and self.wndAcceCombine and self.wndAcceCombine.CantCheckInItem(InvenSlot, InvenType):
				return True
			elif onTopWnd == player.ON_TOP_WND_ACCE_ABSORB and self.wndAcceAbsorption and self.wndAcceAbsorption.CantCheckInItem(InvenSlot, InvenType):
				return True
			elif onTopWnd == player.ON_TOP_WND_DICE and self.dlgDice and self.dlgDice.CantTradableItem(InvenSlot, InvenType):
				return True
			elif onTopWnd == player.ON_TOP_WND_DRAGON_SOUL and self.wndDragonSoul and self.wndDragonSoul.CantTradableItem(InvenSlot, InvenType):
				return True
			elif onTopWnd == player.ON_TOP_WND_OFFLINE_SHOP and self.wndShopOffline and self.wndShopOffline.CantTradableItem(InvenSlot, InvenType):
				return True
							
			return False
		
		def CantTradableItemExchangeFromInventory(self, dstSlotIndex, srcSlotIndex):
			onTopWnd = self.GetOnTopWindow()
			
			if onTopWnd == player.ON_TOP_WND_EXCHANGE:
				self.dlgExchange.CantTradableItemFromInventory(dstSlotIndex, srcSlotIndex)
			else:
				self.dlgDice.CantTradableItemFromInventory(dstSlotIndex, srcSlotIndex)
		
		def CantTradableItemExchangeFromDragonSoul(self, dstSlotIndex, srcSlotIndex):
			onTopWnd = self.GetOnTopWindow()
			
			if onTopWnd == player.ON_TOP_WND_EXCHANGE:
				self.dlgExchange.CantTradableItemFromDragonSoul(dstSlotIndex, srcSlotIndex)

		if app.ENABLE_SPECIAL_STORAGE:
			def CantTradableItemExchangeFromStorage(self, dstSlotIndex, srcSlotIndex, invenType):
				onTopWnd = self.GetOnTopWindow()
				
				if onTopWnd == player.ON_TOP_WND_EXCHANGE:
					self.dlgExchange.CantTradableItemFromStorage(dstSlotIndex, srcSlotIndex, invenType)

		def SetOnTopWindow(self, onTopWnd):
			self.OnTopWindow = onTopWnd
			
		def GetOnTopWindow(self):
			return self.OnTopWindow
		
		def RefreshMarkInventoryBag(self):
			self.wndInventory.RefreshBagSlotWindow()
			self.wndDragonSoul.RefreshBagSlotWindow()
				
			if app.ENABLE_SPECIAL_STORAGE:
				self.wndSpecialStorage.RefreshBagSlotWindow()

	if app.ENABLE_CHECKINOUT_UPDATE:
		def AttachItemFromSafebox(self, slotIndex, itemIndex, wnd):
			if wnd == 0 and self.wndInventory and self.wndInventory.IsShow():
				self.wndInventory.AttachItemFromSafebox(slotIndex, itemIndex)

			return True

		def AttachInvenItemToOtherWindowSlot(self, slotWindow, slotIndex):
			if self.wndSafebox and self.wndSafebox.IsShow() and self.wndSpecialStorage and self.wndSpecialStorage.IsShow():
				return self.wndSafebox.AttachItemFromInventory(slotWindow, slotIndex)
			#elif self.wndSpecialStorage and self.wndSpecialStorage.IsShow():
				#self.wndSpecialStorage.AttachItemFromInventory(slotWindow, slotIndex)

			elif self.dlgExchange and self.dlgExchange.IsShow():
				return self.dlgExchange.AttachItemFromInventory(slotWindow, slotIndex)

			return False

	if app.ENABLE_SWITCHBOT:
		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()
				
		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotItem(slot)

	if app.ENABLE_ITEM_TRANSACTIONS:
		def IsShowItemTransactions(self):
			return self.wndItemTransactions.IsShow()

		def AppendItemTransactionsSlot(self, invenType, slotIndex):
			if self.wndInventory.IsShow() and not self.IsShowItemTransactions():
				self.AdjustItemTransactions()
			self.wndItemTransactions.AppendSellSlot(invenType, slotIndex)
			self.UpdateItemTransactionsPrice()

		def RemoveItemTransactionsSlot(self, invenType, slotIndex):
			self.wndItemTransactions.RemoveSellSlot(invenType, slotIndex)
			self.UpdateItemTransactionsPrice()

		def UpdateItemTransactionsPrice(self):
			self.wndItemTransactions.UpdatePrice()
			self.RefreshMarkInventoryBag()

		def AdjustItemTransactions(self):
			x, y = self.wndInventory.GetGlobalPosition()
			x -= self.wndItemTransactions.WINDOW_WIDTH
			self.wndItemTransactions.AdjustPosition(x, y+313+45)

	if app.ENABLE_BIOLOG_SYSTEM:
		def OpenBiologWindow(self):
			if self.wndBiolog.IsShow():
				self.wndBiolog.Close()
			else:
				self.wndBiolog.Open()
				self.wndBiolog.LevelUpdate()

	def ToggleGameOptionWindow(self, target = False):
		if self.wndgameOption.IsShow():
			self.wndgameOption.Hide()
		else:
			self.wndgameOption.Open()
			if target:
				self.wndgameOption.SetScrollPositionForTarget()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			self.wndInventory.RefreshVisibleCostume()

	if app.ENABLE_DISTANCE_NPC:
		def OpenDistanceNPCWindow(self):
			if self.wndDistanceNPC.IsShow():
				self.wndDistanceNPC.Close()
			else:
				self.wndDistanceNPC.Show()

	def __ShowToolTipButton(self, desc):
		self.TooltipEvent(desc)

	def __HideToolTipButton(self):
		if self.toolTipWhisper:
			self.toolTipWhisper.Hide()

	def TooltipEvent(self, desc):
		if not self.toolTipWhisper:
			return

		self.toolTipWhisper.ClearToolTip()
		self.toolTipWhisper.AutoAppendTextLine(desc)
		self.toolTipWhisper.AlignHorizonalCenter()
		self.toolTipWhisper.Show()

	class MissionBoard(ui.Bar):
		FONT_HEIGHT	= 15
		LINE_HEIGHT	= FONT_HEIGHT + 5
		STEP_HEIGHT	= LINE_HEIGHT + 5
		LONG_TEXT_START_X	= 300
		SCREEN_WIDTH	= wndMgr.GetScreenWidth()
		
		
		def __init__(self):
			ui.Bar.__init__(self)

			self.AddFlag("not_pick")
			self.missionText = None
			self.missionFullText = None
			self.curPos = 0
			self.dstPos = -5
			self.nextScrollTime = 0
			self.flowMode = False
			self.ScrollStartTime = 0.0

			self.SetPosition(0, 100)
			self.SetSize(self.SCREEN_WIDTH, 35)
			self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
			self.SetWindowHorizontalAlignCenter()

			self.__CreateTextBar()
			
		def __del__(self):
			ui.Bar.__del__(self)

		def __CreateTextBar(self):

			x, y = self.GetGlobalPosition()

			self.textBar = BigTextBar(self.SCREEN_WIDTH*2, 300, self.FONT_HEIGHT)
			self.textBar.SetParent(self)
			self.textBar.SetPosition(6, 8)
			self.textBar.SetTextColor(242, 231, 193)
			self.textBar.SetClipRect(0, y, self.SCREEN_WIDTH, y+8+self.STEP_HEIGHT)
			self.textBar.Show()

		def CleanMission(self):
			self.missionText = None
			self.missionFullText = None
			self.textBar.ClearBar()
			self.Hide()

		def __RefreshBoard(self):

			self.textBar.ClearBar()

			if self.missionFullText:
				(text_width, text_height) = self.textBar.GetTextExtent(self.missionFullText)
				
				if text_width>self.SCREEN_WIDTH:
					self.textBar.TextOut(0, (self.STEP_HEIGHT-8-text_height)/2, self.missionFullText)
					self.flowMode = True
				else:
					self.textBar.TextOut((wndMgr.GetScreenWidth()-text_width)/2, (self.STEP_HEIGHT-8-text_height)/2, self.missionFullText)
					self.flowMode = False

		def SetMission(self, text):
			self.__AppendText(text)
			self.__RefreshBoard()

			curTime = app.GetTime()
			
			(text_width, text_height) = self.textBar.GetTextExtent(self.missionFullText)
			
			if self.flowMode:
				self.dstPos = -text_width
				self.curPos = self.LONG_TEXT_START_X
				self.textBar.SetPosition(3 + self.curPos, 8)
			else:
				self.dstPos = 0
				self.curPos = self.STEP_HEIGHT
				self.textBar.SetPosition(3, 8 + self.curPos)
			
			if not self.IsShow():
				self.Show()
				
			self.Timer = Timer()
			self.Timer.Open(10.0)
			self.Timer.SAFE_SetTimeOverEvent(self.CleanMission)
				
		def SetSubMission(self, text):
			self.missionFullText = self.missionText + text
			
			preflowMode = self.flowMode
			
			self.__RefreshBoard()
			
			if preflowMode != self.flowMode:
				if self.flowMode:
					self.dstPos = -text_width
					self.curPos = self.LONG_TEXT_START_X
					self.textBar.SetPosition(3 + self.curPos, 8)
				else:
					self.dstPos = 0
					self.curPos = self.STEP_HEIGHT
					self.textBar.SetPosition(3, 8 + self.curPos)

		def __AppendText(self, text):
			if text == "":
				self.CleanMission()
				return
				
			self.missionText = text
			self.missionFullText = text
			
		def OnUpdate(self):			
			if self.missionFullText == None:
				self.Hide()
				return

			if self.dstPos < self.curPos:
				self.curPos -= 1
				if self.flowMode:
					self.textBar.SetPosition(3 + self.curPos, 8)
				else:
					self.textBar.SetPosition(3, 8 + self.curPos)
			else:
				if self.flowMode:
					self.curPos = self.SCREEN_WIDTH

	if app.ENABLE_EVENT_MANAGER:
		def MakeEventIcon(self):
			if self.wndEventIcon == None:
				self.wndEventIcon = uiEventCalendarNew.MovableImage()
				if systemSetting.IsEventIconShow():
					self.wndEventIcon.Show()
	
		def MakeEventCalendar(self):
			if self.wndEventManager == None:
				self.wndEventManager = uiEventCalendarNew.EventCalendarWindow()
	
		def OpenEventCalendar(self):
			self.MakeEventCalendar()
			if self.wndEventManager.IsShow():
				self.wndEventManager.Close()
			else:
				self.wndEventManager.Open()
	
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			if eventendTime != 0:
				eventendTime += app.GetGlobalTimeStamp()
			uiEventCalendarNew.SetEventStatus(eventID, eventStatus, eventendTime, eventEndTimeText)
			self.RefreshEventManager()

		def ClearEventManager(self):
			uiEventCalendarNew.server_event_data={}

		def RefreshEventManager(self):
			if self.wndEventManager:
				self.wndEventManager.Refresh()
			if self.wndEventIcon:
				if systemSetting.IsEventIconShow():
					self.wndEventIcon.Refresh()

		def SetEventManagerIconState(self):
			if systemSetting.IsEventIconShow():
				self.wndEventIcon.Show()
			else:
				self.wndEventIcon.Hide()

		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.MakeEventCalendar()
			self.MakeEventIcon()
			if startRealTime != 0:
				startRealTime += app.GetGlobalTimeStamp()

			if endRealTime != 0:
				endRealTime += app.GetGlobalTimeStamp()
	
			uiEventCalendarNew.SetServerData(dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart)

	if app.ENABLE_ITEMSHOP:
		def MakeItemShopWindow(self):
			if self.wndItemShop == None:
				self.wndItemShop = uiItemShopNew.ItemShopWindow()
	
		def OpenItemShopWindow(self):
			self.MakeItemShopWindow()
			if self.wndItemShop.IsShow():
				self.wndItemShop.Close()
			else:
				self.wndItemShop.Open()

		def OpenItemShopMainWindow(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.LoadFirstOpening()

		def ItemShopHideLoading(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.CloseLoading()
	
		def ItemShopPurchasesWindow(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.OpenPurchasesWindow()

		def ItemShopUpdateItem(self, itemID, itemMaxSellingCount):
			self.MakeItemShopWindow()
			self.wndItemShop.UpdateItem(itemID, itemMaxSellingCount)

		def ItemShopSetDragonCoin(self,dragonCoin):
			self.MakeItemShopWindow()
			self.wndItemShop.SetDragonCoin(dragonCoin)

		def SetWheelItemData(self, cmd):
			self.MakeItemShopWindow()
			self.wndItemShop.SetWheelItemData(str(cmd))

		def OnSetWhell(self, giftIndex):
			self.MakeItemShopWindow()
			self.wndItemShop.OnSetWhell(int(giftIndex))
	
		def GetWheelGiftData(self, itemVnum, itemCount):
			self.MakeItemShopWindow()
			self.wndItemShop.GetWheelGiftData(int(itemVnum), int(itemCount))

	if app.ENABLE_AURA_SYSTEM:
		def ActAura(self, iAct, bWindow):
			if iAct == 1:
				if bWindow == True:
					if not self.wndAuraRefine.IsOpened():
						self.wndAuraRefine.Open()

					if not self.wndInventory.IsShow():
						self.wndInventory.Show()
				else:
					if not self.wndAuraAbsorption.IsOpened():
						self.wndAuraAbsorption.Open()

					if not self.wndInventory.IsShow():
						self.wndInventory.Show()

				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 2:
				if bWindow == True:
					if self.wndAuraRefine.IsOpened():
						self.wndAuraRefine.Close()
				else:
					if self.wndAuraAbsorption.IsOpened():
						self.wndAuraAbsorption.Close()

				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 3 or iAct == 4:
				if bWindow == True:
					if self.wndAuraRefine.IsOpened():
						self.wndAuraRefine.Refresh(iAct)
				else:
					if self.wndAuraAbsorption.IsOpened():
						self.wndAuraAbsorption.Refresh(iAct)

				self.wndInventory.RefreshBagSlotWindow()

	if app.ENABLE_WIKI:
		def OpenWikiWindow(self):
			if self.wndWiki.IsShow():
				self.wndWiki.Close()
			else:
				self.wndWiki.Open()

		def MakeWiki(self):
			if self.wndWiki == None:
				self.wndWiki = uiWiki.EncyclopediaofGame()

	if app.ENABLE_RENDER_TARGET:
		def MakeRenderTargetWindow(self):
			if self.wndRenderTarget == None:
				self.wndRenderTarget = uiRenderTarget.RenderTargetWindow()

		def OpenRenderTargetWindow(self, renderType = 0, renderVnum = 11299):
			self.MakeRenderTargetWindow()
			self.wndRenderTarget.Open(renderType, renderVnum)

	if app.ENABLE_VOTE4BUFF:
		def MakeVote4BuffIcon(self):
			if self.wndVoteIcon == None:
				self.wndVoteIcon = uiVote4Buff.VoteImage()
				self.wndVoteIcon.Hide()

	if app.ENABLE_MAINTENANCE_SYSTEM:
		def MakeMaintenanceWindows(self):
			if self.wndMaintenanceWindow:
				return

			self.wndMaintenanceWindow = uimaintenance.MaintenanceWindow()
			self.wndMaintenanceWindow.Hide()

		def ShowMaintenanceInfo(self, maintenanceDur, leftTime):
			self.wndMaintenanceWindow.Open(maintenanceDur, leftTime)

	if app.ENABLE_EXTENDED_BATTLE_PASS:
		def ReciveOpenExtBattlePass(self):
			if False == self.isFirstOpeningExtBattlePass:
				self.isFirstOpeningExtBattlePass = True
				self.wndBattlePassExtended.SetPage("NORMAL")
			if False == self.wndBattlePassExtended.IsShow():
				self.ToggleBattlePassExtended()
			else:
				self.wndBattlePassExtended.SetPage(self.wndBattlePassExtended.GetPage())

		def ToggleBattlePassExtended(self):
			if False == self.isFirstOpeningExtBattlePass:
				net.SendExtBattlePassAction(1)
			if False == self.wndBattlePassExtended.IsShow():
				self.wndBattlePassExtended.Show()
				self.wndBattlePassExtended.SetTop()
			else:
				self.wndBattlePassExtended.Close()
		
		def AddExtendedBattleGeneralInfo(self, BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.RecvGeneralInfo(BattlePassType, BattlePassName, BattlePassID, battlePassStartTime, battlePassEndTime)
		
		def AddExtendedBattlePassMission(self, battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.AddMission(battlepassType, battlepassID, missionIndex, missionType, missionInfo1, missionInfo2, missionInfo3)

		def UpdateExtendedBattlePassMission(self, battlepassType, missionIndex, missionType, newProgress):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.UpdateMission(battlepassType, missionIndex, missionType, newProgress)

		def AddExtendedBattlePassMissionReward(self, battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.AddMissionReward(battlepassType, battlepassID, missionIndex, missionType, itemVnum, itemCount)

		def AddExtendedBattlePassReward(self, battlepassType, battlepassID, itemVnum, itemCount):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.AddReward(battlepassType, battlepassID, itemVnum, itemCount)

		def AddExtBattlePassRanklistEntry(self, playername, battlepassType, battlepassID, startTime, endTime):
			if self.wndBattlePassExtended:
				self.wndBattlePassExtended.AddRankingEntry(playername, battlepassType, battlepassID, startTime, endTime)

	if app.ENABLE_FAST_SKILL_BOOK_SYSTEM:
		def OpenReadBookWindow(self):
			if self.readBookWnd.IsShow():
				self.readBookWnd.Close()
			else:
				self.readBookWnd.Open()
    
		def OpenReadBookWindowPage(self, page):
			if self.readBookWnd.IsShow():
				self.readBookWnd.Close()
			else:
				self.readBookWnd.Open()
				self.readBookWnd.SetPage(page)

	if app.ENABLE_BUFFI_SYSTEM:
		def OpenBuffiWindow(self):
			if self.buffiWnd.IsShow():
				self.buffiWnd.Close()
			else:
				self.buffiWnd.Open()

	if app.ENABLE_LEADERSHIP_EXTENSION:
		def TogglePartyBonusWindow(self, forceClose = False):
			if forceClose:
				self.wndPartyBonusWindow.Close()
				return
				
			if not self.wndPartyBonusWindow.IsShow():
				self.wndPartyBonusWindow.Open()
			else:
				self.wndPartyBonusWindow.Close()

	if app.ENABLE_DUNGEON_MODULES:
		def MakeDungeonTimerWindow(self):
			self.wndDungeonTimer = uiDungeonTimer.Cooldown()
			self.wndDungeonTimer.Hide()

	if app.ENABLE_6TH_7TH_ATTR:
		def OpenAttr67AddDlg(self):
			if self.wndAttr67Add:
				self.wndAttr67Add.Show()

		if app.WJ_ENABLE_TRADABLE_ICON:
			def IsAttr67RegistItem(self):
				return self.wndAttr67Add and self.wndAttr67Add.RegistSlotIndex != -1

			def IsAttr67SupportItem(self):
				return self.wndAttr67Add and self.wndAttr67Add.SupportSlotIndex != -1

	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
		def OpenCardsInfoWindow(self):
			self.wndCardsInfo.Open()

		def OpenCardsWindow(self, safemode):
			self.wndCards.Open(safemode)

		def UpdateCardsInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
			self.wndCards.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)

		def UpdateCardsFieldInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.wndCards.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

		def CardsPutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
			self.wndCards.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)

	if app.ENABLE_MINI_GAME_BNW:
		def MinigameBnwOpen(self):
			self.dlgMinigameBnw.Open()

		def MinigameBnwStart(self):
			self.dlgMinigameBnw.Start()

		def MinigameBnwSetResult(self, result, playerPoints, enemyPoints):
			self.dlgMinigameBnw.SetResult(result, playerPoints, enemyPoints)

	if app.ENABLE_MINI_GAME_CATCH_KING:
		def MiniGameCatchKingEventStart(self, bigScore):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.GameStart(bigScore)

		def MiniGameCatchKingSetHandCard(self, cardNumber):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingSetHandCard(cardNumber)

		def MiniGameCatchKingResultField(self, score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingResultField(score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear)

		def MiniGameCatchKingSetEndCard(self, cardPos, cardNumber):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingSetEndCard(cardPos, cardNumber)

		def MiniGameCatchKingReward(self, rewardCode):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingReward(rewardCode)

		def ClickCatchKingEventButton(self):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.Open()


	if app.ENABLE_CHANNEL_SWITCH_SYSTEM:
		def ClickMoveChannelButton(self, fromSystem=False):
			if self.dlgSystem and fromSystem:
				self.dlgSystem.Close()

			if self.moveChannelDlg:
				if self.moveChannelDlg.IsShow():
					self.moveChannelDlg.Hide()
				else:
					self.moveChannelDlg.Show()
			else:
				moveChannelDlg = uiSystem.MoveChannelDialog()
				moveChannelDlg.Show()
				self.moveChannelDlg = moveChannelDlg

	def IsAnyWindowOpen(self):
		if any([self.wndCubeRenewal.IsShow(), self.dlgShop.IsShow(), self.wndShopOffline.IsShow()]):
			return True
		return False
