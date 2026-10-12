# -*- coding: cp949 -*-
#-119339412
import ui, wndMgr

class TextLineColorTest(ui.BoardWithTitleBar):
    WIDTH = 400
    HEIGHT = 330
    def __init__(self):
        ui.BoardWithTitleBar.__init__(self)

        # wndMgr.SetOutlineFlag(1)
        self.rainbauwFontSeed = 0.
        self.rainbauwOutLineSeed = 0.
        self.rainbauwSpeed = .3
        self.rainbauwFont = False
        self.rainbauwOutLine = False
        self.colorFont = [0.0, 0.0, 0.0]
        self.colorOutLine = [0.0, 0.0, 0.0, 0.0]
        self.__LoadWindow()
        self.__LoadGUI()

    def __del__(self):
        ui.BoardWithTitleBar.__del__(self)

    def __LoadWindow(self):
        self.max_pos_x = wndMgr.GetScreenWidth() - self.WIDTH
        self.max_pos_y = wndMgr.GetScreenHeight() - self.HEIGHT
        self.SetSize(self.WIDTH, self.HEIGHT)
        self.SetCenterPosition()
        self.AddFlag('movable')
        self.SetTitleName(" ~ TextLineColorTest ~ ")
        self.SetCloseEvent(self.Close)

    def ResetFontColorSliderBarR(self):
        self.FontColorSliderBarR.SetSliderPos(0.)
        apply(self.FontColorSliderBarR.eventChange, [])

    def SeekFontColorSliderBarR(self):
        self.FontColorSliderBarR.SetSliderPos(float(self.FontColorSliderBarR.backGroundImage.GetMouseLocalPosition()[0])/float(self.FontColorSliderBarR.backGroundImage.GetWidth()))
        apply(self.FontColorSliderBarR.eventChange, [])

    def OnChangeFontColorR(self):
        pos = self.FontColorSliderBarR.GetSliderPos()
        self.FontRLabel.SetText("Font Red: %d" % (0. + 255.*pos))
        self.colorFont[0] = (255. * pos) / 255.
        self.TextLine.SetFontColor(*self.colorFont)

    def ResetFontColorSliderBarG(self):
        self.FontColorSliderBarG.SetSliderPos(0.)
        apply(self.FontColorSliderBarG.eventChange, [])

    def SeekFontColorSliderBarG(self):
        self.FontColorSliderBarG.SetSliderPos(float(self.FontColorSliderBarG.backGroundImage.GetMouseLocalPosition()[0])/float(self.FontColorSliderBarG.backGroundImage.GetWidth()))
        apply(self.FontColorSliderBarG.eventChange, [])

    def OnChangeFontColorG(self):
        pos = self.FontColorSliderBarG.GetSliderPos()
        self.FontGLabel.SetText("Font Green: %d" % (0. + (255.*pos)))
        self.colorFont[1] = (255. * pos)/ 255.
        self.TextLine.SetFontColor(*self.colorFont)

    def ResetFontColorSliderBarB(self):
        self.FontColorSliderBarB.SetSliderPos(0.)
        apply(self.FontColorSliderBarB.eventChange, [])

    def SeekFontColorSliderBarB(self):
        self.FontColorSliderBarB.SetSliderPos(float(self.FontColorSliderBarB.backGroundImage.GetMouseLocalPosition()[0])/float(self.FontColorSliderBarB.backGroundImage.GetWidth()))
        apply(self.FontColorSliderBarB.eventChange, [])

    def OnChangeFontColorB(self):
        pos = self.FontColorSliderBarB.GetSliderPos()
        self.FontBLabel.SetText("Font Blue: %d" % (0. + (255.*pos)))
        self.colorFont[2] = (255. * pos)/ 255.
        self.TextLine.SetFontColor(*self.colorFont)

    def ResetOutLineColorSliderBarR(self):
        self.OutLineColorSliderBarR.SetSliderPos(0.)
        apply(self.OutLineColorSliderBarR.eventChange, [])

    def SeekOutLineColorSliderBarR(self):
        self.OutLineColorSliderBarR.SetSliderPos(float(self.OutLineColorSliderBarR.backGroundImage.GetMouseLocalPosition()[0])/float(self.OutLineColorSliderBarR.backGroundImage.GetWidth()))
        apply(self.OutLineColorSliderBarR.eventChange, [])

    def OnChangeOutLineColorR(self):
        pos = self.OutLineColorSliderBarR.GetSliderPos()
        self.OutLineRLabel.SetText("OutLine Red: %d" % (0. + (255.*pos)))
        self.colorOutLine[0] = (255. * pos)/ 255.
        self.TextLine.SetOutLineColor(*self.colorOutLine)

    def ResetOutLineColorSliderBarG(self):
        self.OutLineColorSliderBarG.SetSliderPos(0.)
        apply(self.OutLineColorSliderBarG.eventChange, [])

    def SeekOutLineColorSliderBarB(self):
        self.OutLineColorSliderBarG.SetSliderPos(float(self.OutLineColorSliderBarG.backGroundImage.GetMouseLocalPosition()[0])/float(self.OutLineColorSliderBarG.backGroundImage.GetWidth()))
        apply(self.OutLineColorSliderBarG.eventChange, [])

    def OnChangeOutLineColorG(self):
        pos = self.OutLineColorSliderBarG.GetSliderPos()
        self.OutLineGLabel.SetText("OutLine Green: %d" % (0. + (255.*pos)))
        self.colorOutLine[1] = (255. * pos)/ 255.
        self.TextLine.SetOutLineColor(*self.colorOutLine)

    def ResetOutLineColorSliderBarB(self):
        self.OutLineColorSliderBarB.SetSliderPos(0.)
        apply(self.OutLineColorSliderBarB.eventChange, [])

    def SeekOutLineColorSliderBarB(self):
        self.OutLineColorSliderBarB.SetSliderPos(float(self.OutLineColorSliderBarB.backGroundImage.GetMouseLocalPosition()[0])/float(self.OutLineColorSliderBarB.backGroundImage.GetWidth()))
        apply(self.OutLineColorSliderBarB.eventChange, [])

    def OnChangeOutLineColorB(self):
        pos = self.OutLineColorSliderBarB.GetSliderPos()
        self.OutLineBLabel.SetText("OutLine Blue: %d" % (0. + (255.*pos)))
        self.colorOutLine[2] = (255. * pos)/ 255.
        self.TextLine.SetOutLineColor(*self.colorOutLine)

    def ResetOutLineColorSliderBarA(self):
        self.OutLineColorSliderBarA.SetSliderPos(0.)
        apply(self.OutLineColorSliderBarA.eventChange, [])

    def SeekOutLineColorSliderBarA(self):
        self.OutLineColorSliderBarA.SetSliderPos(float(self.OutLineColorSliderBarA.backGroundImage.GetMouseLocalPosition()[0])/float(self.OutLineColorSliderBarA.backGroundImage.GetWidth()))
        apply(self.OutLineColorSliderBarA.eventChange, [])

    def OnChangeOutLineColorA(self):
        pos = self.OutLineColorSliderBarA.GetSliderPos()
        self.OutLineALabel.SetText("OutLine Alpha: %.2f" % (0. + (1.*pos)))
        self.colorOutLine[3] = (1. * pos)/ 1.
        self.TextLine.SetOutLineColor(*self.colorOutLine)

    def OnToggleDownRainBowFont(self):
        self.rainbauwFont = True

    def OnToggleUpRainBowFont(self):
        self.rainbauwFont = False
        self.rainbauwFontSeed = 0.
        self.ResetFontColorSliderBarR()
        self.ResetFontColorSliderBarG()
        self.ResetFontColorSliderBarB()

    def OnToggleDownRainBowOutLine(self):
        self.rainbauwOutLine = True

    def OnToggleUpRainBowOutLine(self):
        self.rainbauwOutLine = False
        self.rainbauwOutLineSeed = 0.
        self.ResetOutLineColorSliderBarR()
        self.ResetOutLineColorSliderBarG()
        self.ResetOutLineColorSliderBarB()
        self.ResetOutLineColorSliderBarA()

    def __LoadGUI(self):
        self.ModelView = ui.Window()
        self.ModelView.SetParent(self)
        self.ModelView.SetPosition(16, 29)
        self.ModelView.SetSize(190, 300)
        self.ModelView.Show()

        self.btnRainBowFont = ui.ToggleButton()
        self.btnRainBowFont.SetParent(self.ModelView)
        self.btnRainBowFont.SetPosition(16, 29)
        self.btnRainBowFont.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
        self.btnRainBowFont.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
        self.btnRainBowFont.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
        self.btnRainBowFont.SetText("Font")
        self.btnRainBowFont.SetToggleDownEvent(ui.__mem_func__(self.OnToggleDownRainBowFont))
        self.btnRainBowFont.SetToggleUpEvent(ui.__mem_func__(self.OnToggleUpRainBowFont))
        self.btnRainBowFont.Show()
        
        self.btnRainBowOutLine = ui.ToggleButton()
        self.btnRainBowOutLine.SetParent(self.ModelView)
        self.btnRainBowOutLine.SetPosition(102, 29)
        self.btnRainBowOutLine.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
        self.btnRainBowOutLine.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
        self.btnRainBowOutLine.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
        self.btnRainBowOutLine.SetText("OutLine")
        self.btnRainBowOutLine.SetToggleDownEvent(ui.__mem_func__(self.OnToggleDownRainBowOutLine))
        self.btnRainBowOutLine.SetToggleUpEvent(ui.__mem_func__(self.OnToggleUpRainBowOutLine))
        self.btnRainBowOutLine.Show()

        self.TextLine = ui.TextLine()
        self.TextLine.SetParent(self.ModelView)
        self.TextLine.SetPosition(0, 0)
        self.TextLine.SetOutline(True)
        self.TextLine.SetMultiLine()
        # self.TextLine.SetLineHeight(20)
        self.TextLine.SetFontColor(*self.colorFont)
        self.TextLine.SetOutLineColor(*self.colorOutLine)
        self.TextLine.SetText("TEST TEXT COLOR\\nWHAT IS RAINBAUUUW")
        self.TextLine.SetWindowHorizontalAlignCenter()
        self.TextLine.SetWindowVerticalAlignCenter()
        self.TextLine.SetHorizontalAlignCenter()
        self.TextLine.SetVerticalAlignCenter()
        self.TextLine.Show()

        self.FontRLabel = ui.TextLine()
        self.FontRLabel.SetParent(self)
        self.FontRLabel.SetText("Font Red: 0")
        self.FontRLabel.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 0 * 20)
        self.FontRLabel.Show()

        self.FontColorSliderBarR = ui.SliderBar()
        self.FontColorSliderBarR.SetParent(self)
        self.FontColorSliderBarR.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 1 * 20)
        self.FontColorSliderBarR.SetSliderPos(0.)
        self.FontColorSliderBarR.backGroundImage.OnMouseLeftButtonDown = self.SeekFontColorSliderBarR
        self.FontColorSliderBarR.cursor.OnMouseRightButtonDown = self.ResetFontColorSliderBarR
        self.FontColorSliderBarR.SetEvent(ui.__mem_func__(self.OnChangeFontColorR))
        self.FontColorSliderBarR.Show()

        self.FontGLabel = ui.TextLine()
        self.FontGLabel.SetParent(self)
        self.FontGLabel.SetText("Font Green: 0")
        self.FontGLabel.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 2 * 20)
        self.FontGLabel.Show()

        self.FontColorSliderBarG = ui.SliderBar()
        self.FontColorSliderBarG.SetParent(self)
        self.FontColorSliderBarG.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 3 * 20)
        self.FontColorSliderBarG.SetSliderPos(0.)
        self.FontColorSliderBarG.backGroundImage.OnMouseLeftButtonDown = self.SeekFontColorSliderBarG
        self.FontColorSliderBarG.cursor.OnMouseRightButtonDown = self.ResetFontColorSliderBarG
        self.FontColorSliderBarG.SetEvent(ui.__mem_func__(self.OnChangeFontColorG))
        self.FontColorSliderBarG.Show()

        self.FontBLabel = ui.TextLine()
        self.FontBLabel.SetParent(self)
        self.FontBLabel.SetText("Font Blue: 0")
        self.FontBLabel.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 4 + 4 * 20)
        self.FontBLabel.Show()

        self.FontColorSliderBarB = ui.SliderBar()
        self.FontColorSliderBarB.SetParent(self)
        self.FontColorSliderBarB.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 5 * 20)
        self.FontColorSliderBarB.SetSliderPos(0.)
        self.FontColorSliderBarB.backGroundImage.OnMouseLeftButtonDown = self.SeekFontColorSliderBarB
        self.FontColorSliderBarB.cursor.OnMouseRightButtonDown = self.ResetFontColorSliderBarB
        self.FontColorSliderBarB.SetEvent(ui.__mem_func__(self.OnChangeFontColorB))
        self.FontColorSliderBarB.Show()

        self.OutLineRLabel = ui.TextLine()
        self.OutLineRLabel.SetParent(self)
        self.OutLineRLabel.SetText("OutLine Red: 0")
        self.OutLineRLabel.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 6 * 20)
        self.OutLineRLabel.Show()

        self.OutLineColorSliderBarR = ui.SliderBar()
        self.OutLineColorSliderBarR.SetParent(self)
        self.OutLineColorSliderBarR.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 7 * 20)
        self.OutLineColorSliderBarR.SetSliderPos(0.)
        self.OutLineColorSliderBarR.backGroundImage.OnMouseLeftButtonDown = self.SeekOutLineColorSliderBarR
        self.OutLineColorSliderBarR.cursor.OnMouseRightButtonDown = self.ResetOutLineColorSliderBarR
        self.OutLineColorSliderBarR.SetEvent(ui.__mem_func__(self.OnChangeOutLineColorR))
        self.OutLineColorSliderBarR.Show()

        self.OutLineGLabel = ui.TextLine()
        self.OutLineGLabel.SetParent(self)
        self.OutLineGLabel.SetText("OutLine Green: 0")
        self.OutLineGLabel.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 8 * 20)
        self.OutLineGLabel.Show()

        self.OutLineColorSliderBarG = ui.SliderBar()
        self.OutLineColorSliderBarG.SetParent(self)
        self.OutLineColorSliderBarG.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 9 * 20)
        self.OutLineColorSliderBarG.SetSliderPos(0.)
        self.OutLineColorSliderBarG.backGroundImage.OnMouseLeftButtonDown = self.SeekOutLineColorSliderBarB
        self.OutLineColorSliderBarG.cursor.OnMouseRightButtonDown = self.ResetOutLineColorSliderBarG
        self.OutLineColorSliderBarG.SetEvent(ui.__mem_func__(self.OnChangeOutLineColorG))
        self.OutLineColorSliderBarG.Show()

        self.OutLineBLabel = ui.TextLine()
        self.OutLineBLabel.SetParent(self)
        self.OutLineBLabel.SetText("OutLine Blue: 0")
        self.OutLineBLabel.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 4 + 10 * 20)
        self.OutLineBLabel.Show()

        self.OutLineColorSliderBarB = ui.SliderBar()
        self.OutLineColorSliderBarB.SetParent(self)
        self.OutLineColorSliderBarB.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 11 * 20)
        self.OutLineColorSliderBarB.SetSliderPos(0.)
        self.OutLineColorSliderBarB.backGroundImage.OnMouseLeftButtonDown = self.SeekOutLineColorSliderBarB
        self.OutLineColorSliderBarB.cursor.OnMouseRightButtonDown = self.ResetOutLineColorSliderBarB
        self.OutLineColorSliderBarB.SetEvent(ui.__mem_func__(self.OnChangeOutLineColorB))
        self.OutLineColorSliderBarB.Show()

        self.OutLineALabel = ui.TextLine()
        self.OutLineALabel.SetParent(self)
        self.OutLineALabel.SetText("OutLine Alpha: 1.00")
        self.OutLineALabel.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 4 + 12 * 20)
        self.OutLineALabel.Show()

        self.OutLineColorSliderBarA = ui.SliderBar()
        self.OutLineColorSliderBarA.SetParent(self)
        self.OutLineColorSliderBarA.SetPosition(16 + self.ModelView.GetWidth() + 10, 29 + 3 + 13 * 20)
        self.OutLineColorSliderBarA.SetSliderPos(1.)
        self.OutLineColorSliderBarA.backGroundImage.OnMouseLeftButtonDown = self.SeekOutLineColorSliderBarA
        self.OutLineColorSliderBarA.cursor.OnMouseRightButtonDown = self.ResetOutLineColorSliderBarA
        self.OutLineColorSliderBarA.SetEvent(ui.__mem_func__(self.OnChangeOutLineColorA))
        self.OutLineColorSliderBarA.Show()

    def Open(self):
        ui.BoardWithTitleBar.Show(self)

    def Close(self):
        # wndMgr.SetOutlineFlag(0)
        self.Hide()
        return 1

    def OnPressEscapeKey(self):
        self.Close()
        return 1

    def rgb(self, ratio, isoutline = False):
        normalized = int(ratio * 256 * 6)
        x = normalized % 256

        red = grn = blu = alp = 0
        state = normalized / 256
        if state == 0: # red
            red = 255
            grn = x
            blu = 0
            alp = x if isoutline else 255
        elif state == 1:
            red = 255 - x
            grn = 255
            blu = 0
            alp = 255 - x if isoutline else 255
        elif state == 2:
            red = 0
            grn = 255
            blu = x
            alp = x if isoutline else 255
        elif state == 3:
            red = 0
            grn = 255 - x
            blu = 255
            alp = 255 - x if isoutline else 255
        elif state == 4:
            red = x
            grn = 0
            blu = 255
            alp = x if isoutline else 255
        elif state == 5:
            red = 255
            grn = 0
            blu = 255 - x
            alp = 255 - x if isoutline else 255

        if isoutline:
            self.OutLineColorSliderBarR.SetSliderPos(red/255.); self.OnChangeOutLineColorR()
            self.OutLineColorSliderBarG.SetSliderPos(grn/255.); self.OnChangeOutLineColorG()
            self.OutLineColorSliderBarB.SetSliderPos(blu/255.); self.OnChangeOutLineColorB()
            self.OutLineColorSliderBarA.SetSliderPos(alp/255.); self.OnChangeOutLineColorA()
        else:
            self.FontColorSliderBarR.SetSliderPos(red/255.); self.OnChangeFontColorR()
            self.FontColorSliderBarG.SetSliderPos(grn/255.); self.OnChangeFontColorG()
            self.FontColorSliderBarB.SetSliderPos(blu/255.); self.OnChangeFontColorB()

        #return red + (grn << 8) + (blu << 16) + (alp << 24);

    def OnUpdate(self):
        if self.rainbauwFont:
            self.rgb(self.rainbauwFontSeed / 60, False)

            if self.rainbauwFontSeed < 60:
                self.rainbauwFontSeed += self.rainbauwSpeed
            else:
                self.rainbauwFontSeed = 0.

        if self.rainbauwOutLine:
            self.rgb(self.rainbauwOutLineSeed / 60, True)

            if self.rainbauwOutLineSeed < 60:
                self.rainbauwOutLineSeed += self.rainbauwSpeed
            else:
                self.rainbauwOutLineSeed = 0.

a=TextLineColorTest()
try:
    a.Open()
except:
    a.Show()

