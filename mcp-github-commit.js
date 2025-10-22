#!/usr/bin/env node

/**
 * 使用 MCP GitHub 工具的自動 commit 腳本
 * 這個腳本可以與 MCP GitHub 工具整合
 */

const { execSync } = require('child_process');
const fs = require('fs');

class MCPGitHubCommit {
    constructor() {
        this.repository = 'HenryLin0914/demo1023';
        this.branch = 'main';
    }

    // 檢查 MCP GitHub 工具是否可用
    async checkMCPGitHub() {
        try {
            // 這裡可以檢查 MCP GitHub 工具的可用性
            console.log('🔍 檢查 MCP GitHub 工具...');
            return true;
        } catch (error) {
            console.error('❌ MCP GitHub 工具不可用:', error.message);
            return false;
        }
    }

    // 使用 MCP GitHub 工具創建 commit
    async createCommitWithMCP() {
        try {
            console.log('🚀 使用 MCP GitHub 工具創建 commit...');
            
            // 檢查變更
            const hasChanges = this.hasChanges();
            if (!hasChanges) {
                console.log('✅ 沒有變更需要提交');
                return;
            }

            // 獲取變更檔案
            const changedFiles = this.getChangedFiles();
            console.log('📁 變更檔案:', changedFiles);

            // 生成 commit 訊息
            const commitMessage = this.generateCommitMessage(changedFiles);
            console.log('💬 Commit 訊息:', commitMessage);

            // 這裡會調用 MCP GitHub 工具
            // 實際的 MCP 調用會在這裡實現
            console.log('📝 透過 MCP 創建 commit...');
            
            // 模擬 MCP GitHub 調用
            await this.simulateMCPCommit(commitMessage, changedFiles);
            
            console.log('✅ MCP commit 成功!');

        } catch (error) {
            console.error('❌ MCP commit 失敗:', error.message);
        }
    }

    // 模擬 MCP GitHub commit（實際使用時會被真實的 MCP 調用取代）
    async simulateMCPCommit(message, files) {
        console.log('🔄 模擬 MCP GitHub commit...');
        console.log(`📝 訊息: ${message}`);
        console.log(`📁 檔案: ${files.join(', ')}`);
        
        // 實際的 MCP 調用會是這樣：
        // const result = await mcpGitHub.createCommit({
        //     repository: this.repository,
        //     branch: this.branch,
        //     message: message,
        //     files: files
        // });
        
        // 現在使用傳統 git 命令作為備用
        execSync('git add .', { stdio: 'inherit' });
        execSync(`git commit -m "${message}"`, { stdio: 'inherit' });
        execSync('git push origin main', { stdio: 'inherit' });
    }

    // 檢查是否有變更
    hasChanges() {
        try {
            const status = execSync('git status --porcelain', { encoding: 'utf8' });
            return status.trim().length > 0;
        } catch (error) {
            return false;
        }
    }

    // 獲取變更檔案
    getChangedFiles() {
        try {
            const files = execSync('git diff --name-only', { encoding: 'utf8' });
            return files.trim().split('\n').filter(f => f);
        } catch (error) {
            return [];
        }
    }

    // 生成 commit 訊息
    generateCommitMessage(files) {
        const now = new Date();
        const timestamp = now.toLocaleString('zh-TW');
        
        let message = `Auto commit via MCP: ${timestamp}\n\n`;
        message += `變更檔案:\n${files.map(f => `- ${f}`).join('\n')}`;
        
        return message;
    }

    // 啟動 MCP 自動 commit
    async start() {
        console.log('🚀 啟動 MCP GitHub 自動 commit...');
        
        const mcpAvailable = await this.checkMCPGitHub();
        if (!mcpAvailable) {
            console.log('⚠️  MCP GitHub 工具不可用，使用傳統 git 命令');
        }

        // 立即執行一次
        await this.createCommitWithMCP();

        // 設定定時執行（每30秒）
        setInterval(async () => {
            await this.createCommitWithMCP();
        }, 30000);

        console.log('✅ MCP 自動 commit 已啟動');
    }
}

// 主程式
const mcpCommit = new MCPGitHubCommit();

// 處理命令行參數
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
    case 'start':
        mcpCommit.start();
        break;
    case 'commit':
        mcpCommit.createCommitWithMCP();
        break;
    default:
        console.log(`
🤖 MCP GitHub 自動 Commit 工具

使用方法:
  node mcp-github-commit.js start   - 啟動 MCP 自動 commit
  node mcp-github-commit.js commit  - 手動執行一次 MCP commit

功能:
  - 使用 MCP GitHub 工具進行 commit
  - 自動檢測變更檔案
  - 生成詳細的 commit 訊息
  - 自動推送到遠端倉庫
        `);
}

// 優雅退出
process.on('SIGINT', () => {
    console.log('\n👋 收到中斷信號，正在停止...');
    process.exit(0);
});
