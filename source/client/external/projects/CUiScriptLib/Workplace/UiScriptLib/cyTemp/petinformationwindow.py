# -*- coding: cp949 -*-
#-2097035368
import uiScriptLocale
import app
LOCALE_PATH = uiScriptLocale.WINDOWS_PATH
ROOT_PATH = "d:/ymir work/ui/game/windows/"
ROOT = "d:/ymir work/ui/game/"
PET_UI_ROOT = "d:/ymir work/ui/pet/"
SMALL_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_00.sub"
MIDDLE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_01.sub"
LARGE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_03.sub"
XLARGE_BUTTON_FILE = "d:/ymir work/ui/public/xlarge_button_03.sub"
BASE_SLOT_FILE = "d:/ymir work/ui/public/slot_base.sub"

if app.ENABLE_PET_ATTR_DETERMINE:
	PET_UI_BG_IMAGE = "d:/ymir work/ui/pet/Pet_UI_bg.tga"
	PET_UI_ITEM_SLOT_Y = 49
	PET_UI_BG_HEIGHT	= 456
else:
	PET_UI_ITEM_SLOT_Y = 55
	PET_UI_BG_HEIGHT	= 416

STAR_ICONBG = "d:/ymir work/ui/pet/star/base.png"
STAR_ICON = "d:/ymir work/ui/pet/star/0.png"
PET_UI_BG_WIDTH		= 352

## Evol Name, Pet Name, Pet Abilities
LONG_LABEL_WIDTH	= 266
LONG_LABEL_HEIGHT	= 19

## Level, exp, age, life
SHORT_LABLE_WIDTH	= 90
SHORT_LABLE_HEIGHT	= 20

## Defence, Magic Defence, HP
MIDDLE_LABLE_WIDTH	= 168
MIDDLE_LABLE_HEIGHT	= 20

## EXP Gague interval
EXP_GAGUE_INTERVAL	= 2
EXP_IMG_WIDTH		= 16
EXP_IMG_HEIGHT		= 16

## TEXT COLOR
GOLD_COLOR	= 0xFFFEE3AE
WHITE_COLOR = 0xFFFFFFFF
	
