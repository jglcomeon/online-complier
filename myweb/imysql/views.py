#coding=utf-8
from django.shortcuts import render,redirect
from django.http import *
from .models import *
from datetime import datetime
from pymysql import *
from operator import itemgetter
from django.db import connection
import traceback
from django.utils import timezone
from django.conf import settings
import os
from django.core.paginator import Paginator
import json
import re
from multiprocessing import Pool
# Create your views here.
def enter(request):
    error_false=0

    return render(request,'enter.html',{'error_false':error_false})


def handle(request):
    error_false=0
    current=0
    uname1 = TeacherInfo.objects.filter(t_name__isnull=False)
    uname2=StudentInfo.objects.filter(s_name__isnull=False)
    u_id=request.POST.get('userid')
    upwd=request.POST.get('pwd')
    for data in uname1:
        if(str(data.t_number)==u_id and str(data.t_pwd)==upwd):
            current=1
            t_id=data.id
            try:
                del request.session['s_num']
                del request.session['t_num']
                del request.session['s_uname']
            except:
                print('error')
            request.session['t_id'] = data.id
            request.session['s_uname'] = data.t_name
            request.session['t_num']=data.t_number
            s_uname=request.session.get('s_uname')
    for data1 in uname2:
        if (str(data1.s_number) == u_id and str(data1.s_pwd) == upwd):
            current= 2
            a=Enterinfo()
            a.s_class=data1.s_class
            a.student_name=data1.s_name
            a.enter_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            a.save()
            s_class=data1.s_class
            try:
                del request.session['t_num']
                del request.session['s_num']
                del request.session['s_uname']
            except:
                print('error')
            request.session['s_uname'] = data1.s_name
            request.session['s_id'] = data1.id
            request.session['s_num']=data1.s_number

            s_uname = request.session.get('s_uname')
    request.session.set_expiry(0)
    if(current==0):
        error_false=1
        return render(request,'enter.html',{'error_false':error_false})
    elif(current==1):
        #return render(request, 'teacher/teacher_index.html',{'s_uname':s_uname})
        return redirect('/thomepage')
    else:
        return redirect('/shomepage')
        #return render(request, 'student/student_index.html', {'s_uname': s_uname})
"""获取学生首页"""
def shomepage(request,index1):
    s_uname=request.session.get('s_uname')
    if index1=='':
        index1=1
    s_uname=request.session.get('s_uname')
    a=Question.objects.all().count()
    b=int(a/5)
    c=a%5
    if c!=0:
        b+=1
    return render(request, 'student/student_index.html', {'s_uname': s_uname,'b':b,'index1':index1})
"""获取教师首页"""
def thomepage(request,index1):
    if index1=='':
        index1=1
    s_uname=request.session.get('s_uname')
    a=Question.objects.all().count()
    b=int(a/5)
    c=a%5
    if c!=0:
        b+=1
    return render(request, 'teacher/teacher_index.html', {'s_uname': s_uname,'b':b,'index1':index1})
def t_practice(request):
    s_uname = request.session.get('s_uname')
    return render(request, 'teacher/t_practice.html', {'s_uname': s_uname})
def t_practice2(request):
    #显示我发布的练习
    t_num = request.session.get('t_num')
    teacher = TeacherInfo.objects.get(t_number=t_num)

    practice=PracticeInfo.objects.filter(teacher_id=teacher.id)
    list=[]
    for data in practice:
        list.append({'practice_name':data.practice_name,'practice':data.practice,'course_belong':data.course_belong,'up_time':data.up_time,'id':data.id,'adjust_class':data.adjust_class})
    return JsonResponse({'data':list})
def add_practice(request):
    s_uname = request.session.get('s_uname')
    return render(request,'teacher/add_practice.html',{'s_uname': s_uname})
def add_handle(request):
    b=PracticeInfo()
    s_uname = request.session.get('s_uname')
    c=TeacherInfo.objects.filter(t_name=s_uname)

    if request.method=='POST':
        b.practice_name=request.POST.get('pname')
        b.practice=request.POST.get('pt')
        b.course_belong=request.POST.get('pc')
        b.adjust_class=request.POST.get('be')
        b.answer=request.POST.get('as')
        b.up_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for id in c:
          b.teacher_id=id.id
    b.save()

    return render(request,'teacher/t_practice.html',{'s_uname':s_uname})
