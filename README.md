# Version Sync Checker

自動化執行專案版本號的一致性檢查與同步，確保全專案的文件與程式碼共享單一的事實來源。

## 📏 版本規則
遵循特定的進位規則（PATCH/MINOR 滿 10 進位）：
- **PATCH**: 滿 10 次進位至 MINOR (e.g., 1.2.9 -> 1.3.0)。
- **MINOR**: 滿 10 次進位至 MAJOR (e.g., 1.9.0 -> 2.0.0)。
- **MAJOR**: 不相容的重大變更。

## 🔍 同步對象
- **Source of Truth**: `CHANGELOG.md`
- **YAML 標頭**: `project_version` 與 `document_version`。
- **設定檔**: `package.json` 等。
- **程式碼**: 原始碼中的版本常數。

## 🛠 使用方法
1. **執行檢查**：
   ```bash
   python3 scripts/check_version.py [project_root]
   ```
2. **分析報告**：檢閱輸出的 JSON 報告。
3. **自動同步**：根據報告更新相關文件的 YAML 標頭與版本字串。

## 📂 目錄結構
- `scripts/`: 包含 `check_version.py` 檢查邏輯。
- `SKILL.md`: 詳細的版本遞增與同步執行規範。