window = {
	"name" : "PetInformationWindow",
	"style" : ("movable", "float",),
	
	"x" : SCREEN_WIDTH - 176 -200 -146 -145,	## inven x ??g???? ?? ?????.
	"y" : SCREEN_HEIGHT - 37 - 565,				## inven y ??g?? ????.

	"width" : PET_UI_BG_WIDTH,
	"height" : PET_UI_BG_HEIGHT,

	"children" :
	[
		{
			"name" : "board",
			"type" : "window",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : PET_UI_BG_WIDTH,
			"height" : PET_UI_BG_HEIGHT,
			
			"children" :
			[
				## Page Area
				{
					"name" : "PetInfo_Page",
					"type" : "window",
					"style" : ("attach",),
					
					"x" : 0,
					"y" : 0,
					
					"width" : PET_UI_BG_WIDTH,
					"height" : PET_UI_BG_HEIGHT,
					
					"children":
					[
						## Pet UI BG
						{ "name" : "PetInfoUIBG", "type" : "expanded_image", "style" : ("attach",), "x" : 0, "y" : 0, "image" : PET_UI_BG_IMAGE },
						
						## Pet Information Title
						{ 
							"name" : "TitlePetInfoWindow", "type" : "window", "x" : 10, "y" : 10, "width" : PET_UI_BG_WIDTH-10-15, "height" : 15, "style" : ("attach",),
							"children" :
							(
								{"name":"TitleName", "type":"text", "x":0, "y":0, "text":"Evcil hayvan bilgi penceresi", "all_align" : "center"},
							),	
						},
													
						## Close Button
						{ 
							"name" : "ClosePetInfoWndButton", 
							"type" : "button", 
							"x" : PET_UI_BG_WIDTH -10-15, 
							"y" : 10, 
							"tooltip_text" : uiScriptLocale.CLOSE, 
							"default_image" : "d:/ymir work/ui/public/close_button_01.sub",	
							"over_image" : "d:/ymir work/ui/public/close_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/close_button_03.sub",
						},
					
						## UpBringing Pet Item Slot
						{
							"name" : "UpBringing_Pet_Slot",
							"type" : "slot",
							"x" : 25,
							"y" : PET_UI_ITEM_SLOT_Y,
							"width" : 32,
							"height" : 32,
					
							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
						},
						#Pet Star Bg
						{
							"name": "PetStarBg2", "type" : "image", "x" : 9, "y" : 30, "image":STAR_ICON, 
						},
						#Pet Star
						{
							"name" : "PetStarBg", "type" : "image",	"x" : 9, "y" : 30,	"image" :STAR_ICON,
						},

						## Normal Evol Name + Special Evol Name
						{ 
							"name" : "EvolNameWindow", "type" : "window", "x" : 65, "y" : 50, "width" : LONG_LABEL_WIDTH, "height" : LONG_LABEL_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"EvolName", "type":"text", "x":0, "y":0, "text": "Lv. 3 (Special Evolution)", "r":1.0, "g":0.0, "b":0.0, "a":1.0, "all_align" : "center"},
							),	
						},
				
						## Pet Name
						{ 
							"name" : "NameWindow", "type" : "window", "x" : 65, "y" : 75, "width" : LONG_LABEL_WIDTH, "height" : LONG_LABEL_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"PetName", "type":"text", "x":0, "y":0, "text": "Super Baby White Dragon", "r":0.83, "g":0.77, "b":0.73, "a":1.0, "all_align" : "center"},
							),	
						},
				
						## Level Title
						{ 
							"name" : "LevelWindow", "type" : "window", "x" : 28, "y" : 124, "width" : SHORT_LABLE_WIDTH, "height" : SHORT_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"LevelTitle", "type":"text", "x":0, "y":0, "text": "Level", "color":GOLD_COLOR, "all_align" : "center"},
							),	
						},
						## Level Value
						{ 
							"name" : "LevelValueWindow", "type" : "window", "x" : 28, "y" : 124+SHORT_LABLE_HEIGHT+3, "width" : SHORT_LABLE_WIDTH, "height" : SHORT_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"LevelValue", "type":"text", "x":0, "y":0, "text": "", "color":WHITE_COLOR, "all_align" : "center"},
							),	
						},
						## Type Title
						{ 
							"name" : "TypeWindow", "type" : "window", "x" : 28+204, "y" : 124, "width" : SHORT_LABLE_WIDTH, "height" : SHORT_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"TypeTitle", "type":"text", "x":0, "y":0, "text": "Tip Seviyesi", "color":GOLD_COLOR, "all_align" : "center"},
							),	
						},
						## Type Value
						{ 
							"name" : "TypeValueWindow", "type" : "window", "x" : 28+205, "y" : 124+SHORT_LABLE_HEIGHT+3, "width" : SHORT_LABLE_WIDTH, "height" : SHORT_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"PetTypeText", "type":"text", "x":0, "y":0, "text": "", "color":WHITE_COLOR, "all_align" : "center"},
							),	
						},
						## EXP Title
						{ 
							"name" : "ExpWindow", "type" : "window", "x" : 131, "y" : 124, "width" : SHORT_LABLE_WIDTH, "height" : SHORT_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"ExpTitle", "type":"text", "x":0, "y":0, "text": uiScriptLocale.PET_SYSTEM_EXP, "color":GOLD_COLOR, "all_align" : "center"},
							),	
						},
						## EXP Gauge
						{
							"name" : "UpBringing_Pet_EXP_Gauge_Board",
							"type" : "window",
							"style": ("ltr",),
	
							"x" : 131,
							"y" : 149,
				
							"width"		: EXP_IMG_WIDTH * 5 + EXP_GAGUE_INTERVAL * 4,
							"height"	: EXP_IMG_HEIGHT,

							"children" :
							(
								{
									"name" : "UpBringing_Pet_EXPGauge_01",
									"type" : "expanded_image",

									"x" : 0,
									"y" : 0,

									"image" : PET_UI_ROOT + "exp_gauge/exp_on.sub",
								},
								{
									"name" : "UpBringing_Pet_EXPGauge_02",
									"type" : "expanded_image",

									"x" : EXP_IMG_WIDTH + EXP_GAGUE_INTERVAL,
									"y" : 0,

									"image" : PET_UI_ROOT + "exp_gauge/exp_on.sub",
								},
								{
									"name" : "UpBringing_Pet_EXPGauge_03",
									"type" : "expanded_image",

									"x" : EXP_IMG_WIDTH * 2 + EXP_GAGUE_INTERVAL * 2,
									"y" : 0,

									"image" : PET_UI_ROOT + "exp_gauge/exp_on.sub",
								},
								{
									"name" : "UpBringing_Pet_EXPGauge_04",
									"type" : "expanded_image",

									"x" : EXP_IMG_WIDTH * 3 + EXP_GAGUE_INTERVAL * 3,
									"y" : 0,

									"image" : PET_UI_ROOT + "exp_gauge/exp_on.sub",
								},
								{
									"name" : "UpBringing_Pet_EXPGauge_05",
									"type" : "expanded_image",

									"x" : EXP_IMG_WIDTH * 4 + EXP_GAGUE_INTERVAL * 4,
									"y" : 0,

									"image" : PET_UI_ROOT + "exp_gauge/item_exp_on.sub",
								},
							),
						}, #End of EX
			
						## UpBringing Pet Feed Button(evolution)
						{
							"name" : "FeedEvolButton",
							"type" : "toggle_button",

							"x" : 207,
							"y" : 194,

							"default_image" : PET_UI_ROOT + "feed_button/feed_button_default.sub",
							"over_image" : PET_UI_ROOT + "feed_button/feed_button_over.sub",
							"down_image" : PET_UI_ROOT + "feed_button/feed_button_down.sub",
						
							"text" : uiScriptLocale.PET_SYSTEM_EVOLVE,
							"text_color" : GOLD_COLOR,
						},
				
			
						## Pet Abilities
						{ 
							"name" : "AbilitiesWindow", "type" : "window", "x" : 43, "y" : 259, "width" : LONG_LABEL_WIDTH, "height" : LONG_LABEL_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"AbilitiesName", "type":"text", "x":0, "y":0, "text": uiScriptLocale.PET_SYSTEM_BONUSES, "r":1.0, "g":0.0, "b":0.0, "a":1.0, "all_align" : "center"},
							),	
						},
				
						## HP Title
						{ 
							"name" : "HpWindow", "type" : "window", "x" : 20, "y" : 282, "width" : MIDDLE_LABLE_WIDTH, "height" : MIDDLE_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"HpTitle", "type":"text", "x":0, "y":0, "text": uiScriptLocale.PET_SYSTEM_HP, "color":GOLD_COLOR, "all_align" : "center"},
							),	
						},
						## HP Value
						{ 
							"name" : "HpValueWindow", "type" : "window", "x" : 20 + MIDDLE_LABLE_WIDTH, "y" : 282, "width" : MIDDLE_LABLE_WIDTH, "height" : MIDDLE_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"HpValue", "type":"text", "x":0, "y":0, "text": "", "color":WHITE_COLOR, "all_align" : "center"},
							),	
						},
				
						## Defence Title
						{ 
							"name" : "DefWindow", "type" : "window", "x" : 20, "y" : 304, "width" : MIDDLE_LABLE_WIDTH, "height" : MIDDLE_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"DefTitle", "type":"text", "x":0, "y":0, "text": uiScriptLocale.PET_SYSTEM_DEF, "color":GOLD_COLOR, "all_align" : "center"},
							),	
						},
						## Defence Value
						{ 
							"name" : "DefValueWindow", "type" : "window", "x" : 20 + MIDDLE_LABLE_WIDTH, "y" : 304, "width" : MIDDLE_LABLE_WIDTH, "height" : MIDDLE_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"DefValue", "type":"text", "x":0, "y":0, "text": "", "color":WHITE_COLOR, "all_align" : "center"},
							),	
						},
				
						## SP Title
						{ 
							"name" : "SpWindow", "type" : "window", "x" : 20, "y" : 326, "width" : MIDDLE_LABLE_WIDTH, "height" : MIDDLE_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"SpTitle", "type":"text", "x":0, "y":0, "text": uiScriptLocale.PET_SYSTEM_ATTACK, "color":GOLD_COLOR, "all_align" : "center"},
							),
						},
						## SP Value
						{ 
							"name" : "SpValueWindow", "type" : "window", "x" : 20 + MIDDLE_LABLE_WIDTH, "y" : 326, "width" : MIDDLE_LABLE_WIDTH, "height" : MIDDLE_LABLE_HEIGHT, "style" : ("attach",),
							"children" :
							(
								{"name":"SpValue", "type":"text", "x":0, "y":0, "text": "", "color":WHITE_COLOR, "all_align" : "center"},
							),
						},

						# Pet Skill Slot 0
						{
							"name" : "PetSkillSlot0",
							"type" : "slot",
							
							"x" : 8,
							"y" : 365,
							"width" : 10 + 40*8,
							"height" : 32,
							"image" : BASE_SLOT_FILE,

							"slot" : (
							
								{"index":0, "x":10, "y":0, "width":32, "height":32},
								{"index":1, "x":10 + 40, "y":0, "width":32, "height":32},
								{"index":2, "x":10 + 40*2, "y":0, "width":32, "height":32},
								{"index":3, "x":10 + 40*3, "y":0, "width":32, "height":32},
								{"index":4, "x":10 + 40*4, "y":0, "width":32, "height":32},
								{"index":5, "x":10 + 40*5, "y":0, "width":32, "height":32},
								{"index":6, "x":10 + 40*6,  "y":0, "width":32, "height":32},
								{"index":7, "x":10 + 40*7, "y":0, "width":32, "height":32},
								
							),
						},
				
				
			
					], ## End of board window children			
				},
			],
		},
	],
}

