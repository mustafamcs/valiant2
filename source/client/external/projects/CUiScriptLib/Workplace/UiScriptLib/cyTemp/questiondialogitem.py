# -*- coding: cp949 -*-
#-1389628854
import uiScriptLocale

window = {
	"name" : "QuestionDialog",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH/2 - 125,
	"y" : SCREEN_HEIGHT/2 - 52,

	"width" : 340,
	"height" : 105,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 340,
			"height" : 105,

			"children" :
			(
				{
					"name" : "message",
					"type" : "text",

					"x" : 0,
					"y" : -50,

					"horizontal_align" : "center",
					"text" : uiScriptLocale.MESSAGE,

					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "message2",
					"type" : "text",

					"x" : 0,
					"y" : 55,

					"horizontal_align" : "center",
					"text" : uiScriptLocale.MESSAGE,

					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "sell",
					"type" : "button",

					"x" : -80,
					"y" : 63,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					# "text" : uiScriptLocale.SHOP_SELL,

					"default_image" : "d:/ymir work/ui/public/destroybutton00.sub",
					"over_image" : "d:/ymir work/ui/public/destroybutton01.sub",
					"down_image" : "d:/ymir work/ui/public/destroybutton02.sub",

				},
				{
					"name" : "destroy",
					"type" : "button",

					"x" : 0,
					"y" : 63,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					# "text" : (uiScriptLocale.EXTENDET_BATTLE_PASS_TYPENAME_1)[:-2],

					"default_image" : "d:/ymir work/ui/public/sellbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/sellbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/sellbutton02.sub",


				},
				{
					"name" : "cancel",
					"type" : "button",

					"x" : 80,
					"y" : 63,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					# "text" : uiScriptLocale.NO,

					"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
					"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
					"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
				},
			),
		},
	),
}
