import app, re, player, time, uiScriptLocale

DALGA_BOYU = 450
# EXTRA BEGIN
# loads 5 (B,M,G,P,F) skills .mse
ENABLE_NEW_LEVELSKILL_SYSTEM = 0
# don't set a random channel when you open the client
ENABLE_RANDOM_CHANNEL_SEL = 0
# don't remove id&pass if the login attempt fails
ENABLE_CLEAN_DATA_IF_FAIL_LOGIN = 0
# ctrl+v will now work
ENABLE_PASTE_FEATURE = 1
# display all the bonuses added by a stone instead of the first one
ENABLE_FULLSTONE_DETAILS = 1
# enable successfulness % in the refine dialog
ENABLE_REFINE_PCT = 0
# extra ui features
EXTRA_UI_FEATURE = 1
#
NEW_678TH_SKILL_ENABLE = 1
# EXTRA END

# option
IN_GAME_SHOP_ENABLE = 1

PVPMODE_ENABLE = 1
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 15

FOG_LEVEL0 = 4800.0
FOG_LEVEL1 = 9600.0
FOG_LEVEL2 = 12800.0
FOG_LEVEL = FOG_LEVEL0
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]

CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_SHORT

CHRNAME_COLOR_INDEX = 0

ENVIRONMENT_NIGHT="d:/ymir work/environment/moonlight04.msenv"

# constant
HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0

USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 1
DEATH_TIME_COUNTDOWN = 1
isItemQuestionDialog = 0

def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

import app
import net

########################

def SET_DEFAULT_FOG_LEVEL():
	global FOG_LEVEL
	app.SetMinFog(FOG_LEVEL)

def SET_FOG_LEVEL_INDEX(index):
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	try:
		FOG_LEVEL=FOG_LEVEL_LIST[index]
	except IndexError:
		FOG_LEVEL=FOG_LEVEL_LIST[0]
	app.SetMinFog(FOG_LEVEL)

def GET_FOG_LEVEL_INDEX():
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	return FOG_LEVEL_LIST.index(FOG_LEVEL)

########################

def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_MAX_DISTANCE
	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def SET_CAMERA_MAX_DISTANCE_INDEX(index):
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	try:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[index]
	except:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[0]

	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def GET_CAMERA_MAX_DISTANCE_INDEX():
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	return CAMERA_MAX_DISTANCE_LIST.index(CAMERA_MAX_DISTANCE)

########################

import chrmgr
import player
import app

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgr.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgr.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE():
	global CONVERT_EMPIRE_LANGUAGE_ENABLE
	net.SetEmpireLanguageMode(CONVERT_EMPIRE_LANGUAGE_ENABLE)

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	player.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)

########################
import item

ACCESSORY_MATERIAL_LIST = xrange(50623, 50641)

JewelAccessoryInfos = [
		# jewel		wrist	neck	ear
		[ 50623,	14000, 16000, 17000 ],
		[ 50624,	14020, 16020, 17020 ],
		[ 50625,	14040, 14040, 14040 ],
		[ 50626,	14060, 14060, 14060 ],
		[ 50627,	14080, 14080, 14080 ],
		[ 50628,	14100, 16100, 17100 ],
		[ 50629,	14120, 16120, 17120 ],
		[ 50630,	14140, 16140, 17140 ],
		[ 50631,	14160, 16160, 17160 ],
		[ 50632,	14180, 16180, 17180 ],
		[ 50633,	14200, 16200, 17200 ],
		[ 50634,	14220, 16220, 17220 ],
		[ 50635,	14500, 16500, 17500 ],
		[ 50636,	14520, 16520, 17520 ],
		[ 50637,	14540, 16540, 17540 ],
		[ 50638,	14560, 16560, 17560 ],
		[ 50639,	14570, 16570, 17570 ],
		[ 50640,	14580, 16580, 17580 ],
		[ 50640,	14590, 16590, 17590 ],
		[ 50641,	14600, 16600, 17600 ],
	]
	
