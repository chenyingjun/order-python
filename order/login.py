
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
import json
import datetime

def loginPage(request):
    next = request.GET.get('next','/main')
    return render(request, 'sign.html', {'next': next})

@login_required
def main(request):
    return render_to_response('main.html', {'nowTime': datetime.datetime.now().ctime()})

def submitLogin(request):
    if request.method == 'POST':
        password = request.POST.get('passWord')
        username = request.POST.get('account')
        ret = {'code': False, 'message': ''}
        # password = make_password(password, None, 'pbkdf2_sha256')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            ret['code'] = True
            return HttpResponse(json.dumps(ret))

        ret['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(ret))
    return render(request, 'sign.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')