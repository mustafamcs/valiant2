import app
if app.ENABLE_MESSENGER_TEAM:
	import uiScriptLocale

	IMG_DIR = "new_messenger/"

	window = {
		"name" : "MessengerWindow",

		"x" : SCREEN_WIDTH - 210,
		"y" : SCREEN_HEIGHT - 400 - 50,

		"style" : ("movable", "float",),

		"width" : 170,
		"height" : 310,

		"children" :
		(

			{
				"name" : "board",
				"type" : "board_with_titlebar",

				"x" : 0,
				"y" : 0,

				"width" : 170,
				"height" : 310,
				"title" : uiScriptLocale.MESSENGER_TITLE,
			},

			{
				"name" : "page_bg",
				"type" : "image",
				"x" : 10,
				"y" : 36 + 28,
				"image" : IMG_DIR+"page_0.png",
				"children" : 
				(
					{
						"name" : "page_0_btn",
						"type" : "radio_button",
						"x" : 5,
						"y" : 3,
						#"tooltip_text" : "Friend",
						"tooltip_x" : 0,
						"tooltip_y" : 35,
						"default_image" : IMG_DIR+"btn_size.png",
						"over_image" : IMG_DIR+"btn_size.png",
						"down_image" : IMG_DIR+"btn_size.png",
					},
					{
						"name" : "page_1_btn",
						"type" : "radio_button",
						"x" : 39,
						"y" : 3,
						#"tooltip_text" : "Guild",
						"tooltip_x" : 0,
						"tooltip_y" : 35,
						"default_image" : IMG_DIR+"btn_size.png",
						"over_image" : IMG_DIR+"btn_size.png",
						"down_image" : IMG_DIR+"btn_size.png",
					},
					{
						"name" : "page_2_btn",
						"type" : "radio_button",
						"x" : 73,
						"y" : 3,
						#"tooltip_text" : "Block",
						"tooltip_x" : 0,
						"tooltip_y" : 35,
						"default_image" : IMG_DIR+"btn_size.png",
						"over_image" : IMG_DIR+"btn_size.png",
						"down_image" : IMG_DIR+"btn_size.png",
					},
					{
						"name" : "page_3_btn",
						"type" : "radio_button",
						"x" : 107,
						"y" : 3,
						#"tooltip_text" : "Support",
						"tooltip_x" : 0,
						"tooltip_y" : 35,
						"default_image" : IMG_DIR+"btn_size.png",
						"over_image" : IMG_DIR+"btn_size.png",
						"down_image" : IMG_DIR+"btn_size.png",
					},
				),
			},
			
			{
				"name" : "SearchBG",
				"type" : "image",
				"x" : 10,
				"y" : 36,
				"image" : IMG_DIR+"search_bg.png",
				"children" : (
					{
						"name" : "editline",
						"type" : "editline",
						"x" : 3,
						"y" : 4,
						"width" : 110,
						"height" : 15,
						"input_limit" : 18,
					},

					{
						"name" : "clear_btn",
						"type" : "button",
						"x" : 115,
						"y" : 6,
						"tooltip_text" : uiScriptLocale.CHATTING_SETTING_CLEAR,
						"tooltip_x" : 0,
						"tooltip_y" : 35,
						"default_image" : IMG_DIR+"clear_btn_0.png",
						"over_image" : IMG_DIR+"clear_btn_1.png",
						"down_image" : IMG_DIR+"clear_btn_2.png",
					},
					{
						"name" : "search_btn",
						"type" : "button",
						"x" : 130,
						"y" : 1,
						#"tooltip_text" : "Search",
						"tooltip_x" : 0,
						"tooltip_y" : 35,
						"default_image" : IMG_DIR+"search_btn_0.png",
						"over_image" : IMG_DIR+"search_btn_1.png",
						"down_image" : IMG_DIR+"search_btn_2.png",
					},
				
				),
			},

			{
				"name" : "AddFriendButton",
				"type" : "button",

				"x" : 13 + (30 * 0),
				"y" : 36 + 28 + 214,

				"tooltip_text" : uiScriptLocale.MESSENGER_ADD_FRIEND,
				"tooltip_x" : 0,
				"tooltip_y" : 35,

				"default_image" : IMG_DIR+"add_friend_0.png",
				"over_image" : IMG_DIR+"add_friend_1.png",
				"down_image" : IMG_DIR+"add_friend_2.png",
				"disable_image" : IMG_DIR+"add_friend_2.png",
			},
			{
				"name" : "WhisperButton",
				"type" : "button",

				"x" : 13 + (30 * 1),
				"y" : 36 + 28 + 214,

				"tooltip_text" : uiScriptLocale.MESSENGER_WHISPER,
				"tooltip_x" : 0,
				"tooltip_y" : 35,

				"default_image" : IMG_DIR+"whisper_0.png",
				"over_image" : IMG_DIR+"whisper_1.png",
				"down_image" : IMG_DIR+"whisper_2.png",
				"disable_image" : IMG_DIR+"whisper_2.png",
			},
			{
				"name" : "RemoveButton",
				"type" : "button",

				"x" : 13 + (30 * 2),
				"y" : 36 + 28 + 214,
				
				"tooltip_text" : uiScriptLocale.MESSENGER_DELETE_FRIEND,
				"tooltip_x" : 0,
				"tooltip_y" : 35,
				
				"default_image" : IMG_DIR+"remove_0.png",
				"over_image" : IMG_DIR+"remove_1.png",
				"down_image" : IMG_DIR+"remove_2.png",
				"disable_image" : IMG_DIR+"remove_3.png",
			},

			{
				"name" : "BlockButton",
				"type" : "button",

				"x" : 13 + (30 * 3),
				"y" : 36 + 28 + 214,

				"tooltip_text" : "Block",
				"tooltip_x" : 0,
				"tooltip_y" : 35,

				"default_image" : IMG_DIR+"block_0.png",
				"over_image" : IMG_DIR+"block_1.png",
				"down_image" : IMG_DIR+"block_2.png",
				"disable_image" : IMG_DIR+"block_2.png",
			},
			{
				"name" : "GuildButton",
				"type" : "button",

				"x" : 13 + (30 * 4),
				"y" : 36 + 28 + 214,

				"tooltip_text" : uiScriptLocale.MESSENGER_OPEN_GUILD,
				"tooltip_x" : 0,
				"tooltip_y" : 35,

				"default_image" : IMG_DIR+"guild_0.png",
				"over_image" : IMG_DIR+"guild_1.png",
				"down_image" : IMG_DIR+"guild_2.png",
				"disable_image" : IMG_DIR+"guild_2.png",
			},

		), ## end of main window
	}

