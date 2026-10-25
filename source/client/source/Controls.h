#pragma once
/*
__author__ = MDproject
__discord__ = MDproject
__project__ = MDproject
*/

/********************************************** Fixed Defines (Martysama 5.8) Start **********************************************/

#define LOCALE_SERVICE_EUROPE																// Locale services set Europe
#define ENABLE_COSTUME_SYSTEM																// Costume System
#define ENABLE_ENERGY_SYSTEM																// Energy System
#define ENABLE_DRAGON_SOUL_SYSTEM															// Dragon Soul System
#define ENABLE_NEW_EQUIPMENT_SYSTEM															// Belt inventory system & rings
#define ENABLE_PACK_GET_CHECK																// Pack check
#define ENABLE_CANSEEHIDDENTHING_FOR_GM														// GM's can see everything including invisible
#define ENABLE_PROTOSTRUCT_AUTODETECT														// Proto autodetect
#define ENABLE_PLAYER_PER_ACCOUNT5															// Per player per accounts
#define ENABLE_LEVEL_IN_TRADE																// Level In Trade
#define ENABLE_DICE_SYSTEM																	// Official Dice
#define ENABLE_EXTEND_INVEN_SYSTEM															// 5 Pages Of Inventory
#define ENABLE_LVL115_ARMOR_EFFECT															// 115 Level item armor effect
#define ENABLE_SLOT_WINDOW_EX																// SlotWindow Ex
#define ENABLE_TEXT_LEVEL_REFRESH															// Level text refresh
#define ENABLE_USE_COSTUME_ATTR 															// Costume Item Attr
#define ENABLE_DISCORD_RPC																	// Discord Rich Presence
#ifdef ENABLE_DISCORD_RPC
#define CLIENT_ID		"1140693227301769476"
#define IMAGE_NAME		"image1"
#define IMAGE_OVER_IN	"Metin2"
#define WEB_URL			"www.metin2.com"
#define BUTTON_NAME		"Join!"
#define DISCORD_URL		"https://metin2.com"
#endif

#define WJ_SHOW_MOB_INFO																	// Show Mob Informations
#ifdef WJ_SHOW_MOB_INFO
#define ENABLE_SHOW_MOBAIFLAG
#define ENABLE_SHOW_MOBLEVEL
#endif

#define ENABLE_WOLFMAN_CHARACTER															// Enable Wolfman
#define ENABLE_MAGIC_REDUCTION_SYSTEM														// Magic Reduction Apply
#define ENABLE_MOUNT_COSTUME_SYSTEM 														// Mount Costume
#define ENABLE_WEAPON_COSTUME_SYSTEM 														// Weapon Costume

#define ENABLE_ACCE_COSTUME_SYSTEM 															// Shoulder Sash Costume
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	// #define USE_ACCE_ABSORB_WITH_NO_NEGATIVE_BONUS
#endif

#define ENABLE_EMOJI_SYSTEM																	// Emoji In Textline
#define ENABLE_HAIR_SPECULAR																// Specular for hair
#define ENABLE_QUEST_CATEGORY																// Official Quest Category
#define ENABLE_DS_GRADE_MYTH 																// Myth DragonSoul Update
#define ENABLE_CHAT_COLOR_SYSTEM															// Chat Color
// #define ENABLE_PRINT_RECV_PACKET_DEBUG 													// Debug print debug

//#define ENABLE_DEV_RESOURCE_DIAGNOSTICS													// Developer Module
//#ifdef ENABLE_DEV_RESOURCE_DIAGNOSTICS
//#define IMPROVED_PACKET_ENCRYPTION_REMOVE													// Dev server Removing Packet Enc
//#else
#undef _IMPROVED_PACKET_ENCRYPTION_															// Packed Encryption
//#endif

/********************************************** End of Fixed Defines (Martysama 5.8) **********************************************/

/********************************************** General Defines Start **********************************************/

