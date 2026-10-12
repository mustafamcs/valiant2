import localeInfo
import uiScriptLocale

WINDOW_WIDTH	= 370
WINDOW_HEIGHT	= 485

SAFEBOX_CHILDREN = (
	{
		"name" : "BackGroundSafebox01",
		"type" : "window",

		"x" : 9,
		"y" : 46 - 33,

		"width" : 338,
		"height" : 325,
		"children" :
		(
			{
				"name" : "GridBackground",
				"type" : "border_a",
				"x" : 4,
				"y" : 46 - 33+14,
				"width" : 339,
				"height" : 325,
			},
			{
				"name" : "YangGained",
				"type" : "image",
				# "text" : localeInfo.OFFLINESHOP_SET_NAME,
				"x" : 4,
				"y" : -5,
				"image" : "d:/ymir work/offlineshop/ae/withdrawbg.png",
			},
			{
				"name" : "ShopSafeboxValuteText",
				"type" : "text",

				"x" : -75,
				"y" : -155,

				"all_align" : "center",
				"text" : "000000",
			},
			{
				"name" : "ShopSafeboxWithdrawYangButton",
				"type" : "button",

				"x" : 200,
				"y" : -5,
				"fontsize" : "LARGE",

				"default_image" : "d:/ymir work/offlineshop/ae/pickyang.png",
				"over_image" : "d:/ymir work/offlineshop/ae/pickyang2.png",
				"down_image" : "d:/ymir work/offlineshop/ae/pickyang3.png",
			},
		),
	},
	{
		"name" : "ShopTimeBG",
		"type" : "image",
		"text" : localeInfo.OFFLINESHOP_SET_NAME,
		"x" : 17-3,
		"y" : 365,
		"image"     : "d:/ymir work/offlineshop/ae/timemaxbg.png",
	},
{ "name":"TitleName", "type":"text", "x":-125, "y":-51, "text" : localeInfo.OFFLINESHOP_TITLE_MY_STORAGE, "text_horizontal_align":"center", "horizontal_align":"center" },
)

