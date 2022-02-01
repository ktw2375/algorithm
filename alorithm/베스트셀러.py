n = int(input())
bookDic = {}
for _ in range(n):
    book = input()
    if book not in bookDic:
        bookDic[book] = 1
    else:
        bookDic[book] += 1

target = max(bookDic.values())


result = []

for book, number in bookDic.items():
    if number == target:
        result.append(book)

result = sorted(result)
print(result[0])

