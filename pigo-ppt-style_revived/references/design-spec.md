# Pigo PPT Style - Design Specification

> Pigo 品牌 PPT 完整設計規範

---

## I. Template Overview

| Property | Description |
|----------|-------------|
| **Template Name** | Pigo PPT Style |
| **Use Cases** | Q3 OKR、公司報告、產品簡報、內部會議、商務提案 |
| **Design Tone** | 專業、現代、清晰、品牌一致性 |
| **Theme Mode** | 淺色背景為主，深色用於封面/章節頁 |

---

## II. Canvas Specification

| Property | Value |
|----------|-------|
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 × 720 px |
| **viewBox** | `0 0 1280 720` |
| **Safe Margins** | 60px (left/right), 50px (top/bottom) |
| **Content Area** | x: 60-1220, y: 100-670 |
| **Title Area** | y: 50-100 |
| **Grid Base** | 40px |

---

## III. Color Scheme

### Primary Colors

| Role | Value | Usage |
|------|-------|-------|
| **Pigo Blue** | `#3B82F6` | Brand identity, title emphasis, key data, primary buttons |
| **Pigo Purple** | `#8B5CF6` | Secondary emphasis, chart accents |
| **Pigo Cyan** | `#06B6D4` | Tech accents, highlights |

### Neutral Colors

| Role | Value | Usage |
|------|-------|-------|
| **White** | `#FFFFFF` | Page background, content pages |
| **Surface** | `#F9FAFB` | Card backgrounds |
| **Text Primary** | `#111827` | Body text, headings |
| **Text Secondary** | `#6B7280` | Labels, captions |
| **Border Light** | `#E5E7EB` | Dividers, card borders |

### Status Colors

| Role | Value | Usage |
|------|-------|-------|
| Success | `#10B981` | Positive indicators |
| Warning | `#F59E0B` | Caution states |
| Error | `#EF4444` | Risks, negative indicators |

---

## IV. Typography System

### Font Stack

```
Font Stack: Inter, Arial, "Helvetica Neue", "Segoe UI", system-ui, sans-serif
```

### Font Size Hierarchy

| Level | Usage | Size | Weight |
|-------|-------|------|--------|
| H1 | Cover main title | 56px | Bold (700) |
| H2 | Page title | 32-36px | Bold (700) |
| H3 | Section title | 24-28px | SemiBold (600) |
| H4 | Card title | 20-22px | Bold (700) |
| Body | Content text | 16-18px | Regular (400) |
| Caption | Labels, footnotes | 14px | Regular (400) |
| Page | Page numbers | 12px | Regular (400) |

---

## V. Page Structure

### General Layout

| Area | Position | Description |
|------|----------|-------------|
| Top Bar | y: 0, h: 6-8px | Pigo Blue decorative bar |
| Label | y: 50-70 | Page type label (uppercase) |
| Title | y: 80-140 | Page title (core takeaway) |
| Content | y: 160-620 | Main content area |
| Footer | y: 680 | Page number (centered) |

### Layout Types

1. **Cover**: Dark background (#111827), white text, Pigo Blue accent bar
2. **Chapter**: Light background, large centered title
3. **Content**: White background, left-aligned content, optional sidebar
4. **Data**: Charts and graphs with brand colors
5. **Ending**: Dark background, call-to-action

---

## VI. SVG Constraints

- All text in `<text>` elements (not paths)
- viewBox must match canvas dimensions
- No embedded fonts - use web-safe fonts
- Keep file size under 100KB per page
- Use `<g>` groups with descriptive IDs for animation