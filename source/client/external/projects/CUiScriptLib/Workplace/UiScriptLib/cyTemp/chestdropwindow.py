# -*- coding: cp949 -*-
#-34851945
import localeInfo

BUTTON_ROOT = "d:/ymir work/ui/public/"

window = {
	"name" : "ChestDropWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 500,
	"height" : 250,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 500,
			"height" : 250,
		
			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : 500 - 12,					
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x": 250, "y":3, "text": localeInfo.CHEST_PREVIEW, "text_horizontal_align":"center" },
					),
				},
				# {
					# "name" : "test", "type" : "image", "image" : "chest_header.tga",
					# "x" : 10, "y" : 35,
				# },
				{
				 "name" : "circle",
				 "type" : "thinboard_circle",
				 "x" : 10,
				 "y" : 30,
				 "width" : 479,
				 "height" : 42,
				 "children" :
					(
						{ "name":"Title", "type":"text", "x": 0, "y":0, "text": localeInfo.CHEST_PREVIEW, "all_align":"center" },
					),
				},
				{ 
					"name" : "SlotBG", 
					"type" : "expanded_image", 
					"style" : ("attach",), 
					
					"x" : 10, 
					"y" : 31, 
					
					"image" : "d:/ymir work/ui/pet/Pet_Incu_slot_001.tga",
					
					"children" :
					(
						{
							"name" : "OpenItemSlot",
							"type" : "slot",
								
							"x" : 4,
							"y" : 4,
							"width" : 32,
							"height" : 32,
		
							"slot" : (
								{"index":0, "x":0, "y":0, "width":32, "height":32,},
							),
						},
					),
				},
				{
					"name" : "prev_button", 
					"type" : "button",
					
					"x" : 422, 
					"y" : 63+30,

					"default_image" : "d:/ymir work/ui/public/public_page_button/page_first_prev_btn_01.sub",
					"over_image" 	: "d:/ymir work/ui/public/public_page_button/page_first_prev_btn_02.sub",
					"down_image" 	: "d:/ymir work/ui/public/public_page_button/page_first_prev_btn_01.sub",
				},
				
				{
					"name" : "CurrentPageBack",
					"type" : "thinboard_circle",
					
					"x" : 430,
					"y" : 58+30,
					
					"width" : 30,
					"height" : 30,
					
					"children" :
					(
						{
							"name" : "CurrentPage",
							"type" : "text",
							
							"x" : 0,
							"y" : 0,
							
							"vertical_align" : "center",
							"horizontal_align" : "center",
							
							"text_vertical_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "1",
						},
					),
				},
				
				{
					"name" : "next_button", 
					"type" : "button",

					"x" : 475, 
					"y" : 63+30,

					"default_image" : "d:/ymir work/ui/public/public_page_button/page_last_next_btn_01.sub",
					"over_image" 	: "d:/ymir work/ui/public/public_page_button/page_last_next_btn_02.sub",
					"down_image" 	: "d:/ymir work/ui/public/public_page_button/page_last_next_btn_01.sub",
				},
			),
		},
	),
}


