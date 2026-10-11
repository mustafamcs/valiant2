# -*- coding: cp949 -*-
#-1906271375
ROOT = "d:/ymir work/ui/minimap/"

window = {
	"name" : "MiniMap",

	"x" : SCREEN_WIDTH - 136,
	"y" : 0,

	"width" : 136,
	"height" : 137,

	"children" :
	(
		## OpenWindow
		{
			"name" : "OpenWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 136,
			"height" : 137,

			"children" :
			[
				{
					"name" : "OpenWindowBGI",
					"type" : "image",
					"x" : 0,
					"y" : 0,
					"image" : ROOT + "minimap.sub",
				},
				## MiniMapWindow
				{
					"name" : "MiniMapWindow",
					"type" : "window",

					"x" : 4,
					"y" : 5,

					"width" : 128,
					"height" : 128,
				},
				## ScaleUpButton
				{
					"name" : "ScaleUpButton",
					"type" : "button",

					"x" : 101,
					"y" : 116,

					"default_image" : ROOT + "minimap_scaleup_default.sub",
					"over_image" : ROOT + "minimap_scaleup_over.sub",
					"down_image" : ROOT + "minimap_scaleup_down.sub",
				},
				## ScaleDownButton
				{
					"name" : "ScaleDownButton",
					"type" : "button",

					"x" : 115,
					"y" : 103,

					"default_image" : ROOT + "minimap_scaledown_default.sub",
					"over_image" : ROOT + "minimap_scaledown_over.sub",
					"down_image" : ROOT + "minimap_scaledown_down.sub",
				},
				## MiniMapHideButton
				{
					"name" : "MiniMapHideButton",
					"type" : "button",

					"x" : 111,
					"y" : 6,

					"default_image" : ROOT + "minimap_close_default.sub",
					"over_image" : ROOT + "minimap_close_over.sub",
					"down_image" : ROOT + "minimap_close_down.sub",
				},
				## AtlasShowButton
				{
					"name" : "AtlasShowButton",
					"type" : "button",

					"x" : 12,
					"y" : 12,

					"default_image" : ROOT + "atlas_open_default.sub",
					"over_image" : ROOT + "atlas_open_over.sub",
					"down_image" : ROOT + "atlas_open_down.sub",
				},

				## ServerInfo
				{
					"name" : "ServerInfo",
					"type" : "text",

					"text_horizontal_align" : "center",
					"fontname" : "Verdana:14",

					"outline" : 1,

					"x" : 68,
					"y" : 145,

					"text" : "",
				},
				## Channel
				{
					"name" : "ChannelInfo",
					"type" : "text",

					"text_horizontal_align" : "center",
					"fontname" : "Verdana:14",

					"outline" : 1,

					"x" : 68,
					"y" : 160,

					"text" : "",
				},
				## PositionInfo
				{
					"name" : "PositionInfo",
					"type" : "text",

					"text_horizontal_align" : "center",

					"outline" : 1,
					"fontname" : "Verdana:14",

					"x" : 68,
					"y" : 175,

					"text" : "",
				},

				## Datetime
				{
					"name" : "CurrentDate",
					"type" : "text",

					"text_horizontal_align" : "center",

					"outline" : 1,
					"fontname" : "Verdana:14",

					"x" : 70,
					"y" : 195,

					"text" : "",
				},

				## Datetime
				{
					"name" : "CurrentTime",
					"type" : "text",

					"text_horizontal_align" : "center",

					"outline" : 1,
					"fontname" : "Verdana:12",

					"x" : 70,
					"y" : 210,

					"text" : "",
				},

				## ObserverCount
				{
					"name" : "ObserverCount",
					"type" : "text",

					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 180,

					"text" : "",
				},
				{
					"name" : "FPSInfo",
					"type" : "text",
					"text_horizontal_align" : "center",
					"outline" : 1,
					"x" : -80,
					"y" : 10,
					"text" : "",
				},
			],
		},
		{
			"name" : "CloseWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 132,
			"height" : 48,

			"children" :
			[
				## ShowButton
				{
					"name" : "MiniMapShowButton",
					"type" : "button",

					"x" : 100,
					"y" : 4,

					"default_image" : ROOT + "minimap_open_default.sub",
					"over_image" : ROOT + "minimap_open_default.sub",
					"down_image" : ROOT + "minimap_open_default.sub",
				},
			],
		},
	),
}

import app
if app.ENABLE_GLOBAL_RANKING:
	window["children"][0]["children"] += [
		{
			"name" : "GlobalRankingButton",
			"type" : "button",

			"x" : -3,
			"y" : 35,

			"default_image" : "d:/ymir work/ui/game/minimapbuttons/btn_ranking_normal.png",
			"over_image" : "d:/ymir work/ui/game/minimapbuttons/btn_ranking_over.png",
			"down_image" : "d:/ymir work/ui/game/minimapbuttons/btn_ranking_down.png",
		},]

if app.ENABLE_OFFLINE_SHOP:
	window["children"][0]["children"] += [
		{
			"name" : "ShopSearchButton",
			"type" : "button",

			"x" : 50,
			"y" : 110,

			"default_image" : "d:/ymir work/ui/game/minimapbuttons/searchnormal.png",
			"over_image" : "d:/ymir work/ui/game/minimapbuttons/searchhover.png",
			"down_image" : "d:/ymir work/ui/game/minimapbuttons/searchpress.png",
		},]

		
if app.ENABLE_BIOLOG_SYSTEM:
	window["children"][0]["children"] += [
		{
			"name" : "BiologButton",
			"type" : "button",

			"x" : 0,
			"y" : 85,

			"default_image" : "d:/ymir work/ui/game/minimapbuttons/btn_biolog_normal.png",
			"over_image" : "d:/ymir work/ui/game/minimapbuttons/btn_biolog_over.png",
			"down_image" : "d:/ymir work/ui/game/minimapbuttons/btn_biolog_down.png",
		},]

	window["children"][0]["children"] += [
	{
		"name" : "BattlePassButton",
		"type" : "button",

		"x" : -7,
		"y" : 60,

		"default_image" : "d:/ymir work/ui/game/minimapbuttons/btn_battlepass_normal.png",
		"over_image" : "d:/ymir work/ui/game/minimapbuttons/btn_battlepass_over.png",
		"down_image" : "d:/ymir work/ui/game/minimapbuttons/btn_battlepass_down.png",
	},]

if app.ENABLE_DUNGEON_INFO:
	window["children"][0]["children"] += [
		{
			"name" : "DungeonInfoButton",
			"type" : "button",

			"x" : 18,
			"y" : 105,

			"default_image" : "d:/ymir work/ui/game/minimapbuttons/dungeon_0.png",
			"over_image" : "d:/ymir work/ui/game/minimapbuttons/dungeon_1.png",
			"down_image" : "d:/ymir work/ui/game/minimapbuttons/dungeon_2.png",
		},]

