import json
from django.shortcuts import render, redirect

# Create your views here.
to_do_list = [

    {"work": "吃饭", "status": "finished"},
    {"work": "跑步", "status": False},
]


def home(request):
    global to_do_list
    if request.method == 'POST':
        if request.POST['添加事项']:
            to_do_list.append({"work": request.POST["添加事项"], "status": False})
            content = {'清单': to_do_list, '信息': '添加成功'}
            return render(request, 'to_do_list/html/homepage.html', content)
        else:
            content = {'清单': to_do_list, '信息': None}
            return render(request, 'to_do_list/html/homepage.html', content)
    elif request.method == 'GET':
        content = {'清单': to_do_list, '信息': 'GET'}
        return render(request, 'to_do_list/html/homepage.html', content)

def edit(request, forloop_counter):
    global to_do_list
    if request.method == 'POST':
        if request.POST["已修改事项"]:
            to_do_list[int(forloop_counter) - 1]['work'] = request.POST["已修改事项"]
            return redirect('to_do_list:主页')
        else:
            return render(request, 'to_do_list/html/edit.html', {"警告": "请输入内容！"})
    elif request.method == 'GET':
        content = {'待修改事项': to_do_list[int(forloop_counter) - 1]['work']}
        return render(request, 'to_do_list/html/edit.html', content)

def about(request):
    return render(request, 'to_do_list/html/about.html')

def delete(request, forloop_counter):
    global to_do_list
    to_do_list.pop(int(forloop_counter) - 1)
    return redirect('to_do_list:主页')

def status(request, forloop_counter):
    global to_do_list
    if request.POST["状态"] == 'finished':
        to_do_list[int(forloop_counter) - 1]['status'] = 'finished'
        return redirect('to_do_list:主页')
    else:
        to_do_list[int(forloop_counter) - 1]['status'] = False
        return redirect('to_do_list:主页')
