def even_squares_sum(numbers):
    """
    計算列表中所有偶數的平方和
    
    參數:
        numbers (list): 包含數字的列表
    
    返回:
        int: 所有偶數的平方和
    """
    # 使用列表推導式篩選偶數並計算平方，然後求和
    return sum(x**2 for x in numbers if x % 2 == 0)


# 測試函數
if __name__ == "__main__":
    # 測試用例
    test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = even_squares_sum(test_numbers)
    print(f"測試列表: {test_numbers}")
    print(f"偶數的平方和: {result}")
    
    # 手動驗證: 2² + 4² + 6² + 8² + 10² = 4 + 16 + 36 + 64 + 100 = 220
    print(f"手動驗證: 2² + 4² + 6² + 8² + 10² = {2**2 + 4**2 + 6**2 + 8**2 + 10**2}")