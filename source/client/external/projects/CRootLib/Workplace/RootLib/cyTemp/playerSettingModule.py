# -*- coding: cp949 -*-
#511960237
__author__ = "Light05"
__system__ = "PlayerLoad - PlayerSettingsModule Renewal"
__date__ = "30.08.2022"
__ver__ = "0.15"

import chr, chrmgr, player, constInfo, app, colorInfo, localeInfo, \
	uiGuild, dbg, emotion, extraInfo

if app.ENABLE_WOLFMAN_CHARACTER:
	JOB_WARRIOR,JOB_ASSASSIN,JOB_SURA,JOB_SHAMAN,JOB_WOLFMAN = xrange(5)
else:
	JOB_WARRIOR,JOB_ASSASSIN,JOB_SURA,JOB_SHAMAN = xrange(4)

if app.ENABLE_WOLFMAN_CHARACTER:
	RACE_WARRIOR_M,RACE_ASSASSIN_W,RACE_SURA_M,RACE_SHAMAN_W,RACE_WARRIOR_W,RACE_ASSASSIN_M,RACE_SURA_W,RACE_SHAMAN_M,RACE_WOLFMAN_M = xrange(9)
else:
	RACE_WARRIOR_M,RACE_ASSASSIN_W,RACE_SURA_M,RACE_SHAMAN_W,RACE_WARRIOR_W,RACE_ASSASSIN_M,RACE_SURA_W,RACE_SHAMAN_M = xrange(8)

PASSIVE_GUILD_SKILL_INDEX_LIST = ( 151, )
ACTIVE_GUILD_SKILL_INDEX_LIST = ( 152, 153, 154, 155, 156, 157, )

NAME_COLOR_DICT = {
	chrmgr.NAMECOLOR_PC : colorInfo.CHR_NAME_RGB_PC,
	chrmgr.NAMECOLOR_NPC : colorInfo.CHR_NAME_RGB_NPC,
	chrmgr.NAMECOLOR_MOB : colorInfo.CHR_NAME_RGB_MOB,
	chrmgr.NAMECOLOR_PVP : colorInfo.CHR_NAME_RGB_PVP,
	chrmgr.NAMECOLOR_PK : colorInfo.CHR_NAME_RGB_PK,
	chrmgr.NAMECOLOR_PARTY : colorInfo.CHR_NAME_RGB_PARTY,
	chrmgr.NAMECOLOR_WARP : colorInfo.CHR_NAME_RGB_WARP,
	chrmgr.NAMECOLOR_WAYPOINT : colorInfo.CHR_NAME_RGB_WAYPOINT,

	chrmgr.NAMECOLOR_EMPIRE_MOB : colorInfo.CHR_NAME_RGB_EMPIRE_MOB,
	chrmgr.NAMECOLOR_EMPIRE_NPC : colorInfo.CHR_NAME_RGB_EMPIRE_NPC,
	chrmgr.NAMECOLOR_EMPIRE_PC+1 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_A,
	chrmgr.NAMECOLOR_EMPIRE_PC+2 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_B,
	chrmgr.NAMECOLOR_EMPIRE_PC+3 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_C,
}

if app.ENABLE_MINIMAP_BOSS_STONE:
	NAME_COLOR_DICT.update({
	chrmgr.NAMECOLOR_METINSTONE : colorInfo.CHR_NAME_RGB_METINSTONE,
	chrmgr.NAMECOLOR_BOSS : colorInfo.CHR_NAME_RGB_BOSS,
	})

def registerData():
	# RegisterNameColor
	for nameIdx, nameColor in NAME_COLOR_DICT.items():
		chrmgr.RegisterNameColor(nameIdx, *nameColor)

	# RegisterTitleColor
	for titleColorIdx, titleColor in enumerate(extraInfo.TITLE_COLOR_DICT):
		chrmgr.RegisterTitleColor(titleColorIdx, *titleColor)

	# RegisterTitleName
	for titleIdx, titleName in enumerate(extraInfo.TITLE_NAME_LIST):
		chrmgr.RegisterTitleName(titleIdx, titleName)

	emotion.RegisterEmotionIcons()
	LoadGuildBuildingList(localeInfo.GUILD_BUILDING_LIST_TXT)


COMBO_TYPE_1, COMBO_TYPE_2, COMBO_TYPE_3 = xrange(3)

COMBO_INDEX_1, COMBO_INDEX_2, COMBO_INDEX_3, COMBO_INDEX_4, COMBO_INDEX_5, COMBO_INDEX_6 = xrange(6)

HORSE_SKILL_WILDATTACK = chr.MOTION_SKILL+121
HORSE_SKILL_CHARGE = chr.MOTION_SKILL+122
HORSE_SKILL_SPLASH = chr.MOTION_SKILL+123

