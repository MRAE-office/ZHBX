import pyodbc    # 使用odbc连接数据库
import datetime  # 使用日期时间
import time      # 使用时间
import json

from django.shortcuts import render,HttpResponseRedirect,Http404,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

DBfile = u"""./图书管理.mdb"""
### 图书预约设置的公共变量开始
global count  # 符合查询结果的记录数
global list  # 在图书表中查询书名、出版时间的结果
global bookName  # 书名
global txtTime  # 出版时间
### 图书预约设置的公共变量结束

#### 图书表信息类开始
class BookInfo(object):
    def __init__(self, count, ISBN, bookName, type, pubTime, number):  ## 用于初始化对象
        self.count = count  # 书的序号
        self.ISBN = ISBN  # 书的ISBN
        self.bookName = bookName  # 书名
        self.type = type  # 类型
        self.pubTime = pubTime  # 出版时间
        self.number = number  # 数量
#### 图书表信息类结束

#### 借阅表信息类开始
class BorrowInfo(object):
    def __init__(self, count, studentNumber, ISBN, pubTime):  ## 用于初始化对象
        self.count = count  # 借阅的编号
        self.studentNumber = studentNumber  # 借阅的人的学号
        self.ISBN = ISBN  # 借阅的ISBN
        self.pubTime = pubTime  # 借阅日期
#### 图书表信息类结束

#### 借阅表排行榜信息类开始
class BorrowListInfo(object):
    def __init__(self, ISBN, count):  ## 用于初始化对象
        self.ISBN = ISBN  # 借阅的ISBN
        self.count = count  # 借阅的编号
#### 图书表排行榜信息类结束

# 申请表单处理
@ csrf_protect
#### 借阅表信息类开始
class BorrowInfo(object):
    def __init__(self,count,studentNumber,ISBN,pubTime):        ## 用于初始化对象
        self.count=count                                        # 借阅的编号
        self.studentNumber=studentNumber                        # 借阅的人的学号
        self.ISBN=ISBN                                          # 借阅的ISBN
        self.pubTime=pubTime                                    # 借阅日期
#### 图书表信息类结束

# Create your views here.

def login(request):
    if request.method == 'POST':  # post方法
        ####以下为第3.4节任务一活动2中获取用户信息
        studentNumber = request.POST.get('txtStudentNumber')  # 获取输入的学号
        password = request.POST.get('txtPassword')  # 获取输入的密码
        ####以上为第3.4节任务一活动2中获取用户信息
        try:
            ####以下为第3.4节任务一活动2中连接数据库
            # 建立一个连接对象，该对象用PYODBC作为连接应用程序和指定的数据库的管道
            conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBfile)
            cursor = conn.cursor()  # 用游标方式
            ####以上为第3.4节任务一活动2中连接数据库

            ####以下为第3.4节任务一活动2中查找数据
            sql=u""" Select * FROM [学生表] where [学号]= '%s' and [密码]='%s'""" % (studentNumber,password)
            print(sql)
            cursor.execute(sql)  # 执行SQL查询学生表中的学号=输入的学号的记录
            list = cursor.fetchone()  # 得到查询结果
            print(list)
            if list:  # 查询结果有内容
                ###同时验证用户名和密码
                # request.session['userID'] = studentNumber
                # return HttpResponseRedirect("/shows")
                # warn = u"登录成功！"
                ###同时验证用户名和密码
                ###获取一条记录的访问方式
                if list[1] == password:
                    request.session['userID'] = studentNumber
                    return HttpResponseRedirect("/showBorrow0")
                else:
                    warn = u"密码错！"
                ###获取一条记录的访问方式
                ### 循环遍历，找查询结果中密码等于输入的密码,跳转到"/show"；查询结果中密码不等于输入的密码，给出"密码错！"的反馈信息
                # for row in list:  # 循环遍历
                #     if row[1] == password:  # 查询结果中密码等于输入的密码
                #         request.session['userID'] = studentNumber  # 设置session
                #         #warn = u"欢迎"+row[2]+"登录图书管理系统！！"
                #         warn = row[2]
                #         print(warn)
                #         return HttpResponseRedirect("/shows")
                #         # conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=图书管理.mdb')
                #         # cursor = conn.cursor()
                #         # sql = u""" Select * FROM [借阅表] where [学号] = '%s'""" % (studentNumber)
                #         # cursor.execute(sql)  # 执行查询SQL语句
                #         # list = cursor.fetchall()  # 得到查询结果（根据用户信息，查询图书借阅信息的结果）
                #         #
                #         # return render(request,'show.html', {'borrow_list': list,'warns':warn})
                #
                #     else:  # 查询结果中密码不等于输入的密码
                #         warn = u"密码错！"  # 给出"密码错！"的反馈信息
            else:  # 数据库查询结果没有内容
                warn = u"用户不存在！请重试"  # 给出"无此用户！"的反馈信息
            ####以上为第3.4节任务一活动2中查找数据
        except:  # 执行有异常时
            warn = u"不能连接数据库！"  # 给出"不能连接数据库！"的反馈信息
        return render(request,'login.html', {'warn': warn, 'user': studentNumber})
    else:  # get方法
        return render(request, 'login.html')
