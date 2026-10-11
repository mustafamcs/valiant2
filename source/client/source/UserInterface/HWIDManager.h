#pragma once
#include <string>
#include "../eterBase/Singleton.h"
#include <windows.h>
#include <winioctl.h>
#include <vector>
#include <tchar.h>
#include <iphlpapi.h>
#include <ipifcons.h>

class HWIDMANAGER : public CSingleton <HWIDMANAGER>
{
	public:
		HWIDMANAGER();
		std::string getMachineGUID(){ return m_MachineGUID; };
		std::string getMacAddr(){ return m_MacAddr; };
		std::string getHDDSerial(){ return m_HDDSerial; };
		std::string getHDDModel(){ return m_HDDModel; };
		std::string getCPUid(){ return m_CpuId; };

	private:
		std::string m_MachineGUID;
		std::string m_MacAddr;
		std::string m_HDDSerial;
		std::string m_HDDModel;
		std::string m_CpuId;
};

class CMachineGuid
{
	public:
		CMachineGuid();
		~CMachineGuid();
		std::string getMachineGUID() { return m_MachineGUID; };

	private:
		LONG GetStringRegKey(HKEY hKey, const std::wstring& strValueName, std::wstring& strValue, const std::wstring& strDefaultValue);

	private:
		std::string m_MachineGUID;
};

class CCpuId
{
	public:
		CCpuId();
		~CCpuId();

		std::string getCpuID()
		{
			return m_CpuID;
		};

	private:
		std::string m_CpuID;
};


class CHddData
{
private:
	static int const IDE_ATA_IDENTIFY = 0xEC;
	static int const IDE_ATAPI_IDENTIFY = 0xA1;
	static int const DFP_GET_VERSION = 0x00074080;
	static int const DFP_RECEIVE_DRIVE_DATA = 0x0007c088;
	static int const IOCTL_SCSI_MINIPORT_IDENTIFY = ((0x0000001b << 16) + 0x0501);
	static int const IOCTL_SCSI_MINIPORT = 0x0004D008;
	static int const SENDIDLENGTH = sizeof(SENDCMDOUTPARAMS) + IDENTIFY_BUFFER_SIZE;

public:
	CHddData();
	~CHddData();

	std::string getHDDSerialNumber() { return m_HDDSerialNumber; };
	std::string getHDDModelNumber() { return m_HDDModelNumber; };

private:
	bool ReadPhysicalDriveInNTWithZeroRights();
	bool ReadPhysicalDriveInNTUsingSmart();
	bool ReadPhysicalDriveInNTWithAdminRights();
	bool ReadIdeDriveAsScsiDriveInNT();

	void SetDiskData(int drive, DWORD diskdata[256]);
	void SetDiskData(std::string model, std::string serial);

	char* flipAndCodeBytes(const char* str, int pos, int flip, char* buf);
	void ConvertToString(DWORD diskdata[256], int firstIndex, int lastIndex, std::string& buf);
	void CleanWhitespaces(std::string& buf);

	bool DoIDENTIFY(HANDLE hPhysicalDriveIOCTL, PSENDCMDINPARAMS pSCIP, PSENDCMDOUTPARAMS pSCOP, BYTE bIDCmd, BYTE bDriveNum, PDWORD lpcbBytesReturned);

private:
	BYTE IdOutCmd[sizeof(SENDCMDOUTPARAMS) + IDENTIFY_BUFFER_SIZE - 1];
	std::string m_HDDModelNumber;
	std::string m_HDDSerialNumber;

#pragma pack(1)
	typedef struct _IDENTIFY_DATA
	{
		USHORT GeneralConfiguration;
		USHORT NumberOfCylinders;
		USHORT Reserved1;
		USHORT NumberOfHeads;
		USHORT UnformattedBytesPerTrack;
		USHORT UnformattedBytesPerSector;
		USHORT SectorsPerTrack;
		USHORT VendorUnique1[3];
		USHORT SerialNumber[10];
		USHORT BufferType;
		USHORT BufferSectorSize;
		USHORT NumberOfEccBytes;
		USHORT FirmwareRevision[4];
		USHORT ModelNumber[20];
		UCHAR  MaximumBlockTransfer;
		UCHAR  VendorUnique2;
		USHORT DoubleWordIo;
		USHORT Capabilities;
		USHORT Reserved2;
		UCHAR  VendorUnique3;
		UCHAR  PioCycleTimingMode;
		UCHAR  VendorUnique4;
		UCHAR  DmaCycleTimingMode;
		USHORT TranslationFieldsValid : 1;
		USHORT Reserved3 : 15;
		USHORT NumberOfCurrentCylinders;
		USHORT NumberOfCurrentHeads;
		USHORT CurrentSectorsPerTrack;
		ULONG  CurrentSectorCapacity;
		USHORT CurrentMultiSectorSetting;
		ULONG  UserAddressableSectors;
		USHORT SingleWordDMASupport : 8;
		USHORT SingleWordDMAActive : 8;
		USHORT MultiWordDMASupport : 8;
		USHORT MultiWordDMAActive : 8;
		USHORT AdvancedPIOModes : 8;
		USHORT Reserved4 : 8;
		USHORT MinimumMWXferCycleTime;
		USHORT RecommendedMWXferCycleTime;
		USHORT MinimumPIOCycleTime;
		USHORT MinimumPIOCycleTimeIORDY;
		USHORT Reserved5[2];
		USHORT ReleaseTimeOverlapped;
		USHORT ReleaseTimeServiceCommand;
		USHORT MajorRevision;
		USHORT MinorRevision;
		USHORT Reserved6[50];
		USHORT SpecialFunctionsEnabled;
		USHORT Reserved7[128];
	} IDENTIFY_DATA, * PIDENTIFY_DATA;
#pragma pack()