if app.ENABLE_PET_ATTR_DETERMINE:
	PET_UI_TAB_X = 13
	PET_UI_TAB_Y = 16
	PET_UI_TAB_WIDTH = 77
	PET_UI_TAB_HEIGHT = 30
	
	#Tab ???	
	window["children"] = window["children"] + [
		{
			"name" : "TabControl",
			"type" : "window",
			
			"x" : 0,
			"y" : PET_UI_BG_HEIGHT - 40 - 8,	#??g?? ??? ???? ???? ??
			
			"width" : PET_UI_BG_WIDTH,
			"height" : 48,				#????? u??
			
			"children" :
			[
				## Tab
				{
					"name" : "Tab_01",
					"type" : "image",
					
					"x" : 0,
					"y" : 0,
					
					"width" : PET_UI_BG_WIDTH,			
					"height" : 48,
					
					"image" : PET_UI_ROOT + "res/tab_1.tga",	
				},
				{
					"name" : "Tab_02",
					"type" : "image",
					
					"x" : 0,
					"y" : 0,
					
					"width" : PET_UI_BG_WIDTH,
					"height" : 48,
					
					"image" : PET_UI_ROOT + "res/tab_2.tga",
				},
				## Button
				{
					"name" : "Tab_Button_01",
					"type" : "radio_button",
					
					"x" : PET_UI_TAB_X,
					"y" : PET_UI_TAB_Y,
					
					"width" : PET_UI_TAB_WIDTH,
					"height" : PET_UI_TAB_HEIGHT,
				},
				{
					"name" : "Tab_Button_02",
					"type" : "radio_button",
					
					"x" : PET_UI_TAB_X + 94,
					"y" : PET_UI_TAB_Y,
					
					"width" : PET_UI_TAB_WIDTH,
					"height" : PET_UI_TAB_HEIGHT,
				},
			 ],	
		},
	]

	#Pet Tip Buton
	window["children"] = window["children"] + [
	## Click DETERMINE Button(DETERMINE)
		{
			"name" : "DetermineButton",
			"type" : "button",

			"x" : 21,
			"y" : 89,
			"width" : 38,
			"height" : 26,

			"default_image" : PET_UI_ROOT + "determine_button/determine_button_default.sub",
			"over_image" : PET_UI_ROOT + "determine_button/determine_button_over.sub",
			"down_image" : PET_UI_ROOT + "determine_button/determine_button_down.sub",
		},

		{
			"name" : "StarButton",
			"type" : "button",

			"x" : 60,
			"y" : 89,
			"width" : 38,
			"height" : 26,

			"default_image" : "d:/ymir work/ui/pet/res/starbutton1.tga",
			"over_image" : "d:/ymir work/ui/pet/res/starbutton2.tga",
			"down_image" : "d:/ymir work/ui/pet/res/starbutton3.tga",
		},]

	#?? ??? ???? ??????
	window["children"] = window["children"] + [
		{
			"name" : "PetAttrChange_Page",
			"type" : "window",
			"style" : ("attach",),
			
			"x" : 0,
			"y" : 0,
			
			"width" : 352,
			"height" : 408,
			
			"children" :
			[
				## Pet Attr Change UI BG
				{ "name" : "PetAttrChangeUIBG", "type" : "expanded_image", "style" : ("attach",), "x" : 0, "y" : 0, "image" : "d:/ymir work/ui/pet/Pet_UI_bg2.tga" },
				
				## Pet Information Title
				{ 
					"name" : "TitleAttrChangeWindow", "type" : "window", "x" : 10, "y" : 10, "width" : PET_UI_BG_WIDTH-10-15, "height" : 15, "style" : ("attach",),
					"children" :
					(
						{"name":"TitleName", "type":"text", "x":0, "y":0, "text":"Pet", "all_align" : "center"},
					),	
				},
				
				## Close Button
				{ 
					"name" : "ClosePetChangeWndButton", 
					"type" : "button", 
					"x" : PET_UI_BG_WIDTH -10-15, 
					"y" : 10, 
					"tooltip_text" : uiScriptLocale.CLOSE, 
					"default_image" : "d:/ymir work/ui/public/close_button_01.sub",	
					"over_image" : "d:/ymir work/ui/public/close_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/close_button_03.sub",
				},	
				
				## Pet Attr Change Title
				{ 
					"name" : "Pet_Attr_Change_Title", "type" : "window", "x" : 142, "y" : 41, "width" : 70, "height" : 11, "style" : ("attach",),
					"children" :
					(
						{"name":"PetAttrChangeTitle", "type":"text", "x":0, "y":0, "text": uiScriptLocale.PET_ATTR_CHANGE_TITLE, "r":0.85, "g":0.85, "b":0.85, "a":1.0, "all_align" : "center"},
					),	
				},
				
				## UpBringing Pet Item Slot
				{
					"name" : "Change_Pet_Slot",
					"type" : "slot",
					"x" : 160,
					"y" : 67,
					"width" : 32,
					"height" : 173,
					"slot" : (
						{"index":0, "x":0, "y":0, "width":32, "height":32},	#Pet
						{"index":1, "x":0, "y":69, "width":32, "height":32}, # Pet change item 
						{"index":2, "x":0, "y":140, "width":32, "height":32}, # New Pet
					),
				},


				## Change Pet Text
				{ 
					"name" : "Change_Pet_Text", "type" : "window", "x" : 151, "y" : 112, "width" : 53, "height" : 11, "style" : ("attach",),
					"children" :
					(
						{"name":"ChangePetText", "type":"text", "x":0, "y":0, "text": uiScriptLocale.PET_CHANGE_TEXT, "color":WHITE_COLOR, "all_align" : "center"},
					),	
				},

				## Attr Change Item Text
				{ 
					"name" : "Attr_Change_Item_Text", "type" : "window", "x" : 133, "y" : 181, "width" : 90, "height" : 11, "style" : ("attach",),
					"children" :
					(
						{"name":"AttrChangeItemText", "type":"text", "x":0, "y":0, "text": uiScriptLocale.PET_ATTR_CHANGE_ITEM_TEXT, "color":WHITE_COLOR, "all_align" : "center"},
					),	
				},

				## Attr Change Result Text
				{ 
					"name" : "Attr_Change_Result_Text", "type" : "window", "x" : 166, "y" : 254, "width" : 23, "height" : 11, "style" : ("attach",),
					"children" :
					(
						{"name":"AttrChangeResultText", "type":"text", "x":0, "y":0, "text": uiScriptLocale.ACCE_RESULT, "color":WHITE_COLOR, "all_align" : "center"},
					),	
				},
				
				## Pet Determine Info Title
				{ 
					"name" : "Pet_Determine_Info_Title", "type" : "window", "x" : 142, "y" : 292, "width" : 70, "height" : 11, "style" : ("attach",),
					"children" :
					(
						{"name":"PetDetermineInfoTitle", "type":"text", "x":0, "y":0, "text": uiScriptLocale.PET_ATTR_DETERMINE_TITLE, "color":GOLD_COLOR, "all_align" : "center"},
					),	
				},
				
				## Pet Determine Info Text1
				{ 
					"name" : "Pet_Determine_Info_Text", "type" : "window", "x" : 70, "y" : 333, "width" : 200, "height" : 11, "style" : ("attach",),
					"children" :
					(
						{"name":"PetDetermineInfoText", "type":"text", "x":0, "y":-15, "text": " ", "color":WHITE_COLOR, "all_align" : "center"},
						{"name":"PetDetermineInfoText2", "type":"text", "x":0, "y":0, "text": " ", "color":WHITE_COLOR, "all_align" : "center"},
						{"name":"PetDetermineInfoText3", "type":"text", "x":0, "y":15, "text": " ", "color":WHITE_COLOR, "all_align" : "center"},
					),	
				},		
				
				## Pet Change Button
				{
					"name" : "Pet_Change_Button",
					"type" : "button",

					"x" : 25,
					"y" : 379,

					"default_image" : PET_UI_ROOT + "feed_button/feed_button_default.sub",
					"over_image" : PET_UI_ROOT + "feed_button/feed_button_over.sub",
					"down_image" : PET_UI_ROOT + "feed_button/feed_button_down.sub",
			
					"text" : uiScriptLocale.PET_ATTR_CONFIRMATION,
					"text_color" : GOLD_COLOR,
				},
				
				## Pet OK Button
				{
					"name" : "Pet_OK_Button",
					"type" : "button",

					"x" : 205,
					"y" : 379,

					"default_image" : PET_UI_ROOT + "feed_button/feed_button_default.sub",
					"over_image" : PET_UI_ROOT + "feed_button/feed_button_over.sub",
					"down_image" : PET_UI_ROOT + "feed_button/feed_button_down.sub",
			
					"text" : uiScriptLocale.PET_ATTR_OK,
					"text_color" : GOLD_COLOR,
				},
			],	
		},]
	