#### 访问"/login"，用户登录界面结束

def showBorrow0(request):
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DBfile)
    userID = request.session.get(u'userID', '没有用户')  # 获取session的值，没有时为'没有用户'
    cursor = conn.cursor()
    sql = u""" Select * FROM [借阅表] where [学号] = '%s'""" % (userID)
    cursor.execute(sql)  # 执行查询SQL语句
    list = cursor.fetchall()  # 得到查询结果（根据用户信息，查询图书借阅信息的结果）
    return render(request,'show.html', {'borrow_list': list})


### 以下为第3.4节任务二活动2查询的内容(支持模糊查询)，第3.4节任务三活动1的预约内容
### 访问"/show"，图书预约界面开始
###功能：主要功能：1、用户输入书名、出版年份，查询相应图书信息；
###                2、用户在列表中选择图书，点击预约， 图书数据表数量减少1，借阅图书表增加1条借阅记录。
def show(request):
    userID = request.session.get(u'userID', '没有用户')  # 获取session的值，没有时为'没有用户'
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DBfile)
    cursor = conn.cursor()
    if request.method == 'POST':  # post方法
        global bookName                                         # 书名
        global txtTime                                          # 出版时间
        global list                                             # 在图书表中查询书名、出版时间的结果
        global count                                            # 符合查询结果的记录数

        if request.POST.get('btnFind'):  # 如果是name值为btnFind的查询按钮。has_key方法在python2中是可以使用的，在python3中删除了。
            #### 以下为第3.4节任务二活动2的内容查询(支持模糊查询)
            bookName = (request.POST.get('txtBookName')).strip()  # 获取输入的书名，去除首尾空格
            txtTime = (request.POST.get('txtTime')).strip()  # 获取输入的出版时间，去除首尾空格
            ### 查询用的SQL语句，根据输入的书名，出版时间查找
            sql = u""" Select * FROM [图书表] where [数量] > 0 """
            if bookName == '':  # 书名为空
                if not txtTime == '':  # 出版时间不为空
                    ### sql=sql + u""" and [出版时间]= '%s'""" %txtTime
                    sql = sql + u""" and [出版时间] like '%%'+ '%s'+ '%%' """ % txtTime
            else:  # 书名不为空
                if txtTime == '':  # 出版时间为空
                    ### sql=sql + u""" and [书名]= '%s'""" %bookName
                    sql = sql + u""" and [书名] like '%%'+'%s'+'%%' """ % bookName
                else:  # 出版时间不为空
                    ### sql=sql + u""" and [书名]= '%s' and [出版时间]= '%s'""" %(bookName,txtTime)
                    sql = sql + u""" and [书名] like '%%'+'%s'+'%%' and [出版时间]= '%s'""" % (bookName, txtTime)
            # sql= u"Select * FROM [图书表] where [数量] > 0  and [书名] like '%三国演义%' and [出版时间]= '1998'"
            cursor.execute(sql)  # 执行查询SQL语句
            print(sql)
            list = cursor.fetchall()  # 得到查询结果（在图书表中查询书名、出版时间的结果）
            # return render_to_response('show.html', {'books': books,'bookname':bookName})
        else:# 如果是name值为btnOrder的预约按钮
            #### 以下为第3.4节任务三活动1的预约内容
            checkbox_list = request.POST.getlist("checkbox")  # 获取用户选择的复选框的列表
            ### 遍历查询结果的第一个复选框到最后一个复选框。用户在列表中选择图书，点击预约， 图书数据表数量减少1，借阅图书表增加1条借阅记录。
            print(request.POST.getlist("checkbox"))#['9787121297335', '008']列表
            print(list)#[('9787121297335', '董伟明', 'Python Web开发实战', '计算机', '2017', 5), ('008', None, 'Python程序设计', '计算机', '2018', 10)]
            #Python的元组与列表类似，不同之处在于元组的元素不能修改。元组使用小括号，列表使用方括号。
            for rowList in list:  # 循环遍历
                ## 遍历在图书表中查询书名、出版时间的结果中选中的图书信息。根据选中的复选框的value值，判断图书信息
                if "%s" % rowList[0] in checkbox_list:  # 获取用户选择的复选框的value值
                    # 用户在列表中选择图书， 图书数据表数量减少1
                    print(rowList[0])
                    sql_update=u""" update [图书表] set [数量]=[数量]-1 where [ISBN]='%s' """ % rowList[0]
                    cursor.execute(sql_update)
                    cursor.commit()
                    date = datetime.datetime.now()  # 当前日期时间
                    dt = "%s-%s-%s" % (date.year, date.month, date.day)  # 当前日期（"年-月-日"格式）
                    # 借阅图书表增加1条借阅记录的SQL语句
                    sql_insert = u""" insert into  [借阅表]([学号],[ISBN],[借阅日期]) VALUES  ('%s','%s','%s')""" % (userID, rowList[0], dt)
                    cursor.execute(sql_insert)  # 执行SQL语句（借阅图书表增加1条借阅记录）
                    cursor.commit()
        count =0                                                # 符合查询结果的记录数
        book_list=[]                                            # 在图书表中查询书名、出版时间的结果，为了传递到页面设计的列表
        ### 将在图书表中查询书名、出版时间的结果，传递到页面的列表中
        for row in list :                                       # 循环遍历
            count=count+1                                       # 符合查询结果的记录数
        if request.POST.get('btnOrder'):  # 如果是name值为btnOrder的预约按钮
            find = u"已执行预约"
        else:  # 如果不是name值为btnOrder的查找按钮。因为就只有2个name，所以就不用if request.POST.has_key('btnFind'):了
                ## 根据输入的书名，出版时间查找，显示共有多少条记录
            if bookName == '':  # 书名为空
                if txtTime == '':  # 出版时间为空
                    find = u""" 用户：%s ,  共有%s 条记录""" % (userID, count)  # 提示信息:用户，记录数
                else:  # 出版时间不为空
                    find = u""" 用户：%s ,  出版时间： %s  ,共有%s 条记录""" % (userID, txtTime, count)  # 提示信息:用户，出版时间，记录数
            else:  # 书名不为空
                if txtTime == '':  # 出版时间为空
                    find = u""" 用户：%s ,  书名： %s    ,共有%s 条记录""" % (userID, bookName, count)  # 提示信息:用户，书名，记录数
                else:  # 出版时间不为空
                    find = u""" 用户：%s ,  书名： %s  ,     出版时间： %s  ,共有%s 条记录""" % (
                    userID, bookName, txtTime, count)  # 提示信息:用户，书名，出版时间，记录数
        return render(request,'show.html', {'find': find, 'books': list})
    else:  # get方法
        return render(request, 'show.html')
