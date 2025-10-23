def even_squares_sum(numbers):
    """
    計算列表中所有偶數的平方和
    
    Args:
        numbers (list): 包含數字的列表
        
    Returns:
        int: 所有偶數的平方和
    """
    return sum(x**2 for x in numbers if x % 2 == 0)


# 測試函數
if __name__ == "__main__":
    # 測試用例
    test_cases = [
        [1, 2, 3, 4, 5, 6],  # 偶數: 2, 4, 6 -> 4 + 16 + 36 = 56
        [1, 3, 5, 7],         # 沒有偶數 -> 0
        [2, 4, 6, 8],         # 全部偶數 -> 4 + 16 + 36 + 64 = 120
        [],                    # 空列表 -> 0
        [0, 1, 2, 3, 4]       # 包含0 -> 0 + 4 + 16 = 20
    ]
    
    for i, test_list in enumerate(test_cases, 1):
        result = even_squares_sum(test_list)
        print(f"測試 {i}: {test_list} -> 偶數平方和: {result}")