# 變更日誌 (Changelog)

所有關於 `autorace_jazzy` 專案的顯著更改都會記錄在此檔案中。

## [1.0.0] - 2026-03-17

### 新增 (Added)
* **標準化架構**：建立完全符合 ROS 2 Jazzy 規範的功能包目錄結構 (`launch`, `sdf`, `models`, `worlds`)。
* **賽道環境**：成功將 TurtleBot3 Autorace 2020 的 Gazebo 賽道與交通號誌模型移植至 Gazebo Harmonic。
* **環境控管**：新增 `autorace_manager` Python 節點，實作賽道起跑線柵欄的定時自動升降邏輯。
* **專案說明**：新增中英雙語版本的 `README.md` 與標準 `.gitignore`，完成 GitHub 開源基礎建設。

### 修復 (Fixed)
* **SDF 語法錯誤**：修復 `my_burger.sdf` 中 `<inertial>` 標籤未閉合導致 Gazebo 解析崩潰 (Error Code 1) 的問題。
* **TF 樹對齊**：修正 LiDAR 感測器的 `frame_id` 缺失問題，確保 `/scan` 數據能正確對齊 `base_scan` 座標系。
* **編譯路徑問題**：補齊 Python 模組必需的 `__init__.py` 與 `setup.cfg`，解決 `libexec directory does not exist` 錯誤。

---
*維護者: jkchen525 (陳建凱)*
