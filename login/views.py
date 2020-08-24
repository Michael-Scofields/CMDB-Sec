from django.shortcuts import render
from django.shortcuts import redirect
from . import models    # Django2.0用 from . import models
from . import forms
import hashlib

# Create your views here.


def index(request):
    pass
    return render(request, 'assets/index.html')


def hash_code(s, salt='Michael'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def login(request):

    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容!'
        message2 = '用户名或密码错误!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            print("[+]U:{} | P:{} | H:{}".format(username, password, hash_code(password)))
            try:
                user = models.Userlogin.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/assets/dashboard/')
                else:
                    return render(request, 'login/login.html', locals())
            except:
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


def register(request):
    pass
    return render(request, 'login/register.html')