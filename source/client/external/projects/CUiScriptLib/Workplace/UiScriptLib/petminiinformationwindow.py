import uiScriptLocale

LOCALE_PATH = uiScriptLocale.WINDOWS_PATH
ROOT_PATH = "d:/ymir work/ui/game/windows/"
ROOT = "d:/ymir work/ui/game/"
PET_UI_ROOT = "d:/ymir work/ui/pet/"

MINI_WINDOW_WIDTH	= 111
MINI_WINDOW_HEIGHT	= 44

## Slot File
BASE_SLOT_FILE = "d:/ymir work/ui/public/slot_base.sub"
PET_MINI_INFO_SLOT_FILE = "d:/ymir work/ui/pet/mini_window/pet_slot_corver.sub"

## EXP Gague interval
EXP_GAGUE_INTERVAL	= 2
EXP_GAGUE_SCALE		= 0.8
EXP_IMG_WIDTH		= 16 * EXP_GAGUE_SCALE
EXP_IMG_HEIGHT		= 16 * EXP_GAGUE_SCALE

##LifeTime Gauge
LIFE_TIME_SCALE_X	= 0.536
LIFE_TIME_SCALE_Y	= 0.636

## Skill Slot
SKILL_SLOT_SCALE_X  = 0.5
SKILL_SLOT_SCALE_Y  = 0.5

window = {
	"name" : "PetMiniInformationWindow",
	"style" : ("movable", "float",),
	
	"x" : 10,
	"y" : SCREEN_HEIGHT - 150,	

	"width" : MINI_WINDOW_WIDTH,
	"height" : MINI_WINDOW_HEIGHT,
	
	"children" :
	(
		## Pet Mini Information Window Back Ground
		{
			"name" : "main_bg",
			"type" : "expanded_image",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,
			
			"image" : "d:/ymir work/ui/pet/mini_window/pet_mini_info_back.sub",

			"width" : MINI_WINDOW_WIDTH,
			"height" : MINI_WINDOW_HEIGHT,
		},
		
		## Icon Slot
		{
			"name" : "icon_base",
			"type" : "window",
			"style" : ("attach",),
			
			"x" : 0,
			"y" : 0,
			
			"width" : 32 + 3,
			"height" : MINI_WINDOW_HEIGHT,
			
			"children" :
			(
				## Main Slot Img
				{
					"name" : "main_slot_img",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x" : 3,
					"y" : 3,
					
					"image" : PET_MINI_INFO_SLOT_FILE,

					"width" : 32,
					"height" : 38,
				},
				
				## Main Slot
				{
					"name" : "pet_icon_slot",
					"type" : "slot",
					#"style" : ("attach",),

					"x" : 3,
					"y" : 6,
					"width"	: 35,
					"height" : MINI_WINDOW_HEIGHT,
					"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32,},),
				},
				
				## Main Slot Effect
				{
					"name" : "pet_icon_slot_ani_img",
					"type" : "ani_image",
					"style" : ("attach",),
					
					"x" : 3,
					"y" : 3,
					
					"delay" : 6,

					"images" :
					(
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect1.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect2.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect3.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect4.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect5.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect6.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect6.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect6.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect5.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect4.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect3.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect2.sub",
						"D:/Ymir Work/UI/pet/mini_window/main_slot_effect/main_slot_effect1.sub",						
					),
				},
			),
		},		
		
		## EXP Gauge
		{
			"name" : "pet_mini_info_exp_gauge_board",
			"type" : "window",
			"style": ("ltr",),

			"x" : 36,
			"y" : 15,
		
			"width"		: 72,
			"height"	: 13,

			"children" :
			(
				{
					"name" : "pet_mini_EXPGauge_01",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x_scale" : EXP_GAGUE_SCALE,
					"y_scale" : EXP_GAGUE_SCALE,
					
					"x" : 0,
					"y" : 0,

					"image" : PET_UI_ROOT + "exp_gauge/exp_on.sub",
				},
				{
					"name" : "pet_mini_EXPGauge_02",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x_scale" : EXP_GAGUE_SCALE,
					"y_scale" : EXP_GAGUE_SCALE,
					
					"x" : EXP_IMG_WIDTH + EXP_GAGUE_INTERVAL,
					"y" : 0,
					
					"image" : PET_UI_ROOT + "exp_gauge/exp_on.sub",
				},
				{
					"name" : "pet_mini_EXPGauge_03",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x_scale" : EXP_GAGUE_SCALE,
					"y_scale" : EXP_GAGUE_SCALE,					

					"x" : EXP_IMG_WIDTH * 2 + EXP_GAGUE_INTERVAL * 2,
					"y" : 0,

					"image" : PET_UI_ROOT + "exp_gauge/exp_on.sub",
				},
				{
					"name" : "pet_mini_EXPGauge_04",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x_scale" : EXP_GAGUE_SCALE,
					"y_scale" : EXP_GAGUE_SCALE,
					
					"x" : EXP_IMG_WIDTH * 3 + EXP_GAGUE_INTERVAL * 3,
					"y" : 0,

					"image" : PET_UI_ROOT + "exp_gauge/exp_on.sub",
				},
				{
					"name" : "pet_mini_EXPGauge_05",
					"type" : "expanded_image",
					"style" : ("attach",),

					"x_scale" : EXP_GAGUE_SCALE,
					"y_scale" : EXP_GAGUE_SCALE,
					
					"x" : EXP_IMG_WIDTH * 4 + EXP_GAGUE_INTERVAL * 4,
					"y" : 0,

					"image" : PET_UI_ROOT + "exp_gauge/item_exp_on.sub",
				},
			),
		}, #End of EXP
	
		{
			"name" : "pet_mini_info_exp_gauge_board1",
			"type" : "window",
			"style": ("ltr",),

			"x" : 36,
			"y" : 15,
		
			"width"		: 72,
			"height"	: 13,
		},
		
	),
}
