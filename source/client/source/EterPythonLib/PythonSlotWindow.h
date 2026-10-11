#pragma once

#include "PythonWindow.h"
#include "../Controls.h"
#ifdef ENABLE_OFFLINE_SHOP_GRID
#include "PythonOfflineShopGrid.h"
#endif

namespace UI
{
	enum
	{
		ITEM_WIDTH = 32,
		ITEM_HEIGHT = 32,

		SLOT_NUMBER_NONE = 0xffffffff,
	};

	enum ESlotStyle
	{
		SLOT_STYLE_NONE,
		SLOT_STYLE_PICK_UP,
		SLOT_STYLE_SELECT,
	};

	enum ESlotState
	{
		SLOT_STATE_LOCK = (1 << 0),
		SLOT_STATE_CANT_USE = (1 << 1),
		SLOT_STATE_DISABLE = (1 << 2),
		SLOT_STATE_ALWAYS_RENDER_COVER = (1 << 3),
#ifdef WJ_ENABLE_TRADABLE_ICON
		SLOT_STATE_CANT_MOUSE_EVENT = (1 << 4),
		SLOT_STATE_UNUSABLE = (1 << 5),
#endif
	};

	class CSlotWindow : public CWindow
	{
	public:
		static DWORD Type();

	public:
		class CSlotButton;
		class CCoverButton;
		class CCoolTimeFinishEffect;

		friend class CSlotButton;
		friend class CCoverButton;

		typedef struct SSlot
		{
			DWORD	dwState;
			DWORD	dwSlotNumber;
			DWORD	dwCenterSlotNumber;
			DWORD	dwItemIndex;
			BOOL	isItem;

			// CoolTime
			float	fCoolTime;
			float	fStartCoolTime;

			// Toggle
			BOOL	bActive;
#ifdef ENABLE_HIGHLIGHT_SYSTEM
			BOOL	bActiveNewItem;
			BOOL	bActiveNewItem2;
#endif

			int		ixPosition;
			int		iyPosition;

			int		ixCellSize;
			int		iyCellSize;

			BYTE	byxPlacedItemSize;
			BYTE	byyPlacedItemSize;

			CGraphicImageInstance* pInstance;
			CNumberLine* pNumberLine;

			bool	bRenderBaseSlotImage;
			CCoverButton* pCoverButton;
			CSlotButton* pSlotButton;
			CImageBox* pSignImage;
			CAniImageBox* pFinishCoolTimeEffect;

#ifdef ENABLE_TRADE_BLOCKED_ITEM_ICONS
			CImageBox* pBlockedImage;
			int		ixPlusPosition;
			int		iyPlusPosition;
#endif

		} TSlot;
		typedef std::list<TSlot> TSlotList;
		typedef TSlotList::iterator TSlotListIterator;
		typedef struct SStoreCoolDown { float fCoolTime; float fElapsedTime; bool bActive; } TStoreCoolDown;

	public:
		CSlotWindow(PyObject* ppyObject);
		virtual ~CSlotWindow();

		void Destroy();

		// Manage Slot
		void SetSlotType(DWORD dwType);
		void SetSlotStyle(DWORD dwStyle);

		void AppendSlot(DWORD dwIndex, int ixPosition, int iyPosition, int ixCellSize, int iyCellSize);

#ifdef ENABLE_TRADE_BLOCKED_ITEM_ICONS
		void AppendBlockSlot(const uint32_t dwIndex, const int ixPlusPosition, const int iyPlusPosition);
#endif

		void SetCoverButton(DWORD dwIndex, const char* c_szUpImageName, const char* c_szOverImageName, const char* c_szDownImageName, const char* c_szDisableImageName, BOOL bLeftButtonEnable, BOOL bRightButtonEnable);
		void SetSlotBaseImage(const char* c_szFileName, float fr, float fg, float fb, float fa);
		void AppendSlotButton(const char* c_szUpImageName, const char* c_szOverImageName, const char* c_szDownImageName);
		void AppendRequirementSignImage(const char* c_szImageName);

		void EnableCoverButton(DWORD dwIndex);
		void DisableCoverButton(DWORD dwIndex);
		void SetAlwaysRenderCoverButton(DWORD dwIndex, bool bAlwaysRender = false);