//#define ENABLE_HIGHLIGHT_SYSTEM																// Hightlight Items
//#define ENABLE_TARGET_INFORMATION_SYSTEM													// Target Information System
//#define ENABLE_TARGET_INFORMATION_RENEWAL													// Target Information System
//#define ENABLE_SHOW_TARGET_HP																// Target HP Information
//#define ENABLE_ELEMENT_ADD																	// Target Element Information
//#define ENABLE_CHANNEL_SWITCH_SYSTEM														// Change channel System
//#define ENABLE_CHANNEL_INFO_UPDATE															// Channel Info update
//#define ENABLE_DROP_DIALOG_EXTENDED_SYSTEM													// Sell-Delete on ground System
//#define ENABLE_CUBE_RENEWAL_WORLDARD														// Offical Cube System
//#define ENABLE_SPECIAL_STORAGE																// Special Storage
//#define ENABLE_EXTENDED_COUNT_ITEMS															// Item count extended
//#define ENABLE_EXTENDED_YANG_LIMIT															// Yang limit extended
//#define ENABLE_OFFLINE_SHOP																	// Offlineshop Reworked
//#define ENABLE_SWITCHBOT																	// Serverside Switchbot
//#define ENABLE_CHEST_OPEN_RENEWAL															// Open Chest Renewal
//#define ENABLE_PLAYER_STATS_SYSTEM															// Character Stats
//#define ENABLE_GLOBAL_RANKING																// Global Ranking System
//#define ENABLE_POWER_RANKING

//#define ENABLE_SKILLS_LEVEL_OVER_P															// Sage Skill and Legendary Skill
#ifdef ENABLE_SKILLS_LEVEL_OVER_P
//#define DISABLE_LEGENDARY_SKILLS
#endif

//#define ENABLE_PASSIVE_SKILLS																// New Passive Skills
//#define ENABLE_FAST_SOUL_STONE_SYSTEM														// Read Soulstone Fast System
//#define ENABLE_FAST_SKILL_BOOK_SYSTEM														// Read Book Fast System
//#define ENABLE_DISTANCE_SKILL_SELECT														// Ask skills if player is lv > 5
//#define ENABLE_SKILL_COLOR_SYSTEM															// Colored Skills

//#define ENABLE_CHAR_SETTINGS																// Character settings
//#define ENABLE_ITEM_TRANSACTIONS															// Item transactions
//#define ENABLE_FISHING_RENEWAL																// Official Fishing System
//#define ENABLE_PRESENT_NPC																	// Present NPC
//#define ENABLE_EVENT_MANAGER																// Event Manager
#ifdef ENABLE_EVENT_MANAGER
//#define ENABLE_MINI_GAME_OKEY_NORMAL
//#define ENABLE_MINI_GAME_BNW
//#define ENABLE_MINI_GAME_CATCH_KING
#endif

//#define ENABLE_ITEMSHOP																		// Ingame Itemshop
//#define ENABLE_MINING_RENEWAL																// Mining Renewal

//#define ENABLE_MULTI_LANGUAGE_SYSTEM														// Multi language system
//#define ENABLE_EXTENDED_WHISPER_DETAILS														// Extended whisper target information, created mainly for multi-language country flag but can be used for other information.

//#define ENABLE_LMW_PROTECTION																// Anti Cheat Solution
#ifdef ENABLE_LMW_PROTECTION
////#define AUTO_PATCH_PROTECTION
#define AUTO_PATCH_COMMAND "ng6S&$'{cphv'9cM"

//#define ENABLE_BOT_CONTROL
#endif

//#define ENABLE_ALIGNMENT_SYSTEM																// Alignment System
//#define ENABLE_EXTRA_APPLY_BONUS															// New apply bonuses

//#define ENABLE_DUNGEON_INFO																	// Dungeon Info
//#define ENABLE_DUNGEON_NOTIFICATION															//Dungeon notification

//#define ENABLE_WIKI																			// Ingame Wikipedia
#if defined (ENABLE_WIKI) && defined(ENABLE_WOLFMAN_CHARACTER)
////#define WIKI_WOLFMAN
#endif

