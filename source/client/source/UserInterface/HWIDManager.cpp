#include "StdAfx.h"
#include "HWIDManager.h"
#include <functional>
#include <algorithm>
#include <sstream>
#include <intrin.h>

HWIDMANAGER::HWIDMANAGER()
{
	m_MachineGUID	= "";
	m_MacAddr		= "";
	m_HDDSerial		= "";
	m_HDDModel		= "";
	m_CpuId			= "";

	CMachineGuid	c_MachineGuid;
	CMacAddr		c_MacAddr;
	CHddData		c_HddData;
	CCpuId			c_CpuId;

	m_MachineGUID	= c_MachineGuid.getMachineGUID();
	m_MacAddr		= c_MacAddr.getMacAddr();
	m_HDDSerial		= c_HddData.getHDDSerialNumber();
	m_HDDModel		= c_HddData.getHDDModelNumber();
	m_CpuId			= c_CpuId.getCpuID();
}

/**************************MACHINE GUID************************************/
CMachineGuid::~CMachineGuid() = default;

CMachineGuid::CMachineGuid()
{
	HKEY hKey;
	LSTATUS res = RegOpenKeyExW(HKEY_LOCAL_MACHINE, L"SOFTWARE\\Microsoft\\Cryptography", 0, KEY_READ | KEY_WOW64_64KEY, &hKey);

	if (res == ERROR_SUCCESS)
	{
		std::wstring temp;
		res = GetStringRegKey(hKey, L"MachineGuid", temp, L"");
		if (res == ERROR_SUCCESS)
		{
			m_MachineGUID.assign(temp.begin(), temp.end());
		}
	}
	RegCloseKey(hKey);
}

LONG CMachineGuid::GetStringRegKey(HKEY hKey, const std::wstring& strValueName, std::wstring& strValue, const std::wstring& strDefaultValue)
{
	strValue = strDefaultValue;
	WCHAR szBuffer[512];
	DWORD dwBufferSize = sizeof(szBuffer);
	ULONG nError;
	nError = RegQueryValueExW(hKey, strValueName.c_str(), 0, NULL, (LPBYTE)szBuffer, &dwBufferSize);

	if (ERROR_SUCCESS == nError)
	{
		strValue = szBuffer;
	}

	return nError;
}


/**************************MAC ADDR************************************/

CMacAddr::CMacAddr()
{
	findValidMac();
}

CMacAddr::~CMacAddr()
{
	if (m_pAdapters)
	{
		delete[] m_pAdapters;
		m_pAdapters = NULL;
	}
}

bool CMacAddr::IsPrimaryAdapter(DWORD dwIndex)
{
	bool bIsPrimaryAdapter = false;
	if (m_pAdapters)
	{
		CNetworkAdapter* pAdapt = NULL;
		DWORD dwMinIndex = m_pAdapters->GetAdapterIndex();
		for (unsigned int i = 0; i < m_nCount; i++)
		{
			pAdapt = &m_pAdapters[i];
			if (pAdapt->GetAdapterIndex() < dwMinIndex)
			{
				dwMinIndex = pAdapt->GetAdapterIndex();
			}
		}
		if (dwIndex == dwMinIndex)
		{
			bIsPrimaryAdapter = true;
		}
	}
	return bIsPrimaryAdapter;
}

bool CMacAddr::initAdapters()
{
	bool bRet = true;
	DWORD dwErr = 0;
	ULONG ulNeeded = 0;
	dwErr = EnumNetworkAdapters(m_pAdapters, 0, &ulNeeded);
	if (dwErr == ERROR_INSUFFICIENT_BUFFER)
	{
		m_nCount = ulNeeded / sizeof(CNetworkAdapter);
		m_pAdapters = new CNetworkAdapter[ulNeeded / sizeof(CNetworkAdapter)];
		dwErr = EnumNetworkAdapters(m_pAdapters, ulNeeded, &ulNeeded);
		if (!m_pAdapters)
		{
			bRet = false;
		}
	}
	else
	{
		bRet = false;
	}
	return bRet;
}

