---
name: "AutoIt v3"
description: "Windows GUI 自動化腳本語言指南，專為 Windows GUI 自動化與通用腳本設計。涵蓋 XP 兼容性、核心指令集、環境建置與範例導向實踐。"
tags: ["automation", "windows", "scripting", "legacy-system", "autoit"]
version: "1.4"
---
# AutoIt v3 專家指南

**AutoIt v3** 是一款免費、類 BASIC 語法的腳本語言，透過模擬鍵盤按鍵、滑鼠移動及視窗/控制項操作來實現自動化任務。

## 1. 範例全覽（來源：`D:\Autoit\autoit-v3\install\Examples`）

**注意事項：** `_ReadMe_.txt` 指出多數範例僅在英文版 Windows 上可直接運行，非英文版本需調整視窗標題或控制項文字。

### COM 目錄（COM / WMI / ADSI / Office / IE / SAPI）
- `AutoItX-test.au3`：`AutoItX3.Control`，剪貼簿與 ToolTip 操作。
- `ErrorEventTest-ADSI.au3`：ADSI 測試與 COM 錯誤事件處理。
- `ErrorEventTest-WMI.AU3`：WMI 例外觸發，示範 COM Error Handler。
- `EventTest-IE6.au3`：IE COM 事件（`DWebBrowserEvents`）。
- `EventTest-SAPI.au3`：SAPI 語音辨識事件（需 SAPI SDK 5.1）。
- `EventTest-ShellWindows.au3`：Shell 視窗事件監聽。
- `EventTest-WMI.au3`：WMI 非同步事件（`SWbemSink`）。
- `ExcelAutomationTest.au3`：建立 Excel、填表/清除、關閉。
- `ExcelDataTest.AU3`：`ObjGet` 既有 Excel 檔，Range ↔ Array 寫回。
- `ExcelFastTest.au3`：2D 陣列快速填值。
- `ExcelFileTest.au3`：讀取 Excel 內建文件屬性。
- `ExcelGetObjTest.au3`：`ObjGet("", "Excel.Application")` 連線現有 Excel。
- `FileSearchTest.au3`：Excel `FileSearch` 搜尋檔案。
- `getHTMLsource.au3`：WinHTTP 取 HTML 並在 GUI 顯示。
- `Instance-of-IE-test.au3`：透過 `shell.application` 找到 IE 實例。
- `RegExpTest.au3`：`VBScript.RegExp` 正規表示式。
- `RemoteObjCreateTest.au3`：DCOM 遠端 `ObjCreate` 測試。
- `Scriptomatic.au3`：WMI Scriptomatic GUI（產生 WMI 查詢腳本）。
- `ShellStopStartServiceTest.au3`：Shell 介面啟停服務。
- `ShellWindowsTest.au3`：列出已開啟 Shell 視窗。
- `winntgroups.au3`：ADSI WinNT provider 枚舉群組。
- `Wmi-terminate.au3`：WMI 終止程序。
- `WmiDiskTest.au3`：WMI 取得磁碟資訊。
- `wmiexample.AU3`：WMI 取得 CPU 資訊。
- `wmiForInTest.au3`：WMI 列舉服務。
- `WmiGetStringValue.AU3`：`StdRegProv.GetStringValue` (ByRef)。
- `WordTest.au3`：Word 版本/Build 讀取。
- `WscriptFilesys.au3`：`Scripting.FileSystemObject` 目錄大小。
- `wscriptnetwork.au3`：`WScript.Network` 網路磁碟。
- `wscriptshelltest.au3`：`Scripting.FileSystemObject` 檔案資訊。

### GUI\Simple 目錄（基本 GUI）
- `child.au3`：父/子視窗，`GUIGetMsg(1)` 判斷視窗來源。
- `editbox.au3`：簡單 GUI + Edit + OK/Cancel。
- `msgbox_messageloop.au3`：Message Loop 模式。
- `msgbox_onevent.au3`：`GUIOnEventMode` 事件模式。
- `simplecalc.au3`：計算機 UI 配置示範。

### GUI\Advanced 目錄（進階 GUI / GDI+ / IPC）
- `_NamedPipes_Client.au3`：Named Pipes 客戶端 GUI。
- `_NamedPipes_Server.au3`：Named Pipes 伺服端 + Overlapped I/O。
- `AlphaBlend.au3`：分層視窗、Alpha 混合。
- `BMPToJPG.au3`：GDI+ BMP → JPG。
- `Clock.au3`：分層視窗時鐘（GDI+ 畫圖）。
- `contextmenu.au3`：右鍵 Context Menu。
- `dice.au3`：骰子隨機 GUI。
- `Emboss.au3`：螢幕擷取 + 壓印文字。
- `encrypt.au3`：GUI 加/解密（`Crypt.au3`）。
- `enumicons.au3`：EXE/DLL icon 瀏覽器。
- `imagebutton.au3`：Icon 按鈕。
- `menu.au3`：Menu / Recent Files。
- `msgboxwizard.au3`：MsgBox 代碼產生器 + ClipPut。
- `Rotate.au3`：GDI+ 旋轉影像。
- `setlabel.au3`：Combo → Label 更新。
- `ShowPNG.au3`：顯示 PNG。
- `Slicer.au3`：切片/重組影像。
- `sysinfo.au3`：系統資訊 GUI（`@ComputerName` 等巨集）。
- `treeview.au3`：TreeView + 群組顯示/隱藏。
- `Zoom.au3`：影像放大顯示。

### Helpfile 目錄（_WinAPI_* / _Word_*）

**WinAPI 範例（約 437 個）：** 檔名即對應的 WinAPI UDF 函數名稱，`[2]`/`[3]` 表示同函數的變體範例。
- **Get/Set 系列：** `_WinAPI_GetAncestor`, `_WinAPI_GetAsyncKeyState`, `_WinAPI_SetClassLongEx`, `_WinAPI_SetCursorSize`
- **Path / Reg / Shell / Url：** `_WinAPI_PathAddBackslash`, `_WinAPI_RegCreateKey`, `_WinAPI_ShellChangeNotify`, `_WinAPI_UrlCombine`
- **Create / Load / Open / Register：** `_WinAPI_CreateCaret`, `_WinAPI_LoadLibraryEx`, `_WinAPI_OpenFileDlg`, `_WinAPI_RegisterHotKey`
- **Query / Print / Message / String / Color / System / Window：** `_WinAPI_QueryDosDevice`, `_WinAPI_PrintWindow`, `_WinAPI_MessageBoxIndirect`, `_WinAPI_StringLenW`, `_WinAPI_ColorRGBToHLS`, `_WinAPI_SystemParametersInfo`, `_WinAPI_WindowFromPoint`

**索引說明：** 目的與典型用途依函數名稱歸納，實際行為以 AutoIt Help 為準。

#### WinAPI 索引表（函數 → 目的 → 典型用途）