### 访问"/show"，图书预约界面结束

### 以下为第3.4节任务二活动1的内容
### 访问"/showBorrow"，查询图书借阅界面开始
###功能：根据用户信息，查询图书借阅信息。
def Borrow(request):
    global listBorrow  # 在图书表中查询书名、出版时间的结果
    userID = request.session.get(u'userID', '没有用户')  # 获取session的值，没有时为'没有用户'
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DBfile)
    cursor = conn.cursor()
    print(request.method)
    if request.method == 'GET':
        userID = request.session.get(u'userID', '没有用户')  # 获取session的值，没有时为'没有用户'
        conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DBfile)
        cursor = conn.cursor()
        sql = u""" Select * FROM [借阅表] where [学号] = '%s'""" % (userID)
        cursor.execute(sql)  # 执行查询SQL语句
        listBorrow = cursor.fetchall()  # 得到查询结果（根据用户信息，查询图书借阅信息的结果）
        print(listBorrow)
        return render(request,'showBorrow.html', {'book_list': listBorrow})

    if request.method == 'POST':
        if request.POST.get('btnCanceleOrder'):  # 如果是name值为btnFind的查询按钮。has_key方法在python2中是可以使用的，在python3中删除了。
            checkbox_list = request.POST.getlist("checkbox")  # 获取用户选择的复选框的列表
            print(request.POST.getlist("checkbox"))#['9787121297335', '008']列表
            print(listBorrow)#[('9787121297335', '董伟明', 'Python Web开发实战', '计算机', '2017', 5), ('008', None, 'Python程序设计', '计算机', '2018', 10)]
            for rowList in listBorrow:  # 循环遍历
                if "%s" % rowList[2] in checkbox_list:  # 获取用户选择的复选框的value值
                    # 用户在列表中选择图书， 图书数据表数量减少1
                    print(rowList[2])
                    sql_update=u""" update [图书表] set [数量]=[数量]+1 where [ISBN]='%s' """ % rowList[2]
                    cursor.execute(sql_update)
                    cursor.commit()
                    date = datetime.datetime.now()  # 当前日期时间
                    dt = "%s-%s-%s" % (date.year, date.month, date.day)  # 当前日期（"年-月-日"格式）
                    # 借阅图书表增加1条借阅记录的SQL语句
                    sql_insert = u""" delete from [借阅表] where [学号]='%s' and [ISBN]='%s'""" % (userID,rowList[2])
                    cursor.execute(sql_insert)  # 执行SQL语句（借阅图书表增加1条借阅记录）
                    cursor.commit()
            CanceleOrder = u"已执行预约"

            return render(request, 'showBorrow.html', {'CanceleOrder': CanceleOrder})