bool CMacAddr::findValidMac()
{
	initAdapters();
	DWORD dwIndex;
	CNetworkAdapter* pAdapt = NULL;
	if (m_pAdapters)
	{
		for (UINT i = 0; i < m_nCount; i++)
		{
			pAdapt = &m_pAdapters[i];
			dwIndex = pAdapt->GetAdapterIndex();
			if (IsPrimaryAdapter(dwIndex))
			{
				setMACData(pAdapt->GetAdapterAddress());
				return true;
			}
		}
	}
	return false;
}

void CMacAddr::setMACData(std::string input)
{
	m_macAddr = input;
}

/**************************CPU ID************************************/

CCpuId::CCpuId()
{
	int registers[4];
	char cpuIDHex[17] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

	char* part1 = &cpuIDHex[0];
	char* part2 = &cpuIDHex[8];

	__cpuid(registers, 1);

	sprintf_s(part1, 9, "%08X", registers[3]);
	sprintf_s(part2, 9, "%08X", registers[0]);

	m_CpuID = std::string(cpuIDHex);
}

CCpuId::~CCpuId() {}



/**************************HDD DATA************************************/
CHddData::CHddData()
{
	bool done = false;

	done = ReadPhysicalDriveInNTWithAdminRights();

	if (!done)
		done = ReadIdeDriveAsScsiDriveInNT();

	if (!done)
		done = ReadPhysicalDriveInNTWithZeroRights();

	if (!done)
		done = ReadPhysicalDriveInNTUsingSmart();
}

CHddData::~CHddData() = default;

bool CHddData::ReadPhysicalDriveInNTWithAdminRights()
{
	bool done = false;
	int drive = 0;

	HANDLE hPhysicalDriveIOCTL = 0;
	char driveName[256];

	sprintf_s(driveName, sizeof(driveName), "\\\\.\\PhysicalDrive%d", drive);

	hPhysicalDriveIOCTL = CreateFile(driveName, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);

	if (hPhysicalDriveIOCTL == INVALID_HANDLE_VALUE)
		return done;

	GETVERSIONOUTPARAMS VersionParams;
	DWORD cbBytesReturned = 0;

	memset((void*)&VersionParams, 0, sizeof(VersionParams));

	if (!DeviceIoControl(hPhysicalDriveIOCTL, DFP_GET_VERSION, NULL, 0, &VersionParams, sizeof(VersionParams), &cbBytesReturned, NULL))
		return done;

	if (VersionParams.bIDEDeviceMap <= 0)
		return done;

	BYTE bIDCmd = 0;
	SENDCMDINPARAMS  scip;

	bIDCmd = (VersionParams.bIDEDeviceMap >> drive & 0x10) ? \
		IDE_ATAPI_IDENTIFY : IDE_ATA_IDENTIFY;

	memset(&scip, 0, sizeof(scip));
	memset(IdOutCmd, 0, sizeof(IdOutCmd));

	if (!DoIDENTIFY(hPhysicalDriveIOCTL, &scip, (PSENDCMDOUTPARAMS)&IdOutCmd, (BYTE)bIDCmd, (BYTE)drive, &cbBytesReturned))
	{
		return done;
	}

	DWORD diskdata[256];
	int ijk = 0;
	USHORT* pIdSector = (USHORT*)((PSENDCMDOUTPARAMS)IdOutCmd)->bBuffer;

	for (ijk = 0; ijk < 256; ijk++)
	{
		diskdata[ijk] = pIdSector[ijk];
	}

	SetDiskData(drive, diskdata);

	done = true;

	CloseHandle(hPhysicalDriveIOCTL);

	return done;
}