	typedef struct _SRB_IO_CONTROL
	{
		ULONG HeaderLength;
		UCHAR Signature[8 + 1];
		ULONG Timeout;
		ULONG ControlCode;
		ULONG ReturnCode;
		ULONG Length;
	} SRB_IO_CONTROL, * PSRB_IO_CONTROL;

	typedef struct _IDSECTOR
	{
		USHORT  wGenConfig;
		USHORT  wNumCyls;
		USHORT  wReserved;
		USHORT  wNumHeads;
		USHORT  wBytesPerTrack;
		USHORT  wBytesPerSector;
		USHORT  wSectorsPerTrack;
		USHORT  wVendorUnique[3];
		CHAR    sSerialNumber[20];
		USHORT  wBufferType;
		USHORT  wBufferSize;
		USHORT  wECCSize;
		CHAR    sFirmwareRev[8];
		CHAR    sModelNumber[40];
		USHORT  wMoreVendorUnique;
		USHORT  wDoubleWordIO;
		USHORT  wCapabilities;
		USHORT  wReserved1;
		USHORT  wPIOTiming;
		USHORT  wDMATiming;
		USHORT  wBS;
		USHORT  wNumCurrentCyls;
		USHORT  wNumCurrentHeads;
		USHORT  wNumCurrentSectorsPerTrack;
		ULONG   ulCurrentSectorCapacity;
		USHORT  wMultSectorStuff;
		ULONG   ulTotalAddressableSectors;
		USHORT  wSingleWordDMA;
		USHORT  wMultiWordDMA;
		BYTE    bReserved[128];
	} IDSECTOR, * PIDSECTOR;

	typedef struct _GETVERSIONOUTPARAMS
	{
		BYTE bVersion;
		BYTE bRevision;
		BYTE bReserved;
		BYTE bIDEDeviceMap;
		DWORD fCapabilities;
		DWORD dwReserved[4];
	} GETVERSIONOUTPARAMS, * PGETVERSIONOUTPARAMS, * LPGETVERSIONOUTPARAMS;
};

class CNetworkAdapter;
#ifndef tstring
#ifdef _UNICODE
#define tstring std::wstring
#else
#define tstring std::string
#endif
#endif

#pragma comment( lib, "iphlpapi.lib" )

#define DEFAULT_GATEWAY_ADDR	0

struct _IPINFO
{
	tstring sIp;
	tstring sSubnet;
};

class CIpInfoArray : public std::vector < _IPINFO > {};
class StringArray : public std::vector < tstring > {};

DWORD EnumNetworkAdapters(CNetworkAdapter* lpBuffer, ULONG ulSzBuf, LPDWORD lpdwOutSzBuf);

class CNetworkAdapter
{
public:
	CNetworkAdapter();
	~CNetworkAdapter();
	BOOL SetupAdapterInfo(IP_ADAPTER_INFO* pAdaptInfo);

	tstring GetAdapterName() const;
	tstring GetAdapterDescription() const;

	time_t	GetLeaseObtained() const;
	time_t	GetLeaseExpired() const;

	SIZE_T	GetNumIpAddrs() const;
	SIZE_T	GetNumDnsAddrs() const;
	tstring	GetIpAddr(int nIp = 0) const;
	tstring GetSubnetForIpAddr(int nIp = 0) const;
	tstring	GetDnsAddr(int nDns = 0) const;
	tstring GetCurrentIpAddress() const;

	BOOL IsDhcpUsed() const;
	tstring	GetDchpAddr() const;

	BOOL IsWinsUsed() const;
	tstring GetPrimaryWinsServer() const;
	tstring GetSecondaryWinsServer() const;

	tstring	GetGatewayAddr(int nGateway = DEFAULT_GATEWAY_ADDR) const;
	SIZE_T GetNumGatewayAddrs() const;

	static tstring GetAdapterTypeString(UINT nType);
	UINT GetAdapterType() const;

	DWORD GetAdapterIndex() const;

protected:
	tstring	GetStringFromArray(const StringArray* pPtr, int nIndex) const;

private:
	tstring m_sName;
	tstring m_sDesc;
	tstring m_sPriWins;
	tstring m_sSecWins;
	tstring m_sDefGateway;
	tstring m_sDhcpAddr;
	_IPINFO m_sCurIpAddr;
	DWORD m_dwIndex;
	UINT m_nAdapterType;
	BOOL m_bDhcpUsed;
	BOOL m_bWinsUsed;
	StringArray m_DnsAddresses;
	CIpInfoArray m_IpAddresses;
	StringArray m_GatewayList;
	time_t m_tLeaseObtained;
	time_t m_tLeaseExpires;

	struct UNNAMED
	{
		BYTE	ucAddress[MAX_ADAPTER_ADDRESS_LENGTH];
		UINT	nLen;
	} m_ucAddress;

public:
	tstring GetAdapterAddress(void);
};

class CMacAddr
{
	public:
		CMacAddr();
		~CMacAddr();
		std::string getMacAddr() { return m_macAddr; };

	private:
		typedef unsigned char UCHAR;
		void setMACData(std::string test);
		bool IsPrimaryAdapter(DWORD dwIndex);
		bool findValidMac();
		bool initAdapters();
		int GetPrimaryAdapterIndex(void);

	private:
		std::string m_macAddr;
		CNetworkAdapter* m_pAdapters;
		UINT m_nCount;
};