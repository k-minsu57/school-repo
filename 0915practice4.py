sentence = '나는 소년입니다'
print(sentence)

sentence2 = """
나는 소년이고,
파이선은 쉬워요
"""
print(sentence2)

python = "Python is Amazing"

print(python.lower())
print(python.upper())
print(python[0].isupper())
# python의 0번째 (첫번째) 글자가 upper인가?
print(len(python))
print(python.replace("Python", "Sang Wook"))

index = python.index("n")
print(index)
index = python.index("n", index+1)
print(index)

print(python.find("n"))
print(python.find("Java"))
# python에 원하는 값(내용이 없으면(안 찾아지면) -1을 표시)
# print(python.index("Java"))
# python에 원하는 값(내용)이 없으면 오류가 나면서 더이상 실행을 하지 않고 종료됨

# 위에서 종료되었으므로 그 아래 명령들은 실행 안 됨

print(python.count("n"))
# python에 n이 총 몇번 나오는지 세기