bool CHddData::ReadPhysicalDriveInNTUsingSmart()
{
	bool done = false;
	int drive = 0;

	HANDLE hPhysicalDriveIOCTL = 0;
	char driveName[256];

	sprintf_s(driveName, sizeof(driveName), "\\\\.\\PhysicalDrive%d", drive);

	hPhysicalDriveIOCTL = CreateFile(driveName, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_DELETE | FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);

	if (hPhysicalDriveIOCTL == INVALID_HANDLE_VALUE)
		return done;

	GETVERSIONINPARAMS GetVersionParams;
	DWORD cbBytesReturned = 0;

	memset((void*)&GetVersionParams, 0, sizeof(GetVersionParams));

	if (!DeviceIoControl(hPhysicalDriveIOCTL, SMART_GET_VERSION, NULL, 0, &GetVersionParams, sizeof(GETVERSIONINPARAMS), &cbBytesReturned, NULL))
		return done;

	ULONG CommandSize = sizeof(SENDCMDINPARAMS) + IDENTIFY_BUFFER_SIZE;
	PSENDCMDINPARAMS Command = (PSENDCMDINPARAMS)malloc(CommandSize);
	Command->irDriveRegs.bCommandReg = ID_CMD;
	DWORD BytesReturned = 0;

	if (!DeviceIoControl(hPhysicalDriveIOCTL, SMART_RCV_DRIVE_DATA, Command, sizeof(SENDCMDINPARAMS), Command, CommandSize, &BytesReturned, NULL))
		return done;

	DWORD diskdata[256];
	USHORT* pIdSector = (USHORT*)(PIDENTIFY_DATA)((PSENDCMDOUTPARAMS)Command)->bBuffer;

	for (int ijk = 0; ijk < 256; ijk++)
		diskdata[ijk] = pIdSector[ijk];

	SetDiskData(drive, diskdata);
	done = true;

	CloseHandle(hPhysicalDriveIOCTL);
	free(Command);

	return done;
}

bool CHddData::ReadPhysicalDriveInNTWithZeroRights()
{
	bool done = false;
	int drive = 0;

	HANDLE hPhysicalDriveIOCTL = 0;

	char driveName[256];

	sprintf_s(driveName, sizeof(driveName), "\\\\.\\PhysicalDrive%d", drive);

	hPhysicalDriveIOCTL = CreateFile(driveName, 0, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);

	if (hPhysicalDriveIOCTL == INVALID_HANDLE_VALUE)
		return done;

	char local_buffer[10000];
	STORAGE_PROPERTY_QUERY query;
	DWORD cbBytesReturned = 0;

	memset((void*)&query, 0, sizeof(query));
	query.PropertyId = StorageDeviceProperty;
	query.QueryType = PropertyStandardQuery;

	memset(local_buffer, 0, sizeof(local_buffer));

	if (!DeviceIoControl(hPhysicalDriveIOCTL, IOCTL_STORAGE_QUERY_PROPERTY, &query, sizeof(query), &local_buffer[0], sizeof(local_buffer), &cbBytesReturned, NULL))
		return done;

	STORAGE_DEVICE_DESCRIPTOR* descrip = (STORAGE_DEVICE_DESCRIPTOR*)&local_buffer;
	char serialNumber[1000];
	char modelNumber[1000];

	int swapNeeded = 0;

	unsigned int i = 1;
	char* c = (char*)&i;

	if (*c)
		swapNeeded = 0;
	else
		swapNeeded = 1;

	flipAndCodeBytes(local_buffer, descrip->SerialNumberOffset, swapNeeded, serialNumber);
	flipAndCodeBytes(local_buffer, descrip->ProductIdOffset, swapNeeded, modelNumber);

	if (0 == m_HDDSerialNumber[0] && (isalnum(serialNumber[0]) || isalnum(serialNumber[19])))
	{
		std::string s_SerialNumber(serialNumber);
		std::string s_ModelNumber(modelNumber);
		SetDiskData(s_ModelNumber, s_SerialNumber);
		done = true;
	}

	CloseHandle(hPhysicalDriveIOCTL);

	return done;
}

bool CHddData::DoIDENTIFY(HANDLE hPhysicalDriveIOCTL, PSENDCMDINPARAMS pSCIP, PSENDCMDOUTPARAMS pSCOP, BYTE bIDCmd, BYTE bDriveNum, PDWORD lpcbBytesReturned)
{
	pSCIP->cBufferSize = IDENTIFY_BUFFER_SIZE;
	pSCIP->irDriveRegs.bFeaturesReg = 0;
	pSCIP->irDriveRegs.bSectorCountReg = 1;
	pSCIP->irDriveRegs.bCylLowReg = 0;
	pSCIP->irDriveRegs.bCylHighReg = 0;
	pSCIP->irDriveRegs.bDriveHeadReg = 0xA0 | ((bDriveNum & 1) << 4);
	pSCIP->irDriveRegs.bCommandReg = bIDCmd;
	pSCIP->bDriveNumber = bDriveNum;
	pSCIP->cBufferSize = IDENTIFY_BUFFER_SIZE;
	return (DeviceIoControl(hPhysicalDriveIOCTL, DFP_RECEIVE_DRIVE_DATA, (LPVOID)pSCIP, sizeof(SENDCMDINPARAMS) - 1, (LPVOID)pSCOP, sizeof(SENDCMDOUTPARAMS) + IDENTIFY_BUFFER_SIZE - 1, lpcbBytesReturned, NULL) != 0);
}

