# -*- coding: cp949 -*-
#-696238608
import uiScriptLocale
MAIN_PATH = "d:/ymir work/offlineshop/others/"
window = {
	"name" : "InputDialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 230,
	"height" : 170,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 230,
			"height" : 170,

			"title" : uiScriptLocale.DETERMINE_ITEM_PRICE,

			"children" :
			(

				{
					"name" : "BlackBoard",
					"type" : "thinboard_circle",
					"x" : 68, "y" : 66, "width" : 122, "height" : 92,
				},

				## Input Slot
				{
					"name" : "InputPrice",
					"type" : "image",

					"x" : 3,
					"y" : 35,
					"image" : "d:/ymir work/offlineshop/ae/withdrawbg.png",
					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "InputValue",
							"type" : "editline",

							"x" : 28,
							"y" : 7,

							"width" : 90,
							"height" : 18,

							"input_limit" : 15,
						},
					),
				},

				## Input Slot
				{
					"name" : "MoneyValue",
					"type" : "text",

					"x" : 0,
					"y" : 158,
					"text" : "999999999",
					"text_horizontal_align" : "center",
					"horizontal_align" : "center",
				},

				## Button
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : - 72 + 30,
					"y" : 178,
					"horizontal_align" : "center",

					"text" : uiScriptLocale.OK,

					"default_image" : MAIN_PATH + "buttons/remove_yang_norm.tga",
					"over_image" : MAIN_PATH + "buttons/remove_yang_hover.tga",
					"down_image" : MAIN_PATH + "buttons/remove_yang_down.tga",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 10 + 30,
					"y" : 178,
					"horizontal_align" : "center",

					"text" : uiScriptLocale.CANCEL,

					"default_image" : MAIN_PATH + "buttons/remove_yang_norm.tga",
					"over_image" : MAIN_PATH + "buttons/remove_yang_hover.tga",
					"down_image" : MAIN_PATH + "buttons/remove_yang_down.tga",
				},
			),
		},
	),
}
