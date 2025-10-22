#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版 NER 實作
只使用 OpenAI API 進行實體識別
"""

import pandas as pd
from openai import OpenAI
import json
import time
import os
from typing import List, Dict, Any

# 載入 .env 檔案
def load_env_file():
    """載入 .env 檔案"""
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# 在程式開始時載入 .env 檔案
load_env_file()

class SimpleNER:
    """簡化版命名實體識別"""
    
    def __init__(self):
        # 從環境變數讀取 API Key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("請設定 OPENAI_API_KEY 環境變數")
        
        self.client = OpenAI(api_key=api_key)
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """使用 OpenAI API 進行實體識別"""
        try:
            prompt = f"""
請從以下文本中識別並提取命名實體，包括：
- 人名（PERSON）：人物名稱
- 地名（LOCATION）：地點、城市、國家
- 組織（ORGANIZATION）：公司、機構
- 日期（DATE）：時間表達式
- 金額（MONEY）：貨幣金額

文本：{text}

請以 JSON 格式返回結果：
{{
    "entities": [
        {{"text": "實體文本", "label": "實體類型", "confidence": 0.95}}
    ]
}}

只返回 JSON，不要其他文字。
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            # 嘗試清理回應內容，移除可能的非 JSON 部分
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            return result.get('entities', [])
            
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            print(f"回應內容: {content[:200]}...")
            return []
        except Exception as e:
            print(f"API 錯誤: {e}")
            return []

def demonstrate_ner_applications():
    """展示 NER 在不同應用場景中的使用"""
    
    ner = SimpleNER()
    
    # 應用場景 1: 新聞提取
    print("📰 應用場景 1: 新聞提取")
    print("=" * 50)
    news_text = "台灣半導體龍頭台積電（TSMC）今日宣布，將在台南科學園區投資新台幣1000億元，興建3奈米製程晶圓廠。董事長劉德音表示，此投資將創造5000個就業機會，預計2025年投產。"
    
    print(f"新聞內容：{news_text}")
    print("\n提取的實體：")
    news_entities = ner.extract_entities(news_text)
    display_entities(news_entities)
    
    time.sleep(2)  # 避免 API 限制
    
    # 應用場景 2: 郵件分類
    print("\n📧 應用場景 2: 郵件分類")
    print("=" * 50)
    email_text = "親愛的張經理，我是ABC公司的業務代表李明，想與您討論下週三（2024年1月15日）的會議安排。我們公司位於台北市信義區，希望能在下午2點與您會面。預算約為新台幣50萬元。"
    
    print(f"郵件內容：{email_text}")
    print("\n提取的實體：")
    email_entities = ner.extract_entities(email_text)
    display_entities(email_entities)
    
    time.sleep(2)
    
    # 應用場景 3: 簡歷解析
    print("\n💼 應用場景 3: 簡歷解析")
    print("=" * 50)
    resume_text = "姓名：陳小華，學歷：台灣大學資訊工程學系（2018-2022），工作經驗：2022年6月至今：Google台灣分公司，軟體工程師，期望薪資：月薪新台幣8萬元"
    
    print(f"簡歷內容：{resume_text}")
    print("\n提取的實體：")
    resume_entities = ner.extract_entities(resume_text)
    display_entities(resume_entities)
    
    time.sleep(2)
    
    # 應用場景 4: 合同分析
    print("\n📝 應用場景 4: 合同分析")
    print("=" * 50)
    contract_text = "甲方：台灣科技股份有限公司，乙方：創新軟體有限公司，簽約日期：2024年1月10日，合約金額：新台幣200萬元，履約期限：2024年12月31日"
    
    print(f"合同內容：{contract_text}")
    print("\n提取的實體：")
    contract_entities = ner.extract_entities(contract_text)
    display_entities(contract_entities)
    
    time.sleep(2)
    
    # 應用場景 5: 醫療記錄
    print("\n🏥 應用場景 5: 醫療記錄")
    print("=" * 50)
    medical_text = "患者：王小明，男，35歲，診斷：高血壓，處方藥物：Amlodipine 5mg，每日一次，下次回診：2024年2月15日，血壓：收縮壓140mmHg，舒張壓90mmHg"
    
    print(f"醫療記錄：{medical_text}")
    print("\n提取的實體：")
    medical_entities = ner.extract_entities(medical_text)
    display_entities(medical_entities)
    
    return {
        'news': news_entities,
        'email': email_entities,
        'resume': resume_entities,
        'contract': contract_entities,
        'medical': medical_entities
    }

