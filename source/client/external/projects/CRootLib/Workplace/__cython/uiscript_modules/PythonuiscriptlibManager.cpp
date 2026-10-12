#include "StdAfx.h"
#include "PythonuiscriptlibManager.h"
#include "python27/Python.h"
#ifdef _DEBUG
	#pragma comment (lib, "uiscriptlib_d.lib")
#else
	#pragma comment (lib, "uiscriptlib.lib")
#endif

struct uiscriptlib_SMethodDef
{
	const char* func_name;
	void (*func)();
};

PyMODINIT_FUNC initacceptguildwardialog();
PyMODINIT_FUNC initacce_absorbwindow();
PyMODINIT_FUNC initacce_combinewindow();
PyMODINIT_FUNC initatlaswindow();
PyMODINIT_FUNC initattachstonedialog();
PyMODINIT_FUNC initbuildguildbuildingwindow();
PyMODINIT_FUNC initchangegradenamedialog();
PyMODINIT_FUNC initchangepassworddialog();
PyMODINIT_FUNC initcharacterdetailswindow();
PyMODINIT_FUNC initcharacterwindow();
PyMODINIT_FUNC initchestdropwindow();
PyMODINIT_FUNC initconnectingdialog();
PyMODINIT_FUNC initcreatecharacterwindow();
PyMODINIT_FUNC initcuberenewalwindow();
PyMODINIT_FUNC initdeclareguildwardialog();
PyMODINIT_FUNC initdragonsoulrefinewindow();
PyMODINIT_FUNC initdragonsoulwindow();
PyMODINIT_FUNC initenergybar();
PyMODINIT_FUNC initequipmentdialog();
PyMODINIT_FUNC initexchangedialog_new();
PyMODINIT_FUNC initexpandedmoneytaskbar();
PyMODINIT_FUNC initexpandedtaskbar();
PyMODINIT_FUNC initfishinggamewindow();
PyMODINIT_FUNC initfishingwindow();
PyMODINIT_FUNC initgameoptiondialog();
PyMODINIT_FUNC initgamewindow();
PyMODINIT_FUNC initgame_option_0_0();
PyMODINIT_FUNC initgame_option_0_1();
PyMODINIT_FUNC initgame_option_1_0();
PyMODINIT_FUNC initgame_option_1_1();
PyMODINIT_FUNC initgame_option_1_2();
PyMODINIT_FUNC initgame_option_2_0();
PyMODINIT_FUNC initgiftbox();
PyMODINIT_FUNC initguildwindow();
PyMODINIT_FUNC initguildwindow_baseinfopage();
PyMODINIT_FUNC initguildwindow_boardpage();
PyMODINIT_FUNC initguildwindow_gradepage();
PyMODINIT_FUNC initguildwindow_guildinfopage();
PyMODINIT_FUNC initguildwindow_guildinfopage_eu();
PyMODINIT_FUNC initguildwindow_guildinfopage_jp();
PyMODINIT_FUNC initguildwindow_guildskillpage();
PyMODINIT_FUNC initguildwindow_memberpage();
PyMODINIT_FUNC inithelpwindow();
PyMODINIT_FUNC inithelpwindow2();
PyMODINIT_FUNC initimekor();
PyMODINIT_FUNC initinputdialog();
PyMODINIT_FUNC initinputdialogwithdescription();
PyMODINIT_FUNC initinputdialogwithdescription2();
PyMODINIT_FUNC initinventorywindow();
PyMODINIT_FUNC inititemquestiondialog();
PyMODINIT_FUNC initlegendarysoulstone();
PyMODINIT_FUNC initloadingwindow();
PyMODINIT_FUNC initloginwindow();
PyMODINIT_FUNC initmallwindow();
PyMODINIT_FUNC initmarklistwindow();
PyMODINIT_FUNC initmessengerwindow();
PyMODINIT_FUNC initminimap();
PyMODINIT_FUNC initmoneyinputdialog();
PyMODINIT_FUNC initmousebuttonwindow();
PyMODINIT_FUNC initmovechanneldialog();
PyMODINIT_FUNC initmultiplebuydialog();
PyMODINIT_FUNC initmusiclistwindow();
PyMODINIT_FUNC initofflineshopinputdialog();
PyMODINIT_FUNC initofflineshopmoneydialog();
PyMODINIT_FUNC initofflineshopwindow();
PyMODINIT_FUNC initpartymemberinfoboard();
PyMODINIT_FUNC initpassivefastsoulstone();
PyMODINIT_FUNC initpassworddialog();
PyMODINIT_FUNC initpickitemdialog();
PyMODINIT_FUNC initpickmoneydialog();
PyMODINIT_FUNC initpopupdialog();
PyMODINIT_FUNC initprivateshopbuilder();
PyMODINIT_FUNC initquestdialog();
PyMODINIT_FUNC initquestiondialog();
PyMODINIT_FUNC initquestiondialog2();
PyMODINIT_FUNC initquestiondialogitem();
PyMODINIT_FUNC initranking();
PyMODINIT_FUNC initrefinedialog();
PyMODINIT_FUNC initrendertargetwindow();
PyMODINIT_FUNC initrestartdialog();
PyMODINIT_FUNC initrightmousebuttonwindow();
PyMODINIT_FUNC initsafeboxwindow();
PyMODINIT_FUNC initsagesoulstone();
PyMODINIT_FUNC initselectcharacterwindow();
PyMODINIT_FUNC initselectempirewindow();
PyMODINIT_FUNC initselectitemwindow();
PyMODINIT_FUNC initshopdialog();
PyMODINIT_FUNC initskillpointresetdialog();
PyMODINIT_FUNC initsoulstone();
PyMODINIT_FUNC initspecialstoragewindow();
PyMODINIT_FUNC initsystemdialog();
PyMODINIT_FUNC inittaskbar();
PyMODINIT_FUNC initwebwindow();
PyMODINIT_FUNC initwhisperdialog();

