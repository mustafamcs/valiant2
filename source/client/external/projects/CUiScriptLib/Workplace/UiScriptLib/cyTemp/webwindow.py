# -*- coding: cp949 -*-
#-1335634280
WEB_WIDTH = 800
WEB_HEIGHT = 600

window = {
	"name" : "MallWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width"  : WEB_WIDTH  + 20,
	"height" : WEB_HEIGHT + 40,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width"	 : WEB_WIDTH  + 20,
			"height" : WEB_HEIGHT + 40,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : WEB_WIDTH + 10,
					"color" : "yellow",

					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":3,
						"text" : "Web Window",
						"horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},
			),
		},
	),
}

