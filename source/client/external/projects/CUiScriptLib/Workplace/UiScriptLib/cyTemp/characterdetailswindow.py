# -*- coding: cp949 -*-
#-1050575949
import uiScriptLocale

MAINBOARD_WIDTH = 247
MAINBOARD_HEIGHT = 408

X_OF_STAT_TITLE = 18

IMG_DIR = "d:/ymir work/ui/game/characterdetails/"

window = {
	"name" : "CharacterDetailsWindow",
	"style" : ("float",),
	"x" : 271,
	"y" : (SCREEN_HEIGHT - 398) / 2,
	"width" : MAINBOARD_WIDTH,
	"height" : MAINBOARD_HEIGHT,
	"children" :
	(
		{
			"name" : "MainBoard",
			"type" : "board",
			"x" : 0,
			"y" : 0,
			"width" : MAINBOARD_WIDTH,
			"height" : MAINBOARD_HEIGHT,
			"children" :
			(
				{
					"name" : "bonus_button",
					"type" : "radio_button",
					"x" : 10,
					"y" : 373,
					"text" : uiScriptLocale.PET_INFORMATION_ABILITIES,
					"default_image" :IMG_DIR+"btn_1.png",
					"over_image" :IMG_DIR+"btn_2.png",
					"down_image" :IMG_DIR+"btn_0.png",
				},
				{
					"name" : "stat_button",
					"type" : "radio_button",
					"x" : 130-4,
					"y" : 373,
					"text" : uiScriptLocale.CHARACTER_STATS_PAGE,
					"default_image" :IMG_DIR+"btn_1.png",
					"over_image" :IMG_DIR+"btn_2.png",
					"down_image" :IMG_DIR+"btn_0.png",
				},
				{
					"name" : "search_winodw",
					"type" : "border_a",
					"x" : 10,
					"y" : 10,
					"width" : 227, "height" : 50,
				},
				{
					"name" : "bonus_window",
					"type" : "border_a",
					"x" : 10,
					"y" : 60,
					"width" : 227, "height" : 310,
				},
				{
					"name" : "stat_window",
					"type" : "image",
					"x" : 10,
					"y" : 10,
					"image" :IMG_DIR+"log_bg.png",
				},
			),
		},
	),
}

