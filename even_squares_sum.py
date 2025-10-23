def even_squares_sum(numbers):
    """
    計算列表中所有偶數的平方和
    
    Args:
        numbers (list): 包含數字的列表
        
    Returns:
        int: 所有偶數的平方和
    """
    # 使用列表推導式篩選偶數並計算平方，然後求和
    return sum(x**2 for x in numbers if x % 2 == 0)


# 測試函數
if __name__ == "__main__":
    # 測試用例
    test_list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    test_list2 = [1, 3, 5, 7, 9]  # 沒有偶數
    test_list3 = [2, 4, 6, 8]     # 全是偶數
    test_list4 = []               # 空列表
    
    print(f"列表 {test_list1} 中偶數的平方和: {even_squares_sum(test_list1)}")
    print(f"列表 {test_list2} 中偶數的平方和: {even_squares_sum(test_list2)}")
    print(f"列表 {test_list3} 中偶數的平方和: {even_squares_sum(test_list3)}")
    print(f"列表 {test_list4} 中偶數的平方和: {even_squares_sum(test_list4)}")
    
    # 手動驗證第一個測試用例
    # 偶數: 2, 4, 6, 8, 10
    # 平方: 4, 16, 36, 64, 100
    # 和: 4 + 16 + 36 + 64 + 100 = 220
    print(f"手動驗證: 2² + 4² + 6² + 8² + 10² = 4 + 16 + 36 + 64 + 100 = 220")