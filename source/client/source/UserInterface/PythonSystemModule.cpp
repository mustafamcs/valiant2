#include "StdAfx.h"
#include "PythonSystem.h"

PyObject* systemGetWidth(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().GetWidth());
}

PyObject* systemGetHeight(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().GetHeight());
}

PyObject* systemSetInterfaceHandler(PyObject* poSelf, PyObject* poArgs)
{
	PyObject* poHandler;
	if (!PyTuple_GetObject(poArgs, 0, &poHandler))
		return Py_BuildException();

	CPythonSystem::Instance().SetInterfaceHandler(poHandler);
	return Py_BuildNone();
}

PyObject* systemDestroyInterfaceHandler(PyObject* poSelf, PyObject* poArgs)
{
	CPythonSystem::Instance().DestroyInterfaceHandler();
	return Py_BuildNone();
}

PyObject* systemisInterfaceConfig(PyObject* poSelf, PyObject* poArgs)
{
	int isInterfaceConfig = CPythonSystem::Instance().isInterfaceConfig();
	return Py_BuildValue("i", isInterfaceConfig);
}

PyObject* systemSaveWindowStatus(PyObject* poSelf, PyObject* poArgs)
{
	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iIndex))
		return Py_BuildException();

	int iVisible;
	if (!PyTuple_GetInteger(poArgs, 1, &iVisible))
		return Py_BuildException();

	int iMinimized;
	if (!PyTuple_GetInteger(poArgs, 2, &iMinimized))
		return Py_BuildException();

	int ix;
	if (!PyTuple_GetInteger(poArgs, 3, &ix))
		return Py_BuildException();

	int iy;
	if (!PyTuple_GetInteger(poArgs, 4, &iy))
		return Py_BuildException();

	int iHeight;
	if (!PyTuple_GetInteger(poArgs, 5, &iHeight))
		return Py_BuildException();

	CPythonSystem::Instance().SaveWindowStatus(iIndex, iVisible, iMinimized, ix, iy, iHeight);
	return Py_BuildNone();
}

PyObject* systemGetWindowStatus(PyObject* poSelf, PyObject* poArgs)
{
	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iIndex))
		return Py_BuildException();

	const CPythonSystem::TWindowStatus& c_rWindowStatus = CPythonSystem::Instance().GetWindowStatusReference(iIndex);
	return Py_BuildValue("iiiii", c_rWindowStatus.isVisible,
		c_rWindowStatus.isMinimized,
		c_rWindowStatus.ixPosition,
		c_rWindowStatus.iyPosition,
		c_rWindowStatus.iHeight);
}

PyObject* systemGetConfig(PyObject* poSelf, PyObject* poArgs)
{
	CPythonSystem::TConfig* tmp = CPythonSystem::Instance().GetConfig();

	int iRes = CPythonSystem::Instance().GetResolutionIndex(tmp->width, tmp->height, tmp->bpp);
	int iFrequency = CPythonSystem::Instance().GetFrequencyIndex(iRes, tmp->frequency);

	return Py_BuildValue("iiiiii", iRes,
		iFrequency,
		tmp->is_software_cursor,
		tmp->is_object_culling,
		tmp->gamma,
		tmp->iDistance);
}

PyObject* systemSetSaveID(PyObject* poSelf, PyObject* poArgs)
{
	int iValue;
	if (!PyTuple_GetInteger(poArgs, 0, &iValue))
		return Py_BuildException();

	char* szSaveID;
	if (!PyTuple_GetString(poArgs, 1, &szSaveID))
		return Py_BuildException();

	CPythonSystem::Instance().SetSaveID(iValue, szSaveID);
	return Py_BuildNone();
}

PyObject* systemisSaveID(PyObject* poSelf, PyObject* poArgs)
{
	int value = CPythonSystem::Instance().IsSaveID();
	return Py_BuildValue("i", value);
}

