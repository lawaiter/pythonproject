from django.urls import path, include
from to_do_list import views

app_name = "to_do_list"
urlpatterns = [
    path('', views.home, name='主页'),
    path('edit/<forloop_counter>', views.edit, name='添加事项'),
    path('about/', views.about, name='关于本站'),
    path('del/<forloop_counter>', views.delete, name='删除'),
    path('status/<forloop_counter>', views.status, name='是否完成')
]
