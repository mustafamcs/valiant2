import app

AUTOBAN_QUIZ_ANSWER = "ANSWER"
AUTOBAN_QUIZ_REFRESH = "REFRESH"
AUTOBAN_QUIZ_REST_TIME = "REST_TIME"

OPTION_SHADOW = "SHADOW"
OPTION_TILING = "GPU"
OPTION_TILING_APPLY = "OK"
OPTION_TILING_CPU = "CPU"
OPTION_TILING_GPU = "GPU"
CUBE_INFO_TITLE = "Recipe"
CUBE_REQUIRE_MATERIAL = "Requirements"
CUBE_REQUIRE_MATERIAL_OR = "or"
SAVE_ACCOUNT_CONNECT2 = "|cffFF0000|hF{}|r {}"
SAVE_ACCOUNT_TITLE = "Hesap Kayit"
SAVE_ACCOUNT_SAVE = "Kaydet"
SAVE_ACCOUNT_CONNECT = "Baglan #{}"
SAVE_ACCOUNT_REMOVE = "Sil"

CODEPAGE = str(app.GetDefaultCodePage())

def LoadLocaleFile(srcFileName, localeDict):
	try:
		lines = open(srcFileName, "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoaduiScriptLocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		tokens = line[:-1].split("\t")

		if len(tokens) >= 2:
			localeDict[tokens[0]] = tokens[1]

		else:
			pass

name = app.GetLocalePath()

LOCALE_UISCRIPT_PATH = "locale/common/ui/"
LOGIN_PATH = "locale/common/ui/login/"
EMPIRE_PATH = "locale/common/ui/empire/"
GUILD_PATH = "locale/common/ui/guild/"
SELECT_PATH = "locale/common/ui/select/"
WINDOWS_PATH = "locale/common/ui/windows/"
MAPNAME_PATH = "locale/common/ui/mapname/"
# MAPNAME_PATH = "%s/ui/mapname/" % (name)

JOBDESC_WARRIOR_PATH = "%s/jobdesc_warrior.txt" % (name)
JOBDESC_ASSASSIN_PATH = "%s/jobdesc_assassin.txt" % (name)
JOBDESC_SURA_PATH = "%s/jobdesc_sura.txt" % (name)
JOBDESC_SHAMAN_PATH = "%s/jobdesc_shaman.txt" % (name)
if app.ENABLE_WOLFMAN_CHARACTER:
	JOBDESC_WOLFMAN_PATH = "%s/jobdesc_wolfman.txt" % (name)

EMPIREDESC_A = "%s/empiredesc_a.txt" % (name)
EMPIREDESC_B = "%s/empiredesc_b.txt" % (name)
EMPIREDESC_C = "%s/empiredesc_c.txt" % (name)

LOCALE_INTERFACE_FILE_NAME = "%s/locale_interface.txt" % (name)
LOCALE_INTERFACE_FILE_NAME_CUSTOM = "%s/locale_interface_custom.txt" % (name)

LoadLocaleFile(LOCALE_INTERFACE_FILE_NAME, locals())
LoadLocaleFile(LOCALE_INTERFACE_FILE_NAME_CUSTOM, locals())

if app.ENABLE_MINI_GAME_OKEY_NORMAL:
	MINIGAME_RUMI_DESC = "%s/mini_game_okey_desc.txt" % (name)

if app.ENABLE_MINI_GAME_CATCH_KING:
	MINIGAME_CATCH_KING_DESC = "%s/catchking_event_desc.txt" % (name)
	MINIGAME_CATCH_KING_SIMPLE_DESC = "%s/catchking_event_simple_desc.txt" % (name)