def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum / 10) * 10
	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:
			if info[1] == item_base:
				return info[0]
		elif item.ARMOR_NECK == subType:
			if info[2] == item_base:
				return info[0]
		elif item.ARMOR_EAR == subType:
			if info[3] == item_base:
				return info[0]

	if vnum >= 16210 and vnum <= 16219:
		return 50625

	if item.ARMOR_WRIST == subType:
		WRIST_ITEM_VNUM_BASE = 14000
		ret -= WRIST_ITEM_VNUM_BASE
	elif item.ARMOR_NECK == subType:
		NECK_ITEM_VNUM_BASE = 16000
		ret -= NECK_ITEM_VNUM_BASE
	elif item.ARMOR_EAR == subType:
		EAR_ITEM_VNUM_BASE = 17000
		ret -= EAR_ITEM_VNUM_BASE

	type = ret/20

	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
		type = (ret-170) / 20
		if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
			return 0

	return ACCESSORY_MATERIAL_LIST[type]

JewelAccessoryInfosDict = {
	50623 : 950623,
	50624 : 950624,
	50625 : 950625,
	50626 : 950626,
	50627 : 950627,
	50628 : 950628,
	50629 : 950629,
	50630 : 950630,
	50631 : 950631,
	50632 : 950632,
	50633 : 950633,
	50634 : 950634,
	50635 : 950635,
	50636 : 950636,
	50637 : 950637,
	50638 : 950638,
	50639 : 950639,
	50640 : 950640,
	50641 : 950641,
	18900 : 918900,
}

SELECTED_ITEM_VNUM = [0, 0, 0, False] # Vnum, inventory, Slot, ShowTooltip

##################################################################

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	return 18900

##################################################################

def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum)

def IS_AUTO_POTION_HP(itemVnum):
	if 72726 == itemVnum or 72730 >= itemVnum:
		return 1
	return 0

def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:
		return 1
	elif itemVnum == 79013:
		return 1

	return 0

if app.ENABLE_TARGET_INFORMATION_SYSTEM:
	MONSTER_INFO_DATA = {}

if app.ENABLE_CHANNEL_SWITCH_SYSTEM:
	channel_idx = 0

if app.ENABLE_REFINE_RENEWAL:
	IS_AUTO_REFINE = False
	AUTO_REFINE_TYPE = 0
	AUTO_REFINE_DATA = {
		"ITEM" : [-1, -1],
		"NPC" : [0, -1, -1, 0]
	}

if app.ENABLE_SPECIAL_STORAGE:
	SpecialInventoryMode=0
	IsSpecialInventoryOpen=0
	OPEN_SAFEBOX_MALL_IN_SPECIAL_INV = True
else:
	OPEN_SAFEBOX_MALL_IN_SPECIAL_INV = False

INCREASE_POINTS_CTRL = 10 #@Hizli statu verme miktari

def ConvertMoneyText(text, powers = dict(k = 10**3, m = 10**6, t = 10**9, kt = 10**12)):
	match = re.search(r'(\d+)({:s}+)?'.format('+|'.join(powers.keys())), text.lower(), re.I)
	if match:
		moneyValue, suffixName = match.groups()
		moneyValue = int(moneyValue)
		if not suffixName:
			return moneyValue

		return moneyValue * (powers[suffixName[0]] ** len(suffixName))

	return 0

if app.ENABLE_SWITCHBOT:
	def CanPutItemInSwitchbot(itemIndex):
		item.SelectItem(itemIndex)

		armorSubtypes = [item.ARMOR_BODY, item.ARMOR_HEAD, item.ARMOR_SHIELD, item.ARMOR_WRIST, item.ARMOR_FOOTS, item.ARMOR_NECK, item.ARMOR_EAR]

		# if not item.GetItemType() in [item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_COSTUME]:
		if not item.GetItemType() in [item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR]:
			return False
		
		if item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == item.WEAPON_ARROW:
			# item.GetItemSubType() in [item.WEAPON_ARROW,item.WEAPON_QUIVER]:
			return False

		if item.GetItemType() == item.ITEM_TYPE_ARMOR and not item.GetItemSubType() in armorSubtypes:
			return False

		# if item.GetItemType() == item.ITEM_TYPE_COSTUME and\
			# not item.GetItemSubType() in [item.COSTUME_TYPE_BODY, item.COSTUME_TYPE_HAIR, item.COSTUME_TYPE_WEAPON]:
			# return False
		
		return True