bool CHddData::ReadIdeDriveAsScsiDriveInNT()
{
	bool done = false;
	int controller = 0;

	for (controller = 0; controller < 16; controller++)
	{
		HANDLE hScsiDriveIOCTL = 0;
		char   driveName[256];

		sprintf_s(driveName, sizeof(driveName), "\\\\.\\Scsi%d:", controller);

		hScsiDriveIOCTL = CreateFile(driveName, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);

		if (hScsiDriveIOCTL == INVALID_HANDLE_VALUE)
			continue;

		int drive = 0;

		char buffer[sizeof(SRB_IO_CONTROL) + SENDIDLENGTH];
		SRB_IO_CONTROL* p = (SRB_IO_CONTROL*)buffer;
		SENDCMDINPARAMS* pin = (SENDCMDINPARAMS*)(buffer + sizeof(SRB_IO_CONTROL));
		DWORD dummy;

		memset(buffer, 0, sizeof(buffer));
		p->HeaderLength = sizeof(SRB_IO_CONTROL);
		p->Timeout = 10000;
		p->Length = SENDIDLENGTH;
		p->ControlCode = IOCTL_SCSI_MINIPORT_IDENTIFY;
		strncpy_s((char*)p->Signature, 8 + 1, "SCSIDISK", 8 + 1);

		pin->irDriveRegs.bCommandReg = IDE_ATA_IDENTIFY;
		pin->bDriveNumber = drive;

		if (!DeviceIoControl(hScsiDriveIOCTL, IOCTL_SCSI_MINIPORT, buffer, sizeof(SRB_IO_CONTROL) + sizeof(SENDCMDINPARAMS) - 1, buffer, sizeof(SRB_IO_CONTROL) + SENDIDLENGTH, &dummy, NULL))
			continue;

		SENDCMDOUTPARAMS* pOut = (SENDCMDOUTPARAMS*)(buffer + sizeof(SRB_IO_CONTROL));
		IDSECTOR* pId = (IDSECTOR*)(pOut->bBuffer);

		if (!pId->sModelNumber[0])
			continue;

		DWORD diskdata[256];
		int ijk = 0;
		USHORT* pIdSector = (USHORT*)pId;

		for (ijk = 0; ijk < 256; ijk++)
			diskdata[ijk] = pIdSector[ijk];

		SetDiskData(controller * 2 + drive, diskdata);

		done = true;

		CloseHandle(hScsiDriveIOCTL);
		break;
	}
	return done;
}

void CHddData::SetDiskData(int drive, DWORD diskdata[256])
{
	std::string serialNumber;
	std::string modelNumber;
	ConvertToString(diskdata, 10, 19, serialNumber);
	ConvertToString(diskdata, 27, 46, modelNumber);
	SetDiskData(modelNumber, serialNumber);
}

void CHddData::SetDiskData(std::string model, std::string serial)
{
	if (m_HDDSerialNumber.empty() && (isalnum(serial[0]) || isalnum(serial[19])) && !serial[0] == 0)
	{
		CleanWhitespaces(model);
		CleanWhitespaces(serial);
		m_HDDModelNumber = model;
		m_HDDSerialNumber = serial;
	}
}

void CHddData::ConvertToString(DWORD diskdata[256], int firstIndex, int lastIndex, std::string& buf)
{
	std::stringstream ss;
	for (int index = firstIndex; index <= lastIndex; index++)
	{
		ss.put((char)(diskdata[index] / 256));
		ss.put((char)(diskdata[index] % 256));
	}
	buf = ss.str();
	CleanWhitespaces(buf);
}

void CHddData::CleanWhitespaces(std::string& buf)
{
	buf.erase(std::remove(buf.begin(), buf.end(), ' '), buf.end());
}

