import app
if app.ENABLE_INVENTORY_REWORK:
	import uiScriptLocale
	import item
	import player
	
	EQUIPMENT_START_INDEX = player.EQUIPMENT_SLOT_START
	
	window = {
		"name" : "InventoryWindow",
	
		"x" : SCREEN_WIDTH - 196,
		"y" : SCREEN_HEIGHT - 37 - 543-30,
	
		"style" : ("movable", "float", "window_without_alpha",),
	
		"width" : 196,
		"height" : 543,
	
		"children" :
		(
			## Inventory, Equipment Slots
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),
	
				"x" : 20,
				"y" : 0,
	
				"width" : 176,
				"height" : 543,
	
				"children" :
				(
	
					## Title
					{
						"name" : "TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),
	
						"x" : 8+36,
						"y" : 7,
	
						"width" : 161 - 36,
						"color" : "yellow",
	
						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":77 - 20, "y":4, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center" },
						),
					},
	
					{
						"name" : "SeparateBaseImage",
						"type" : "image",
						"style" : ("attach",),
	
						"x" : 8,
						"y" : 7,
	
						"image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",
	
						"children" :
						(
							# Separate Button (38x24)
							{
								"name" : "arrange_button",
								"type" : "button",
	
								"x" : 11,
								"y" : 3,
	
								"default_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_01.sub",
								"over_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_02.sub",
								"down_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_03.sub",
								"disable_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_04.sub",
							},
						),
					},
	
					{
						"name" : "equipment_window",
						"type" : "window",
						"style" : ("window_without_alpha",),
						
						"x" : -13,
						"y" : 33,
						
						"width" : 178,
						"height" : 187,
						
						"children" :
						[
							## Equipment Slot
							{
								"name" : "Equipment_Base",
								"type" : "expanded_image",
								"style" : ("attach", "window_without_alpha",),
								
								"x" : 0,
								"y" : 0,
	
								"image" : "d:/ymir work/ui/game/inventory/equipment_bg.png",
	
								"children" :
								(
	
									{
										"name" : "Equipments_Slot",
										"type" : "slot",
	
										"x" : 25,
										"y" : 3,
	
										"width" : 172,
										"height" : 182,
	
										"slot" : (
													{"index":item.EQUIPMENT_BODY, "x":39, "y":37, "width":32, "height":64},
													{"index":item.EQUIPMENT_HEAD, "x":39, "y":2, "width":32, "height":32},
													{"index":item.EQUIPMENT_SHOES, "x":39, "y":145, "width":32, "height":32},
													{"index":item.EQUIPMENT_WRIST, "x":75, "y":67, "width":32, "height":32},
													{"index":item.EQUIPMENT_WEAPON, "x":3, "y":3, "width":32, "height":96},
													{"index":item.EQUIPMENT_NECK, "x":114, "y":67, "width":32, "height":32},
													{"index":item.EQUIPMENT_EAR, "x":114, "y":35, "width":32, "height":32},
													{"index":item.EQUIPMENT_ARROW, "x":114, "y":2, "width":32, "height":32},
													{"index":item.EQUIPMENT_SHIELD, "x":75, "y":35, "width":32, "height":32},
													{"index":item.EQUIPMENT_PENDANT, "x":3, "y":106, "width":32, "height":32},
													{"index":item.EQUIPMENT_UNIQUE1, "x":3, "y":144, "width":32, "height":32},
													{"index":item.EQUIPMENT_UNIQUE2, "x":75, "y":144, "width":32, "height":32},
													{"index":item.EQUIPMENT_BELT, "x":39, "y":106, "width":32, "height":32},
													{"index":item.EQUIPMENT_GLOVE, "x":75, "y":106, "width":32, "height":32},
												),
									},
									{
										"name" : "hideCrownBtn",
										"type" : "toggle_button",
	
										"x" : 98-7,
										"y" : 2,
	
	
										# "default_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										# "over_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										# "down_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_03.tga",
									},
									## Dragon Soul Button
									{
										"name" : "DSSButton",
										"type" : "button",
										"x" : 73+64, #114,
										"y" : 107,
	
										"tooltip_text" : uiScriptLocale.DRAGONSOUL_TITLE,
	
										"default_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_01.tga",
										"over_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_02.tga",
										"down_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_03.tga",
									},
									## MallButton
									{
										"name" : "MallButton",
										"type" : "button",
	
										"x" : 73+67,
										"y" : 148,
	
										"tooltip_text" : uiScriptLocale.SPECIAL_INVENTORY_TITLE,
	
										"default_image" : "d:/ymir work/ui/game/taskbar/mall_button_01.tga",
										"over_image" : "d:/ymir work/ui/game/taskbar/mall_button_02.tga",
										"down_image" : "d:/ymir work/ui/game/taskbar/mall_button_03.tga",
									},
								),
							},
						],
					},
	
					{
						"name" : "costume_window",
						"type" : "window",
						"style" : ("window_without_alpha",),
						
						"x" : -13,
						"y" : 33,
						
						"width" : 178,
						"height" : 187,
						
						"children" :
						[
							## Equipment Slot
							{
								"name" : "Costume_Background",
								"type" : "expanded_image",
								"style" : ("attach", "window_without_alpha",),
								
								"x" : 0,
								"y" : 0,
	
								"image" : "d:/ymir work/ui/game/inventory/costume_bg.png",
	
								"children" :
								[
									{
										"name" : "Costumes_Slot",
										"type" : "slot",
	
										"x" : 0,
										"y" : 0,
	
										"width" : 172,
										"height" : 182,
	
										"slot" : (
													{"index":item.EQUIPMENT_COSTUME_WEAPON, "x":67-10, "y":9, "width":32, "height":96}, #silah
													{"index":item.EQUIPMENT_COSTUME_HAIR, "x":105-10, "y":9, "width":32, "height":32}, #saç kostümü
													{"index":item.EQUIPMENT_COSTUME_BODY, "x":105-10, "y":43, "width":32, "height":64}, #zýrh kostümü
	
													{"index":item.EQUIPMENT_NEW_PET, "x":32+5+34*3, "y":43, "width":32, "height":32},
	
													{"index":item.EQUIPMENT_MOUNT, "x":30.6, "y":115, "width":32, "height":32}, #binek
													{"index":item.EQUIPMENT_PET, "x":32+34, "y":115, "width":32, "height":32}, #pet
													{"index":item.EQUIPMENT_ACCE, "x":32+3.5+34*2, "y":115, "width":32, "height":32},#kuþak
													{"index":item.COSTUME_SLOT_AURA, "x":32+5+34*3, "y":115, "width":32, "height":32},#kuþak
				
													{"index":item.MOUNT_SKIN_SLOT, "x":30.6, "y" :151, "width":32, "height":32}, #skin-binek
													{"index":item.PET_SKIN_SLOT, "x":32+34, "y" :151, "width":32, "height":32}, #skin-pet
													{"index":item.COSTUME_SLOT_WING, "x":32+3.5+34*2, "y" :150, "width":32, "height":32}, #skin-kusak
													{"index":item.ITEM_AURA_SKIN_SLOT, "x":32+5+34*3, "y":150, "width":32, "height":32}, #skin-aura
												),
									},
	
									# ENABLE_HIDE_COSTUME_SYSTEM
									{
										"name" : "hideHairCostumeBtn",
										"type" : "toggle_button",
	
										"x" : 85,
										"y" : 7,
	
	
										"default_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"over_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"down_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_03.tga",
									},
									{
										"name" : "hideBodyCostumeBtn",
										"type" : "toggle_button",
	
										"x" : 85,
										"y" : 39,
	
	
										"default_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"over_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"down_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_03.tga",
									},
									{
										"name" : "hideWeaponCostumeBtn",
										"type" : "toggle_button",
	
										"x" : 47,
										"y" : 7,
	
										"default_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"over_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"down_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_03.tga",
									},
									{
										"name" : "hideAcceCostumeBtn",
										"type" : "toggle_button",
	
										"x" : 32+5+34*2-7,
										"y" : 113.3,
	
	
										"default_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"over_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"down_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_03.tga",
									},
									{
										"name" : "hideAuraCostumeBtn",
										"type" : "toggle_button",
	
										"x" : 32+5+34*3-7,
										"y" : 113.3,
	
	
										"default_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"over_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_01.tga",
										"down_image" : "d:/ymir work/ui/game/inventory/button/visible_mark_03.tga",
									},
								],
							},
						],
					},
	
					{
						"name" : "booster_window",
						"type" : "window",
						"style" : ("window_without_alpha",),
						
						"x" : -13,
						"y" : 33,
						
						"width" : 178,
						"height" : 187,
						
						"children" :
						[
							## Equipment Slot
							{
								"name" : "Boosters_Background",
								"type" : "expanded_image",
								"style" : ("attach", "window_without_alpha",),
								
								"x" : 0,
								"y" : 0,
	
								"image" : "d:/ymir work/ui/game/inventory/misc_bg.png",
	
								"children" :
								[
									{
										"name" : "Boosters_Slot",
										"type" : "slot",
	
										"x" : 0,
										"y" : 0,
	
										"width" : 190,
										"height" : 182,
	
										"slot" : (
	
													{"index":item.BOOSTER_SLOT_WEAPON, "x":63, "y":31, "width":32, "height":96},
													{"index":item.BOOSTER_SLOT_BODY, "x":107, "y":27+35, "width":32, "height":64},
													{"index":item.BOOSTER_SLOT_HEAD, "x":107, "y":27, "width":32, "height":32},
	
													{"index":item.RING_SLOT_0, "x":34, "y":139, "width":32, "height":32},
													{"index":item.RING_SLOT_1, "x":34*2, "y":139, "width":32, "height":32},
													{"index":item.RING_SLOT_2, "x":34*3 + 1, "y":139, "width":32, "height":32},
													{"index":item.RING_SLOT_3, "x":34*4 + 2, "y":139, "width":32, "height":32},
	
													# {"index":item.BOOSTER_SLOT_SASH, "x":131, "y":20, "width":32, "height":32},
													# {"index":item.BOOSTER_SLOT_PET, "x":131, "y":20+34*2, "width":32, "height":32},
													# {"index":item.BOOSTER_SLOT_MOUNT, "x":131, "y":20+34, "width":32, "height":32},
	
												),
									},
								],
							},
						],
					},
	
					{
						"name" : "Inventory_Tab_01",
						"type" : "radio_button",
	
						"x" : 7,
						"y" : 33 + 191,
	
						"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1,
	
						"children" :
						(
							{
								"name" : "Inventory_Tab_01_Print",
								"type" : "text",
	
								"x" : 0,
								"y" : 0,
	
								"all_align" : "center",
	
								"text" : "I",
							},
						),
					},
					{
						"name" : "Inventory_Tab_02",
						"type" : "radio_button",
	
						"x" : 7 + 32,
						"y" : 33 + 191,
	
						"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2,
	
						"children" :
						(
							{
								"name" : "Inventory_Tab_02_Print",
								"type" : "text",
	
								"x" : 0,
								"y" : 0,
	
								"all_align" : "center",
	
								"text" : "II",
							},
						),
					},
					{
						"name" : "Inventory_Tab_03",
						"type" : "radio_button",
	
						"x" : 7 + 64,
						"y" : 33 + 191,
	
						"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_3,
	
						"children" :
						(
							{
								"name" : "Inventory_Tab_03_Print",
								"type" : "text",
	
								"x" : 0,
								"y" : 0,
	
								"all_align" : "center",
	
								"text" : "III",
							},
						),
					},
					{
						"name" : "Inventory_Tab_04",
						"type" : "radio_button",
	
						"x" : 7 + 96,
						"y" : 33 + 191,
	
						"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_4,
	
						"children" :
						(
							{
								"name" : "Inventory_Tab_04_Print",
								"type" : "text",
	
								"x" : 0,
								"y" : 0,
	
								"all_align" : "center",
	
								"text" : "IV",
							},
						),
					},
					{
						"name" : "Inventory_Tab_05",
						"type" : "radio_button",
	
						"x" : 7 + 128,
						"y" : 33 + 191,
	
						"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_5,
	
						"children" :
						(
							{
								"name" : "Inventory_Tab_05_Print",
								"type" : "text",
	
								"x" : 0,
								"y" : 0,
	
								"all_align" : "center",
	
								"text" : "V",
							},
						),
					},
	
					## Item Slot
					{
						"name" : "ItemSlot",
						"type" : "grid_table",
	
						"x" : 8,
						"y" : 246,
	
						"start_index" : 0,
						"x_count" : 5,
						"y_count" : 9,
						"x_step" : 32,
						"y_step" : 32,
	
						"image" : "d:/ymir work/ui/public/slot_base.sub"
					},
	
				),
			},
			{
				"name" : "Equipment_Tab_01",
				"type" : "radio_button",
	
				"x" : 5,
				"y" : 33,
	
				"default_image" : "d:/ymir work/ui/game/inventory/button/inv_cat_button.tga",
				"over_image" : "d:/ymir work/ui/game/inventory/button/inv_cat_button.tga",
				"down_image" : "d:/ymir work/ui/game/inventory/button/inv_cat_button.tga",
			},
			{
				"name" : "Equipment_Tab_02",
				"type" : "radio_button",
	
				"x" : 5,
				"y" : 33+22,
	
				"default_image" : "d:/ymir work/ui/game/inventory/button/inv_cat_button.tga",
				"over_image" : "d:/ymir work/ui/game/inventory/button/inv_cat_button.tga",
				"down_image" : "d:/ymir work/ui/game/inventory/button/inv_cat_button.tga",
			},
			{
				"name" : "Equipment_Tab_03",
				"type" : "radio_button",
	
				"x" : 5,
				"y" : 33+22*2,
	
				"default_image" : "d:/ymir work/ui/game/inventory/button/inv_cat_button.tga",
				"over_image" : "d:/ymir work/ui/game/inventory/button/inv_cat_button.tga",
				"down_image" : "d:/ymir work/ui/game/inventory/button/inv_cat_button.tga",
			},
		),
	}