PyObject* systemGetSaveID(PyObject* poSelf, PyObject* poArgs)
{
	const char* c_szSaveID = CPythonSystem::Instance().GetSaveID();
	return Py_BuildValue("s", c_szSaveID);
}

PyObject* systemGetMusicVolume(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("f", CPythonSystem::Instance().GetMusicVolume());
}

PyObject* systemGetSoundVolume(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().GetSoundVolume());
}

PyObject* systemSetMusicVolume(PyObject* poSelf, PyObject* poArgs)
{
	float fVolume;
	if (!PyTuple_GetFloat(poArgs, 0, &fVolume))
		return Py_BuildException();

	CPythonSystem::Instance().SetMusicVolume(fVolume);
	return Py_BuildNone();
}

PyObject* systemSetSoundVolumef(PyObject* poSelf, PyObject* poArgs)
{
	float fVolume;
	if (!PyTuple_GetFloat(poArgs, 0, &fVolume))
		return Py_BuildException();

	CPythonSystem::Instance().SetSoundVolumef(fVolume);
	return Py_BuildNone();
}

PyObject* systemIsSoftwareCursor(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().IsSoftwareCursor());
}

PyObject* systemSetViewChatFlag(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	CPythonSystem::Instance().SetViewChatFlag(iFlag);

	return Py_BuildNone();
}

PyObject* systemIsViewChat(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().IsViewChat());
}

PyObject* systemSetAlwaysShowNameFlag(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	CPythonSystem::Instance().SetAlwaysShowNameFlag(iFlag);

	return Py_BuildNone();
}

PyObject* systemSetShowDamageFlag(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	CPythonSystem::Instance().SetShowDamageFlag(iFlag);

	return Py_BuildNone();
}

PyObject* systemSetShowSalesTextFlag(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	CPythonSystem::Instance().SetShowSalesTextFlag(iFlag);

	return Py_BuildNone();
}

#ifdef WJ_SHOW_MOB_INFO
#include "PythonCharacterManager.h"
#include "PythonNonPlayer.h"
#include "PythonSystem.h"
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBAIFLAG)
PyObject* systemIsShowMobAIFlag(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().IsShowMobAIFlag());
}
PyObject* systemSetShowMobAIFlag(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	CPythonSystem::Instance().SetShowMobAIFlagFlag(iFlag);

	for (CPythonCharacterManager::CharacterIterator it = CPythonCharacterManager::Instance().CharacterInstanceBegin(), ti = CPythonCharacterManager::Instance().CharacterInstanceEnd();
		it != ti;
		++it)
	{
		CInstanceBase* pkInst = *it;
		if (pkInst && pkInst->IsEnemy())
			pkInst->MobInfoAiFlagRefresh();
	}
	return Py_BuildNone();
}
#endif
#if defined(WJ_SHOW_MOB_INFO) && defined(ENABLE_SHOW_MOBLEVEL)
PyObject* systemIsShowMobLevel(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().IsShowMobLevel());
}
PyObject* systemSetShowMobLevel(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	CPythonSystem::Instance().SetShowMobLevelFlag(iFlag);

	for (CPythonCharacterManager::CharacterIterator it = CPythonCharacterManager::Instance().CharacterInstanceBegin(), ti = CPythonCharacterManager::Instance().CharacterInstanceEnd();
		it != ti;
		++it)
	{
		CInstanceBase* pkInst = *it;
		if (pkInst && pkInst->IsEnemy())
			pkInst->MobInfoLevelRefresh();
	}
	return Py_BuildNone();
}
#endif
#endif

PyObject* systemIsAlwaysShowName(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().IsAlwaysShowName());
}

PyObject* systemIsShowDamage(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().IsShowDamage());
}

PyObject* systemIsShowSalesText(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().IsShowSalesText());
}

