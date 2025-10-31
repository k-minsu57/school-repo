# print("python", "Java", sep=" , ")
# print("무엇이 더 재미있을까요?")

# print("Python", "Java", "JavaScript", sep=" vs ", end="? ")
# print("무엇이 더 재미있을까요?")

# import sys
# print("Python", "Java", file=sys.stdout)
# print("Python", "Java", file=sys.stderr)

# import sys
# print("Python version:", sys.version)
# print("실행 인자:", sys.argv)

# print("이건 stdout", file=sys.stdout)
# print("이건 stderr", file=sys.stderr)

# # 시험 성적
# scores = {"수학":0, "영어":50, "코딩":100}
# for subject, score in scores.items():
#     # print(subject, score)
#     print(subject.ljust(8), str(score).rjust(4), sep=":")

# # 은행 대기순번표
# # 001, 002, 003, ...
# for num in range(1,21):
#     # print("대기번호 : " + str(num))
#     print("대기번호 : " + str(num).zfill(3))
    

answer = input("아무 값이나 입력하세요: ")
# answer = 10
print(type(answer))
print("입력하신 값은 " + str(answer) + "입니다")