#删除练习
def d_practice(request,id):
    b=PracticeInfo.objects.filter(id=id)
    b.delete()
    return render(request, 'teacher/t_practice.html')
#学生获取练习
def get_practice(request):
    s_uname=request.session.get('s_uname')
    student=StudentInfo.objects.filter(s_name=s_uname)

    #获取操作学生的班级
    s_c=''
    for sc in student:
        s_c=sc.s_class
        s_number=sc.s_number
        request.session['s_number']=sc.s_number
    return render(request,'student/get_practice.html',{'s_uname':s_uname,'s_c':s_c})
def get_handle(request,s_class):
    s_uname = request.session.get('s_uname')
    find_practice=PracticeInfo.objects.filter(adjust_class=s_class)
    student_practice = StudentPractice.objects.filter(practice_author=s_uname)
    list=[]
    state=''
    for data in find_practice:

        for data1 in student_practice:
            #验证是否提交过练习
            if(data1.practice_name==data.practice_name):
                state='已提交'
                break
        else:
            state='未提交'
        list.append({'id':data.id,'practice_name':data.practice_name,'course_belong':data.course_belong,'up_time':data.up_time,'practice':data.practice,'teacher_id':data.teacher_id,'state':state})
    return JsonResponse({'data':list})
"""def sub_practice(request,p_name):
    s_name=request.session.get('s_uname')
    return render(request,'student/sub_practice.html',{'s_name':s_name,'p_name':p_name})"""
def sub_handle(request,p_name,teacher_id,id):
    s_num=request.session.get('s_num')
    t_num=request.session.get('t_num')
    s_uname=request.session.get('s_uname')
    c=PracticeInfo.objects.get(id=id)
    answer=c.answer
    num=0
    if s_num==None:
        a=TeacherInfo.objects.get(t_number=t_num)
    else:
        a=StudentInfo.objects.get(s_number=s_num)
    sc=''
    s_id=0
    s=''
    #for data in a:
    if s_num!=None:
        s_c=a.s_class
        s_id=a.id
        s_nbr=a.s_number
    else:
        s_c='教师'
        s_id = a.id
        s_nbr = a.t_number
    b=StudentPractice()
    try:
        sql = request.GET.get('practice_1')
        for data in re.split(' |\*|,',answer):
            print(data)
            for data1 in re.split(' |\*|,',sql):

                if data==data1:
                    num+=1
        length=len(sql.split(';'))-1
        conn = connect(host='localhost', port=3306, db='IMysql', user='root', passwd='1234', charset='UTF8')
        cs1 = conn.cursor()
        def test(sql):
            cs1.execute(sql+';')
        pool=Pool(length)

        for i in sql.split(';'):
            pool.apply_async(test,(i,))
        pool.close()
        pool.join()
        conn.commit()
        cs1.close()
        conn.close()

    except Exception as e:
        s=str(e)
    else:
        print('运行正确')

    b.practice_author=s_uname
    b.practice_authornumber=s_nbr
    b.author_class=s_c
    b.practice_content = request.GET.get('practice_1')
    b.practice_results=s
    b.sub_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    b.teacher_id=teacher_id
    if(s=='' and num>=2):
        b.s_result='正确'
    else:
        b.s_result='未正确'
    b.practice_name=p_name
    b.subauthor_id=s_id
    b.save()

    #return render(request,'student/get_practice.html',{'s_uname':s_name,'s_c':s_c})
    if s_num==None:
        return  redirect('/t_practice')
    else:
        return  redirect('/get_practice')
def see_result(request):
    s_name = request.session.get('s_uname')
    return render(request, 'student/see_result.html', {'s_name': s_name})
def see_resulthandle(request):
    id=request.session.get('s_number')
    s_num=request.session.get('s_num')
    t_num=request.session.get('t_num')
    if s_num==None:
        a=StudentPractice.objects.filter(practice_authornumber=t_num)
    else:
        a = StudentPractice.objects.filter(practice_authornumber=s_num)
    list=[]
    for data in a:
        list.append({'id':data.id,'practice_author':data.practice_author,'sub_time':data.sub_time,'practice_authornumber':data.practice_authornumber,'author_class':data.author_class,'practice_name':data.practice_name,'s_result':data.s_result})
    return JsonResponse({'data':list})