#ifdef ENABLE_OFFLINE_SHOP
//#define ENABLE_SHOP_IN_CITIES																// Shop Entities in City
//#define ENABLE_LARGE_DYNAMIC_PACKET															// Package Limits are increased for offshop
//#define ENABLE_SHOP_SEARCH																	// OfflineShop Shop Search
//#define ENABLE_OFFLINE_SHOP_GRID															// OfflineShop Grid
//#define ENABLE_OFFLINESHOP_NOTIFICATION														// Offlineshop Notification
//#define ENABLE_SHOP_DECORATION																// Offlineshop Decoration
//#define ENABLE_OFFLINESHOP_EXTEND_TIME														// Extend shop time
//#define ENABLE_AVERAGE_PRICE
#endif

//#define ENABLE_BIOLOG_SYSTEM
#ifdef ENABLE_SPECIAL_STORAGE
//#define ENABLE_CHECK_IF_SAFEBOX_OPEN														// Checks safebox
//#define ENABLE_CHECK_IF_MALL_OPEN															// Checks Mall
#endif

#ifdef ENABLE_EXTENDED_COUNT_ITEMS
#define MAX_COUNT DWORD// (uint16_t = 65535)
#define SET_MAX_COUNT 2000
#endif
//#define ENABLE_SOCKET_LIMIT_5											//Socket Limiti

//#define ENABLE_IN_GAME_LOG_SYSTEM															// Ingame Log System
//#define ENABLE_HWID																			// Hwid System
//#define ENABLE_NEW_PET_SYSTEM																// Level pet system
#ifdef ENABLE_NEW_PET_SYSTEM
//#define ENABLE_PET_ATTR_DETERMINE															//Pet Efsunlama Ve Tip Belirleme
#endif
//#define ENABLE_METIN_QUEUE
/********************************************** End of General Defines **********************************************/

/********************************************** Item Related Defines Start **********************************************/
//#define ENABLE_ANIMATION_WING																// Animation wing system
//#define ENABLE_PET_COSTUME_SYSTEM 															// Pet Costume
//#define ENABLE_DS_SET_BONUS 																// Dragon Soul Set Bonus
//#define ENABLE_AURA_SYSTEM																	// Aura System
//#define ENABLE_ITEMS_SHINING																// Shining Items

//#define ENABLE_MOUNT_SKIN																	// Mount Skin
//#define ENABLE_PET_SKIN																		// Pet Skin
//#define ENABLE_ACCE_COSTUME_SKIN															// Acce Costume Skin
//#define ENABLE_CROWN_SYSTEM																	// Crown part
//#define ENABLE_AURA_SKIN																	// Aura Skin

//#define ENABLE_ATTR_RARE_RENEWAL

//#define ENABLE_BOOSTER_ITEM
//#define ENABLE_PENDANT_ITEM
//#define ENABLE_GLOVE_ITEM
//#define ENABLE_RINGS
//#define ENABLE_DREAMSOUL
//#define ENABLE_NAMING_SCROLL																	// Naming Scroll

/********************************************** End of Item Related Defines **********************************************/

/********************************************** Fix Defines Start **********************************************/

//#define ENABLE_HEAVY_EFFECT_FIX																// Heavy Effect Fix
//#define ENABLE_CONNECT_FIX																	// Connect Fix
//#define ENABLE_NO_COLLISION																	// No Collision with any kind of thing (map, mob, safezone etc)
//#define ENABLE_BOSS_FALL_FIX																// Boss Fall Fix
//#define ENABLE_EFFECT_LOOP_FIX																// Blocks the loop of the effects
//#define ENABLE_WHITE_TEXTURE_FIX															// Fixes any white texture problems
//#define ENABLE_CAMERA_MINIMIZARE_CLIENT_FIX													// Minimize camera bug fix
//#define ENABLE_FIX_VISUAL_CHARACTER															// Visual bleed or poison fix
//#define ENABLE_FIX_HEIGHT_TASKBAR_COLLISION													// Taskbar fixed on resolution
//#define ENABLE_FIX_MOBS_LAG																	// Mob name related text fix
//#define ENABLE_GRID_MOVE_ITEM_FIX															// Grid move item fix for 4 inventories, configure if you have 5 or more (for normal inven)
//#define ENABLE_REFRESH_CONTROL																// Refresh Optimsation
//#define ENABLE_CHAT_SETTINGS																// New Chat 

