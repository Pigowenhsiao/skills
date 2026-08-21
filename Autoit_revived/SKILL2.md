1. 簡介與環境準備
AutoIt v3 是一款免費、類 BASIC 語法的腳本語言，專為 Windows GUI 自動化與通用腳本設計。它透過模擬鍵盤按鍵、滑鼠移動及視窗/控制項操作，實現其他語言難以達成的自動化任務。
⚠️ Windows XP 重要限制
• 版本建議： v3.3.16.1 是最後一個支援 Windows XP 的版本。
• 無需運行環境： 腳本可編譯成獨立的 .exe 檔，在未安裝 AutoIt 的電腦上直接執行。
必備工具組
1. AutoIt3.exe： 核心直譯器，負責執行腳本。
2. SciTE Script Editor： 專用的編輯環境，支援語法高亮與程式碼完成。
3. Au3Info.exe (重要)： 用於偵測目標軟體的「視窗標題」與「控制項 ID (Control ID)」，這是精準定位的關鍵。
4. Aut2Exe： 將腳本編譯成執行檔的工具。

--------------------------------------------------------------------------------
2. 基礎語法結構
• 變數宣告： 變數必須以 $ 開頭。
• 註解： 使用分號 ; 開頭。
• 命令行參數： 透過 $CmdLine 陣列接收從外部（如 Python 橋接程式）傳入的 Recipe 名稱。

--------------------------------------------------------------------------------
3. 核心功能函數表
類別,函數名稱,說明
視窗操作 ,  WinActivate , 啟動並激活指定的視窗。
視窗操作 ,WinWaitActive ,等待特定視窗出現並成為活動狀態（確保同步）。
視窗操作 ,WinGetPos ,取得視窗的座標與大小。
視窗操作 , WinMove ,移動視窗的位置或改變其大小
視窗操作 , WinSetState , 	改變視窗的狀態，例如將其最大化 (@SW_MAXIMIZE) 或隱藏。
視窗操作 , WinGetHandle , 獲取視窗的內部 Win32 API 控制代碼 (Handle)，用於更底層的互動。
控制項互動,ControlClick,最可靠的方法。直接點擊按鈕，不依賴滑鼠座標。
控制項互動,ControlSetText,在文字框中直接填入資料（如 Recipe 名稱）。
控制項互動, ControlCommand , 向特定的控制項發送更複雜的指令（如選取下拉選單中的項目）。
模擬輸入 , Send ,模擬鍵盤輸入（如按 Enter 或快捷鍵）。
模擬輸入 ,MouseClick ,在指定座標點擊（若 Control ID 無效時的備案）。
模擬輸入 , MouseGetPos , 獲取滑鼠目前的座標資訊。
程序管理 , Run ,啟動外部應用程式。
程序管理 , ProcessExists ,檢查特定程序是否正在運行。
程序管理 , ProcessWaitClose ,等待特定的系統程序完全結束後才繼續執行腳本。
程序管理 , Exit ,立即終止腳本的執行程序。
資料與檔案操作, FileRead ,讀取檔案中的資料內容。
資料與檔案操作, FileWriteLine , 向指定的檔案寫入一行新的文字資料。
資料與檔案操作, FileDelete, 刪除指定的檔案。
資料與檔案操作, IniWrite, 向 .ini 格式的設定檔中寫入特定的數值或設定項。
資料與檔案操作, StringInStr, 檢查字串中是否包含特定的子字串。
系統進階功能, DllCall , 直接呼叫外部 Windows API 或第三方 DLL 中的函數。
系統進階功能, ObjCreateInterface, 創建並連接 COM 介面，常用於 UIA (UI Automation) 進階自動化。
系統進階功能, TimerInit, 初始化計時器，用於監測操作是否超時或閒置時間。
系統進階功能, TimerDiff, 計算自計時器啟動以來所經過的時間。
系統進階功能, HotKeySet, 設置全域熱鍵，當按下特定按鍵時觸發腳本中的函數。
通用腳本語法, Sleep ,暫停腳本運行一段指定的時間（毫秒），讓系統有時間響應操作。
通用腳本語法, MsgBox, 彈出訊息視窗向使用者顯示提示資訊或調試訊息。
--------------------------------------------------------------------------------
4. 實戰程式碼範例：自動載入 Recipe
以下腳本模擬接收來自條碼系統的 Recipe 名稱，並在控制軟體中執行的流程：
; --- 步驟 1: 確保目標視窗開啟並激活 ---
WinActivate("設備控制系統")
WinWaitActive("設備控制系統") [15, 18]

; --- 步驟 2: 點擊「載入」按鈕 ---
; 使用 Au3Info.exe 獲取的 Class/Instance 定位更穩健
ControlClick("設備控制系統", "", "[CLASS:Button; INSTANCE:1]") [18, 21]

; --- 步驟 3: 輸入從外部傳入的資料 ---
WinWaitActive("選取 Recipe 檔案")
; 假設 $CmdLine[22] 是從 MES 查到的 Recipe 名稱
Local $RecipeName = $CmdLine[22]
ControlSetText("選取 Recipe 檔案", "", "[CLASS:Edit; INSTANCE:1]", $RecipeName) [18, 21]

; --- 步驟 4: 確認並執行 ---
ControlClick("選取 Recipe 檔案", "", "[CLASS:Button; INSTANCE:2]") ; 點擊確定
WinWaitActive("設備控制系統")
ControlClick("設備控制系統", "", "[CLASS:Button; INSTANCE:3]") ; 點擊開始運行 [16, 18]

--------------------------------------------------------------------------------
5. 專家級實踐指南 (Best Practices)
1. 遵循「可靠性金字塔」： 永遠優先使用 ControlClick 與 ControlSetText。只有在萬不得已時，才使用不穩定的 MouseClick 或 PixelSearch。
2. 先規劃再編碼： 在撰寫前先記錄手動流程，形成「偽代碼 (Pseudo script)」。
3. 建立容錯機制： 使用 WinWait 搭配超時參數，處理視窗延遲彈出的情況。
4. 固定環境： 由於 UI 自動化是視覺導向，執行時不可移動滑鼠或改變螢幕解析度。
5. 跨語言整合 (AutoItX)： 如果您習慣使用 Python 或 C# 處理資料庫，可使用 AutoItX 元件，在 Python 中直接呼叫 AutoIt 的 ControlClick 功能。

--------------------------------------------------------------------------------
💡 總結
AutoIt 就像是一支精準的數位機械臂，能模擬人類操作員的動作，將封閉的舊系統與現代化的 MES 流程連接起來。透過 Au3Info.exe 的精準定位，您可以確保這支機械臂每次都能準確地點擊正確的按鈕。