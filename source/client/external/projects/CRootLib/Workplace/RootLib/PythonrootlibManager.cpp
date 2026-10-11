#include "StdAfx.h"
#include "PythonrootlibManager.h"
#include "python27/Python.h"
#ifdef _DEBUG
	#pragma comment (lib, "rootlib_d.lib")
#else
	#pragma comment (lib, "rootlib.lib")
#endif

struct rootlib_SMethodDef
{
	const char* func_name;
	void (*func)();
};

PyMODINIT_FUNC initblend_table();
PyMODINIT_FUNC initcolorcreator();
PyMODINIT_FUNC initcolorInfo();
PyMODINIT_FUNC initconstInfo();
PyMODINIT_FUNC initdragon_soul_refine_settings();
PyMODINIT_FUNC initemotion();
PyMODINIT_FUNC initexception();
PyMODINIT_FUNC initexpandedtaskbar();
PyMODINIT_FUNC initextrainfo();
PyMODINIT_FUNC initgame();
PyMODINIT_FUNC initinterfaceModule();
PyMODINIT_FUNC initintroCreate();
PyMODINIT_FUNC initintroEmpire();
PyMODINIT_FUNC initintroLoading();
PyMODINIT_FUNC initintroLogin();
PyMODINIT_FUNC initintroSelect();
PyMODINIT_FUNC initlightwork();
PyMODINIT_FUNC initlocaleInfo();
PyMODINIT_FUNC initmouseModule();
PyMODINIT_FUNC initnetworkModule();
PyMODINIT_FUNC initplayerSettingModule();
PyMODINIT_FUNC initPrototype();
PyMODINIT_FUNC initRootLibCythonizer();
PyMODINIT_FUNC initserverCommandParser();
PyMODINIT_FUNC initserverInfo();
PyMODINIT_FUNC initstringCommander();
PyMODINIT_FUNC initsystem();
PyMODINIT_FUNC initui();
PyMODINIT_FUNC inituiacce();
PyMODINIT_FUNC inituiAffectShower();
PyMODINIT_FUNC inituiAttachMetin();
PyMODINIT_FUNC inituiattr67add();
PyMODINIT_FUNC inituiaura();
PyMODINIT_FUNC inituibattlepassextended();
PyMODINIT_FUNC inituibosstimer();
PyMODINIT_FUNC inituibuffisystem();
PyMODINIT_FUNC inituiCharacter();
PyMODINIT_FUNC inituicharacterdetails();
PyMODINIT_FUNC inituiChat();
PyMODINIT_FUNC inituiCommon();
PyMODINIT_FUNC inituicuberenewal();
PyMODINIT_FUNC inituidistancenpc();
PyMODINIT_FUNC inituiDragonSoul();
PyMODINIT_FUNC inituidungeontimer();
PyMODINIT_FUNC inituiEquipmentDialog();
PyMODINIT_FUNC inituieventcalendarnew();
PyMODINIT_FUNC inituiExchange();
PyMODINIT_FUNC inituifishgame();
PyMODINIT_FUNC inituiGameButton();
PyMODINIT_FUNC inituiGameOption();
PyMODINIT_FUNC inituigameoptionnew();
PyMODINIT_FUNC inituiGuild();
PyMODINIT_FUNC inituiHelp();
PyMODINIT_FUNC inituiingamelog();
PyMODINIT_FUNC inituiInventory();
PyMODINIT_FUNC inituiitemshopnew();
PyMODINIT_FUNC inituiitemtransactions();
PyMODINIT_FUNC inituimaintenance();
PyMODINIT_FUNC inituiMapNameShower();
PyMODINIT_FUNC inituiMessenger();
PyMODINIT_FUNC inituiminigameblacknwhite();
PyMODINIT_FUNC inituiminigamecatchking();
PyMODINIT_FUNC inituiminigamerumi();
PyMODINIT_FUNC inituiMiniMap();
PyMODINIT_FUNC inituiminingrenewal();
PyMODINIT_FUNC inituinewbiolog();
PyMODINIT_FUNC inituiOption();
PyMODINIT_FUNC inituiParty();
PyMODINIT_FUNC inituipartybonusdistribute();
PyMODINIT_FUNC inituipetsystem();
PyMODINIT_FUNC inituiPhaseCurtain();
PyMODINIT_FUNC inituipickitem();
PyMODINIT_FUNC inituiPickMoney();
PyMODINIT_FUNC inituiPlayerGauge();
PyMODINIT_FUNC inituiPointReset();
PyMODINIT_FUNC inituiPrivateShopBuilder();
PyMODINIT_FUNC inituiQuest();
PyMODINIT_FUNC inituiranking();
PyMODINIT_FUNC inituireadbook();
PyMODINIT_FUNC inituiRefine();
PyMODINIT_FUNC inituirefinerenewal();
PyMODINIT_FUNC inituirendertarget();
PyMODINIT_FUNC inituiRestart();
PyMODINIT_FUNC inituiSafebox();
PyMODINIT_FUNC inituiscriptlocale();
PyMODINIT_FUNC inituisecurity();
PyMODINIT_FUNC inituiselectitem();
PyMODINIT_FUNC inituisendpmall();
PyMODINIT_FUNC inituiShop();
PyMODINIT_FUNC inituishopsearch();
PyMODINIT_FUNC inituiskillcolor();
PyMODINIT_FUNC inituispecialinventory();
PyMODINIT_FUNC inituiswitchbot();
PyMODINIT_FUNC inituiSystem();
PyMODINIT_FUNC inituiTarget();
PyMODINIT_FUNC inituiTaskBar();
PyMODINIT_FUNC inituiTip();
PyMODINIT_FUNC inituiToolTip();
PyMODINIT_FUNC inituiUploadMark();
PyMODINIT_FUNC inituivote4buff();
PyMODINIT_FUNC inituiWeb();
PyMODINIT_FUNC inituiWhisper();
PyMODINIT_FUNC initutils();
PyMODINIT_FUNC initwikiui();