| 函數 | 目的 | 典型用途 |
| :--- | :--- | :--- |
| `_WinAPI_ActivateKeyboardLayout` | 啟用 Keyboard Layout | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_AddClipboardFormatListener` | 新增 Clipboard Format Listener | 剪貼簿監聽/格式管理 |
| `_WinAPI_AddFontMemResourceEx` | 新增 Font Mem Resource | 字型/文字量測/字串處理 |
| `_WinAPI_AddFontResourceEx` | 新增 Font Resource | 字型/文字量測/字串處理 |
| `_WinAPI_AddIconOverlay` | 新增 Icon Overlay | 影像/GDI 物件處理 |
| `_WinAPI_AddIconTransparency` | 新增 Icon Transparency | 影像/GDI 物件處理 |
| `_WinAPI_AdjustBitmap` | 調整 Bitmap | 影像/GDI 物件處理 |
| `_WinAPI_AlphaBlend` | 處理 Alpha Blend | WinAPI 輔助功能 |
| `_WinAPI_AnimateWindow` | 動畫顯示 Window | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_AssocGetPerceivedType` | 取得 Assoc Perceived Type | WinAPI 輔助功能 |
| `_WinAPI_AssocQueryString` | 查詢 Assoc String | 字型/文字量測/字串處理 |
| `_WinAPI_BackupRead` | 讀取 Backup | WinAPI 輔助功能 |
| `_WinAPI_Beep` | 處理 Beep | WinAPI 輔助功能 |
| `_WinAPI_BeginBufferedPaint` | 開始 Buffered Paint | WinAPI 輔助功能 |
| `_WinAPI_BeginPaint` | 開始 Paint | WinAPI 輔助功能 |
| `_WinAPI_BeginPath` | 開始 Path | 路徑字串正規化/解析/組合 |
| `_WinAPI_BeginUpdateResource` | 開始 Update Resource | 資源/模組/Handle 操作 |
| `_WinAPI_BitBlt` | 處理 Bit Blt | WinAPI 輔助功能 |
| `_WinAPI_BrowseForFolderDlg` | 瀏覽 Folder Dialog | UI 對話框/訊息/選單 |
| `_WinAPI_CallWindowProc` | 處理 Call Window Proc | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_CascadeWindows` | 處理 Cascade Windows | WinAPI 輔助功能 |
| `_WinAPI_ClientToScreen` | 轉換 Client 為 Screen | WinAPI 輔助功能 |
| `_WinAPI_ClipCursor` | 處理 Clip Cursor | 影像/GDI 物件處理 |
| `_WinAPI_CLSIDFromProgID` | 由 PROGID 取得 CLSID | WinAPI 輔助功能 |
| `_WinAPI_ColorAdjustLuma` | 調整 Color Luma | WinAPI 輔助功能 |
| `_WinAPI_ColorHLSToRGB` | 轉換 Color HLS 為 RGB | WinAPI 輔助功能 |
| `_WinAPI_ColorRGBToHLS` | 轉換 Color RGB 為 HLS | WinAPI 輔助功能 |
| `_WinAPI_CommandLineToArgv` | 轉換 Command Line 為 Argv | WinAPI 輔助功能 |
| `_WinAPI_CompareString` | 比較 String | 字型/文字量測/字串處理 |
| `_WinAPI_CompressBitmapBits` | 壓縮 Bitmap Bits | 影像/GDI 物件處理 |
| `_WinAPI_CompressBuffer` | 壓縮 Buffer | WinAPI 輔助功能 |
| `_WinAPI_ComputeCrc32` | 計算 Crc 32 | WinAPI 輔助功能 |
| `_WinAPI_CopyFileEx` | 複製 File | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_CopyStruct` | 複製 Struct | WinAPI 輔助功能 |
| `_WinAPI_Create32BitHBITMAP` | 建立 32 Bit HBITMAP | 影像/GDI 物件處理 |
| `_WinAPI_CreateANDBitmap` | 建立 AND Bitmap | 影像/GDI 物件處理 |
| `_WinAPI_CreateCaret` | 建立 Caret | WinAPI 輔助功能 |
| `_WinAPI_CreateColorAdjustment` | 建立 Color Adjustment | WinAPI 輔助功能 |
| `_WinAPI_CreateDesktop` | 建立 Desktop | WinAPI 輔助功能 |
| `_WinAPI_CreateDIB` | 建立 DIB | 影像/GDI 物件處理 |
| `_WinAPI_CreateDIBSection` | 建立 DIB Section | 影像/GDI 物件處理 |
| `_WinAPI_CreateEnhMetaFile` | 建立 Enh Meta File | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_CreateFile` | 建立 File | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_CreateFileMapping` | 建立 File Mapping | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_CreateGUID` | 建立 GUID | WinAPI 輔助功能 |
| `_WinAPI_CreateHardLink` | 建立 Hard Link | WinAPI 輔助功能 |
| `_WinAPI_CreateIcon` | 建立 Icon | 影像/GDI 物件處理 |
| `_WinAPI_CreateIconFromResourceEx` | 建立 Icon From Resource | 影像/GDI 物件處理 |
| `_WinAPI_CreateIconIndirect` | 建立 Icon Indirect | 影像/GDI 物件處理 |
| `_WinAPI_CreateJobObject` | 建立 Job Object | WinAPI 輔助功能 |
| `_WinAPI_CreateMRUList` | 建立 MRU List | WinAPI 輔助功能 |
| `_WinAPI_CreateObjectID` | 建立 Object ID | WinAPI 輔助功能 |
| `_WinAPI_CreatePen` | 建立 Pen | WinAPI 輔助功能 |
| `_WinAPI_CreatePolygonRgn` | 建立 Polygon Rgn | WinAPI 輔助功能 |
| `_WinAPI_CreateProcess` | 建立 Process | 處理程序資訊/控制 |
| `_WinAPI_CreateRectRgn` | 建立 Rect Rgn | WinAPI 輔助功能 |
| `_WinAPI_CreateSemaphore` | 建立 Semaphore | 同步/事件/等待 |
| `_WinAPI_CreateStreamOnHGlobal` | 建立 Stream On H Global | WinAPI 輔助功能 |
| `_WinAPI_CreateString` | 建立 String | 字型/文字量測/字串處理 |
| `_WinAPI_CreateSymbolicLink` | 建立 Symbolic Link | WinAPI 輔助功能 |
| `_WinAPI_CreateTransform` | 建立 Transform | WinAPI 輔助功能 |
| `_WinAPI_DefineDosDevice` | 處理 Define Dos Device | WinAPI 輔助功能 |
| `_WinAPI_DefSubclassProc` | 處理 Def Subclass Proc | 事件/訊息掛鉤與通知 |
| `_WinAPI_DisplayStruct` | 處理 Display Struct | WinAPI 輔助功能 |
| `_WinAPI_DllGetVersion` | 取得 Dll Version | WinAPI 輔助功能 |
| `_WinAPI_DragAcceptFiles` | 處理 Drag Accept Files | WinAPI 輔助功能 |
| `_WinAPI_DrawAnimatedRects` | 繪製 Animated Rects | WinAPI 輔助功能 |
| `_WinAPI_DrawBitmap` | 繪製 Bitmap | 影像/GDI 物件處理 |
| `_WinAPI_DrawShadowText` | 繪製 Shadow Text | 字型/文字量測/字串處理 |
| `_WinAPI_DrawThemeText` | 繪製 Theme Text | 字型/文字量測/字串處理 |
| `_WinAPI_DrawThemeTextEx` | 繪製 Theme Text | 字型/文字量測/字串處理 |
| `_WinAPI_DuplicateHandle` | 處理 Duplicate Handle | 資源/模組/Handle 操作 |
| `_WinAPI_DwmEnableBlurBehindWindow` | 啟用 DWM Blur Behind Window | DWM 視窗外觀/縮圖/屬性 |
| `_WinAPI_DwmExtendFrameIntoClientArea` | 處理 DWM Extend Frame Into Client Area | DWM 視窗外觀/縮圖/屬性 |
| `_WinAPI_DwmGetColorizationColor` | 取得 DWM Colorization Color | DWM 視窗外觀/縮圖/屬性 |
| `_WinAPI_DwmGetWindowAttribute` | 取得 DWM Window Attribute | DWM 視窗外觀/縮圖/屬性 |
| `_WinAPI_DwmIsCompositionEnabled` | 判斷 DWM Composition Enabled | DWM 視窗外觀/縮圖/屬性 |
| `_WinAPI_DwmRegisterThumbnail` | 註冊 DWM Thumbnail | DWM 視窗外觀/縮圖/屬性 |
| `_WinAPI_DwmSetIconicThumbnail` | 設定 DWM Iconic Thumbnail | DWM 視窗外觀/縮圖/屬性 |
| `_WinAPI_DwmSetWindowAttribute` | 設定 DWM Window Attribute | DWM 視窗外觀/縮圖/屬性 |
| `_WinAPI_DWordToInt` | 轉換 DWORD 為 Int | WinAPI 輔助功能 |
| `_WinAPI_EmptyWorkingSet` | 設定 Empty Working | WinAPI 輔助功能 |
| `_WinAPI_EncryptFile` | 加密 File | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_EndPaint` | 結束 Paint | WinAPI 輔助功能 |
| `_WinAPI_EnumChildProcess` | 列舉 Child Process | 處理程序資訊/控制 |
| `_WinAPI_EnumChildWindows` | 列舉 Child Windows | WinAPI 輔助功能 |
| `_WinAPI_EnumDesktops` | 列舉 Desktops | WinAPI 輔助功能 |
| `_WinAPI_EnumDesktopWindows` | 列舉 Desktop Windows | WinAPI 輔助功能 |
| `_WinAPI_EnumDeviceDrivers` | 列舉 Device Drivers | WinAPI 輔助功能 |
| `_WinAPI_EnumDisplayDevices` | 列舉 Display Devices | WinAPI 輔助功能 |
| `_WinAPI_EnumDisplayMonitors` | 列舉 Display Monitors | WinAPI 輔助功能 |
| `_WinAPI_EnumDisplaySettings` | 列舉 Display Settings | WinAPI 輔助功能 |
| `_WinAPI_EnumDllProc` | 列舉 Dll Proc | WinAPI 輔助功能 |
| `_WinAPI_EnumFiles` | 列舉 Files | WinAPI 輔助功能 |
| `_WinAPI_EnumFileStreams` | 列舉 File Streams | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_EnumFontFamilies` | 列舉 Font Families | 字型/文字量測/字串處理 |
| `_WinAPI_EnumPageFiles` | 列舉 Page Files | WinAPI 輔助功能 |
| `_WinAPI_EnumProcessHandles` | 列舉 Process Handles | 處理程序資訊/控制 |
| `_WinAPI_EnumProcessModules` | 列舉 Process Modules | 處理程序資訊/控制 |
| `_WinAPI_EnumProcessWindows` | 列舉 Process Windows | 處理程序資訊/控制 |
| `_WinAPI_EnumRawInputDevices` | 列舉 Raw Input Devices | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_EnumResourceLanguages` | 列舉 Resource Languages | 資源/模組/Handle 操作 |
| `_WinAPI_EnumResourceNames` | 列舉 Resource Names | 資源/模組/Handle 操作 |
| `_WinAPI_EnumResourceTypes` | 列舉 Resource Types | 資源/模組/Handle 操作 |
| `_WinAPI_EnumSystemGeoID` | 列舉 System Geo ID | WinAPI 輔助功能 |
| `_WinAPI_EnumSystemLocales` | 列舉 System Locales | WinAPI 輔助功能 |
| `_WinAPI_EnumUILanguages` | 列舉 UI Languages | WinAPI 輔助功能 |
| `_WinAPI_EnumWindows` | 列舉 Windows | WinAPI 輔助功能 |
| `_WinAPI_EnumWindowsPopup` | 列舉 Windows Popup | WinAPI 輔助功能 |
| `_WinAPI_EnumWindowStations` | 列舉 Window Stations | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_EnumWindowsTop` | 列舉 Windows Top | WinAPI 輔助功能 |
| `_WinAPI_EqualMemory` | 處理 Equal Memory | WinAPI 輔助功能 |
| `_WinAPI_ExpandEnvironmentStrings` | 展開 Environment Strings | WinAPI 輔助功能 |
| `_WinAPI_ExtCreatePen` | 建立 Ext Pen | WinAPI 輔助功能 |
| `_WinAPI_ExtractIconEx` | 擷取 Icon | 影像/GDI 物件處理 |
| `_WinAPI_FileExists` | 處理 File Exists | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_FileIconInit` | 處理 File Icon Init | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_FileInUse` | 處理 File In Use | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_FindExecutable` | 搜尋 Executable | WinAPI 輔助功能 |
| `_WinAPI_FindFirstChangeNotification` | 搜尋 First Change Notification | WinAPI 輔助功能 |
| `_WinAPI_FindFirstFile` | 搜尋 First File | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_FindFirstFileName` | 搜尋 First File Name | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_FindFirstStream` | 搜尋 First Stream | WinAPI 輔助功能 |
| `_WinAPI_FindTextDlg` | 搜尋 Text Dialog | 字型/文字量測/字串處理 |
| `_WinAPI_FlashWindow` | 處理 Flash Window | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_FlashWindowEx` | 處理 Flash Window | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_FloatToInt` | 轉換 Float 為 Int | WinAPI 輔助功能 |
| `_WinAPI_FormatDriveDlg` | 格式化 Drive Dialog | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetAncestor` | 取得 Ancestor | WinAPI 輔助功能 |
| `_WinAPI_GetAsyncKeyState` | 取得 Async Key State | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_GetBinaryType` | 取得 Binary Type | WinAPI 輔助功能 |
| `_WinAPI_GetBitmapDimension` | 取得 Bitmap Dimension | 影像/GDI 物件處理 |
| `_WinAPI_GetBkMode` | 取得 Bk Mode | WinAPI 輔助功能 |
| `_WinAPI_GetCapture` | 取得 Capture | WinAPI 輔助功能 |
| `_WinAPI_GetCaretPos` | 取得 Caret Pos | WinAPI 輔助功能 |
| `_WinAPI_GetCDType` | 取得 CD Type | WinAPI 輔助功能 |
| `_WinAPI_GetClassName` | 取得 Class Name | WinAPI 輔助功能 |
| `_WinAPI_GetClientHeight` | 取得 Client Height | WinAPI 輔助功能 |
| `_WinAPI_GetClientRect` | 取得 Client Rect | WinAPI 輔助功能 |
| `_WinAPI_GetClientWidth` | 取得 Client Width | WinAPI 輔助功能 |
| `_WinAPI_GetCompression` | 取得 Compression | WinAPI 輔助功能 |
| `_WinAPI_GetConnectedDlg` | 取得 Connected Dialog | UI 對話框/訊息/選單 |
| `_WinAPI_GetCurrentHwProfile` | 取得 Current Hw Profile | WinAPI 輔助功能 |
| `_WinAPI_GetCurrentProcessID` | 取得 Current Process ID | 處理程序資訊/控制 |
| `_WinAPI_GetCurrentThemeName` | 取得 Current Theme Name | WinAPI 輔助功能 |
| `_WinAPI_GetCurrentThreadId` | 取得 Current Thread Id | 執行緒資訊/控制 |
| `_WinAPI_GetCursorInfo` | 取得 Cursor Info | 影像/GDI 物件處理 |
| `_WinAPI_GetDateFormat` | 取得 Date Format | 語系/時間/格式化 |
| `_WinAPI_GetDC` | 取得 DC | WinAPI 輔助功能 |
| `_WinAPI_GetDCEx` | 取得 DC | WinAPI 輔助功能 |
| `_WinAPI_GetDesktopWindow` | 取得 Desktop Window | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_GetDeviceGammaRamp` | 取得 Device Gamma Ramp | WinAPI 輔助功能 |
| `_WinAPI_GetDiskFreeSpaceEx` | 取得 Disk Free Space | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetDlgCtrlID` | 取得 Dialog Ctrl ID | UI 對話框/訊息/選單 |
| `_WinAPI_GetDlgItem` | 取得 Dialog Item | UI 對話框/訊息/選單 |
| `_WinAPI_GetDllDirectory` | 取得 Dll Directory | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetDriveBusType` | 取得 Drive Bus Type | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetDriveGeometryEx` | 取得 Drive Geometry | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetDriveNumber` | 取得 Drive Number | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetDriveType` | 取得 Drive Type | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetDurationFormat` | 取得 Duration Format | 語系/時間/格式化 |
| `_WinAPI_GetEffectiveClientRect` | 取得 Effective Client Rect | WinAPI 輔助功能 |
| `_WinAPI_GetEnhMetaFileDescription` | 取得 Enh Meta File Description | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetEnhMetaFileDimension` | 取得 Enh Meta File Dimension | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetExitCodeProcess` | 取得 Exit Code Process | 處理程序資訊/控制 |
| `_WinAPI_GetFileID` | 取得 File ID | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetFileInformationByHandle` | 取得 File Information By Handle | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetFileSizeOnDisk` | 取得 File Size On Disk | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetFinalPathNameByHandle` | 取得 Final Path Name By Handle | 路徑字串正規化/解析/組合 |
| `_WinAPI_GetFinalPathNameByHandleEx` | 取得 Final Path Name By Handle | 路徑字串正規化/解析/組合 |
| `_WinAPI_GetFocus` | 取得 Focus | WinAPI 輔助功能 |
| `_WinAPI_GetFontName` | 取得 Font Name | 字型/文字量測/字串處理 |
| `_WinAPI_GetFontResourceInfo` | 取得 Font Resource Info | 字型/文字量測/字串處理；含變體範例 [2]/[3] |
| `_WinAPI_GetForegroundWindow` | 取得 Foreground Window | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_GetFullPathName` | 取得 Full Path Name | 路徑字串正規化/解析/組合 |
| `_WinAPI_GetGeoInfo` | 取得 Geo Info | WinAPI 輔助功能；含變體範例 [2] |
| `_WinAPI_GetGlyphOutline` | 取得 Glyph Outline | 字型/文字量測/字串處理 |
| `_WinAPI_GetGUIThreadInfo` | 取得 GUI Thread Info | 執行緒資訊/控制 |
| `_WinAPI_GetIconDimension` | 取得 Icon Dimension | 影像/GDI 物件處理 |
| `_WinAPI_GetIconInfo` | 取得 Icon Info | 影像/GDI 物件處理 |
| `_WinAPI_GetIconInfoEx` | 取得 Icon Info | 影像/GDI 物件處理 |
| `_WinAPI_GetIdleTime` | 取得 Idle Time | 語系/時間/格式化 |
| `_WinAPI_GetKeyboardLayout` | 取得 Keyboard Layout | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_GetKeyboardLayoutList` | 取得 Keyboard Layout List | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_GetKeyboardLayoutLocale` | 取得 Keyboard Layout Locale | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_GetKeyboardState` | 取得 Keyboard State | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_GetKeyboardType` | 取得 Keyboard Type | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_GetKeyNameText` | 取得 Key Name Text | 字型/文字量測/字串處理 |
| `_WinAPI_GetKeyState` | 取得 Key State | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_GetLayeredWindowAttributes` | 取得 Layered Window Attributes | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_GetLocaleInfo` | 取得 Locale Info | 語系/時間/格式化 |
| `_WinAPI_GetModuleHandle` | 取得 Module Handle | 資源/模組/Handle 操作 |
| `_WinAPI_GetMonitorInfo` | 取得 Monitor Info | WinAPI 輔助功能 |
| `_WinAPI_GetMousePos` | 取得 Mouse Pos | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_GetMousePosX` | 取得 Mouse Pos X | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_GetNumberFormat` | 取得 Number Format | 語系/時間/格式化 |
| `_WinAPI_GetObjectInfoByHandle` | 取得 Object Info By Handle | 資源/模組/Handle 操作 |
| `_WinAPI_GetObjectNameByHandle` | 取得 Object Name By Handle | 資源/模組/Handle 操作 |
| `_WinAPI_GetOpenFileName` | 取得 Open File Name | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetOutlineTextMetrics` | 取得 Outline Text Metrics | 字型/文字量測/字串處理 |
| `_WinAPI_GetPerformanceInfo` | 取得 Performance Info | WinAPI 輔助功能 |
| `_WinAPI_GetPosFromRect` | 取得 Pos From Rect | WinAPI 輔助功能 |
| `_WinAPI_GetProcAddress` | 取得 Proc Address | WinAPI 輔助功能 |
| `_WinAPI_GetProcessCommandLine` | 取得 Process Command Line | 處理程序資訊/控制 |
| `_WinAPI_GetProcessFileName` | 取得 Process File Name | 處理程序資訊/控制 |
| `_WinAPI_GetProcessMemoryInfo` | 取得 Process Memory Info | 處理程序資訊/控制 |
| `_WinAPI_GetProcessName` | 取得 Process Name | 處理程序資訊/控制 |
| `_WinAPI_GetProcessTimes` | 取得 Process Times | 處理程序資訊/控制 |
| `_WinAPI_GetProcessUser` | 取得 Process User | 處理程序資訊/控制 |
| `_WinAPI_GetProcessWorkingDirectory` | 取得 Process Working Directory | 處理程序資訊/控制 |
| `_WinAPI_GetPwrCapabilities` | 取得 Power Capabilities | 電源與電池狀態 |
| `_WinAPI_GetRegKeyNameByHandle` | 取得 Reg Key Name By Handle | 登錄鍵/登錄值存取或監聽 |
| `_WinAPI_GetSaveFileName` | 取得 Save File Name | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetString` | 取得 String | 字型/文字量測/字串處理 |
| `_WinAPI_GetSysColor` | 取得 Sys Color | WinAPI 輔助功能 |
| `_WinAPI_GetSystemPowerStatus` | 取得 System Power Status | 電源與電池狀態 |
| `_WinAPI_GetTabbedTextExtent` | 取得 Tabbed Text Extent | 字型/文字量測/字串處理 |
| `_WinAPI_GetTextExtentPoint32` | 取得 Text Extent Point 32 | 字型/文字量測/字串處理 |
| `_WinAPI_GetThemeAppProperties` | 取得 Theme App Properties | WinAPI 輔助功能 |
| `_WinAPI_GetThemeColor` | 取得 Theme Color | WinAPI 輔助功能 |
| `_WinAPI_GetThemeTransitionDuration` | 取得 Theme Transition Duration | WinAPI 輔助功能 |
| `_WinAPI_GetThreadLocale` | 取得 Thread Locale | 執行緒資訊/控制 |
| `_WinAPI_GetTickCount` | 取得 Tick Count | WinAPI 輔助功能 |
| `_WinAPI_GetTimeFormat` | 取得 Time Format | 語系/時間/格式化 |
| `_WinAPI_GetUserObjectInformation` | 取得 User Object Information | WinAPI 輔助功能 |
| `_WinAPI_GetVersion` | 取得 Version | WinAPI 輔助功能 |
| `_WinAPI_GetVolumeInformation` | 取得 Volume Information | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetVolumeInformationByHandle` | 取得 Volume Information By Handle | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetVolumeNameForVolumeMountPoint` | 取得 Volume Name Volume Mount Point | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_GetWindowInfo` | 取得 Window Info | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_GetWindowPlacement` | 取得 Window Placement | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_GetWindowSubclass` | 取得 Window Subclass | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_GetWindowText` | 取得 Window Text | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_GetWindowThreadProcessId` | 取得 Window Thread Process Id | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_GetWorkArea` | 取得 Work Area | WinAPI 輔助功能 |
| `_WinAPI_GradientFill` | 處理 Gradient Fill | WinAPI 輔助功能 |
| `_WinAPI_GUIDFromString` | 由 String 取得 GUID | 字型/文字量測/字串處理 |
| `_WinAPI_HashData` | 雜湊 Data | WinAPI 輔助功能 |
| `_WinAPI_HashString` | 雜湊 String | 字型/文字量測/字串處理 |
| `_WinAPI_IntToDWord` | 轉換 Int 為 DWORD | WinAPI 輔助功能 |
| `_WinAPI_IntToFloat` | 轉換 Int 為 Float | WinAPI 輔助功能 |
| `_WinAPI_InvertANDBitmap` | 反轉 AND Bitmap | 影像/GDI 物件處理 |
| `_WinAPI_InvertColor` | 反轉 Color | WinAPI 輔助功能 |
| `_WinAPI_IsInternetConnected` | 判斷 Internet Connected | WinAPI 輔助功能 |
| `_WinAPI_IsNetworkAlive` | 判斷 Network Alive | WinAPI 輔助功能 |
| `_WinAPI_IsWritable` | 判斷 Writable | WinAPI 輔助功能 |
| `_WinAPI_LineDDA` | 處理 Line DDA | WinAPI 輔助功能 |
| `_WinAPI_LoadCursorFromFile` | 載入 Cursor From File | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_LoadIconWithScaleDown` | 載入 Icon With Scale Down | 影像/GDI 物件處理 |
| `_WinAPI_LoadIndirectString` | 載入 Indirect String | 字型/文字量測/字串處理 |
| `_WinAPI_LoadLibraryEx` | 載入 Library | 資源/模組/Handle 操作 |
| `_WinAPI_LoadMedia` | 載入 Media | WinAPI 輔助功能 |
| `_WinAPI_LoadResource` | 載入 Resource | 資源/模組/Handle 操作 |
| `_WinAPI_LoadStringEx` | 載入 String | 字型/文字量測/字串處理 |
| `_WinAPI_LockDevice` | 鎖定 Device | WinAPI 輔助功能 |
| `_WinAPI_LoDWord` | 處理 Lo DWORD | WinAPI 輔助功能 |
| `_WinAPI_LongMid` | 處理 Long Mid | WinAPI 輔助功能 |
| `_WinAPI_LoWord` | 處理 LOWORD | WinAPI 輔助功能 |
| `_WinAPI_MapVirtualKey` | 處理 Map Virtual Key | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_MaskBlt` | 處理 Mask Blt | WinAPI 輔助功能 |
| `_WinAPI_MessageBoxCheck` | 檢查 Message Box | UI 對話框/訊息/選單 |
| `_WinAPI_MessageBoxIndirect` | 處理 Message Box Indirect | UI 對話框/訊息/選單 |
| `_WinAPI_MirrorIcon` | 處理 Mirror Icon | 影像/GDI 物件處理 |
| `_WinAPI_MonitorFromPoint` | 由 Point 取得 Monitor | WinAPI 輔助功能 |
| `_WinAPI_MonitorFromRect` | 由 Rect 取得 Monitor | WinAPI 輔助功能 |
| `_WinAPI_MonitorFromWindow` | 由 Window 取得 Monitor | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_MoveFileEx` | 移動 File | 檔案/磁碟/磁碟機操作；含變體範例 [2] |
| `_WinAPI_MoveMemory` | 移動 Memory | WinAPI 輔助功能 |
| `_WinAPI_NtStatusToDosError` | 轉換 Nt Status 為 Dos Error | WinAPI 輔助功能 |
| `_WinAPI_OpenEvent` | 開啟 Event | 同步/事件/等待 |
| `_WinAPI_OpenFileById` | 開啟 File By Id | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_OpenFileDlg` | 開啟 File Dialog | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_PageSetupDlg` | 處理 Page Setup Dialog | UI 對話框/訊息/選單 |
| `_WinAPI_ParseURL` | 解析 URL | URL 組合/解析/正規化 |
| `_WinAPI_ParseUserName` | 解析 User Name | WinAPI 輔助功能 |
| `_WinAPI_PathAddBackslash` | 新增 Path Backslash | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathAddExtension` | 新增 Path Extension | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathAppend` | 處理 Path Append | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathBuildRoot` | 建立 Path Root | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathCanonicalize` | 處理 Path Canonicalize | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathCommonPrefix` | 處理 Path Common Prefix | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathCompactPath` | 處理 Path Compact Path | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathCompactPathEx` | 處理 Path Compact Path | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathCreateFromUrl` | 建立 Path From URL | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathFindFileName` | 搜尋 Path File Name | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathFindNextComponent` | 搜尋 Path Next Component | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathFindOnPath` | 搜尋 Path On Path | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathGetArgs` | 取得 Path Args | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathGetDriveNumber` | 取得 Path Drive Number | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathIsContentType` | 判斷 Path Content Type | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathIsDirectory` | 判斷 Path Directory | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathIsExe` | 判斷 Path Exe | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathMatchSpec` | 處理 Path Match Spec | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathParseIconLocation` | 解析 Path Icon Location | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathRelativePathTo` | 處理 Path Relative Path To | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathRemoveArgs` | 移除 Path Args | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathRemoveBackslash` | 移除 Path Backslash | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathRemoveExtension` | 移除 Path Extension | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathRemoveFileSpec` | 移除 Path File Spec | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathRenameExtension` | 處理 Path Rename Extension | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathSearchAndQualify` | 處理 Path Search Qualify | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathSkipRoot` | 處理 Path Skip Root | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathStripPath` | 處理 Path Strip Path | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathStripToRoot` | 轉換 Path Strip 為 Root | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathUndecorate` | 處理 Path Undecorate | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathUnExpandEnvStrings` | 展開 Path Un Env Strings | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathUnquoteSpaces` | 處理 Path Unquote Spaces | 路徑字串正規化/解析/組合 |
| `_WinAPI_PathYetAnotherMakeUniqueName` | 處理 Path Yet Another Make Unique Name | 路徑字串正規化/解析/組合 |
| `_WinAPI_PickIconDlg` | 挑選 Icon Dialog | 影像/GDI 物件處理 |
| `_WinAPI_PlayEnhMetaFile` | 播放 Enh Meta File | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_PlaySound` | 播放 Sound | WinAPI 輔助功能 |
| `_WinAPI_PrintDlg` | 列印 Dialog | UI 對話框/訊息/選單 |
| `_WinAPI_PrintDlgEx` | 列印 Dialog | UI 對話框/訊息/選單 |
| `_WinAPI_PrintWindow` | 列印 Window | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_ProgIDFromCLSID` | 由 CLSID 取得 PROGID | WinAPI 輔助功能 |
| `_WinAPI_QueryDosDevice` | 查詢 Dos Device | WinAPI 輔助功能 |
| `_WinAPI_QueryProcessCycleTime` | 查詢 Process Cycle Time | 處理程序資訊/控制 |
| `_WinAPI_QueryProcessorUsage` | 查詢 Processor Usage | WinAPI 輔助功能 |
| `_WinAPI_RadialGradientFill` | 處理 Radial Gradient Fill | WinAPI 輔助功能 |
| `_WinAPI_ReadDirectoryChanges` | 讀取 Directory Changes | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_Rectangle` | 處理 Rectangle | WinAPI 輔助功能 |
| `_WinAPI_RegCreateKey` | 建立 Reg Key | 登錄鍵/登錄值存取或監聽；含變體範例 [2] |
| `_WinAPI_RegDeleteKey` | 刪除 Reg Key | 登錄鍵/登錄值存取或監聽 |
| `_WinAPI_RegEnumKey` | 列舉 Reg Key | 登錄鍵/登錄值存取或監聽 |
| `_WinAPI_RegEnumValue` | 列舉 Reg Value | 登錄鍵/登錄值存取或監聽 |
| `_WinAPI_RegisterApplicationRestart` | 註冊 Application Restart | WinAPI 輔助功能 |
| `_WinAPI_RegisterClassEx` | 註冊 Class | WinAPI 輔助功能 |
| `_WinAPI_RegisterHotKey` | 註冊 Hot Key | 輸入裝置/鍵鼠狀態 |
| `_WinAPI_RegisterRawInputDevices` | 註冊 Raw Input Devices | 輸入裝置/鍵鼠狀態；含變體範例 [2] |
| `_WinAPI_RegisterShellHookWindow` | 註冊 Shell Hook Window | Shell 檔案/圖示/通知整合 |
| `_WinAPI_RegNotifyChangeKeyValue` | 通知 Reg Change Key Value | 登錄鍵/登錄值存取或監聽 |
| `_WinAPI_RegOpenKey` | 開啟 Reg Key | 登錄鍵/登錄值存取或監聽；含變體範例 [2]/[3] |
| `_WinAPI_RegQueryMultipleValues` | 查詢 Reg Multiple Values | 登錄鍵/登錄值存取或監聽 |
| `_WinAPI_RegQueryValue` | 查詢 Reg Value | 登錄鍵/登錄值存取或監聽；含變體範例 [2] |
| `_WinAPI_RegSaveKey` | 儲存 Reg Key | 登錄鍵/登錄值存取或監聽 |
| `_WinAPI_ReleaseDC` | 釋放 DC | WinAPI 輔助功能 |
| `_WinAPI_ReplaceFile` | 取代 File | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_ReplaceTextDlg` | 取代 Text Dialog | 字型/文字量測/字串處理 |
| `_WinAPI_RGB` | 處理 RGB | WinAPI 輔助功能 |
| `_WinAPI_RotatePoints` | 旋轉 Points | WinAPI 輔助功能 |
| `_WinAPI_SaveFileDlg` | 儲存 File Dialog | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_SaveHICONToFile` | 儲存 HICON To File | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_ScreenToClient` | 轉換 Screen 為 Client | WinAPI 輔助功能 |
| `_WinAPI_SearchPath` | 處理 Search Path | 路徑字串正規化/解析/組合 |
| `_WinAPI_SelectClipRgn` | 選取 Clip Rgn | WinAPI 輔助功能 |
| `_WinAPI_SendInput` | 處理 Send Input | 輸入裝置/鍵鼠狀態；含變體範例 [2] |
| `_WinAPI_SetClassLongEx` | 設定 Class Long | WinAPI 輔助功能 |
| `_WinAPI_SetCurrentProcessExplicitAppUserModelID` | 設定 Current Process Explicit App User Model ID | 處理程序資訊/控制 |
| `_WinAPI_SetCursorSize` | 設定 Cursor Size | 影像/GDI 物件處理 |
| `_WinAPI_SetFileShortName` | 設定 File Short Name | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_SetParent` | 設定 Parent | WinAPI 輔助功能 |
| `_WinAPI_SetPriorityClass` | 設定 Priority Class | WinAPI 輔助功能 |
| `_WinAPI_SetProcessShutdownParameters` | 設定 Process Shutdown Parameters | 處理程序資訊/控制 |
| `_WinAPI_SetSystemCursor` | 設定 System Cursor | 影像/GDI 物件處理 |
| `_WinAPI_SetTextColor` | 設定 Text Color | 字型/文字量測/字串處理 |
| `_WinAPI_SetThreadExecutionState` | 設定 Thread Execution State | 執行緒資訊/控制 |
| `_WinAPI_SetTimer` | 設定 Timer | WinAPI 輔助功能；含變體範例 [2] |
| `_WinAPI_SetVolumeMountPoint` | 設定 Volume Mount Point | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_SetWindowDisplayAffinity` | 設定 Window Display Affinity | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_SetWindowPos` | 設定 Window Pos | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_SetWindowTheme` | 設定 Window Theme | 視窗 Handle/樣式/位置管理；含變體範例 [2] |
| `_WinAPI_SetWinEventHook` | 設定 Win Event Hook | 同步/事件/等待 |
| `_WinAPI_SfcIsFileProtected` | 判斷 Sfc File Protected | 檔案/磁碟/磁碟機操作 |
| `_WinAPI_ShellAboutDlg` | 處理 Shell About Dialog | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellAddToRecentDocs` | 新增 Shell To Recent Docs | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellChangeNotify` | 變更 Shell Notify | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellChangeNotifyRegister` | 變更 Shell Notify Register | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellExecute` | 執行 Shell | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellExecuteEx` | 執行 Shell | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellExtractAssociatedIcon` | 擷取 Shell Associated Icon | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellExtractIcon` | 擷取 Shell Icon | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellFileOperation` | 處理 Shell File Operation | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellGetFileInfo` | 取得 Shell File Info | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellGetImageList` | 取得 Shell Image List | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellGetKnownFolderPath` | 取得 Shell Known Folder Path | 路徑字串正規化/解析/組合 |
| `_WinAPI_ShellGetLocalizedName` | 取得 Shell Localized Name | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellGetSetFolderCustomSettings` | 取得 Shell Set Folder Custom Settings | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellGetSettings` | 取得 Shell Settings | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellGetSpecialFolderPath` | 取得 Shell Special Folder Path | 路徑字串正規化/解析/組合 |
| `_WinAPI_ShellGetStockIconInfo` | 取得 Shell Stock Icon Info | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellNotifyIcon` | 通知 Shell Icon | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellNotifyIconGetRect` | 通知 Shell Icon Get Rect | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellObjectProperties` | 處理 Shell Object Properties | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellOpenFolderAndSelectItems` | 開啟 Shell Folder Select Items | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellOpenWithDlg` | 開啟 Shell With Dialog | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellQueryRecycleBin` | 查詢 Shell Recycle Bin | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellSetLocalizedName` | 設定 Shell Localized Name | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellUserAuthenticationDlg` | 處理 Shell User Authentication Dialog | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShellUserAuthenticationDlgEx` | 處理 Shell User Authentication Dialog | Shell 檔案/圖示/通知整合 |
| `_WinAPI_ShortToWord` | 轉換 Short 為 Word | WinAPI 輔助功能 |
| `_WinAPI_ShowCaret` | 顯示 Caret | WinAPI 輔助功能 |
| `_WinAPI_ShowWindow` | 顯示 Window | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_ShutdownBlockReasonQuery` | 查詢 Shutdown Block Reason | WinAPI 輔助功能 |
| `_WinAPI_StrFormatByteSize` | 格式化 Str Byte Size | 語系/時間/格式化 |
| `_WinAPI_StrFormatByteSizeEx` | 格式化 Str Byte Size | 語系/時間/格式化 |
| `_WinAPI_StrFormatKBSize` | 格式化 Str KB Size | 語系/時間/格式化 |
| `_WinAPI_StrFromTimeInterval` | 由 Time Interval 取得 Str | 語系/時間/格式化 |
| `_WinAPI_StringLenA` | 處理 String Len | 字型/文字量測/字串處理 |
| `_WinAPI_StringLenW` | 處理 String Len | 字型/文字量測/字串處理 |
| `_WinAPI_SwapDWord` | 交換 DWORD | WinAPI 輔助功能 |
| `_WinAPI_SwapQWord` | 交換 QWORD | WinAPI 輔助功能 |
| `_WinAPI_SwapWord` | 交換 Word | WinAPI 輔助功能 |
| `_WinAPI_SwitchColor` | 處理 Switch Color | WinAPI 輔助功能 |
| `_WinAPI_SystemParametersInfo` | 處理 System Parameters Info | WinAPI 輔助功能 |
| `_WinAPI_TabbedTextOut` | 處理 Tabbed Text Out | 字型/文字量測/字串處理 |
| `_WinAPI_TileWindows` | 處理 Tile Windows | WinAPI 輔助功能 |
| `_WinAPI_TransparentBlt` | 處理 Transparent Blt | WinAPI 輔助功能 |
| `_WinAPI_UnionStruct` | 處理 Union Struct | WinAPI 輔助功能 |
| `_WinAPI_UniqueHardwareID` | 處理 Unique Hardware ID | WinAPI 輔助功能 |
| `_WinAPI_UpdateLayeredWindowEx` | 更新 Layered Window | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_UrlApplyScheme` | 處理 URL Apply Scheme | URL 組合/解析/正規化 |
| `_WinAPI_UrlCanonicalize` | 處理 URL Canonicalize | URL 組合/解析/正規化 |
| `_WinAPI_UrlCombine` | 處理 URL Combine | URL 組合/解析/正規化 |
| `_WinAPI_UrlCompare` | 比較 URL | URL 組合/解析/正規化 |
| `_WinAPI_UrlFixup` | 處理 URL Fixup | URL 組合/解析/正規化 |
| `_WinAPI_UrlGetPart` | 取得 URL Part | URL 組合/解析/正規化 |
| `_WinAPI_UrlHash` | 雜湊 URL | URL 組合/解析/正規化 |
| `_WinAPI_VerQueryValue` | 查詢 Ver Value | WinAPI 輔助功能 |
| `_WinAPI_VerQueryValueEx` | 查詢 Ver Value | WinAPI 輔助功能 |
| `_WinAPI_WaitForMultipleObjects` | 等待 Multiple Objects | 同步/事件/等待 |
| `_WinAPI_WaitSystemIdle` | 等待 System Idle | 同步/事件/等待 |
| `_WinAPI_WideCharToMultiByte` | 轉換 Wide Char 為 Multi Byte | WinAPI 輔助功能 |
| `_WinAPI_WindowFromPoint` | 由 Point 取得 Window | 視窗 Handle/樣式/位置管理 |
| `_WinAPI_WordToShort` | 轉換 Word 為 Short | WinAPI 輔助功能 |
| `_WinAPI_ZeroMemory` | 處理 Zero Memory | WinAPI 輔助功能 |

**Word 範例（29 個）：**
- `_Word_Create.au3`
- `_Word_DocAdd.au3`
- `_Word_DocAttach.au3`
- `_Word_DocAttach[2].au3`
- `_Word_DocClose.au3`
- `_Word_DocExport.au3`
- `_Word_DocExport[2].au3`
- `_Word_DocExport[3].au3`
- `_Word_DocFind.au3`
- `_Word_DocFind[2].au3`
- `_Word_DocFind[3].au3`
- `_Word_DocFind[4].au3`
- `_Word_DocFindReplace.au3`
- `_Word_DocFindReplace[2].au3`
- `_Word_DocGet.au3`
- `_Word_DocLinkAdd.au3`
- `_Word_DocLinkAdd[2].au3`
- `_Word_DocLinkGet.au3`
- `_Word_DocLinkGet[2].au3`
- `_Word_DocOpen.au3`
- `_Word_DocPictureAdd.au3`
- `_Word_DocPictureAdd[2].au3`
- `_Word_DocPrint.au3`
- `_Word_DocRangeSet.au3`
- `_Word_DocSave.au3`
- `_Word_DocSaveAs.au3`
- `_Word_DocTableRead.au3`
- `_Word_DocTableWrite.au3`
- `_Word_Quit.au3`

## 2. 環境與工具

1. **AutoIt3.exe**：核心直譯器。
2. **SciTE Script Editor**：官方編輯器。
3. **Au3Info.exe**：偵測視窗/控制項資訊（定位用）。
4. **Aut2Exe.exe**：編譯 `.au3` 成可執行檔。
5. **AutoIt.chm / AutoIt3Help.exe**：官方說明與函式索引。

## 3. 先決條件與注意事項

- **Office**：Excel/Word 範例需安裝 Office。
- **IE / SAPI**：IE 事件範例與 SAPI 範例需相容環境。
- **WMI / ADSI**：WMI/ADSI 例子在禁用服務或權限不足時會失敗。
- **語系**：英文版 Windows 對話框/控制項文字不同步需調整。

## 4. 常見錯誤排查與權限需求

- **0x80040154 (Class not registered)**：`ObjCreate` 失敗。修正：安裝對應軟體、確認 x86/x64 一致、重新註冊 COM/ProgID。
- **0x80070005 (Access denied)**：COM/WMI/登錄權限不足。修正：以系統管理員執行、檢查 DCOM/WMI 安全性、UAC/ACL。
- **0x8004100E / 0x80041010 (WMI namespace/class)**：命名空間或類別錯。修正：確認 `root\\cimv2`，必要時重建 WMI repository。
- **0x800706BA (RPC server unavailable)**：遠端 WMI/DCOM 連線失敗。修正：開啟 RPC 服務、放行防火牆、啟用 DCOM。
- **WinAPI `GetLastError` 2/3/5/32**：檔案或路徑不存在/權限不足/檔案占用。修正：檢查路徑、提升權限、關閉占用程序。
- **ShellExecute 回傳值 <=32**：常見 2/3/5。修正：檢查檔案路徑/權限/Verb。
- **Named Pipes 234/258/535/997**：資料超過緩衝、逾時、已連線、Overlapped 進行中。修正：提高 buffer、處理等待分支。
- **`ObjGet` 失敗（@error）**：目標應用需先啟動（如 `Excel.Application`），或指定正確 ProgID。
- **ADSI 非必要錯誤**：WinNT provider 速度慢、網域/群組不存在會觸發錯誤事件。
- **控制項定位失敗**：不同語系/主題造成標題變動，優先用 `Au3Info.exe` 取 `[CLASS:...]`。
- **權限需求**：服務啟停、登錄寫入、WMI/遠端 DCOM 通常需管理員；`_WinAPI_RegCreateKey` 範例直接 `#RequireAdmin`。
- **GDI+ 相關錯誤**：圖片不存在、分層視窗需 32-bit PNG 含 Alpha 通道，確認 `_GDIPlus_Startup()`。