if app.ENABLE_SPECIAL_STORAGE:
	def getSpecialInventoryType(win):
		if win == player.SLOT_TYPE_UPGRADE_INVENTORY:
			return player.UPGRADE_INVENTORY
		elif win == player.SLOT_TYPE_STONE_INVENTORY:
			return player.STONE_INVENTORY
		elif win == player.SLOT_TYPE_BOOK_INVENTORY:
			return player.BOOK_INVENTORY
		elif win == player.SLOT_TYPE_CHEST_INVENTORY:
			return player.CHEST_INVENTORY
		elif win == player.SLOT_TYPE_INVENTORY:
			return player.INVENTORY
		return -1

	def getSpecialInventoryWindowbyType(win):
		if win == player.UPGRADE_INVENTORY:
			return player.SLOT_TYPE_UPGRADE_INVENTORY
		elif win == player.STONE_INVENTORY:
			return player.SLOT_TYPE_STONE_INVENTORY
		elif win == player.SLOT_TYPE_BOOK_INVENTORY:
			return player.BOOK_INVENTORY
		elif win == player.CHEST_INVENTORY:
			return player.SLOT_TYPE_CHEST_INVENTORY
		return -1
	
if app.ENABLE_SHOP_SEARCH:
	import grp
	def GetPriceColor(price):
		if price < 500000000:
			return grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
		elif price < 1000000000:
			return grp.GenerateColor( (255.0/255.0), (153.0/255.0), (51.0/255.0), 1.0)
		elif price < 10000000000:
			return grp.GenerateColor( (153.0/255.0), (76.0/255.0), (0.0/255.0), 1.0)
		else:
			return grp.GenerateColor( (255.0/255.0), (51.0/255.0), (51.0/255.0), 1.0)

if app.ENABLE_CHEST_OPEN_RENEWAL:
	CHEST_OPEN_COUNT = 50000
	chestCheckMaps =[
	"metin2_map_a1",
	"metin2_map_a3",
	"metin2_map_b1",
	"metin2_map_b3",
	"metin2_map_c1",
	"metin2_map_c3"
	]
	

_game_instance = None
def GetGameInstance():
	global _game_instance
	return _game_instance
def SetGameInstance(instance):
	global _game_instance
	if _game_instance:
		del _game_instance
	_game_instance = instance
def GetInterfaceInstance():
	global _game_instance
	if _game_instance:
		return _game_instance.interface
	return None


if app.ENABLE_GLOBAL_RANKING:
	py_Flag = {}

	def GetFlag(flagname):
		global py_Flag
		return py_Flag.get(flagname, None)

	def SetFlag(flagname, value):
		global py_Flag
		py_Flag[flagname] = value

def waitTime(waitTime):
	time.sleep(waitTime)

if app.ENABLE_HIDE_AFFECT_ICONS:
	AffectIconState = FALSE

if app.ENABLE_ITEM_TRANSACTIONS:
	ITEM_INFORMATIONS_TRANSACTIONS = {}

def NumberToStrRomanNumerals(number):
	ROMAN = [
		(1000, "M"),
		( 900, "CM"),
		( 500, "D"),
		( 400, "CD"),
		( 100, "C"),
		(  90, "XC"),
		(  50, "L"),
		(  40, "XL"),
		(  10, "X"),
		(   9, "IX"),
		(   5, "V"),
		(   4, "IV"),
		(   1, "I"),
	]
	
	result = ""
	for (arabic, roman) in ROMAN:
		(factor, number) = divmod(number, arabic)
		result += roman * factor
	return result

if app.ENABLE_AUTO_SHOUT:
	AUTO_SHOUT_ACTIVATED = 0
	SHOUT_PER_SECOND = 15
	LAST_SHOUT_MESSAGE = ""

if app.ENABLE_NEW_PET_SYSTEM:
	petVnums = [55701, 55702, 55703, 55704, 55705, 55706, 55710, 55711]
	petUsableItems = xrange(980, 991) # Aralıktaki tüm nesneler

	def IS_NEW_PET_ITEM(itemVnum):
		if itemVnum in petVnums:
			return 1
		return 0

	def IS_NEW_PET_USABLE_ITEM(itemVnum):
		if itemVnum in petUsableItems:
			return 1
		return 0

if app.ENABLE_DISTANCE_SKILL_SELECT:
	CHOOSE_SKILL = 0

ENABLE_DSS_ACTIVE_EFFECT_BUTTON = 1

if app.ENABLE_WIKI:
	_main_wiki_instance = None
	_listbox_wiki_instance = None
	def SetMainParent(instance):
		global _main_wiki_instance
		if _main_wiki_instance:
			del _main_wiki_instance
		_main_wiki_instance = instance
	def GetMainParent():
		global _main_wiki_instance
		return _main_wiki_instance
	def SetListBox(instance):
		global _listbox_wiki_instance
		if _listbox_wiki_instance:
			del _listbox_wiki_instance
		_listbox_wiki_instance = instance
	def GetListBox():
		global _listbox_wiki_instance
		return _listbox_wiki_instance
	def IS_SET(value, flag):
		return (value & flag) == flag