PyObject* systemSetConfig(PyObject* poSelf, PyObject* poArgs)
{
	int res_index;
	int width;
	int height;
	int bpp;
	int frequency_index;
	int frequency;
	int software_cursor;
	int shadow;
	int object_culling;
	int gamma;
	int distance;

	if (!PyTuple_GetInteger(poArgs, 0, &res_index))
		return Py_BuildException();

	if (!PyTuple_GetInteger(poArgs, 1, &frequency_index))
		return Py_BuildException();

	if (!PyTuple_GetInteger(poArgs, 2, &software_cursor))
		return Py_BuildException();

	if (!PyTuple_GetInteger(poArgs, 3, &shadow))
		return Py_BuildException();

	if (!PyTuple_GetInteger(poArgs, 4, &object_culling))
		return Py_BuildException();

	if (!PyTuple_GetInteger(poArgs, 7, &gamma))
		return Py_BuildException();

	if (!PyTuple_GetInteger(poArgs, 8, &distance))
		return Py_BuildException();

	if (!CPythonSystem::Instance().GetResolution(res_index, (DWORD*)&width, (DWORD*)&height, (DWORD*)&bpp))
		return Py_BuildNone();

	if (!CPythonSystem::Instance().GetFrequency(res_index, frequency_index, (DWORD*)&frequency))
		return Py_BuildNone();

	CPythonSystem::TConfig tmp;

	memcpy(&tmp, CPythonSystem::Instance().GetConfig(), sizeof(tmp));

	tmp.width = width;
	tmp.height = height;
	tmp.bpp = bpp;
	tmp.frequency = frequency;
	tmp.is_software_cursor = software_cursor ? true : false;
	tmp.is_object_culling = object_culling ? true : false;
	tmp.gamma = gamma;
	tmp.iDistance = distance;

	CPythonSystem::Instance().SetConfig(&tmp);
	return Py_BuildNone();
}

PyObject* systemApplyConfig(PyObject* poSelf, PyObject* poArgs)
{
	CPythonSystem::Instance().ApplyConfig();
	return Py_BuildNone();
}

PyObject* systemSaveConfig(PyObject* poSelf, PyObject* poArgs)
{
	int ret = CPythonSystem::Instance().SaveConfig();
	return Py_BuildValue("i", ret);
}

PyObject* systemGetResolutionCount(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().GetResolutionCount());
}

PyObject* systemGetFrequencyCount(PyObject* poSelf, PyObject* poArgs)
{
	int	index;

	if (!PyTuple_GetInteger(poArgs, 0, &index))
		return Py_BuildException();

	return Py_BuildValue("i", CPythonSystem::Instance().GetFrequencyCount(index));
}

PyObject* systemGetResolution(PyObject* poSelf, PyObject* poArgs)
{
	int	index;
	DWORD width = 0, height = 0, bpp = 0;

	if (!PyTuple_GetInteger(poArgs, 0, &index))
		return Py_BuildException();

	CPythonSystem::Instance().GetResolution(index, &width, &height, &bpp);
	return Py_BuildValue("iii", width, height, bpp);
}

PyObject* systemGetCurrentResolution(PyObject* poSelf, PyObject* poArgs)
{
	CPythonSystem::TConfig* tmp = CPythonSystem::Instance().GetConfig();
	return Py_BuildValue("iii", tmp->width, tmp->height, tmp->bpp);
}

PyObject* systemGetFrequency(PyObject* poSelf, PyObject* poArgs)
{
	int	index, frequency_index;
	DWORD frequency = 0;

	if (!PyTuple_GetInteger(poArgs, 0, &index))
		return Py_BuildException();

	if (!PyTuple_GetInteger(poArgs, 1, &frequency_index))
		return Py_BuildException();

	CPythonSystem::Instance().GetFrequency(index, frequency_index, &frequency);
	return Py_BuildValue("i", frequency);
}

PyObject* systemGetShadowLevel(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().GetShadowLevel());
}

