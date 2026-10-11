import uiScriptLocale, localeInfo

PATH_BASE = "lightwork/login/"

window = {
	"name" : "LoginWindow",

	"x" : 0,
	"y" : 0,
	
	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,
	
	"children" :
	[
		# Main Background
		{
			"name" : "BGImg",
			"type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : PATH_BASE + "background.png"
		},	
		{
			"name" : "Logo",
			"type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : PATH_BASE + "logo.png"
		},	
		{
			"name" : "LoginPanel",
			"type" : "window",
			
			"x" : -15,
			"y" : 30,
			
			"horizontal_align" : "center",
			"vertical_align" : "center",
			
			"width" : 910,
			"height" : 625,
			
			"children" : 
			[
				{
					"name" : "Login",
					"type" : "image",
					
					"x" : 0,
					"y" : 125,
					
					"image" : PATH_BASE + "login_panel_bg.png",
					
					"children" : 
					[
						{
							"name" : "UserInputImg",
							"type" : "image",
							
							"x" : 141,
							"y" : 65+15,
							
							"image" : PATH_BASE + "id_bg.png",
							
							"children" : 
							[
								{
									"name" : "UserEditLine",
									"type" : "editline",
									"info_msg": uiScriptLocale.LOGIN_ID,

									"x" : 50,
									"y" : 15,

									"width" : 215,
									"height" : 30,

									"input_limit" : 16,

									# "fontsize" : "LARGE",
									"overlay_text" : localeInfo.LOGIN_INFO_ID,
									"color" : 0xffb09574,
								},
							],
						},
						
						{
							"name" : "PwInputImg",
							"type" : "image",
							
							"x" : 141,
							"y" : 105+50,
							
							"image" : PATH_BASE + "pw_bg.png",
							
							"children" : 
							[
								{
									"name" : "PwEditLine",
									"type" : "editline",
									"info_msg": uiScriptLocale.LOGIN_PW,

									"x" : 50,
									"y" : 15,

									"width" : 215,
									"height" : 30,

									"input_limit" : 16,
									"secret_flag" : 1,

									# "fontsize" : "LARGE",
									"overlay_text" : localeInfo.LOGIN_INFO_PW,
									"color" : 0xffb09574,
								},
							],
						},
						{
							"name" : "LoginBtn",
							"type" : "button",
							
							"x" : 138,
							"y" : 155+72,
							
							"default_image" :  PATH_BASE + "buttons/login_btn.png",
							"over_image" : 	PATH_BASE + "buttons/login_btn_2.png",
							"down_image" : PATH_BASE + "buttons/login_btn_3.png",
						},
						{
							"name" : "RegisterBtn",
							"type" : "button",
							
							"x" : 138,
							"y" : 155+174,
							
							"default_image" :  PATH_BASE + "buttons/register_btn.png",
							"over_image" : 	PATH_BASE + "buttons/register_btn_2.png",
							"down_image" : PATH_BASE + "buttons/register_btn_3.png",
						},
						{
							"name" : "ForgotBtn",
							"type" : "button",
							
							"x" : 138+151,
							"y" : 155+174,
							
							"default_image" :  PATH_BASE + "buttons/forgot_pw_btn.png",
							"over_image" : 	PATH_BASE + "buttons/forgot_pw_btn_2.png",
							"down_image" : PATH_BASE + "buttons/forgot_pw_btn_3.png",
						},
						{
							"name" : "SvButton1",
							"type" : "radio_button",
							
							"x" : 110,
							"y" : 445,
							"default_image" :  PATH_BASE + "buttons/s1_btn.png",
							"over_image" : 	PATH_BASE + "buttons/s1_btn_2.png",
							"down_image" : PATH_BASE + "buttons/s1_btn_3.png",
						},
						{
							"name" : "SvButton2",
							"type" : "radio_button",
							
							"x" : 202,
							"y" : 445,
							# "default_image" :  PATH_BASE + "buttons/s2_btn.png",
							# "over_image" : 	PATH_BASE + "buttons/s2_btn_2.png",
							# "down_image" : PATH_BASE + "buttons/s2_btn_3.png",
						},
						{
							"name" : "ExitBtn",
							"type" : "button",
							
							"x" : 300,
							"y" : 445,
							
							"default_image" :  PATH_BASE + "buttons/exit_btn.png",
							"over_image" : 	PATH_BASE + "buttons/exit_btn_2.png",
							"down_image" : PATH_BASE + "buttons/exit_btn_3.png",
						},
						{
							"name" : "ChannelBtn1",
							"type" : "radio_button",
							
							"x" : 41,
							"y" : 35,
							
							"default_image" :  PATH_BASE + "buttons/channels/ch1.png",
							"over_image" : 	PATH_BASE + "buttons/channels/ch1.png",
							"down_image" : PATH_BASE + "buttons/channels/ch1_2.png",
						},
						{
							"name" : "ChannelBtn2",
							"type" : "radio_button",
							
							"x" : 41,
							"y" : 35 +60,
							
							"default_image" :  PATH_BASE + "buttons/channels/ch2.png",
							"over_image" : 	PATH_BASE + "buttons/channels/ch2.png",
							"down_image" : PATH_BASE + "buttons/channels/ch2_2.png",
						},
						
						{
							"name" : "ChannelBtn3",
							"type" : "radio_button",
							
							"x" : 41,
							"y" : 35 + 60*2,
							
							"default_image" :  PATH_BASE + "buttons/channels/ch3.png",
							"over_image" : 	PATH_BASE + "buttons/channels/ch3.png",
							"down_image" : PATH_BASE + "buttons/channels/ch3_2.png",
						},
						{
							"name" : "ChannelBtn4",
							"type" : "radio_button",
							
							"x" : 41,
							"y" : 35 + 60*3,
							
							"default_image" :  PATH_BASE + "buttons/channels/ch4.png",
							"over_image" : 	PATH_BASE + "buttons/channels/ch4.png",
							"down_image" : PATH_BASE + "buttons/channels/ch4_2.png",
						},
						{
							"name" : "ChannelBtn5",
							"type" : "radio_button",
							
							"x" : 41,
							"y" : 35 + 60*4,
							
							"default_image" :  PATH_BASE + "buttons/channels/ch5.png",
							"over_image" : 	PATH_BASE + "buttons/channels/ch5.png",
							"down_image" : PATH_BASE + "buttons/channels/ch5_2.png",
						},
						{
							"name" : "ChannelBtn6",
							"type" : "radio_button",
							
							"x" : 41,
							"y" : 35 + 60*5,
							
							"default_image" :  PATH_BASE + "buttons/channels/ch6.png",
							"over_image" : 	PATH_BASE + "buttons/channels/ch6.png",
							"down_image" : PATH_BASE + "buttons/channels/ch6_2.png",
						},
					],
					
				},		

				{
					"name" : "Save",
					"type" : "image",
					
					"x" : 475,
					"y" : 125,
					
					"image" : PATH_BASE + "save_account_board.png",
					"children" : [
							{
							"name" : "WebBtn",
							"type" : "button",
							
							"x" : 18,
							"y" : 441,
							

							"default_image" :  PATH_BASE + "buttons/home_btn.png",
							"over_image" : 	PATH_BASE + "buttons/home_btn_2.png",
							"down_image" : PATH_BASE + "buttons/home_btn_3.png",
						},
						{
							"name" : "DiscordBtn",
							"type" : "button",
							
							"x" : 18+200,
							"y" : 441,
							
							"default_image" :  PATH_BASE + "buttons/discord_btn.png",
							"over_image" : 	PATH_BASE + "buttons/discord_btn_2.png",
							"down_image" : PATH_BASE + "buttons/discord_btn_3.png",
						},
					]
				},		
			],
		},
	],
}


