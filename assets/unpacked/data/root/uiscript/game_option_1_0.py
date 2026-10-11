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
					"name" : "show_damage_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_show_damage",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_EFFECT,
						},
					),
				},
				{
					"name" : "show_damage_on_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_VIEW_CHAT_ON,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "show_damage_off_button",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_VIEW_CHAT_OFF,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},
		{
			"name" : "camera_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "camera_mode_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_camera_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
						},
					),
				},
				{
					"name" : "camera_short",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
				{
					"name" : "camera_long",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},
		{
			"name" : "fog_mode_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*2,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "fog_mode_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_fog_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_FOG,
						},
					),
				},
				{
					"name" : "fog_level0",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_FOG_DENSE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
				{
					"name" : "fog_level1",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_FOG_MIDDLE,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
				{
					"name" : "fog_level2",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_FOG_LIGHT,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},
		{
			"name" : "fov_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*3,
			"width":304,
			"height":SLIDER_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "fov_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "fov_sound",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_FOV,
						},
					),
				},
				{
					"name" : "fov_controller",
					"type" : "newsliderbar",
					"x" : OPTION_START_X+SLIDER_POSITION_X,
					"y" : SLIDER_START_Y,
				},
			),
		},
		{
			"name" : "damage_type_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*4,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "damage_type_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "damage_type",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_DAMAGE_TYPE,
						},
					),
				},
				{
					"name" : "damage_type_normal",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_DAMAGE_TYPE0,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "damage_type_dotted",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_DAMAGE_TYPE1,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "damage_type_with_letter",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_DAMAGE_TYPE2,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},

		{
			"name" : "damage_type_renewed_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*5,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "damage_type_renewed_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "damage_type_renewed",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.GAMEOPTION_DAMAGE_RENEWED_TYPE,
						},
					),
				},
				{
					"name" : "damage_type_renewal_normal",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_DAMAGE_RENEWED_TYPE0,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "damage_type_renewal_new",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_DAMAGE_RENEWED_TYPE1,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},


		{
			"name" : "loading_type_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*6,
			"width":304,
			"height":SMALL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "loading_type_title_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "loading_type_Text",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							# "text" : " ",
							"text" : uiScriptLocale.GAMEOPTION_LOADING_TYPE,
						},
					),
				},
				{
					"name" : "loading_type_animated",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.GAMEOPTION_LOADING_TYPE_BUTTON,
					# "text" : " ",
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},

				{
					"name" : "loading_type_normal",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1.5,
					"y" : 33,
					# "text" : "2",
					"text" : uiScriptLocale.GAMEOPTION_LOADING_TYPE_BUTTON2,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : IMG_DIR + "radio_unselected.tga",
					"over_image" : IMG_DIR + "radio_unselected.tga",
					"down_image" : IMG_DIR + "radio_selected.tga",
				},
			),
		},

		{
			"name" : "skybox_window",
			"type" : "window",
			"x" : 0,
			"y" : SMALL_OPTION_HEIGHT*7,
			"width":304,
			"height":NORMAL_OPTION_HEIGHT,
			"children":
			(
				{
					"name" : "skybox_window_img",
					"type" : "expanded_image",
					"x" : 0,
					"y" : 0,
					"image" : IMG_DIR+"option_title.png",
					"children":
					(
						{
							"name" : "title_skybox_mode",
							"type" : "text",
							"x" : TITLE_IMAGE_TEXT_X+5,
							"y" : TITLE_IMAGE_TEXT_Y,
							"text_horizontal_align":"left",
							"text" : uiScriptLocale.OPTION_SKYBOX,
						},
					),
				},
				{
					"name" : "skybox_type_default",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*0,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SKYBOX_0,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "skybox_type_1",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*1,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SKYBOX_1,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "skybox_type_2",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*2,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SKYBOX_2,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "skybox_type_3",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*3,
					"y" : 33,
					"text" : uiScriptLocale.OPTION_SKYBOX_3,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "skybox_type_4",
					"type" : "radio_button",
					"x" : OPTION_START_X,
					"y" : 33+20,
					"text" : uiScriptLocale.OPTION_SKYBOX_4,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "skybox_type_5",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X,
					"y" : 33+20,
					"text" : uiScriptLocale.OPTION_SKYBOX_5,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "skybox_type_6",
					"type" : "radio_button",
					"x" : OPTION_START_X + RADIO_BUTTON_RANGE_X * 2,
					"y" : 33+20,
					"text" : uiScriptLocale.OPTION_SKYBOX_6,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
				{
					"name" : "skybox_type_7",
					"type" : "radio_button",
					"x" : OPTION_START_X+RADIO_BUTTON_RANGE_X*3,
					"y" : 33+20,
					"text" : uiScriptLocale.OPTION_SKYBOX_7,
					"text_x" : RADIO_BUTTON_TEXT_X,
					"default_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"over_image" : "d:/ymir work/ui/game/biolog_system/select_button01.png",
					"down_image" : "d:/ymir work/ui/game/biolog_system/select_button02.png",
				},
			),
		},

	),
}