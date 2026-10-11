# -*- coding: cp949 -*-
#-2004043981
ROOT = "d:/ymir work/maintenance/"

BOARD_WIDTH = 283
BOARD_HEIGHT = 63

window = {
	"name" : "MaintenanceWindow",
	"style" : ("float",),

	"x" : SCREEN_WIDTH / 2 - 283 / 2,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "image",

			"x" : 0,
			"y" : 0,

			"image" : ROOT + "bg.tga",

			"children" :
			(
				{
					"name" : "close",
					"type" : "button",

					"x" : 8 + 10,
					"y" : 5,

					"horizontal_align" : "right",

					"default_image" : ROOT + "cancel_button.tga",
					"over_image" : ROOT + "cancel_button_hover.tga",
					"down_image" : ROOT + "cancel_button_select.tga",
				},
				{
					"name" : "remaining_time",
					"type" : "text",

					"x" : 0,
					"y" : 5,

					"horizontal_align" : "center",
				},
				{
					"name" : "cause",
					"type" : "text",

					"x" : 0,
					"y" : 25,

					"horizontal_align" : "center",
				},
				{
					"name" : "duration",
					"type" : "text",

					"x" : 0,
					"y" : 45,

					"horizontal_align" : "center",
				},
			),
		},
	),
}

