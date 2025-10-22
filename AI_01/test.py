from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 檢查 API Key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ 錯誤：未找到 OPENAI_API_KEY 環境變數")
    print("請參考 README.md 設定您的 API Key")
    exit(1)

# 初始化 OpenAI 客戶端
try:
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI 客戶端初始化成功")
except Exception as e:
    print(f"❌ OpenAI 客戶端初始化失敗: {e}")
    exit(1)

def classify_sentiment(texts):
    """
    分類文本的情感
    
    Args:
        texts (list): 要分類的文本列表
        
    Returns:
        list: 包含情感分析結果的列表
    """
    results = []
    
    for text in texts:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # 修正模型名稱
                messages=[{
                    "role": "user",
                    "content": f"""分類以下文本的情感。

只回傳 JSON 格式: {{"sentiment": "正面|負面|中性", "confidence": 0.0-1.0}}

文本: {text}"""
                }],
                temperature=0.1  # 降低隨機性，提高一致性
            )
            
            # 修正回應內容的取得方式
            content = response.choices[0].message.content
            result = json.loads(content)
            results.append(result)
            
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            # 如果 JSON 解析失敗，提供預設結果
            results.append({
                "sentiment": "neutral",
                "confidence": 0.5,
                "error": "JSON 解析失敗"
            })
        except Exception as e:
            print(f"處理文本 '{text}' 時發生錯誤: {e}")
            results.append({
                "sentiment": "neutral", 
                "confidence": 0.0,
                "error": str(e)
            })
    
    return results

def load_texts_from_file(filename):
    """
    從檔案讀取文本
    
    Args:
        filename (str): 檔案路徑
        
    Returns:
        list: 文本列表
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f.readlines() if line.strip()]
        return texts
    except FileNotFoundError:
        print(f"檔案 {filename} 不存在")
        return []
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return []

def main():
    """主程式執行區塊"""
    # 從 demo.txt 讀取文本
    texts = load_texts_from_file("demo.txt")
    
    if not texts:
        print("沒有找到有效的文本，使用預設範例...")
        texts = ["太棒了！", "很失望", "還不錯"]
    
    print(f"開始情感分析... (共 {len(texts)} 個文本)")
    classifications = classify_sentiment(texts)
    
    # 顯示結果
    for i, (text, result) in enumerate(zip(texts, classifications)):
        print(f"\n文本 {i+1}: {text}")
        print(f"情感: {result.get('sentiment', 'unknown')}")
        print(f"信心度: {result.get('confidence', 0):.2f}")
        if 'error' in result:
            print(f"錯誤: {result['error']}")
    
    # 統計結果
    sentiment_counts = {}
    for result in classifications:
        sentiment = result.get('sentiment', 'unknown')
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
    
    print(f"\n=== 統計結果 ===")
    for sentiment, count in sentiment_counts.items():
        print(f"{sentiment}: {count} 個")

if __name__ == "__main__":
    main()