rootlib_SMethodDef rootlib_init_methods[] =
{
	{ "blend_table", initblend_table },
	{ "colorcreator", initcolorcreator },
	{ "colorInfo", initcolorInfo },
	{ "constInfo", initconstInfo },
	{ "dragon_soul_refine_settings", initdragon_soul_refine_settings },
	{ "emotion", initemotion },
	{ "exception", initexception },
	{ "expandedtaskbar", initexpandedtaskbar },
	{ "extrainfo", initextrainfo },
	{ "game", initgame },
	{ "interfaceModule", initinterfaceModule },
	{ "introCreate", initintroCreate },
	{ "introEmpire", initintroEmpire },
	{ "introLoading", initintroLoading },
	{ "introLogin", initintroLogin },
	{ "introSelect", initintroSelect },
	{ "lightwork", initlightwork },
	{ "localeInfo", initlocaleInfo },
	{ "mouseModule", initmouseModule },
	{ "networkModule", initnetworkModule },
	{ "playerSettingModule", initplayerSettingModule },
	{ "Prototype", initPrototype },
	{ "RootLibCythonizer", initRootLibCythonizer },
	{ "serverCommandParser", initserverCommandParser },
	{ "serverInfo", initserverInfo },
	{ "stringCommander", initstringCommander },
	{ "system", initsystem },
	{ "ui", initui },
	{ "uiacce", inituiacce },
	{ "uiAffectShower", inituiAffectShower },
	{ "uiAttachMetin", inituiAttachMetin },
	{ "uiattr67add", inituiattr67add },
	{ "uiaura", inituiaura },
	{ "uibattlepassextended", inituibattlepassextended },
	{ "uibosstimer", inituibosstimer },
	{ "uibuffisystem", inituibuffisystem },
	{ "uiCharacter", inituiCharacter },
	{ "uicharacterdetails", inituicharacterdetails },
	{ "uiChat", inituiChat },
	{ "uiCommon", inituiCommon },
	{ "uicuberenewal", inituicuberenewal },
	{ "uidistancenpc", inituidistancenpc },
	{ "uiDragonSoul", inituiDragonSoul },
	{ "uidungeontimer", inituidungeontimer },
	{ "uiEquipmentDialog", inituiEquipmentDialog },
	{ "uieventcalendarnew", inituieventcalendarnew },
	{ "uiExchange", inituiExchange },
	{ "uifishgame", inituifishgame },
	{ "uiGameButton", inituiGameButton },
	{ "uiGameOption", inituiGameOption },
	{ "uigameoptionnew", inituigameoptionnew },
	{ "uiGuild", inituiGuild },
	{ "uiHelp", inituiHelp },
	{ "uiingamelog", inituiingamelog },
	{ "uiInventory", inituiInventory },
	{ "uiitemshopnew", inituiitemshopnew },
	{ "uiitemtransactions", inituiitemtransactions },
	{ "uimaintenance", inituimaintenance },
	{ "uiMapNameShower", inituiMapNameShower },
	{ "uiMessenger", inituiMessenger },
	{ "uiminigameblacknwhite", inituiminigameblacknwhite },
	{ "uiminigamecatchking", inituiminigamecatchking },
	{ "uiminigamerumi", inituiminigamerumi },
	{ "uiMiniMap", inituiMiniMap },
	{ "uiminingrenewal", inituiminingrenewal },
	{ "uinewbiolog", inituinewbiolog },
	{ "uiOption", inituiOption },
	{ "uiParty", inituiParty },
	{ "uipartybonusdistribute", inituipartybonusdistribute },
	{ "uipetsystem", inituipetsystem },
	{ "uiPhaseCurtain", inituiPhaseCurtain },
	{ "uipickitem", inituipickitem },
	{ "uiPickMoney", inituiPickMoney },
	{ "uiPlayerGauge", inituiPlayerGauge },
	{ "uiPointReset", inituiPointReset },
	{ "uiPrivateShopBuilder", inituiPrivateShopBuilder },
	{ "uiQuest", inituiQuest },
	{ "uiranking", inituiranking },
	{ "uireadbook", inituireadbook },
	{ "uiRefine", inituiRefine },
	{ "uirefinerenewal", inituirefinerenewal },
	{ "uirendertarget", inituirendertarget },
	{ "uiRestart", inituiRestart },
	{ "uiSafebox", inituiSafebox },
	{ "uiscriptlocale", inituiscriptlocale },
	{ "uisecurity", inituisecurity },
	{ "uiselectitem", inituiselectitem },
	{ "uisendpmall", inituisendpmall },
	{ "uiShop", inituiShop },
	{ "uishopsearch", inituishopsearch },
	{ "uiskillcolor", inituiskillcolor },
	{ "uispecialinventory", inituispecialinventory },
	{ "uiswitchbot", inituiswitchbot },
	{ "uiSystem", inituiSystem },
	{ "uiTarget", inituiTarget },
	{ "uiTaskBar", inituiTaskBar },
	{ "uiTip", inituiTip },
	{ "uiToolTip", inituiToolTip },
	{ "uiUploadMark", inituiUploadMark },
	{ "uivote4buff", inituivote4buff },
	{ "uiWeb", inituiWeb },
	{ "uiWhisper", inituiWhisper },
	{ "utils", initutils },
	{ "wikiui", initwikiui },
	{ NULL, NULL },
};