PyObject* systemSetShadowLevel(PyObject* poSelf, PyObject* poArgs)
{
	int level;

	if (!PyTuple_GetInteger(poArgs, 0, &level))
		return Py_BuildException();

	if (level > 0)
		CPythonSystem::Instance().SetShadowLevel(level);

	return Py_BuildNone();
}

#ifdef ENABLE_OUTLINED_NAMES
PyObject* systemSetNamesType(PyObject* poSelf, PyObject* poArgs)
{
	int type;

	if (PyTuple_GetInteger(poArgs, 0, &type))
	{
		CPythonSystem::Instance().SetNamesType(type == 0 ? false : true);
	}

	return Py_BuildNone();
}

PyObject* systemGetNamesType(PyObject* poSelf, PyObject* poArgs) {
	return Py_BuildValue("b", CPythonSystem::Instance().GetNamesType());
}
#endif

#ifdef ENABLE_HIDE_AFFECT_ICONS
PyObject* systemSetEffectIconShow(PyObject* poSelf, PyObject* poArgs)
{
	int type;

	if (PyTuple_GetInteger(poArgs, 0, &type))
	{
		CPythonSystem::Instance().SetEffectIconShow(type == 0 ? false : true);
	}

	return Py_BuildNone();
}

PyObject* systemIsAffectIconShow(PyObject* poSelf, PyObject* poArgs) {
	return Py_BuildValue("b", CPythonSystem::Instance().IsAffectIconShow());
}
#endif

#ifdef ENABLE_PERSPECTIVE_VIEW
PyObject* systemSetFieldPerspective(PyObject* poSelf, PyObject* poArgs)
{
	float fValue;
	if (!PyTuple_GetFloat(poArgs, 0, &fValue))
		return Py_BuildException();

	CPythonSystem::Instance().SetFieldPerspective(fValue);
	return Py_BuildNone();
}

PyObject* systemGetFieldPerspective(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("f", CPythonSystem::Instance().GetFieldPerspective());
}
#endif

#ifdef ENABLE_HIDE_HIGHLIGHT
PyObject* systemSetHighlightShow(PyObject* poSelf, PyObject* poArgs)
{
	int type;

	if (PyTuple_GetInteger(poArgs, 0, &type))
	{
		CPythonSystem::Instance().SetHighlightShow(type == 0 ? false : true);
	}

	return Py_BuildNone();
}

PyObject* systemIsHighlightShow(PyObject* poSelf, PyObject* poArgs) {
	return Py_BuildValue("b", CPythonSystem::Instance().IsHighlightShow());
}
#endif

#ifdef ENABLE_HIDE_MOB_SYSTEM
PyObject* systemSetMobTypeHiddenState(PyObject* poSelf, PyObject* poArgs)
{
	int type;
	bool state = false;

	if (!PyTuple_GetInteger(poArgs, 0, &type))
	{
		return Py_BuildNone();
	}

	if (!PyTuple_GetBoolean(poArgs, 1, &state))
	{
		return Py_BuildNone();
	}

	CPythonSystem::Instance().SetHiddenState(type, state);
	return Py_BuildNone();
}

PyObject* systemIsMobTypeHidden(PyObject* poSelf, PyObject* poArgs)
{
	int type;
	if (PyTuple_GetInteger(poArgs, 0, &type))
	{
		return Py_BuildValue("b", CPythonSystem::Instance().GetHiddenState(type));
	}
	return Py_BuildNone();
}
#endif

#ifdef ENABLE_ANIMATION_SELECT
PyObject* systemSetAnimation(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();
	CPythonSystem::Instance().SetAnimation(iFlag);
	return Py_BuildNone();
}

PyObject* systemGetCurrentAnimation(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().GetAnimation());
}
#endif

#ifdef ENABLE_FONT_SELECT
PyObject* systemSetFontType(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();
	CPythonSystem::Instance().SetFontType(iFlag);
	return Py_BuildNone();
}

PyObject* systemGetFontType(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().GetFontType());
}
#endif

