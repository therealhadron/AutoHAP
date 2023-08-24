;~ Import ctrl list view click item function
#include <GuiListView.au3>
#include <GuiTreeView.au3>
#include <GUIButton.au3>
#include <.\autoit_Json\Json.au3>

Opt("MouseCoordMode", 0)
;~ todo: json decoding
$file = @ScriptDir & "\final_data.json"
$jsonObject = json_decode_from_file($file)
$spaceObject = Json_ObjGet($jsonObject, ".Spaces")

Global Const $THUNDER_COMBO_BOX = "ThunderRT6ComboBox"
Global Const $THUNDER_TEXT_BOX = "ThunderRT6TextBox"
Global Const $MAIN_FORM = '[Class:ThunderRT6FormDC]'

;~ main($Command)

main()

;~ Main execution of functions
Func main()
    startHAP()

	Sleep(2000)

    openWalls()
    openWindows()
    openDoors()
    openRoofs()
    openSchedule()

    openSpaces()
    WinActivate($MAIN_FORM)

	$spaceObject = Json_Get($jsonObject, ".Spaces[0]")

    _insert_space_general(Json_Get($spaceObject, '.General.Name'), _
						Json_Get($spaceObject, '.General.Floor_Area'), _
						Json_Get($spaceObject, '.General.Avg_Ceiling_Height'))
    _insert_space_internals(Json_Get($spaceObject, '.Internals.Electrical_Equipment.Wattage_Units'), _
							Json_Get($spaceObject, '.Internals.Electrical_Equipment.Wattage'), _
							Json_Get($spaceObject, '.Internals.Electrical_Equipment.Schedule'), _
							Json_Get($spaceObject, '.Internals.People.Activity_Level'), _
							Json_Get($spaceObject, '.Internals.People.Occupancy'), _
							Json_Get($spaceObject, '.Internals.People.Schedule'))
    _insert_space_walls_windows_doors(0)
    ;~ _insert_space_roofs_skylights(0)
    ;~ _insert_space_infiltration(0)
    ;~ _insert_space_floors(0)
    ;~ _insert_space_partitions(0)
EndFunc

;~ ===================
;~ General
;~ ===================
Func _insert_space_general($space_name, $space_area, $space_avg_height)
    ControlSetText($MAIN_FORM, "", "ThunderRT6TextBox97", $space_name)
    ControlSetText($MAIN_FORM, "", "ThunderRT6TextBox96", $space_area)
    ControlSetText($MAIN_FORM, "", "ThunderRT6TextBox95", $space_avg_height)
EndFunc

;~ ===================
;~ Internals
;~ ===================
Func _insert_space_internals($electric_unit, $electric_value, $electric_schedule, $people_activity, $people_value, $people_schedule)
    ControlClick($MAIN_FORM, "", "SSTabCtlWndClass1", "primary", 1, 80, 10)
    ;~ Electrical Equipment
    ;~ W/ft² or Watts
    $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 26, "FindString", $electric_unit)
    ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 26, "SetCurrentSelection", $occ)
    ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 86, $electric_value)
    $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 27, "FindString", $electric_schedule)
    ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 27, "SetCurrentSelection", $occ)

    ;~ People
    ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 87, $people_value)
    $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 28, "FindString", $people_activity)
    ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 28, "SetCurrentSelection", $occ)
    $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 30, "FindString", $people_schedule)
    ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 30, "SetCurrentSelection", $occ)

    ;~ HAP wants actual mouse input to validate schedule
    ControlClick($MAIN_FORM, "", $THUNDER_COMBO_BOX & 27)
    ControlClick($MAIN_FORM, "", $THUNDER_COMBO_BOX & 30)
EndFunc

