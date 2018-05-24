from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class TeacherInfo(models.Model):
    t_number=models.IntegerField()
    t_name=models.CharField(max_length=20)
    t_pwd=models.IntegerField()
    e_mail = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=110, null=True)
    sex = models.CharField(max_length=10, null=True)
    sign = models.CharField(max_length=100, null=True)
    school = models.CharField(max_length=30, null=True)
    major = models.CharField(max_length=20, null=True)
    work = models.CharField(max_length=30, null=True)
    company = models.CharField(max_length=30, null=True)
    position = models.CharField(max_length=30, null=True)
    photo_address = models.CharField(max_length=50, null=True)


class StudentInfo(models.Model):
    s_number = models.IntegerField()
    s_name = models.CharField(max_length=20)
    s_pwd = models.IntegerField()
    s_class=models.CharField(max_length=20)
    e_mail=models.CharField(max_length=100,null=True)
    phone_number=models.CharField(max_length=110,null=True)
    sex=models.CharField(max_length=10,null=True)
    sign=models.CharField(max_length=100,null=True)
    school=models.CharField(max_length=30,null=True)
    major=models.CharField(max_length=20,null=True)
    work=models.CharField(max_length=30,null=True)
    company=models.CharField(max_length=30,null=True)
    position=models.CharField(max_length=30,null=True)
    photo_address=models.CharField(max_length=50,null=True)




class PracticeInfo(models.Model):
    practice_name=models.CharField(max_length=100)
    practice=HTMLField()
    answer=models.CharField(max_length=1000,null=True)
    course_belong=models.CharField(max_length=100)
    up_time=models.DateTimeField()
    adjust_class=models.CharField(max_length=30)
    teacher=models.ForeignKey(TeacherInfo,on_delete=models.CASCADE)

class StudentPractice(models.Model):
    practice_author=models.CharField(max_length=30)
    sub_time=models.DateTimeField()
    author_class=models.CharField(max_length=30)
    s_result=models.CharField(max_length=20)
    teacher_id=models.CharField(max_length=20)
    practice_content=HTMLField()
    practice_name=models.CharField(max_length=20)
    practice_authornumber=models.CharField(max_length=20)
    practice_results=models.CharField(max_length=1000)
    subauthor=models.ForeignKey(StudentInfo,on_delete=models.CASCADE)
class Question(models.Model):
    question_title=models.CharField(max_length=100)
    questions_content=HTMLField()
    attentions_number=models.IntegerField()
    anonymity=models.CharField(max_length=10,null=True)
    author_name=models.CharField(max_length=20)
    sub_time=models.DateTimeField()
    answers_number=models.IntegerField()
    teacher_author=models.ForeignKey(TeacherInfo,on_delete=models.CASCADE,null=True)
    student_author=models.ForeignKey(StudentInfo,on_delete=models.CASCADE,null=True)
class Answer(models.Model):
    s_answer_num=models.ForeignKey(TeacherInfo,on_delete=models.CASCADE,null=True)
    t_answer_num=models.ForeignKey(StudentInfo,on_delete=models.CASCADE,null=True)
    answer_name=models.CharField(max_length=20,null=True)
    answer_time=models.DateTimeField()
    praise_numbers1=models.IntegerField()
    critical_numbers=models.IntegerField()
    answer_content=HTMLField()
    anonymity = models.CharField(max_length=10, null=True)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)

class Attention(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherInfo, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE, null=True)
class TestFiles(models.Model):
    testname=models.CharField(max_length=20)
    author_num=models.ForeignKey(TeacherInfo,on_delete=models.CASCADE)
    sub_time=models.DateTimeField()
    adjust_class=models.CharField(max_length=20)
    saveaddress=models.CharField(max_length=100)
class Enterinfo(models.Model):
    student_name=models.CharField(max_length=20)
    enter_time=models.DateTimeField()
    s_class=models.CharField(max_length=20)
