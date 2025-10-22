#!/usr/bin/env node

/**
 * 簡單的檔案伺服器
 * 提供檔案總管 API 支援
 */

const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3000;

// 啟用 CORS
app.use(cors());

// 解析 JSON
app.use(express.json());

// 靜態檔案服務
app.use(express.static('.'));

// 檔案總管 API
app.get('/api/files', async (req, res) => {
    try {
        const { path: dirPath } = req.query;
        
        if (!dirPath) {
            return res.status(400).json({ error: '缺少路徑參數' });
        }

        // 安全檢查：防止路徑遍歷攻擊
        const safePath = path.resolve(dirPath);
        const rootPath = path.resolve('.');
        
        if (!safePath.startsWith(rootPath)) {
            return res.status(403).json({ error: '無權限訪問此路徑' });
        }

        // 檢查路徑是否存在
        if (!fs.existsSync(safePath)) {
            return res.status(404).json({ error: '路徑不存在' });
        }

        // 讀取目錄內容
        const files = await readDirectory(safePath);
        res.json(files);

    } catch (error) {
        console.error('讀取目錄失敗:', error);
        res.status(500).json({ error: '讀取目錄失敗: ' + error.message });
    }
});

// 讀取目錄內容
async function readDirectory(dirPath) {
    const files = [];
    
    try {
        const entries = fs.readdirSync(dirPath, { withFileTypes: true });
        
        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);
            const stats = fs.statSync(fullPath);
            
            const file = {
                name: entry.name,
                type: entry.isDirectory() ? 'folder' : getFileType(entry.name),
                size: formatFileSize(stats.size),
                icon: getFileIcon(entry.name, entry.isDirectory()),
                isDirectory: entry.isDirectory(),
                modified: stats.mtime.toISOString(),
                path: fullPath
            };
            
            files.push(file);
        }
        
        // 排序：資料夾在前，檔案在後
        files.sort((a, b) => {
            if (a.isDirectory && !b.isDirectory) return -1;
            if (!a.isDirectory && b.isDirectory) return 1;
            return a.name.localeCompare(b.name);
        });
        
    } catch (error) {
        console.error('讀取目錄失敗:', error);
        throw error;
    }
    
    return files;
}

// 格式化檔案大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// 獲取檔案類型
function getFileType(filename) {
    const ext = path.extname(filename).toLowerCase().slice(1);
    const typeMap = {
        'html': 'html',
        'htm': 'html',
        'css': 'css',
        'js': 'js',
        'json': 'json',
        'md': 'md',
        'txt': 'text',
        'png': 'image',
        'jpg': 'image',
        'jpeg': 'image',
        'gif': 'image',
        'svg': 'image',
        'pdf': 'pdf',
        'zip': 'archive',
        'rar': 'archive'
    };
    return typeMap[ext] || 'file';
}

// 獲取檔案圖示
function getFileIcon(filename, isDirectory) {
    if (isDirectory) return '📁';
    
    const ext = path.extname(filename).toLowerCase().slice(1);
    const iconMap = {
        'html': '🌐',
        'htm': '🌐',
        'css': '🎨',
        'js': '⚡',
        'json': '⚙️',
        'md': '📝',
        'txt': '📄',
        'png': '🖼️',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'gif': '🖼️',
        'svg': '🖼️',
        'pdf': '📄',
        'zip': '📦',
        'rar': '📦'
    };
    return iconMap[ext] || '📄';
}

// 啟動伺服器
app.listen(PORT, () => {
    console.log(`🚀 檔案伺服器已啟動`);
    console.log(`📡 服務地址: http://localhost:${PORT}`);
    console.log(`📁 檔案總管 API: http://localhost:${PORT}/api/files`);
    console.log(`🌐 主頁面: http://localhost:${PORT}/index.html`);
    console.log('');
    console.log('💡 使用說明:');
    console.log('1. 開啟瀏覽器訪問 http://localhost:3000');
    console.log('2. 點擊專案卡片的 "📁 檔案" 按鈕');
    console.log('3. 瀏覽專案目錄下的所有檔案');
});

// 優雅關閉
process.on('SIGINT', () => {
    console.log('\n👋 正在關閉伺服器...');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n👋 正在關閉伺服器...');
    process.exit(0);
});