;~ ===================
;~ Walls, Windows, Doors
;~ ===================
Func _insert_space_walls_windows_doors($index)
    ControlClick($MAIN_FORM, "", "SSTabCtlWndClass1", "primary", 1, 170, 10)
    Sleep(500)
    $directionCount = 20
    $areaCount = 82
    $windowCount = 51
    $doorCount = 80
    For $i = 0 To 7 Step 1

		$exposure = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $i & '].Exposure')
		$wall_area = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $i & '].Wall_Area')
		$window = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $i & '].Window')
		$door = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $i & '].Door')
		$wall_assembly = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $i & '].Wall_Assembly')
		$window_assembly = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $i & '].Window_Assembly')
		$door_assembly = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $i & '].Door_Assembly')

        $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & $directionCount, "FindString", $exposure)
        ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & $directionCount, "SetCurrentSelection", $occ)

        ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $areaCount, $wall_area)

        ;~ Vaildates windows
        ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $windowCount, $window)

        ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $doorCount, $door)

        $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 12, "FindString", $wall_assembly)
        ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 12, "SetCurrentSelection", $occ)
        $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 11, "FindString", $window_assembly)
        ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 11, "SetCurrentSelection", $occ)
        $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 7, "FindString", $door_assembly)
        ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 7, "SetCurrentSelection", $occ)

        $directionCount = $directionCount - 1
        $areaCount = $areaCount - 3
        $windowCount = $windowCount + 1
        $doorCount = $doorCount - 3
    Next

    ;~ HAP requires clicks in each area textbox after all inputs before being able to verify data
    $areaCount = 82
    $windowCount = 51
    $doorCount = 80
    For $i = 0 To 7 Step 1
        ControlClick($MAIN_FORM, "", $THUNDER_TEXT_BOX & $areaCount, "primary", 1)

        ControlClick($MAIN_FORM, "", $THUNDER_TEXT_BOX & $windowCount, "primary", 1, 20, 10)
        ControlClick($MAIN_FORM, "", "UpDownWndClass2", "primary", 1, 8, 5)
        ControlClick($MAIN_FORM, "", "UpDownWndClass2", "primary", 1, 8, 15)

        ControlClick($MAIN_FORM, "", $THUNDER_TEXT_BOX & $doorCount, "primary", 1, 20, 10)
        ControlClick($MAIN_FORM, "", "UpDownWndClass2", "primary", 1, 8, 5)
        ControlClick($MAIN_FORM, "", "UpDownWndClass2", "primary", 1, 8, 15)

        $areaCount = $areaCount - 3
        $windowCount = $windowCount + 1
        $doorCount = $doorCount - 3
    Next
EndFunc

;~ ===================
;~ Roofs and skylights
;~ ===================
Func _insert_space_roofs_skylights($index)
    Local $Array = _RS_get_json_data($index)
    ControlClick($MAIN_FORM, "", "SSTabCtlWndClass1", "primary", 1, 270, 10)

    ;~ Inital set has numbers that are non-sequential
    $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 6, "FindString", $Array[0][0])
    ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 6, "SetCurrentSelection", $occ)

    ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 49, $Array[0][1])
    ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 50, $Array[0][2])
    ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 48, $Array[0][3])

    $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 5, "FindString", $Array[0][4])
    ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 5, "SetCurrentSelection", $occ)
    $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 4, "FindString", $Array[0][5])
    ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 4, "SetCurrentSelection", $occ)

    ;~ Rest of textboxes and comboboxes are sequential
    $directionCount = 3
    $areaCount = 41
    $slopeCount = 46
    $skylightCount = 47

    For $i = 3 To 1 Step -1
        $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & $directionCount, "FindString", $Array[$i][0])
        ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & $directionCount, "SetCurrentSelection", $occ)

        ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $areaCount, $Array[$i][1])
        ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $slopeCount, $Array[$i][2])
        ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $skylightCount, $Array[$i][3])

        $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 5, "FindString", $Array[$i][4])
        ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 5, "SetCurrentSelection", $occ)
        $occ = ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 4, "FindString", $Array[$i][5])
        ControlCommand($MAIN_FORM, "", $THUNDER_COMBO_BOX & 4, "SetCurrentSelection", $occ)

        $directionCount = $directionCount - 1
        $areaCount = $areaCount - 1
        $slopeCount = $slopeCount - 2
        $skylightCount = $skylightCount - 2
    Next
EndFunc

