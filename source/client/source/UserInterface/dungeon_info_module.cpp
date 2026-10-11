#include "StdAfx.h"
#ifdef ENABLE_DUNGEON_INFO
#include "dungeon_info.h"

PyObject* dungeonInfoMaxDungeon(PyObject* poSelf, PyObject* poArgs)
{
	BYTE dungeonMaxCount = CDungeonInfo::instance().GetMaxDungeon();
	return Py_BuildValue("i", dungeonMaxCount);
}

PyObject* dungeonInfotimeRequest(PyObject* poSelf, PyObject* poArgs)
{
	CDungeonInfo::instance().TimeRequest();
	return Py_BuildNone();
}

PyObject* dungeonInfoGetTable(PyObject* poSelf, PyObject* poArgs)
{
	BYTE dungeonIdx;
	if (!PyTuple_GetInteger(poArgs, 0, &dungeonIdx))
		return Py_BadArgument();

	TDungeonInfoTable* t =  CDungeonInfo::instance().GetDungonInfoTable(dungeonIdx);
	if (!t)
		return Py_BadArgument();

	return Py_BuildValue("(iiiiii)", t->bossVnum, t->cooldown, t->minLevel, t->maxLevel, t->ticketVnum, t->chestVnum);
}

PyObject* dungeonInfoGetTime(PyObject * poSelf, PyObject * poArgs)
{
	BYTE dungeonIdx;
	if (!PyTuple_GetInteger(poArgs, 0, &dungeonIdx))
		return Py_BadArgument();

	int time = CDungeonInfo::instance().TimeVectorGetTime(dungeonIdx);

	if (time < timeGetTime())
	{
		time = 0;
	}
	else
	{
		time -= timeGetTime();
		time /= 1000;
	}
	return Py_BuildValue("i", time);
}

PyObject* dungeonInfoLoginRequest(PyObject* poSelf, PyObject* poArgs)
{
	BYTE dungeonIdx;
	if (!PyTuple_GetInteger(poArgs, 0, &dungeonIdx))
		return Py_BadArgument();

	CDungeonInfo::instance().DungeonLoginRequest(dungeonIdx);
	return Py_BuildNone();
}

void initDungeonInfo()
{
	static PyMethodDef s_methods[] =
	{
		{"timeRequest", dungeonInfotimeRequest, METH_VARARGS},
		{"maxDungeon", dungeonInfoMaxDungeon, METH_VARARGS},
		{"getTable", dungeonInfoGetTable, METH_VARARGS},
		{"getTime", dungeonInfoGetTime, METH_VARARGS},
		{"loginRequest", dungeonInfoLoginRequest, METH_VARARGS},

		{nullptr, nullptr, 0 },
	};
	PyObject* poModule = Py_InitModule("dungeonInfo", s_methods);
}

#endif