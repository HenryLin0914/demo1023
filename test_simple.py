print("Hello, Python!")
print("Testing basic Python execution...")

def even_squares_sum(numbers):
    return sum(x**2 for x in numbers if x % 2 == 0)

# 測試
test = [1, 2, 3, 4, 5, 6]
result = even_squares_sum(test)
print(f"測試結果: {result}")
