---
name: ubuntu-gpu-driver-headless-install
description: 在 Ubuntu 24.04 無頭環境安裝 NVIDIA GPU 驅動程式。包含驅動選擇、Secure Boot 處理、CUDA 安裝與驗證。
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [gpu, nvidia, cuda, ubuntu, driver, whisper, ml-inference]
category: devops
triggers:
  - "ubuntu-gpu-driver-headless-install"

---

# Ubuntu GPU 驅動安裝（無頭環境）

## 適用情境

在無顯示器的 Ubuntu 24.04 伺服器上安裝 NVIDIA GPU 驅動，給 Whisper、LLM 推論等 ML 任務用。

## 前置檢查

```bash
# 確認 GPU 型號
lspci | grep -i 'vga\|3d\|gpu'

# 確認目前驅動狀態
nvidia-smi 2>/dev/null || echo "nvidia-smi not available"

# 檢查 /dev/nvidia* 裝置
ls /dev/nvidia* 2>/dev/null || echo "no nvidia devices"

# 查看可用驅動
ubuntu-drivers devices
```

## 安裝流程

### Step 1: 檢查 Secure Boot 狀態

**⚠️ 這是關鍵步驟**

如果在 VM 或無 BIOS 操作權限的環境：
- 先確認 Secure Boot 是否已關閉
- 若無法關閉，Secure Boot 密碼輸入會卡住互動式安裝

```bash
# 檢查
mokutil --sb-state 2>/dev/null
```

### Step 2: 安裝驅動

```bash
# 互動式密碼 pipe（無頭環境）
echo "<sudo-password>" | sudo -S apt install -y nvidia-driver-535 2>&1

# 非互動式（推薦用这个）
DEBIAN_FRONTEND=noninteractive sudo apt install -y nvidia-driver-535
```

**驅動選擇參考：**
- `nvidia-driver-535` — 長期支援，GTX 10xx 系列適用
- `nvidia-driver-545` — 較新
- `nvidia-driver-550` — CUDA 12.x 支援

### Step 3: 驗證

```bash
nvidia-smi
# 預期輸出：GPU 型號、記憶體、使用率

# 檢查 CUDA 版本
nvcc --version 2>/dev/null || echo "CUDA not in PATH"
```

## 常見問題

### Secure Boot 密碼卡住

```
The Secure Boot key you've entered is not valid...
Enter a password for Secure Boot. It will not be asked again after a reboot.
```

**解法：** 必須在本機 BIOS 關閉 Secure Boot，無法遠端解決。

### nvidia-smi: command not found

驅動安裝了但還沒生效：
```bash
sudo modprobe nvidia
# 或重啟
sudo reboot
```

### /dev/nvidia* 不存在

即使 nvidia-smi 可以執行，裝置檔案不存在可能是因為 kernel module 未載入：
```bash
ls /dev/nvidia*
sudo modprobe nvidia_uvm
```

## Whisper GPU 加速

安裝完成後，用 GPU 跑 Whisper：

```python
from faster_whisper import WhisperModel
# device='cuda' 而非 'cpu'
model = WhisperModel('medium', device='cuda', compute_type='float16')
segments, info = model.transcribe('/path/to/audio.wav', language='en')
```

**模型選擇：**
| 模型 | GPU VRAM | CPU 速度 | 準確率 |
|------|---------|---------|--------|
| base | ~1GB | 快 | 基礎 |
| small | ~2GB | 中 | 較好 |
| medium | ~5GB | 慢(CPU) | 很好 | ★ 推薦 GPU |
| large-v3 | ~10GB | 慢(CPU) | 最好 | 需要大 VRAM |

## 與 Whisper 的整合

在 skill 或 script 中偵測 GPU 是否可用，自動選擇 device：

```python
import subprocess
def has_gpu():
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False

device = 'cuda' if has_gpu() else 'cpu'
model = WhisperModel('medium', device=device, compute_type='float16' if device == 'cuda' else 'int8')
```