;~ ===================
;~ Infiltration
;~ ===================
;~ WIP
Func _insert_space_infiltration($index)
    ControlClick($MAIN_FORM, "", "SSTabCtlWndClass1", "primary", 1, 350, 10)

    ;~ todo: if no walls then no infiltration
    ;~ todo: Speicify CFM, CFM/ft^2, or ACH

    ;~ Design Cooling
    ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 2, Json_Get($spaceObject, '.Infiltration[' & $index & '].Design_Cooling.CFM'))
    ;~ ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 5, 0.15)
    ;~ ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 8, 0.15)
    ;~ Design Heating
    ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 1, Json_Get($spaceObject, '.Infiltration[' & $index & '].Design_Heating.CFM'))
    ;~ ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 6, 0.15)
    ;~ ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 9, 0.15)
    ;~ Energy analysis
    ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 3, Json_Get($spaceObject, '.Infiltration[' & $index & '].Energy_Analysis.CFM'))
    ;~ ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 4, 0.15)
    ;~ ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & 7, 0.15)

    If Json_Get($spaceObject, '.Infiltration[' & $index & '].Infiltration_Occurs.Only_When_Fan_Off_All_Hours') == "Only When Fan Off" Then
        $fanCond = 1
    ElseIf Json_Get($spaceObject, '.Infiltration[' & $index & '].Infiltration_Occurs.Only_When_Fan_Off_All_Hours') == "All Hours" Then
        $fanCond = 2
    Else
        ;~ Todo: Throw error
        Exit
    EndIf

    ControlCommand($MAIN_FORM, "", "ThunderRT6OptionButton" & $fanCond, "Check")
EndFunc

;~ ===================
;~ Floors
;~ ===================
Func _insert_space_floors($index)
    ControlClick($MAIN_FORM, "", "SSTabCtlWndClass1", "primary", 1, 400, 10)

    Local Enum $efloor_above_conditioned_space = 10, $efloor_above_unconditioned_space = 9, $efloor_on_grade = 8, $efloor_below_grade = 7

    if Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Above_Conditioned_Space.TF') Then
        $floorCond = $efloor_above_conditioned_space
    ElseIf Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Above_Unconditioned_Space.TF') Then
        $floorCond = $efloor_above_unconditioned_space
    ElseIf Json_Get($spaceObject, '.Floors[' & $index & '].Floor_On_Grade.TF') Then
        $floorCond = $efloor_on_grade
    ElseIf Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Below_Grade.TF') Then
        $floorCond = $efloor_below_grade
    Else
        ;~ Todo: throw error
    EndIf

    ;~ Selects the correct radio option
    ControlCommand($MAIN_FORM, "", "ThunderRT6OptionButton" & $floorCond, "Check")
    Sleep(25)

    ;~ No need to check for $efloor_above_conditioned since there wont be any additional inputs
    Switch $floorCond
        Case $efloor_above_unconditioned_space
            Local $Array[6]
            $Array[0] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Above_Unconditioned_Space.Floor_Area')
            $Array[1] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Above_Unconditioned_Space.Floor_Uvalue')
            $Array[2] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Above_Unconditioned_Space.Unconditioned_Space_Max_Temp')
            $Array[3] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Above_Unconditioned_Space.Ambient_At_Space_Max_Temp')
            $Array[4] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Above_Unconditioned_Space.Unconditioned_Space_Min_Temp')
            $Array[5] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Above_Unconditioned_Space.Ambient_At_Space_Min_Temp')
            $j = 38 ;~ Instance value of first textbox
            for $i in $Array
                ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $j, $i)
                $j = $j - 1
            Next
        Case $efloor_on_grade
            Local $Array[4]
            $Array[0] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_On_Grade.Floor_Area')
            $Array[1] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_On_Grade.Floor_Uvalue')
            $Array[2] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_On_Grade.Exposed_Perimeter')
            $Array[3] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_On_Grade.Edge_Insulation_RValue')
            $j = 32 ;~ Instance value of first textbox
            for $i in $Array
                ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $j, $i)
                $j = $j - 1
            Next
        Case $efloor_below_grade
            Local $Array[7]
            $Array[0] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Below_Grade.Floor_Area')
            $Array[1] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Below_Grade.Exposed_Perimeter')
            $Array[2] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Below_Grade.Floor_Uvalue')
            $Array[3] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Below_Grade.Floor_Depth')
            $Array[4] = Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Below_Grade.Basement_Wall_Uvalue')
            $Array[5] =  Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Below_Grade.Wall_Insulation_Rvalue')
            $Array[6] =  Json_Get($spaceObject, '.Floors[' & $index & '].Floor_Below_Grade.Depth_Of_Wall_Insulation')
            $j = 28 ;~ Instance value of first textbox
            for $i in $Array
                ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $j, $i)
                $j = $j - 1
            Next
    EndSwitch
