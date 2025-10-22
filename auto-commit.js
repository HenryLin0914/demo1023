#!/usr/bin/env node

/**
 * 自動 GitHub Commit & Push 腳本
 * 使用 MCP GitHub 工具自動提交和推送變更
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
    repository: 'HenryLin0914/demo1023',
    branch: 'main',
    commitMessage: 'Auto commit: 更新專案檔案',
    autoPush: true,
    checkInterval: 30000, // 30秒檢查一次
    excludeFiles: ['.git', 'node_modules', '.DS_Store', '.history']
};

class AutoCommit {
    constructor() {
        this.isRunning = false;
        this.lastCommitHash = this.getLastCommitHash();
    }

    // 獲取最後一次 commit hash
    getLastCommitHash() {
        try {
            return execSync('git rev-parse HEAD', { encoding: 'utf8' }).trim();
        } catch (error) {
            return null;
        }
    }

    // 檢查是否有變更
    hasChanges() {
        try {
            const status = execSync('git status --porcelain', { encoding: 'utf8' });
            return status.trim().length > 0;
        } catch (error) {
            console.error('檢查 Git 狀態時發生錯誤:', error.message);
            return false;
        }
    }

    // 獲取變更的檔案列表
    getChangedFiles() {
        try {
            const files = execSync('git diff --name-only', { encoding: 'utf8' });
            const stagedFiles = execSync('git diff --cached --name-only', { encoding: 'utf8' });
            return {
                unstaged: files.trim().split('\n').filter(f => f),
                staged: stagedFiles.trim().split('\n').filter(f => f)
            };
        } catch (error) {
            return { unstaged: [], staged: [] };
        }
    }

    // 生成 commit 訊息
    generateCommitMessage() {
        const now = new Date();
        const timestamp = now.toLocaleString('zh-TW');
        const changedFiles = this.getChangedFiles();
        
        let message = `Auto commit: ${timestamp}\n\n`;
        
        if (changedFiles.staged.length > 0) {
            message += `已暫存檔案:\n${changedFiles.staged.map(f => `- ${f}`).join('\n')}\n\n`;
        }
        
        if (changedFiles.unstaged.length > 0) {
            message += `未暫存檔案:\n${changedFiles.unstaged.map(f => `- ${f}`).join('\n')}`;
        }
        
        return message;
    }

    // 執行自動 commit
    async performAutoCommit() {
        try {
            console.log('🔄 開始自動 commit 流程...');
            
            // 檢查是否有變更
            if (!this.hasChanges()) {
                console.log('✅ 沒有變更需要提交');
                return;
            }

            // 添加所有變更
            console.log('📁 添加檔案到暫存區...');
            execSync('git add .', { stdio: 'inherit' });

            // 生成 commit 訊息
            const commitMessage = this.generateCommitMessage();
            console.log('💬 Commit 訊息:', commitMessage);

            // 執行 commit
            console.log('📝 執行 commit...');
            execSync(`git commit -m "${commitMessage}"`, { stdio: 'inherit' });

            // 更新最後 commit hash
            this.lastCommitHash = this.getLastCommitHash();
            console.log('✅ Commit 成功!');

            // 如果啟用自動推送
            if (CONFIG.autoPush) {
                console.log('🚀 推送到遠端倉庫...');
                execSync('git push origin main', { stdio: 'inherit' });
                console.log('✅ 推送成功!');
            }

        } catch (error) {
            console.error('❌ 自動 commit 失敗:', error.message);
        }
    }

    // 開始監控
    start() {
        if (this.isRunning) {
            console.log('⚠️  自動 commit 已在運行中');
            return;
        }

        console.log('🚀 啟動自動 commit 監控...');
        console.log(`📊 檢查間隔: ${CONFIG.checkInterval / 1000}秒`);
        console.log(`📦 倉庫: ${CONFIG.repository}`);
        console.log(`🌿 分支: ${CONFIG.branch}`);
        console.log(`🚀 自動推送: ${CONFIG.autoPush ? '啟用' : '停用'}`);

        this.isRunning = true;

        // 立即執行一次檢查
        this.performAutoCommit();

        // 設定定時檢查
        this.intervalId = setInterval(() => {
            this.performAutoCommit();
        }, CONFIG.checkInterval);
    }

    // 停止監控
    stop() {
        if (!this.isRunning) {
            console.log('⚠️  自動 commit 未在運行');
            return;
        }

        console.log('🛑 停止自動 commit 監控...');
        this.isRunning = false;
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    // 手動執行一次 commit
    async manualCommit() {
        console.log('🔧 手動執行 commit...');
        await this.performAutoCommit();
    }
}

// 主程式
const autoCommit = new AutoCommit();

// 處理命令行參數
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
    case 'start':
        autoCommit.start();
        break;
    case 'stop':
        autoCommit.stop();
        break;
    case 'commit':
        autoCommit.manualCommit();
        break;
    case 'status':
        console.log('📊 當前狀態:');
        console.log(`- 運行中: ${autoCommit.isRunning ? '是' : '否'}`);
        console.log(`- 有變更: ${autoCommit.hasChanges() ? '是' : '否'}`);
        console.log(`- 最後 commit: ${autoCommit.lastCommitHash || '無'}`);
        break;
    default:
        console.log(`
🤖 自動 GitHub Commit & Push 工具

使用方法:
  node auto-commit.js start    - 啟動自動監控
  node auto-commit.js stop     - 停止自動監控
  node auto-commit.js commit   - 手動執行一次 commit
  node auto-commit.js status   - 查看當前狀態

配置:
  - 檢查間隔: ${CONFIG.checkInterval / 1000}秒
  - 倉庫: ${CONFIG.repository}
  - 分支: ${CONFIG.branch}
  - 自動推送: ${CONFIG.autoPush ? '啟用' : '停用'}
        `);
}

// 優雅退出
process.on('SIGINT', () => {
    console.log('\n👋 收到中斷信號，正在停止...');
    autoCommit.stop();
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n👋 收到終止信號，正在停止...');
    autoCommit.stop();
    process.exit(0);
});