def results(request,id):
    a=StudentPractice.objects.filter(id=id)
    s_name=request.session.get('s_uname')
    for data in a:
        ids = data.id
        author=data.practice_author
        author_number=data.practice_authornumber
        sub_time=data.sub_time
        author_class=data.author_class
        result=data.s_result
        contents=data.practice_content
        practicename=data.practice_name
        result_info=data.practice_results
    return render(request,'student/results.html',{'ids':ids,'author':author,'author_number':author_number,'sub_time':sub_time,'author_class':author_class,'result':result,'contents':contents,'practicename': practicename,'result_info':result_info,'s_name':s_name})
def sd_practice(request,id):
    b=StudentPractice.objects.get(id=id)
    s_name=request.session.get('s_uname')
    b.delete()
    return render(request, 'student/see_result.html',{'s_name':s_name})

def query_result(request):
    s_uname=request.session.get('s_uname')
    return render(request,'teacher/query_result.html',{'s_uname':s_uname})


def query_resulthandle(request):
    t_id=request.session.get('t_id')
    a = StudentPractice.objects.filter(teacher_id=t_id)
    list = []
    for data in a:
        list.append({'id': data.id, 'practice_author': data.practice_author, 'sub_time': data.sub_time,
                     'practice_authornumber': data.practice_authornumber, 'author_class': data.author_class,
                     'practice_name': data.practice_name, 's_result': data.s_result,
                     })
    return JsonResponse({'data': list})
def t_results(request,id):
    a=StudentPractice.objects.filter(id=id)
    s_uname=request.session.get('s_uname')
    for data in a:
        ids = data.id
        author=data.practice_author
        author_number=data.practice_authornumber
        sub_time=data.sub_time
        author_class=data.author_class
        result=data.s_result
        contents=data.practice_content
        practicename=data.practice_name
        result_info=data.practice_results
    return render(request,'teacher/t_results.html',{'ids':ids,'author':author,'author_number':author_number,'sub_time':sub_time,'author_class':author_class,'result':result,'contents':contents,'practicename': practicename,'result_info':result_info,'s_uname':s_uname})
def td_practice(request,id):
    b=StudentPractice.objects.filter(id=id)
    s_uname=request.session.get('s_uname')
    b.delete()
    return render(request, 'teacher/query_result.html',{'s_uname':s_uname})
def query2(request):
    s_uname=request.session.get('s_uname')
    if(request.method=='POST'):
        practicename=request.POST.get('practicename')
    if(practicename==''):
        return redirect('/query_result')
    else:
        return render(request,'teacher/query_result2.html',{'practicename':practicename,'s_uname':s_uname})
def query_resulthandle2(request,practicename):
    a = StudentPractice.objects.filter(practice_name=practicename)
    list = []
    for data in a:
        list.append({'id': data.id, 'practice_author': data.practice_author, 'sub_time': data.sub_time,
                     'practice_authornumber': data.practice_authornumber, 'author_class': data.author_class,
                     'practice_name': data.practice_name, 's_result': data.s_result,
                     })
    return JsonResponse({'data': list})
def s_question(request):
    s_uname=request.session.get('s_uname')

    return render(request,'student/s_question.html',{'s_uname':s_uname})
def t_question(request):
    s_uname=request.session.get('s_uname')

    return render(request,'teacher/t_question.html',{'s_uname':s_uname})
def s_questionhandle(request):
    a=Question()
    name=request.session.get('s_uname')
    s_id=request.session.get('s_id')
    b=StudentInfo.objects.filter(id=s_id)

    if request.method=='POST':
        a.question_title=request.POST.get('title')
        a.questions_content=request.POST.get('content')
        a.anonymity=request.POST.get('anonymity')
        a.answers_number=0
        a.attentions_number=0
        if(request.POST.get('anonymity')!=None):

            a.author_name = '匿名用户'
        else:
            a.author_name = name
        a.sub_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for data in b:
            a.student_author_id = data.s_number
    a.save()
    return redirect('/shomepage')