char* CHddData::flipAndCodeBytes(const char* str, int pos, int flip, char* buf)
{
	int i;
	int j = 0;
	int k = 0;

	buf[0] = '\0';

	if (pos <= 0)
		return buf;

	if (!j)
	{
		char p = 0;
		j = 1;
		k = 0;
		buf[k] = 0;
		for (i = pos; j && str[i] != '\0'; ++i)
		{
			char c = tolower(str[i]);

			if (isspace(c))
				c = '0';

			++p;
			buf[k] <<= 4;

			if (c >= '0' && c <= '9')
				buf[k] |= (unsigned char)(c - '0');
			else if (c >= 'a' && c <= 'f')
				buf[k] |= (unsigned char)(c - 'a' + 10);
			else
			{
				j = 0;
				break;
			}

			if (p == 2)
			{
				if (buf[k] != '\0' && !isprint(buf[k]))
				{
					j = 0;
					break;
				}
				++k;
				p = 0;
				buf[k] = 0;
			}
		}
	}

	if (!j)
	{
		j = 1;
		k = 0;
		for (i = pos; j && str[i] != '\0'; ++i)
		{
			char c = str[i];

			if (!isprint(c))
			{
				j = 0;
				break;
			}

			buf[k++] = c;
		}
	}

	if (!j)
	{
		k = 0;
	}

	buf[k] = '\0';

	if (flip)
	{
		for (j = 0; j < k; j += 2)
		{
			char t = buf[j];
			buf[j] = buf[j + 1];
			buf[j + 1] = t;
		}
	}

	i = j = -1;
	for (k = 0; buf[k] != '\0'; ++k)
	{
		if (!isspace(buf[k]))
		{
			if (i < 0)
				i = k;
			j = k;
		}
	}

	if ((i >= 0) && (j >= 0))
	{
		for (k = i; (k <= j) && (buf[k] != '\0'); ++k)
			buf[k - i] = buf[k];
		buf[k - i] = '\0';
	}

	return buf;
}


/**************************NETWORK ADAPTER************************************/
#define ALLOCATE_FROM_PROCESS_HEAP( bytes )		::HeapAlloc( ::GetProcessHeap(), HEAP_ZERO_MEMORY, bytes )
#define DEALLOCATE_FROM_PROCESS_HEAP( ptr )		if( ptr ) ::HeapFree( ::GetProcessHeap(), 0, ptr )
#define REALLOC_FROM_PROCESS_HEAP( ptr, bytes )	::HeapReAlloc( ::GetProcessHeap(), HEAP_ZERO_MEMORY, ptr, bytes )

DWORD EnumNetworkAdapters(CNetworkAdapter* pAdapters, ULONG ulSzBuf, LPDWORD lpdwOutSzBuf)
{
	IP_ADAPTER_INFO* pAdptInfo = NULL;
	IP_ADAPTER_INFO* pNextAd = NULL;
	ULONG ulLen = 0;
	int nCnt = 0;
	DWORD erradapt;

	erradapt = ::GetAdaptersInfo(pAdptInfo, &ulLen);

	if (erradapt == ERROR_BUFFER_OVERFLOW)
	{
		pAdptInfo = (IP_ADAPTER_INFO*)ALLOCATE_FROM_PROCESS_HEAP(ulLen);
		erradapt = ::GetAdaptersInfo(pAdptInfo, &ulLen);
	}

	pNextAd = pAdptInfo;
	while (pNextAd)
	{
		nCnt++;
		pNextAd = pNextAd->Next;
	}

	*lpdwOutSzBuf = nCnt * sizeof(CNetworkAdapter);
	if (ulSzBuf < *lpdwOutSzBuf)
	{
		DEALLOCATE_FROM_PROCESS_HEAP(pAdptInfo);
		return ERROR_INSUFFICIENT_BUFFER;
	}

	nCnt = 0;

	if (erradapt == ERROR_SUCCESS)
	{
		pNextAd = pAdptInfo;
		while (pNextAd)
		{
			pAdapters[nCnt].SetupAdapterInfo(pNextAd);
			pNextAd = pNextAd->Next;
			nCnt++;
		}
	}

	DEALLOCATE_FROM_PROCESS_HEAP(pAdptInfo);

	return ERROR_SUCCESS;
}

