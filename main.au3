;~ Import ctrl list view click item function
#include <GuiListView.au3>
#include <GuiTreeView.au3>
#include <.\autoit_Json\Json.au3>

;~ todo: json decoding
;~ $file = @ScriptDir & "\json_test.json"
;~ $jsonObject = json_decode_from_file($file)

;~ Variables that are recieved from python caller and then defined
$Command = ''
$Arg = ''
$main_form = '[Class:ThunderRT6FormDC]'

If $CmdLine[0] > 0 Then
    If $CmdLine[1] <> @ScriptName Then
        $Command = $CmdLine[1]
        $Arg = $CmdLine[2]
    EndIf
EndIf

;~ main($Command)
startHAP()
openWalls()
openWindows()
openDoors()
openSpaces()
insertSpaceInfo()

;~ Main execution of functions
Func main($CommandInput)
    if $CommandInput == "startHAP" Then
        startHAP()
    EndIf
EndFunc

;~ Start the HAP42 software and sets focus on the window
Func startHAP()
    run("C:\E20-II\HAP42\CODE\hap42.exe")
    WinWaitActive($main_form)
    ;~ to do: detect open project screen and handle it
    ControlClick($main_form, "", "ThunderRT6CommandButton2")
    WinActivate($main_form)
EndFunc

Func openTreeItem($item)
    $treeHandler = ControlGetHandle($main_form, "", "TreeViewWndClass1")
    $treeItem = _GUICtrlTreeView_FindItem($treeHandler, $item)
    _GUICtrlTreeView_ClickItem($treeHandler, $treeItem, "left", False, 1)
EndFunc

Func openSpaces()
    openTreeItem("Spaces")
    $listhandler = ControlGetHandle($main_form, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "left", False, 2)
EndFunc

;~ Atm just creates a default wall
Func openWalls()
    openTreeItem("Walls")
    $listhandler = ControlGetHandle($main_form, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "left", False, 2)
    WinWaitActive("Wall Properties")
    ControlClick($main_form, "", "ThunderRT6CommandButton2", "left", 1)
    WinWaitActive("HAP42")
EndFunc

;~ Atm just creates a default window
Func openWindows()
    openTreeItem("Windows")
    $listhandler = ControlGetHandle($main_form, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "left", False, 2)
    WinWaitActive("Window Properties")
    ControlClick($main_form, "", "ThunderRT6CommandButton2", "left", 1)
    WinWaitActive("HAP42")
EndFunc

;~ Atm just creates a default door
Func openDoors()
    openTreeItem("Doors")
    $listhandler = ControlGetHandle($main_form, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "left", False, 2)
    WinWaitActive("Door Properties")
    ControlClick($main_form, "", "ThunderRT6CommandButton2", "left", 1)
    WinWaitActive("HAP42")
EndFunc

Func insertSpaceInfo()
    WinWaitActive("Space Properties")
    ;~ General
    ControlSetText($main_form, "", "ThunderRT6TextBox97", "placeholder")
    ControlSetText($main_form, "", "ThunderRT6TextBox96", 12)
    ControlSetText($main_form, "", "ThunderRT6TextBox95", 12)

    ;~ Internals
    ControlSetText($main_form, "", "ThunderRT6TextBox87", 12)

    ;~ Walls, Windows, Doors
    ControlClick($main_form, "", "SSTabCtlWndClass1", "left", 1, 170, 10)
    $occ = ControlCommand($main_form, "", "ThunderRT6ComboBox20", "FindString", "N")
    ControlCommand($main_form, "", "ThunderRT6ComboBox20", "SetCurrentSelection", $occ)
    ControlSetText($main_form, "", "ThunderRT6TextBox82", 12)
EndFunc