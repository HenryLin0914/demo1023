from even_squares_sum import even_squares_sum

# 測試更多案例
test_cases = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [2, 4, 6, 8],
    [1, 3, 5, 7, 9],  # 只有奇數
    [0, 1, 2, 3, 4],
    [10, 20, 30, 40, 50],
    []  # 空列表
]

print("=== 偶數平方和函數測試 ===\n")

for i, numbers in enumerate(test_cases, 1):
    result = even_squares_sum(numbers)
    even_numbers = [x for x in numbers if x % 2 == 0]
    print(f"測試案例 {i}:")
    print(f"  輸入列表: {numbers}")
    print(f"  偶數: {even_numbers}")
    print(f"  偶數平方: {[x**2 for x in even_numbers]}")
    print(f"  結果: {result}")
    print("-" * 40)