#ifdef ENABLE_HIDE_EFFECTS
PyObject* systemSetEffectActive(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();
	CPythonSystem::Instance().SetEffectActive(iFlag);
	return Py_BuildNone();
}

PyObject* systemIsEffectActive(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().IsEffectActive());
}
#endif

#ifdef ENABLE_HIDE_TOOLTIP_EMOJI
PyObject* systemSetEmojiStatus(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();
	CPythonSystem::Instance().SetEmojiStatus(iFlag);
	return Py_BuildNone();
}

PyObject* systemGetEmojiStatus(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().GetEmojiStatus());
}
#endif

#ifdef ENABLE_METIN_SCALE
PyObject* systemSetMetinstoneScale(PyObject* poSelf, PyObject* poArgs)
{
	float fValue;
	if (!PyTuple_GetFloat(poArgs, 0, &fValue))
		return Py_BuildException();

	CPythonSystem::Instance().SetMetinstoneScale(fValue);
	return Py_BuildNone();
}

PyObject* systemGetMetinstoneScale(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("f", CPythonSystem::Instance().GetMetinstoneScale());
}
#endif

#ifdef ENABLE_DAMAGE_SIZE_SCALE
PyObject* systemSetDamageTextureScale(PyObject* poSelf, PyObject* poArgs)
{
	float fValue;
	if (!PyTuple_GetFloat(poArgs, 0, &fValue))
		return Py_BuildException();

	CPythonSystem::Instance().SetDamageTextureScale(fValue);
	return Py_BuildNone();
}

PyObject* systemGetDamageTextureScale(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("f", CPythonSystem::Instance().GetDamageTextureScale());
}
#endif

#ifdef ENABLE_SKYBOX_SELECT
PyObject* systemSetSkyBox(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	CPythonSystem::Instance().SetSkyBoxType(iFlag);
	return Py_BuildNone();
}

PyObject* systemGetSkyBox(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonSystem::Instance().GetSkyBox());
}
#endif

#ifdef ENABLE_RANGE_ENTITY_OPTIMISATION
PyObject* systemSetEntityRange(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	DWORD range = ENTITY_FAR;

	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	if (range > ENTITY_FAR)
		range = ENTITY_FAR;

	if (iFlag == 0)
	{
		range = ENTITY_CLOSE;
	}
	else if (iFlag == 1)
	{
		range = ENTITY_MIDDLE;
	}

	CPythonSystem::Instance().SetShowOnlyEntityInRange(range);
	return Py_BuildNone();
}

PyObject* systemGetEntityRange(PyObject* poSelf, PyObject* poArgs)
{
	DWORD currentRange = CPythonSystem::Instance().GetEntityRange();
	BYTE rangeidx;

	if (currentRange == ENTITY_FAR)
	{
		rangeidx = 2;
	}
	else if (currentRange == ENTITY_MIDDLE)
	{
		rangeidx = 1;
	}
	else
	{
		rangeidx = 0;
	}

	return Py_BuildValue("i", rangeidx);
}

#endif

#ifdef ENABLE_AREA_OPTIMISATION
PyObject* systemSetLoadingDistance(PyObject* poSelf, PyObject* poArgs)
{
	float fValue;
	if (!PyTuple_GetFloat(poArgs, 0, &fValue))
		return Py_BuildException();

	CPythonSystem::Instance().SetLoadingDistance(fValue);
	return Py_BuildNone();
}

PyObject* systemGetLoadingDistance(PyObject* poSelf, PyObject* poArgs)
{

	return Py_BuildValue("f", CPythonSystem::Instance().GetLoadingDistance());
}
#endif

#ifdef ENABLE_SELECT_DAMAGE_TYPE
PyObject* systemSetDamageType(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	CPythonSystem::Instance().SetDamageType(iFlag);
	return Py_BuildNone();
}

