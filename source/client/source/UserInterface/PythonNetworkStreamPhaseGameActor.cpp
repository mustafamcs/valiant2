#include "StdAfx.h"
#include "PythonNetworkStream.h"
#include "NetworkActorManager.h"
#include "PythonBackground.h"
#include "PythonApplication.h"
#include "AbstractPlayer.h"
#include "../gamelib/ActorInstance.h"
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
#include "InstanceBase.h"
#endif

void CPythonNetworkStream::__GlobalPositionToLocalPosition(LONG& rGlobalX, LONG& rGlobalY)
{
	CPythonBackground& rkBgMgr = CPythonBackground::Instance();
	rkBgMgr.GlobalPositionToLocalPosition(rGlobalX, rGlobalY);
}

void CPythonNetworkStream::__LocalPositionToGlobalPosition(LONG& rLocalX, LONG& rLocalY)
{
	CPythonBackground& rkBgMgr = CPythonBackground::Instance();
	rkBgMgr.LocalPositionToGlobalPosition(rLocalX, rLocalY);
}

bool CPythonNetworkStream::__CanActMainInstance()
{
	CPythonCharacterManager& rkChrMgr = CPythonCharacterManager::Instance();
	CInstanceBase* pkInstMain = rkChrMgr.GetMainInstancePtr();
	if (!pkInstMain)
		return false;

	return pkInstMain->CanAct();
}

void CPythonNetworkStream::__ClearNetworkActorManager()
{
	m_rokNetActorMgr->Destroy();
}

void __SetWeaponPower(IAbstractPlayer& rkPlayer, DWORD dwWeaponID)
{
	DWORD minPower = 0;
	DWORD maxPower = 0;
	DWORD minMagicPower = 0;
	DWORD maxMagicPower = 0;
	DWORD addPower = 0;

	CItemData* pkWeapon;
	if (CItemManager::Instance().GetItemDataPointer(dwWeaponID, &pkWeapon))
	{
		if (pkWeapon->GetType() == CItemData::ITEM_TYPE_WEAPON)
		{
			minPower = pkWeapon->GetValue(3);
			maxPower = pkWeapon->GetValue(4);
			minMagicPower = pkWeapon->GetValue(1);
			maxMagicPower = pkWeapon->GetValue(2);
			addPower = pkWeapon->GetValue(5);
		}
#ifdef ENABLE_WEAPON_COSTUME_SYSTEM
		else if (pkWeapon->GetType() == CItemData::ITEM_TYPE_COSTUME && pkWeapon->GetSubType() == CItemData::COSTUME_WEAPON)
		{
			CItemData* pkRealWeapon;
			if (CItemManager::Instance().GetItemDataPointer(CPythonPlayer::Instance().GetItemIndex(TItemPos(INVENTORY, c_Equipment_Weapon)), &pkRealWeapon))
			{
				minPower = pkRealWeapon->GetValue(3);
				maxPower = pkRealWeapon->GetValue(4);
				minMagicPower = pkRealWeapon->GetValue(1);
				maxMagicPower = pkRealWeapon->GetValue(2);
				addPower = pkRealWeapon->GetValue(5);
			}
		}
#endif
	}

	rkPlayer.SetWeaponPower(minPower, maxPower, minMagicPower, maxMagicPower, addPower);
}

bool IsInvisibleRace(WORD raceNum)
{
	switch (raceNum)
	{
	case 20025:
	case 20038:
	case 20039:
		return true;
	default:
		return false;
	}
}

static SNetworkActorData s_kNetActorData;

