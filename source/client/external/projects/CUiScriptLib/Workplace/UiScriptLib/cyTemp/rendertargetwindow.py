# -*- coding: cp949 -*-
#-946497028
import localeInfo

WINDOW_WIDTH = 410
WINDOW_HEIGHT = 440

RENDER_TARGET_INDEX = 1

window = {
	"name" : "RenderTargetWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children":
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : WINDOW_WIDTH - 15,
					"color" : "yellow",

					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",

							"x" : (WINDOW_WIDTH - 15) / 2,
							"y" : 3,

							"text" : localeInfo.MODEL_PREVIEW,
							"text_horizontal_align":"center"
						},
					),
				},

				# RenderView
				{
					"name" : "RenderTarget",
					"type" : "render_target",
					"style" : ("attach",),

					"x" : 10,
					"y" : 30,

					"width" : 390,
					"height" : 400,

					"index" : RENDER_TARGET_INDEX,
				},
			),
		},
	),
}
