---
name: "Remotion"
description: "基於 React 的程式化影片製作框架指南。涵蓋專案結構、核心 Hook、時間軸管理與渲染規則。"
docs_url: "https://www.remotion.dev/docs/"
tags: ["react", "video-generation", "animation", "frontend"]
version: "1.0"
post_task_action: "播放系統音效: C:\\Windows\\Media\\Windows Ding.wav"
---

# Remotion 開發指南

**Remotion** 是一個透過 React 程式碼與逐幀渲染 (Frame-by-frame rendering) 來生成 MP4 影片的框架。它允許開發者使用熟悉的 React/CSS 技術棧來建立動態影像。

## 1. 專案結構 (Project Structure)

### Root (src/Root.tsx)
整個影片專案的入口點，用於定義 `Composition`。

### Composition Component
定義影片輸出的核心設定。

| 屬性 (Prop) | 描述 | 預設值 |
| :--- | :--- | :--- |
| `id` | 唯一識別碼 (Render ID) | "MyComp" |
| `component` | 要渲染的 React 元件 | - |
| `durationInFrames` | 影片總幀數 | - |
| `width` | 影片寬度 | 1920 |
| `height` | 影片高度 | 1080 |
| `fps` | 幀率 (Frames Per Second) | 30 |
| `defaultProps` | 傳遞給組件的預設屬性物件 | {} |

---

## 2. 核心概念 (Core Concepts)

### Frame Access
* **Hook:** `useCurrentFrame()`
* **用途:** 獲取當前幀數 (從 0 開始)，是用於驅動所有動畫的基礎數值。

### Config Access
* **Hook:** `useVideoConfig()`
* **用途:** 獲取影片配置資訊，如 `fps`, `durationInFrames`, `width`, `height`。

### 渲染規則 (Rendering Rules)
1.  **確定性 (Deterministic):** 渲染結果必須可重現。禁止使用原生的 `Math.random()`，應改用 Remotion 提供的 `random(seed)`。
2.  **無副作用:** 禁止在渲染過程中產生副作用 (No `useEffect` for logic that affects layout)。
3.  **專用標籤:** 影片與音訊需使用 Remotion 提供的專用標籤 (`<Video>`, `<Audio>`) 以確保同步。

---

## 3. 媒體組件 (Media Components)

| 類型 | 組件標籤 | 關鍵屬性 | 備註 |
| :--- | :--- | :--- | :--- |
| **Video** | `<OffthreadVideo />` | `src`, `startFrom`, `endAt`, `volume` | 用於嵌入外部影片檔案。 |
| **Image** | `<Img />` | `src` | 靜態圖片顯示。 |
| **GIF** | `<Gif />` | `src`, `playbackRate` | 需安裝 `@remotion/gif` 套件。 |
| **Audio** | `<Audio />` | `src`, `startFrom`, `endAt`, `volume` | 支援本地 (使用 `staticFile`) 或遠端 URL。 |

---

## 4. 佈局與時間軸 (Layout & Sequencing)

Remotion 提供了一套強大的時間軸管理機制，讓開發者能精確控制元素出現的時機。

### AbsoluteFill
* **組件:** `<AbsoluteFill>`
* **用途:** 用於將元素重疊 (Layering)，類似 CSS 的 `position: absolute; top: 0; left: 0; right: 0; bottom: 0;`。

### Sequence
* **組件:** `<Sequence>`
* **行為:** 創造一個新的時間軸上下文。子元件的 `frame` 計數會在此區域內重置為 0。
* **屬性:**
    * `from`: 開始出現的幀數。
    * `durationInFrames`: 持續時間。

### Series
* **組件:** `<Series>`
* **行為:** 自動依序排列多個 `<Series.Sequence>`，無需手動計算 `from`。
* **用途:** 製作依序播放的場景或清單動畫。

---

## 5. 動畫與物理 (Animation & Physics)

### 插值 (Interpolation)
將幀數映射到動畫屬性值。

```javascript
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});