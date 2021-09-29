;~ Import ctrl list view click item function
#include <GuiListView.au3>

;~ Start hap42
run("C:\E20-II\HAP42\CODE\hap42.exe")
;~ waits for hap42 to open
WinWaitActive("[Class:ThunderRT6FormDC]")
;~ Click thru splash screen
;~ to do: detect open project screen and handle it
ControlClick("[Class:ThunderRT6FormDC]", "", "ThunderRT6CommandButton2")
;~ focuses main window
WinActivate("[Class:ThunderRT6FormDC]")
$listhandler = ControlGetHandle("[Class:ThunderRT6FormDC]", "", "ListViewWndClass1")
;~ clicks to open spaces
_GUICtrlListView_ClickItem($listhandler, 1, "left", False, 2)
;~ Opens new space entry
_GUICtrlListView_ClickItem($listhandler, 0, "left", False, 2)