PyObject* systemGetDamageType(PyObject* poSelf, PyObject* poArgs)
{
	if (CPythonSystem::Instance().GetDamageType() > 2)
		CPythonSystem::Instance().SetDamageType(0);

	return Py_BuildValue("i", CPythonSystem::Instance().GetDamageType());
}

PyObject* systemSetDamageTypeRenewal(PyObject* poSelf, PyObject* poArgs)
{
	int iFlag;
	if (!PyTuple_GetInteger(poArgs, 0, &iFlag))
		return Py_BuildException();

	CPythonSystem::Instance().SetDamageTypeRenewal(iFlag);
	return Py_BuildNone();
}

PyObject* systemGetDamageTypeRenewal(PyObject* poSelf, PyObject* poArgs)
{
	if (CPythonSystem::Instance().GetDamageTypeRenewal() > 1)
		CPythonSystem::Instance().SetDamageTypeRenewal(0);

	return Py_BuildValue("i", CPythonSystem::Instance().GetDamageTypeRenewal());
}

#endif


#ifdef ENABLE_EVENT_MANAGER
PyObject* systemSetEventIconShow(PyObject* poSelf, PyObject* poArgs)
{
	int type;

	if (PyTuple_GetInteger(poArgs, 0, &type))
	{
		CPythonSystem::Instance().SetEventIconShow(type == 0 ? false : true);
	}

	return Py_BuildNone();
}

PyObject* systemIsEventIconShow(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("b", CPythonSystem::Instance().IsEventIconShow());
}
#endif

#ifdef ENABLE_LOADING_WINDOW_RENEWAL
PyObject* systemSetLoadingWindowType(PyObject* poSelf, PyObject* poArgs)
{
	int type;

	if (PyTuple_GetInteger(poArgs, 0, &type))
	{
		CPythonSystem::Instance().SetLoadingWindowType(type == 0 ? false : true);
	}

	return Py_BuildNone();
}

PyObject* systemIsLoadingAnimated(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("b", CPythonSystem::Instance().IsLoadingAnimated());
}
#endif