#### 访问"/showBorrow"，查询图书借阅界面结束


#### 以下为第3.3节任务二的内容
#### 访问"/book_insert"，图书信息录入页面开始
####功能：向图书数据库的图书表插入数据
def insertbooks(request):
    if request.method == 'POST':  # post方法

        userID = request.session.get(u'userID', '')  # 获取session的值，没有时为''
        ISBN = request.POST.get('txtISBN')  # 获取输入的ISBN
        bookTitle = request.POST.get('txtBookTitle')  # 获取输入的书名
        BookAuthor=request.POST.get("txtBookAuthor")
        BookNum=request.POST.get('txtBookNum')
        try:
            #### 以下为第3.3节任务二活动1连接图书数据库的内容
            conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBfile)
            cursor = conn.cursor()  # 用游标方式
            #### 以上为第3.3节任务二活动1连接图书数据库的内容

            #### 以下为第3.3节任务二活动2将图书数据插入数据库的内容
            ## sql语句（插入数据），没有检查数据的重复，即原来有此数据，会再插入一遍
            sql = u""" insert into  [图书表]([ISBN],[书名],[数量],[作者]) VALUES  ('%s','%s','%s','%s')""" % (ISBN, bookTitle,BookNum,BookAuthor)
            #sql = u""" insert into  [图书表]([书名],[数量],[作者]) VALUES  ('"""+bookTitle+"""',"""+BookNum+""",'"""+BookAuthor+"""')"""
            #sql = u" insert into  [图书表]([书名],[数量],[作者]) VALUES  ('"+bookTitle+"',"+BookNum+",'"+BookAuthor+"')"
            ##以下语句是错误的写法
            #sql = u""" insert into  [图书表]([书名]) VALUES  ('%s')""" % ('txtBookTitle')
            #sql = u""" insert into  [图书表]([ISBN],[书名],[数量],[作者]) VALUES  (ISBN, bookTitle,BookNum,BookAuthor)"""##insert into  [图书表]([ISBN],[书名],[数量],[作者]) VALUES  (ISBN, bookTitle,BookNum,BookAuthor)
            cursor.execute(sql)  # 执行SQL语句插入数据
            cursor.commit()
            print(sql)
            #### 以上为第3.3节任务二活动2将图书数据插入数据库的内容
            warn = "添加成功"  # 没有给出反馈信息
        except:  # 执行有异常时
            warn = u"数据没有录入数据库！"  # 给出"数据没有录入数据库！"的反馈信息
        print(sql)
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        return render(request,'bookinsert.html', {'warn': warn, 'user': userID})
    else:  # get方法
        return render(request, 'bookinsert.html')
#### 访问"/book_insert"，图书信息录入页面结束