EndFunc

;~ ===================
;~ Partitions
;~ ===================
Func _insert_space_partitions($index)
    ControlClick($MAIN_FORM, "", "SSTabCtlWndClass1", "primary", 1, 450, 10)

    If Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_1.Ceiling_Wall') == "Ceiling" Then
        $partition1Cond = 5
    ElseIf Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_1.Ceiling_Wall') == "Wall" Then
        $partition1Cond = 6
    Else
        ;~ Todo: throw error
        Exit
    EndIf

    If Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_2.Ceiling_Wall') == "Ceiling" Then
        $partition2Cond = 4
    ElseIf Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_2.Ceiling_Wall') == "Wall" Then
        $partition2Cond = 3
    Else
        ;~ Todo: throw error
        Exit
    EndIf

    Local $partition1Array[6]
    Local $partition2Array[6]

    $partition1Array[0] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_1.Area')
    $partition1Array[1] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_1.Uvalue')
    $partition1Array[2] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_1.Unconditioned_Space_Max_Temp')
    $partition1Array[3] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_1.Ambient_At_Space_Max_Temp')
    $partition1Array[4] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_1.Unconditioned_Space_Min_Temp')
    $partition1Array[5] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_1.Ambient_At_Space_Min_Temp')

    $partition2Array[0] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_2.Area')
    $partition2Array[1] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_2.Uvalue')
    $partition2Array[2] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_2.Unconditioned_Space_Max_Temp')
    $partition2Array[3] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_2.Ambient_At_Space_Max_Temp')
    $partition2Array[4] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_2.Unconditioned_Space_Min_Temp')
    $partition2Array[5] = Json_Get($spaceObject, '.Partitions[' & $index & '].Partition_2.Ambient_At_Space_Min_Temp')

    ControlCommand($MAIN_FORM, "", "ThunderRT6OptionButton" & $partition1Cond, "Check")
    ControlCommand($MAIN_FORM, "", "ThunderRT6OptionButton" & $partition2Cond, "Check")

    $partition1Count = 16
    $partition2Count = 10
    for $i = 0 To 5 Step 1
        ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $partition1Count, $partition1Array[$i])
        ControlSetText($MAIN_FORM, "", $THUNDER_TEXT_BOX & $partition2Count, $partition2Array[$i])
        $partition1Count = $partition1Count + 1
        $partition2Count = $partition2Count + 1
    Next
EndFunc

;~ Inserts all the space data
Func insertSpaceInfo()
    WinWaitActive("Space Properties")

    ;~ Save space
    ControlClick($MAIN_FORM, "", "ThunderRT6CommandButton15", "primary", 1)
    WinWaitActive("HAP42")
EndFunc

;~ Start the HAP42 software and sets focus on the window
Func startHAP()
    run("C:\E20-II\HAP42\CODE\hap42.exe")
    WinWaitActive($MAIN_FORM)
    ;~ to do: detect open project screen and handle it
    ControlClick($MAIN_FORM, "", "ThunderRT6CommandButton2")
    WinActivate($MAIN_FORM)
EndFunc

Func openTreeItem($item)
    $treeHandler = ControlGetHandle($MAIN_FORM, "", "TreeViewWndClass1")
    $treeItem = _GUICtrlTreeView_FindItem($treeHandler, $item)
    _GUICtrlTreeView_ClickItem($treeHandler, $treeItem, "primary", False, 1)
