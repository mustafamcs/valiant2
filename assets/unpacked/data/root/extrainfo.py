import app
import localeInfo

ENABLE_INVENTORY_SIDEBAR = 1 if (app.ENABLE_SPECIAL_STORAGE or app.ENABLE_SWITCHBOT or app.ENABLE_BIOLOG_SYSTEM or app.ENABLE_DISTANCE_NPC or app.ENABLE_OFFLINE_SHOP) else 0

if app.ENABLE_ALIGNMENT_SYSTEM:
	TITLE_NAME_LIST = (
		localeInfo.PVP_LEVEL0,
		localeInfo.PVP_LEVEL1,
		localeInfo.PVP_LEVEL2,
		localeInfo.PVP_LEVEL3,
		localeInfo.PVP_LEVEL4,
		localeInfo.PVP_LEVEL5,
		localeInfo.PVP_LEVEL6,
		localeInfo.PVP_LEVEL7,
		localeInfo.PVP_LEVEL8,
		localeInfo.PVP_LEVEL9,
		localeInfo.PVP_LEVEL10,
		localeInfo.PVP_LEVEL11,
		localeInfo.PVP_LEVEL12,
		localeInfo.PVP_LEVEL13
	)

	TITLE_COLOR_DICT = (
		(0, 204, 255),
		(0, 204, 255),
		(0, 204, 255),
		(0, 204, 255),
		(0, 204, 255),
		(0, 204, 255),
		(0, 144, 255),
		(92, 110, 255),
		(155, 155, 255),
		(255, 255, 255),
		(207, 117, 0),
		(235, 83, 0),
		(227, 0, 0),
		(255, 0, 0)
	)
else:
	TITLE_NAME_LIST = (
		localeInfo.PVP_LEVEL5,
		localeInfo.PVP_LEVEL6,
		localeInfo.PVP_LEVEL7,
		localeInfo.PVP_LEVEL8,
		localeInfo.PVP_LEVEL9,
		localeInfo.PVP_LEVEL10,
		localeInfo.PVP_LEVEL11,
		localeInfo.PVP_LEVEL12,
		localeInfo.PVP_LEVEL13
	)

	TITLE_COLOR_DICT = (
		(0, 204, 255),
		(0, 144, 255),
		(92, 110, 255),
		(155, 155, 255),
		(255, 255, 255),
		(207, 117, 0),
		(235, 83, 0),
		(227, 0, 0),
		(255, 0, 0)
	)