CNetworkAdapter::CNetworkAdapter() : m_tLeaseObtained(0), m_tLeaseExpires(0)
{
	m_bDhcpUsed = FALSE;
	m_bWinsUsed = FALSE;
	m_dwIndex = 0;
	m_nAdapterType = 0;

	::memset(&m_ucAddress.ucAddress, 0, MAX_ADAPTER_ADDRESS_LENGTH);
	m_ucAddress.nLen = 0;

	m_DnsAddresses.clear();
	m_IpAddresses.clear();
	m_GatewayList.clear();

	return;
}

CNetworkAdapter::~CNetworkAdapter()
{
#ifdef _DEBUG
	::memset(&m_ucAddress.ucAddress, 0, MAX_ADAPTER_ADDRESS_LENGTH);
	m_ucAddress.nLen = 0;
	m_bDhcpUsed = FALSE;
	m_bWinsUsed = FALSE;
	m_dwIndex = 0;
	m_nAdapterType = 0;
#endif
	m_DnsAddresses.clear();
	m_IpAddresses.clear();
	m_GatewayList.clear();
	return;
}

BOOL CNetworkAdapter::SetupAdapterInfo(IP_ADAPTER_INFO* pAdaptInfo)
{
	BOOL bSetupPassed = FALSE;
	IP_ADDR_STRING* pNext = NULL;
	IP_PER_ADAPTER_INFO* pPerAdapt = NULL;
	ULONG ulLen = 0;
	DWORD err;

	_IPINFO iphold;

	if (pAdaptInfo)
	{
#ifndef _UNICODE
		m_sName = pAdaptInfo->AdapterName;
		m_sDesc = pAdaptInfo->Description;
#else
		USES_CONVERSION;
		m_sName = A2W(pAdaptInfo->AdapterName);
		m_sDesc = A2W(pAdaptInfo->Description);
#endif

		m_sPriWins = pAdaptInfo->PrimaryWinsServer.IpAddress.String;
		m_sSecWins = pAdaptInfo->SecondaryWinsServer.IpAddress.String;
		m_dwIndex = pAdaptInfo->Index;
		m_nAdapterType = pAdaptInfo->Type;
		m_bDhcpUsed = pAdaptInfo->DhcpEnabled;
		m_bWinsUsed = pAdaptInfo->HaveWins;
		m_tLeaseObtained = pAdaptInfo->LeaseObtained;
		m_tLeaseExpires = pAdaptInfo->LeaseExpires;
		m_sDhcpAddr = pAdaptInfo->DhcpServer.IpAddress.String;

		m_ucAddress.nLen = pAdaptInfo->AddressLength;
		for (int i = 0; i < (int)m_ucAddress.nLen; i++)
		{
			m_ucAddress.ucAddress[i] = pAdaptInfo->Address[i];
		}

		if (pAdaptInfo->CurrentIpAddress)
		{
			m_sCurIpAddr.sIp = pAdaptInfo->CurrentIpAddress->IpAddress.String;
			m_sCurIpAddr.sSubnet = pAdaptInfo->CurrentIpAddress->IpMask.String;
		}
		else
		{
			m_sCurIpAddr.sIp = _T("0.0.0.0");
			m_sCurIpAddr.sSubnet = _T("0.0.0.0");
		}

		pNext = &(pAdaptInfo->IpAddressList);

		while (pNext)
		{
			iphold.sIp = pNext->IpAddress.String;
			iphold.sSubnet = pNext->IpMask.String;
			m_IpAddresses.push_back(iphold);
			pNext = pNext->Next;
		}

		pNext = &(pAdaptInfo->GatewayList);
		while (pNext)
		{
			m_GatewayList.push_back(pNext->IpAddress.String);
			pNext = pNext->Next;
		}

		err = ::GetPerAdapterInfo(m_dwIndex, pPerAdapt, &ulLen);

		if (err == ERROR_BUFFER_OVERFLOW)
		{
			pPerAdapt = (IP_PER_ADAPTER_INFO*)ALLOCATE_FROM_PROCESS_HEAP(ulLen);
			err = ::GetPerAdapterInfo(m_dwIndex, pPerAdapt, &ulLen);
			if (err == ERROR_SUCCESS)
			{
				pNext = &(pPerAdapt->DnsServerList);
				while (pNext)
				{
					m_DnsAddresses.push_back(pNext->IpAddress.String);
					pNext = pNext->Next;
				}
				bSetupPassed = TRUE;
			}
			DEALLOCATE_FROM_PROCESS_HEAP(pPerAdapt);
		}
	}
	return bSetupPassed;
}