def display_entities(entities: List[Dict[str, Any]]):
    """顯示實體結果"""
    if not entities:
        print("  未找到任何實體")
        return
    
    # 按類型分組
    entity_groups = {}
    for entity in entities:
        label = entity.get('label', 'UNKNOWN')
        if label not in entity_groups:
            entity_groups[label] = []
        entity_groups[label].append(entity)
    
    # 顯示結果
    for label, group in entity_groups.items():
        print(f"  {label}:")
        for entity in group:
            confidence = entity.get('confidence', 0)
            print(f"    - {entity['text']} (可信度: {confidence:.2f})")

def batch_process_texts(texts: List[str], batch_size: int = 3) -> pd.DataFrame:
    """批量處理文本並進行實體識別"""
    ner = SimpleNER()
    results = []
    
    print(f"\n🔄 批量處理 {len(texts)} 個文本...")
    print("=" * 50)
    
    for i, text in enumerate(texts):
        print(f"處理文本 {i+1}/{len(texts)}")
        
        try:
            entities = ner.extract_entities(text)
            
            result = {
                'text_id': i,
                'text': text,
                'entities': json.dumps(entities, ensure_ascii=False),
                'entity_count': len(entities),
                'processed': True
            }
            
            results.append(result)
            
            # 顯示提取的實體
            if entities:
                print(f"  找到 {len(entities)} 個實體:")
                for entity in entities:
                    print(f"    - {entity['text']} ({entity['label']})")
            else:
                print("  未找到實體")
            
        except Exception as e:
            print(f"  處理錯誤: {e}")
            results.append({
                'text_id': i,
                'text': text,
                'entities': json.dumps([], ensure_ascii=False),
                'entity_count': 0,
                'processed': False,
                'error': str(e)
            })
        
        # 批次間暫停
        if (i + 1) % batch_size == 0:
            print("  暫停 2 秒...")
            time.sleep(2)
    
    return pd.DataFrame(results)

def analyze_results(df: pd.DataFrame):
    """分析處理結果"""
    print("\n📊 結果分析")
    print("=" * 50)
    
    # 基本統計
    total_texts = len(df)
    processed_texts = df['processed'].sum()
    total_entities = df['entity_count'].sum()
    
    print(f"總文本數: {total_texts}")
    print(f"成功處理: {processed_texts}")
    print(f"總實體數: {total_entities}")
    print(f"平均每文本實體數: {total_entities/processed_texts:.2f}" if processed_texts > 0 else "平均每文本實體數: 0")
    
    # 實體類型統計
    all_entities = []
    for entities_json in df['entities']:
        try:
            entities = json.loads(entities_json)
            all_entities.extend(entities)
        except:
            continue
    
    if all_entities:
        entity_types = [entity.get('label', 'UNKNOWN') for entity in all_entities]
        type_counts = {}
        for entity_type in entity_types:
            type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
        
        print(f"\n實體類型分布:")
        for entity_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {entity_type}: {count}")
        
        # 可信度統計
        confidences = [entity.get('confidence', 0) for entity in all_entities]
        if confidences:
            print(f"\n可信度統計:")
            print(f"  平均可信度: {sum(confidences)/len(confidences):.2f}")
            print(f"  最高可信度: {max(confidences):.2f}")
            print(f"  最低可信度: {min(confidences):.2f}")

def main():
    """主程式"""
    print("🚀 命名實體識別（NER）實作範例")
    print("=" * 60)
    
    # 展示不同應用場景
    all_results = demonstrate_ner_applications()
    
    # 批量處理範例
    print("\n" + "=" * 60)
    print("📋 批量處理範例")
    print("=" * 60)
    
    # 準備測試數據
    test_texts = [
        "台灣半導體龍頭台積電將在台南投資1000億元",
        "張經理，我們下週三在台北市信義區會面",
        "陳小華畢業於台灣大學，現任Google工程師",
        "甲方：台灣科技公司，合約金額200萬元",
        "患者王小明，診斷高血壓，處方Amlodipine"
    ]
    
    # 批量處理
    results_df = batch_process_texts(test_texts)
    
    # 分析結果
    analyze_results(results_df)
    
    # 保存結果
    results_df.to_csv('ner_labeled_data.csv', index=False, encoding='utf-8')
    print(f"\n✅ 結果已保存至 'ner_labeled_data.csv'")
    
    print("\n🎉 NER 實作範例完成！")

if __name__ == "__main__":
    main()
