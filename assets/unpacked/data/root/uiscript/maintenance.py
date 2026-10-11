import uiScriptLocale
import localeInfo
ROOT = "d:/ymir work/maintenance/"

BOARD_WIDTH = 283
BOARD_HEIGHT = 99

window = {
	"name" : "MaintenanceWindow",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH-430,
	"y" : 40,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "Thinboard",
			"type" : "image",

			"x" : 0,
			"y" : 0,
			"width" : 264,
			"height" : 85,

			"image" : ROOT + "bg.png",

			"children" :
			(
				{
					"name" : "maintitle",
					"type" : "text",

					"x" : 0,
					"y" : 10,

					"color" : 0xfff8d090,

					"text" : localeInfo.MAINTENANCE_TITLE,
					"fontname" : "Verdana:12",
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "message1",
					"type" : "text",

					"x" : 0,
					"y" : 30,

					"text" : uiScriptLocale.MESSAGE,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "message2",
					"type" : "text",

					"x" : 0,
					"y" : 50,

					"text" : "Check our discord for details!",

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "message3",
					"type" : "text",

					"x" : 0,
					"y" : 80,

					"text" : "Check our discord for details!",

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
			),
		},
	),
}