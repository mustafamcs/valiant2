#pragma once

#include "../eterGrnLib/Thing.h"

class CRaceMotionData;
class CAttributeData;

#define COMBO_KEY									DWORD
#define MAKE_COMBO_KEY(motion_mode, combo_type)		(	(DWORD(motion_mode) << 16) | (DWORD(combo_type))	)
#define COMBO_KEY_GET_MOTION_MODE(key)				(	WORD(DWORD(key) >> 16 & 0xFFFF)						)
#define COMBO_KEY_GET_COMBO_TYPE(key)				(	WORD(DWORD(key) & 0xFFFF)							)

class CRaceData
{
public:
	enum EParts
	{
		// Share index with server
		PART_MAIN,
		PART_WEAPON,
		PART_HEAD,
		PART_WEAPON_LEFT,
		PART_HAIR,
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
		PART_ACCE,
#endif
#ifdef ENABLE_AURA_SYSTEM
		PART_AURA,
#endif
#ifdef ENABLE_CROWN_SYSTEM
		PART_CROWN,
#endif
		PART_MAX_NUM,
	};

	enum
	{
		RACE_WARRIOR_M,
		RACE_ASSASSIN_W,
		RACE_SURA_M,
		RACE_SHAMAN_W,
		RACE_WARRIOR_W,
		RACE_ASSASSIN_M,
		RACE_SURA_W,
		RACE_SHAMAN_M,
#ifdef ENABLE_WOLFMAN_CHARACTER
		RACE_WOLFMAN_M,
#endif
		RACE_MAX_NUM,
	};

	enum
	{
		SMOKE_NUM = 4,
	};

	/////////////////////////////////////////////////////////////////////////////////
	// Graphic Resource

	// Model
	typedef std::map<WORD, CGraphicThing*> TGraphicThingMap;
	typedef std::map<DWORD, std::string> TAttachingBoneNameMap;

	// Motion
	typedef struct SMotion
	{
		BYTE byPercentage;
		CGraphicThing* pMotion;
		CRaceMotionData* pMotionData;
	} TMotion;
	typedef std::vector<TMotion> TMotionVector;
	typedef std::map<WORD, TMotionVector> TMotionVectorMap;

	typedef struct SMotionModeData
	{
		WORD wMotionModeIndex;

		TMotionVectorMap MotionVectorMap;

		SMotionModeData() : wMotionModeIndex(0) {} /*@M2Fixme001*/
		virtual ~SMotionModeData() {}
	} TMotionModeData;
	typedef std::map<WORD, TMotionModeData*> TMotionModeDataMap;
	typedef TMotionModeDataMap::iterator TMotionModeDataIterator;

	/////////////////////////////////////////////////////////////////////////////////
	// Model Data
	typedef struct SModelData
	{
		NRaceData::TAttachingDataVector AttachingDataVector;
	} TModelData;
	typedef std::map<DWORD, TModelData> TModelDataMap;
	typedef TModelDataMap::iterator TModelDataMapIterator;

	/////////////////////////////////////////////////////////////////////////////////
	// Motion Data
	typedef std::map<DWORD, CRaceMotionData*> TMotionDataMap;

	/////////////////////////////////////////////////////////////////////////////////
	// Combo Data
	typedef std::vector<DWORD> TComboIndexVector;
	typedef struct SComboAttackData
	{
		TComboIndexVector ComboIndexVector;
	} TComboData;
	typedef std::map<DWORD, DWORD> TNormalAttackIndexMap;
	typedef std::map<COMBO_KEY, TComboData> TComboAttackDataMap;
	typedef TComboAttackDataMap::iterator TComboAttackDataIterator;

	struct SSkin
	{
		int m_ePart;

		std::string m_stSrcFileName;
		std::string m_stDstFileName;

		SSkin()
		{
			m_ePart = 0;
		}
		SSkin(const SSkin& c_rkSkin)
		{
			Copy(c_rkSkin);
		}
		void operator=(const SSkin& c_rkSkin)
		{
			Copy(c_rkSkin);
		}
		void Copy(const SSkin& c_rkSkin)
		{
			m_ePart = c_rkSkin.m_ePart;
			m_stSrcFileName = c_rkSkin.m_stSrcFileName;
			m_stDstFileName = c_rkSkin.m_stDstFileName;
		}
	};

	struct SHair
	{
		std::string m_stModelFileName;
		std::vector<SSkin> m_kVct_kSkin;
	};
#ifdef ENABLE_CROWN_SYSTEM
	struct SCrown
	{
		std::string m_stModelFileName;
		std::vector<SSkin> m_kVct_kSkin;
	};
#endif
	struct SShape
	{
		std::string m_stModelFileName;
		std::vector<SSkin> m_kVct_kSkin;
	};

public:
	static CRaceData* New();
	static void Delete(CRaceData* pkRaceData);
	static void CreateSystem(unsigned uCapacity, unsigned uMotModeCapacity);
	static void DestroySystem();

public:
	CRaceData();
	virtual ~CRaceData();

	void Destroy();

	// Codes For Client
	const char* GetBaseModelFileName() const;
	const char* GetAttributeFileName() const;
	const char* GetMotionListFileName() const;
	CGraphicThing* GetBaseModelThing();
	CGraphicThing* GetLODModelThing();
	CAttributeData* GetAttributeDataPtr();
	BOOL GetAttachingBoneName(DWORD dwPartIndex, const char** c_pszBoneName);
	BOOL CreateMotionModeIterator(TMotionModeDataIterator& itor);
	BOOL NextMotionModeIterator(TMotionModeDataIterator& itor);
	BOOL GetMotionKey(const WORD &wMotionModeIndex, const WORD &wMotionIndex, MOTION_KEY* pMotionKey);