#if defined(ENABLE_FIX_MOBS_LAG)
	// -> The define ENABLE_FIX_MOBS_LAG have problems in device reseting.
	// -> With this new define all this problems are fixed.
//#define FIX_MOBS_LAG_FIX
#endif

/********************************************** End of Fix Defines **********************************************/

/********************************************** Misc Defines Start **********************************************/

//#define ENABLE_CLIENT_OPTIMISATION															// Client Optimisation
//#define ENABLE_LOADING_WINDOW_RENEWAL														// Loading Animation


#ifdef ENABLE_CLIENT_OPTIMISATION
//#define _ENABLE_PLAYER_CACHE_
////#define _ENABLE_LOAD_DATA_WITH_THREAD_
#endif

//#define ENABLE_FPS_SYSTEM_LIMIT_REWORK														// FPS Limit Rework

////#define ENABLE_AREA_OPTIMISATION															// Client Optimisation
//#define ENABLE_MINIMAP_BOSS_STONE															// Show metinstones and boss in Minimap
//#define ENABLE_WHEEL_MOUSE																	// Can use the scroll bar via windows
//#define ENABLE_NEW_WHITEMARK_MINIMAP														// New whitemark Minimap
//#define ENABLE_MAX_HIT_COUNT_RENEWAL														// Max hit count renewal 16 to 24 hits
//#define ENABLE_EXCHANGE_WINDOW_RENEWAL														// Exchange window renewal
//#define ENABLE_EXTENDED_SHOP_SLOTS															// Shop slot renewal 40 to 80
//#define ENABLE_CHAT_FLAG_AND_PM																// PM And Flag in Chat
//#define ENABLE_REFINE_RENEWAL																// Refine Renewal
//#define ENABLE_CHAT_STACK_SYSTEM															// Chat Stack system
//#define ENABLE_OFFICAL_CHARACTER_SCREEN														// Official Charselect
//#define ENABLE_EXTENDED_ITEMNAME_ON_GROUND													// Extended itemname System
//#define ENABLE_AFFECT_BUFF_REMOVE															// Affect buff remover
//#define ENABLE_AFFECT_POLYMORPH_REMOVE														// Polymorph Remove
//// #define ENABLE_RANDOM_METINSTONE_GENERATOR												// Guard For pixelbot
//#define ENABLE_QUICK_PICKUP																	// Pickup all items quickly
////#define ENABLE_NO_TEXTAIL																	// Optimisation and Safety
//#define ENABLE_CEF_BROWSER																	// Chromium Based Browser
//#define ENABLE_CHECKINOUT_UPDATE															// Safebox - Exchange Check-in/out
//#define WJ_ENABLE_TRADABLE_ICON																// Tradable icon
//#define ENABLE_BUY_WITH_ITEMS																// Buy items with items
//#define ENABLE_MULTIPLE_BUY_ITEMS															// Multi Buy
//#define ENABLE_RENDER_TARGET																// Render Target
//#define ENABLE_DOT_DAMAGE																	// Dot Damage
//#define ENABLE_CRIT_HIT_EFFECT																// Critical damage colored
//#define ENABLE_MINIMAP_TELEPORT																// Teleport to a Location Via Minimap
//#define ENABLE_ATLAS_SCALE																	// Official Atlas Window
//#define ENABLE_WINDOW_ANIMATION																// Window Animation
//#define ENABLE_COLORFUL_DESCRIPTIONS 														// Enables multiple item_desc colors
//#define ENABLE_LINK_IN_CHAT																	// Links in Chat

