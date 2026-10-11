#pragma once
#ifdef ENABLE_BIOLOG_SYSTEM
#include "packet.h"
class BiologSystem : public singleton<BiologSystem>
{
public:
	BiologSystem();
	virtual ~BiologSystem();
	void Initialize();
	void LoadBiologInformations(const TPacketGCBiologInformations* pBiologInformations);
	void LoadBiologState(const TPacketGCBiologUpdate* pBiologInformations);
	void SendPacket(BYTE SubHeader, TPacketCGBiologUpgrade data = SPacketCGBiologUpgrade(false,false,false));

	bool IsMaxLevel() { return m_IsMaxLevel; }
	void SetMaxLevel(bool state) { m_IsMaxLevel = state; }

	void OpenWindow();
	TPacketGCBiologInformations* GetInformations();
	TPacketGCBiologUpdate* GetState();
private:
	TPacketGCBiologInformations m_BiologInformations;
	TPacketGCBiologUpdate		m_BiologState;
	bool						m_initialize;
	bool						m_IsMaxLevel;
};
#endif