void initsystemSetting()
{
	static PyMethodDef s_methods[] =
	{
		{ "GetWidth",					systemGetWidth,					METH_VARARGS },
		{ "GetHeight",					systemGetHeight,				METH_VARARGS },

		{ "SetInterfaceHandler",		systemSetInterfaceHandler,		METH_VARARGS },
		{ "DestroyInterfaceHandler",	systemDestroyInterfaceHandler,	METH_VARARGS },

		{ "isInterfaceConfig",			systemisInterfaceConfig,		METH_VARARGS },
		{ "SaveWindowStatus",			systemSaveWindowStatus,			METH_VARARGS },
		{ "GetWindowStatus",			systemGetWindowStatus,			METH_VARARGS },

		{ "GetResolutionCount",			systemGetResolutionCount,		METH_VARARGS },
		{ "GetFrequencyCount",			systemGetFrequencyCount,		METH_VARARGS },

		{ "GetCurrentResolution",		systemGetCurrentResolution,		METH_VARARGS },

		{ "GetResolution",				systemGetResolution,			METH_VARARGS },
		{ "GetFrequency",				systemGetFrequency,				METH_VARARGS },

		{ "ApplyConfig",				systemApplyConfig,				METH_VARARGS },
		{ "SetConfig",					systemSetConfig,				METH_VARARGS },
		{ "SaveConfig",					systemSaveConfig,				METH_VARARGS },
		{ "GetConfig",					systemGetConfig,				METH_VARARGS },

		{ "SetSaveID",					systemSetSaveID,				METH_VARARGS },
		{ "isSaveID",					systemisSaveID,					METH_VARARGS },
		{ "GetSaveID",					systemGetSaveID,				METH_VARARGS },
		{ "GetMusicVolume",				systemGetMusicVolume,			METH_VARARGS },
		{ "GetSoundVolume",				systemGetSoundVolume,			METH_VARARGS },
		{ "SetMusicVolume",				systemSetMusicVolume,			METH_VARARGS },
		{ "SetSoundVolumef",				systemSetSoundVolumef,			METH_VARARGS },

		{ "IsSoftwareCursor",			systemIsSoftwareCursor,			METH_VARARGS },

		{ "SetViewChatFlag",			systemSetViewChatFlag,			METH_VARARGS },
		{ "IsViewChat",					systemIsViewChat,				METH_VARARGS },

		{ "SetAlwaysShowNameFlag",		systemSetAlwaysShowNameFlag,	METH_VARARGS },
		{ "IsAlwaysShowName",			systemIsAlwaysShowName,			METH_VARARGS },

		{ "SetShowDamageFlag",			systemSetShowDamageFlag,		METH_VARARGS },
		{ "IsShowDamage",				systemIsShowDamage,				METH_VARARGS },

		{ "SetShowSalesTextFlag",		systemSetShowSalesTextFlag,		METH_VARARGS },
		{ "IsShowSalesText",			systemIsShowSalesText,			METH_VARARGS },

		{ "GetShadowLevel",				systemGetShadowLevel,			METH_VARARGS },
		{ "SetShadowLevel",				systemSetShadowLevel,			METH_VARARGS },

#ifdef WJ_SHOW_MOB_INFO
		{ "IsShowMobAIFlag",			systemIsShowMobAIFlag,			METH_VARARGS },
		{ "SetShowMobAIFlag",			systemSetShowMobAIFlag,			METH_VARARGS },

		{ "IsShowMobLevel",				systemIsShowMobLevel,			METH_VARARGS },
		{ "SetShowMobLevel",			systemSetShowMobLevel,			METH_VARARGS },
#endif

#ifdef ENABLE_OUTLINED_NAMES
		{"SetNamesType",				systemSetNamesType,				METH_VARARGS},
		{"GetNamesType",				systemGetNamesType,				METH_VARARGS},
#endif

#ifdef ENABLE_HIDE_AFFECT_ICONS
		{"SetEffectIconShow",			systemSetEffectIconShow,		METH_VARARGS},
		{"IsAffectIconShow",			systemIsAffectIconShow,			METH_VARARGS},
#endif

#ifdef ENABLE_PERSPECTIVE_VIEW
		{"SetFieldPerspective",			systemSetFieldPerspective,		METH_VARARGS},
		{"GetFieldPerspective",			systemGetFieldPerspective,		METH_VARARGS},
#endif

#ifdef ENABLE_HIDE_HIGHLIGHT
		{"SetHighlightShow",			systemSetHighlightShow,			METH_VARARGS},
		{"IsHighlightShow",				systemIsHighlightShow,			METH_VARARGS},
#endif

#ifdef ENABLE_HIDE_MOB_SYSTEM	
		{"SetMobTypeHiddenState",		systemSetMobTypeHiddenState,	METH_VARARGS},
		{"IsMobTypeHidden",				systemIsMobTypeHidden,			METH_VARARGS},
#endif
#ifdef ENABLE_ANIMATION_SELECT
		{ "SetAnimation", 				systemSetAnimation,				METH_VARARGS },
		{ "GetCurrentAnimation",		systemGetCurrentAnimation,		METH_VARARGS },
#endif
#ifdef ENABLE_FONT_SELECT
		{ "SetFontType", 				systemSetFontType,				METH_VARARGS },
		{ "GetFontType",				systemGetFontType,				METH_VARARGS },
#endif
#ifdef ENABLE_HIDE_EFFECTS
		{ "SetEffectActive", 			systemSetEffectActive,			METH_VARARGS },
		{ "IsEffectActive",				systemIsEffectActive,			METH_VARARGS },
#endif
#ifdef ENABLE_HIDE_TOOLTIP_EMOJI
		{ "SetEmojiStatus", 			systemSetEmojiStatus,			METH_VARARGS },
		{ "GetEmojiStatus",				systemGetEmojiStatus,			METH_VARARGS },
#endif

#ifdef ENABLE_METIN_SCALE
		{"SetMetinstoneScale",			systemSetMetinstoneScale,		METH_VARARGS},
		{"GetMetinstoneScale",			systemGetMetinstoneScale,		METH_VARARGS},
#endif
#ifdef ENABLE_DAMAGE_SIZE_SCALE
		{"SetDamageTextureScale",		systemSetDamageTextureScale,	METH_VARARGS},
		{"GetDamageTextureScale",		systemGetDamageTextureScale,	METH_VARARGS},
#endif
#ifdef ENABLE_SKYBOX_SELECT
		{ "SetSkyBox", 					systemSetSkyBox,				METH_VARARGS },
		{ "GetSkyBox",					systemGetSkyBox,				METH_VARARGS },
#endif
#ifdef ENABLE_RANGE_ENTITY_OPTIMISATION
		{ "SetEntityRange", 			systemSetEntityRange,				METH_VARARGS },
		{ "GetEntityRange",				systemGetEntityRange,				METH_VARARGS },
#endif
#ifdef ENABLE_AREA_OPTIMISATION
		{ "SetLoadingDistance",			systemSetLoadingDistance,	METH_VARARGS },
		{ "GetLoadingDistance",			systemGetLoadingDistance,	METH_VARARGS },
#endif
#ifdef ENABLE_SELECT_DAMAGE_TYPE
		{ "SetDamageType", 				systemSetDamageType,				METH_VARARGS },
		{ "GetDamageType",				systemGetDamageType,				METH_VARARGS },
		{ "SetDamageTypeRenewal", 				systemSetDamageTypeRenewal,				METH_VARARGS },
		{ "GetDamageTypeRenewal",				systemGetDamageTypeRenewal,				METH_VARARGS },
#endif
#ifdef ENABLE_EVENT_MANAGER
		{ "SetEventIconShow",			systemSetEventIconShow,			METH_VARARGS },
		{ "IsEventIconShow",			systemIsEventIconShow,			METH_VARARGS },
#endif
#ifdef ENABLE_LOADING_WINDOW_RENEWAL
		{ "SetLoadingWindowType",			systemSetLoadingWindowType,			METH_VARARGS },
		{ "IsLoadingAnimated",			systemIsLoadingAnimated,			METH_VARARGS },
#endif

		{ NULL,							NULL,							NULL }
	};

	PyObject* poModule = Py_InitModule("systemSetting", s_methods);

	PyModule_AddIntConstant(poModule, "WINDOW_STATUS", CPythonSystem::WINDOW_STATUS);
	PyModule_AddIntConstant(poModule, "WINDOW_INVENTORY", CPythonSystem::WINDOW_INVENTORY);
	PyModule_AddIntConstant(poModule, "WINDOW_ABILITY", CPythonSystem::WINDOW_ABILITY);
	PyModule_AddIntConstant(poModule, "WINDOW_SOCIETY", CPythonSystem::WINDOW_SOCIETY);
	PyModule_AddIntConstant(poModule, "WINDOW_JOURNAL", CPythonSystem::WINDOW_JOURNAL);
	PyModule_AddIntConstant(poModule, "WINDOW_COMMAND", CPythonSystem::WINDOW_COMMAND);

	PyModule_AddIntConstant(poModule, "WINDOW_QUICK", CPythonSystem::WINDOW_QUICK);
	PyModule_AddIntConstant(poModule, "WINDOW_GAUGE", CPythonSystem::WINDOW_GAUGE);
	PyModule_AddIntConstant(poModule, "WINDOW_MINIMAP", CPythonSystem::WINDOW_MINIMAP);
	PyModule_AddIntConstant(poModule, "WINDOW_CHAT", CPythonSystem::WINDOW_CHAT);
}