//#define ENABLE_NEW_DISTANCE_CALC															// Distance Calculation Renewal
//#define ENABLE_GLOBAL_SCALE																	// Global Matrix Scaling
//#define ENABLE_GLOBAL_SCALE_TEXTAIL															// Global Matrix Scaling
//#define ENABLE_COLLISION_RENEWAL															// Collision Renewal
//#define ENABLE_SLOT_TOOLTIP																	// Slot Tooltip
//#define ENABLE_HIDE_COSTUME_SYSTEM															// Hide costume parts
//#define ENABLE_STOP_CHAT																	// Stops the shout receiving when the button is pressed.
//#define ENABLE_DISTANCE_NPC																	// Distance Shopping from NPC's
//#define ENABLE_PM_ALL_SEND_SYSTEM															// Send PM to Everyone (Only gm can send)
//#define ENABLE_AUTO_SHOUT																	// Auto Shout
//#define ENABLE_ZODIAC_TEMPLE_CHAT															// Official Zodiac Notice
//#define ENABLE_SHINING_SYSTEM																// Shining Table
//#define ENABLE_SHOW_STROKE_INFO																// Show Damage Count On Target
//#define ENABLE_CHECK_EFFECT																	// Check Effect
//#define ENABLE_MONSTER_SPECULAR																// Specular

//#define ENABLE_CLIENT_VERSION_AND_ONLY_GM													// Only gm mode and client version
//#define ENABLE_VOTE4BUFF																	// Vote4Buff
//#define ENABLE_PREMIUM_MEMBER_SYSTEM														// Premium Member System
//#define ENABLE_NEW_BLEND_AFFECT																// Dew Effect System
//#define ENABLE_EXTENDED_BLEND_AFFECT														// Permanent Dew System
//#define ENABLE_MESSENGER_TEAM																// Messenger Team
//#define ENABLE_LEADERSHIP_EXTENSION															// Leadership Extension
//#define ENABLE_MAINTENANCE_SYSTEM															// Maintenance System
//#define ENABLE_EXTENDED_BATTLE_PASS															// Battlepass
//#define ENABLE_DUNGEON_MODULES																// New dungeon Modules
//#define ENABLE_6TH_7TH_ATTR																	// 6th 7th attr
//#define ENABLE_BOSS_SHOWER_ON_ATLAS															// Boss Shower Atlas
//#define ENABLE_BOSS_EFFECT_ON_BOSS															// Boss Effect Shower
//#define ENABLE_TELEPORT_TO_A_FRIEND															// Teleport Friend
//#define ENABLE_ADDSTONE_NOT_FAIL_ITEM															// Teleport Friend

////#define ENABLE_LIMIT_MOVING_WINDOWS															// Limit Window Moving for width and height

#ifdef ENABLE_DOT_DAMAGE
	 //#define ENABLE_KMT_DAMAGE
#endif

#ifdef ENABLE_BUY_WITH_ITEMS
#define MAX_SHOP_PRICES 5
#endif
#ifdef ENABLE_MULTIPLE_BUY_ITEMS
#define MULTIPLE_BUY_MAX_COUNT 100
#else
#define MULTIPLE_BUY_MAX_COUNT 0
#endif

//#define ENABLE_NEW_CHAT

/********************************************** End of Misc Defines **********************************************/



