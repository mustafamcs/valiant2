#include "StdAfx.h"
#ifdef ENABLE_NEW_PET_SYSTEM
#include "PythonNetworkStream.h"

bool CPythonNetworkStream::RecvNewPet()
{
	TNewPetGCPacket packet;
	if (!Recv(sizeof(TNewPetGCPacket), &packet))
	{
		TraceError("New Pet Packet Recovery Error");
		return false;
	}

	WORD buffersize = packet.size - sizeof(TNewPetGCPacket);
	bool ret = true;

	switch (packet.subHeader)
	{
		case SUB_GC_UNSUMMON: { RecvNewPetUnSummon(); break; }
		case SUB_GC_UPDATE: { ret = RecvNewPetUpdate(); break; }
		case SUB_GC_UPDATE_EXP: { ret = RecvNewPetUpdateExp(); break; }
		default: { TraceError("New Pet noting sub header %d", packet.subHeader); ret = false;}
	}
	return ret;
}

bool CPythonNetworkStream::RecvNewPetUpdate()
{
	TNewPetInfo subPack;
	if (!Recv(sizeof(TNewPetInfo), &subPack))
	{
		return false;
	}

	PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "SetPetInformations",
		Py_BuildValue("(iiii)", subPack.level, subPack.evolution, subPack.type, subPack.star));

	PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "SetPetSkin", Py_BuildValue("(ii)", subPack.skinCount, subPack.skinVnum));
	PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "SetPetExp", Py_BuildValue("(ii)", subPack.exp, subPack.nextExp));


	PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "SetPetBonus", Py_BuildValue("(iii)", subPack.bonus[0], subPack.bonus[1], subPack.bonus[2]));
	
	for (int i = 0; i < 8; i++)
	{
		if (subPack.evolution != 3)
			break;
		if (subPack.skill[i].level == 62)
			break;

		PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "SetPetskill", Py_BuildValue("(iii)", i, subPack.skill[i].type, subPack.skill[i].level));
	}

	return true;
}

void CPythonNetworkStream::RecvNewPetUnSummon()
{
	PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "PetUnsummon", Py_BuildValue("()"));
}

bool CPythonNetworkStream::RecvNewPetUpdateExp()
{
	DWORD subPack;
	if (!Recv(sizeof(DWORD), &subPack))
	{
		return false;
	}

	PyCallClassMemberFunc(CPythonNetworkStream::instance().GetGameWindow(), "SetPetExp", Py_BuildValue("(ii)", subPack, 0));
	return true;
}

void CPythonNetworkStream::SendNewPetPacket(BYTE subHeader)
{
	TNewPetCGPacket packet;
	packet.header = HEADER_CG_NEW_PET;
	packet.subHeader = subHeader;

	if (!Send(sizeof(packet), &packet))
	{
		TraceError("New Pet Send Packet Error sub %d", subHeader);
		return;
	}
}


PyObject* newpetTypeIncrease(PyObject* poSelf, PyObject* poArgs)
{
	CPythonNetworkStream::Instance().SendNewPetPacket(SUB_CG_TYPE_INCREASE);
	return Py_BuildNone();
}

PyObject* newpetEvolutionIncrease(PyObject* poSelf, PyObject* poArgs)
{
	CPythonNetworkStream::Instance().SendNewPetPacket(SUB_CG_EVOLUTION_INCREASE);
	return Py_BuildNone();
}

PyObject* newpetStarIncrease(PyObject* poSelf, PyObject* poArgs)
{
	CPythonNetworkStream::Instance().SendNewPetPacket(SUB_CG_STAR_INCREASE);
	return Py_BuildNone();
}

PyObject* newpetBonusChange(PyObject* poSelf, PyObject* poArgs)
{
	CPythonNetworkStream::Instance().SendNewPetPacket(SUB_CG_BONUS_CHANGE);
	return Py_BuildNone();
}

PyObject* newpetActivateSkin(PyObject* poSelf, PyObject* poArgs)
{
	CPythonNetworkStream::Instance().SendNewPetPacket(SUB_CG_ACTIVATE_SKIN);
	return Py_BuildNone();
}

PyObject* newpetSkinChange(PyObject* poSelf, PyObject* poArgs)
{
	BYTE skinIdx;
	if (!PyTuple_GetInteger(poArgs, 0, &skinIdx))
		return Py_BadArgument();

	if (skinIdx >= 6)
		return Py_BadArgument();

	TNewPetCGPacket packet;
	packet.header = HEADER_CG_NEW_PET;
	packet.subHeader = SUB_CG_SKIN_CHANGE;

	CPythonNetworkStream& rkNetStream = CPythonNetworkStream::Instance();
	if (!rkNetStream.Send(sizeof(packet), &packet))
	{
		TraceError("New Pet Skin change error packet");
		return Py_BuildNone();
	}

	if (!rkNetStream.Send(sizeof(skinIdx), &skinIdx))
	{
		TraceError("New Pet Skin change error index");
		return Py_BuildNone();
	}

	return Py_BuildNone();
}

void initnewpet()
{
	static PyMethodDef s_methods[] =
	{
		{ "TypeIncrease",					newpetTypeIncrease,						METH_VARARGS },
		{ "EvolutionIncrease",				newpetEvolutionIncrease,				METH_VARARGS },
		{ "StarIncrease",					newpetStarIncrease,						METH_VARARGS },
		{ "BonusChange",					newpetBonusChange,						METH_VARARGS },
		{ "ActivateSkin",					newpetActivateSkin,						METH_VARARGS },
		{ "SkinChange",						newpetSkinChange,						METH_VARARGS },
		{ NULL,								NULL,									NULL		 },
	};

	PyObject* poModule = Py_InitModule("newpet", s_methods);
}
#endif