__author__ = "Light5"
__latest_update__ = "02.04.2023, 14.00"
__work__ = "wikipedia"

import ui, app, renderTarget
import localeInfo
import renderTarget
from wikiui import GetCharTypeHairCamera

IMG_DIR = "d:/ymir work/ui/game/wiki/"
PATH_ROOT = "offlineshop/lightwork/searchshop/"

class WikipediaBoard(ui.BoardWithTitleBar):

    def __del__(self):
        ui.BoardWithTitleBar.__del__(self)

    def __init__(self):	
        ui.BoardWithTitleBar.__init__(self)
        self.Constructor()
        self.LoadInterface()

        if app.ENABLE_WINDOW_ANIMATION:
            self.SetWindowAnimation()

    def Constructor(self):
        self.selectedCharacterButton = 0

    def LoadInterface(self):
        self.SetSize(750, 500)
        self.SetTitleName(localeInfo.WIKI_TITLE)
        self.SetCenterPosition()
        self.AddFlag("movable")
        self.AddFlag("float")

        self.categoryBoard = ui.ExpandedImageBox()
        self.categoryBoard.SetParent(self)
        self.categoryBoard.SetPosition(10, 40)
        self.categoryBoard.LoadImage(IMG_DIR+"category_bg.png")
        self.categoryBoard.Show()

        self.wikiBoard = ui.ExpandedImageBox()
        self.wikiBoard.SetParent(self)
        self.wikiBoard.SetPosition(70, 40)
        self.wikiBoard.LoadImage(IMG_DIR+"category_bg.png")
        # self.wikiBoard.Show()

    def OnPressEscapeKey(self):
        self.Close()
        return True

    def Close(self):
        self.Hide()

class ModelTester(ui.BoardWithTitleBar):

    def __del__(self):
        ui.BoardWithTitleBar.__del__(self)

    def __init__(self):	
        ui.BoardWithTitleBar.__init__(self)
        self.SetSize(780, 500)
        self.SetTitleName("ESSEK GIBI OLMAMAK ICIN TEST GUISI")
        self.SetCenterPosition()
        self.AddFlag("movable")
        self.AddFlag("float")
        self.indexList = list()
        self.modelPreviews = [x for x in xrange(8)]

        for i in xrange(8):
            self.indexList.append(app.GetRandom(0, 1000))
    
            self.modelPreviews[i] = ui.RenderTarget()
            self.modelPreviews[i].SetParent(self)
            self.modelPreviews[i].SetWindowHorizontalAlignCenter()
            self.modelPreviews[i].SetSize(200, 200)
            if i < 4:
                self.modelPreviews[i].SetPosition(-250+i*175, 45)
            else:
                self.modelPreviews[i].SetPosition(-250+(i-4)*175, 250)
            
            self.modelPreviews[i].SetRenderTarget(self.indexList[i])
        
            renderTarget.SetBackground(self.indexList[i], "d:/ymir work/ui/game/render/preview_back.tga")
            renderTarget.SetVisibility(self.indexList[i], True)
            renderTarget.ResetModel(self.indexList[i])
            renderTarget.SelectModel(self.indexList[i], i)
            renderTarget.Zoom(self.indexList[i], -15)
            self.modelPreviews[i].Show()

        self.hairBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbgmin.png", 200, 462)

        self.hairEditline = ui.EditLine()
        self.hairEditline.SetParent(self.hairBG)
        self.hairEditline.SetSize(100, 100)
        self.hairEditline.SetPosition(4, 4)
        self.hairEditline.SetMax(6)
        self.hairEditline.SetLimitWidth(100)
        self.hairEditline.SetMultiLine()
        self.hairEditline.SetText("")
        self.hairEditline.SetOverlayText("Hair Vnum")
        self.hairEditline.Show()

        self.bodyBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbgmin.png", 300, 462)

        self.bodyBGEditline = ui.EditLine()
        self.bodyBGEditline.SetParent(self.bodyBG)
        self.bodyBGEditline.SetSize(100, 100)
        self.bodyBGEditline.SetPosition(4, 4)
        self.bodyBGEditline.SetMax(6)
        self.bodyBGEditline.SetLimitWidth(100)
        self.bodyBGEditline.SetMultiLine()
        self.bodyBGEditline.SetText("")
        self.bodyBGEditline.SetOverlayText("Body Vnum")
        self.bodyBGEditline.Show()

        self.WeaponBG = ui.MakeImageBox(self, "offlineshop/lightwork/searchshop/searchbgmin.png", 400, 462)

        self.WeaponBGEditline = ui.EditLine()
        self.WeaponBGEditline.SetParent(self.WeaponBG)
        self.WeaponBGEditline.SetSize(100, 100)
        self.WeaponBGEditline.SetPosition(4, 4)
        self.WeaponBGEditline.SetMax(6)
        self.WeaponBGEditline.SetLimitWidth(100)
        self.WeaponBGEditline.SetMultiLine()
        self.WeaponBGEditline.SetText("")
        self.WeaponBGEditline.SetOverlayText("Weapons Vnum")
        self.WeaponBGEditline.Show()

        self.button = ui.Button()
        self.button.SetParent(self)
        self.button.SetPosition(500, 462)
        self.button.SetUpVisual(PATH_ROOT + "btn_filter_norm.png")
        self.button.SetOverVisual(PATH_ROOT + "btn_filter_hover.png")
        self.button.SetDownVisual(PATH_ROOT + "btn_filter_down.png")
        self.button.SetText("Dene")
        self.button.SetEvent(self.ConfirmButton)	
        self.button.Show()

    def ConfirmButton(self):
        import chat
        for index, model in enumerate(self.modelPreviews):
            model.SetRenderTarget(self.indexList[index])
        
            if len(self.hairEditline.GetText()):
                renderTarget.SetHair(self.indexList[index], int(self.hairEditline.GetText()))
                (V3Eye, V3Target) = GetCharTypeHairCamera(index)
                if len(V3Eye) and len(V3Target):
                    renderTarget.SetModelV3Eye(self.indexList[index], *V3Eye)
                    renderTarget.SetModelV3Target(self.indexList[index], *V3Target)
                    # chat.AppendChat(1, "I did it %d" % index)

            if len(self.bodyBGEditline.GetText()):
                renderTarget.SetArmor(self.indexList[index],int(self.bodyBGEditline.GetText()))
            if len(self.WeaponBGEditline.GetText()):
                renderTarget.SetWeapon(self.indexList[index], int(self.WeaponBGEditline.GetText()))

    def Open(self):
        self.Show()
    
    def Close(self):
        self.Hide()