bool CPythonNetworkStream::RecvCharacterAppendPacket()
{
	TPacketGCCharacterAdd chrAddPacket;
	if (!Recv(sizeof(chrAddPacket), &chrAddPacket))
		return false;

	__GlobalPositionToLocalPosition(chrAddPacket.x, chrAddPacket.y);

	SNetworkActorData kNetActorData;
	kNetActorData.m_bType = chrAddPacket.bType;
	kNetActorData.m_dwMovSpd = chrAddPacket.bMovingSpeed;
	kNetActorData.m_dwAtkSpd = chrAddPacket.bAttackSpeed;
	kNetActorData.m_dwRace = chrAddPacket.wRaceNum;

	kNetActorData.m_dwStateFlags = chrAddPacket.bStateFlag;
	kNetActorData.m_dwVID = chrAddPacket.dwVID;
	kNetActorData.m_fRot = chrAddPacket.angle;

	kNetActorData.m_stName = "";

	kNetActorData.m_stName = "";
	kNetActorData.m_kAffectFlags.CopyData(0, sizeof(chrAddPacket.dwAffectFlag[0]), &chrAddPacket.dwAffectFlag[0]);
	kNetActorData.m_kAffectFlags.CopyData(32, sizeof(chrAddPacket.dwAffectFlag[1]), &chrAddPacket.dwAffectFlag[1]);

	kNetActorData.SetPosition(chrAddPacket.x, chrAddPacket.y);

	kNetActorData.m_sAlignment = 0;/*chrAddPacket.sAlignment*/;
	kNetActorData.m_byPKMode = 0;/*chrAddPacket.bPKMode*/;
	kNetActorData.m_dwGuildID = 0;/*chrAddPacket.dwGuild*/;
	kNetActorData.m_dwEmpireID = 0;/*chrAddPacket.bEmpire*/;
	kNetActorData.m_dwArmor = 0;/*chrAddPacket.awPart[CHR_EQUIPPART_ARMOR]*/;
	kNetActorData.m_dwWeapon = 0;/*chrAddPacket.awPart[CHR_EQUIPPART_WEAPON]*/;
	kNetActorData.m_dwHair = 0;/*chrAddPacket.awPart[CHR_EQUIPPART_HAIR]*/;
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	kNetActorData.m_dwAcce = 0;
#endif
#ifdef ENABLE_AURA_SYSTEM
	kNetActorData.m_dwAura = 0;
#endif
#ifdef ENABLE_CROWN_SYSTEM
	kNetActorData.m_dwCrown=0;
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	kNetActorData.m_bLanguage = 0;
#endif
	kNetActorData.m_dwMountVnum = 0;/*chrAddPacket.dwMountVnum*/;
	kNetActorData.m_dwLevel = 0;

	if (kNetActorData.m_bType != CActorInstance::TYPE_PC &&
		kNetActorData.m_bType != CActorInstance::TYPE_NPC)
	{
		const char* c_szName;
		CPythonNonPlayer& rkNonPlayer = CPythonNonPlayer::Instance();
		if (rkNonPlayer.GetName(kNetActorData.m_dwRace, &c_szName))
			kNetActorData.m_stName = c_szName;
		__RecvCharacterAppendPacket(&kNetActorData);
	}
	else
	{
		s_kNetActorData = kNetActorData;
	}

	return true;
}

