#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NER 視覺化分析工具
根據不同實體類型生成對應的圖表
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from collections import Counter
import numpy as np
from typing import List, Dict, Any
import warnings
warnings.filterwarnings('ignore')

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class NERVisualizer:
    """NER 視覺化分析器"""
    
    def __init__(self):
        self.entity_colors = {
            'PERSON': '#FF6B6B',      # 紅色 - 人名
            'LOCATION': '#4ECDC4',    # 青色 - 地名
            'ORGANIZATION': '#45B7D1', # 藍色 - 組織
            'DATE': '#96CEB4',        # 綠色 - 日期
            'MONEY': '#FFEAA7',       # 黃色 - 金額
            'OTHER': '#DDA0DD'        # 紫色 - 其他
        }
    
    def load_data(self, csv_file: str) -> pd.DataFrame:
        """載入 NER 分析結果"""
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')
            return df
        except Exception as e:
            print(f"載入資料錯誤: {e}")
            return pd.DataFrame()
    
    def parse_entities(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """解析實體資料"""
        all_entities = []
        
        for _, row in df.iterrows():
            if pd.notna(row['entities']) and row['entities'] != '[]':
                try:
                    # 嘗試解析 JSON 格式的實體
                    if isinstance(row['entities'], str):
                        entities = json.loads(row['entities'])
                    else:
                        entities = row['entities']
                    
                    for entity in entities:
                        all_entities.append({
                            'text': entity.get('text', ''),
                            'label': entity.get('label', 'UNKNOWN'),
                            'confidence': entity.get('confidence', 0),
                            'text_id': row['text_id']
                        })
                except Exception as e:
                    print(f"解析實體錯誤: {e}")
                    continue
        
        return all_entities
    
    def create_entity_type_distribution(self, entities: List[Dict[str, Any]], save_path: str = None):
        """創建實體類型分布圖"""
        if not entities:
            print("沒有實體資料可視覺化")
            return
        
        # 統計實體類型
        entity_types = [entity['label'] for entity in entities]
        type_counts = Counter(entity_types)
        
        # 創建圖表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 圓餅圖
        labels = list(type_counts.keys())
        sizes = list(type_counts.values())
        colors = [self.entity_colors.get(label, self.entity_colors['OTHER']) for label in labels]
        
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('實體類型分布 - 圓餅圖', fontsize=14, fontweight='bold')
        
        # 長條圖
        bars = ax2.bar(labels, sizes, color=colors)
        ax2.set_title('實體類型分布 - 長條圖', fontsize=14, fontweight='bold')
        ax2.set_xlabel('實體類型')
        ax2.set_ylabel('數量')
        ax2.tick_params(axis='x', rotation=45)
        
        # 在長條圖上顯示數值
        for bar, size in zip(bars, sizes):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(size), ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"實體類型分布圖已保存至: {save_path}")
        
        plt.show()
    
    def create_confidence_distribution(self, entities: List[Dict[str, Any]], save_path: str = None):
        """創建可信度分布圖"""
        if not entities:
            print("沒有實體資料可視覺化")
            return
        
        confidences = [entity['confidence'] for entity in entities]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 直方圖
        ax1.hist(confidences, bins=20, color='skyblue', alpha=0.7, edgecolor='black')
        ax1.set_title('可信度分布 - 直方圖', fontsize=14, fontweight='bold')
        ax1.set_xlabel('可信度')
        ax1.set_ylabel('頻率')
        ax1.axvline(np.mean(confidences), color='red', linestyle='--', 
                   label=f'平均: {np.mean(confidences):.3f}')
        ax1.legend()
        
        # 箱線圖
        ax2.boxplot(confidences, patch_artist=True, 
                   boxprops=dict(facecolor='lightblue', alpha=0.7))
        ax2.set_title('可信度分布 - 箱線圖', fontsize=14, fontweight='bold')
        ax2.set_ylabel('可信度')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"可信度分布圖已保存至: {save_path}")
        
        plt.show()
    
    def create_entity_by_type_analysis(self, entities: List[Dict[str, Any]], save_path: str = None):
        """創建各類型實體的詳細分析"""
        if not entities:
            print("沒有實體資料可視覺化")
            return
        
        # 按類型分組
        entity_groups = {}
        for entity in entities:
            label = entity['label']
            if label not in entity_groups:
                entity_groups[label] = []
            entity_groups[label].append(entity)
        
        # 計算每個類型的統計資訊
        stats = {}
        for label, group in entity_groups.items():
            confidences = [e['confidence'] for e in group]
            stats[label] = {
                'count': len(group),
                'avg_confidence': np.mean(confidences),
                'min_confidence': np.min(confidences),
                'max_confidence': np.max(confidences)
            }
        
        # 創建圖表
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. 各類型實體數量
        labels = list(stats.keys())
        counts = [stats[label]['count'] for label in labels]
        colors = [self.entity_colors.get(label, self.entity_colors['OTHER']) for label in labels]
        
        bars1 = ax1.bar(labels, counts, color=colors)
        ax1.set_title('各類型實體數量', fontsize=14, fontweight='bold')
        ax1.set_ylabel('數量')
        ax1.tick_params(axis='x', rotation=45)
        
        for bar, count in zip(bars1, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom')
        
        # 2. 各類型平均可信度
        avg_confidences = [stats[label]['avg_confidence'] for label in labels]
        bars2 = ax2.bar(labels, avg_confidences, color=colors)
        ax2.set_title('各類型平均可信度', fontsize=14, fontweight='bold')
        ax2.set_ylabel('平均可信度')
        ax2.tick_params(axis='x', rotation=45)
        ax2.set_ylim(0, 1)
        
        for bar, conf in zip(bars2, avg_confidences):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{conf:.3f}', ha='center', va='bottom')
        
        # 3. 各類型可信度分布（箱線圖）
        confidence_data = []
        confidence_labels = []
        for label, group in entity_groups.items():
            confidences = [e['confidence'] for e in group]
            confidence_data.append(confidences)
            confidence_labels.append(label)
        
        box_plot = ax3.boxplot(confidence_data, labels=confidence_labels, patch_artist=True)
        for patch, label in zip(box_plot['boxes'], confidence_labels):
            patch.set_facecolor(self.entity_colors.get(label, self.entity_colors['OTHER']))
            patch.set_alpha(0.7)
        
        ax3.set_title('各類型可信度分布', fontsize=14, fontweight='bold')
        ax3.set_ylabel('可信度')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # 4. 各類型實體詳細統計表
        ax4.axis('tight')
        ax4.axis('off')
        
        table_data = []
        for label in labels:
            table_data.append([
                label,
                stats[label]['count'],
                f"{stats[label]['avg_confidence']:.3f}",
                f"{stats[label]['min_confidence']:.3f}",
                f"{stats[label]['max_confidence']:.3f}"
            ])
        
        table = ax4.table(cellText=table_data,
                         colLabels=['類型', '數量', '平均可信度', '最低可信度', '最高可信度'],
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)
        
        # 設定表格顏色
        for i, label in enumerate(labels):
            color = self.entity_colors.get(label, self.entity_colors['OTHER'])
            for j in range(len(table_data[0])):
                table[(i+1, j)].set_facecolor(color)
                table[(i+1, j)].set_alpha(0.3)
        
        ax4.set_title('詳細統計表', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"各類型實體分析圖已保存至: {save_path}")
        
        plt.show()
    
    def create_top_entities(self, entities: List[Dict[str, Any]], top_n: int = 10, save_path: str = None):
        """創建最常見實體排行榜"""
        if not entities:
            print("沒有實體資料可視覺化")
            return
        
        # 統計最常見的實體
        entity_texts = [entity['text'] for entity in entities]
        text_counts = Counter(entity_texts)
        top_entities = text_counts.most_common(top_n)
        
        if not top_entities:
            print("沒有找到實體")
            return
        
        # 創建圖表
        fig, ax = plt.subplots(figsize=(12, 8))
        
        texts = [item[0] for item in top_entities]
        counts = [item[1] for item in top_entities]
        
        # 根據實體類型設定顏色
        colors = []
        for text in texts:
            # 找到對應的實體類型
            entity_type = None
            for entity in entities:
                if entity['text'] == text:
                    entity_type = entity['label']
                    break
            color = self.entity_colors.get(entity_type, self.entity_colors['OTHER'])
            colors.append(color)
        
        bars = ax.barh(texts, counts, color=colors, alpha=0.7)
        ax.set_title(f'最常見實體排行榜 (前 {top_n} 名)', fontsize=14, fontweight='bold')
        ax.set_xlabel('出現次數')
        
        # 在長條上顯示數值
        for bar, count in zip(bars, counts):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                   str(count), ha='left', va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"最常見實體排行榜已保存至: {save_path}")
        
        plt.show()
    
    def create_comprehensive_analysis(self, csv_file: str, output_dir: str = "ner_analysis"):
        """創建完整的視覺化分析"""
        import os
        
        # 創建輸出目錄
        os.makedirs(output_dir, exist_ok=True)
        
        print("🔍 載入資料...")
        df = self.load_data(csv_file)
        if df.empty:
            print("❌ 無法載入資料")
            return
        
        print("📊 解析實體...")
        entities = self.parse_entities(df)
        if not entities:
            print("❌ 沒有找到實體資料")
            return
        
        print(f"✅ 找到 {len(entities)} 個實體")
        
        # 生成各種圖表
        print("\n📈 生成實體類型分布圖...")
        self.create_entity_type_distribution(entities, f"{output_dir}/entity_type_distribution.png")
        
        print("📊 生成可信度分布圖...")
        self.create_confidence_distribution(entities, f"{output_dir}/confidence_distribution.png")
        
        print("🔍 生成各類型詳細分析...")
        self.create_entity_by_type_analysis(entities, f"{output_dir}/entity_by_type_analysis.png")
        
        print("🏆 生成最常見實體排行榜...")
        self.create_top_entities(entities, top_n=15, save_path=f"{output_dir}/top_entities.png")
        
        # 生成統計報告
        self.generate_statistics_report(entities, f"{output_dir}/statistics_report.txt")
        
        print(f"\n🎉 所有分析圖表已保存至 '{output_dir}' 目錄")
    
    def generate_statistics_report(self, entities: List[Dict[str, Any]], save_path: str):
        """生成統計報告"""
        if not entities:
            return
        
        # 統計分析
        entity_types = [entity['label'] for entity in entities]
        type_counts = Counter(entity_types)
        confidences = [entity['confidence'] for entity in entities]
        
        # 按類型分組統計
        type_stats = {}
        for label in type_counts.keys():
            type_entities = [e for e in entities if e['label'] == label]
            type_confidences = [e['confidence'] for e in type_entities]
            type_stats[label] = {
                'count': len(type_entities),
                'avg_confidence': np.mean(type_confidences),
                'min_confidence': np.min(type_confidences),
                'max_confidence': np.max(type_confidences)
            }
        
        # 生成報告
        report = f"""
NER 分析統計報告
================

總體統計
--------
總實體數: {len(entities)}
平均可信度: {np.mean(confidences):.3f}
最高可信度: {np.max(confidences):.3f}
最低可信度: {np.min(confidences):.3f}

各類型統計
----------
"""
        
        for label, stats in type_stats.items():
            report += f"""
{label}:
  數量: {stats['count']}
  平均可信度: {stats['avg_confidence']:.3f}
  最高可信度: {stats['max_confidence']:.3f}
  最低可信度: {stats['min_confidence']:.3f}
"""
        
        # 最常見實體
        entity_texts = [entity['text'] for entity in entities]
        text_counts = Counter(entity_texts)
        top_entities = text_counts.most_common(10)
        
        report += f"""

最常見實體 (前10名)
------------------
"""
        for i, (text, count) in enumerate(top_entities, 1):
            report += f"{i:2d}. {text} (出現 {count} 次)\n"
        
        # 保存報告
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"統計報告已保存至: {save_path}")

def main():
    """主程式"""
    print("🚀 NER 視覺化分析工具")
    print("=" * 50)
    
    visualizer = NERVisualizer()
    
    # 檢查是否有 CSV 檔案
    csv_file = 'ner_labeled_data.csv'
    if not pd.io.common.file_exists(csv_file):
        print(f"❌ 找不到 {csv_file} 檔案")
        print("請先執行 NER 分析程式生成資料")
        return
    
    # 執行完整分析
    visualizer.create_comprehensive_analysis(csv_file)

if __name__ == "__main__":
    main()
