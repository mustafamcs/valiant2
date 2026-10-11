#include "StdAfx.h"
#include "PythonNetworkStream.h"
#include "PythonApplication.h"
#include "Packet.h"

void CPythonNetworkStream::OffLinePhase()
{
	TPacketHeader header;

	if (!CheckPacket(&header))
		return;

#if defined(_DEBUG) && defined(ENABLE_PRINT_RECV_PACKET_DEBUG)
	Tracenf("RECV HEADER : %u , phase num %u ", header, m_gamePhase);
#endif

	switch (header)
	{
	case HEADER_GC_PHASE:
		if (RecvPhasePacket())
			return;
		break;
	}

	RecvErrorPacket(header);
}