else:
	old_open = open
	import uiScriptLocale
	import app
	from utils import ReplaceElement, AppendChildren
	
	EQUIPMENT_START_INDEX = 90
	
	window = {
		"name" : "InventoryWindow",
	
		"x" : SCREEN_WIDTH - 176 - 200,
		"y" : SCREEN_HEIGHT - 37 - 565,
	
		"style" : ("movable", "float",),
	
		"width" : 176,
		"height" : 565,
	
		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),
	
				"x" : 0,
				"y" : 0,
	
				"width" : 176,
				"height" : 565,
	
				"children" :
				(
					## Title
					{
						"name" : "TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),
	
						"x" : 8,
						"y" : 7,
	
						"width" : 161,
						"color" : "yellow",
	
						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":77, "y":3, "text":uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2, "text_horizontal_align":"center" },
						),
					},
	
					## Equipment Slot
					{
						"name" : "Equipment_Base",
						"type" : "image",
	
						"x" : 10,
						"y" : 33,
	
						"image" : "d:/ymir work/ui/game/windows/equipment_base.sub",
	
						"children" :
						(
	
							{
								"name" : "EquipmentSlot",
								"type" : "slot",
	
								"x" : 3,
								"y" : 3,
	
								"width" : 150,
								"height" : 182,
	
								"slot" : (
											{"index":item.EQUIPMENT_BODY, "x":39, "y":37, "width":32, "height":64},
											{"index":item.EQUIPMENT_HEAD, "x":39, "y":2, "width":32, "height":32},
											{"index":item.EQUIPMENT_SHOES, "x":39, "y":145, "width":32, "height":32},
											{"index":item.EQUIPMENT_WRIST, "x":75, "y":67, "width":32, "height":32},
											{"index":item.EQUIPMENT_WEAPON, "x":3, "y":3, "width":32, "height":96},
											{"index":item.EQUIPMENT_NECK, "x":114, "y":84, "width":32, "height":32},
											{"index":item.EQUIPMENT_EAR, "x":114, "y":52, "width":32, "height":32},
											{"index":item.EQUIPMENT_UNIQUE1, "x":2, "y":113, "width":32, "height":32},
											{"index":item.EQUIPMENT_UNIQUE2, "x":75, "y":113, "width":32, "height":32},
											{"index":item.EQUIPMENT_ARROW, "x":114, "y":1, "width":32, "height":32},
											{"index":item.EQUIPMENT_SHIELD, "x":75, "y":35, "width":32, "height":32},
										),
							},
	
							{
								"name" : "Equipment_Tab_01",
								"type" : "radio_button",
	
								"x" : 86,
								"y" : 161,
	
								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",
	
								"children" :
								(
									{
										"name" : "Equipment_Tab_01_Print",
										"type" : "text",
	
										"x" : 0,
										"y" : 0,
	
										"all_align" : "center",
	
										"text" : "I",
									},
								),
							},
							{
								"name" : "Equipment_Tab_02",
								"type" : "radio_button",
	
								"x" : 86 + 32,
								"y" : 161,
	
								"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
								"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
								"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",
	
								"children" :
								(
									{
										"name" : "Equipment_Tab_02_Print",
										"type" : "text",
	
										"x" : 0,
										"y" : 0,
	
										"all_align" : "center",
	
										"text" : "II",
									},
								),
							},
	
						),
					},
	
					{
						"name" : "Inventory_Tab_01",
						"type" : "radio_button",
	
						"x" : 10,
						"y" : 33 + 191,
	
						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1,
	
						"children" :
						(
							{
								"name" : "Inventory_Tab_01_Print",
								"type" : "text",
	
								"x" : 0,
								"y" : 0,
	
								"all_align" : "center",
	
								"text" : "I",
							},
						),
					},
					{
						"name" : "Inventory_Tab_02",
						"type" : "radio_button",
	
						"x" : 10 + 78,
						"y" : 33 + 191,
	
						"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
						"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
						"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",
						"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2,
	
						"children" :
						(
							{
								"name" : "Inventory_Tab_02_Print",
								"type" : "text",
	
								"x" : 0,
								"y" : 0,
	
								"all_align" : "center",
	
								"text" : "II",
							},
						),
					},
	
					## Item Slot
					{
						"name" : "ItemSlot",
						"type" : "grid_table",
	
						"x" : 8,
						"y" : 246,
	
						"start_index" : 0,
						"x_count" : 5,
						"y_count" : 9,
						"x_step" : 32,
						"y_step" : 32,
	
						"image" : "d:/ymir work/ui/public/Slot_Base.sub"
					},
	
					## Print
					{
						"name":"Money_Slot",
						"type":"button",
	
						"x":8,
						"y":28,
	
						"horizontal_align":"center",
						"vertical_align":"bottom",
	
						"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
						"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
	
						"children" :
						(
							{
								"name":"Money_Icon",
								"type":"image",
	
								"x":-18,
								"y":20,
	
								"image":"d:/ymir work/ui/game/windows/money_icon.sub",
							},
	
							{
								"name" : "Money",
								"type" : "text",
	
								"x" : 3,
								"y" : 3,
	
								"horizontal_align" : "right",
								"text_horizontal_align" : "right",
	
								"text" : "123456789",
							},
						),
					},
	
				),
			},
		),
	}
	
	if app.ENABLE_CHEQUE_SYSTEM:
		slot = {
			"name":"Money_Slot",
			"type":"button",
	
			"x":75,
			"y":28,
	
			#"horizontal_align":"center",
			"vertical_align":"bottom",
	
			"default_image" : "d:/ymir work/ui/public/gold_slot.sub",
			"over_image" : "d:/ymir work/ui/public/gold_slot.sub",
			"down_image" : "d:/ymir work/ui/public/gold_slot.sub",
	
			"children" :
			(
				{
					"name" : "Money",
					"type" : "text",
	
					"x" : 3,
					"y" : 3,
	
					"horizontal_align" : "right",
					"text_horizontal_align" : "right",
	
					"text" : "123456789",
				},
			),
		}
	
		children = (
			{
				"name":"Money_Icon",
				"type":"image",
				"vertical_align":"bottom",
	
				"x":57,
				"y":26,
	
				"image":"d:/ymir work/ui/game/windows/money_icon.sub",
			},
	
			{
				"name":"Cheque_Icon",
				"type":"image",
				"vertical_align":"bottom",
	
				"x":10,
				"y":26,
	
				"image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
			},
			{
				"name":"Cheque_Slot",
				"type":"button",
	
				"x":28,
				"y":28,
	
				#"horizontal_align":"center",
				"vertical_align":"bottom",
	
				"default_image" : "d:/ymir work/ui/public/cheque_slot.sub",
				"over_image" : "d:/ymir work/ui/public/cheque_slot.sub",
				"down_image" : "d:/ymir work/ui/public/cheque_slot.sub",
	
				"children" :
				(
					{
						"name" : "Cheque",
						"type" : "text",
	
						"x" : 3,
						"y" : 3,
	
						"horizontal_align" : "right",
						"text_horizontal_align" : "right",
	
						"text" : "99",
					},
				),
			},
		)
	
		ReplaceElement("Money_Slot", slot, window)
		AppendChildren("board", children, window)
