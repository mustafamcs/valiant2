---
name: m2ui
description: Generate, modify, and audit Metin2 Python 2.7 client UI code (uiscript layout dicts, root ui*.py window classes, locale strings, and interfacemodule/game.py bindings) for VALIANT2.
---

# VALIANT2 — Metin2 UI Code Generator & Architecture Skill (`/m2ui`)

Use this skill whenever creating or modifying in-game UI windows in `C:\GitHub\valiant2\assets\unpacked\data\root\` or `uiscript\`.

## 1. Core Rules & Memory Safety
- **Python 2.7 Compatibility:** Use `xrange`, `%` or `.format()` string formatting, old-style/new-style classes inheriting from `ui.ScriptWindow` or `ui.BoardWithTitleBar`.
- **Callback Wrapping (`ui.__mem_func__`):** Always wrap bound methods passed to C++ widgets (`SetEvent`, `SetCloseEvent`, `SetOverInItemEvent`, `SetOverOutItemEvent`, `SAFE_SetEvent`) with `ui.__mem_func__(self.MethodName)` or use `SAFE_SetEvent` to prevent circular reference memory leaks.
- **Feature Flags (`Controls.h` -> `app.ENABLE_*`):** Wrap all optional systems in `if app.ENABLE_<FEATURE>:` blocks so they can be toggled cleanly.
- **Destructor & Cleanup (`Destroy` / `__del__`):** Clear widget references in `Destroy(self)` and call `self.ClearDictionary()`.

## 2. Standard Programmatic Window Pattern (`ui.BoardWithTitleBar`)
When creating self-contained windows without requiring external `.sub` assets:
```python
import ui
import app
import net
import chat
import player
import item
import wndMgr

class ExampleWindow(ui.BoardWithTitleBar):
    def __init__(self):
        ui.BoardWithTitleBar.__init__(self)
        self.isLoaded = False
        self.__BuildWindow()

    def __del__(self):
        ui.BoardWithTitleBar.__del__(self)

    def __BuildWindow(self):
        self.SetSize(360, 280)
        self.SetCenterPosition()
        self.AddFlag("movable")
        self.AddFlag("float")
        self.SetTitleName("Valiant2 Pencere")
        self.SetCloseEvent(ui.__mem_func__(self.Close))
        self.isLoaded = True

    def Open(self):
        self.SetTop()
        self.Show()

    def Close(self):
        self.Hide()

    def OnPressEscapeKey(self):
        self.Close()
        return True
```

## 3. Standard Widget Catalog
- `ui.BoardWithTitleBar()` — Movable board with title and close button (`SetSize`, `SetTitleName`, `SetCloseEvent`).
- `ui.ThinBoard()` — Semi-transparent floating HUD panel (`SetSize`, `SetPosition`).
- `ui.Bar()` — Solid colored rectangle (`SetSize`, `SetColor(0xAA000000)`).
- `ui.TextLine()` — Single-line label (`SetText`, `SetPosition`, `SetPackedFontColor`, `SetHorizontalAlignCenter`, `SetOutline`).
- `ui.Button()` — Clickable button (`SetUpVisual`, `SetOverVisual`, `SetDownVisual`, `SetText`, `SetEvent`).
- `ui.EditLine()` — Text input (`SetSize`, `SetMax`, `SetFocus`, `GetText`, `SetReturnEvent`, `SetEscapeEvent`).
- `ui.GridSlotWindow()` — Item grid (`ArrangeSlot(startIdx, cols, rows, 32, 32, 0, 0)`, `SetItemSlot`, `SetSelectItemSlotEvent`, `SetOverInItemEvent`, `SetOverOutItemEvent`, `RefreshSlot`).

## 4. Packaging & Deployment
After editing files in `assets/unpacked/data/root/` or `locale/`, rebuild the client packs with:
`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/windows/build-client-packs.ps1`

## 5. Critical Pitfalls & Mandatory Conventions (Learned Rules)
1. **NEVER Hardcode Turkish or Non-ASCII Strings in Python (`root` / `uiscript`):**
   - `CGraphicTextInstance` converts strings using `app.GetDefaultCodePage()` (`CP1254` for `tr/en/de/it`, `CP1250` for `ro/pl/cz/hu`). Writing UTF-8 Turkish strings directly in `.py` files produces mojibake (`YÃ¼zen`), and writing `\xfc` hex escapes breaks multi-language support.
   - **Rule:** Always add text keys to all 8 language files (`assets/unpacked/data/locale/{tr,en,de,it,ro,pl,cz,hu}/locale_interface_custom.txt` and `locale_game_custom.txt`) using `scripts\windows\add-locale-string.ps1` and reference them via `localeInfo.KEY` or `uiScriptLocale.KEY`.
2. **`ItemToolTip.AddItemData` Array Lengths:**
   - Never pass a 6-element `metinSlot` or 7-element `attrSlot` list to `tooltipItem.AddItemData(vnum, metinSlot, attrSlot)`! `VALIANT2` uses `player.ATTRIBUTE_SLOT_MAX_NUM` (10) and `player.METIN_SOCKET_MAX_NUM` (6). Passing shorter lists causes `IndexError: list index out of range` in `__AdjustAttrMaxWidth`, leaving an empty tooltip box.
   - **Rule:** Always size `metinSlot` to `max(6, player.METIN_SOCKET_MAX_NUM)` and `attrSlot` to `max(10, player.ATTRIBUTE_SLOT_MAX_NUM)`.
3. **Hover Detection on Custom Rows (`ui.Bar` / `ui.TextLine`):**
   - `ui.Bar` does not reliably fire `OnMouseOverIn` when child labels or buttons overlap it.
   - **Rule:** For custom list rows requiring item tooltips, check cursor coordinates in `OnUpdate(self)` via `mx, my = wndMgr.GetMousePosition()` and `wx, wy = self.GetGlobalPosition()`.
4. **Preventing Dialog Text Overflow:**
   - Long confirmation messages overflow single-line `uiCommon.QuestionDialog()`.
   - **Rule:** Use two-line `uiCommon.QuestionDialog2()` (`SetText1` + `SetText2`) and `SetWidth(340)` for long item/Yang confirmation prompts.