def t_questionhandle(request):
    a=Question()

    name=request.session.get('s_uname')
    t_id=request.session.get('t_id')
    b=TeacherInfo.objects.filter(id=t_id)

    if request.method=='POST':
        a.question_title=request.POST.get('title')
        a.questions_content=request.POST.get('content')
        a.anonymity=request.POST.get('anonymity')
        a.answers_number=0
        a.attentions_number=0
        if(request.POST.get('anonymity')!=None):

            a.author_name = '匿名用户'
        else:
            a.author_name = name
        a.sub_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for data in b:
            a.teacher_author_id = data.t_number
    a.save()
    return redirect('/thomepage')
"""获取最热问题"""
def get_question(request,index):
    a=Question.objects.filter()
    if index=='':
        index=1
    list=[]
    for data in a:

        if data.student_author_id==None:
            b = TeacherInfo.objects.get(t_number=data.teacher_author_id)
            icon_address = b.photo_address
            author_id=data.teacher_author_id
        else:
            b = StudentInfo.objects.get(s_number=data.student_author_id)
            icon_address = b.photo_address
            author_id=data.student_author_id
        list.append({'icon_address':icon_address,'id':data.id,'question_title':data.question_title,'questions_content':data.questions_content,'attentions_number':data.attentions_number,'author_name':data.author_name,'sub_time':data.sub_time,'answers_number':data.answers_number,'author_id':author_id})
    b=sorted(list, key=itemgetter('answers_number'),reverse=True)


    #print(p.page(1).question_title)
    return JsonResponse({'data':b[int(index)*5-5:int(index)*5]})

def attention(request,id):
    s_uname = request.session.get('s_uname')
    a=Question.objects.get(id=id)
    s_num=request.session.get('s_num')
    t_num=request.session.get('t_num')
    #s=StudentInfo.objects.filter(s_number=s_num)
    #t=TeacherInfo.objects.filter(t_number=t_num)
    #for data2 in s:
     #   s_num=data2.s_number
    #for data3 in t:
     #   t_num=data3.t_number
    """查询该用户有没有关注过这条提问"""

    c=Attention.objects.filter(question_id=id)
    b=Attention()
    for data1 in c:
        if(data1.student_id==s_num or data1.teacher_id==t_num):
            return render(request, 'student/student_index.html', {'s_uname': s_uname})
    a.attentions_number=a.attentions_number+1
    a.save()
    b.question_id=id
    if(s_num==None):
        b.teacher_id=t_num
        b.save()
        return render(request, 'teacher/teacher_index.html', {'s_uname': s_uname})
    else:
        b.student_id=s_num
        b.save()
        return render(request, 'student/student_index.html', {'s_uname': s_uname})

"""学生获取最新问题"""
def sget_newquestion(request,index1):
    s_uname=request.session.get('s_uname')
    if index1=='':
        index1=1
    s_uname=request.session.get('s_uname')
    a=Question.objects.all().count()
    b=int(a/5)
    c=a%5
    if c!=0:
        b+=1
    return render(request,'student/get_newquestion.html',{'s_uname':s_uname,'b':b,'index1':index1})
def get_newquestionhandle(request,index):
    a = Question.objects.filter()
    list = []
    if index=='':
        index=1
    for data in a:

        if data.student_author_id == None:
            author_id = data.teacher_author_id
            b = TeacherInfo.objects.get(t_number=data.teacher_author_id)
            icon_address = b.photo_address
        else:
            b = StudentInfo.objects.get(s_number=data.student_author_id)
            icon_address = b.photo_address
            author_id = data.student_author_id
        list.append({'icon_address':icon_address,'id': data.id, 'question_title': data.question_title, 'questions_content': data.questions_content,
                     'attentions_number': data.attentions_number, 'author_name': data.author_name,
                     'sub_time': data.sub_time, 'answers_number': data.answers_number, 'author_id': author_id})
    b = sorted(list, key=itemgetter('sub_time'), reverse=True)
    return JsonResponse({'data': b[int(index)*5-5:int(index)*5]})