		void ShowSlotBaseImage(DWORD dwIndex);
		void HideSlotBaseImage(DWORD dwIndex);
		BOOL IsDisableCoverButton(DWORD dwIndex);
		BOOL HasSlot(DWORD dwIndex);
#ifdef ENABLE_MINI_GAME_OKEY_NORMAL
		void SetCardSlot(uint32_t dwIndex, uint32_t dwVirtualNumber, uint8_t byWidth, uint8_t byHeight, const char* c_szFileName, D3DXCOLOR& diffuseColor);
#endif
		void ClearAllSlot();
		void ClearSlot(DWORD dwIndex);
		void SetSlot(DWORD dwIndex, DWORD dwVirtualNumber, BYTE byWidth, BYTE byHeight, CGraphicImage* pImage, D3DXCOLOR& diffuseColor);
		void SetSlotCount(DWORD dwIndex, DWORD dwCount);
		void SetSlotCountNew(DWORD dwIndex, DWORD dwGrade, DWORD dwCount);
		void SetSlotCoolTime(DWORD dwIndex, float fCoolTime, float fElapsedTime = 0.0f);
		void UpdateSlotCoolTime(DWORD iSkillType, DWORD iRealSlotIndex, DWORD iOldSlotIndex);

		void StoreSlotCoolTime(DWORD dwKey, DWORD dwSlotIndex, float fCoolTime, float fElapsedTime = .0f);
		void RestoreSlotCoolTime(DWORD dwKey);
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
		void ActivateSlot(DWORD dwIndex, float r = 1.0f, float g = 1.0f, float b = 1.0f, float a = 1.0f, bool isDs = false);
#else
		void ActivateSlot(DWORD dwIndex);
#endif
		void DeactivateSlot(DWORD dwIndex);
		void RefreshSlot();
#ifdef ENABLE_HIGHLIGHT_SYSTEM
		void NewItemActivateSlot(DWORD dwIndex);
		void NewItemActivateSlot2(DWORD dwIndex);
#endif

#ifdef ENABLE_SLOT_WINDOW_EX
		float GetSlotCoolTime(DWORD dwIndex, float* fElapsedTime);
		bool IsActivatedSlot(DWORD dwIndex);
#endif

		DWORD GetSlotCount();

#ifdef ENABLE_OFFLINE_SHOP_GRID
		void	SetGridWindow(int32_t w, int32_t h);
		int32_t	FindEmptyGrid(uint8_t bSizeItem);
		void	PutItemGrid(int32_t iPos, uint8_t bSizeItem);
		void	RemoveItemGrid(int32_t iPos, uint8_t bSizeItem);
		void	ClearItemGrid();

		std::unique_ptr<CGrid> m_pGrid;
#endif

		void GetSlotNumber(std::vector<DWORD>* _v);
		void LockSlot(DWORD dwIndex);
		void UnlockSlot(DWORD dwIndex);
		BOOL IsLockSlot(DWORD dwIndex);
		void SetCantUseSlot(DWORD dwIndex);
		void SetUseSlot(DWORD dwIndex);
		BOOL IsCantUseSlot(DWORD dwIndex);
		void EnableSlot(DWORD dwIndex);
		void DisableSlot(DWORD dwIndex);
		BOOL IsEnableSlot(DWORD dwIndex);
#ifdef WJ_ENABLE_TRADABLE_ICON
		void SetCanMouseEventSlot(DWORD dwIndex);
		void SetCantMouseEventSlot(DWORD dwIndex);
		void SetUsableSlotOnTopWnd(DWORD dwIndex);
		void SetUnusableSlotOnTopWnd(DWORD dwIndex);
#endif

		// Select
		void ClearSelected();
		void SelectSlot(DWORD dwSelectingIndex);
		BOOL isSelectedSlot(DWORD dwIndex);
		DWORD GetSelectedSlotCount();
		DWORD GetSelectedSlotNumber(DWORD dwIndex);

		// Slot Button
		void ShowSlotButton(DWORD dwSlotNumber);
		void HideAllSlotButton();
		void OnPressedSlotButton(DWORD dwType, DWORD dwSlotNumber, BOOL isLeft = TRUE);

		// Requirement Sign
		void ShowRequirementSign(DWORD dwSlotNumber);
		void HideRequirementSign(DWORD dwSlotNumber);