## 5. 核心語法與常用巨集

- **變數**：`$var`。
- **註解**：`;`。
- **錯誤處理**：`@error` + `ObjEvent("AutoIt.Error", ...)`。
- **常用巨集**：`@CRLF`、`@ComputerName`、`@UserName`、`@WindowsDir`。

## 6. GUI 模式重點

**Message Loop 模式**
- `GUIGetMsg()` + `Select/Case`。

**OnEvent 模式**
- `Opt("GUIOnEventMode", 1)` + `GUICtrlSetOnEvent`。

**多視窗來源**
- `GUIGetMsg(1)` 取得 `[msg, hwnd]`，用於父/子視窗判斷。

## 7. COM / WMI / ADSI 常見模式

- **建立 COM**：`ObjCreate("ProgID")`。
- **附加既有 COM**：`ObjGet("", "Excel.Application")`。
- **WMI 查詢**：`ObjGet("winmgmts:\\<host>\\root\\cimv2")` + `ExecQuery`。
- **事件處理**：`ObjEvent($o, "Prefix_")`。
- **遠端 DCOM**：`ObjCreate("ProgID", $host, $user, $pass)`。

## 8. 影像/GDI+ 常用流程

- `_GDIPlus_Startup()` → `_GDIPlus_ImageLoadFromFile()` → 操作 → `_GDIPlus_Shutdown()`。
- 分層視窗與透明度：`_WinAPI_UpdateLayeredWindow()`。
- 螢幕擷取：`_ScreenCapture_Capture()`。

