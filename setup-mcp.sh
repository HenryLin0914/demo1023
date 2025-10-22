#!/bin/bash

# MCP Git 工作流設定腳本
# 這個腳本會設定 MCP GitHub 工具和相關依賴

echo "🚀 設定 MCP Git 工作流工具..."

# 檢查 Node.js 是否已安裝
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安裝，請先安裝 Node.js"
    exit 1
fi

# 檢查 npm 是否已安裝
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安裝，請先安裝 npm"
    exit 1
fi

echo "✅ Node.js 和 npm 已安裝"

# 安裝 MCP GitHub 工具
echo "📦 安裝 MCP GitHub 工具..."
npm install -g @modelcontextprotocol/server-github

# 安裝其他必要的依賴
echo "📦 安裝其他依賴..."
npm install

# 設定 Git 認證（如果需要）
echo "🔐 設定 Git 認證..."
echo "請確保您已設定 GitHub Personal Access Token"
echo "您可以在 GitHub Settings > Developer settings > Personal access tokens 中建立"

# 建立 .env 檔案（如果不存在）
if [ ! -f .env ]; then
    echo "📝 建立 .env 檔案..."
    cat > .env << EOF
# GitHub Personal Access Token
GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here

# MCP 設定
MCP_SERVER_URL=http://localhost:3000
MCP_REPOSITORY=HenryLin0914/demo1023
MCP_BRANCH=main
EOF
    echo "✅ .env 檔案已建立，請編輯並填入您的 GitHub token"
fi

# 設定執行權限
chmod +x mcp-git-workflow.js
chmod +x auto-commit.js
chmod +x mcp-github-commit.js

echo "✅ 設定完成！"
echo ""
echo "📋 使用說明："
echo "1. 編輯 .env 檔案，填入您的 GitHub Personal Access Token"
echo "2. 執行 'node mcp-git-workflow.js start' 啟動自動化工作流"
echo "3. 執行 'node mcp-git-workflow.js status' 查看狀態"
echo ""
echo "🔗 相關連結："
echo "- GitHub Personal Access Token: https://github.com/settings/tokens"
echo "- MCP GitHub 工具文檔: https://github.com/modelcontextprotocol/servers/tree/main/src/github"
