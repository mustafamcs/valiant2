#include "stdafx.h"
#ifdef ENABLE_BIOLOG_SYSTEM
#include "biolog_system.h"
#include "PythonNetworkStream.h"
BiologSystem::BiologSystem()
{
	Initialize();
}

BiologSystem::~BiologSystem() 
{
	Initialize();
}

void BiologSystem::Initialize()
{
	memset(&m_BiologInformations, 0, sizeof(m_BiologInformations));
	memset(&m_BiologState, 0, sizeof(m_BiologState));
	m_initialize = false;
	m_IsMaxLevel = false;
}

void BiologSystem::LoadBiologInformations(const TPacketGCBiologInformations* pBiologInfo)
{
	memset(&m_BiologInformations, 0, sizeof(m_BiologInformations));
	memcpy(&m_BiologInformations, pBiologInfo, sizeof(m_BiologInformations));
	m_initialize = true;
}

void BiologSystem::LoadBiologState(const TPacketGCBiologUpdate* pBiologState)
{
	memset(&m_BiologState, 0, sizeof(m_BiologState));
	memcpy(&m_BiologState, pBiologState, sizeof(m_BiologState));
	if (m_BiologState.time != 0)
	{
		m_BiologState.time *= 1000;
		m_BiologState.time += timeGetTime();
	}
}

void BiologSystem::SendPacket(BYTE SubHeader, TPacketCGBiologUpgrade data)
{
	TPacketCGBiolog packet;
	packet.header = HEADER_CG_BIOLOG;
	packet.sub_header = SubHeader;

	CPythonNetworkStream& rkNetStream = CPythonNetworkStream::Instance();
	rkNetStream.Send(sizeof(packet), &packet);
	if (SubHeader == SUBHEADER_CG_BIOLOG_UPGRADE)
	{
		rkNetStream.Send(sizeof(data), &data);
	}
}

void BiologSystem::OpenWindow()
{
	if (IsMaxLevel())
	{
		PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "BIOLOG_MAX_LEVEL", Py_BuildValue("()"));
		return;
	}
	if (m_initialize)
	{
		PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "BIOLOG_OpenWindow", Py_BuildValue("()"));
		return;
	}
	SendPacket(SUBHEADER_CG_BIOLOG_OPEN);
}

TPacketGCBiologInformations* BiologSystem::GetInformations()
{
	return &m_BiologInformations;
}

TPacketGCBiologUpdate* BiologSystem::GetState()
{
	return &m_BiologState;
}
/**********************PYTHON MODULE***********************************************/
PyObject* biologSendInformations(PyObject* poSelf, PyObject* poArgs)
{
	TPacketGCBiologInformations* Info = BiologSystem::Instance().GetInformations();
	TPacketGCBiologUpdate* state = BiologSystem::Instance().GetState();

	if (state->state == 1)
	{
		return Py_BuildValue("iiiiiiiiii", Info->mission_stone_vnum, 1,
			Info->mission_bonus[0].type, Info->mission_bonus[0].value, Info->mission_bonus[1].type, Info->mission_bonus[1].value,
			Info->mission_bonus[2].type, Info->mission_bonus[2].value, Info->mission_bonus[3].type, Info->mission_bonus[3].value);
	}
	return Py_BuildValue("iiiiiiiiii", Info->mission_vnum, Info->mission_count,
		Info->mission_bonus[0].type, Info->mission_bonus[0].value, Info->mission_bonus[1].type, Info->mission_bonus[1].value,
		Info->mission_bonus[2].type, Info->mission_bonus[2].value, Info->mission_bonus[3].type, Info->mission_bonus[3].value);
}

PyObject* biologGetMissionLevel(PyObject* poSelf, PyObject* poArgs)
{
	TPacketGCBiologInformations* Info = BiologSystem::Instance().GetInformations();
	return Py_BuildValue("i",Info->mission_level);
}

PyObject* biologOpenWindow(PyObject* poSelf, PyObject* poArgs)
{
	BiologSystem::Instance().OpenWindow();
	return Py_BuildNone();
}

PyObject* biologSendState(PyObject* poSelf, PyObject* poArgs)
{
	TPacketGCBiologUpdate* State = BiologSystem::Instance().GetState();
	DWORD updatetime = State->time;
	if (updatetime < timeGetTime())
	{
		updatetime = 0;
	}
	else
	{
		updatetime -= timeGetTime();
		updatetime /= 1000;
	}
	return Py_BuildValue("ii", State->given_count, updatetime);
}

PyObject* biologDeliveryItem(PyObject* poSelf, PyObject* poArgs)
{
	bool bDeliveryall = false;
	if (!PyTuple_GetBoolean(poArgs, 0, &bDeliveryall))
		return Py_BadArgument();

	bool bChanceItem = false;
	if (!PyTuple_GetBoolean(poArgs, 1, &bChanceItem))
		return Py_BadArgument();

	bool bTimeResetItem = false;
	if (!PyTuple_GetBoolean(poArgs, 2, &bTimeResetItem))
		return Py_BadArgument();

	TPacketCGBiologUpgrade p(bTimeResetItem, bChanceItem, bDeliveryall);
	BiologSystem::Instance().SendPacket(SUBHEADER_CG_BIOLOG_UPGRADE,p);
	return Py_BuildNone();
}

PyObject* biologIsMaxLevel(PyObject* poSelf, PyObject* poArgs)
{
	bool IsMaxLevel = BiologSystem::Instance().IsMaxLevel();
	return Py_BuildValue("i", IsMaxLevel);
}

void initBiolog()
{
	static PyMethodDef s_methods[] =
	{
		{ "OpenWindow", biologOpenWindow, METH_VARARGS },
		{ "SendInformations", biologSendInformations, METH_VARARGS },
		{ "DeliveryItem", biologDeliveryItem, METH_VARARGS },
		{ "GetMissionLevel", biologGetMissionLevel, METH_VARARGS },
		{ "SendState", biologSendState, METH_VARARGS },
		{ "IsMaxLevel", biologIsMaxLevel, METH_VARARGS },

		{nullptr, nullptr, 0 },
	};
	PyObject* poModule = Py_InitModule("biolog", s_methods);
}
#endif