#### 访问"/insertData"，学生信息录入页面开始
####功能：向图书数据库的学生表插入数据
def insertData(request):
    if request.method == 'POST':  # post方法
        studentNumber = request.POST.get('txtStudentNumber')  # 获取输入的学号
        studentName = request.POST.get('txtStudentName')  # 获取输入的姓名
        sex = request.POST.get('txtSex')  # 获取输入的性别
        age = request.POST.get('txtAge')  # 获取输入的年龄
        grade = request.POST.get('txtGrade')  # 获取输入的年级
        txtClass = request.POST.get('txtClass')  # 获取输入的班级

        try:
            # conn = pyodbc.connect('DSN=mdb',autocommit=True)  # 用odbc连接DSN为mdb的数据库，修改后自动提交
            conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBfile)
            cursor = conn.cursor()  # 用游标方式
            cursor = conn.cursor()  # 用游标方式
            ## sql语句（插入数据），没有检查数据的重复，即原来有此数据，会再插入一遍
            sql = u""" insert into  [学生表]([学号],[密码],[姓名],[性别],[年龄],[年级],[班级]) VALUES  ('%s','%s','%s','%s',%d,'%s','%s')""" % (
            studentNumber, studentNumber, studentName, sex, int(age), grade, txtClass)
            cursor.execute(sql)  # 执行SQL语句插入数据
            warn = ""  # 没有给出反馈信息
        except:  # 执行有异常时
            warn = u"数据没有录入数据库！"  # 给出"数据没有录入数据库！"的反馈信息

        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        return render('insertData.html', {'warn': warn, 'user': studentNumber})
    else:  # get方法
        return render(request, 'insertData.html')
#### 访问"/insertData"，学生信息录入页面结束

#### 以下为第3.5节任务一活动2的内容
#### 访问"/showNew"，查询最受欢迎的图书借阅排行榜界面开始
####功能：查询最受欢迎的图书借阅排行榜。
def showNew(request):
    if request.method == 'POST':  # post方法
        global list  # 在借阅表中查询图书借阅信息的结果
        topNumber = request.POST.get('txtTopNumber')  # 获取输入的借阅最多的次数
        #### 如果输入的借阅最多的次数为空,则输入的借阅最多的次数设为10
        if topNumber.strip() == '':  # 输入的借阅最多的次数为空
            topNumber = "10"  # 借阅最多的次数=10

        #### 以下为第3.5节任务一活动2连接图书数据库的内容
        conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DBfile)
        cursor = conn.cursor()  # 用游标方式
        #### 以上为第3.5节任务一活动2连接图书数据库的内容

        #### 以下为第3.5节任务一活动2查询最受欢迎的图书借阅排行榜
        ### 查询用的SQL语句，查询最受欢迎的图书借阅排行榜
        sql = "Select top " + topNumber + u""" [ISBN] ,count(*)  FROM  [借阅表] group by [ISBN] order by [ISBN] DESC"""
        cursor.execute(sql)  # 执行查询SQL语句
        list = cursor.fetchall()  # 得到查询结果（在图书借阅排行榜的结果）
        book_list = []  # 查询图书借阅排行榜信息的结果，为了传递到页面设计的列表
        ### 将在借阅表中查询借阅排行榜的结果，传递到页面的列表中
        for row in list:  # 循环遍历
            book = BorrowListInfo(row[0], row[1])  # 生成图书借阅排行榜信息的book对象
            book_list.append(book)  # 将对象添加到传递到页面设计的列表
        return render('showNew.html', {'book_list': book_list})
    else:  # get方法
        return render(request, 'showNew.html')
#### 访问"/showNew"，查询图书借阅界面结束


#### 以下为第3.5节任务二活动2的内容
#### 访问"/showTime"，查询当前日期
####功能：查询当前日期。
def showTime(request):
    if request.method == 'POST':  # post方法
        userID = request.session.get(u'userID', '没有用户')  # 获取session的值，没有时为'没有用户'
        today = time.strftime('%Y-%m-%d',
        time.localtime(time.time()))  # 显示当前日期时间.如格式为：年-月-日 时:分:秒strftime('%Y-%m-%d %H:%M:%S')

        return render('showTime.html', {'userID': userID, 'today': today})
    else:  # get方法
        userID = request.session.get(u'userID', '没有用户')  # 获取session的值，没有时为'没有用户'
        today = time.strftime('%Y-%m-%d',
        time.localtime(time.time()))  # 显示当前日期时间.如格式为：年-月-日 时:分:秒strftime('%Y-%m-%d %H:%M:%S')
        return render(request, 'showTime.html', {'userID': userID, 'today': today})
#### 访问"/showNew"，查询图书借阅界面结束