		// ToolTip
		BOOL OnOverInItem(DWORD dwSlotNumber);
		void OnOverOutItem();

#ifdef ENABLE_SLOT_TOOLTIP
		// OverInSlot
		BOOL OnOverInSlot(DWORD dwSlotNumber);
		void OnOverOutSlot();
#endif

		// For Usable Item
		void SetUseMode(BOOL bFlag);
		void SetUsableItem(BOOL bFlag);

		// CallBack
		void ReserveDestroyCoolTimeFinishEffect(DWORD dwSlotIndex);

#ifdef ENABLE_NEW_PET_SYSTEM
		void SetSlotBaseImageScale(const char* c_szFileName, float fr, float fg, float fb, float fa, float sx, float sy);
		void SetSlotScale(DWORD dwIndex, DWORD dwVirtualNumber, BYTE byWidth, BYTE byHeight, CGraphicImage* pImage, float sx, float sy, D3DXCOLOR& diffuseColor);
		void __CreateBaseImageScale(const char* c_szFileName, float fr, float fg, float fb, float fa, float sx, float sy);
#endif

	protected:
		void __Initialize();
		void __CreateToggleSlotImage();
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
		void __CreateSlotEnableEffect(float r = 1.0f, float g = 1.0f, float b = 1.0f, float a = 1.0f, bool isDs = false);
#else
		void __CreateSlotEnableEffect();
#endif

#ifdef ENABLE_HIGHLIGHT_SYSTEM
		void __CreateSlotNewItemEffect();
		void __CreateSlotNewItemEffect2();
#endif
		void __CreateFinishCoolTimeEffect(TSlot* pSlot);
		void __CreateBaseImage(const char* c_szFileName, float fr, float fg, float fb, float fa);
		void __DestroyToggleSlotImage();
		void __DestroySlotEnableEffect();
#ifdef ENABLE_HIGHLIGHT_SYSTEM
		void __DestroyNewItemSlotEffect();
		void __DestroyNewItemSlotEffect2();
#endif
		void __DestroyFinishCoolTimeEffect(TSlot* pSlot);
		void __DestroyBaseImage();

		// Event
		void OnUpdate();
		void OnRender();
		BOOL OnMouseLeftButtonDown();
		BOOL OnMouseLeftButtonUp();
		BOOL OnMouseRightButtonDown();
		BOOL OnMouseLeftButtonDoubleClick();
		void OnMouseOverOut();
		void OnMouseOver();
		void RenderSlotBaseImage();
		void RenderLockedSlot();
		virtual void OnRenderPickingSlot();
		virtual void OnRenderSelectedSlot();

		// Select
		void OnSelectEmptySlot(int iSlotNumber);
		void OnSelectItemSlot(int iSlotNumber);
		void OnUnselectEmptySlot(int iSlotNumber);
		void OnUnselectItemSlot(int iSlotNumber);
		void OnUseSlot();

		// Manage Slot
		BOOL GetSlotPointer(DWORD dwIndex, TSlot** ppSlot);
		BOOL GetSelectedSlotPointer(TSlot** ppSlot);
		virtual BOOL GetPickedSlotPointer(TSlot** ppSlot);
		void ClearSlot(TSlot* pSlot);
		virtual void OnRefreshSlot();

		// ETC
		BOOL OnIsType(DWORD dwType);

	protected:
		DWORD m_dwSlotType;
		DWORD m_dwSlotStyle;
		std::list<DWORD> m_dwSelectedSlotIndexList;
		TSlotList m_SlotList;
#ifdef ENABLE_SLOT_TOOLTIP
		DWORD m_dwOverInSlotNumber;
#endif
		DWORD m_dwToolTipSlotNumber;
		std::map<DWORD, std::map<DWORD, SStoreCoolDown>>	m_CoolDownStore;
		BOOL m_isUseMode;
		BOOL m_isUsableItem;

		CGraphicImageInstance* m_pBaseImageInstance;
		CImageBox* m_pToggleSlotImage;
#ifdef ENABLE_HIGHLIGHT_SYSTEM
		CAniImageBox* m_apSlotActiveEffect[3];
		CAniImageBox* m_apSlotNewItemEffect[3];//R2.TO effect lwork
		CAniImageBox* m_apSlotNewItemEffect2[3];//R2.TO effect lwork
#else
		CAniImageBox* m_pSlotActiveEffect;
#endif
		std::deque<DWORD> m_ReserveDestroyEffectDeque;
	};
};
