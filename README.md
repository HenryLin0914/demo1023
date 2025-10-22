# 🤖 自動 GitHub Commit & Push 工具

這個專案提供了多種方式來實現自動 GitHub commit 和 push 功能。

## 🚀 功能特色

- ✅ 自動檢測檔案變更
- ✅ 智能生成 commit 訊息
- ✅ 自動推送到遠端倉庫
- ✅ 支援 MCP GitHub 工具整合
- ✅ 可配置的檢查間隔
- ✅ 優雅的錯誤處理

## 📦 安裝與使用

### 方法一：使用 Node.js 腳本

```bash
# 啟動自動 commit 監控
node auto-commit.js start

# 手動執行一次 commit
node auto-commit.js commit

# 查看當前狀態
node auto-commit.js status

# 停止自動監控
node auto-commit.js stop
```

### 方法二：使用 MCP GitHub 工具

```bash
# 啟動 MCP 自動 commit
node mcp-github-commit.js start

# 手動執行 MCP commit
node mcp-github-commit.js commit
```

## ⚙️ 配置選項

### auto-commit.js 配置

```javascript
const CONFIG = {
    repository: 'HenryLin0914/demo1023',  // GitHub 倉庫
    branch: 'main',                        // 分支名稱
    commitMessage: 'Auto commit: 更新專案檔案',  // 預設 commit 訊息
    autoPush: true,                        // 是否自動推送
    checkInterval: 30000,                  // 檢查間隔（毫秒）
    excludeFiles: ['.git', 'node_modules', '.DS_Store', '.history']  // 排除檔案
};
```

## 🔧 使用 MCP GitHub 工具

如果您想使用 MCP GitHub 工具，可以這樣整合：

```javascript
// 在您的 MCP 環境中
const mcpGitHub = require('@modelcontextprotocol/server-github');

// 創建 commit
const result = await mcpGitHub.createCommit({
    repository: 'HenryLin0914/demo1023',
    branch: 'main',
    message: 'Auto commit via MCP',
    files: ['index.html', 'auto-commit.js']
});
```

## 📊 監控功能

### 自動監控
- 每30秒檢查一次檔案變更
- 自動添加所有變更檔案
- 生成詳細的 commit 訊息
- 自動推送到遠端倉庫

### 手動操作
- 隨時可以手動執行 commit
- 查看當前 Git 狀態
- 停止/啟動自動監控

## 🛠️ 進階功能

### 智能 Commit 訊息
腳本會自動生成包含以下資訊的 commit 訊息：
- 時間戳記
- 已暫存檔案列表
- 未暫存檔案列表

### 錯誤處理
- Git 操作失敗時會顯示詳細錯誤訊息
- 網路問題時會重試推送
- 優雅的中斷處理

### 日誌記錄
- 詳細的操作日誌
- 變更檔案追蹤
- 成功/失敗狀態記錄

## 🚀 快速開始

1. **啟動自動監控**：
   ```bash
   node auto-commit.js start
   ```

2. **檢查狀態**：
   ```bash
   node auto-commit.js status
   ```

3. **手動 commit**：
   ```bash
   node auto-commit.js commit
   ```

## 📝 注意事項

- 確保 Git 已正確配置
- 確保有 GitHub 倉庫的推送權限
- 建議在測試環境中先試用
- 可以調整檢查間隔以符合需求

## 🔗 相關連結

- [GitHub 倉庫](https://github.com/HenryLin0914/demo1023)
- [GitHub Actions 文檔](https://docs.github.com/en/actions)
- [Git 官方文檔](https://git-scm.com/doc)
- [Node.js Git 自動化](https://github.com/steveukx/git-js)
