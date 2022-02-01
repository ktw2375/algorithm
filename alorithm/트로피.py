n = int(input())
array = []
leftCnt = 0
rightCnt = 0
tmpValue = 0
max = 0
for _ in range(n):
    tropy = int(input())
    array.append(tropy)

#왼쪽
for i in array:
    if max < i:
        leftCnt += 1
        max = i
print(leftCnt)

max = 0 # 초기화

#오른쪽
for i in reversed(array):
    if max < i:
        rightCnt += 1
        max = i
print(rightCnt)