EndFunc

Func openSpaces()
    openTreeItem("Spaces")
    $listhandler = ControlGetHandle($MAIN_FORM, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "primary", False, 2)
EndFunc

;~ Atm just creates a default wall
Func openWalls()
    openTreeItem("Walls")
    $listhandler = ControlGetHandle($MAIN_FORM, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "primary", False, 2)
    WinWaitActive("Wall Properties")
    ControlClick($MAIN_FORM, "", "ThunderRT6CommandButton2", "primary", 1)
    WinWaitActive("HAP42")
EndFunc

;~ Atm just creates a default window
Func openWindows()
    openTreeItem("Windows")
    $listhandler = ControlGetHandle($MAIN_FORM, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "primary", False, 2)
    WinWaitActive("Window Properties")
    ControlClick($MAIN_FORM, "", "ThunderRT6CommandButton2", "primary", 1)
    WinWaitActive("HAP42")
EndFunc

;~ Atm just creates a default door
Func openDoors()
    openTreeItem("Doors")
    $listhandler = ControlGetHandle($MAIN_FORM, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "primary", False, 2)
    WinWaitActive("Door Properties")
    ControlClick($MAIN_FORM, "", "ThunderRT6CommandButton2", "primary", 1)
    WinWaitActive("HAP42")
EndFunc

;~ Atm just creates a default roof
Func openRoofs()
    openTreeItem("Roofs")
    $listhandler = ControlGetHandle($MAIN_FORM, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "primary", False, 2)
    WinWaitActive("Roof Properties")
    ControlClick($MAIN_FORM, "", "ThunderRT6CommandButton2", "primary", 1)
    WinWaitActive("HAP42")
EndFunc

;~ Atm just creates a default schedule
Func openSchedule()
    openTreeItem("Schedules")
    $listhandler = ControlGetHandle($MAIN_FORM, "", "ListViewWndClass1")
    _GUICtrlListView_ClickItem($listhandler, 0, "primary", False, 2)
    WinWaitActive("Schedule Properties")
    ControlClick($MAIN_FORM, "", "ThunderRT6CommandButton3", "primary", 1)
    WinWaitActive("HAP42")
EndFunc

Func _WWD_get_json_data($index)
    Local $WWDArray[8][7]
    For $i = 1 to 8 step 1
        $WWDArray[$i-1][0] = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $index & '].' & $i & '.Exposure')
        $WWDArray[$i-1][1] = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $index & '].' & $i & '.Wall_Area')
        $WWDArray[$i-1][2] = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $index & '].' & $i & '.Window')
        $WWDArray[$i-1][3] = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $index & '].' & $i & '.Door')

        $WWDArray[$i-1][4] = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $index & '].Construction_Types.Wall')
        $WWDArray[$i-1][5] = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $index & '].Construction_Types.Window')
        $WWDArray[$i-1][6] = Json_Get($spaceObject, '.Walls_Windows_Doors[' & $index & '].Construction_Types.Door')
    Next
    Return $WWDArray
EndFunc

Func _RS_get_json_data($index)
    Local $RSArray[4][6]
    For $i = 1 to 4 step 1
        $RSArray[$i-1][0] = Json_Get($spaceObject, '.Roofs_Skylights[' & $index & '].' & $i & '.Exposure')
        $RSArray[$i-1][1] = Json_Get($spaceObject, '.Roofs_Skylights[' & $index & '].' & $i & '.Roof_Area')
        $RSArray[$i-1][2] = Json_Get($spaceObject, '.Roofs_Skylights[' & $index & '].' & $i & '.Roof_Slope')
        $RSArray[$i-1][3] = Json_Get($spaceObject, '.Roofs_Skylights[' & $index & '].' & $i & '.Skylight')

        $RSArray[$i-1][4] = Json_Get($spaceObject, '.Roofs_Skylights[' & $index & '].Construction_Types.Roof')
        $RSArray[$i-1][5] = Json_Get($spaceObject, '.Roofs_Skylights[' & $index & '].Construction_Types.Skylight')
    Next
    Return $RSArray
EndFunc