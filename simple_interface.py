from even_squares_sum import even_squares_sum

def calculate_even_squares_sum(numbers):
    """
    計算並顯示偶數平方和的詳細過程
    """
    print(f"📊 計算偶數平方和")
    print(f"   輸入列表: {numbers}")
    
    # 找出偶數
    even_numbers = [x for x in numbers if x % 2 == 0]
    print(f"   偶數: {even_numbers}")
    
    if even_numbers:
        # 計算平方
        squares = [x**2 for x in even_numbers]
        print(f"   偶數平方: {squares}")
        
        # 計算總和
        result = sum(squares)
        print(f"   偶數平方和: {result}")
        
        # 顯示計算過程
        calculation = " + ".join([f"{x}²" for x in even_numbers])
        print(f"   計算過程: {calculation} = {result}")
    else:
        print(f"   沒有偶數，結果為: 0")
    
    print("-" * 50)
    return even_squares_sum(numbers)

def main():
    """
    主程式 - 測試多個案例
    """
    print("=== 偶數平方和計算器 ===\n")
    
    # 預設測試案例
    test_cases = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [2, 4, 6, 8],
        [1, 3, 5, 7, 9],
        [0, 1, 2, 3, 4],
        [10, 20, 30, 40, 50],
        []
    ]
    
    print("🔍 測試多個案例：\n")
    
    for i, numbers in enumerate(test_cases, 1):
        print(f"案例 {i}:")
        calculate_even_squares_sum(numbers)
        print()
    
    # 自定義案例
    print("🎯 自定義案例：")
    custom_numbers = [12, 15, 18, 21, 24, 27, 30]
    calculate_even_squares_sum(custom_numbers)

if __name__ == "__main__":
    main()