"""教师获取最新问题"""
def tget_newquestion(request,index1):
    s_uname=request.session.get('s_uname')
    if index1=='':
        index1=1
    s_uname=request.session.get('s_uname')
    a=Question.objects.all().count()
    b=int(a/5)
    c=a%5
    if c!=0:
        b+=1
    return render(request,'teacher/get_newquestion.html',{'s_uname':s_uname,'b':b,'index1':index1})
"""获取回答"""
def getanswers(request,id):
    a=Answer.objects.filter(question_id=id)
    list=[]
    for data in a:
        list.append({'question_id':data.question_id,'id':data.id,'answer_name':data.answer_name,'answer_content':data.answer_content,'answer_time':data.answer_time,'praise_numbers1':data.praise_numbers1,'critical_numbers':data.critical_numbers})
    return JsonResponse({'data':list})
"""x学生获取问题详情"""
def squestiondetail(request,id):
    a=Question.objects.filter(id=id)
    for data in a:
        question_title=data.question_title
        questions_content=data.questions_content
        attentions_number=data.attentions_number
        author_name=data.author_name
        sub_time=data.sub_time
        answers_number=data.answers_number
        id=data.id
        if data.student_author_id == None:
            author_id = data.teacher_author_id
            b = TeacherInfo.objects.get(t_number=data.teacher_author_id)
            icon_address = b.photo_address
        else:
            b = StudentInfo.objects.get(s_number=data.student_author_id)
            icon_address = b.photo_address
            author_id = data.student_author_id
    s_uname=request.session.get('s_uname')

    return render(request,'student/squestiondetail.html',{'icon_address':icon_address,'s_uname':s_uname,'id':id,'question_title':question_title,'questions_content':questions_content,'attentions_number':attentions_number,'author_name':author_name,'sub_time':sub_time,'answers_number':answers_number,'author_id':author_id})
"""学生提问处理"""
def sanswerhandle(request,id):
    s_num=request.session.get('s_num')
    t_num=request.session.get('t_num')
    s_uname=request.session.get('s_uname')
    a=Answer()
    b=Question.objects.get(id=id)
    if request.method=='POST':

        a.t_answer_num_id = t_num
        a.s_answer_num_id = s_num
        a.answer_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        a.praise_numbers1=0
        a.critical_numbers=0
        a.answer_content=request.POST.get('content')
        a.anonymity=request.POST.get('anonymity')
        a.question_id=id

        if(request.POST.get('anonymity')==None):
            a.answer_name=s_uname
        else:
            a.answer_name='匿名'
    a.save()
    b.answers_number+=1
    b.save()
    return redirect('/squestiondetail/'+id+'')

def sattention2(request,id,id1):
    a=Answer.objects.get(id=id)
    a.praise_numbers1+=1
    a.save()
    return redirect('/squestiondetail/' +id1+ '')

def sdislike(request,id,id1):
    a = Answer.objects.get(id=id)
    a.critical_numbers+= 1
    a.save()
    return redirect('/squestiondetail/' +id1+ '')
"""教师获取回答详情"""
def tquestiondetail(request,id):
    a=Question.objects.filter(id=id)
    for data in a:
        question_title=data.question_title
        questions_content=data.questions_content
        attentions_number=data.attentions_number
        author_name=data.author_name
        sub_time=data.sub_time
        answers_number=data.answers_number
        id=data.id
        if data.student_author_id == None:
            author_id = data.teacher_author_id
            b = TeacherInfo.objects.get(t_number=data.teacher_author_id)
            icon_address = b.photo_address
        else:
            b = StudentInfo.objects.get(s_number=data.student_author_id)
            icon_address = b.photo_address
            author_id = data.student_author_id
    s_uname=request.session.get('s_uname')
    return render(request,'teacher/tquestiondetail.html',{'icon_address':icon_address,'s_uname':s_uname,'id':id,'question_title':question_title,'questions_content':questions_content,'attentions_number':attentions_number,'author_name':author_name,'sub_time':sub_time,'answers_number':answers_number,'author_id':author_id})