	BOOL GetMotionModeDataPointer(const WORD &wMotionMode, TMotionModeData** ppMotionModeData);
	BOOL GetModelDataPointer(const DWORD &dwModelIndex, const TModelData** c_ppModelData);
	BOOL GetMotionVectorPointer(const WORD &wMotionMode, const WORD &wMotionIndex, const TMotionVector** c_ppMotionVector);
	BOOL GetMotionDataPointer(const WORD &wMotionMode, const WORD &wMotionIndex, const WORD &wMotionSubIndex, CRaceMotionData** ppMotionData);
	BOOL GetMotionDataPointer(const DWORD &dwMotionKey, CRaceMotionData** ppMotionData);
#ifdef ENABLE_CLIENT_OPTIMISATION
	DWORD GetRace() const { return m_dwRaceIndex; };
#endif

	DWORD GetAttachingDataCount();
	BOOL GetAttachingDataPointer(DWORD dwIndex, const NRaceData::TAttachingData** c_ppAttachingData);
	BOOL GetCollisionDataPointer(DWORD dwIndex, const NRaceData::TAttachingData** c_ppAttachingData);
	BOOL GetBodyCollisionDataPointer(const NRaceData::TAttachingData** c_ppAttachingData);

	BOOL IsTree();
	const char* GetTreeFileName();

	///////////////////////////////////////////////////////////////////
	// Setup by Script
	BOOL LoadRaceData(const char* c_szFileName);

	CGraphicThing* RegisterMotionData(WORD wMotionMode, DWORD wMotionIndex, const char* c_szFileName, BYTE byPercentage = 100);

	///////////////////////////////////////////////////////////////////
	// Setup by Python
	void SetRace(DWORD dwRaceIndex);
	void RegisterAttachingBoneName(DWORD dwPartIndex, const char* c_szBoneName);

	void RegisterMotionMode(WORD wMotionModeIndex);
	void SetMotionModeParent(WORD wParentMotionModeIndex, WORD wMotionModeIndex);
	CGraphicThing* NEW_RegisterMotion(CRaceMotionData* pkMotionData, const WORD wMotionModeIndex, const WORD wMotionIndex, const char* c_szFileName, BYTE byPercentage = 100);
	bool SetMotionRandomWeight(WORD wMotionModeIndex, WORD wMotionIndex, WORD wMotionSubIndex, BYTE byPercentage);

	void RegisterNormalAttack(WORD wMotionModeIndex, WORD wMotionIndex);
	BOOL GetNormalAttackIndex(WORD wMotionModeIndex, WORD* pwMotionIndex);

	void ReserveComboAttack(WORD wMotionModeIndex, WORD wComboType, DWORD dwComboCount);
	void RegisterComboAttack(WORD wMotionModeIndex, WORD wComboType, DWORD dwComboIndex, WORD wMotionIndex);
	BOOL GetComboDataPointer(WORD wMotionModeIndex, WORD wComboType, TComboData** ppComboData);

	void SetShapeModel(unsigned eShape, const char* c_szModelFileName);
	void AppendShapeSkin(unsigned eShape, unsigned ePart, const char* c_szSrcFileName, const char* c_szDstFileName);

	void SetHairSkin(const unsigned eHair, const unsigned ePart, const char* c_szModelFileName, const char* c_szSrcFileName, const char* c_szDstFileName);
#ifdef ENABLE_CROWN_SYSTEM
	void SetCrownSkin(unsigned eCrown, unsigned ePart, const char* c_szModelFileName, const char* c_szSrcFileName, const char* c_szDstFileName);
#endif
	/////

	DWORD GetSmokeEffectID(unsigned eSmoke);

	const std::string& GetSmokeBone();

	SHair* FindHair(const unsigned& eHair);
	SShape* FindShape(const unsigned& eShape);
#ifdef ENABLE_CROWN_SYSTEM
	SCrown* FindCrown(const unsigned &eCrown);
#endif

protected:
	void __Initialize();
	BOOL GetMotionVectorPointer(const WORD &wMotionMode, const WORD &wMotionIndex, TMotionVector** ppMotionVector);

protected:
	DWORD m_dwRaceIndex;
	DWORD m_adwSmokeEffectID[SMOKE_NUM];

	CGraphicThing* m_pBaseModelThing;
	CGraphicThing* m_pLODModelThing;

	std::string m_strBaseModelFileName;
	std::string m_strTreeFileName;
	std::string m_strAttributeFileName;
	std::string m_strMotionListFileName;
	std::string m_strSmokeBoneName;

	TModelDataMap m_ModelDataMap;
	TMotionModeDataMap m_pMotionModeDataMap;
	TAttachingBoneNameMap m_AttachingBoneNameMap;
	TComboAttackDataMap m_ComboAttackDataMap;
	TNormalAttackIndexMap m_NormalAttackIndexMap;

	std::map<DWORD, SHair> m_kMap_dwHairKey_kHair;
	std::map<DWORD, SShape> m_kMap_dwShapeKey_kShape;
#ifdef ENABLE_CROWN_SYSTEM
	std::map<DWORD, SCrown> m_kMap_dwCrownKey_kCrown;
#endif

	NRaceData::TAttachingDataVector m_AttachingDataVector;

protected:
	static CMemoryPoolNew<TMotionModeData>	ms_MotionModeDataPool;
	static CMemoryPoolNew<CRaceData>			ms_kPool;
};