bool CPythonNetworkStream::RecvCharacterAdditionalInfo()
{
	TPacketGCCharacterAdditionalInfo chrInfoPacket;
	if (!Recv(sizeof(chrInfoPacket), &chrInfoPacket))
		return false;

	SNetworkActorData kNetActorData = s_kNetActorData;
	if (IsInvisibleRace(kNetActorData.m_dwRace))
		return true;

	if (kNetActorData.m_dwVID == chrInfoPacket.dwVID)
	{
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
		const char* c_szNpcClientName;
		if (kNetActorData.m_bType == CActorInstance::TYPE_NPC
			&& (!(kNetActorData.m_dwRace == 30000 || kNetActorData.m_dwRace >= 30002 && kNetActorData.m_dwRace <= 30008
#ifdef ENABLE_BUFFI_SYSTEM
				|| kNetActorData.m_dwRace == 62
#endif
			))
			&& (!((kNetActorData.m_dwRace >= 34000 && kNetActorData.m_dwRace <= 34099) || (kNetActorData.m_dwRace >= 30247 && kNetActorData.m_dwRace <= 30248) || (kNetActorData.m_dwRace >= 4026 && kNetActorData.m_dwRace <= 4027)))
			&& (!((kNetActorData.m_dwRace >= 20110 && kNetActorData.m_dwRace <= 20125) || (kNetActorData.m_dwRace >= 20127 && kNetActorData.m_dwRace <= 20248) || (kNetActorData.m_dwRace >= 20601 && kNetActorData.m_dwRace <= 20602) || (kNetActorData.m_dwRace >= 817 && kNetActorData.m_dwRace <= 821) || (kNetActorData.m_dwRace >= 35000 && kNetActorData.m_dwRace <= 35005) || (kNetActorData.m_dwRace >= 30245 && kNetActorData.m_dwRace <= 30246) || (kNetActorData.m_dwRace >= 49763 && kNetActorData.m_dwRace <= 49767) || (kNetActorData.m_dwRace >= 9293 && kNetActorData.m_dwRace <= 9293) || (kNetActorData.m_dwRace >= 9296 && kNetActorData.m_dwRace <= 9296))
			&& (!((kNetActorData.m_dwRace >= 25000 && kNetActorData.m_dwRace <= 25200)))
			&& (!((kNetActorData.m_dwRace >= 34055 && kNetActorData.m_dwRace <= 34134)))
			&& (!((kNetActorData.m_dwRace >= 20201 && kNetActorData.m_dwRace <= 20270)))))
		{
			if (CPythonNonPlayer::Instance().GetName(kNetActorData.m_dwRace, &c_szNpcClientName))
				kNetActorData.m_stName = c_szNpcClientName;
			else
				kNetActorData.m_stName = chrInfoPacket.name;
		}
		else
			kNetActorData.m_stName = chrInfoPacket.name;
#else
		kNetActorData.m_stName = chrInfoPacket.name;
#endif
		kNetActorData.m_dwGuildID = chrInfoPacket.dwGuildID;
		kNetActorData.m_dwLevel = chrInfoPacket.dwLevel;
		kNetActorData.m_sAlignment = chrInfoPacket.sAlignment;
		kNetActorData.m_byPKMode = chrInfoPacket.bPKMode;
		kNetActorData.m_dwGuildID = chrInfoPacket.dwGuildID;
		kNetActorData.m_dwEmpireID = chrInfoPacket.bEmpire;
		kNetActorData.m_dwArmor = chrInfoPacket.awPart[CHR_EQUIPPART_ARMOR];
		kNetActorData.m_dwWeapon = chrInfoPacket.awPart[CHR_EQUIPPART_WEAPON];
		kNetActorData.m_dwHair = chrInfoPacket.awPart[CHR_EQUIPPART_HAIR];
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
		kNetActorData.m_dwAcce = chrInfoPacket.awPart[CHR_EQUIPPART_ACCE];
#endif
#ifdef ENABLE_AURA_SYSTEM
		kNetActorData.m_dwAura = chrInfoPacket.awPart[CHR_EQUIPPART_AURA];
#endif
#ifdef ENABLE_CROWN_SYSTEM
		kNetActorData.m_dwCrown = chrInfoPacket.awPart[CHR_EQUIPPART_CROWN];
#endif
#ifdef ENABLE_ITEMS_SHINING
		for (int i = 0; i < CHR_SHINING_NUM; i++)
			kNetActorData.m_dwShining[i] = chrInfoPacket.adwShining[i];
#endif
		kNetActorData.m_dwMountVnum = chrInfoPacket.dwMountVnum;
#ifdef ENABLE_SKILL_COLOR_SYSTEM
		memcpy(kNetActorData.m_dwSkillColor, chrInfoPacket.dwSkillColor, sizeof(kNetActorData.m_dwSkillColor));
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
		kNetActorData.m_bLanguage = chrInfoPacket.bLanguage;
#endif
		__RecvCharacterAppendPacket(&kNetActorData);
	}
	else
	{
		TraceError("TPacketGCCharacterAdditionalInfo name=%s vid=%d race=%d Error", chrInfoPacket.name, chrInfoPacket.dwVID, kNetActorData.m_dwRace);
	}
	return true;
}

