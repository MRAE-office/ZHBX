"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views#导入 views

urlpatterns = [
    path('', views.login),
    path('showBorrow/', views.Borrow),
    #视图views文件里的Borrow函数
    #访问地址为http://127.0.0.1:8000/showBorrow/
    path('showBorrow0/', views.showBorrow0),
    path('shows/', views.show),
    path('insertbook/', views.insertbooks),  # 在这里添加这一行代码，这是我们上一步编写的视图函数的路由，默认是 / 路径
    path('insertData/', views.insertData),  # 在这里添加这一行代码，这是我们上一步编写的视图函数的路由，默认是 / 路径
    path('showNew/', views.showNew),  # 在这里添加这一行代码，这是我们上一步编写的视图函数的路由，默认是 / 路径
    path('showTime/', views.showTime),  # 这里接受两个参数，一个是用正则表达式表示的键值，这个可以任意起名，只要在访问网页时用它就行了；第二个参数是我们要实现的那个视图函数。
    # 这里接受两个参数，一个是用正则表达式表示的键值，这个可以任意起名，只要在访问网页时用它就行了；第二个参数是我们要实现的那个视图函数。
    #path('admin/', admin.site.urls),
]