else:
	import uiScriptLocale

	BUTTON_START_X_POS = -60
	BUTTON_X_STEP = 30

	window = {
		"name" : "MessengerWindow",

		"x" : SCREEN_WIDTH - 200,
		"y" : SCREEN_HEIGHT - 400 - 50,

		"style" : ("movable", "float",),

		"width" : 170,
		"height" : 300,

		"children" :
		(

			{
				"name" : "board",
				"type" : "board_with_titlebar",

				"x" : 0,
				"y" : 0,

				"width" : 170,
				"height" : 300,
				"title" : uiScriptLocale.MESSENGER_TITLE,
			},

			{
				"name" : "ScrollBar",
				"type" : "scrollbar",

				"x" : 27,
				"y" : 40,
				"size" : 100,
				"horizontal_align" : "right",
			},

			{
				"name" : "AddFriendButton",
				"type" : "button",

				"x" : BUTTON_START_X_POS + BUTTON_X_STEP*0,
				"y" : 30,
				"horizontal_align" : "center",
				"vertical_align" : "bottom",
				"tooltip_text" : uiScriptLocale.MESSENGER_ADD_FRIEND,
				"tooltip_x" : 0,
				"tooltip_y" : 35,

				"default_image" : "d:/ymir work/ui/game/windows/messenger_add_friend_01.sub",
				"over_image" : "d:/ymir work/ui/game/windows/messenger_add_friend_02.sub",
				"down_image" : "d:/ymir work/ui/game/windows/messenger_add_friend_03.sub",
				"disable_image" : "d:/ymir work/ui/game/windows/messenger_add_friend_04.sub",
			},
			{
				"name" : "WhisperButton",
				"type" : "button",

				"x" : BUTTON_START_X_POS + BUTTON_X_STEP*1,
				"y" : 30,
				"horizontal_align" : "center",
				"vertical_align" : "bottom",
				"tooltip_text" : uiScriptLocale.MESSENGER_WHISPER,
				"tooltip_x" : 0,
				"tooltip_y" : 35,

				"default_image" : "d:/ymir work/ui/game/windows/messenger_whisper_01.sub",
				"over_image" : "d:/ymir work/ui/game/windows/messenger_whisper_02.sub",
				"down_image" : "d:/ymir work/ui/game/windows/messenger_whisper_03.sub",
				"disable_image" : "d:/ymir work/ui/game/windows/messenger_whisper_04.sub",
			},
			{
				"name" : "RemoveButton",
				"type" : "button",

				"x" : BUTTON_START_X_POS + BUTTON_X_STEP*3,
				"y" : 30,
				"horizontal_align" : "center",
				"vertical_align" : "bottom",
				"tooltip_text" : uiScriptLocale.MESSENGER_DELETE_FRIEND,
				"tooltip_x" : 0,
				"tooltip_y" : 35,

				"default_image" : "d:/ymir work/ui/game/windows/messenger_delete_01.sub",
				"over_image" : "d:/ymir work/ui/game/windows/messenger_delete_02.sub",
				"down_image" : "d:/ymir work/ui/game/windows/messenger_delete_03.sub",
				"disable_image" : "d:/ymir work/ui/game/windows/messenger_delete_04.sub",
			},
			{
				"name" : "GuildButton",
				"type" : "button",

				"x" : BUTTON_START_X_POS + BUTTON_X_STEP*4,
				"y" : 30,
				"horizontal_align" : "center",
				"vertical_align" : "bottom",
				"tooltip_text" : uiScriptLocale.MESSENGER_OPEN_GUILD,
				"tooltip_x" : 0,
				"tooltip_y" : 35,

				"default_image" : "d:/ymir work/ui/game/windows/messenger_guild_01.sub",
				"over_image" : "d:/ymir work/ui/game/windows/messenger_guild_02.sub",
				"down_image" : "d:/ymir work/ui/game/windows/messenger_guild_03.sub",
				"disable_image" : "d:/ymir work/ui/game/windows/messenger_guild_04.sub",
			},

		), ## end of main window
	}

