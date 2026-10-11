import uiScriptLocale

IMG_DIR = "d:/ymir work/ui/game/gameoption/"

TITLE_IMAGE_TEXT_X = 5
TITLE_IMAGE_TEXT_Y = 4

OPTION_START_X = 17
SLIDER_POSITION_X = 50

SLIDER_START_Y = 40
BUTTON_START_Y = 33
BUTTON_NEXT_Y = 20

RADIO_BUTTON_RANGE_X = 65
TOGGLE_BUTTON_RANGE_X = 65

RADIO_BUTTON_TEXT_X = 25
TOGGLE_BUTTON_TEXT_X = 20

SMALL_OPTION_HEIGHT = 65
NORMAL_OPTION_HEIGHT = 80
SLIDER_OPTION_HEIGHT = 65

window = {
	"name" : "GameOptionDialog",
	# Dont touch these lines!
	"style" : (),
	"x" : 171,
	"y" : 3,
	"width" : 300,
	"height" : 324,
	# Dont touch these lines!
	"children" :
	(
		{
			"name" : "show_name_window",
			"type" : "window",
			"x" : 0,
			"y" : 0,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "show_name_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_show_name",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_ALWAYS_SHOW_NAME,
						},
					),
				},
				{
					"name" : "always_show_name_on_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "always_show_name_off_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

			),
		},
		{
			"name" : "outline_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "outline_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_outline",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_OUTLINE_TEXT,
						},
					),
				},
				{
					"name" : "outline_on_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "outline_off_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},
		{
			"name" : "entity_range_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*2,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "entity_range_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "entity_range_outline",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_ENTITY_RANGE,
						},
					),
				},
				{
					"name" : "entity_range_short_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_ENTITY_RANGE0,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "entity_range_normal_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_ENTITY_RANGE1,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
				{
					"name" : "entity_range_far_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_ENTITY_RANGE2,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},
		{
			"name" : "affect_icons_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*3,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "affect_icons_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_affect_icons",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_AFFECT_TEXT,
						},
					),
				},
				{
					"name" : "show_affect_icons",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "hide_affect_icons",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},
		{
			"name" : "highlight_state_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*4,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "highlight_state_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_highlight_state",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_HIGHLIGHT_TEXT,
						},
					),
				},
				{
					"name" : "show_highlight_new_items",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "hide_highlight_new_items",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},
		{
			"name" : "effects_state_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "effects_state_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_effects_state",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_EFFECT_TEXT,
						},
					),
				},
				{
					"name" : "show_effects",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "hide_effects",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SALESTEXT_VIEW_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},
		{
			"name" : "shadow_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*6,
			"width":304,
			"height":NORMAL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "shadow_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "shadow_quality_title",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_SHADOW_QUALITY,
						},
					),
				},
				{
					"name" : "shadow_off",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SHADOW_QUALITY_BAD,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "shadow_normal",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SHADOW_QUALITY_AVERAGE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
				{
					"name" : "shadow_high",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SHADOW_QUALITY_GOOD,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},
		# {
		# 	"name" : "object_scale_window",
		# 	"type" : "window",
		# 	"x" : 0,
		# 	"y" : SMALL_OPTION_HEIGHT*7,
		# 	"width":304,
		# 	"height":SLIDER_OPTION_HEIGHT,
		# 	"children":
		# 	(
		# 		{
		# 			"name" : "object_scale_title_img",
		# 			"type" : "expanded_image",
		# 			"x" : 0,
		# 			"y" : 0,
		# 			"image" : IMG_DIR+"option_title.png",
		# 			"children":
		# 			(
		# 				{
		# 					"name" : "object_scale",
		# 					"type" : "text",
		# 					"x" : TITLE_IMAGE_TEXT_X+5,
		# 					"y" : TITLE_IMAGE_TEXT_Y,
		# 					"text_horizontal_align":"left",
		# 					"text" : uiScriptLocale.GAMEOPTION_OBJECT_SCALE,
		# 				},
		# 			),
		# 		},
		# 		{
		# 			"name" : "object_distance_scale",
		# 			"type" : "newsliderbar",
		# 			"x" : OPTION_START_X+SLIDER_POSITION_X,
		# 			"y" : SLIDER_START_Y,
		# 		},
		# 	),
		# },
		{
			"name" : "hide_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*7,
			"width":304,
			"height":NORMAL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "hide_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "hide_block",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_HIDE_TEXT,
						},
					),
				},
				{
					"name" : "hide_mount",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X*0 + 20,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_HIDE_MOUNT,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "hide_pet",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X*1 + 40,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_HIDE_PET,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "hide_npc",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X*0 + 20,
					"y" : 33+20,
					"text" : uiScriptLocale.GAMEOPTION_HIDE_NPC,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "hide_shops",
					"type" : "toggle_button",
					"x" : OPTION_START_X+TOGGLE_BUTTON_RANGE_X*1 + 40,
					"y" : 33+20,
					"text" : uiScriptLocale.GAMEOPTION_HIDE_SHOPS,
					"text_x" : TOGGLE_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
			),
		},
	),
}
