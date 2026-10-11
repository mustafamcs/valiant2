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
TOGGLE_BUTTON_RANGE_X = 85

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
			"name" : "stone_scale_window",
			"type" : "window",
			"x" : 0,
			"y" : 0,
			"width":304,
			"height":SLIDER_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "stone_scale_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "stone_scale",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_STONE_SCALE,
						},
					),
				},
				{
					"name" : "stone_scale",
					"type" : "newsliderbar",
					"x" : OPTION_START_X+SLIDER_POSITION_X,
					"y" : SLIDER_START_Y,
				},
			),
		},
		{
			"name" : "damage_scale_window",
			"type" : "window",
			"x" : 0,
			"y" : NORMAL_OPTION_HEIGHT,
			"width":304,
			"height":SLIDER_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "damage_scale_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "damage_scale",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_DAMAGE_SCALE,
						},
					),
				},
				{
					"name" : "damage_scale",
					"type" : "newsliderbar",
					"x" : OPTION_START_X+SLIDER_POSITION_X,
					"y" : SLIDER_START_Y,
				},
			),
		},
	),
}