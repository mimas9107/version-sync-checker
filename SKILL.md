---
name: version-sync-checker
description: 檢查並同步專案內所有文件的版本號。當使用者要求「檢查版本一致性」、「更新版本」、「升級專案」或在完成修復後需要遞增版本號時，請使用此 Skill。此 Skill 確保 CHANGELOG.md、README.md、SPEC.md、MEMOIR.md 的 YAML 標頭以及 package.json 和程式碼中的版本常數完全同步，並遵循 10 進位遞增規則 (PATCH/MINOR 滿 10 進位)。
---

# Version Sync Checker

此 Skill 用於自動化執行專案版本號的一致性檢查與同步。它以 `CHANGELOG.md` 為「單一事實來源 (Source of Truth)」，並確保全專案的版本標記符合 `GEMINI.md` 的規範。

## 觸發條件
- 使用者要求檢查版本一致性。
- 準備發布新版本或完成 Bug Fix 需要前進版本號。
- 任何涉及「版本」、「同步」、「一致性」的開發任務。

## 版本遞增規則 (MAJOR.MINOR.PATCH)
1. **PATCH**: Bug Fix。滿 10 次進位至 MINOR (e.g., 1.2.9 -> 1.3.0)。
2. **MINOR**: 新功能。滿 10 次進位至 MAJOR (e.g., 1.9.0 -> 2.0.0)。
3. **MAJOR**: 不相容的變更。

## 執行流程

### 1. 執行檢查腳本
使用隨附的 Python 腳本進行掃描：
```bash
python3 /home/mimas/.gemini/tmp/mimas/version-sync-checker/scripts/check_version.py [project_root]
```

### 2. 分析檢查結果
腳本會輸出 JSON 格式的報告，包含：
- `expected_version`: 來自 CHANGELOG.md 的基準版本。
- `files`: 各文件（README.md, SPEC.md, MEMOIR.md, package.json 等）的狀態：
    - `ok`: 版本一致。
    - `version_mismatch`: 版本不符。
    - `missing_header`: 缺少 YAML 標頭。
    - `missing_file`: 文件不存在。

### 3. 同步與修正
若發現不一致，請依照以下優先順序進行修正：
1. **更新 CHANGELOG.md**: 若版本號需前進，先在 CHANGELOG.md 建立新條目。
2. **更新 YAML 標頭**:
    - 更新 `project_version`。
    - 若內容有變更，更新 `modified_date` 為目前時間。
    - 根據變更程度決定是否遞增 `document_version`。
3. **更新 package.json**: 確保 `"version"` 欄位與基準一致。
4. **全域字串搜尋**: 使用 `grep_search` 搜尋舊版本號，並在程式碼中進行替換。

## YAML 標頭範例
```yaml
----
name:          "README.md"
description:   "專案說明文件"
created_date:  "2026/05/01 10:00:00"
modified_date: "2026/05/02 17:00:00"
project_version: "1.3.0"
document_version: "1.0.2"
agent_sign: ['human/name', 'gemini cli/current_agent']
----
```

## 注意事項
- **嚴禁刪除** 原始的 `agent_sign` 名單，僅能將自己加入末尾。
- 更新標頭時，務必確保 YAML 格式正確（使用 `----` 包圍）。
