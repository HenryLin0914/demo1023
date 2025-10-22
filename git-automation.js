#!/usr/bin/env node

/**
 * Git 自動化工具
 * 使用 Node.js 和 simple-git 庫實現自動 commit 和 push
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class GitAutomation {
    constructor() {
        this.repository = 'HenryLin0914/demo1023';
        this.branch = 'main';
        this.autoPush = true;
        this.checkInterval = 30000; // 30秒
        this.isRunning = false;
    }

    // 檢查是否有變更
    hasChanges() {
        try {
            const status = execSync('git status --porcelain', { encoding: 'utf8' });
            return status.trim().length > 0;
        } catch (error) {
            console.error('❌ 檢查 Git 狀態失敗:', error.message);
            return false;
        }
    }

    // 獲取變更檔案列表
    getChangedFiles() {
        try {
            const files = execSync('git diff --name-only', { encoding: 'utf8' });
            return files.trim().split('\n').filter(f => f);
        } catch (error) {
            return [];
        }
    }

    // 獲取已暫存檔案列表
    getStagedFiles() {
        try {
            const files = execSync('git diff --cached --name-only', { encoding: 'utf8' });
            return files.trim().split('\n').filter(f => f);
        } catch (error) {
            return [];
        }
    }

    // 生成智能 commit 訊息
    generateCommitMessage() {
        const now = new Date();
        const timestamp = now.toLocaleString('zh-TW');
        const changedFiles = this.getChangedFiles();
        const stagedFiles = this.getStagedFiles();
        
        let message = `Auto commit: ${timestamp}\n\n`;
        
        // 分析變更類型
        const fileTypes = this.analyzeFileTypes([...changedFiles, ...stagedFiles]);
        
        if (fileTypes.html > 0) message += '🌐 更新 HTML 檔案\n';
        if (fileTypes.js > 0) message += '⚡ 更新 JavaScript 檔案\n';
        if (fileTypes.css > 0) message += '🎨 更新樣式檔案\n';
        if (fileTypes.json > 0) message += '📋 更新配置檔案\n';
        if (fileTypes.md > 0) message += '📝 更新文檔檔案\n';
        
        message += '\n變更檔案:\n';
        [...new Set([...changedFiles, ...stagedFiles])].forEach(file => {
            message += `- ${file}\n`;
        });
        
        return message;
    }

    // 分析檔案類型
    analyzeFileTypes(files) {
        const types = { html: 0, js: 0, css: 0, json: 0, md: 0, other: 0 };
        
        files.forEach(file => {
            if (file.endsWith('.html')) types.html++;
            else if (file.endsWith('.js')) types.js++;
            else if (file.endsWith('.css')) types.css++;
            else if (file.endsWith('.json')) types.json++;
            else if (file.endsWith('.md')) types.md++;
            else types.other++;
        });
        
        return types;
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
            console.log('💬 Commit 訊息:');
            console.log(commitMessage);

            // 執行 commit
            console.log('📝 執行 commit...');
            execSync(`git commit -m "${commitMessage}"`, { stdio: 'inherit' });

            console.log('✅ Commit 成功!');

            // 如果啟用自動推送
            if (this.autoPush) {
                console.log('🚀 推送到遠端倉庫...');
                execSync('git push origin main', { stdio: 'inherit' });
                console.log('✅ 推送成功!');
            }

        } catch (error) {
            console.error('❌ 自動 commit 失敗:', error.message);
        }
    }

    // 手動執行 commit
    async manualCommit(customMessage = null) {
        console.log('🔧 手動執行 commit...');
        
        if (customMessage) {
            console.log('💬 使用自訂訊息:', customMessage);
            execSync(`git commit -m "${customMessage}"`, { stdio: 'inherit' });
        } else {
            await this.performAutoCommit();
        }
        
        if (this.autoPush) {
            execSync('git push origin main', { stdio: 'inherit' });
        }
    }

    // 啟動自動監控
    start() {
        if (this.isRunning) {
            console.log('⚠️  自動化已在運行中');
            return;
        }

        console.log('🚀 啟動 Git 自動化監控...');
        console.log(`📊 檢查間隔: ${this.checkInterval / 1000}秒`);
        console.log(`📦 倉庫: ${this.repository}`);
        console.log(`🌿 分支: ${this.branch}`);
        console.log(`🚀 自動推送: ${this.autoPush ? '啟用' : '停用'}`);

        this.isRunning = true;

        // 立即執行一次檢查
        this.performAutoCommit();

        // 設定定時檢查
        this.intervalId = setInterval(() => {
            this.performAutoCommit();
        }, this.checkInterval);
    }

    // 停止監控
    stop() {
        if (!this.isRunning) {
            console.log('⚠️  自動化未在運行');
            return;
        }

        console.log('🛑 停止 Git 自動化監控...');
        this.isRunning = false;
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    // 顯示狀態
    showStatus() {
        console.log('📊 Git 自動化狀態:');
        console.log(`- 運行中: ${this.isRunning ? '是' : '否'}`);
        console.log(`- 有變更: ${this.hasChanges() ? '是' : '否'}`);
        console.log(`- 變更檔案: ${this.getChangedFiles().length} 個`);
        console.log(`- 已暫存: ${this.getStagedFiles().length} 個`);
        
        try {
            const lastCommit = execSync('git log -1 --pretty=%B', { encoding: 'utf8' }).trim();
            console.log(`- 最後 commit: ${lastCommit.substring(0, 50)}...`);
        } catch (error) {
            console.log('- 最後 commit: 無');
        }
    }
}

// 主程式
const gitAutomation = new GitAutomation();

// 處理命令行參數
const args = process.argv.slice(2);
const command = args[0];
const customMessage = args[1];

switch (command) {
    case 'start':
        gitAutomation.start();
        break;
    case 'stop':
        gitAutomation.stop();
        break;
    case 'commit':
        gitAutomation.manualCommit(customMessage);
        break;
    case 'status':
        gitAutomation.showStatus();
        break;
    default:
        console.log(`
🤖 Git 自動化工具

使用方法:
  node git-automation.js start                    - 啟動自動監控
  node git-automation.js stop                     - 停止自動監控
  node git-automation.js commit [自訂訊息]        - 手動執行 commit
  node git-automation.js status                   - 查看狀態

功能特色:
  ✅ 自動檢測檔案變更
  ✅ 智能生成 commit 訊息
  ✅ 檔案類型分析
  ✅ 自動推送到遠端
  ✅ 完整的錯誤處理
        `);
}

// 優雅退出
process.on('SIGINT', () => {
    console.log('\n👋 收到中斷信號，正在停止...');
    gitAutomation.stop();
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n👋 收到終止信號，正在停止...');
    gitAutomation.stop();
    process.exit(0);
});