## 9. 常用函數矩陣（依範例來源）

| 類別 | 函數 | 範例用途 |
| :--- | :--- | :--- |
| GUI | `GUICreate` | 建立視窗 |
| GUI | `GUIGetMsg` | Message Loop |
| GUI | `GUICtrlCreateMenu` | Menu |
| GUI | `GUICtrlCreateContextMenu` | Context Menu |
| GUI | `GUICtrlCreateTreeView` | TreeView |
| GUI | `GUIRegisterMsg` | 攔截 WM_* 訊息 |
| COM | `ObjCreate` / `ObjGet` | COM/WMI/ADSI |
| COM | `ObjEvent` | COM 事件 |
| GDI+ | `_GDIPlus_*` | 影像操作 |
| IPC | `_NamedPipes_*` | Named Pipes |
| 系統 | `DriveGetLabel` / `DriveSpaceTotal` | 系統資訊 |
| 視窗 | `Run` / `WinWaitActive` | 程式自動化 |

## 10. 小片段（對應範例）

```autoit
; Message Loop
While 1
    Switch GUIGetMsg()
        Case $GUI_EVENT_CLOSE
            ExitLoop
    EndSwitch
WEnd

; COM 錯誤處理
Global $g_oErr = ObjEvent("AutoIt.Error", "MyErrFunc")
```