if app.ENABLE_NAMING_SCROLL:

	NAMING_BONUS_RATES = [0, 0]

	def IS_NAMING_SCROLL(itemVnum):
		if itemVnum in xrange(24050, 24062):
			return True

		if itemVnum in xrange(64000, 64003):
			return True

		return False

	def NAMING_SCROLL_GET_BONUS_RATE(type):
		if len(NAMING_BONUS_RATES):
			if NAMING_BONUS_RATES[type] > 0:
				return NAMING_BONUS_RATES[type]
		return -1

if app.ENABLE_MINING_RENEWAL:
	MINING_POINT = 0

if app.ENABLE_LOADING_WINDOW_RENEWAL:
	CURTAIN_ACTIVE = 1

if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
	MULTI_LANGUAGE_NEED_RESTART_CLIENT = True # Enable the requirement to restart client after changing language in game
	langList = ( "en", "pt","es", "fr","de", "ro","pl", "it","cz", "hu", "tr")

	LOCALE_LANG_DICT = {
		app.LOCALE_EN : { "name" : uiScriptLocale.LANGUAGE_EN, "locale" : "en", "code_page" : 1254 },
		app.LOCALE_PT : { "name" : uiScriptLocale.LANGUAGE_PT, "locale" : "pt", "code_page" : 1254 },
		app.LOCALE_ES : { "name" : uiScriptLocale.LANGUAGE_ES, "locale" : "es", "code_page" : 1254 },
		app.LOCALE_FR : { "name" : uiScriptLocale.LANGUAGE_FR, "locale" : "fr", "code_page" : 1254 },
		app.LOCALE_DE : { "name" : uiScriptLocale.LANGUAGE_DE, "locale" : "de", "code_page" : 1254 },
		app.LOCALE_RO : { "name" : uiScriptLocale.LANGUAGE_RO, "locale" : "ro", "code_page" : 1250 },
		app.LOCALE_PL : { "name" : uiScriptLocale.LANGUAGE_PL, "locale" : "pl", "code_page" : 1250 },
		app.LOCALE_IT : { "name" : uiScriptLocale.LANGUAGE_IT, "locale" : "it", "code_page" : 1254 },
		app.LOCALE_CZ : { "name" : uiScriptLocale.LANGUAGE_CZ, "locale" : "cz", "code_page" : 1250 },
		app.LOCALE_HU : { "name" : uiScriptLocale.LANGUAGE_HU, "locale" : "hu", "code_page" : 1250 },
		app.LOCALE_TR : { "name" : uiScriptLocale.LANGUAGE_TR, "locale" : "tr", "code_page" : 1254 },
	}


if app.ENABLE_VOTE4BUFF:
	VOTE_QUEST_IDX = 0

if app.ENABLE_EXTENDED_BLEND_AFFECT:
	def IS_BLEND_POTION(itemVnum):
		if itemVnum >= 50821 and itemVnum <= 50835:
			return 1
		elif itemVnum == 51002:
			return 1
		elif itemVnum >= 950021 and itemVnum <= 950036: # Dews Limited 1d / 30m
			return 1
		elif itemVnum >= 71027 and itemVnum <= 71030:
			return 1
		elif itemVnum == 71044 or itemVnum == 71045:
			return 1
		elif itemVnum == 27102 or itemVnum == 27105:
			return 1
		elif itemVnum == 50817 or itemVnum == 50818:
			return 1
		elif itemVnum == 950817 or itemVnum == 950818:
			return 1

		return 0

	def IS_EXTENDED_BLEND_POTION(itemVnum):
		if itemVnum >= 950821 and itemVnum <= 950835: # Dews
			return 1
		elif itemVnum == 951002: # Cristal Energy
			return 1
		elif itemVnum >= 939017 and itemVnum <= 939020: # Dragon God Medals
			return 1
		elif itemVnum == 939024 or itemVnum == 939025: # Critical & Penetration
			return 1
		elif itemVnum == 927209 or itemVnum == 927212: # Attack Speed & Move Speed
			return 1

		return 0

