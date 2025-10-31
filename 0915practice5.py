# 리스트
# 지하철 칸별로 10명, 20명, 30명
subway1 = 10
subway2 = 20
subway3 = 30

subway = [10, 20, 30]
print(subway)

subway = ["유재석", "조세호", "박명수"]
print(subway)

# 조세호가 몇 번째 칸에 타고 있는가?
print(subway.index("조세호")) # index는 0, 1, 2로 시작됨

# 하하가 다음 정류장에서 다음 칸에 탐
subway.append("하하")
print(subway)

# 정형돈을 유재석 / 조세호 사이에 태워봄
subway.insert(1, "정형돈")
print(subway)

# 지하철에 있는 #번째 사람을 꺼냄, ()로 둘 경우 한 명씩 맨 뒤에서부터 꺼냄
print(subway.pop(2))
print(subway)

subway.append("유재석")
print(subway) # 다시 유재석이 뒤에 추가됨

cabinet = {3:"유재석", 100:"김태호"}
print(cabinet[3])
print(cabinet[100])

print(cabinet.get(3))

# print(cabinet[5])
print("hi")

cabinet = {"A-3":"유재석", "B-100":"김태호"}
print(cabinet["A-3"])
print(cabinet["B-100"])
# 새손님
print(cabinet)
cabinet["A-3"] = "김종국" # 유재석이 빠지고 김종국이 들어감
cabinet["C-20"] = "조세호"
print(cabinet)