"""教师提问处理"""
def tanswerhandle(request,id):
    s_num=request.session.get('s_num')
    t_num=request.session.get('t_num')
    s_uname=request.session.get('s_uname')
    a=Answer()
    b=Question.objects.get(id=id)
    if request.method=='POST':

        a.t_answer_num_id = t_num
        a.s_answer_num_id = s_num
        a.answer_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        a.praise_numbers1=0
        a.critical_numbers=0
        a.answer_content=request.POST.get('content')
        a.anonymity=request.POST.get('anonymity')
        a.question_id=id

        if(request.POST.get('anonymity')==None):
            a.answer_name=s_uname
        else:
            a.answer_name='匿名'
    a.save()
    b.answers_number+=1
    b.save()
    return redirect('/tquestiondetail/'+id+'')

def tattention2(request,id,id1):
    a=Answer.objects.get(id=id)
    a.praise_numbers1+=1
    a.save()
    return redirect('/tquestiondetail/' +id1+ '')

def tdislike(request,id,id1):
    a = Answer.objects.get(id=id)
    a.critical_numbers+= 1
    a.save()
    return redirect('/tquestiondetail/' +id1+ '')
"""学生获取关注的问题"""
def sget_attentions(request):
    s_uname=request.session.get('s_uname')
    return render(request,'student/get_attentions.html',{'s_uname':s_uname})
"""获取已关注问题数据"""
def get_attentionshandle(request):
    s_num=request.session.get('s_num')
    t_num=request.session.get('t_num')
    if s_num==None:
        a=Attention.objects.filter(teacher_id=t_num)
    else:
        a=Attention.objects.filter(student_id=s_num)
    list=[]

    for data in a:
        b=Question.objects.get(id=data.question_id)
        if b.student_author_id == None:
            c = TeacherInfo.objects.get(t_number=b.teacher_author_id)
            icon_address = c.photo_address
            author_id = b.teacher_author_id
        else:
            c = StudentInfo.objects.get(s_number=b.student_author_id)
            icon_address = c.photo_address
            author_id = b.student_author_id
        list.append({'icon_address':icon_address,'id': b.id, 'question_title': b.question_title, 'questions_content': b.questions_content,
                     'attentions_number': b.attentions_number, 'author_name': b.author_name,
                     'sub_time': b.sub_time, 'answers_number': b.answers_number, 'author_id': author_id})

    return JsonResponse({'data':list})
"""老师获取关注的问题"""
def tget_attentions(request):
    s_uname=request.session.get('s_uname')
    return render(request,'teacher/get_attentions.html',{'s_uname':s_uname})

"""学生获取已经回答的问题"""
def sget_myanswer(request):
    s_uname=request.session.get('s_uname')
    return render(request,'student/get_myanswer.html',{'s_uname':s_uname})
"""教师获取已回答的问题"""

def tget_myanswer(request):
    s_uname = request.session.get('s_uname')
    return render(request, 'teacher/get_myanswer.html', {'s_uname': s_uname})
"""获取已回答问题数据"""
def get_myanswerhandle(request):
    s_num = request.session.get('s_num')
    t_num = request.session.get('t_num')
    if s_num == None:
        a = Answer.objects.filter(t_answer_num_id=t_num)
    else:
        a = Answer.objects.filter(s_answer_num_id=s_num)
    list = []
    for data in a:
        b = Question.objects.get(id=data.question_id)
        if b.student_author_id == None:
            author_id = b.teacher_author_id
            c = TeacherInfo.objects.get(t_number=b.teacher_author_id)
            icon_address = c.photo_address
        else:
            c = StudentInfo.objects.get(s_number=b.student_author_id)
            icon_address = c.photo_address
            author_id = b.student_author_id
        list.append({'icon_address':icon_address,'id': b.id, 'question_title': b.question_title, 'questions_content': b.questions_content,
                     'attentions_number': b.attentions_number, 'author_name': b.author_name,
                     'sub_time': b.sub_time, 'answers_number': b.answers_number, 'author_id': author_id})

    return JsonResponse({'data': list})
"""学生获取自己的提问"""
def sget_myquestion(request):
    s_uname = request.session.get('s_uname')
    return render(request, 'student/get_myquestion.html', {'s_uname': s_uname})
"""教师获取自己的提问"""
def tget_myquestion(request):
    s_uname = request.session.get('s_uname')
    return render(request, 'teacher/get_myquestion.html', {'s_uname': s_uname})
