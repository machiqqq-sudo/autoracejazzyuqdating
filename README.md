# TurtleBot3 AutoRace Jazzy Simulation 🏎️

[![ROS 2](https://img.shields.io/badge/ROS_2-Jazzy-blue.svg)](https://docs.ros.org/en/jazzy/)
[![Simulator](https://img.shields.io/badge/Gazebo-Harmonic-orange.svg)](https://gazebosim.org/home)

這是一個基於 **ROS 2 Jazzy** 與 **Gazebo Harmonic** 構建的 TurtleBot3 自動駕駛模擬專案。本專案為淡江大學人工智慧學系大三專題，旨在將傳統的 AutoRace 賽道環境移植至最新的 ROS 2 架構中，並解決底層模型的座標對齊與感測器相容性問題。

This is a TurtleBot3 autonomous driving simulation project built on **ROS 2 Jazzy** and **Gazebo Harmonic**. Developed as a junior-year project at the Department of Artificial Intelligence, Tamkang University, this repository ports the classic AutoRace environment to the latest ROS 2 architecture, resolving core coordinate alignment and sensor compatibility issues.

---

## 🌟 核心功能 (Key Features)

* **環境移植 (Environment Porting)**：成功將 2020 AutoRace 賽道與交通號誌模型移植至 Gazebo Harmonic。
* **精準感測 (Sensor Accuracy)**：修復 LiDAR `frame_id` 遺失問題，確保 RViz 中 LaserScan 數據與 TF 座標樹完美對齊。
* **動態管理 (Dynamic Management)**：實作 `autorace_manager` 節點，可自動定時控制賽道柵欄升降。
* **標準架構 (Standardized Structure)**：完全遵循 ROS 2 標準功能包架構，支援 `colcon` 編譯與快速部署。

## 📂 專案架構 (Project Structure)

```text
autorace_jazzy/
├── autorace_jazzy/     # Python 節點原始碼 (Python Node Source Code)
├── config/             # 參數設定檔 (Configuration files)
├── launch/             # 啟動腳本 (Launch files)
├── models/             # 3D 網格與材質模型 (3D Models and Textures)
├── rviz/               # RViz 預設視覺化設定 (RViz configurations)
├── sdf/                # 機器人描述檔 (Robot description files)
└── worlds/             # Gazebo 賽道地圖 (Gazebo world files)