uiscriptlib_SMethodDef uiscriptlib_init_methods[] =
{
	{ "acceptguildwardialog", initacceptguildwardialog },
	{ "acce_absorbwindow", initacce_absorbwindow },
	{ "acce_combinewindow", initacce_combinewindow },
	{ "atlaswindow", initatlaswindow },
	{ "attachstonedialog", initattachstonedialog },
	{ "buildguildbuildingwindow", initbuildguildbuildingwindow },
	{ "changegradenamedialog", initchangegradenamedialog },
	{ "changepassworddialog", initchangepassworddialog },
	{ "characterdetailswindow", initcharacterdetailswindow },
	{ "characterwindow", initcharacterwindow },
	{ "chestdropwindow", initchestdropwindow },
	{ "connectingdialog", initconnectingdialog },
	{ "createcharacterwindow", initcreatecharacterwindow },
	{ "cuberenewalwindow", initcuberenewalwindow },
	{ "declareguildwardialog", initdeclareguildwardialog },
	{ "dragonsoulrefinewindow", initdragonsoulrefinewindow },
	{ "dragonsoulwindow", initdragonsoulwindow },
	{ "energybar", initenergybar },
	{ "equipmentdialog", initequipmentdialog },
	{ "exchangedialog_new", initexchangedialog_new },
	{ "expandedmoneytaskbar", initexpandedmoneytaskbar },
	{ "expandedtaskbar", initexpandedtaskbar },
	{ "fishinggamewindow", initfishinggamewindow },
	{ "fishingwindow", initfishingwindow },
	{ "gameoptiondialog", initgameoptiondialog },
	{ "gamewindow", initgamewindow },
	{ "game_option_0_0", initgame_option_0_0 },
	{ "game_option_0_1", initgame_option_0_1 },
	{ "game_option_1_0", initgame_option_1_0 },
	{ "game_option_1_1", initgame_option_1_1 },
	{ "game_option_1_2", initgame_option_1_2 },
	{ "game_option_2_0", initgame_option_2_0 },
	{ "giftbox", initgiftbox },
	{ "guildwindow", initguildwindow },
	{ "guildwindow_baseinfopage", initguildwindow_baseinfopage },
	{ "guildwindow_boardpage", initguildwindow_boardpage },
	{ "guildwindow_gradepage", initguildwindow_gradepage },
	{ "guildwindow_guildinfopage", initguildwindow_guildinfopage },
	{ "guildwindow_guildinfopage_eu", initguildwindow_guildinfopage_eu },
	{ "guildwindow_guildinfopage_jp", initguildwindow_guildinfopage_jp },
	{ "guildwindow_guildskillpage", initguildwindow_guildskillpage },
	{ "guildwindow_memberpage", initguildwindow_memberpage },
	{ "helpwindow", inithelpwindow },
	{ "helpwindow2", inithelpwindow2 },
	{ "imekor", initimekor },
	{ "inputdialog", initinputdialog },
	{ "inputdialogwithdescription", initinputdialogwithdescription },
	{ "inputdialogwithdescription2", initinputdialogwithdescription2 },
	{ "inventorywindow", initinventorywindow },
	{ "itemquestiondialog", inititemquestiondialog },
	{ "legendarysoulstone", initlegendarysoulstone },
	{ "loadingwindow", initloadingwindow },
	{ "loginwindow", initloginwindow },
	{ "mallwindow", initmallwindow },
	{ "marklistwindow", initmarklistwindow },
	{ "messengerwindow", initmessengerwindow },
	{ "minimap", initminimap },
	{ "moneyinputdialog", initmoneyinputdialog },
	{ "mousebuttonwindow", initmousebuttonwindow },
	{ "movechanneldialog", initmovechanneldialog },
	{ "multiplebuydialog", initmultiplebuydialog },
	{ "musiclistwindow", initmusiclistwindow },
	{ "offlineshopinputdialog", initofflineshopinputdialog },
	{ "offlineshopmoneydialog", initofflineshopmoneydialog },
	{ "offlineshopwindow", initofflineshopwindow },
	{ "partymemberinfoboard", initpartymemberinfoboard },
	{ "passivefastsoulstone", initpassivefastsoulstone },
	{ "passworddialog", initpassworddialog },
	{ "pickitemdialog", initpickitemdialog },
	{ "pickmoneydialog", initpickmoneydialog },
	{ "popupdialog", initpopupdialog },
	{ "privateshopbuilder", initprivateshopbuilder },
	{ "questdialog", initquestdialog },
	{ "questiondialog", initquestiondialog },
	{ "questiondialog2", initquestiondialog2 },
	{ "questiondialogitem", initquestiondialogitem },
	{ "ranking", initranking },
	{ "refinedialog", initrefinedialog },
	{ "rendertargetwindow", initrendertargetwindow },
	{ "restartdialog", initrestartdialog },
	{ "rightmousebuttonwindow", initrightmousebuttonwindow },
	{ "safeboxwindow", initsafeboxwindow },
	{ "sagesoulstone", initsagesoulstone },
	{ "selectcharacterwindow", initselectcharacterwindow },
	{ "selectempirewindow", initselectempirewindow },
	{ "selectitemwindow", initselectitemwindow },
	{ "shopdialog", initshopdialog },
	{ "skillpointresetdialog", initskillpointresetdialog },
	{ "soulstone", initsoulstone },
	{ "specialstoragewindow", initspecialstoragewindow },
	{ "systemdialog", initsystemdialog },
	{ "taskbar", inittaskbar },
	{ "webwindow", initwebwindow },
	{ "whisperdialog", initwhisperdialog },
	{ NULL, NULL },
};