/********************************************** Setting Related Defines Start **********************************************/
//#define ENABLE_OUTLINED_NAMES																// Optional Outline deleted names (more efficient)
//#define ENABLE_HIDE_AFFECT_ICONS															// For hiding affect icons
//#define ENABLE_PERSPECTIVE_VIEW																// Perspective System
//#define ENABLE_HIDE_MOB_SYSTEM																// Hide Mobs, Npc's Etc
//#define ENABLE_ANIMATION_SELECT																// Change Animation Window
//#define ENABLE_FONT_SELECT																	// Select Ingame Fonts
//#define ENABLE_HIDE_EFFECTS																	// Hide effects
//#define ENABLE_HIDE_TOOLTIP_EMOJI															// Hide Tooltip Emoji
//#define ENABLE_METIN_SCALE																	// Metinstone Scale
//#define ENABLE_DAMAGE_SIZE_SCALE															// Damage Size Scale
//#define ENABLE_SKYBOX_SELECT																// Skybox Select
//#define ENABLE_SHADER_OPTIONS																// Shader Level Select
//#define ENABLE_SELECT_DAMAGE_TYPE															// Damage Type Select
//#define ENABLE_IMAGE_SCALE																	// Image Scale
//#define ENABLE_CLIP_MASK																	// Clip Mask
//#define WJ_MULTI_TEXTLINE																	// Multi textline addition
//#define ENABLE_BUFFI_SYSTEM
//#define ENABLE_RANGE_ENTITY_OPTIMISATION													// Render Entities in Range
//#define ENABLE_RTT_STATISTICS																// Ping Statistics
//#define ENABLE_TRADE_BLOCKED_ITEM_ICONS
//#define ENABLE_MOVIEMODE_CAMERA																// MovieMode Camera

////#define __USE_CYTHON__																		// Root Cython
////#define __USE_EXTRA_CYTHON__																// Uiscript Cython


#ifdef ENABLE_HIGHLIGHT_SYSTEM
//#define ENABLE_HIDE_HIGHLIGHT																// For hiding highlight effect
#endif

/********************************************** End of Setting Related Defines **********************************************/


/********************************************** Official Type Modules Start **********************************************/

//#define ENABLE_HIDE_WEAPON_WHEN_EMOTE
////#define ENABLE_DETAILED_DEBUG
//#define ENABLE_ETER_PACK_OBSCURING														// Enable EterPack key obscuring (hide heys from binary)
//#define ENABLE_NEW_MODULE_CONFIG														// Config per User
//#define ENABLE_ITEM_PROTO_APPLY_LIMIT
//#define ENABLE_ITEM_TABLE_ATTR_LIMIT
//#define ENABLE_CROWN_SPECULAR

/********************************************** VALIANT2 Unified Modules Start **********************************************/
//#define ENABLE_QUEST_ITEM_DUPE_FIX															// Quest m_dwQuestItemVID dangling pointer & dupe fix
//#define ENABLE_MARRIAGE_CRASH_FIX															// DB Marriage Manager Use-After-Free crash fix
//#define ENABLE_PACKET_BUFFER_FIX															// Packet buffer reallocation & dangling pointer fix
//#define ENABLE_GUILD_MASTER_CRASH_FIX														// Guild ChangeMaster null iterator crash fix
//#define ENABLE_CLIENT_SAFE_GUARD_FIX														// ThingInstance & PythonWindow null-pointer guard
//#define ENABLE_CLIENT_DARK_MODE																// Windows 10/11 immersive dark mode title bar
//#define ENABLE_CRASH_MINIDUMP																// Automatic .dmp crash minidump generator
//#define ENABLE_DROP_INFO_WINDOW																// Floating item & Yang pickup tracker window
//#define ENABLE_BUY_BACK_ITEM																// Repurchase last 12 sold items from NPC
//#define ENABLE_SERVER_ANTIHACK_GUARD														// Authoritative server-side anti-cheat & hack log
/********************************************** VALIANT2 Unified Modules End **********************************************/

/********************************************** Official Type Modules Defines **********************************************/

/*
Information: Some fixes were not added with defines to avoid complexity, you can search @lightwork  or nevoria in binary to find them.
*/


/**************VARIABLES**********************/
using DAM_ULL = unsigned long long;
using DAM_LL = long long;
using HP_ULL = unsigned long long;
using HP_LL = long long;
using QS_USHORT = unsigned short;

#define TITLE_CLIENT "Metin2 - Show the world that who is the greatest!"
