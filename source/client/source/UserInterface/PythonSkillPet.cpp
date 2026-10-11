#include "StdAfx.h"
#include "PythonSkillPet.h"

#include "../EterBase/Poly/Poly.h"
#include "../EterFSLib/FileSystemIncl.hpp"
#include "InstanceBase.h"
#include "PythonPlayer.h"

bool CPythonSkillPet::RegisterSkillPet(const char * c_szFileName)
{
	const auto file = PackGet(c_szFileName);
	if (!file)
		return false;

	CMemoryTextFileLoader textFileLoader;
	textFileLoader.Bind(file->get_size(), file->get_data());
	
	CTokenVector TokenVector;
	for (DWORD i = 0; i < textFileLoader.GetLineCount()-1; ++i)
	{
		if (!textFileLoader.SplitLine(i, &TokenVector, "\t"))
			return false;
		if (DESCPET_TOKEN_TYPE_MAX_NUM > TokenVector.size())
		{
			return false;
		}
		DWORD iSkillIndex = atoi(TokenVector[DESCPET_TOKEN_TYPE_VNUM].c_str());
		if (iSkillIndex == 0)
		{
			//TraceError("SkillPetDesc.line(%d).NO_INDEX_ERROR\n", i + 1);
			continue;
		}

		m_SkillDataPetMap.insert(std::make_pair(iSkillIndex, TSkillDataPet()));
		TSkillDataPet & rSkillData = m_SkillDataPetMap[iSkillIndex];
		// Vnum
		rSkillData.dwSkillIndex = iSkillIndex;		
		// Name
		rSkillData.strName = TokenVector[DESCPET_TOKEN_TYPE_NAME];
		//Icon Name		
		char szIconFileNameHeader[64+1];
		_snprintf(szIconFileNameHeader, sizeof(szIconFileNameHeader), "%sskill/pet/%s.sub", g_strImagePath.c_str(), TokenVector[DESCPET_TOKEN_TYPE_ICON_NAME].c_str());

		rSkillData.strIconFileName = szIconFileNameHeader;

		//Type
		std::map<std::string, DWORD>::iterator itor = m_SkillPetTypeIndexMap.begin();
		for(; itor != m_SkillPetTypeIndexMap.end(); ++itor){
			if (TokenVector[DESCPET_TOKEN_TYPE].compare(itor->first) == 0)
					rSkillData.byType = itor->second;
		}
		rSkillData.strDescription = TokenVector[DESCPET_TOKEN_TYPE_DESCRIPTION];
		rSkillData.dwskilldelay = atoi(TokenVector[DESCPET_TOKEN_TYPE_DELAY].c_str());

		
		rSkillData.pImage = (CGraphicImage *)CResourceManager::Instance().GetResourcePointer(szIconFileNameHeader);			
		
	}

	return true;
}

void CPythonSkillPet::__RegisterNormalIconImage(TSkillDataPet & rData, const char * c_szHeader, const char * c_szImageName)
{
	std::string strFileName = "";
	strFileName += c_szHeader;
	strFileName += c_szImageName;
	strFileName += ".sub";
	rData.pImage = (CGraphicImage *)CResourceManager::Instance().GetResourcePointer(strFileName.c_str());
	
}
void CPythonSkillPet::Destroy()
{
	
	m_SkillDataPetMap.clear();	
}

CPythonSkillPet::SSkillDataPet::SSkillDataPet()
{


	dwSkillIndex = 0;
	strName = "";
	strIconFileName = "";
	byType = 0;			
	strDescription = "";
	dwskilldelay = 0;
	pImage = NULL;	
	
}

CPythonSkillPet::CPythonSkillPet()
{
	petslot[0] = 0;
	petslot[1] = 0;
	petslot[2] = 0;
	petslot[3] = 0;
	petslot[4] = 0;
	petslot[5] = 0;
	petslot[6] = 0;
	petslot[7] = 0;
	m_SkillPetTypeIndexMap.insert(std::map<std::string, DWORD>::value_type("EMPTY", SKILLPET_TYPE_NONE));
	m_SkillPetTypeIndexMap.insert(std::map<std::string, DWORD>::value_type("PASSIVE", SKILLPET_TYPE_PASSIVE));
	m_SkillPetTypeIndexMap.insert(std::map<std::string, DWORD>::value_type("AUTO", SKILLPET_TYPE_AUTO));

}

CPythonSkillPet::~CPythonSkillPet() = default;


void CPythonSkillPet:: SetSkillbySlot(int slot, int skillIndex)
{
	petslot[slot] = skillIndex;
}

BOOL CPythonSkillPet::GetSkillData(DWORD dwSkillIndex, TSkillDataPet ** ppSkillData)
{
	TSkillDataPetMap::iterator it = m_SkillDataPetMap.find(dwSkillIndex);

	if (m_SkillDataPetMap.end() == it)
		return FALSE;

	*ppSkillData = &(it->second);
	return TRUE;
}

BOOL CPythonSkillPet::GetSkillIndex(int slot, int* skillIndex) 
{
	*skillIndex = petslot[slot];
	return TRUE;
}

PyObject * petskillSetSkillSlot(PyObject * poSelf, PyObject * poArgs)
{
	int slot;
	int skillIndex;

	if (!PyTuple_GetInteger(poArgs, 0, &slot))
		return Py_BadArgument();
	if (!PyTuple_GetInteger(poArgs, 1, &skillIndex))
		return Py_BadArgument();
	CPythonSkillPet::Instance().SetSkillbySlot(slot, skillIndex);
	return Py_BuildValue("i", 0);
}

PyObject * petskillGetIconImage(PyObject * poSelf, PyObject * poArgs)
{
	int iSkillIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iSkillIndex))
		return Py_BadArgument();

	CPythonSkillPet::SSkillDataPet * c_pSkillData;
	if (!CPythonSkillPet::Instance().GetSkillData(iSkillIndex, &c_pSkillData))
		return Py_BuildValue("i", 0);

	return Py_BuildValue("i", c_pSkillData->pImage);
}

PyObject * petskillGetSkillbySlot(PyObject * poSelf, PyObject * poArgs)
{
	int slot;
	int skillIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &slot))
		return Py_BadArgument();

	if (slot > 2)
		return Py_BadArgument();

	if (!CPythonSkillPet::Instance().GetSkillIndex(slot, &skillIndex))
		return Py_BuildValue("i", 0);

	return Py_BuildValue("i", skillIndex);

}

PyObject * petskillGetEmptySkill(PyObject * poSelf, PyObject * poArgs)
{
	CGraphicImage * noskillbtn;
	char szIconFileNameHeader[64 + 1];
	_snprintf(szIconFileNameHeader, sizeof(szIconFileNameHeader), "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub");
	noskillbtn = (CGraphicImage *)CResourceManager::Instance().GetResourcePointer(szIconFileNameHeader);
	return Py_BuildValue("i", noskillbtn);
}

void initskillpet()
{
	static PyMethodDef s_methods[] =
	{
		///Variabili setting //
		{ "SetSkillSlot",					petskillSetSkillSlot,						METH_VARARGS },
		//Variabili Get //
		{ "GetIconImage",					petskillGetIconImage,						METH_VARARGS },
		{ "GetSkillbySlot",					petskillGetSkillbySlot ,					METH_VARARGS },
		{ "GetEmptySkill",					petskillGetEmptySkill,						METH_VARARGS },
		{ NULL,										NULL,										NULL },
	};

	PyObject * poModule = Py_InitModule("petskill", s_methods);
}