bool CPythonNetworkStream::RecvCharacterUpdatePacket()
{
	TPacketGCCharacterUpdate chrUpdatePacket;
	if (!Recv(sizeof(chrUpdatePacket), &chrUpdatePacket))
		return false;

	SNetworkUpdateActorData kNetUpdateActorData;
	kNetUpdateActorData.m_dwGuildID = chrUpdatePacket.dwGuildID;
	kNetUpdateActorData.m_dwMovSpd = chrUpdatePacket.bMovingSpeed;
	kNetUpdateActorData.m_dwAtkSpd = chrUpdatePacket.bAttackSpeed;
	kNetUpdateActorData.m_dwArmor = chrUpdatePacket.awPart[CHR_EQUIPPART_ARMOR];
	kNetUpdateActorData.m_dwWeapon = chrUpdatePacket.awPart[CHR_EQUIPPART_WEAPON];
	kNetUpdateActorData.m_dwHair = chrUpdatePacket.awPart[CHR_EQUIPPART_HAIR];
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	kNetUpdateActorData.m_dwAcce = chrUpdatePacket.awPart[CHR_EQUIPPART_ACCE];
#endif
#ifdef ENABLE_AURA_SYSTEM
	kNetUpdateActorData.m_dwAura = chrUpdatePacket.awPart[CHR_EQUIPPART_AURA];
#endif
#ifdef ENABLE_CROWN_SYSTEM
	kNetUpdateActorData.m_dwCrown = chrUpdatePacket.awPart[CHR_EQUIPPART_CROWN];
#endif
#ifdef ENABLE_ITEMS_SHINING
	for (int i = 0; i < CHR_SHINING_NUM; i++)
		kNetUpdateActorData.m_dwShining[i] = chrUpdatePacket.adwShining[i];
#endif
	kNetUpdateActorData.m_dwVID = chrUpdatePacket.dwVID;
#if defined(ENABLE_NEW_PET_SYSTEM)
	kNetUpdateActorData.m_dwLevel = chrUpdatePacket.dwLevel;
#endif
	kNetUpdateActorData.m_kAffectFlags.CopyData(0, sizeof(chrUpdatePacket.dwAffectFlag[0]), &chrUpdatePacket.dwAffectFlag[0]);
	kNetUpdateActorData.m_kAffectFlags.CopyData(32, sizeof(chrUpdatePacket.dwAffectFlag[1]), &chrUpdatePacket.dwAffectFlag[1]);
	kNetUpdateActorData.m_sAlignment = chrUpdatePacket.sAlignment;
	kNetUpdateActorData.m_byPKMode = chrUpdatePacket.bPKMode;
	kNetUpdateActorData.m_dwStateFlags = chrUpdatePacket.bStateFlag;
	kNetUpdateActorData.m_dwMountVnum = chrUpdatePacket.dwMountVnum;
#ifdef ENABLE_SKILL_COLOR_SYSTEM
	memcpy(kNetUpdateActorData.m_dwSkillColor, chrUpdatePacket.dwSkillColor, sizeof(kNetUpdateActorData.m_dwSkillColor));
#endif
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	kNetUpdateActorData.m_bLanguage = chrUpdatePacket.bLanguage;
#endif
	__RecvCharacterUpdatePacket(&kNetUpdateActorData);

	return true;
}

void CPythonNetworkStream::__RecvCharacterAppendPacket(SNetworkActorData* pkNetActorData)
{
	IAbstractPlayer& rkPlayer = IAbstractPlayer::GetSingleton();
	if (rkPlayer.IsMainCharacterIndex(pkNetActorData->m_dwVID))
	{
		rkPlayer.SetRace(pkNetActorData->m_dwRace);

		__SetWeaponPower(rkPlayer, pkNetActorData->m_dwWeapon);

		if (rkPlayer.NEW_GetMainActorPtr())
		{
			CPythonBackground::Instance().Update(pkNetActorData->m_lCurX, pkNetActorData->m_lCurY, 0.0f);
			CPythonCharacterManager::Instance().Update();

			{
				std::string strMapName = CPythonBackground::Instance().GetWarpMapName();
				if (strMapName == "metin2_map_deviltower1")
					__ShowMapName(pkNetActorData->m_lCurX, pkNetActorData->m_lCurY);
			}
		}
		else
		{
			__ShowMapName(pkNetActorData->m_lCurX, pkNetActorData->m_lCurY);
		}
	}

	m_rokNetActorMgr->AppendActor(*pkNetActorData);

	if (GetMainActorVID() == pkNetActorData->m_dwVID)
	{
		rkPlayer.SetTarget(0);
		if (m_bComboSkillFlag)
			rkPlayer.SetComboSkillFlag(m_bComboSkillFlag);

		__SetGuildID(pkNetActorData->m_dwGuildID);
		//CPythonApplication::Instance().SkipRenderBuffering(10000);
	}
}

