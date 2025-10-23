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
    test_numbers1 = [1, 2, 3, 4, 5, 6]
    test_numbers2 = [2, 4, 6, 8]
    test_numbers3 = [1, 3, 5, 7]
    test_numbers4 = []
    
    print(f"列表 {test_numbers1} 中偶數的平方和: {even_squares_sum(test_numbers1)}")
    print(f"列表 {test_numbers2} 中偶數的平方和: {even_squares_sum(test_numbers2)}")
    print(f"列表 {test_numbers3} 中偶數的平方和: {even_squares_sum(test_numbers3)}")
    print(f"空列表的偶數平方和: {even_squares_sum(test_numbers4)}")