tstring	CNetworkAdapter::GetStringFromArray(const StringArray* pPtr, int nIndex) const
{
	tstring sStr = _T("");
	if (pPtr && ((SIZE_T)nIndex < pPtr->size()))
	{
		sStr = (*pPtr)[nIndex];
	}
	return sStr;
}

tstring CNetworkAdapter::GetAdapterTypeString(UINT nType)
{
	tstring sType = _T("");
	switch (nType)
	{
	case MIB_IF_TYPE_OTHER:		sType = _T("Other");		break;
	case MIB_IF_TYPE_ETHERNET:	sType = _T("Ethernet");		break;
	case MIB_IF_TYPE_TOKENRING:	sType = _T("Token Ring");	break;
	case MIB_IF_TYPE_FDDI:		sType = _T("FDDI");			break;
	case MIB_IF_TYPE_PPP:		sType = _T("PPP");			break;
	case MIB_IF_TYPE_LOOPBACK:	sType = _T("Loopback");		break;
	case MIB_IF_TYPE_SLIP:		sType = _T("SLIP");			break;
	default: sType = _T("Invalid Adapter Type");			break;
	};
	return sType;
}

tstring CNetworkAdapter::GetAdapterName()				const { return m_sName; }
tstring CNetworkAdapter::GetAdapterDescription()		const { return m_sDesc; }
time_t CNetworkAdapter::GetLeaseObtained()				const { return m_tLeaseObtained; }
time_t CNetworkAdapter::GetLeaseExpired()				const { return m_tLeaseExpires; }
SIZE_T	CNetworkAdapter::GetNumIpAddrs()				const { return m_IpAddresses.size(); }
SIZE_T	CNetworkAdapter::GetNumDnsAddrs()				const { return m_DnsAddresses.size(); }
tstring	CNetworkAdapter::GetDnsAddr(int nDns)			const { return GetStringFromArray(&m_DnsAddresses, nDns); }
tstring CNetworkAdapter::GetCurrentIpAddress()			const { return m_sCurIpAddr.sIp; }
BOOL CNetworkAdapter::IsDhcpUsed()						const { return m_bDhcpUsed; }
tstring	CNetworkAdapter::GetDchpAddr()					const { return m_sDhcpAddr; }
BOOL CNetworkAdapter::IsWinsUsed()						const { return m_bWinsUsed; }
tstring CNetworkAdapter::GetPrimaryWinsServer()			const { return m_sPriWins; }
tstring CNetworkAdapter::GetSecondaryWinsServer()		const { return m_sSecWins; }
tstring	CNetworkAdapter::GetGatewayAddr(int nGateway)	const { return GetStringFromArray(&m_GatewayList, nGateway); }
SIZE_T	CNetworkAdapter::GetNumGatewayAddrs()			const { return m_GatewayList.size(); }
DWORD CNetworkAdapter::GetAdapterIndex()				const { return m_dwIndex; }
UINT CNetworkAdapter::GetAdapterType()					const { return m_nAdapterType; }

tstring	CNetworkAdapter::GetIpAddr(int nIp) const
{
	tstring sAddr = _T("");
	if ((SIZE_T)nIp < m_IpAddresses.size())
	{
		sAddr = m_IpAddresses[nIp].sIp;
	}
	return sAddr;
}

tstring CNetworkAdapter::GetSubnetForIpAddr(int nIp) const
{
	tstring sAddr = _T("");
	if ((SIZE_T)nIp < m_IpAddresses.size())
	{
		sAddr = m_IpAddresses[nIp].sSubnet;
	}
	return sAddr;
}

tstring CNetworkAdapter::GetAdapterAddress(void)
{
	tstring sTemp = "";
	char macTemp[8];
	for (unsigned int i = 0; i < m_ucAddress.nLen; i++)
	{
		if (i > 0)
		{
			sTemp += "::";
		}
		sprintf_s(macTemp, sizeof(macTemp), "%02X", m_ucAddress.ucAddress[i]);
		sTemp += macTemp;
	}
	return sTemp;
}