def SHOW_COUNT_TYPE_LIST(itemVnum):
	item.SelectItem(itemVnum)
	itemType = item.GetItemType()

	if itemType in [item.ITEM_TYPE_SPECIAL, item.ITEM_TYPE_MATERIAL
		, item.ITEM_TYPE_SPECIAL, item.ITEM_TYPE_GIFTBOX, item.ITEM_TYPE_METIN
		, item.ITEM_TYPE_RESOURCE, item.ITEM_TYPE_SKILLBOOK]:
		return True


	return False

def CONFIRM_BEFORE_USE_ITEMLIST(itemVnum):
	if itemVnum in [70005, 70043, 970005, 970043, 55140]:
		return True

	return False

if app.ENABLE_BUFFI_SYSTEM:
	def IS_BUFFI_ITEM(itemVnum):
		if itemVnum in xrange(71992, 72000):
			return True

		elif itemVnum == 64005:
			return True

		return False

def IsAttr(itemVnum):
	if itemVnum in [71084, 71085, 71151, 71152, 70024, 39028, 39029, 24102, 24103, 24104, 24105, 72351, 72346]:
		return True

	return False

BOOSTER_ITEM_RATES = { \
	24200 : (10, 1),
	24201 : (10, 1),
	24202 : (10, 1),
	24203 : (10, 1),
	24204 : (10, 1),
	24205 : (10, 1),

	224200 : (10, 1),
	224201 : (10, 1),
	224202 : (10, 1),
	224203 : (10, 1),
	224204 : (10, 1),
	224205 : (10, 1),

	24206 : (15, 1),
	24207 : (15, 1),
	24208 : (15, 1),
	24209 : (15, 1),
	24210 : (15, 1),
	24211 : (15, 1),

	224206 : (15, 1),
	224207 : (15, 1),
	224208 : (15, 1),
	224209 : (15, 1),
	224210 : (15, 1),
	224211 : (15, 1),

	24212 : (20, 1),
	24213 : (20, 1),
	24214 : (20, 1),
	24215 : (20, 1),
	24216 : (20, 1),
	24217 : (20, 1),

	224212 : (20, 1),
	224213 : (20, 1),
	224214 : (20, 1),
	224215 : (20, 1),
	224216 : (20, 1),
	224217 : (20, 1),

}

def CloseWindows():
	global DALGA_BOYU
	if app.GetTime() < DALGA_BOYU:
		DALGA_BOYU -= app.GetTime()
	else:
		DALGA_BOYU = 450

	if GetInterfaceInstance():
		GetInterfaceInstance().HideWindowsBeforeWarp()
	if GetGameInstance():
		GetGameInstance().CloseShownWindows()

usedUpgraddeItemType = 0

def IsFastReadItem(vnum):
	if vnum in (50513, 24000):
		return True

	elif vnum in xrange(24002, 24013):
		return True 

	elif vnum in xrange(50400, 50500):
		return True

	return False

def GetFastReadItemPage(vnum):
	if vnum == 50513:
		return 1

	elif vnum == 24000:
		return 2

	elif vnum in xrange(24002, 24013):
		return 3

	return 0

ALREADY_NOTIFY_LIST = list()

MESSENGER_GM_FLAGLIST = {
    "[SA]Athenis": "pl",
    "[TA]Rience": "de",
    "[CM]Hestia": "tr",
    "[GA]Hermes": "ro",
    "[SGM]Non": "it",
    "[SGM]Lecter": "hu",
}

