from even_squares_sum import even_squares_sum

def get_user_input():
    """
    獲取用戶輸入的數字列表
    """
    print("=== 偶數平方和計算器 ===")
    print("請輸入數字，用逗號分隔（例如：1,2,3,4,5）")
    print("輸入 'quit' 或 'exit' 退出程式")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\n請輸入數字列表: ").strip()
            
            # 檢查是否要退出
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("感謝使用！再見！")
                break
            
            # 處理空輸入
            if not user_input:
                print("請輸入至少一個數字！")
                continue
            
            # 解析輸入的數字
            numbers_str = user_input.split(',')
            numbers = []
            
            for num_str in numbers_str:
                num_str = num_str.strip()
                if num_str:
                    numbers.append(int(num_str))
            
            if not numbers:
                print("請輸入有效的數字！")
                continue
            
            # 計算並顯示結果
            result = even_squares_sum(numbers)
            even_numbers = [x for x in numbers if x % 2 == 0]
            
            print(f"\n📊 計算結果:")
            print(f"   輸入列表: {numbers}")
            print(f"   偶數: {even_numbers}")
            if even_numbers:
                squares = [x**2 for x in even_numbers]
                print(f"   偶數平方: {squares}")
                print(f"   偶數平方和: {result}")
            else:
                print(f"   沒有偶數，結果為: {result}")
            
            print("-" * 40)
            
        except ValueError:
            print("❌ 錯誤：請輸入有效的數字！")
        except KeyboardInterrupt:
            print("\n\n程式被中斷，再見！")
            break
        except Exception as e:
            print(f"❌ 發生錯誤：{e}")

def demo_mode():
    """
    演示模式 - 顯示一些預設的測試案例
    """
    print("=== 演示模式 ===")
    demo_cases = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [2, 4, 6, 8],
        [1, 3, 5, 7, 9],
        [0, 1, 2, 3, 4],
        [10, 20, 30, 40, 50]
    ]
    
    for i, numbers in enumerate(demo_cases, 1):
        result = even_squares_sum(numbers)
        even_numbers = [x for x in numbers if x % 2 == 0]
        print(f"\n演示案例 {i}:")
        print(f"   輸入: {numbers}")
        print(f"   偶數: {even_numbers}")
        print(f"   結果: {result}")

if __name__ == "__main__":
    print("選擇模式：")
    print("1. 互動輸入模式")
    print("2. 演示模式")
    
    while True:
        try:
            choice = input("\n請選擇模式 (1 或 2): ").strip()
            if choice == "1":
                get_user_input()
                break
            elif choice == "2":
                demo_mode()
                break
            else:
                print("請輸入 1 或 2！")
        except KeyboardInterrupt:
            print("\n\n程式被中斷，再見！")
            break