GUILD_SKILL_DRAGONBLOOD = chr.MOTION_SKILL+101
GUILD_SKILL_DRAGONBLESS = chr.MOTION_SKILL+102
GUILD_SKILL_BLESSARMOR = chr.MOTION_SKILL+103
GUILD_SKILL_SPPEDUP = chr.MOTION_SKILL+104
GUILD_SKILL_DRAGONWRATH = chr.MOTION_SKILL+105
GUILD_SKILL_MAGICUP = chr.MOTION_SKILL+106

PASSIVE_GUILD_SKILL_INDEX_LIST = ( 151, )
ACTIVE_GUILD_SKILL_INDEX_LIST = ( 152, 153, 154, 155, 156, 157, )

NEW_678TH_SKILL_ENABLE = constInfo.NEW_678TH_SKILL_ENABLE
HORSE_INDEX_DICT = []

SKILL_INDEX_DICT = {
	JOB_WARRIOR : {
		1 : (1, 2, 3, 4, 5, 6, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (16, 17, 18, 19, 20, 21, 0, 0, 137, 0, 138, 0, 139, 0,),
		"HORSE" : (137, 138, 139, 0, 0, 0,),
		"SUPPORT" : (122, 121, 208, 124, 200, 201, 202, 203, 204, 205, 206, 207),
	},
	JOB_ASSASSIN : {
		1 : (31, 32, 33, 34, 35, 36, 0, 0, 137, 0, 138, 0, 139, 0, 140,),
		2 : (46, 47, 48, 49, 50, 51, 0, 0, 137, 0, 138, 0, 139, 0, 140,),
		"HORSE" : (137, 138, 139, 0, 0, 0,),
		"SUPPORT" : (122, 121, 208, 124, 200, 201, 202, 203, 204, 205, 206, 207),
	},
	JOB_SURA : {
		1 : (61, 62, 63, 64, 65, 66, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (76, 77, 78, 79, 80, 81, 0, 0, 137, 0, 138, 0, 139, 0,),
		"HORSE" : (137, 138, 139, 0, 0, 0,),
		"SUPPORT" : (122, 121, 208, 124, 200, 201, 202, 203, 204, 205, 206, 207),
	},
	JOB_SHAMAN : {
		1 : (91, 92, 93, 94, 95, 96, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (106, 107, 108, 109, 110, 111, 0, 0, 137, 0, 138, 0, 139, 0,),
		"HORSE" : (137, 138, 139, 0, 0, 0,),
		"SUPPORT" : (122, 121, 208, 124, 200, 201, 202, 203, 204, 205, 206, 207),
	},
}
if app.ENABLE_WOLFMAN_CHARACTER:
	SKILL_INDEX_DICT.update({
		JOB_WOLFMAN : {
			1 : (170, 171, 172, 173, 174, 175, 0, 0, 137, 0, 138, 0, 139, 0,),
			2 : (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,),
			"HORSE" : (137, 138, 139, 0, 0, 0,),
			"SUPPORT" : (122, 121, 208, 124, 200, 201, 202, 203, 204, 205, 206, 207),
		},
	})

def RegisterSkill(race, group, empire=0):


	job = chr.RaceToJob(race)

	## Character Skill
	if SKILL_INDEX_DICT.has_key(job):
		if SKILL_INDEX_DICT[job].has_key(group):

			activeSkillList = SKILL_INDEX_DICT[job][group]

			for i in xrange(len(activeSkillList)):
				skillIndex = activeSkillList[i]

				if i != 6 and i != 7:
					player.SetSkill(i+1, skillIndex)

			supportSkillList = SKILL_INDEX_DICT[job]["SUPPORT"]

			for i in xrange(len(supportSkillList)):
				player.SetSkill(i+100+1, supportSkillList[i])

			horseSkillList = SKILL_INDEX_DICT[job]["HORSE"]
			for i in xrange(len(horseSkillList)):
				player.SetSkill(i+120+1, horseSkillList[i])

			buffiSkillList = [180, 181, 182, 183, 184]
			for i in xrange(len(buffiSkillList)):
				player.SetSkill(i+160+1, buffiSkillList[i])

	## Language Skill
	# if 0 != empire:
	# 	languageSkillList = []
	# 	for i in xrange(3):
	# 		if (i+1) != empire:
	# 			languageSkillList.append(player.SKILL_INDEX_LANGUAGE1+i)
	# 	for i in xrange(len(languageSkillList)):
	# 		player.SetSkill(107+i, languageSkillList[i])

	## Guild Skill
	for i in xrange(len(PASSIVE_GUILD_SKILL_INDEX_LIST)):
		player.SetSkill(200+i, PASSIVE_GUILD_SKILL_INDEX_LIST[i])

	for i in xrange(len(ACTIVE_GUILD_SKILL_INDEX_LIST)):
		player.SetSkill(210+i, ACTIVE_GUILD_SKILL_INDEX_LIST[i])

# GUILD_BUILDING
def LoadGuildBuildingList(filename):
	uiGuild.BUILDING_DATA_LIST = []

	handle = app.OpenTextFile(filename)
	count = app.GetTextFileLineCount(handle)
	for i in xrange(count):
		line = app.GetTextFileLine(handle, i)
		tokens = line.split("\t")

		TOKEN_VNUM = 0
		TOKEN_TYPE = 1
		TOKEN_NAME = 2
		TOKEN_LOCAL_NAME = 3
		NO_USE_TOKEN_SIZE_1 = 4
		NO_USE_TOKEN_SIZE_2 = 5
		NO_USE_TOKEN_SIZE_3 = 6
		NO_USE_TOKEN_SIZE_4 = 7
		TOKEN_X_ROT_LIMIT = 8
		TOKEN_Y_ROT_LIMIT = 9
		TOKEN_Z_ROT_LIMIT = 10
		TOKEN_PRICE = 11
		TOKEN_MATERIAL = 12
		TOKEN_NPC = 13
		TOKEN_GROUP = 14
		TOKEN_DEPEND_GROUP = 15
		TOKEN_ENABLE_FLAG = 16
		LIMIT_TOKEN_COUNT = 17

		if not tokens[TOKEN_VNUM].isdigit():
			continue

		if len(tokens) < LIMIT_TOKEN_COUNT:
			dbg.TraceError("Strange token count [%d/%d] [%s]" % (len(tokens), LIMIT_TOKEN_COUNT, line))
			continue

		ENABLE_FLAG_TYPE_NOT_USE = False
		ENABLE_FLAG_TYPE_USE = True
		ENABLE_FLAG_TYPE_USE_BUT_HIDE = 2

		if ENABLE_FLAG_TYPE_NOT_USE == int(tokens[TOKEN_ENABLE_FLAG]):
			continue

		vnum = int(tokens[TOKEN_VNUM])
		type = tokens[TOKEN_TYPE]
		name = tokens[TOKEN_NAME]
		localName = tokens[TOKEN_LOCAL_NAME]
		xRotLimit = int(tokens[TOKEN_X_ROT_LIMIT])
		yRotLimit = int(tokens[TOKEN_Y_ROT_LIMIT])
		zRotLimit = int(tokens[TOKEN_Z_ROT_LIMIT])
		price = tokens[TOKEN_PRICE]
		material = tokens[TOKEN_MATERIAL]

		folderName = ""
		if "HEADQUARTER" == type:
			folderName = "headquarter"
		elif "FACILITY" == type:
			folderName = "facility"
		elif "OBJECT" == type:
			folderName = "object"
		elif "WALL" == type:
			folderName = "fence"

		materialList = ["0", "0", "0"]
		if material:
			if material[0] == "\"":
				material = material[1:]
			if material[-1] == "\"":
				material = material[:-1]
			for one in material.split("/"):
				data = one.split(",")
				if 2 != len(data):
					continue
				itemID = int(data[0])
				count = data[1]

				if itemID == uiGuild.MATERIAL_STONE_ID:
					materialList[uiGuild.MATERIAL_STONE_INDEX] = count
				elif itemID == uiGuild.MATERIAL_LOG_ID:
					materialList[uiGuild.MATERIAL_LOG_INDEX] = count
				elif itemID == uiGuild.MATERIAL_PLYWOOD_ID:
					materialList[uiGuild.MATERIAL_PLYWOOD_INDEX] = count

		chrmgr.RegisterRaceSrcName(name, folderName)
		chrmgr.RegisterRaceName(vnum, name)

		appendingData = { "VNUM":vnum,
						"TYPE":type,
						"NAME":name,
						"LOCAL_NAME":localName,
						"X_ROT_LIMIT":xRotLimit,
						"Y_ROT_LIMIT":yRotLimit,
						"Z_ROT_LIMIT":zRotLimit,
						"PRICE":price,
						"MATERIAL":materialList,
						"SHOW" : True }

		if ENABLE_FLAG_TYPE_USE_BUT_HIDE == int(tokens[TOKEN_ENABLE_FLAG]):
			appendingData["SHOW"] = False

		uiGuild.BUILDING_DATA_LIST.append(appendingData)

	app.CloseTextFile(handle)
# END_OF_GUILD_BUILDING