BLOCK_TRADE_ITEM_LIST = [ \

	232000,
	232002,
	232004,
	232006,
	232008,
	232010,
	232012,
	232014,
	232016,
	232018,
	232020,
	232022,
	232024,
	232026,
	232028,
	232030,
	232032,
	232034,
	232036,
	232038,
	232040,
	232042,
	232044,
	232046,
	232048,
	232050,
	232052,
	232054,
	232056,
	232058,
	232060,
	232062,
	232064,
	232066,
	232068,
	232070,
	232072,
	232074,
	232076,
	232078,
	232080,
	232082,
	232084,
	232086,
	232088,
	232090,
	232092,
	232094,
	232096,
	232098,
	232001,
	232003,
	232005,
	232007,
	232009,
	232011,
	232013,
	232015,
	232017,
	232019,
	232021,
	232023,
	232025,
	232027,
	232029,
	232031,
	232033,
	232035,
	232037,
	232039,
	232041,
	232043,
	232045,
	232047,
	232049,
	232051,
	232053,
	232055,
	232057,
	232059,
	232061,
	232063,
	232065,
	232067,
	232069,
	232071,
	232073,
	232075,
	232077,
	232079,
	232081,
	232083,
	232085,
	232087,
	232089,
	232091,
	232093,
	232095,
	232097,
	232099,
	232100,
	232102,
	232104,
	232106,
	232108,
	232110,
	232112,
	232114,
	232116,
	232118,
	232120,
	232122,
	232124,
	232126,
	232128,
	232130,
	232132,
	232134,
	232136,
	232138,
	232140,
	232142,
	232144,
	232146,
	232148,
	232150,
	232152,
	232154,
	232156,
	232158,
	232160,
	232162,
	232164,
	232166,
	232168,
	232170,
	232172,
	232174,
	232176,
	232178,
	232180,
	232182,
	232184,
	232186,
	232188,
	232190,
	232192,
	232194,
	232196,
	232198,
	232200,
	232201,
	232202,
	232203,
	232204,
	232205,
	232206,
	232207,
	232208,
	232209,
	232210,
	232211,
	232212,
	232213,
	232214,
	232215,
	232216,
	232217,
	232218,
	232219,
	232220,
	232221,
	232222,
	232223,
	232224,
	232225,
	232226,
	232227,
	232228,
	232229,
	232230,
	232231,
	232232,
	232233,
	232234,
	232235,
	232236,
	232237,
	232238,
	232239,
	232240,
	232241,
	232242,
	232243,
	232244,
	232245,
	232246,
	232247,
	232248,
	232249,
	232250,
	232251,
	232252,
	232253,
	232254,
	232255,
	232256,
	232257,
	232258,
	232259,
	232260,
	232261,
	232262,
	232263,
	232264,
	232265,
	232266,
	232267,
	232268,
	232269,
	232270,
	232271,
	232272,
	232273,
	232274,
	232275,
	232276,
	232277,
	232278,
	232279,
	232280,
	232281,
	232282,
	232283,
	232284,
	232285,
	232286,
	232287,
	232288,
	232289,
	232290,
	232291,
	232292,
	232293,
	232294,
	232295,
	232296,
	232297,
	232298,
	232299,
	232300,
	232301,
	232302,
	232303,
	232304,
	232305,
	232306,
	232307,
	232308,
	232309,
	232310,
	232311,
	232312,
	232313,
	232314,
	232315,
	232316,
	232317,
	232318,
	232319,
	232320,
	232321,
	232322,
	232323,
	232324,
	232325,
	232326,
	232327,
	232328,
	232329,
	232330,
	232331,
	232332,
	232333,
	232334,
	232335,
	232336,
	232337,
	232338,
	232339,
	232340,
	232341,
	232342,
	232343,
	232344,
	232345,
	232346,
	232347,
	232348,
	232349,
	232350,
	232351,
	232352,
	232353,
	232354,
	232355,
	232356,
	232357,
	232358,
	232359,
	232360,
	232361,
	232362,
	232363,
	232364,
	232365,
	232366,
	232367,
	232368,
	232369,
	232370,
	232371,
	232372,
	232373,
	232374,
	232375,
	232376,
	232377,
	232378,
	232379,
	232380,
	232381,
	232382,
	232383,
	232384,
	232385,
	232386,
	232387,
	232388,
	232389,
	232390,
	232391,
	232392,
	232393,
	232394,
	232395,
	232396,
	232397,
	232398,
	232399,
	232400,
	232401,
	232402,
	232403,
	232404,
	232405,
	232406,
	232407,
	232408,
	232409,
	232410,
	232411,
	232412,
	232413,
	232414,
	232415,
	232416,
	232417,
	232418,
	232419,
	232420,
	232421,
	232422,
	232423,
	232424,
	232425,
	232426,
	232427,
	232428,
	232429,
	232430,
	232431,
	232432,
	232433,
	232434,
	232435,
	232436,
	232437,
	232438,
	232439,
	232440,
	232441,
	232442,
	232443,
	232444,
	232445,
	232446,
	232447,
	232448,
	232449,
	232450,
	232451,
	232452,
	232453,
	232454,
	232455,
	232456,
	232457,
	232458,
	232459,
	232460,
	232461,
	232462,
	232463,
	232464,
	232465,
	232466,
	232467,
	232468,
	232469,
	232470,
	232471,
	232472,
	232473,
	232474,
	232475,
	232476,
	232477,
	232478,
	232479,
	232480,
	232481,
	232482,
	232483,
	232484,
	232485,
	232486,
	232487,
	232488,
	232489,
	232490,
	232491,
	232492,
	232493,
	232494,
	232495,
	232496,
	232497,
	232498,
	232499,
	232550,
	232551,
	232552,
	232553,
	232554,
	232555,
	232556,
	232557,
	232558,
	232559,
	232560,
	232561,
	232562,
	232563,
	232564,
	232565,
	232566,
	232567,
	232568,
	232569,
	232570,
	232571,
	232572,
	232573,
	232574,
	232575,
	232576,
	232577,
	232578,
	232579,
	232580,
	232581,
	232582,
	232583,
	232584,
	232585,
	232586,
	232587,
	232588,
	232589,
	232590,
	232591,
	232592,
	232593,
	232594,
	232595,
	232596,
	232597,
	232598,
	232599,
	232600,
	232601,
	232602,
	232603,
	232604,
	232605,
	232606,
	232607,
	232608,
	232609,
	232610,
	232611,
	232612,
	232613,
	232614,
	232615,
	232616,
	232617,
	232618,
	232619,
	232620,
	232621,
	232622,
	232623,
	232624,
	232625,
	232626,
	232627,
	232628,
	232629,
	232630,
	232631,
	232632,
	232633,
	232634,
	232635,
	232636,
	232637,
	232638,
	232639,
	232640,
	232641,
	232642,
	232643,
	232644,
	232645,
	232646,
	232647,
	232648,
	232649,
	234000,
	234001,
	234002,
	234003,
	234004,
	234005,
	234006,
	234007,
	234008,
	234009,
	234010,
	234011,
	234012,
	234013,
	234014,
	234015,
	234016,
	234017,
	234018,
	234019,
	234020,
	234021,
	234022,
	234023,
	234024,
	234025,
	234026,
	234027,
	234028,
	234029,
	234030,
	234031,
	234032,
	234033,
	234034,
	234035,
	234036,
	234037,
	234038,
	234039,
	234040,
	234041,
	234042,
	234043,
	234044,
	234045,
	234046,
	234047,
	234048,
	234049,
	234050,
	234051,
	234052,
	234053,
	234054,
	234055,
	234056,
	234057,
	234058,
	234059,
	234060,
	234061,
	234062,
	234063,
	234064,
	234065,
	234066,
	234067,
	234068,
	234069,
	234070,
	234071,
	234072,
	234073,
	234074,
	234075,
	234076,
	234077,
	234078,
	234079,
	234080,
	234081,
	234082,
	234083,
	234084,
	234085,
	234086,
	234087,
	234088,
	234089,
	234090,
	234091,
	234092,
	234093,
	234094,
	234095,
	234096,
	234097,
	234098,
	234099,
	234100,
	234101,
	234102,
	234103,
	234104,
	234105,
	234106,
	234107,
	234108,
	234109,
	234110,
	234111,
	234112,
	234113,
	234114,
	234115,
	234116,
	234117,
	234118,
	234119,
	234120,
	234121,
	234122,
	234123,
	234124,
	234125,
	234126,
	234127,
	234128,
	234129,
	234130,
	234131,
	234132,
	234133,
	234134,
	234135,
	234136,
	234137,
	234138,
	234139,
	234140,
	234141,
	234142,
	234143,
	234144,
	234145,
	234146,
	234147,
	234148,
	234149,
	234150,
	234151,
	234152,
	234153,
	234154,
	234155,
	234156,
	234157,
	234158,
	234159,
	234160,
	234161,
	234162,
	234163,
	234164,
	234165,
	234166,
	234167,
	234168,
	234169,
	234170,
	234171,
	234172,
	234173,
	234174,
	234175,
	234176,
	234177,
	234178,
	234179,
	234180,
	234181,
	234182,
	234183,
	234184,
	234185,
	234186,
	234187,
	234188,
	234189,
	234190,
	234191,
	234192,
	234193,
	234194,
	234195,
	234196,
	234197,
	234198,
	234199,
	234200,
	234201,
	234202,
	234203,
	234204,
	234205,
	234206,
	234207,
	234208,
	234209,
	234210,
	234211,
	234212,
	234213,
	234214,
	234215,
	234216,
	234217,
	234218,
	234219,
	234220,
	234221,
	234222,
	234223,
	234224,
	234225,
	234226,
	234227,
	234228,
	234229,
	234230,
	234231,
	234232,
	234233,
	234234,
	234235,
	234236,
	234237,
	234238,
	234239,
	234240,
	234241,
	234242,
	234243,
	234244,
	234245,
	234246,
	234247,
	234248,
	234249,
	234250,
	234251,
	234252,
	234253,
	234254,
	234255,
	234256,
	234257,
	234258,
	234259,
	234260,
	234261,
	234262,
	234263,
	234264,
	234265,
	234266,
	234267,
	234268,
	234269,
	234270,
	234271,
	234272,
	234273,
	234274,
	234275,
	234276,
	234277,
	234278,
	234279,
	234280,
	234281,
	234282,
	234283,
	234284,
	234285,
	234286,
	234287,
	234288,
	234289,
	234290,
	234291,
	234292,
	234293,
	234294,
	234295,
	234296,
	234297,
	234298,
	234299,
	234300,
	234301,
	234302,
	234303,
	234304,
	234305,
	234306,
	234307,
	234308,
	234309,
	234310,
	234311,
	234312,
	234313,
	234314,
	234315,
	234316,
	234317,
	234318,
	234319,
	234320,
	234321,
	234322,
	234323,
	234324,
	234325,
	234326,
	234327,
	234328,
	234329,
	234330,
	234331,
	234332,
	234333,
	234334,
	234335,
	234336,
	234337,
	234338,
	234339,
	234340,
	234341,
	234342,
	234343,
	234344,
	234345,
	234346,
	234347,
	234348,
	234349,
	234350,
	234351,
	234352,
	234353,
	234354,
	234355,
	234356,
	234357,
	234358,
	234359,
	234360,
	234361,
	234362,
	234363,
	234364,
	234365,
	234366,
	234367,
	234368,
	234369,
	234370,
	234371,
	234372,
	234373,
	234374,
	234375,
	234376,
	234377,
	234378,
	234379,
	234380,
	234381,
	234382,
	234383,
	234384,
	234385,
	234386,
	234387,
	234388,
	234389,
	234390,
	234391,
	234392,
	234393,
	234394,
	234395,
	234396,
	234397,
	234398,
	234399,
	200610,
	200611,
	200612,
	200613,
	200614,
	200615,
	200616,
	36022,
	36023,
	36026,
	36027,
	36030,
	36031,
	36034,
	36035,
	37004,
	37005,
	37006,
	37007,
	37012,
	37013,
	37014,
	37015,
	37020,
	37021,
	37022,
	37023,
	71996,
	71997,
	71998,
	71999,
	24052,
	24053,
	24056,
	24057,
	24060,
	24061,
	234400,
	234401,
	234402,
	234403,
	234404,
	234405,
	234406,
	234407,
	234408,
	234409,
	234410,
	234411,
	234412,
	234413,
	234414,
	234415,
	234416,
	234417,
	234418,
	234419,
	234420,
	234421,
	234422,
	234423,
	234424,
	234425,
	234426,
	234427,
	234428,
	234429,
	234430,
	234431,
	234432,
	234433,
	234434,
	234435,
	234436,
	234437,
	234438,
	234439,
	234440,
	234441,
	234442,
	234443,
	234444,
	234445,
	234446,
	234447,
	234448,
	234449,
	224200,
	224201,
	224202,
	224203,
	224204,
	224205,
	224206,
	224207,
	224208,
	224209,
	224210,
	224211,
	224212,
	224213,
	224214,
	224215,
	224216,
	224217,
	201008,
	201009,
	201010,
	201011,
	201012,
	201013,
	201014,
	201015,
	201024,
	201025,
	201026,
	201027,
	201028,
	201029,
	201030,
	201031,
	201040,
	201041,
	201042,
	201043,
	201044,
	201045,
	201046,
	201047,
	201056,
	201057,
	201058,
	201059,
	201060,
	201061,
	201062,
	201063,
	201072,
	201073,
	201074,
	201075,
	201076,
	201077,
	201078,
	201079,
]

SERVER_SELECTED = 0

REG_PATH = r"SOFTWARE\UserData\Lightwork"
import _winreg

def SetReg(name, value):
	try:
		_winreg.CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
		registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0, _winreg.KEY_WRITE)
		_winreg.SetValueEx(registry_key, name, 0, _winreg.REG_SZ, value)
		_winreg.CloseKey(registry_key)
		return True
	except WindowsError:
		return False

def GetReg(name):
	try:
		registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0, _winreg.KEY_READ)
		value, regtype = _winreg.QueryValueEx(registry_key, name)
		_winreg.CloseKey(registry_key)
		return value
	except WindowsError:
		return None
