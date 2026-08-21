---
name: vault-bootstrap
description: Use when initializing a brand-new vault or workspace that needs first-time structure, conventions, templates, and navigation rather than maintenance on an already mature vault.
---

# Vault Bootstrap

## Description

`vault-bootstrap` 是新 vault / 新 workspace 的起始建置 skill。  
它不適合直接拿來重做成熟中的 Pigo 主 vault；在目前 Codex runtime 中，應把它視為規劃與初始化入口，而不是日常維護工具。

## Current Mode

目前為 deferred-mode 安裝版本：

- 可用來規劃新 vault 的初始化結構
- 可用來定義基本分類、模板與導航層
- 不應直接重做既有成熟 vault 的骨架

## Handoff

成熟 vault 的日常維護請改用：

- `vault-check`
- `vault-reshape`
- `vault-GPS`
