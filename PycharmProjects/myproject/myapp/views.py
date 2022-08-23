import pyodbc
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@ csrf_protect
def index(request):
    if request.method == 'POST':  # post方法
        xk1 = request.POST.get('txtXuanke1')
        xk2 = request.POST.get('txtXuanke2')
        xk3 = request.POST.get('txtXuanke3')
        #conn = pyodbc.connect("Provider=Microsoft.ACE.OLEDB.12.0;Data Source=学生管理.accdb")
        conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=.\学生管理.accdb')
        #conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=学生管理.mdb')
        cursor = conn.cursor()  # 用游标方式
        sql = u""" Select * FROM [学生表] where [选课] like '%%'+'%s'+'%%' and [选课] like '%%'+'%s'+'%%'""" % (xk1,xk2)
        cursor.execute(sql)  # 执行SQL查询学生表中的学号=输入的学号的记录
        list = cursor.fetchall()  # 得到查询结果

        if list:  # 查询结果有内容
            return render(request, 'index.html',{'lists': list})
    else:  # get方法
        return render(request, 'index.html')