"""获取自己提问数据"""
def get_myquestionhandle(request):
    s_num = request.session.get('s_num')
    t_num = request.session.get('t_num')
    if s_num == None:
        a = Question.objects.filter(teacher_author_id=t_num)
    else:
        a = Question.objects.filter(student_author_id=s_num)
    list = []
    for data in a:
        b = Question.objects.get(id=data.id)
        if b.student_author_id == None:
            author_id = b.teacher_author_id
            c = TeacherInfo.objects.get(t_number=b.teacher_author_id)
            icon_address = c.photo_address
        else:
            c = StudentInfo.objects.get(s_number=b.student_author_id)
            icon_address = c.photo_address
            author_id = b.student_author_id
        list.append({'icon_address':icon_address,'id': b.id, 'question_title': b.question_title, 'questions_content': b.questions_content,
                     'attentions_number': b.attentions_number, 'author_name': b.author_name,
                     'sub_time': b.sub_time, 'answers_number': b.answers_number, 'author_id': author_id})

    return JsonResponse({'data': list})
"""教师上传题库"""
def uploadFiles(request):
    s_uname=request.session.get('s_uname')
    return render(request,'teacher/uploadfiles.html',{'s_uname':s_uname})
def uploadHandle(request):
    a=TestFiles()

    if request.method=="POST":
        files=request.FILES['file']
        a.author_num_id=request.session.get('t_num')
        a.sub_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        a.adjust_class=request.POST.get('s_class')
        a.testname=files.name
        fname=os.path.join(settings.MEDIA_ROOT,files.name)
        a.saveaddress=fname
        a.save()

        with open('/'+fname,'wb') as file:
            for a in files.chunks():
                file.write(a)

        return redirect('/thomepage')
    else:
        return HttpResponse('ERROR')
def see_testfiles(request):
    s_uname=request.session.get('s_uname')
    t_num=request.session.get('t_num')
    s_num=request.session.get('s_num')
    if t_num==None:
        return render(request, 'student/testfiles.html', {'s_uname': s_uname})
    else:
        return render(request,'teacher/see_testfiles.html',{'s_uname':s_uname})
#教师获取自己上传的题库
def see_testfileshandle(request):

    t_num=request.session.get('t_num')
    s_uname = request.session.get('s_uname')
    a=TestFiles.objects.filter(author_num=t_num)
    list=[]
    for data in a:
        list.append({'saveaddress':data.saveaddress,'id':data.id,'testname':data.testname,'sub_time':data.sub_time,'adjust_class':data.adjust_class,'name':s_uname})

    return JsonResponse({'data':list})
def download(request,adress,name):

    def readFile(filename, chunk_size=512):
        with open('/'+filename, 'rb') as f:
            while True:
                c=open(name,'ab')
                c=f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response=FileResponse(readFile(adress))
    response['Content-Type'] ='application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)
    return response
def td_testfiles(request,id):
    a=TestFiles.objects.get(id=id)
    os.remove('/private'+a.saveaddress)
    a.delete()

    s_uname = request.session.get('s_uname')
    return render(request, 'teacher/see_testfiles.html', {'s_uname': s_uname})
def s_gettestfiles(request):
    s_num=request.session.get('s_num')
    s_uname = request.session.get('s_uname')
    a=StudentInfo.objects.get(s_number=s_num)
    b=TestFiles.objects.filter(adjust_class=a.s_class)
    list = []
    for data in b:
        list.append(
            {'saveaddress': data.saveaddress, 'id': data.id, 'testname': data.testname, 'sub_time': data.sub_time,
             'adjust_class': data.adjust_class, 'name': s_uname})

    return JsonResponse({'data': list})
"""根据题库名查询题库"""
def query_testfiles(request):
    s_num=request.session.get('s_num')
    t_num=request.session.get('t_num')
    s_uname=request.session.get('s_uname')
    if(request.method=='POST'):
        practicename=request.POST.get('practicename')
    if(practicename=='' and s_num==None):
        return redirect('/see_testfiles')
    elif(practicename ==''and(t_num == None or s_num==None)):
        return redirect('/see_testfiles')
    else:
        return render(request, 'student/testfiles2.html', {'practicename': practicename, 's_uname': s_uname})
