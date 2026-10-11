# -*- coding: cp949 -*-
#969511447
import uiScriptLocale, app, localeInfo

randomNum = app.GetRandom(0, 8)

LOCALE_PATH = uiScriptLocale.WINDOWS_PATH
ROOT_PATH = "d:/ymir work/ui/game/miningrenewal/"
WINDOW_WIDTH = 278 + 14
WINDOW_HEIGHT = 226 + 37

window = {
	"name" : "FishingGameWindow",
	"style" : ("movable", "float", "limit", ),
		
	"x" : SCREEN_WIDTH - 176 - 387 - 10-200,
	"y" : SCREEN_HEIGHT - 37 - 525,
	
	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,
	
	"children" :
	[
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("ltr", ),
			
			"x" : 0,
			"y" : 0,
			
			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,
			"title" : localeInfo.MINING_TITLE,
			"children" :
			(
				## BackGround Water
				{
					"name" : "background_cave",
					"type" : "image",
					"style" : ("ltr", ),
					"x" : 7,
					"y" : 29,
					"image" : ROOT_PATH + "fishing_background_water.sub",
					
					"children" :
					(
						
						## Goal Circle
						{
							"name" : "fishing_goal_circle",
							"type" : "image",
							"style" : ("not_pick", "ltr", ),
							"x" : 100,
							"y" : 42,
							"image" : ROOT_PATH + "lode/{}.png".format(randomNum),
						},
					),
				},

				{
					"name" : "fishing_goal_count",
					"type" : "expanded_image",
					"style" : ("not_pick",),
					"x" : 7 + 278 - 73,
					"y" : 29 + 5,
					"image" : ROOT_PATH + "fishing_goal_count.sub",
				},

				{ 
					"name" : "totalPoints",
					"type" : "text",
					"x" : 7 + 278 - 73+45,
					"y" : 29 + 5+8, 
					"text" : "0/100",
					"text_horizontal_align" : "center" 	
				},


				{
					"name" : "fishing_timer_base",
					"type" : "expanded_image",
					"style" : ("not_pick",),
					"x" : 37,
					"y" : 211,
					"image" : ROOT_PATH + "fishing_timer_base.sub",
				},
				## Timer Gauge type expand_image
				{
					"name" : "fishing_timer_gauge",
					"type" : "expanded_image",
					"style" : ("not_pick",),
					"x" : 65,
					"y" : 220,
					"image" : ROOT_PATH + "timer.png",
				},

			),
		},
	],
}
