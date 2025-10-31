class Student:
    def __init__(self, name, age, location):
        self.name = name
        self.age = age
        self.location = location

    def __str__(self):
        # return f"Name: {self.name}, Age: {self.age}, Location: {self.location}"
        return "name: {0}, Age: {1}, Location: {2}".format(self.name, self.age, self.location)
    
class Classroom:
    def __init__(self, *students_info):
        self.students = []
        for info in students_info:
            self.add_student(*info)

    def add_student(self, name, age, location):
        student = Student(name, age, location)
        self.students.append(student)

    def list_students(self):
        for student in self.students:
            print(student)

print("첫 번째 교실")
# 여러 학생 정보를 넣어 Classroom 인스턴스를 생성합니다.
classroom = Classroom(('이상욱', 47, '서울'), ('홍길동', 16, '부산'), ('김철수', 15, '대구'))
# 학생들의 목록을 출력합니다.
classroom.list_students()

print("두 번째 교실")
# 두 번째 classroom 인스턴스를 생성합니다.
classroom2 = Classroom(('박영희', 17, '인천'), ('최민수', 16, '광주'), ('김철수', 15, '대구'))
# classroom2에 있는 학생들의 목록을 출력합니다.
classroom2.list_students()

# 첫 번재 교실 생성
classroom1 = Classroom()
classroom1.add_student("이상욱", 47, "서울")
classroom1.add_student("홍길동", 16, "부산")

# 두 번째 교실 생성
classroom2 = Classroom()
classroom2.add_student("박영희", 17, "인천")
classroom2.add_student("최민수", 16, "광주")

# 각 교실의 학생 목록 출력
print("- 첫 번째 교실")
classroom1.list_students()

print("\n- 두 번째 교실")
classroom2.list_students()