def query_testfileshandle(request,practicename):
    a =TestFiles.objects.filter(testname=practicename)
    s_uname = request.session.get('s_uname')
    list = []
    for data in a:
        list.append(
            {'saveaddress': data.saveaddress, 'id': data.id, 'testname': data.testname, 'sub_time': data.sub_time,
             'adjust_class': data.adjust_class, 'name': s_uname})
    return JsonResponse({'data': list})
"""查看学生登入日志"""
def senter_info(request):
    s_uname=request.session.get('s_uname')
    return render(request,'teacher/senter_info.html',{'s_uname':s_uname})
def enter_infohandle(request):
    a=Enterinfo.objects.all()
    list=[]
    for data in a:
        list.append({'id':data.id,'student_name':data.student_name,'enter_time':data.enter_time,'s_class':data.s_class})
    return JsonResponse({'data':list})
"""根据姓名查询学生登入记录"""
def query_enterinfo(request):
    s_uname=request.session.get('s_uname')
    if request.method=='POST':
        name=request.POST.get('name')
    if name=='':
        return redirect('/senter_info')
    else:
        return render(request,'teacher/query_enterinfo.html',{'s_uname':s_uname,'name':name})

def query_enterinfohandle(request,name):
    a=Enterinfo.objects.filter(student_name=name)
    list = []
    for data in a:
        list.append(
            {'id': data.id, 'student_name': data.student_name, 'enter_time': data.enter_time, 's_class': data.s_class})
    return JsonResponse({'data': list})

def info(request):
    s_uname=request.session.get('s_uname')
    t_num=request.session.get('t_num')
    s_num=request.session.get('s_num')
    if t_num==None:
        a=StudentInfo.objects.get(s_number=s_num)
        homepage='/shomepage'
    else:
        a=TeacherInfo.objects.get(t_number=t_num)
        homepage = '/thomepage'

    return render(request,'info.html',{'homepage':homepage,'s_uname':s_uname,'company':a.company,'e_mail':a.e_mail,'major':a.major,'phone_number':a.phone_number,'photo_address':a.photo_address,'position':a.position,'school':a.school,'sex':a.sex,'sign':a.sign,'work':a.work})


def infohandle(request):
    s_num=request.session.get('s_num')
    t_num=request.session.get('t_num')

    if s_num==None:
        a=TeacherInfo.objects.get(t_number=t_num)
    else:
        a=StudentInfo.objects.get(s_number=s_num)
    try:
        files=request.FILES['icon']
        fname=os.path.join(settings.MEDIA_ROOT2,files.name)
        a.photo_address = "/static/icon/" + files.name
        with open('/'+fname,'wb') as file:
            for i in files.chunks():
               file.write(i)
    except:
        print('error')
    a.e_mail = request.POST.get('e_mail')

    a.phone_number = request.POST.get('phone_number')
    a.sex = request.POST.get('sex')
    a.sign = request.POST.get('sign')
    a.school = request.POST.get('school')
    a.major = request.POST.get('major')
    a.work = request.POST.get('work')
    a.company = request.POST.get('company')
    a.position = request.POST.get('position')
    a.save()
    return redirect('/info')
def about(request):
    s_uname=request.session.get('s_uname')
    return render(request,'about.html',{'s_uname':s_uname})
def see_practice(request,id):
    s_num=request.session.get('s_num')
    t_num=request.session.get('t_num')
    s_uname = request.session.get('s_uname')
    a=PracticeInfo.objects.get(id=id)
    practice=a.practice
    teacher_id=a.teacher_id
    practice_name=a.practice_name
    print(practice_name)
    up_time=a.up_time
    adjust_class=a.adjust_class
    id=a.id
    course_belong=a.course_belong
    if s_num==None:
        homepage='/thomepage'
    else:
        homepage='/shomepage'
    return render(request,'see_practice.html',{'homepage':homepage,'id':id,'teacher_id':teacher_id,'practice_name':practice_name,'s_uname':s_uname,'practice':practice,'up_time':up_time,'adjust_class':adjust_class,'course_belong':course_belong})

def sqlknowledge(request):
    s_uname=request.session.get('s_uname')
    return render(request,'student/sqlknowledge.html',{'s_uname':s_uname})