static PyObject* uiscriptlib_isExist(PyObject *self, PyObject *args)
{
	char* func_name;

	if(!PyArg_ParseTuple(args, "s", &func_name))
		return NULL;

	for (int i = 0; NULL != uiscriptlib_init_methods[i].func_name;i++)
	{
		if (0 == _stricmp(uiscriptlib_init_methods[i].func_name, func_name))
		{
			return Py_BuildValue("i", 1);
		}
	}
	return Py_BuildValue("i", 0);
}

static PyObject* uiscriptlib_moduleImport(PyObject *self, PyObject *args)
{
	char* func_name;

	if(!PyArg_ParseTuple(args, "s", &func_name))
		return NULL;

	for (int i = 0; NULL != uiscriptlib_init_methods[i].func_name;i++)
	{
		if (0 == _stricmp(uiscriptlib_init_methods[i].func_name, func_name))
		{
			uiscriptlib_init_methods[i].func();
			if (PyErr_Occurred())
				return NULL;
			PyObject* m = PyDict_GetItemString(PyImport_GetModuleDict(), uiscriptlib_init_methods[i].func_name);
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

static PyObject* uiscriptlib_getList(PyObject *self, PyObject *args)
{
	int iTupleSize = 0;
	while (NULL != uiscriptlib_init_methods[iTupleSize].func_name) {iTupleSize++;}

	PyObject* retTuple = PyTuple_New(iTupleSize);
	for (int i = 0; NULL != uiscriptlib_init_methods[i].func_name; i++)
	{
		PyObject* retSubString = PyString_FromString(uiscriptlib_init_methods[i].func_name);
		PyTuple_SetItem(retTuple, i, retSubString);
	}
	return retTuple;
}

void inituiscriptlibManager()
{
	static struct PyMethodDef methods[] =
	{
		{"isExist", uiscriptlib_isExist, METH_VARARGS},
		{"moduleImport", uiscriptlib_moduleImport, METH_VARARGS},
		{"getList", uiscriptlib_getList, METH_VARARGS},
		{NULL, NULL},
	};

	PyObject* m;
	m = Py_InitModule("uiscriptlib", methods);
}