void CPythonNetworkStream::__RecvCharacterUpdatePacket(SNetworkUpdateActorData* pkNetUpdateActorData)
{
	m_rokNetActorMgr->UpdateActor(*pkNetUpdateActorData);

	IAbstractPlayer& rkPlayer = IAbstractPlayer::GetSingleton();
	if (rkPlayer.IsMainCharacterIndex(pkNetUpdateActorData->m_dwVID))
	{
		__SetGuildID(pkNetUpdateActorData->m_dwGuildID);
		__SetWeaponPower(rkPlayer, pkNetUpdateActorData->m_dwWeapon);

		__RefreshStatus();
		__RefreshAlignmentWindow();
		__RefreshEquipmentWindow();
		__RefreshInventoryWindow();
	}
	else
	{
		rkPlayer.NotifyCharacterUpdate(pkNetUpdateActorData->m_dwVID);
	}
}

bool CPythonNetworkStream::RecvCharacterDeletePacket()
{
	TPacketGCCharacterDelete chrDelPacket;

	if (!Recv(sizeof(chrDelPacket), &chrDelPacket))
	{
		TraceError("CPythonNetworkStream::RecvCharacterDeletePacket - Recv Error");
		return false;
	}

	m_rokNetActorMgr->RemoveActor(chrDelPacket.dwVID);

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME],
		"BINARY_PrivateShop_Disappear",
		Py_BuildValue("(i)", chrDelPacket.dwVID)
	);

	return true;
}

bool CPythonNetworkStream::RecvCharacterMovePacket()
{
	TPacketGCMove kMovePacket;
	if (!Recv(sizeof(TPacketGCMove), &kMovePacket))
	{
		Tracen("CPythonNetworkStream::RecvCharacterMovePacket - PACKET READ ERROR");
		return false;
	}

	__GlobalPositionToLocalPosition(kMovePacket.lX, kMovePacket.lY);

	SNetworkMoveActorData kNetMoveActorData;
	kNetMoveActorData.m_dwArg = kMovePacket.bArg;
	kNetMoveActorData.m_dwFunc = kMovePacket.bFunc;
	kNetMoveActorData.m_dwTime = kMovePacket.dwTime;
	kNetMoveActorData.m_dwVID = kMovePacket.dwVID;
	kNetMoveActorData.m_fRot = kMovePacket.bRot * 5.0f;
	kNetMoveActorData.m_lPosX = kMovePacket.lX;
	kNetMoveActorData.m_lPosY = kMovePacket.lY;
	kNetMoveActorData.m_dwDuration = kMovePacket.dwDuration;

	m_rokNetActorMgr->MoveActor(kNetMoveActorData);

	return true;
}

bool CPythonNetworkStream::RecvOwnerShipPacket()
{
	TPacketGCOwnership kPacketOwnership;

	if (!Recv(sizeof(kPacketOwnership), &kPacketOwnership))
		return false;

	m_rokNetActorMgr->SetActorOwner(kPacketOwnership.dwOwnerVID, kPacketOwnership.dwVictimVID);

	return true;
}

bool CPythonNetworkStream::RecvSyncPositionPacket()
{
	TPacketGCSyncPosition kPacketSyncPos;
	if (!Recv(sizeof(kPacketSyncPos), &kPacketSyncPos))
		return false;

	TPacketGCSyncPositionElement kSyncPos;

	UINT uSyncPosCount = (kPacketSyncPos.wSize - sizeof(kPacketSyncPos)) / sizeof(kSyncPos);
	for (UINT iSyncPos = 0; iSyncPos < uSyncPosCount; ++iSyncPos)
	{
		if (!Recv(sizeof(TPacketGCSyncPositionElement), &kSyncPos))
			return false;

#ifdef __MOVIE_MODE__
		return true;
#endif __MOVIE_MODE__

		//Tracenf("CPythonNetworkStream::RecvSyncPositionPacket %d (%d, %d)", kSyncPos.dwVID, kSyncPos.lX, kSyncPos.lY);

		__GlobalPositionToLocalPosition(kSyncPos.lX, kSyncPos.lY);
		m_rokNetActorMgr->SyncActor(kSyncPos.dwVID, kSyncPos.lX, kSyncPos.lY);

		/*
		CPythonCharacterManager & rkChrMgr = CPythonCharacterManager::Instance();
		CInstanceBase * pkChrInst = rkChrMgr.GetInstancePtr(kSyncPos.dwVID);

		if (pkChrInst)
		{
			pkChrInst->NEW_SyncPixelPosition(kSyncPos.lX, kSyncPos.lY);
		}
		*/
	}
	return true;
}
