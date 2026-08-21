---
name: pigo-ppt-style
description: >
  Pigo 品牌 PPT 風格模板技能。當需要製作符合 Pigo 品牌風格的簡報、投影片、PPT，或需要使用 Pigo 品牌色彩與排版時觸發。
  適用場景：
  - 製作 Q3 OKR、公司報告、產品簡報
  - 使用 Pigo 品牌色彩（藍 #3B82F6 / 紫 #8B5CF6）
  - 需要專業商務風格的 PPT 投影片
  - 觸發詞：「做簡報」、「製作 PPT」、「符合 Pigo 風格」、「pigo-ppt-style」、「Q3 OKR 簡報」
---

# Pigo PPT Style Skill

## Overview

Pigo 品牌專屬的 PPT 簡報風格模板，提供一致的色彩、字體、與版型設計系統。

## Brand Colors

| 用途 | 色值 | 說明 |
|------|------|------|
| Primary Blue | `#3B82F6` | 主要按鈕、連結、重點標示 |
| Secondary Purple | `#8B5CF6` | 強調元素、圖表輔助 |
| Background | `#FFFFFF` | 頁面背景 |
| Surface | `#F9FAFB` | 卡片背景 |
| Text Primary | `#111827` | 主要文字 |
| Text Secondary | `#6B7280` | 次要文字 |
| Accent Cyan | `#06B6D4` | 科技感輔助色 |
| Success Green | `#10B981` | 正向指標、成功狀態 |
| Warning Orange | `#F59E0B` | 警告、注意 |
| Error Red | `#EF4444` | 錯誤、風險 |

## Typography System

```
主要字體：Inter, system-ui, sans-serif
備用字體：Arial, "Helvetica Neue", sans-serif

權級與尺寸：
- H1: 48-56px, Bold (封面標題)
- H2: 32-36px, Bold (頁面標題)
- H3: 24-28px, SemiBold (章節標題)
- H4: 20-22px, Bold (卡片標題)
- Body: 16-18px, Regular (內文)
- Caption: 14px, Regular (註解)
- Footnote: 12px, Regular (頁碼/日期)
```

## PPT Layout System

### Canvas Format
- **Standard**: 16:9 (1280×720px)
- **viewBox**: `0 0 1280 720`
- **Safe Margin**: 60px (left/right), 50px (top/bottom)

### Page Types

| 頁面類型 | 特色 | 適用場景 |
|----------|------|----------|
| Cover | 深色背景 + 品牌藍強調 | 封面 |
| Chapter | 淺色背景 + 大標題 | 章節頁 |
| Content | 白底 + 圖文混排 | 內容頁 |
| Data | 圖表+數據展示 | 統計圖表 |
| Ending | 結語 + 行動呼籲 | 結尾頁 |

## Design Principles

1. **結論優先**: 每頁標題就是核心訊息
2. **品牌一致性**: 嚴格使用品牌色彩系統
3. **留白呼吸**: 內容比例 < 65%
4. **層次清晰**: 標題 → 內文 → 輔助資訊
5. **圖表專業**: 使用品牌色彩對應數據維度

## Quick Usage

When creating a PPT with Pigo style:

1. Set primary color: `#3B82F6`
2. Set secondary color: `#8B5CF6`
3. Use Inter font family
4. Follow 16:9 aspect ratio
5. Keep content under 65% area

## Aesthetic Modules

除了 Pigo 品牌預設風格外，支援以下美學參考模組：

| 模組 | 觸發關鍵詞 | 用途 |
|------|-----------|------|
| **Bauhaus** | 「包浩斯」「Bauhaus」「幾何簡約」 | 海報、產品、室內、建築視覺，結構性幾何美學 |

### Bauhaus 模組

當用戶要求包浩斯風格時，調用 `references/bauhaus-aesthetic.md`：
- 媒介選擇：海報 / 產品 / 室內 / 建築
- 骨架 Prompt 結構
- 色彩系統（經典五色 + 進階色調）
- 四種構圖關係
- 質感處理原則
- 與 Pigo 品牌色彩整合方式

## Resources

- `references/pigo-colors.json` - 完整色彩系統 (CSS variables)
- `references/design-spec.md` - 詳細設計規範
- `references/bauhaus-aesthetic.md` - 包豪斯美學設計參考（2026-06-26）
- `assets/pigo-style-layouts/` - 頁面模板 SVG 檔案