static PyObject* rootlib_isExist(PyObject *self, PyObject *args)
{
	char* func_name;

	if(!PyArg_ParseTuple(args, "s", &func_name))
		return NULL;

	for (int i = 0; NULL != rootlib_init_methods[i].func_name;i++)
	{
		if (0 == _stricmp(rootlib_init_methods[i].func_name, func_name))
		{
			return Py_BuildValue("i", 1);
		}
	}
	return Py_BuildValue("i", 0);
}

static PyObject* rootlib_moduleImport(PyObject *self, PyObject *args)
{
	char* func_name;

	if(!PyArg_ParseTuple(args, "s", &func_name))
		return NULL;

	for (int i = 0; NULL != rootlib_init_methods[i].func_name;i++)
	{
		if (0 == _stricmp(rootlib_init_methods[i].func_name, func_name))
		{
			rootlib_init_methods[i].func();
			if (PyErr_Occurred())
				return NULL;
			PyObject* m = PyDict_GetItemString(PyImport_GetModuleDict(), rootlib_init_methods[i].func_name);
			if (m == NULL) {
				PyErr_SetString(PyExc_SystemError,
					"dynamic module not initialized properly");
				return NULL;
			}
			Py_INCREF(m);
			return Py_BuildValue("S", m);
		}
	}
	return NULL;
}

static PyObject* rootlib_getList(PyObject *self, PyObject *args)
{
	int iTupleSize = 0;
	while (NULL != rootlib_init_methods[iTupleSize].func_name) {iTupleSize++;}

	PyObject* retTuple = PyTuple_New(iTupleSize);
	for (int i = 0; NULL != rootlib_init_methods[i].func_name; i++)
	{
		PyObject* retSubString = PyString_FromString(rootlib_init_methods[i].func_name);
		PyTuple_SetItem(retTuple, i, retSubString);
	}
	return retTuple;
}

void initrootlibManager()
{
	static struct PyMethodDef methods[] =
	{
		{"isExist", rootlib_isExist, METH_VARARGS},
		{"moduleImport", rootlib_moduleImport, METH_VARARGS},
		{"getList", rootlib_getList, METH_VARARGS},
		{NULL, NULL},
	};

	PyObject* m;
	m = Py_InitModule("rootlib", methods);
}
