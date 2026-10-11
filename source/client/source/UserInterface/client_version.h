#pragma once
#include "Packet.h"

static int g_clientVersion = 1000138964;
static int g_clientVersion2 = 1000138963;
class RandomClass : public CSingleton<RandomClass>
{
public:
	RandomClass() = default;
	~RandomClass() = default;
private:
	TRefineTable m_0;
	TPacketGCPartyInvite m_1;
	TPacketAcce m_2;
	char* m_3;
	TPacketGCPartyUpdate m_4;
};
class RandomClass2 : public CSingleton<RandomClass2>
{
public:
	RandomClass2() = default;
	~RandomClass2() = default;
private:
	TRefineTable m_0;
	int m_1;
	TPacketGCGuildInfo m_2;
	TPacketGCDuelStart m_3;
	TPacketGCGuildSubMember m_4;
	TPacketGCDigMotion m_5;
	TPacketGCFishing m_6;
};