window = {

	"name" : "OfflineshopBoard",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH/2  - WINDOW_WIDTH/2,
	"y" : SCREEN_HEIGHT/2  - WINDOW_HEIGHT/2,

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "MainBoard",
			"type" : "board",
			
			"style" : ("attach",),
			
			"x" : 0,
			"y" : 0,
			
			"width" 	: WINDOW_WIDTH,
			"height" 	: WINDOW_HEIGHT,
			
			"children" : 
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",

					"x" : 8,
					"y" : 7,

					"width"  : WINDOW_WIDTH - 16,

					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",

							"x" : 0,
							"y" : 3,

							"text" : "",

							"text_horizontal_align":"center",
							"horizontal_align":"center",
						},
					),
				},

				{
					"name": "MyShopButton",
					"type": "button",

					"x": 339- 45*2-130, "y": 32,

					"tooltip_text" : localeInfo.OFFLINESHOP_MY_MARKET,

					"default_image" : "d:/ymir work/offlineshop/shopsearchp2p/myshop1.png",
					"over_image" : "d:/ymir work/offlineshop/shopsearchp2p/myshop2.png",
					"down_image" : "d:/ymir work/offlineshop/shopsearchp2p/myshop3.png",
				},
				{
					"name": "ShopSafeboxButton",
					"type": "button",

					"x": 339 - 45-130, "y": 32,

					"tooltip_text" : localeInfo.OFFLINESHOP_SAFEBOX_NAME,

					"default_image" : "d:/ymir work/offlineshop/shopsearchp2p/depo1.png",
					"over_image" : "d:/ymir work/offlineshop/shopsearchp2p/depo2.png",
					"down_image" : "d:/ymir work/offlineshop/shopsearchp2p/depo3.png",
				},
				# Back Button
				{
					"name": "SearchFilterButton",
					"type": "button",

					"x": 430 - 26 - 35 -30-130, "y": 32,

					"tooltip_text" : localeInfo.OFFLINESHOP_TITLE_SEARCH,

					"default_image" : "d:/ymir work/offlineshop/shopsearchp2p/buy1.png",
					"over_image" : "d:/ymir work/offlineshop/shopsearchp2p/buy2.png",
					"down_image" : "d:/ymir work/offlineshop/shopsearchp2p/buy3.png",
					
				},

				{
					"name" : "MyShopBoardNoShop",
					"type" : "window",
					
                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 61,
					
					"children":
					(
						{
							"name" : "CreateShopButton",
							"type" : "button",
							
							"x" : 190,
							"y" : 7,
							"default_image" : "d:/ymir work/offlineshop/ae/create.png",
							"over_image" : "d:/ymir work/offlineshop/ae/create2.png",
							"down_image" : "d:/ymir work/offlineshop/ae/create3.png",
							"text" : localeInfo.OFFLINESHOP_SCRIPTFILE_CREATE_TEXT,
						},
						{
							"name" : "ShopNameImage",
							"type" : "image",
							"text" : localeInfo.OFFLINESHOP_SET_NAME,
							"x" : 17-3,
							"y" : 7,
							"image"     : "d:/ymir work/offlineshop/ae/nametitle.png",
						},
						{
							"name" : "ShopTimeBG",
							"type" : "image",
							"text" : localeInfo.OFFLINESHOP_SET_NAME,
							"x" : 17-3,
							"y" : 365,
							"image"     : "d:/ymir work/offlineshop/ae/timemaxbg.png",
						},
						{
							"name" : "ShopNameInput",
							"type" : "editline",
							"info_msg":localeInfo.OFFLINESHOP_SET_NAME,
							"width" : 200 , "height" : 75 ,
							
							"input_limit" : 35,
							"x" : 17, "y" : 15,
						},
						{
							"name" : "DaysTimeBG",
							"type" : "image",
							"x" : 107,
							"y" : 374,
							"image"     : "d:/ymir work/offlineshop/ae/timebg.png",
						},
						{
							"name" : "HoursTimeBG",
							"type" : "image",
							"x" : 216,
							"y" : 374,
							"image"     : "d:/ymir work/offlineshop/ae/timebg.png",
						},
						{
							"name" : "DaysCountText",
							"type" : "text",
							
							"text" : "0",
							"text_horizontal_align" : "center",
							"x" : 255-130-3, "y" :377,
						},
						{
							"name" : "Days",
							"type" : "text",
							
							"text" : localeInfo.DAYS_TIME,
							"text_horizontal_align" : "center",
							"x" : 255-130-3+15, "y" :377,
						},
						{
							"name" : "HoursCountText",
							"type" : "text",
							
							"text" : "0",
							"text_horizontal_align" : "center",
							"x" : 367-130-3, "y" : 377,
						},
						{
							"name" : "Hours",
							"type" : "text",
							
							"text" : localeInfo.HOURS_TIME,
							"text_horizontal_align" : "center",
							"x" : 367-130-3+15, "y" : 377,
						},
						{
							"name" : "DecreaseDaysButton",
							"type" : "button",
							
							"x" : 218-130,
							"y" : 375,
							
							"default_image" : "d:/ymir work/offlineshop/ae/left1.png",
							"over_image" 	: "d:/ymir work/offlineshop/ae/left2.png",
							"down_image" 	: "d:/ymir work/offlineshop/ae/left3.png",
						},
						{
							"name" : "IncreaseDaysButton",
							"type" : "button",
							
							"x" : 283+12-130,
							"y" : 375,
							"default_image" : "d:/ymir work/offlineshop/ae/right1.png",
							"over_image" 	: "d:/ymir work/offlineshop/ae/right2.png",
							"down_image" 	: "d:/ymir work/offlineshop/ae/right3.png",
						},
						{
							"name" : "DecreaseHoursButton",
							"type" : "button",
							
							"x" : 327-130,
							"y" : 375,
							
							"default_image" : "d:/ymir work/offlineshop/ae/left1.png",
							"over_image" 	: "d:/ymir work/offlineshop/ae/left2.png",
							"down_image" 	: "d:/ymir work/offlineshop/ae/left3.png",
						},
						{
							"name" : "IncreaseHoursButton",
							"type" : "button",
							
							"x" : 404-130,
							"y" : 375,
							
							"default_image" : "d:/ymir work/offlineshop/ae/right1.png",
							"over_image" 	: "d:/ymir work/offlineshop/ae/right2.png",
							"down_image" 	: "d:/ymir work/offlineshop/ae/right3.png",
						},

						{
							"name" : "GridBackground",
							"type" : "border_a",

							"x" : 13,
							"y" : 46 - 33+27,

							"width" : 339,
							"height" : 325,
						},

						{ "name":"TitleName", "type":"text", "x":-125, "y":-51, "text" : localeInfo.OFFLINESHOP_TITLE_MYSHOP, "text_horizontal_align":"center", "horizontal_align":"center" },

					),
				},

				{
					"name" : "MyShopBoard",
					"type" : "window",
					
					"width" :  622,  "height" :  567,

					"x" : 3, "y" : 61,

					"children":
					(
						{
							"name" : "ShopNameImage",
							"type" : "image",
							"text" : localeInfo.OFFLINESHOP_SET_NAME,
							"x" : 17-3,
							"y" : 7,
							"image"     : "d:/ymir work/offlineshop/ae/nametitle.png",
						},
						{
							"name" : "MyShopShopTitle",
							"type" : "text",

							"x" : 20, "y" : 11,

							"text" : "title",
							"r" : 1.0,
							"g" : 1.0,
							"b" : 1.0,
							"a" : 1.0,
						},
						{
							"name" : "MyShopTotalPrice",
							"type" : "text",
							"x" : 20, "y" : 35,
							"text" : "99999999 Yang",
							"r" : 1.0, "g" : 1.0, "b" : 1.0, "a" : 1.0,
						},
						{
							"name" : "BGs",
							"type" : "image",
							"text" : localeInfo.OFFLINESHOP_SET_NAME,
							"x" : 17-3,
							"y" : 365,
							"image"     : "d:/ymir work/offlineshop/ae/timemaxbg.png",
						},
						{
							"name" : "ShopTimeBG",
							"type" : "image",
							"text" : localeInfo.OFFLINESHOP_SET_NAME,
							"x" : 18-3,
							"y" : 375,
							"image"     : "d:/ymir work/offlineshop/ae/timeremaining.png",
						},
						{
							"name" : "GridBackground",
							"type" : "border_a",

							"x" : 13,
							"y" : 46 - 33+27,

							"width" : 339,
							"height" : 325,
						},
						{
							"name" : "MyShopShopDuration",
							"type" : "text",

							"x" : 95, "y" : 377,

							"text" : "99 days",
							"text_horizontal_align" : "center",
						},
						{
							"name" : "MyShopCloseButton",
							"type" : "button",
							
							"x" : 185,
							"y" : 7,
							
							"tooltip_text" : uiScriptLocale.PRIVATE_SHOP_CLOSE_BUTTON,

							"default_image" : "d:/ymir work/offlineshop/ae/close.png",
							"over_image" 	: "d:/ymir work/offlineshop/ae/close2.png",
							"down_image" 	: "d:/ymir work/offlineshop/ae/close3.png",
						},
					{ "name":"TitleName", "type":"text", "x":-125, "y":-51, "text" : localeInfo.OFFLINESHOP_MY_MARKET, "text_horizontal_align":"center", "horizontal_align":"center" },

					),
				},

				{
					"name" : "ListOfShop_OpenShop",
					"type" : "window",
					
                    "width" :  622,  "height" :  567,

                    "x" : 3, "y" : 61,
					
					"children":
					(
						{
							"name" : "ShopNameImage",
							"type" : "image",
							"text" : localeInfo.OFFLINESHOP_SET_NAME,
							"x" : 17-3,
							"y" : 7,
							"image"     : "d:/ymir work/offlineshop/ae/nametitle.png",
						},
						{
							"name" : "ShopTimeBG",
							"type" : "image",
							"text" : localeInfo.OFFLINESHOP_SET_NAME,
							"x" : 17-3,
							"y" : 365,
							"image"     : "d:/ymir work/offlineshop/ae/timemaxbg.png",
						},
						{
							"name" : "ShopTimeBG",
							"type" : "image",
							"text" : localeInfo.OFFLINESHOP_SET_NAME,
							"x" : 18-3,
							"y" : 375,
							"image"     : "d:/ymir work/offlineshop/ae/timeremaining.png",
						},
						{
							"name" : "ShopMsgButton",
							"type" : "button",
							
							"x" : 185,
							"y" : 7,
							
							"tooltip_text" : uiScriptLocale.PRIVATE_SHOP_MSG_BUTTON,

							"default_image" : "d:/ymir work/offlineshop/ae/msg.png",
							"over_image" 	: "d:/ymir work/offlineshop/ae/msg2.png",
							"down_image" 	: "d:/ymir work/offlineshop/ae/msg3.png",
						},
						{
								"name" : "OwnerShopTitle",
								"type" : "text",

								"x" : 20, "y" : 11,
	
								"text" : "title",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
						},
						{
							"name" : "OpenShopShopDuration",
							"type" : "text",

							"x" : 95, "y" : 377,

							"text" : "99 days",
							"text_horizontal_align" : "center",
						},
						{
							"name" : "GridBackground",
							"type" : "border_a",

							"x" : 13,
							"y" : 46 - 33+27,

							"width" : 339,
							"height" : 325,
						},
						{ "name":"TitleName", "type":"text", "x":-125, "y":-51, "text" : localeInfo.OFFLINE_SHOP_VIEWED_NOW , "text_horizontal_align":"center", "horizontal_align":"center" },
					),
				},
				{
					"name" : "ListOfShop_List",
					"type" : "window",
					
					"width" :  622,  "height" :  544,
					"x" : 3, "y" : 61,
				},
				{
					"name": "ShopSafeboxPage",
					"type": "window",

					"width" :  622,  "height" :  567,

					"x" : 3, "y" : 61,
					"children":
					(
						SAFEBOX_CHILDREN
					),
				},
			),
		},
	),
}

